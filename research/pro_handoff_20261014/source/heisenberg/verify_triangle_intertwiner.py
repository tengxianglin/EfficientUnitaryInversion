#!/usr/bin/env python3
"""Exact fixed-gate inverter for the uniformly coupled three-site XYZ triangle.

An independent dense certificate; no project helpers are imported. Qubit 0 is
the left Kronecker factor. The target is conjugate transpose, not transpose.
"""

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import sympy as sp


def verify():
    identity = sp.eye(8)
    paulis = {"I": sp.eye(2), "X": sp.Matrix([[0, 1], [1, 0]]),
              "Y": sp.Matrix([[0, -sp.I], [sp.I, 0]]),
              "Z": sp.diag(1, -1)}

    def word(label):
        return sp.kronecker_product(*(paulis[c] for c in label))

    def clean(matrix):
        return matrix.applyfunc(sp.simplify)

    labels = ["XXI", "YYI", "ZZI", "IXX", "IYY", "IZZ", "XIX", "YIY", "ZIZ"]
    terms = [word(s) for s in labels]
    h = sum(terms, sp.zeros(8))
    basis = [identity[:, i] for i in range(8)]
    positive = [basis[0], (basis[1] + basis[2] + basis[4]) / sp.sqrt(3),
                (basis[3] + basis[5] + basis[6]) / sp.sqrt(3), basis[7]]
    negative = [(basis[1] - basis[2]) / sp.sqrt(2),
                (basis[1] + basis[2] - 2 * basis[4]) / sp.sqrt(6),
                (basis[3] - basis[5]) / sp.sqrt(2),
                (basis[3] + basis[5] - 2 * basis[6]) / sp.sqrt(6)]
    eigenbasis = sp.Matrix.hstack(*positive, *negative)
    assert clean(eigenbasis.H * eigenbasis) == identity
    assert h * h == 9 * identity
    assert all(clean(h * p - 3 * p) == sp.zeros(8, 1) for p in positive)
    assert all(clean(h * m + 3 * m) == sp.zeros(8, 1) for m in negative)
    v = clean(sum((p * m.H + m * p.H for p, m in zip(positive, negative)), sp.zeros(8)))
    assert v.H == v
    assert clean(v * v) == identity
    assert clean(v * h * v + h) == sp.zeros(8)
    # Exact counterexample to transferring this gate to independent coefficients.
    independent_difference = clean(v * terms[0] * v + terms[0])
    assert independent_difference != sp.zeros(8)
    entry = next((i, j, str(independent_difference[i, j])) for i in range(8)
                 for j in range(8) if independent_difference[i, j] != 0)
    edge = sum(terms[:3], sp.zeros(8))
    assert clean(v * edge * v + edge) != sp.zeros(8)

    numeric_h = np.array(h, dtype=np.complex128)
    numeric_v = np.array(v.evalf(), dtype=np.complex128)
    eigvals, eigvecs = np.linalg.eigh(numeric_h)
    seed = 20260909
    parameters = [0.0, -0.25, 0.25, *np.random.default_rng(seed).normal(size=32).tolist()]
    max_residual = max_transpose_difference = 0.0
    for a in parameters:
        u = (eigvecs * np.exp(-1j * a * eigvals)) @ eigvecs.conj().T
        max_residual = max(max_residual, float(np.linalg.norm(numeric_v @ u @ numeric_v - u.conj().T)))
        max_transpose_difference = max(max_transpose_difference, float(np.linalg.norm(u.T - u.conj().T)))
    assert max_residual < 1e-12
    assert max_transpose_difference > 1
    v_strings = [[str(v[i, j]) for j in range(8)] for i in range(8)]
    return {
        "status": "VERIFIED_EXACT_FIXED_UNITARY_INVERTER",
        "family": "H(a)=a*(XXI+YYI+ZZI+IXX+IYY+IZZ+XIX+YIY+ZIZ), a real",
        "target": "U(a)^dagger; U(a)=exp(-i*a*H0)",
        "support": labels,
        "exact_checks": {"H0_squared_equals_9I": True, "eigenbasis_unitary": True,
                         "V_hermitian": True, "V_squared_equals_I": True, "V_H0_V_equals_minus_H0": True},
        "eigenvalues_and_multiplicities": {"3": 4, "-3": 4},
        "V_matrix_sympy_strings": v_strings,
        "V_matrix_sha256": hashlib.sha256(json.dumps(v_strings, separators=(",", ":")).encode()).hexdigest(),
        "physical_contract": {"sequence": "V -> U -> V", "queries": 1, "slots": 1,
                              "parallel": 1, "ancilla_qubits": 0, "success_probability": "1",
                              "known_gates": "two applications of the explicit 8x8 unitary V",
                              "elementary_gate_decomposition": "not computed; arbitrary known unitaries permitted"},
        "independent_coefficients_counterexample": {"term": labels[0], "V_P_V_plus_P_nonzero_entry": entry,
                                                   "single_edge_XYZ_also_fails": True},
        "numerical_corroboration": {"dtype": "complex128", "seed": seed, "trials": len(parameters),
                                    "max_dagger_residual_frobenius": max_residual,
                                    "max_transpose_minus_dagger_frobenius": max_transpose_difference},
        "claim_limits": ["Only the uniform one-real-parameter triangle family is inverted by this V.",
                         "The construction uses spectral pairing; literature novelty is not assessed.",
                         "No elementary gate cost or noisy/hardware performance claim."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists")
    started = time.monotonic()
    result = verify()
    result["elapsed_seconds"] = time.monotonic() - started
    result["versions"] = {"numpy": np.__version__, "sympy": sp.__version__}
    with args.output.open("x") as output:
        json.dump(result, output, indent=2, ensure_ascii=False)
        output.write("\n")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
