"""Float-screen unused canonical physical columns against the certified 20-probe 93-column dual."""
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit
from joint_low_six_eighth_lp import matrix, orbit_minor

CERT_PATH = ROOT / "evidence/twenty_probe_93col_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_with_twenty_sixth_probes_expanded_n21.json"
SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/twenty_probe_dual_pricing_screen_n21.json"


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
    cert_raw = CERT_PATH.read_bytes()
    cert_sha = hashlib.sha256(cert_raw).hexdigest()
    cert = json.loads(cert_raw)
    lp_raw = LP_PATH.read_bytes()
    lp = json.loads(lp_raw)
    if cert["status"] != "strict_pool_separation" or not cert["complete"]:
        raise RuntimeError("the pinned Arb dual separation certificate is not complete")
    if cert["lp_transcript_sha256"] != hashlib.sha256(lp_raw).hexdigest():
        raise RuntimeError("dual certificate and LP transcript hashes disagree")
    if cert["column_count"] != 93 or cert["row_count"] != 1744:
        raise RuntimeError("unexpected dual-certificate dimensions")

    z = np.array([float(Fraction(value)) for value in cert["dual_vector_rational"]])
    lam = float(Fraction(cert["dual_lambda_before_slack"]) - Fraction(cert["dual_slack_delta"]))
    if z.shape != (1744,):
        raise RuntimeError("unexpected exact dual-vector dimension")
    active_rows = np.flatnonzero(z)
    active_low = [int(i) for i in active_rows if i < 1461]
    active_sixth = [int(i) for i in active_rows if 1461 <= i < 1737]
    active_eighth = [int(i) for i in active_rows if 1737 <= i < 1744]

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }

    screen = json.loads(SCREEN_PATH.read_text())["records"]
    screen_rows = [tuple(record["indices"]) for record in screen]
    probe_rows = [tuple(row) for row in lp["sixth_probe_rows"]]
    sixth_rows = screen_rows + probe_rows
    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
    if len(sixth_rows) != 276 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected finite pricing row family")

    all_columns, _, _ = canonical_ensemble()
    active_columns = sorted(int(value) for value in cert["columns"])
    active_set = set(active_columns)
    if len(active_columns) != 93 or len(all_columns) != 1641:
        raise RuntimeError("canonical ensemble no longer has the pinned 93/1641 pool structure")
    all_column_array = np.asarray(all_columns, dtype="<f8")
    all_columns_sha = hashlib.sha256(all_column_array.tobytes()).hexdigest()
    if all_columns_sha != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical physical column pool hash mismatch")

    scores = []
    for column, couplings in enumerate(all_columns):
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"canonical column {column} is not a legal path generator")
        rotation = matrix(couplings)
        score = lam
        for row in active_low:
            feature = active_low_feature(system, rotation, row, fourth_groups)
            score += z[row] * feature / low_scales[row]
        for row in active_sixth:
            feature = orbit_minor(rotation, sixth_rows[row - 1461])
            score += z[row] * feature / (5 / 19721)
        for row in active_eighth:
            feature = orbit_minor(rotation, eighth_rows[row - 1737])
            score += z[row] * feature / (1 / 19721)
        scores.append(float(score))

    active_scores = [scores[column] for column in active_columns]
    unused = [column for column in range(len(all_columns)) if column not in active_set]
    unused_scores = [(column, scores[column]) for column in unused]
    unused_scores.sort(key=lambda item: item[1], reverse=True)
    positive = [(column, score) for column, score in unused_scores if score > 0]

    result = {
        "status": "priced_existing_pool",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": cert["lp_transcript_sha256"],
        "canonical_all_columns_sha256_le_f64": all_columns_sha,
        "canonical_column_count": len(all_columns),
        "active_column_count": len(active_columns),
        "unused_column_count": len(unused),
        "active_dual_row_count": len(active_rows),
        "active_row_blocks": {
            "low": len(active_low),
            "sixth": len(active_sixth),
            "eighth": len(active_eighth),
        },
        "active_pool_max_float_pricing_score": max(active_scores),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": unused_scores[0][1],
        "top_unused_candidates": [
            {
                "column": int(column),
                "float_pricing_score": float(score),
                "couplings": [float(value) for value in all_columns[column]],
            }
            for column, score in unused_scores[:50]
        ],
        "top_positive_candidates": [
            {
                "column": int(column),
                "float_pricing_score": float(score),
                "couplings": [float(value) for value in all_columns[column]],
            }
            for column, score in positive[:50]
        ],
        "scope": (
            "Binary64 pricing screen of all 1,548 unused columns among the 1,641 "
            "canonical legal path generators. Positive scores are candidates only; "
            "they require exact 128-bit Arb verification before entering an expanded pool."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "canonical_column_count": len(all_columns),
        "active_column_count": len(active_columns),
        "unused_column_count": len(unused),
        "active_dual_row_count": len(active_rows),
        "active_row_blocks": result["active_row_blocks"],
        "active_pool_max_float_pricing_score": result["active_pool_max_float_pricing_score"],
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": result["max_unused_float_pricing_score"],
        "top_positive_candidates": result["top_positive_candidates"][:5],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
