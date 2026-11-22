"""Reoptimize the 162-column pool on low-order plus sixth-order rows only.

This removes the seven selected eighth-order rows from the 2,113-row mixed
design, so the resulting dual can directly answer the sixth-only scope question.
"""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from joint_low_six_eighth_lp import matrix, orbit_minor
from screen_ising_sixth_moments import target

LP162_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CERT162_PATH = ROOT / "evidence/55probe_162col_full_sixth_cut_dual_certificate_n21.json"
CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
PRICING_ARB_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_pricing_arb_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_lp_162col_sixth_only_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_162col_sixth_only_n21.json"
SIXTH_SCALE = Fraction(5, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    paths = (LP162_PATH, CERT162_PATH, CANDIDATE_PATH, CUT_LP_PATH, PRICING_ARB_PATH)
    raw = [path.read_bytes() for path in paths]
    lp162, cert162, candidate, cut_lp, pricing_arb = [json.loads(value) for value in raw]
    hashes = {path.name: sha(value) for path, value in zip(paths, raw)}

    if (lp162.get("columns"), lp162.get("rows")) != (162, 2113):
        raise RuntimeError("unexpected parent 162-column mixed-order LP")
    if cert162.get("status") != "strict_162col_2113row_minimax_obstruction" or not cert162.get("complete"):
        raise RuntimeError("parent 162-column mixed-order certificate is incomplete")
    if cert162.get("lp_transcript_sha256") != hashes[LP162_PATH.name]:
        raise RuntimeError("162-column certificate does not pin parent LP")
    if lp162.get("parent_candidate_sha256") != hashes[CANDIDATE_PATH.name]:
        raise RuntimeError("162-column LP does not pin parent exact candidate")
    sixth_rows_check = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    eighth_rows_check = [tuple(int(x) for x in row) for row in cut_lp["selected_eighth_rows"]]
    sixth_hash_check = sha(json.dumps([list(x) for x in sixth_rows_check], separators=(",", ":")).encode())
    eighth_hash_check = sha(json.dumps([list(x) for x in eighth_rows_check], separators=(",", ":")).encode())
    if sixth_hash_check != lp162.get("sixth_rows_sha256") or eighth_hash_check != lp162.get("eighth_rows_sha256"):
        raise RuntimeError("current parent LP row inventory differs from the pinned 162-column design")
    if lp162.get("pricing_arb_sha256") != hashes[PRICING_ARB_PATH.name]:
        raise RuntimeError("162-column LP does not pin its Arb pricing transcript")
    if pricing_arb.get("status") != "arb_positive_columns_found":
        raise RuntimeError("ten-column pricing transcript is not successful")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp162["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen canonical pool hash/count mismatch")
    base_columns = [int(x) for x in lp162["base_columns"]]
    added_columns = [int(x) for x in lp162["added_canonical_columns"]]
    column_order = [int(x) for x in lp162["column_order"]]
    if len(base_columns) != 151 or len(added_columns) != 10:
        raise RuntimeError("unexpected 162-column generator inventory")
    if column_order != base_columns + [1641] + added_columns:
        raise RuntimeError("162-column order mismatch")
    priced = [int(x["column"]) for x in pricing_arb["results"] if x.get("strictly_positive")]
    if priced != added_columns:
        raise RuntimeError("added columns differ from the ten Arb-priced escapes")
    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in added_columns]
    )
    if len(physical_columns) != 162:
        raise RuntimeError("wrong physical pool size")

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
        raise RuntimeError("unexpected complete low-order row count")

    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(x) for x in cut_lp["sixth_cut_targets"]]
    if len(sixth_rows) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("unexpected sixth-order row inventory")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-order target mismatch")
    sixth = np.empty((162, len(sixth_rows)), dtype=np.float64)
    for j, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[j] = [orbit_minor(rotation, row) for row in sixth_rows]
        if (j + 1) % 16 == 0 or j == 161:
            print(f"Built sixth-only feature columns {j + 1}/162", flush=True)

    sixth_scale = np.full(len(sixth_rows), float(SIXTH_SCALE))
    A = np.vstack([low.T / low_scale[:, None], sixth.T / sixth_scale[:, None]])
    y = np.r_[
        low_target / low_scale,
        np.asarray([float(x) for x in sixth_targets]) / sixth_scale,
    ]
    if A.shape != (2106, 162):
        raise RuntimeError(f"unexpected sixth-only LP dimensions {A.shape}")

    m, n = A.shape
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
    dual_z = result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]
    dual_objective = float(result.eqlin.marginals[0] + np.dot(dual_z, y))
    support = [
        {"column": column_order[j], "weight": float(w)}
        for j, w in enumerate(result.x[:-1]) if w > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())
    sixth_sha = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    transcript = {
        "status": "162col_sixth_only_lp_above_one_third" if result.fun > 1 / 3 else "162col_sixth_only_lp_at_or_below_one_third",
        "parent_162col_lp_sha256": hashes[LP162_PATH.name],
        "parent_162col_dual_certificate_sha256": hashes[CERT162_PATH.name],
        "parent_152col_cut_lp_sha256": hashes[CUT_LP_PATH.name],
        "parent_candidate_sha256": hashes[CANDIDATE_PATH.name],
        "pricing_arb_sha256": hashes[PRICING_ARB_PATH.name],
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": {"low_complete": 1461, "sixth_selected_plus_all_cuts": 645},
        "base_columns": base_columns,
        "continuous_escape_column_index": 1641,
        "added_canonical_columns": added_columns,
        "column_order": column_order,
        "sixth_rows_sha256": sixth_sha,
        "matrix_and_target_sha256_le_f64": matrix_sha,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "objective": float(result.fun),
        "recomputed_max": float(residual.max()),
        "block_maxima": {
            "low_complete": float(residual[:1461].max()),
            "sixth_selected_plus_all_cuts": float(residual[1461:].max()),
        },
        "positive_support": support,
        "dual_discovery": {
            "z_l1_norm": float(np.abs(dual_z).sum()),
            "objective": dual_objective,
            "primal_dual_gap": abs(float(result.fun) - dual_objective),
            "inequality_marginals": [float(x) for x in result.ineqlin.marginals],
            "equality_marginal": float(result.eqlin.marginals[0]),
        },
        "scope": (
            "Binary64 minimax discovery on a sixth-only 2,106-row design: all 1,461 complete "
            "second/fourth rows and 645 sixth-order rows, with no eighth-order rows. If the "
            "rationalized dual is Arb-certified, its lower bound will apply to the complete "
            "sixth-order objective for this fixed 162-column pool because all 645 sixth rows "
            "are members of the complete 63,133-orbit domain. This transcript alone is not a theorem."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (column_order[j], Fraction.from_float(float(w)))
            for j, w in enumerate(result.x[:-1]) if w > 1e-10
        ]
        total = sum((w for _, w in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": col, "probability": str(weight / total)}
            for col, weight in raw_weights
        ]
        if sum((Fraction(x["probability"]) for x in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized probabilities do not sum to one")
        out = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_out_sha,
            "parent_162col_lp_sha256": hashes[LP162_PATH.name],
            "parent_162col_dual_certificate_sha256": hashes[CERT162_PATH.name],
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "continuous_escape_column_index": 1641,
            "escape_couplings_exact": [str(x) for x in escape_couplings],
            "added_canonical_columns": added_columns,
            "column_order": column_order,
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_rows_sha256": sixth_sha,
            "sixth_rows": [list(x) for x in sixth_rows],
            "sixth_targets": [str(x) for x in sixth_targets],
            "scope": (
                "Exact rationalized probability candidate for the pinned 2,106-row sixth-only "
                "design. Requires a complete Arb row audit and a complete 63,133-orbit sixth scan."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(out, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": transcript["status"],
        "columns": n,
        "rows": m,
        "objective": float(result.fun),
        "recomputed_max": float(residual.max()),
        "block_maxima": transcript["block_maxima"],
        "support_size": len(support),
        "primal_dual_gap": transcript["dual_discovery"]["primal_dual_gap"],
        "candidate_written": candidate_written,
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if candidate_written else None,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
