"""128-bit Arb verification of positive pricing scores for unused columns under the 133-column dual."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit
from joint_low_six_eighth_lp import EIGHTH_ROWS
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_133col_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_133col_55probe_n21.json"
SCREEN_PATH = ROOT / "evidence/55probe_133col_dual_pricing_screen_n21.json"
SIXTH_SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_133col_dual_pricing_arb_n21.json"
PRECISION_BITS = 128
MAX_CANDIDATES = 10


def orbit_average_minor(entries, indices):
    from flint import arb_mat
    group = orbit(indices)
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
    return total / len(group)


def active_low_feature(system, entries, row, fourth_groups):
    from flint import arb_mat
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
    cert_raw = CERT_PATH.read_bytes()
    cert_sha = hashlib.sha256(cert_raw).hexdigest()
    cert = json.loads(cert_raw)
    lp_raw = LP_PATH.read_bytes()
    lp = json.loads(lp_raw)
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    if cert["lp_transcript_sha256"] != lp_sha:
        raise RuntimeError("dual certificate and LP transcript hashes disagree")
    if cert["column_count"] != 133 or cert["row_count"] != 1779:
        raise RuntimeError("unexpected 133-column dual-certificate dimensions")

    screen_raw = SCREEN_PATH.read_bytes()
    screen_sha = hashlib.sha256(screen_raw).hexdigest()
    screen = json.loads(screen_raw)
    if screen["dual_certificate_sha256"] != cert_sha:
        raise RuntimeError("pricing screen does not pin the current dual certificate")
    if screen["canonical_all_columns_sha256_le_f64"] != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("pricing screen and LP use different canonical pools")

    all_columns, _, _ = canonical_ensemble()
    active_columns = set(int(value) for value in cert["columns"])
    if len(active_columns) != 133 or len(all_columns) != 1641:
        raise RuntimeError("unexpected canonical pool dimensions")
    index_hash = hashlib.sha256()
    for column in sorted(active_columns):
        index_hash.update(int(column).to_bytes(4, "little", signed=False))
    if index_hash.hexdigest() != cert["canonical_133_column_index_sha256"]:
        raise RuntimeError("133-column dual certificate index hash mismatch")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    lam = Fraction(cert["dual_lambda_before_slack"]) - Fraction(cert["dual_slack_delta"])
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 1772]
    active_eighth = [i for i in active_rows if 1772 <= i < 1779]

    system = FourthMoments(21)
    system.exact_target_check()
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }
    sixth_screen = json.loads(SIXTH_SCREEN_PATH.read_text())["records"]
    sixth_rows = [tuple(record["indices"]) for record in sixth_screen]
    sixth_rows += [tuple(row) for row in lp["sixth_probe_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_full_audit_separator_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_prefix_separator_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_additional_full_audit_separator_rows"]]
    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
    if len(sixth_rows) != 311 or eighth_rows != [tuple(row) for row in EIGHTH_ROWS]:
        raise RuntimeError("55-separator pricing row family mismatch")

    candidates = [
        row for row in screen["top_positive_candidates"]
        if int(row["column"]) not in active_columns
    ][:MAX_CANDIDATES]
    results = []
    for candidate in candidates:
        column = int(candidate["column"])
        couplings = all_columns[column]
        if [float(value) for value in couplings] != candidate["couplings"]:
            raise RuntimeError(f"candidate {column} couplings do not match the frozen canonical pool")
        entries = rotation_entries_exact(couplings)
        score = ball(lam)
        for row in active_low:
            feature = active_low_feature(system, entries, row, fourth_groups)
            scale = Fraction(1, 41) if row < 21 else Fraction(comb(21, 2), comb(42, 4))
            score += ball(z[row]) * feature / ball(scale)
        for row in active_sixth:
            score += ball(z[row]) * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(Fraction(5, 19721))
        for row in active_eighth:
            score += ball(z[row]) * orbit_average_minor(entries, eighth_rows[row - 1772]) / ball(Fraction(1, 19721))
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

    positive = [row for row in results if row["strictly_positive"]]
    result = {
        "status": "arb_positive_columns_found" if positive else (
            "no_float_positive_candidates" if not candidates else "float_candidates_not_arb_certified"
        ),
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "pricing_screen_sha256": screen_sha,
        "canonical_all_columns_sha256_le_f64": screen["canonical_all_columns_sha256_le_f64"],
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive),
        "results": results,
        "scope": (
            "Arb verification of up to ten top binary64-positive candidates among the 1,518 "
            "unused canonical physical path generators. A positive score invalidates the "
            "133-column separator after adding that column; it does not prove an improved ensemble."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"], "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive), "results": results,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
