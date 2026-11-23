"""Reoptimize the 2,113-row EUI LP after a fifth Arb-certified continuous path.

The parent is the exact 187-column pool. The new path is independently
certified against the 187-column dual. HiGHS is discovery only; the workflow
branches to an exact-mixture Arb audit or a new 188-column dual certificate.
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

LP_187 = ROOT / "evidence/joint_low_six_eighth_lp_187col_fourth_continuous_escape_n21.json"
DUAL_187 = ROOT / "evidence/55probe_187col_fourth_continuous_escape_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
ESCAPE_1 = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
ESCAPE_2 = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
ESCAPE_3 = ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json"
ESCAPE_4 = ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json"
ESCAPE_5 = ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_188col_fifth_continuous_escape_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_188col_fifth_continuous_escape_n21.json"

SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
ESCAPE_1_COLUMN = 1641
ESCAPE_2_COLUMN = 1642
ESCAPE_3_COLUMN = 1643
ESCAPE_4_COLUMN = 1644
ESCAPE_5_COLUMN = 1645
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    paths = (LP_187, DUAL_187, CANDIDATE_152, CUT_LP, CUT_DUAL,
             ESCAPE_1, ESCAPE_2, ESCAPE_3, ESCAPE_4, ESCAPE_5, SEED_POOL)
    raw = {path: path.read_bytes() for path in paths}
    data = {path: (value if path.suffix == ".npy" else json.loads(value))
            for path, value in raw.items()}
    hashes = {path.name: sha(value) for path, value in raw.items()}

    parent_lp = data[LP_187]
    parent_dual = data[DUAL_187]
    candidate152 = data[CANDIDATE_152]
    cut_lp = data[CUT_LP]
    cut_dual = data[CUT_DUAL]
    escape1 = data[ESCAPE_1]
    escape2 = data[ESCAPE_2]
    escape3 = data[ESCAPE_3]
    escape4 = data[ESCAPE_4]
    escape5 = data[ESCAPE_5]

    if parent_lp.get("status") != "188col_fifth_continuous_escape_lp_above_one_third":
        raise RuntimeError("187-column parent LP is not the expected above-cap discovery")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (187, 2113):
        raise RuntimeError("unexpected 187-column parent dimensions")
    if parent_dual.get("status") != "strict_187col_2113row_fourth_continuous_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("187-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != hashes[LP_187.name]:
        raise RuntimeError("187-column parent dual does not pin its LP")
    if parent_lp.get("parent_152col_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("186-column parent LP does not pin its 152-column ancestor")
    if parent_lp.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name] or parent_lp.get("cut_dual_certificate_sha256") != hashes[CUT_DUAL.name]:
        raise RuntimeError("186-column parent LP does not pin the 2,113-row cut design")
    if parent_lp.get("first_continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_1.name]:
        raise RuntimeError("186-column parent LP does not pin the first continuous escape")
    if parent_lp.get("second_continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_2.name]:
        raise RuntimeError("186-column parent LP does not pin the second continuous escape")
    if parent_dual.get("first_continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_1.name]:
        raise RuntimeError("186-column parent dual does not pin the first continuous escape")
    if parent_dual.get("second_continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_2.name]:
        raise RuntimeError("186-column parent dual does not pin the second continuous escape")
    if parent_lp.get("third_continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_3.name] or parent_dual.get("third_continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_3.name]:
        raise RuntimeError("186-column parent does not pin the third continuous escape")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column ancestor dual is not strictly certified")
    if cut_dual.get("lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("152-column ancestor dual does not pin its cut LP")

    for label, cert in (("first", escape1), ("second", escape2), ("third", escape3), ("fourth", escape4)):
        if cert.get("status") != "certified_continuous_path_dual_escape" or not cert.get("complete") or not cert.get("strictly_positive"):
            raise RuntimeError(f"{label} continuous path lacks a strict Arb certificate")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_1.name]:
        raise RuntimeError("152-column ancestor candidate does not pin the first escape")
    if escape3.get("dual_certificate_sha256") != parent_lp.get("parent_185col_dual_certificate_sha256"):
        raise RuntimeError("third escape does not pin the exact 185-column dual")
    if escape3.get("lp_transcript_sha256") != parent_lp.get("parent_185col_lp_sha256"):
        raise RuntimeError("third escape does not pin the exact 185-column LP")
    if escape3.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("third escape does not pin the 2,113-row design")
    if escape4.get("dual_certificate_sha256") != parent_dual.get("parent_186col_dual_certificate_sha256") or escape4.get("lp_transcript_sha256") != parent_dual.get("parent_186col_lp_sha256"):
        raise RuntimeError("fourth escape does not pin the exact 186-column parent dual/LP")
    if escape4.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("fourth escape does not pin the 2,113-row design")
    if escape5.get("dual_certificate_sha256") != hashes[DUAL_187.name] or escape5.get("lp_transcript_sha256") != hashes[LP_187.name]:
        raise RuntimeError("fifth escape does not pin the exact 187-column parent dual/LP")
    if escape5.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("fifth escape does not pin the 2,113-row design")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if parent_lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("187-column parent LP does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    added_columns = [int(x) for x in parent_lp["added_canonical_columns"]]
    parent_order = [int(x) for x in parent_lp["column_order"]]
    expected_parent_order = base_columns + [ESCAPE_1_COLUMN] + added_columns + [ESCAPE_2_COLUMN, ESCAPE_3_COLUMN]
    if len(base_columns) != 151 or len(added_columns) != 32:
        raise RuntimeError("unexpected canonical inventory in the 186-column parent")
    if parent_order != expected_parent_order or len(set(parent_order)) != 187:
        raise RuntimeError("187-column parent ordering is inconsistent")

    couplings1 = [Fraction(x) for x in candidate152["escape_couplings_exact"]]
    couplings2 = [Fraction(x) for x in escape2["candidate_couplings_exact"]]
    couplings3 = [Fraction(x) for x in escape3["candidate_couplings_exact"]]
    couplings4 = [Fraction(x) for x in escape4["candidate_couplings_exact"]]
    couplings5 = [Fraction(x) for x in escape5["candidate_couplings_exact"]]
    if [str(x) for x in couplings1] != escape1["candidate_couplings_exact"]:
        raise RuntimeError("first path differs from its Arb-certified input")
    for label, couplings in (("first", couplings1), ("second", couplings2), ("third", couplings3), ("fourth", couplings4), ("fifth", couplings5)):
        if len(couplings) != 42 or couplings[-1] != 0 or any(x <= 0 for x in couplings[:-1]):
            raise RuntimeError(f"{label} path is not a strictly-positive 41-edge open path")
    if len({tuple(couplings1), tuple(couplings2), tuple(couplings3), tuple(couplings4), tuple(couplings5)}) != 5:
        raise RuntimeError("the five continuous escape paths are not pairwise distinct")
    if escape5.get("candidate_outside_frozen_canonical_pool") is not True:
        raise RuntimeError("fifth path is not certified outside the canonical inventory")

    column_order = parent_order + [ESCAPE_5_COLUMN]
    if len(column_order) != 188 or len(set(column_order)) != 187:
        raise RuntimeError("expanded physical pool must contain 188 unique columns")
    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [couplings1]
        + [all_columns[column] for column in added_columns]
        + [couplings2, couplings3, couplings4, couplings5]
    )
    if len(physical_columns) != 188:
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
        raise RuntimeError("row inventory differs from the certified 187-column design")

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

    sixth = np.empty((188, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((188, len(eighth_rows)), dtype=np.float64)
    for index, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[index] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (index + 1) % 16 == 0 or index == 187:
            print(f"Built physical feature columns {index + 1}/188", flush=True)

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
    if (m, n) != (2113, 188):
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
        "188col_fifth_continuous_escape_lp_candidate_below_one_third"
        if result.fun < 1 / 3 else "187col_fourth_continuous_escape_lp_above_one_third"
    )
    transcript = {
        "status": lp_status,
        "parent_186col_lp_sha256": hashes[LP_186.name],
        "parent_186col_dual_certificate_sha256": hashes[DUAL_187.name],
        "parent_152col_candidate_sha256": hashes[CANDIDATE_152.name],
        "cut_lp_transcript_sha256": hashes[CUT_LP.name],
        "cut_dual_certificate_sha256": hashes[CUT_DUAL.name],
        "first_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_1.name],
        "second_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_2.name],
        "third_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_3.name],
        "fourth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_4.name],
        "fifth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_5.name],
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
            "Binary64 HiGHS discovery on the fixed 2,113-row mixed-order design, adding a third "
            "continuous path whose positive pricing score against the exact 187-column dual was "
            "independently certified with 128-bit Arb. A sub-1/3 result is only a candidate until "
            "the exact rationalized mixture passes Arb on all 2,113 pinned rows and a complete "
            "63,133-orbit sixth-order audit. An above-cap result requires a new exact rational dual "
            "and independent Arb verification against all 188 physical columns."
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
            "parent_186col_lp_sha256": hashes[LP_186.name],
            "parent_186col_dual_certificate_sha256": hashes[DUAL_186.name],
            "first_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_1.name],
            "second_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_2.name],
            "third_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_3.name],
            "fourth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_4.name],
            "fifth_continuous_escape_arb_certificate_sha256": hashes[ESCAPE_5.name],
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
                "Exact rational probabilities obtained by normalizing binary64 188-column HiGHS "
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
