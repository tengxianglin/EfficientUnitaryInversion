#!/usr/bin/env python3
"""Independent exact census for the proper 3x3 rank-one Pauli grid.

This file intentionally does not import any repository helper.  The fixed
coefficient grid is the Segre grid

    g[i,j] = r_i tensor c_j,  r=(10,01,11), c=(10,01,11) in F_2^2,

flattened in the basis (00,01,10,11) of W=F_2^4.  A case consists of one of
the 64 alternating bilinear forms on W and one of its 16 compatible binary
quadratic refinements.  All arithmetic used for certificates is integer,
mod-2, mod-4, or Fraction arithmetic; no random sample or floating optimizer
is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


DIM = 4
GRID = (
    (0b0001, 0b0010, 0b0011),
    (0b0100, 0b1000, 0b1100),
    (0b0101, 0b1010, 0b1111),
)
GRID_FLAT = tuple(value for row in GRID for value in row)
ALL_VECTORS = tuple(range(1 << DIM))
PAIR_INDEX = tuple((i, j) for i in range(DIM) for j in range(i + 1, DIM))
FACTOR_VECTORS = ((1, 0), (0, 1), (1, 1))


def tensor_factor_vector(left: Sequence[int], right: Sequence[int]) -> int:
    value = 0
    for i, left_bit in enumerate(left):
        for j, right_bit in enumerate(right):
            if left_bit and right_bit:
                value |= 1 << (2 * i + j)
    return value


EXPECTED_GRID = tuple(
    tuple(tensor_factor_vector(left, right) for right in FACTOR_VECTORS)
    for left in FACTOR_VECTORS
)


def parity(value: int) -> int:
    return value.bit_count() & 1


def rank_binary(rows: Iterable[int], ncols: int = DIM) -> int:
    pivots: dict[int, int] = {}
    for value in rows:
        reduced = value
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


def rref_basis(rows: Iterable[int], ncols: int = DIM) -> tuple[int, ...]:
    """Return a deterministic reduced row basis over F2."""
    values = [value for value in rows if value]
    pivots: dict[int, int] = {}
    for value in values:
        reduced = value
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    for pivot in sorted(pivots):
        for other in tuple(pivots):
            if other != pivot and ((pivots[other] >> pivot) & 1):
                pivots[other] ^= pivots[pivot]
    return tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))


def span(basis: Sequence[int]) -> tuple[int, ...]:
    values = [0]
    for vector in basis:
        values += [value ^ vector for value in values]
    return tuple(values)


def form_matrix(mask: int) -> tuple[tuple[int, ...], ...]:
    matrix = [[0] * DIM for _ in range(DIM)]
    for bit, (i, j) in enumerate(PAIR_INDEX):
        value = (mask >> bit) & 1
        matrix[i][j] = matrix[j][i] = value
    return tuple(tuple(row) for row in matrix)


def form_mask(matrix: Sequence[Sequence[int]]) -> int:
    mask = 0
    for bit, (i, j) in enumerate(PAIR_INDEX):
        mask |= (matrix[i][j] & 1) << bit
    return mask


def bilinear(left: int, right: int, matrix: Sequence[Sequence[int]]) -> int:
    return sum(
        ((left >> i) & 1) * ((right >> j) & 1) * matrix[i][j]
        for i in range(DIM)
        for j in range(DIM)
    ) & 1


def quadratic(value: int, linear_mask: int, matrix: Sequence[Sequence[int]]) -> int:
    result = parity(value & linear_mask)
    for i, j in PAIR_INDEX:
        result ^= ((value >> i) & 1) * ((value >> j) & 1) * matrix[i][j]
    return result & 1


def compatible_quadratic(linear_mask: int, matrix: Sequence[Sequence[int]]) -> bool:
    return all(
        quadratic(left ^ right, linear_mask, matrix)
        == quadratic(left, linear_mask, matrix)
        ^ quadratic(right, linear_mask, matrix)
        ^ bilinear(left, right, matrix)
        for left in ALL_VECTORS
        for right in ALL_VECTORS
    )


def symplectic_rank(matrix: Sequence[Sequence[int]]) -> int:
    rows = [sum(matrix[i][j] << j for j in range(DIM)) for i in range(DIM)]
    return rank_binary(rows)


def radical(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    return tuple(
        value
        for value in ALL_VECTORS
        if all(bilinear(value, basis, matrix) == 0 for basis in ALL_VECTORS)
    )


def line_vectors() -> tuple[tuple[int, int, int], ...]:
    rows = tuple(tuple(row) for row in GRID)
    columns = tuple(tuple(GRID[i][j] for i in range(3)) for j in range(3))
    return rows + columns


LINES = line_vectors()


def line_commutation_pattern(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """One bit per line: the first two entries commute (0) or anticommute (1)."""
    return tuple(bilinear(line[0], line[1], matrix) for line in LINES)


def full_line_pair_pattern(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(bilinear(line[i], line[j], matrix) for i, j in ((0, 1), (0, 2), (1, 2)))
        for line in LINES
    )


def cocycle_matrix(linear_mask: int, matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """A deterministic Z2 lift C with C+C^T=omega and diag(C)=q(e_i)."""
    result = [[0] * DIM for _ in range(DIM)]
    for i in range(DIM):
        result[i][i] = (linear_mask >> i) & 1
        for j in range(i):
            result[i][j] = matrix[i][j]
    return tuple(tuple(row) for row in result)


def cocycle_phase(
    left: int,
    right: int,
    linear_mask: int,
    matrix: Sequence[Sequence[int]],
) -> int:
    """Return e in Z4 for P(left)P(right)=i**e P(left+right)."""
    q_left = quadratic(left, linear_mask, matrix)
    q_right = quadratic(right, linear_mask, matrix)
    q_sum = quadratic(left ^ right, linear_mask, matrix)
    c = cocycle_matrix(linear_mask, matrix)
    bilinear_lift = sum(
        ((left >> i) & 1) * ((right >> j) & 1) * c[i][j]
        for i in range(DIM)
        for j in range(DIM)
    ) & 1
    return (q_left + q_right - q_sum + 2 * bilinear_lift) % 4


def phase_table(
    linear_mask: int, matrix: Sequence[Sequence[int]]
) -> tuple[tuple[int, ...], ...]:
    """Precompute the complete Z4 multiplication table for one case."""
    qvalues = [quadratic(value, linear_mask, matrix) for value in ALL_VECTORS]
    c = cocycle_matrix(linear_mask, matrix)
    table = []
    for left in ALL_VECTORS:
        row = []
        for right in ALL_VECTORS:
            lift = sum(
                ((left >> i) & 1) * ((right >> j) & 1) * c[i][j]
                for i in range(DIM)
                for j in range(DIM)
            ) & 1
            row.append((qvalues[left] + qvalues[right] - qvalues[left ^ right] + 2 * lift) % 4)
        table.append(tuple(row))
    return tuple(table)


def validate_phase_lift(linear_mask: int, matrix: Sequence[Sequence[int]]) -> None:
    """Check associativity, involutions, commutators, and transpose exactly."""
    phases = phase_table(linear_mask, matrix)
    qvalues = [quadratic(value, linear_mask, matrix) for value in ALL_VECTORS]
    for left in ALL_VECTORS:
        for right in ALL_VECTORS:
            phase = phases[left][right]
            if left == right and phase != 0:
                raise AssertionError("P(v)^2 is not the identity in the phase lift")
            if (phase - phases[right][left]) % 4 \
                    != 2 * bilinear(left, right, matrix) % 4:
                raise AssertionError("phase lift has the wrong commutator")
            for third in ALL_VECTORS:
                lhs = (
                    phase
                    + phases[left ^ right][third]
                ) % 4
                rhs = (
                    phases[right][third]
                    + phases[left][right ^ third]
                ) % 4
                if lhs != rhs:
                    raise AssertionError("phase lift is not associative")
            # Transpose is an anti-automorphism with sign q.
            if (phase + 2 * qvalues[left ^ right]) % 4 != (
                phases[right][left]
                + 2 * qvalues[left]
                + 2 * qvalues[right]
            ) % 4:
                raise AssertionError("transpose signs are inconsistent with the phase lift")


def add_gaussian(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def multiply_by_i(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    a, b = value
    return ((a, b), (-b, a), (-a, -b), (b, -a))[exponent % 4]


def symbolic_power_supports(
    linear_mask: int, matrix: Sequence[Sequence[int]]
) -> tuple[tuple[int, ...], ...]:
    """Return exact supports of H^0,...,H^7, with symbolic real parameters."""
    number = len(GRID_FLAT)
    phases = phase_table(linear_mask, matrix)
    polynomial: dict[tuple[int, ...], dict[int, tuple[int, int]]] = {
        (0,) * number: {0: (1, 0)}
    }
    supports: list[tuple[int, ...]] = []
    for degree in range(1 << 3):
        labels = {
            label
            for terms in polynomial.values()
            for label, coefficient in terms.items()
            if coefficient != (0, 0)
        }
        supports.append(tuple(sorted(labels)))
        if degree == (1 << 3) - 1:
            break
        next_polynomial: dict[tuple[int, ...], dict[int, tuple[int, int]]] = {}
        for exponents, terms in polynomial.items():
            for index, generator in enumerate(GRID_FLAT):
                next_exponents = list(exponents)
                next_exponents[index] += 1
                output = next_polynomial.setdefault(tuple(next_exponents), {})
                for label, coefficient in terms.items():
                    phase = phases[label][generator]
                    product = label ^ generator
                    contribution = multiply_by_i(coefficient, phase)
                    output[product] = add_gaussian(
                        output.get(product, (0, 0)), contribution
                    )
        polynomial = {
            exponents: {
                label: coefficient
                for label, coefficient in terms.items()
                if coefficient != (0, 0)
            }
            for exponents, terms in next_polynomial.items()
        }
    return tuple(supports)


def character_equations(
    support: Sequence[int], linear_mask: int, matrix: Sequence[Sequence[int]]
) -> tuple[tuple[int, ...], ...]:
    """Rows of A c = f for all characters c_l on the listed T_L coordinates."""
    return tuple(
        tuple(1 if parity(character & value) == 0 else -1 for character in ALL_VECTORS)
        + (1 if quadratic(value, linear_mask, matrix) == 0 else -1,)
        for value in support
    )


def restricted_character_witnesses(
    support: Sequence[int], linear_mask: int, matrix: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    """Characters ell in W* that agree with transpose on T_L."""
    return tuple(
        character
        for character in ALL_VECTORS
        if all(
            (1 if parity(character & value) == 0 else -1)
            == (1 if quadratic(value, linear_mask, matrix) == 0 else -1)
            for value in support
        )
    )


def ambient_pauli_witnesses(
    support: Sequence[int], linear_mask: int, matrix: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    return tuple(
        character
        for character in ALL_VECTORS
        if all(
            (1 if bilinear(character, value, matrix) == 0 else -1)
            == (1 if quadratic(value, linear_mask, matrix) == 0 else -1)
            for value in support
        )
    )


def independent_row_indices(rows: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Select a maximal independent subset of integer rows exactly."""
    selected: list[int] = []
    current: list[list[Fraction]] = []
    rank = 0
    for index, row in enumerate(rows):
        trial = current + [[Fraction(value) for value in row]]
        # transpose to use rank_binary-like elimination over Q
        matrix = [list(column) for column in zip(*trial)]
        trial_rank = rational_rank(matrix)
        if trial_rank > rank:
            selected.append(index)
            current = trial
            rank = trial_rank
    return tuple(selected)


