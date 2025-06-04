"""
    For unitaries satisfying Theorem 1 and Theorem 5, which can be
    transformed to their inverse, transpose, or conjugate by a Pauli
    operator `V`, this script validates the efficiency of the algorithm
    for finding `V`.

    For unitaries that can be transformed to their inverse and satisfy
    Theorem 3, it gives the anticommuting set solution $\{V_i\}$ for its
    inverse.

    Validates the efficiency and uniqueness of the mapping algorithm
    using a 1-slot Pauli example, with tunable parameters for
    transformation mode, number of qubits, support set size, and sorting
    strategy.

Parameters for tuning:
        MODE        : 'transpose', 'conj', or 'dagger' (transformation mode).
        NUM_QUBITS  : Number of qubits in the Pauli operators.
        TARGET_COUNT: Size of the Pauli support set generated.
        SORT_MODE   : Sorting mode in find_pauli_mapping_operators by the
                                    rows of the GF(2) matrix built from pauli_support.
                                    Options:
                0: No sorting (original order).
                1: Sort by row-sum (number of nonzero entries), then by
                     first-one position.
                2: Sort by first-one position, then by row-sum.
"""

import time
from typing import Set
from utils.hamiltonian_utils import (
    generate_random_pauli,
    generate_qubit_ops,
    find_pauli_mapping_operators,
    is_commuting,
)

# import quairkit as qk
# qk.set_device("cuda:0")

MODE = "dagger"  # Transformation mode: "transpose", "conj", or "dagger"
NUM_QUBITS = 10
TARGET_COUNT = 10**5
SORT_MODE = 0  # Sorting mode for find_pauli_mapping_operators

# V is the unique 1-slot solution.
V = generate_random_pauli(NUM_QUBITS)


def generate_1slot_paulis(
    base_pauli: str, num_qubits: int, target_count: int, mode: str
) -> Set[str]:
    """
    Generate all Pauli terms and filter by mode-specific (anti)commutation.

    Args:
        base_pauli: Reference Pauli string (e.g., "X0,Z1").
        num_qubits: Total number of qubits.
        mode: Transformation mode: "transpose", "conj", or "dagger".

    Returns:
        A set of Pauli strings meeting the specified criteria.
    """
    valid_items: Set[str] = set()
    while len(valid_items) < target_count:
        candidates = generate_qubit_ops(num_qubits, target_count)
        for term in candidates:
            y_count = sum(
                bool(op.strip().upper().startswith("Y")) for op in term.split(",")
            )
            if mode == "transpose":
                should_anti = y_count % 2 == 1
                cond = (should_anti and not is_commuting(base_pauli, term)) or (
                    not should_anti and is_commuting(base_pauli, term)
                )
            elif mode == "conj":
                should_comm = y_count % 2 == 1
                cond = (should_comm and is_commuting(base_pauli, term)) or (
                    not should_comm and not is_commuting(base_pauli, term)
                )
            elif mode == "dagger":
                cond = not is_commuting(base_pauli, term)
            else:
                raise ValueError(f"Unknown mode: {mode}")
            if cond:
                valid_items.add(term)
                if len(valid_items) >= target_count:
                    break
    return valid_items


def main():
    mode = MODE
    num_qubits = NUM_QUBITS
    target_count = TARGET_COUNT
    sort_mode = SORT_MODE

    print(f"Validation 1-slot Pauli V: {V}")
    print(f"Generating Pauli support of size {target_count} for mode='{mode}'...")
    pauli_support = generate_1slot_paulis(V, num_qubits, target_count, mode)
    print(f"Pauli support generated, size: {len(pauli_support)}")

    print(f"Running find_pauli_mapping_operators(mode='{mode}')...")
    start_time = time.time()
    pauli_gate_solution = find_pauli_mapping_operators(
        pauli_support=pauli_support, mode=mode, sort_mode=sort_mode
    )
    elapsed = time.time() - start_time
    print(f"Elapsed time: {elapsed:.6f} seconds")

    # Validate that the only solution is V
    assert len(pauli_gate_solution) == 1 and V in pauli_gate_solution, \
        f"Expected unique solution V, got {pauli_gate_solution}"
    print("Validation passed: unique solution matches V")
    print(f"Result set: {pauli_gate_solution}")


if __name__ == "__main__":
    main()