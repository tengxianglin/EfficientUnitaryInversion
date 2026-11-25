"""Exact structural audit of perfect-matching atoms in the 42-cycle family."""
from __future__ import annotations
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from verify_perfect_matching_atom_cycle_unreachability import (
    commutator_matrix, enumerate_matchings, exact_rank,
)
ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence/cycle_matching_atom_reachability_n21.json"
N, HALF = 42, 21

def partner_map(matching, size):
    p = [-1] * size
    for a, b in matching:
        if p[a] != -1 or p[b] != -1:
            raise AssertionError("repeated matching vertex")
        p[a], p[b] = b, a
    if any(x < 0 for x in p):
        raise AssertionError("incomplete matching")
    return p

def image_edge(p, edge):
    size = len(p)
    x, y = p[edge], p[(edge + 1) % size]
    if (y - x) % size == 1:
        return x
    if (x - y) % size == 1:
        return y
    return None

def orbit_nullity(matching, size):
    p = partner_map(matching, size)
    good = {i for i in range(size) if image_edge(p, i) is not None}
    unseen, count = set(good), 0
    while unseen:
        i = min(unseen)
        j = image_edge(p, i)
        if j is None or j not in good or image_edge(p, j) != i:
            raise AssertionError("good-edge map is not an involution")
        unseen.discard(i)
        unseen.discard(j)
        count += 1
    return count

def exact_commutant_audit(n):
    size, hist, count = 2 * n, {}, 0
    for matching in enumerate_matchings(list(range(size))):
        matrix, _ = commutator_matrix(n, matching)
        nullity = size - exact_rank(matrix)
        if nullity != orbit_nullity(matching, size):
            raise AssertionError(f"N={size}: exact commutant nullity mismatch")
        hist[str(nullity)] = hist.get(str(nullity), 0) + 1
        count += 1
    return {"N":size,"matching_count":count,"commutant_nullity_histogram":hist,
            "all_exact_ranks_match_edge_orbit_formula":True,"exact_matchings_checked":count}

