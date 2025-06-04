"""
This script searches for comb circuits that implement a specified
transformation (e.g. dagger, conj, transpose) on Pauli-based unitaries.
You can tweak the following parameters at the top of this file:
    • NUM_SLOTS     – Number of time slots (Pauli gates) in the comb ansatz.
    • TARGET_FUNC   – Target transformation function (dagger, conj, transpose).
    • PAULI_SUPPORTS – List of Hamiltonian Pauli-term supports.
    • RETURN_ALL    – If True, return all found solutions; if False,
                       only indicate whether a solution exists.

Usage:
    # (Optional) Enable GPU acceleration:
    qk.set_device("cuda")

    # Run the search with your settings:
    solutions = search_pauli_solutions(
        target_func=TARGET_FUNC,
        pauli_supports=PAULI_SUPPORTS,
        num_slots=NUM_SLOTS,
        return_all=RETURN_ALL,
    )

    # To save results:
    save_solutions_to_csv("pauli_results.csv", PAULI_SUPPORTS, solutions)

    - Example output for num_slots=1:
        ['iii_iii', 'iiy_iiy', 'iyi_iyi', 'iyy_iyy', 'yii_yii',
         'yiy_yiy', 'yyi_yyi', 'yyy_yyy']
      Each entry represents a single-slot solution for a specific 3-qubit
      Pauli list. For example, 'iiy_iiy' indicates the solution applies
      two I ⊗ I ⊗ Y.
"""

from typing import Callable, List

import torch
from quairkit.qinfo import dagger

from utils.hamiltonian_utils import pauli_gate_solutions
import quairkit as qk

# (Optional) Enable GPU acceleration
# qk.set_device("cuda")
# Set default data type
qk.set_dtype("complex128")

NUM_SLOTS = 1  # Number of time slots in the comb

# Target transformation function (e.g., dagger, conj, transpose)
TARGET_FUNC: Callable[[torch.Tensor], torch.Tensor] = dagger

# Define the sets of Hamiltonian Pauli terms
PAULI_SUPPORTS: List[List[str]] = [
    ["Y0", "Y1", "Y0,Y1"],
    ["Y0", "Y1", "Y2", "Y0,Y1,Y2"],
    ["Y0", "Y1", "Y1,Y2", "Y0,Y2"],
    ["Z0", "Z1", "Z2", "Z0,Z1", "Z0,Z2", "Z1,Z2", "Z0,Z1,Z2"],
]
RETURN_ALL = True  # Whether to return all solutions or just boolean indicating if a solution was found


def search_pauli_solutions(
    target_func: Callable[[torch.Tensor], torch.Tensor],
    pauli_supports: List[List[str]],
    num_slots: int,
    return_all: bool,
) -> List[List[str]]:
    """
    Search for Pauli-gate inversion solutions.

    Args:
        pauli_supports: List of Pauli supports, where each sublist contains Pauli-term strings for a Hamiltonian.
        num_data_set: Number of random data sets to sample for the search.
        num_slots: Number of time slots (gates) in the solution ansatz.
        return_all: If True, return all found solutions; otherwise, return only one.
        target_func: Function to apply as the target transformation.

    Returns:
        List of Pauli supports, where each sublist contains the Pauli-gate solution(s) for the corresponding Hamiltonian.
    """
    return pauli_gate_solutions(
        target_func=target_func,
        pauli_supports=pauli_supports,
        num_slots=num_slots,
        return_all=return_all,
    )


def save_solutions_to_csv(
    filepath: str,
    hamiltonian_terms: List[List[str]],
    solutions: List[List[str]],
) -> None:
    """Write Hamiltonian names and their Pauli solutions to a CSV file."""
    import csv

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pauli_support", "pauli_solution"])
        for h_list, sol in zip(hamiltonian_terms, solutions):
            writer.writerow([str(h_list), ";".join(sol)])


if __name__ == "__main__":
    solutions = search_pauli_solutions(
        target_func=TARGET_FUNC,
        pauli_supports=PAULI_SUPPORTS,
        num_slots=NUM_SLOTS,
        return_all=True,
    )
    print("Solutions for each pauli_support:")
    for h_list, sol in zip(PAULI_SUPPORTS, solutions):
        print(f"pauli_support={h_list} -> solution(s): {sol}")
    # To save the solutions to a CSV file:
    # save_solutions_to_csv("pauli_results.csv", PAULI_SUPPORTS, solutions)
