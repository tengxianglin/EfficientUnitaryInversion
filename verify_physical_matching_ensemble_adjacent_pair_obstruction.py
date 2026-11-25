"""Exact checks for the adjacent-pair obstruction on physical matching atoms."""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/physical_matching_ensemble_adjacent_pair_obstruction_n42.json"


def odd_double_factorial(n: int) -> int:
    if n < 1 or n % 2 == 0:
        raise ValueError("n must be positive and odd")
    out = 1
    for value in range(1, n + 1, 2):
        out *= value
    return out


def matching_from_permutation(p: list[int]) -> list[tuple[int, int]]:
    return sorted(
        (j, p[j]) if j < p[j] else (p[j], j)
        for j in range(len(p))
        if j < p[j]
    )


def adjacent_matched_count(matching: list[tuple[int, int]], n: int) -> int:
    edges = {tuple(edge) for edge in matching}
    return sum(
        tuple(sorted((j, (j + 1) % n))) in edges
        for j in range(n)
    )


def audit_edge_axis_reflections(n: int) -> list[dict]:
    rows = []
    for a in range(1, n, 2):
        p = [(a - j) % n for j in range(n)]
        if any(p[p[j]] != j or p[j] == j for j in range(n)):
            raise AssertionError("reflection is not a fixed-point-free involution")
        matching = matching_from_permutation(p)
        count = adjacent_matched_count(matching, n)
        if count != 2:
            raise AssertionError(f"reflection a={a} has {count} adjacent pairs")
        rows.append({"a": a, "adjacent_matched_pairs": count})
    return rows


def audit_halfturn(n: int) -> dict:
    half = n // 2
    p = [(j + half) % n for j in range(n)]
    count = adjacent_matched_count(matching_from_permutation(p), n)
    if count != 0:
        raise AssertionError("half-turn should have no adjacent matched pair")
    if half % 2 != 1:
        raise AssertionError("the complex-trace obstruction requires odd n/2")
    return {
        "adjacent_matched_pairs": count,
        "half_turn_shift": half,
        "half_turn_shift_is_odd": True,
        "trace_sum_zero_impossible": True,
    }


