#!/usr/bin/env python3
"""Independent sparse-Pauli T5 B55 candidate producer.

The sole input is the pinned T4 JSON. Products and adjoints use Gaussian-rational
Pauli coordinates; dense matrices are made only for the small exact embedding,
characteristic polynomial, and physical LCU interface. No T4 helper is imported.

certificate.json uses schema t5-sparse-v1. A matrix is {rows,cols,entries},
with row-major exact SymPy expression strings. A Pauli vector is a dictionary
from three-letter IXYZ words to exact expression strings. Entries need only the
whitelisted grammar Integer, Rational, Add, Mul, Pow, I and sqrt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as S

LET = "IXYZ"
GRID = [["XII", "ZII", "YII"], ["ZXI", "YIY", "XXY"], ["YXI", "XIY", "ZXY"]]
TAB = {
    ("I", x): (x, 1) for x in LET
} | {
    (x, "I"): (x, 1) for x in LET
} | {
    (x, x): ("I", 1) for x in "XYZ"
} | {
    ("X", "Y"): ("Z", S.I), ("Y", "Z"): ("X", S.I),
    ("Z", "X"): ("Y", S.I), ("Y", "X"): ("Z", -S.I),
    ("Z", "Y"): ("X", -S.I), ("X", "Z"): ("Y", -S.I),
}
PAULI2 = {
    "I": S.eye(2), "X": S.Matrix([[0, 1], [1, 0]]),
    "Y": S.Matrix([[0, -S.I], [S.I, 0]]), "Z": S.diag(1, -1),
}


def clean(a):
    return {k: S.simplify(v) for k, v in a.items() if S.simplify(v) != 0}


def add(*args):
    out = {}
    for a in args:
        for k, v in a.items():
            out[k] = out.get(k, 0) + v
    return clean(out)


def scale(a, x):
    return clean({k: x * v for k, v in a.items()})


def mul(a, b):
    out = {}
    for u, v in a.items():
        for w, z in b.items():
            letters, phase = zip(*(TAB[(x, y)] for x, y in zip(u, w)))
            key = "".join(letters)
            out[key] = out.get(key, 0) + v * z * S.prod(phase)
    return clean(out)


def dagger(a):
    return clean({k: S.conjugate(v) for k, v in a.items()})


def transpose(a):
    return clean({k: (-1) ** k.count("Y") * v for k, v in a.items()})


def star(a):
    return clean({k: (-1) ** k.count("Y") * S.conjugate(v) for k, v in a.items()})


def sm(a):
    return {k: str(v) for k, v in sorted(clean(a).items())}


def dense(a):
    out = S.zeros(8)
    for word, coefficient in a.items():
        out += coefficient * S.kronecker_product(*(PAULI2[t] for t in word))
    return out


def dm(a):
    return {"rows": a.rows, "cols": a.cols,
            "entries": [str(S.simplify(x)) for x in a]}


def check(label, residual):
    if isinstance(residual, S.MatrixBase):
        bad = [(i, j, str(S.simplify(residual[i, j])))
               for i in range(residual.rows) for j in range(residual.cols)
               if S.simplify(residual[i, j]) != 0]
    else:
        bad = list(sm(residual).items())
    if bad:
        raise AssertionError(f"{label}: {bad[:8]}")


def word(index):
    return "".join(LET[(index >> (2 * q)) & 3] for q in (2, 1, 0))


def basis(obj, kind):
    rows = obj[kind]["echelon_basis"]
    pointers = obj[kind]["independent_coefficient_rows"]
    assert len(rows) == len(pointers) == obj[kind]["rank"]
    for pointer in pointers:
        assert 0 <= pointer < len(obj["coefficient_rows"])
    return [{word(int(k)): S.Rational(v) for k, v in row.items()}
            for row in rows]


def coordinates(target, vectors):
    coeff = S.Matrix([target.get(word(i), 0) for i in range(64)])
    matrix = S.Matrix(64, len(vectors),
                      lambda i, j: vectors[j].get(word(i), 0))
    ans, parameters = matrix.gauss_jordan_solve(coeff)
    assert not parameters, "basis coordinates are not unique"
    check("coordinate reconstruction", matrix * ans - coeff)
    return [str(S.simplify(x)) for x in ans]


def sector_projectors():
    identity = {"III": S.Integer(1)}
    r = {"IXI": S.Integer(1)}
    s = {"IIY": S.Integer(1)}
    return {(a, b): scale(mul(add(identity, scale(r, a)),
                              add(identity, scale(s, b))), S.Rational(1, 4))
            for a in (1, -1) for b in (1, -1)}


def sector_matrix(projector, h):
    # Tr(P sigma_a H)/rank(P), with rank(P)=2.
    # A Pauli word has trace eight only when it is III.
    return tuple(S.simplify(4 * mul(mul(projector, {axis + "II": 1}), h).get("III", 0))
                 for axis in "XYZ")


def canonical_columns(m00, bx):
    mat = dense(m00)
    vectors = []
    selected = []
    for index in range(8):
        u = mat[:, index]
        for v in vectors:
            u -= v * (v.conjugate().T * u)[0]
        u = u.applyfunc(S.simplify)
        norm = S.simplify((u.conjugate().T * u)[0])
        if norm == 0:
            continue
        u = (u / S.sqrt(norm)).applyfunc(S.simplify)
        first = next(i for i in range(8) if u[i] != 0)
        phase = S.simplify(u[first] / S.sqrt(S.conjugate(u[first]) * u[first]))
        u = (u / phase).applyfunc(S.simplify)
        vectors.append(u)
        selected.append(index)
        if len(vectors) == 3:
            break
    assert len(vectors) == 3
    j = S.Matrix.hstack(*(vectors + [(dense(bx) * v).applyfunc(S.simplify)
                                   for v in vectors]))
    return j, selected


def family(obj, name, projectors, p0, pc, h0, q0):
    grid = sum(obj["grid"], [])
    h = [add(*(scale({grid[k]: 1}, S.Integer(obj["C"][k][j]))
               for k in range(9))) for j in range(3)]
    full, even, odd = (basis(obj, key) for key in ("full", "even", "odd"))
    assert (len(full), len(even), len(odd)) == (6, 2, 4)
    sectors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    aa = {f"{r:+d},{s:+d}": S.Matrix(3, 3, lambda i, j:
                                   sector_matrix(projectors[(r, s)], h[j])[i])
          for r, s in sectors}
    a0 = aa["+1,-1"]
    assert a0.det() != 0
    rotations = {}
    assert aa["+1,+1"] == S.ones(3)
    expected_a0 = S.Matrix([[1, -1, -1], [1, -1, 1], [1, 1, -1]])
    assert a0 == expected_a0
    for key in ("+1,-1", "-1,+1", "-1,-1"):
        a = aa[key]
        check("sector gram " + key, a.T * a - (4 * S.eye(3) - S.ones(3)))
        assert a.det() == -4
        rot = a * a0.inv()
        check("rotation " + key, rot.T * rot - S.eye(3))
        assert rot.det() == 1
        rotations[key] = dm(rot)
    b = [add(*(scale(mul(pc, h[j]), a0.inv()[j, k])
               for j in range(3))) for k in range(3)]
    for k in range(3):
        check("B hermitian", add(b[k], scale(dagger(b[k]), -1)))
    for i in range(3):
        for k in range(3):
            rhs = scale(pc, int(i == k))
            if i != k:
                other = ({0, 1, 2} - {i, k}).pop()
                sign = 1 if (i, k, other) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1
                rhs = add(rhs, scale(b[other], sign * S.I))
            check("B product", add(mul(b[i], b[k]), scale(rhs, -1)))
    m = {
        "00": scale(add(pc, b[2]), S.Rational(1, 2)),
        "11": scale(add(pc, scale(b[2], -1)), S.Rational(1, 2)),
        "01": scale(add(b[0], scale(b[1], S.I)), S.Rational(1, 2)),
        "10": scale(add(b[0], scale(b[1], -S.I)), S.Rational(1, 2)),
    }
    for x in "01":
        for y in "01":
            check("unit adjoint", add(dagger(m[x+y]), scale(m[y+x], -1)))
            for z in "01":
                for w in "01":
                    rhs = m[x+w] if y == z else {}
                    check("matrix units", add(mul(m[x+y], m[z+w]), scale(rhs, -1)))
    assert S.trace(dense(m["00"])) == S.trace(dense(m["11"])) == 3
    odd0 = mul(p0, add({"XII": 1}, {"YII": 1}, {"ZII": 1}))
    named = {"Pi0": p0, "Pic": pc, "Pi0_sumXYZ": odd0,
             "Bx": b[0], "By": b[1], "Bz": b[2]}
    named.update({"M" + key: value for key, value in m.items()})
    coords = {key: {space: coordinates(value, vectors)
                    for space, vectors in (("full", full), ("even", even), ("odd", odd))
                    if (space == "full" or (key in ("Pi0", "Pic") and space == "even")
                    or (key in ("Pi0_sumXYZ", "Bx", "By", "Bz") and space == "odd"))}
              for key, value in named.items()}
    # Each matrix unit has an even and an odd part with the appropriate sign.
    unit_parity = {}
    for key, value in m.items():
        if key in ("00", "11"):
            ve = scale(pc, S.Rational(1, 2))
            vo = scale(b[2], S.Rational(1, 2) if key == "00" else -S.Rational(1, 2))
        else:
            ve = {}
            vo = value
        check("unit parity", add(value, scale(add(ve, vo), -1)))
        unit_parity[key] = {"even": coordinates(ve, even), "odd": coordinates(vo, odd)}
    assert S.Matrix(64, 6, lambda i, j: [p0, pc, odd0, *b][j].get(word(i), 0)).rank() == 6
    assert S.Matrix(64, 2, lambda i, j: [p0, pc][j].get(word(i), 0)).rank() == 2
    assert S.Matrix(64, 4, lambda i, j: [odd0, *b][j].get(word(i), 0)).rank() == 4
    j, selected = canonical_columns(m["00"], b[0])
    check("J isometry", j.conjugate().T * j - S.eye(6))
    check("J range", j * j.conjugate().T - dense(pc))
    for x in "01":
        for y in "01":
            e = S.zeros(2); e[int(x), int(y)] = 1
            check("J matrix unit", j * S.kronecker_product(e, S.eye(3)) * j.conjugate().T - dense(m[x+y]))
            check("transpose encoded", dense(m[x+y]).T - j.conjugate() * S.kronecker_product(e.T, S.eye(3)) * j.T)
    naive = dense(pc).T - dense(pc)
    assert any(x != 0 for x in naive)
    assert any(x != 0 for x in dense(add({"III": 1}, scale(pc, -1))))
    sigma = [{"III": 1}, {"XII": 1}, {"YII": 1}, {"ZII": 1}]
    signs = [-1, 1, 1, 1]
    elcu = S.Matrix.vstack(*(dense(x) / 2 for x in sigma))
    klcu = S.Matrix.hstack(*(signs[k] * dense(x) / 2 for k, x in enumerate(sigma)))
    check("LCU E isometry", elcu.conjugate().T * elcu - S.eye(8))
    check("LCU K contraction", klcu * klcu.conjugate().T - S.eye(8))
    lcu_basis = {}
    for space, vectors, sign in (("even", even, 1), ("odd", odd, -1)):
        for index, vector in enumerate(vectors):
            actual = klcu * S.kronecker_product(S.eye(4), dense(vector)) * elcu
            check("LCU parity basis", actual - sign * dense(vector) / 2)
            lcu_basis[f"{space}_{index}"] = dm(actual)
    return {
        "C": obj["C"], "H": [sm(x) for x in h],
        "saved_basis": {key: [sm(x) for x in vectors] for key, vectors in
                        (("full", full), ("even", even), ("odd", odd))},
        "saved_basis_pointers": {key: obj[key]["independent_coefficient_rows"]
                                 for key in ("full", "even", "odd")},
        "A": {key: dm(val) for key, val in aa.items()}, "A0_inverse": dm(a0.inv()),
        "rotations": rotations, "B": {key: sm(val) for key, val in zip("xyz", b)},
        "M": {key: sm(val) for key, val in m.items()},
        "named": {key: sm(val) for key, val in named.items()},
        "coordinates": coords, "unit_parity_coordinates": unit_parity,
        "J": dm(j), "J_order": "logical qubit first, multiplicity three second",
        "J_projected_computational_indices": selected,
        "transpose_naive_residual": dm(naive),
        "full_oracle_at_zero_defect": dm(S.eye(8) - dense(pc)),
        "LCU": {"E": dm(elcu), "K": dm(klcu), "basis_contractions": lcu_basis},
        "ranks": {"full": 6, "even": 2, "odd": 4, "combined": 6, "intersection": 0},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--families", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert args.families == ["row", "column", "uniform"]
    sources = {name: args.evidence_root / "results" / "T4_final" / f"B55q0_{name}.json"
               for name in args.families}
    inputs = {name: json.loads(path.read_text()) for name, path in sources.items()}
    assert all(obj["grid"] == GRID for obj in inputs.values())
    assert all(obj["constraint"] == name for name, obj in inputs.items())
    for name, obj in inputs.items():
        expected = [[int(name == "uniform" or
                         (name == "row" and k // 3 == j) or
                         (name == "column" and k % 3 == j))
                     for j in range(1 if name == "uniform" else 3)] for k in range(9)]
        assert obj["C"] == expected
    assert mul({"XII": 1}, {"YII": 1}) == {"ZII": S.I}
    assert mul({"YII": 1}, {"ZII": 1}) == {"XII": S.I}
    assert mul({"ZII": 1}, {"XII": 1}) == {"YII": S.I}
    words = sum(GRID, [])
    h0 = add(*({key: 1} for key in words))
    identity = {"III": S.Integer(1)}
    w = scale(add({"XII": 1}, {"YIY": -1}), 1 / S.sqrt(2))
    q0 = {"YIX": S.Integer(1)}
    # Cheapest kills precede all saved-span decoding.
    check("W square", add(mul(w, w), scale(identity, -1)))
    check("W Hermitian", add(w, scale(dagger(w), -1)))
    check("W anti H0", add(mul(w, h0), mul(h0, w)))
    for p in words:
        check("Q0 star generator " + p,
              add(mul(mul(q0, {p: 1}), q0), star({p: 1})))
    negative_w = {}
    for name in ("row", "column"):
        obj = inputs[name]
        hfirst = add(*(scale({words[k]: 1}, obj["C"][k][0]) for k in range(9)))
        residual = add(mul(w, hfirst), mul(hfirst, w))
        assert residual, "W wrongly generalizes to first " + name
        negative_w[name] = {"first_generator": sm(hfirst), "anticommutator": sm(residual)}
    x = S.Symbol("x")
    charpoly = S.Poly(dense(h0).charpoly(x).as_expr(), x)
    expected_poly = S.Poly((x*x - 27) * (x*x - 3) ** 3, x)
    assert charpoly == expected_poly
    projectors = sector_projectors()
    for key, value in projectors.items():
        check("projector Hermitian", add(value, scale(dagger(value), -1)))
        check("projector idempotent", add(mul(value, value), scale(value, -1)))
        assert S.trace(dense(value)) == 2
        for key2, value2 in projectors.items():
            if key != key2:
                check("projector orthogonality", mul(value, value2))
        check("projector transpose", add(transpose(value), scale(projectors[(key[0], -key[1])], -1)))
    check("projector sum", add(*projectors.values(), scale(identity, -1)))
    p0 = projectors[(1, 1)]
    pc = add(identity, scale(p0, -1))
    assert S.trace(dense(p0)) == 2 and S.trace(dense(pc)) == 6
    result = {
        "schema": "t5-sparse-v1", "grid": GRID,
        "serialization": {"dense": "rows,cols,row-major entries of exact SymPy expression strings",
                          "pauli": "IXYZ word -> exact SymPy expression string",
                          "allowed_functions": ["Integer", "Rational", "Add", "Mul", "Pow", "I", "sqrt"]},
        "uniform": {"H0": sm(h0), "W": sm(w), "Q0": sm(q0),
                    "H0_dense": dm(dense(h0)), "W_dense": dm(dense(w)), "Q0_dense": dm(dense(q0)),
                    "characteristic_polynomial": str(charpoly.as_expr()),
                    "multiplicities": {"-3*sqrt(3)": 1, "-sqrt(3)": 3,
                                       "sqrt(3)": 3, "3*sqrt(3)": 1},
                    "operations_time_order": {"dagger": ["W", "U", "W"],
                                              "star": ["Q0", "U", "Q0"],
                                              "transpose": ["Q0", "W", "U", "W", "Q0"]}},
        "negative_W_generator_controls": negative_w,
        "projectors": {f"{r:+d},{s:+d}": sm(p) for (r, s), p in projectors.items()},
        "Pi0": sm(p0), "Pic": sm(pc),
        "families": {name: family(inputs[name], name, projectors, p0, pc, h0, q0)
                     for name in ("row", "column")},
    }
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "certificate.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
