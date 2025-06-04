"""Robustness analysis of unitary inversion via Choi-state fidelity metrics.

This script implements five Monte-Carlo noise-simulation routines corresponding
to the comb-circuit protocols in our paper:

1. comb_1slot_noise_simulation            : protocol 2a
2. comb_3slot_a_noise_simulation          : protocol 3a
3. comb_3slot_b_noise_simulation          : protocol 3b
4. comb_recurrence_7slot_noise_simulation : protocol 2c
5. comb_recurrence_15slot_noise_simulation: extension of 2c

Usage:
    Call any function with (delta, size, num_qubits) to estimate the
    average Choi-state fidelity of the V-U-V… sequence versus U^\dagger under noise.
"""

SAMPLE_SIZE = 10000  # Number of Monte Carlo samples

from typing import List

import torch
import quairkit as qk
from quairkit.database import bell_state, eye
from quairkit.qinfo import dagger, state_fidelity


from utils.hamiltonian_utils import (
    generate_unitaries,
    is_commuting,
    create_pauli_complete_set,
    build_V_from_base,
    generate_random_pauli,
)
from itertools import combinations

qk.set_dtype("complex128")
# qk.set_device("cuda")


def comb_1slot_noise_simulation(
    delta: float, size: int = 1000, num_qubits: int = 3
) -> float:
    """
    2a: Single-slot comb for inversion of specific unitaries (VUV inversion, Thm. 1slot).

    Compute the average Choi-state fidelity between V U V and U^\dagger for a randomly perturbed unitary.

    - delta: scaling factor for the noise amplitude.
    - size: number of Monte Carlo samples.
    - num_qubits: number of qubits in U.

    Returns:
        Mean fidelity of Choi states between V U V and U^\dagger.
    """
    # 1. Build anti-commuting set S: all Paulis that anti-commute with the chosen base V (excluding V itself)
    #    and commuting set S' (all others, excluding V itself)
    omega = create_pauli_complete_set(num_qubits)
    base = generate_random_pauli(num_qubits)
    S, S_prime = [], []
    for pauli in omega:
        (S_prime if is_commuting(base, pauli) else S).append(pauli)
    pauli_support = S + S_prime

    # 2. Generate parameter batches:
    #    - S: random parameters
    #    - S': random parameters scaled by delta * (sum of |S| params) / (sum of |S'| params)
    #    - t: global time parameter
    params_S = torch.randn(size, len(S))
    params_Sp = torch.randn(size, len(S_prime))
    sum_S = params_S.abs().sum(dim=1, keepdim=True)
    sum_Sp = params_Sp.abs().sum(dim=1, keepdim=True)
    params_Sp *= delta * sum_S / sum_Sp
    t = torch.rand(size, 1)
    params = torch.cat([params_S, params_Sp, t], dim=1)

    # 3. Build batch of noisy unitaries and the V operator, then evaluate Choi-state fidelity
    U_batch = generate_unitaries(pauli_support, params, num_qubits=num_qubits)
    V = build_V_from_base(base, num_qubits)
    bell = bell_state(2 * num_qubits)
    comb_1slot = V @ U_batch @ V
    psi1 = bell.evolve(comb_1slot.kron(eye(2**num_qubits)))
    psi2 = bell.evolve(dagger(U_batch).kron(eye(2**num_qubits)))
    return state_fidelity(psi1, psi2).mean().item()


def comb_3slot_a_noise_simulation(
    delta: float, size: int = 1000, num_qubits: int = 3
) -> float:
    """
    3a: Three-slot comb for H = sum_{i<j} Y_i Y_j + sum_i Y_i on 3 qubits.

    Compute the average Choi-state fidelity of the sequence V0 U V1 U V0 U V1 under noise.

    - delta: scaling factor for the noise amplitude.
    - size: number of Monte Carlo samples.
    - num_qubits: number of qubits in U.

    Returns:
        Mean fidelity of Choi states between the comb with noisy U and U^\dagger.
    """
    # 1. Build anti-commute set S: all non-empty combinations of Y_i (single and two-qubit terms)
    S = [
        ",".join([f"Y{i}" for i in idxs])
        for r in range(1, num_qubits)
        for idxs in combinations(range(num_qubits), r)
    ]
    omega = create_pauli_complete_set(num_qubits)
    S_prime = [p for p in omega if p not in S]
    pauli_support = S + S_prime

    # 2. Generate parameters: S part random, S_prime part scaled by delta
    params_S = torch.randn(size, len(S))
    params_Sp = torch.randn(size, len(S_prime))
    sum_S = params_S.abs().sum(dim=1, keepdim=True)
    sum_Sp = params_Sp.abs().sum(dim=1, keepdim=True)
    params_Sp = params_Sp * (delta * sum_S / sum_Sp)
    t = torch.rand(size, 1)
    params = torch.cat([params_S, params_Sp, t], dim=1)
    U_batch = generate_unitaries(pauli_support, params, num_qubits=num_qubits)

    # 3. Define V0 and V1
    V0 = build_V_from_base("Z0,Z1", num_qubits)
    V1 = build_V_from_base("Z1,Z2", num_qubits)

    # 4. Build composite operator sequence: V0 U V1 U V0 U V1
    comb_3slots = V0 @ U_batch @ V1 @ U_batch @ V0 @ U_batch @ V1
    bell = bell_state(2 * num_qubits)
    psi1 = bell.evolve(comb_3slots.kron(eye(2**num_qubits)))
    psi2 = bell.evolve(dagger(U_batch).kron(eye(2**num_qubits)))
    return state_fidelity(psi1, psi2).mean().item()


