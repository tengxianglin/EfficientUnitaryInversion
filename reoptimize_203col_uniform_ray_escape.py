"""Binary64 discovery LP after appending the 202-dual Arb-certified uniform-ray path as column 1660.

The LP is discovery only. An above-cap result needs a new exact rational dual
and independent Arb checks of all 203 columns. A below-cap result needs an
exact rational primal audit and the complete sixth-order orbit verification.
"""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import matrix, orbit_minor
from discover_193col_uniform_torus_pricing import block_rotation, uniform_path_basis

PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_202col_uniform_ray_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_202col_uniform_ray_escape_dual_certificate_n21.json"
BASE_LP = ROOT / "evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json"
BASE_DUAL = ROOT / "evidence/55probe_192col_ninth_continuous_escape_dual_certificate_n21.json"
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
BASE_TIME_CERT = ROOT / "evidence/192col_uniform_ray_time_arb_n21.json"
PARENT_TIME_CERT = ROOT / "evidence/193col_uniform_ray_time_arb_n21.json"
GRANDPARENT_TIME_CERT = ROOT / "evidence/194col_uniform_ray_time_arb_n21.json"
GREATGRANDPARENT_TIME_CERT = ROOT / "evidence/195col_uniform_ray_time_arb_n21.json"
PREVIOUS_TIME_CERT = ROOT / "evidence/196col_uniform_ray_time_arb_n21.json"
TIME_CERT = ROOT / "evidence/197col_uniform_ray_time_arb_n21.json"
NEW_TIME_CERT = ROOT / "evidence/198col_uniform_ray_time_arb_n21.json"
LATEST_TIME_CERT = ROOT / "evidence/199col_uniform_ray_time_arb_n21.json"
FINAL_TIME_CERT = ROOT / "evidence/200col_uniform_ray_time_arb_n21.json"
NEXT_TIME_CERT = ROOT / "evidence/201col_uniform_ray_time_arb_n21.json"
NEXT2_TIME_CERT = ROOT / "evidence/202col_uniform_ray_time_arb_n21.json"
SEED_POOL = ROOT / "evidence/seed_pool_n21_frozen.npy"
LP_OUT = ROOT / "evidence/joint_low_six_eighth_lp_203col_uniform_ray_escape_n21.json"
CANDIDATE_OUT = ROOT / "evidence/candidate_joint_input_203col_uniform_ray_escape_n21.json"

SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CANONICAL_COUNT = 1641
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)
NEW_COLUMN = 1660


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_json(path):
    raw = path.read_bytes()
    return json.loads(raw), sha(raw)


def low_features_from_rotation(system, rotation):
    N = 42
    indices = np.arange(N)
    diagonal = rotation.diagonal()
    second = [
        np.mean(
            diagonal * diagonal[(indices + distance) % N]
            - rotation[indices, (indices + distance) % N]
            * rotation[(indices + distance) % N, indices]
        )
        for distance in range(1, system.n + 1)
    ]
    subsets = system.indices
    determinants = np.linalg.det(rotation[subsets[:, :, None], subsets[:, None, :]])
    fourth = np.bincount(
        system.ids, weights=determinants, minlength=len(system.keys)
    ) / system.counts
    return np.r_[second, fourth]


