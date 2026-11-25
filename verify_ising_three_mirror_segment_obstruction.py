#!/usr/bin/env python3
"""Exact obstruction for three perfect-mirror segments on the 42-site path.

Only the Python standard library is required. Every matrix entry is in
{0, +/-1}; all moment and dual calculations use fractions.Fraction.
"""
from collections import Counter
from fractions import Fraction
import json

N = 42
N_HALF = 21
TARGET_DENOMINATOR = 41
DUAL_NUMERATOR = (
    -10, 8, -6, 6, -4, 2, -2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1
)
DUAL_DENOMINATOR = 47


def compositions(total, parts):
    """Yield all ordered compositions of total into parts positive parts."""
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def signed_mirror_permutation(lengths):
    """Return the signed permutation for three consecutive mirror blocks."""
    if (
        len(lengths) != 3
        or any(int(length) != length or length < 1 for length in lengths)
        or sum(lengths) != N
    ):
        raise ValueError("lengths must be a composition of 42 into three parts")

    permutation = list(range(N))
    signs = [1] * N
    start = 0
    for length in lengths:
        for local in range(length):
            permutation[start + local] = start + length - 1 - local
            signs[start + local] = -1 if local % 2 else 1
        start += length

    if sorted(permutation) != list(range(N)):
        raise AssertionError("mirror map is not a permutation")
    if any(sign not in (-1, 1) for sign in signs):
        raise AssertionError("invalid signed-permutation entry")
    return permutation, signs


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(N)
        for j in range(i + 1, N)
    )
    return -1 if inversions % 2 else 1


def verify_so42_determinant(lengths, permutation, signs):
    """A signed permutation is orthogonal; verify its determinant is +1."""
    determinant = permutation_sign(permutation)
    for sign in signs:
        determinant *= sign
    if determinant != 1:
        raise AssertionError(f"determinant is {determinant}, not +1")


def second_moment_vector(lengths):
    """Compute all 21 cyclic distance-averaged 2x2 principal minors exactly."""
    permutation, signs = signed_mirror_permutation(lengths)
    verify_so42_determinant(lengths, permutation, signs)
    moments = []

    for distance in range(1, N_HALF + 1):
        total = 0
        for i in range(N):
            j = (i + distance) % N
            rii = signs[i] if permutation[i] == i else 0
            rjj = signs[j] if permutation[j] == j else 0
            rij = signs[i] if permutation[i] == j else 0
            rji = signs[j] if permutation[j] == i else 0
            total += rii * rjj - rij * rji
        moments.append(Fraction(total, N))

    return tuple(moments)


TARGET = tuple(
    Fraction((-1) ** (distance + 1), TARGET_DENOMINATOR)
    for distance in range(1, N_HALF + 1)
)
DUAL = tuple(Fraction(value, DUAL_DENOMINATOR) for value in DUAL_NUMERATOR)


def exact_dual_slack(lengths):
    moments = second_moment_vector(lengths)
    return sum(
        (DUAL[d] * (TARGET[d] - moments[d]) for d in range(N_HALF)),
        Fraction(0),
    )


def main():
    if sum(abs(value) for value in DUAL_NUMERATOR) != DUAL_DENOMINATOR:
        raise AssertionError("dual does not have exact l1 norm one")

    records = [
        (exact_dual_slack(lengths), lengths)
        for lengths in compositions(N, 3)
    ]
    if len(records) != 820:
        raise AssertionError(f"expected 820 compositions, found {len(records)}")

    slack_histogram = Counter(slack for slack, _ in records)
    minimum = min(slack_histogram)
    maximum = max(slack_histogram)
    if minimum != Fraction(2, 40467):
        raise AssertionError(f"unexpected exact minimum slack: {minimum}")
    if slack_histogram[minimum] != 117:
        raise AssertionError("unexpected number of minimum-slack compositions")
    if maximum != Fraction(192, 13489):
        raise AssertionError(f"unexpected exact maximum slack: {maximum}")
    if any(slack <= 0 for slack, _ in records):
        raise AssertionError("a three-segment seed escaped the exact dual")

    output = {
        "status": "exact_rational_three_mirror_segment_obstruction",
        "n": 21,
        "site_count": N,
        "segment_count": 3,
        "composition_count": len(records),
        "moment_count": N_HALF,
        "target_moments": [str(value) for value in TARGET],
        "dual_numerator": list(DUAL_NUMERATOR),
        "dual_denominator": DUAL_DENOMINATOR,
        "dual_l1_norm": str(sum((abs(value) for value in DUAL), Fraction(0))),
        "minimum_exact_slack": str(minimum),
        "minimum_slack_attainers": slack_histogram[minimum],
        "maximum_exact_slack": str(maximum),
        "distinct_exact_slacks": len(slack_histogram),
        "program_mass_tv_lower_bound": "1/40467",
        "arithmetic": "exact fractions.Fraction; no floating-point operations",
        "scope": (
            "convex mixtures of the 820 three-block perfect-mirror seeds, "
            "their dihedral images, and vertex-sign gauges"
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
