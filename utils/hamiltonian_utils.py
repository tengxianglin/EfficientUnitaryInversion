import csv
import itertools
import math
import os
import pickle
import random
from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union, Set

import quairkit as qkit
import torch
from quairkit import Circuit, Hamiltonian
from quairkit.database import eye, x, y, z
from quairkit.qinfo import dagger, nkron, pauli_decomposition
from torch.nn import ModuleList
from tqdm import tqdm
import numpy as np
from typing import Set

from .comb import PQCombNet


def build_V_from_base(base_pauli: str, num_qubits: int = 3) -> torch.Tensor:
    """
    Construct a Pauli operator V = ⨂_{i=0..num_qubits-1} P_i from a base string.

    Args:
        base_pauli: Comma-separated Pauli labels (e.g. "Z0,Z2").
        num_qubits: Total number of qubits in the system.

    Returns:
        A torch.Tensor representing the Kronecker product operator V.
    """
    op_map = {"X": x, "Y": y, "Z": z}
    terms = {int(t[1:]): t[0] for t in base_pauli.split(",") if t}
    ops = [(op_map[terms[i]]() if i in terms else eye()) for i in range(num_qubits)]
    return nkron(*ops)


def has_3prod_with_1anti(pauli_support: List[str]) -> bool:
    """
    Check if there exist three terms whose product is in the list with exactly one anticommute pair.

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        bool: True if condition met.
    """
    for combo in itertools.combinations(pauli_support, 3):
        anticomm = sum(
            not is_commuting(x, y) for x, y in itertools.combinations(combo, 2)
        )
        prod = combo[0]
        for term in combo[1:]:
            prod = multiply_paulis(prod, term)
        if prod in pauli_support and anticomm == 1:
            return True
    return False


def generate_v_transpose_param_circuits(num_qubits_u: int) -> ModuleList:
    """
    Generate a list of parameterized circuits V for transposed unitary operations.

    Args:
        num_qubits_u: Number of qubits in the unknown unitary.

    Returns:
        ModuleList: A list of two Circuit objects implementing V transposition.
    """
    num_ancilla_qubits = 2 * num_qubits_u
    total_qubits = num_qubits_u + num_ancilla_qubits
    v_circuits: ModuleList = ModuleList()

    # First circuit: apply universal two-qubit, CX, CZ gates
    circ0 = Circuit(total_qubits)
    for i in range(num_qubits_u):
        anc_x = num_ancilla_qubits - 2 * i - 1
        anc_z = num_ancilla_qubits + i
        circ0.universal_two_qubits([anc_x, anc_z])
        circ0.cx([anc_x, anc_z])
        circ0.cz([anc_x - 1, anc_z])
    v_circuits.append(circ0)

    # Second circuit: apply CZ, CX, universal two-qubit gates
    circ1 = Circuit(total_qubits)
    for i in range(num_qubits_u):
        ctrl_z = 2 * i
        target = total_qubits - i - 1
        circ1.cz([ctrl_z, target])
        circ1.cx([ctrl_z + 1, target])
        circ1.universal_two_qubits([ctrl_z, ctrl_z + 1])
    v_circuits.append(circ1)

    return v_circuits


def get_num_qubits_from_pauli_support(pauli_support: List[str]) -> int:
    """
    Extract the number of qubits from a list of Pauli strings.

    Args:
        pauli_support: List of Pauli operator strings.

    Returns:
        int: Number of qubits (max index + 1).
    """
    return (
        max(
            int(term.strip()[1:])
            for name in pauli_support
            for term in name.split(",")
            if term.strip()[1:].isdigit()
        )
        + 1
    )


def find_identity_subsets_pauli(pauli_support: List[str]) -> List[List[str]]:
    """
    Find non-exhaustive subsets of Pauli strings whose product equals the identity.

    Args:
        pauli_strings: List of Pauli operator strings (e.g., ["X0", "Y1,Z2"]).

    Returns:
        List[List[str]]: List of subsets where the product is identity.
    """
    # Determine number of qubits
    num_qubits = get_num_qubits_from_pauli_support(pauli_support)
    vector_length = 2 * num_qubits

    def pauli_to_vector(pauli_str: str) -> List[int]:
        vec = [0] * vector_length
        op_map: Dict[int, str] = {}
        for term in pauli_str.split(","):
            term = term.strip()
            if not term:
                continue
            op, idx_str = term[0].upper(), term[1:]
            if idx_str.isdigit():
                op_map[int(idx_str)] = op
        for idx, op in op_map.items():
            if op == "X":
                vec[idx] = 1
            elif op == "Z":
                vec[num_qubits + idx] = 1
            elif op == "Y":
                vec[idx] = 1
                vec[num_qubits + idx] = 1
        return vec

    def is_valid_combination(matrix: torch.Tensor, indices: List[int]) -> bool:
        submat = matrix[indices, :]
        ones_count = submat.sum(dim=0)
        return torch.all(ones_count % 2 == 0)

    vectors = [pauli_to_vector(p) for p in pauli_support]
    mat = torch.tensor(vectors, dtype=torch.int)

    rows, _ = mat.shape
    first_col = mat[:, 0]
    ones_idxs = torch.nonzero(first_col == 1, as_tuple=True)[0].tolist()
    zeros_idxs = torch.nonzero(first_col == 0, as_tuple=True)[0].tolist()

    valid_indices_combinations: List[List[int]] = []
    for r in range(0, len(ones_idxs) + 1, 2):
        for ones_comb in itertools.combinations(ones_idxs, r):
            for s in range(len(zeros_idxs) + 1):
                for zeros_comb in itertools.combinations(zeros_idxs, s):
                    combo = sorted(list(ones_comb) + list(zeros_comb))
                    if len(combo) < 3:
                        continue
                    if is_valid_combination(mat, combo):
                        valid_indices_combinations.append(combo)
    return [[pauli_support[i] for i in combo] for combo in valid_indices_combinations]


def generate_random_pauli(num_qubits: int) -> str:
    """
    Generate a random Pauli string for given qubit count.

    Args:
        num_qubits: Number of qubits.

    Returns:
        str: A Pauli string (e.g., "X0,Z1").
    """
    choices = ["I", "X", "Y", "Z"]
    terms: List[str] = []
    while not terms:
        rand_ops = random.choices(choices, k=num_qubits)
        terms = [f"{letter}{i}" for i, letter in enumerate(rand_ops) if letter != "I"]
    return ",".join(terms)


def create_pauli_complete_set(num_qubits: int) -> List[str]:
    """
    Generate all possible non-identity Pauli strings with caching.

    Args:
        num_qubits: Number of qubits.

    Returns:
        List[str]: All Pauli strings excluding identity.
    """
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"paulis_{num_qubits}.pkl")

    if os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print(f"Cache {cache_file} corrupted, regenerating...")

    letters = ["I", "X", "Y", "Z"]
    all_paulis: List[str] = []
    for combo in itertools.product(letters, repeat=num_qubits):
        if any(letter != "I" for letter in combo):
            terms = [f"{letter}{i}" for i, letter in enumerate(combo) if letter != "I"]
            all_paulis.append(",".join(terms))

    with open(cache_file, "wb") as f:
        pickle.dump(all_paulis, f)
    return all_paulis


