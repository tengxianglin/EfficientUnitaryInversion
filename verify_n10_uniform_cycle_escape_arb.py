#!/usr/bin/env python3
"""256-bit Arb pricing of the N=10 block-mirror separator on a connected cycle."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx, fmpq

N = 10
COUPLING = Fraction(409, 100)
DUAL_TERMS = (
    ((0, 1), Fraction(3, 35)),
    ((0, 2), Fraction(3, 35)),
    ((0, 1, 2, 3, 4, 5), Fraction(11, 35)),
    ((0, 1, 2, 4, 5, 6), Fraction(8, 35)),
    ((0, 1, 2, 3, 4, 7), Fraction(3, 35)),
    ((0, 1, 2, 5, 6, 7), Fraction(3, 70)),
    ((0, 1, 2, 3, 5, 6, 7, 8), Fraction(11, 70)),
)


def fq(value: Fraction) -> fmpq:
    value = Fraction(value)
    return fmpq(value.numerator, value.denominator)


def dihedral_orbit(subset: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    orbit = set()
    for shift in range(N):
        for reflection in (False, True):
            if reflection:
                image = tuple(sorted((shift - i) % N for i in subset))
            else:
                image = tuple(sorted((i + shift) % N for i in subset))
            orbit.add(image)
    return tuple(sorted(orbit))


def build_uniform_cycle() -> tuple[arb_mat, arb_mat]:
    c = arb(fq(COUPLING))
    generator = arb_mat(N, N)
    for j in range(N):
        generator[j, (j + 1) % N] = 2 * c
        generator[(j + 1) % N, j] = -2 * c
    rotation = generator.exp()
    d = [(-1) ** j for j in range(N)]
    q = arb_mat(N, N)
    for i in range(N):
        for j in range(N):
            q[i, j] = rotation[i, j] * d[j]
    return rotation, q


def check_zero(ball: arb, label: str) -> None:
    if not ball.contains(0):
        raise AssertionError(f"{label} interval excludes zero: {ball}")


def main() -> dict:
    ctx.prec = 256
    rotation, q = build_uniform_cycle()

    orthogonality = rotation.transpose() * rotation
    involution = q * q
    for i in range(N):
        for j in range(N):
            check_zero(orthogonality[i, j] - (1 if i == j else 0), "R^T R-I")
            check_zero(q[i, j] - q[j, i], "Q symmetry")
            check_zero(involution[i, j] - (1 if i == j else 0), "Q^2-I")
    trace_q = sum((q[i, i] for i in range(N)), arb(0))
    check_zero(trace_q, "tr(Q)")
    det_r = rotation.det()
    if not det_r.contains(1):
        raise AssertionError(f"det(R) does not enclose one: {det_r}")

    score = arb(0)
    orbit_records = []
    for representative, coefficient in DUAL_TERMS:
        orbit = dihedral_orbit(representative)
        subtotal = arb(0)
        for subset in orbit:
            principal = arb_mat(
                [[q[i, j] for j in subset] for i in subset]
            ).det()
            subtotal += principal
        average = subtotal / len(orbit)
        score += arb(fq(coefficient)) * average
        orbit_records.append({
            "representative": list(representative),
            "orbit_size": len(orbit),
            "average_interval": str(average),
        })

    block_ceiling = arb(fq(Fraction(-2, 35)))
    target_score = arb(fq(Fraction(-74, 2205)))
    if not score > block_ceiling:
        raise AssertionError(
            f"connected physical cycle did not escape block separator: score={score}"
        )
    if not score > target_score:
        raise AssertionError(
            f"connected physical score is not above target score: score={score}"
        )

    result = {
        "status": "arb_certified_connected_cycle_escape_from_N10_block_separator",
        "precision_bits": ctx.prec,
        "coupling_all_edges": f"{COUPLING.numerator}/{COUPLING.denominator}",
        "det_R_interval": str(det_r),
        "trace_Q_interval": str(trace_q),
        "block_family_score_ceiling": "-2/35",
        "target_score": "-74/2205",
        "connected_cycle_score_interval": str(score),
        "strictly_above_block_ceiling": True,
        "strictly_above_target_score": True,
        "orbit_scores": orbit_records,
        "scope": (
            "This certifies that the N=10 block-reversal separator is not a "
            "global separator for the full connected cycle-exponential family. "
            "It does not establish target convex-hull feasibility."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
