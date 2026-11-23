"""Mixed-order minimax reoptimization after Arb-certified pricing against the 185-column dual."""
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

PARENT_LP = ROOT / "evidence/joint_low_six_lp_185col_mixed_order_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_185col_mixed_order_dual_certificate_n21.json"
PRICING_SCREEN = ROOT / "evidence/55probe_185col_mixed_order_dual_pricing_screen_n21.json"
PRICING_ARB = ROOT / "evidence/55probe_185col_mixed_order_dual_pricing_arb_n21.json"
PARENT_182_LP = ROOT / "evidence/joint_low_six_lp_182col_sixth_only_n21.json"
PARENT_182_DUAL = ROOT / "evidence/55probe_182col_sixth_only_dual_certificate_n21.json"
PARENT_162_LP = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_lp_186col_mixed_order_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_186col_mixed_order_n21.json"
SIXTH_SCALE = Fraction(5, 19721)
EXPECTED_NEW_COLUMNS = 1


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    paths = (
        PARENT_LP, PARENT_DUAL, PRICING_SCREEN, PRICING_ARB,
        PARENT_182_LP, PARENT_182_DUAL, PARENT_162_LP, CUT_LP, ESCAPE_CERT,
    )
    raw = [path.read_bytes() for path in paths]
    parent, dual, screen, pricing, parent182, dual182, parent162, cut_lp, escape = [
        json.loads(value) for value in raw
    ]
    hashes = {path.name: sha(value) for path, value in zip(paths, raw)}

    if (parent.get("columns"), parent.get("rows")) != (185, 2106):
        raise RuntimeError("unexpected parent 185-column LP dimensions")
    if parent.get("status") != "185col_mixed_order_lp_above_one_third":
        raise RuntimeError("parent 185-column LP is not the expected above-cap discovery")
    if dual.get("status") != "strict_185col_2106row_mixed_order_minimax_obstruction" or not dual.get("complete"):
        raise RuntimeError("parent 185-column mixed-order Arb dual is incomplete")
    if dual.get("lp_transcript_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("parent 185-column dual does not pin its LP")
    if dual.get("parent_182col_lp_sha256") != hashes[PARENT_182_LP.name]:
        raise RuntimeError("parent 185-column dual does not pin the 182-column LP")
    if dual.get("parent_182col_dual_certificate_sha256") != hashes[PARENT_182_DUAL.name]:
        raise RuntimeError("parent 185-column dual does not pin the 182-column Arb certificate")
    if parent.get("parent_182col_lp_sha256") != hashes[PARENT_182_LP.name]:
        raise RuntimeError("parent 185-column LP does not pin the 182-column LP")
    if parent.get("parent_182col_dual_certificate_sha256") != hashes[PARENT_182_DUAL.name]:
        raise RuntimeError("parent 185-column LP does not pin the 182-column Arb certificate")
    if parent182.get("status") != "182col_sixth_only_lp_above_one_third" or (parent182.get("columns"), parent182.get("rows")) != (182, 2106):
        raise RuntimeError("unexpected 182-column ancestor LP")
    if dual182.get("status") != "strict_182col_2106row_mixed_order_minimax_obstruction" or not dual182.get("complete"):
        raise RuntimeError("182-column ancestor Arb certificate is incomplete")
    if dual182.get("lp_transcript_sha256") != hashes[PARENT_182_LP.name]:
        raise RuntimeError("182-column ancestor dual does not pin its LP")
    if parent.get("parent_172col_lp_sha256") != parent182.get("parent_172col_lp_sha256"):
        raise RuntimeError("185-column LP and 182-column parent disagree on 172-column ancestor")
    if dual.get("parent_172col_lp_sha256") != parent182.get("parent_172col_lp_sha256"):
        raise RuntimeError("185-column dual and 182-column parent disagree on 172-column ancestor")
    # The 185-column LP pins the 172-column LP but omits the redundant 172-dual hash;
    # the 185-column Arb certificate carries that hash and is checked below.
    if dual.get("parent_172col_dual_certificate_sha256") != parent182.get("parent_172col_dual_certificate_sha256"):
        raise RuntimeError("185-column dual and 182-column parent disagree on 172-column dual")
    if parent.get("parent_162col_lp_sha256") != hashes[PARENT_162_LP.name]:
        raise RuntimeError("parent 185-column LP does not pin its 162-column ancestor")
    if dual.get("parent_162col_lp_sha256") != hashes[PARENT_162_LP.name]:
        raise RuntimeError("parent 185-column dual does not pin its 162-column ancestor")
    if parent.get("parent_sixth_row_inventory_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("parent 185-column LP does not pin the sixth-row inventory")
    if dual.get("parent_sixth_row_inventory_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("parent 185-column dual does not pin the sixth-row inventory")
    if dual.get("continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_CERT.name]:
        raise RuntimeError("parent 185-column dual does not pin the continuous-path Arb certificate")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
        raise RuntimeError("continuous path generator lacks its strict Arb certificate")
    if parent162.get("columns") != 162 or parent162.get("rows") != 2113:
        raise RuntimeError("unexpected 162-column physical ancestor dimensions")

    if pricing.get("status") != "arb_positive_columns_found":
        raise RuntimeError("185-column Arb pricing transcript is incomplete")
    if pricing.get("certificate_sha256") != hashes[PARENT_DUAL.name]:
        raise RuntimeError("pricing transcript does not pin the exact 185-column dual")
    if pricing.get("lp_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("pricing transcript does not pin the 185-column LP")
    if pricing.get("pricing_screen_sha256") != hashes[PRICING_SCREEN.name]:
        raise RuntimeError("pricing transcript does not pin the binary64 screen")
    if screen.get("certificate_sha256") != hashes[PARENT_DUAL.name]:
        raise RuntimeError("binary64 screen does not pin the exact 185-column dual")
    if screen.get("lp_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("binary64 screen does not pin the 185-column LP")
    if screen.get("unused_column_count") != 1457 or screen.get("canonical_column_count") != 1641:
        raise RuntimeError("unexpected frozen canonical-pool pricing dimensions")
    if pricing.get("candidates_checked") != EXPECTED_NEW_COLUMNS or pricing.get("arb_certified_positive_count") != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("expected one strict Arb-positive canonical pricing column")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != parent.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical pool hash/count mismatch")
    if all_sha != dual.get("canonical_all_columns_sha256_le_f64") or all_sha != screen.get("canonical_pool_sha256"):
        raise RuntimeError("parent dual, pricing screen, and expanded LP use different canonical pools")

    base_columns = [int(x) for x in parent["base_columns"]]
    previous_added = [int(x) for x in parent["previous_added_canonical_columns"]] + [
        int(x) for x in parent["added_canonical_columns"]
    ]
    escape_couplings = [Fraction(x) for x in escape["candidate_couplings_exact"]]
    new_results = [item for item in pricing.get("results", []) if item.get("strictly_positive")]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("malformed 151-column canonical base")
    if len(previous_added) != 33 or len(set(previous_added)) != 33:
        raise RuntimeError("malformed 33-column prior extension")
    new_added = [int(item["column"]) for item in new_results]
    if len(new_added) != EXPECTED_NEW_COLUMNS or len(set(new_added)) != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("malformed new one-column extension")
    if (set(base_columns) & set(previous_added)) or (set(base_columns) & set(new_added)) or (set(previous_added) & set(new_added)):
        raise RuntimeError("canonical physical column inventories overlap")
    parent_order = base_columns + [1641] + previous_added
    if parent.get("column_order") != parent_order or dual.get("columns") != parent_order:
        raise RuntimeError("parent 185-column physical ordering mismatch")
    column_order = parent_order + new_added
    if len(column_order) != 186 or len(set(column_order)) != 186:
        raise RuntimeError("expanded 186-column physical inventory mismatch")
    for item in new_results:
        j = int(item["column"])
        if not np.array_equal(
            np.asarray(item["couplings"], dtype=np.float64),
            np.asarray(all_columns[j], dtype=np.float64),
        ):
            raise RuntimeError(f"Arb-priced coupling payload differs from frozen canonical column {j}")

    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in previous_added]
        + [all_columns[j] for j in new_added]
    )
    if len(physical_columns) != 186:
        raise RuntimeError("expanded physical column count mismatch")

    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(x) for x in cut_lp["sixth_cut_targets"]]
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    if len(sixth_rows) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("incomplete or duplicated sixth-order row inventory")
    if sixth_hash != parent.get("sixth_rows_sha256"):
        raise RuntimeError("parent and expanded LP sixth-row inventories disagree")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-order target mismatch")

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

    sixth = np.empty((186, len(sixth_rows)), dtype=np.float64)
    for j, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[j] = [orbit_minor(rotation, row) for row in sixth_rows]
        if (j + 1) % 16 == 0 or j == 185:
            print(f"Built sixth-order feature columns {j + 1}/186", flush=True)

    A = np.vstack([low.T / low_scale[:, None], sixth.T / float(SIXTH_SCALE)])
    y = np.r_[
        low_target / low_scale,
        np.asarray([float(value) for value in sixth_targets]) / float(SIXTH_SCALE),
    ]
    row_blocks = {"low_complete": len(low_target), "sixth_selected_plus_all_cuts": len(sixth_rows)}
    m, n = A.shape
    if (m, n) != (2106, 186):
        raise RuntimeError(f"unexpected mixed-order LP dimensions: {(m, n)}")

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
        {"column": column_order[j], "weight": float(weight)}
        for j, weight in enumerate(result.x[:-1]) if weight > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())
    transcript = {
        "status": "186col_mixed_order_lp_candidate_below_one_third" if result.fun < 1 / 3 else "186col_mixed_order_lp_above_one_third",
        "parent_185col_lp_sha256": hashes[PARENT_LP.name],
        "parent_185col_dual_certificate_sha256": hashes[PARENT_DUAL.name],
        "pricing_screen_sha256": hashes[PRICING_SCREEN.name],
        "pricing_arb_sha256": hashes[PRICING_ARB.name],
        "parent_182col_lp_sha256": hashes[PARENT_182_LP.name],
        "parent_182col_dual_certificate_sha256": hashes[PARENT_182_DUAL.name],
        "parent_162col_lp_sha256": hashes[PARENT_162_LP.name],
        "parent_sixth_row_inventory_sha256": hashes[CUT_LP.name],
        "continuous_escape_arb_certificate_sha256": hashes[ESCAPE_CERT.name],
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "continuous_escape_column_index": 1641,
        "previous_added_canonical_columns": previous_added,
        "added_canonical_columns": new_added,
        "column_order": column_order,
        "sixth_rows_sha256": sixth_hash,
        "matrix_and_target_sha256_le_f64": matrix_sha,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "objective": float(result.fun),
        "recomputed_max": float(residual.max()),
        "block_maxima": {
            name: float(residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
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
            "Binary64 minimax discovery on 2,106 rows: all 1,461 second/fourth rows and 645 pinned "
            "sixth-order D42 orbits. The 186 physical columns comprise the 151-column canonical base, "
            "one exact continuous-path generator, thirty-three earlier canonical additions, and one new "
            "canonical column whose reduced-cost score was independently certified strictly positive "
            "by 128-bit Arb against the parent 185-column mixed-order dual. This is not a theorem; any "
            "sub-1/3 candidate requires exact probability rationalization, a fresh Arb audit of all "
            "2,106 rows, and a complete 63,133-orbit sixth-order separation scan."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (column_order[j], Fraction.from_float(float(weight)))
            for j, weight in enumerate(result.x[:-1]) if weight > 1e-10
        ]
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": col, "probability": str(weight / total)}
            for col, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized probabilities do not sum exactly to one")
        next_candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_out_sha,
            "parent_185col_lp_sha256": hashes[PARENT_LP.name],
            "parent_185col_dual_certificate_sha256": hashes[PARENT_DUAL.name],
            "pricing_screen_sha256": hashes[PRICING_SCREEN.name],
            "pricing_arb_sha256": hashes[PRICING_ARB.name],
            "parent_182col_lp_sha256": hashes[PARENT_182_LP.name],
            "parent_182col_dual_certificate_sha256": hashes[PARENT_182_DUAL.name],
            "parent_162col_lp_sha256": hashes[PARENT_162_LP.name],
            "parent_sixth_row_inventory_sha256": hashes[CUT_LP.name],
            "continuous_escape_arb_certificate_sha256": hashes[ESCAPE_CERT.name],
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "continuous_escape_column_index": 1641,
            "escape_couplings_exact": [str(value) for value in escape_couplings],
            "previous_added_canonical_columns": previous_added,
            "added_canonical_columns": new_added,
            "column_order": column_order,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "low_complete_row_count": 1461,
            "sixth_cut_rows": [list(row) for row in sixth_rows],
            "sixth_cut_targets": [str(value) for value in sixth_targets],
            "sixth_cut_count": len(sixth_rows),
            "scope": (
                "Exact rational probabilities obtained by normalizing binary64 weights from the "
                "186-column, 2,106-row mixed-order discovery LP. The probability sum is exactly one. "
                "This candidate is constrained only on the pinned 2,106 rows and requires a fresh "
                "128-bit Arb audit plus a complete 63,133-orbit sixth-order separation scan."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(next_candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": transcript["status"],
        "columns": n,
        "rows": m,
        "previous_added_canonical_columns": previous_added,
        "new_added_canonical_columns": new_added,
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
