"""128-bit Arb certificate for the 162-column / 2,113-row full-sixth cut LP."""
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

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
PARENT_DUAL_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
PRICING_SCREEN_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_pricing_screen_n21.json"
PRICING_ARB_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_pricing_arb_n21.json"
ORIGINAL_DUAL_PATH = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_CERT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_162col_full_sixth_cut_dual_certificate_n21.json"
PRECISION_BITS = 128
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


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


def load_exact_design(lp):
    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    low_targets = list(system.rational_target)
    if len(low_targets) != 1461:
        raise RuntimeError("unexpected complete low-order row count")

    sixth_rows = [tuple(int(x) for x in row) for row in lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(x) for x in lp["sixth_cut_targets"]]
    if len(sixth_rows) != 645 or len(sixth_rows) != len(sixth_targets):
        raise RuntimeError("unexpected sixth cut inventory")
    if len(set(sixth_rows)) != len(sixth_rows):
        raise RuntimeError("sixth cut rows are not unique")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth cut target mismatch")

    eighth_rows = [tuple(int(x) for x in row) for row in lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(x) for x in lp["selected_eighth_targets"]]
    if len(eighth_rows) != 7 or len(eighth_rows) != len(eighth_targets):
        raise RuntimeError("unexpected selected eighth-order row inventory")
    expected_eighth = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    if expected_eighth != eighth_targets:
        raise RuntimeError("selected eighth-order target mismatch")

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
    if len(y) != 2113 or blocks != lp["row_blocks"] or lp["rows"] != len(y):
        raise RuntimeError("exact row order/dimensions disagree with 162-column LP transcript")
    return system, low_scales, sixth_rows, eighth_rows, y, blocks


