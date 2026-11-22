"""128-bit Arb counterexample to extending the 151-column dual over all positive path couplings.

The candidate is an exact rational 42-site path generator.  The verifier reuses
the pinned 1,779-row design and the exact rational 151-column dual, then
certifies that its pricing score lambda - delta + z^T a(c) is strictly
positive.  This refutes only the proposed *global extension of this dual*;
it does not refute the finite 1,641-column theorem or prove feasibility of the
full continuous-family minimax problem.
"""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit
from joint_low_six_eighth_lp import EIGHTH_ROWS
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
from verify_55probe_151col_full_canonical_pool_arb import (
    active_low_feature,
    orbit_average_minor,
)

CERT_PATH = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_151col_55probe_n21.json"
SCREEN_PATH = ROOT / "evidence/55probe_151col_dual_pricing_screen_n21.json"
SIXTH_SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
PRECISION_BITS = 128

# Discovery found a near signed-permutation regime.  The final witness is
# rational: c_j = 1/1000 when m_j=0 and c_j = 3927*m_j/5000 otherwise.
MULTIPLIERS = [
    6, 0, 14, 0, 0, 26, 0, 10, 0, 32, 0, 18, 0, 34, 0, 30, 2, 6, 0, 7, 23,
    0, 28, 0, 10, 0, 32, 0, 20, 2, 4, 1, 32, 0, 68, 0, 2, 0, 26, 0, 30,
]
COUPLINGS = [
    Fraction(1, 1000) if m == 0 else Fraction(3927 * m, 5000)
    for m in MULTIPLIERS
] + [Fraction(0)]
CANDIDATE_SHA256 = hashlib.sha256(
    json.dumps([str(x) for x in COUPLINGS], separators=(",", ":")).encode()
).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    cert_raw = CERT_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    screen_raw = SCREEN_PATH.read_bytes()
    cert = json.loads(cert_raw)
    lp = json.loads(lp_raw)
    screen = json.loads(screen_raw)
    cert_sha = hashlib.sha256(cert_raw).hexdigest()
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    screen_sha = hashlib.sha256(screen_raw).hexdigest()

    if cert.get("status") != "strict_pool_separation" or not cert.get("complete"):
        raise RuntimeError("the pinned 151-column dual certificate is incomplete")
    if cert["column_count"] != 151 or cert["row_count"] != 1779:
        raise RuntimeError("unexpected dual dimensions")
    if cert["lp_transcript_sha256"] != lp_sha:
        raise RuntimeError("dual certificate does not pin the 151-column LP")
    if screen.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("pricing screen does not pin the dual certificate")
    if screen.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("pricing screen does not pin the LP transcript")
    if len(COUPLINGS) != 42 or COUPLINGS[-1] != 0:
        raise RuntimeError("candidate must be a 42-site open path")
    if any(x <= 0 for x in COUPLINGS[:-1]):
        raise RuntimeError("all 41 path-edge magnitudes must be strictly positive")

    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = hashlib.sha256(all_array.tobytes()).hexdigest()
    if len(all_columns) != 1641 or all_sha != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen 1,641-column pool hash/count mismatch")
    if any(list(column) == COUPLINGS for column in all_columns):
        raise RuntimeError("the proposed escape is already in the frozen canonical pool")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(z) != 1779:
        raise RuntimeError("unexpected dual-vector length")
    if sum((abs(value) for value in z), Fraction(0)) != 1:
        raise RuntimeError("the exact dual L1 norm is not one")
    lam = Fraction(cert["dual_lambda_before_slack"]) - Fraction(cert["dual_slack_delta"])
    z_arb = [ball(value) for value in z]

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    screen_rows = json.loads(SIXTH_SCREEN_PATH.read_text())["records"]
    if len(screen_rows) != 256:
        raise RuntimeError("unexpected frozen sixth-screen row count")
    sixth_rows = [tuple(row["indices"]) for row in screen_rows]
    sixth_rows += [tuple(row) for row in lp["sixth_probe_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_full_audit_separator_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_prefix_separator_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_additional_full_audit_separator_rows"]]
    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
    if len(sixth_rows) != 311 or eighth_rows != [tuple(row) for row in EIGHTH_ROWS]:
        raise RuntimeError("pinned 55-separator row inventory mismatch")
    if len(low_scales) + len(sixth_rows) + len(eighth_rows) != len(z):
        raise RuntimeError("feature and dual dimensions disagree")

    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 1772]
    active_eighth = [i for i in active_rows if 1772 <= i < 1779]
    if (len(active_low), len(active_sixth), len(active_eighth)) != (19, 28, 5):
        raise RuntimeError("unexpected active dual-row block counts")
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }

    entries = rotation_entries_exact(COUPLINGS)
    score = ball(lam)
    contributions = []
    for row in active_low:
        feature = active_low_feature(system, entries, row, fourth_groups)
        contribution = z_arb[row] * feature / ball(low_scales[row])
        score += contribution
        contributions.append({"row": row, "block": "low", "contribution": str(contribution)})
    for row in active_sixth:
        feature = orbit_average_minor(entries, sixth_rows[row - 1461])
        contribution = z_arb[row] * feature / ball(Fraction(5, 19721))
        score += contribution
        contributions.append({"row": row, "block": "sixth", "contribution": str(contribution)})
    for row in active_eighth:
        feature = orbit_average_minor(entries, eighth_rows[row - 1772])
        contribution = z_arb[row] * feature / ball(Fraction(1, 19721))
        score += contribution
        contributions.append({"row": row, "block": "eighth", "contribution": str(contribution)})

    lower, upper = score.lower(), score.upper()
    strict_positive = bool(lower > 0)
    result = {
        "status": "certified_continuous_path_dual_escape" if strict_positive else "candidate_not_certified_positive",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "pricing_screen_sha256": screen_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_pool_size": len(all_columns),
        "candidate_outside_frozen_pool": True,
        "candidate_sha256": CANDIDATE_SHA256,
        "candidate_multipliers": MULTIPLIERS,
        "candidate_rule": "c_j=1/1000 if m_j=0, otherwise c_j=3927*m_j/5000, for j=0..40; c_41=0",
        "candidate_couplings_exact": [str(x) for x in COUPLINGS],
        "all_41_edge_magnitudes_strictly_positive": True,
        "dual_l1_norm_exact": "1",
        "dual_lambda_minus_slack_exact": str(lam),
        "active_dual_rows": {"low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)},
        "pricing_score_interval": str(score),
        "pricing_score_lower_endpoint": str(lower),
        "pricing_score_upper_endpoint": str(upper),
        "strictly_positive": strict_positive,
        "row_contributions": contributions,
        "scope": (
            "A strictly positive score is a rigorous counterexample to extending this exact "
            "151-column dual separator over the full continuous positive-coupling path family. "
            "It does not invalidate the finite 1,641-column canonical-pool theorem, does not "
            "prove a full-family feasible ensemble, and does not settle the full-family minimax optimum."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_sha256": CANDIDATE_SHA256,
        "precision_bits": ctx.prec,
        "pricing_score_interval": str(score),
        "strictly_positive": strict_positive,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)
    if not strict_positive:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
