"""128-bit Arb verification of a complete-sixth-screen counterexample.

The exhaustive binary64 scan found 334 sixth-order D42 orbits with normalized
error >= 1/3 for the exact-rational 152-column candidate. This script checks
the worst reported orbit independently using exact rational probabilities,
exact rational path couplings, and Arb determinants. A strict pass here proves
that this candidate is NOT a complete sixth-order witness; it does not assess
other ensembles or the full physical-family optimum.
"""
import hashlib
import json
from fractions import Fraction

from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from screen_ising_sixth_moments import orbit, target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json"
ESCAPE_CERT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SCREEN_PATH = ROOT / "evidence/candidate_152col_complete_sixth_binary64_n21.json"
OUTPUT_PATH = ROOT / "evidence/candidate_152col_sixth_counterexample_arb_n21.json"
PRECISION_BITS = 128
INDICES = (0, 1, 8, 18, 25, 35)
EXPECTED_ORBIT_INDEX = 30283
CAP = Fraction(1, 3)
SCALE = Fraction(5, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def orbit_average_minor(entries, indices):
    group = orbit(indices, 42)
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
    return total / len(group)


def main():
    ctx.prec = PRECISION_BITS
    candidate_raw = CANDIDATE_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    escape_raw = ESCAPE_CERT_PATH.read_bytes()
    screen_raw = SCREEN_PATH.read_bytes()
    candidate = json.loads(candidate_raw)
    lp = json.loads(lp_raw)
    escape = json.loads(escape_raw)
    screen = json.loads(screen_raw)

    candidate_sha, lp_sha, escape_sha, screen_sha = map(
        sha, (candidate_raw, lp_raw, escape_raw, screen_raw)
    )
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate does not pin its 152-column LP transcript")
    if candidate.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("candidate does not pin the continuous-path Arb certificate")
    if screen.get("candidate_input_sha256") != candidate_sha:
        raise RuntimeError("complete-sixth screen and exact candidate hashes disagree")
    if screen.get("status") != "complete_sixth_binary64_violations_found":
        raise RuntimeError("the pinned full sixth screen does not report violations")
    if screen.get("complete") is not True or screen.get("sixth_orbits") != 63133:
        raise RuntimeError("the pinned sixth screen is not exhaustive")
    if screen.get("violating_orbit_count_at_or_above_one_third") != 334:
        raise RuntimeError("unexpected complete-sixth violation count")
    if screen.get("maximum_orbit_index") != EXPECTED_ORBIT_INDEX:
        raise RuntimeError("worst orbit index does not match the frozen target row")
    if tuple(screen.get("maximum_indices", ())) != INDICES:
        raise RuntimeError("worst orbit representative does not match")

    probabilities = {
        int(row["column"]): Fraction(row["probability"])
        for row in candidate["exact_probabilities"]
    }
    if sum(probabilities.values(), Fraction(0)) != 1:
        raise RuntimeError("exact probabilities do not sum to one")
    if len(probabilities) != candidate.get("support_size") or 1641 not in probabilities:
        raise RuntimeError("unexpected candidate support")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous escape lacks its strict Arb certificate")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(b"".join(
        __import__("numpy").asarray(all_columns, dtype="<f8").tobytes().split()
    )) if False else None
    # Keep the canonical pool pin byte-for-byte identical to the established verifier.
    import numpy as np
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != candidate["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen canonical pool hash/count mismatch")

    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("escape couplings disagree with the Arb certificate")
    if len(escape_couplings) != 42 or escape_couplings[-1] != 0 or any(x <= 0 for x in escape_couplings[:-1]):
        raise RuntimeError("escape input is not a legal positive open path")

    exact_target = target(INDICES)
    if exact_target != SCALE:
        raise RuntimeError(f"unexpected exact sixth target: {exact_target}")

    mixture = arb(0)
    column_terms = []
    for column, probability in sorted(probabilities.items()):
        couplings = escape_couplings if column == 1641 else all_columns[column]
        entries = rotation_entries_exact(couplings)
        feature = orbit_average_minor(entries, INDICES)
        term = ball(probability) * feature
        mixture += term
        column_terms.append({
            "column": column,
            "probability": str(probability),
            "orbit_average_minor_interval": str(feature),
        })

    residual = (mixture - ball(exact_target)) / ball(SCALE)
    absolute_error = abs(residual)
    cap_ball = ball(CAP)
    strict_violation = bool(absolute_error > cap_ball)
    if not strict_violation:
        raise RuntimeError("the selected orbit was not strictly above the 1/3 cap in Arb")

    result = {
        "status": "strict_sixth_order_counterexample_certified",
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "complete_sixth_binary64_screen_sha256": screen_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "candidate_support_size": len(probabilities),
        "exact_probability_sum": "1",
        "orbit_index_in_frozen_D42_enumeration": EXPECTED_ORBIT_INDEX,
        "representative_indices": list(INDICES),
        "orbit_size": len(orbit(INDICES, 42)),
        "exact_target": str(exact_target),
        "normalization_scale": str(SCALE),
        "mixture_moment_interval": str(mixture),
        "normalized_signed_residual_interval": str(residual),
        "normalized_absolute_error_interval": str(absolute_error),
        "one_third_cap": str(cap_ball),
        "strictly_exceeds_one_third": strict_violation,
        "binary64_screen_maximum_normalized_error": screen["maximum_normalized_error"],
        "binary64_screen_violation_count": screen["violating_orbit_count_at_or_above_one_third"],
        "column_terms": column_terms,
        "scope": (
            "A rigorous Arb counterexample for this one exact-rational 51-support mixture: "
            "the D42-orbit-averaged sixth-order row at representative (0,1,8,18,25,35) "
            "has normalized absolute error strictly greater than 1/3. This disproves a "
            "complete-sixth-order cap for this candidate only. It does not imply infeasibility "
            "of other ensembles or of the continuous physical family."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "representative_indices": list(INDICES),
        "orbit_size": result["orbit_size"],
        "normalized_absolute_error_interval": str(absolute_error),
        "strictly_exceeds_one_third": strict_violation,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