def main():
    parent_lp, parent_lp_sha = load_json(PARENT_LP)
    parent_dual, parent_dual_sha = load_json(PARENT_DUAL)
    base_lp, base_lp_sha = load_json(BASE_LP)
    base_dual, base_dual_sha = load_json(BASE_DUAL)
    candidate152, candidate152_sha = load_json(CANDIDATE_152)
    cut_lp, cut_lp_sha = load_json(CUT_LP)
    cut_dual, cut_dual_sha = load_json(CUT_DUAL)
    base_time_cert, base_time_cert_sha = load_json(BASE_TIME_CERT)
    parent_time_cert, parent_time_cert_sha = load_json(PARENT_TIME_CERT)
    grandparent_time_cert, grandparent_time_cert_sha = load_json(GRANDPARENT_TIME_CERT)
    greatgrandparent_time_cert, greatgrandparent_time_cert_sha = load_json(GREATGRANDPARENT_TIME_CERT)
    previous_time_cert, previous_time_cert_sha = load_json(PREVIOUS_TIME_CERT)
    time_cert, time_cert_sha = load_json(TIME_CERT)
    new_time_cert, new_time_cert_sha = load_json(NEW_TIME_CERT)
    latest_time_cert, latest_time_cert_sha = load_json(LATEST_TIME_CERT)
    final_time_cert, final_time_cert_sha = load_json(FINAL_TIME_CERT)
    next_time_cert, next_time_cert_sha = load_json(NEXT_TIME_CERT)
    next2_time_cert, next2_time_cert_sha = load_json(NEXT2_TIME_CERT)
    escapes, escape_hashes = zip(*(load_json(path) for path in ESCAPE_PATHS))
    escapes, escape_hashes = list(escapes), list(escape_hashes)

    if parent_lp.get("status") != "202col_uniform_ray_escape_lp_above_one_third":
        raise RuntimeError("202-column parent LP is not the expected above-cap discovery")
    if (parent_lp.get("columns"), parent_lp.get("rows")) != (202, 2113):
        raise RuntimeError("unexpected 202-column parent dimensions")
    if parent_dual.get("status") != "strict_202col_2113row_uniform_ray_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("202-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("202-column parent dual does not pin its LP")
    if parent_lp.get("parent_199col_lp_sha256") != parent_dual.get("parent_199col_lp_sha256") or parent_lp.get("parent_199col_dual_certificate_sha256") != parent_dual.get("parent_199col_dual_certificate_sha256"):
        raise RuntimeError("200-column parent-LP/dual ancestry mismatch")
    if parent_lp.get("parent_198col_lp_sha256") != parent_dual.get("parent_198col_lp_sha256") or parent_lp.get("parent_198col_dual_certificate_sha256") != parent_dual.get("parent_198col_dual_certificate_sha256"):
        raise RuntimeError("199-column parent-LP/dual ancestry mismatch")
    if parent_lp.get("parent_195col_lp_sha256") != parent_dual.get("parent_195col_lp_sha256"):
        raise RuntimeError("197-column parent-LP ancestry mismatch")
    if parent_lp.get("parent_195col_dual_certificate_sha256") != parent_dual.get("parent_195col_dual_certificate_sha256"):
        raise RuntimeError("197-column parent-dual ancestry mismatch")
    if parent_lp.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("195-column parent does not pin the 152-column ancestor")
    if parent_lp.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("195-column parent does not pin the exact cut design/dual")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut-design dual is not strictly Arb-certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("cut-design dual does not pin the cut LP")

    for label, cert in (("192-column", base_time_cert), ("193-column", parent_time_cert), ("194-column", grandparent_time_cert), ("195-column", greatgrandparent_time_cert), ("196-column", previous_time_cert), ("197-column", time_cert), ("198-column", new_time_cert)):
        if cert.get("status") != "certified_finite_uniform_ray_escape" or not cert.get("finite_physical_escape_certified"):
            raise RuntimeError(f"{label} uniform-ray time lacks a strict Arb certificate")
    if base_lp.get("status") != "192col_ninth_continuous_escape_lp_above_one_third" or (base_lp.get("columns"), base_lp.get("rows")) != (192, 2113):
        raise RuntimeError("base 192-column LP is not the expected above-cap parent")
    if base_dual.get("status") != "strict_192col_2113row_ninth_continuous_escape_minimax_obstruction" or not base_dual.get("complete"):
        raise RuntimeError("base 192-column dual is not strictly Arb-certified")
    if base_dual.get("lp_transcript_sha256") != base_lp_sha:
        raise RuntimeError("base 192-column dual does not pin its LP")
    if base_lp.get("cut_lp_transcript_sha256") != cut_lp_sha or base_dual.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("base 192-column ancestry does not pin the exact cut design")
    if base_time_cert.get("dual_certificate_sha256") != base_dual_sha or base_time_cert.get("lp_transcript_sha256") != base_lp_sha or base_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("base uniform-ray time does not pin the exact 192-column dual/LP/cut design")
    if parent_lp.get("parent_192col_dual_certificate_sha256") != base_dual_sha:
        raise RuntimeError("195-column parent does not pin the base 192-column dual")
    if parent_lp.get("parent_192col_uniform_ray_time_arb_certificate_sha256") != base_time_cert_sha:
        raise RuntimeError("195-column parent does not pin the base uniform-ray time certificate")
    base_t = Fraction(base_time_cert["t_exact_rational"])
    if base_t <= 0 or Fraction(base_time_cert["t_exact_decimal"]) != base_t:
        raise RuntimeError("base uniform-ray exact rational/decimal mismatch")
    base_uniform_couplings = [Fraction(value) for value in base_time_cert["uniform_couplings_exact_decimal"]]
    if len(base_uniform_couplings) != 41 or any(value != base_t for value in base_uniform_couplings):
        raise RuntimeError("base time certificate is not a uniform 41-edge path")
    if Fraction(parent_lp["parent_192col_uniform_ray_time_exact_rational"]) != base_t:
        raise RuntimeError("195-column parent has a different base uniform-ray time")

    if parent_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_193col_dual_certificate_sha256"):
        raise RuntimeError("193-column time does not pin the 193-column ancestor dual")
    if parent_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_193col_lp_sha256") or parent_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("193-column time does not pin the 193-column LP/cut design")
    if parent_lp.get("parent_193col_uniform_ray_time_arb_certificate_sha256") != parent_time_cert_sha:
        raise RuntimeError("195-column parent does not pin the 193-column time certificate")
    parent_t = Fraction(parent_time_cert["t_exact_rational"])
    if parent_t <= 0 or Fraction(parent_time_cert["t_exact_decimal"]) != parent_t or parent_t == base_t:
        raise RuntimeError("193-column time is nonpositive, inconsistent, or duplicates the base path")
    parent_uniform_couplings = [Fraction(value) for value in parent_time_cert["uniform_couplings_exact_decimal"]]
    if len(parent_uniform_couplings) != 41 or any(value != parent_t for value in parent_uniform_couplings):
        raise RuntimeError("193-column time certificate is not a uniform 41-edge path")
    if Fraction(parent_lp["parent_193col_uniform_ray_time_exact_rational"]) != parent_t:
        raise RuntimeError("195-column parent has a different 193-column ancestor time")

    if grandparent_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_194col_dual_certificate_sha256") or grandparent_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_194col_lp_sha256"):
        raise RuntimeError("194-column ancestor time does not pin the exact 194-column dual/LP")
    if grandparent_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_lp.get("parent_194col_uniform_ray_time_arb_certificate_sha256") != grandparent_time_cert_sha:
        raise RuntimeError("197-column parent does not pin the exact 194-column time certificate/cut design")
    grandparent_t = Fraction(grandparent_time_cert["t_exact_rational"])
    if grandparent_t <= 0 or Fraction(grandparent_time_cert["t_exact_decimal"]) != grandparent_t or grandparent_t in (base_t, parent_t):
        raise RuntimeError("194-column ancestor time is invalid or duplicates an earlier path")
    if Fraction(parent_lp["parent_194col_uniform_ray_time_exact_rational"]) != grandparent_t:
        raise RuntimeError("197-column parent has a different 194-column ancestor time")
    grandparent_uniform_couplings = [Fraction(value) for value in grandparent_time_cert["uniform_couplings_exact_decimal"]]
    if len(grandparent_uniform_couplings) != 41 or any(value != grandparent_t for value in grandparent_uniform_couplings):
        raise RuntimeError("194-column ancestor time is not a uniform 41-edge path")

    if greatgrandparent_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_195col_dual_certificate_sha256") or greatgrandparent_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_195col_lp_sha256") or greatgrandparent_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("195-column time certificate does not pin the exact 195-column ancestor")
    greatgrandparent_t = Fraction(greatgrandparent_time_cert["t_exact_rational"])
    if greatgrandparent_t <= 0 or Fraction(greatgrandparent_time_cert["t_exact_decimal"]) != greatgrandparent_t or greatgrandparent_t in (base_t, parent_t, grandparent_t):
        raise RuntimeError("195-column ancestor time is invalid or duplicates an earlier path")
    greatgrandparent_uniform_couplings = [Fraction(value) for value in greatgrandparent_time_cert["uniform_couplings_exact_decimal"]]
    if len(greatgrandparent_uniform_couplings) != 41 or any(value != greatgrandparent_t for value in greatgrandparent_uniform_couplings):
        raise RuntimeError("195-column ancestor time certificate is not a uniform 41-edge path")
    if Fraction(parent_lp["parent_195col_uniform_ray_time_exact_rational"]) != greatgrandparent_t:
        raise RuntimeError("197-column parent has a different 195-column ancestor time")

    if parent_lp.get("parent_196col_lp_sha256") != parent_dual.get("parent_196col_lp_sha256") or parent_lp.get("parent_196col_dual_certificate_sha256") != parent_dual.get("parent_196col_dual_certificate_sha256"):
        raise RuntimeError("197-column parent LP/dual ancestry mismatch")
    if previous_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_196col_dual_certificate_sha256") or previous_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_196col_lp_sha256"):
        raise RuntimeError("196-column previous time does not pin the exact parent LP/dual")
    if previous_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("196-column previous time does not pin the cut design")
    if parent_lp.get("parent_196col_uniform_ray_time_arb_certificate_sha256") != previous_time_cert_sha:
        raise RuntimeError("198-column parent does not pin the 196-column previous time certificate")
    previous_t = Fraction(previous_time_cert["t_exact_rational"])
    if previous_t <= 0 or Fraction(previous_time_cert["t_exact_decimal"]) != previous_t:
        raise RuntimeError("196-column previous time is nonpositive or inconsistent")
    previous_uniform_couplings = [Fraction(value) for value in previous_time_cert["uniform_couplings_exact_decimal"]]
    if len(previous_uniform_couplings) != 41 or any(value != previous_t for value in previous_uniform_couplings):
        raise RuntimeError("196-column previous time is not a uniform 41-edge path")
    if Fraction(parent_lp["parent_196col_uniform_ray_time_exact_rational"]) != previous_t:
        raise RuntimeError("198-column parent has a different 196-column ancestor time")

    if time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_197col_dual_certificate_sha256") or time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_197col_lp_sha256"):
        raise RuntimeError("197-column time does not pin the exact 197-column ancestor dual/LP")
    if time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha or time_cert.get("status") != "certified_finite_uniform_ray_escape" or not time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("197-column time does not pin the cut design or lacks a strict Arb certificate")
    t = Fraction(time_cert["t_exact_rational"])
    if t <= 0 or Fraction(time_cert["t_exact_decimal"]) != t or t in (base_t, parent_t, grandparent_t, greatgrandparent_t, previous_t):
        raise RuntimeError("new uniform-ray time is invalid or duplicates an existing path")
    uniform_couplings = [Fraction(value) for value in time_cert["uniform_couplings_exact_decimal"]]
    if len(uniform_couplings) != 41 or any(value != t for value in uniform_couplings):
        raise RuntimeError("197-column finite-time certificate is not a uniform 41-edge path")
    if parent_lp.get("parent_197col_uniform_ray_time_arb_certificate_sha256") != time_cert_sha:
        raise RuntimeError("199-column parent does not pin the exact 197-column finite-time certificate")
    if Fraction(parent_lp.get("parent_197col_uniform_ray_time_exact_rational")) != t:
        raise RuntimeError("199-column parent has a different 197-column uniform-ray time")

    if new_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_198col_dual_certificate_sha256") or new_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_198col_lp_sha256") or new_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("198-column finite-time certificate does not pin the exact 198-column ancestor dual/LP/cut design")
    if new_time_cert.get("status") != "certified_finite_uniform_ray_escape" or not new_time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("198-column finite-time path lacks a strict Arb certificate")
    t_new = Fraction(new_time_cert["t_exact_rational"])
    if t_new <= 0 or Fraction(new_time_cert["t_exact_decimal"]) != t_new or t_new in (base_t, parent_t, grandparent_t, greatgrandparent_t, previous_t, t):
        raise RuntimeError("198-column finite-time path is invalid or duplicates an existing path")
    new_uniform_couplings = [Fraction(value) for value in new_time_cert["uniform_couplings_exact_decimal"]]
    if len(new_uniform_couplings) != 41 or any(value != t_new for value in new_uniform_couplings):
        raise RuntimeError("198-column finite-time certificate is not a uniform 41-edge path")
    if parent_lp.get("parent_198col_uniform_ray_time_arb_certificate_sha256") != new_time_cert_sha:
        raise RuntimeError("200-column parent does not pin the exact 198-column ancestor finite-time certificate")
    t_final = Fraction(final_time_cert["t_exact_rational"])
    if parent_lp.get("uniform_ray_time_arb_certificate_sha256") != next_time_cert_sha or Fraction(parent_lp.get("uniform_ray_time_exact_rational")) != Fraction(next_time_cert["t_exact_rational"]):
        raise RuntimeError("202-column parent current escape pin does not match the 201-column finite-time certificate")
    if Fraction(parent_lp.get("parent_198col_uniform_ray_time_exact_rational")) != t_new:
        raise RuntimeError("200-column parent has a different 198-column ancestor uniform-ray time")

    if latest_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_199col_dual_certificate_sha256") or latest_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_199col_lp_sha256") or latest_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("199-column finite-time certificate does not pin the exact 199-column ancestor dual/LP/cut design")
    if parent_lp.get("parent_199col_uniform_ray_time_arb_certificate_sha256") != latest_time_cert_sha:
        raise RuntimeError("200-column parent does not pin the exact 199-column finite-time certificate")
    if Fraction(parent_lp.get("parent_199col_uniform_ray_time_exact_rational")) != Fraction(latest_time_cert["t_exact_rational"]):
        raise RuntimeError("200-column parent has a different 199-column uniform-ray time")
    if latest_time_cert.get("status") != "certified_finite_uniform_ray_escape" or not latest_time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("199-column finite-time path lacks a strict Arb certificate")
    t_latest = Fraction(latest_time_cert["t_exact_rational"])
    if t_latest <= 0 or Fraction(latest_time_cert["t_exact_decimal"]) != t_latest or t_latest in (base_t, parent_t, grandparent_t, greatgrandparent_t, previous_t, t, t_new):
        raise RuntimeError("199-column finite-time path is invalid or duplicates an existing path")
    latest_uniform_couplings = [Fraction(value) for value in latest_time_cert["uniform_couplings_exact_decimal"]]
    if len(latest_uniform_couplings) != 41 or any(value != t_latest for value in latest_uniform_couplings):
        raise RuntimeError("199-column finite-time certificate is not a uniform 41-edge path")

    if final_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_200col_dual_certificate_sha256") or final_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_200col_lp_sha256") or final_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("200-column finite-time certificate does not pin the exact 200-column ancestor dual/LP/cut design")
    if parent_lp.get("parent_200col_uniform_ray_time_arb_certificate_sha256") != final_time_cert_sha:
        raise RuntimeError("202-column parent does not pin the exact 200-column finite-time certificate")
    if final_time_cert.get("status") != "certified_finite_uniform_ray_escape" or not final_time_cert.get("complete") or not final_time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("200-column finite-time path lacks a complete strict Arb certificate")
    if t_final <= 0 or Fraction(final_time_cert["t_exact_decimal"]) != t_final or t_final in (base_t, parent_t, grandparent_t, greatgrandparent_t, previous_t, t, t_new, t_latest):
        raise RuntimeError("200-column finite-time path is invalid or duplicates an existing path")
    final_uniform_couplings = [Fraction(value) for value in final_time_cert["uniform_couplings_exact_decimal"]]
    if len(final_uniform_couplings) != 41 or any(value != t_final for value in final_uniform_couplings):
        raise RuntimeError("200-column finite-time certificate is not a uniform 41-edge path")

    seed_raw = SEED_POOL.read_bytes()
    seed = np.asarray(np.load(SEED_POOL, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if parent_lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("195-column parent does not pin the frozen seed pool")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != CANONICAL_COUNT or all_sha != parent_lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical inventory count/hash mismatch")

    if candidate152.get("escape_couplings_exact") != escapes[0].get("candidate_couplings_exact"):
        raise RuntimeError("152-column ancestor path differs from its Arb-certified first escape")
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

    parent_order = [int(value) for value in parent_lp["column_order"]]
    if len(parent_order) != 202 or len(set(parent_order)) != 202:
        raise RuntimeError("202-column parent ordering is not unique")
    escape_couplings = (
        [[Fraction(value) for value in candidate152["escape_couplings_exact"]]]
        + [[Fraction(value) for value in escape["candidate_couplings_exact"]] for escape in escapes[1:]]
    )
    if len(escape_couplings) != 9:
        raise RuntimeError("expected nine Arb-certified nonuniform path vectors")
    base_uniform_path = base_uniform_couplings + [Fraction(0)]
    parent_uniform_path = parent_uniform_couplings + [Fraction(0)]
    grandparent_uniform_path = grandparent_uniform_couplings + [Fraction(0)]
    greatgrandparent_uniform_path = greatgrandparent_uniform_couplings + [Fraction(0)]
    previous_uniform_path = previous_uniform_couplings + [Fraction(0)]
    time_uniform_path = uniform_couplings + [Fraction(0)]
    new_uniform_path = new_uniform_couplings + [Fraction(0)]
    latest_uniform_path = latest_uniform_couplings + [Fraction(0)]
    final_uniform_path = final_uniform_couplings + [Fraction(0)]
    next_t = Fraction(next_time_cert["t_exact_rational"])
    next_uniform_couplings = [Fraction(value) for value in next_time_cert["uniform_couplings_exact_decimal"]]
    next_uniform_path = next_uniform_couplings + [Fraction(0)]
    physical_columns = []
    for column in parent_order:
        if column < CANONICAL_COUNT:
            physical_columns.append(all_columns[column])
        elif column < 1650:
            escape_index = column - CANONICAL_COUNT
            if not 0 <= escape_index < 9:
                raise RuntimeError(f"unknown parent physical column label {column}")
            physical_columns.append(escape_couplings[escape_index])
        elif column == 1650:
            physical_columns.append(base_uniform_path)
        elif column == 1651:
            physical_columns.append(parent_uniform_path)
        elif column == 1652:
            physical_columns.append(grandparent_uniform_path)
        elif column == 1653:
            physical_columns.append(greatgrandparent_uniform_path)
        elif column == 1654:
            physical_columns.append(previous_uniform_path)
        elif column == 1655:
            physical_columns.append(time_uniform_path)
        elif column == 1656:
            physical_columns.append(new_uniform_path)
        elif column == 1657:
            physical_columns.append(latest_uniform_path)
        elif column == 1658:
            physical_columns.append(final_uniform_path)
        elif column == 1659:
            physical_columns.append(next_uniform_path)
        else:
            raise RuntimeError(f"unknown parent physical column label {column}")
    if next_time_cert.get("dual_certificate_sha256") != parent_lp.get("parent_201col_dual_certificate_sha256") or next_time_cert.get("lp_transcript_sha256") != parent_lp.get("parent_201col_lp_sha256") or next_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("201-column finite-time certificate does not pin the 201-column ancestor dual/LP/cut design")
    if next_time_cert.get("status") != "certified_finite_uniform_ray_escape" or not next_time_cert.get("complete") or not next_time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("201-column finite-time path lacks a complete strict Arb certificate")
    if next_t <= 0 or Fraction(next_time_cert["t_exact_decimal"]) != next_t or next_t in (base_t, parent_t, grandparent_t, greatgrandparent_t, previous_t, t, t_new, t_latest, t_final):
        raise RuntimeError("201-column finite-time path is invalid or duplicates an existing path")
    if len(next_uniform_couplings) != 41 or any(value != next_t for value in next_uniform_couplings):
        raise RuntimeError("201-column finite-time certificate is not a uniform 41-edge path")
    if parent_lp.get("parent_201col_uniform_ray_time_arb_certificate_sha256") != next_time_cert_sha or Fraction(parent_lp.get("parent_201col_uniform_ray_time_exact_rational")) != next_t:
        raise RuntimeError("202-column parent does not pin the 201-column finite-time ancestor certificate")
    if parent_lp.get("uniform_ray_time_arb_certificate_sha256") != next_time_cert_sha or Fraction(parent_lp.get("uniform_ray_time_exact_rational")) != next_t:
        raise RuntimeError("202-column parent current path differs from the 201-column finite-time certificate")

    next2_t = Fraction(next2_time_cert["t_exact_rational"])
    if next2_time_cert.get("dual_certificate_sha256") != parent_dual_sha or next2_time_cert.get("lp_transcript_sha256") != parent_lp_sha or next2_time_cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("202-column finite-time certificate does not pin the exact parent dual/LP/cut design")
    if next2_time_cert.get("status") != "certified_finite_uniform_ray_escape" or not next2_time_cert.get("complete") or not next2_time_cert.get("finite_physical_escape_certified"):
        raise RuntimeError("202-column finite-time path lacks a complete strict Arb certificate")
    if next2_t <= 0 or Fraction(next2_time_cert["t_exact_decimal"]) != next2_t or next2_t in (base_t, parent_t, grandparent_t, greatgrandparent_t, previous_t, t, t_new, t_latest, t_final, next_t):
        raise RuntimeError("202-column finite-time path is invalid or duplicates an existing path")
    next2_uniform_couplings = [Fraction(value) for value in next2_time_cert["uniform_couplings_exact_decimal"]]
    if len(next2_uniform_couplings) != 41 or any(value != next2_t for value in next2_uniform_couplings):
        raise RuntimeError("202-column finite-time certificate is not a uniform 41-edge path")
    new_couplings = next2_uniform_couplings + [Fraction(0)]
    new_float = np.asarray([float(value) for value in new_couplings], dtype="<f8")
    if any(np.array_equal(new_float, np.asarray(column, dtype="<f8")) for column in physical_columns):
        raise RuntimeError("new uniform-ray escape duplicates a parent column")
    physical_columns.append(new_couplings)
    column_order = parent_order + [NEW_COLUMN]
    if len(physical_columns) != 203:
        raise RuntimeError("expanded physical pool must contain 203 columns")
    torus_q, torus_omega = uniform_path_basis()
    base_uniform_rotation = torus_q @ block_rotation(float(base_t) * torus_omega) @ torus_q.T
    parent_uniform_rotation = torus_q @ block_rotation(float(parent_t) * torus_omega) @ torus_q.T
    grandparent_uniform_rotation = torus_q @ block_rotation(float(grandparent_t) * torus_omega) @ torus_q.T
    greatgrandparent_uniform_rotation = torus_q @ block_rotation(float(greatgrandparent_t) * torus_omega) @ torus_q.T
    previous_uniform_rotation = torus_q @ block_rotation(float(previous_t) * torus_omega) @ torus_q.T
    time_uniform_rotation = torus_q @ block_rotation(float(t) * torus_omega) @ torus_q.T
    uniform_rotation = torus_q @ block_rotation(float(t_new) * torus_omega) @ torus_q.T
    latest_uniform_rotation = torus_q @ block_rotation(float(t_latest) * torus_omega) @ torus_q.T
    final_uniform_rotation = torus_q @ block_rotation(float(t_final) * torus_omega) @ torus_q.T
    next_uniform_rotation = torus_q @ block_rotation(float(next_t) * torus_omega) @ torus_q.T
    next2_uniform_rotation = torus_q @ block_rotation(float(next2_t) * torus_omega) @ torus_q.T
    base_defect = float(np.max(np.abs(base_uniform_rotation.T @ base_uniform_rotation - np.eye(42))))
    parent_defect = float(np.max(np.abs(parent_uniform_rotation.T @ parent_uniform_rotation - np.eye(42))))
    time_orthogonality_defect = float(np.max(np.abs(time_uniform_rotation.T @ time_uniform_rotation - np.eye(42))))
    uniform_orthogonality_defect = float(np.max(np.abs(uniform_rotation.T @ uniform_rotation - np.eye(42))))
    latest_orthogonality_defect = float(np.max(np.abs(latest_uniform_rotation.T @ latest_uniform_rotation - np.eye(42))))
    final_orthogonality_defect = float(np.max(np.abs(final_uniform_rotation.T @ final_uniform_rotation - np.eye(42))))
    next_orthogonality_defect = float(np.max(np.abs(next_uniform_rotation.T @ next_uniform_rotation - np.eye(42))))
    next2_orthogonality_defect = float(np.max(np.abs(next2_uniform_rotation.T @ next2_uniform_rotation - np.eye(42))))
    grandparent_defect = float(np.max(np.abs(grandparent_uniform_rotation.T @ grandparent_uniform_rotation - np.eye(42))))
    greatgrandparent_defect = float(np.max(np.abs(greatgrandparent_uniform_rotation.T @ greatgrandparent_uniform_rotation - np.eye(42))))
    previous_defect = float(np.max(np.abs(previous_uniform_rotation.T @ previous_uniform_rotation - np.eye(42))))
    if max(base_defect, parent_defect, grandparent_defect, greatgrandparent_defect, previous_defect, time_orthogonality_defect, uniform_orthogonality_defect, latest_orthogonality_defect, final_orthogonality_defect, next_orthogonality_defect, next2_orthogonality_defect) > 1e-8:
        raise RuntimeError(f"uniform-ray spectral rotation is not orthogonal: {max(base_defect, parent_defect, grandparent_defect, greatgrandparent_defect, previous_defect, time_orthogonality_defect, uniform_orthogonality_defect, latest_orthogonality_defect, final_orthogonality_defect, next_orthogonality_defect, next2_orthogonality_defect)}")

    sixth_rows = [tuple(int(v) for v in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_targets = [Fraction(v) for v in cut_lp["sixth_cut_targets"]]
    eighth_rows = [tuple(int(v) for v in row) for row in cut_lp["selected_eighth_rows"]]
    eighth_targets = [Fraction(v) for v in cut_lp["selected_eighth_targets"]]
    if len(sixth_rows) != 645 or len(sixth_targets) != 645 or len(set(sixth_rows)) != 645:
        raise RuntimeError("unexpected sixth-order row inventory")
    if len(eighth_rows) != 7 or len(eighth_targets) != 7:
        raise RuntimeError("unexpected selected eighth-order row inventory")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth-order target mismatch")
    expected_eighth = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]
    if expected_eighth != eighth_targets:
        raise RuntimeError("eighth-order target mismatch")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != parent_lp.get("sixth_rows_sha256") or eighth_hash != parent_lp.get("eighth_rows_sha256"):
        raise RuntimeError("row inventory differs from the certified 192-column design")

    system = FourthMoments(21)
    system.exact_target_check()
    low_rows = []
    for index, couplings in enumerate(physical_columns):
        column = column_order[index]
        if column == 1650:
            low_rows.append(low_features_from_rotation(system, base_uniform_rotation))
        elif column == 1651:
            low_rows.append(low_features_from_rotation(system, parent_uniform_rotation))
        elif column == 1652:
            low_rows.append(low_features_from_rotation(system, grandparent_uniform_rotation))
        elif column == 1653:
            low_rows.append(low_features_from_rotation(system, greatgrandparent_uniform_rotation))
        elif column == 1654:
            low_rows.append(low_features_from_rotation(system, previous_uniform_rotation))
        elif column == 1655:
            low_rows.append(low_features_from_rotation(system, time_uniform_rotation))
        elif column == 1656:
            low_rows.append(low_features_from_rotation(system, uniform_rotation))
        elif column == 1657:
            low_rows.append(low_features_from_rotation(system, latest_uniform_rotation))
        elif column == 1658:
            low_rows.append(low_features_from_rotation(system, final_uniform_rotation))
        elif column == 1659:
            low_rows.append(low_features_from_rotation(system, next_uniform_rotation))
        elif column == NEW_COLUMN:
            low_rows.append(low_features_from_rotation(system, next2_uniform_rotation))
        else:
            low_rows.append(system.features(np.asarray(list(map(float, couplings)))))
    low = np.asarray(low_rows)
    low_target = system.target.copy()
    low_scale = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]
    if len(low_target) != 1461:
        raise RuntimeError("unexpected complete second/fourth row count")

    sixth = np.empty((203, len(sixth_rows)), dtype=np.float64)
    eighth = np.empty((203, len(eighth_rows)), dtype=np.float64)
    for index, couplings in enumerate(physical_columns):
        column = column_order[index]
        if column == 1650:
            rotation = base_uniform_rotation
        elif column == 1651:
            rotation = parent_uniform_rotation
        elif column == 1652:
            rotation = grandparent_uniform_rotation
        elif column == 1653:
            rotation = greatgrandparent_uniform_rotation
        elif column == 1654:
            rotation = previous_uniform_rotation
        elif column == 1655:
            rotation = time_uniform_rotation
        elif column == 1656:
            rotation = uniform_rotation
        elif column == 1657:
            rotation = latest_uniform_rotation
        elif column == 1658:
            rotation = final_uniform_rotation
        elif column == 1659:
            rotation = next_uniform_rotation
        elif column == NEW_COLUMN:
            rotation = next2_uniform_rotation
        else:
            rotation = matrix(couplings)
        sixth[index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[index] = [orbit_minor(rotation, row) for row in eighth_rows]
        if (index + 1) % 16 == 0 or index == 202:
            print(f"Built physical feature columns {index + 1}/203", flush=True)

    sixth_scale = np.full(len(sixth_rows), float(SIXTH_SCALE))
    eighth_scale = np.full(len(eighth_rows), float(EIGHTH_SCALE))
    A = np.vstack([
        low.T / low_scale[:, None],
        sixth.T / sixth_scale[:, None],
        eighth.T / eighth_scale[:, None],
    ])
    y = np.r_[
        low_target / low_scale,
        np.asarray([float(value) for value in sixth_targets]) / sixth_scale,
        np.asarray([float(value) for value in eighth_targets]) / eighth_scale,
    ]
    row_blocks = {
        "low_complete": len(low_target),
        "sixth_selected_plus_all_cuts": len(sixth_rows),
        "eighth_selected": len(eighth_rows),
    }
    m, n = A.shape
    if (m, n) != (2113, 203):
        raise RuntimeError(f"unexpected expanded LP dimensions: {(m, n)}")

    aub = np.vstack([np.c_[A, -np.ones(m)], np.c_[-A, -np.ones(m)]])
    bub = np.r_[y, -y]
    result = linprog(
        np.r_[np.zeros(n), 1.0],
        A_ub=aub,
        b_ub=bub,
        A_eq=np.r_[np.ones(n), 0.0][None, :],
        b_eq=[1.0],
        bounds=[(0.0, None)] * n + [(0.0, None)],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"HiGHS failed: {result.message}")

    residual = np.abs(A @ result.x[:-1] - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))
    dual_z = result.ineqlin.marginals[:m] - result.ineqlin.marginals[m:]
    dual_objective = float(result.eqlin.marginals[0] + np.dot(dual_z, y))
    support = [
        {"column": int(column_order[index]), "weight": float(weight)}
        for index, weight in enumerate(result.x[:-1]) if weight > 1e-10
    ]
    matrix_sha = sha(np.asarray(A, dtype="<f8").tobytes() + np.asarray(y, dtype="<f8").tobytes())
    status = (
        "203col_uniform_ray_escape_lp_candidate_below_one_third"
        if result.fun < 1 / 3 else "203col_uniform_ray_escape_lp_above_one_third"
    )
    transcript = {
        "status": status,
        "parent_202col_lp_sha256": parent_lp_sha,
        "parent_202col_dual_certificate_sha256": parent_dual_sha,
        "parent_201col_lp_sha256": parent_lp.get("parent_201col_lp_sha256"),
        "parent_201col_dual_certificate_sha256": parent_lp.get("parent_201col_dual_certificate_sha256"),
        "parent_200col_lp_sha256": parent_lp.get("parent_200col_lp_sha256"),
        "parent_200col_dual_certificate_sha256": parent_lp.get("parent_200col_dual_certificate_sha256"),
        "parent_199col_lp_sha256": parent_lp.get("parent_199col_lp_sha256"),
        "parent_199col_dual_certificate_sha256": parent_lp.get("parent_199col_dual_certificate_sha256"),
        "parent_198col_lp_sha256": parent_lp.get("parent_198col_lp_sha256"),
        "parent_198col_dual_certificate_sha256": parent_lp.get("parent_198col_dual_certificate_sha256"),
        "parent_197col_lp_sha256": parent_lp.get("parent_197col_lp_sha256"),
        "parent_197col_dual_certificate_sha256": parent_lp.get("parent_197col_dual_certificate_sha256"),
        "parent_196col_lp_sha256": parent_lp.get("parent_196col_lp_sha256"),
        "parent_196col_dual_certificate_sha256": parent_lp.get("parent_196col_dual_certificate_sha256"),
        "parent_196col_uniform_ray_time_arb_certificate_sha256": previous_time_cert_sha,
        "parent_196col_uniform_ray_time_exact_rational": str(previous_t),
        "parent_195col_lp_sha256": parent_lp.get("parent_195col_lp_sha256"),
        "parent_195col_dual_certificate_sha256": parent_lp.get("parent_195col_dual_certificate_sha256"),
        "parent_195col_uniform_ray_time_arb_certificate_sha256": greatgrandparent_time_cert_sha,
        "parent_195col_uniform_ray_time_exact_rational": str(greatgrandparent_t),
        "parent_194col_lp_sha256": parent_lp.get("parent_194col_lp_sha256"),
        "parent_194col_dual_certificate_sha256": parent_lp.get("parent_194col_dual_certificate_sha256"),
        "parent_194col_uniform_ray_time_arb_certificate_sha256": grandparent_time_cert_sha,
        "parent_194col_uniform_ray_time_exact_rational": str(grandparent_t),
        "parent_193col_lp_sha256": parent_lp.get("parent_193col_lp_sha256"),
        "parent_193col_dual_certificate_sha256": parent_lp.get("parent_193col_dual_certificate_sha256"),
        "parent_193col_uniform_ray_time_arb_certificate_sha256": parent_time_cert_sha,
        "parent_193col_uniform_ray_time_exact_rational": str(parent_t),
        "parent_192col_lp_sha256": base_lp_sha,
        "parent_192col_dual_certificate_sha256": parent_lp.get("parent_192col_dual_certificate_sha256"),
        "parent_192col_uniform_ray_time_arb_certificate_sha256": base_time_cert_sha,
        "parent_192col_uniform_ray_time_exact_rational": str(base_t),
        "parent_152col_candidate_sha256": candidate152_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "cut_dual_certificate_sha256": cut_dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_hashes,
        "parent_197col_uniform_ray_time_arb_certificate_sha256": time_cert_sha,
        "parent_197col_uniform_ray_time_exact_rational": str(t),
        "parent_198col_uniform_ray_time_arb_certificate_sha256": new_time_cert_sha,
        "parent_198col_uniform_ray_time_exact_rational": str(t_new),
        "parent_199col_uniform_ray_time_arb_certificate_sha256": latest_time_cert_sha,
        "parent_199col_uniform_ray_time_exact_rational": str(t_latest),
        "parent_200col_uniform_ray_time_arb_certificate_sha256": final_time_cert_sha,
        "parent_200col_uniform_ray_time_exact_rational": str(t_final),
        "parent_201col_uniform_ray_time_arb_certificate_sha256": next_time_cert_sha,
        "parent_201col_uniform_ray_time_exact_rational": str(next_t),
        "parent_202col_dual_escape_time_arb_certificate_sha256": next2_time_cert_sha,
        "parent_202col_dual_escape_time_exact_rational": str(next2_t),
        "uniform_ray_time_arb_certificate_sha256": next2_time_cert_sha,
        "uniform_ray_time_exact_rational": str(next2_t),
        "uniform_ray_time_exact_decimal": next2_time_cert["t_exact_decimal"],
        "parent_194col_uniform_ray_time_exact_rational": str(grandparent_t),
        "uniform_ray_escape_column_index": NEW_COLUMN,
        "uniform_ray_rotation_source": "explicit 21-torus spectral representation",
        "uniform_ray_rotation_orthogonality_max_abs": next2_orthogonality_defect,
        "parent_201col_uniform_ray_rotation_orthogonality_max_abs": next_orthogonality_defect,
        "parent_200col_uniform_ray_rotation_orthogonality_max_abs": final_orthogonality_defect,
        "parent_199col_uniform_ray_rotation_orthogonality_max_abs": latest_orthogonality_defect,
        "parent_197col_uniform_ray_rotation_orthogonality_max_abs": time_orthogonality_defect,
        "parent_198col_uniform_ray_rotation_orthogonality_max_abs": uniform_orthogonality_defect,
        "uniform_ray_low_features_source": "same explicit spectral rotation as sixth/eighth features",
        "seed_pool_sha256_le_f64": seed_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "parent_column_order": parent_order,
        "column_order": column_order,
        "sixth_rows_sha256": sixth_hash,
        "eighth_rows_sha256": eighth_hash,
        "matrix_and_target_sha256_le_f64": matrix_sha,
        "solver": "scipy.optimize.linprog(method=highs), binary64 discovery only",
        "expanded_lp_objective": float(result.fun),
        "expanded_recomputed_max": float(residual.max()),
        "expanded_block_maxima": {
            name: float(residual[cuts[index]:cuts[index + 1]].max())
            for index, name in enumerate(row_blocks)
        },
        "positive_support": support,
        "dual_discovery": {
            "z_l1_norm": float(np.abs(dual_z).sum()),
            "objective": dual_objective,
            "primal_dual_gap": abs(float(result.fun) - dual_objective),
            "inequality_marginals": [float(value) for value in result.ineqlin.marginals],
            "equality_marginal": float(result.eqlin.marginals[0]),
        },
        "finite_candidate_below_one_third": bool(result.fun < 1 / 3),
        "scope": (
            "Binary64 HiGHS discovery on the fixed 2,113-row mixed-order design after appending "
            "the exact Arb-certified 202-dual uniform positive-coupling path as physical column 1660. "
            "A sub-1/3 result is discovery only until an exact rational primal passes Arb on all "
            "pinned rows and a complete 63,133-orbit sixth-order audit. An above-cap result requires "
            "a new exact rational dual and independent Arb verification against all 203 physical columns."
        ),
    }
    LP_OUT.write_text(json.dumps(transcript, indent=2) + "\n")
    lp_sha = sha(LP_OUT.read_bytes())

    candidate_written = False
    if result.fun < 1 / 3:
        raw_weights = [
            (int(column_order[index]), Fraction.from_float(float(weight)))
            for index, weight in enumerate(result.x[:-1]) if weight > 1e-10
        ]
        total = sum((weight for _, weight in raw_weights), Fraction(0))
        exact_probabilities = [
            {"column": column, "probability": str(weight / total)}
            for column, weight in raw_weights
        ]
        if sum((Fraction(row["probability"]) for row in exact_probabilities), Fraction(0)) != 1:
            raise RuntimeError("exact candidate probabilities do not sum to one")
        candidate = {
            "source_file": str(LP_OUT.relative_to(ROOT)),
            "source_sha256": lp_sha,
            "parent_202col_lp_sha256": parent_lp_sha,
            "parent_202col_dual_certificate_sha256": parent_dual_sha,
            "parent_201col_lp_sha256": parent_lp.get("parent_201col_lp_sha256"),
            "parent_201col_dual_certificate_sha256": parent_lp.get("parent_201col_dual_certificate_sha256"),
            "parent_200col_lp_sha256": parent_lp.get("parent_200col_lp_sha256"),
            "parent_200col_dual_certificate_sha256": parent_lp.get("parent_200col_dual_certificate_sha256"),
            "parent_199col_lp_sha256": parent_lp.get("parent_199col_lp_sha256"),
            "parent_199col_dual_certificate_sha256": parent_lp.get("parent_199col_dual_certificate_sha256"),
            "parent_198col_lp_sha256": parent_lp.get("parent_198col_lp_sha256"),
            "parent_198col_dual_certificate_sha256": parent_lp.get("parent_198col_dual_certificate_sha256"),
            "parent_197col_lp_sha256": parent_lp.get("parent_197col_lp_sha256"),
            "parent_197col_dual_certificate_sha256": parent_lp.get("parent_197col_dual_certificate_sha256"),
            "parent_196col_lp_sha256": parent_lp.get("parent_196col_lp_sha256"),
            "parent_196col_dual_certificate_sha256": parent_lp.get("parent_196col_dual_certificate_sha256"),
            "parent_196col_uniform_ray_time_arb_certificate_sha256": previous_time_cert_sha,
            "parent_196col_uniform_ray_time_exact_rational": str(previous_t),
            "parent_195col_lp_sha256": parent_lp.get("parent_195col_lp_sha256"),
            "parent_195col_dual_certificate_sha256": parent_lp.get("parent_195col_dual_certificate_sha256"),
            "parent_195col_uniform_ray_time_arb_certificate_sha256": greatgrandparent_time_cert_sha,
            "parent_195col_uniform_ray_time_exact_rational": str(greatgrandparent_t),
            "parent_194col_lp_sha256": parent_lp.get("parent_194col_lp_sha256"),
            "parent_194col_dual_certificate_sha256": parent_lp.get("parent_194col_dual_certificate_sha256"),
            "parent_194col_uniform_ray_time_arb_certificate_sha256": grandparent_time_cert_sha,
            "parent_194col_uniform_ray_time_exact_rational": str(grandparent_t),
            "parent_193col_lp_sha256": parent_lp.get("parent_193col_lp_sha256"),
            "parent_193col_dual_certificate_sha256": parent_lp.get("parent_193col_dual_certificate_sha256"),
            "parent_193col_uniform_ray_time_arb_certificate_sha256": parent_time_cert_sha,
            "parent_193col_uniform_ray_time_exact_rational": str(parent_t),
            "parent_192col_uniform_ray_time_arb_certificate_sha256": base_time_cert_sha,
            "parent_192col_lp_sha256": base_lp_sha,
            "parent_192col_uniform_ray_time_exact_rational": str(base_t),
            "parent_192col_dual_certificate_sha256": parent_lp.get("parent_192col_dual_certificate_sha256"),
            "parent_197col_uniform_ray_time_arb_certificate_sha256": time_cert_sha,
            "parent_197col_uniform_ray_time_exact_rational": str(t),
            "parent_198col_uniform_ray_time_arb_certificate_sha256": new_time_cert_sha,
            "parent_198col_uniform_ray_time_exact_rational": str(t_new),
            "parent_199col_uniform_ray_time_arb_certificate_sha256": latest_time_cert_sha,
            "parent_199col_uniform_ray_time_exact_rational": str(t_latest),
            "parent_200col_uniform_ray_time_arb_certificate_sha256": final_time_cert_sha,
            "parent_200col_uniform_ray_time_exact_rational": str(t_final),
            "parent_201col_uniform_ray_time_arb_certificate_sha256": next_time_cert_sha,
            "parent_201col_uniform_ray_time_exact_rational": str(next_t),
            "parent_202col_dual_escape_time_arb_certificate_sha256": next2_time_cert_sha,
            "parent_202col_dual_escape_time_exact_rational": str(next2_t),
            "uniform_ray_time_arb_certificate_sha256": next2_time_cert_sha,
            "uniform_ray_time_exact_rational": str(next2_t),
            "parent_194col_uniform_ray_time_exact_rational": str(grandparent_t),
            "uniform_ray_escape_column_index": NEW_COLUMN,
            "seed_pool_sha256_le_f64": seed_sha,
            "canonical_all_columns_sha256_le_f64": all_sha,
            "parent_column_order": parent_order,
            "column_order": column_order,
            "columns": [row["column"] for row in exact_probabilities],
            "exact_probabilities": exact_probabilities,
            "exact_probability_sum": "1",
            "support_size": len(exact_probabilities),
            "precision_bits": 64,
            "finite_lp_objective": repr(float(result.fun)),
            "sixth_cut_rows": [list(row) for row in sixth_rows],
            "sixth_cut_targets": [str(value) for value in sixth_targets],
            "selected_eighth_rows": [list(row) for row in eighth_rows],
            "selected_eighth_targets": [str(value) for value in eighth_targets],
            "scope": (
                "Exact rational probabilities obtained by normalizing binary64 203-column HiGHS weights. "
                "This candidate is constrained only on the pinned 2,113 rows and requires independent "
                "Arb verification plus complete sixth-order separation."
            ),
        }
        CANDIDATE_OUT.write_text(json.dumps(candidate, indent=2) + "\n")
        candidate_written = True

    print(json.dumps({
        "status": status,
        "columns": n,
        "rows": m,
        "objective": float(result.fun),
        "recomputed_max": float(residual.max()),
        "block_maxima": transcript["expanded_block_maxima"],
        "support_size": len(support),
        "primal_dual_gap": abs(float(result.fun) - dual_objective),
        "candidate_written": candidate_written,
        "lp_output": str(LP_OUT.relative_to(ROOT)),
        "candidate_output": str(CANDIDATE_OUT.relative_to(ROOT)) if candidate_written else None,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
