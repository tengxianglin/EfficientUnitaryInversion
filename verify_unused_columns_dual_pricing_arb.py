"""128-bit Arb certification of positive dual-pricing scores for unused columns."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import arb, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit
from joint_low_six_eighth_lp import EIGHTH_ROWS
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/fifteen_probe_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_with_fifteen_sixth_probes_n21.json"
SCREEN_PATH = ROOT / "evidence/fifteen_probe_dual_pricing_screen_n21.json"
SIXTH_SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/fifteen_probe_dual_pricing_arb_n21.json"
PRECISION_BITS = 128
MAX_CANDIDATES = 10


def orbit_average_minor(entries, indices):
    group = orbit(indices)
    total = arb(0)
    for subset in group:
        from flint import arb_mat
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
    from flint import arb_mat
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
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    if cert["lp_transcript_sha256"] != lp_sha:
        raise RuntimeError("dual certificate and LP transcript hashes disagree")

    screen_raw = SCREEN_PATH.read_bytes()
    screen_sha = hashlib.sha256(screen_raw).hexdigest()
    screen = json.loads(screen_raw)
    if screen["dual_certificate_sha256"] != cert_sha:
        raise RuntimeError("pricing screen does not pin the current dual certificate")
    all_columns, _, probabilities = canonical_ensemble()
    active_columns = set(sorted(probabilities))
    all_column_array = np.asarray(all_columns, dtype="<f8")
    all_columns_sha = hashlib.sha256(all_column_array.tobytes()).hexdigest()
    if screen["canonical_all_columns_sha256_le_f64"] != all_columns_sha:
        raise RuntimeError("canonical physical column pool hash mismatch")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    lam = Fraction(cert["dual_lambda_before_slack"]) - Fraction(cert["dual_slack_delta"])
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 1732]
    active_eighth = [i for i in active_rows if 1732 <= i < 1739]

    system = FourthMoments(21)
    system.exact_target_check()
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }
    sixth_screen = json.loads(SIXTH_SCREEN_PATH.read_text())["records"]
    sixth_rows = [tuple(record["indices"]) for record in sixth_screen]
    sixth_rows += [tuple(row) for row in lp["sixth_probe_rows"]]
    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
    if len(sixth_rows) != 271 or eighth_rows != [tuple(row) for row in EIGHTH_ROWS]:
        raise RuntimeError("pricing row family mismatch")

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
            scale = Fraction(1, 41) if row < 21 else Fraction( comb(21, 2), comb(42, 4))
            score += ball(z[row]) * feature / ball(scale)
        for row in active_sixth:
            feature = orbit_average_minor(entries, sixth_rows[row - 1461])
            score += ball(z[row]) * feature / ball(Fraction(5, 19721))
        for row in active_eighth:
            feature = orbit_average_minor(entries, eighth_rows[row - 1732])
            score += ball(z[row]) * feature / ball(Fraction(1, 19721))
        lower = score.lower()
        upper = score.upper()
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
        "canonical_all_columns_sha256_le_f64": all_columns_sha,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive),
        "results": results,
        "scope": (
            "Arb pricing verification of up to ten top binary64-positive columns "
            "among the 1,556 unused canonical physical path generators. A positive "
            "score invalidates the 83-column dual separator for the expanded pool; "
            "it does not by itself prove an improved ensemble."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive),
        "results": results,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
