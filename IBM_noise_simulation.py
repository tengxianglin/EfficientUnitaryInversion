# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Tengxiang Lin
# Full license: IBM_noise_simulation.LICENSE
# License scope and provenance: LICENSE_SCOPE.md

"""
Perform noise simulations on fake IBM Quantum backends to evaluate the fidelity
of quantum circuits under realistic noise.

For each backend in BACKEND_QUBIT_DICT and each Pauli support in
PAULI_SUPPORTS_WITH_GATE:
    - Generate NUM_DATA_SET random unitaries via get_data_set_pauli.
    - Build ideal and noisy circuits with build_circuits.
    - Transpile and simulate using AerSimulator with and without noise.
    - Compute average Choi-state fidelity and append results to file_path.
"""

# Constants
PAULI_SUPPORTS_WITH_GATE = {
    # ---------------------- X ----------------------
    # 2-qubit all-X
    ("X0", "X1", "X0,X1"): ["YI", "IY"],
    # 3-qubit all-X (without XXX)
    ("X0", "X1", "X2", "X0,X1", "X0,X2", "X1,X2"): ["ZZI", "IZZ"],
    # 3-qubit all-X (with XXX)
    ("X0", "X1", "X2", "X0,X1", "X0,X2", "X1,X2", "X0,X1,X2"): [
        "ZII",
        "IZI",
        "ZII",
        "IIZ",
    ],
    # ---------------------- Y ----------------------
    ("Y0", "Y1", "Y0,Y1"): ["ZZI", "IZZ"],
    # ("Y0", "Y1", "Y2", "Y0,Y1", "Y0,Y2", "Y1,Y2"): ["ZZI", "IZZ"],
    ("Y0", "Y1", "Y2", "Y0,Y1", "Y0,Y2", "Y1,Y2", "Y0,Y1,Y2"): [
        "ZII",
        "IZI",
        "ZII",
        "IIZ",
    ],
    # ---------------------- Z ----------------------
    ("Z0", "Z1", "Z2", "Z0,Z1", "Z0,Z2", "Z1,Z2"): ["YYI", "IYY"],
    ("Z0", "Z1", "Z2", "Z0,Z1", "Z0,Z2", "Z1,Z2", "Z0,Z1,Z2"): [
        "YII",
        "IYI",
        "YII",
        "IIY",
    ],
    # 3-qubit cluster Ising model
    ("Z0,X1,Z2", "X0,X1", "X1,X2", "X0", "X1", "X2"): ["IYI", "YXZ"],
}

# Generate Pauli support sets for Ising model with 2 to 6 qubits
for n in range(2, 5):
    pauli_support = tuple(f"Z{i},Z{i+1}" for i in range(n - 1)) + tuple(
        f"X{i}" for i in range(n)
    )
    PAULI_SUPPORTS_WITH_GATE[pauli_support] = [
        "".join("Y" if i % 2 == 0 else "Z" for i in range(n))
    ]

NUM_DATA_SET = 100

FILE_PATH = (
    f"fidelity_results_{time.strftime('%Y%m%d_%H%M%S')}_{NUM_DATA_SET}sample.csv"
)


# Imports
import time
import os, csv
import numpy as np
import quairkit as qk
from tqdm import tqdm
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import state_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from utils.hamiltonian_utils import get_data_set_pauli
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import (
    FakeCairoV2 as Cairo,  # 27 qubit
    FakeOsaka as Osaka,  # 127 qubit
    FakeBrisbane as Brisbane,  # 127 qubit
    FakeMarrakesh as Marrakesh,  # 156 qubit
)

# Initialize QiskitRuntimeService
service = QiskitRuntimeService(
    channel="ibm_cloud",
    token="your token",
    instance="your instance",
)

BACKEND_QUBIT_DICT = {
    Cairo: 27,
    Osaka: 127,
    Brisbane: 127,
    Marrakesh: 156,
}
# Initialize quairkit dtype
qk.set_dtype("complex128")


