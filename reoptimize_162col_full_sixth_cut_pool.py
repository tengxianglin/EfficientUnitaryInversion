"""Reoptimize the 2,113-row full-sixth cut LP after certified canonical pricing escapes.

The ten added columns are selected only from the 128-bit Arb-positive pricing
transcript. This is a binary64 HiGHS discovery run; any sub-threshold result
must be rationalized and independently Arb-audited.
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

CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DUAL_CERT = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
PRICING_SCREEN = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_pricing_screen_n21.json"
PRICING_ARB = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_pricing_arb_n21.json"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_162col_full_sixth_cuts_n21.json"
SIXTH_SCALE = Fraction(5, 19721)
EXPECTED_PRICED_COLUMNS = 10


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    raw = {p: p.read_bytes() for p in (
        CANDIDATE_IN, PARENT_LP, DUAL_CERT, PRICING_SCREEN, PRICING_ARB
    )}
    candidate, parent_lp, dual, screen, pricing = [
        json.loads(raw[p]) for p in (
            CANDIDATE_IN, PARENT_LP, DUAL_CERT, PRICING_SCREEN, PRICING_ARB
        )
    ]
    hashes = {p.name: sha(data) for p, data in raw.items()}

    if candidate.get("source_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("152-column parent candidate does not pin its source LP")
    if dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not dual.get("complete"):
        raise RuntimeError("152-column full-sixth dual is not strictly certified")
    if dual.get("lp_transcript_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("dual certificate does not pin the parent LP")
    if pricing.get("status") != "arb_positive_columns_found":
        raise RuntimeError("pricing Arb transcript is not successful")
    if pricing.get("dual_certificate_sha256") != hashes[DUAL_CERT.name]:
        raise RuntimeError("pricing Arb transcript does not pin the strict dual")
    if pricing.get("lp_transcript_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("pricing Arb transcript does not pin the parent LP")
    if pricing.get("pricing_screen_sha256") != hashes[PRICING_SCREEN.name]:
        raise RuntimeError("pricing Arb transcript does not pin the binary64 screen")
    if screen.get("dual_certificate_sha256") != hashes[DUAL_CERT.name]:
        raise RuntimeError("binary64 pricing screen does not pin the strict dual")
    if screen.get("lp_transcript_sha256") != hashes[PARENT_LP.name]:
        raise RuntimeError("binary64 pricing screen does not pin the parent LP")
    if screen.get("canonical_column_count") != 1641 or screen.get("unused_column_count") != 1490:
        raise RuntimeError("unexpected frozen canonical pool dimensions")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (152, 2113):
        raise RuntimeError("unexpected parent LP dimensions")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != dual.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical pool hash/count mismatch")

    base_columns = [int(x) for x in candidate["base_columns"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("malformed 151-column base pool")
    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    priced_results = [x for x in pricing.get("results", []) if x.get("strictly_positive")]
    if len(priced_results) != EXPECTED_PRICED_COLUMNS:
        raise RuntimeError("expected exactly ten Arb-certified positive pricing columns")
    added_columns = [int(x["column"]) for x in priced_results]
    if len(set(added_columns)) != EXPECTED_PRICED_COLUMNS:
        raise RuntimeError("duplicate priced canonical columns")
    if set(added_columns) & set(base_columns):
        raise RuntimeError("a priced canonical column is already in the 151-column base")
    if any(j < 0 or j >= len(all_columns) for j in added_columns):
        raise RuntimeError("priced canonical index outside frozen pool")
    for item in priced_results:
        j = int(item["column"])
        if not np.array_equal(np.asarray(item["couplings"], dtype=np.float64), np.asarray(all_columns[j], dtype=np.float64)):
            raise RuntimeError(f"priced coupling payload differs from frozen canonical column {j}")

    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in added_columns]
    )
    column_labels = base_columns + [1641] + added_columns
    if len(physical_columns) != 162 or len(set(column_labels)) != 162:
        raise RuntimeError("expanded physical pool must contain 162 unique columns")

    sixth_rows = [tuple(int(v) for v in row) for row in parent_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(v) for v in parent_lp["sixth_cut_targets"]]
    eighth_rows = [tuple(int(v) for v in row) for row in parent_lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(v) for v in parent_lp["selected_eighth_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645:
        raise RuntimeError("the 645-row sixth cut inventory is incomplete")
    if len(eighth_rows) != 7 or len(eighth_targets) != 7:
        raise RuntimeError("the seven pinned eighth rows changed")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-row target mismatch")
    if len(set(sixth_rows)) != len(sixth_rows):
        raise RuntimeError("duplicate sixth rows in parent LP")
    if any(len(row) != 8 for row in eighth_rows):
        raise RuntimeError("malformed selected eighth rows")

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

    sixth = np.empty((162, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((162, len(eighth_rows)), dtype=np.float64)
    for j, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[j] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[j] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (j + 1) % 16 == 0 or j == 161:
            print(f"Built physical feature columns {j + 1}/162", flush=True)

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
    row_blocks = {
        "low_complete": len(low_target),
        "sixth_selected_plus_all_cuts": len(sixth_rows),
        "eighth_selected": len(eighth_rows),
    }
    m, n = A.shape
    if (m, n) != (2113, 162):
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

    labels = column_labels
    optimized_residual = np.abs(A @ result.x[:-1] - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    dual_z = result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]
    dual_objective = float(result.eqlin.marginals[0] + np.dot(dual_z, y))
    support = [
        {"column": labels[j], "weight": float(w)}
        for j, w in enumerate(result.x[:-1]) if w > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())
    transcript = {
        "status": "162col_full_sixth_cut_lp_candidate_below_one_third" if result.fun < 1 / 3 else "162col_full_sixth_cut_lp_above_one_third",
        "parent_candidate_sha256": hashes[CANDIDATE_IN.name],
        "parent_lp_sha256": hashes[PARENT_LP.name],
        "parent_dual_certificate_sha256": hashes[DUAL_CERT.name],
        "pricing_screen_sha256": hashes[PRICING_SCREEN.name],
        "pricing_arb_sha256": hashes[PRICING_ARB.name],
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "continuous_escape_column_index": 1641,
        "added_canonical_columns": added_columns,
        "added_canonical_pricing_intervals": [
            {
                "column": int(item["column"]),
                "score_interval": item["arb_pricing_score_interval"],
                "strictly_positive": True,
            }
            for item in priced_results
        ],
        "column_order": labels,
        "sixth_rows_sha256": sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode()),
        "eighth_rows_sha256": sha(json.dumps([list(x) for x in eighth_rows], separators=(",", ":")).encode()),
        "matrix_and_target_sha256_le_f64": matrix_sha,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized_residual.max()),
        "expanded_block_maxima": {
            name: float(optimized_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "positive_support": support,
        "dual_discovery": {
            "z_l1_norm": float(np.abs(dual_z).sum()),
            "objective": dual_objective,
            "primal_dual_gap": abs(float(result.fun) - dual_objective),
            "inequality_marginals": [float(x) for x in result.ineqlin.marginals],
            "equality_marginal": float(result.eqlin.marginals[0]),
        },
        "finite_candidate_below_one_third": bool(result.fun < 1 / 3),
        "scope": (
            "Binary64 minimax reoptimization on the exact 2,113-row cut design, "
            "adding ten canonical columns whose reduced-cost scores were independently "
            "certified strictly positive by 128-bit Arb against the parent 152-column dual. "
            "This is a finite discovery LP, not a theorem. A sub-1/3 result requires exact "
            "probability rationalization, a fresh Arb audit of all 2,113 rows, and a complete "
            "63,133-orbit sixth-order separation scan."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (labels[j], Fraction.from_float(float(w)))
            for j, w in enumerate(result.x[:-1]) if w > 1e-10
        ]
        total = sum((w for _, w in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": col, "probability": str(weight / total)}
            for col, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized probabilities do not sum to one")
        next_candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_out_sha,
            "parent_candidate_sha256": hashes[CANDIDATE_IN.name],
            "parent_lp_sha256": hashes[PARENT_LP.name],
            "parent_dual_certificate_sha256": hashes[DUAL_CERT.name],
            "pricing_screen_sha256": hashes[PRICING_SCREEN.name],
            "pricing_arb_sha256": hashes[PRICING_ARB.name],
            "canonical_all_columns_sha256_le_f64": all_sha,
            "base_columns": base_columns,
            "continuous_escape_column_index": 1641,
            "escape_couplings_exact": [str(x) for x in escape_couplings],
            "added_canonical_columns": added_columns,
            "column_order": labels,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "low_complete_row_count": 1461,
            "sixth_cut_rows": [list(row) for row in sixth_rows],
            "sixth_cut_targets": [str(x) for x in sixth_targets],
            "sixth_cut_count": len(sixth_rows),
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "selected_eighth_targets": [str(x) for x in eighth_targets],
            "scope": (
                "Exact rational probabilities obtained by normalizing the binary64 162-column "
                "cut-LP weights. This candidate is only constrained on the pinned 2,113 rows; "
                "it requires independent Arb verification and a complete-sixth separation scan."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(next_candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": transcript["status"],
        "columns": n,
        "rows": m,
        "added_canonical_columns": added_columns,
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized_residual.max()),
        "block_maxima": transcript["expanded_block_maxima"],
        "support_size": len(support),
        "primal_dual_gap": transcript["dual_discovery"]["primal_dual_gap"],
        "candidate_written": candidate_written,
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if candidate_written else None,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