def rational_rank(rows: Sequence[Sequence[Fraction]]) -> int:
    if not rows:
        return 0
    matrix = [list(row) for row in rows]
    nrows, ncols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(ncols):
        pivot = next((i for i in range(rank, nrows) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for i in range(nrows):
            if i != rank and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


def solve_l1_exact(
    support: Sequence[int], linear_mask: int, matrix: Sequence[Sequence[int]]
) -> dict:
    """Exact L1 solution for m=4 character equations.

    Full T_L uses Walsh inversion.  A partial T_L is solved by an exact
    Fraction simplex over split variables; the returned dual vector certifies
    the objective.  This routine is deliberately independent of SciPy/HiGHS.
    """
    if 0 not in support:
        raise AssertionError("T_L must contain the identity coordinate from H^0")
    witnesses = restricted_character_witnesses(support, linear_mask, matrix)
    if witnesses:
        coefficients = [Fraction(0)] * len(ALL_VECTORS)
        coefficients[witnesses[0]] = Fraction(1)
        return {
            "method": "exact one-Pauli witness plus identity-coordinate lower bound",
            "lambda_fraction": [1, 1],
            "branch_count": 1,
            "postselection_probability_fraction": [1, 1],
            "coefficients_fraction": [
                [value.numerator, value.denominator] for value in coefficients
            ],
            "witnesses": list(witnesses),
            "dual_objective_fraction": [1, 1],
            "lower_bound_certificate": {
                "identity_coordinate": 0,
                "dual_value_at_identity": [1, 1],
            },
        }
    if set(support) == set(ALL_VECTORS):
        numerators = [
            sum(
                (1 if quadratic(value, linear_mask, matrix) == 0 else -1)
                * (1 if parity(character & value) == 0 else -1)
                for value in ALL_VECTORS
            )
            for character in ALL_VECTORS
        ]
        denominator = 1 << DIM
        coefficients = [Fraction(value, denominator) for value in numerators]
        objective = sum(abs(value) for value in coefficients)
        rank = symplectic_rank(matrix)
        expected = Fraction(1 << (rank // 2))
        if objective != expected:
            raise AssertionError(
                f"saturated Walsh objective {objective} != 2^(rank/2)={expected}"
            )
        dual_denominator = 1 << (DIM - rank // 2)
        dual = [
            Fraction(
                1 if quadratic(value, linear_mask, matrix) == 0 else -1,
                dual_denominator,
            )
            for value in ALL_VECTORS
        ]
        dual_character_values = [
            sum(
                dual[index]
                * (1 if parity(character & value) == 0 else -1)
                for index, value in enumerate(ALL_VECTORS)
            )
            for character in ALL_VECTORS
        ]
        if any(abs(value) > 1 for value in dual_character_values):
            raise AssertionError("saturated Walsh dual witness is infeasible")
        if sum(
            dual[index] * (1 if quadratic(value, linear_mask, matrix) == 0 else -1)
            for index, value in enumerate(ALL_VECTORS)
        ) != objective:
            raise AssertionError("saturated Walsh dual objective mismatch")
        return {
            "method": "exact full Walsh inversion plus Gauss/LP-dual certificate",
            "lambda_fraction": [objective.numerator, objective.denominator],
            "branch_count": sum(value != 0 for value in coefficients),
            "postselection_probability_fraction": [
                (objective * objective).denominator,
                (objective * objective).numerator,
            ],
            "coefficients_fraction": [
                [value.numerator, value.denominator] for value in coefficients
            ],
            "dual_objective_fraction": [objective.numerator, objective.denominator],
            "dual_fraction": [
                [value.numerator, value.denominator] for value in dual
            ],
            "saturated_formula_expected": [expected.numerator, expected.denominator],
        }
    equations = character_equations(support, linear_mask, matrix)
    row_indices = independent_row_indices([row[:-1] for row in equations])
    reduced = [equations[i] for i in row_indices]
    row_count = len(reduced)
    # A feasible point from the zero-filled extension of f to all W.
    extension = {
        value: (1 if quadratic(value, linear_mask, matrix) == 0 else -1)
        if value in support
        else 0
        for value in ALL_VECTORS
    }
    initial = tuple(
        Fraction(
            sum(
                extension[value] * (1 if parity(character & value) == 0 else -1)
                for value in ALL_VECTORS
            ),
            1 << DIM,
        )
        for character in ALL_VECTORS
    )
    # Split variables x=(u,v), c=u-v.
    columns = [
        tuple(Fraction(row[character]) for row in reduced)
        for character in ALL_VECTORS
    ]
    columns += [tuple(-value for value in column) for column in columns]
    variable_count = len(columns)
    feasible = tuple(
        max(value, Fraction(0)) for value in initial
    ) + tuple(max(-value, Fraction(0)) for value in initial)

    def solve_basis(indices: Sequence[int]) -> tuple[Fraction, ...] | None:
        basis_columns = [columns[index] for index in indices]
        # Gaussian elimination on A_B x = b.
        augmented = [
            [basis_columns[j][i] for j in range(row_count)]
            + [Fraction(reduced[i][-1])]
            for i in range(row_count)
        ]
        rank = 0
        pivot_cols: list[int] = []
        for col in range(row_count):
            pivot = next((i for i in range(rank, row_count) if augmented[i][col]), None)
            if pivot is None:
                continue
            augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
            scale = augmented[rank][col]
            augmented[rank] = [v / scale for v in augmented[rank]]
            for i in range(row_count):
                if i != rank and augmented[i][col]:
                    factor = augmented[i][col]
                    augmented[i] = [a - factor * b for a, b in zip(augmented[i], augmented[rank])]
            pivot_cols.append(col)
            rank += 1
        if rank != row_count:
            return None
        solution = [Fraction(0)] * row_count
        for i, col in enumerate(pivot_cols):
            solution[col] = augmented[i][-1]
        return tuple(solution)

    # Reduce the support of the known feasible point to a basic feasible point
    # by exact null-space moves.  This avoids the enormous ``choose(32, r)``
    # search that a naive rational LP implementation would require.
    basis_indices = reduce_feasible_support(columns, reduced, feasible)
    if basis_indices is None:
        raise AssertionError("could not construct an exact feasible LP basis")

    def objective(values: Sequence[Fraction]) -> Fraction:
        return sum(values)

    # Exact primal simplex.  Recompute the basis solve and reduced costs each
    # iteration; dimensions are at most 16x32.
    basis_set = list(basis_indices)
    for _ in range(256):
        bvalues = solve_basis(basis_set)
        if bvalues is None:
            raise AssertionError("singular exact simplex basis")
        nonbasic = [index for index in range(variable_count) if index not in basis_set]
        # dual y solves A_B^T y = c_B
        dual = solve_transpose_basis(columns, basis_set, [Fraction(1)] * row_count)
        if dual is None:
            raise AssertionError("dual basis solve failed")
        entering = None
        reduced_costs: dict[int, Fraction] = {}
        for index in nonbasic:
            reduced_cost = Fraction(1) - sum(
                dual[i] * columns[index][i] for i in range(row_count)
            )
            reduced_costs[index] = reduced_cost
            if reduced_cost < 0 and (entering is None or index < entering):
                entering = index
        if entering is None:
            values = [Fraction(0)] * variable_count
            for index, value in zip(basis_set, bvalues):
                values[index] = value
            coeffs = tuple(values[i] - values[i + len(ALL_VECTORS)] for i in range(len(ALL_VECTORS)))
            # Verify every original equation exactly.
            for equation in equations:
                lhs = sum(Fraction(equation[i]) * coeffs[i] for i in range(len(ALL_VECTORS)))
                if lhs != equation[-1]:
                    raise AssertionError("exact L1 solution failed an original equation")
            dual_full = tuple(dual)
            dual_objective = sum(
                Fraction(equation[-1]) * dual_full[pos]
                for pos, equation in enumerate(reduced)
            )
            if dual_objective != objective(values):
                raise AssertionError("primal/dual exact objectives disagree")
            return {
                "method": "exact Fraction simplex with primal/dual certificate",
                "lambda_fraction": [objective(values).numerator, objective(values).denominator],
                "branch_count": sum(value != 0 for value in coeffs),
                "postselection_probability_fraction": [
                    (objective(values) * objective(values)).denominator,
                    (objective(values) * objective(values)).numerator,
                ],
                "coefficients_fraction": [
                    [value.numerator, value.denominator] for value in coeffs
                ],
                "dual_fraction": [
                    [value.numerator, value.denominator] for value in dual_full
                ],
                "dual_objective_fraction": [
                    dual_objective.numerator,
                    dual_objective.denominator,
                ],
            }
        # Compute d_B = -A_B^{-1} A_entering directly.
        d_basic = solve_basis_direction(columns, basis_set, entering)
        leaving_candidates = [
            (bvalues[pos] / (-d_basic[pos]), basis_set[pos])
            for pos in range(row_count)
            if d_basic[pos] < 0
        ]
        if not leaving_candidates:
            raise AssertionError("unbounded L1 program")
        _, leaving = min(leaving_candidates, key=lambda item: (item[0], item[1]))
        basis_set[basis_set.index(leaving)] = entering
    raise AssertionError("exact simplex iteration limit exceeded")


def homogeneous_null_vector(
    columns: Sequence[Sequence[Fraction]], active: Sequence[int]
) -> tuple[Fraction, ...] | None:
    """Return a nonzero z with sum_j A[:,active[j]] z_j = 0."""
    if not active:
        return None
    rows = len(columns[active[0]])
    matrix = [
        [Fraction(columns[index][row]) for index in active]
        for row in range(rows)
    ]
    ncols = len(active)
    pivot_columns: list[int] = []
    pivot_row = 0
    for col in range(ncols):
        pivot = next((i for i in range(pivot_row, rows) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for i in range(rows):
            if i != pivot_row and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[pivot_row])]
        pivot_columns.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = next((col for col in range(ncols) if col not in pivot_columns), None)
    if free is None:
        return None
    vector = [Fraction(0)] * ncols
    vector[free] = Fraction(1)
    for row, pivot in reversed(list(enumerate(pivot_columns))):
        vector[pivot] = -sum(matrix[row][j] * vector[j] for j in range(ncols) if j != pivot)
    return tuple(vector)


def reduce_feasible_support(
    columns: Sequence[Sequence[Fraction]],
    equations: Sequence[Sequence[Fraction]],
    feasible: Sequence[Fraction],
) -> tuple[int, ...] | None:
    """Find a nonnegative basic feasible representation of A x=b."""
    row_count = len(equations)
    values = list(feasible)
    active = [index for index, value in enumerate(values) if value > 0]
    while True:
        null = homogeneous_null_vector(columns, active)
        if null is None:
            break
        direction = list(null)
        if all(value >= 0 for value in direction):
            direction = [-value for value in direction]
        limits = [
            values[index] / (-direction[pos])
            for pos, index in enumerate(active)
            if direction[pos] < 0
        ]
        if not limits:
            return None
        step = min(limits)
        for pos, index in enumerate(active):
            values[index] += step * direction[pos]
            if values[index] < 0:
                values[index] = Fraction(0)
        active = [index for index in active if values[index] > 0]
    # A degenerate BFS may have fewer positive columns than equations.  Extend
    # it with zero-valued columns to obtain a square basis and verify it.
    basis = list(active)
    current_rank = rational_rank(
        [
            [Fraction(columns[index][row]) for index in basis]
            for row in range(row_count)
        ]
    ) if basis else 0
    for index in range(len(columns)):
        if len(basis) == row_count:
            break
        trial = basis + [index]
        trial_rank = rational_rank(
            [
                [Fraction(columns[item][row]) for item in trial]
                for row in range(row_count)
            ]
        )
        if trial_rank > current_rank:
            basis.append(index)
            current_rank = trial_rank
    if len(basis) != row_count:
        return None
    solved = solve_square_columns(
        [columns[index] for index in basis],
        tuple(Fraction(row[-1]) for row in equations),
    )
    if solved is None or any(value < 0 for value in solved):
        return None
    return tuple(basis)


def solve_square_columns(
    columns: Sequence[Sequence[Fraction]], rhs: Sequence[Fraction]
) -> tuple[Fraction, ...] | None:
    n = len(rhs)
    if len(columns) != n:
        return None
    matrix = [
        [columns[j][i] for j in range(n)] + [Fraction(rhs[i])]
        for i in range(n)
    ]
    for col in range(n):
        pivot = next((i for i in range(col, n) if matrix[i][col]), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [value / scale for value in matrix[col]]
        for i in range(n):
            if i != col and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[col])]
    return tuple(matrix[i][-1] for i in range(n))


def solve_transpose_basis(
    columns: Sequence[Sequence[Fraction]],
    basis: Sequence[int],
    rhs: Sequence[Fraction],
) -> tuple[Fraction, ...] | None:
    transposed = [
        tuple(columns[index][row] for index in basis)
        for row in range(len(rhs))
    ]
    return solve_square_columns(transposed, rhs)


def solve_basis_direction(
    columns: Sequence[Sequence[Fraction]], basis: Sequence[int], entering: int
) -> tuple[Fraction, ...]:
    rhs = tuple(-columns[entering][row] for row in range(len(basis)))
    values = solve_square_columns(
        [columns[index] for index in basis], rhs
    )
    if values is None:
        raise AssertionError("direction solve failed")
    return values


def grid_automorphisms() -> tuple[tuple[int, ...], ...]:
    """Return the 72 (GL2 x GL2) ⋊ swap maps preserving the rank-one grid."""
    gl2 = tuple(
        (a, b)
        for a in (1, 2, 3)
        for b in (1, 2, 3)
        if a != b
    )
    maps: list[tuple[int, ...]] = []
    for left in gl2:
        for right in gl2:
            for swap in (False, True):
                image = []
                for value in ALL_VECTORS:
                    mapped = 0
                    for i in range(2):
                        for j in range(2):
                            if not ((value >> (2 * i + j)) & 1):
                                continue
                            for ii in range(2):
                                if not ((left[i] >> ii) & 1):
                                    continue
                                for jj in range(2):
                                    if not ((right[j] >> jj) & 1):
                                        continue
                                    target_i, target_j = (jj, ii) if swap else (ii, jj)
                                    mapped ^= 1 << (2 * target_i + target_j)
                    image.append(mapped)
                maps.append(tuple(image))
    return tuple(dict.fromkeys(maps))


AUTOMORPHISMS = grid_automorphisms()


def inverse_map(mapping: Sequence[int]) -> tuple[int, ...]:
    inverse = [0] * len(mapping)
    for source, target in enumerate(mapping):
        inverse[target] = source
    return tuple(inverse)


INVERSE_AUTOMORPHISMS = tuple(inverse_map(mapping) for mapping in AUTOMORPHISMS)


def transform_case(
    form: Sequence[Sequence[int]], linear_mask: int, inverse: Sequence[int]
) -> tuple[int, int]:
    transformed = [[0] * DIM for _ in range(DIM)]
    for i in range(DIM):
        for j in range(i + 1, DIM):
            value = 0
            left, right = inverse[1 << i], inverse[1 << j]
            for a in range(DIM):
                for b in range(DIM):
                    value ^= ((left >> a) & 1) * ((right >> b) & 1) * form[a][b]
            transformed[i][j] = transformed[j][i] = value
    new_linear = sum(
        quadratic(inverse[1 << i], linear_mask, form) << i for i in range(DIM)
    )
    return form_mask(transformed), new_linear


def case_orbits() -> tuple[tuple[tuple[int, int], ...], ...]:
    cases = tuple((form_mask(form_matrix(mask)), linear) for mask in range(64) for linear in range(16))
    unseen = set(cases)
    orbits = []
    while unseen:
        case = min(unseen)
        orbit = frozenset(
            transform_case(form_matrix(case[0]), case[1], inverse)
            for inverse in INVERSE_AUTOMORPHISMS
        )
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    return tuple(orbits)


def grid_lines_are_preserved(mapping: Sequence[int]) -> bool:
    line_sets = {frozenset(line) for line in LINES}
    return all(
        frozenset(mapping[value] for value in line) in line_sets for line in LINES
    )


def fraction_value(value: Sequence[int]) -> Fraction:
    return Fraction(value[0], value[1])


def case_certificate(form_mask_value: int, linear_mask: int) -> dict:
    form = form_matrix(form_mask_value)
    line_pattern = line_commutation_pattern(form)
    power_supports = symbolic_power_supports(linear_mask, form)
    envelope = tuple(sorted({label for support in power_supports for label in support}))
    witnesses = restricted_character_witnesses(envelope, linear_mask, form)
    ambient_witnesses = ambient_pauli_witnesses(envelope, linear_mask, form)
    l1 = solve_l1_exact(envelope, linear_mask, form)
    equations = character_equations(envelope, linear_mask, form)
    rank = symplectic_rank(form)
    radical_values = radical(form)
    return {
        "form_mask": form_mask_value,
        "linear_refinement_mask": linear_mask,
        "alternating_form_matrix": form,
        "quadratic_values": [quadratic(value, linear_mask, form) for value in ALL_VECTORS],
        "symplectic_rank": rank,
        "three_qubit_realizable_rank": rank in (2, 4),
        "radical_dimension": len(radical_values),
        "radical_vectors": list(radical_values),
        "line_commutation_pattern": list(line_pattern),
        "line_commutation_pattern_bits": "".join(map(str, line_pattern)),
        "line_pair_patterns": full_line_pair_pattern(form),
        "all_six_lines_commuting": not any(line_pattern),
        "power_supports": [list(support) for support in power_supports],
        "T_L": list(envelope),
        "T_L_size": len(envelope),
        "T_L_equals_W": len(envelope) == 16,
        "restricted_character_witnesses": list(witnesses),
        "ambient_pauli_witnesses_inside_W": list(ambient_witnesses),
        "one_pauli_witness_possible_in_three_qubit_ambient": (
            bool(witnesses) if rank in (2, 4) else None
        ),
        "restricted_character_equations": [list(row) for row in equations],
        "l1_solution": l1,
        "proof_obligations": {
            "quadratic_refinement_identity": True,
            "associative_phase_lift": True,
            "restricted_character_equations": True,
            "exact_l1_optimality_certificate": True,
        },
    }


def classify_claim(certificate: dict) -> dict:
    all_commuting = certificate["all_six_lines_commuting"]
    t_size = certificate["T_L_size"]
    witnesses = certificate["restricted_character_witnesses"]
    lambda_fraction = fraction_value(certificate["l1_solution"]["lambda_fraction"])
    saturated = certificate["T_L_equals_W"]
    rank = certificate["symplectic_rank"]
    return {
        "claim_all_commuting_iff_T10_and_witness": all_commuting == (t_size == 10 and bool(witnesses)),
        "claim_otherwise_T_equals_W": (not all_commuting) == saturated,
        "claim_saturated_lambda_formula": (not saturated)
        or lambda_fraction == (1 << (rank // 2)),
        "observed_lambda_fraction": [
            lambda_fraction.numerator,
            lambda_fraction.denominator,
        ],
    }


CLAIM_KEYS = (
    "claim_all_commuting_iff_T10_and_witness",
    "claim_otherwise_T_equals_W",
    "claim_saturated_lambda_formula",
)


def claim_passes(claim: dict) -> bool:
    return all(bool(claim[key]) for key in CLAIM_KEYS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if GRID != EXPECTED_GRID:
        raise AssertionError("fixed coefficient grid is not the rank-one tensor grid")
    if len(set(GRID_FLAT)) != 9 or 0 in GRID_FLAT:
        raise AssertionError("fixed coefficient grid is not proper")
    if len(AUTOMORPHISMS) != 72:
        raise AssertionError(f"grid automorphism group has {len(AUTOMORPHISMS)} maps, expected 72")
    if any(set(mapping[value] for value in GRID_FLAT) != set(GRID_FLAT) for mapping in AUTOMORPHISMS):
        raise AssertionError("an alleged grid automorphism does not preserve the rank-one grid")
    if not all(grid_lines_are_preserved(mapping) for mapping in AUTOMORPHISMS):
        raise AssertionError("an alleged grid automorphism does not preserve the six lines")
    for form_mask_value in range(64):
        form = form_matrix(form_mask_value)
        for linear_mask in range(16):
            if not compatible_quadratic(linear_mask, form):
                raise AssertionError("quadratic refinement enumeration is inconsistent")
            validate_phase_lift(linear_mask, form)
            for inverse in INVERSE_AUTOMORPHISMS:
                transformed_form, transformed_linear = transform_case(
                    form, linear_mask, inverse
                )
                if not compatible_quadratic(
                    transformed_linear, form_matrix(transformed_form)
                ):
                    raise AssertionError("grid automorphism broke quadratic compatibility")

    orbits = case_orbits()
    case_to_orbit = {
        case: orbit_id
        for orbit_id, orbit in enumerate(orbits)
        for case in orbit
    }
    if len(case_to_orbit) != 64 * 16:
        raise AssertionError("case orbits do not cover all 1024 cases")

    certificates = []
    all_cases = []
    for orbit_id, orbit in enumerate(orbits):
        representative = orbit[0]
        certificate = case_certificate(*representative)
        claim = classify_claim(certificate)
        certificate["orbit_id"] = orbit_id
        certificate["orbit_size"] = len(orbit)
        certificate["member_cases"] = [
            {"form_mask": form, "linear_refinement_mask": linear}
            for form, linear in orbit
        ]
        certificate["claim_checks"] = claim
        certificate["certificate_sha256"] = hashlib.sha256(
            json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        certificates.append(certificate)
        for form, linear in orbit:
            all_cases.append(
                {
                    "form_mask": form,
                    "linear_refinement_mask": linear,
                    "orbit_id": orbit_id,
                    "representative": {
                        "form_mask": representative[0],
                        "linear_refinement_mask": representative[1],
                    },
                    "representative_certificate_sha256": certificate["certificate_sha256"],
                }
            )

    # Verify the certificate is invariant under every member map by checking
    # the cheap exact fields after transporting the representative.
    for item in all_cases:
        rep = next(
            certificate
            for certificate in certificates
            if certificate["orbit_id"] == item["orbit_id"]
        )
        transformed = case_certificate(item["form_mask"], item["linear_refinement_mask"])
        if transformed["symplectic_rank"] != rep["symplectic_rank"]:
            raise AssertionError("orbit transport changed symplectic rank")
        if transformed["T_L_size"] != rep["T_L_size"]:
            raise AssertionError("orbit transport changed T_L size")
        if transformed["l1_solution"]["lambda_fraction"] != rep["l1_solution"]["lambda_fraction"]:
            raise AssertionError("orbit transport changed exact lambda")
        item.update(
            {
                "symplectic_rank": transformed["symplectic_rank"],
                "three_qubit_realizable_rank": transformed["symplectic_rank"] in (2, 4),
                "line_commutation_pattern_bits": transformed["line_commutation_pattern_bits"],
                "all_six_lines_commuting": transformed["all_six_lines_commuting"],
                "power_support_sizes": [len(values) for values in transformed["power_supports"]],
                "T_L": transformed["T_L"],
                "T_L_size": transformed["T_L_size"],
                "T_L_equals_W": transformed["T_L_equals_W"],
                "restricted_character_witness_count": len(
                    transformed["restricted_character_witnesses"]
                ),
                "lambda_fraction": transformed["l1_solution"]["lambda_fraction"],
                "claim_checks": classify_claim(transformed),
            }
        )

    counterexamples = [
        {
            "orbit_id": certificate["orbit_id"],
            "representative": {
                "form_mask": certificate["form_mask"],
                "linear_refinement_mask": certificate["linear_refinement_mask"],
            },
            "claim_checks": certificate["claim_checks"],
            "all_six_lines_commuting": certificate["all_six_lines_commuting"],
            "T_L_size": certificate["T_L_size"],
            "T_L_equals_W": certificate["T_L_equals_W"],
            "restricted_character_witnesses": certificate[
                "restricted_character_witnesses"
            ],
            "symplectic_rank": certificate["symplectic_rank"],
            "certificate_sha256": certificate["certificate_sha256"],
            "member_case_count": certificate["orbit_size"],
            "member_cases": certificate["member_cases"],
        }
        for certificate in certificates
        if not claim_passes(certificate["claim_checks"])
    ]
    raw_counterexamples = [
        item for item in all_cases if not claim_passes(item["claim_checks"])
    ]
    realizable_counterexamples = [
        item for item in raw_counterexamples if item["three_qubit_realizable_rank"]
    ]
    summary = {
        "raw_case_count": len(all_cases),
        "alternating_form_count": 64,
        "quadratic_refinements_per_form": 16,
        "alternating_form_rank_histogram": {
            str(rank): count
            for rank, count in sorted(
                Counter(symplectic_rank(form_matrix(mask)) for mask in range(64)).items()
            )
        },
        "grid_automorphism_group_order": len(AUTOMORPHISMS),
        "equivalence_class_count": len(certificates),
        "raw_realizable_three_qubit_case_count": sum(
            item["three_qubit_realizable_rank"] for item in all_cases
        ),
        "raw_all_six_lines_commuting_count": sum(
            item["all_six_lines_commuting"] for item in all_cases
        ),
        "equivalence_class_line_pattern_histogram": dict(
            Counter(
                certificate["line_commutation_pattern_bits"]
                for certificate in certificates
            )
        ),
        "raw_line_pattern_histogram": dict(
            Counter(item["line_commutation_pattern_bits"] for item in all_cases)
        ),
        "raw_T_L_size_histogram": {
            str(size): count
            for size, count in sorted(Counter(item["T_L_size"] for item in all_cases).items())
        },
        "raw_lambda_histogram": {
            f"{fraction[0]}/{fraction[1]}": count
            for fraction, count in sorted(
                Counter(tuple(item["lambda_fraction"]) for item in all_cases).items()
            )
        },
        "classification_claim": {
            "all_1024_abstract_cases_pass": not raw_counterexamples,
            "raw_counterexample_case_count": len(raw_counterexamples),
            "counterexample_orbit_count": len(counterexamples),
            "all_rank_2_or_4_three_qubit_realizable_cases_pass": not realizable_counterexamples,
            "realizable_counterexample_case_count": len(realizable_counterexamples),
            "refined_statement": (
                "The proposed classification fails for the rank-0 zero form, which cannot be "
                "the restriction of the three-qubit nondegenerate symplectic form to a proper "
                "four-dimensional grid span. It holds for every enumerated rank-2 or rank-4 case."
            ),
        },
    }
    payload = {
        "schema": "eui-independent-exact-grid-certificate-v1",
        "arithmetic": {
            "field": "F2",
            "phase_lift": "Z4 Gaussian-integer cocycle from (omega,q)",
            "phase_lift_formula": (
                "phi(u,v)=q(u)+q(v)-q(u+v)+2*u^T*C*v mod 4; "
                "C_ii=q(e_i), C_ij=omega(e_i,e_j) for i>j, C_ij=0 for i<j"
            ),
            "lp": "exact Fraction primal simplex plus dual certificate",
            "randomness": False,
            "floating_point_optimization": False,
        },
        "fixed_rank_one_coefficient_grid": [list(row) for row in GRID],
        "proper_grid": {
            "nine_distinct_vectors": len(set(GRID_FLAT)) == 9,
            "no_identity_vector": 0 not in GRID_FLAT,
        },
        "rank_one_factor_vectors": {
            "row_vectors_F2_2": [[1, 0], [0, 1], [1, 1]],
            "column_vectors_F2_2": [[1, 0], [0, 1], [1, 1]],
            "flattening_basis": ["e0_tensor_f0", "e0_tensor_f1", "e1_tensor_f0", "e1_tensor_f1"],
        },
        "line_order": ["row0", "row1", "row2", "col0", "col1", "col2"],
        "power_support_semantics": (
            "power_supports[k] is the exact nonzero Pauli-label support of the "
            "symbolic homogeneous polynomial H^k; T_L is their union for k=0..7"
        ),
        "character_equation_semantics": (
            "A[v,ell]=(-1)^(ell dot v), rhs[v]=(-1)^q(v), for v in T_L and ell in W*"
        ),
        "character_witness_semantics": (
            "restricted_character_witnesses are ell in W*; for realizable rank-2/rank-4 "
            "forms every such ell has an ambient Pauli extension, while the separate "
            "ambient_pauli_witnesses_inside_W field lists only witnesses represented inside W"
        ),
        "physical_scope": (
            "A proper four-dimensional subspace of the nondegenerate three-qubit "
            "Pauli symplectic space has restricted rank 2 or 4; rank 0 cases are "
            "retained as abstract counterexamples but are not physical three-qubit embeddings"
        ),
        "equivalence": {
            "group": "(GL(2,2) x GL(2,2)) semidirect C2 acting on r tensor c",
            "group_order": len(AUTOMORPHISMS),
            "raw_case_key": ["alternating_form_mask", "quadratic_linear_refinement_mask"],
        },
        "summary": summary,
        "counterexamples": counterexamples,
        "equivalence_classes": certificates,
        "all_cases": sorted(all_cases, key=lambda item: (item["orbit_id"], item["form_mask"], item["linear_refinement_mask"])),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
