#!/usr/bin/env python3
"""Exact n=21 obstruction for 3--7 consecutive perfect-mirror segments.

The exhaustive composition scan uses only integer arithmetic.  A separate
signed-permutation implementation cross-checks the closed-form moment formula
on 700 deterministic random compositions.
"""
from argparse import ArgumentParser
from fractions import Fraction
from itertools import combinations
from math import comb
import json
import random
import sys

N = 42
N_HALF = 21
DUAL_NUMERATOR = (-10, 8, -6, 6, -4, 2, -2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1)
DUAL_DENOMINATOR = 47
COMMON_DENOMINATOR = DUAL_DENOMINATOR * 41 * N
SEGMENT_COUNTS = (3, 4, 5, 6, 7)

EXPECTED = {
    3: (820, "2/40467", 117, "192/13489", 15),
    4: (10660, "2/40467", 38, "1027/40467", 26),
    5: (101270, "4/1927", 30, "1478/40467", 35),
    6: (749398, "4/1927", 6, "86/1927", 43),
    7: (4496388, "166/40467", 7, "299/5781", 48),
}


def compositions(total, parts):
    """Yield every ordered positive composition using its cut set."""
    for cuts in combinations(range(1, total), parts - 1):
        previous = 0
        lengths = []
        for cut in cuts:
            lengths.append(cut - previous)
            previous = cut
        lengths.append(total - previous)
        yield tuple(lengths)