# Function definitions
def build_circuits(u, num_qubits, num_qubits_cir, gate_solution):
    circuit = QuantumCircuit(num_qubits_cir)
    ideal_circuit = QuantumCircuit(num_qubits_cir)
    for i in range(num_qubits):
        circuit.h(i)
        circuit.cx(i, i + num_qubits)
        ideal_circuit.h(i)
        ideal_circuit.cx(i, i + num_qubits)
    # Apply gates as specified by gate_solution
    for _ in range(2):
        for gate_str in gate_solution:
            for idx, gate in enumerate(gate_str):
                if gate == "X":
                    circuit.x(idx)
                    ideal_circuit.x(idx)
                elif gate == "Y":
                    circuit.y(idx)
                    ideal_circuit.y(idx)
                elif gate == "Z":
                    circuit.z(idx)
                    ideal_circuit.z(idx)
            circuit.unitary(u, list(range(num_qubits)))
            ideal_circuit.unitary(u, list(range(num_qubits)))
    circuit.save_state()
    ideal_circuit.save_state()
    return circuit, ideal_circuit


def closest_unitary_batch(A):
    """Batch version: Calculate the closest unitary matrix to each matrix in A using SVD.
    A: shape (batch, N, N)
    Returns: shape (batch, N, N)
    """
    # SVD: A = U S Vh
    V, _, Wh = np.linalg.svd(A, full_matrices=False)
    return np.matmul(V, Wh)


# Main execution
if __name__ == "__main__":
    for Backend, num_qubits_backend in BACKEND_QUBIT_DICT.items():
        print(f"Testing backend: {Backend} (qubits: {num_qubits_backend})")
        # Initialize the backend
        backend = Backend()
        # Generate noise model from the backend
        noise_model = NoiseModel.from_backend(backend)
        # Initialize ideal simulator
        ideal_simulator = AerSimulator(method="density_matrix")
        # Initialize simulator with noise model
        simulator = AerSimulator(method="density_matrix", noise_model=noise_model)

        for pauli_support, gate_solution in PAULI_SUPPORTS_WITH_GATE.items():
            print(
                f"Testing Pauli support: {pauli_support}, Gate solution: {gate_solution}"
            )
            # Determine the number of qubits based on the gate solution
            num_qubits = len(gate_solution[0])
            num_qubits_cir = num_qubits * 2
            # Generate unitary set for the Pauli support
            unitary_set = get_data_set_pauli(pauli_support, NUM_DATA_SET, num_qubits)

            # Ensure all matrices in unitary_set are unitary (batch processing)
            unitary_set = closest_unitary_batch(np.asarray(unitary_set))
            num_slots = len(gate_solution) * 2 - 1
            fid_list = []

            # Loop over unitaries and measure fidelity
            for u in tqdm(unitary_set, desc="Unitary fidelity", leave=False):
                circuit, ideal_circuit = build_circuits(
                    u, num_qubits, num_qubits_cir, gate_solution
                )
                transpiled_qc = transpile(circuit, simulator)
                transpiled_ideal_qc = transpile(ideal_circuit, ideal_simulator)
                choi_mat = (
                    simulator.run(transpiled_qc).result().data(0)["density_matrix"]
                )
                ideal_choi_mat = (
                    ideal_simulator.run(transpiled_ideal_qc)
                    .result()
                    .data(0)["density_matrix"]
                )
                fid_list.append(state_fidelity(choi_mat, ideal_choi_mat))

            # Calculate average fidelity
            avg_fid = np.mean(fid_list)
            print(f"Average fidelity for {pauli_support}: {avg_fid:.4f}")

            # Write results to CSV file
            file_exists = os.path.exists(FILE_PATH)
            with open(FILE_PATH, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(
                        [
                            "Backend",
                            "Pauli Support",
                            "Num Slots",
                            "Num Qubits Backend",
                            "Average Fidelity",
                        ]
                    )
                writer.writerow(
                    [
                        Backend.backend_name,
                        pauli_support,
                        num_slots,
                        num_qubits_backend,
                        float(np.real(avg_fid)),
                    ]
                )
