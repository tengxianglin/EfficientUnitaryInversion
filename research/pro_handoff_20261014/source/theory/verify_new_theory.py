#!/usr/bin/env python3
"""Independent checks for the 2026-09-07 EUI audio/manuscript claims.

Conventions: an n-qubit label is read left-to-right as q0 tensor ... tensor
q(n-1); P(x|z)=i^(x.z) X^x Z^z is Hermitian; q(x|z)=x.z mod 2 and
omega((x|z),(x'|z'))=x.z'+z.x' mod 2.  T, dagger, and star mean ordinary
transpose, conjugate transpose, and entrywise complex conjugation.

This file intentionally imports no project verification helper.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import numpy as np


I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
GAMMA_LABELS = ("YXX", "IYX", "YZX", "IIY", "YIZ", "XYZ", "ZYZ")


def parity(value: int) -> int:
    return value.bit_count() & 1


def label_to_vector(label: str) -> int:
    n = len(label)
    x = z = 0
    for index, char in enumerate(label):
        if char in "XY":
            x |= 1 << index
        if char in "YZ":
            z |= 1 << index
    return x | (z << n)


def vector_to_label(value: int, n: int) -> str:
    mask = (1 << n) - 1
    x, z = value & mask, value >> n
    chars = []
    for index in range(n):
        chars.append(
            {
                (0, 0): "I",
                (1, 0): "X",
                (0, 1): "Z",
                (1, 1): "Y",
            }[((x >> index) & 1, (z >> index) & 1)]
        )
    return "".join(chars)


def qform(value: int, n: int) -> int:
    mask = (1 << n) - 1
    return parity((value & mask) & (value >> n))


def symplectic(left: int, right: int, n: int) -> int:
    mask = (1 << n) - 1
    lx, lz = left & mask, left >> n
    rx, rz = right & mask, right >> n
    return parity((lx & rz) ^ (lz & rx))


def gf2_rank(rows: list[int] | tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def gf2_affine_dimension(rows: list[int], rhs: list[int], nvars: int) -> int:
    augmented = [row | (bit << nvars) for row, bit in zip(rows, rhs)]
    pivot_row = 0
    for column in range(nvars):
        found = next(
            (index for index in range(pivot_row, len(augmented)) if (augmented[index] >> column) & 1),
            None,
        )
        if found is None:
            continue
        augmented[pivot_row], augmented[found] = augmented[found], augmented[pivot_row]
        for index in range(len(augmented)):
            if index != pivot_row and ((augmented[index] >> column) & 1):
                augmented[index] ^= augmented[pivot_row]
        pivot_row += 1
    mask = (1 << nvars) - 1
    assert all((row & mask) or not ((row >> nvars) & 1) for row in augmented)
    return nvars - pivot_row


def pauli_matrix(label: str) -> np.ndarray:
    result = np.array([[1]], dtype=np.complex128)
    for char in label:
        result = np.kron(result, PAULI[char])
    return result


def matrix_from_vector(value: int, n: int) -> np.ndarray:
    return pauli_matrix(vector_to_label(value, n))


def exp_minus_i_hermitian(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * np.exp(-1j * values)) @ vectors.conj().T


def diagonal_pauli_map(matrix: np.ndarray, n: int, sign) -> np.ndarray:
    dim = 1 << n
    result = np.zeros_like(matrix, dtype=np.complex128)
    for value in range(1 << (2 * n)):
        pauli = matrix_from_vector(value, n)
        coefficient = np.trace(pauli @ matrix) / dim
        result += ((-1) ** sign(value)) * coefficient * pauli
    return result


def check_seven_generator_family() -> dict[str, object]:
    n = 3
    vectors = tuple(label_to_vector(label) for label in GAMMA_LABELS)
    matrices = tuple(pauli_matrix(label) for label in GAMMA_LABELS)
    identity = np.eye(1 << n, dtype=np.complex128)

    assert all(qform(value, n) == 1 for value in vectors)
    assert all(symplectic(a, b, n) == 1 for i, a in enumerate(vectors) for b in vectors[i + 1 :])
    assert gf2_rank(vectors) == 6
    assert np.bitwise_xor.reduce(vectors) == 0
    assert all(np.array_equal(matrix @ matrix, identity) for matrix in matrices)
    assert all(
        np.array_equal(a @ b + b @ a, np.zeros_like(identity))
        for i, a in enumerate(matrices)
        for b in matrices[i + 1 :]
    )

    common_anticommuters = [
        value
        for value in range(1 << (2 * n))
        if all(symplectic(value, gamma, n) == 1 for gamma in vectors)
    ]
    assert common_anticommuters == []

    character_sums = sorted(
        {
            sum(1 if symplectic(character, gamma, n) == 0 else -1 for gamma in vectors)
            for character in range(1 << (2 * n))
        }
    )
    dual_constraints = [Fraction(1 - total, 6) for total in character_sums]
    assert character_sums == [-5, -1, 3, 7]
    assert max(map(abs, dual_constraints)) == 1
    primal = [Fraction(-1, 6)] + [Fraction(1, 6)] * 7
    assert sum(map(abs, primal)) == Fraction(4, 3)
    assert Fraction(1, 6) + 7 * Fraction(1, 6) == Fraction(4, 3)

    rng = np.random.default_rng(20260907)
    max_h2 = max_transpose = max_identity = max_success = max_circuit = 0.0
    for trial in range(32):
        alpha = rng.normal(size=7)
        hamiltonian = sum((coefficient * matrix for coefficient, matrix in zip(alpha, matrices)), start=np.zeros_like(identity))
        radius2 = float(alpha @ alpha)
        max_h2 = max(max_h2, float(np.linalg.norm(hamiltonian @ hamiltonian - radius2 * identity)))
        unitary = exp_minus_i_hermitian(hamiltonian)
        numerator = -unitary + sum((gamma @ unitary @ gamma for gamma in matrices), start=np.zeros_like(identity))
        formula = numerator / 6
        kraus = numerator / 8
        max_transpose = max(max_transpose, float(np.linalg.norm(unitary.T - unitary.conj().T)))
        max_identity = max(max_identity, float(np.linalg.norm(formula - unitary.conj().T)))
        max_success = max(
            max_success,
            float(np.linalg.norm(kraus.conj().T @ kraus - (9.0 / 16.0) * identity)),
        )
        if trial == 0:
            hadamard = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
            branch_hadamard = np.kron(np.kron(hadamard, hadamard), hadamard)
            branches = (identity, *matrices)
            select = np.zeros((64, 64), dtype=np.complex128)
            for branch, pauli in enumerate(branches):
                select[branch * 8 : (branch + 1) * 8, branch * 8 : (branch + 1) * 8] = pauli
            phase = np.diag([-1, 1, 1, 1, 1, 1, 1, 1]).astype(np.complex128)
            prepare = np.kron(branch_hadamard, identity)
            circuit = prepare @ np.kron(phase, identity) @ select @ np.kron(np.eye(8), unitary) @ select @ prepare
            max_circuit = float(np.linalg.norm(circuit[:8, :8] - 0.75 * unitary.conj().T))
    assert max(max_h2, max_transpose, max_identity, max_success, max_circuit) < 2e-13

    return {
        "status": "VERIFIED",
        "support": list(GAMMA_LABELS),
        "gf2_rank": 6,
        "unique_relation": "xor(Gamma_1,...,Gamma_7)=0",
        "common_anticommuting_paulis": 0,
        "character_sums": character_sums,
        "lambda": "4/3",
        "kraus_amplitude": "3/4",
        "success_probability": "9/16",
        "random_trials": 32,
        "max_h_squared_residual": max_h2,
        "max_ut_equals_udagger_residual": max_transpose,
        "max_lcu_identity_residual": max_identity,
        "max_success_operator_residual": max_success,
        "explicit_ancilla_circuit_block_residual": max_circuit,
    }


def jordan_wigner_frame(n: int) -> tuple[str, ...]:
    labels = []
    for index in range(n):
        prefix = "Z" * index
        suffix = "I" * (n - index - 1)
        labels.extend((prefix + "X" + suffix, prefix + "Y" + suffix))
    labels.append("Z" * n)
    return tuple(labels)


def check_general_clifford_inversion_family() -> dict[str, object]:
    rng = np.random.default_rng(260907)
    frames = []
    global_max_residual = 0.0
    for n in range(1, 6):
        labels = jordan_wigner_frame(n)
        vectors = tuple(map(label_to_vector, labels))
        matrices = tuple(map(pauli_matrix, labels))
        count = 2 * n + 1
        dim = 1 << n
        identity = np.eye(dim, dtype=np.complex128)
        assert len(labels) == count
        assert gf2_rank(vectors) == 2 * n
        assert np.bitwise_xor.reduce(vectors) == 0
        assert all(
            symplectic(left, right, n) == 1
            for index, left in enumerate(vectors)
            for right in vectors[index + 1 :]
        )

        character_sums = sorted(
            {
                sum(1 if symplectic(character, gamma, n) == 0 else -1 for gamma in vectors)
                for character in range(1 << (2 * n))
            }
        )
        expected_sums = list(range(2 - count, count + 1, 4))
        assert character_sums == expected_sums
        dual_constraints = [Fraction(1 - total, count - 1) for total in character_sums]
        assert max(map(abs, dual_constraints)) == 1
        l1_cost = Fraction(count + 1, count - 1)
        success = Fraction(count - 1, count + 1) ** 2

        max_residual = 0.0
        trials = 8 if n <= 4 else 4
        for _ in range(trials):
            alpha = rng.normal(size=count)
            hamiltonian = sum(
                (coefficient * matrix for coefficient, matrix in zip(alpha, matrices)),
                start=np.zeros_like(identity),
            )
            unitary = exp_minus_i_hermitian(hamiltonian)
            formula = (
                -unitary
                + sum((gamma @ unitary @ gamma for gamma in matrices), start=np.zeros_like(identity))
            ) / (count - 1)
            max_residual = max(max_residual, float(np.linalg.norm(formula - unitary.conj().T)))
        assert max_residual < 4e-13
        global_max_residual = max(global_max_residual, max_residual)
        frames.append(
            {
                "n": n,
                "m": count,
                "support": list(labels),
                "gf2_rank": 2 * n,
                "unique_odd_relation": "xor(all frame labels)=0",
                "y_parities": [qform(value, n) for value in vectors],
                "lambda": str(l1_cost),
                "success_probability": str(success),
                "random_trials": trials,
                "max_identity_residual": max_residual,
            }
        )

    return {
        "status": "VERIFIED_NEW_PROJECT_LEVEL_GENERALIZATION",
        "identity": "U^dagger=(-U+sum_j Gamma_j U Gamma_j)/(m-1)",
        "hypotheses": "real H coefficients and pairwise anticommuting Hermitian involutions Gamma_j, m>1",
        "maximal_pauli_frame_corollary": {
            "m": "2n+1",
            "lambda": "(n+1)/n",
            "branches": "2n+2",
            "success_probability": "[n/(n+1)]^2",
            "ancillas_standard": "ceil(log2(2n+2))",
            "query_resource": "K=P=Q=1, postselected",
        },
        "optimality_scope": "exact within the one-query Pauli-conjugation LCU dictionary on span{I,Gamma_j}",
        "transpose_boundary": "odd Y parity is needed for U^T=U^dagger, not for the dagger identity itself",
        "frames_n1_to_n5": frames,
        "global_max_dense_residual": global_max_residual,
    }


def check_pairwise_frame_dichotomy() -> dict[str, object]:
    cases = []
    specifications = [
        (2, jordan_wigner_frame(2)[:2]),
        (2, jordan_wigner_frame(2)[:3]),
        (2, jordan_wigner_frame(2)),
        (3, ("XII", "YII", "ZII")),
        (3, jordan_wigner_frame(3)[:4]),
        (3, jordan_wigner_frame(3)[:5]),
        (3, jordan_wigner_frame(3)),
    ]
    for n, labels in specifications:
        count = len(labels)
        vectors = tuple(map(label_to_vector, labels))
        rank = gf2_rank(vectors)
        assert all(
            symplectic(left, right, n) == 1
            for index, left in enumerate(vectors)
            for right in vectors[index + 1 :]
        )
        common = [
            value
            for value in range(1 << (2 * n))
            if all(symplectic(value, gamma, n) == 1 for gamma in vectors)
        ]
        dependent = rank == count - 1
        assert rank in (count, count - 1)
        assert not dependent or (count % 2 == 1 and np.bitwise_xor.reduce(vectors) == 0)
        assert bool(common) != dependent
        if count % 2 == 0:
            product_label = np.bitwise_xor.reduce(vectors)
            assert all(symplectic(product_label, gamma, n) == 1 for gamma in vectors)
        optimum = Fraction(count + 1, count - 1) if dependent else Fraction(1)
        cases.append(
            {
                "n": n,
                "m": count,
                "gf2_rank": rank,
                "dependent_unique_odd_relation": dependent,
                "common_anticommuting_paulis": len(common),
                "lambda_optimum": str(optimum),
            }
        )
    return {
        "status": "VERIFIED",
        "theorem": (
            "For pairwise-anticommuting Pauli labels, the relation kernel is either empty or the "
            "all-ones vector. Independent labels admit a common anticommuting Pauli and Lambda=1; "
            "the unique odd relation forbids it and gives Lambda=(m+1)/(m-1)."
        ),
        "scope": "one-query Pauli-conjugation LCU on span{I,Gamma_j}",
        "representative_exact_cases": cases,
    }


def check_sign_map_classification() -> dict[str, object]:
    systems = []
    for n in (1, 2, 3):
        size = 1 << (2 * n)
        for defect, name in ((0, "linear"), (1, "quadratic_refinement")):
            rows = [1]
            rhs = [0]
            for left in range(size):
                for right in range(size):
                    rows.append((1 << left) ^ (1 << right) ^ (1 << (left ^ right)))
                    rhs.append(defect * symplectic(left, right, n))
            dimension = gf2_affine_dimension(rows, rhs, size)
            assert dimension == 2 * n
            for character in range(size):
                for left in range(size):
                    for right in range(size):
                        def value(vector: int) -> int:
                            base = qform(vector, n) if defect else 0
                            return base ^ symplectic(character, vector, n)

                        assert value(left ^ right) == (
                            value(left) ^ value(right) ^ (defect * symplectic(left, right, n))
                        )
            systems.append(
                {
                    "n": n,
                    "type": name,
                    "affine_dimension": dimension,
                    "number_of_maps": 1 << dimension,
                }
            )

    rng = np.random.default_rng(907)
    odd_x_checks = []
    cost_shift_checks = []
    for n in (1, 2, 3):
        mask = (1 << n) - 1
        z_all_vector = mask << n

        def literal_x_parity(value: int) -> int:
            x, z = value & mask, value >> n
            return parity(x & (mask ^ z))

        assert all(
            literal_x_parity(value) == (qform(value, n) ^ parity(value & mask))
            for value in range(1 << (2 * n))
        )
        assert all(
            symplectic(character ^ z_all_vector, value, n)
            == (symplectic(character, value, n) ^ symplectic(z_all_vector, value, n))
            for character in range(1 << (2 * n))
            for value in range(1 << (2 * n))
        )
        cost_shift_checks.append({"n": n, "characters_checked": 1 << (2 * n)})
        dim = 1 << n
        matrix = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
        z_all = pauli_matrix("Z" * n)
        transformed = diagonal_pauli_map(matrix, n, literal_x_parity)
        expected = z_all @ matrix.T @ z_all
        dual = z_all @ transformed.conj() @ z_all
        anti_hom = diagonal_pauli_map(matrix @ matrix, n, literal_x_parity)
        residual = max(
            float(np.linalg.norm(transformed - expected)),
            float(np.linalg.norm(dual - matrix.conj().T)),
            float(np.linalg.norm(anti_hom - transformed @ transformed)),
        )
        assert residual < 2e-13
        odd_x_checks.append({"n": n, "max_residual": residual})

    return {
        "status": "VERIFIED_WITH_NOVELTY_BOUNDARY",
        "classification": systems,
        "theorem": {
            "linear_signs": "r(v)=ell(v): complex-linear automorphisms or conjugate-linear anti-automorphisms",
            "quadratic_signs": "r(v)=q(v)+ell(v): complex-linear anti-automorphisms or conjugate-linear automorphisms",
        },
        "literal_odd_x_rule": {
            "identity": "r_X(v)=q(v)+parity(x)=sign of Ad[Z^tensor n] after transpose",
            "map": "F_X(M)=Z^tensor n M^T Z^tensor n",
            "dual": "G_X(F_X(M))=M^dagger with G_X(N)=Z^tensor n N^* Z^tensor n",
            "dense_checks": odd_x_checks,
            "pauli_lcu_cost_invariance": {
                "status": "VERIFIED",
                "reason": "multiplying the transpose target by a Pauli character only permutes LCU coefficient columns",
                "exact_checks": cost_shift_checks,
            },
            "boundary": "This is a Pauli-conjugated transpose/star pair, not a new full-algebra map class.",
        },
    }


def span(values: tuple[int, ...]) -> set[int]:
    result = {0}
    for value in values:
        result |= {item ^ value for item in tuple(result)}
    return result


def degree_two_coordinates(values: tuple[int, ...], n: int) -> set[int]:
    result: set[int] = set()
    for index, left in enumerate(values):
        for right in values[index:]:
            if symplectic(left, right, n) == 0:
                result.add(left ^ right)
    return result


def pauli_product_phase(left: int, right: int, n: int) -> int:
    """Return p in P(left)P(right)=i^p P(left xor right)."""
    mask = (1 << n) - 1
    lx, lz = left & mask, left >> n
    rx, rz = right & mask, right >> n
    sx, sz = lx ^ rx, lz ^ rz
    return (
        (lx & lz).bit_count()
        + (rx & rz).bit_count()
        + 2 * (lz & rx).bit_count()
        - (sx & sz).bit_count()
    ) % 4


def exact_graded_coordinates(values: tuple[int, ...], n: int) -> list[set[int]]:
    """Coordinates in fully symmetrized parameter coefficients of H^k."""
    powers_of_i = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def multiply(value: tuple[int, int], phase: int) -> tuple[int, int]:
        real, imag = value
        phase_real, phase_imag = powers_of_i[phase]
        return real * phase_real - imag * phase_imag, real * phase_imag + imag * phase_real

    state: dict[tuple[int, ...], tuple[int, tuple[int, int]]] = {
        (0,) * len(values): (0, (1, 0))
    }
    result = [{0}]
    for _ in range(1, 1 << n):
        following: dict[tuple[int, ...], tuple[int, tuple[int, int]]] = {}
        for counts, (current, coefficient) in state.items():
            for index, value in enumerate(values):
                next_counts = list(counts)
                next_counts[index] += 1
                key = tuple(next_counts)
                next_value = current ^ value
                term = multiply(coefficient, pauli_product_phase(current, value, n))
                if key in following:
                    previous_value, previous = following[key]
                    assert previous_value == next_value
                    term = (previous[0] + term[0], previous[1] + term[1])
                following[key] = next_value, term
        state = following
        result.append({value for value, coefficient in state.values() if coefficient != (0, 0)})
    return result


def edge_label(sites: int, edge: int, char: str) -> str:
    label = ["I"] * sites
    label[edge] = label[edge + 1] = char
    return "".join(label)


def gram_rank(values: tuple[int, ...], n: int) -> int:
    rows = []
    for left in values:
        row = 0
        for index, right in enumerate(values):
            row |= symplectic(left, right, n) << index
        rows.append(row)
    return gf2_rank(rows)


def check_deletion_and_heisenberg_claims() -> dict[str, object]:
    n = 2
    full_labels = ("XX", "YY", "ZZ")
    reduced_labels = ("XX", "YY")
    full = tuple(map(label_to_vector, full_labels))
    reduced = tuple(map(label_to_vector, reduced_labels))
    assert full[0] ^ full[1] == full[2]
    assert all(symplectic(a, b, n) == 0 for i, a in enumerate(full) for b in full[i + 1 :])
    assert span(full) == span(reduced) == {0, *full}
    full_e1, reduced_e1 = set(full), set(reduced)
    full_e2 = degree_two_coordinates(full, n)
    reduced_e2 = degree_two_coordinates(reduced, n)
    assert full_e1 & full_e2 == set(full)
    assert reduced_e1 & reduced_e2 == set()
    full_anticommuters = [
        value for value in range(16) if all(symplectic(value, item, n) for item in full)
    ]
    reduced_anticommuters = [
        vector_to_label(value, n)
        for value in range(16)
        if all(symplectic(value, item, n) for item in reduced)
    ]
    assert full_anticommuters == []
    assert reduced_anticommuters
    assert all(qform(value, n) == 0 for value in full)

    cumulative_full_labels = ("XI", "IX", "XX", "ZI", "IZ")
    cumulative_reduced_labels = ("XI", "IX", "ZI", "IZ")
    cumulative_full = tuple(map(label_to_vector, cumulative_full_labels))
    cumulative_reduced = tuple(map(label_to_vector, cumulative_reduced_labels))
    assert cumulative_full[0] ^ cumulative_full[1] == cumulative_full[2]
    assert symplectic(cumulative_full[0], cumulative_full[1], 2) == 0
    graded_full = exact_graded_coordinates(cumulative_full, 2)
    graded_reduced = exact_graded_coordinates(cumulative_reduced, 2)
    envelope_full = set().union(*graded_full)
    envelope_reduced = set().union(*graded_reduced)
    only_full = envelope_full - envelope_reduced
    assert {vector_to_label(value, 2) for value in only_full} == {"YY"}
    assert len(envelope_full) == 10 and len(envelope_reduced) == 9

    chain = []
    for sites in range(2, 11):
        edges = sites - 1
        generators = tuple(
            label_to_vector(edge_label(sites, edge, char))
            for edge in range(edges)
            for char in ("X", "Z")
        )
        adjacency_rows = [
            sum(1 << right for right in range(edges) if abs(left - right) == 1)
            for left in range(edges)
        ]
        expected_symplectic_rank = 2 * gf2_rank(adjacency_rows)
        actual_symplectic_rank = gram_rank(generators, sites)
        assert gf2_rank(generators) == 2 * edges
        assert actual_symplectic_rank == expected_symplectic_rank
        chain.append(
            {
                "sites": sites,
                "phase_free_rank": 2 * edges,
                "symplectic_rank": actual_symplectic_rank,
                "radical_dimension": 2 * edges - actual_symplectic_rank,
                "active_logical_qubits": actual_symplectic_rank // 2,
                "abstract_pauli_algebra": (
                    f"M_{1 << edges}(C)" if edges % 2 == 0
                    else f"direct_sum_4(M_{1 << (edges - 1)}(C))"
                ),
            }
        )

    return {
        "status": "DISPROVED_AS_GENERAL_ENVELOPE_OR_DAGGER_EQUIVALENCE",
        "cumulative_envelope_counterexample": {
            "full_support": list(cumulative_full_labels),
            "reduced_support": list(cumulative_reduced_labels),
            "commuting_product_relation": "XX = XI * IX",
            "full_degree_dimensions": [len(values) for values in graded_full],
            "reduced_degree_dimensions": [len(values) for values in graded_reduced],
            "full_envelope_dimension": 10,
            "reduced_envelope_dimension": 9,
            "coordinate_lost_by_deletion": "YY",
        },
        "heisenberg_two_site_graded_counterexample": {
            "full_support": list(full_labels),
            "reduced_support": list(reduced_labels),
            "same_phase_free_span": True,
            "same_ungraded_commuting_envelope": ["II", "XX", "YY", "ZZ"],
            "full_E1_intersect_E2": list(full_labels),
            "reduced_E1_intersect_E2": [],
            "full_common_anticommuting_paulis": 0,
            "reduced_common_anticommuting_examples": reduced_anticommuters,
            "transpose_action": "identity on both families because all coordinates have even Y parity",
        },
        "conclusion": (
            "Deleting a commuting product can change even the cumulative exponential envelope; "
            "when it happens to preserve that envelope, it can still change graded parity and "
            "fixed-scalar one-query dagger feasibility."
        ),
        "dagger_scope": (
            "one forward query, fixed parameter-independent gates, a clean successful block, "
            "and one fixed nonzero success scalar"
        ),
        "heisenberg_chain_canonical_ranks": chain,
        "chain_boundary": (
            "For a chain with m edges, the XX/ZZ generator Gram rank is 2*rank(A_path_m): "
            "full when m is even and deficient by two when m is odd. A uniform m-logical-qubit "
            "compression therefore needs a center-sector caveat."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "schema_version": 1,
        "scope": "independent exact and complex128 checks of claims extracted from the 2026-09-07 audio/manuscript",
        "conventions": {
            "qubit_order": "left-to-right q0 tensor ... tensor q(n-1)",
            "pauli": "P(x|z)=i^(x.z) X^x Z^z",
            "transpose": "ordinary matrix transpose",
            "dagger": "conjugate transpose",
            "star": "entrywise complex conjugation",
            "random_seed": 20260907,
            "dtype": "complex128",
            "tolerance": 2e-13,
        },
        "seven_generator_family": check_seven_generator_family(),
        "general_clifford_inversion_family": check_general_clifford_inversion_family(),
        "pairwise_frame_optimality_dichotomy": check_pairwise_frame_dichotomy(),
        "diagonal_sign_maps": check_sign_map_classification(),
        "commuting_product_deletion": check_deletion_and_heisenberg_claims(),
    }
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
