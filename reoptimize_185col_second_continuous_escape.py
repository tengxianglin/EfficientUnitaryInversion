"""Reoptimize the pinned 2,113-row EUI LP after a second Arb-certified path escape.

This is a binary64 HiGHS discovery step. A sub-1/3 output is not a theorem
until verify_185col_continuous_candidate_arb.py passes; an above-cap output
is not a theorem until verify_185col_continuous_dual_arb.py passes.
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

LP_184 = ROOT / "evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json"
DUAL_184 = ROOT / "evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
OLD_ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
NEW_ESCAPE_CERT = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_185col_second_continuous_escape_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_185col_second_continuous_escape_n21.json"

SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
OLD_ESCAPE_COLUMN = 1641
NEW_ESCAPE_COLUMN = 1642
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    raw = path.read_bytes()
    return raw, json.loads(raw)


def main():
    paths = (LP_184, DUAL_184, CANDIDATE_152, CUT_LP, CUT_DUAL,
             OLD_ESCAPE_CERT, NEW_ESCAPE_CERT, SEED_POOL)
    raw = {path: path.read_bytes() for path in paths}
    data = {path: (value if path.suffix == ".npy" else json.loads(value))
            for path, value in raw.items()}
    hashes = {path.name: sha(value) for path, value in raw.items()}

    parent_lp = data[LP_184]
    parent_dual = data[DUAL_184]
    candidate152 = data[CANDIDATE_152]
    cut_lp = data[CUT_LP]
    cut_dual = data[CUT_DUAL]
    old_escape = data[OLD_ESCAPE_CERT]
    new_escape = data[NEW_ESCAPE_CERT]

    if parent_lp.get("status") != "184col_full_sixth_cut_lp_above_one_third":
        raise RuntimeError("184-column parent LP is not the expected above-cap discovery")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (184, 2113):
        raise RuntimeError("unexpected 184-column parent dimensions")
    if parent_dual.get("status") != "strict_184col_2113row_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("184-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != hashes[LP_184.name]:
        raise RuntimeError("184-column dual does not pin its LP transcript")
    if parent_lp.get("parent_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("184-column LP does not pin the exact 152-column ancestor candidate")
    if parent_lp.get("current_152col_cut_lp_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("184-column LP does not pin the current 2,113-row cut inventory")
    if parent_lp.get("current_152col_cut_dual_certificate_sha256") != hashes[CUT_DUAL.name]:
        raise RuntimeError("184-column LP does not pin the 152-column cut dual")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column parent dual is not strictly certified")
    if cut_dual.get("lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("152-column parent dual does not pin the cut LP")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != hashes[OLD_ESCAPE_CERT.name]:
        raise RuntimeError("152-column candidate does not pin the original continuous escape")
    if old_escape.get("status") != "certified_continuous_path_dual_escape" or not old_escape.get("strictly_positive"):
        raise RuntimeError("original continuous escape lacks its Arb certificate")
    if new_escape.get("status") != "certified_continuous_path_dual_escape" or not new_escape.get("complete") or not new_escape.get("strictly_positive"):
        raise RuntimeError("second continuous escape lacks its strict Arb certificate")
    if new_escape.get("dual_certificate_sha256") != hashes[DUAL_184.name]:
        raise RuntimeError("second escape does not pin the exact 184-column dual")
    if new_escape.get("lp_transcript_sha256") != hashes[LP_184.name]:
        raise RuntimeError("second escape does not pin the exact 184-column LP")
    if new_escape.get("cut_lp_transcript_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("second escape does not pin the exact 2,113-row design")
    if parent_dual.get("continuous_escape_arb_certificate_sha256") != hashes[OLD_ESCAPE_CERT.name]:
        raise RuntimeError("184-column parent dual does not pin the first continuous escape")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool shape/hash mismatch")
    if parent_lp.get("seed_pool_sha256_le_f64") != seed_sha or parent_dual.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("184-column parent evidence does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    added_columns = [int(x) for x in parent_lp["added_canonical_columns"]]
    parent_order = [int(x) for x in parent_lp["column_order"]]
    expected_parent_order = base_columns + [OLD_ESCAPE_COLUMN] + added_columns
    if len(base_columns) != 151 or len(added_columns) != 32:
        raise RuntimeError("unexpected 184-column canonical inventory")
    if parent_order != expected_parent_order or len(set(parent_order)) != 184:
        raise RuntimeError("184-column parent ordering is inconsistent")

    old_couplings = [Fraction(x) for x in candidate152["escape_couplings_exact"]]
    if [str(x) for x in old_couplings] != old_escape["candidate_couplings_exact"]:
        raise RuntimeError("first continuous escape couplings do not match their Arb input")
    new_couplings = [Fraction(x) for x in new_escape["candidate_couplings_exact"]]
    if len(old_couplings) != 42 or len(new_couplings) != 42:
        raise RuntimeError("continuous paths must contain 42 entries")
    for label, couplings in (("first", old_couplings), ("second", new_couplings)):
        if couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError(f"{label} continuous path is not a strictly-positive 41-edge open path")
    if old_couplings == new_couplings:
        raise RuntimeError("second continuous path duplicates the first")
    if new_escape.get("candidate_outside_frozen_canonical_pool") is not True:
        raise RuntimeError("second continuous path is not certified outside the canonical inventory")

    column_order = parent_order + [NEW_ESCAPE_COLUMN]
    if len(column_order) != 185 or len(set(column_order)) != 185:
        raise RuntimeError("expanded physical pool must contain 185 unique columns")
    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [old_couplings]
        + [all_columns[column] for column in added_columns]
        + [new_couplings]
    )
    if len(physical_columns) != 185:
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
        raise RuntimeError("row inventory differs from the certified 184-column design")

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

    sixth = np.empty((185, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((185, len(eighth_rows)), dtype=np.float64)
    for index, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[index] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (index + 1) % 16 == 0 or index == 184:
            print(f"Built physical feature columns {index + 1}/185", flush=True)

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
    if (m, n) != (2113, 185):
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
        "185col_second_continuous_escape_lp_candidate_below_one_third"
        if result.fun < 1 / 3 else "185col_second_continuous_escape_lp_above_one_third"
    )
    transcript = {
        "status": lp_status,
        "parent_184col_lp_sha256": hashes[LP_184.name],
        "parent_184col_dual_certificate_sha256": hashes[DUAL_184.name],
        "parent_152col_candidate_sha256": hashes[CANDIDATE_152.name],
        "cut_lp_transcript_sha256": hashes[CUT_LP.name],
        "cut_dual_certificate_sha256": hashes[CUT_DUAL.name],
        "first_continuous_escape_arb_certificate_sha256": hashes[OLD_ESCAPE_CERT.name],
        "second_continuous_escape_arb_certificate_sha256": hashes[NEW_ESCAPE_CERT.name],
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "first_continuous_escape_column_index": OLD_ESCAPE_COLUMN,
        "added_canonical_columns": added_columns,
        "second_continuous_escape_column_index": NEW_ESCAPE_COLUMN,
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
            "Binary64 HiGHS discovery on the fixed 2,113-row mixed-order design, adding a second "
            "continuous path whose positive pricing score against the exact 184-column dual was "
            "independently certified with 128-bit Arb. A sub-1/3 result is only a candidate until "
            "the exact rationalized mixture passes Arb on all 2,113 pinned rows and a complete "
            "63,133-orbit sixth-order audit. An above-cap result requires a new exact rational dual "
            "and independent Arb verification against all 185 physical columns."
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
            "parent_184col_lp_sha256": hashes[LP_184.name],
            "parent_184col_dual_certificate_sha256": hashes[DUAL_184.name],
            "first_continuous_escape_arb_certificate_sha256": hashes[OLD_ESCAPE_CERT.name],
            "second_continuous_escape_arb_certificate_sha256": hashes[NEW_ESCAPE_CERT.name],
            "seed_pool_sha256_le_f64": seed_sha,
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "first_continuous_escape_column_index": OLD_ESCAPE_COLUMN,
            "first_continuous_escape_couplings_exact": [str(x) for x in old_couplings],
            "added_canonical_columns": added_columns,
            "second_continuous_escape_column_index": NEW_ESCAPE_COLUMN,
            "second_continuous_escape_couplings_exact": [str(x) for x in new_couplings],
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
                "Exact rational probabilities obtained by normalizing binary64 185-column HiGHS "
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
