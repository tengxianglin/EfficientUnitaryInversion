"""Reoptimize the 2,113-row EUI LP after an eighth Arb-certified continuous path.

The parent is the exact 190-column pool. The new path is independently
certified against the 190-column dual. HiGHS is discovery only; the workflow
branches to an exact-mixture Arb audit or a new 191-column dual certificate.
"""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import matrix, orbit_minor

LP_190 = ROOT / "evidence/joint_low_six_eighth_lp_190col_seventh_continuous_escape_n21.json"
DUAL_190 = ROOT / "evidence/55probe_190col_seventh_continuous_escape_dual_certificate_n21.json"
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
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_191col_eighth_continuous_escape_n21.json"

SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
ESCAPE_1_COLUMN = 1641
ESCAPE_2_COLUMN = 1642
ESCAPE_3_COLUMN = 1643
ESCAPE_4_COLUMN = 1644
ESCAPE_5_COLUMN = 1645
ESCAPE_6_COLUMN = 1646
ESCAPE_7_COLUMN = 1647
ESCAPE_8_COLUMN = 1648
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    paths = (LP_190, DUAL_190, CANDIDATE_152, CUT_LP, CUT_DUAL,
             ESCAPE_1, ESCAPE_2, ESCAPE_3, ESCAPE_4, ESCAPE_5, ESCAPE_6, ESCAPE_7, ESCAPE_8, SEED_POOL)
    raw = {path: path.read_bytes() for path in paths}
    data = {path: (value if path.suffix == ".npy" else json.loads(value))
            for path, value in raw.items()}
    hashes = {path.name: sha(value) for path, value in raw.items()}

    parent_lp = data[LP_190]
    parent_dual = data[DUAL_190]
    candidate152 = data[CANDIDATE_152]
    cut_lp = data[CUT_LP]
    cut_dual = data[CUT_DUAL]
    escape1 = data[ESCAPE_1]
    escape2 = data[ESCAPE_2]
    escape3 = data[ESCAPE_3]
    escape4 = data[ESCAPE_4]
    escape5 = data[ESCAPE_5]
    escape6 = data[ESCAPE_6]
    escape7 = data[ESCAPE_7]
    escape8 = data[ESCAPE_8]

    if parent_lp.get("status") != "190col_seventh_continuous_escape_lp_above_one_third":
        raise RuntimeError("190-column parent LP is not the expected above-cap discovery")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (190, 2113):
        raise RuntimeError("unexpected 190-column parent dimensions")
    if parent_dual.get("status") != "strict_190col_2113row_seventh_continuous_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("190-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != hashes[LP_190.name]:
        raise RuntimeError("190-column parent dual does not pin its LP")
    if parent_lp.get("parent_189col_lp_sha256") != parent_dual.get("parent_189col_lp_sha256") or parent_lp.get("parent_189col_dual_certificate_sha256") != parent_dual.get("parent_189col_dual_certificate_sha256"):
        raise RuntimeError("190-column parent LP/dual ancestry mismatch")
    if parent_lp.get("parent_152col_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("190-column parent LP does not pin its 152-column ancestor")
    if parent_lp.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name] or parent_lp.get("cut_dual_certificate_sha256") != hashes[CUT_DUAL.name]:
        raise RuntimeError("190-column parent LP does not pin the 2,113-row cut design")
    if parent_dual.get("parent_152col_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("190-column parent dual does not pin its 152-column ancestor")
    if parent_dual.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name] or parent_dual.get("cut_dual_certificate_sha256") != hashes[CUT_DUAL.name]:
        raise RuntimeError("190-column parent dual does not pin the 2,113-row cut design")
    for label, key, path in (
        ("first", "first_continuous_escape_arb_certificate_sha256", ESCAPE_1),
        ("second", "second_continuous_escape_arb_certificate_sha256", ESCAPE_2),
        ("third", "third_continuous_escape_arb_certificate_sha256", ESCAPE_3),
        ("fourth", "fourth_continuous_escape_arb_certificate_sha256", ESCAPE_4),
        ("fifth", "fifth_continuous_escape_arb_certificate_sha256", ESCAPE_5),
        ("sixth", "sixth_continuous_escape_arb_certificate_sha256", ESCAPE_6),
        ("seventh", "seventh_continuous_escape_arb_certificate_sha256", ESCAPE_7),
    ):
        if parent_lp.get(key) != hashes[path.name] or parent_dual.get(key) != hashes[path.name]:
            raise RuntimeError(f"190-column parent provenance mismatch for {label} escape")
    if escape8.get("dual_certificate_sha256") != hashes[DUAL_190.name] or escape8.get("lp_transcript_sha256") != hashes[LP_190.name]:
        raise RuntimeError("eighth escape does not pin the exact 190-column parent dual/LP")
    if escape8.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name] or escape8.get("candidate_outside_frozen_canonical_pool") is not True:
        raise RuntimeError("eighth escape does not pin the cut design or canonical exclusion")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column ancestor dual is not strictly Arb-certified")
    if cut_dual.get("lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("152-column ancestor dual does not pin its LP")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_1.name]:
        raise RuntimeError("152-column ancestor candidate does not pin the first escape")
    for label, cert in (
        ("first", escape1), ("second", escape2), ("third", escape3),
        ("fourth", escape4), ("fifth", escape5), ("sixth", escape6), ("seventh", escape7), ("eighth", escape8),
    ):
        if cert.get("status") != "certified_continuous_path_dual_escape" or not cert.get("complete") or not cert.get("strictly_positive"):
            raise RuntimeError(f"{label} continuous path lacks a strict Arb certificate")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if parent_lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("190-column parent LP does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    added_columns = [int(x) for x in parent_lp["added_canonical_columns"]]
    parent_order = [int(x) for x in parent_lp["column_order"]]
    expected_parent_order = base_columns + [ESCAPE_1_COLUMN] + added_columns + [ESCAPE_2_COLUMN, ESCAPE_3_COLUMN, ESCAPE_4_COLUMN, ESCAPE_5_COLUMN, ESCAPE_6_COLUMN, ESCAPE_7_COLUMN]
    if len(base_columns) != 151 or len(added_columns) != 32:
        raise RuntimeError("unexpected canonical inventory in the 190-column parent")
    if parent_order != expected_parent_order or len(set(parent_order)) != 190:
        raise RuntimeError("190-column parent ordering is inconsistent")

    couplings1 = [Fraction(x) for x in candidate152["escape_couplings_exact"]]
    couplings2 = [Fraction(x) for x in escape2["candidate_couplings_exact"]]
    couplings3 = [Fraction(x) for x in escape3["candidate_couplings_exact"]]
    couplings4 = [Fraction(x) for x in escape4["candidate_couplings_exact"]]
    couplings5 = [Fraction(x) for x in escape5["candidate_couplings_exact"]]
    couplings6 = [Fraction(x) for x in escape6["candidate_couplings_exact"]]
    couplings7 = [Fraction(x) for x in escape7["candidate_couplings_exact"]]
    couplings8 = [Fraction(x) for x in escape8["candidate_couplings_exact"]]
    if [str(x) for x in couplings1] != escape1["candidate_couplings_exact"]:
        raise RuntimeError("first path differs from its Arb-certified input")
    for label, couplings in (("first", couplings1), ("second", couplings2), ("third", couplings3), ("fourth", couplings4), ("fifth", couplings5), ("sixth", couplings6), ("seventh", couplings7), ("eighth", couplings8)):
        if len(couplings) != 42 or couplings[-1] != 0 or any(x <= 0 for x in couplings[:-1]):
            raise RuntimeError(f"{label} path is not a strictly-positive 41-edge open path")
    if len({tuple(couplings1), tuple(couplings2), tuple(couplings3), tuple(couplings4), tuple(couplings5), tuple(couplings6), tuple(couplings7), tuple(couplings8)}) != 8:
        raise RuntimeError("the seven continuous escape paths are not pairwise distinct")
    if escape8.get("candidate_outside_frozen_canonical_pool") is not True:
        raise RuntimeError("eighth path is not certified outside the canonical inventory")

    column_order = parent_order + [ESCAPE_8_COLUMN]
    if len(column_order) != 191 or len(set(column_order)) != 191:
        raise RuntimeError("expanded physical pool must contain 191 unique columns")
    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [couplings1]
        + [all_columns[column] for column in added_columns]
        + [couplings2, couplings3, couplings4, couplings5, couplings6, couplings7, couplings8]
    )
    if len(physical_columns) != 191:
        raise RuntimeError("wrong expanded physical column count")

    sixth_rows = [tuple(int(v) for v in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(v) for v in cut_lp["sixth_cut_targets"]]
    eighth_rows = [tuple(int(v) for v in row) for row in cut_lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(v) for v in cut_lp["selected_eighth_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("unexpected 645-row sixth inventory")
    if len(eighth_rows) != 7 or len(eighth_targets) != 7:
        raise RuntimeError("unexpected selected eighth-order inventory")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-order target mismatch")
    expected_eighth = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    if expected_eighth != eighth_targets:
        raise RuntimeError("eighth-order target mismatch")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != parent_lp.get("sixth_rows_sha256") or eighth_hash != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("row inventory differs from the certified 190-column design")

    system = FourthMoments(21)
    system.exact_target_check()
    low = np.asarray([
        system.features(np.asarray(list(map(float, couplings))))
        for couplings in physical_columns
    ])
    low_target = system.target.copy()
    low_scale = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]
    if len(low_target) != 1461:
        raise RuntimeError("unexpected complete second/fourth row count")

    sixth = np.empty((191, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((191, len(eighth_rows)), dtype=np.float64)
    for index, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[index] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (index + 1) % 16 == 0 or index == 190:
            print(f"Built physical feature columns {index + 1}/191", flush=True)

    sixth_scale = np.full(len(sixth_rows), float(SIXTH_SCALE))
    eighth_scale = np.full(len(eighth_rows), float(EIGHTH_SCALE))
    A = np.vstack([
        low.T / low_scale[:, None],
        sixth.T / sixth_scale[:, None],
        eighth.T / eighth_scale[:, None],
    ])
    y = np.r_[
        low_target / low_scale,
        np.asarray([float(value) for value in sixth_targets]) / sixth_scale,
        np.asarray([float(value) for value in eighth_targets]) / eighth_scale,
    ]
    row_blocks = {
        "low_complete": len(low_target),
        "sixth_selected_plus_all_cuts": len(sixth_rows),
        "eighth_selected": len(eighth_rows),
    }
    m, n = A.shape
    if (m, n) != (2113, 191):
        raise RuntimeError(f"unexpected expanded LP dimensions: {(m, n)}")

    aub = np.vstack([np.c_[A, -np.ones(m)], np.c_[-A, -np.ones(m)]])
    bub = np.r_[y, -y]
    result = linprog(
        np.r_[np.zeros(n), 1.0],
        A_ub=aub,
        b_ub=bub,
        A_eq=np.r_[np.ones(n), 0.0][None, :],
        b_eq=[1.0],
        bounds=[(0.0, None)] * n + [(0.0, None)],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"HiGHS failed: {result.message}")

    residual = np.abs(A @ result.x[:-1] - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    dual_z = result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]
    dual_objective = float(result.eqlin.marginals[0] + np.dot(dual_z, y))
    support = [
        {"column": int(column_order[index]), "weight": float(weight)}
        for index, weight in enumerate(result.x[:-1]) if weight > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())
    lp_status = (
        "191col_eighth_continuous_escape_lp_candidate_below_one_third"
        if result.fun < 1 / 3 else "191col_eighth_continuous_escape_lp_above_one_third"
    )
    transcript = {
        "status": lp_status,
        "parent_190col_lp_sha256": hashes[LP_190.name],
        "parent_190col_dual_certificate_sha256": hashes[DUAL_190.name],
        "parent_152col_candidate_sha256": hashes[CANDIDATE_152.name],
        "cut_lp_transcript_sha256": hashes[CUT_LP.name],
        "cut_dual_certificate_sha256": hashes[CUT_DUAL.name],
        "first_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_1.name],
        "second_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_2.name],
        "third_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_3.name],
        "fourth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_4.name],
        "fifth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_5.name],
        "sixth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_6.name],
        "seventh_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_7.name],
        "eighth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_8.name],
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "first_continuous_escape_column_index": ESCAPE_1_COLUMN,
        "added_canonical_columns": added_columns,
        "second_continuous_escape_column_index": ESCAPE_2_COLUMN,
        "third_continuous_escape_column_index": ESCAPE_3_COLUMN,
        "fourth_continuous_escape_column_index": ESCAPE_4_COLUMN,
        "fifth_continuous_escape_column_index": ESCAPE_5_COLUMN,
        "sixth_continuous_escape_column_index": ESCAPE_6_COLUMN,
        "seventh_continuous_escape_column_index": ESCAPE_7_COLUMN,
        "eighth_continuous_escape_column_index": ESCAPE_8_COLUMN,
        "column_order": column_order,
        "sixth_rows_sha256": sixth_hash,
        "eighth_rows_sha256": eighth_hash,
        "matrix_and_target_sha256_le_f64": matrix_sha,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(residual.max()),
        "expanded_block_maxima": {
            name: float(residual[cuts[index]:cuts[index + 1]].max())
            for index, name in enumerate(row_blocks)
        },
        "positive_support": support,
        "dual_discovery": {
            "z_l1_norm": float(np.abs(dual_z).sum()),
            "objective": dual_objective,
            "primal_dual_gap": abs(float(result.fun) - dual_objective),
            "inequality_marginals": [float(value) for value in result.ineqlin.marginals],
            "equality_marginal": float(result.eqlin.marginals[0]),
        },
        "finite_candidate_below_one_third": bool(result.fun < 1 / 3),
        "scope": (
            "Binary64 HiGHS discovery on the fixed 2,113-row mixed-order design, adding an eighth "
            "continuous path whose positive pricing score against the exact 190-column dual was "
            "independently certified with 128-bit Arb. A sub-1/3 result is only a candidate until "
            "the exact rationalized mixture passes Arb on all 2,113 pinned rows and a complete "
            "63,133-orbit sixth-order audit. An above-cap result requires a new exact rational dual "
            "and independent Arb verification against all 191 physical columns."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (int(column_order[index]), Fraction.from_float(float(weight)))
            for index, weight in enumerate(result.x[:-1]) if weight > 1e-10
        ]
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": column, "probability": str(weight / total)}
            for column, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("exact candidate probabilities do not sum to one")
        next_candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_sha,
            "parent_190col_lp_sha256": hashes[LP_190.name],
            "parent_190col_dual_certificate_sha256": hashes[DUAL_190.name],
            "first_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_1.name],
            "second_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_2.name],
            "third_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_3.name],
            "fourth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_4.name],
            "fifth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_5.name],
            "sixth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_6.name],
        "seventh_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_7.name],
            "eighth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_8.name],
            "seed_pool_sha256_le_f64": seed_sha,
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "first_continuous_escape_column_index": ESCAPE_1_COLUMN,
            "first_continuous_escape_couplings_exact": [str(x) for x in couplings1],
            "added_canonical_columns": added_columns,
            "second_continuous_escape_column_index": ESCAPE_2_COLUMN,
            "second_continuous_escape_couplings_exact": [str(x) for x in couplings2],
            "third_continuous_escape_column_index": ESCAPE_3_COLUMN,
            "third_continuous_escape_couplings_exact": [str(x) for x in couplings3],
            "fourth_continuous_escape_column_index": ESCAPE_4_COLUMN,
            "fourth_continuous_escape_couplings_exact": [str(x) for x in couplings4],
            "fifth_continuous_escape_column_index": ESCAPE_5_COLUMN,
            "fifth_continuous_escape_couplings_exact": [str(x) for x in couplings5],
            "sixth_continuous_escape_column_index": ESCAPE_6_COLUMN,
        "seventh_continuous_escape_column_index": ESCAPE_7_COLUMN,
            "eighth_continuous_escape_column_index": ESCAPE_8_COLUMN,
            "sixth_continuous_escape_couplings_exact": [str(x) for x in couplings6],
            "seventh_continuous_escape_couplings_exact": [str(x) for x in couplings7],
            "eighth_continuous_escape_couplings_exact": [str(x) for x in couplings8],
            "column_order": column_order,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_cut_rows": [list(row) for row in sixth_rows],
            "sixth_cut_targets": [str(x) for x in sixth_targets],
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "selected_eighth_targets": [str(x) for x in eighth_targets],
            "scope": (
                "Exact rational probabilities obtained by normalizing binary64 191-column HiGHS "
                "weights. This candidate is constrained only on the pinned 2,113 rows and requires "
                "independent Arb verification plus complete sixth-order separation."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(next_candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": lp_status,
        "columns": n,
        "rows": m,
        "objective": float(result.fun),
        "recomputed_max": float(residual.max()),
        "block_maxima": transcript["expanded_block_maxima"],
        "support_size": len(support),
        "primal_dual_gap": abs(float(result.fun) - dual_objective),
        "candidate_written": candidate_written,
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if candidate_written else None,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
