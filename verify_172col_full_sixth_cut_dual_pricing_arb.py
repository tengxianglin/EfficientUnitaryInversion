"""128-bit Arb pricing verification for unused canonical columns against the 172-column dual."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_172col_full_sixth_cut_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_172col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
SCREEN_PATH = ROOT / "evidence/55probe_172col_full_sixth_cut_dual_pricing_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_172col_full_sixth_cut_dual_pricing_arb_n21.json"
PRECISION_BITS = 128
MAX_CANDIDATES = 10


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def orbit_average_minor(entries, indices):
    group = orbit(indices, 42)
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
    return total / len(group)


def active_low_feature(system, entries, row, fourth_groups):
    if row < 21:
        d = row + 1
        total = arb(0)
        for i in range(42):
            j = (i + d) % 42
            total += entries[i][i] * entries[j][j] - entries[i][j] * entries[j][i]
        return total / 42
    group = fourth_groups[row - 21]
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[int(i)][int(j)] for j in subset] for i in subset]).det()
    return total / len(group)


def main():
    ctx.prec = PRECISION_BITS
    cert_raw, lp_raw, cut_lp_raw, screen_raw = (
        CERT_PATH.read_bytes(), LP_PATH.read_bytes(), CUT_LP_PATH.read_bytes(), SCREEN_PATH.read_bytes()
    )
    cert, lp, cut_lp, screen = [
        json.loads(raw) for raw in (cert_raw, lp_raw, cut_lp_raw, screen_raw)
    ]
    cert_sha, lp_sha, cut_lp_sha, screen_sha = map(sha, (cert_raw, lp_raw, cut_lp_raw, screen_raw))
    if cert.get("status") != "strict_172col_2113row_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("172-column strict dual certificate is incomplete")
    if cert["lp_transcript_sha256"] != lp_sha or screen["lp_transcript_sha256"] != lp_sha:
        raise RuntimeError("dual/LP/pricing transcript hashes disagree")
    sixth_rows_check = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    eighth_rows_check = [tuple(int(x) for x in row) for row in cut_lp["selected_eighth_rows"]]
    sixth_hash_check = sha(json.dumps([list(x) for x in sixth_rows_check], separators=(",", ":")).encode())
    eighth_hash_check = sha(json.dumps([list(x) for x in eighth_rows_check], separators=(",", ":")).encode())
    if sixth_hash_check != lp.get("sixth_rows_sha256") or eighth_hash_check != lp.get("eighth_rows_sha256"):
        raise RuntimeError("current parent LP row inventory differs from the pinned 172-column design")
    if screen["dual_certificate_sha256"] != cert_sha:
        raise RuntimeError("pricing screen does not pin the strict dual")
    if screen["canonical_all_columns_sha256_le_f64"] != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("pricing screen canonical pool hash mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if all_sha != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical pool hash mismatch")
    active_canonical = set(int(x) for x in cert["columns"] if int(x) != 1641)
    if len(active_canonical) != 171:
        raise RuntimeError("unexpected active canonical-column count")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 2106]
    active_eighth = [i for i in active_rows if 2106 <= i < 2113]
    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = [Fraction(1, 41)] * 21 + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }
    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    eighth_rows = [tuple(int(x) for x in row) for row in cut_lp["selected_eighth_rows"]]
    if len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected pinned row inventory")

    candidates = [
        row for row in screen["top_positive_candidates"]
        if int(row["column"]) not in active_canonical
    ][:MAX_CANDIDATES]
    results = []
    for candidate in candidates:
        column = int(candidate["column"])
        couplings = all_columns[column]
        if [float(value) for value in couplings] != candidate["couplings"]:
            raise RuntimeError(f"candidate {column} couplings differ from frozen pool")
        entries = rotation_entries_exact(couplings)
        score = ball(lam)
        for row in active_low:
            score += ball(z[row]) * active_low_feature(system, entries, row, fourth_groups) / ball(low_scales[row])
        for row in active_sixth:
            score += ball(z[row]) * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(Fraction(5, 19721))
        for row in active_eighth:
            score += ball(z[row]) * orbit_average_minor(entries, eighth_rows[row - 2106]) / ball(Fraction(1, 19721))
        lower, upper = score.lower(), score.upper()
        results.append({
            "column": column,
            "float_pricing_score": candidate["float_pricing_score"],
            "arb_pricing_score_interval": str(score),
            "arb_lower_endpoint": str(lower),
            "arb_upper_endpoint": str(upper),
            "strictly_positive": lower > 0,
            "couplings": [float(value) for value in couplings],
        })
        print(f"Arb-priced canonical column {column}: {score}", flush=True)

    positive = [row for row in results if row["strictly_positive"]]
    result = {
        "status": "arb_positive_columns_found" if positive else (
            "no_float_positive_candidates" if not candidates else "float_candidates_not_arb_certified"
        ),
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "pricing_screen_sha256": screen_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "active_dual_rows": len(active_rows),
        "active_canonical_column_count": len(active_canonical),
        "unused_canonical_column_count": len(all_columns) - len(active_canonical),
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive),
        "results": results,
        "scope": (
            "Arb verification of up to ten top binary64-positive unused canonical columns against "
            "the 172-column dual. A strictly positive score invalidates this separator after adding "
            "that column; it does not prove a feasible ensemble."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive),
        "results": results,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
