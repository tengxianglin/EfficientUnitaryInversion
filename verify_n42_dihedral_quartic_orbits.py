#!/usr/bin/env python3
"""Exact bit-mask audit of C42 and D42 subset orbits for EUI."""
from collections import Counter
from itertools import combinations
from math import comb
import hashlib
import json
from pathlib import Path

N = 42
FULL = (1 << N) - 1
OUTPUT = Path(__file__).resolve().parent / "evidence/n42_dihedral_quartic_orbits.json"


def rotate(mask: int, shift: int) -> int:
    shift %= N
    if shift == 0:
        return mask
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def reflect(mask: int) -> int:
    """Reflection rho(i)=-i mod N."""
    out = mask & 1
    for i in range(1, N):
        if (mask >> i) & 1:
            out |= 1 << (N - i)
    return out


def cyclic_representative(mask: int) -> int:
    return min(rotate(mask, s) for s in range(N))


def dihedral_orbit(mask: int) -> set[int]:
    reflected = reflect(mask)
    return {rotate(mask, s) for s in range(N)} | {
        rotate(reflected, s) for s in range(N)
    }


def subset_mask(indices) -> int:
    value = 0
    for i in indices:
        value |= 1 << i
    return value


def audit_order(k: int) -> dict:
    covered = set()
    records = []
    size_hist = Counter()
    cyclic_merge_hist = Counter()
    for indices in combinations(range(N), k):
        mask = subset_mask(indices)
        if mask in covered:
            continue
        orbit = dihedral_orbit(mask)
        representative = min(orbit)
        if representative in covered:
            raise AssertionError("canonical representative already covered")
        if any(x.bit_count() != k for x in orbit):
            raise AssertionError("group action changed subset cardinality")
        if len(orbit) not in (21, 42, 84):
            raise AssertionError(f"unexpected D42 orbit size {len(orbit)}")
        if 84 % len(orbit):
            raise AssertionError("orbit-stabilizer divisibility failed")
        if any(x in covered for x in orbit):
            raise AssertionError("distinct dihedral orbits overlap")
        covered.update(orbit)
        size_hist[len(orbit)] += 1

        c0 = cyclic_representative(representative)
        c1 = cyclic_representative(reflect(representative))
        cyclic_count = 1 if c0 == c1 else 2
        cyclic_merge_hist[cyclic_count] += 1
        records.append({
            "representative": [i for i in range(N) if (representative >> i) & 1],
            "orbit_size": len(orbit),
            "cyclic_orbits_merged": cyclic_count,
        })

    expected = comb(N, k)
    if len(covered) != expected:
        raise AssertionError(f"coverage {len(covered)} != C(42,{k})={expected}")
    if sum(size * count for size, count in size_hist.items()) != expected:
        raise AssertionError("orbit-size sum does not cover all subsets")
    records.sort(key=lambda item: tuple(item["representative"]))
    representative_payload = [item["representative"] for item in records]
    representative_sha256 = hashlib.sha256(
        json.dumps(representative_payload, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "subset_size": k,
        "subset_count": expected,
        "dihedral_orbit_count": len(records),
        "dihedral_orbit_size_histogram": {
            str(size): size_hist[size] for size in sorted(size_hist)
        },
        "cyclic_orbit_count_reconstructed": sum(
            count * merged for merged, count in cyclic_merge_hist.items()
        ),
        "cyclic_orbits_per_dihedral_orbit_histogram": {
            str(count): cyclic_merge_hist[count]
            for count in sorted(cyclic_merge_hist)
        },
        "representative_sha256": representative_sha256,
    }


def verify() -> dict:
    pair = audit_order(2)
    quartic = audit_order(4)
    if pair["dihedral_orbit_count"] != 21:
        raise AssertionError("pair D42 orbit count changed")
    if pair["dihedral_orbit_size_histogram"] != {"21": 1, "42": 20}:
        raise AssertionError("pair D42 orbit-size histogram changed")
    if pair["cyclic_orbit_count_reconstructed"] != 21:
        raise AssertionError("pair cyclic-orbit reconstruction failed")
    if quartic["dihedral_orbit_count"] != 1440:
        raise AssertionError("quartic D42 orbit count changed")
    if quartic["dihedral_orbit_size_histogram"] != {
        "21": 10, "42": 200, "84": 1230
    }:
        raise AssertionError("quartic D42 orbit-size histogram changed")
    if quartic["cyclic_orbit_count_reconstructed"] != 2670:
        raise AssertionError("quartic cyclic-orbit reconstruction failed")
    if quartic["cyclic_orbits_per_dihedral_orbit_histogram"] != {
        "1": 210, "2": 1230
    }:
        raise AssertionError("unexpected reflection pairing of cyclic orbits")

    result = {
        "schema": "eui_n42_dihedral_quartic_orbits_v1",
        "status": "exact_D42_orbit_partition_verified",
        "N": N,
        "dihedral_group_order": 2 * N,
        "reflection": "i -> -i mod 42",
        "pair_orbits": pair,
        "quartic_orbits": {
            **quartic,
            "independent_orbit_coordinates_after_global_sum_rule":
                quartic["dihedral_orbit_count"] - 1,
            "reduction_from_cyclic_orbit_count":
                quartic["cyclic_orbit_count_reconstructed"]
                - quartic["dihedral_orbit_count"],
        },
        "scope": (
            "Exact combinatorial D42 orbit enumeration. The accompanying theorem "
            "proves that the even-principal-minor feature family is D42-equivariant "
            "for the real and strictly-positive cycle-coupling domains. This is a "
            "symmetry reduction, not a moment-feasibility certificate."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "pair_orbits": {
            "count": pair["dihedral_orbit_count"],
            "histogram": pair["dihedral_orbit_size_histogram"],
        },
        "quartic_orbits": {
            "count": quartic["dihedral_orbit_count"],
            "histogram": quartic["dihedral_orbit_size_histogram"],
            "cyclic_count": quartic["cyclic_orbit_count_reconstructed"],
            "cyclic_orbits_per_dihedral_orbit":
                quartic["cyclic_orbits_per_dihedral_orbit_histogram"],
            "independent_after_sum_rule":
                result["quartic_orbits"]["independent_orbit_coordinates_after_global_sum_rule"],
        },
    }, indent=2))
    return result


if __name__ == "__main__":
    verify()
