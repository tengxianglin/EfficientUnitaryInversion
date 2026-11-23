"""Binary64 pricing of unused canonical paths against the refreshed 183-column Arb dual."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from joint_low_six_eighth_lp import matrix, orbit_minor

CERT_PATH = ROOT / "evidence/55probe_183col_full_sixth_cut_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_183col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_183col_full_sixth_cut_dual_pricing_screen_n21.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def active_low_feature(system, rotation, row, fourth_groups):
    if row < 21:
        d = row + 1
        indices = np.arange(42)
        diagonal = rotation.diagonal()
        return float(np.mean(
            diagonal * diagonal[(indices + d) % 42]
            - rotation[indices, (indices + d) % 42]
            * rotation[(indices + d) % 42, indices]
        ))
    group = fourth_groups[row - 21]
    values = np.linalg.det(rotation[group[:, :, None], group[:, None, :]])
    return float(np.mean(values))


def main():
    cert_raw, lp_raw, cut_lp_raw = CERT_PATH.read_bytes(), LP_PATH.read_bytes(), CUT_LP_PATH.read_bytes()
    cert, lp, cut_lp = [json.loads(raw) for raw in (cert_raw, lp_raw, cut_lp_raw)]
    cert_sha, lp_sha, cut_lp_sha = map(sha, (cert_raw, lp_raw, cut_lp_raw))
    if cert.get("status") != "strict_183col_2113row_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("the 183-column Arb dual certificate is incomplete")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("183-column dual and LP transcript hashes disagree")
    if lp.get("current_152col_cut_lp_sha256") != cut_lp_sha:
        raise RuntimeError("183-column LP does not pin the current 152-column row inventory")
    if cert.get("parent_182col_lp_sha256") != lp.get("parent_182col_lp_sha256"):
        raise RuntimeError("183-column certificate and LP disagree on the 172-column parent LP")
    if cert.get("parent_182col_dual_certificate_sha256") != lp.get("parent_182col_dual_certificate_sha256"):
        raise RuntimeError("183-column certificate and LP disagree on the 172-column parent dual")
    if cert.get("parent_152col_lp_sha256") != lp.get("current_152col_cut_lp_sha256"):
        raise RuntimeError("183-column certificate and LP disagree on the 152-column cut LP")
    if cert.get("parent_152col_dual_certificate_sha256") != lp.get("current_152col_cut_dual_certificate_sha256"):
        raise RuntimeError("183-column certificate and LP disagree on the 152-column cut dual")
    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    eighth_rows = [tuple(int(x) for x in row) for row in cut_lp["selected_eighth_rows"]]
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(x) for x in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("current parent LP row inventory differs from the pinned 183-column design")
    if (cert.get("column_count"), cert.get("row_count")) != (183, 2113):
        raise RuntimeError("unexpected 183-column dual dimensions")
    if (lp.get("columns"), lp.get("rows")) != (183, 2113):
        raise RuntimeError("unexpected 183-column LP dimensions")

    zq = [Fraction(value) for value in cert["dual_vector_rational"]]
    z = np.asarray([float(value) for value in zq], dtype=np.float64)
    lam = float(Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"]))
    if z.shape != (2113,):
        raise RuntimeError("dual vector has wrong dimension")
    active_rows = np.flatnonzero(z)
    active_low = [int(i) for i in active_rows if i < 1461]
    active_sixth = [int(i) for i in active_rows if 1461 <= i < 2106]
    active_eighth = [int(i) for i in active_rows if 2106 <= i < 2113]
    if len(active_rows) != cert["active_dual_rows"]:
        raise RuntimeError("active dual row count disagrees with certificate")

    fourth_system = FourthMoments(21)
    fourth_system.exact_target_check()
    low_scales = np.r_[
        np.full(21, 1 / 41),
        np.full(len(fourth_system.keys), comb(21, 2) / comb(42, 4)),
    ]
    fourth_groups = {
        row - 21: fourth_system.indices[fourth_system.ids == (row - 21)]
        for row in active_low if row >= 21
    }
    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    eighth_rows = [tuple(int(x) for x in row) for row in cut_lp["selected_eighth_rows"]]
    if len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected pinned row inventory")

    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = sha(all_array.tobytes())
    if len(all_columns) != 1641 or all_sha != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical pool hash/count mismatch")
    active_canonical = sorted(int(x) for x in cert["columns"] if int(x) != 1641)
    if len(active_canonical) != 182 or len(set(active_canonical)) != 182:
        raise RuntimeError("unexpected active canonical-column inventory")
    if active_canonical != sorted(set(lp["base_columns"]) | set(lp["added_canonical_columns"])):
        raise RuntimeError("active canonical columns disagree with 183-column LP")
    active_set = set(active_canonical)

    scores = np.empty(len(all_columns), dtype=np.float64)
    for column, couplings in enumerate(all_columns):
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"canonical column {column} is not a legal 42-site open path")
        rotation = matrix(couplings)
        score = lam
        for row in active_low:
            score += z[row] * active_low_feature(fourth_system, rotation, row, fourth_groups) / low_scales[row]
        for row in active_sixth:
            score += z[row] * orbit_minor(rotation, sixth_rows[row - 1461]) / (5 / 19721)
        for row in active_eighth:
            score += z[row] * orbit_minor(rotation, eighth_rows[row - 2106]) / (1 / 19721)
        scores[column] = score
        if (column + 1) % 100 == 0:
            print(f"Priced canonical columns {column + 1}/{len(all_columns)}", flush=True)

    active_scores = [scores[column] for column in active_canonical]
    unused = [column for column in range(len(all_columns)) if column not in active_set]
    ranked = sorted(((column, float(scores[column])) for column in unused), key=lambda x: x[1], reverse=True)
    positive = [(column, score) for column, score in ranked if score > 0]
    result = {
        "status": "priced_unused_canonical_pool",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_column_count": len(all_columns),
        "active_column_count": len(active_set),
        "active_canonical_columns": active_canonical,
        "unused_column_count": len(unused),
        "active_dual_row_count": len(active_rows),
        "active_row_blocks": {"low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)},
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
            "Binary64 pricing of all unused canonical columns in the frozen 1,641-column physical "
            "pool against the exact 183-column full-sixth-cut dual. Positive scores are discovery candidates only "
            "and require Arb verification. No conclusion about the unrestricted continuous physical "
            "family follows."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "active_dual_rows": len(active_rows),
        "active_row_blocks": result["active_row_blocks"],
        "unused_column_count": len(unused),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": ranked[0][1],
        "top_positive_candidates": result["top_positive_candidates"][:10],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
