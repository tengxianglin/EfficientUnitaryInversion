#!/usr/bin/env python3
"""Compile the certified triangle inverter and check its ideal matrix action.

This is a gate-synthesis cost/ordering probe only.  It contains no hardware or
gate-noise model, and is not an algorithm-advantage benchmark.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import expm

from verify_triangle_intertwiner import verify as certified_triangle


def phase_residual(actual, expected):
    """Frobenius residual after aligning one global phase."""
    overlap = np.trace(expected.conj().T @ actual)
    phase = 1.0 if abs(overlap) == 0 else overlap / abs(overlap)
    return float(np.linalg.norm(actual - phase * expected)), [float(phase.real), float(phase.imag)]


def process_fidelity(target, actual):
    return float(abs(np.trace(target.conj().T @ actual) / 8) ** 2)


def matrices():
    """Return raw arrays in the certificate's left-Kronecker-factor ordering."""
    certificate = certified_triangle()
    v = np.array(sp.Matrix(certificate["V_matrix_sympy_strings"]), dtype=np.complex128)
    paulis = {
        "I": np.eye(2, dtype=np.complex128),
        "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
        "Z": np.diag([1, -1]).astype(np.complex128),
    }

    def word(label):
        return np.kron(np.kron(paulis[label[0]], paulis[label[1]]), paulis[label[2]])

    terms = {label: word(label) for label in certificate["support"]}
    h_uniform = sum(terms.values())
    b23 = terms["IXX"] + terms["IYY"] + terms["IZZ"]
    assert np.linalg.norm(v.conj().T @ v - np.eye(8)) < 1e-12
    assert np.linalg.norm(v @ h_uniform @ v + h_uniform) < 1e-12
    return certificate, v, h_uniform, b23


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists")
    try:
        import qiskit
        from qiskit import QuantumCircuit, transpile
        from qiskit.quantum_info import Operator
    except ImportError as exc:
        parser.error("qiskit is required in the selected environment: " + repr(exc))

    started = time.monotonic()
    certificate, v, h_uniform, b23 = matrices()
    # Qiskit displays basis states as |q2 q1 q0>, so q0 is its LSB.  The
    # certificate's Pauli labels put q0 at the left Kronecker factor.  Feeding
    # the same raw matrix to unitary() makes Operator(...).data and this V use
    # one common matrix ordering: original sites (0,1,2) are Qiskit wires (2,1,0).
    # The unknown oracle is supplied in this same raw ordering.
    direct = QuantumCircuit(3)
    direct.unitary(v, [0, 1, 2])
    direct_residual, direct_phase = phase_residual(Operator(direct).data, v)
    assert direct_residual < 1e-12

    def synthesize(known_gate, name):
        direct_gate = QuantumCircuit(3)
        direct_gate.unitary(known_gate, [0, 1, 2])
        compiled = []
        for optimization_level in (0, 3):
            for seed in (11, 22, 33):
                circuit = transpile(
                    direct_gate, basis_gates=["u", "cx"], optimization_level=optimization_level,
                    seed_transpiler=seed,
                )
                compiled_v = Operator(circuit).data
                residual, phase = phase_residual(compiled_v, known_gate)
                raw_residual = float(np.linalg.norm(compiled_v-known_gate))
                assert raw_residual < 1e-10
                operations = [{"name": item.operation.name,
                               "qubits": [circuit.find_bit(q).index for q in item.qubits],
                               "parameters": [float(p) for p in item.operation.params]} for item in circuit.data]
                replay = QuantumCircuit(3)
                replay.global_phase = float(circuit.global_phase)
                for operation in operations:
                    getattr(replay, operation["name"])(*operation["parameters"], *operation["qubits"])
                assert np.linalg.norm(Operator(replay).data-known_gate) < 1e-10
                compiled.append({
                    "known_gate": name,
                    "optimization_level": optimization_level,
                    "seed_transpiler": seed,
                    "cx_count": int(circuit.count_ops().get("cx", 0)),
                    "depth": int(circuit.depth()),
                    "global_phase_aligned_frobenius_residual_to_gate": residual,
                    "alignment_phase": phase,
                    "raw_frobenius_residual_to_gate": raw_residual,
                    "global_phase": float(circuit.global_phase),
                    "operations": operations,
                    "basis_gates": ["u", "cx"],
                    "matrix_ordering": "same raw Qiskit ordering as V",
                })
        return compiled
    compiled = synthesize(v, "uniform_V")

    # Preselected opt3/seed11 circuit; no best-seed selection.
    compiled_v = Operator(transpile(
        direct, basis_gates=["u", "cx"], optimization_level=3, seed_transpiler=11
    )).data
    rng = np.random.default_rng(20260909)
    amplitudes = [0.0, *rng.normal(size=34).tolist()]
    uniform_trials = []
    for amplitude in amplitudes:
        u = expm(-1j * amplitude * h_uniform)
        target = u.conj().T
        actual = compiled_v @ u @ compiled_v
        residual, phase = phase_residual(actual, target)
        assert np.linalg.norm(actual-target) < 1e-10
        uniform_trials.append({
            "a": float(amplitude),
            "compiled_V_U_compiled_V_residual": residual,
            "compiled_V_U_compiled_V_process_fidelity": process_fidelity(target, actual),
            "no_V_baseline_process_fidelity": process_fidelity(target, u),
            "alignment_phase": phase,
        })
    assert max(row["compiled_V_U_compiled_V_residual"] for row in uniform_trials) < 1e-10

    imbalance = []
    for epsilon in (0.0, 1e-4, 1e-3, 1e-2, 1e-1):
        h = h_uniform + epsilon * b23
        for t in (0.25, 0.5, 1.0):
            u = expm(-1j * t * h)
            target = u.conj().T
            actual = compiled_v @ u @ compiled_v
            imbalance.append({
                "epsilon": epsilon,
                "t": t,
                "process_fidelity": process_fidelity(target, actual),
                "no_V_baseline_process_fidelity": process_fidelity(target, u),
                "frobenius_residual_after_global_phase": phase_residual(actual, target)[0],
            })

    # Compile the independently certified zero-sum-plane gate as a second arm.
    from run_heisenberg_followup_extensions import triangle
    zero_sum = triangle()
    w = np.array(sp.Matrix(zero_sum["zero_sum_W_matrix"]), dtype=np.complex128)
    compiled_w_records = synthesize(w, "zero_sum_W")
    w_circuit = QuantumCircuit(3)
    w_circuit.unitary(w, [0, 1, 2])
    compiled_w = Operator(transpile(w_circuit, basis_gates=["u", "cx"], optimization_level=3, seed_transpiler=11)).data
    x = np.array([[0,1],[1,0]], dtype=np.complex128)
    y = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
    z = np.diag([1,-1]).astype(np.complex128)
    b12 = sum(np.kron(np.kron(p,p),np.eye(2)) for p in (x,y,z))
    b13 = sum(np.kron(np.kron(p,np.eye(2)),p) for p in (x,y,z))
    plane_trials = []
    rng = np.random.default_rng(20260909)
    for a,b in [np.zeros(2), *rng.normal(size=(34,2))]:
        h = a*(b12-b23)+b*(b12-b13)
        u = expm(-1j*h)
        actual = compiled_w @ u @ compiled_w
        target = u.conj().T
        residual = float(np.linalg.norm(actual-target))
        assert residual < 1e-10
        plane_trials.append({"plane_coefficients": [float(a),float(b)], "residual": residual,
                             "process_fidelity": process_fidelity(target,actual),
                             "no_W_baseline_process_fidelity": process_fidelity(target,u)})

    result = {
        "status": "COMPILED_IDEAL_MATRIX_PROBE",
        "certificate": {
            "source": "scripts/verify_triangle_intertwiner.py",
            "V_matrix_sha256": certificate["V_matrix_sha256"],
            "target": certificate["target"],
        },
        "qiskit_version": qiskit.__version__,
        "ordering": {
            "certificate": "Pauli q0 is the left Kronecker factor",
            "qiskit": "qiskit qubit 0 is the LSB; displayed basis is |q2 q1 q0>",
            "site_to_wire_mapping": "original sites (0,1,2) correspond to Qiskit wires (2,1,0)",
            "known_gate_input": "Operator(QuantumCircuit.unitary(V, [0,1,2])).data compared directly to the same raw V; U uses identical ordering",
            "direct_oracle_global_phase_aligned_frobenius_residual": direct_residual,
            "direct_oracle_alignment_phase": direct_phase,
        },
        "compilations": compiled,
        "zero_sum_W_compilations": compiled_w_records,
        "zero_sum_W_trials": plane_trials,
        "synthesis_scope": "all-to-all CX and arbitrary u gates; counts for each known gate, excluding unknown-U cost; no optimality claim",
        "uniform_family": {
            "seed": 20260909,
            "amplitudes": "0 plus 34 standard-normal draws",
            "trials": uniform_trials,
            "max_compiled_residual": max(row["compiled_V_U_compiled_V_residual"] for row in uniform_trials),
        },
        "frozen_coupling_imbalance_diagnostic": {
            "H": "H_uniform + epsilon*(IXX+IYY+IZZ)",
            "rows": imbalance,
            "metric": "|Tr(Utarget^dagger W)/8|^2, Utarget=U^dagger, W=compiledV U compiledV",
            "scope": "ideal matrix sensitivity only; not hardware, gate-noise, or algorithm-advantage evidence",
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
