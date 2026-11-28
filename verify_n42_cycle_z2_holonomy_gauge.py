#!/usr/bin/env python3
"""Exact gauge-orbit audit for the N=42 cycle EUI feature family.

The proof is algebraic in the accompanying theory note. This verifier exhausts
all signed/zero edge patterns for N=4,6,8,10 and performs deterministic N=42
normal-form and D42-invariance smoke checks.
"""
from collections import defaultdict
from itertools import product
import hashlib
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/n42_cycle_z2_holonomy_gauge.json"
SMALL_SIZES = (4, 6, 8, 10)
N42_SAMPLES = 4096
N42_SEED = 20261128


def gauge_transform(signs, eps):
    n = len(signs)
    return tuple(signs[j] * eps[j] * eps[(j + 1) % n] for j in range(n))


def canonicalize_signs(signs):
    """Return canonical edge signs, Z2 holonomy, and a vertex gauge."""
    n = len(signs)
    eps = [None] * n

    if all(s != 0 for s in signs):
        eps[0] = 1
        for j in range(n - 1):
            eps[j + 1] = eps[j] * signs[j]
        canonical = gauge_transform(signs, eps)
        holonomy = math.prod(signs)
        if canonical[:-1] != (1,) * (n - 1) or canonical[-1] != holonomy:
            raise AssertionError("full-cycle canonical form failed")
        return canonical, holonomy, tuple(eps)

    # Removing at least one zero edge turns the support graph into a forest.
    adjacency = [[] for _ in range(n)]
    for j, sign in enumerate(signs):
        if sign:
            k = (j + 1) % n
            adjacency[j].append((k, sign))
            adjacency[k].append((j, sign))

    for root in range(n):
        if eps[root] is not None:
            continue
        eps[root] = 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, sign in adjacency[vertex]:
                if eps[neighbor] is None:
                    eps[neighbor] = eps[vertex] * sign
                    stack.append(neighbor)
                elif eps[vertex] * eps[neighbor] * sign != 1:
                    raise AssertionError("unexpected cycle in a proper subgraph")

    canonical = gauge_transform(signs, eps)
    if any(sign not in (0, 1) for sign in canonical):
        raise AssertionError("forest gauge did not make every live edge positive")
    return canonical, 0, tuple(eps)


def rotate_signs(signs, shift):
    n = len(signs)
    return tuple(signs[(j - shift) % n] for j in range(n))


def reflect_signs(signs):
    n = len(signs)
    return tuple(signs[(-j - 1) % n] for j in range(n))


def support_mask(signs):
    return sum((sign != 0) << j for j, sign in enumerate(signs))


def rotate_mask(mask, n, shift):
    return sum(((mask >> ((j - shift) % n)) & 1) << j for j in range(n))


def reflect_mask(mask, n):
    return sum(((mask >> ((-j - 1) % n)) & 1) << j for j in range(n))


def dihedral_support_key(mask, n):
    reflected = reflect_mask(mask, n)
    return min(
        [rotate_mask(mask, n, shift) for shift in range(n)]
        + [rotate_mask(reflected, n, shift) for shift in range(n)]
    )


def audit_small_size(n):
    full = (1 << n) - 1
    support_keys = [dihedral_support_key(mask, n) for mask in range(1 << n)]
    representatives_by_support = [set() for _ in range(1 << n)]
    combined_keys = set()
    pattern_count = 0

    for signs in product((-1, 0, 1), repeat=n):
        pattern_count += 1
        canonical, holonomy, eps = canonicalize_signs(signs)
        support = support_mask(signs)
        if support_mask(canonical) != support:
            raise AssertionError("gauge changed the support")
        if gauge_transform(signs, eps) != canonical:
            raise AssertionError("stored gauge does not produce canonical form")
        expected_holonomy = math.prod(signs) if support == full else 0
        if holonomy != expected_holonomy:
            raise AssertionError("wrong Z2 holonomy")

        representatives_by_support[support].add(canonical)
        key = (support_keys[support], holonomy)
        combined_keys.add(key)

        for shift in range(n):
            moved = rotate_signs(signs, shift)
            moved_support = support_mask(moved)
            moved_holonomy = math.prod(moved) if moved_support == full else 0
            if (support_keys[moved_support], moved_holonomy) != key:
                raise AssertionError("rotation changed the gauge/dihedral key")

        moved = reflect_signs(signs)
        moved_support = support_mask(moved)
        moved_holonomy = math.prod(moved) if moved_support == full else 0
        if (support_keys[moved_support], moved_holonomy) != key:
            raise AssertionError("reflection changed the gauge/dihedral key")

    total_gauge_orbits = 0
    for support, representatives in enumerate(representatives_by_support):
        expected = 2 if support == full else 1
        if len(representatives) != expected:
            raise AssertionError(
                f"N={n}, support={support}: {len(representatives)} "
                f"gauge orbits, expected {expected}"
            )
        total_gauge_orbits += len(representatives)

    key_payload = repr(sorted(combined_keys)).encode("ascii")
    return {
        "N": n,
        "signed_zero_edge_patterns_exhausted": pattern_count,
        "support_masks": 1 << n,
        "gauge_orbits_over_all_patterns": total_gauge_orbits,
        "nonfull_supports_with_one_gauge_orbit": (1 << n) - 1,
        "full_support_gauge_orbits": len(representatives_by_support[full]),
        "combined_gauge_dihedral_orbits": len(combined_keys),
        "combined_key_sha256": hashlib.sha256(key_payload).hexdigest(),
    }


