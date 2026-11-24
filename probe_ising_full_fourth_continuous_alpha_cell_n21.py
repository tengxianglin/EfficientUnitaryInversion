"""Rigorous Taylor enclosure of the n=21 full-fourth separator on a continuous alpha cell.

The score is a rational linear combination of principal minors of orders
0 through 4 of the active path block. Each such minor is a matrix coefficient
of an exterior-power representation. Its Taylor remainder is bounded by the
operator norm of the induced generator, avoiding interval-matrix-exponential
dependency blow-up.
"""
import hashlib
import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path

from flint import arb, arb_mat, arb_poly, ctx

from ising_fourth_moments import FourthMoments
from verify_ising_full_fourth_fractional_grid_dual_arb import (
    block_score,
    build_mask_weights,
)
from verify_ising_low_moment_design import rational

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
WARM_CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_continuous_alpha_cell_probe_n21.json"
PRECISION_BITS = 512
TAYLOR_DEGREE = 40
LENGTH = 40
CENTER = Fraction(46, 25)
RADIUS = Fraction(1, 200)


def fractional_generator(length, scale):
    generator = arb_mat(length, length)
    for j in range(length - 1):
        coupling = scale * arb.pi() / 4 * arb((j + 1) * (length - j - 1)).sqrt()
        generator[j, j + 1] = 2 * coupling
        generator[j + 1, j] = -2 * coupling
    return generator


def exact_mask_weights(system, coefficient_by_feature, length):
    """Combine second and fourth rows into exact weights on active minors."""
    weights = {}

    def add(mask, value):
        weights[mask] = weights.get(mask, Fraction(0)) + value

    n_sites = system.N
    for distance in range(1, 22):
        coefficient = coefficient_by_feature.get(distance - 1, Fraction(0))
        if not coefficient:
            continue
        for i in range(n_sites):
            j = (i + distance) % n_sites
            mask = 0
            if i < length:
                mask |= 1 << i
            if j < length:
                mask |= 1 << j
            add(mask, coefficient / n_sites)

    for quartet, raw_orbit_id in zip(system.indices, system.ids):
        orbit_id = int(raw_orbit_id)
        coefficient = coefficient_by_feature.get(21 + orbit_id, Fraction(0))
        if not coefficient:
            continue
        mask = 0
        for raw_index in quartet:
            index = int(raw_index)
            if index < length:
                mask |= 1 << index
        add(mask, coefficient / int(system.counts[orbit_id]))

    return {mask: value for mask, value in weights.items() if value}


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant_polynomial(indices, matrix_polynomials, degree):
    order = len(indices)
    if order == 0:
        return arb_poly([1])
    if order == 1:
        return matrix_polynomials[indices[0]][indices[0]].truncate(degree + 1)
    if order == 2:
        i, j = indices
        return (
            matrix_polynomials[i][i] * matrix_polynomials[j][j]
            - matrix_polynomials[i][j] * matrix_polynomials[j][i]
        ).truncate(degree + 1)

    result = arb_poly([0])
    for permutation in permutations(range(order)):
        term = arb_poly([1])
        for row, column in enumerate(permutation):
            term = (
                term
                * matrix_polynomials[indices[row]][indices[column]]
            ).truncate(degree + 1)
        if permutation_sign(permutation) > 0:
            result += term
        else:
            result -= term
    return result.truncate(degree + 1)


