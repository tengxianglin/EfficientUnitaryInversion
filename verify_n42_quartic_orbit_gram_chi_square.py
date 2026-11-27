#!/usr/bin/env python3
"""Exact-Gram aggregation of all 1,440 N=42 quartic-orbit residuals.

The input residuals are 256-bit Arb intervals from the frozen all-orbit audit.
The coefficient vector is chosen deterministically from their interval
midpoints, but the final linear-form numerator is re-evaluated with Arb and
the Gram quadratic form is computed exactly over the integers/rationals.
"""
import hashlib
import json
import re
from array import array
from decimal import Decimal, ROUND_HALF_EVEN
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, fmpq, ctx

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_six_quartic_all_orbits_arb.json"
OUTPUT = ROOT / "evidence/n42_quartic_orbit_gram_chi_square_arb.json"
N = 42
N_PARTICLES = 21
GROUP_ORDER = 2 * N
COEFFICIENT_SCALE = 10**9


def canonical_orbit(indices):
    images = {
        tuple(sorted((sign * x + shift) % N for x in indices))
        for sign in (1, -1)
        for shift in range(N)
    }
    return min(images)


def enumerate_orbits():
    members = {}
    for I in combinations(range(N), 4):
        key = canonical_orbit(I)
        members.setdefault(key, []).append(I)
    ordered = sorted(members)
    assert len(ordered) == 1440, len(ordered)
    assert sum(len(members[key]) for key in ordered) == comb(N, 4)
    assert all(GROUP_ORDER % len(members[key]) == 0 for key in ordered)
    return ordered, [members[key] for key in ordered]


def interval_midpoint_decimal(text):
    if text.startswith("[+/-"):
        return Decimal(0)
    match = re.match(r"^\[\s*([^\s]+)\s*\+/-", text)
    if not match:
        raise ValueError(f"unrecognized Arb interval: {text}")
    return Decimal(match.group(1))


