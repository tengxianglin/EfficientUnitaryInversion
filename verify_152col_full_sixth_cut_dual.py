"""128-bit Arb dual certificate for the 152-column / 2,113-row mixed-order LP.

The LP contains 1,461 complete second/fourth rows, 645 selected sixth rows,
and seven selected eighth rows. The rationalized HiGHS dual is independently
checked against all 152 physical generators using Arb. Since two active dual
coordinates are eighth-order rows, this is not a sixth-only certificate.
"""
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

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
SCAN_PATH = ROOT / "evidence/candidate_152col_complete_sixth_binary64_n21.json"
PARENT_CANDIDATE = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
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
    if len(sixth_rows) != len(sixth_targets) or len(sixth_rows) != 645:
        raise RuntimeError("unexpected complete-sixth cut inventory")
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
    blocks = {"low_complete": len(low_targets), "sixth_selected_plus_all_cuts": len(sixth_rows), "eighth_selected": len(eighth_rows)}
    if len(y) != 2113 or blocks != lp["row_blocks"] or lp["rows"] != len(y):
        raise RuntimeError("exact row order/dimensions disagree with LP transcript")
    return system, low_scales, sixth_rows, sixth_targets, eighth_rows, eighth_targets, y, blocks


def load_rational_dual(lp, y):
    discovery = lp.get("dual_discovery")
    if not discovery:
        raise RuntimeError("LP transcript lacks dual discovery data")
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
    paths = (LP_PATH, SCAN_PATH, PARENT_CANDIDATE, PARENT_LP, PARENT_DUAL, ESCAPE_CERT)
    raw = [path.read_bytes() for path in paths]
    lp, scan, candidate, parent_lp, parent_dual, escape = [json.loads(x) for x in raw]
    lp_sha, scan_sha, candidate_sha, parent_lp_sha, parent_dual_sha, escape_sha = map(sha, raw)

    if (lp.get("columns"), lp.get("rows")) != (152, 2113):
        raise RuntimeError("unexpected 152-column cut-LP dimensions")
    if lp.get("status") != "full_sixth_cut_lp_above_one_third":
        raise RuntimeError("cut LP is not the expected above-cap discovery")
    if lp.get("complete_sixth_binary64_scan_sha256") != scan_sha:
        raise RuntimeError("LP and complete sixth scan hashes disagree")
    if lp.get("parent_candidate_sha256") != candidate_sha:
        raise RuntimeError("LP does not pin its parent exact candidate")
    if lp.get("parent_lp_sha256") != sha(PARENT_LP.read_bytes()):
        raise RuntimeError("parent LP hash mismatch")
    if lp.get("parent_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("parent dual certificate hash mismatch")
    if lp.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("continuous escape certificate hash mismatch")
    if scan.get("candidate_input_sha256") != candidate_sha or scan.get("status") != "complete_sixth_binary64_violations_found":
        raise RuntimeError("full sixth scan does not pin the parent candidate")
    if len(scan.get("violating_orbits", [])) != 334:
        raise RuntimeError("full sixth scan must persist all 334 violations")
    if len(lp.get("new_sixth_cut_rows", [])) != 334:
        raise RuntimeError("LP does not contain every newly found sixth cut")
    if lp.get("complete_sixth_violations") != 334 or lp.get("new_unique_sixth_cuts") != 334:
        raise RuntimeError("unexpected cut count")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous path escape is not Arb-certified")
    if candidate.get("source_sha256") != parent_lp_sha:
        raise RuntimeError("parent exact candidate does not pin parent LP")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical physical pool hash/count mismatch")

    base_columns = [int(x) for x in lp["base_columns"]]
    if len(base_columns) != 151 or len(set(base_columns)) != 151:
        raise RuntimeError("unexpected base-column inventory")
    columns = base_columns + [1641]
    escape_couplings = [Fraction(x) for x in lp["escape_couplings_exact"]]
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("escape generator does not match strict Arb certificate")
    if len(escape_couplings) != 42 or escape_couplings[-1] != 0 or any(x <= 0 for x in escape_couplings[:-1]):
        raise RuntimeError("escape generator is not a legal positive open path")
    physical_columns = [all_columns[j] for j in base_columns] + [escape_couplings]

    system, low_scales, sixth_rows, sixth_targets, eighth_rows, eighth_targets, y, row_blocks = load_exact_design(lp)
    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    if len(z) != len(y):
        raise RuntimeError("dual vector dimension mismatch")

    z_arb = [ball(value) for value in z]
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 1461 + len(sixth_rows)]
    active_eighth = [i for i in active_rows if i >= 1461 + len(sixth_rows)]
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }
    base_lhs = []
    index_hash = hashlib.sha256()
    for column, couplings in zip(columns, physical_columns):
        index_hash.update(int(column).to_bytes(4, "little", signed=False))
        entries = rotation_entries_exact(couplings)
        lhs = arb(0)
        for row in active_low:
            feature = active_low_feature(system, entries, row, fourth_groups)
            lhs += z_arb[row] * feature / ball(low_scales[row])
        for row in active_sixth:
            lhs += z_arb[row] * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(SIXTH_SCALE)
        for row in active_eighth:
            offset = 1461 + len(sixth_rows)
            lhs += z_arb[row] * orbit_average_minor(entries, eighth_rows[row - offset]) / ball(EIGHTH_SCALE)
        base_lhs.append(lhs + ball(lam))
        print(f"Arb-evaluated dual column {len(base_lhs)}/{len(columns)} (column {column}); active rows {len(active_rows)}/{len(y)}", flush=True)

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
        shifted = [value - ball(delta) for value in base_lhs]
        if all(value.upper() <= 0 for value in shifted):
            selected_delta = delta
            selected_intervals = shifted
            break
    if selected_delta is None:
        maximum = max(float(value.upper()) for value in base_lhs)
        raise RuntimeError(f"could not certify all 152 dual inequalities; max unshifted upper={maximum}")

    lower = dual_objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_152col_2113row_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "complete_sixth_binary64_scan_sha256": scan_sha,
        "parent_candidate_sha256": candidate_sha,
        "parent_lp_sha256": parent_lp_sha,
        "parent_dual_certificate_sha256": parent_dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": columns,
        "column_count": len(columns),
        "row_count": len(y),
        "row_blocks": row_blocks,
        "original_sixth_rows": lp["original_sixth_rows"],
        "new_unique_sixth_cuts": lp["new_unique_sixth_cuts"],
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
            for column, value in zip(columns, selected_intervals)
        ],
        "dual_vector_rational": [str(value) for value in z],
        "scope": (
            "Rigorous finite-pool minimax lower bound for every convex mixture over the 152 pinned "
            "physical generators (151 frozen canonical paths plus one exact-rational continuous-path "
            "escape), on 2,113 exact normalized rows: all 1,461 second/fourth rows, 645 sixth rows "
            "(the original 311 plus all 334 rows that violated the previous candidate), and seven "
            "selected eighth rows. The dual has two nonzero eighth-order coordinates, so this is a "
            "mixed-order 2,113-row certificate and not a sixth-only lower-bound certificate. It applies "
            "to any objective whose row set contains all 2,113 pinned rows, but not to additional "
            "physical generators or the unrestricted continuous family."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "column_count": len(columns),
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
