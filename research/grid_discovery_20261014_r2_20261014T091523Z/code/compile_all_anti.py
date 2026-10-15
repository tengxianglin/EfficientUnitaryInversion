#!/usr/bin/env python3
"""Compile and simulate primitive ordered one-query star/dagger circuits."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from audit_transport import TOL, dense, dump, SINGLE, checked

H = np.array([[1, 1], [1, -1]], dtype=np.complex128)/np.sqrt(2)
S = np.diag([1, 1j]).astype(np.complex128)


def primitive(name, *qubits):
    return {'gate': name, 'qubits': list(qubits)}


def controlled_pauli(tag, control):
    gates = []
    for j, char in enumerate(tag):
        target = j+2
        if char == 'X':
            gates.append(primitive('CX', control, target))
        elif char == 'Z':
            gates.append(primitive('CZ', control, target))
        elif char == 'Y':
            # Time order Sdag, CX, S gives S X Sdag = Y on control=1.
            gates.extend([primitive('Sdag', target), primitive('CX', control, target),
                          primitive('S', target)])
    return gates


def single_pauli(tag):
    return [primitive(c, j) for j, c in enumerate(tag) if c != 'I']


def apply_gate_to_unitary(matrix, gate, n, oracle):
    """Left apply a local gate without constructing a second circuit matrix."""
    name, qubits = gate['gate'], gate['qubits']
    if name == 'ORACLE_FWD':
        local = oracle
    elif name == 'H':
        local = H
    elif name == 'S':
        local = S
    elif name == 'Sdag':
        local = S.conj().T
    elif name in SINGLE:
        local = SINGLE[name]
    elif name == 'CX':
        local = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                          [0, 0, 0, 1], [0, 0, 1, 0]], dtype=np.complex128)
    elif name == 'CZ':
        local = np.diag([1, 1, 1, -1]).astype(np.complex128)
    else:
        raise ValueError(name)
    axes = qubits + [j for j in range(n) if j not in qubits] + [n]
    tensor = matrix.reshape([2]*n + [2**n]).transpose(axes)
    updated = (local @ tensor.reshape(2**len(qubits), -1)).reshape(tensor.shape)
    return updated.transpose(np.argsort(axes)).reshape(matrix.shape)


def simulate(gates, n, oracle):
    matrix = np.eye(2**n, dtype=np.complex128)
    for gate in gates:
        matrix = apply_gate_to_unitary(matrix, gate, n, oracle)
    return matrix


def counts(gates):
    known = [g for g in gates if g['gate'] != 'ORACLE_FWD']
    return {'one_qubit': sum(len(g['qubits']) == 1 for g in known),
            'two_qubit': sum(len(g['qubits']) == 2 for g in known),
            'by_primitive': dict(Counter(g['gate'] for g in known)),
            'forward_oracle_calls': sum(g['gate'] == 'ORACLE_FWD' for g in gates)}


def choi(matrix):
    # |Omega> = sum_j |j,j>/sqrt(8), using vec column-major (out,ref).
    vector = matrix.reshape(-1, order='F')/np.sqrt(matrix.shape[0])
    return np.outer(vector, vector.conj())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20261015)
    parser.add_argument('--samples-per-grid', type=int, default=3)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text())
    assert len(rows) == 30 and args.samples_per_grid == 3
    args.output.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(args.seed)
    records, all_errors = [], []
    for row in rows:
        A, D = row['grid'][0][0], row['grid'][0][1]
        Q0 = row['star_witness']
        cA, cD = controlled_pauli(A, 0), controlled_pauli(D, 1)
        # SELECT = A^a D^b, so SELECTdag time order is cA,cD.
        # Reflection is exactly diag(-1,1,1,1), with no dropped global sign.
        reflection = [primitive('X', 0), primitive('X', 1), primitive('CZ', 0, 1),
                      primitive('X', 1), primitive('X', 0)]
        dagger_gates = ([primitive('H', 0), primitive('H', 1)] + cA + cD +
                        [primitive('ORACLE_FWD', 2, 3, 4)] + cD + cA +
                        reflection + [primitive('H', 0), primitive('H', 1)])
        star_gates = single_pauli(Q0) + [primitive('ORACLE_FWD', 0, 1, 2)] + single_pauli(Q0)
        mats = [dense(tag) for line in row['grid'] for tag in line]
        # Verify witness on every generator (linear, parameter-independent).
        Q = dense(Q0)
        witness_residuals = [float(np.linalg.norm(Q @ P @ Q + P.conj())) for P in mats]
        checked(witness_residuals)
        name = f"B{row['B']:02d}_q{row['q']:02d}"
        raw_files = []
        samples = []
        for sample in range(args.samples_per_grid):
            coefficients = rng.integers(-4, 5, size=9)
            theta = .137
            hamiltonian = sum(int(c)*P for c, P in zip(coefficients, mats))
            U = expm(-1j*theta*hamiltonian)
            full = simulate(dagger_gates, 5, U)
            K = full[:8, :8].copy()
            errors = {'dagger_success_block': float(np.linalg.norm(K-U.conj().T/2)),
                      'dagger_probability_operator': float(np.linalg.norm(K.conj().T @ K-np.eye(8)/4)),
                      'dagger_reference_Choi': float(np.linalg.norm(choi(K)-choi(U.conj().T)/4)),
                      'full_unitarity': float(np.linalg.norm(full.conj().T @ full-np.eye(32)))}
            # Stream each full circuit to disk; no earlier sample's full circuit
            # remains resident while the next circuit is simulated.
            circuit_path = args.output/f'{name}_sample{sample}_dagger_circuit.npy'
            with circuit_path.open('xb') as handle:
                np.save(handle, full)
            raw_files.append({'path': circuit_path.name,
                              'sha256': hashlib.sha256(circuit_path.read_bytes()).hexdigest()})
            del full
            star = simulate(star_gates, 3, U)
            errors.update({'star_success_block': float(np.linalg.norm(star-U.conj())),
                           'star_reference_Choi': float(np.linalg.norm(choi(star)-choi(U.conj()))),
                           'star_probability_operator': float(np.linalg.norm(star.conj().T @ star-np.eye(8)))})
            checked(list(errors.values()))
            all_errors.extend(errors.values())
            raw_path = args.output/f'{name}_sample{sample}_raw.npz'
            with raw_path.open('xb') as handle:
                np.savez_compressed(handle, coefficients=coefficients, oracle=U,
                                    dagger_success_block=K, star_unitary=star)
            raw_files.append({'path': raw_path.name,
                              'sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest()})
            del star
            samples.append({'sample': sample, 'coefficients': coefficients.tolist(), 'theta': theta,
                            'residuals': errors})
        cost = counts(dagger_gates)
        assert cost['two_qubit'] == 2*(sum(c != 'I' for c in A)+sum(c != 'I' for c in D))+1
        record = {'B': row['B'], 'q': row['q'], 'grid': row['grid'],
                  'parameter_order': 'row-major nine independent real coefficients',
                  'star_witness': Q0, 'star_generator_residuals': witness_residuals,
                  'dagger_conjugators': row['dagger_conjugators'],
                  'dagger_lcu_coefficients': ['-1/2', '1/2', '1/2', '1/2'],
                  'star': {'ordered_gates': star_gates, 'cost': counts(star_gates),
                           'A': 0, 'workspace': 3, 'K': 1, 'P': 1, 'Q': 1,
                           'success_probability': 1, 'postselection': None},
                  'dagger': {'ordered_gates': dagger_gates, 'cost': cost,
                             'A': 2, 'workspace': 5, 'K': 1, 'P': 1, 'Q': 1,
                             'success_probability': .25, 'postselection': {'ancillas': [0, 1], 'outcome': '00'},
                             'wire_order': ['ancA', 'ancD', 'q0', 'q1', 'q2']},
                  'samples': samples, 'raw_files': raw_files,
                  'query_contract': 'one unmodified uncontrolled original 8x8 forward U',
                  'gate_contract': 'all-to-all known H,X,Y,Z,S,Sdag,CX,CZ; CY fully decomposed; no hardware routing claim',
                  'Choi_contract': 'normalized maximally entangled physical system/reference, dimension 8 each',
                  'limitations': ['Construction counts only; no gate/ancilla optimality',
                                  'No multi-controlled gate hidden in counts', 'No target architecture or SWAP routing assumed']}
        dump(args.output/f'{name}.json', record)
        records.append(record)
    summary = {'status': 'VERIFIED_FINITE_NUMERICAL', 'grids_completed': len(records),
               'samples_per_grid': args.samples_per_grid, 'total_samples': len(records)*args.samples_per_grid,
               'seed': args.seed, 'arithmetic': 'complex128', 'tolerance': TOL,
               'max_circuit_matrix_dimension': 32, 'max_Choi_matrix_dimension': 64,
               'max_residual': max(all_errors),
               'dagger_one_qubit_range': [min(r['dagger']['cost']['one_qubit'] for r in records), max(r['dagger']['cost']['one_qubit'] for r in records)],
               'dagger_two_qubit_range': [min(r['dagger']['cost']['two_qubit'] for r in records), max(r['dagger']['cost']['two_qubit'] for r in records)],
               'star_one_qubit_range': [min(r['star']['cost']['one_qubit'] for r in records), max(r['star']['cost']['one_qubit'] for r in records)],
               'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
               'limitations': 'Finite-support corroboration; exact gate identities establish construction; no optimality or hardware routing claim'}
    dump(args.output/'summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
