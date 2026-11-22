"""Cut the 113-column candidate with eight full-domain Arb sixth-order separators.

The eight rows are one strict 128-bit Arb violation from each of the eight
contiguous shards of the preceding candidate's full-domain audit. This is a
finite HiGHS reweighting step; the rationalized result must be rechecked by Arb.
"""
import hashlib
import json
from pathlib import Path
from fractions import Fraction
from math import comb

import numpy as np
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import EIGHTH_ROWS, matrix, orbit_minor

LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_103col_38probe_n21.json"
DUAL_IN = ROOT / "evidence/38probe_103col_dual_certificate_n21.json"
SCREEN_IN = ROOT / "evidence/38probe_103col_dual_pricing_screen_n21.json"
PRICING_IN = ROOT / "evidence/38probe_103col_dual_pricing_arb_n21.json"
OLD_CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_113col_38probe_n21.json"
AUDIT_IN = ROOT / "evidence/candidate_113col_38probe_complete_sixth_arb_n21.json"
SIXTH_SCREEN_IN = ROOT / "evidence/sixth_moment_screen_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_113col_46probe_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_113col_46probe_n21.json"
CAP = Fraction(1, 3)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    lp_raw = LP_IN.read_bytes()
    dual_raw = DUAL_IN.read_bytes()
    screen_raw = SCREEN_IN.read_bytes()
    pricing_raw = PRICING_IN.read_bytes()
    lp = json.loads(lp_raw)
    dual = json.loads(dual_raw)
    screen = json.loads(screen_raw)
    pricing = json.loads(pricing_raw)
    old_candidate_raw = OLD_CANDIDATE_IN.read_bytes()
    old_candidate_sha = sha256(old_candidate_raw)
    audit_raw = AUDIT_IN.read_bytes()
    audit_sha = sha256(audit_raw)
    audit = json.loads(audit_raw)

    if lp.get("columns") != 103 or lp.get("rows") != 1762:
        raise RuntimeError("the pinned parent LP must be 103 columns x 1,762 rows")
    if dual.get("status") != "strict_pool_separation" or not dual.get("complete"):
        raise RuntimeError("the 103-column Arb dual certificate is not complete")
    if dual.get("lp_transcript_sha256") != sha256(lp_raw):
        raise RuntimeError("the dual certificate does not pin the parent LP transcript")
    if dual.get("column_count") != 103 or dual.get("row_count") != 1762:
        raise RuntimeError("unexpected dual certificate dimensions")
    if screen.get("status") != "priced_existing_pool" or screen.get("active_column_count") != 103:
        raise RuntimeError("the binary64 pricing screen does not match the 103-column pool")
    if screen.get("dual_certificate_sha256") != sha256(dual_raw):
        raise RuntimeError("the pricing screen does not pin the Arb dual certificate")
    if pricing.get("status") != "arb_positive_columns_found" or pricing.get("precision_bits", 0) < 128:
        raise RuntimeError("the Arb pricing result is not a 128-bit positive-column certificate")
    if pricing.get("dual_certificate_sha256") != sha256(dual_raw):
        raise RuntimeError("the Arb pricing result does not pin the dual certificate")
    if pricing.get("pricing_screen_sha256") != sha256(screen_raw):
        raise RuntimeError("the Arb pricing result does not pin the binary64 screen")
    if pricing.get("lp_transcript_sha256") != sha256(lp_raw):
        raise RuntimeError("the Arb pricing result does not pin the parent LP")
    if pricing.get("arb_certified_positive_count") != 10 or len(pricing.get("results", [])) != 10:
        raise RuntimeError("expected exactly ten Arb-certified positive columns")
    if audit.get("status") != "strict_violation" or audit.get("complete") is not False:
        raise RuntimeError("the parent 113-column full-domain Arb audit is not a strict candidate rejection")
    if audit.get("candidate_input_sha256") != old_candidate_sha:
        raise RuntimeError("the full-domain separator transcript does not pin the exact parent candidate")
    if audit.get("precision_bits", 0) < 128 or audit.get("requested_orbits") != 63133:
        raise RuntimeError("the separator transcript is not a 128-bit full-domain sixth audit")
    audit_failures = audit.get("failures", [])
    if len(audit_failures) != 8 or sorted(int(row["shard"]) for row in audit_failures) != list(range(8)):
        raise RuntimeError("expected one Arb-certified strict separator from each of eight audit shards")
    audit_rows = [tuple(int(x) for x in row["indices"]) for row in audit_failures]
    audit_targets = [Fraction(row["target"]) for row in audit_failures]
    if len(set(audit_rows)) != 8 or any(row.get("status") != "strict_violation" for row in audit_failures):
        raise RuntimeError("the eight full-domain separators are not distinct strict Arb violations")
    if any(target(indices) != expected for indices, expected in zip(audit_rows, audit_targets)):
        raise RuntimeError("a full-domain separator target disagrees with the exact sixth-order parity formula")

    all_columns, _, baseline_probabilities = canonical_ensemble()
    all_column_array = np.asarray(all_columns, dtype="<f8")
    all_columns_sha = sha256(all_column_array.tobytes())
    expected_columns_sha = pricing.get("canonical_all_columns_sha256_le_f64")
    if all_columns_sha != expected_columns_sha or all_columns_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical 1,641-column physical pool hash mismatch")
    if len(all_columns) != 1641:
        raise RuntimeError("canonical physical pool size changed")

    base_columns = [int(x) for x in dual["columns"]]
    if len(base_columns) != 103 or len(set(base_columns)) != 103 or base_columns != sorted(base_columns):
        raise RuntimeError("the dual certificate's active column list is malformed")
    if base_columns != sorted(int(x) for x in lp["base_columns"]):
        raise RuntimeError("parent LP columns differ from the certified dual pool")
    if screen.get("canonical_column_count") != len(all_columns) or screen.get("unused_column_count") != 1538:
        raise RuntimeError("pricing-screen pool dimensions changed")

    new_columns = []
    for record in pricing["results"]:
        column = int(record["column"])
        if not record.get("strictly_positive") or column in base_columns or not 0 <= column < len(all_columns):
            raise RuntimeError(f"invalid Arb-positive pricing column: {column}")
        couplings = all_columns[column]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"column {column} is not a legal nonzero 42-site path generator")
        if [float(value) for value in couplings] != record["couplings"]:
            raise RuntimeError(f"Arb-priced column {column} does not match canonical input")
        new_columns.append(column)
    if len(set(new_columns)) != 10:
        raise RuntimeError("Arb-positive pricing columns are not distinct")
    columns = sorted(set(base_columns) | set(new_columns))
    if len(columns) != 113:
        raise RuntimeError(f"expected 113 columns after pricing expansion, got {len(columns)}")
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

    sixth_screen = json.loads(SIXTH_SCREEN_IN.read_text())["records"]
    screen_rows = [tuple(row["indices"]) for row in sixth_screen]
    screen_targets = [Fraction(row["target"]) for row in sixth_screen]
    probe_rows = [tuple(row) for row in lp["sixth_probe_rows"]]
    probe_targets = [Fraction(value) for value in lp["sixth_probe_targets"]]
    if len(screen_rows) != 256 or len(probe_rows) != 38:
        raise RuntimeError("unexpected sixth-order row inventory")
    if any(target(row) != value for row, value in zip(probe_rows, probe_targets)):
        raise RuntimeError("a pinned sixth-probe target disagrees with the exact parity formula")
    if set(audit_rows) & (set(screen_rows) | set(probe_rows)):
        raise RuntimeError("a new full-domain separator duplicates an existing sixth-order row")
    sixth_rows = screen_rows + probe_rows + audit_rows
    sixth_targets = np.asarray([float(x) for x in screen_targets + probe_targets + audit_targets])

    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
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
        "sixth_full_audit_separators": len(audit_rows),
        "selected_eighth": len(eighth_rows),
    }
    m, n = A.shape
    if (m, n) != (1770, 113) or m != sum(row_blocks.values()):
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
    for column, weight in lp["positive_weights"]:
        if int(column) not in columns:
            raise RuntimeError("parent LP weight refers to a column outside its certified pool")
        baseline[columns.index(int(column))] = float(weight)
    baseline_residual = np.abs(A @ baseline - y)
    optimized_residual = np.abs(A @ weights - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    inequality_marginals = np.asarray(result.ineqlin.marginals, dtype=np.float64)
    equality_marginal = float(result.eqlin.marginals[0])
    dual_z = inequality_marginals[:m] - inequality_marginals[m:]
    dual_l1 = float(np.abs(dual_z).sum())
    dual_objective = equality_marginal + float(np.dot(dual_z, y))

    transcript = {
        "parent_lp_sha256": sha256(lp_raw),
        "parent_dual_certificate_sha256": sha256(dual_raw),
        "parent_pricing_screen_sha256": sha256(screen_raw),
        "parent_pricing_screen_sha256": sha256(screen_raw),
            "parent_arb_pricing_sha256": sha256(pricing_raw),
        "parent_complete_sixth_audit_sha256": audit_sha,
        "sixth_full_audit_separator_rows": [list(row) for row in audit_rows],
        "sixth_full_audit_separator_targets": [str(value) for value in audit_targets],
        "canonical_all_columns_sha256_le_f64": all_columns_sha,
        "base_columns": base_columns,
        "added_arb_positive_columns": sorted(new_columns),
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
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
            "Finite binary64 LP over 113 canonical legal 42-site path columns and 1,770 normalized "
            "rows (1,461 low, 302 sixth including eight strict full-domain Arb separators, seven "
            "selected eighth). The eight new rows are one strict 128-bit Arb violation from each "
            "shard of the rejected parent candidate's 63,133-orbit audit. This reweighting does "
            "not certify the new exact candidate, complete sixth/eighth maxima, other physical "
            "generators, or an operational Choi/diamond-norm inversion bound."
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
            "source_file": "evidence/joint_low_six_eighth_lp_113col_46probe_n21.json",
            "source_sha256": lp_out_sha,
            "parent_lp_sha256": sha256(lp_raw),
            "parent_dual_certificate_sha256": sha256(dual_raw),
            "parent_pricing_screen_sha256": sha256(screen_raw),
            "parent_arb_pricing_sha256": sha256(pricing_raw),
            "parent_complete_sixth_audit_sha256": audit_sha,
            "sixth_full_audit_separator_rows": [list(row) for row in audit_rows],
            "sixth_full_audit_separator_targets": [str(value) for value in audit_targets],
            "canonical_all_columns_sha256_le_f64": all_columns_sha,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_probe_rows": [list(row) for row in probe_rows],
            "sixth_probe_targets": [str(value) for value in probe_targets],
            "sixth_full_audit_separator_rows": [list(row) for row in audit_rows],
            "sixth_full_audit_separator_targets": [str(value) for value in audit_targets],
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "scope": "Exact rational input obtained by normalizing binary64 HiGHS weights on the 1,770-row cutting-plane LP; all 302 selected sixth rows and a fresh full-domain prefix require independent Arb verification.",
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
        "added_columns": sorted(new_columns),
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
