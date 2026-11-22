"""128-bit Arb certificate for the 143-column / 55-separator finite-pool dual."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit, target
from joint_low_six_eighth_lp import EIGHTH_ROWS
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
from verify_full_low_moment_certificate import all_features

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_143col_55probe_n21.json"
SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_143col_dual_certificate_n21.json"
PRECISION_BITS = 128


def orbit_average_minor(entries, indices):
    group = orbit(indices)
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
    return total / len(group)


def exact_targets_and_scales(lp):
    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = ([Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys))
    low_y = [Fraction(value) / scale for value, scale in zip(system.rational_target, low_scales)]

    screen = json.loads(SCREEN_PATH.read_text())["records"]
    if len(screen) != 256:
        raise RuntimeError("the frozen sixth-order screening set must have 256 rows")
    screen_rows = [tuple(row["indices"]) for row in screen]
    screen_targets = [Fraction(row["target"]) for row in screen]
    probe_rows = [tuple(row) for row in lp["sixth_probe_rows"]]
    probe_targets = [Fraction(value) for value in lp["sixth_probe_targets"]]
    full_rows = [tuple(row) for row in lp["sixth_full_audit_separator_rows"]]
    full_targets = [Fraction(value) for value in lp["sixth_full_audit_separator_targets"]]
    prefix_rows = [tuple(row) for row in lp["sixth_prefix_separator_rows"]]
    prefix_targets = [Fraction(value) for value in lp["sixth_prefix_separator_targets"]]
    additional_rows = [tuple(row) for row in lp["sixth_additional_full_audit_separator_rows"]]
    additional_targets = [Fraction(value) for value in lp["sixth_additional_full_audit_separator_targets"]]
    if (len(probe_rows), len(full_rows), len(prefix_rows), len(additional_rows)) != (38, 8, 1, 8):
        raise RuntimeError("unexpected 55-separator row inventory")
    for rows, targets, label in (
        (probe_rows, probe_targets, "parent probes"),
        (full_rows, full_targets, "original full-audit separators"),
        (prefix_rows, prefix_targets, "prefix separator"),
        (additional_rows, additional_targets, "additional full-audit separators"),
    ):
        if len(rows) != len(targets) or any(target(row) != value for row, value in zip(rows, targets)):
            raise RuntimeError(f"sixth-order target mismatch in {label}")

    sixth_rows = screen_rows + probe_rows + full_rows + prefix_rows + additional_rows
    sixth_targets = screen_targets + probe_targets + full_targets + prefix_targets + additional_targets
    sixth_scale = Fraction(5, 19721)
    sixth_y = [value / sixth_scale for value in sixth_targets]

    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
    if [list(row) for row in eighth_rows] != EIGHTH_ROWS:
        raise RuntimeError("selected eighth-order rows differ from the pinned design")
    eighth_scale = Fraction(1, 19721)
    eighth_targets = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    eighth_y = [value / eighth_scale for value in eighth_targets]
    y = low_y + sixth_y + eighth_y
    row_blocks = {
        "low": len(low_y),
        "sixth_screen": len(screen_rows),
        "sixth_certified_probes": len(probe_rows),
        "sixth_full_audit_separators": len(full_rows),
        "sixth_prefix_separators": len(prefix_rows),
        "sixth_additional_full_audit_separators": len(additional_rows),
        "selected_eighth": len(eighth_rows),
    }
    if len(y) != 1779 or row_blocks != lp["row_blocks"]:
        raise RuntimeError("exact row ordering/dimensions disagree with the 143-column LP transcript")
    return system, low_scales, sixth_rows, sixth_scale, eighth_rows, eighth_scale, y, row_blocks


def load_dual(lp):
    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("LP transcript has no stored HiGHS dual multipliers")
    m = lp["rows"]
    marginals = discovery["inequality_marginals"]
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
        raise RuntimeError("exact rational dual l1 norm exceeds one")
    return z, lam, norm, scale


def build_column_dual_lhs(columns, all_columns, z, lam,
                          system, low_scales, sixth_rows, sixth_scale,
                          eighth_rows, eighth_scale):
    z_arb = [ball(value) for value in z]
    low_count = len(system.rational_target)
    sixth_count = len(sixth_rows)
    base_lhs = []
    column_hash = hashlib.sha256()
    for column in columns:
        couplings = all_columns[column]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"column {column} is not a legal 42-site path generator")
        column_hash.update(int(column).to_bytes(4, "little", signed=False))
        entries = rotation_entries_exact(couplings)
        low_values = all_features(system, entries)
        if len(low_values) != low_count:
            raise RuntimeError("low-order Arb feature count mismatch")
        lhs = arb(0)
        for i, (value, scale) in enumerate(zip(low_values, low_scales)):
            lhs += z_arb[i] * value / ball(scale)

        offset = low_count
        for j, indices in enumerate(sixth_rows):
            value = orbit_average_minor(entries, indices) / ball(sixth_scale)
            lhs += z_arb[offset + j] * value
        offset += sixth_count
        for j, indices in enumerate(eighth_rows):
            value = orbit_average_minor(entries, indices) / ball(eighth_scale)
            lhs += z_arb[offset + j] * value
        base_lhs.append(lhs + ball(lam))
    return base_lhs, column_hash.hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    lp_raw = LP_PATH.read_bytes()
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    lp = json.loads(lp_raw)
    if (lp.get("columns"), lp.get("rows")) != (143, 1779):
        raise RuntimeError("unexpected finite LP dimensions")
    expected_blocks = {
        "low": 1461, "sixth_screen": 256, "sixth_certified_probes": 38,
        "sixth_full_audit_separators": 8, "sixth_prefix_separators": 1,
        "sixth_additional_full_audit_separators": 8, "selected_eighth": 7,
    }
    if lp.get("row_blocks") != expected_blocks:
        raise RuntimeError("unexpected 55-separator LP row blocks")
    if not lp["lp_objective"] > 1 / 3:
        raise RuntimeError("the 143-column LP is not above the 1/3 cap")

    seed_array = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = hashlib.sha256(seed_array.tobytes()).hexdigest()
    if seed_array.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")

    system, low_scales, sixth_rows, sixth_scale, eighth_rows, eighth_scale, y, row_blocks = exact_targets_and_scales(lp)
    z, lam, norm, scale = load_dual(lp)
    if len(z) != len(y):
        raise RuntimeError("dual vector and exact target vector have different dimensions")
    dual_objective = lam + sum((a * b for a, b in zip(z, y)), Fraction(0))
    if not dual_objective > Fraction(1, 3):
        raise RuntimeError("rationalized dual objective no longer exceeds 1/3")

    all_columns, _, _ = canonical_ensemble()
    all_column_array = np.asarray(all_columns, dtype="<f8")
    all_columns_sha = hashlib.sha256(all_column_array.tobytes()).hexdigest()
    if all_columns_sha != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("expanded LP does not pin the canonical physical column pool")
    columns = sorted(set(int(x) for x in lp["base_columns"]) | set(int(x) for x in lp["added_arb_positive_columns"]))
    if len(columns) != 143 or len(set(columns)) != 143:
        raise RuntimeError("expanded physical pool does not contain 143 distinct columns")

    base_lhs, column_hash = build_column_dual_lhs(
        columns, all_columns, z, lam,
        system, low_scales, sixth_rows, sixth_scale, eighth_rows, eighth_scale,
    )

    deltas = [
        Fraction(0), Fraction(1, 10**12), Fraction(1, 10**10),
        Fraction(1, 10**9), Fraction(1, 10**8), Fraction(1, 10**7),
        Fraction(1, 10**6), Fraction(1, 10**5), Fraction(1, 10**4),
    ]
    selected_delta = None
    selected_upper = None
    for delta in deltas:
        if dual_objective - delta <= Fraction(1, 3):
            continue
        shifted = [value - ball(delta) for value in base_lhs]
        if all(value.upper() <= 0 for value in shifted):
            selected_delta = delta
            selected_upper = shifted
            break
    if selected_delta is None:
        max_upper = max(float(value.upper()) for value in base_lhs)
        raise RuntimeError(f"could not certify all 143 dual inequalities; max unshifted upper={max_upper}")

    certified_objective = dual_objective - selected_delta
    max_upper = max(value.upper() for value in selected_upper)
    result = {
        "status": "strict_pool_separation",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_columns_sha,
        "canonical_143_column_index_sha256": column_hash,
        "columns": columns,
        "column_count": len(columns),
        "row_count": len(y),
        "row_blocks": row_blocks,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_convention": "z = first m HiGHS inequality marginals minus second m; lambda is the sum-to-one equality marginal",
        "dual_l1_norm_exact": str(norm),
        "dual_scale_applied": str(scale),
        "dual_lambda_before_slack": str(lam),
        "dual_slack_delta": str(selected_delta),
        "dual_objective_before_slack": str(dual_objective),
        "certified_minimax_lower_bound": str(certified_objective),
        "strict_lower_bound_above_one_third": str(certified_objective - Fraction(1, 3)),
        "max_arb_upper_of_A_transpose_z_plus_lambda_minus_delta": str(max_upper),
        "column_dual_lhs_intervals": [
            {"column": column, "interval": str(value - ball(selected_delta))}
            for column, value in zip(columns, base_lhs)
        ],
        "dual_vector_rational": [str(value) for value in z],
        "scope": (
            "Rigorous lower bound for the minimum worst normalized residual over convex mixtures "
            "of these exact 143 legal physical path columns, restricted to the 1,779 pinned "
            "low/sixth/selected-eighth rows. This is not a no-go theorem for new physical columns, "
            "the remaining canonical pool, other Hamiltonian families, or the full program moment."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "lp_transcript_sha256": lp_sha,
        "column_count": len(columns),
        "row_count": len(y),
        "dual_l1_norm_exact": str(norm),
        "certified_minimax_lower_bound": str(certified_objective),
        "strict_gap_above_one_third": str(certified_objective - Fraction(1, 3)),
        "selected_slack": str(selected_delta),
        "max_arb_upper": str(max_upper),
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
