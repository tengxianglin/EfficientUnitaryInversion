#!/usr/bin/env python3
"""Exact N=10 no-go certificate for the contiguous signed-reversal block ansatz.

The verifier exhausts all 2^(N-1)=512 ordered compositions of N=10.
Every score is computed with integers/Fractions; no floating point is used.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from fractions import Fraction

N = 10
DUAL_TERMS = (
    ((0, 1), Fraction(3, 35)),
    ((0, 2), Fraction(3, 35)),
    ((0, 1, 2, 3, 4, 5), Fraction(11, 35)),
    ((0, 1, 2, 4, 5, 6), Fraction(8, 35)),
    ((0, 1, 2, 3, 4, 7), Fraction(3, 35)),
    ((0, 1, 2, 5, 6, 7), Fraction(3, 70)),
    ((0, 1, 2, 3, 5, 6, 7, 8), Fraction(11, 70)),
)
EXPECTED_SCORE_HASH = "79911ca8a15b51b84eab95720c0265dc52b7f9db6c44feab26b7d11ea5e16804"


def compositions(n: int):
    """All ordered compositions, indexed by the n-1 internal cut bits."""
    for cutmask in range(1 << (n - 1)):
        cuts = [i + 1 for i in range(n - 1) if (cutmask >> i) & 1]
        bounds = [0, *cuts, n]
        yield tuple(bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1))


def dihedral_orbit(subset: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    orbit = set()
    for shift in range(N):
        for reflection in (False, True):
            if reflection:
                image = tuple(sorted((shift - i) % N for i in subset))
            else:
                image = tuple(sorted((i + shift) % N for i in subset))
            orbit.add(image)
    return tuple(sorted(orbit))


def permutation_sign(permutation: list[int]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def block_atom(comp: tuple[int, ...]) -> tuple[list[int], list[int]]:
    """Return p and Q-entry signs for Q=R D of the block signed reversal."""
    if sum(comp) != N or any(length < 1 for length in comp):
        raise AssertionError("invalid composition")
    permutation = list(range(N))
    row_signs = [1] * N
    start = 0
    for length in comp:
        for r in range(length):
            i = start + r
            permutation[i] = start + length - 1 - r
            row_signs[i] = -1 if r % 2 else 1
        start += length

    # R has entry row_signs[i] at (i, permutation[i]); Q=R D.
    q_entry_signs = [
        row_signs[i] * (-1 if permutation[i] % 2 else 1)
        for i in range(N)
    ]

    assert all(permutation[permutation[i]] == i for i in range(N))
    assert all(q_entry_signs[i] == q_entry_signs[permutation[i]] for i in range(N))
    assert all(q_entry_signs[i] * q_entry_signs[permutation[i]] == 1 for i in range(N))
    assert sum(q_entry_signs[i] for i in range(N) if permutation[i] == i) == 0
    assert permutation_sign(permutation) * math.prod(row_signs) == 1
    return permutation, q_entry_signs


def principal_minor(
    permutation: list[int], q_entry_signs: list[int], subset: tuple[int, ...]
) -> int:
    selected = set(subset)
    if any(permutation[i] not in selected for i in subset):
        return 0
    # The induced permutation is an involution: each contained transposition
    # contributes one minus sign.
    transpositions = sum(
        1 for i in subset if permutation[i] != i and i < permutation[i]
    )
    value = -1 if transpositions % 2 else 1
    for i in subset:
        value *= q_entry_signs[i]
    return value


def target_moment(order: int) -> Fraction:
    r = order // 2
    return Fraction((-1) ** r * math.comb(N // 2, r), math.comb(N, order))


def verify() -> dict:
    orbits = [dihedral_orbit(rep) for rep, _ in DUAL_TERMS]
    orbit_sizes = [len(orbit) for orbit in orbits]
    if orbit_sizes != [10, 10, 10, 10, 10, 5, 5]:
        raise AssertionError(f"unexpected D10 orbit sizes: {orbit_sizes}")

    if sum(weight for _, weight in DUAL_TERMS) != 1:
        raise AssertionError("dual coefficients do not have L1 norm one")
    if any(weight <= 0 for _, weight in DUAL_TERMS):
        raise AssertionError("dual coefficients must be nonnegative")

    target_score = sum(
        weight * target_moment(len(rep))
        for rep, weight in DUAL_TERMS
    )
    if target_score != Fraction(-74, 2205):
        raise AssertionError(f"wrong target score: {target_score}")

    records = []
    score_histogram = Counter()
    for comp in compositions(N):
        permutation, q_entry_signs = block_atom(comp)
        score = Fraction(0)
        for (_, weight), orbit in zip(DUAL_TERMS, orbits):
            orbit_average = Fraction(
                sum(principal_minor(permutation, q_entry_signs, subset) for subset in orbit),
                len(orbit),
            )
            score += weight * orbit_average
        records.append({
            "composition": list(comp),
            "score": f"{score.numerator}/{score.denominator}",
        })
        score_histogram[score] += 1

    if len(records) != 512:
        raise AssertionError(f"expected 512 compositions, found {len(records)}")

    maximum = max(score_histogram)
    minimum = min(score_histogram)
    maximizer_count = score_histogram[maximum]
    if maximum != Fraction(-2, 35):
        raise AssertionError(f"unexpected maximum block score: {maximum}")
    if minimum != Fraction(-38, 175):
        raise AssertionError(f"unexpected minimum block score: {minimum}")
    if maximizer_count != 82:
        raise AssertionError(f"unexpected maximizer count: {maximizer_count}")
    if len(score_histogram) != 24:
        raise AssertionError("unexpected number of distinct exact scores")

    score_table = json.dumps(records, separators=(",", ":"), sort_keys=True)
    score_hash = hashlib.sha256(score_table.encode("utf-8")).hexdigest()
    if score_hash != EXPECTED_SCORE_HASH:
        raise AssertionError(f"score-table hash mismatch: {score_hash}")

    gap = target_score - maximum
    if gap != Fraction(52, 2205):
        raise AssertionError(f"unexpected separator gap: {gap}")

    return {
        "status": "exact_N10_block_mirror_subfamily_separator",
        "N": N,
        "n": N // 2,
        "family": (
            "all ordered compositions of 10 into contiguous path blocks; "
            "each block is a perfect-transfer signed reversal; arbitrary "
            "D10 conjugates and probability mixtures are included"
        ),
        "composition_count": len(records),
        "dihedral_group_order": 2 * N,
        "dual_terms": [
            {
                "representative": list(rep),
                "orbit_size": len(orbit),
                "coefficient": f"{weight.numerator}/{weight.denominator}",
                "target_moment": (
                    f"{target_moment(len(rep)).numerator}/"
                    f"{target_moment(len(rep)).denominator}"
                ),
            }
            for (rep, weight), orbit in zip(DUAL_TERMS, orbits)
        ],
        "dual_l1_norm": "1/1",
        "target_score": f"{target_score.numerator}/{target_score.denominator}",
        "maximum_block_family_score": f"{maximum.numerator}/{maximum.denominator}",
        "minimum_block_family_score": f"{minimum.numerator}/{minimum.denominator}",
        "certified_linf_moment_gap": f"{gap.numerator}/{gap.denominator}",
        "maximizer_count": maximizer_count,
        "distinct_score_count": len(score_histogram),
        "score_table_sha256": score_hash,
        "arithmetic": "exact integer and fractions.Fraction; no floating point",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
