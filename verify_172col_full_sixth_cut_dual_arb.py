"""128-bit Arb certificate for the 172-column / 2,113-row full-sixth cut LP."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit, target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_172col_full_sixth_cuts_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP_152 = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL_152 = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
LP_162 = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
DUAL_162 = ROOT / "evidence/55probe_162col_full_sixth_cut_dual_certificate_n21.json"
SCREEN_162 = ROOT / "evidence/55probe_162col_full_sixth_cut_dual_pricing_screen_n21.json"
PRICING_162 = ROOT / "evidence/55probe_162col_full_sixth_cut_dual_pricing_arb_n21.json"
ORIGINAL_DUAL_151 = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT_PATH = ROOT / "evidence/55probe_172col_full_sixth_cut_dual_certificate_n21.json"

PRECISION_BITS = 128
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)
ESCAPE_COLUMN = 1641


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def orbit_average_minor(entries, indices):
    group = orbit(indices, 42)
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
    return total / len(group)


def active_low_feature(system, entries, row, fourth_groups):
    if row < 21:
        distance = row + 1
        total = arb(0)
        for index in range(42):
            other = (index + distance) % 42
            total += (
                entries[index][index] * entries[other][other]
                - entries[index][other] * entries[other][index]
            )
        return total / 42
    group = fourth_groups[row - 21]
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[int(i)][int(j)] for j in subset] for i in subset]).det()
    return total / len(group)


def load_exact_design(cut_lp):
    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    low_targets = list(system.rational_target)
    if len(low_targets) != 1461:
        raise RuntimeError("unexpected complete low-order row count")

    sixth_rows = [tuple(int(value) for value in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(value) for value in cut_lp["sixth_cut_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("unexpected 645-row sixth inventory")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth target mismatch")

    eighth_rows = [tuple(int(value) for value in row) for row in cut_lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(value) for value in cut_lp["selected_eighth_targets"]]
    if len(eighth_rows) != 7 or len(eighth_targets) != 7:
        raise RuntimeError("unexpected selected eighth-order inventory")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != parent_lp.get("sixth_rows_sha256") or eighth_hash != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("current 152-column row inventory differs from the certified 162-column design")
    expected_eighth = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    if expected_eighth != eighth_targets:
        raise RuntimeError("selected eighth target mismatch")

    y = (
        [value / scale for value, scale in zip(low_targets, low_scales)]
        + [value / SIXTH_SCALE for value in sixth_targets]
        + [value / EIGHTH_SCALE for value in eighth_targets]
    )
    blocks = {
        "low_complete": len(low_targets),
        "sixth_selected_plus_all_cuts": len(sixth_rows),
        "eighth_selected": len(eighth_rows),
    }
    if len(y) != 2113:
        raise RuntimeError("unexpected exact target dimension")
    return system, low_scales, sixth_rows, eighth_rows, y, blocks


def load_rational_dual(lp, y):
    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("172-column LP lacks HiGHS dual discovery data")
    m = len(y)
    marginals = discovery.get("inequality_marginals", [])
    if len(marginals) != 2 * m:
        raise RuntimeError("unexpected number of inequality marginals")
    first = [Fraction.from_float(float(value)) for value in marginals[:m]]
    second = [Fraction.from_float(float(value)) for value in marginals[m:]]
    z_raw = [a - b for a, b in zip(first, second)]
    lam_raw = Fraction.from_float(float(discovery["equality_marginal"]))
    norm_raw = sum((abs(value) for value in z_raw), Fraction(0))
    scale = max(Fraction(1), norm_raw)
    z = [value / scale for value in z_raw]
    lam = lam_raw / scale
    norm = sum((abs(value) for value in z), Fraction(0))
    if norm > 1:
        raise RuntimeError("exact rational dual L1 norm exceeds one")
    objective = lam + sum((value * target_value for value, target_value in zip(z, y)), Fraction(0))
    if objective <= Fraction(1, 3):
        raise RuntimeError("rationalized dual objective does not exceed 1/3")
    return z, lam, norm, scale, objective


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        LP_PATH, CANDIDATE_152, CUT_LP_152, CUT_DUAL_152, LP_162, DUAL_162,
        SCREEN_162, PRICING_162, ORIGINAL_DUAL_151, ESCAPE_CERT, SEED_POOL,
    )
    raw = [path.read_bytes() for path in paths]
    values = [
        json.loads(value) if path.suffix != ".npy" else value
        for path, value in zip(paths, raw)
    ]
    (
        lp, candidate, cut_lp, cut_dual, parent_lp, parent_dual,
        screen, pricing, original_dual, escape, seed_raw,
    ) = values
    (
        lp_sha, candidate_sha, cut_lp_sha, cut_dual_sha, parent_lp_sha,
        parent_dual_sha, screen_sha, pricing_sha, original_dual_sha,
        escape_sha, seed_file_sha,
    ) = map(sha, raw)

    if lp.get("status") != "172col_full_sixth_cut_lp_above_one_third":
        raise RuntimeError("172-column LP is not an above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (172, 2113):
        raise RuntimeError("unexpected 172-column / 2,113-row dimensions")
    if lp.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("172-column LP does not pin the 152-column candidate")
    if lp.get("current_152col_cut_lp_sha256") != cut_lp_sha:
        raise RuntimeError("172-column LP does not pin the current 152-column cut LP")
    if lp.get("current_152col_cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("172-column LP does not pin the current 152-column cut dual")
    if lp.get("historical_parent_152col_lp_sha256") != parent_lp.get("parent_lp_sha256"):
        raise RuntimeError("172-column LP historical 152-column LP hash mismatch")
    if lp.get("historical_parent_152col_dual_certificate_sha256") != parent_lp.get("parent_dual_certificate_sha256"):
        raise RuntimeError("172-column LP historical 152-column dual hash mismatch")
    if lp.get("parent_162col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("172-column LP does not pin the 162-column LP")
    if lp.get("parent_162col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("172-column LP does not pin the 162-column dual")
    if lp.get("pricing_screen_sha256") != screen_sha or lp.get("pricing_arb_sha256") != pricing_sha:
        raise RuntimeError("172-column LP pricing hashes disagree")
    if lp.get("canonical_all_columns_sha256_le_f64") != parent_dual.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("172-column LP and parent dual disagree on canonical pool")
    if parent_dual.get("status") != "strict_162col_2113row_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("162-column parent dual is not strictly certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("162-column dual does not pin its LP")
    if parent_lp.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("162-column parent does not pin the 152-column candidate")
    if parent_dual.get("parent_152col_lp_sha256") != parent_lp.get("parent_lp_sha256"):
        raise RuntimeError("162-column LP/certificate historical 152-column LP hashes disagree")
    if parent_dual.get("parent_152col_dual_certificate_sha256") != parent_lp.get("parent_dual_certificate_sha256"):
        raise RuntimeError("162-column LP/certificate historical 152-column dual hashes disagree")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column parent dual is not strictly certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("current 152-column dual does not pin its LP")
    if cut_dual.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("current 152-column dual does not pin the exact candidate")
    if candidate.get("parent_dual_certificate_sha256") != original_dual_sha:
        raise RuntimeError("152-column candidate does not pin original 151-column dual")
    if candidate.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("152-column candidate does not pin continuous escape")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous path escape is not Arb-certified")
    if screen.get("dual_certificate_sha256") != parent_dual_sha or screen.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("162-column pricing screen provenance mismatch")
    if screen.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("162-column pricing screen row provenance mismatch")
    if pricing.get("dual_certificate_sha256") != parent_dual_sha or pricing.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("162-column Arb pricing provenance mismatch")
    if pricing.get("cut_lp_transcript_sha256") != cut_lp_sha or pricing.get("pricing_screen_sha256") != screen_sha:
        raise RuntimeError("162-column Arb pricing screen/row provenance mismatch")
    if pricing.get("status") != "arb_positive_columns_found" or pricing.get("arb_certified_positive_count") != 10:
        raise RuntimeError("ten strict Arb-positive parent escapes are not present")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed pool hash/shape mismatch")
    if parent_dual.get("seed_pool_sha256_le_f64") != seed_sha or lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("172-column LP/parent dual seed-pool provenance mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical pool hash/count mismatch")

    base_columns = [int(value) for value in lp["base_columns"]]
    previous_added = [int(value) for value in lp["previous_added_canonical_columns"]]
    new_added = [int(value) for value in lp["new_added_canonical_columns"]]
    column_order = [int(value) for value in lp["column_order"]]
    expected_order = base_columns + [ESCAPE_COLUMN] + previous_added + new_added
    if len(base_columns) != 151 or len(previous_added) != 10 or len(new_added) != 10:
        raise RuntimeError("unexpected 172-column inventory")
    if column_order != expected_order or len(set(column_order)) != 172:
        raise RuntimeError("172-column ordering mismatch")
    if lp["added_canonical_columns"] != previous_added + new_added:
        raise RuntimeError("combined added-column inventory mismatch")
    priced_results = [item for item in pricing["results"] if item.get("strictly_positive")]
    if [int(item["column"]) for item in priced_results] != new_added:
        raise RuntimeError("172-column LP does not use exactly the Arb-positive pricing columns")

    escape_couplings = [Fraction(value) for value in candidate["escape_couplings_exact"]]
    if [str(value) for value in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("continuous escape coupling mismatch")
    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [escape_couplings]
        + [all_columns[column] for column in previous_added + new_added]
    )
    if len(physical_columns) != 172:
        raise RuntimeError("wrong physical column count")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut_lp)
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("172-column row inventory hash mismatch")
    if row_blocks != lp.get("row_blocks"):
        raise RuntimeError("172-column row-block inventory mismatch")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    z_arb = [ball(value) for value in z]
    active_rows = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active_rows if index < 1461]
    active_sixth = [index for index in active_rows if 1461 <= index < 2106]
    active_eighth = [index for index in active_rows if index >= 2106]
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }

    column_lhs = []
    index_hash = hashlib.sha256()
    for column, couplings in zip(column_order, physical_columns):
        index_hash.update(int(column).to_bytes(4, "little", signed=False))
        entries = rotation_entries_exact(couplings)
        lhs = arb(0)
        for row in active_low:
            lhs += z_arb[row] * active_low_feature(system, entries, row, fourth_groups) / ball(low_scales[row])
        for row in active_sixth:
            lhs += z_arb[row] * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(SIXTH_SCALE)
        for row in active_eighth:
            offset = 1461 + len(sixth_rows)
            lhs += z_arb[row] * orbit_average_minor(entries, eighth_rows[row - offset]) / ball(EIGHTH_SCALE)
        column_lhs.append(lhs + ball(lam))
        print(
            f"Arb-evaluated dual column {len(column_lhs)}/172 (column {column}); "
            f"active rows {len(active_rows)}/{len(y)}",
            flush=True,
        )

    deltas = [
        Fraction(0), Fraction(1, 10**12), Fraction(1, 10**10),
        Fraction(1, 10**9), Fraction(1, 10**8), Fraction(1, 10**7),
        Fraction(1, 10**6), Fraction(1, 10**5), Fraction(1, 10**4),
    ]
    selected_delta = None
    selected_intervals = None
    for delta in deltas:
        if dual_objective - delta <= Fraction(1, 3):
            continue
        shifted = [value - ball(delta) for value in column_lhs]
        if all(value.upper() <= 0 for value in shifted):
            selected_delta = delta
            selected_intervals = shifted
            break
    if selected_delta is None:
        maximum = max(float(value.upper()) for value in column_lhs)
        raise RuntimeError(f"could not certify all 172 dual inequalities; max unshifted upper={maximum}")

    lower = dual_objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_172col_2113row_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_candidate_sha256": candidate_sha,
        "parent_152col_lp_sha256": cut_lp_sha,
        "parent_152col_dual_certificate_sha256": cut_dual_sha,
        "parent_162col_lp_sha256": parent_lp_sha,
        "parent_162col_dual_certificate_sha256": parent_dual_sha,
        "pricing_screen_sha256": screen_sha,
        "pricing_arb_sha256": pricing_sha,
        "original_151col_dual_sha256": original_dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": 172,
        "previous_added_canonical_columns": previous_added,
        "new_added_canonical_columns": new_added,
        "row_count": len(y),
        "row_blocks": row_blocks,
        "total_sixth_rows": len(sixth_rows),
        "active_dual_rows": len(active_rows),
        "active_dual_low_rows": len(active_low),
        "active_dual_sixth_rows": len(active_sixth),
        "active_dual_eighth_rows": len(active_eighth),
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_convention": "z = first m HiGHS inequality marginals minus second m; lambda is the sum-to-one equality marginal",
        "dual_l1_norm_exact": str(norm),
        "dual_scale_applied": str(dual_scale),
        "dual_lambda_exact": str(lam),
        "dual_objective_exact": str(dual_objective),
        "dual_slack_delta": str(selected_delta),
        "certified_minimax_lower_bound": str(lower),
        "strict_lower_bound_above_one_third": str(lower - Fraction(1, 3)),
        "maximum_arb_upper_of_column_dual_lhs_minus_slack": str(maximum_upper),
        "column_dual_lhs_intervals": [
            {"column": column, "interval": str(value)}
            for column, value in zip(column_order, selected_intervals)
        ],
        "dual_vector_rational": [str(value) for value in z],
        "scope": (
            "Rigorous mixed-order minimax lower bound for every convex mixture over the 172 pinned "
            "physical generators on the exact 2,113-row design: all 1,461 second/fourth rows, 645 "
            "selected sixth-order rows (including the 334 cuts found by the complete binary64 scan "
            "of the preceding 152-column candidate), and seven selected eighth-order rows. This is "
            "not a complete-sixth/eighth orbit certificate and does not exclude additional physical "
            "generators or the unrestricted continuous family."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "column_count": 172,
        "row_count": len(y),
        "active_dual_rows": len(active_rows),
        "active_row_blocks": {
            "low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)
        },
        "dual_l1_norm_exact": str(norm),
        "dual_objective_exact": str(dual_objective),
        "certified_minimax_lower_bound": str(lower),
        "gap_above_one_third": str(lower - Fraction(1, 3)),
        "selected_slack": str(selected_delta),
        "max_arb_upper": str(maximum_upper),
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