def audit_n42_smoke():
    n = 42
    rng = random.Random(N42_SEED)
    support_key_cache = {}
    for _ in range(N42_SAMPLES):
        signs = tuple(rng.choice((-1, 0, 1)) for _ in range(n))
        canonical, holonomy, eps = canonicalize_signs(signs)
        if gauge_transform(signs, eps) != canonical:
            raise AssertionError("N=42 canonical gauge reconstruction failed")

        eps2 = tuple(rng.choice((-1, 1)) for _ in range(n))
        regauged = gauge_transform(signs, eps2)
        canonical2, holonomy2, _ = canonicalize_signs(regauged)
        if (canonical2, holonomy2) != (canonical, holonomy):
            raise AssertionError("N=42 vertex-gauge invariance failed")

        support = support_mask(signs)
        if support not in support_key_cache:
            support_key_cache[support] = dihedral_support_key(support, n)
        key = (support_key_cache[support], holonomy)

        for shift in (0, 1, 7, 21, 41):
            moved = rotate_signs(signs, shift)
            moved_support = support_mask(moved)
            if moved_support not in support_key_cache:
                support_key_cache[moved_support] = dihedral_support_key(moved_support, n)
            _, moved_holonomy, _ = canonicalize_signs(moved)
            if (support_key_cache[moved_support], moved_holonomy) != key:
                raise AssertionError("N=42 rotation invariance failed")

        moved = reflect_signs(signs)
        moved_support = support_mask(moved)
        if moved_support not in support_key_cache:
            support_key_cache[moved_support] = dihedral_support_key(moved_support, n)
        _, moved_holonomy, _ = canonicalize_signs(moved)
        if (support_key_cache[moved_support], moved_holonomy) != key:
            raise AssertionError("N=42 reflection invariance failed")

    return {
        "N": n,
        "deterministic_random_patterns": N42_SAMPLES,
        "seed": N42_SEED,
        "distinct_support_masks_cached": len(support_key_cache),
        "result": "passed",
        "scope": "smoke test only; the all-N statement is proved algebraically",
    }


def verify():
    small = [audit_small_size(n) for n in (4, 6, 8, 10)]
    expected_patterns = {4: 81, 6: 729, 8: 6561, 10: 59049}
    expected_dihedral = {4: 7, 6: 14, 8: 31, 10: 79}
    for item in small:
        n = item["N"]
        if item["signed_zero_edge_patterns_exhausted"] != expected_patterns[n]:
            raise AssertionError("exhaustive pattern count changed")
        if item["gauge_orbits_over_all_patterns"] != (1 << n) + 1:
            raise AssertionError("gauge orbit count should be 2^N+1")
        if item["combined_gauge_dihedral_orbits"] != expected_dihedral[n]:
            raise AssertionError("combined gauge/dihedral count changed")

    result = {
        "schema": "eui_n42_cycle_z2_holonomy_gauge_v1",
        "status": "exact_small_cycle_gauge_classification_verified",
        "target_N": 42,
        "gauge_action": "c_j -> epsilon_j epsilon_(j+1) c_j",
        "holonomy": "product_j sign(c_j), defined only when every edge is nonzero",
        "canonical_full_support": "(|c_0|,...,|c_40|, holonomy*|c_41|)",
        "canonical_proper_support": "(|c_0|,...,|c_41|), retaining zero entries",
        "small_cycle_exhaustive_audits": small,
        "n42_deterministic_smoke": audit_n42_smoke(),
        "theorem_scope": (
            "Vertex-sign gauge preserves every principal minor, at every order. "
            "For a proper edge support the support graph is a forest and all signs "
            "are gauge-removable. For full cycle support there are exactly two "
            "gauge classes, distinguished by Z2 holonomy. D42 preserves the "
            "holonomy and acts on the support/magnitude pattern."
        ),
        "closed_convex_hull_reduction": (
            "The real-coupling feature family has the same closed convex hull as "
            "the union of the strictly-positive sector and the sector with the "
            "first N-1 couplings positive and the final coupling negative. "
            "Zero-edge canonical representatives lie in the closure of the "
            "strictly-positive sector by continuity."
        ),
        "limitations": (
            "The verifier is an exact finite sign-pattern audit for N<=10 plus "
            "a deterministic N=42 smoke test. The all-N gauge classification "
            "and closed-convex-hull reduction follow from the algebraic proof, "
            "not from extrapolation of these finite checks."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "small_cycles": [
            {
                "N": x["N"],
                "patterns": x["signed_zero_edge_patterns_exhausted"],
                "gauge_orbits": x["gauge_orbits_over_all_patterns"],
                "gauge_D42_orbits": x["combined_gauge_dihedral_orbits"],
            }
            for x in small
        ],
        "n42_smoke": result["n42_deterministic_smoke"],
    }, indent=2))
    return result


if __name__ == "__main__":
    verify()
