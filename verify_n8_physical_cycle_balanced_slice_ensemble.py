#!/usr/bin/env python3
"""Exact N=8 physical-cycle balanced-slice ensemble verifier.

Only the Python standard library is required. All moment and weight checks
use integers and fractions.Fraction; no floating-point arithmetic is used.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path

N = 8
BASE_COMPOSITIONS = (
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 6),
    (1, 2, 5),
    (1, 3, 1, 3),
)
BASE_WEIGHTS = (
    Fraction(1, 105),
    Fraction(16, 105),
    Fraction(80, 105),
    Fraction(8, 105),
)
BASE_COUPLINGS = (
    ("0", "0", "0", "0", "0", "0", "0", "0"),
    ("0", "0", "pi*sqrt(5)/4", "pi*sqrt(2)/2",
     "3*pi/4", "pi*sqrt(2)/2", "pi*sqrt(5)/4", "0"),
    ("0", "pi/4", "0", "pi/2", "pi*sqrt(6)/4",
     "pi*sqrt(6)/4", "pi/2", "0"),
    ("0", "pi*sqrt(2)/4", "pi*sqrt(2)/4", "0",
     "0", "pi*sqrt(2)/4", "pi*sqrt(2)/4", "0"),
)


def signed_reversal(comp: tuple[int, ...]) -> tuple[list[int], list[int]]:
    if sum(comp) != N or any(L < 1 for L in comp):
        raise ValueError("composition must be positive and sum to 8")
    permutation = list(range(N))
    row_signs = [1] * N
    start = 0
    for length in comp:
        for r in range(length):
            permutation[start + r] = start + length - 1 - r
            row_signs[start + r] = -1 if r % 2 else 1
        start += length
    return permutation, row_signs


def dihedral_vertex_map(shift: int, reflection: bool) -> tuple[int, ...]:
    if reflection:
        return tuple((shift - i) % N for i in range(N))
    return tuple((i + shift) % N for i in range(N))


def conjugate_signed_permutation(
    permutation: list[int], row_signs: list[int],
    shift: int, reflection: bool,
) -> tuple[list[int], list[int]]:
    g = dihedral_vertex_map(shift, reflection)
    inverse = [0] * N
    for old, new in enumerate(g):
        inverse[new] = old
    new_permutation = [0] * N
    new_signs = [0] * N
    for new_row in range(N):
        old_row = inverse[new_row]
        new_permutation[new_row] = g[permutation[old_row]]
        new_signs[new_row] = row_signs[old_row]
    return new_permutation, new_signs


def permutation_sign(permutation: list[int]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def signed_permutation_determinant(permutation: list[int], row_signs: list[int]) -> int:
    product = permutation_sign(permutation)
    for sign in row_signs:
        product *= sign
    return product


def q_diagonal_trace(permutation: list[int], row_signs: list[int]) -> int:
    return sum(
        row_signs[i] * (-1 if permutation[i] % 2 else 1)
        for i in range(N) if permutation[i] == i
    )


def verify_q_involution(permutation: list[int], row_signs: list[int]) -> None:
    # Q=R D is a signed permutation. Check Q^T=Q, Q^2=I, and tr(Q)=0.
    qsign = [
        row_signs[i] * (-1 if permutation[i] % 2 else 1)
        for i in range(N)
    ]
    for i in range(N):
        j = permutation[i]
        if permutation[j] != i or qsign[i] != qsign[j]:
            raise AssertionError("Q is not a symmetric involution")
    if q_diagonal_trace(permutation, row_signs) != 0:
        raise AssertionError("Q does not have balanced signature")


def principal_minor_q(
    permutation: list[int], row_signs: list[int], subset: tuple[int, ...],
) -> int:
    image = [permutation[i] for i in subset]
    if set(image) != set(subset):
        return 0
    index = {vertex: position for position, vertex in enumerate(subset)}
    induced = [index[permutation[i]] for i in subset]
    value = permutation_sign(induced)
    for i in subset:
        value *= row_signs[i]
        value *= -1 if i % 2 else 1
    return value


def target(order: int) -> Fraction:
    r = order // 2
    return Fraction((-1) ** r * comb(4, r), comb(8, order))


def dihedral_orbits(order: int):
    unseen = set(itertools.combinations(range(N), order))
    result = []
    while unseen:
        representative = min(unseen)
        orbit = set()
        for reflection in (False, True):
            for shift in range(N):
                g = dihedral_vertex_map(shift, reflection)
                orbit.add(tuple(sorted(g[i] for i in representative)))
        result.append((representative, tuple(sorted(orbit))))
        unseen -= orbit
    return result


def fraction_string(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def verify() -> dict:
    if sum(BASE_WEIGHTS) != 1 or any(w <= 0 for w in BASE_WEIGHTS):
        raise AssertionError("base weights are not a strictly positive probability vector")

    base_matrices = []
    for comp in BASE_COMPOSITIONS:
        p, s = signed_reversal(comp)
        if signed_permutation_determinant(p, s) != 1:
            raise AssertionError(f"base atom {comp} is not in SO(8)")
        verify_q_involution(p, s)
        base_matrices.append((p, s))

    # Four base atoms times the 16 labelled elements of D_8.
    aggregate = defaultdict(Fraction)
    labelled_count = 0
    for (p, s), weight in zip(base_matrices, BASE_WEIGHTS):
        for reflection in (False, True):
            for shift in range(N):
                pp, ss = conjugate_signed_permutation(p, s, shift, reflection)
                if signed_permutation_determinant(pp, ss) != 1:
                    raise AssertionError("a dihedral image left SO(8)")
                verify_q_involution(pp, ss)
                aggregate[(tuple(pp), tuple(ss))] += weight / 16
                labelled_count += 1

    if len(aggregate) != 37:
        raise AssertionError(f"expected 37 distinct atoms, found {len(aggregate)}")
    if sum(aggregate.values()) != 1:
        raise AssertionError("aggregated physical weights do not sum to one")
    histogram = Counter(fraction_string(w) for w in aggregate.values())
    expected_histogram = {"1/105": 17, "1/21": 16, "2/105": 4}
    if dict(histogram) != expected_histogram:
        raise AssertionError(f"unexpected atom-weight histogram: {dict(histogram)}")

    # Direct exact check on every even subset, not just orbit representatives.
    subset_checks = 0
    for order in (0, 2, 4, 6, 8):
        for subset in itertools.combinations(range(N), order):
            expectation = sum(
                weight * principal_minor_q(list(p), list(s), subset)
                for (p, s), weight in aggregate.items()
            )
            if expectation != target(order):
                raise AssertionError(
                    f"subset {subset}: exact moment {expectation} != {target(order)}"
                )
            subset_checks += 1
    if subset_checks != 128:
        raise AssertionError(f"expected 128 even subsets including empty, got {subset_checks}")

    orbit_summary = []
    orbit_feature_table = []
    for order in (2, 4, 6, 8):
        orbits = dihedral_orbits(order)
        orbit_summary.append({
            "order": order,
            "subset_count": comb(N, order),
            "orbit_count": len(orbits),
            "orbit_sizes": [len(orbit) for _, orbit in orbits],
            "target": fraction_string(target(order)),
        })
        for representative_subset, orbit in orbits:
            per_atom = []
            for p, s in base_matrices:
                value = sum(
                    Fraction(principal_minor_q(p, s, I), len(orbit))
                    for I in orbit
                )
                per_atom.append(fraction_string(value))
            mixed = sum(
                weight * Fraction(value)
                for weight, value in zip(BASE_WEIGHTS, per_atom)
            )
            if mixed != target(order):
                raise AssertionError("orbit-level exact check failed")
            orbit_feature_table.append({
                "order": order,
                "representative": list(representative_subset),
                "orbit_size": len(orbit),
                "base_atom_orbit_averages": per_atom,
                "mixture_average": fraction_string(mixed),
            })

    return {
        "status": "exact_n8_physical_cycle_balanced_slice_ensemble",
        "site_count": N,
        "n": 4,
        "base_atoms": [
            {
                "composition": list(comp),
                "weight": fraction_string(weight),
                "cycle_couplings": list(couplings),
                "determinant_R": 1,
                "trace_Q": 0,
                "strictly_positive_weight": True,
                "gapped_cycle": True,
            }
            for comp, weight, couplings in zip(
                BASE_COMPOSITIONS, BASE_WEIGHTS, BASE_COUPLINGS
            )
        ],
        "labelled_dihedral_images": labelled_count,
        "distinct_physical_atoms_after_aggregation": len(aggregate),
        "distinct_atom_weight_histogram": expected_histogram,
        "distinct_atom_minimum_weight": fraction_string(min(aggregate.values())),
        "distinct_atom_maximum_weight": fraction_string(max(aggregate.values())),
        "even_subset_checks_including_empty": subset_checks,
        "nonempty_even_subset_checks": subset_checks - 1,
        "failed_checks": 0,
        "targets_by_order": [
            {"order": k, "target": fraction_string(target(k))}
            for k in (0, 2, 4, 6, 8)
        ],
        "dihedral_orbit_summary": orbit_summary,
        "orbit_feature_table": orbit_feature_table,
        "arithmetic": "exact integers and fractions.Fraction; no floating-point arithmetic",
        "scope": (
            "A positive mixture of 37 distinct real nearest-neighbour cycle "
            "exponentials realizes every even principal-minor balanced-slice "
            "target at N=8. This is a small-size matrix-moment construction; "
            "it does not establish the N=42 result or an odd-spin-length "
            "operational diamond theorem."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(verify(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
