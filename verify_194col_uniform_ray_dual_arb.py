"""128-bit Arb certification of the 194-column LP dual, including both explicit uniform-ray paths."""
import hashlib
import json
from fractions import Fraction

import numpy as np
from flint import ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from screen_ising_sixth_moments import orbit
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    load_rational_dual,
    orbit_average_minor,
)
from verify_192col_uniform_ray_time_arb import exact_uniform_ray_rotation
from verify_ising_moment_pricing import ball
from verify_ising_sixth_escape import rotation_entries_exact

PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_194col_uniform_ray_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_194col_uniform_ray_escape_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
ESCAPE_PATHS = [
    ROOT / "evidence/continuous_path_dual_escape_arb_n21.json",
    ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/188col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/189col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/190col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/191col_continuous_dual_escape_arb_n21.json",
]
PARENT_TIME_CERT = ROOT / "evidence/192col_uniform_ray_time_arb_n21.json"
TIME_CERT = ROOT / "evidence/193col_uniform_ray_time_arb_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_193col_uniform_ray_escape_n21.json"
OUTPUT_PATH = ROOT / "evidence/55probe_193col_uniform_ray_escape_dual_certificate_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"

PRECISION_BITS = 128
CANONICAL_COUNT = 1641
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)
NEW_COLUMN = 1651
SLACK_CANDIDATES = [
    Fraction(0),
    Fraction(1, 10**14),
    Fraction(1, 10**12),
    Fraction(1, 10**10),
    Fraction(1, 10**9),
    Fraction(1, 10**8),
    Fraction(1, 10**7),
    Fraction(1, 10**6),
    Fraction(1, 10**5),
    Fraction(1, 10**4),
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_json(path):
    raw = path.read_bytes()
    return json.loads(raw), sha(raw)


def main():
    ctx.prec = PRECISION_BITS
    parent_lp, parent_lp_sha = load_json(PARENT_LP)
    parent_dual, parent_dual_sha = load_json(PARENT_DUAL)
    candidate152, candidate152_sha = load_json(CANDIDATE_152)
    cut_lp, cut_lp_sha = load_json(CUT_LP)
    cut_dual, cut_dual_sha = load_json(CUT_DUAL)
    parent_time_cert, parent_time_cert_sha = load_json(PARENT_TIME_CERT)
    time_cert, time_cert_sha = load_json(TIME_CERT)
    lp, lp_sha = load_json(LP_PATH)
    escapes, escape_hashes = zip(*(load_json(path) for path in ESCAPE_PATHS))
    escapes, escape_hashes = list(escapes), list(escape_hashes)

    if lp.get("status") != "194col_uniform_ray_escape_lp_above_one_third":
        result = {
            "status": "194col_lp_not_above_one_third_requires_primal_audit",
            "complete": True,
            "strict_minimax_obstruction_certified": False,
            "lp_transcript_sha256": lp_sha,
            "expanded_lp_objective": lp.get("expanded_lp_objective"),
            "scope": "The 194-column LP is not an above-one-third discovery; do not attempt to certify a dual obstruction.",
        }
        OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        return

    if (lp.get("columns"), lp.get("rows")) != (194, 2113):
        raise RuntimeError("unexpected 194-column LP dimensions")
    if parent_lp.get("status") != "193col_uniform_ray_escape_lp_above_one_third":
        raise RuntimeError("193-column parent LP is not the expected above-cap discovery")
    if parent_dual.get("status") != "strict_194col_2113row_uniform_ray_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("193-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("192-column parent dual does not pin its LP")
    if lp.get("parent_193col_lp_sha256") != parent_lp_sha or lp.get("parent_193col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("194-column LP does not pin the exact 193-column parent")
    if lp.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("194-column LP does not pin the 152-column ancestor")
    if lp.get("cut_lp_transcript_sha256") != cut_lp_sha or lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("194-column LP does not pin the exact cut design/dual")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut-design dual is not strictly certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("cut-design dual does not pin its LP")

    if parent_time_cert.get("status") != "certified_finite_uniform_ray_escape" or not parent_time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("previous uniform-ray path is not strictly Arb-certified")
    if parent_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_192col_dual_certificate_sha256") or parent_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_192col_lp_sha256"):
        raise RuntimeError("previous uniform-ray time does not pin the 192-column ancestry")
    if parent_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("previous uniform-ray time does not pin the cut design")
    if parent_lp.get("uniform_ray_time_arb_certificate_sha256") != parent_time_cert_sha:
        raise RuntimeError("193-column parent does not pin its original finite-time certificate")
    old_t = Fraction(parent_time_cert["t_exact_rational"])
    if old_t <= 0 or Fraction(parent_time_cert["t_exact_decimal"]) != old_t:
        raise RuntimeError("previous uniform-ray exact rational/decimal mismatch")
    if Fraction(parent_lp["uniform_ray_time_exact_rational"]) != old_t:
        raise RuntimeError("193-column parent has a different previous uniform-ray time")
    if time_cert.get("status") != "certified_finite_uniform_ray_escape" or not time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("new uniform-ray path is not strictly Arb-certified")
    if time_cert.get("dual_certificate_sha256") != parent_dual_sha or time_cert.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("new uniform-ray time certificate does not pin the exact 193-column parent")
    if time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("new uniform-ray time certificate does not pin the cut design")
    if lp.get("uniform_ray_time_arb_certificate_sha256") != time_cert_sha:
        raise RuntimeError("194-column LP does not pin the new finite-time Arb certificate")
    if lp.get("parent_192col_uniform_ray_time_arb_certificate_sha256") != parent_time_cert_sha:
        raise RuntimeError("194-column LP does not pin the previous uniform-ray time certificate")
    t = Fraction(time_cert["t_exact_rational"])
    if t <= 0 or Fraction(time_cert["t_exact_decimal"]) != t or t == old_t:
        raise RuntimeError("new uniform-ray exact rational/decimal time is invalid or duplicated")
    if Fraction(lp["uniform_ray_time_exact_rational"]) != t:
        raise RuntimeError("194-column LP has a different new uniform-ray time")
    if Fraction(lp["parent_192col_uniform_ray_time_exact_rational"]) != old_t:
        raise RuntimeError("194-column LP has a different previous uniform-ray time")
    if lp.get("uniform_ray_escape_column_index") != NEW_COLUMN:
        raise RuntimeError("unexpected new uniform-ray column label")
    if lp.get("uniform_ray_rotation_source") != "explicit 21-torus spectral representation":
        raise RuntimeError("194-column LP did not use the stable spectral rotation")
    if lp.get("uniform_ray_low_features_source") != "same explicit spectral rotation as sixth/eighth features":
        raise RuntimeError("194-column LP mixed moment orders from different uniform-path rotations")

    seed_raw = SEED_POOL.read_bytes()
    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315":
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if lp.get("seed_pool_sha256_le_f64") != seed_sha or parent_lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("LP ancestry does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or lp.get("canonical_all_columns_sha256_le_f64") != all_sha:
        raise RuntimeError("canonical inventory count/hash mismatch")

    if candidate152.get("escape_couplings_exact") != escapes[0].get("candidate_couplings_exact"):
        raise RuntimeError("152-column ancestor path differs from its first Arb escape")
    for index, (escape, digest) in enumerate(zip(escapes, escape_hashes), 1):
        if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
            raise RuntimeError(f"continuous escape {index} lacks a strict Arb certificate")
        couplings = [Fraction(value) for value in escape["candidate_couplings_exact"]]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError(f"continuous escape {index} is not a positive 41-edge path")
    if len({tuple(Fraction(v) for v in e["candidate_couplings_exact"]) for e in escapes}) != 9:
        raise RuntimeError("the nine open-path escape vectors are not pairwise distinct")
    if parent_lp.get("continuous_escape_arb_certificate_sha256") != escape_hashes:
        raise RuntimeError("192-column parent escape-certificate ancestry mismatch")
    if lp.get("continuous_escape_arb_certificate_sha256") != escape_hashes:
        raise RuntimeError("193-column LP escape-certificate ancestry mismatch")
    if parent_lp.get("ninth_continuous_escape_candidate_sha256") != escapes[-1].get("candidate_sha256"):
        raise RuntimeError("192-column parent does not pin the ninth open-path escape")

    parent_order = [int(value) for value in parent_lp["column_order"]]
    column_order = [int(value) for value in lp["column_order"]]
    if len(parent_order) != 193 or len(set(parent_order)) != 193:
        raise RuntimeError("193-column parent ordering is not unique")
    if lp.get("parent_column_order") != parent_order or column_order != parent_order + [NEW_COLUMN]:
        raise RuntimeError("194-column ordering is not the exact parent plus second uniform-ray column")

    escape_couplings = (
        [[Fraction(value) for value in candidate152["escape_couplings_exact"]]]
        + [[Fraction(value) for value in escape["candidate_couplings_exact"]] for escape in escapes[1:]]
    )
    physical_columns = []
    for column in parent_order:
        if column < CANONICAL_COUNT:
            physical_columns.append([Fraction.from_float(float(value)) for value in all_columns[column]])
        elif column < 1650:
            escape_index = column - CANONICAL_COUNT
            if not 0 <= escape_index < 9:
                raise RuntimeError(f"unknown parent physical column label {column}")
            physical_columns.append(escape_couplings[escape_index])
        elif column == 1650:
            old_uniform_couplings = [Fraction(value) for value in parent_time_cert["uniform_couplings_exact_decimal"]]
            if len(old_uniform_couplings) != 41 or any(value != old_t for value in old_uniform_couplings):
                raise RuntimeError("previous uniform-ray certificate does not contain 41 identical positive couplings")
            physical_columns.append(old_uniform_couplings + [Fraction(0)])
        else:
            raise RuntimeError(f"unknown parent physical column label {column}")
    uniform_couplings = [Fraction(value) for value in time_cert["uniform_couplings_exact_decimal"]]
    if len(uniform_couplings) != 41 or any(value != t for value in uniform_couplings):
        raise RuntimeError("new uniform-ray certificate does not contain 41 identical positive couplings")
    physical_columns.append(uniform_couplings + [Fraction(0)])
    if len(physical_columns) != 194:
        raise RuntimeError("expected exactly 194 physical columns")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut_lp)
    if row_blocks != lp.get("row_blocks") or row_blocks != parent_lp.get("row_blocks"):
        raise RuntimeError("194-column exact row-block mismatch")
    if len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected mixed-order row inventory")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("194-column LP row-inventory hash mismatch")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, y)
    if len(z) != 2113 or norm > 1 or dual_objective <= Fraction(1, 3):
        raise RuntimeError("rationalized 194-column dual does not satisfy the norm/objective gate")
    active = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active if index < LOW_COUNT]
    active_sixth = [index for index in active if LOW_COUNT <= index < SIXTH_END]
    active_eighth = [index for index in active if index >= SIXTH_END]

    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }
    column_lhs = []
    column_lhs_intervals = []
    for column, couplings in zip(column_order, physical_columns):
        if column == 1650:
            entries = exact_uniform_ray_rotation(old_t)
        elif column == NEW_COLUMN:
            entries = exact_uniform_ray_rotation(t)
        else:
            entries = rotation_entries_exact(couplings)
        value = ball(lam)
        for row in active_low:
            feature = active_low_feature(system, entries, row, fourth_groups)
            value += ball(z[row]) * feature / ball(low_scales[row])
        for row in active_sixth:
            feature = orbit_average_minor(entries, sixth_rows[row - LOW_COUNT])
            value += ball(z[row]) * feature / ball(SIXTH_SCALE)
        for row in active_eighth:
            feature = orbit_average_minor(entries, eighth_rows[row - SIXTH_END])
            value += ball(z[row]) * feature / ball(EIGHTH_SCALE)
        column_lhs.append(value)
        column_lhs_intervals.append({
            "column": int(column),
            "lhs_interval": str(value),
            "upper_endpoint": str(value.upper()),
        })
        if (len(column_lhs) % 16 == 0) or column == NEW_COLUMN:
            print(f"Arb-verified 194-column inequalities {len(column_lhs)}/194", flush=True)

    chosen_delta = None
    for delta in SLACK_CANDIDATES:
        if dual_objective - delta <= Fraction(1, 3):
            continue
        if all(value.upper() <= ball(delta).lower() for value in column_lhs):
            chosen_delta = delta
            break
    if chosen_delta is None:
        raise RuntimeError("no exact rational slack leaves all 193 column inequalities strict and the lower bound above 1/3")
    shifted_upper = max(float((value - ball(chosen_delta)).upper()) for value in column_lhs)
    lower_bound = dual_objective - chosen_delta
    if lower_bound <= Fraction(1, 3) or shifted_upper >= 0:
        raise RuntimeError("final 193-column Arb strictness/lower-bound check failed")

    column_order_sha = sha(json.dumps(column_order, separators=(",", ":")).encode())
    result = {
        "status": "strict_193col_2113row_uniform_ray_escape_minimax_obstruction",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "parent_193col_lp_sha256": parent_lp_sha,
        "parent_193col_dual_certificate_sha256": parent_dual_sha,
        "parent_192col_uniform_ray_time_arb_certificate_sha256": parent_time_cert_sha,
        "parent_192col_uniform_ray_time_exact_rational": str(old_t),
        "parent_192col_dual_certificate_sha256": parent_dual_sha,
        "uniform_ray_time_arb_certificate_sha256": time_cert_sha,
        "lp_transcript_sha256": lp_sha,
        "candidate_152col_sha256": candidate152_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "cut_dual_certificate_sha256": cut_dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_hashes,
        "uniform_ray_time_exact_rational": str(t),
        "uniform_ray_time_exact_decimal": time_cert["t_exact_decimal"],
        "uniform_ray_escape_column_index": NEW_COLUMN,
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_order_sha256": column_order_sha,
        "column_order": column_order,
        "column_count": len(column_order),
        "row_count": len(y),
        "row_blocks": row_blocks,
        "sixth_rows_sha256": sixth_hash,
        "eighth_rows_sha256": eighth_hash,
        "dual_vector_rational": [str(value) for value in z],
        "dual_lambda_exact": str(lam),
        "dual_l1_norm_exact": str(norm),
        "dual_raw_normalization_scale_exact": str(dual_scale),
        "dual_objective_exact": str(dual_objective),
        "dual_slack_delta": str(chosen_delta),
        "certified_minimax_lower_bound": str(lower_bound),
        "certified_minimax_lower_bound_decimal": float(lower_bound),
        "strict_lower_bound_above_one_third": True,
        "maximum_shifted_column_lhs_upper": shifted_upper,
        "active_dual_rows": {
            "total": len(active),
            "low": len(active_low),
            "sixth": len(active_sixth),
            "eighth": len(active_eighth),
        },
        "column_dual_lhs_intervals": column_lhs_intervals,
        "scope": (
            Strict rational-dual/128-bit Arb obstruction for exactly the 194 listed physical columns "
            "and the fixed 2,113-row mixed-order design. It is not a certificate for the full 1,641-column "
            "canonical inventory, all continuous paths, complete sixth/eighth orbit constraints, or a "
            "Choi/diamond operational error bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "dual_objective": str(dual_objective),
        "delta": str(chosen_delta),
        "lower_bound": str(lower_bound),
        "dual_l1_norm": str(norm),
        "active_rows": result["active_dual_rows"],
        "maximum_shifted_column_lhs_upper": shifted_upper,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
