"""128-bit Arb dual certificate for the 172-column, 2,106-row sixth-only discovery LP."""
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

LP_PATH = ROOT / "evidence/joint_low_six_lp_172col_sixth_only_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DUAL162_PATH = ROOT / "evidence/55probe_162col_sixth_only_dual_certificate_n21.json"
LP162_SIXTH_PATH = ROOT / "evidence/joint_low_six_lp_162col_sixth_only_n21.json"
SCREEN_PATH = ROOT / "evidence/55probe_162col_sixth_only_dual_pricing_screen_n21.json"
PRICING_ARB_PATH = ROOT / "evidence/55probe_162col_sixth_only_dual_pricing_arb_n21.json"
ESCAPE_CERT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_172col_sixth_only_dual_certificate_n21.json"
PRECISION_BITS = 128
SIXTH_SCALE = Fraction(5, 19721)


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
        d = row + 1
        total = arb(0)
        for i in range(42):
            j = (i + d) % 42
            total += entries[i][i] * entries[j][j] - entries[i][j] * entries[j][i]
        return total / 42
    group = fourth_groups[row - 21]
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[int(i)][int(j)] for j in subset] for i in subset]).det()
    return total / len(group)


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        LP_PATH, PARENT_LP_PATH, CUT_LP_PATH, DUAL162_PATH, LP162_SIXTH_PATH,
        SCREEN_PATH, PRICING_ARB_PATH, ESCAPE_CERT_PATH, SEED_POOL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    (
        lp, parent_lp, cut_lp, dual162, lp162_sixth, screen, pricing, escape, seed_raw
    ) = [
        json.loads(value) if path.suffix != ".npy" else value
        for path, value in zip(paths, raw)
    ]
    (
        lp_sha, parent_lp_sha, cut_lp_sha, dual162_sha, lp162_sixth_sha,
        screen_sha, pricing_sha, escape_sha, seed_file_sha,
    ) = map(sha, raw)

    if (lp.get("columns"), lp.get("rows")) != (172, 2106):
        raise RuntimeError("unexpected 172-column sixth-only LP dimensions")
    if lp.get("status") != "172col_sixth_only_lp_above_one_third":
        raise RuntimeError("172-column LP is not the expected above-cap discovery")
    if lp.get("parent_162col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("172-column LP does not pin its 162-column physical parent")
    if lp.get("parent_sixth_only_dual_certificate_sha256") != dual162_sha:
        raise RuntimeError("172-column LP does not pin the exact 162-column sixth-only dual")
    if lp.get("parent_sixth_only_lp_sha256") != lp162_sixth_sha:
        raise RuntimeError("172-column LP does not pin the 162-column sixth-only LP")
    if lp.get("pricing_screen_sha256") != screen_sha or lp.get("pricing_arb_sha256") != pricing_sha:
        raise RuntimeError("172-column LP does not pin the pricing evidence")
    if lp.get("parent_sixth_row_inventory_sha256") != cut_lp_sha:
        raise RuntimeError("172-column LP does not pin the sixth-row inventory")
    if dual162.get("status") != "strict_162col_2106row_sixth_only_minimax_obstruction" or not dual162.get("complete"):
        raise RuntimeError("parent 162-column sixth-only dual certificate is incomplete")
    if dual162.get("lp_transcript_sha256") != lp162_sixth_sha:
        raise RuntimeError("parent 162-column dual does not pin its LP")
    if dual162.get("parent_162col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("parent 162-column dual does not pin its physical LP")
    if dual162.get("parent_152col_cut_lp_sha256") != cut_lp_sha:
        raise RuntimeError("parent 162-column dual does not pin the sixth-row inventory")
    if dual162.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("parent dual does not pin the continuous-path Arb certificate")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
        raise RuntimeError("continuous path generator lacks its strict Arb certificate")
    if pricing.get("status") != "arb_positive_columns_found":
        raise RuntimeError("ten-column Arb pricing evidence is incomplete")
    if pricing.get("dual_certificate_sha256") != dual162_sha:
        raise RuntimeError("pricing Arb transcript does not pin the parent dual")
    if pricing.get("lp_transcript_sha256") != lp162_sixth_sha:
        raise RuntimeError("pricing Arb transcript does not pin the parent sixth-only LP")
    if pricing.get("pricing_screen_sha256") != screen_sha:
        raise RuntimeError("pricing Arb transcript does not pin the binary64 screen")
    if pricing.get("candidates_checked") != 10 or pricing.get("arb_certified_positive_count") != 10:
        raise RuntimeError("not all ten new canonical columns have strict Arb-positive intervals")
    if screen.get("dual_certificate_sha256") != dual162_sha or screen.get("lp_transcript_sha256") != lp162_sixth_sha:
        raise RuntimeError("binary64 screen does not pin the parent sixth-only dual and LP")
    if screen.get("parent_162col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("binary64 screen does not pin the 162-column physical parent")
    if screen.get("parent_sixth_row_inventory_sha256") != cut_lp_sha:
        raise RuntimeError("binary64 screen does not pin the sixth-row inventory")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen canonical pool hash/count mismatch")
    if all_sha != dual162.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("parent dual and expanded LP use different canonical pools")

    base_columns = [int(x) for x in lp["base_columns"]]
    old_added = [int(x) for x in lp["previous_added_canonical_columns"]]
    new_added = [int(x) for x in lp["added_canonical_columns"]]
    escape_couplings = [Fraction(x) for x in escape["candidate_couplings_exact"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("malformed original canonical base")
    if len(old_added) != 10 or len(set(old_added)) != 10:
        raise RuntimeError("malformed previous ten-column extension")
    if len(new_added) != 10 or len(set(new_added)) != 10:
        raise RuntimeError("malformed new ten-column extension")
    if set(base_columns) & set(old_added) or set(base_columns) & set(new_added) or set(old_added) & set(new_added):
        raise RuntimeError("canonical physical column inventories overlap")
    if [int(x) for x in parent_lp["base_columns"]] != base_columns:
        raise RuntimeError("expanded LP changed the original canonical base")
    if [int(x) for x in parent_lp["added_canonical_columns"]] != old_added:
        raise RuntimeError("expanded LP changed the previous canonical additions")
    parent_order = base_columns + [1641] + old_added
    if parent_lp.get("column_order") != parent_order or dual162.get("columns") != parent_order:
        raise RuntimeError("parent 162-column physical ordering mismatch")
    column_order = base_columns + [1641] + old_added + new_added
    if lp.get("column_order") != column_order or len(column_order) != 172 or len(set(column_order)) != 172:
        raise RuntimeError("172-column physical ordering mismatch")

    priced_results = [item for item in pricing.get("results", []) if item.get("strictly_positive")]
    if [int(item["column"]) for item in priced_results] != new_added:
        raise RuntimeError("new canonical additions differ from the strict Arb pricing order")
    for item in priced_results:
        j = int(item["column"])
        if not np.array_equal(
            np.asarray(item["couplings"], dtype=np.float64),
            np.asarray(all_columns[j], dtype=np.float64),
        ):
            raise RuntimeError(f"Arb-priced coupling payload differs from frozen canonical column {j}")

    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in old_added]
        + [all_columns[j] for j in new_added]
    )
    if len(physical_columns) != 172:
        raise RuntimeError("expanded physical column count mismatch")

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    low_targets = list(system.rational_target)
    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(x) for x in cut_lp["sixth_cut_targets"]]
    if len(low_targets) != 1461 or len(sixth_rows) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("unexpected complete low/sixth row inventory")
    if any(len(row) != 6 or tuple(sorted(set(row))) != row for row in sixth_rows):
        raise RuntimeError("malformed sixth-order orbit representative")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-order target mismatch")
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or sixth_hash != parent_lp.get("sixth_rows_sha256"):
        raise RuntimeError("sixth-order row inventory hash mismatch")

    y = (
        [value / scale for value, scale in zip(low_targets, low_scales)]
        + [value / SIXTH_SCALE for value in sixth_targets]
    )
    if len(y) != 2106 or lp.get("row_blocks") != {"low_complete": 1461, "sixth_selected_plus_all_cuts": 645}:
        raise RuntimeError("sixth-only exact target vector dimensions mismatch")

    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("172-column LP transcript lacks dual multipliers")
    m = len(y)
    marginals = discovery.get("inequality_marginals", [])
    if len(marginals) != 2 * m:
        raise RuntimeError("wrong 172-column dual marginal count")
    first = [Fraction.from_float(float(value)) for value in marginals[:m]]
    second = [Fraction.from_float(float(value)) for value in marginals[m:]]
    z_raw = [a - b for a, b in zip(first, second)]
    lam_raw = Fraction.from_float(float(discovery["equality_marginal"]))
    norm_raw = sum((abs(value) for value in z_raw), Fraction(0))
    dual_scale = max(Fraction(1), norm_raw)
    z = [value / dual_scale for value in z_raw]
    lam = lam_raw / dual_scale
    norm = sum((abs(value) for value in z), Fraction(0))
    if norm > 1:
        raise RuntimeError("exact rational 172-column dual L1 norm exceeds one")
    objective = lam + sum((a * b for a, b in zip(z, y)), Fraction(0))
    if objective <= Fraction(1, 3):
        raise RuntimeError("rationalized 172-column dual objective no longer exceeds 1/3")

    z_arb = [ball(value) for value in z]
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if i >= 1461]
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
        column_lhs.append(lhs + ball(lam))
        print(
            f"Arb-evaluated 172-column dual column {len(column_lhs)}/172 "
            f"(column {column}); active rows {len(active_rows)}/{m}",
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
        if objective - delta <= Fraction(1, 3):
            continue
        shifted = [value - ball(delta) for value in column_lhs]
        if all(value.upper() <= 0 for value in shifted):
            selected_delta = delta
            selected_intervals = shifted
            break
    if selected_delta is None:
        maximum = max(float(value.upper()) for value in column_lhs)
        raise RuntimeError(f"could not certify all 172 column inequalities; max upper={maximum}")

    lower = objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    sixth_only = len(active_low) == 0
    status = (
        "strict_172col_2106row_sixth_only_minimax_obstruction"
        if sixth_only else "strict_172col_2106row_mixed_order_minimax_obstruction"
    )
    scope = (
        "Rigorous complete-sixth-order minimax lower bound for every convex mixture over the fixed "
        "172 physical generators: the exact dual is supported only on sixth-order rows, all drawn "
        "from the complete 63,133-orbit D42 sixth-order domain. This remains a finite-pool theorem "
        "and does not exclude additional physical generators or the unrestricted continuous family."
        if sixth_only else
        "Rigorous mixed-order minimax lower bound for every convex mixture over the fixed 172 physical "
        "generators, using a subset of the complete second/fourth/sixth moment rows. This remains a "
        "finite-pool theorem and does not exclude additional physical generators or the unrestricted "
        "continuous family."
    )
    result = {
        "status": status,
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_162col_lp_sha256": parent_lp_sha,
        "parent_sixth_only_dual_certificate_sha256": dual162_sha,
        "parent_sixth_only_lp_sha256": lp162_sixth_sha,
        "pricing_screen_sha256": screen_sha,
        "pricing_arb_sha256": pricing_sha,
        "parent_sixth_row_inventory_sha256": cut_lp_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": len(column_order),
        "base_columns": base_columns,
        "continuous_escape_column_index": 1641,
        "previous_added_canonical_columns": old_added,
        "added_canonical_columns": new_added,
        "row_count": len(y),
        "row_blocks": {"low_complete": 1461, "sixth_selected_plus_all_cuts": 645},
        "sixth_rows_sha256": sixth_hash,
        "active_dual_rows": len(active_rows),
        "active_dual_low_rows": len(active_low),
        "active_dual_sixth_rows": len(active_sixth),
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_l1_norm_exact": str(norm),
        "dual_scale_applied": str(dual_scale),
        "dual_lambda_exact": str(lam),
        "dual_objective_exact": str(objective),
        "dual_slack_delta": str(selected_delta),
        "certified_minimax_lower_bound": str(lower),
        "strict_lower_bound_above_one_third": str(lower - Fraction(1, 3)),
        "maximum_arb_upper_of_column_dual_lhs_minus_slack": str(maximum_upper),
        "column_dual_lhs_intervals": [
            {"column": column, "interval": str(value)}
            for column, value in zip(column_order, selected_intervals)
        ],
        "dual_vector_rational": [str(value) for value in z],
        "scope": scope,
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": status,
        "columns": len(column_order),
        "rows": len(y),
        "active_dual_rows": len(active_rows),
        "active_low": len(active_low),
        "active_sixth": len(active_sixth),
        "dual_l1_norm_exact": str(norm),
        "dual_objective_exact": str(objective),
        "certified_minimax_lower_bound": str(lower),
        "gap_above_one_third": str(lower - Fraction(1, 3)),
        "selected_slack": str(selected_delta),
        "max_arb_upper": str(maximum_upper),
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