def mirror_moment_sums(lengths):
    """Return S_d=sum_i det R[{i,i+d}] for all d=1,...,21.

    For a signed reversal block of length L, every transposed pair has
    principal minor (-1)^L.  An odd block has one fixed centre with sign
    (-1)^((L-1)/2); pairs of such centres contribute the product of signs.
    For d<21 each unordered pair occurs once in the directed sum over i;
    for d=21 the antipodal pair occurs twice.
    """
    sums = [0] * N_HALF
    centres = []
    start = 0
    for length in lengths:
        if length & 1:
            centres.append((start + (length - 1) // 2,
                            -1 if ((length - 1) // 2) & 1 else 1))
        block_minor = -1 if length & 1 else 1
        for local in range(length // 2):
            separation = length - 1 - 2 * local
            distance = min(separation, N - separation)
            multiplicity = 2 if distance == N_HALF else 1
            sums[distance - 1] += multiplicity * block_minor
        start += length

    for index, (left_site, left_sign) in enumerate(centres):
        for right_site, right_sign in centres[index + 1:]:
            separation = abs(left_site - right_site)
            distance = min(separation, N - separation)
            multiplicity = 2 if distance == N_HALF else 1
            sums[distance - 1] += multiplicity * left_sign * right_sign
    return sums


def exact_slack_numerator(lengths):
    """Return integer numerator over 47*41*42 for y.(t-m(R))."""
    sums = mirror_moment_sums(lengths)
    return sum(
        coefficient * (N * ((-1) ** (distance + 1)) - 41 * moment_sum)
        for distance, (coefficient, moment_sum) in enumerate(
            zip(DUAL_NUMERATOR, sums), start=1
        )
    )


def direct_signed_permutation(lengths):
    """Independent direct matrix check: return determinant and all S_d."""
    permutation = [0] * N
    signs = [1] * N
    start = 0
    for length in lengths:
        for local in range(length):
            permutation[start + local] = start + length - 1 - local
            signs[start + local] = -1 if local & 1 else 1
        start += length

    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(N)
        for j in range(i + 1, N)
    )
    determinant = -1 if inversions & 1 else 1
    for sign in signs:
        determinant *= sign

    sums = []
    for distance in range(1, N_HALF + 1):
        total = 0
        for i in range(N):
            j = (i + distance) % N
            rii = signs[i] if permutation[i] == i else 0
            rjj = signs[j] if permutation[j] == j else 0
            rij = signs[i] if permutation[i] == j else 0
            rji = signs[j] if permutation[j] == i else 0
            total += rii * rjj - rij * rji
        sums.append(total)
    return determinant, sums


def self_test():
    rng = random.Random(20261125)
    checked = 0
    for parts in range(1, 8):
        for _ in range(100):
            cuts = sorted(rng.sample(range(1, N), parts - 1)) if parts > 1 else []
            previous = 0
            lengths = []
            for cut in cuts:
                lengths.append(cut - previous)
                previous = cut
            lengths.append(N - previous)
            lengths = tuple(lengths)
            determinant, direct = direct_signed_permutation(lengths)
            if determinant != 1:
                raise AssertionError(f"SO(42) determinant failed for {lengths}: {determinant}")
            if direct != mirror_moment_sums(lengths):
                raise AssertionError(f"closed-form moment formula mismatch for {lengths}")
            checked += 1
    return checked


def enumerate_segment_count(parts):
    minimum = None
    maximum = None
    minimum_example = None
    maximum_example = None
    minimum_attainers = 0
    distinct = set()
    nonpositive = 0
    count = 0

    for lengths in compositions(N, parts):
        numerator = exact_slack_numerator(lengths)
        count += 1
        distinct.add(numerator)
        if minimum is None or numerator < minimum:
            minimum = numerator
            minimum_example = lengths
            minimum_attainers = 1
        elif numerator == minimum:
            minimum_attainers += 1
        if maximum is None or numerator > maximum:
            maximum = numerator
            maximum_example = lengths
        if numerator <= 0:
            nonpositive += 1

    result = {
        "segment_count": parts,
        "composition_count": count,
        "minimum_slack": str(Fraction(minimum, COMMON_DENOMINATOR)),
        "minimum_slack_attainers": minimum_attainers,
        "minimum_example": list(minimum_example),
        "maximum_slack": str(Fraction(maximum, COMMON_DENOMINATOR)),
        "maximum_example": list(maximum_example),
        "distinct_exact_slacks": len(distinct),
        "nonpositive_count": nonpositive,
    }
    expected_count, expected_min, expected_attainers, expected_max, expected_distinct = EXPECTED[parts]
    if count != comb(N - 1, parts - 1) or count != expected_count:
        raise AssertionError(f"composition count mismatch for k={parts}: {count}")
    if result["minimum_slack"] != expected_min:
        raise AssertionError(f"minimum slack mismatch for k={parts}: {result}")
    if minimum_attainers != expected_attainers:
        raise AssertionError(f"minimum-attainer count mismatch for k={parts}: {result}")
    if result["maximum_slack"] != expected_max:
        raise AssertionError(f"maximum slack mismatch for k={parts}: {result}")
    if len(distinct) != expected_distinct or nonpositive:
        raise AssertionError(f"slack census mismatch for k={parts}: {result}")
    return result


def build_evidence():
    if sum(abs(value) for value in DUAL_NUMERATOR) != DUAL_DENOMINATOR:
        raise AssertionError("dual does not have exact l1 norm one")
    checked = self_test()
    per_count = [enumerate_segment_count(parts) for parts in SEGMENT_COUNTS]
    total = sum(item["composition_count"] for item in per_count)
    overall_minimum = min(Fraction(item["minimum_slack"]) for item in per_count)
    if total != 5358536 or overall_minimum != Fraction(2, 40467):
        raise AssertionError("global segment-family census changed")

    two_segment_counterexample = exact_slack_numerator((1, 41))
    if Fraction(two_segment_counterexample, COMMON_DENOMINATOR) != Fraction(-80, 40467):
        raise AssertionError("the stated two-segment scope counterexample changed")

    return {
        "status": "exact_rational_three_to_seven_mirror_segment_obstruction",
        "n": 21,
        "site_count": N,
        "segment_counts": list(SEGMENT_COUNTS),
        "total_compositions": total,
        "dual_numerator": list(DUAL_NUMERATOR),
        "dual_denominator": DUAL_DENOMINATOR,
        "dual_l1_norm": "1",
        "target_moments": [
            str(Fraction((-1) ** (distance + 1), 41))
            for distance in range(1, N_HALF + 1)
        ],
        "common_slack_denominator": COMMON_DENOMINATOR,
        "overall_minimum_slack": str(overall_minimum),
        "overall_minimum_slack_attainers": sum(
            item["minimum_slack_attainers"]
            for item in per_count
            if Fraction(item["minimum_slack"]) == overall_minimum
        ),
        "program_mass_tv_lower_bound": "1/40467",
        "per_segment_count": per_count,
        "two_segment_scope_counterexample": {
            "composition": [1, 41],
            "same_dual_slack": str(Fraction(two_segment_counterexample, COMMON_DENOMINATOR)),
        },
        "independent_direct_matrix_crosschecks": checked,
        "arithmetic": "integer exact during exhaustive scan; fractions.Fraction only for reduced output; no floating point",
        "scope": (
            "all ordered compositions of 42 into k=3,4,5,6,7 positive contiguous "
            "perfect-mirror blocks; convex mixtures, dihedral images, and vertex-sign "
            "gauges. This is not a theorem for arbitrary couplings or k>=8."
        ),
    }


def main():
    parser = ArgumentParser()
    parser.add_argument("--output", help="write deterministic JSON evidence to this path")
    args = parser.parse_args()
    evidence = build_evidence()
    payload = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
    else:
        sys.stdout.write(payload)


if __name__ == "__main__":
    main()
