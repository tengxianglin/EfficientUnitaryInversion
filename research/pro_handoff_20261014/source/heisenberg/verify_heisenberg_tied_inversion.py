#!/usr/bin/env python3
"""Exact, bounded uniform-Heisenberg census; no project helpers imported."""

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np
import sympy as sp


def matrix(label):
    """Integer/Gaussian-integer Pauli matrix, q0 the left tensor factor."""
    n = len(label)
    out = sp.zeros(1 << n)
    for column in range(1 << n):
        row, phase = column, sp.Integer(1)
        for q, axis in enumerate(label):
            bit = 1 << (n - q - 1)
            sign = -1 if column & bit else 1
            if axis in "XY":
                row ^= bit
            if axis == "Y":
                phase *= sp.I * sign
            if axis == "Z":
                phase *= sign
        out[row, column] = phase
    return out


def anticommutes(a, b):
    return sum(x != y and x != "I" and y != "I" for x, y in zip(a, b)) % 2 == 1


def rank(rows):
    pivots = {}
    for value in rows:
        while value:
            p = value.bit_length() - 1
            if p not in pivots:
                pivots[p] = value
                break
            value ^= pivots[p]
    return len(pivots)


def evaluate(coefficients, h):
    identity, result = sp.eye(h.rows), sp.zeros(h.rows)
    for coefficient in coefficients:
        result = result * h + coefficient * identity
    return result


def case(n, boundary, axes):
    started = time.monotonic()
    edges = [(i, i + 1) for i in range(n - 1)]
    if boundary == "periodic":
        edges.append((0, n - 1))
    edges = sorted(set(edges))
    labels = []
    for a, b in edges:
        for axis in axes:
            label = ["I"] * n
            label[a] = label[b] = axis
            labels.append("".join(label))
    h = sum((matrix(label) for label in labels), sp.zeros(1 << n))
    assert h == h.T and all(entry.is_Integer for entry in h)
    polynomial = h.charpoly().as_poly().sqf_part().monic()
    coefficients = polynomial.all_coeffs()
    zero = sp.zeros(h.rows)
    assert evaluate(coefficients, h) == zero
    degree = polynomial.degree()
    even = [c if (degree - i) % 2 == 0 else 0 for i, c in enumerate(coefficients)]
    odd = [c if (degree - i) % 2 else 0 for i, c in enumerate(coefficients)]
    mixed = any(even) and any(odd)
    witness = None
    if mixed:
        e, o = evaluate(even, h), evaluate(odd, h)
        assert e != zero and e == -o
        witness = next({"row": i, "column": j, "value": str(e[i, j])}
                       for i in range(h.rows) for j in range(h.cols) if e[i, j])
    common = ["".join(p) for p in itertools.product("IXYZ", repeat=n)
              if all(anticommutes(p, label) for label in labels)]
    status = "FIXED_AMPLITUDE_LINEAR_OBSTRUCTION" if mixed else "LINEAR_PARITY_COMPATIBLE_NO_PAULI_WITNESS"
    numeric = None
    if common:
        assert not mixed
        v = matrix(common[0])
        assert v * v == sp.eye(h.rows) and v * h * v == -h
        status = "EXACT_DETERMINISTIC_PAULI_INVERTER"
        values, vectors = np.linalg.eigh(np.array(h, dtype=np.complex128))
        vn = np.array(v, dtype=np.complex128)
        residual = 0.0
        for a in [0., *np.random.default_rng(20260909).normal(size=16)]:
            u = (vectors * np.exp(-1j * a * values)) @ vectors.conj().T
            residual = max(residual, float(np.linalg.norm(vn @ u @ vn - u.conj().T)))
        assert residual < 1e-12
        numeric = {"seed": 20260909, "trials": 17, "dtype": "complex128", "tolerance": 1e-12,
                   "max_dagger_residual_frobenius": residual}
    vectors = [sum((int(c in "XY") << q) | (int(c in "YZ") << (q + n))
                   for q, c in enumerate(label)) for label in labels]
    support_rank = rank(vectors)
    omega_rank = rank([sum(int(anticommutes(a, b)) << j for j, b in enumerate(labels)) for a in labels])
    return {"n": n, "boundary": boundary, "axes": axes, "edges": edges, "support": labels,
            "parameter_domain": "H(a)=a*H0, all real a", "status": status,
            "matrix_sha256": hashlib.sha256(json.dumps([int(v) for v in h], separators=(",", ":")).encode()).hexdigest(),
            "minimal_polynomial_coefficients_descending": [str(c) for c in coefficients],
            "minimal_polynomial_degree": degree, "exact_annihilation": True,
            "mixed_parity": bool(mixed), "even_odd_overlap_entry": witness,
            "common_anticommuting_pauli_count": len(common), "pauli_witness": common[0] if common else None,
            "binary_rank": support_rank, "symplectic_rank": omega_rank, "radical_dimension": support_rank - omega_rank,
            "numerical_corroboration": numeric, "elapsed_seconds": time.monotonic() - started}


def self_check():
    assert matrix("X") * matrix("Y") == sp.I * matrix("Z")
    assert matrix("YY") == sp.kronecker_product(matrix("Y"), matrix("Y"))
    assert case(2, "open", "XYZ")["minimal_polynomial_coefficients_descending"] == ["1", "2", "-3"]
    assert case(2, "open", "XZ")["status"] == "EXACT_DETERMINISTIC_PAULI_INVERTER"
    assert case(3, "periodic", "XZ")["minimal_polynomial_coefficients_descending"] == ["1", "-2", "-8", "0"]
    u = np.diag(np.exp(-1j * np.array([1., -1.])))
    assert np.array_equal(u.T, u) and not np.allclose(u.T, u.conj().T)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-min", type=int, default=2)
    parser.add_argument("--n-max", type=int, default=6)
    parser.add_argument("--boundary", choices=("open", "periodic", "both"), default="both")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not 2 <= args.n_min <= args.n_max <= 6 or args.output.exists():
        parser.error("require 2 <= n-min <= n-max <= 6 and a fresh output path")
    started = time.monotonic()
    self_check()
    boundaries = ("open", "periodic") if args.boundary == "both" else (args.boundary,)
    cases = []
    for boundary in boundaries:
        for n in range(args.n_min, args.n_max + 1):
            if n == 2 and boundary == "periodic":
                continue  # The two-site simple graph is already the open case.
            for axes in ("XYZ", "XZ"):
                result = case(n, boundary, axes)
                cases.append(result)
                print(json.dumps({k: result[k] for k in ("n", "boundary", "axes", "status", "elapsed_seconds")}), flush=True)
    output = {"status": "COMPLETED", "cases": cases, "self_check": "PASS",
              "versions": {"numpy": np.__version__, "sympy": sp.__version__},
              "elapsed_seconds": time.monotonic() - started,
              "negative_scope": "No fixed complex-linear L and fixed nonzero c with L(U(a))=c*U(a)^dagger for every real a; not an arbitrary channel or phase-dependent no-go.",
              "positive_scope": "A listed Pauli V gives V->U->V, Q=1,A=0,p=1, including arbitrary real independent coefficients on this support.",
              "parity_compatible_scope": "Linear map condition only; a physical construction requires a separate certificate."}
    with args.output.open("x") as stream:
        json.dump(output, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
