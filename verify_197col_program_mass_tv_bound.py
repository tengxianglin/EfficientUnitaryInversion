"""Exact rational audit of the 197-column program-label TV corollary.

No floating-point arithmetic is used: the script reconstructs the raw-character
coefficient L1 bound from the pinned rational dual and exact row scales.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CERT_PATH = ROOT / "evidence/55probe_197col_uniform_ray_escape_dual_certificate_n21.json"
THEORY_PATH = ROOT / "THEORY_PROGRAM_DPP.md"
OUTPUT_PATH = ROOT / "evidence/197col_program_mass_tv_bound_n21.json"

LOW_COUNT = 1461
SECOND_COUNT = 21
FOURTH_COUNT = 1440
SIXTH_COUNT = 645
EIGHTH_COUNT = 7
SIXTH_END = LOW_COUNT + SIXTH_COUNT
ROW_COUNT = LOW_COUNT + SIXTH_COUNT + EIGHTH_COUNT


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    cert_raw = CERT_PATH.read_bytes()
    theory_raw = THEORY_PATH.read_bytes()
    cert = json.loads(cert_raw)
    if cert.get("status") != "strict_197col_2113row_uniform_ray_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("the 197-column rational dual is not strictly Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (197, ROW_COUNT):
        raise RuntimeError("unexpected finite-pool certificate dimensions")
    blocks = cert.get("row_blocks", {})
    if blocks != {
        "low_complete": LOW_COUNT,
        "sixth_selected_plus_all_cuts": SIXTH_COUNT,
        "eighth_selected": EIGHTH_COUNT,
    }:
        raise RuntimeError("the exact 2,113-row block inventory changed")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(z) != ROW_COUNT:
        raise RuntimeError("rational dual vector length mismatch")
    norm = sum((abs(value) for value in z), Fraction(0))
    if norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("rational dual L1 normalization mismatch")

    objective = Fraction(cert["dual_objective_exact"])
    delta = Fraction(cert["dual_slack_delta"])
    lower = Fraction(cert["certified_minimax_lower_bound"])
    if objective - delta != lower or lower <= Fraction(1, 3):
        raise RuntimeError("finite-pool minimax lower-bound identity/cap check failed")

    scales = (
        [Fraction(1, 41)] * SECOND_COUNT
        + [Fraction(1, 533)] * FOURTH_COUNT
        + [Fraction(5, 19721)] * SIXTH_COUNT
        + [Fraction(1, 19721)] * EIGHTH_COUNT
    )
    if len(scales) != ROW_COUNT:
        raise RuntimeError("row-scale inventory length mismatch")
    raw_character_l1 = sum(
        (abs(coefficient) / scale for coefficient, scale in zip(z, scales)),
        Fraction(0),
    )
    if raw_character_l1 <= 0:
        raise RuntimeError("raw-character test-function norm must be positive")
    tv_lower = lower / (2 * raw_character_l1)

    expected_norm = Fraction("2305843009213687359/2305843009213693952")
    expected_objective = Fraction("957172851239594049/2305843009213693952")
    expected_lower = Fraction("9347391123134860821080377/22517998136852480000000000")
    expected_raw_l1 = Fraction("48834410514256017587079/11529215046068469760")
    expected_tv = Fraction("9347391123134860821080377/190759416071312568699527343750")
    if (norm, objective, lower, raw_character_l1, tv_lower) != (
        expected_norm, expected_objective, expected_lower, expected_raw_l1, expected_tv
    ):
        raise RuntimeError("exact 197-column TV corollary changed from the pinned theorem values")

    result = {
        "status": "exact_197col_program_mass_tv_corollary_verified",
        "complete": True,
        "arithmetic": "Python fractions.Fraction; exact rational only",
        "dual_certificate_sha256": sha(cert_raw),
        "program_dpp_theory_sha256": sha(theory_raw),
        "column_count": 197,
        "row_count": ROW_COUNT,
        "row_blocks": blocks,
        "dual_l1_norm_exact": str(norm),
        "dual_objective_exact": str(objective),
        "dual_slack_delta_exact": str(delta),
        "finite_pool_minimax_lower_bound_exact": str(lower),
        "raw_character_test_function_linf_bound_exact": str(raw_character_l1),
        "program_mass_tv_lower_bound_exact": str(tv_lower),
        "program_mass_tv_lower_bound_decimal": float(tv_lower),
        "strict_program_mass_tv_lower_bound": True,
        "interpretation": (
            "For every probability mixture supported on the exact 197-column pool, the ensemble-averaged "
            "balanced program-label mass distribution has total-variation distance from uniform balanced "
            "labels strictly greater than the displayed rational lower bound."
        ),
        "scope": (
            "This is a finite-pool classical program-label mass bound, equivalently a dephased program-register "
            "trace-distance bound. It is not a Choi-state trace-distance or channel diamond-distance bound, "
            "and it does not extend to arbitrary continuous couplings; the same 197-column dual has a "
            "separately Arb-certified positive uniform-ray escape."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "raw_character_l1": str(raw_character_l1),
        "program_mass_tv_lower_bound": str(tv_lower),
        "decimal": float(tv_lower),
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
