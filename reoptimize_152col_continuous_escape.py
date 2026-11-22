"""Binary64 reoptimization after adding the Arb-certified continuous-path escape.

This is a discovery experiment only.  It reuses the exact 1,779-row design
and 151-column parent LP, adds one exact-rational physical path generator,
recomputes all features in binary64, and resolves the minimax LP.  Any
sub-1/3 result would require a separate rational/Arb certificate.
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
from verify_continuous_path_dual_escape_arb import COUPLINGS, CANDIDATE_SHA256

PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_151col_55probe_n21.json"
DUAL_CERT = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SIXTH_SCREEN = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT = ROOT / "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json"
CANDIDATE_OUTPUT = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parent_raw = PARENT_LP.read_bytes()
    dual_raw = DUAL_CERT.read_bytes()
    escape_raw = ESCAPE_CERT.read_bytes()
    parent = json.loads(parent_raw)
    dual = json.loads(dual_raw)
    escape = json.loads(escape_raw)
    parent_sha, dual_sha, escape_sha = sha(parent_raw), sha(dual_raw), sha(escape_raw)

    if (parent.get("columns"), parent.get("rows")) != (151, 1779):
        raise RuntimeError("unexpected parent LP dimensions")
    if dual.get("status") != "strict_pool_separation" or dual.get("lp_transcript_sha256") != parent_sha:
        raise RuntimeError("the parent dual certificate does not pin the parent LP")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("the continuous-path escape lacks a strict Arb certificate")
    if escape.get("candidate_sha256") != CANDIDATE_SHA256:
        raise RuntimeError("escape certificate and candidate input disagree")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != dual["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen canonical-pool hash/count mismatch")
    base_columns = sorted(int(x) for x in dual["columns"])
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("malformed 151-column parent active set")
    physical_columns = [all_columns[index] for index in base_columns] + [COUPLINGS]
    if any(list(column) == COUPLINGS for column in all_columns):
        raise RuntimeError("escape column unexpectedly belongs to the frozen pool")

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

    screen_records = json.loads(SIXTH_SCREEN.read_text())["records"]
    screen_rows = [tuple(row["indices"]) for row in screen_records]
    screen_targets = [Fraction(row["target"]) for row in screen_records]
    probe_rows = [tuple(row) for row in parent["sixth_probe_rows"]]
    probe_targets = [Fraction(value) for value in parent["sixth_probe_targets"]]
    full_rows = [tuple(row) for row in parent["sixth_full_audit_separator_rows"]]
    full_targets = [Fraction(value) for value in parent["sixth_full_audit_separator_targets"]]
    prefix_rows = [tuple(row) for row in parent["sixth_prefix_separator_rows"]]
    prefix_targets = [Fraction(value) for value in parent["sixth_prefix_separator_targets"]]
    additional_rows = [tuple(row) for row in parent["sixth_additional_full_audit_separator_rows"]]
    additional_targets = [Fraction(value) for value in parent["sixth_additional_full_audit_separator_targets"]]
    sixth_rows = screen_rows + probe_rows + full_rows + prefix_rows + additional_rows
    sixth_targets_exact = screen_targets + probe_targets + full_targets + prefix_targets + additional_targets
    if len(sixth_rows) != 311 or any(target(row) != value for row, value in zip(sixth_rows, sixth_targets_exact)):
        raise RuntimeError("pinned sixth-row inventory/target mismatch")

    eighth_rows = [tuple(row) for row in parent["selected_eighth_rows"]]
    if [list(row) for row in eighth_rows] != EIGHTH_ROWS:
        raise RuntimeError("selected eighth-row inventory mismatch")
    eighth_targets_exact = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]

    sixth = np.empty((len(physical_columns), len(sixth_rows)))
    eighth = np.empty((len(physical_columns), len(eighth_rows)))
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
        np.asarray([float(x) for x in sixth_targets_exact]) / sixth_scale,
        np.asarray([float(x) for x in eighth_targets_exact]) / eighth_scale,
    ]
    row_blocks = {"low": len(low_target), "sixth": len(sixth_rows), "selected_eighth": len(eighth_rows)}
    m, n = A.shape
    if (m, n) != (1779, 152):
        raise RuntimeError(f"unexpected expanded LP dimensions: {m} x {n}")

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

    baseline = np.zeros(n)
    for column, weight in parent["positive_weights"]:
        index = base_columns.index(int(column))
        baseline[index] = float(weight)
    baseline_residual = np.abs(A @ baseline - y)
    optimized_residual = np.abs(A @ result.x[:-1] - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    support = [
        {"column": base_columns[j] if j < 151 else "continuous_escape",
         "weight": float(weight)}
        for j, weight in enumerate(result.x[:-1]) if weight > 1e-10
    ]
    candidate_weight = float(result.x[-2])
    transcript = {
        "parent_lp_sha256": parent_sha,
        "parent_dual_certificate_sha256": dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "candidate_sha256": CANDIDATE_SHA256,
        "candidate_couplings_exact": [str(x) for x in COUPLINGS],
        "base_columns": base_columns,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "baseline_parent_max": float(baseline_residual.max()),
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized_residual.max()),
        "expanded_block_maxima": {
            name: float(optimized_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "baseline_block_maxima": {
            name: float(baseline_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "continuous_escape_weight": candidate_weight,
        "continuous_escape_in_support": candidate_weight > 1e-10,
        "positive_support": support,
        "dual_discovery": {
            "z_l1_norm": float(np.abs(result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]).sum()),
            "objective": float(result.eqlin.marginals[0] + np.dot(result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:], y)),
            "primal_dual_gap": abs(float(result.fun) - float(result.eqlin.marginals[0] + np.dot(result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:], y))),
        },
        "finite_candidate_below_one_third": bool(result.fun < 1 / 3),
        "scope": (
            "Binary64 reoptimization over the 151 pinned canonical columns plus one exact-rational "
            "continuous-family escape, on the same 1,779 selected rows. This is discovery evidence "
            "only; no exact probabilities, full sixth/eighth audit, or operational channel guarantee "
            "is certified by this LP."
        ),
    }
    OUTPUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(OUTPUT.read_bytes())
    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = []
        for j, weight in enumerate(result.x[:-1]):
            if weight > 1e-10:
                column = base_columns[j] if j < 151 else 1641
                raw_weights.append((int(column), Fraction.from_float(float(weight))))
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": column, "probability": str(weight / total)}
            for column, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized candidate probabilities do not sum to one")
        candidate = {
            "source_file": "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json",
            "source_sha256": lp_out_sha,
            "parent_lp_sha256": parent_sha,
            "parent_dual_certificate_sha256": dual_sha,
            "continuous_escape_arb_certificate_sha256": escape_sha,
            "canonical_all_columns_sha256_le_f64": all_sha,
            "candidate_sha256": CANDIDATE_SHA256,
            "base_columns": base_columns,
            "escape_column_index": 1641,
            "escape_couplings_exact": [str(x) for x in COUPLINGS],
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_probe_rows": parent["sixth_probe_rows"],
            "sixth_probe_targets": parent["sixth_probe_targets"],
            "sixth_full_audit_separator_rows": parent["sixth_full_audit_separator_rows"],
            "sixth_full_audit_separator_targets": parent["sixth_full_audit_separator_targets"],
            "sixth_prefix_separator_rows": parent["sixth_prefix_separator_rows"],
            "sixth_prefix_separator_targets": parent["sixth_prefix_separator_targets"],
            "sixth_additional_full_audit_separator_rows": parent["sixth_additional_full_audit_separator_rows"],
            "sixth_additional_full_audit_separator_targets": parent["sixth_additional_full_audit_separator_targets"],
            "selected_eighth_rows": parent["selected_eighth_rows"],
            "scope": "Exact rational probabilities obtained by normalizing the binary64 152-column HiGHS weights. This is only a selected-row candidate input; strict Arb verification is required.",
        }
        CANDIDATE_OUTPUT.write_text(json.dumps(candidate, indent=2) + "\n")
        candidate_written = True
    elif CANDIDATE_OUTPUT.exists():
        CANDIDATE_OUTPUT.unlink()
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "lp_sha256": lp_out_sha,
        "candidate_output": str(CANDIDATE_OUTPUT.relative_to(ROOT)) if candidate_written else None,
        "columns": n,
        "rows": m,
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized_residual.max()),
        "continuous_escape_weight": candidate_weight,
        "finite_candidate_below_one_third": transcript["finite_candidate_below_one_third"],
        "support_size": len(support),
        "primal_dual_gap": transcript["dual_discovery"]["primal_dual_gap"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