def matching_from_cuts(size, cuts):
    cuts = tuple(sorted(cuts))
    pairs = []
    for k, left in enumerate(cuts):
        right = cuts[(k + 1) % len(cuts)]
        length = (right - left) % size or size
        if length % 2:
            raise AssertionError("cut gaps must be even")
        vertices = [(left + q) % size for q in range(1, length + 1)]
        for q in range(length // 2):
            pairs.append(tuple(sorted((vertices[q], vertices[length - 1 - q]))))
    return tuple(sorted(pairs))

def cut_audit(n):
    size, checked, unique = 2 * n, 0, set()
    for parity in (0, 1):
        edges = list(range(parity, size, 2))
        for mask in range(1, 1 << n):
            cuts = tuple(edges[q] for q in range(n) if (mask >> q) & 1)
            matching = matching_from_cuts(size, cuts)
            p = partner_map(matching, size)
            if any((i - p[i]) % 2 == 0 for i in range(size)):
                raise AssertionError("segment mirror failed to exchange parity")
            unique.add(matching)
            checked += 1
    return {"N":size,"nonempty_same_parity_cut_sets_checked":checked,
            "distinct_segment_mirror_matchings":len(unique),
            "all_segment_mirror_matchings_are_bipartite":True,
            "formula_cut_set_count":2*((1 << n)-1)}

def full_cycle_audit(n):
    if n % 2 == 0:
        raise ValueError("requires odd n")
    size = 2 * n
    maps = [[(i+n) % size for i in range(size)]]
    maps += [[(axis-i) % size for i in range(size)] for axis in range(1,size,2)]
    for p in maps:
        if any(p[i] == i or p[p[i]] != i or (p[i]-i) % 2 == 0 for i in range(size)):
            raise AssertionError("invalid fixed-point-free parity-flipping dihedral map")
    return {"N":size,"fixed_point_free_involutive_dihedral_maps":len(maps),
            "expected_count":n+1,"all_are_bipartite_matchings":True}

def main():
    small_commutant = [exact_commutant_audit(n) for n in (2,3,4)]
    small_cuts = [cut_audit(n) for n in (2,3,4,5)]
    full_cycle = [full_cycle_audit(n) for n in (3,5,21)]
    total = 1
    for x in range(1,N,2):
        total *= x
    cut_count = 2*((1 << HALF)-1)
    dihedral_count = HALF+1
    upper = cut_count+dihedral_count
    upper_fraction = Fraction(upper,total)
    excluded_fraction = 1-upper_fraction
    with localcontext() as ctx:
        ctx.prec = 60
        upper_decimal = str(Decimal(upper_fraction.numerator)/Decimal(upper_fraction.denominator))
        excluded_decimal = str(Decimal(excluded_fraction.numerator)/Decimal(excluded_fraction.denominator))
    frozen = ((0,11),(1,38),(2,8),(3,13),(4,30),(5,25),(6,21),(7,14),
              (9,41),(10,36),(12,37),(15,18),(16,28),(17,40),(19,22),
              (20,27),(23,29),(24,31),(26,32),(33,35),(34,39))
    fp = partner_map(frozen,N)
    same_parity = [[i,fp[i]] for i in range(N) if i<fp[i] and (i-fp[i])%2==0]
    if not same_parity:
        raise AssertionError("frozen matching should be non-bipartite")
    result = {
        "status":"certified_cycle_matching_atom_structural_reachability_bound",
        "complete":True,"N":N,
        "generator":"A(c)[j,j+1]=2*c_j; A(c)[j+1,j]=-2*c_j, cyclic indices",
        "matching_atom":"R_M=P_M D, D[j,j]=(-1)^j",
        "theorem":"Every matching atom equal to exp(A(c)) is bipartite. With a nonempty zero-edge set, the cuts lie in one edge-parity class and f reverses each even path component. With all edges active, f is one of 21 edge-axis reflections or the half-turn.",
        "proper_support_cut_set_count":cut_count,
        "full_support_fixed_point_free_dihedral_count":dihedral_count,
        "reachable_matching_atom_count_upper_bound":upper,
        "total_perfect_matchings":str(total),
        "reachable_fraction_upper_bound_exact":f"{upper_fraction.numerator}/{upper_fraction.denominator}",
        "reachable_fraction_upper_bound_decimal":upper_decimal,
        "unreachable_uniform_matching_mass_lower_bound_exact":f"{excluded_fraction.numerator}/{excluded_fraction.denominator}",
        "unreachable_uniform_matching_mass_lower_bound_decimal":excluded_decimal,
        "same_parity_pair_target_in_Q_basis":"-1/41",
        "consequence":"No probability measure supported only on physically reachable matching atoms can reproduce the target: every such atom has zero same-parity 2x2 principal minors, while the target is -1/41.",
        "frozen_non_bipartite_matching_same_parity_pairs":same_parity,
        "small_exact_commutant_cross_checks":small_commutant,
        "small_cut_set_cross_checks":small_cuts,
        "full_cycle_dihedral_cross_checks":full_cycle,
        "scope":"This bounds the reachable atoms inside the perfect-matching signed-permutation ensemble only. It does not rule out a positive measure supported on non-permutation cycle exponentials."
    }
    if json.loads(EVIDENCE.read_text()) != result:
        raise AssertionError("committed evidence differs from exact recomputation")
    print(json.dumps({"status":result["status"],"reachable_matching_atom_count_upper_bound":upper,
        "total_perfect_matchings":str(total),
        "reachable_fraction_upper_bound_exact":result["reachable_fraction_upper_bound_exact"],
        "unreachable_uniform_matching_mass_lower_bound_exact":result["unreachable_uniform_matching_mass_lower_bound_exact"],
        "small_exact_commutant_cross_checks":small_commutant,
        "small_cut_set_cross_checks":small_cuts,"full_cycle_dihedral_cross_checks":full_cycle},indent=2))

if __name__ == "__main__":
    main()
