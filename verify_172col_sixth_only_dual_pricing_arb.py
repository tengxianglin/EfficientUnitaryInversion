"""128-bit Arb checks of the top unused canonical columns against the 172-column sixth-only dual."""
import hashlib
import json
from fractions import Fraction

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from screen_ising_sixth_moments import orbit
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_172col_sixth_only_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_lp_172col_sixth_only_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
SCREEN_PATH = ROOT / "evidence/55probe_172col_sixth_only_dual_pricing_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_172col_sixth_only_dual_pricing_arb_n21.json"
PRECISION_BITS = 128
MAX_CANDIDATES = 10
SIXTH_SCALE = Fraction(5, 19721)


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
    raw = [
        CERT_PATH.read_bytes(),
        LP_PATH.read_bytes(),
        PARENT_LP_PATH.read_bytes(),
        CUT_LP_PATH.read_bytes(),
        SCREEN_PATH.read_bytes(),
    ]
    cert, lp, parent_lp, cut_lp, screen = [json.loads(value) for value in raw]
    cert_sha, lp_sha, parent_lp_sha, cut_sha, screen_sha = map(sha, raw)

    if cert.get("status") != "strict_172col_2106row_sixth_only_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("172-column sixth-only Arb certificate is incomplete")
    if cert.get("lp_transcript_sha256") != lp_sha or screen.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("172-column certificate, LP, and pricing-screen hashes disagree")
    if cert.get("parent_162col_lp_sha256") != parent_lp_sha or lp.get("parent_162col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("172-column parent LP hash mismatch")
    if cert.get("parent_sixth_row_inventory_sha256") != cut_sha or lp.get("parent_sixth_row_inventory_sha256") != cut_sha:
        raise RuntimeError("sixth-row inventory parent hash mismatch")
    if screen.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("pricing screen does not pin the exact 172-column dual")
    if screen.get("parent_162col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("pricing screen does not pin the 162-column parent LP")
    if screen.get("parent_sixth_row_inventory_sha256") != cut_sha:
        raise RuntimeError("pricing screen does not pin the sixth-row inventory")
    if (cert.get("column_count"), cert.get("row_count")) != (172, 2106):
        raise RuntimeError("unexpected 172-column certificate dimensions")
    if (lp.get("columns"), lp.get("rows")) != (172, 2106):
        raise RuntimeError("unexpected 172-column LP dimensions")
    if parent_lp.get("columns") != 162 or parent_lp.get("rows") != 2113:
        raise RuntimeError("unexpected parent 162-column LP dimensions")

    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    if len(sixth_rows) != 645 or len(set(sixth_rows)) != 645 or sixth_hash != lp.get("sixth_rows_sha256"):
        raise RuntimeError("unexpected sixth-order cut inventory")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(z) != 2106:
        raise RuntimeError("172-column dual vector has wrong dimension")
    active_rows = [i for i, value in enumerate(z) if value]
    active_sixth = [i for i in active_rows if i >= 1461]
    if len(active_rows) != 50 or len(active_sixth) != 50:
        raise RuntimeError("172-column dual support is not exactly 50 sixth-order rows")
    norm = sum((abs(value) for value in z), Fraction(0))
    if norm > 1 or norm != Fraction(cert["dual_l1_norm_exact"]):
        raise RuntimeError("exact 172-column dual L1 norm mismatch")
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != cert.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical pool hash/count mismatch")
    if screen.get("canonical_all_columns_sha256_le_f64") != all_sha:
        raise RuntimeError("pricing screen canonical pool hash mismatch")
    active_canonical = set(int(x) for x in cert["columns"] if int(x) != 1641)
    if len(active_canonical) != 171 or set(screen.get("active_canonical_columns", [])) != active_canonical:
        raise RuntimeError("pricing screen active-column inventory mismatch")
    if screen.get("unused_column_count") != 1470:
        raise RuntimeError("pricing screen did not cover all 1,470 unused canonical columns")

    candidates = [
        item for item in screen.get("top_positive_candidates", [])
        if int(item["column"]) not in active_canonical
    ][:MAX_CANDIDATES]
    results = []
    for item in candidates:
        column = int(item["column"])
        couplings = all_columns[column]
        if [float(value) for value in couplings] != item["couplings"]:
            raise RuntimeError(f"candidate {column} differs from the frozen canonical pool")
        entries = rotation_entries_exact(couplings)
        score = ball(lam)
        for row in active_sixth:
            score += ball(z[row]) * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(SIXTH_SCALE)
        lower, upper = score.lower(), score.upper()
        results.append({
            "column": column,
            "float_pricing_score": item["float_pricing_score"],
            "arb_pricing_score_interval": str(score),
            "arb_lower_endpoint": str(lower),
            "arb_upper_endpoint": str(upper),
            "strictly_positive": lower > 0,
            "couplings": [float(value) for value in couplings],
        })
        print(f"Arb-priced canonical column {column}: {score}", flush=True)

    positive = [item for item in results if item["strictly_positive"]]
    result = {
        "status": "arb_positive_columns_found" if positive else (
            "no_float_positive_candidates" if not candidates else "float_candidates_not_arb_certified"
        ),
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "parent_162col_lp_sha256": parent_lp_sha,
        "parent_sixth_row_inventory_sha256": cut_sha,
        "pricing_screen_sha256": screen_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "active_dual_rows": len(active_rows),
        "active_sixth_dual_rows": len(active_sixth),
        "active_canonical_column_count": len(active_canonical),
        "unused_canonical_column_count": len(all_columns) - len(active_canonical),
        "float_positive_candidate_count": screen.get("unused_positive_pricing_count"),
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(positive),
        "results": results,
        "scope": (
            "128-bit Arb checks of up to ten top binary64-positive unused canonical columns against "
            "the exact sixth-only 172-column dual. A strictly positive score invalidates this separator "
            "after adding that column; it does not prove a feasible ensemble. If none of the checked "
            "candidates is positive, this is not a global certificate for all unused columns."
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
