"""Exact cycle-edge count distribution for uniform perfect matchings.

For N=4m+2 >= 6, the physical-matching reachability theorem proves that
every matching atom reachable as exp(A(c)) has at least two physical cycle
edges. This verifier quantifies the excluded mass in the uniform matching
representation using exact integer arithmetic.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/perfect_matching_cycle_edge_distribution_n42.json"
N_TARGET = 42


def odd_double_factorial(value: int) -> int:
    if value == -1:
        return 1
    if value < 1 or value % 2 == 0:
        raise ValueError(f"expected a positive odd integer or -1, got {value}")
    result = 1
    for term in range(value, 0, -2):
        result *= term
    return result


def cycle_k_matching_count(n: int, k: int) -> int:
    """Number of k-edge matchings in the labelled cycle C_n."""
    if not 0 <= k <= n // 2:
        raise ValueError("k must lie between 0 and floor(n/2)")
    if k == 0:
        return 1
    numerator = n * comb(n - k, k)
    denominator = n - k
    if numerator % denominator:
        raise AssertionError("cycle matching count is not integral")
    return numerator // denominator


def binomial_moments(n: int) -> list[int]:
    """B_k = sum_M binom(X(M), k), summed over all perfect matchings M."""
    return [
        cycle_k_matching_count(n, k)
        * odd_double_factorial(n - 2 * k - 1)
        for k in range(n // 2 + 1)
    ]


def exact_cycle_edge_distribution(n: int) -> list[int]:
    """Return C_j = # perfect matchings with exactly j cycle edges."""
    moments = binomial_moments(n)
    half = n // 2
    counts = [
        sum(
            (-1) ** (k - j) * comb(k, j) * moments[k]
            for k in range(j, half + 1)
        )
        for j in range(half + 1)
    ]
    if any(count < 0 for count in counts):
        raise AssertionError("negative exact-count coefficient")
    if sum(counts) != odd_double_factorial(n - 1):
        raise AssertionError("exact counts do not sum to (n-1)!!")
    for k, expected in enumerate(moments):
        recovered = sum(comb(j, k) * counts[j] for j in range(k, half + 1))
        if recovered != expected:
            raise AssertionError(f"binomial inversion failed at k={k}")
    return counts


def brute_force_cycle_edge_distribution(n: int) -> list[int]:
    """Independent recursive enumeration, used only for small n."""
    cycle_edges = {tuple(sorted((j, (j + 1) % n))) for j in range(n)}
    distribution: Counter[int] = Counter()

    def visit(remaining: tuple[int, ...], hits: int) -> None:
        if not remaining:
            distribution[hits] += 1
            return
        first = remaining[0]
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            edge = tuple(sorted((first, partner)))
            visit(rest, hits + int(edge in cycle_edges))

    visit(tuple(range(n)), 0)
    return [distribution[j] for j in range(n // 2 + 1)]


def factorial_moment(n: int, k: int) -> Fraction:
    total = odd_double_factorial(n - 1)
    numerator = (
        factorial(k)
        * cycle_k_matching_count(n, k)
        * odd_double_factorial(n - 2 * k - 1)
    )
    return Fraction(numerator, total)


def build_evidence() -> dict:
    small_checks = []
    for n in (4, 6, 8, 10, 12, 14):
        exact = exact_cycle_edge_distribution(n)
        brute = brute_force_cycle_edge_distribution(n)
        if exact != brute:
            raise AssertionError(f"exact formula disagrees with brute force at N={n}")
        small_checks.append(
            {
                "N": n,
                "counts_by_cycle_edge_count": [str(x) for x in exact],
                "total": str(sum(exact)),
                "brute_force_match": True,
            }
        )

    n = N_TARGET
    counts = exact_cycle_edge_distribution(n)
    total = odd_double_factorial(n - 1)
    zero_or_one = counts[0] + counts[1]
    excluded_mass = Fraction(zero_or_one, total)
    remaining_mass = 1 - excluded_mass

    moments = [
        {"k": k, "factorial_moment": str(factorial_moment(n, k))}
        for k in range(1, 7)
    ]

    return {
        "status": "exact_cycle_edge_count_distribution_for_uniform_perfect_matchings",
        "N": n,
        "cycle_edge_count_definition": (
            "X(M) is the number of edges of the fixed Hamiltonian cycle C_N "
            "that belong to the perfect matching M."
        ),
        "total_perfect_matchings": str(total),
        "counts_by_cycle_edge_count": [str(x) for x in counts],
        "zero_cycle_edge_count": str(counts[0]),
        "one_cycle_edge_count": str(counts[1]),
        "zero_or_one_cycle_edge_count": str(zero_or_one),
        "uniform_mass_zero_or_one": str(excluded_mass),
        "uniform_mass_zero_or_one_decimal": format(float(excluded_mass), ".16g"),
        "upper_bound_on_uniform_mass_of_physically_reachable_matching_atoms": str(
            remaining_mass
        ),
        "tv_distance_lower_bound_from_uniform_matching_measure_to_any_measure_"
        "supported_on_reachable_matching_atoms": str(excluded_mass),
        "factorial_moments_N42": moments,
        "poisson_limit": (
            "For every fixed k, E[(X_N)_k] = k! m_k(C_N) "
            "(N-2k-1)!!/(N-1)!! tends to 1 as even N tends to infinity. "
            "The factorial-moment method gives X_N -> Poisson(1) in "
            "distribution, and P(X_N <= 1) -> 2/e."
        ),
        "poisson_limit_2_over_e_decimal": format(2 / __import__("math").e, ".16g"),
        "small_size_bruteforce_checks": small_checks,
        "scope": (
            "The total-variation statement concerns probability measures on "
            "the discrete perfect-matching atoms only. It does not bound arbitrary "
            "cycle-exponential ensembles and is not a Choi- or diamond-distance bound."
        ),
    }


def main() -> None:
    evidence = build_evidence()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": evidence["status"],
                "N": evidence["N"],
                "total_perfect_matchings": evidence["total_perfect_matchings"],
                "zero_cycle_edge_count": evidence["zero_cycle_edge_count"],
                "one_cycle_edge_count": evidence["one_cycle_edge_count"],
                "uniform_mass_zero_or_one": evidence["uniform_mass_zero_or_one"],
                "small_size_bruteforce_checks": [
                    row["N"] for row in evidence["small_size_bruteforce_checks"]
                ],
                "output": str(OUTPUT.relative_to(ROOT)),
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