def load_rational_dual(lp, y):
    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("162-column LP transcript lacks dual discovery data")
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
    objective = lam + sum((a * b for a, b in zip(z, y)), Fraction(0))
    if objective <= Fraction(1, 3):
        raise RuntimeError("rationalized dual objective no longer exceeds 1/3")
    return z, lam, norm, scale, objective


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        LP_PATH, CANDIDATE_PATH, PARENT_LP_PATH, PARENT_DUAL_PATH,
        PRICING_SCREEN_PATH, PRICING_ARB_PATH, ORIGINAL_DUAL_PATH,
        ESCAPE_CERT_PATH, SEED_POOL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    (
        lp, candidate, parent_lp, parent_dual, pricing_screen, pricing_arb,
        original_dual, escape, seed_raw,
    ) = [
        json.loads(value) if path.suffix != ".npy" else value
        for path, value in zip(paths, raw)
    ]
    (
        lp_sha, candidate_sha, parent_lp_sha, parent_dual_sha,
        pricing_screen_sha, pricing_arb_sha, original_dual_sha,
        escape_sha, seed_file_sha,
    ) = map(sha, raw)

    if (lp.get("columns"), lp.get("rows")) != (162, 2113):
        raise RuntimeError("unexpected 162-column / 2,113-row LP dimensions")
    if lp.get("status") != "162col_full_sixth_cut_lp_above_one_third":
        raise RuntimeError("162-column LP is not the expected above-cap discovery")
    if lp.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("162-column LP does not pin its parent candidate")
    if lp.get("parent_lp_sha256") != parent_lp_sha:
        raise RuntimeError("162-column LP does not pin the 152-column cut LP")
    if lp.get("parent_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("162-column LP does not pin the 152-column Arb dual")
    if lp.get("pricing_screen_sha256") != pricing_screen_sha:
        raise RuntimeError("162-column LP does not pin the pricing screen")
    if lp.get("pricing_arb_sha256") != pricing_arb_sha:
        raise RuntimeError("162-column LP does not pin the Arb pricing transcript")
    if parent_lp.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("152-column cut LP does not pin the original exact candidate")
    if parent_lp.get("parent_lp_sha256") != candidate.get("source_sha256"):
        raise RuntimeError("152-column cut LP and candidate parent LP hash disagree")
    if parent_lp.get("parent_dual_certificate_sha256") != candidate.get("parent_dual_certificate_sha256"):
        raise RuntimeError("152-column cut LP and candidate parent dual hash disagree")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (152, 2113):
        raise RuntimeError("unexpected 152-column parent cut LP dimensions")
    if parent_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("parent 152-column dual is not strictly certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("parent dual does not pin its cut LP")
    if pricing_arb.get("status") != "arb_positive_columns_found":
        raise RuntimeError("pricing Arb transcript is not successful")
    if pricing_arb.get("dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("pricing Arb transcript does not pin the parent dual")
    if pricing_arb.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("pricing Arb transcript does not pin the parent LP")
    if pricing_arb.get("pricing_screen_sha256") != pricing_screen_sha:
        raise RuntimeError("pricing Arb transcript does not pin the binary64 screen")
    if pricing_screen.get("dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("binary64 pricing screen does not pin the parent dual")
    if pricing_screen.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("binary64 pricing screen does not pin the parent LP")
    if candidate.get("parent_dual_certificate_sha256") != original_dual_sha:
        raise RuntimeError("original 151-column dual hash mismatch")
    if candidate.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("continuous escape certificate hash mismatch")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous path escape is not Arb-certified")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical physical pool hash/count mismatch")

    base_columns = [int(x) for x in lp["base_columns"]]
    added_columns = [int(x) for x in lp["added_canonical_columns"]]
    column_order = [int(x) for x in lp["column_order"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("unexpected 151-column base inventory")
    if len(added_columns) != 10 or len(set(added_columns)) != 10:
        raise RuntimeError("unexpected ten-column pricing escape inventory")
    if set(base_columns) & set(added_columns):
        raise RuntimeError("new canonical columns overlap the base pool")
    expected_order = base_columns + [1641] + added_columns
    if column_order != expected_order or len(set(column_order)) != 162:
        raise RuntimeError("162-column ordering mismatch")

    priced_results = [x for x in pricing_arb.get("results", []) if x.get("strictly_positive")]
    if [int(x["column"]) for x in priced_results] != added_columns:
        raise RuntimeError("162-column LP does not use exactly the Arb-positive pricing columns")
    for item in priced_results:
        j = int(item["column"])
        if not np.array_equal(np.asarray(item["couplings"], dtype=np.float64), np.asarray(all_columns[j], dtype=np.float64)):
            raise RuntimeError(f"priced coupling payload differs from frozen canonical column {j}")

    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    if len(escape_couplings) != 42 or escape_couplings[-1] != 0 or any(x <= 0 for x in escape_couplings[:-1]):
        raise RuntimeError("continuous escape is not a legal positive open path")
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("continuous escape couplings differ from Arb-certified input")
    physical_columns = (
        [all_columns[j] for j in base_columns]
        + [escape_couplings]
        + [all_columns[j] for j in added_columns]
    )
    if len(physical_columns) != 162:
        raise RuntimeError("wrong physical column count")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(parent_lp)
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(x) for x in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("row inventory hash mismatch")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    if len(z) != len(y):
        raise RuntimeError("dual vector dimension mismatch")
    z_arb = [ball(value) for value in z]
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 2106]
    active_eighth = [i for i in active_rows if i >= 2106]
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
            feature = active_low_feature(system, entries, row, fourth_groups)
            lhs += z_arb[row] * feature / ball(low_scales[row])
        for row in active_sixth:
            lhs += z_arb[row] * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(SIXTH_SCALE)
        for row in active_eighth:
            lhs += z_arb[row] * orbit_average_minor(entries, eighth_rows[row - 2106]) / ball(EIGHTH_SCALE)
        column_lhs.append(lhs + ball(lam))
        print(
            f"Arb-evaluated dual column {len(column_lhs)}/162 (column {column}); "
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
        raise RuntimeError(f"could not certify all 162 dual inequalities; max unshifted upper={maximum}")

    lower = dual_objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_162col_2113row_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_candidate_sha256": candidate_sha,
        "parent_152col_lp_sha256": parent_lp_sha,
        "parent_152col_dual_certificate_sha256": parent_dual_sha,
        "pricing_screen_sha256": pricing_screen_sha,
        "pricing_arb_sha256": pricing_arb_sha,
        "original_151col_dual_sha256": original_dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": len(column_order),
        "added_canonical_columns": added_columns,
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
            "Rigorous finite-pool minimax lower bound for every convex mixture over the 162 pinned "
            "physical generators (151 frozen canonical paths, one exact-rational continuous-path "
            "escape, and ten additional frozen canonical paths), on the 2,113 exact normalized rows: "
            "all 1,461 second/fourth rows, 645 sixth rows, and seven selected eighth rows. Since the "
            "complete sixth-order maximum contains these rows, the same lower bound applies to the "
            "complete-sixth objective restricted to this fixed 162-column pool. It does not rule out "
            "additional physical generators or the unrestricted continuous family."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "column_count": len(column_order),
        "row_count": len(y),
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