def build_score_taylor(length, center, degree, weights):
    """Return the degree-M Taylor polynomial of the complete frozen score."""
    generator = fractional_generator(length, rational(Fraction(1)))
    midpoint_rotation = fractional_generator(length, rational(center)).exp()

    identity = arb_mat(length, length)
    for i in range(length):
        identity[i, i] = 1

    entry_coefficients = [[[] for _ in range(length)] for _ in range(length)]
    power = identity
    for k in range(degree + 1):
        derivative_matrix = power * midpoint_rotation
        factor = rational(Fraction(1, __import__("math").factorial(k)))
        for i in range(length):
            for j in range(length):
                entry_coefficients[i][j].append(derivative_matrix[i, j] * factor)
        power = power * generator

    matrix_polynomials = [
        [arb_poly(entry_coefficients[i][j]) for j in range(length)]
        for i in range(length)
    ]

    score_polynomial = arb_poly([0])
    for mask, weight in sorted(weights.items()):
        indices = tuple(i for i in range(length) if (mask >> i) & 1)
        minor_polynomial = determinant_polynomial(
            indices, matrix_polynomials, degree
        )
        score_polynomial += minor_polynomial * rational(weight)

    return score_polynomial, midpoint_rotation


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    diagnostic = json.loads(diagnostic_raw)
    warm_raw = WARM_CERT.read_bytes()
    warm = json.loads(warm_raw)

    if hashlib.sha256(warm_raw).hexdigest() != diagnostic["warm_certificate_sha256"]:
        raise RuntimeError("warm certificate hash does not match frozen diagnostic")
    if diagnostic["status"] != "floating_finite_grid_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected diagnostic status")

    coefficient_by_feature = {
        int(item["feature_index"]): Fraction(item["coefficient"])
        for item in diagnostic["dual"]["nonzero_coefficients"]
    }
    if len(coefficient_by_feature) != 80:
        raise RuntimeError("expected the frozen 80-term separator")

    system = FourthMoments(21)
    if not set(coefficient_by_feature).issubset(set(system.reduced_indices())):
        raise RuntimeError("separator support is outside the pinned reduced system")

    second_coefficients = [
        rational(coefficient_by_feature.get(d, Fraction(0)))
        for d in range(21)
    ]
    mask_weights = build_mask_weights(system, coefficient_by_feature)
    weights = exact_mask_weights(system, coefficient_by_feature, LENGTH)
    if any(mask.bit_count() > 4 for mask in weights):
        raise RuntimeError("an active mask exceeds fourth order")

    target_score = sum(
        (
            rational(coefficient_by_feature[index])
            * rational(system.rational_target[index])
            for index in coefficient_by_feature
        ),
        arb(0),
    )

    score_polynomial, midpoint_rotation = build_score_taylor(
        LENGTH, CENTER, TAYLOR_DEGREE, weights
    )
    delta = arb(0, rational(RADIUS))
    polynomial_interval = score_polynomial(delta)

    # For a principal r-minor, det R[J,J] is a diagonal matrix coefficient
    # of exp(alpha * wedge^r(A)). The induced generator has norm <= r*||A||.
    # Here ||A||_2 = pi*(L-1)/2 by the spin-j representation, and pi < 22/7.
    # Thus every r<=4 Taylor tail on |delta|<=1/200 is bounded by
    # exp(x) * x^(M+1)/(M+1)!, x = 11*(L-1)/350.
    x_bound = rational(Fraction(11 * (LENGTH - 1), 350))
    minor_remainder_bound = (
        x_bound.exp()
        * (x_bound ** (TAYLOR_DEGREE + 1))
        / __import__("math").factorial(TAYLOR_DEGREE + 1)
    )
    weight_l1 = sum((abs(value) for value in weights.values()), Fraction(0))
    weighted_remainder_bound = rational(weight_l1) * minor_remainder_bound
    score_remainder_ball = weighted_remainder_bound * arb(0, 1)
    score_interval = polynomial_interval + score_remainder_ball
    gap_interval = target_score - score_interval

    point_score = block_score(
        midpoint_rotation,
        LENGTH,
        second_coefficients,
        mask_weights[LENGTH],
    )
    midpoint_polynomial = score_polynomial(arb(0))
    midpoint_defect = midpoint_polynomial - point_score

    sample_delta = rational(Fraction(1, 1000))
    sample_polynomial_interval = (
        score_polynomial(sample_delta) + score_remainder_ball
    )
    sample_rotation = fractional_generator(
        LENGTH, rational(CENTER + Fraction(1, 1000))
    ).exp()
    sample_score = block_score(
        sample_rotation,
        LENGTH,
        second_coefficients,
        mask_weights[LENGTH],
    )
    if not midpoint_defect.contains(0):
        raise RuntimeError(f"Taylor midpoint reconstruction mismatch: {midpoint_defect}")
    if not sample_polynomial_interval.contains(sample_score):
        raise RuntimeError("Taylor enclosure failed to contain an independent point score")

    floor = rational(Fraction(1, 4))
    certified = gap_interval.lower() > floor
    alpha_interval = rational(CENTER) + delta

    result = {
        "status": (
            "arb_certified_continuous_alpha_cell_gap_gt_1_over_4"
            if certified
            else "continuous_alpha_cell_taylor_inconclusive"
        ),
        "complete_for_declared_cell": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb Taylor coefficients and exterior-power remainder",
        "diagnostic_sha256": hashlib.sha256(diagnostic_raw).hexdigest(),
        "warm_certificate_sha256": hashlib.sha256(warm_raw).hexdigest(),
        "length": LENGTH,
        "alpha_interval": str(alpha_interval),
        "alpha_interval_lower": str(alpha_interval.lower()),
        "alpha_interval_upper": str(alpha_interval.upper()),
        "midpoint_alpha": str(CENTER),
        "taylor_degree": TAYLOR_DEGREE,
        "active_minor_mask_count": len(weights),
        "exact_weight_l1": str(weight_l1),
        "exterior_generator_norm_bound_x": str(x_bound),
        "unweighted_minor_taylor_remainder_bound": str(minor_remainder_bound),
        "weighted_score_taylor_remainder_bound": str(weighted_remainder_bound),
        "target_score_interval": str(target_score),
        "taylor_polynomial_score_interval": str(polynomial_interval),
        "score_interval_over_entire_alpha_cell": str(score_interval),
        "gap_interval_over_entire_alpha_cell": str(gap_interval),
        "gap_lower_endpoint": str(gap_interval.lower()),
        "gap_upper_endpoint": str(gap_interval.upper()),
        "required_strict_floor": "1/4",
        "midpoint_score_interval": str(point_score),
        "midpoint_reconstruction_defect": str(midpoint_defect),
        "sample_delta": "1/1000",
        "sample_score_interval": str(sample_score),
        "sample_taylor_enclosure": str(sample_polynomial_interval),
        "point_and_taylor_checks_passed": True,
        "strictly_above_floor_over_entire_cell": bool(certified),
        "scope": (
            "If certified, every alpha in the displayed interval for the "
            "L=40 single-open-path family has separator gap strictly greater "
            "than 1/4. This is only one continuum cell; it does not cover "
            "other path lengths, other alpha cells, multi-segment paths, "
            "arbitrary gapped couplings, or the full physical family."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
