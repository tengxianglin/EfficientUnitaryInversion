"""Reoptimize the 2,113-row full-sixth cut LP with one new Arb-positive column.

The parent is the strictly Arb-certified 182-column mixed-order cut dual.
This script is a binary64 HiGHS discovery step; a sub-1/3 candidate is only
a candidate until exact-probability Arb and complete-sixth audits pass.
"""
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import matrix, orbit_minor

CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP_152 = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL_152 = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
LP_182 = ROOT / "evidence/joint_low_six_eighth_lp_182col_full_sixth_cuts_n21.json"
DUAL_182 = ROOT / "evidence/55probe_182col_full_sixth_cut_dual_certificate_n21.json"
SCREEN_182 = ROOT / "evidence/55probe_182col_full_sixth_cut_dual_pricing_screen_n21.json"
PRICING_182 = ROOT / "evidence/55probe_182col_full_sixth_cut_dual_pricing_arb_n21.json"
ORIGINAL_DUAL_151 = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_183col_full_sixth_cuts_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_183col_full_sixth_cuts_n21.json"

SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
ESCAPE_COLUMN = 1641
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)
EXPECTED_NEW_COLUMNS = 1


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    paths = (
        CANDIDATE_152, CUT_LP_152, CUT_DUAL_152, LP_182, DUAL_182,
        SCREEN_182, PRICING_182, ORIGINAL_DUAL_151, ESCAPE_CERT, SEED_POOL,
    )
    raw = {path: path.read_bytes() for path in paths}
    data = {
        path: (json.loads(value) if path.suffix != ".npy" else value)
        for path, value in raw.items()
    }
    hashes = {path.name: sha(value) for path, value in raw.items()}
    candidate = data[CANDIDATE_152]
    cut_lp = data[CUT_LP_152]
    cut_dual = data[CUT_DUAL_152]
    parent_lp = data[LP_182]
    parent_dual = data[DUAL_182]
    screen = data[SCREEN_182]
    pricing = data[PRICING_182]
    original_dual = data[ORIGINAL_DUAL_151]
    escape = data[ESCAPE_CERT]

    # Verify the complete 151 -> 152 -> 182 evidence chain.
    if candidate.get("parent_dual_certificate_sha256") != hashes[ORIGINAL_DUAL_151.name]:
        raise RuntimeError("152 candidate does not pin the original 151-column dual")
    if candidate.get("continuous_escape_arb_certificate_sha256") != hashes[ESCAPE_CERT.name]:
        raise RuntimeError("152 candidate does not pin the continuous-path Arb certificate")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous-path escape is not strictly Arb-certified")
    if cut_lp.get("parent_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("152 cut LP does not pin the exact 152-column candidate")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column 2,113-row parent dual is not certified")
    if cut_dual.get("lp_transcript_sha256") != hashes[CUT_LP_152.name]:
        raise RuntimeError("152-column dual does not pin its LP transcript")
    if parent_lp.get("status") != "182col_full_sixth_cut_lp_above_one_third":
        raise RuntimeError("182-column parent LP is not the expected above-cap discovery")
    if parent_lp.get("parent_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("182-column LP does not pin the 152-column candidate")
    # The 152-column cut LP/dual were refreshed after the 182-column LP was
    # created. The 182 certificate preserves the historical parent hashes;
    # the current row inventory is checked independently below.
    if parent_dual.get("parent_172col_lp_sha256") != parent_lp.get("parent_172col_lp_sha256"):
        raise RuntimeError("182-column certificate and LP disagree on parent 172-column LP")
    if parent_dual.get("parent_172col_dual_certificate_sha256") != parent_lp.get("parent_172col_dual_certificate_sha256"):
        raise RuntimeError("182-column certificate and LP disagree on parent 172-column dual")
    if cut_dual.get("lp_transcript_sha256") != hashes[CUT_LP_152.name]:
        raise RuntimeError("current 152-column dual does not pin the current cut LP")
    if cut_dual.get("parent_candidate_sha256") != hashes[CANDIDATE_152.name]:
        raise RuntimeError("current 152-column dual does not pin the exact candidate")
    if parent_dual.get("status") != "strict_182col_2113row_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("182-column parent dual is not strictly certified")
    if parent_dual.get("lp_transcript_sha256") != hashes[LP_182.name]:
        raise RuntimeError("182-column dual does not pin its LP transcript")
    if parent_dual.get("canonical_all_columns_sha256_le_f64") != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("182-column parent dual and LP disagree on the canonical pool")
    if screen.get("dual_certificate_sha256") != hashes[DUAL_182.name]:
        raise RuntimeError("pricing screen does not pin the strict 182-column dual")
    if screen.get("lp_transcript_sha256") != hashes[LP_182.name]:
        raise RuntimeError("pricing screen does not pin the 182-column LP")
    if screen.get("cut_lp_transcript_sha256") != hashes[CUT_LP_152.name]:
        raise RuntimeError("pricing screen does not pin the 152-column row inventory")
    if pricing.get("status") != "arb_positive_columns_found":
        raise RuntimeError("182-column Arb pricing did not certify positive escapes")
    if pricing.get("dual_certificate_sha256") != hashes[DUAL_182.name]:
        raise RuntimeError("Arb pricing does not pin the strict 182-column dual")
    if pricing.get("lp_transcript_sha256") != hashes[LP_182.name]:
        raise RuntimeError("Arb pricing does not pin the 182-column LP")
    if pricing.get("cut_lp_transcript_sha256") != hashes[CUT_LP_152.name]:
        raise RuntimeError("Arb pricing does not pin the 152-column row inventory")
    if pricing.get("pricing_screen_sha256") != hashes[SCREEN_182.name]:
        raise RuntimeError("Arb pricing does not pin its binary64 screen")
    if screen.get("canonical_all_columns_sha256_le_f64") != parent_dual.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("pricing screen and parent dual disagree on canonical pool")
    if pricing.get("canonical_all_columns_sha256_le_f64") != parent_dual.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("Arb pricing and parent dual disagree on canonical pool")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool shape/hash mismatch")
    if parent_dual.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("182-column certificate does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = sha(all_array.tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != parent_dual["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical pool count/hash mismatch")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    previous_added = [int(x) for x in parent_lp["added_canonical_columns"]]
    previous_order = [int(x) for x in parent_lp["column_order"]]
    if len(base_columns) != 151 or len(previous_added) != 30:
        raise RuntimeError("unexpected 182-column parent inventory")
    if previous_order != base_columns + [ESCAPE_COLUMN] + previous_added:
        raise RuntimeError("182-column parent ordering is inconsistent")
    if len(set(previous_order)) != 182:
        raise RuntimeError("182-column parent contains duplicate labels")

    priced = [item for item in pricing.get("results", []) if item.get("strictly_positive")]
    if len(priced) != EXPECTED_NEW_COLUMNS or pricing.get("arb_certified_positive_count") != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("expected one strictly Arb-positive new canonical column")
    new_added = [int(item["column"]) for item in priced]
    if len(set(new_added)) != EXPECTED_NEW_COLUMNS:
        raise RuntimeError("duplicate new pricing columns")
    active_canonical = set(base_columns + previous_added)
    if active_canonical & set(new_added):
        raise RuntimeError("new pricing columns overlap the 182-column pool")
    if any(column < 0 or column >= CANONICAL_COUNT for column in new_added):
        raise RuntimeError("new pricing column outside the frozen canonical pool")
    for item in priced:
        column = int(item["column"])
        if not np.array_equal(np.asarray(item["couplings"], dtype=np.float64),
                              np.asarray(all_columns[column], dtype=np.float64)):
            raise RuntimeError(f"pricing couplings differ from canonical column {column}")

    escape_couplings = [Fraction(value) for value in candidate["escape_couplings_exact"]]
    if [str(value) for value in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("continuous escape couplings differ from strict Arb input")
    if len(escape_couplings) != 42 or escape_couplings[-1] != 0 or any(value <= 0 for value in escape_couplings[:-1]):
        raise RuntimeError("continuous escape is not a legal positive open path")

    column_labels = previous_order + new_added
    if len(column_labels) != 183 or len(set(column_labels)) != 183:
        raise RuntimeError("expanded physical pool must contain 183 unique columns")
    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [escape_couplings]
        + [all_columns[column] for column in previous_added + new_added]
    )

    sixth_rows = [tuple(int(value) for value in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(value) for value in cut_lp["sixth_cut_targets"]]
    eighth_rows = [tuple(int(value) for value in row) for row in cut_lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(value) for value in cut_lp["selected_eighth_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("the 645-row sixth inventory is incomplete or duplicated")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != parent_lp.get("sixth_rows_sha256") or eighth_hash != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("current 152-column cut LP row inventory differs from the certified 182-column design")
    if len(eighth_rows) != 7 or len(eighth_targets) != 7:
        raise RuntimeError("the seven selected eighth rows changed")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth target mismatch")
    expected_eighth = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    if expected_eighth != eighth_targets:
        raise RuntimeError("selected eighth-order target mismatch")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != parent_lp.get("sixth_rows_sha256") or eighth_hash != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("182-column parent row hashes do not match the frozen 152-column row inventory")

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

    sixth = np.empty((183, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((183, len(eighth_rows)), dtype=np.float64)
    for index, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[index] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (index + 1) % 16 == 0 or index == 182:
            print(f"Built physical feature columns {index + 1}/183", flush=True)

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
    if (m, n) != (2113, 183):
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

    optimized = np.abs(A @ result.x[:-1] - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    dual_z = result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]
    dual_objective = float(result.eqlin.marginals[0] + np.dot(dual_z, y))
    support = [
        {"column": int(column_labels[index]), "weight": float(weight)}
        for index, weight in enumerate(result.x[:-1]) if weight > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())

    transcript = {
        "status": "183col_full_sixth_cut_lp_candidate_below_one_third" if result.fun < 1 / 3 else "183col_full_sixth_cut_lp_above_one_third",
        "parent_candidate_sha256": hashes[CANDIDATE_152.name],
        "historical_parent_152col_lp_sha256": parent_lp["historical_parent_152col_lp_sha256"],
        "historical_parent_152col_dual_certificate_sha256": parent_lp["historical_parent_152col_dual_certificate_sha256"],
        "current_152col_cut_lp_sha256": hashes[CUT_LP_152.name],
        "current_152col_cut_dual_certificate_sha256": hashes[CUT_DUAL_152.name],
        "parent_182col_lp_sha256": hashes[LP_182.name],
        "parent_182col_dual_certificate_sha256": hashes[DUAL_182.name],
        "pricing_screen_sha256": hashes[SCREEN_182.name],
        "pricing_arb_sha256": hashes[PRICING_182.name],
        "original_151col_dual_sha256": hashes[ORIGINAL_DUAL_151.name],
        "continuous_escape_arb_certificate_sha256": hashes[ESCAPE_CERT.name],
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "base_columns": base_columns,
        "continuous_escape_column_index": ESCAPE_COLUMN,
        "previous_added_canonical_columns": previous_added,
        "new_added_canonical_columns": new_added,
        "added_canonical_columns": previous_added + new_added,
        "column_order": column_labels,
        "sixth_rows_sha256": sixth_hash,
        "eighth_rows_sha256": eighth_hash,
        "matrix_and_target_sha256_le_f64": matrix_sha,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized.max()),
        "expanded_block_maxima": {
            name: float(optimized[cuts[index]:cuts[index + 1]].max())
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
            "Binary64 HiGHS discovery on the fixed 2,113-row design, expanding the 182-column "
            "parent pool by one canonical generator whose reduced-cost scores were independently "
            "certified strictly positive with 128-bit Arb. A sub-1/3 result is not a theorem until "
            "the exact rationalized candidate passes Arb on all 2,113 rows and a complete 63,133-orbit "
            "sixth-order audit. An above-cap result is not a theorem until its rationalized dual is "
            "independently Arb-certified against all 183 physical columns."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_out_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (int(column_labels[index]), Fraction.from_float(float(weight)))
            for index, weight in enumerate(result.x[:-1]) if weight > 1e-10
        ]
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": column, "probability": str(weight / total)}
            for column, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("rationalized candidate probabilities do not sum to one")
        next_candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_out_sha,
            "parent_candidate_sha256": hashes[CANDIDATE_152.name],
            "parent_152col_lp_sha256": hashes[CUT_LP_152.name],
            "parent_152col_dual_certificate_sha256": hashes[CUT_DUAL_152.name],
            "parent_182col_lp_sha256": hashes[LP_182.name],
            "parent_182col_dual_certificate_sha256": hashes[DUAL_182.name],
            "pricing_screen_sha256": hashes[SCREEN_182.name],
            "pricing_arb_sha256": hashes[PRICING_182.name],
            "canonical_all_columns_sha256_le_f64": all_sha,
            "seed_pool_sha256_le_f64": seed_sha,
            "base_columns": base_columns,
            "continuous_escape_column_index": ESCAPE_COLUMN,
            "escape_couplings_exact": [str(value) for value in escape_couplings],
            "previous_added_canonical_columns": previous_added,
            "new_added_canonical_columns": new_added,
            "added_canonical_columns": previous_added + new_added,
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
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "selected_eighth_targets": [str(value) for value in eighth_targets],
            "scope": (
                "Exact rational probabilities obtained by normalizing the binary64 183-column "
                "cut-LP weights. This candidate is only constrained on the pinned 2,113 rows; "
                "it requires independent Arb verification and complete sixth-order separation."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(next_candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": transcript["status"],
        "columns": n,
        "rows": m,
        "new_added_canonical_columns": new_added,
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(optimized.max()),
        "block_maxima": transcript["expanded_block_maxima"],
        "support_size": len(support),
        "primal_dual_gap": transcript["dual_discovery"]["primal_dual_gap"],
        "candidate_written": candidate_written,
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if candidate_written else None,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
