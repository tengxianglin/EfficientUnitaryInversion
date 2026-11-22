"""Sixth-only minimax reoptimization after Arb-certified canonical pricing escapes."""
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

ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DUAL_CERT = ROOT / "evidence/55probe_162col_sixth_only_dual_certificate_n21.json"
SIXTH_ONLY_LP = ROOT / "evidence/joint_low_six_lp_162col_sixth_only_n21.json"
PRICING_SCREEN = ROOT / "evidence/55probe_162col_sixth_only_dual_pricing_screen_n21.json"
PRICING_ARB = ROOT / "evidence/55probe_162col_sixth_only_dual_pricing_arb_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_lp_172col_sixth_only_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_172col_sixth_only_n21.json"
SIXTH_SCALE = Fraction(5, 19721)
EXPECTED_NEW_COLUMNS = 10


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    paths = (
        ESCAPE_CERT, PARENT_LP, CUT_LP, DUAL_CERT, SIXTH_ONLY_LP,
        PRICING_SCREEN, PRICING_ARB,
    )
    raw = [path.read_bytes() for path in paths]
    escape, parent_lp, cut_lp, dual, sixth_lp, screen, pricing = [
        json.loads(value) for value in raw
    ]
    hashes = {path.name: sha(value) for path, value in zip(paths, raw)}

    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
        raise RuntimeError("continuous path generator lacks its strict Arb certificate")
    if dual.get("continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_CERT.name]:
        raise RuntimeError("162-column dual does not pin the exact continuous escape generator")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (162, 2113):
        raise RuntimeError("unexpected 162-column parent LP dimensions")
    # The 162-column parent LP stores the canonical sixth-row inventory hash directly.
    if dual.get("status") != "strict_162col_2106row_sixth_only_minimax_obstruction" or not dual.get("complete"):
        raise RuntimeError("162-column sixth-only dual certificate is incomplete")
    if dual.get("lp_transcript_sha256") != hashes[SIXTH_ONLY_LP.name]:
        raise RuntimeError("sixth-only dual does not pin its LP transcript")
    if dual.get("parent_162col_lp_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("sixth-only dual does not pin the 162-column physical inventory")
    if dual.get("parent_152col_cut_lp_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("sixth-only dual does not pin the sixth-row inventory")
    if (dual.get("column_count"), dual.get("row_count")) != (162, 2106):
        raise RuntimeError("unexpected sixth-only dual dimensions")
    if (sixth_lp.get("columns"), sixth_lp.get("rows")) != (162, 2106):
        raise RuntimeError("unexpected sixth-only LP dimensions")
    if pricing.get("status") != "arb_positive_columns_found":
        raise RuntimeError("new pricing candidates lack strict Arb positivity")
    if pricing.get("dual_certificate_sha256") != hashes[DUAL_CERT.name]:
        raise RuntimeError("Arb pricing transcript does not pin the exact sixth-only dual")
    if pricing.get("lp_transcript_sha256") != hashes[SIXTH_ONLY_LP.name]:
        raise RuntimeError("Arb pricing transcript does not pin the sixth-only LP")
    if pricing.get("pricing_screen_sha256") != hashes[PRICING_SCREEN.name]:
        raise RuntimeError("Arb pricing transcript does not pin the binary64 screen")
    if screen.get("dual_certificate_sha256") != hashes[DUAL_CERT.name]:
        raise RuntimeError("binary64 pricing screen does not pin the exact sixth-only dual")
    if screen.get("lp_transcript_sha256") != hashes[SIXTH_ONLY_LP.name]:
        raise RuntimeError("binary64 pricing screen does not pin the sixth-only LP")
    if screen.get("parent_162col_lp_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("pricing screen does not pin the physical-pool LP")
    if screen.get("parent_sixth_row_inventory_sha256") != hashes[CUT_LP.name]:
        raise RuntimeError("pricing screen does not pin the sixth-row inventory")
    if screen.get("unused_column_count") != 1480 or screen.get("canonical_column_count") != 1641:
        raise RuntimeError("pricing screen did not cover the expected canonical pool")
    if pricing.get("candidates_checked") != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("expected ten independently Arb-checked candidates")
    if pricing.get("arb_certified_positive_count") != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("not all ten pricing candidates have strict positive Arb lower endpoints")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != dual.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical physical pool hash/count mismatch")
    if all_sha != screen.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("pricing screen and canonical physical pool hashes disagree")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    old_added = [int(x) for x in parent_lp["added_canonical_columns"]]
    escape_couplings = [Fraction(x) for x in escape["candidate_couplings_exact"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("malformed original 151-column canonical base")
    if parent_lp.get("column_order") != base_columns + [1641] + old_added:
        raise RuntimeError("parent LP physical column ordering is inconsistent")
    if dual.get("columns") != parent_lp.get("column_order"):
        raise RuntimeError("sixth-only dual and parent LP physical inventories disagree")
    if len(old_added) != 10 or len(set(old_added)) != 10:
        raise RuntimeError("malformed ten-column extension already in the 162-column pool")
    if set(base_columns) & set(old_added):
        raise RuntimeError("existing canonical additions overlap the original base")
    if [int(x) for x in parent_lp["base_columns"]] != base_columns:
        raise RuntimeError("162-column parent LP changed the original canonical base")

    priced_results = [item for item in pricing.get("results", []) if item.get("strictly_positive")]
    if len(priced_results) != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("the Arb transcript does not contain ten strictly positive columns")
    new_added = [int(item["column"]) for item in priced_results]
    if len(set(new_added)) != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("duplicate newly priced canonical columns")
    occupied = set(base_columns) | set(old_added)
    if occupied & set(new_added):
        raise RuntimeError("new pricing candidates overlap the existing 162-column pool")
    for item in priced_results:
        j = int(item["column"])
        if not 0 <= j < len(all_columns):
            raise RuntimeError(f"canonical column index out of range: {j}")
        if not np.array_equal(
            np.asarray(item["couplings"], dtype=np.float64),
            np.asarray(all_columns[j], dtype=np.float64),
        ):
            raise RuntimeError(f"Arb-priced coupling payload differs from frozen column {j}")

    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in old_added]
        + [all_columns[j] for j in new_added]
    )
    column_labels = base_columns + [1641] + old_added + new_added
    if len(physical_columns) != 172 or len(set(column_labels)) != 172:
        raise RuntimeError("expanded sixth-only physical pool must contain 172 unique columns")

    sixth_rows = [tuple(int(v) for v in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(v) for v in cut_lp["sixth_cut_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("the 645-row sixth-order cut inventory is incomplete or duplicated")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-order target mismatch")
    sixth_rows_sha = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    if sixth_rows_sha != sixth_lp.get("sixth_rows_sha256"):
        raise RuntimeError("sixth-only LP and pinned sixth-row inventory disagree")
    if sixth_rows_sha != parent_lp.get("sixth_rows_sha256"):
        raise RuntimeError("162-column parent LP and sixth-only LP use different sixth-row inventories")

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

    sixth = np.empty((172, len(sixth_rows)), dtype=np.float64)
    for j, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[j] = [orbit_minor(rotation, row) for row in sixth_rows]
        if (j + 1) % 16 == 0 or j == 171:
            print(f"Built sixth-order feature columns {j + 1}/172", flush=True)

    A = np.vstack([
        low.T / low_scale[:, None],
        sixth.T / float(SIXTH_SCALE),
    ])
    y = np.r_[
        low_target / low_scale,
        np.asarray([float(value) for value in sixth_targets]) / float(SIXTH_SCALE),
    ]
    row_blocks = {"low_complete": len(low_target), "sixth_selected_plus_all_cuts": len(sixth_rows)}
    m, n = A.shape
    if (m, n) != (2106, 172):
        raise RuntimeError(f"unexpected sixth-only LP dimensions: {(m, n)}")

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
        {"column": column_labels[j], "weight": float(weight)}
        for j, weight in enumerate(result.x[:-1]) if weight > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())
    transcript = {
        "status": "172col_sixth_only_lp_candidate_below_one_third" if result.fun < 1 / 3 else "172col_sixth_only_lp_above_one_third",
        "continuous_escape_arb_certificate_sha256": hashes[ESCAPE_CERT.name],
        "parent_162col_lp_sha256": hashes[PARENT_LP.name],
        "parent_sixth_only_dual_certificate_sha256": hashes[DUAL_CERT.name],
        "parent_sixth_only_lp_sha256": hashes[SIXTH_ONLY_LP.name],
        "pricing_screen_sha256": hashes[PRICING_SCREEN.name],
        "pricing_arb_sha256": hashes[PRICING_ARB.name],
        "parent_sixth_row_inventory_sha256": hashes[CUT_LP.name],
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "continuous_escape_column_index": 1641,
        "previous_added_canonical_columns": old_added,
        "added_canonical_columns": new_added,
        "column_order": column_labels,
        "sixth_rows_sha256": sixth_rows_sha,
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
            "Binary64 minimax discovery on 2,106 rows: all 1,461 second/fourth rows and 645 "
            "pinned sixth-order D42 orbits. The 172 physical columns comprise the 151-column "
            "canonical base, one exact continuous-path generator, ten earlier canonical additions, "
            "and ten new canonical columns whose reduced-cost scores were independently certified "
            "strictly positive by 128-bit Arb against the 162-column sixth-only dual. This is not "
            "a theorem; any sub-1/3 candidate requires exact probability rationalization, a fresh "
            "Arb audit of all 2,106 rows, and a complete 63,133-orbit sixth-order separation scan."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (column_labels[j], Fraction.from_float(float(weight)))
            for j, weight in enumerate(result.x[:-1]) if weight > 1e-10
        ]
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": column, "probability": str(weight / total)}
            for column, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized probabilities do not sum exactly to one")
        next_candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_out_sha,
            "continuous_escape_arb_certificate_sha256": hashes[ESCAPE_CERT.name],
            "parent_162col_lp_sha256": hashes[PARENT_LP.name],
            "parent_sixth_only_dual_certificate_sha256": hashes[DUAL_CERT.name],
            "parent_sixth_only_lp_sha256": hashes[SIXTH_ONLY_LP.name],
            "pricing_screen_sha256": hashes[PRICING_SCREEN.name],
            "pricing_arb_sha256": hashes[PRICING_ARB.name],
            "parent_sixth_row_inventory_sha256": hashes[CUT_LP.name],
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "continuous_escape_column_index": 1641,
            "escape_couplings_exact": [str(value) for value in escape_couplings],
            "previous_added_canonical_columns": old_added,
            "added_canonical_columns": new_added,
            "column_order": column_labels,
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
                "172-column, 2,106-row sixth-only discovery LP. The probability sum is exactly one. "
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
        "previous_added_canonical_columns": old_added,
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