def comb_3slot_b_noise_simulation(
    delta: float, size: int = 1000, num_qubits: int = 3
) -> float:
    """
    3b: Three-slot comb for H = Z_0 X_1 Z_2 + sum_i X_i X_{i+1} + sum_i X_i.

    Compute the average Choi-state fidelity of the sequence V0 U V1 U V0 U V1 under noise.

    - delta: scaling factor for the noise amplitude.
    - size: number of Monte Carlo samples.
    - num_qubits: number of qubits in U.

    Returns:
        Mean fidelity of Choi states between the comb with noisy U and U^\dagger.
    """
    # Build anti-commute set S (custom): ['Z0,X1,Z2'] plus all X_i X_{i+1} and X_i terms
    S = (
        ["Z0,X1,Z2"]
        + [f"X{i},X{i+1}" for i in range(num_qubits - 1)]
        + [f"X{i}" for i in range(num_qubits)]
    )
    omega = create_pauli_complete_set(num_qubits)
    S_prime = [p for p in omega if p not in S]
    pauli_support = S + S_prime

    # Construct parameters: S part random, S_prime part scaled by delta
    params_S = torch.randn(size, len(S))
    params_Sp = torch.randn(size, len(S_prime))
    sum_S = params_S.abs().sum(dim=1, keepdim=True)
    sum_Sp = params_Sp.abs().sum(dim=1, keepdim=True)
    params_Sp = params_Sp * (delta * sum_S / sum_Sp)
    t = torch.rand(size, 1)
    params = torch.cat([params_S, params_Sp, t], dim=1)
    U_batch = generate_unitaries(pauli_support, params, num_qubits=num_qubits)

    # Define V0, V1
    V0 = build_V_from_base("Y1", num_qubits)
    V1 = build_V_from_base("Y0,X1,Z2", num_qubits)

    # Build composite operator sequence: V0 U V1 U V0 U V1
    comb_3slots = V0 @ U_batch @ V1 @ U_batch @ V0 @ U_batch @ V1
    bell = bell_state(2 * num_qubits)
    # Compute Choi-state fidelity in batch
    psi1 = bell.evolve(comb_3slots.kron(eye(2**num_qubits)))
    psi2 = bell.evolve(dagger(U_batch).kron(eye(2**num_qubits)))
    return state_fidelity(psi1, psi2).mean().item()


