"""128-bit Arb certification of the 204-column mixed-order LP dual."""
import hashlib
import json
from fractions import Fraction

import numpy as np
from flint import ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    load_rational_dual,
    orbit_average_minor,
)
from verify_192col_uniform_ray_time_arb import exact_uniform_ray_rotation
from verify_ising_moment_pricing import ball
from verify_ising_sixth_escape import rotation_entries_exact

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_204col_uniform_ray_escape_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_203col_uniform_ray_escape_n21.json"
PARENT_DUAL_PATH = ROOT / "evidence/55probe_203col_uniform_ray_escape_dual_certificate_n21.json"
PARENT_TIME_PATH = ROOT / "evidence/203col_uniform_ray_time_arb_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CANDIDATE_152_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
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
UNIFORM_TIME_PATHS = {
    1650: ROOT / "evidence/192col_uniform_ray_time_arb_n21.json",
    1651: ROOT / "evidence/193col_uniform_ray_time_arb_n21.json",
    1652: ROOT / "evidence/194col_uniform_ray_time_arb_n21.json",
    1653: ROOT / "evidence/195col_uniform_ray_time_arb_n21.json",
    1654: ROOT / "evidence/196col_uniform_ray_time_arb_n21.json",
    1655: ROOT / "evidence/197col_uniform_ray_time_arb_n21.json",
    1656: ROOT / "evidence/198col_uniform_ray_time_arb_n21.json",
    1657: ROOT / "evidence/199col_uniform_ray_time_arb_n21.json",
    1658: ROOT / "evidence/200col_uniform_ray_time_arb_n21.json",
    1659: ROOT / "evidence/201col_uniform_ray_time_arb_n21.json",
    1660: ROOT / "evidence/202col_uniform_ray_time_arb_n21.json",
    1661: ROOT / "evidence/203col_uniform_ray_time_arb_n21.json",
}
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT_PATH = ROOT / "evidence/55probe_204col_uniform_ray_escape_dual_certificate_n21.json"

