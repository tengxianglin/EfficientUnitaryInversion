#!/usr/bin/env python3
"""Exact all-order principal-minor incidence hierarchy and D_42 orbit audit.

No third-party dependencies. N=42 orbit counts use Burnside's lemma.
Small-N checks independently enumerate dihedral orbits, compute restricted
incidence ranks over Q, and test the determinant identity on rational
balanced-signature symmetric involutions.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations
from math import comb, gcd
import json
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "evidence" / "all_order_principal_minor_hierarchy_n42.json"


def burnside_dihedral_orbits(n: int, k: int) -> int:
    if n % 2:
        raise ValueError("even n required")
    rotations = 0
    for shift in range(n):
        d = gcd(n, shift)
        length = n // d
        if k % length == 0:
            rotations += comb(d, k // length)
    vertex_reflection = 0
    for j in range((n - 2) // 2 + 1):
        fixed = k - 2 * j
        if 0 <= fixed <= 2:
            vertex_reflection += comb((n - 2) // 2, j) * comb(2, fixed)
    edge_reflection = comb(n // 2, k // 2) if k % 2 == 0 else 0
    total = rotations + (n // 2) * (vertex_reflection + edge_reflection)
    assert total % (2 * n) == 0
    return total // (2 * n)


def transform(mask: int, n: int, shift: int, reflect: bool) -> int:
    out = 0
    for i in range(n):
        if (mask >> i) & 1:
            j = (shift - i) % n if reflect else (i + shift) % n
            out |= 1 << j
    return out


def canonical(mask: int, n: int) -> int:
    return min(transform(mask, n, s, r) for s in range(n) for r in (False, True))


def brute_orbits(n: int, k: int) -> int:
    unseen = {sum(1 << i for i in c) for c in combinations(range(n), k)}
    count = 0
    while unseen:
        rep = min(unseen)
        orbit = {transform(rep, n, s, r) for s in range(n) for r in (False, True)}
        unseen.difference_update(orbit)
        count += 1
    return count


def reps(n: int, k: int) -> list[int]:
    return sorted({canonical(sum(1 << i for i in c), n) for c in combinations(range(n), k)})


def rational_rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    rows, cols, rank = len(a), len(a[0]), 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [x / p for x in a[rank]]
        for i in range(rows):
            if i != rank and a[i][col]:
                f = a[i][col]
                a[i] = [a[i][j] - f * a[rank][j] for j in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def restricted_rank(n: int, s: int) -> tuple[int, int, int]:
    rr, cr = reps(n, s), reps(n, s + 1)
    ci = {m: j for j, m in enumerate(cr)}
    matrix = [[0] * len(cr) for _ in rr]
    for i, mask in enumerate(rr):
        for v in range(n):
            if not ((mask >> v) & 1):
                matrix[i][ci[canonical(mask | (1 << v), n)]] += 1
    return len(rr), len(cr), rational_rank(matrix)


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def det(a):
    if not a:
        return Fraction(1)
    w, n, sign, out = [row[:] for row in a], len(a), 1, Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if w[i][c]), None)
        if p is None:
            return Fraction(0)
        if p != c:
            w[c], w[p], sign = w[p], w[c], -sign
        x = w[c][c]
        out *= x
        for i in range(c + 1, n):
            if w[i][c]:
                f = w[i][c] / x
                for j in range(c + 1, n):
                    w[i][j] -= f * w[c][j]
                w[i][c] = Fraction(0)
    return sign * out


def rational_involution(n: int):
    h = n // 2
    o = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for p in range(h):
        i, j = p, h + ((3 * p + 1) % h)
        c, s = ((Fraction(3, 5), Fraction(4, 5)) if p % 2 == 0
                else (Fraction(4, 5), Fraction(3, 5)))
        for row in range(n):
            x, y = o[row][i], o[row][j]
            o[row][i], o[row][j] = c * x - s * y, s * x + c * y
    d = [1] * h + [-1] * h
    return mm([[o[i][j] * d[j] for j in range(n)] for i in range(n)], tr(o))


def verify_minor_identity(n: int) -> dict:
    q = rational_involution(n)
    assert q == tr(q)
    assert mm(q, q) == [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    assert sum(q[i][i] for i in range(n)) == 0
    minors = {}
    for k in range(0, n + 1, 2):
        for c in combinations(range(n), k):
            mask = sum(1 << i for i in c)
            minors[mask] = det([[q[i][j] for j in c] for i in c])
    checks = 0
    for s in range(1, n, 2):
        for c in combinations(range(n), s):
            mask = sum(1 << i for i in c)
            lhs = sum((minors[mask | (1 << v)] for v in range(n)
                       if not ((mask >> v) & 1)), Fraction(0))
            rhs = -sum((minors[mask ^ (1 << v)] for v in c), Fraction(0))
            assert lhs == rhs, (n, c, lhs, rhs)
            checks += 1
    return {"N": n, "even_principal_minors_computed": len(minors),
            "odd_subset_identities_checked": checks, "all_residuals_exactly_zero": True}


def target(n: int, order: int) -> Fraction:
    r = order // 2
    return Fraction((-1) ** r * comb(n // 2, r), comb(n, order))


def build():
    n = 42
    h = n // 2
    oc = {k: burnside_dihedral_orbits(n, k) for k in range(h + 1)}
    assert (oc[1], oc[2], oc[3], oc[4], oc[6], oc[8]) == (1, 21, 147, 1440, 63133, 1408185)
    for k in range(h + 1):
        assert oc[k] == burnside_dihedral_orbits(n, n - k)
    hierarchy = []
    for r in range(1, h // 2 + 1):
        m, s = 2 * r, 2 * r - 1
        assert (n - s) * target(n, m) == -s * target(n, m - 2)
        hierarchy.append({
            "even_order": m, "odd_subset_size": s,
            "odd_orbit_count": oc[s], "even_orbit_count": oc[m],
            "incidence_rank": oc[s],
            "remaining_even_orbit_coordinates": oc[m] - oc[s],
            "target_identity_exact": True
        })
    burnside_checks = []
    for small in (4, 6, 8, 10, 12):
        for k in range(small + 1):
            assert burnside_dihedral_orbits(small, k) == brute_orbits(small, k)
        burnside_checks.append(small)
    rank_checks = []
    for small in (4, 6, 8, 10, 12):
        for s in range(1, small // 2, 2):
            rows, cols, rank = restricted_rank(small, s)
            assert rank == rows
            rank_checks.append({"N": small, "s": s, "rows": rows,
                                "columns": cols, "rank": rank})
    minor_checks = [verify_minor_identity(small) for small in (4, 6, 8, 10)]
    variables = sum(x["even_orbit_count"] for x in hierarchy)
    relations = sum(x["incidence_rank"] for x in hierarchy)
    remaining = sum(x["remaining_even_orbit_coordinates"] for x in hierarchy)
    assert variables - relations == remaining
    return {
        "schema": "eui_all_order_principal_minor_hierarchy_n42_v1",
        "N": n, "n": h, "group": "dihedral D_42", "group_order": 84,
        "orbit_counts_by_subset_size": {str(k): oc[k] for k in range(h + 1)},
        "hierarchy": hierarchy,
        "even_order_variables_2_to_20": variables,
        "independent_adjacent_incidence_relations": relations,
        "remaining_orbit_coordinates_after_adjacent_hierarchy": remaining,
        "small_exact_checks": {
            "burnside_vs_bruteforce_N": burnside_checks,
            "restricted_incidence_rank": rank_checks,
            "rational_balanced_involution_identities": minor_checks
        },
        "scope": (
            "Residual-coordinate count after only consecutive odd-to-even incidence "
            "identities and complementary-minor reduction. It is not a claim that all "
            "remaining coordinates are algebraically independent or that no further "
            "physical/algebraic constraints exist."
        ),
        "status": "exact_combinatorial_hierarchy_and_orbit_count"
    }


if __name__ == "__main__":
    result = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
