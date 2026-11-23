"""128-bit Arb dual certificate for the 188-column fifth-continuous-escape LP."""
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

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_188col_fifth_continuous_escape_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_187col_fourth_continuous_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_187col_fourth_continuous_escape_dual_certificate_n21.json"
PARENT_186_LP = ROOT / "evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json"
PARENT_186_DUAL = ROOT / "evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
ESCAPE_1 = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
ESCAPE_2 = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
ESCAPE_3 = ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json"
ESCAPE_4 = ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json"
ESCAPE_5 = ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT_PATH = ROOT / "evidence/55probe_188col_fifth_continuous_escape_dual_certificate_n21.json"

PRECISION_BITS = 128
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
ESCAPE_1_COLUMN = 1641
ESCAPE_2_COLUMN = 1642
ESCAPE_3_COLUMN = 1643
ESCAPE_4_COLUMN = 1644
ESCAPE_5_COLUMN = 1645


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        LP_PATH, PARENT_LP, PARENT_DUAL, PARENT_186_LP, PARENT_186_DUAL,
        CANDIDATE_152, CUT_LP, CUT_DUAL, ESCAPE_1, ESCAPE_2, ESCAPE_3,
        ESCAPE_4, ESCAPE_5, SEED_POOL,
    )
    raw = [path.read_bytes() for path in paths]
    values = [value if path.suffix == ".npy" else json.loads(value)
              for path, value in zip(paths, raw)]
    (lp, parent_lp, parent_dual, parent_186_lp, parent_186_dual,
     candidate152, cut_lp, cut_dual, escape1, escape2, escape3,
     escape4, escape5, seed_raw) = values
    (lp_sha, parent_lp_sha, parent_dual_sha, parent_186_lp_sha,
     parent_186_dual_sha, candidate_sha, cut_lp_sha, cut_dual_sha,
     escape1_sha, escape2_sha, escape3_sha, escape4_sha, escape5_sha,
     seed_file_sha) = map(sha, raw)

    if lp.get("status") != "188col_fifth_continuous_escape_lp_above_one_third":
        raise RuntimeError("188-column LP is not an above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (188, 2113):
        raise RuntimeError("unexpected 188-column / 2,113-row dimensions")
    if lp.get("parent_187col_lp_sha256") != parent_lp_sha or lp.get("parent_187col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("188-column LP does not pin its exact 187-column parent")
    if lp.get("parent_152col_candidate_sha256") != candidate_sha:
        raise RuntimeError("188-column LP does not pin its 152-column ancestor candidate")
    if lp.get("cut_lp_transcript_sha256") != cut_lp_sha or lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("188-column LP does not pin the 2,113-row cut design")
    for key, digest in (
        ("first_continuous_escape_arb_certificate_sha256", escape1_sha),
        ("second_continuous_escape_arb_certificate_sha256", escape2_sha),
        ("third_continuous_escape_arb_certificate_sha256", escape3_sha),
        ("fourth_continuous_escape_arb_certificate_sha256", escape4_sha),
        ("fifth_continuous_escape_arb_certificate_sha256", escape5_sha),
    ):
        if lp.get(key) != digest:
            raise RuntimeError(f"188-column LP provenance mismatch for {key}")

    if parent_lp.get("status") != "187col_fourth_continuous_escape_lp_above_one_third" or parent_lp.get("columns") != 187:
        raise RuntimeError("187-column parent LP is not the expected above-cap result")
    if parent_dual.get("status") != "strict_187col_2113row_fourth_continuous_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("187-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("187-column parent dual/LP hash mismatch")
    if lp.get("parent_187col_lp_sha256") != parent_lp_sha or lp.get("parent_187col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("188-column LP parent hashes disagree")
    if parent_186_dual.get("status") != "strict_186col_2113row_third_continuous_escape_minimax_obstruction" or not parent_186_dual.get("complete"):
        raise RuntimeError("186-column ancestor dual is not strictly Arb-certified")
    if parent_186_dual.get("lp_transcript_sha256") != parent_186_lp_sha:
        raise RuntimeError("186-column ancestor dual/LP hash mismatch")
    if parent_dual.get("parent_186col_lp_sha256") != parent_186_lp_sha or parent_dual.get("parent_186col_dual_certificate_sha256") != parent_186_dual_sha:
        raise RuntimeError("187-column parent does not pin its 186-column ancestor")
    if escape3.get("dual_certificate_sha256") != parent_186_dual.get("parent_185col_dual_certificate_sha256") or escape3.get("lp_transcript_sha256") != parent_186_dual.get("parent_185col_lp_sha256"):
        raise RuntimeError("third escape does not pin the 185-column parent dual/LP")
    if escape4.get("dual_certificate_sha256") != parent_186_dual_sha or escape4.get("lp_transcript_sha256") != parent_186_lp_sha:
        raise RuntimeError("fourth escape does not pin the 186-column parent dual/LP")
    if escape5.get("dual_certificate_sha256") != parent_dual_sha or escape5.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("fifth escape does not pin the 187-column parent dual/LP")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != escape1_sha:
        raise RuntimeError("152-column ancestor candidate does not pin the first escape")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut dual is not strictly Arb-certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("152-column cut dual does not pin its cut LP")

    escapes = (escape1, escape2, escape3, escape4, escape5)
    escape_hashes = (escape1_sha, escape2_sha, escape3_sha, escape4_sha, escape5_sha)
    for index, cert in enumerate(escapes, 1):
        if cert.get("status") != "certified_continuous_path_dual_escape" or not cert.get("complete") or not cert.get("strictly_positive"):
            raise RuntimeError(f"continuous escape {index} is not strictly Arb-certified")
    for key, digest in zip((
        "first_continuous_escape_arb_certificate_sha256",
        "second_continuous_escape_arb_certificate_sha256",
        "third_continuous_escape_arb_certificate_sha256",
        "fourth_continuous_escape_arb_certificate_sha256",
    ), escape_hashes[:4]):
        if parent_lp.get(key) != digest or parent_dual.get(key) != digest:
            raise RuntimeError(f"187-column parent does not pin {key}")
    if parent_lp.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("187-column parent does not pin the cut-row inventory")

    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("188-column LP does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")

    base_columns = [int(x) for x in parent_lp["base_columns"]]
    added_columns = [int(x) for x in parent_lp["added_canonical_columns"]]
    parent_order = [int(x) for x in parent_lp["column_order"]]
    expected_parent_order = base_columns + [ESCAPE_1_COLUMN] + added_columns + [
        ESCAPE_2_COLUMN, ESCAPE_3_COLUMN, ESCAPE_4_COLUMN
    ]
    column_order = [int(x) for x in lp["column_order"]]
    if len(base_columns) != 151 or len(added_columns) != 32 or parent_order != expected_parent_order:
        raise RuntimeError("187-column parent inventory/order mismatch")
    if column_order != parent_order + [ESCAPE_5_COLUMN] or len(set(column_order)) != 188:
        raise RuntimeError("188-column expanded ordering mismatch")

    couplings1 = [Fraction(x) for x in escape1["candidate_couplings_exact"]]
    couplings2 = [Fraction(x) for x in escape2["candidate_couplings_exact"]]
    couplings3 = [Fraction(x) for x in escape3["candidate_couplings_exact"]]
    couplings4 = [Fraction(x) for x in escape4["candidate_couplings_exact"]]
    couplings5 = [Fraction(x) for x in escape5["candidate_couplings_exact"]]
    all_couplings = (couplings1, couplings2, couplings3, couplings4, couplings5)
    for index, couplings in enumerate(all_couplings, 1):
        if len(couplings) != 42 or couplings[-1] != 0 or any(x <= 0 for x in couplings[:-1]):
            raise RuntimeError(f"continuous escape {index} is not a legal positive open path")
    if len({tuple(x) for x in all_couplings}) != 5:
        raise RuntimeError("the five continuous paths are not pairwise distinct")

    physical_columns = (
        [all_columns[column] for column in base_columns]
        + [couplings1]
        + [all_columns[column] for column in added_columns]
        + [couplings2, couplings3, couplings4, couplings5]
    )
    if len(physical_columns) != 188:
        raise RuntimeError("wrong physical column count")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut_lp)
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("188-column row inventory hash mismatch")
    if row_blocks != lp.get("row_blocks"):
        raise RuntimeError("188-column row-block inventory mismatch")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    if norm > 1 or dual_objective <= Fraction(1, 3):
        raise RuntimeError("rationalized 188-column dual does not meet minimax dual conditions")
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
        print(f"Arb-evaluated dual column {index}/188 (label {column})", flush=True)

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
        raise RuntimeError(f"could not certify all 188 dual inequalities; max unshifted upper={maximum}")

    lower = dual_objective - selected_delta
    maximum_upper = max(value.upper() for value in selected_intervals)
    result = {
        "status": "strict_188col_2113row_fifth_continuous_escape_minimax_obstruction",
        "complete": True,
        "lp_transcript_sha256": lp_sha,
        "parent_187col_lp_sha256": parent_lp_sha,
        "parent_187col_dual_certificate_sha256": parent_dual_sha,
        "parent_186col_lp_sha256": parent_186_lp_sha,
        "parent_186col_dual_certificate_sha256": parent_186_dual_sha,
        "parent_152col_candidate_sha256": candidate_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "cut_dual_certificate_sha256": cut_dual_sha,
        "first_continuous_escape_arb_certificate_sha256": escape1_sha,
        "second_continuous_escape_arb_certificate_sha256": escape2_sha,
        "third_continuous_escape_arb_certificate_sha256": escape3_sha,
        "fourth_continuous_escape_arb_certificate_sha256": escape4_sha,
        "fifth_continuous_escape_arb_certificate_sha256": escape5_sha,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_index_sha256": index_hash.hexdigest(),
        "columns": column_order,
        "column_count": 188,
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
            "Rigorous mixed-order minimax lower bound for every convex mixture over the 188 pinned "
            "physical generators on the exact 2,113-row design. This is not a complete sixth/eighth "
            "orbit certificate, a continuous-family no-go, or an operational Choi/diamond theorem."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "column_count": 188,
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