PRECISION_BITS = 128
CANONICAL_COUNT = 1641
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)
SLACK_CANDIDATES = [
    Fraction(0), Fraction(1, 10**14), Fraction(1, 10**12),
    Fraction(1, 10**10), Fraction(1, 10**9), Fraction(1, 10**8),
    Fraction(1, 10**7), Fraction(1, 10**6), Fraction(1, 10**5),
    Fraction(1, 10**4),
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_json(path):
    raw = path.read_bytes()
    return json.loads(raw), sha(raw)


def main():
    ctx.prec = PRECISION_BITS
    lp, lp_sha = load_json(LP_PATH)
    parent_lp, parent_lp_sha = load_json(PARENT_LP_PATH)
    parent_dual, parent_dual_sha = load_json(PARENT_DUAL_PATH)
    parent_time, parent_time_sha = load_json(PARENT_TIME_PATH)
    cut_lp, cut_lp_sha = load_json(CUT_LP_PATH)
    candidate152, candidate152_sha = load_json(CANDIDATE_152_PATH)
    escapes, escape_hashes = zip(*(load_json(path) for path in ESCAPE_PATHS))
    escapes, escape_hashes = list(escapes), list(escape_hashes)
    uniform_times = {}
    uniform_time_hashes = {}
    for label, path in UNIFORM_TIME_PATHS.items():
        uniform_times[label], uniform_time_hashes[label] = load_json(path)

    if lp.get("status") != "204col_uniform_ray_escape_lp_above_one_third":
        raise RuntimeError("204-column LP is not an above-one-third discovery; use the primal-audit branch")
    if (lp.get("columns"), lp.get("rows")) != (204, 2113):
        raise RuntimeError("unexpected 204-column / 2,113-row dimensions")
    if parent_lp.get("status") != "203col_uniform_ray_escape_lp_above_one_third" or (parent_lp.get("columns"), parent_lp.get("rows")) != (203, 2113):
        raise RuntimeError("203-column parent LP is not the pinned above-cap parent")
    if parent_dual.get("status") != "strict_203col_2113row_uniform_ray_escape_minimax_obstruction" or parent_dual.get("complete") is not True:
        raise RuntimeError("203-column parent dual is not independently Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("203-column parent dual does not pin its LP transcript")
    if lp.get("parent_203col_lp_sha256") != parent_lp_sha or lp.get("parent_203col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("204-column LP does not pin the exact 203-column parent LP and dual")
    if lp.get("parent_column_order") != parent_lp.get("column_order"):
        raise RuntimeError("204-column LP parent column order differs from the certified 203-column parent")
    parent_order = [int(value) for value in parent_lp["column_order"]]
    column_order = [int(value) for value in lp["column_order"]]
    if len(parent_order) != 203 or len(set(parent_order)) != 203:
        raise RuntimeError("203-column parent order is not unique and complete")
    if column_order != parent_order + [1661] or len(set(column_order)) != 204:
        raise RuntimeError("204-column order is not exactly the parent plus physical column 1661")
    if lp.get("uniform_ray_escape_column_index") != 1661:
        raise RuntimeError("204-column appended physical label is not 1661")
    if lp.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_lp.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("204-column ancestry does not pin the exact mixed-order cut design")
    if lp.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("204-column LP does not pin the 152-column physical ancestor")
    if lp.get("sixth_rows_sha256") != parent_lp.get("sixth_rows_sha256") or lp.get("eighth_rows_sha256") != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("204-column mixed-order row inventory differs from its parent")
    if lp.get("row_blocks") != parent_lp.get("row_blocks"):
        raise RuntimeError("204-column row blocks differ from the certified parent")

    if parent_time.get("status") != "certified_finite_uniform_ray_escape" or parent_time.get("complete") is not True or not parent_time.get("finite_physical_escape_certified"):
        raise RuntimeError("203-column explicit finite-time path is not certified")
    if parent_time.get("dual_certificate_sha256") != parent_dual_sha or parent_time.get("lp_transcript_sha256") != parent_lp_sha or parent_time.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("203-column finite-time certificate does not pin its parent dual/LP/cut design")
    if lp.get("uniform_ray_time_arb_certificate_sha256") != parent_time_sha:
        raise RuntimeError("204-column LP does not pin the 203-column finite-time Arb certificate")
    t203 = Fraction(parent_time["t_exact_rational"])
    if t203 <= 0 or Fraction(parent_time["t_exact_decimal"]) != t203:
        raise RuntimeError("203-column exact rational and decimal times disagree")
    if Fraction(lp.get("uniform_ray_time_exact_rational", "0")) != t203:
        raise RuntimeError("204-column LP records a different 203-column escape time")
    c203 = [Fraction(value) for value in parent_time["uniform_couplings_exact_decimal"]]
    if len(c203) != 41 or any(value != t203 for value in c203):
        raise RuntimeError("203-column escape is not a uniform positive 41-edge path")

    seed_raw = SEED_POOL_PATH.read_bytes()
    seed = np.load(SEED_POOL_PATH, allow_pickle=False)
    seed_sha = sha(seed_raw)
    if seed.shape != (1600, 42) or seed_sha != "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315":
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if lp.get("seed_pool_sha256_le_f64") != sha(np.asarray(seed, dtype="<f8").tobytes()):
        raise RuntimeError("204-column LP does not pin the frozen seed pool")
    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or lp.get("canonical_all_columns_sha256_le_f64") != all_sha:
        raise RuntimeError("canonical inventory count/hash mismatch")

    if candidate152.get("escape_couplings_exact") != escapes[0].get("candidate_couplings_exact"):
        raise RuntimeError("152-column candidate differs from its first Arb-certified escape")
    escape_couplings = [[Fraction(value) for value in candidate152["escape_couplings_exact"]]]
    for index, (escape, digest) in enumerate(zip(escapes[1:], escape_hashes[1:]), start=2):
        if escape.get("status") != "certified_continuous_path_dual_escape" or escape.get("complete") is not True or not escape.get("strictly_positive"):
            raise RuntimeError(f"continuous escape {index} lacks a strict Arb certificate")
        couplings = [Fraction(value) for value in escape["candidate_couplings_exact"]]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError(f"continuous escape {index} is not a positive 41-edge path")
        escape_couplings.append(couplings)
    if len(escape_couplings) != 9 or len({tuple(values) for values in escape_couplings}) != 9:
        raise RuntimeError("the nine nonuniform physical escape columns are not pairwise distinct")

    uniform_couplings = {}
    uniform_t = {}
    for label, cert in uniform_times.items():
        if cert.get("status") != "certified_finite_uniform_ray_escape" or cert.get("complete") is not True or not cert.get("finite_physical_escape_certified"):
            raise RuntimeError(f"uniform path certificate for column {label} is incomplete")
        t = Fraction(cert["t_exact_rational"])
        if t <= 0 or Fraction(cert["t_exact_decimal"]) != t:
            raise RuntimeError(f"uniform path {label} has an invalid exact time")
        values = [Fraction(value) for value in cert["uniform_couplings_exact_decimal"]]
        if len(values) != 41 or any(value != t for value in values):
            raise RuntimeError(f"uniform path {label} is not a 41-edge equal-positive-coupling path")
        uniform_t[label] = t
        uniform_couplings[label] = values + [Fraction(0)]
    if len(set(uniform_t.values())) != 12:
        raise RuntimeError("the twelve uniform-path columns are not pairwise distinct")
    if uniform_time_hashes[1661] != parent_time_sha:
        raise RuntimeError("column 1661 does not use the pinned 203-column finite-time certificate")

    physical_columns = []
    for label in column_order:
        if label < CANONICAL_COUNT:
            physical_columns.append([Fraction.from_float(float(value)) for value in all_columns[label]])
        elif 1641 <= label <= 1649:
            physical_columns.append(escape_couplings[label - 1641])
        elif 1650 <= label <= 1661:
            physical_columns.append(uniform_couplings[label])
        else:
            raise RuntimeError(f"unknown physical column label {label}")
    if len(physical_columns) != 204:
        raise RuntimeError("expected exactly 204 physical columns")

    system, low_scales, sixth_rows, eighth_rows, target, row_blocks = load_exact_design(cut_lp)
    if row_blocks != lp.get("row_blocks") or len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected exact 2,113-row mixed-order design")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("204-column LP sixth/eighth row-inventory hash mismatch")

    z, lam, norm, dual_scale, dual_objective = load_rational_dual(lp, target)
    if len(z) != 2113 or norm > 1 or dual_objective <= Fraction(1, 3):
        raise RuntimeError("rationalized 204-column dual fails the exact norm/objective gate")
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
    for label, couplings in zip(column_order, physical_columns):
        entries = exact_uniform_ray_rotation(uniform_t[label]) if 1650 <= label <= 1661 else rotation_entries_exact(couplings)
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
            "column": int(label),
            "lhs_interval": str(value),
            "upper_endpoint": str(value.upper()),
        })
        if len(column_lhs) % 16 == 0 or label == 1661:
            print(f"Arb-verified 204-column inequalities {len(column_lhs)}/204", flush=True)

    chosen_delta = None
    for delta in SLACK_CANDIDATES:
        if dual_objective - delta <= Fraction(1, 3):
            continue
        if all(value.upper() <= ball(delta).lower() for value in column_lhs):
            chosen_delta = delta
            break
    if chosen_delta is None:
        raise RuntimeError("no rational slack certifies all 204 columns while retaining a lower bound above 1/3")
    shifted_upper = max(float((value - ball(chosen_delta)).upper()) for value in column_lhs)
    lower_bound = dual_objective - chosen_delta
    if lower_bound <= Fraction(1, 3) or shifted_upper >= 0:
        raise RuntimeError("final 204-column Arb strictness/lower-bound check failed")

    column_order_sha = sha(json.dumps(column_order, separators=(",", ":")).encode())
    result = {
        "status": "strict_204col_2113row_uniform_ray_escape_minimax_obstruction",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "lp_transcript_sha256": lp_sha,
        "parent_203col_lp_sha256": parent_lp_sha,
        "parent_203col_dual_certificate_sha256": parent_dual_sha,
        "parent_203col_uniform_ray_time_arb_certificate_sha256": parent_time_sha,
        "parent_152col_candidate_sha256": candidate152_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "seed_pool_sha256": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "column_order_sha256": column_order_sha,
        "column_order": column_order,
        "column_count": 204,
        "row_count": 2113,
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
            "total": len(active), "low": len(active_low),
            "sixth": len(active_sixth), "eighth": len(active_eighth),
        },
        "column_dual_lhs_intervals": column_lhs_intervals,
        "scope": (
            "Strict rational-dual/128-bit Arb obstruction for exactly the 204 listed physical columns "
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
