#!/usr/bin/env python3
"""Exact edge-coefficient and circuit-transfer follow-ups, small fixed domains."""

import argparse
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np
import sympy as sp

from verify_heisenberg_tied_inversion import case, evaluate, matrix
from verify_triangle_intertwiner import verify


def clean(m):
    return m.applyfunc(sp.simplify)


def numeric_check(v, generators, seed=20260909):
    vn = np.array(v, dtype=np.complex128)
    gn = [np.array(g, dtype=np.complex128) for g in generators]
    rng = np.random.default_rng(seed)
    maximum = 0.0
    for coefficients in [np.zeros(len(gn)), *rng.normal(size=(16, len(gn)))]:
        h = sum((a * g for a, g in zip(coefficients, gn)), np.zeros_like(vn))
        values, vectors = np.linalg.eigh(h)
        u = (vectors * np.exp(-1j * values)) @ vectors.conj().T
        maximum = max(maximum, float(np.linalg.norm(vn @ u @ vn.conj().T - u.conj().T)))
    assert maximum < 1e-12
    return {"seed": seed, "trials": 17, "max_frobenius_residual": maximum, "tolerance": 1e-12}


def triangle():
    words = ["XXI", "YYI", "ZZI", "IXX", "IYY", "IZZ", "XIX", "YIY", "ZIZ"]
    terms = [matrix(w) for w in words]
    edges = [sum(terms[i:i + 3], sp.zeros(8)) for i in (0, 3, 6)]
    identity = sp.eye(8)
    h_uniform = sum(edges, sp.zeros(8))
    uniform_result = verify()
    v = sp.Matrix([[sp.sympify(value) for value in row] for row in uniform_result["V_matrix_sympy_strings"]])
    # A different gate covers the entire zero-sum plane of signed edge couplings.
    symmetric = (h_uniform + 3 * identity) / 6
    swap12, swap23 = [(edge + identity) / 2 for edge in edges[:2]]
    w = symmetric + sp.I / sp.sqrt(3) * (swap12 * swap23 - swap23 * swap12)
    assert w.H == w and clean(w * w) == identity
    plane_generators = [edges[0] - edges[1], edges[0] - edges[2]]
    assert all(clean(w * g * w + g) == sp.zeros(8) for g in plane_generators)
    assert clean(w * h_uniform * w + h_uniform) != sp.zeros(8)
    nullspace = sp.Matrix.hstack(*(clean(v * g + g * v).reshape(64, 1) for g in terms)).nullspace()
    assert len(nullspace) == 1 and nullspace[0] == sp.ones(9, 1)

    a, b, c, x = sp.symbols("a b c x")
    s, d = a + b + c, a*a + b*b + c*c - a*b - a*c - b*c
    symbolic_h = a * edges[0] + b * edges[1] + c * edges[2]
    expected = (x - s)**4 * ((x + s)**2 - 4*d)**2
    assert sp.expand(symbolic_h.charpoly(x).as_expr() - expected) == 0

    rays = []
    for j in itertools.product(range(-2, 3), repeat=3):
        if not any(j) or math.gcd(*j) != 1 or next(v for v in j if v) < 0:
            continue
        h = sum((a * g for a, g in zip(j, edges)), sp.zeros(8))
        p = h.charpoly().as_poly().sqf_part().monic()
        coeff = p.all_coeffs()
        assert evaluate(coeff, h) == sp.zeros(8)
        powers = {i % 2 for i, value in enumerate(reversed(coeff)) if value}
        pure = len(powers) == 1
        total = sum(j)
        spread = sum(a*a for a in j) - sum(j[i]*j[k] for i in range(3) for k in range(i+1, 3))
        assert pure == (total == 0 or spread == 0)
        witness = None
        gate = None
        if pure:
            gate = "zero_sum_W" if total == 0 else "uniform_V"
            inverter = w if total == 0 else v
            assert clean(inverter * h * inverter + h) == sp.zeros(8)
        else:
            degree = p.degree()
            even = evaluate([value if (degree-i) % 2 == 0 else 0 for i, value in enumerate(coeff)], h)
            assert even != sp.zeros(8)
            witness = next([i, k, str(even[i, k])] for i in range(8) for k in range(8) if even[i, k])
        rays.append({"J": j, "sum_J": total, "D": spread, "minimal_polynomial": list(map(str, coeff)),
                     "status": "EXACT_FIXED_UNITARY_INVERTER" if pure else "FIXED_AMPLITUDE_LINEAR_OBSTRUCTION",
                     "gate": gate, "even_odd_overlap_entry": witness})
    assert len(rays) == 49
    return {"status": "VERIFIED", "edge_order": ["12", "23", "13"], "pauli_order": words,
            "symbolic_charpoly": "(x-S)^4*((x+S)^2-4D)^2; S=J12+J23+J13; D=sum(J^2)-sum_pair(J_i*J_j)",
            "symbolic_charpoly_exact_match": True,
            "uniform_V_allowed_9_term_coefficient_kernel": [list(map(str, v)) for v in nullspace],
            "zero_sum_W_matrix": [[str(w[i,k]) for k in range(8)] for i in range(8)],
            "zero_sum_W_exact_checks": {"hermitian": True, "unitary": True, "anticommutes_with_plane_basis": True},
            "zero_sum_family": "J12+J23+J13=0, arbitrary real signed couplings; one shared W",
            "zero_sum_numerical": numeric_check(w, plane_generators), "rays": rays,
            "ray_scope": "primitive integer triples in [-2,2]^3, nonzero, sign identified; each ray has all real scale a",
            "physical_contract": "V or W -> unknown U -> V or W; Q=1,A=0,p=1; gate selected using the known promised family",
            "limits": "Uniform-axis and zero-sum-plane gates differ. These certificates do not give one gate for their union or arbitrary edge couplings."}


