"""Independent 128-bit Arb certificate for the 185-column mixed-order minimax LP."""
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

LP_PATH = ROOT / "evidence/joint_low_six_lp_185col_mixed_order_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_lp_182col_sixth_only_n21.json"
PARENT_DUAL_PATH = ROOT / "evidence/55probe_182col_sixth_only_dual_certificate_n21.json"
PARENT_SCREEN_PATH = ROOT / "evidence/55probe_182col_mixed_order_dual_pricing_screen_n21.json"
PARENT_PRICING_ARB_PATH = ROOT / "evidence/55probe_182col_mixed_order_dual_pricing_arb_n21.json"
PARENT_162_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
ESCAPE_CERT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_185col_mixed_order_dual_certificate_n21.json"
THEORY_PATH = ROOT / "THEORY_185COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md"
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


def verify_theorem_file_exists():
    # The formal theorem is maintained as a reviewed source document.
    # The Arb verifier must not overwrite its LaTeX with a generated summary.
    if not THEORY_PATH.exists():
        raise RuntimeError("formal 185-column theorem document is missing")



def main():
    ctx.prec = PRECISION_BITS
    paths = (
        LP_PATH, PARENT_LP_PATH, PARENT_DUAL_PATH, PARENT_SCREEN_PATH,
        PARENT_PRICING_ARB_PATH, PARENT_162_LP_PATH, CUT_LP_PATH,
        ESCAPE_CERT_PATH, SEED_POOL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    (
        lp, parent_lp, parent_dual, parent_screen, parent_pricing,
        parent_162_lp, cut_lp, escape, seed_raw,
    ) = [
        json.loads(value) if path.suffix != ".npy" else value
        for path, value in zip(paths, raw)
    ]
    (
        lp_sha, parent_lp_sha, parent_dual_sha, screen_sha, pricing_sha,
        parent_162_lp_sha, cut_lp_sha, escape_sha, seed_file_sha,
    ) = map(sha, raw)

    if (lp.get("columns"), lp.get("rows")) != (185, 2106):
        raise RuntimeError("unexpected 185-column mixed-order LP dimensions")
    if lp.get("status") != "185col_mixed_order_lp_above_one_third":
        raise RuntimeError("185-column LP is not the expected above-cap discovery")
    if float(lp.get("objective", 0.0)) <= 1 / 3:
        raise RuntimeError("185-column LP objective is not above one third")

    if lp.get("parent_182col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("185-column LP does not pin the exact 182-column parent LP")
    if lp.get("parent_182col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("185-column LP does not pin the exact 182-column parent dual")
    if lp.get("pricing_screen_sha256") != screen_sha or lp.get("pricing_arb_sha256") != pricing_sha:
        raise RuntimeError("185-column LP does not pin its parent pricing evidence")
    if lp.get("parent_172col_lp_sha256") != parent_lp.get("parent_172col_lp_sha256"):
        raise RuntimeError("185-column LP and parent 182 LP disagree on the 172-column ancestor")
    # The 185-column discovery transcript pins the 182-column parent dual directly;
    # the 182-column LP and its Arb certificate carry the 172-column dual hash.
    # Verify that ancestor link below rather than requiring a redundant 185-LP field.
    if lp.get("parent_162col_lp_sha256") != parent_162_lp_sha:
        raise RuntimeError("185-column LP does not pin its 162-column ancestor")
    if lp.get("parent_sixth_row_inventory_sha256") != cut_lp_sha:
        raise RuntimeError("185-column LP does not pin its sixth-row inventory")
    if lp.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("185-column LP does not pin the continuous-path Arb certificate")

    if (parent_lp.get("columns"), parent_lp.get("rows")) != (182, 2106):
        raise RuntimeError("unexpected parent 182-column LP dimensions")
    if parent_lp.get("status") != "182col_sixth_only_lp_above_one_third":
        raise RuntimeError("parent 182-column LP has unexpected status")
    if parent_dual.get("status") != "strict_182col_2106row_mixed_order_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("parent 182-column mixed-order Arb certificate is incomplete")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("parent 182-column certificate does not pin its LP")
    if parent_dual.get("parent_172col_lp_sha256") != parent_lp.get("parent_172col_lp_sha256"):
        raise RuntimeError("parent 182 dual and LP disagree on 172-column ancestor")
    if parent_dual.get("parent_172col_dual_certificate_sha256") != parent_lp.get("parent_172col_dual_certificate_sha256"):
        raise RuntimeError("parent 182 dual and LP disagree on 172-column dual")
    if parent_dual.get("parent_162col_lp_sha256") != parent_162_lp_sha:
        raise RuntimeError("parent 182 dual does not pin the 162-column ancestor")
    if parent_dual.get("parent_sixth_row_inventory_sha256") != cut_lp_sha:
        raise RuntimeError("parent 182 dual does not pin the sixth-row inventory")
    if parent_dual.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("parent 182 dual does not pin the continuous-path certificate")

    if parent_pricing.get("status") != "arb_positive_columns_found":
        raise RuntimeError("parent 182-column pricing Arb transcript is incomplete")
    if parent_pricing.get("dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("parent pricing does not pin the exact 182-column dual")
    if parent_pricing.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("parent pricing does not pin the 182-column LP")
    if parent_pricing.get("pricing_screen_sha256") != screen_sha:
        raise RuntimeError("parent pricing does not pin the binary64 screen")
    if parent_pricing.get("candidates_checked") != 3 or parent_pricing.get("arb_certified_positive_count") != 3:
        raise RuntimeError("parent pricing does not contain exactly three strict Arb-positive columns")
    if parent_screen.get("dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("parent screen does not pin the 182-column dual")
    if parent_screen.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("parent screen does not pin the 182-column LP")
    if parent_screen.get("unused_column_count") != 1460 or parent_screen.get("canonical_column_count") != 1641:
        raise RuntimeError("unexpected parent canonical pricing inventory")
    if parent_162_lp.get("columns") != 162 or parent_162_lp.get("rows") != 2113:
        raise RuntimeError("162-column ancestor inventory mismatch")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
        raise RuntimeError("continuous-path generator lacks its strict Arb certificate")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical pool hash/count mismatch")
    if all_sha != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("parent and expanded LP use different canonical pools")

    base_columns = [int(x) for x in lp["base_columns"]]
    previous_added = [int(x) for x in lp["previous_added_canonical_columns"]]
    new_added = [int(x) for x in lp["added_canonical_columns"]]
    escape_couplings = [Fraction(x) for x in escape["candidate_couplings_exact"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("malformed 151-column canonical base")
    if len(previous_added) != 30 or len(set(previous_added)) != 30:
        raise RuntimeError("malformed 30-column prior extension")
    if len(new_added) != 3 or len(set(new_added)) != 3:
        raise RuntimeError("malformed three-column extension")
    if set(base_columns) & set(previous_added) or set(base_columns) & set(new_added) or set(previous_added) & set(new_added):
        raise RuntimeError("canonical physical inventories overlap")

    parent_order = base_columns + [1641] + previous_added
    if parent_lp.get("column_order") != parent_order or parent_dual.get("columns") != parent_order:
        raise RuntimeError("parent 182-column physical ordering mismatch")
    if lp.get("column_order") != parent_order + new_added:
        raise RuntimeError("185-column physical ordering mismatch")
    column_order = parent_order + new_added
    if len(column_order) != 185 or len(set(column_order)) != 185:
        raise RuntimeError("expanded physical column count mismatch")

    priced_results = [item for item in parent_pricing.get("results", []) if item.get("strictly_positive")]
    if [int(item["column"]) for item in priced_results] != new_added:
        raise RuntimeError("new canonical additions differ from strict Arb pricing order")
    for item in priced_results:
        j = int(item["column"])
        if not np.array_equal(np.asarray(item["couplings"], dtype=np.float64), np.asarray(all_columns[j], dtype=np.float64)):
            raise RuntimeError(f"Arb-priced couplings differ from frozen canonical column {j}")

    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in previous_added]
        + [all_columns[j] for j in new_added]
    )
    if len(physical_columns) != 185:
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
        raise RuntimeError("exact target vector dimensions mismatch")

    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("185-column LP transcript lacks dual multipliers")
    m = len(y)
    marginals = discovery.get("inequality_marginals", [])
    if len(marginals) != 2 * m:
        raise RuntimeError("wrong 185-column dual marginal count")
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
        raise RuntimeError("exact rational dual L1 norm exceeds one")
    objective = lam + sum((a * b for a, b in zip(z, y)), Fraction(0))
    if objective <= Fraction(1, 3):
        raise RuntimeError("rationalized dual objective no longer exceeds one third")

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
            f"Arb-evaluated 185-column dual column {len(column_lhs)}/185 "
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
        raise RuntimeError(f"could not certify all 185 column inequalities; max upper={maximum}")

    lower = objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    status = (
        "strict_185col_2106row_sixth_only_minimax_obstruction"
        if not active_low else "strict_185col_2106row_mixed_order_minimax_obstruction"
    )
    scope = (
        "Rigorous complete-sixth-order minimax lower bound for every convex mixture over the fixed "
        "185 physical generators: the exact dual is supported only on sixth-order rows, all drawn "
        "from the complete 63,133-orbit D42 sixth-order domain. This remains a finite-pool theorem."
        if not active_low else
        "Rigorous mixed-order minimax lower bound for every convex mixture over the fixed 185 physical "
        "generators, using a subset of the complete second/fourth/sixth moment rows. The exact dual "
        "support contains both low-order and sixth-order rows; this is a finite-pool theorem."
    )
    result = {
        "status": status,
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_182col_lp_sha256": parent_lp_sha,
        "parent_182col_dual_certificate_sha256": parent_dual_sha,
        "parent_172col_lp_sha256": parent_lp.get("parent_172col_lp_sha256"),
        "parent_172col_dual_certificate_sha256": parent_lp.get("parent_172col_dual_certificate_sha256"),
        "parent_162col_lp_sha256": parent_162_lp_sha,
        "parent_sixth_row_inventory_sha256": cut_lp_sha,
        "pricing_screen_sha256": screen_sha,
        "pricing_arb_sha256": pricing_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": len(column_order),
        "base_columns": base_columns,
        "continuous_escape_column_index": 1641,
        "previous_added_canonical_columns": previous_added,
        "added_canonical_columns": new_added,
        "row_count": len(y),
        "row_blocks": {"low_complete": 1461, "sixth_selected_plus_all_cuts": 645},
        "sixth_rows_sha256": sixth_hash,
        "active_dual_rows": len(active_rows),
        "active_dual_low_rows": len(active_low),
        "active_dual_sixth_rows": len(active_sixth),
        "active_dual_low_row_indices": active_low,
        "active_dual_sixth_row_indices": active_sixth,
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
    verify_theorem_file_exists()
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
        "certificate": str(OUTPUT_PATH.relative_to(ROOT)),
        "theory": str(THEORY_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