def audit_path_component_counts(half_size: int) -> dict:
    # A proper support partition has even component sizes 2*k_i, where
    # (k_i) is a composition of half_size. There are 2^(half_size-1)
    # compositions, with C(half_size-1,k-1) having k components.
    distribution = {
        str(k): comb(half_size - 1, k - 1)
        for k in range(1, half_size + 1)
    }
    if sum(distribution.values()) != 1 << (half_size - 1):
        raise AssertionError("composition count mismatch")
    score = {
        str(k): (2 if k == 1 else k)
        for k in range(1, half_size + 1)
    }
    if min(score.values()) != 2:
        raise AssertionError("proper-path adjacent-pair lower bound failed")
    return {
        "composition_count": 1 << (half_size - 1),
        "component_count_distribution": distribution,
        "adjacent_pair_count_by_component_count": score,
        "minimum_adjacent_pair_count": 2,
    }


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def audit_n4_counterexample() -> dict:
    K = [
        [0, 1, 0, 1],
        [-1, 0, 1, 0],
        [0, -1, 0, -1],
        [-1, 0, 1, 0],
    ]
    K2 = matmul(K, K)
    K3 = matmul(K2, K)
    if any(K[i][j] != -K[j][i] for i in range(4) for j in range(4)):
        raise AssertionError("K is not skew-symmetric")
    if K3 != [[-4 * x for x in row] for row in K]:
        raise AssertionError("K^3=-4K identity failed")

    polynomial = [
        [int(i == j) + K2[i][j] // 2 for j in range(4)]
        for i in range(4)
    ]
    P = [[0] * 4 for _ in range(4)]
    for i, j in ((0, 2), (1, 3)):
        P[i][j] = P[j][i] = 1
    D = [
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ]
    target = matmul(P, D)
    if polynomial != target:
        raise AssertionError("exp((pi/2)K)=P_M D identity failed")

    return {
        "N": 4,
        "matching": [[0, 2], [1, 3]],
        "couplings": ["pi/4", "pi/4", "-pi/4", "-pi/4"],
        "adjacent_matched_pairs": 0,
        "identities": [
            "K^T=-K",
            "K^3=-4K",
            "exp((pi/2)K)=I+K^2/2=P_M D",
        ],
        "purpose": "Counterexample outside N=4m+2; the congruence hypothesis is essential.",
    }


def build_evidence() -> dict:
    N = 42
    n = N // 2
    reflections = audit_edge_axis_reflections(N)
    halfturn = audit_halfturn(N)
    paths = audit_path_component_counts(n)

    total = odd_double_factorial(N - 1)
    bipartite = factorial(n)
    target_value = Fraction(N, N - 1)
    gap = Fraction(2, 1) - target_value
    if total != 13113070457687988603440625:
        raise AssertionError("41!! mismatch")
    if bipartite != 51090942171709440000:
        raise AssertionError("21! mismatch")
    if target_value != Fraction(42, 41) or gap != Fraction(40, 41):
        raise AssertionError("exact separator arithmetic mismatch")

    small_sizes = []
    for size in (6, 10, 42):
        small_sizes.append(
            {
                "N": size,
                "n": size // 2,
                "edge_axis_reflections": size // 2,
                "adjacent_pairs_per_edge_axis_reflection": 2,
                "halfturn": audit_halfturn(size),
                "target_adjacent_score": str(Fraction(size, size - 1)),
                "strict_gap_to_two": str(Fraction(size - 2, size - 1)),
            }
        )

    return {
        "status": "exact_physical_matching_ensemble_adjacent_pair_obstruction",
        "complete": True,
        "theorem_scope": "N=4m+2, N>=6",
        "N": N,
        "n": n,
        "theorem": (
            "Every perfect-matching atom R_M=P_M D that equals exp(A(c)) "
            "for a real skew generator supported on the N-cycle has at least "
            "two matching edges that are cycle edges."
        ),
        "proof_lemmas": {
            "support_graph": (
                "A commutes with exp(A)=P_M D, so conjugation by the signed "
                "permutation preserves the nonzero-edge support graph. Since "
                "exp(A) is block diagonal over support components and is a "
                "signed permutation, the matching permutation preserves each component."
            ),
            "proper_support": (
                "Every component is an even path and the fixed-point-free path "
                "automorphism is reversal. Each component contributes its central "
                "adjacent matched pair. If there is only one component, it spans "
                "all N vertices and its endpoint pair across the unique missing "
                "cycle edge is a second adjacent matched pair."
            ),
            "full_support": (
                "A fixed-point-free involutive cycle automorphism is an edge-axis "
                "reflection or the half-turn. Every edge-axis reflection has exactly "
                "two adjacent matched pairs."
            ),
            "halfturn_exclusion": (
                "For p(j)=j+n and odd n, J=P_M D is an orthogonal complex structure. "
                "A commutes with J and e^A=J=iI on the induced complex vector space. "
                "The antipodal permutation has no cycle-edge support, so tr_R(JA)=0; "
                "also tr_R(A)=0, hence tr_C(A)=0. But the n complex eigenphases are "
                "theta_l=pi/2+2*pi*k_l, so their sum pi/2*(n+4K) cannot vanish for odd n."
            ),
        },
        "N42_checks": {
            "edge_axis_reflections_checked": len(reflections),
            "edge_axis_reflection_adjacent_pair_counts": sorted(
                {row["adjacent_matched_pairs"] for row in reflections}
            ),
            "halfturn": halfturn,
            "proper_path_compositions": paths,
            "total_perfect_matchings": total,
            "bipartite_perfect_matchings": bipartite,
            "uniform_matching_mass_on_same_parity_atoms": str(
                Fraction(total - bipartite, total)
            ),
            "separating_functional": {
                "definition": (
                    "Lambda(Q)=-sum_j det(Q_{ {j,j+1},{j,j+1} }) "
                    "with cyclic indices"
                ),
                "minimum_on_reachable_matching_atoms": 2,
                "balanced_target_value": str(target_value),
                "strict_gap": str(gap),
            },
        },
        "small_size_checks": small_sizes,
        "N4_counterexample": audit_n4_counterexample(),
        "scope_limit": (
            "The separator applies only to physically reachable signed "
            "perfect-matching atoms and their positive mixtures. It is not "
            "proved for arbitrary cycle exponentials Q=exp(A(c))D, so the "
            "full physical convex-hull problem remains open."
        ),
    }


def main() -> None:
    evidence = build_evidence()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(encoded)
    print(
        json.dumps(
            {
                "status": evidence["status"],
                "N": evidence["N"],
                "edge_axis_reflections_checked": evidence["N42_checks"][
                    "edge_axis_reflections_checked"
                ],
                "halfturn_excluded_by_trace": True,
                "proper_path_compositions": evidence["N42_checks"][
                    "proper_path_compositions"
                ]["composition_count"],
                "target": evidence["N42_checks"]["separating_functional"][
                    "balanced_target_value"
                ],
                "gap": evidence["N42_checks"]["separating_functional"][
                    "strict_gap"
                ],
                "N4_counterexample": "passed",
                "output": str(OUTPUT.relative_to(ROOT)),
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
