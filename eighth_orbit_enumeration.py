"""Exact dihedral orbit enumeration for even-cardinality subsets of even cycles.

A k-subset is represented by its positive cyclic gap tuple, modulo rotations
and reversal.  The first gap is fixed to the minimum gap, and tasks are
partitioned by the first three gaps.  This avoids materializing all C(N-1,k-1)
anchored subsets in one global Python set.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import comb, gcd
import json


def weak_compositions(total, parts):
    """Yield weak compositions in lexicographic order."""
    if parts < 1:
        raise ValueError("parts must be positive")
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first,) + tail


def task_specs(N, k):
    """Partition canonical gap tuples by (minimum gap, second excess, third excess)."""
    if N % 2 or k % 2 or not (4 <= k <= N):
        raise ValueError("require even N and even 4 <= k <= N")
    for minimum in range(1, N // k + 1):
        slack = N - k * minimum
        for h1 in range(slack + 1):
            for h2 in range(slack - h1 + 1):
                yield (minimum, h1, h2)


def is_dihedral_canonical(gaps):
    """Whether a cyclic gap tuple is lexicographically minimal under D_k."""
    g = tuple(gaps)
    k = len(g)
    minimum = g[0]
    # Every rotation beginning with a value larger than the minimum is
    # lexicographically larger than g, so only minimum-starting rotations matter.
    for seq in (g, g[::-1]):
        for shift, value in enumerate(seq):
            if value == minimum:
                candidate = seq[shift:] + seq[:shift]
                if candidate < g:
                    return False
    return True


def task_keys(N, k, spec):
    """Yield exactly the canonical gap keys assigned to one task."""
    minimum, h1, h2 = spec
    slack = N - k * minimum - h1 - h2
    if slack < 0:
        return
    for tail in weak_compositions(slack, k - 3):
        gaps = (minimum, minimum + h1, minimum + h2)
        gaps += tuple(minimum + x for x in tail)
        if is_dihedral_canonical(gaps):
            yield gaps


def representative_from_gaps(gaps):
    out = []
    position = 0
    for gap in gaps:
        out.append(position)
        position += gap
    if position != sum(gaps):
        raise AssertionError("gap tuple does not close")
    return tuple(out)


def orbit_size_from_gaps(gaps, N):
    g = tuple(gaps)
    k = len(g)
    reverse = g[::-1]
    stabilizer = sum(g == g[s:] + g[:s] for s in range(k))
    stabilizer += sum(reverse == g[s:] + g[:s] for s in range(k))
    if (2 * N) % stabilizer:
        raise AssertionError("nonintegral dihedral orbit size")
    return (2 * N) // stabilizer


def burnside_even(N, k):
    """Burnside count for k-subsets of Z_N under D_N, N and k even."""
    if N % 2 or k % 2 or not (0 <= k <= N):
        raise ValueError("require even N and even 0 <= k <= N")
    rotation_fixed = 0
    for shift in range(N):
        cycles = gcd(N, shift)
        cycle_length = N // cycles
        if k % cycle_length == 0:
            rotation_fixed += comb(cycles, k // cycle_length)

    vertex_fixed = 0
    for fixed_vertices in range(3):
        remaining = k - fixed_vertices
        if remaining >= 0 and remaining % 2 == 0:
            pairs = remaining // 2
            if pairs <= (N - 2) // 2:
                vertex_fixed += comb(2, fixed_vertices) * comb((N - 2) // 2, pairs)

    edge_fixed = comb(N // 2, k // 2)
    reflection_fixed = (N // 2) * (vertex_fixed + edge_fixed)
    numerator = rotation_fixed + reflection_fixed
    if numerator % (2 * N):
        raise AssertionError("Burnside numerator is not divisible by |D_N|")
    return {
        "rotation_fixed_sum": rotation_fixed,
        "vertex_reflection_fixed": vertex_fixed,
        "edge_reflection_fixed": edge_fixed,
        "reflection_fixed_sum": reflection_fixed,
        "orbit_count": numerator // (2 * N),
    }


def hash_keys(keys):
    h = sha256()
    h.update(b"[")
    first = True
    for key in keys:
        if not first:
            h.update(b",")
        h.update(json.dumps(list(key), separators=(",", ":")).encode())
        first = False
    h.update(b"]")
    return h.hexdigest()


def enumeration_summary(N=42, k=8):
    """Enumerate canonical keys, task hashes, orbit sizes and exact coverage."""
    records = []
    histogram = Counter()
    global_hash = sha256()
    global_hash.update(b"[")
    global_first = True
    orbit_count = 0
    set_count = 0
    nonempty = 0

    specs = list(task_specs(N, k))
    for task_id, spec in enumerate(specs):
        keys = list(task_keys(N, k, spec))
        task_sets = 0
        for key in keys:
            size = orbit_size_from_gaps(key, N)
            histogram[size] += 1
            task_sets += size
            if not global_first:
                global_hash.update(b",")
            global_hash.update(json.dumps(list(key), separators=(",", ":")).encode())
            global_first = False
        records.append({
            "task_id": task_id,
            "task": list(spec),
            "orbits": len(keys),
            "eight_sets": task_sets,
            "key_sha256": hash_keys(keys),
        })
        orbit_count += len(keys)
        set_count += task_sets
        nonempty += bool(keys)

    global_hash.update(b"]")
    burnside = burnside_even(N, k)
    raw_candidates = sum(
        comb(N - k * minimum + k - 2, k - 2)
        for minimum in range(1, N // k + 1)
    )
    expected_sets = comb(N, k)
    if orbit_count != burnside["orbit_count"] or set_count != expected_sets:
        raise AssertionError("canonical gap enumeration disagrees with Burnside/coverage")

    summary = {
        "N": N,
        "k": k,
        "raw_weak_composition_candidates": raw_candidates,
        "task_count": len(specs),
        "nonempty_tasks": nonempty,
        "canonical_orbits": orbit_count,
        "orbit_size_histogram": {str(s): histogram[s] for s in sorted(histogram)},
        "orbit_size_sum": set_count,
        "all_k_subsets": expected_sets,
        "burnside": burnside,
        "canonical_key_sha256": global_hash.hexdigest(),
        "enumeration_complete": True,
    }
    return summary, records
