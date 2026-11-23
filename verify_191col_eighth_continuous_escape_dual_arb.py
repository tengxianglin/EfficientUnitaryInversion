"""128-bit Arb certificate for the 191-column eighth-continuous-escape LP.

The HiGHS solve is discovery only. This verifier reconstructs its dual exactly
from the stored binary64 marginals, rescales to exact l1 norm <= 1, and checks
all 191 physical-column inequalities with Arb at 128-bit precision.
"""
import hashlib
import json
from fractions import Fraction

import numpy as np
from flint import arb, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    load_rational_dual,
    orbit_average_minor,
)
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_190col_seventh_continuous_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_190col_seventh_continuous_escape_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
ESCAPE_1 = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
ESCAPE_2 = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
ESCAPE_3 = ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json"
ESCAPE_4 = ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json"
ESCAPE_5 = ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json"
ESCAPE_6 = ROOT / "evidence/188col_continuous_dual_escape_arb_n21.json"
ESCAPE_7 = ROOT / "evidence/189col_continuous_dual_escape_arb_n21.json"
ESCAPE_8 = ROOT / "evidence/190col_continuous_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT_PATH = ROOT / "evidence/55probe_191col_eighth_continuous_escape_dual_certificate_n21.json"

PRECISION_BITS = 128
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
ESCAPE_COLUMNS = (1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648)
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        LP_PATH, PARENT_LP, PARENT_DUAL, CANDIDATE_152, CUT_LP, CUT_DUAL,
        ESCAPE_1, ESCAPE_2, ESCAPE_3, ESCAPE_4, ESCAPE_5, ESCAPE_6, ESCAPE_7, ESCAPE_8, SEED_POOL,
    )
    raw = [path.read_bytes() for path in paths]
    values = [
        value if path.suffix == ".npy" else json.loads(value)
        for path, value in zip(paths, raw)
    ]
    (
        lp, parent_lp, parent_dual, candidate152, cut_lp, cut_dual,
        escape1, escape2, escape3, escape4, escape5, escape6, escape7, escape8, seed_raw,
    ) = values
    (
        lp_sha, parent_lp_sha, parent_dual_sha, candidate_sha, cut_lp_sha,
        cut_dual_sha, escape1_sha, escape2_sha, escape3_sha, escape4_sha,
        escape5_sha, escape6_sha, escape7_sha, escape8_sha, seed_file_sha,
    ) = map(sha, raw)

    if lp.get("status") != "191col_eighth_continuous_escape_lp_above_one_third":
        raise RuntimeError("191-column LP is not an above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (191, 2113):
        raise RuntimeError("unexpected 191-column / 2,113-row dimensions")
    if lp.get("parent_190col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("191-column LP does not pin its exact 190-column parent LP")
    if lp.get("parent_190col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("191-column LP does not pin its exact 190-column parent dual")
    if lp.get("parent_152col_candidate_sha256") != candidate_sha:
        raise RuntimeError("190-column LP does not pin its 152-column ancestor candidate")
    if lp.get("cut_lp_transcript_sha256") != cut_lp_sha or lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("190-column LP does not pin the exact 2,113-row cut design")

    if parent_lp.get("status") != "190col_seventh_continuous_escape_lp_above_one_third":
        raise RuntimeError("190-column parent LP has an unexpected status")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (190, 2113):
        raise RuntimeError("unexpected 190-column parent dimensions")
    if parent_dual.get("status") != "strict_190col_2113row_seventh_continuous_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("190-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("190-column parent dual does not pin its LP")
    if parent_lp.get("parent_189col_lp_sha256") != parent_dual.get("parent_189col_lp_sha256") or parent_lp.get("parent_189col_dual_certificate_sha256") != parent_dual.get("parent_189col_dual_certificate_sha256"):
        raise RuntimeError("190-column parent LP/dual ancestry mismatch")
    if parent_lp.get("parent_152col_candidate_sha256") != candidate_sha or parent_dual.get("parent_152col_candidate_sha256") != candidate_sha:
        raise RuntimeError("190-column parent does not pin the 152-column ancestor candidate")
    if parent_lp.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("190-column parent LP does not pin the cut design and dual")
    if parent_dual.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_dual.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("190-column parent dual does not pin the cut design and dual")

    escape_hashes = (escape1_sha, escape2_sha, escape3_sha, escape4_sha, escape5_sha, escape6_sha, escape7_sha, escape8_sha)
    escape_objects = (escape1, escape2, escape3, escape4, escape5, escape6, escape7, escape8)
    escape_keys = (
        "first_continuous_escape_arb_certificate_sha256",
        "second_continuous_escape_arb_certificate_sha256",
        "third_continuous_escape_arb_certificate_sha256",
        "fourth_continuous_escape_arb_certificate_sha256",
        "fifth_continuous_escape_arb_certificate_sha256",
        "sixth_continuous_escape_arb_certificate_sha256",
        "seventh_continuous_escape_arb_certificate_sha256",
        "eighth_continuous_escape_arb_certificate_sha256",
    )
    for index, (cert, digest) in enumerate(zip(escape_objects, escape_hashes), 1):
        if cert.get("status") != "certified_continuous_path_dual_escape":
            raise RuntimeError(f"continuous escape {index} has an unexpected status")
        if not cert.get("complete") or not cert.get("strictly_positive"):
            raise RuntimeError(f"continuous escape {index} lacks a complete strict Arb certificate")
        if lp.get(escape_keys[index - 1]) != digest:
            raise RuntimeError(f"191-column LP provenance mismatch for escape {index}")
        if index <= 7:
            if parent_lp.get(escape_keys[index - 1]) != digest or parent_dual.get(escape_keys[index - 1]) != digest:
                raise RuntimeError(f"190-column parent does not pin escape {index}")

    if candidate152.get("continuous_escape_arb_certificate_sha256") != escape1_sha:
        raise RuntimeError("152-column ancestor candidate does not pin the first escape")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut dual is not strictly Arb-certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("152-column cut dual does not pin its LP")
    if escape8.get("dual_certificate_sha256") != parent_dual_sha or escape8.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("eighth escape does not pin the exact 190-column parent dual/LP")
    if escape8.get("cut_lp_transcript_sha256") != cut_lp_sha or escape8.get("candidate_outside_frozen_canonical_pool") is not True:
        raise RuntimeError("eighth escape does not pin the cut design or canonical exclusion")

    all_couplings = [
        [Fraction(value) for value in cert["candidate_couplings_exact"]]
        for cert in escape_objects
    ]
    for index, couplings in enumerate(all_couplings, 1):
        if len(couplings) != 42 or couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError(f"continuous escape {index} is not a legal strictly-positive 41-edge path")
    if len({tuple(couplings) for couplings in all_couplings}) != 8:
        raise RuntimeError("the eight continuous escape paths are not pairwise distinct")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if lp.get("seed_pool_sha256_le_f64") != seed_sha or parent_lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("191/190 LP seed-pool provenance mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")
    if parent_lp.get("canonical_all_columns_sha256_le_f64") != all_sha:
        raise RuntimeError("189-column parent uses a different canonical inventory")

    base_columns = [int(value) for value in parent_lp["base_columns"]]
    added_columns = [int(value) for value in parent_lp["added_canonical_columns"]]
    parent_order = [int(value) for value in parent_lp["column_order"]]
    expected_parent_order = (
        base_columns + [ESCAPE_COLUMNS[0]] + added_columns + list(ESCAPE_COLUMNS[1:7])
    )
    column_order = [int(value) for value in lp["column_order"]]
    if len(base_columns) != 151 or len(added_columns) != 32 or parent_order != expected_parent_order:
        raise RuntimeError("190-column parent inventory/order mismatch")
    if column_order != parent_order + [ESCAPE_COLUMNS[7]] or len(column_order) != 191 or len(set(column_order)) != 191:
        raise RuntimeError("191-column expanded physical-column ordering mismatch")

    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [all_couplings[0]]
        + [all_columns[column] for column in added_columns]
        + all_couplings[1:]
    )
    if len(physical_columns) != 191:
        raise RuntimeError("wrong expanded physical column count")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut_lp)
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("191-column row inventory hash mismatch")
    if sixth_hash != parent_lp.get("sixth_rows_sha256") or eighth_hash != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("191-column row inventory differs from the certified 190-column parent")
    if row_blocks != lp.get("row_blocks") or row_blocks != parent_lp.get("row_blocks"):
        raise RuntimeError("191/190 row-block inventories disagree")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    if norm > 1 or dual_objective <= Fraction(1, 3):
        raise RuntimeError("rationalized 191-column dual does not meet minimax dual conditions")
    z_arb = [ball(value) for value in z]
    active_rows = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active_rows if index < 1461]
    active_sixth = [index for index in active_rows if 1461 <= index < 2106]
    active_eighth = [index for index in active_rows if index >= 2106]
    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }

    column_lhs = []
    index_hash = hashlib.sha256()
    for position, (column, couplings) in enumerate(zip(column_order, physical_columns), 1):
        index_hash.update(int(column).to_bytes(4, "little", signed=False))
        entries = rotation_entries_exact(couplings)
        lhs = arb(0)
        for row in active_low:
            lhs += z_arb[row] * active_low_feature(system, entries, row, fourth_groups) / ball(low_scales[row])
        for row in active_sixth:
            lhs += z_arb[row] * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(SIXTH_SCALE)
        for row in active_eighth:
            lhs += z_arb[row] * orbit_average_minor(entries, eighth_rows[row - 2106]) / ball(EIGHTH_SCALE)
        column_lhs.append(lhs + ball(lam))
        print(
            f"Arb-evaluated dual column {position}/191 (label {column}); "
            f"active rows {len(active_rows)}/{len(y)}",
            flush=True,
        )

    deltas = [
        Fraction(0), Fraction(1, 10**12), Fraction(1, 10**10),
        Fraction(1, 10**9), Fraction(1, 10**8), Fraction(1, 10**7),
        Fraction(1, 10**6), Fraction(1, 10**5), Fraction(1, 10**4),
    ]
    selected_delta = None
    selected_intervals = None
    for delta in deltas:
        if dual_objective - delta <= Fraction(1, 3):
            continue
        shifted = [value - ball(delta) for value in column_lhs]
        if all(value.upper() <= 0 for value in shifted):
            selected_delta, selected_intervals = delta, shifted
            break
    if selected_delta is None:
        maximum = max(float(value.upper()) for value in column_lhs)
        raise RuntimeError(
            f"could not certify all 191 dual inequalities; max unshifted upper={maximum}"
        )

    lower = dual_objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_191col_2113row_eighth_continuous_escape_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_190col_lp_sha256": parent_lp_sha,
        "parent_190col_dual_certificate_sha256": parent_dual_sha,
        "parent_152col_candidate_sha256": candidate_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "cut_dual_certificate_sha256": cut_dual_sha,
        "first_continuous_escape_arb_certificate_sha256": escape1_sha,
        "second_continuous_escape_arb_certificate_sha256": escape2_sha,
        "third_continuous_escape_arb_certificate_sha256": escape3_sha,
        "fourth_continuous_escape_arb_certificate_sha256": escape4_sha,
        "fifth_continuous_escape_arb_certificate_sha256": escape5_sha,
        "sixth_continuous_escape_arb_certificate_sha256": escape6_sha,
        "seventh_continuous_escape_arb_certificate_sha256": escape7_sha,
        "eighth_continuous_escape_arb_certificate_sha256": escape8_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": 191,
        "row_count": len(y),
        "row_blocks": row_blocks,
        "total_sixth_rows": len(sixth_rows),
        "active_dual_rows": len(active_rows),
        "active_dual_low_rows": len(active_low),
        "active_dual_sixth_rows": len(active_sixth),
        "active_dual_eighth_rows": len(active_eighth),
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_convention": "z = first m HiGHS inequality marginals minus second m; lambda is the sum-to-one equality marginal",
        "dual_l1_norm_exact": str(norm),
        "dual_scale_applied": str(dual_scale),
        "dual_lambda_exact": str(lam),
        "dual_objective_exact": str(dual_objective),
        "dual_slack_delta": str(selected_delta),
        "certified_minimax_lower_bound": str(lower),
        "strict_lower_bound_above_one_third": str(lower - Fraction(1, 3)),
        "maximum_arb_upper_of_column_dual_lhs_minus_slack": str(maximum_upper),
        "column_dual_lhs_intervals": [
            {"column": column, "interval": str(value)}
            for column, value in zip(column_order, selected_intervals)
        ],
        "dual_vector_rational": [str(value) for value in z],
        "scope": (
            "Rigorous mixed-order minimax lower bound for every convex mixture over the 191 "
            "pinned physical generators on the exact 2,113-row design: all 1,461 second/fourth "
            "rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. "
            "This is not a complete sixth/eighth orbit certificate, a continuous-family no-go, "
            "or an operational Choi/diamond theorem."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "column_count": 191,
        "row_count": len(y),
        "active_dual_rows": len(active_rows),
        "active_row_blocks": {
            "low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)
        },
        "dual_l1_norm_exact": str(norm),
        "dual_objective_exact": str(dual_objective),
        "certified_minimax_lower_bound": str(lower),
        "gap_above_one_third": str(lower - Fraction(1, 3)),
        "selected_slack": str(selected_delta),
        "max_arb_upper": str(maximum_upper),
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
