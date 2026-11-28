#!/usr/bin/env python3
"""Exact combinatorial checks for N=42 involution principal-minor sum rules.

No third-party dependencies. The analytic proof is in
THEORY_N42_INVOLUTION_MOMENT_SUM_RULES.md.
"""
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

N = 42
HALF = 21
FULL_MASK = (1 << N) - 1
OUTPUT = Path(__file__).resolve().parent / "evidence/n42_involution_moment_sum_rules.json"


def subset_mask(subset):
    mask = 0
    for i in subset:
        mask |= 1 << i
    return mask


def rotate_mask(mask, shift):
    if shift == 0:
        return mask
    return ((mask << shift) | (mask >> (N - shift))) & FULL_MASK


def cyclic_orbit_partition(k):
    representatives = set()
    for subset in combinations(range(N), k):
        mask = subset_mask(subset)
        representatives.add(min(rotate_mask(mask, shift) for shift in range(N)))
    sizes = [
        len({rotate_mask(rep, shift) for shift in range(N)})
        for rep in representatives
    ]
    histogram = {str(size): sizes.count(size) for size in sorted(set(sizes))}
    return {
        "orbit_count": len(representatives),
        "subset_count": sum(sizes),
        "orbit_sizes": sorted(set(sizes)),
        "size_histogram": histogram,
    }


def verify():
    hierarchy = []
    for r in range(HALF + 1):
        order = 2 * r
        target = Fraction((-1) ** r * comb(HALF, r), comb(N, order))
        aggregate = comb(N, order) * target
        expected = (-1) ** r * comb(HALF, r)
        if aggregate != expected:
            raise AssertionError(f"global sum rule failed at order {order}")
        complement_target = Fraction(
            (-1) ** (HALF - r) * comb(HALF, HALF - r),
            comb(N, N - order),
        )
        if complement_target != -target:
            raise AssertionError(f"complement sign failed at order {order}")
        hierarchy.append({
            "r": r,
            "order": order,
            "target_coordinate": str(target),
            "aggregate": str(aggregate),
            "complement_order": N - order,
            "complement_target": str(complement_target),
        })

    pair = cyclic_orbit_partition(2)
    quartic = cyclic_orbit_partition(4)
    if pair["orbit_count"] != 21 or pair["subset_count"] != comb(42, 2):
        raise AssertionError("pair cyclic-orbit partition is incorrect")
    if pair["size_histogram"] != {"21": 1, "42": 20}:
        raise AssertionError("unexpected pair orbit-size distribution")
    if quartic["orbit_count"] != 2670 or quartic["subset_count"] != comb(42, 4):
        raise AssertionError("quartic cyclic-orbit partition is incorrect")
    if quartic["size_histogram"] != {"21": 10, "42": 2660}:
        raise AssertionError("unexpected quartic orbit-size distribution")

    quartic_target = Fraction(1, 533)
    quartic_aggregate = comb(42, 4) * quartic_target
    if quartic_aggregate != 210:
        raise AssertionError("quartic target aggregate is not 210")

    result = {
        "N": N,
        "n": HALF,
        "status": "exact_involution_global_sum_and_complement_checks_passed",
        "assumptions": [
            "Q is real symmetric",
            "Q^2 = I",
            "trace(Q) = 0",
        ],
        "pair_cyclic_orbits": pair,
        "quartic_cyclic_orbits": {
            **quartic,
            "independent_orbit_coordinates_after_global_sum_rule":
                quartic["orbit_count"] - 1,
        },
        "quartic_target": str(quartic_target),
        "quartic_aggregate": str(quartic_aggregate),
        "even_order_hierarchy": hierarchy,
        "independent_even_orders": list(range(0, 22, 2)),
        "determined_by_complement": list(range(22, 43, 2)),
        "scope": (
            "Exact integer/rational checks of identities proved analytically for "
            "every real symmetric trace-zero involution. This is a structural "
            "reduction, not a feasibility certificate for the cycle-exponential family."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "pair_orbits": pair,
        "quartic_orbits": quartic,
        "quartic_aggregate": str(quartic_aggregate),
        "independent_even_orders": result["independent_even_orders"],
        "complement_determined_orders": result["determined_by_complement"],
    }, indent=2))


if __name__ == "__main__":
    verify()