def comb_recurrence_7slot_noise_simulation(
    delta: float, size: int = 1000, num_qubits: int = 3
) -> float:
    """
    2c: Symmetric 7-slot comb via recurrence (Fig.2c).

    Compute the average Choi-state fidelity of the symmetric 7-slot comb
    with U under noise.

    - delta: scaling factor for the noise amplitude.
    - size: number of Monte Carlo samples.
    - num_qubits: number of qubits in U.

    Returns:
        Mean fidelity of Choi states between the comb with noisy U and U^\dagger.
    """
    # 1. Build anti-commute set S: all non-empty combinations of Y_i
    S = [
        ",".join([f"Y{i}" for i in idxs])
        for r in range(1, num_qubits + 1)
        for idxs in combinations(range(num_qubits), r)
    ]
    omega = create_pauli_complete_set(num_qubits)
    S_prime = [p for p in omega if p not in S]
    pauli_support = S + S_prime

    # 2. Generate parameters: S part random, S_prime part scaled by delta
    params_S = torch.randn(size, len(S))
    params_Sp = torch.randn(size, len(S_prime))
    sum_S = params_S.abs().sum(dim=1, keepdim=True)
    sum_Sp = params_Sp.abs().sum(dim=1, keepdim=True)
    params_Sp = params_Sp * (delta * sum_S / sum_Sp)
    t = torch.rand(size, 1)
    params = torch.cat([params_S, params_Sp, t], dim=1)
    U_batch = generate_unitaries(pauli_support, params, num_qubits=num_qubits)

    # 3. Define V0, V1, V2 for the 3-qubit system
    V0 = build_V_from_base("Z0", num_qubits)
    V1 = build_V_from_base("Z1", num_qubits)
    V2 = build_V_from_base("Z2", num_qubits)

    # 4. Build the composite operator sequence for the 7-slot comb
    #    The V sequence is symmetric, with U inserted between each V
    V_seq = [V0, V1, V0, V2] * 2
    comb_7slot = V_seq[0]
    for V in V_seq[1:]:
        comb_7slot = comb_7slot @ U_batch @ V

    # 5. Compute Choi-state fidelity in batch
    bell = bell_state(2 * num_qubits)
    psi1 = bell.evolve(comb_7slot.kron(eye(2**num_qubits)))
    psi2 = bell.evolve(dagger(U_batch).kron(eye(2**num_qubits)))
    return state_fidelity(psi1, psi2).mean().item()


def comb_recurrence_15slot_noise_simulation(
    delta: float, size: int = 1000, num_qubits: int = 4
) -> float:
    """
    2c-extension: 15-slot comb via recurrence.

    Compute the average Choi-state fidelity of the 15-slot comb
    with U under noise.

    - delta: scaling factor for the noise amplitude.
    - size: number of Monte Carlo samples.
    - num_qubits: number of qubits in U.

    Returns:
        Mean fidelity of Choi states between the comb with noisy U and U^\dagger.
    """
    # 1. Build anti-commute set S: all non-empty combinations of Y_i for 4 qubits
    S = [
        ",".join([f"Y{i}" for i in idxs])
        for r in range(1, num_qubits + 1)
        for idxs in combinations(range(num_qubits), r)
    ]
    omega = create_pauli_complete_set(num_qubits)
    S_prime = [p for p in omega if p not in S]
    pauli_support = S + S_prime

    # 2. Generate parameters: S part random, S_prime part scaled by delta
    params_S = torch.randn(size, len(S))
    params_Sp = torch.randn(size, len(S_prime))
    sum_S = params_S.abs().sum(dim=1, keepdim=True)
    sum_Sp = params_Sp.abs().sum(dim=1, keepdim=True)
    params_Sp = params_Sp * (delta * sum_S / sum_Sp)
    t = torch.rand(size, 1)
    params = torch.cat([params_S, params_Sp, t], dim=1)
    U_batch = generate_unitaries(pauli_support, params, num_qubits=num_qubits)

    # 3. Define V0, V1, V2, V3 for the 4-qubit system
    V0 = build_V_from_base("Z0", num_qubits)
    V1 = build_V_from_base("Z1", num_qubits)
    V2 = build_V_from_base("Z2", num_qubits)
    V3 = build_V_from_base("Z3", num_qubits)

    # 4. Build the composite operator sequence for the 15-slot comb
    #    The V sequence is symmetric, with U inserted between each V
    V_seq = [V0, V1, V0, V2, V0, V1, V0, V3] * 2
    comb = V_seq[0]
    for V in V_seq[1:]:
        comb = comb @ U_batch @ V

    # 5. Compute Choi-state fidelity in batch
    bell = bell_state(2 * num_qubits)
    psi1 = bell.evolve(comb.kron(eye(2**num_qubits)))
    psi2 = bell.evolve(dagger(U_batch).kron(eye(2**num_qubits)))
    return state_fidelity(psi1, psi2).mean().item()


if __name__ == "__main__":
    deltas = reversed([0, 0.001, 0.01, 0.1])
    results: List[tuple] = []
    for func in (
        # comb_1slot_noise_simulation,
        # comb_3slot_a_noise_simulation,
        # comb_3slot_b_noise_simulation,
        # comb_recurrence_7slot_noise_simulation,
        comb_recurrence_15slot_noise_simulation,
    ):
        for d in deltas:
            fid = func(d, size=SAMPLE_SIZE)
            print(f"[{func.__name__}] δ = {d:.3f} → fidelity = {fid:.10f}")
            results.append((func.__name__, d, fid))

    import csv

    with open("robustness_results1.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["task", "delta", "fidelity"])
        writer.writerows(results)
