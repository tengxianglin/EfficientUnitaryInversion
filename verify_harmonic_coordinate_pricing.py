#!/usr/bin/env python3
"""Exact small-N regression for local harmonic-coordinate pricing.

The script uses only the Python standard library. It verifies the harmonic
projection coefficients, the compact local-minor identity, and the target
centering/variance formulas on rational symmetric involutions.
"""
from fractions import Fraction
from itertools import combinations
from math import comb
import json


def det_fraction(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    n = len(a)
    if n == 0:
        return Fraction(1)
    sign = 1
    value = Fraction(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        value *= p
        for i in range(k + 1, n):
            if a[i][k]:
                factor = a[i][k] / p
                for j in range(k + 1, n):
                    a[i][j] -= factor * a[k][j]
                a[i][k] = Fraction(0)
    return sign * value


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def rational_balanced_involution(N):
    """Build Q=O diag(+1^n,-1^n) O^T with rational orthogonal O."""
    n = N // 2
    o = [[Fraction(int(i == j)) for j in range(N)] for i in range(N)]
    c, s = Fraction(3, 5), Fraction(4, 5)
    for i in range(n):
        g = [[Fraction(int(r == col)) for col in range(N)]
             for r in range(N)]
        g[i][i] = c
        g[n + i][n + i] = c
        g[i][n + i] = -s
        g[n + i][i] = s
        o = matmul(o, g)
    d = [[Fraction(0) for _ in range(N)] for __ in range(N)]
    for i in range(N):
        d[i][i] = Fraction(1 if i < n else -1)
    q = matmul(matmul(o, d), transpose(o))
    identity = [[Fraction(int(i == j)) for j in range(N)]
                for i in range(N)]
    assert q == transpose(q)
    assert matmul(q, q) == identity
    assert sum(q[i][i] for i in range(N)) == 0
    return q


def projection_coefficients(N, m):
    assert N % 2 == 0 and m % 2 == 0 and 0 < m <= N // 2
    p_m = Fraction(N - 2 * m + 1, N - m + 1)
    return [
        p_m * Fraction((-1) ** (m - t), comb(N - m, m - t))
        for t in range(m + 1)
    ]


def pricing_coefficients(N, m):
    """Return Newton alpha_k and local-minor beta_|L| coefficients."""
    n = N // 2
    alpha = [
        Fraction((-1) ** k, comb(N - m + 1 - k, m - k))
        for k in range(m + 1)
    ]
    beta = {}
    for ell in range(0, m + 1, 2):
        total = Fraction(0)
        for k in range(ell, m + 1):
            j = m // 2 - k + ell // 2
            if 0 <= j <= n - k:
                total += (
                    alpha[k]
                    * comb(m - ell, k - ell)
                    * (-1) ** (m // 2 - ell // 2)
                    * comb(n - k, j)
                )
        beta[ell] = total
    return alpha, beta


def balanced_character_moment(N, order):
    if order == 0:
        return Fraction(1)
    value = Fraction(1)
    for j in range(1, order // 2 + 1):
        value *= Fraction(-(2 * j - 1), N - (2 * j - 1))
    return value


def direct_pricing(q, N, m, S):
    p = projection_coefficients(N, m)
    total = Fraction(0)
    S = set(S)
    for J in combinations(range(N), m):
        t = len(S.intersection(J))
        sub = [[q[i][j] for j in J] for i in J]
        total += p[t] * det_fraction(sub)
    return total


def compact_pricing(q, N, m, S):
    _, beta = pricing_coefficients(N, m)
    total = Fraction(0)
    for ell, coefficient in beta.items():
        for L in combinations(S, ell):
            sub = [[q[i][j] for j in L] for i in L]
            total += coefficient * det_fraction(sub)
    return total


def verify_case(N, m):
    q = rational_balanced_involution(N)
    p = projection_coefficients(N, m)
    alpha, beta = pricing_coefficients(N, m)
    n = N // 2
    probes = [tuple(range(m)), tuple(range(0, 2 * m, 2))]
    if N >= 10 and m >= 4:
        probes.append(tuple([0, 1] + list(range(N - (m - 2), N))))

    for S in probes:
        direct = direct_pricing(q, N, m, S)
        compact = compact_pricing(q, N, m, S)
        assert direct == compact, (N, m, S, direct, compact)

    # Verify every down relation through the intersection-count recurrence.
    for K in combinations(range(N), m - 1):
        t = len(set(K).intersection(probes[0]))
        down = ((m - t) * p[t + 1]
                + (N - 2 * m + 1 + t) * p[t])
        assert down == 0

    # The projected coordinate vector has squared norm equal to its diagonal.
    norm2 = sum(
        p[len(set(J).intersection(probes[0]))] ** 2
        for J in combinations(range(N), m)
    )
    assert norm2 == p[m]

    target_mean = sum(
        beta[ell] * comb(m, ell) * balanced_character_moment(N, ell)
        for ell in beta
    )
    assert target_mean == 0

    lam = Fraction(
        4 ** m * comb(N - 2 * m, n - m),
        comb(N, n),
    )
    variance = lam * p[m]
    return {
        "N": N,
        "m": m,
        "probes_checked": len(probes),
        "projection_diagonal_and_norm_squared": str(p[m]),
        "alpha": [str(x) for x in alpha],
        "beta": {str(k): str(v) for k, v in beta.items()},
        "uniform_target_mean": str(target_mean),
        "harmonic_gram_eigenvalue": str(lam),
        "witness_variance": str(variance),
    }


def main():
    results = [
        verify_case(8, 4),
        verify_case(10, 2),
        verify_case(10, 4),
    ]

    alpha42, beta42 = pricing_coefficients(42, 6)
    target42 = sum(
        beta42[ell] * comb(6, ell) * balanced_character_moment(42, ell)
        for ell in beta42
    )
    assert beta42 == {
        0: Fraction(1, 2849),
        2: Fraction(1, 385),
        4: Fraction(1, 33),
        6: Fraction(1),
    }
    assert target42 == 0
    lam42 = Fraction(4 ** 6 * comb(30, 15), comb(42, 21))
    variance42 = lam42 * Fraction(31, 37)
    assert lam42 == Fraction(7938048, 6724861)
    assert variance42 == Fraction(7938048, 8026447)
    results.append({
        "N": 42,
        "m": 6,
        "beta": {str(k): str(v) for k, v in beta42.items()},
        "uniform_target_mean": str(target42),
        "harmonic_gram_eigenvalue": str(lam42),
        "projection_diagonal_and_norm_squared": "31/37",
        "witness_variance": str(variance42),
        "chi_square_multiplier": str(1 / variance42),
        "note": (
            "N=42 coefficient and target identities checked exactly; "
            "the full C(42,6) direct sum is not enumerated here."
        ),
    })

    print(json.dumps({
        "status": "exact_local_harmonic_pricing_checks_passed",
        "cases": results,
    }, indent=2))


if __name__ == "__main__":
    main()
