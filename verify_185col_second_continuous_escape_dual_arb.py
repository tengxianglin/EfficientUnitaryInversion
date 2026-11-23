"""128-bit Arb dual certificate for the 185-column second-continuous-escape LP."""
import hashlib
import json
from fractions import Fraction

import numpy as np
from flint import arb, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    load_rational_dual,
    orbit_average_minor,
)
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_185col_second_continuous_escape_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
OLD_ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
NEW_ESCAPE_CERT = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT_PATH = ROOT / "evidence/55probe_185col_second_continuous_escape_dual_certificate_n21.json"

PRECISION_BITS = 128
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OLD_ESCAPE_COLUMN = 1641
NEW_ESCAPE_COLUMN = 1642


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    paths = (LP_PATH, PARENT_LP, PARENT_DUAL, CANDIDATE_152, CUT_LP, CUT_DUAL,
             OLD_ESCAPE_CERT, NEW_ESCAPE_CERT, SEED_POOL)
    raw = [path.read_bytes() for path in paths]
    values = [value if path.suffix == ".npy" else json.loads(value)
              for path, value in zip(paths, raw)]
    (lp, parent_lp, parent_dual, candidate152, cut_lp, cut_dual,
     old_escape, new_escape, seed_raw) = values
    (lp_sha, parent_lp_sha, parent_dual_sha, candidate_sha, cut_lp_sha,
     cut_dual_sha, old_escape_sha, new_escape_sha, seed_file_sha) = map(sha, raw)

    if lp.get("status") != "185col_second_continuous_escape_lp_above_one_third":
        raise RuntimeError("185-column LP is not an above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (185, 2113):
        raise RuntimeError("unexpected 185-column / 2,113-row dimensions")
    if lp.get("parent_184col_lp_sha256") != parent_lp_sha or lp.get("parent_184col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("185-column LP does not pin its exact 184-column parent")
    if lp.get("parent_152col_candidate_sha256") != candidate_sha:
        raise RuntimeError("185-column LP does not pin its 152-column ancestor candidate")
    if lp.get("cut_lp_transcript_sha256") != cut_lp_sha or lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("185-column LP does not pin the 2,113-row cut design")
    if lp.get("first_continuous_escape_arb_certificate_sha256") != old_escape_sha:
        raise RuntimeError("185-column LP does not pin the first continuous escape")
    if lp.get("second_continuous_escape_arb_certificate_sha256") != new_escape_sha:
        raise RuntimeError("185-column LP does not pin the second continuous escape")
    if parent_lp.get("status") != "184col_full_sixth_cut_lp_above_one_third" or parent_lp.get("columns") != 184:
        raise RuntimeError("184-column parent LP is not the expected above-cap result")
    if parent_dual.get("status") != "strict_184col_2113row_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("184-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("184-column parent dual/LP hash mismatch")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != old_escape_sha:
        raise RuntimeError("152-column candidate does not pin the first escape")
    if old_escape.get("status") != "certified_continuous_path_dual_escape" or not old_escape.get("strictly_positive"):
        raise RuntimeError("first continuous escape is not Arb-certified")
    if new_escape.get("status") != "certified_continuous_path_dual_escape" or not new_escape.get("complete") or not new_escape.get("strictly_positive"):
        raise RuntimeError("second continuous escape is not Arb-certified")
    if new_escape.get("dual_certificate_sha256") != parent_dual_sha or new_escape.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("second escape does not pin the 184-column parent dual/LP")
    if new_escape.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("second escape does not pin the cut-row inventory")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut dual is not strictly certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("152-column cut dual does not pin the cut LP")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("185-column LP does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    added_columns = [int(x) for x in parent_lp["added_canonical_columns"]]
    parent_order = [int(x) for x in parent_lp["column_order"]]
    expected_order = base_columns + [OLD_ESCAPE_COLUMN] + added_columns
    column_order = [int(x) for x in lp["column_order"]]
    if len(base_columns) != 151 or len(added_columns) != 32 or parent_order != expected_order:
        raise RuntimeError("184-column parent inventory/order mismatch")
    if column_order != parent_order + [NEW_ESCAPE_COLUMN] or len(set(column_order)) != 185:
        raise RuntimeError("185-column expanded ordering mismatch")

    old_couplings = [Fraction(x) for x in candidate152["escape_couplings_exact"]]
    new_couplings = [Fraction(x) for x in new_escape["candidate_couplings_exact"]]
    if [str(x) for x in old_couplings] != old_escape["candidate_couplings_exact"]:
        raise RuntimeError("first path differs from its Arb-certified input")
    if len(new_couplings) != 42 or new_couplings[-1] != 0 or any(x <= 0 for x in new_couplings[:-1]):
        raise RuntimeError("second path is not a legal strictly-positive open path")
    if old_couplings == new_couplings:
        raise RuntimeError("the two continuous paths are duplicates")
    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [old_couplings]
        + [all_columns[column] for column in added_columns]
        + [new_couplings]
    )
    if len(physical_columns) != 185:
        raise RuntimeError("wrong physical column count")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut_lp)
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("185-column row inventory hash mismatch")
    if row_blocks != lp.get("row_blocks"):
        raise RuntimeError("185-column row-block inventory mismatch")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    if norm > 1 or dual_objective <= Fraction(1, 3):
        raise RuntimeError("rationalized 185-column dual does not meet the minimax dual conditions")
    z_arb = [ball(value) for value in z]
    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 2106]
    active_eighth = [i for i in active_rows if i >= 2106]
    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }

    column_lhs = []
    index_hash = hashlib.sha256()
    for index, (column, couplings) in enumerate(zip(column_order, physical_columns), 1):
        index_hash.update(int(column).to_bytes(4, "little", signed=False))
        entries = rotation_entries_exact(couplings)
        lhs = arb(0)
        for row in active_low:
            lhs += z_arb[row] * active_low_feature(system, entries, row, fourth_groups) / ball(low_scales[row])
        for row in active_sixth:
            lhs += z_arb[row] * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(Fraction(5, 19721))
        for row in active_eighth:
            lhs += z_arb[row] * orbit_average_minor(entries, eighth_rows[row - 2106]) / ball(Fraction(1, 19721))
        column_lhs.append(lhs + ball(lam))
        print(f"Arb-evaluated dual column {index}/185 (label {column})", flush=True)

    deltas = [Fraction(0), Fraction(1, 10**12), Fraction(1, 10**10),
              Fraction(1, 10**9), Fraction(1, 10**8), Fraction(1, 10**7),
              Fraction(1, 10**6), Fraction(1, 10**5), Fraction(1, 10**4)]
    selected_delta = None
    selected_intervals = None
    for delta in deltas:
        if dual_objective - delta <= Fraction(1, 3):
            continue
        shifted = [value - ball(delta) for value in column_lhs]
        if all(value.upper() <= 0 for value in shifted):
            selected_delta, selected_intervals = delta, shifted
            break
    if selected_delta is None:
        maximum = max(float(value.upper()) for value in column_lhs)
        raise RuntimeError(f"could not certify all 185 dual inequalities; max unshifted upper={maximum}")

    lower = dual_objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_185col_2113row_second_continuous_escape_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_184col_lp_sha256": parent_lp_sha,
        "parent_184col_dual_certificate_sha256": parent_dual_sha,
        "parent_152col_candidate_sha256": candidate_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "cut_dual_certificate_sha256": cut_dual_sha,
        "first_continuous_escape_arb_certificate_sha256": old_escape_sha,
        "second_continuous_escape_arb_certificate_sha256": new_escape_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": 185,
        "row_count": len(y),
        "row_blocks": row_blocks,
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
            "Rigorous mixed-order minimax lower bound for every convex mixture over the 185 pinned "
            "physical generators on the exact 2,113-row design. This is not a complete sixth/eighth "
            "orbit certificate, a continuous-family no-go, or an operational Choi/diamond theorem."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "column_count": 185,
        "row_count": len(y),
        "active_dual_rows": len(active_rows),
        "dual_l1_norm_exact": str(norm),
        "dual_objective_exact": str(dual_objective),
        "certified_minimax_lower_bound": str(lower),
        "selected_slack": str(selected_delta),
        "maximum_arb_upper": str(maximum_upper),
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
