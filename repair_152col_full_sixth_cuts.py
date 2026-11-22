"""Cutting-plane LP repair using every violation from the complete sixth scan.

The input 152-column candidate is first exhaustively screened in binary64.
All sixth-order orbit rows with residual >= 1/3 are added to the existing
1,779-row design (deduplicated), then the same 152 physical generators are
reoptimized. This is a discovery LP; any resulting rational candidate needs
a new Arb audit and a fresh complete-sixth scan.
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
from joint_low_six_eighth_lp import EIGHTH_ROWS, matrix, orbit_minor

CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json"
DUAL_IN = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_IN = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SIXTH_SCAN = ROOT / "evidence/candidate_152col_complete_sixth_binary64_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_152col_full_sixth_cuts_n21.json"
SIXTH_SCALE = Fraction(5, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    candidate_raw, lp_raw, dual_raw, escape_raw, scan_raw = (
        path.read_bytes() for path in (CANDIDATE_IN, LP_IN, DUAL_IN, ESCAPE_IN, SIXTH_SCAN)
    )
    candidate, parent_lp, dual, escape, scan = (
        json.loads(raw) for raw in (candidate_raw, lp_raw, dual_raw, escape_raw, scan_raw)
    )
    candidate_sha, lp_sha, dual_sha, escape_sha, scan_sha = map(
        sha, (candidate_raw, lp_raw, dual_raw, escape_raw, scan_raw)
    )
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate does not pin its parent 152-column LP")
    if candidate.get("parent_dual_certificate_sha256") != dual_sha:
        raise RuntimeError("candidate does not pin the 151-column parent dual")
    if candidate.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("candidate does not pin the Arb escape certificate")
    if scan.get("candidate_input_sha256") != candidate_sha or scan.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("complete sixth scan does not pin the exact 152-column candidate")
    if scan.get("status") != "complete_sixth_binary64_violations_found" or not scan.get("complete"):
        raise RuntimeError("expected an exhaustive sixth scan with violations")
    violations = scan.get("violating_orbits", [])
    if len(violations) != scan.get("violating_orbit_count_at_or_above_one_third"):
        raise RuntimeError("complete sixth scan did not persist every violating orbit")
    if len(violations) != 334:
        raise RuntimeError(f"unexpected number of sixth cuts: {len(violations)}")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != candidate["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen canonical pool hash/count mismatch")
    base_columns = [int(x) for x in candidate["base_columns"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("unexpected 151-column parent pool")
    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("candidate and Arb escape couplings disagree")
    physical_columns = [all_columns[j] for j in base_columns] + [escape_couplings]
    if len(physical_columns) != 152:
        raise RuntimeError("expanded physical pool must contain 152 columns")

    sixth_rows = []
    sixth_targets = []
    seen = {}
    groups = [
        (candidate["sixth_probe_rows"], candidate["sixth_probe_targets"]),
        (candidate["sixth_full_audit_separator_rows"], candidate["sixth_full_audit_separator_targets"]),
        (candidate["sixth_prefix_separator_rows"], candidate["sixth_prefix_separator_targets"]),
        (candidate["sixth_additional_full_audit_separator_rows"], candidate["sixth_additional_full_audit_separator_targets"]),
    ]
    screen_rows = json.loads((ROOT / "evidence/sixth_moment_screen_n21.json").read_text())["records"]
    groups.insert(0, (
        [row["indices"] for row in screen_rows],
        [row["target"] for row in screen_rows],
    ))
    for rows, targets in groups:
        if len(rows) != len(targets):
            raise RuntimeError("sixth row/target lengths disagree")
        for row, value in zip(rows, targets):
            key = tuple(int(x) for x in row)
            exact_target = Fraction(value)
            if target(key) != exact_target:
                raise RuntimeError(f"incorrect sixth target for {key}")
            if key in seen and seen[key] != exact_target:
                raise RuntimeError(f"duplicate sixth row has inconsistent target: {key}")
            if key not in seen:
                seen[key] = exact_target
                sixth_rows.append(key)
                sixth_targets.append(exact_target)
    original_sixth_count = len(sixth_rows)
    new_cuts = []
    for item in violations:
        row = tuple(int(x) for x in item["indices"])
        exact_target = Fraction(item["target"])
        if target(row) != exact_target:
            raise RuntimeError(f"wrong target in violation cut {row}")
        if row not in seen:
            seen[row] = exact_target
            sixth_rows.append(row)
            sixth_targets.append(exact_target)
            new_cuts.append(row)
    if original_sixth_count != 311:
        raise RuntimeError(f"unexpected original sixth row count: {original_sixth_count}")
    if len(sixth_rows) != original_sixth_count + len(new_cuts):
        raise RuntimeError("sixth cut deduplication failed")

    system = FourthMoments(21)
    system.exact_target_check()
    low = np.asarray([
        system.features(np.asarray(list(map(float, c))))
        for c in physical_columns
    ])
    low_target = system.target.copy()
    low_scale = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]
    if len(low_target) != 1461:
        raise RuntimeError("unexpected complete second/fourth row count")

    sixth = np.empty((len(physical_columns), len(sixth_rows)), dtype=np.float64)
    eighth_rows = [tuple(row) for row in candidate["selected_eighth_rows"]]
    if [list(row) for row in eighth_rows] != EIGHTH_ROWS:
        raise RuntimeError("selected eighth rows changed")
    eighth_targets = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    eighth = np.empty((len(physical_columns), len(eighth_rows)), dtype=np.float64)
    for j, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[j] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[j] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (j + 1) % 16 == 0:
            print(f"Built physical feature columns {j + 1}/{len(physical_columns)}", flush=True)

    sixth_scale = np.full(len(sixth_rows), float(SIXTH_SCALE))
    eighth_scale = np.full(len(eighth_rows), 1 / 19721)
    A = np.vstack([
        low.T / low_scale[:, None],
        sixth.T / sixth_scale[:, None],
        eighth.T / eighth_scale[:, None],
    ])
    y = np.r_[
        low_target / low_scale,
        np.asarray([float(x) for x in sixth_targets]) / sixth_scale,
        np.asarray([float(x) for x in eighth_targets]) / eighth_scale,
    ]
    row_blocks = {"low_complete": len(low_target), "sixth_selected_plus_all_cuts": len(sixth_rows), "eighth_selected": len(eighth_rows)}
    m, n = A.shape
    if n != 152 or m != 1461 + len(sixth_rows) + len(eighth_rows):
        raise RuntimeError("unexpected expanded LP dimensions")

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

    initial_probabilities = {
        int(row["column"]): Fraction(row["probability"])
        for row in candidate["exact_probabilities"]
    }
    initial_weights = np.zeros(n)
    column_position = {column: j for j, column in enumerate(base_columns)}
    for column, probability in initial_probabilities.items():
        if column == 1641:
            initial_weights[-1] = float(probability)
        else:
            initial_weights[column_position[column]] = float(probability)
    initial_residual = np.abs(A @ initial_weights - y)
    optimized_residual = np.abs(A @ result.x[:-1] - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    support = [
        {"column": base_columns[j] if j < 151 else "continuous_escape", "weight": float(w)}
        for j, w in enumerate(result.x[:-1]) if w > 1e-10
    ]
    transcript = {
        "status": "full_sixth_cut_lp_candidate_below_one_third" if result.fun < 1 / 3 else "full_sixth_cut_lp_above_one_third",
        "parent_candidate_sha256": candidate_sha,
        "parent_lp_sha256": lp_sha,
        "parent_dual_certificate_sha256": dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "complete_sixth_binary64_scan_sha256": scan_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "base_columns": base_columns,
        "escape_couplings_exact": [str(x) for x in escape_couplings],
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "original_sixth_rows": original_sixth_count,
        "complete_sixth_violations": len(violations),
        "new_unique_sixth_cuts": len(new_cuts),
        "total_sixth_rows_after_deduplication": len(sixth_rows),
        "new_sixth_cut_rows": [list(row) for row in new_cuts],
        "sixth_cut_rows": [list(row) for row in sixth_rows],
        "sixth_cut_targets": [str(x) for x in sixth_targets],
        "selected_eighth_rows": [list(row) for row in eighth_rows],
        "selected_eighth_targets": [str(x) for x in eighth_targets],
        "solver": "scipy.optimize.linprog(method=highs), binary64 cutting-plane discovery only",
        "initial_candidate_max_on_expanded_rows": float(initial_residual.max()),
        "initial_candidate_sixth_max_on_expanded_rows": float(initial_residual[cuts[1]:cuts[2]].max()),
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized_residual.max()),
        "expanded_block_maxima": {
            name: float(optimized_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "positive_support": support,
        "dual_discovery": {
            "z_l1_norm": float(np.abs(result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]).sum()),
            "objective": float(result.eqlin.marginals[0] + np.dot(result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:], y)),
            "primal_dual_gap": abs(float(result.fun) - float(result.eqlin.marginals[0] + np.dot(result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:], y))),
            "inequality_marginals": [float(x) for x in result.ineqlin.marginals],
            "equality_marginal": float(result.eqlin.marginals[0]),
        },
        "finite_candidate_below_one_third": bool(result.fun < 1 / 3),
        "scope": (
            "Binary64 reoptimization over the same 152 physical generators after adding every unique "
            "sixth-order orbit that violated the previous exact candidate in the complete 63,133-orbit "
            "screen. This remains a finite cut LP; any new candidate needs exact rationalization, Arb "
            "verification of all included rows, and another complete-sixth separation scan."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (base_columns[j] if j < 151 else 1641, Fraction.from_float(float(w)))
            for j, w in enumerate(result.x[:-1]) if w > 1e-10
        ]
        total = sum((w for _, w in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": col, "probability": str(weight / total)}
            for col, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized cut-LP probabilities do not sum to one")
        next_candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_out_sha,
            "parent_candidate_sha256": candidate_sha,
            "parent_lp_sha256": lp_sha,
            "parent_dual_certificate_sha256": dual_sha,
            "continuous_escape_arb_certificate_sha256": escape_sha,
            "complete_sixth_binary64_scan_sha256": scan_sha,
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "escape_column_index": 1641,
            "escape_couplings_exact": [str(x) for x in escape_couplings],
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "low_complete_row_count": len(low_target),
            "sixth_cut_rows": [list(row) for row in sixth_rows],
            "sixth_cut_targets": [str(x) for x in sixth_targets],
            "sixth_cut_count": len(sixth_rows),
            "new_unique_sixth_cut_rows": [list(row) for row in new_cuts],
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "selected_eighth_targets": [str(x) for x in eighth_targets],
            "scope": (
                "Exact rational probabilities obtained by normalizing the binary64 cut-LP weights. "
                "This candidate is constrained by all original 1,779 rows plus every unique row found "
                "violating the previous candidate in the exhaustive sixth screen; it is not yet a "
                "complete-sixth certificate and requires independent Arb verification."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(next_candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": transcript["status"],
        "columns": n,
        "rows": m,
        "original_sixth_rows": original_sixth_count,
        "complete_sixth_violations": len(violations),
        "new_unique_sixth_cuts": len(new_cuts),
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized_residual.max()),
        "support_size": len(support),
        "primal_dual_gap": transcript["dual_discovery"]["primal_dual_gap"],
        "candidate_written": candidate_written,
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if candidate_written else None,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