def balanced_slice_moment(order):
    """E product of order distinct balanced signs, for even order <= 8."""
    if order % 2:
        return fmpq(0)
    value = fmpq(1)
    for r in range(1, order // 2 + 1):
        value *= fmpq(-(2 * r - 1), N - (2 * r - 1))
    return value


def verify_moment_kernel():
    expected = [
        fmpq(1),
        fmpq(-1, 41),
        fmpq(3, 41 * 39),
        fmpq(-15, 41 * 39 * 37),
        fmpq(105, 41 * 39 * 37 * 35),
    ]
    actual = [balanced_slice_moment(2 * r) for r in range(5)]
    assert actual == expected
    assert actual[2] == fmpq(1, 533)
    return actual


def build_exact_gram_quadratic(ordered, orbit_members, coefficients):
    """Return a^T G a exactly, using the common denominator 84*D.

    For quartets I,J, f_I f_J = f_(I symmetric-difference J). If
    s=|I intersect J|, the balanced-slice moment is mu_(8-2s).
    D=41*39*37*35 clears all five possible denominators.
    """
    D = 41 * 39 * 37 * 35
    H = [
        D,
        -(39 * 37 * 35),
        3 * 37 * 35,
        -15 * 35,
        105,
    ]
    m = len(ordered)
    sizes = [len(group) for group in orbit_members]
    representative_masks = [
        sum(1 << x for x in representative)
        for representative in ordered
    ]
    orbit_masks = [
        [sum(1 << x for x in quartet) for quartet in group]
        for group in orbit_members
    ]

    h_sums = array("q", [0]) * (m * m)
    for i, representative_mask in enumerate(representative_masks):
        row_offset = i * m
        for j, masks in enumerate(orbit_masks):
            total = 0
            for mask in masks:
                intersection = (representative_mask & mask).bit_count()
                total += H[4 - intersection]
            h_sums[row_offset + j] = total

    for i in range(m):
        for j in range(i, m):
            lhs = h_sums[i * m + j] * sizes[i]
            rhs = h_sums[j * m + i] * sizes[j]
            if lhs != rhs:
                raise AssertionError(
                    f"exact Gram symmetry failed at ({i},{j}): {lhs} != {rhs}"
                )

    quadratic_numerator = 0
    for i in range(m):
        ai = coefficients[i]
        for j in range(i, m):
            aj = coefficients[j]
            scaled_entry = (
                h_sums[i * m + j] * (GROUP_ORDER // sizes[j])
            )
            reverse_entry = (
                h_sums[j * m + i] * (GROUP_ORDER // sizes[i])
            )
            assert scaled_entry == reverse_entry
            term = ai * aj * scaled_entry
            quadratic_numerator += term if i == j else 2 * term

    denominator = GROUP_ORDER * D
    if quadratic_numerator <= 0:
        raise AssertionError("Gram quadratic form is not strictly positive")
    return fmpq(quadratic_numerator, denominator), quadratic_numerator, denominator


def verify():
    ctx.prec = 256
    data = json.loads(INPUT.read_text())
    assert data["N"] == N and data["n"] == N_PARTICLES
    assert data["quartic_orbit_count"] == 1440
    assert data["quartic_subset_count"] == comb(N, 4)
    assert data["orbits_with_strict_certified_mismatch"] == 1434
    assert data["orbits_whose_residual_interval_contains_zero"] == 6

    moments = verify_moment_kernel()
    ordered, orbit_members = enumerate_orbits()
    records = {
        tuple(record["representative"]): record
        for record in data["all_orbit_records"]
    }
    if len(records) != 1440 or set(records) != set(ordered):
        raise AssertionError("orbit representatives do not match frozen Arb evidence")
    for representative, group in zip(ordered, orbit_members):
        if len(group) != records[representative]["orbit_size"]:
            raise AssertionError(f"orbit-size mismatch at {representative}")

    coefficients = []
    residual_intervals = []
    for representative in ordered:
        interval_text = records[representative]["residual_interval"]
        midpoint = interval_midpoint_decimal(interval_text)
        coefficient = int(
            (midpoint * COEFFICIENT_SCALE).to_integral_value(
                rounding=ROUND_HALF_EVEN
            )
        )
        coefficients.append(coefficient)
        residual_intervals.append(arb(interval_text))

    if not any(coefficients):
        raise AssertionError("all aggregate witness coefficients vanished")

    linear_form = sum(
        (residual_intervals[i] * coefficients[i] for i in range(1440)),
        arb(0),
    )
    if not (linear_form > 0):
        raise AssertionError("aggregate quartic linear form is not certified positive")

    gram_quadratic, gram_numerator, gram_denominator = (
        build_exact_gram_quadratic(ordered, orbit_members, coefficients)
    )
    gram_arb = arb(gram_quadratic)
    chi_square_lower_bound = linear_form * linear_form / gram_arb
    threshold = arb("0.073")
    if not (chi_square_lower_bound > threshold):
        raise AssertionError(
            f"aggregate chi-square bound did not exceed 0.073: {chi_square_lower_bound}"
        )

    d = comb(N, N_PARTICLES)
    frame_potential_target = arb(fmpq(4, d))
    frame_potential_lower_bound = (
        frame_potential_target * (1 + chi_square_lower_bound)
    )
    coefficient_json = json.dumps(
        coefficients, separators=(",", ":")
    ).encode()
    coefficient_sha256 = hashlib.sha256(coefficient_json).hexdigest()

    result = {
        "schema": "eui_n42_quartic_orbit_gram_chi_square_arb_v1",
        "status": "strict_aggregate_quartic_chi_square_lower_bound_certified",
        "N": N,
        "n": N_PARTICLES,
        "group": "D_42",
        "quartic_subset_count": comb(N, 4),
        "quartic_orbit_count": len(ordered),
        "quartic_orbit_size_sum": sum(len(group) for group in orbit_members),
        "strict_residual_orbits": data["orbits_with_strict_certified_mismatch"],
        "zero-containing_residual_orbits": data["orbits_whose_residual_interval_contains_zero"],
        "balanced_slice_even_moments_order_0_to_8": [str(x) for x in moments],
        "gram_kernel": {
            "definition": "G[O,O'] = E_uniform[phi_O(S) phi_O'(S)]",
            "feature": "phi_O(S) = average_{I in O} product_{i in I}(2*1[i in S]-1)",
            "intersection_rule": "if s=|I intersect J| then E[f_I f_J]=mu_(8-2s)",
            "common_denominator_D": 41 * 39 * 37 * 35,
            "group_order_common_multiplier": GROUP_ORDER,
            "exact_symmetry_checked": True,
        },
        "coefficient_rule": (
            "A_O = nearest integer (ties-to-even) to 10^9 times the midpoint "
            "of the frozen 256-bit Arb residual interval for orbit O"
        ),
        "coefficient_scale": COEFFICIENT_SCALE,
        "coefficient_l1": sum(abs(x) for x in coefficients),
        "coefficient_sha256": coefficient_sha256,
        "coefficients": coefficients,
        "linear_form_interval": str(linear_form),
        "gram_quadratic_exact": str(gram_quadratic),
        "gram_quadratic_numerator_common_denominator": str(gram_numerator),
        "gram_quadratic_denominator": str(gram_denominator),
        "chi_square_lower_bound_interval": str(chi_square_lower_bound),
        "chi_square_lower_bound_gt_0.073": True,
        "frame_potential_target_interval": str(frame_potential_target),
        "frame_potential_lower_bound_interval": str(frame_potential_lower_bound),
        "relative_frame_potential_factor_lower_bound": str(1 + chi_square_lower_bound),
        "existing_single_witness_program_TV_lower_bound": data[
            "program_label_tv_lower_bound_interval"
        ],
        "scope": (
            "Candidate-specific certificate for the frozen 37-base/74-labelled "
            "period-two ensemble. The aggregate quartic witness proves a "
            "chi-square lower bound for its complement-folded program-label "
            "distribution. It does not prove a TV lower bound stronger than "
            "the separately recorded bounded single-character witness, does "
            "not exclude other period-two or general cycle ensembles, and "
            "does not imply a Choi or diamond-distance bound."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "quartic_orbits": result["quartic_orbit_count"],
        "coefficient_l1": result["coefficient_l1"],
        "coefficient_sha256": coefficient_sha256,
        "linear_form_interval": result["linear_form_interval"],
        "gram_quadratic_exact": result["gram_quadratic_exact"],
        "chi_square_lower_bound_interval": result["chi_square_lower_bound_interval"],
        "frame_potential_lower_bound_interval": result["frame_potential_lower_bound_interval"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
