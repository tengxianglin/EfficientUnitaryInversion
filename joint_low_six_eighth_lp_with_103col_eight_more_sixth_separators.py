"""Reweight the 103-column pool using all eight strict Arb separators from the 30-probe candidate audit."""
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from flint import arb, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments, orbit_key
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import EIGHTH_ROWS, matrix, orbit_minor

PARENT_LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_103col_30probe_n21.json"
PARENT_CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_103col_30probe_n21.json"
SIXTH_AUDIT_IN = ROOT / "evidence/candidate_103col_30probe_complete_sixth_arb_n21.json"
SIXTH_SCREEN_IN = ROOT / "evidence/sixth_moment_screen_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_103col_38probe_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_103col_38probe_n21.json"
CAP = Fraction(1, 3)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = 128
    parent_lp_raw = PARENT_LP_IN.read_bytes()
    parent_candidate_raw = PARENT_CANDIDATE_IN.read_bytes()
    audit_raw = SIXTH_AUDIT_IN.read_bytes()
    parent_lp = json.loads(parent_lp_raw)
    parent_candidate = json.loads(parent_candidate_raw)
    audit = json.loads(audit_raw)

    parent_lp_sha = sha256(parent_lp_raw)
    parent_candidate_sha = sha256(parent_candidate_raw)
    audit_sha = sha256(audit_raw)
    if parent_lp.get("columns") != 103 or parent_lp.get("rows") != 1754:
        raise RuntimeError("parent LP is not the pinned 103-column / 1,754-row design")
    if parent_candidate.get("source_sha256") != parent_lp_sha:
        raise RuntimeError("parent exact candidate does not pin its LP transcript")
    if parent_candidate.get("support_size") != len(parent_candidate.get("exact_probabilities", [])):
        raise RuntimeError("parent candidate support metadata mismatch")
    if sum((Fraction(row["probability"]) for row in parent_candidate["exact_probabilities"]), Fraction(0)) != 1:
        raise RuntimeError("parent candidate probabilities do not sum exactly to one")
    if audit.get("status") != "strict_violation" or audit.get("complete") is not False:
        raise RuntimeError("parent complete-sixth audit is not a candidate-specific strict rejection")
    if audit.get("candidate_input_sha256") != parent_candidate_sha or audit.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("complete-sixth audit does not pin the exact parent candidate and LP")
    if audit.get("precision_bits", 0) < 128 or audit.get("interval_backend") != "python-flint 0.8.0 / Arb":
        raise RuntimeError("parent rejection is not a pinned 128-bit Arb audit")
    failures = audit.get("failures", [])
    if len(failures) != 8 or len(audit.get("shards", [])) != 8:
        raise RuntimeError("expected one strict Arb separator from each of eight sixth-orbit shards")
    new_rows = []
    new_targets = []
    new_separator_records = []
    for failure in failures:
        if failure.get("status") != "strict_violation" or failure.get("candidate_input_sha256") != parent_candidate_sha:
            raise RuntimeError("an imported sixth separator is not a strict violation of the exact parent candidate")
        lower = arb(failure["absolute_error_lower"]).lower()
        if not lower > arb(1) / 3:
            raise RuntimeError("an imported Arb lower endpoint does not strictly exceed 1/3")
        row = tuple(int(x) for x in failure["indices"])
        value = Fraction(failure["target"])
        if target(row) != value:
            raise RuntimeError("an imported separator target disagrees with the exact parity formula")
        if len(row) != 6 or tuple(sorted(set(row))) != row or row[0] != 0:
            raise RuntimeError("an imported separator is not a canonical six-subset representative")
        new_rows.append(row)
        new_targets.append(value)
        new_separator_records.append({
            "indices": list(row),
            "target": str(value),
            "orbit_size": int(failure["orbit_size"]),
            "relative_error_interval": failure["error_interval"],
            "absolute_error_lower": failure["absolute_error_lower"],
            "absolute_error_upper": failure["absolute_error_upper"],
            "parent_failure_orbit_index": int(failure["failure_orbit_index"]),
            "parent_shard": int(failure["shard"]),
        })
    if len(set(new_rows)) != 8:
        raise RuntimeError("the eight Arb separators are not distinct")

    all_columns, _, _ = canonical_ensemble()
    all_hash = sha256(np.asarray(all_columns, dtype="<f8").tobytes())
    if all_hash != parent_lp.get("canonical_all_columns_sha256_le_f64") or all_hash != parent_candidate.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical physical-column fingerprint changed")
    if len(all_columns) != 1641:
        raise RuntimeError("canonical physical pool size changed")

    columns = sorted(set(int(x) for x in parent_lp["base_columns"]) | set(int(x) for x in parent_lp["added_arb_positive_columns"]))
    if len(columns) != 103:
        raise RuntimeError("parent LP does not identify exactly 103 physical columns")
    physical_columns = [all_columns[index] for index in columns]

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

    screen_rows_data = json.loads(SIXTH_SCREEN_IN.read_text())["records"]
    screen_rows = [tuple(row["indices"]) for row in screen_rows_data]
    screen_targets = [Fraction(row["target"]) for row in screen_rows_data]
    old_probe_rows = [tuple(row) for row in parent_lp["sixth_probe_rows"]]
    old_probe_targets = [Fraction(value) for value in parent_lp["sixth_probe_targets"]]
    old_keys = {orbit_key(row, 42) for row in screen_rows + old_probe_rows}
    new_keys = [orbit_key(row, 42) for row in new_rows]
    if any(key in old_keys for key in new_keys) or len(set(new_keys)) != len(new_keys):
        raise RuntimeError("one or more new Arb separators duplicate an existing or newly added dihedral orbit")
    probe_rows = old_probe_rows + new_rows
    probe_targets = old_probe_targets + new_targets
    if len(screen_rows) != 256 or len(old_probe_rows) != 30 or len(probe_rows) != 38:
        raise RuntimeError("unexpected sixth-order row inventory")

    sixth_rows = screen_rows + probe_rows
    sixth_targets = np.asarray([float(x) for x in screen_targets + probe_targets])
    eighth_rows = [tuple(row) for row in parent_lp["selected_eighth_rows"]]
    if [list(row) for row in eighth_rows] != EIGHTH_ROWS:
        raise RuntimeError("selected eighth-order rows differ from the pinned design")
    eighth_targets = np.asarray([
        float(Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8)))
        for row in eighth_rows
    ])

    sixth = np.empty((len(columns), len(sixth_rows)))
    eighth = np.empty((len(columns), len(eighth_rows)))
    for j, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[j] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[j] = [orbit_minor(rotation, row) for row in eighth_rows]

    sixth_scale = np.full(len(sixth_rows), 5 / 19721)
    eighth_scale = np.full(len(eighth_rows), 1 / 19721)
    A = np.vstack([
        low.T / low_scale[:, None],
        sixth.T / sixth_scale[:, None],
        eighth.T / eighth_scale[:, None],
    ])
    y = np.r_[
        low_target / low_scale,
        sixth_targets / sixth_scale,
        eighth_targets / eighth_scale,
    ]
    row_blocks = {
        "low": len(low_target),
        "sixth_screen": len(screen_rows),
        "sixth_certified_probes": len(probe_rows),
        "selected_eighth": len(eighth_rows),
    }
    m, n = A.shape
    if (m, n) != (1762, 103) or m != sum(row_blocks.values()):
        raise RuntimeError(f"unexpected LP dimensions: {m} rows x {n} columns")

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

    weights = result.x[:-1]
    baseline = np.zeros(n)
    for row in parent_candidate["exact_probabilities"]:
        column = int(row["column"])
        if column not in columns:
            raise RuntimeError("parent candidate uses a column outside the 103-column pool")
        baseline[columns.index(column)] = float(Fraction(row["probability"]))
    baseline_residual = np.abs(A @ baseline - y)
    optimized_residual = np.abs(A @ weights - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    inequality_marginals = np.asarray(result.ineqlin.marginals, dtype=np.float64)
    equality_marginal = float(result.eqlin.marginals[0])
    dual_z = inequality_marginals[:m] - inequality_marginals[m:]
    dual_l1 = float(np.abs(dual_z).sum())
    dual_objective = equality_marginal + float(np.dot(dual_z, y))

    transcript = {
        "parent_lp_sha256": parent_lp_sha,
        "parent_candidate_input_sha256": parent_candidate_sha,
        "parent_sixth_audit_sha256": audit_sha,
        "canonical_all_columns_sha256_le_f64": all_hash,
        "columns": n,
        "rows": m,
        "base_columns": columns,
        "added_arb_positive_columns": parent_lp["added_arb_positive_columns"],
        "row_blocks": row_blocks,
        "new_sixth_separators": new_separator_records,
        "solver": "scipy.optimize.linprog(method=highs), binary64 finite design only",
        "baseline_max": float(baseline_residual.max()),
        "lp_max": float(optimized_residual.max()),
        "lp_objective": float(result.fun),
        "finite_candidate_below_one_third": bool(result.fun < float(CAP)),
        "block_maxima": {
            name: float(optimized_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "baseline_block_maxima": {
            name: float(baseline_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "dual_discovery": {
            "convention": "z = first m inequality marginals minus second m; lambda is equality marginal for sum(weights)=1",
            "inequality_marginals": [float(x) for x in inequality_marginals],
            "equality_marginal": equality_marginal,
            "z_l1_norm": dual_l1,
            "dual_objective": dual_objective,
            "primal_dual_objective_gap": abs(dual_objective - float(result.fun)),
            "max_column_lhs": float(np.max(A.T @ dual_z + equality_marginal)),
        },
        "positive_weights": [
            [int(column), float(weight)]
            for column, weight in zip(columns, weights)
            if weight > 1e-10
        ],
        "sixth_probe_rows": [list(row) for row in probe_rows],
        "sixth_probe_targets": [str(value) for value in probe_targets],
        "selected_eighth_rows": [list(row) for row in eighth_rows],
        "scope": (
            "Finite binary64 cutting-plane LP over the same 103 canonical legal 42-site path columns "
            "and 1,754 pinned normalized rows (1,461 low, 286 sixth, seven selected eighth). The "
            "eight new sixth rows are 128-bit Arb-certified violations of the exact parent candidate, "
            "not a pool-wide no-go. This LP does not certify the new rational candidate, complete "
            "sixth/eighth maxima, other physical generators, or an operational Choi/diamond-norm bound."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha256(LP_OUT.read_bytes())

    if result.fun < float(CAP):
        raw_weights = [
            (int(column), Fraction.from_float(float(weight)))
            for column, weight in zip(columns, weights)
            if weight > 1e-10
        ]
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": column, "probability": str(weight / total)}
            for column, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("exact rationalized candidate probabilities do not sum to one")
        candidate = {
            "source_file": "evidence/joint_low_six_eighth_lp_103col_38probe_n21.json",
            "source_sha256": lp_out_sha,
            "parent_lp_sha256": parent_lp_sha,
            "parent_candidate_input_sha256": parent_candidate_sha,
            "parent_sixth_audit_sha256": audit_sha,
            "canonical_all_columns_sha256_le_f64": all_hash,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_probe_rows": [list(row) for row in probe_rows],
            "sixth_probe_targets": [str(value) for value in probe_targets],
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "new_sixth_separators": transcript["new_sixth_separators"],
            "scope": "Exact rational input obtained by normalizing binary64 HiGHS weights; moment bounds require independent Arb verification.",
        }
        CANDIDATE_OUT.write_text(json.dumps(candidate, indent=2) + "\n")
    elif CANDIDATE_OUT.exists():
        CANDIDATE_OUT.unlink()

    print(json.dumps({
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "lp_sha256": lp_out_sha,
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if CANDIDATE_OUT.exists() else None,
        "columns": n,
        "rows": m,
        "new_separators": transcript["new_sixth_separators"],
        "lp_objective": float(result.fun),
        "max_recomputed_residual": float(optimized_residual.max()),
        "block_maxima": transcript["block_maxima"],
        "baseline_max": float(baseline_residual.max()),
        "finite_candidate_below_one_third": transcript["finite_candidate_below_one_third"],
        "support_size": len(transcript["positive_weights"]),
        "dual_l1_norm": dual_l1,
        "primal_dual_gap": transcript["dual_discovery"]["primal_dual_objective_gap"],
    }, indent=2))


if __name__ == "__main__":
    main()
