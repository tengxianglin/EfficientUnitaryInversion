"""Binary64 discovery LP after appending the ninth Arb-certified continuous path.

The solver is not a proof. An above-cap result requires a fresh rational dual
and independent Arb checks of all 192 columns; a below-cap result requires an
exact rational primal Arb audit and complete sixth-order separation.
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

PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_191col_eighth_continuous_escape_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
ESCAPE_PATHS = [
    ROOT / "evidence/continuous_path_dual_escape_arb_n21.json",
    ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/188col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/189col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/190col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/191col_continuous_dual_escape_arb_n21.json",
]
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_192col_ninth_continuous_escape_n21.json"

SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_json(path):
    raw = path.read_bytes()
    return json.loads(raw), sha(raw)


def main():
    parent_lp, parent_lp_sha = load_json(PARENT_LP)
    parent_dual, parent_dual_sha = load_json(PARENT_DUAL)
    candidate152, candidate152_sha = load_json(CANDIDATE_152)
    cut_lp, cut_lp_sha = load_json(CUT_LP)
    cut_dual, cut_dual_sha = load_json(CUT_DUAL)
    escapes, escape_hashes = zip(*(load_json(path) for path in ESCAPE_PATHS))
    escapes = list(escapes)
    escape_hashes = list(escape_hashes)
    seed_raw = SEED_POOL.read_bytes()
    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())

    if parent_lp.get("status") != "191col_eighth_continuous_escape_lp_above_one_third":
        raise RuntimeError("191-column parent LP is not the expected above-cap discovery")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (191, 2113):
        raise RuntimeError("unexpected 191-column parent dimensions")
    if parent_dual.get("status") != "strict_191col_2113row_eighth_continuous_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("191-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("191-column parent dual does not pin its LP")
    if parent_lp.get("parent_190col_lp_sha256") != parent_dual.get("parent_190col_lp_sha256"):
        raise RuntimeError("191-column LP/dual parent-LP ancestry mismatch")
    if parent_lp.get("parent_190col_dual_certificate_sha256") != parent_dual.get("parent_190col_dual_certificate_sha256"):
        raise RuntimeError("191-column LP/dual parent-dual ancestry mismatch")
    if parent_lp.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("191-column parent does not pin its 152-column ancestor")
    if parent_lp.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("191-column parent does not pin the exact cut design and dual")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut-design dual is not strictly Arb-certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("cut-design dual does not pin its LP")
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if parent_lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("191-column parent does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical inventory count/hash mismatch")

    for index, (escape, digest) in enumerate(zip(escapes, escape_hashes), 1):
        if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
            raise RuntimeError(f"continuous escape {index} lacks a strict Arb certificate")
        couplings = [Fraction(value) for value in escape["candidate_couplings_exact"]]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError(f"continuous escape {index} is not a positive 41-edge open path")
        if escape.get("candidate_outside_frozen_canonical_pool") is not True:
            raise RuntimeError(f"continuous escape {index} is not certified outside the canonical pool")
    if len({tuple(Fraction(v) for v in e["candidate_couplings_exact"]) for e in escapes}) != 9:
        raise RuntimeError("the nine Arb-certified escape paths are not pairwise distinct")

    escape9 = escapes[-1]
    if escape9.get("dual_certificate_sha256") != parent_dual_sha or escape9.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("ninth escape does not pin the exact 191-column parent dual/LP")
    if escape9.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("ninth escape does not pin the exact 2,113-row cut design")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != escape_hashes[0]:
        raise RuntimeError("152-column ancestor candidate does not pin the first escape")

    parent_order = [int(value) for value in parent_lp["column_order"]]
    if len(parent_order) != 191 or len(set(parent_order)) != 191:
        raise RuntimeError("191-column parent ordering is not unique")
    base_columns = [int(value) for value in parent_lp["base_columns"]]
    added_columns = [int(value) for value in parent_lp["added_canonical_columns"]]
    expected_parent_order = (
        base_columns + [1641] + added_columns + list(range(1642, 1649))
    )
    if parent_order != expected_parent_order or len(base_columns) != 151 or len(added_columns) != 32:
        raise RuntimeError("191-column parent physical-column order is inconsistent")

    escape_couplings = [
        [Fraction(value) for value in candidate152["escape_couplings_exact"]]
    ] + [
        [Fraction(value) for value in escape["candidate_couplings_exact"]]
        for escape in escapes[1:]
    ]
    if len(escape_couplings) != 9:
        raise RuntimeError("expected nine escape coupling vectors")
    column_order = parent_order + [1649]
    physical_columns = []
    for column in column_order:
        if column < CANONICAL_COUNT:
            physical_columns.append(all_columns[column])
        else:
            escape_index = column - CANONICAL_COUNT
            if not 0 <= escape_index < 9:
                raise RuntimeError(f"unknown physical column label {column}")
            physical_columns.append(escape_couplings[escape_index])
    if len(physical_columns) != 192 or len(column_order) != 192:
        raise RuntimeError("expanded physical pool must contain 192 columns")

    sixth_rows = [tuple(int(v) for v in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(v) for v in cut_lp["sixth_cut_targets"]]
    eighth_rows = [tuple(int(v) for v in row) for row in cut_lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(v) for v in cut_lp["selected_eighth_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("unexpected sixth-order row inventory")
    if len(eighth_rows) != 7 or len(eighth_targets) != 7:
        raise RuntimeError("unexpected selected eighth-order row inventory")
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
        raise RuntimeError("row inventory differs from the certified 191-column design")

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

    sixth = np.empty((192, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((192, len(eighth_rows)), dtype=np.float64)
    for index, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[index] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (index + 1) % 16 == 0 or index == 191:
            print(f"Built physical feature columns {index + 1}/192", flush=True)

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
    if (m, n) != (2113, 192):
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
    status = (
        "192col_ninth_continuous_escape_lp_candidate_below_one_third"
        if result.fun < 1 / 3 else "192col_ninth_continuous_escape_lp_above_one_third"
    )
    transcript = {
        "status": status,
        "parent_191col_lp_sha256": parent_lp_sha,
        "parent_191col_dual_certificate_sha256": parent_dual_sha,
        "parent_152col_candidate_sha256": candidate152_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "cut_dual_certificate_sha256": cut_dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_hashes,
        "ninth_continuous_escape_column_index": 1649,
        "ninth_continuous_escape_candidate_sha256": escape9.get("candidate_sha256"),
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "added_canonical_columns": added_columns,
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
            "Binary64 HiGHS discovery on the fixed 2,113-row mixed-order design after appending "
            "the ninth continuous path as physical column 1649. A sub-1/3 result is discovery only "
            "until its exact rationalized mixture passes Arb on all pinned rows and a complete "
            "63,133-orbit sixth-order audit. An above-cap result requires a new exact rational dual "
            "and independent Arb verification against all 192 physical columns."
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
        candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_sha,
            "parent_191col_lp_sha256": parent_lp_sha,
            "parent_191col_dual_certificate_sha256": parent_dual_sha,
            "continuous_escape_arb_certificate_sha256": escape_hashes,
            "ninth_continuous_escape_column_index": 1649,
            "ninth_continuous_escape_couplings_exact": [str(value) for value in escape_couplings[-1]],
            "seed_pool_sha256_le_f64": seed_sha,
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "added_canonical_columns": added_columns,
            "column_order": column_order,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_cut_rows": [list(row) for row in sixth_rows],
            "sixth_cut_targets": [str(value) for value in sixth_targets],
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "selected_eighth_targets": [str(value) for value in eighth_targets],
            "scope": (
                "Exact rational probabilities obtained by normalizing binary64 192-column HiGHS "
                "weights. This candidate is constrained only on the pinned 2,113 rows and requires "
                "independent Arb verification plus complete sixth-order separation."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": status,
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
