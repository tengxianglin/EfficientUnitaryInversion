"""128-bit Arb certificate for the 162-column sixth-only 2,106-row minimax LP."""
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

LP_PATH = ROOT / "evidence/joint_low_six_lp_162col_sixth_only_n21.json"
LP162_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CERT162_PATH = ROOT / "evidence/55probe_162col_full_sixth_cut_dual_certificate_n21.json"
CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
PRICING_ARB_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_pricing_arb_n21.json"
ESCAPE_CERT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_162col_sixth_only_dual_certificate_n21.json"
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
        LP_PATH, LP162_PATH, CERT162_PATH, CANDIDATE_PATH, CUT_LP_PATH,
        PRICING_ARB_PATH, ESCAPE_CERT_PATH, SEED_POOL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    (
        lp, lp162, cert162, candidate, cut_lp, pricing_arb, escape, seed_raw
    ) = [
        json.loads(value) if path.suffix != ".npy" else value
        for path, value in zip(paths, raw)
    ]
    (
        lp_sha, lp162_sha, cert162_sha, candidate_sha, cut_lp_sha,
        pricing_arb_sha, escape_sha, seed_file_sha,
    ) = map(sha, raw)

    if (lp.get("columns"), lp.get("rows")) != (162, 2106):
        raise RuntimeError("unexpected sixth-only LP dimensions")
    if lp.get("status") != "162col_sixth_only_lp_above_one_third":
        raise RuntimeError("sixth-only LP is not the expected above-cap discovery")
    if lp.get("parent_162col_lp_sha256") != lp162_sha:
        raise RuntimeError("sixth-only LP does not pin the 162-column parent LP")
    if lp.get("parent_162col_dual_certificate_sha256") != cert162_sha:
        raise RuntimeError("sixth-only LP does not pin the 162-column parent certificate")
    if lp.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("sixth-only LP does not pin the exact continuous-path candidate")
    if lp.get("parent_152col_cut_lp_sha256") != cut_lp_sha:
        raise RuntimeError("sixth-only LP does not pin the current sixth-row inventory")
    if lp.get("pricing_arb_sha256") != pricing_arb_sha:
        raise RuntimeError("sixth-only LP does not pin its Arb-priced column inventory")
    if cert162.get("status") != "strict_162col_2113row_minimax_obstruction" or not cert162.get("complete"):
        raise RuntimeError("parent 162-column mixed-order certificate is incomplete")
    if cert162.get("lp_transcript_sha256") != lp162_sha:
        raise RuntimeError("parent 162-column certificate does not pin its LP")
    if (lp162.get("columns"), lp162.get("rows")) != (162, 2113):
        raise RuntimeError("unexpected parent 162-column mixed-order LP")
    if pricing_arb.get("status") != "arb_positive_columns_found":
        raise RuntimeError("parent ten-column Arb pricing evidence is incomplete")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous escape generator lacks its strict Arb certificate")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("frozen canonical pool hash/count mismatch")

    base_columns = [int(x) for x in lp["base_columns"]]
    added_columns = [int(x) for x in lp["added_canonical_columns"]]
    column_order = [int(x) for x in lp["column_order"]]
    if column_order != base_columns + [1641] + added_columns or len(column_order) != 162:
        raise RuntimeError("sixth-only physical column ordering mismatch")
    if base_columns != [int(x) for x in lp162["base_columns"]]:
        raise RuntimeError("base canonical columns differ from the 162-column parent pool")
    if added_columns != [int(x) for x in lp162["added_canonical_columns"]]:
        raise RuntimeError("added canonical columns differ from the 162-column parent pool")
    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("continuous escape input differs from its strict Arb certificate")
    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in added_columns]
    )

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
    if sixth_hash != lp.get("sixth_rows_sha256"):
        raise RuntimeError("sixth-order row inventory hash mismatch")

    y = (
        [value / scale for value, scale in zip(low_targets, low_scales)]
        + [value / SIXTH_SCALE for value in sixth_targets]
    )
    if len(y) != 2106 or lp.get("row_blocks") != {"low_complete": 1461, "sixth_selected_plus_all_cuts": 645}:
        raise RuntimeError("sixth-only exact target vector dimensions mismatch")

    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("sixth-only LP transcript lacks dual multipliers")
    m = len(y)
    marginals = discovery.get("inequality_marginals", [])
    if len(marginals) != 2 * m:
        raise RuntimeError("wrong sixth-only dual marginal count")
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
        raise RuntimeError("exact rational sixth-only dual L1 norm exceeds one")
    objective = lam + sum((a * b for a, b in zip(z, y)), Fraction(0))
    if objective <= Fraction(1, 3):
        raise RuntimeError("rationalized sixth-only dual objective no longer exceeds 1/3")

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
            f"Arb-evaluated sixth-only dual column {len(column_lhs)}/162 "
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
        raise RuntimeError(f"could not certify all sixth-only column inequalities; max upper={maximum}")

    lower = objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_162col_2106row_sixth_only_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_162col_lp_sha256": lp162_sha,
        "parent_162col_dual_certificate_sha256": cert162_sha,
        "parent_152col_cut_lp_sha256": cut_lp_sha,
        "parent_candidate_sha256": candidate_sha,
        "pricing_arb_sha256": pricing_arb_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": len(column_order),
        "added_canonical_columns": added_columns,
        "row_count": len(y),
        "row_blocks": {"low_complete": 1461, "sixth_selected_plus_all_cuts": 645},
        "total_sixth_rows": len(sixth_rows),
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
        "scope": (
            "Rigorous sixth-only finite-pool minimax lower bound for every convex mixture over the "
            "162 pinned physical generators. The certified row set contains all 1,461 second/fourth "
            "rows and 645 distinct sixth-order D42 orbits, and contains no eighth-order rows. Since "
            "these 645 sixth-order orbits are a subset of the complete 63,133-orbit sixth-order domain, "
            "the complete sixth-order objective for this fixed 162-column pool is at least this lower "
            "bound. This does not rule out additional physical generators or the unrestricted continuous family."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
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