def edge_families():
    rows = []
    for boundary in ("open", "periodic"):
        for n in range(2 if boundary == "open" else 3, 7):
            for axes in ("XYZ", "XZ"):
                if axes == "XYZ":
                    # Setting all but one independent edge coupling to zero is an exact subfamily.
                    h = sum((matrix(axis + axis + "I" * (n-2)) for axis in axes), sp.zeros(1 << n))
                    assert h*h + 2*h - 3*sp.eye(h.rows) == sp.zeros(h.rows)
                    assert h != sp.zeros(h.rows)
                    rows.append({"n": n, "boundary": boundary, "axes": axes,
                                 "status": "FIXED_AMPLITUDE_LINEAR_OBSTRUCTION",
                                 "slice": "J_first_edge=a, all other J_edges=0", "annihilator": [1, 2, -3],
                                 "nonzero_overlap": "H0^2-3I=-2H0 != 0"})
                else:
                    c = case(n, boundary, axes)
                    if c["pauli_witness"]:
                        v = matrix(c["pauli_witness"])
                        assert all(v*matrix(p)*v == -matrix(p) for p in c["support"])
                    rows.append({"n": n, "boundary": boundary, "axes": axes, "status": c["status"],
                                 "pauli_witness": c["pauli_witness"],
                                 "slice": "full independent family" if c["pauli_witness"] else "all J_edges=a",
                                 "slice_certificate": c})
    assert len(rows) == 18
    return {"parameter_domain": "Each edge has independent real J_e; all axes on the same edge share J_e",
            "cases": rows, "negative_scope": "Fixed nonzero amplitude complex-linear one-query successful branch only"}


def transfer():
    identity = sp.eye(8)
    encoder = sp.Matrix.hstack(*(identity[:, b ^ (7 if spectator else 0)]
                                for b in (0, 3, 5, 6) for spectator in (0, 1)))
    assert encoder.T*encoder == identity
    assert encoder.T*matrix("XXX")*encoder == sp.kronecker_product(sp.eye(4), matrix("X"))
    assert encoder.T*matrix("ZZZ")*encoder == sp.kronecker_product(sp.eye(4), matrix("Z"))
    mapping, logical_matrices = {}, {}
    for word in ("XXI", "YYI", "ZZI", "IXX", "IYY", "IZZ"):
        encoded = encoder.T*matrix(word)*encoder
        logical = encoded.extract(range(0,8,2), range(0,8,2))
        assert encoded == sp.kronecker_product(logical, sp.eye(2))
        matches = [(sign, "".join(p)) for p in itertools.product("IXYZ", repeat=2) for sign in (-1,1)
                   if logical == sign*matrix("".join(p))]
        assert len(matches) == 1
        mapping[word] = matches[0]
        logical_matrices[word] = [[str(logical[i,j]) for j in range(4)] for i in range(4)]
    physical_v = matrix("YIY")
    logical_v = (encoder.T*physical_v*encoder).extract(range(0,8,2), range(0,8,2))
    assert encoder*sp.kronecker_product(logical_v, sp.eye(2))*encoder.T == physical_v
    xz = [matrix(p) for p in ("XXI", "ZZI", "IXX", "IZZ")]
    assert all(physical_v*g*physical_v == -g for g in xz)
    i16 = sp.eye(16)
    centers = [matrix("XXXX"), matrix("ZZZZ")]
    n4_support = []
    for edge in range(3):
        for axis in "XYZ":
            word = ["I"]*4
            word[edge] = word[edge+1] = axis
            n4_support.append("".join(word))
    assert centers[0]*centers[1] == centers[1]*centers[0]
    assert all(center*matrix(word)==matrix(word)*center for center in centers for word in n4_support)
    projectors = [(i16+s*matrix("XXXX"))*(i16+t*matrix("ZZZZ"))/4 for s,t in itertools.product((-1,1),repeat=2)]
    assert sum(projectors, sp.zeros(16)) == i16
    assert all(p*p==p and p.rank()==4 for p in projectors)
    assert all(p*q==sp.zeros(16) for i,p in enumerate(projectors) for q in projectors[i+1:])
    return {"status": "VERIFIED", "N3_encoder_columns": [b^(7 if s else 0) for b in (0,3,5,6) for s in (0,1)],
            "N3_convention": "C maps logical(4) tensor spectator(2) to physical(8); encoded oracle C^T U C",
            "N3_support_map": mapping, "N3_physical_inverter": "YIY",
            "N3_logical_matrices": logical_matrices,
            "N3_encoded_family_scope": "All six source Pauli coefficients may vary independently over the reals; each transforms to logical matrix tensor I2",
            "N3_logical_inverter": [[str(logical_v[i,j]) for j in range(4)] for i in range(4)],
            "N3_numerical_independent_XZ": numeric_check(physical_v, xz),
            "resource": "one call to original 3-qubit U, no additional ancilla; no claim of physical oracle dimension reduction",
            "N4_center": ["XXXX", "ZZZZ"], "N4_sector_ranks": [4,4,4,4],
            "N4_open_XYZ_support": n4_support, "N4_center_commutes_with_each_source_term": True,
            "limits": "N3 open-chain explicit transfer and N4 sector check only; not a general canonicalizer"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output exists")
    started = time.monotonic()
    result = {"status": "COMPLETED", "triangle": triangle(), "edge_families": edge_families(), "transfer": transfer(),
              "versions": {"numpy": np.__version__, "sympy": sp.__version__}}
    result["elapsed_seconds"] = time.monotonic()-started
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
