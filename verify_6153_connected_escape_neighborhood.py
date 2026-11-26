#!/usr/bin/env python3
"""Certify an open positive-coupling escape region for the 6,153-column dual.

The base point is certified independently at 256-bit Arb. This script then
uses exact rational inequalities plus an analytic Duhamel/Hadamard Lipschitz
bound to extend the strict escape to a full-dimensional open set with all 42
cyclic couplings strictly positive. It does not claim a global convex-hull
result.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
DIAGNOSTIC = EVIDENCE / "ising_full_fourth_plus_thirty_gapped_n21.json"
FINITE_CERT = EVIDENCE / "ising_full_fourth_plus_thirty_gapped_arb_n21.json"
SEARCH = EVIDENCE / "ising_full_fourth_plus_thirty_gapped_search_n21.json"
ESCAPE = EVIDENCE / "ising_full_fourth_plus_thirty_gapped_escape_arb_n21.json"
OUTPUT = EVIDENCE / "ising_full_fourth_plus_thirty_gapped_open_box_arb_n21.json"
PRECISION_BITS = 256
DELTA = Fraction(1, 2_000_000)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_sha = sha256(DIAGNOSTIC)
    finite_sha = sha256(FINITE_CERT)
    search_sha = sha256(SEARCH)
    diagnostic = json.loads(DIAGNOSTIC.read_text())
    finite = json.loads(FINITE_CERT.read_text())
    search = json.loads(SEARCH.read_text())
    escape = json.loads(ESCAPE.read_text())

    if diagnostic.get("candidate_count") != 6153:
        raise RuntimeError("unexpected finite-pool diagnostic")
    if finite.get("status") != "arb_certified_finite_6153_column_full_fourth_plus_thirty_gapped_separator":
        raise RuntimeError("the pinned finite-pool Arb certificate is not certified")
    if not finite.get("complete") or finite.get("candidate_count") != 6153:
        raise RuntimeError("the finite-pool certificate is incomplete")
    if finite.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("finite certificate does not pin the current diagnostic")
    if finite.get("dual_full_coordinate_l1_exact") != "533":
        raise RuntimeError("the exact full-coordinate dual L1 norm is not 533")
    if finite.get("full_feature_count") != 1461:
        raise RuntimeError("unexpected full feature dimension")

    if escape.get("status") != "arb_certified_6153_dual_general_gapped_escape" or not escape.get("complete"):
        raise RuntimeError("the connected escape is not independently Arb-certified")
    if escape.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("escape certificate diagnostic pin mismatch")
    if escape.get("finite_certificate_sha256") != finite_sha:
        raise RuntimeError("escape certificate finite-certificate pin mismatch")
    if escape.get("search_sha256") != search_sha:
        raise RuntimeError("escape certificate search pin mismatch")
    pins = search.get("pins", {})
    if pins.get("diagnostic_sha256") != diagnostic_sha or pins.get("finite_certificate_sha256") != finite_sha:
        raise RuntimeError("search transcript pins do not match the current inputs")

    witness = escape["candidate_results"]["connected"]
    if not witness.get("strict_separator_escape_certified"):
        raise RuntimeError("the connected base point is not a certified escape")
    if not witness.get("orthogonality_all_interval_defects_contain_zero"):
        raise RuntimeError("the base-point orthogonality check is incomplete")
    if witness.get("orthogonality_matrix_entries_checked") != 42 * 42:
        raise RuntimeError("unexpected orthogonality-check count")
    if not witness.get("determinant_contains_one"):
        raise RuntimeError("the base-point determinant-one check is missing")

    couplings = [Fraction(value) for value in witness["couplings_exact_rational"]]
    if len(couplings) != 42 or couplings[-1] != 0:
        raise RuntimeError("the base point must have 41 path edges and a zero wrap edge")
    if any(value <= 0 for value in couplings[:41]):
        raise RuntimeError("the 41 internal base couplings are not all positive")
    minimum_internal = min(couplings[:41])
    if minimum_internal <= DELTA:
        raise RuntimeError("the chosen perturbation radius would reach an internal zero/negative edge")

    # For cyclic nearest-neighbour A(c), max row/column sum of A(c)-A(c*)
    # is <= 4*||c-c*||_infinity. Duhamel for skew generators gives the same
    # operator-norm bound for their exponentials. Each retained feature is an
    # average of order-2 or order-4 principal minors; determinant multilinearity
    # and Hadamard give a feature Lipschitz constant at most 4. The exact dual
    # coefficient L1 norm is 533.
    generator_lipschitz = Fraction(4)
    minor_feature_lipschitz = Fraction(4)
    dual_l1 = Fraction(finite["dual_full_coordinate_l1_exact"])
    score_variation = generator_lipschitz * minor_feature_lipschitz * dual_l1 * DELTA
    if score_variation != Fraction(533, 125000):
        raise RuntimeError("unexpected exact score-variation bound")

    base_gap = arb(witness["arb_target_minus_score_interval"])
    if not base_gap.upper() < arb(-20.324):
        raise RuntimeError("base-point Arb gap is not below the pinned -20.324 threshold")
    robust_gap = base_gap + arb(score_variation.numerator) / arb(score_variation.denominator)
    if not robust_gap.upper() < 0:
        raise RuntimeError("the analytic Lipschitz extension does not preserve strict escape")

    minimum_after = minimum_internal - DELTA
    wrap_example = DELTA / 2
    if minimum_after <= 0 or not (0 < wrap_example < DELTA):
        raise RuntimeError("the displayed full-cycle positive region is not strictly positive")

    result = {
        "status": "arb_basepoint_plus_analytic_full_cycle_positive_open_box_escape",
        "complete": True,
        "precision_bits_basepoint": PRECISION_BITS,
        "method": "256-bit Arb base point + exact-rational Duhamel/Hadamard Lipschitz extension",
        "diagnostic_sha256": diagnostic_sha,
        "finite_certificate_sha256": finite_sha,
        "search_sha256": search_sha,
        "escape_certificate_sha256": sha256(ESCAPE),
        "finite_pool_columns": 6153,
        "dual_full_coordinate_l1_exact": str(dual_l1),
        "base_point_target_minus_score_interval": str(base_gap),
        "coupling_radius_exact": str(DELTA),
        "minimum_internal_base_coupling_exact": str(minimum_internal),
        "minimum_internal_coupling_after_perturbation_exact": str(minimum_after),
        "generator_operator_norm_lipschitz": "4",
        "principal_minor_feature_lipschitz": "4",
        "dual_score_lipschitz": str(generator_lipschitz * minor_feature_lipschitz * dual_l1),
        "score_variation_bound_exact": str(score_variation),
        "robust_target_minus_score_interval": str(robust_gap),
        "robust_target_minus_score_upper_bound": str(robust_gap.upper()),
        "all_42_cycle_couplings_strictly_positive": True,
        "full_dimensional_open_region": {
            "internal_edges": "|c_j-c_j_star| < 1/2000000 for j=0,...,40",
            "wrap_edge": "0 < c_41 < 1/2000000",
            "explicit_wrap_edge_example": str(wrap_example),
        },
        "proof_scope": (
            "Every cyclic coupling vector in the displayed full-dimensional open region "
            "has all 42 couplings strictly positive and violates this particular 6,153-column "
            "dual. The result follows from the 256-bit Arb base-point gap and an analytic "
            "Duhamel/Hadamard Lipschitz bound. It does not invalidate the finite-pool theorem, "
            "prove full-family convex-hull feasibility or infeasibility, construct an all-even-"
            "principal-minor ensemble, or imply a Choi/diamond-distance bound."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "coupling_radius": result["coupling_radius_exact"],
        "score_variation_bound": result["score_variation_bound_exact"],
        "robust_gap_upper": result["robust_target_minus_score_upper_bound"],
        "all_42_couplings_strictly_positive": True,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
