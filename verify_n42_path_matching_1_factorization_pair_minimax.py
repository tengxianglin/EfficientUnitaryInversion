#!/usr/bin/env python3
"""Exact N=42 path-perfect-transfer 1-factorization and pair-minimax audit.

No third-party dependencies. All combinatorial counts and divergences are
recomputed with integers and fractions.
"""
from collections import Counter
from fractions import Fraction
from math import comb, gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/n42_path_matching_1_factorization_pair_minimax.json"
N = 42
n = 21
TARGET_PAIR = Fraction(-1, 41)


def matching(t):
    """2t-translate of the path reversal i <-> 41-i."""
    shift = 2 * t
    return tuple(sorted(
        tuple(sorted(((i + shift) % N, (41 - i + shift) % N)))
        for i in range(n)
    ))


def is_cycle_edge(edge):
    a, b = edge
    return (a - b) % N in (1, N - 1)


def component_count(first, second):
    """Components of the union of two perfect matchings."""
    adjacency = [set() for _ in range(N)]
    for a, b in first + second:
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen = set()
    components = 0
    for start in range(N):
        if start in seen:
            continue
        components += 1
        stack = [start]
        seen.add(start)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return components


def verify():
    matchings = [matching(t) for t in range(n)]
    if len(set(matchings)) != n:
        raise AssertionError("the 21 translated matchings are not distinct")

    edge_counts = Counter()
    cycle_edge_counts = []
    for M in matchings:
        vertices = [v for edge in M for v in edge]
        if sorted(vertices) != list(range(N)):
            raise AssertionError("a translated object is not a perfect matching")
        if any((a % 2) == (b % 2) for a, b in M):
            raise AssertionError("a matching edge does not cross the bipartition")
        edge_counts.update(M)
        cycle_edge_counts.append(sum(is_cycle_edge(edge) for edge in M))

    cross_edges = {
        tuple(sorted((a, b)))
        for a in range(0, N, 2) for b in range(1, N, 2)
    }
    if set(edge_counts) != cross_edges or set(edge_counts.values()) != {1}:
        raise AssertionError("the 21 matchings do not form a 1-factorization of K21,21")
    if cycle_edge_counts != [2] * n:
        raise AssertionError("each path-transfer matching must contain exactly two cycle edges")

    component_histogram = Counter()
    overlap_numerator = 0
    for t in range(n):
        for s in range(n):
            components = component_count(matchings[t], matchings[s])
            expected = gcd(n, (t - s) % n)
            if components != expected:
                raise AssertionError(
                    f"union component count mismatch for ({t},{s}): "
                    f"{components} != {expected}"
                )
            component_histogram[str(components)] += 1
            overlap_numerator += 2 ** components

    gcd_sum = sum(2 ** gcd(n, r) for r in range(n))
    if overlap_numerator != n * gcd_sum:
        raise AssertionError("ordered-pair overlap sum mismatch")
    mean_common_transversals = Fraction(gcd_sum, n)
    if mean_common_transversals != 99880:
        raise AssertionError("unexpected exact overlap average")

    d = comb(N, n)
    sum_q_squared = mean_common_transversals / (2 ** N)
    chi_square = d * sum_q_squared - 1
    frame_potential = 4 * sum_q_squared
    support_upper = n * (2 ** n)
    tv_lower = 1 - Fraction(support_upper, d)

    same_parity_pairs = 2 * comb(n, 2)
    cross_parity_pairs = n * n
    same_residual = Fraction(1, 41)
    cross_residual = Fraction(1, 41) - Fraction(1, 21)
    pair_residual_norm_squared = (
        same_parity_pairs * same_residual ** 2
        + cross_parity_pairs * cross_residual ** 2
    )
    if pair_residual_norm_squared != Fraction(20, 41):
        raise AssertionError("pair residual norm does not equal 20/41")

    # mu_0=1, mu_2=-1/41, mu_4=1/533; lambda_2=mu_0-2mu_2+mu_4.
    lambda_2 = Fraction(560, 533)
    pair_chi_square_bound = pair_residual_norm_squared / lambda_2
    if pair_chi_square_bound != Fraction(13, 28):
        raise AssertionError("pair-harmonic chi-square bound mismatch")

    expected_chi = Fraction(839949975821189, 68719476736)
    expected_fp = Fraction(12485, 137438953472)
    expected_tv = Fraction(22425576427, 22427411435)
    if chi_square != expected_chi:
        raise AssertionError(f"full chi-square mismatch: {chi_square}")
    if frame_potential != expected_fp:
        raise AssertionError(f"frame-potential mismatch: {frame_potential}")
    if tv_lower != expected_tv:
        raise AssertionError(f"support TV bound mismatch: {tv_lower}")
    if chi_square <= pair_chi_square_bound:
        raise AssertionError("full chi-square must dominate its pair projection bound")

    result = {
        "schema": "eui_n42_path_matching_1_factorization_pair_minimax_v1",
        "status": "exact_pair_minimax_and_full_divergence_certified",
        "N": N,
        "n": n,
        "physical_atom": {
            "base_matching": "i <-> 41-i, i=0,...,20",
            "path_couplings": "c_j=(pi/4)*sqrt((j+1)*(41-j)) for j=0,...,40; c_41=0",
            "path_transfer_identity": "R e_j=(-1)^j e_(41-j), hence Q=R D is the unsigned reversal permutation",
            "translated_atoms": "M_t={(i+2t,41-i+2t) mod 42 : i=0,...,20}, t=0,...,20",
            "zero_coupling_edges": "one translated closing edge per atom; all other couplings are strictly positive",
            "literature": "Christandl, Datta, Ekert, Landahl, Phys. Rev. Lett. 92, 187902 (2004), DOI 10.1103/PhysRevLett.92.187902"
        },
        "factorization": {
            "matching_count": len(matchings),
            "distinct": len(set(matchings)),
            "cross_bipartite_edges": len(cross_edges),
            "each_cross_edge_occurs_exactly_once": True,
            "same_parity_edges": 0,
            "cycle_edges_per_matching": cycle_edge_counts,
            "union_component_histogram_ordered_pairs": dict(sorted(component_histogram.items(), key=lambda x: int(x[0]))),
            "union_components_formula": "components(M_t union M_s)=gcd(21,t-s)"
        },
        "pair_moment_minimax": {
            "target_pair_moment_all_pairs": str(TARGET_PAIR),
            "same_parity_pair_count": same_parity_pairs,
            "cross_parity_pair_count": cross_parity_pairs,
            "mixture_cross_edge_marginals": "1/21",
            "mixture_same_parity_pair_moments": "0",
            "mixture_cross_parity_pair_moments": "-1/21",
            "same_parity_residual": str(same_residual),
            "cross_parity_residual": str(cross_residual),
            "minimum_squared_degree_two_residual_norm": str(pair_residual_norm_squared),
            "degree_two_balanced_slice_gram_eigenvalue": str(lambda_2),
            "universal_chi_square_lower_bound_for_any_bipartite_matching_mixture": str(pair_chi_square_bound),
            "attains_pair_level_minimax": True
        },
        "full_distribution": {
            "balanced_slice_size": d,
            "transversals_per_matching": 2 ** n,
            "support_size_upper_bound": support_upper,
            "support_tv_lower_bound": str(tv_lower),
            "support_tv_lower_bound_decimal": float(tv_lower),
            "mean_common_transversals_for_ordered_atom_pairs": str(mean_common_transversals),
            "sum_q_squared": str(sum_q_squared),
            "chi_square_exact": str(chi_square),
            "chi_square_decimal": float(chi_square),
            "frame_potential_exact": str(frame_potential),
            "frame_potential_decimal": float(frame_potential),
            "derivation": (
                "q_M is uniform on the 2^21 transversals of M. "
                "M_t union M_s has gcd(21,t-s) alternating cycles, hence "
                "2^gcd common transversals. Therefore sum_S q(S)^2="
                "2^-42*(1/21)*sum_r 2^gcd(21,r)=99880/2^42."
            )
        },
        "scope": (
            "The 21 path-transfer atoms are in the real-coupling cycle family "
            "when zero couplings are allowed. Their mixture is pair-level optimal "
            "among bipartite perfect-matching mixtures but is not the balanced-slice "
            "target: it has zero same-parity pair moments and -1/21 cross-parity "
            "pair moments, rather than -1/41 for every pair. The chi-square and TV "
            "bounds are for this explicit program-label law, not Choi or diamond distance. "
            "This does not settle the convex hull of non-permutation cycle exponentials."
        ),
        "complete": True
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    result = verify()
    print(json.dumps({
        "status": result["status"],
        "matching_count": result["factorization"]["matching_count"],
        "pair_chi_square_bound": result["pair_moment_minimax"]["universal_chi_square_lower_bound_for_any_bipartite_matching_mixture"],
        "full_chi_square": result["full_distribution"]["chi_square_exact"],
        "tv_lower": result["full_distribution"]["support_tv_lower_bound"],
        "output": str(OUTPUT.relative_to(ROOT))
    }, indent=2))
