"""Binary64 pricing of unused canonical paths against the 162-column sixth-only dual."""
import hashlib
import json
from fractions import Fraction

import numpy as np

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from joint_low_six_eighth_lp import matrix, orbit_minor

CERT_PATH = ROOT / "evidence/55probe_162col_sixth_only_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_lp_162col_sixth_only_n21.json"
LP162_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_162col_sixth_only_dual_pricing_screen_n21.json"
SIXTH_SCALE = 5 / 19721


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    cert_raw, lp_raw, lp162_raw, cut_raw = (
        CERT_PATH.read_bytes(), LP_PATH.read_bytes(), LP162_PATH.read_bytes(), CUT_LP_PATH.read_bytes()
    )
    cert, lp, lp162, cut_lp = [json.loads(raw) for raw in (cert_raw, lp_raw, lp162_raw, cut_raw)]
    cert_sha, lp_sha, lp162_sha, cut_sha = map(sha, (cert_raw, lp_raw, lp162_raw, cut_raw))
    if cert.get("status") != "strict_162col_2106row_sixth_only_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("sixth-only Arb certificate is incomplete")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("sixth-only certificate does not pin its LP")
    if cert.get("parent_162col_lp_sha256") != lp162_sha or lp.get("parent_162col_lp_sha256") != lp162_sha:
        raise RuntimeError("sixth-only design does not pin its 162-column physical inventory")
    if cert.get("parent_152col_cut_lp_sha256") != cut_sha or lp.get("parent_152col_cut_lp_sha256") != cut_sha:
        raise RuntimeError("sixth-only certificate does not pin the sixth-row inventory")
    if (cert.get("column_count"), cert.get("row_count")) != (162, 2106):
        raise RuntimeError("unexpected sixth-only dual dimensions")
    if (lp.get("columns"), lp.get("rows")) != (162, 2106):
        raise RuntimeError("unexpected sixth-only LP dimensions")
    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    if len(sixth_rows) != 645 or sixth_hash != cert.get("sixth_rows_sha256"):
        raise RuntimeError("sixth-order row inventory hash/count mismatch")

    zq = [Fraction(value) for value in cert["dual_vector_rational"]]
    z = np.asarray([float(value) for value in zq], dtype=np.float64)
    lam = float(Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"]))
    if z.shape != (2106,):
        raise RuntimeError("sixth-only dual vector has wrong dimension")
    active_rows = np.flatnonzero(z)
    active_sixth = [int(i) for i in active_rows if i >= 1461]
    if len(active_rows) != 45 or len(active_sixth) != 45 or any(i < 1461 for i in active_rows):
        raise RuntimeError("sixth-only dual support is not exactly 45 sixth rows")

    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = sha(all_array.tobytes())
    if len(all_columns) != 1641 or all_sha != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical physical pool hash/count mismatch")
    active_canonical = sorted(int(x) for x in cert["columns"] if int(x) != 1641)
    if len(active_canonical) != 161 or len(set(active_canonical)) != 161:
        raise RuntimeError("unexpected active canonical inventory")
    expected_active = sorted(set(lp162["base_columns"]) | set(lp162["added_canonical_columns"]))
    if active_canonical != expected_active:
        raise RuntimeError("sixth-only certificate and 162-column LP inventory disagree")
    active_set = set(active_canonical)
    unused = [j for j in range(len(all_columns)) if j not in active_set]

    scores = np.empty(len(all_columns), dtype=np.float64)
    for column, couplings in enumerate(all_columns):
        rotation = matrix(couplings)
        score = lam
        for row in active_sixth:
            score += z[row] * orbit_minor(rotation, sixth_rows[row - 1461]) / SIXTH_SCALE
        scores[column] = score
        if (column + 1) % 100 == 0:
            print(f"Priced canonical columns {column + 1}/{len(all_columns)}", flush=True)

    active_scores = [scores[column] for column in active_canonical]
    ranked = sorted(((column, float(scores[column])) for column in unused), key=lambda x: x[1], reverse=True)
    positive = [(column, score) for column, score in ranked if score > 0]
    result = {
        "status": "priced_unused_canonical_pool_against_sixth_only_dual",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "parent_162col_lp_sha256": lp162_sha,
        "parent_sixth_row_inventory_sha256": cut_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_column_count": len(all_columns),
        "active_column_count": len(cert["columns"]),
        "active_canonical_columns": active_canonical,
        "unused_column_count": len(unused),
        "active_dual_row_count": len(active_rows),
        "active_sixth_row_count": len(active_sixth),
        "active_pool_max_float_pricing_score": max(active_scores),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": ranked[0][1],
        "top_unused_candidates": [
            {"column": int(column), "float_pricing_score": float(score),
             "couplings": [float(value) for value in all_columns[column]]}
            for column, score in ranked[:50]
        ],
        "top_positive_candidates": [
            {"column": int(column), "float_pricing_score": float(score),
             "couplings": [float(value) for value in all_columns[column]]}
            for column, score in positive[:50]
        ],
        "scope": (
            "Binary64 pricing of all 1,480 unused canonical paths against the exact sixth-only "
            "162-column dual. Positive values are discovery candidates only and require Arb checks. "
            "The dual has support only on sixth-order rows; this pricing is therefore aligned with "
            "the sixth-only minimax theorem, not the mixed-order dual."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "active_sixth_rows": len(active_sixth),
        "unused_column_count": len(unused),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": ranked[0][1],
        "top_positive_candidates": result["top_positive_candidates"][:10],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
