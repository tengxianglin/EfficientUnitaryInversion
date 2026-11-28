#!/usr/bin/env python3
"""Exact minimax divergence of bipartite matching-transversal mixtures.

Dependency-free: uses only Python integers, fractions, and itertools.
The theorem applies to every mixture of bipartite perfect-matching atoms,
therefore in particular to the subset reachable by the N=42 cycle exponential.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import permutations
from math import comb
import json


def q_uniform_bipartite(n, subset):
    """Probability of a fixed n-subset under the uniform matching mixture."""
    k = sum(1 for i in subset if i < n)
    return Fraction(1, (2 ** n) * comb(n, k))


def exact_divergences(n):
    c = comb(2 * n, n)
    chi = Fraction((n + 1) * c, 4 ** n) - 1
    q_orbit = [Fraction(comb(n, k), 2 ** n) for k in range(n + 1)]
    u_orbit = [Fraction(comb(n, k) ** 2, c) for k in range(n + 1)]
    tv = sum((a - b for a, b in zip(q_orbit, u_orbit) if a > b), Fraction(0))
    tv_direct = sum((abs(a - b) for a, b in zip(q_orbit, u_orbit)), Fraction(0)) / 2
    if tv != tv_direct:
        raise AssertionError("TV positive-part and absolute-value formulas disagree")
    return chi, tv, q_orbit, u_orbit


def enumerate_small_n(n):
    """Explicitly average every bipartite matching and all its transversals."""
    matchings = list(permutations(range(n)))
    q = defaultdict(Fraction)
    for pi in matchings:
        for mask in range(1 << n):
            subset = frozenset(
                i if ((mask >> i) & 1) else n + pi[i]
                for i in range(n)
            )
            q[subset] += Fraction(1, len(matchings) * (2 ** n))
    target = Fraction(1, comb(2 * n, n))
    expected = comb(2 * n, n)
    if len(q) != expected:
        raise AssertionError(f"n={n}: support has {len(q)} labels, expected {expected}")
    for subset, probability in q.items():
        formula = q_uniform_bipartite(n, subset)
        if probability != formula:
            raise AssertionError(f"n={n}: enumeration/formula mismatch at {sorted(subset)}")
    if sum(q.values(), Fraction(0)) != 1:
        raise AssertionError(f"n={n}: q does not normalize")
    chi_direct = sum((p * p / target for p in q.values()), Fraction(0)) - 1
    tv_direct = sum((abs(p - target) for p in q.values()), Fraction(0)) / 2
    chi_formula, tv_formula, _, _ = exact_divergences(n)
    if chi_direct != chi_formula or tv_direct != tv_formula:
        raise AssertionError(f"n={n}: exact divergence mismatch")
    return {
        "n": n,
        "matchings_enumerated": len(matchings),
        "transversal_pairs_enumerated": len(matchings) * (2 ** n),
        "balanced_labels": expected,
        "all_label_probabilities_match_closed_formula": True,
        "chi_square_exact": str(chi_direct),
        "tv_exact": str(tv_direct),
    }


def main():
    small = [enumerate_small_n(n) for n in range(1, 6)]
    n = 21
    c = comb(2 * n, n)
    chi, tv, q_orbit, u_orbit = exact_divergences(n)

    positive_k = [k for k in range(n + 1) if q_orbit[k] > u_orbit[k]]
    negative_k = [k for k in range(n + 1) if q_orbit[k] < u_orbit[k]]
    zero_k = [k for k in range(n + 1) if q_orbit[k] == u_orbit[k]]
    if positive_k != list(range(0, 9)) + list(range(13, 22)):
        raise AssertionError(f"unexpected positive TV orbits: {positive_k}")
    if negative_k != [9, 10, 11, 12] or zero_k:
        raise AssertionError("unexpected TV sign partition")

    expected_chi = Fraction(465226670411, 274877906944)
    expected_tv = Fraction(452040940614809, 2713482158407680)
    if chi != expected_chi or tv != expected_tv:
        raise AssertionError("N=42 exact divergence constants changed")
    if chi <= Fraction(13, 28):
        raise AssertionError("symmetrized chi-square floor should improve the pair-only bound")
    if tv <= Fraction(1, 5330):
        raise AssertionError("symmetrized TV floor should exceed the older finite-pool floor")

    result = {
        "schema": "eui_n42_bipartite_matching_convex_hull_minimax_v1",
        "status": "exact_bipartite_matching_mixture_minimax_certified",
        "N": 42,
        "n": n,
        "balanced_slice_size": c,
        "group": "S_21 x S_21 acting separately on even and odd vertices",
        "atom_law": "uniform on the 2^21 transversals of each bipartite perfect matching",
        "symmetrized_law": {
            "for_subset_with_k_even_vertices": "1/(2^21 * binom(21,k))",
            "orbit_mass_under_q": "binom(21,k)/2^21",
            "orbit_mass_under_uniform_target": "binom(21,k)^2/binom(42,21)",
            "ratio_q_over_target": "binom(42,21)/(2^21*binom(21,k))",
            "proof": "S_21 x S_21 is transitive on bipartite perfect matchings; averaging any matching mixture over the group gives the uniform matching mixture. Total variation and chi-square are convex and the target is group-invariant, so this symmetrization cannot increase either divergence."
        },
        "universal_minimax_over_all_bipartite_matching_mixtures": {
            "chi_square_exact": str(chi),
            "chi_square_decimal": float(chi),
            "chi_square_formula": "(22*binom(42,21)/2^42)-1",
            "tv_exact": str(tv),
            "tv_decimal": float(tv),
            "tv_positive_orbit_indices": positive_k,
            "tv_negative_orbit_indices": negative_k,
            "tv_zero_orbit_indices": zero_k,
            "tv_formula": "sum_{k: binom(21,k)<binom(42,21)/2^21} [binom(21,k)/2^21 - binom(21,k)^2/binom(42,21)]",
            "strictly_convex_chi_square_unique_minimizing_output_law": True,
            "attainment_in_full_bipartite_matching_hull": "uniform mixture over all 21! bipartite perfect matchings",
            "attainment_by_cycle_reachable_subset_not_claimed": True
        },
        "comparison": {
            "previous_pair_harmonic_chi_square_floor": "13/28",
            "new_chi_square_floor_is_stronger": True,
            "previous_finite_pool_tv_floor": "1/5330",
            "new_tv_floor_is_stronger": True,
            "scope": "All mixtures supported on bipartite matching atoms; by the N=42 cycle-matching reachability theorem this includes every mixture supported only on cycle-reachable perfect-matching atoms. It does not apply to non-permutation cycle exponentials."
        },
        "small_exact_exhaustive_cross_checks": small,
        "complete": True
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
