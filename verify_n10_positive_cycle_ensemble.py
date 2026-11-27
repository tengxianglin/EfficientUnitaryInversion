#!/usr/bin/env python3
"""Arb-certified exact-real positive cycle ensemble for the N=10 balanced slice.

The 13 positive weights are defined as the unique real solution of a 13x13
system consisting of four pair-orbit equations, eight independent quartic
orbit equations, and normalization. A nonzero Arb determinant and strictly
positive Arb weight intervals certify existence. Exact principal-minor
hierarchies then imply every even-order target equation.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from flint import arb, arb_mat, ctx, fmpq

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n10_positive_cycle_ensemble_atoms.json"
OUTPUT = ROOT / "evidence/n10_positive_cycle_ensemble_arb.json"
N = 10


def rational(value: Fraction | int | str) -> arb:
    q = Fraction(value)
    return arb(fmpq(q.numerator, q.denominator))


def dihedral_orbit(subset: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    orbit = set()
    for shift in range(N):
        orbit.add(tuple(sorted((i + shift) % N for i in subset)))
        orbit.add(tuple(sorted((shift - i) % N for i in subset)))
    return tuple(sorted(orbit))


def subset_orbits(size: int):
    groups: dict[tuple[int, ...], set[tuple[int, ...]]] = {}
    for subset in combinations(range(N), size):
        image = min(dihedral_orbit(subset))
        groups.setdefault(image, set()).add(subset)
    reps = tuple(sorted(groups))
    return reps, groups


def bareiss_determinant(matrix: list[list[int]]) -> int:
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next((r for r in range(k + 1, n) if a[r][k]), None)
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[n - 1][n - 1]


def incidence_matrices(pair_reps, pair_groups, quartic_reps, quartic_groups, triple_reps):
    pair_index = {
        subset: j for j, rep in enumerate(pair_reps) for subset in pair_groups[rep]
    }
    quartic_index = {
        subset: j for j, rep in enumerate(quartic_reps) for subset in quartic_groups[rep]
    }
    C = [[0 for _ in quartic_reps] for _ in triple_reps]
    D = [[0 for _ in pair_reps] for _ in triple_reps]
    for row, K in enumerate(triple_reps):
        Kset = set(K)
        for I in combinations(range(N), 4):
            if Kset.issubset(I):
                C[row][quartic_index[I]] += 1
        for J in combinations(K, 2):
            D[row][pair_index[J]] += 1
    return C, D


def check_zero(value: arb, label: str) -> None:
    if not value.contains(0):
        raise AssertionError(f"{label} interval excludes zero: {value}")


def principal_minor(q: arb_mat, subset: tuple[int, ...]) -> arb:
    return arb_mat([[q[i, j] for j in subset] for i in subset]).det()


def orbit_average(q: arb_mat, orbit: tuple[tuple[int, ...], ...]) -> arb:
    return sum((principal_minor(q, subset) for subset in orbit), arb(0)) / len(orbit)


def build_rotation(couplings: tuple[Fraction, ...]) -> arb_mat:
    generator = arb_mat(N, N)
    for j, coupling in enumerate(couplings):
        edge = 2 * rational(coupling)
        generator[j, (j + 1) % N] = edge
        generator[(j + 1) % N, j] = -edge
    return generator.exp()


def build_q(rotation: arb_mat) -> arb_mat:
    q = arb_mat(N, N)
    for i in range(N):
        for j in range(N):
            q[i, j] = rotation[i, j] * ((-1) ** j)
    return q


def verify_structural_identities(C, D, pair_reps, pair_groups, quartic_reps):
    if len(pair_reps) != 5 or len(quartic_reps) != 16:
        raise AssertionError("unexpected N=10 D10 orbit counts")
    if len(C) != 8 or any(len(row) != 16 for row in C):
        raise AssertionError("unexpected triple/quartic incidence shape")
    pivot_det = bareiss_determinant([row[:8] for row in C])
    if pivot_det != 64:
        raise AssertionError(f"unexpected exact pivot determinant: {pivot_det}")

    # The balanced target has p_d=-1/9 and q_o=1/21.
    # Every triple-incidence equation C q + D p = 0 must hold exactly.
    for row in range(8):
        lhs = sum((Fraction(C[row][j], 21) for j in range(16)), Fraction(0))
        rhs = sum((Fraction(D[row][j], 9) for j in range(5)), Fraction(0))
        if lhs != rhs:
            raise AssertionError("balanced target fails the exact triple incidence identity")

    pair_sizes = [len(pair_groups[rep]) for rep in pair_reps]
    if pair_sizes != [10, 10, 10, 10, 5]:
        raise AssertionError(f"unexpected pair orbit sizes: {pair_sizes}")
    if sum((Fraction(size) * Fraction(-1, 9) for size in pair_sizes), Fraction(0)) != -5:
        raise AssertionError("balanced pair target fails the e2(Q) identity")
    return pivot_det, pair_sizes


def main():
    ctx.prec = 512
    raw = INPUT.read_bytes()
    data = json.loads(raw)
    if data.get("schema") != "eui-n10-positive-cycle-ensemble-atoms-v1":
        raise AssertionError("unexpected frozen atom schema")
    atoms = tuple(tuple(Fraction(value) for value in row) for row in data["atoms"])
    if len(atoms) != 13 or any(len(row) != N for row in atoms):
        raise AssertionError("expected exactly thirteen ten-edge atoms")
    if not all(value > 0 for row in atoms for value in row):
        raise AssertionError("every frozen base coupling must be strictly positive")

    pair_reps, pair_groups = subset_orbits(2)
    quartic_reps, quartic_groups = subset_orbits(4)
    triple_reps, triple_groups = subset_orbits(3)
    all_even_orbits = sum(len(subset_orbits(k)[0]) for k in (0, 2, 4, 6, 8, 10))
    if all_even_orbits != 44:
        raise AssertionError(f"unexpected total even-subset D10 orbit count: {all_even_orbits}")
    if sum(map(len, pair_groups.values())) != 45:
        raise AssertionError("pair orbits do not partition all 45 pairs")
    if sum(map(len, quartic_groups.values())) != 210:
        raise AssertionError("quartic orbits do not partition all 210 quartets")
    if len(triple_reps) != 8:
        raise AssertionError("unexpected triple orbit count")

    C, D = incidence_matrices(
        pair_reps, pair_groups, quartic_reps, quartic_groups, triple_reps
    )
    pivot_det, pair_sizes = verify_structural_identities(
        C, D, pair_reps, pair_groups, quartic_reps
    )

    pair_orbits = [dihedral_orbit(rep) for rep in pair_reps]
    quartic_orbits = [dihedral_orbit(rep) for rep in quartic_reps]
    pair_columns = []
    quartic_columns = []
    atom_records = []
    for atom_index, couplings in enumerate(atoms):
        rotation = build_rotation(couplings)
        q = build_q(rotation)
        orthogonality = rotation.transpose() * rotation
        involution = q * q
        for i in range(N):
            for j in range(N):
                check_zero(
                    orthogonality[i, j] - (1 if i == j else 0),
                    f"atom {atom_index}: R^T R-I",
                )
                check_zero(q[i, j] - q[j, i], f"atom {atom_index}: Q symmetry")
                check_zero(
                    involution[i, j] - (1 if i == j else 0),
                    f"atom {atom_index}: Q^2-I",
                )
        trace_q = sum((q[i, i] for i in range(N)), arb(0))
        check_zero(trace_q, f"atom {atom_index}: trace(Q)")
        det_r = rotation.det()
        if not det_r.contains(1):
            raise AssertionError(f"atom {atom_index}: det(R) does not enclose one: {det_r}")
        det_q = q.det()
        if not det_q.contains(-1):
            raise AssertionError(f"atom {atom_index}: det(Q) does not enclose -1: {det_q}")

        pair_values = [orbit_average(q, orbit) for orbit in pair_orbits]
        quartic_values = [orbit_average(q, orbit) for orbit in quartic_orbits]
        pair_columns.append(pair_values)
        quartic_columns.append(quartic_values)
        atom_records.append({
            "index": atom_index,
            "minimum_coupling_exact": str(min(couplings)),
            "maximum_coupling_exact": str(max(couplings)),
            "det_R_interval": str(det_r),
            "det_Q_interval": str(det_q),
            "trace_Q_interval": str(trace_q),
        })

    # Four pair-orbit equations + eight nonpivot quartic equations + normalization.
    selected_pair_indices = (0, 1, 2, 3)
    selected_quartic_indices = tuple(range(8, 16))
    matrix_rows = [
        [pair_columns[j][i] for j in range(13)]
        for i in selected_pair_indices
    ] + [
        [quartic_columns[j][i] for j in range(13)]
        for i in selected_quartic_indices
    ] + [[arb(1) for _ in range(13)]]
    rhs = arb_mat(
        [[rational(Fraction(-1, 9))] for _ in range(4)]
        + [[rational(Fraction(1, 21))] for _ in range(8)]
        + [[arb(1)]]
    )
    matrix = arb_mat(matrix_rows)
    determinant = matrix.det()
    if determinant.contains(0):
        raise AssertionError(f"13x13 moment matrix is not certified invertible: {determinant}")
    weights = matrix.solve(rhs)
    weight_intervals = [weights[j, 0] for j in range(13)]
    if not all(weight > 0 for weight in weight_intervals):
        raise AssertionError("at least one exact-real ensemble weight is not certified positive")
    if not sum(weight_intervals, arb(0)).contains(1):
        raise AssertionError("exact-real weights do not enclose normalization")

    selected_residuals = matrix * weights - rhs
    for row in range(13):
        check_zero(selected_residuals[row, 0], f"selected system row {row}")

    # Independent Arb audit of every D10 pair and quartic orbit. Exact equality
    # of omitted coordinates follows from the integer identities below.
    pair_mixture = [
        sum((weight_intervals[j] * pair_columns[j][i] for j in range(13)), arb(0))
        for i in range(5)
    ]
    quartic_mixture = [
        sum((weight_intervals[j] * quartic_columns[j][i] for j in range(13)), arb(0))
        for i in range(16)
    ]
    pair_residuals = [value - rational(Fraction(-1, 9)) for value in pair_mixture]
    quartic_residuals = [value - rational(Fraction(1, 21)) for value in quartic_mixture]
    for i, residual in enumerate(pair_residuals):
        check_zero(residual, f"pair orbit residual {i}")
    for i, residual in enumerate(quartic_residuals):
        check_zero(residual, f"quartic orbit residual {i}")

    for row in range(8):
        value = sum((rational(Fraction(C[row][j], 21)) for j in range(16)), arb(0))
        value -= sum((rational(Fraction(D[row][j], 9)) for j in range(5)), arb(0))
        check_zero(value, f"Arb incidence target row {row}")

    result = {
        "status": "arb_certified_exact_real_positive_cycle_ensemble_n10",
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.9.0 / Arb",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "base_atom_count": 13,
        "dihedral_group_order": 20,
        "labelled_symmetrized_atom_count": 260,
        "all_base_couplings_strictly_positive": True,
        "minimum_base_coupling_exact": str(min(min(row) for row in atoms)),
        "maximum_base_coupling_exact": str(max(max(row) for row in atoms)),
        "pair_orbit_count": 5,
        "quartic_orbit_count": 16,
        "triple_orbit_count": 8,
        "all_even_subset_orbit_count": all_even_orbits,
        "all_even_subsets_count": 512,
        "pair_orbit_sizes": pair_sizes,
        "triple_quartic_incidence_pivot_determinant_exact": pivot_det,
        "selected_pair_representatives": [list(pair_reps[i]) for i in selected_pair_indices],
        "selected_quartic_representatives": [list(quartic_reps[i]) for i in selected_quartic_indices],
        "moment_matrix_determinant_interval": str(determinant),
        "exact_real_weight_intervals": [str(value) for value in weight_intervals],
        "strictly_positive_exact_real_weights": True,
        "pair_orbit_residual_intervals": [str(value) for value in pair_residuals],
        "quartic_orbit_residual_intervals": [str(value) for value in quartic_residuals],
        "atom_structural_checks": atom_records,
        "proof": (
            "The exact-real weights are the unique solution of the selected 13x13 "
            "system. Arb proves its determinant excludes zero and every weight is "
            "strictly positive. D10 symmetrization makes each principal-minor "
            "coordinate equal its orbit average. The pair identity sum_{|I|=2} "
            "det(Q_I)=e2(Q)=-5 fixes the fifth pair orbit. For each 3-set K, "
            "sum_{I superset K, |I|=4} det(Q_I)=-sum_{J subset K, |J|=2} "
            "det(Q_J). The 8x8 first-eight-quartic incidence minor has exact "
            "determinant 64, so the four pair coordinates and eight free quartic "
            "coordinates determine all 16 quartic orbits. The balanced target "
            "satisfies these same identities exactly. Finally Jacobi's complementary "
            "minor identity and Q^{-1}=Q, det(Q)=-1 give order-6 and order-8 "
            "moments from orders 4 and 2. Thus all 512 even subsets, not only the "
            "selected 12 coordinates, match exactly."
        ),
        "scope": (
            "This is an exact positive ensemble for the N=10 real nearest-neighbour "
            "cycle-exponential family. Every base coupling is a strictly positive "
            "exact rational decimal. Reflected images can be vertex-sign gauged to "
            "strictly positive couplings without changing principal minors. It is "
            "not an N=42 construction and implies no Choi/diamond-distance bound."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "precision_bits": result["precision_bits"],
        "input_sha256": result["input_sha256"],
        "moment_matrix_determinant_interval": result["moment_matrix_determinant_interval"],
        "exact_real_weight_intervals": result["exact_real_weight_intervals"],
        "minimum_base_coupling_exact": result["minimum_base_coupling_exact"],
        "all_even_subset_orbit_count": result["all_even_subset_orbit_count"],
        "pair_orbit_residual_intervals": result["pair_orbit_residual_intervals"],
        "quartic_orbit_residual_intervals": result["quartic_orbit_residual_intervals"],
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