def generate_qubit_ops(
    num_qubits: int,
    num_items: int,
    conditions: Dict[Callable, List] = {},
) -> List[str]:
    """
    Generate Hamiltonian operators satisfying specified evaluation conditions.

    Args:
        num_qubits: Number of qubits.
        num_items: Number of operators to generate.
        conditions: Dict mapping evaluation functions to expected values.

    Returns:
        List[str]: Generated Pauli operator strings.
    """

    def multiply_pauli_support(paulis: List[str]) -> str:
        if not paulis:
            return ""
        result = paulis[0]
        for term in paulis[1:]:
            result = multiply_paulis(result, term)
        return result

    h_type_expected = None
    for func, exp in conditions.items():
        if func.__name__ == "H_type" and exp:
            h_type_expected = exp[0]
            break

    generated: List[str] = []
    pool = set(create_pauli_complete_set(num_qubits))

    if h_type_expected is None:
        max_possible = 4**num_qubits - 1  # Subtract 1 to exclude identity

        if num_items > max_possible:
            raise ValueError(
                f"Cannot generate {num_items} operators: maximum possible is {max_possible}"
            )

        # If num_items is close to max_possible (>75%), generate all and sample
        if num_items * 1.618 > max_possible:
            complete_pauli_set = create_pauli_complete_set(num_qubits)
            return random.sample(complete_pauli_set, num_items)

        # Otherwise, generate randomly with checking for duplicates
        result = set()
        while len(result) < num_items:
            pauli = generate_random_pauli(num_qubits)
            result.add(pauli)

        return list(result)

    elif h_type_expected == "1":
        while len(generated) < num_items and pool:
            new_term = random.choice(list(pool))
            generated.append(new_term)
            pool.remove(new_term)
            to_remove: set = set()
            for k in range(2, len(generated) + 1, 2):
                for combo in itertools.combinations(generated, k):
                    prod = multiply_pauli_support(list(combo))
                    if prod:
                        to_remove.add(prod)
            pool -= to_remove

    elif h_type_expected == "1.2":
        if num_items < 5:
            raise ValueError("Type-1.2 requires at least 5 items.")
        k_val = random.randint(1, num_items - 4)
        base_count = num_items - k_val
        while len(generated) < base_count and pool:
            new_term = random.choice(list(pool))
            generated.append(new_term)
            pool.remove(new_term)
            remove_set: set = set()
            for combo in itertools.combinations(generated, 2):
                prod = multiply_pauli_support(list(combo))
                remove_set.add(prod)
            pool -= remove_set
        temp_pool = set(create_pauli_complete_set(num_qubits)) - set(generated)
        all_combos: List[Tuple[str, ...]] = []
        for count in range(4, len(generated) + 1, 2):
            all_combos.extend(itertools.combinations(generated, count))
        random.shuffle(all_combos)
        for combo in all_combos:
            if len(generated) >= num_items or not temp_pool:
                break
            prod = multiply_pauli_support(list(combo))
            if prod in temp_pool and all(
                multiply_paulis(prod, term) not in generated for term in generated
            ):
                generated.append(prod)
                temp_pool.remove(prod)
        if conditions.get(H_type) and H_type(generated) != "1.2":
            return generate_qubit_ops(num_qubits, num_items, conditions)
        if len(generated) < num_items:
            pool = set(create_pauli_complete_set(num_qubits)) - set(generated)
            remove_set: set = set()
            for combo in itertools.combinations(generated, 2):
                remove_set.add(multiply_pauli_support(list(combo)))
            pool -= remove_set
            while len(generated) < num_items and pool:
                new_term = random.choice(list(pool))
                generated.append(new_term)
                pool.remove(new_term)
                remove_set = {
                    multiply_pauli_support([generated[i], generated[j]])
                    for i, j in itertools.combinations(range(len(generated)), 2)
                }
                pool -= remove_set

    elif h_type_expected == "2.1":
        first = random.choice(list(pool))
        generated.append(first)
        pool.remove(first)
        pool = {term for term in pool if is_commuting(first, term)}
        second = random.choice(list(pool))
        generated.append(second)
        pool.remove(second)
        pool = {term for term in pool if is_commuting(second, term)}
        third = multiply_paulis(first, second)
        if third in pool:
            generated.append(third)
            pool.remove(third)
            pool = {term for term in pool if is_commuting(third, term)}
        while len(generated) < num_items and pool:
            term = random.choice(list(pool))
            generated.append(term)
            pool.remove(term)
            pool = {t for t in pool if is_commuting(term, t)}

    elif h_type_expected == "2.2.1":
        k_val = random.randint(1, num_items - 3)
        base_count = num_items - k_val
        first = random.choice(list(pool))
        generated.append(first)
        pool.remove(first)
        comm_pool = {t for t in pool if is_commuting(first, t)}
        while len(generated) < base_count and comm_pool:
            cand = random.choice(list(comm_pool))
            if all(is_commuting(cand, g) for g in generated):
                generated.append(cand)
                pool.remove(cand)
            comm_pool.discard(cand)
        anti_commute_candidates = [
            t for t in pool if any(not is_commuting(t, g) for g in generated)
        ]
        if not anti_commute_candidates:
            return []
        p_term = random.choice(anti_commute_candidates)
        generated.append(p_term)
        pool.remove(p_term)
        commute_with_p = [t for t in generated[:-1] if is_commuting(t, p_term)]
        for term in commute_with_p:
            prod = multiply_paulis(p_term, term)
            if prod and prod in pool:
                generated.append(prod)
                pool.remove(prod)
            if len(generated) >= num_items:
                break

    elif h_type_expected == "2.2.2":
        k_groups = random.randint(1, (num_items + 2) // 3)
        for _ in tqdm(range(k_groups), desc="Generating anti-commuting groups"):
            if len(generated) + 3 > num_items:
                break
            term1 = random.choice(list(pool))
            candidates = [t for t in pool if not is_commuting(term1, t)]
            if not candidates:
                continue
            term2 = random.choice(candidates)
            term3 = multiply_paulis(term1, term2)
            if term3 and term3 in pool:
                new_group = {term1, term2, term3}
                existing = [
                    set(generated[i : i + 3]) for i in range(0, len(generated), 3)
                ]
                if new_group not in existing:
                    generated.extend([term1, term2, term3])
                    pool -= {term1, term2, term3}
        for _ in tqdm(
            range(num_items - len(generated)), desc="Filling remaining slots"
        ):
            if not pool:
                break
            term = random.choice(list(pool))
            generated.append(term)
            pool.remove(term)

    for func, expected in conditions.items():
        if expected is not None and func != H_type and func(generated) not in expected:
            return generate_qubit_ops(num_qubits, num_items, conditions)
    return generated


def multiply_paulis(pauli_a: str, pauli_b: str) -> str:
    """
    Multiply two Pauli strings and return the resulting Pauli string.

    Args:
        pauli_a: First Pauli string.
        pauli_b: Second Pauli string.

    Returns:
        str: Product Pauli string.
    """
    if not pauli_a:
        return pauli_b
    if not pauli_b:
        return pauli_a

    dict_a: Dict[int, str] = {}
    dict_b: Dict[int, str] = {}
    for term in pauli_a.split(","):
        op, idx_str = term[0], term[1:]
        if idx_str.isdigit():
            dict_a[int(idx_str)] = op
    for term in pauli_b.split(","):
        op, idx_str = term[0], term[1:]
        if idx_str.isdigit():
            dict_b[int(idx_str)] = op

    result_terms: List[str] = []
    for pos in sorted(set(dict_a.keys()) | set(dict_b.keys())):
        op_a = dict_a.get(pos, "I")
        op_b = dict_b.get(pos, "I")
        if op_a == "I":
            if op_b != "I":
                result_terms.append(f"{op_b}{pos}")
        elif op_b == "I":
            result_terms.append(f"{op_a}{pos}")
        elif op_a == op_b:
            continue
        elif sorted([op_a, op_b]) == ["X", "Y"]:
            result_terms.append(f"Z{pos}")
        elif sorted([op_a, op_b]) == ["X", "Z"]:
            result_terms.append(f"Y{pos}")
        elif sorted([op_a, op_b]) == ["Y", "Z"]:
            result_terms.append(f"X{pos}")
    return ",".join(result_terms) if result_terms else ""


def is_commuting(pauli_a: str, pauli_b: str) -> bool:
    """
    Check if two Pauli strings commute.

    Args:
        pauli_a: First Pauli string.
        pauli_b: Second Pauli string.

    Returns:
        bool: True if they commute, False otherwise.
    """
    dict_a: Dict[int, str] = {}
    dict_b: Dict[int, str] = {}
    for term in pauli_a.split(","):
        op, idx_str = term[0], term[1:]
        if idx_str.isdigit():
            dict_a[int(idx_str)] = op
    for term in pauli_b.split(","):
        op, idx_str = term[0], term[1:]
        if idx_str.isdigit():
            dict_b[int(idx_str)] = op

    anticommute_count = 0
    for pos in set(dict_a.keys()) & set(dict_b.keys()):
        op_a = dict_a[pos]
        op_b = dict_b[pos]
        if op_a != op_b and sorted([op_a, op_b]) in [
            ["X", "Y"],
            ["Y", "Z"],
            ["X", "Z"],
        ]:
            anticommute_count += 1
    return anticommute_count % 2 == 0


def is_type_1(pauli_support: List[str]) -> bool:
    """
    Check if list of Pauli strings satisfies type-1 Hamiltonian conditions.

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        bool: True if type-1, False otherwise.
    """
    return all(
        multiply_paulis(a, b) not in pauli_support
        for a, b in itertools.combinations(pauli_support, 2)
    )


def is_type_1_2(pauli_support: List[str]) -> bool:
    """
    Check if list of Pauli strings satisfies type-1.2 conditions.

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        bool: True if type-1.2, False otherwise.
    """
    if len(pauli_support) <= 3:
        return False
    for count in range(5, len(pauli_support) + 1, 2):
        for combo in itertools.combinations(pauli_support, count):
            product = combo[0]
            for term in combo[1:]:
                product = multiply_pauli_support(product, term)
            if product == "":
                return True
    return False


def get_data_set_pauli(
    pauli_support: List[str],
    size: int,
    num_qubits: int,
    sigma: float = 1.0,
    data_type: str = "train",
) -> torch.Tensor:
    """
    Generate dataset of unitaries for Hamiltonian sampling.

    Args:
        pauli_support: List of Pauli operator strings.
        size: Number of samples.
        num_qubits: Number of qubits.
        sigma: Noise standard deviation for training.
        data_type: 'train' for normal distribution, else uniform range.

    Returns:
        torch.Tensor: Stack of generated unitaries.
    """
    if data_type == "train":
        params = torch.randn(size, len(pauli_support) + 1) * sigma
    else:
        params = torch.rand(size, len(pauli_support) + 1) * sigma * 100 - sigma * 50
    return generate_unitaries(pauli_support, params, num_qubits)


def generate_unitaries(
    pauli_support: List[str], params: torch.Tensor, num_qubits: int
) -> torch.Tensor:
    """
    Internal: generate unitary matrices from Hamiltonian parameters.

    Args:
        pauli_support: List of Pauli operator strings.
        params: Tensor of shape (batch, len(pauli_support)+1).
        num_qubits: Number of qubits.

    Returns:
        torch.Tensor: Tensor of unitaries.
    """
    unitaries: List[torch.Tensor] = []
    for row in params:
        *coeffs, t = row.tolist()
        ham = Hamiltonian(
            [(coeffs[i], pauli_support[i]) for i in range(len(pauli_support))]
        )
        h_mat = torch.from_numpy(ham.construct_h_matrix(num_qubits)).to(
            qkit.get_device()
        )
        unitary = torch.matrix_exp(-1j * h_mat * t)
        unitaries.append(unitary)
    return torch.stack(unitaries)


def is_type_2_1(pauli_support: List[str]) -> bool:
    """
    Check if all Pauli strings mutually commute (type-2.1).

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        bool: True if all commute.
    """
    return all(is_commuting(a, b) for a, b in itertools.combinations(pauli_support, 2))


def is_type_2_2(pauli_support: List[str]) -> bool:
    """
    Check if there exists at least one non-commuting pair (type-2.2).

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        bool: True if any pair anticommutes.
    """
    return any(
        not is_commuting(a, b) for a, b in itertools.combinations(pauli_support, 2)
    )


def is_type_2_2_1(pauli_support: List[str]) -> bool:
    """
    Check type-2.2.1: for any a*b=c in list, all three commute.

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        bool: True if condition met.
    """
    for a, b in itertools.combinations(pauli_support, 2):
        prod = multiply_paulis(a, b)
        if prod in pauli_support:
            c = prod
            if not (is_commuting(a, b) and is_commuting(b, c) and is_commuting(a, c)):
                return False
    return True


def H_type(pauli_support: List[str]) -> str:
    """
    Determine Hamiltonian type for a set of Pauli operators.

    Args:
        pauli_support: List of Pauli strings.

    Returns:
        str: One of '1', '1.2', '2.1', '2.2.1', '2.2.2', or 'unknown'.
    """
    if is_type_1(pauli_support):
        return "1.2" if is_type_1_2(pauli_support) else "1"
    elif is_type_2_1(pauli_support):
        return "2.1"
    elif is_type_2_2(pauli_support):
        return "2.2.1" if is_type_2_2_1(pauli_support) else "2.2.2"
    else:
        return "unknown"


def get_pauli_decomposition_properties(
    pauli_support: List[str],
    num_qubits: int,
    threshold: float = 1e-10,
    samples: int = 100,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Compute Pauli decomposition masks (real, imag, zero) for Hamiltonians.

    Args:
        pauli_support: List of Pauli strings.
        num_qubits: Number of qubits.
        threshold: Value threshold.
        samples: Number of random samples.

    Returns:
        Tuple of Tensors: (is_real, is_imag, is_zero) masks.
    """
    params = torch.randn(samples, len(pauli_support) + 1)
    units = generate_unitaries(pauli_support, params, num_qubits)
    decomps = torch.stack([pauli_decomposition(u) for u in units])
    phase = torch.exp(1j * torch.angle(decomps[:, 0])).unsqueeze(1)
    decomps = decomps / phase

    is_real = torch.all(torch.abs(decomps.imag) < threshold, dim=0)
    is_imag = torch.all(torch.abs(decomps.real) < threshold, dim=0)
    is_zero = torch.all(torch.abs(decomps) < threshold, dim=0)
    return is_real, is_imag, is_zero


def has_complex_pauli(pauli_support: List[str], threshold: float = 1e-10) -> bool:
    """
    Check if Pauli decomposition contains complex terms.

    Args:
        pauli_support: List of Pauli strings.
        threshold: Threshold for zero.

    Returns:
        bool: True if complex terms exist.
    """
    num_qubits = get_num_qubits_from_pauli_support(pauli_support)
    is_real, is_imag, is_zero = get_pauli_decomposition_properties(
        pauli_support, num_qubits, threshold
    )
    return any(
        not (is_real[i] or is_imag[i] or is_zero[i]) for i in range(len(is_zero))
    )


def pauli_decomp(pauli_support: List[str], threshold: float = 1e-10) -> str:
    """
    Return string representation of non-zero Pauli decomposition terms.

    Args:
        pauli_support: List of Pauli strings.
        threshold: Zero threshold.

    Returns:
        str: String of terms (e.g., 'r*I+i*X+...').
    """
    num_qubits = get_num_qubits_from_pauli_support(pauli_support)
    is_real, is_imag, is_zero = get_pauli_decomposition_properties(
        pauli_support, num_qubits, threshold
    )
    types: List[str] = []
    total_terms = 4**num_qubits
    for i in range(total_terms):
        if is_zero[i]:
            types.append("0")
        elif is_real[i]:
            types.append("r")
        elif is_imag[i]:
            types.append("i")
        else:
            types.append("c")
    pauli_basis = [
        "".join(p) for p in itertools.product(["I", "X", "Y", "Z"], repeat=num_qubits)
    ]
    terms: List[str] = [f"{et}*{p}" for et, p in zip(types, pauli_basis) if et != "0"]
    return "+".join(terms) if terms else "0"


def find_fixed_size_identity_subsets(
    pauli_support: List[str], size: int
) -> List[List[str]]:
    """
    Find all subsets of given size whose product is identity.

    Args:
        pauli_support: List of Pauli strings.
        size: Subset size.

    Returns:
        List of subsets (each a list of strings).
    """

    def prod_terms(terms: List[str]) -> str:
        result = terms[0]
        for t in terms[1:]:
            result = multiply_paulis(result, t)
        return result

    valid: List[List[str]] = []
    for combo in itertools.combinations(pauli_support, size):
        if prod_terms(list(combo)) == "":
            valid.append(list(combo))
    return valid


def i():
    """Identity gate function"""
    return eye(2)


def pauli_gate_solutions(
    target_func: Callable[[torch.Tensor], torch.Tensor],
    pauli_supports: Union[List[str], List[List[str]]],
    num_slots: int = 1,
    return_all: bool = False,
    num_data_set: int = 100,
) -> Union[List[str], bool, List[bool]]:
    """
    Search for Pauli gate sequences that invert unknown unitaries.

    Args:
        target_func: Function mapping parameters to unitary.
        pauli_supports: List of Pauli supports or a single pauli support.
        num_slots: Number of slots in the circuit.
        return_all: If True, return all solutions; else only the first found.
        num_data_set: Number of random samples.

    Returns:
        Depending on return_all: solution string, list of flags, or boolean.
    """
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    is_batch = isinstance(pauli_supports[0], list)
    if not is_batch:
        pauli_supports = [pauli_supports]
    # Group by num_qubits, use index for mapping
    qubit_groups = defaultdict(list)
    index_groups = defaultdict(list)
    for idx, h_list in enumerate(pauli_supports):
        num_qubits = get_num_qubits_from_pauli_support(h_list)
        qubit_groups[num_qubits].append(h_list)
        index_groups[num_qubits].append(idx)  # Use index for mapping

    all_results = {}  # Store results

    for computed_qubits, group in qubit_groups.items():
        batch_U = []
        group_indices = index_groups[computed_qubits]

        for h_list in group:
            num_param = len(h_list) + 1
            params = torch.randn(num_data_set, num_param)
            U = generate_unitaries(h_list, params, computed_qubits)
            batch_U.append(U)

        U_batch = torch.stack(batch_U)
        identity = eye(2**computed_qubits)
        result_flags = [False] * len(group)

        pauli_counts = computed_qubits * (num_slots + 1)
        pauli_combinations_cache = os.path.join(
            cache_dir, f"pauli_combinations_{pauli_counts}pauli.pkl"
        )
        # Try to load cached Pauli combinations
        if os.path.exists(pauli_combinations_cache):
            try:
                with open(pauli_combinations_cache, "rb") as f:
                    pauli_combinations = pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                print(
                    f"Cache file {pauli_combinations_cache} is corrupted, regenerating..."
                )
                pauli_combinations = list(
                    itertools.product([i, x, y, z], repeat=pauli_counts)
                )
                with open(pauli_combinations_cache, "wb") as f:
                    pickle.dump(pauli_combinations, f)
        else:
            print(
                f"Generating new Pauli combinations cache file: {pauli_combinations_cache}"
            )
            pauli_combinations = list(
                itertools.product([i, x, y, z], repeat=pauli_counts)
            )
            with open(pauli_combinations_cache, "wb") as f:
                pickle.dump(pauli_combinations, f)

        # Search for solutions in the current group
        results_by_group = [
            [] for _ in range(len(group))
        ]  # Store results for each H in group

        # Initialize active_indices and current_U_batch
        if return_all:
            current_U_batch = U_batch
        else:
            active_indices = [idx for idx in range(len(group)) if not result_flags[idx]]
            current_U_batch = U_batch[active_indices] if active_indices else None

        found_new_solution = False  # Initialize before the loop
        for pauli_support in tqdm(
            pauli_combinations, desc="Testing Pauli combinations", leave=False
        ):
            result = "_".join(
                [
                    "".join(
                        [
                            pauli.__name__
                            for pauli in pauli_support[
                                computed_qubits * j : computed_qubits * (j + 1)
                            ]
                        ]
                    )
                    for j in range(num_slots + 1)
                ]
            )

            if return_all:
                current_U_batch = U_batch
            elif found_new_solution:
                # Find indices that have not found a solution yet
                active_indices = [
                    idx for idx in range(len(group)) if not result_flags[idx]
                ]

                # If all have found solutions, exit early
                if not active_indices:
                    break

                current_U_batch = U_batch[active_indices]

            guessed_unitary_list = []
            for j in range(num_slots, -1, -1):
                if j < num_slots:
                    unitary = current_U_batch
                else:
                    unitary = dagger(target_func(current_U_batch))
                start_idx = computed_qubits * j
                end_idx = computed_qubits * (j + 1)
                pauli_ops = [pauli() for pauli in pauli_support[start_idx:end_idx]]
                guessed_unitary_list.append(unitary @ nkron(*pauli_ops))

            guessed_unitary = guessed_unitary_list[0]
            for j in range(1, num_slots + 1):
                guessed_unitary = guessed_unitary @ guessed_unitary_list[j]

            guessed_unitary = guessed_unitary / torch.exp(
                1j * guessed_unitary[..., 0, 0].angle().unsqueeze(-1).unsqueeze(-1)
            )

            # Batch check which guessed_unitary equals identity
            is_identity = torch.all(
                torch.isclose(guessed_unitary, identity), dim=(-2, -1)
            )
            # Save results for each item in the group
            if return_all:
                if isinstance(is_identity, bool):
                    is_identity = [is_identity] * len(group)
                else:
                    is_identity = is_identity.tolist()
                for idx, flag in enumerate(is_identity):
                    if all(flag):
                        results_by_group[idx].append(result)
            else:
                # Check if new solution found
                found_new_solution = False
                if isinstance(is_identity, bool):
                    is_identity = [is_identity] * len(active_indices)
                else:
                    is_identity = is_identity.tolist()
                for batch_idx, group_idx in enumerate(active_indices):
                    if all(is_identity[batch_idx]):
                        result_flags[group_idx] = True
                        found_new_solution = True

        # Save results according to return_all
        if return_all:
            for orig_idx, group_results in zip(group_indices, results_by_group):
                all_results[orig_idx] = group_results
        else:
            for orig_idx, flag in zip(group_indices, result_flags):
                all_results[orig_idx] = flag
    if is_batch:
        return [all_results[i] for i in range(len(pauli_supports))]
    else:
        return all_results[0]


class HamiltonianPQCombNet:
    """
    Class implementing PQCombNet-based search for efficient inversion of unitaries.
    """

    LOG_SEARCH = "[SEARCH]"
    LOG_CONFIG = "[SEARCH CONFIG]"
    LOG_SAMPLE = "[SAMPLE SEARCH]"
    LOG_LIST = "[LIST SEARCH]"
    LOG_RECALC = "[RECALCULATE]"
    LOG_EVAL = "[EVALUATION]"

    def __init__(
        self,
        target_func: Callable[[torch.Tensor], torch.Tensor],
        task_name: str,
        num_qubits: int = 2,
        v_circuits: Optional[Iterable[Circuit]] = None,
        fidelity_threshold: float = 0.999,
        num_train_set: int = 1000,
        num_test_set: int = 1000,
        save_dir: str = "results",
    ):
        """
        Initialize HamiltonianPQCombNetwork.

        Args:
            target_func: Target unitary function.
            task_name: Identifier for the task.
            num_qubits: Number of qubits.
            v_circuits: Optional list of V circuits.
            fidelity_threshold: Fidelity cutoff for success.
            num_train: Training set size.
            num_test: Testing set size.
            save_dir: Directory to save results.
        """
        self.target_func = target_func
        self.task_name = task_name
        self.num_qubits = num_qubits
        self.v_circuits = v_circuits
        self.fidelity_threshold = fidelity_threshold
        self.num_train = num_train_set
        self.num_test = num_test_set
        self.save_dir = os.path.join(os.getcwd(), save_dir, task_name)
        os.makedirs(self.save_dir, exist_ok=True)

        self.evaluation_funcs: Dict[Callable, Optional[List]] = {
            H_type: None,
            has_complex_pauli: None,
            pauli_decomp: None,
        }

    def _get_param_combinations(
        self,
        parallel: Union[int, Tuple[int, int]],
        ancilla: Union[List[int], int],
        slots: Union[int, Tuple[int, int]],
    ) -> List[Tuple[int, int, int]]:
        """
        Generate all combinations of slots and parallel parameters.

        Args:
            slots: Either a single integer or a tuple (min_slots, max_slots) for range
            parallel: Either a single integer or a tuple (min_parallel, max_parallel) for range
            ancilla: Either a single integer or a tuple (min_ancilla, max_ancilla) for range

        Returns:
            List of tuples (num_parallels, ancilla, num_slots) for all combinations
        """
        # Convert single integers to ranges with the same start and end
        slots_range = (
            [slots] if isinstance(slots, int) else list(range(slots[0], slots[1] + 1))
        )
        parallel_range = (
            [parallel]
            if isinstance(parallel, int)
            else list(range(parallel[0], parallel[1] + 1))
        )
        ancilla_range = (
            [ancilla]
            if isinstance(ancilla, int)
            else list(range(ancilla[0], ancilla[1] + 1))
        )

        # Generate all combinations of slots and parallel values
        return list(itertools.product(parallel_range, ancilla_range, slots_range))

    def search_config(
        self,
        pauli_support: List[str],
        slots: Union[int, Tuple[int, int]] = None,
        parallel: Union[int, Tuple[int, int]] = 1,
        ancilla: Union[List[int], int] = 0,
        max_attempts: int = 50,
        **train_kwargs,
    ) -> Optional[Dict[str, Union[float, int]]]:
        """
        Search for optimal configuration across multiple parameter combinations.

        Args:
            pauli_support: List of Pauli operator strings.
            slots: Single value or tuple (min, max) for slots.
            parallel: Single value or tuple (min, max) for parallel circuits.
            ancilla: Ancilla qubit configuration.
            projector: Optional projector for evaluation.
            max_attempts: Maximum search attempts per configuration.
            **train_kwargs: Additional training parameters.

        Returns:
            Best result dictionary or None if evaluation failed.
        """
        if self.v_circuits is not None:
            slots = len(self.v_circuits) - 1
        print(
            f"\n{self.LOG_CONFIG} Starting search for Hamiltonian operators: {pauli_support}"
        )
        print(
            f"{self.LOG_CONFIG} Slots parameter: {slots}, Parallel parameter: {parallel}"
        )

        # First evaluate with all functions to check if we should proceed
        if self.evaluation_funcs:
            evaluation_results = {}
            skip_config = False
            for func, expected_values in self.evaluation_funcs.items():
                result = func(pauli_support)
                evaluation_results[func.__name__] = result

                if expected_values is not None and result not in expected_values:
                    print(
                        f"{self.LOG_EVAL} Skipping configuration because {func.__name__}={result} not in {expected_values}"
                    )
                    skip_config = True
                    break

            if skip_config:
                return None

        combinations = self._get_param_combinations(
            slots=slots, parallel=parallel, ancilla=ancilla
        )
        print(
            f"{self.LOG_CONFIG} Testing {len(combinations)} different configurations: {combinations}"
        )

        computed_qubits = get_num_qubits_from_pauli_support(pauli_support)
        print(f"{self.LOG_CONFIG} Computed qubits: {computed_qubits}")

        train_set = get_data_set_pauli(
            pauli_support, self.num_train, num_qubits=computed_qubits, data_type="train"
        )
        test_set = get_data_set_pauli(
            pauli_support, self.num_test, num_qubits=computed_qubits, data_type="test"
        )
        print(
            f"{self.LOG_CONFIG} Generated training set size: {len(train_set)}, test set size: {len(test_set)}"
        )

        best_result = None
        # Add tqdm progress bar for configurations
        for idx, (num_parallels, ancilla_val, num_slots) in enumerate(
            tqdm(combinations, desc=f"{self.LOG_CONFIG} Testing configurations")
        ):
            print(
                f"\n{self.LOG_CONFIG} Testing configuration {idx+1}/{len(combinations)}: slots={num_slots}, parallel={num_parallels}"
            )
            result = self.search_single_config(
                pauli_support=pauli_support,
                slots=num_slots,
                parallel=num_parallels,
                ancilla=ancilla_val,
                train_set=train_set,
                test_set=test_set,
                computed_qubits=computed_qubits,
                max_attempts=max_attempts,
                **train_kwargs,
            )
            if result is None:
                continue
            if best_result is None or result["fidelity"] > best_result["fidelity"]:
                best_result = result
                print(
                    f"{self.LOG_CONFIG} New best configuration: slots={num_slots}, parallel={num_parallels}, ancilla={ancilla_val}, fidelity={result['fidelity']:.6f}"
                )

            if result["fidelity"] > self.fidelity_threshold:
                print(
                    f"{self.LOG_CONFIG} Found satisfactory configuration with fidelity {result['fidelity']:.6f}"
                )
                return result

        # If no configuration meets threshold, mark as invalid
        if best_result is not None:
            print(
                f"{self.LOG_CONFIG} No configuration met threshold. Best fidelity: {best_result['fidelity']:.6f}"
            )
            best_result["num_slots"] = -1
            best_result["num_parallels"] = -1
            best_result["repeat"] = -max_attempts
            best_result["ancilla"] = -(
                math.prod(best_result["ancilla"])
                if isinstance(best_result["ancilla"], list)
                else best_result["ancilla"]
            )
        return best_result

    def save_result_incrementally(
        self, result: Optional[Dict[str, Union[float, int]]], base_filename: str
    ):
        """
        Save a single result to a CSV file incrementally.
        Creates the file with headers if it doesn't exist, otherwise appends to it.

        Args:
            result: The result dictionary to save
            base_filename: Base name for the CSV file (without timestamp)
        """
        # Skip if result is None (evaluation check failed)
        if result is None:
            print(
                f"{self.LOG_SEARCH} Skipping result saving - configuration failed evaluation"
            )
            return

        try:
            # Ensure the directory exists (redundant with __init__ but safer)
            os.makedirs(self.save_dir, exist_ok=True)

            # Create filename path
            filepath = os.path.join(self.save_dir, f"{base_filename}.csv")
            print(f"{self.LOG_SEARCH} Attempting to save result to: {filepath}")

            fieldnames = [
                "num_slots",
                "num_parallels",
                "pauli_support",
                "repeat",
                "num_qubits",
                "fidelity",
            ]

            # Add any additional fields from the result
            additional_fields = set(result.keys()) - set(fieldnames)
            if additional_fields:
                fieldnames.extend(sorted(additional_fields))

            # Check if file exists
            file_exists = os.path.isfile(filepath)
            print(f"{self.LOG_SEARCH} File already exists: {file_exists}")

            # Open in append mode if file exists, write mode otherwise
            with open(filepath, "a" if file_exists else "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # Write header only if creating a new file
                if not file_exists:
                    writer.writeheader()
                    print(f"{self.LOG_SEARCH} Created new file with headers")
                else:
                    print(f"{self.LOG_SEARCH} Appending to existing file")

                writer.writerow(result)

            print(f"{self.LOG_SEARCH} Successfully saved result to {filepath}")

        except Exception as e:
            print(f"{self.LOG_SEARCH} ERROR: Failed to save result to file: {str(e)}")
            # Print information about the directory and file
            print(f"{self.LOG_SEARCH} Save directory: {self.save_dir}")
            print(
                f"{self.LOG_SEARCH} Directory exists: {os.path.exists(self.save_dir)}"
            )

    def search_single_config(
        self,
        pauli_support: List[str],
        slots: int,
        parallel: int,
        ancilla: Union[List[int], int] = 0,
        train_set: Optional[torch.Tensor] = None,
        test_set: Optional[torch.Tensor] = None,
        computed_qubits: Optional[int] = None,
        max_attempts: int = 50,
        **train_kwargs,
    ) -> Optional[Dict]:
        print(
            f"\n{self.LOG_SEARCH} Testing configuration: slots={slots}, parallel={parallel}, ancilla={ancilla}"
        )
        print(f"{self.LOG_SEARCH} Hamiltonian operators: {pauli_support}")

        if computed_qubits is None:
            computed_qubits = get_num_qubits_from_pauli_support(pauli_support)
        print(f"{self.LOG_SEARCH} Number of qubits: {computed_qubits}")

        # Evaluate the pauli_support with all evaluation functions first
        if self.evaluation_funcs:
            evaluation_results = {}
            for func, expected_values in self.evaluation_funcs.items():
                result = func(pauli_support)
                evaluation_results[func.__name__] = result

                # Skip this configuration if the result doesn't match expected values
                if expected_values is not None and result not in expected_values:
                    print(
                        f"{self.LOG_EVAL} Skipping configuration because {func.__name__}={result} is not in {expected_values}"
                    )
                    return None

        if train_set is None:
            train_set = get_data_set_pauli(
                pauli_support,
                self.num_train,
                num_qubits=computed_qubits,
                data_type="train",
            )
        if test_set is None:
            test_set = get_data_set_pauli(
                pauli_support,
                self.num_test,
                num_qubits=computed_qubits,
                data_type="test",
            )
        slot_dim = 2**computed_qubits

        best_fidelity = 0
        best_prob_success = 0
        best_repeat = -1
        fidelities = []
        prob_successes = []

        for attempt in tqdm(
            range(max_attempts), desc=f"{self.LOG_SEARCH} Testing attempts"
        ):
            print(f"{self.LOG_SEARCH} Attempt {attempt+1}/{max_attempts}...")
            task_name = f"{self.task_name}_" + "_".join(pauli_support)
            net = PQCombNet(
                target_function=self.target_func,
                num_slots=slots,
                num_parallels=parallel,
                ancilla=ancilla,
                slot_dim=slot_dim,
                train_unitary_info=train_set,
                test_unitary_info=test_set,
                task_name=task_name,
            )
            if self.v_circuits is not None:
                net.V_circuit_list = self.v_circuits
            else:
                V_circuit_list = torch.nn.ModuleList()
                system_dim_list = (
                    [2] * ancilla if isinstance(ancilla, int) else ancilla
                ) + [slot_dim] * parallel
                for _ in range(slots + 1):
                    cir = Circuit(system_dim=system_dim_list)
                    for _ in range(4):
                        cir.universal_qudits(range(len(system_dim_list)))
                    V_circuit_list.append(cir)
                net.V_circuit_list = V_circuit_list

            # Prepare train_kwargs, set is_save_data=False if not provided
            train_args = dict(train_kwargs)
            train_args.setdefault("is_save_data", False)
            train_args.setdefault("verbose", False)

            # Always call net.train and unpack results
            train_results = net.train(**train_args)
            prob_success = (
                -1 if train_args.get("projector") is None else train_results[2]
            )
            fidelity = train_results[1]
            fidelities.append(fidelity)
            prob_successes.append(prob_success)
            print(f"{self.LOG_SEARCH} Attempt {attempt+1} fidelity: {fidelity:.6f}")

            if fidelity > best_fidelity:
                best_fidelity = fidelity
                best_prob_success = prob_success
                best_repeat = attempt
                print(
                    f"{self.LOG_SEARCH} New best fidelity: {best_fidelity:.6f}, new best prob_success: {best_prob_success:.6f}"
                )

            if fidelity > self.fidelity_threshold:
                print(
                    f"{self.LOG_SEARCH} Success! Fidelity {fidelity:.6f} exceeds threshold {self.fidelity_threshold}"
                )
                result = {
                    "num_slots": slots,
                    "num_parallels": parallel,
                    "pauli_support": pauli_support,
                    "repeat": best_repeat,
                    "fidelity": best_fidelity,
                    "prob_success": best_prob_success,
                    "num_qubits": computed_qubits,
                    "ancilla": ancilla,
                }
                if self.evaluation_funcs:
                    result |= evaluation_results
                return result

        avg_fidelity = sum(fidelities) / len(fidelities) if fidelities else 0
        avg_prob_success = (
            sum(prob_successes) / len(prob_successes) if prob_successes else 0
        )
        result = {
            "num_slots": -1,
            "num_parallels": -1,
            "ancilla": -ancilla,
            "pauli_support": pauli_support,
            "repeat": -max_attempts,
            "fidelity": avg_fidelity,
            "prob_success": avg_prob_success,
            "num_qubits": computed_qubits,
        }
        if self.evaluation_funcs:
            result |= evaluation_results
        return result

    def search_from_samples(
        self,
        num_samples: int,
        num_item: int,
        num_qubits: int,
        slots: Union[int, Tuple[int, int]],
        parallel: Union[int, Tuple[int, int]],
        ancilla: Union[List[int], int],
        max_attempts: int = 50,
        max_skips: int = 10000,
        **train_kwargs,
    ) -> List[Dict[str, Union[float, int]]]:
        """
        Search configurations from randomly generated samples.

        Args:
            num_samples: Number of samples to generate.
            num_item: Number of operators per sample.
            num_qubits: Number of qubits.
            slots: Slot configuration.
            parallel: Parallel configuration.
            ancilla: Ancilla configuration.
            projector: Optional projector.
            max_attempts: Max attempts per configuration.
            max_skips: Max consecutive skips allowed.

        Returns:
            List of valid results.
        """
        print(
            f"\n{self.LOG_SAMPLE} Starting search from {num_samples} random samples with {num_item} Hamiltonian operators each"
        )

        results = []
        base_filename = f"samples_{num_item}terms"

        valid_samples = 0
        consecutive_skips = 0  # Counter for consecutive invalid samples

        # Add tqdm progress bar for samples
        while valid_samples < num_samples:
            print(
                f"\n{self.LOG_SAMPLE} Processing sample {valid_samples + 1}/{num_samples} (Skips: {consecutive_skips})"
            )

            # Check if max skips exceeded
            if consecutive_skips >= max_skips:
                print(
                    f"{self.LOG_SAMPLE} WARNING: Exceeded maximum number of skips ({max_skips})"
                )
                print(
                    f"{self.LOG_SAMPLE} Returning empty results due to too many consecutive skips"
                )
                return []  # Return empty list instead of recording failure

            pauli_support = generate_qubit_ops(num_qubits, num_item)
            print(f"{self.LOG_SAMPLE} Generated operators: {pauli_support}")

            # Check if operators pass all evaluations
            skip_sample = False
            for func, expected_values in self.evaluation_funcs.items():
                if expected_values is not None:
                    result = func(pauli_support)
                    if result not in expected_values:
                        print(
                            f"{self.LOG_SAMPLE} Skip: {func.__name__}={result} not in {expected_values}"
                        )
                        skip_sample = True
                        break

            if skip_sample:
                consecutive_skips += 1
                print(
                    f"{self.LOG_SAMPLE} Sample skipped (consecutive skips: {consecutive_skips})"
                )
                continue

            # Try to find a valid configuration
            result = self.search_config(
                pauli_support=pauli_support,
                slots=slots,
                parallel=parallel,
                ancilla=ancilla,
                max_attempts=max_attempts,
                **train_kwargs,
            )

            # Only append and save if result is not None
            if result is not None:
                results.append(result)
                # Save each result incrementally
                self.save_result_incrementally(result, base_filename)
                print(
                    f"{self.LOG_SAMPLE} Sample {valid_samples + 1} completed with fidelity: {result['fidelity']:.6f}"
                )
                valid_samples += 1
                consecutive_skips = 0 # Reset skip counter on success
            else:
                consecutive_skips += 1
                print(
                    f"{self.LOG_SAMPLE} Sample skipped - failed evaluation (consecutive skips: {consecutive_skips})"
                )

        print(
            f"\n{self.LOG_SAMPLE} All {num_samples} samples completed. Valid results saved to {base_filename}.csv"
        )
        return results

    def search_from_list(
        self,
        pauli_supports: List[List[str]],
        slots: Union[int, Tuple[int, int]],
        parallels: Union[int, Tuple[int, int]],
        ancilla: Union[List[int], int],
        max_attempts: int = 50,
        output_filename: str = "from_list",
        **train_kwargs,
    ) -> List[Dict[str, Union[float, int]]]:
        """
        Search configurations from predefined lists of Pauli operators.

        Args:
            pauli_supports: List of Pauli supports.
            slots: Slot configuration.
            parallel: Parallel configuration.
            ancilla: Ancilla configuration.
            max_attempts: Max attempts per configuration.
            base_filename: Base filename for saving results.

        Returns:
            List of valid results.
        """
        print(
            f"\n{self.LOG_LIST} Starting search from {len(pauli_supports)} predefined Hamiltonian operator lists"
        )

        results = []

        # Add tqdm progress bar for lists
        for i, pauli_support in enumerate(
            tqdm(pauli_supports, desc=f"{self.LOG_LIST} Processing lists")
        ):
            print(f"\n{self.LOG_LIST} Processing list {i+1}/{len(pauli_supports)}")
            print(f"{self.LOG_LIST} Operators: {pauli_support}")
            result = self.search_config(
                pauli_support=pauli_support,
                slots=slots,
                parallel=parallels,
                ancilla=ancilla,
                max_attempts=max_attempts,
                **train_kwargs,
            )

            # Only append and save if result is not None
            if result is not None:
                results.append(result)
                # Save each result incrementally
                self.save_result_incrementally(result, output_filename)
                print(
                    f"{self.LOG_LIST} List {i+1} completed with fidelity: {result['fidelity']:.6f}"
                )
            else:
                print(
                    f"{self.LOG_LIST} List {i+1} skipped - failed evaluation criteria"
                )

        print(
            f"\n{self.LOG_LIST} All {len(pauli_supports)} lists completed. Valid results saved to {output_filename}.csv"
        )
        return results

    def save_results(self, results: List[Dict[str, Union[float, int]]], filename: str):
        """
        Save multiple results to a CSV file with timestamp.

        Args:
            results: List of result dictionaries to save.
            filename: Base filename for the CSV file.
        """
        filepath = os.path.join(
            self.save_dir, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        # Only include core fields by default
        fieldnames = [
            "num_slots",
            "num_parallels",
            "pauli_support",
            "repeat",
            "num_qubits",
            "fidelity",
        ]

        # Add any additional fields from evaluation functions
        if results:
            additional_fields = set()
            for result in results:
                additional_fields.update(set(result.keys()) - set(fieldnames))
            fieldnames.extend(sorted(additional_fields))

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

    def plot(self, **kwargs):
        r"""
        Plot the quantum comb circuit.

        All arguments are passed directly to Circuit.plot.

        Returns:
            None, or a ``matplotlib.figure.Figure`` instance depending on Circuit.plot.
        """
        net = PQCombNet(target_function=self.target_func)
        net.V_circuit_list = self.v_circuits
        net.plot(**kwargs)


def _map_paulis_to_aug_matrix(
    pauli_support: Set[str], mode: str
) -> Tuple[torch.Tensor, int]:
    """
    Build an augmented binary matrix [X|Z|b] over GF(2) from a set of Pauli strings.

    Args:
        pauli_support: Set of Pauli operator strings (e.g. {"X0,Z1", ...}).
        mode: Mapping type: 'dagger', 'conj', or 'transpose'.

    Returns:
        A tuple (A_b, num_qubits) where:
            A_b: torch.Tensor of shape (n_rows, 2*num_qubits + 1) over GF(2)
            num_qubits: inferred qubit count
    """
    # determine number of qubits
    num_qubits = (
        max(
            int(term[1:])
            for name in pauli_support
            for term in name.split(",")
            if term and term[1:].isdigit()
        )
        + 1
    )

    def pauli_to_bits(s: str):
        x = [0] * num_qubits
        z = [0] * num_qubits
        for term in s.split(","):
            t = term.strip()
            if not t or t[0] == "I":
                continue
            op, idx = t[0], int(t[1:])
            if op == "X":
                x[idx] = 1
            elif op == "Z":
                z[idx] = 1
            elif op == "Y":
                x[idx] = 1
                z[idx] = 1
        return x, z

    def get_b(x: List[int], z: List[int]):
        if mode == "dagger":
            return 1
        same = sum(a & b for a, b in zip(x, z))
        if mode == "conj":
            return 1 if same % 2 == 0 else 0
        if mode == "transpose":
            return 0 if same % 2 == 0 else 1
        raise ValueError(f"Unknown mode: {mode}")

    rows = []
    for p in pauli_support:
        x_bits, z_bits = pauli_to_bits(p)
        rows.append(x_bits + z_bits + [get_b(x_bits, z_bits)])
    return torch.tensor(rows, dtype=torch.int32), num_qubits


def _bits_matrix_to_pauli_set(A: torch.Tensor) -> Set[str]:
    """
    Convert each row [x|z] in a 2N-bit matrix to a Pauli string and collect as a set.

    Args:
        A: Tensor of shape (n_rows, 2*num_qubits).

    Returns:
        Set[str]: Unique Pauli strings.
    """
    num_qubits = A.shape[1] // 2
    paulis: Set[str] = set()
    for row in A:
        x_bits = row[:num_qubits]
        z_bits = row[num_qubits:]
        terms = []
        for i, (qx, qz) in enumerate(zip(x_bits, z_bits)):
            if qx == 1 and qz == 0:
                terms.append(f"X{i}")
            elif qx == 0 and qz == 1:
                terms.append(f"Z{i}")
            elif qx == 1 and qz == 1:
                terms.append(f"Y{i}")
        paulis.add(",".join(terms) if terms else "I")
    return paulis


def find_pauli_mapping_operators(
    pauli_support: Set[str], mode: str, sort_mode: int = 0
) -> Set[str]:
    """
    Find a minimal set of Pauli mappings V that implements dagger/conj/transpose.
    This function builds an augmented GF(2) matrix from the pauli_support,
    optionally sorts its rows, solves for bit-vectors, and converts them
    back to Pauli operators.

    Args:
        pauli_support: Set of input Pauli strings.
        mode: 'dagger', 'conj', or 'transpose'.
        sort_mode: Matrix ordering mode:
            0: No sorting (original order).
            1: Sort by row-sum (number of nonzero entries), then by first-one position.
            2: Sort by first-one position, then by row-sum.

    Returns:
        Set[str]: Minimal Pauli strings implementing the requested mapping.
    """

    def sort_aug_matrix(A_b: torch.Tensor) -> torch.Tensor:
        if sort_mode == 0:
            # No sorting, keep original order
            return A_b
        A = A_b[:, :-1]
        row_sum = A.sum(dim=1)
        # For each row, find the index of the first nonzero entry
        first_one = (
            torch.where(A == 1, torch.arange(A.size(1)), A.size(1)).min(dim=1).values
        )

        if sort_mode == 1:
            # Sort by row-sum (ascending), then by first-one position (ascending)
            idx = np.lexsort((first_one.cpu().numpy(), row_sum.cpu().numpy()))
        else:
            # sort_mode == 2: Sort by first-one position (ascending), then by row-sum (ascending)
            idx = np.lexsort((row_sum.cpu().numpy(), first_one.cpu().numpy()))
        return A_b[idx]

    A_b, nq = _map_paulis_to_aug_matrix(pauli_support, mode)
    A_b = sort_aug_matrix(A_b)
    sols = _recursive_gf2_solve(A_b)
    return set(_bits_matrix_to_pauli_support(sols, nq))


def _gf2_solve(A_b: torch.Tensor) -> List[int]:
    """
    Solve A·x = b over GF(2) via in-place Gaussian elimination.

    Args:
        A_b: Tensor of shape (n_rows, n_vars+1) representing [A|b].

    Returns:
        List[int]: solution vector x of length n_vars (0/1 entries).
    """
    A = A_b.clone()
    n_rows, m1 = A.shape
    n_vars = m1 - 1
    pivot_row = 0
    pivot_cols: List[int] = []
    for col in range(n_vars):
        if pivot_row >= n_rows:
            break
        sub = A[pivot_row:, col]
        nz = torch.nonzero(sub, as_tuple=False)
        if nz.numel() == 0:
            continue
        r = pivot_row + nz[0].item()
        if r != pivot_row:
            A[[pivot_row, r]] = A[[r, pivot_row]]
        mask = A[:, col].bool()
        mask[pivot_row] = False
        A[mask] ^= A[pivot_row]
        pivot_cols.append(col)
        pivot_row += 1
    # back-substitute b-values
    if pivot_cols:
        rows = torch.arange(len(pivot_cols), dtype=torch.long)
        bvals = A[rows, -1]
        cols = torch.tensor(pivot_cols, dtype=torch.long)
    else:
        cols = torch.empty(0, dtype=torch.long)
        bvals = torch.empty(0, dtype=torch.int32)
    x = torch.zeros(n_vars, dtype=torch.int32)
    x[cols] = bvals.to(torch.int32)
    return x.tolist()


def _recursive_gf2_solve(A_b: torch.Tensor) -> List[List[int]]:
    """
    Recursively solve A·x=b and peel off one solution at a time.

    Args:
        A_b: Augmented GF(2) matrix [A|b].

    Returns:
        List of solution vectors.
    """
    solutions: List[List[int]] = []

    def _recurse(mat: torch.Tensor):
        if mat.size(0) == 0:
            return
        sol = _gf2_solve(mat)
        solutions.append(sol)
        num_vars = mat.size(1) - 1
        nq = num_vars // 2
        z_sol = torch.tensor(sol[:nq], dtype=torch.int32)
        x_sol = torch.tensor(sol[nq:], dtype=torch.int32)
        x_mat, z_mat = mat[:, :nq], mat[:, nq:-1]
        b = mat[:, -1]
        dot = ((x_mat * z_sol) + (z_mat * x_sol)).sum(dim=1) % 2
        keep = dot != b
        if keep.any():
            _recurse(mat[keep])

    _recurse(A_b)
    return solutions


def _bits_matrix_to_pauli_support(
    sol_vectors: List[List[int]], num_qubits: int
) -> List[str]:
    """
    Convert bit-vector solutions [x|z] into Pauli string representations.

    Args:
        sol_vectors: List of solution vectors (length 2*num_qubits each).
        num_qubits: Number of qubits.

    Returns:
        List[str]: Corresponding Pauli strings (e.g. ["X0,Y2", ...]).
    """
    pauli_support: List[str] = []
    for sol in sol_vectors:
        z_bits, x_bits = sol[:num_qubits], sol[num_qubits:]
        terms = []
        for i, (qx, qz) in enumerate(zip(x_bits, z_bits)):
            if qx == 1 and qz == 0:
                terms.append(f"X{i}")
            elif qx == 0 and qz == 1:
                terms.append(f"Z{i}")
            elif qx == 1 and qz == 1:
                terms.append(f"Y{i}")
        pauli_support.append(",".join(terms) if terms else "I")
    return pauli_support
