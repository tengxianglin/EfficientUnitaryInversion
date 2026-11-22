"""Binary64 pricing of unused canonical paths against the certified 182-column mixed-order dual."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from joint_low_six_eighth_lp import matrix, orbit_minor

CERT_PATH = ROOT / "evidence/55probe_182col_sixth_only_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_lp_182col_sixth_only_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_lp_172col_sixth_only_n21.json"
PARENT_DUAL_PATH = ROOT / "evidence/55probe_172col_sixth_only_dual_certificate_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_182col_mixed_order_dual_pricing_screen_n21.json"
SIXTH_SCALE = 5 / 19721


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    raw = [
        CERT_PATH.read_bytes(), LP_PATH.read_bytes(), PARENT_LP_PATH.read_bytes(),
        PARENT_DUAL_PATH.read_bytes(), CUT_LP_PATH.read_bytes(),
    ]
    cert, lp, parent_lp, parent_dual, cut_lp = [json.loads(value) for value in raw]
    cert_sha, lp_sha, parent_lp_sha, parent_dual_sha, cut_sha = map(sha, raw)

    if cert.get("status") != "strict_182col_2106row_mixed_order_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("182-column mixed-order Arb certificate is incomplete")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("182-column certificate does not pin its LP")
    if cert.get("parent_172col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("182-column certificate does not pin its 172-column parent")
    if cert.get("parent_172col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("182-column certificate does not pin the 172-column dual")
    if lp.get("parent_172col_lp_sha256") != parent_lp_sha or lp.get("parent_172col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("182-column LP parent provenance mismatch")
    if cert.get("parent_sixth_row_inventory_sha256") != cut_sha or lp.get("parent_sixth_row_inventory_sha256") != cut_sha:
        raise RuntimeError("182-column certificate does not pin the sixth-row inventory")
    if parent_dual.get("status") != "strict_172col_2106row_sixth_only_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("172-column parent certificate is incomplete")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("172-column parent certificate does not pin its LP")
    if (cert.get("column_count"), cert.get("row_count")) != (182, 2106):
        raise RuntimeError("unexpected 182-column certificate dimensions")
    if (lp.get("columns"), lp.get("rows")) != (182, 2106):
        raise RuntimeError("unexpected 182-column LP dimensions")

    zq = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(zq) != 2106 or sum((abs(value) for value in zq), Fraction(0)) != 1:
        raise RuntimeError("182-column exact dual vector or L1 norm mismatch")
    active_rows = [i for i, value in enumerate(zq) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if i >= 1461]
    if len(active_low) != 2 or len(active_sixth) != 50:
        raise RuntimeError("182-column certificate support no longer matches its mixed-order scope")

    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    if len(sixth_rows) != 645 or sixth_hash != lp.get("sixth_rows_sha256"):
        raise RuntimeError("sixth-order row inventory hash/count mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = sha(all_array.tobytes())
    if len(all_columns) != 1641 or all_sha != cert.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical physical pool hash/count mismatch")
    active_canonical = sorted(int(x) for x in cert["columns"] if int(x) != 1641)
    if len(active_canonical) != 181 or len(set(active_canonical)) != 181:
        raise RuntimeError("unexpected active canonical inventory")
    expected_active = sorted(
        set(cert["base_columns"])
        | set(cert["previous_added_canonical_columns"])
        | set(cert["added_canonical_columns"])
    )
    if active_canonical != expected_active:
        raise RuntimeError("182-column certificate and LP canonical inventory disagree")
    if cert.get("columns") != lp.get("column_order"):
        raise RuntimeError("certificate and LP physical column order mismatch")
    active_set = set(active_canonical)
    unused = [j for j in range(len(all_columns)) if j not in active_set]
    if len(unused) != 1460:
        raise RuntimeError("expected exactly 1,460 unused canonical columns")

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]
    z = np.asarray([float(value) for value in zq], dtype=np.float64)
    lam = float(Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"]))
    active_low_np = np.asarray(active_low, dtype=int)
    active_sixth_np = np.asarray(active_sixth, dtype=int)

    scores = np.empty(len(all_columns), dtype=np.float64)
    for column, couplings in enumerate(all_columns):
        rotation = matrix(couplings)
        low_features = system.features(np.asarray(couplings, dtype=np.float64))
        score = lam
        if len(active_low_np):
            score += float(np.dot(z[active_low_np], low_features[active_low_np] / low_scales[active_low_np]))
        for row in active_sixth_np:
            score += z[row] * orbit_minor(rotation, sixth_rows[row - 1461]) / SIXTH_SCALE
        scores[column] = score
        if (column + 1) % 100 == 0:
            print(f"Priced canonical columns {column + 1}/{len(all_columns)}", flush=True)

    active_scores = [scores[column] for column in active_canonical]
    ranked = sorted(((column, float(scores[column])) for column in unused), key=lambda x: x[1], reverse=True)
    positive = [(column, score) for column, score in ranked if score > 0]
    result = {
        "status": "priced_unused_canonical_pool_against_182col_mixed_order_dual",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "parent_172col_lp_sha256": parent_lp_sha,
        "parent_172col_dual_certificate_sha256": parent_dual_sha,
        "parent_sixth_row_inventory_sha256": cut_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_column_count": len(all_columns),
        "active_column_count": len(cert["columns"]),
        "active_canonical_columns": active_canonical,
        "unused_column_count": len(unused),
        "active_dual_row_count": len(active_rows),
        "active_low_dual_rows": active_low,
        "active_sixth_dual_rows": active_sixth,
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
            "Binary64 pricing of all 1,460 unused canonical paths against the exact rational 182-column "
            "mixed-order dual. The score includes its two low-order and fifty sixth-order coordinates. "
            "Positive values are discovery candidates only and require Arb checks. Nonpositive binary64 "
            "scores do not certify exclusion."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "active_low_rows": len(active_low),
        "active_sixth_rows": len(active_sixth),
        "unused_column_count": len(unused),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": ranked[0][1],
        "top_positive_candidates": result["top_positive_candidates"][:10],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
