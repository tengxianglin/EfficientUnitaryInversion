"""Exact parity obstruction for perfect-matching atoms of a cycle exponential."""
from __future__ import annotations

import json
from fractions import Fraction
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/cycle_matching_atom_parity_obstruction_n42.json"


def odd_double_factorial(n: int) -> int:
    if n < 0 or n % 2 == 0:
        raise ValueError("n must be a nonnegative odd integer")
    out = 1
    for value in range(1, n + 1, 2):
        out *= value
    return out


def enumerate_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in enumerate_matchings(rest):
            yield ((first, second),) + tail


def is_bipartite_matching(matching) -> bool:
    return all((left - right) % 2 != 0 for left, right in matching)


def audit_small_sizes():
    rows = []
    for n in range(2, 6):
        N = 2 * n
        matchings = list(enumerate_matchings(tuple(range(N))))
        total = len(matchings)
        bipartite = sum(is_bipartite_matching(m) for m in matchings)
        expected_total = odd_double_factorial(N - 1)
        expected_bipartite = factorial(n)
        if total != expected_total or bipartite != expected_bipartite:
            raise AssertionError(f"small-N count mismatch at N={N}")
        rows.append(
            {
                "N": N,
                "total_perfect_matchings": total,
                "bipartite_matchings": bipartite,
                "same_parity_pair_matchings": total - bipartite,
                "exact_bipartite_fraction": str(Fraction(bipartite, total)),
                "theorem_applies": N % 4 == 2,
            }
        )
    return rows


def audit_n4_counterexample_modulus():
    # N=4 is not in the N == 2 (mod 4) theorem. The antipodal matching
    # M={(0,2),(1,3)} is physically reachable with A=(pi/2)K below.
    K = [
        [0, 1, 0, 1],
        [-1, 0, 1, 0],
        [0, -1, 0, -1],
        [-1, 0, 1, 0],
    ]
    P = [[0] * 4 for _ in range(4)]
    for left, right in ((0, 2), (1, 3)):
        P[left][right] = 1
        P[right][left] = 1
    D = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]
    R = [[sum(P[i][k] * D[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

    def matmul(left, right):
        return [
            [sum(left[i][k] * right[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)
        ]

    K2 = matmul(K, K)
    K3 = matmul(K2, K)
    I_plus_half_K2 = [
        [int(i == j) + K2[i][j] // 2 for j in range(4)] for i in range(4)
    ]
    if any(K[i][j] != -K[j][i] for i in range(4) for j in range(4)):
        raise AssertionError("N=4 K is not skew-symmetric")
    if K3 != [[-4 * K[i][j] for j in range(4)] for i in range(4)]:
        raise AssertionError("N=4 K^3=-4K identity failed")
    if I_plus_half_K2 != R:
        raise AssertionError("N=4 exponential polynomial does not equal P_M D")
    # Since K^3=-4K, exp((pi/2)K)=I+K^2/2 exactly by functional calculus.
    return {
        "N": 4,
        "matching": [[0, 2], [1, 3]],
        "couplings": ["pi/4", "pi/4", "-pi/4", "-pi/4"],
        "generator": "A=(pi/2)K",
        "exact_identity": "K^T=-K, K^3=-4K, exp((pi/2)K)=I+K^2/2=P_M D",
        "purpose": "Shows the N=4m+2 hypothesis cannot be dropped: N=4 admits a same-parity reachable matching atom.",
    }


def main():
    n = 21
    N = 2 * n
    total = odd_double_factorial(N - 1)
    bipartite = factorial(n)
    unreachable = total - bipartite
    reachable_fraction_upper = Fraction(bipartite, total)
    unreachable_fraction_lower = Fraction(unreachable, total)

    if N % 4 != 2:
        raise AssertionError("the EUI dimension must be 2 modulo 4")
    if total != 13113070457687988603440625:
        raise AssertionError("unexpected 41!!")
    if bipartite != 51090942171709440000:
        raise AssertionError("unexpected 21!")
    if reachable_fraction_upper != Fraction(262144, 67282234305):
        raise AssertionError("unexpected reduced reachable fraction")
    if unreachable_fraction_lower != Fraction(67281972161, 67282234305):
        raise AssertionError("unexpected reduced unreachable fraction")

    result = {
        "status": "exact_cycle_matching_atom_parity_obstruction_N42",
        "complete": True,
        "N": N,
        "modulus_condition": "N=4m+2",
        "theorem": (
            "For N=4m+2, if a signed perfect-matching matrix R_M=P_M D is exp(A) "
            "for a real skew-symmetric A supported on the N-cycle, then every edge "
            "of M joins opposite cycle bipartition classes."
        ),
        "proof_lemmas": [
            "A commutes with exp(A)=R_M, so conjugation by the signed permutation R_M preserves the nonzero-edge support graph of A.",
            "Because A is block diagonal over connected components of its support graph, exp(A) is too; the matching permutation therefore preserves each component.",
            "Every nontrivial proper connected subgraph component of a cycle is a path. A fixed-point-free path automorphism is reversal of an even path, which pairs opposite bipartition classes.",
            "If the support graph is the full cycle, a fixed-point-free involutive dihedral automorphism is either an edge-axis reflection or the half-turn. Edge-axis reflections swap parity; for N=4m+2 the half-turn shift N/2 is odd and also swaps parity.",
            "An isolated vertex would be fixed by exp(A), contradicting that a perfect matching has no fixed points. Hence every matched pair lies in one of the path/cycle components above and is cross-parity."
        ],
        "total_perfect_matchings": total,
        "bipartite_perfect_matchings": bipartite,
        "same_parity_matchings_proved_unreachable": unreachable,
        "max_physical_fraction_of_uniform_matching_support": str(reachable_fraction_upper),
        "max_physical_fraction_decimal": float(reachable_fraction_upper),
        "minimum_unreachable_fraction": str(unreachable_fraction_lower),
        "minimum_unreachable_fraction_decimal": float(unreachable_fraction_lower),
        "minimum_unreachable_percentage": 100.0 * float(unreachable_fraction_lower),
        "small_N_exhaustive_counts": audit_small_sizes(),
        "modulus_counterexample": audit_n4_counterexample_modulus(),
        "scope": (
            "This excludes every same-parity perfect-matching atom at N=42 and bounds "
            "the physically reachable fraction of the uniform perfect-matching support. "
            "It does not exclude a different positive measure on physical cycle exponentials "
            "with the same complete moments, and it does not classify all cross-parity atoms."
        ),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(encoded)
    print(json.dumps({
        "status": result["status"],
        "total": total,
        "bipartite": bipartite,
        "same_parity_unreachable": unreachable,
        "max_physical_fraction": str(reachable_fraction_upper),
        "minimum_unreachable_fraction": str(unreachable_fraction_lower),
        "small_N": result["small_N_exhaustive_counts"],
        "N4_counterexample": result["modulus_counterexample"],
        "output": str(OUTPUT),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
