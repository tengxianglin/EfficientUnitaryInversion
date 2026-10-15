#!/usr/bin/env python3
"""Constructive target-aware Pauli block encodings; numerical linear certificates.

Independent of the r1 implementation. Every output directory must be fresh.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

TOL = 1e-10
G = [1, 2, 3, 4, 8, 12, 5, 10, 15]
BITS = {'I': (0, 0), 'X': (1, 0), 'Y': (1, 1), 'Z': (0, 1)}
REV = {v: k for k, v in BITS.items()}
SINGLE = {'I': np.eye(2, dtype=np.complex128),
          'X': np.array([[0, 1], [1, 0]], dtype=np.complex128),
          'Y': np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
          'Z': np.diag([1, -1]).astype(np.complex128)}


def dense(tag):
    out = np.ones((1, 1), dtype=np.complex128)
    for char in tag:
        out = np.kron(out, SINGLE[char])
    return out


def physical_tag(v, base):
    word = 0
    for i in range(4):
        if v >> i & 1:
            word ^= base[i]
    return ''.join(REV[(word >> i & 1, word >> (3+i) & 1)] for i in range(3))


def bil(u, v, B):
    return sum(((u >> i & 1)*(v >> j & 1) +
                (u >> j & 1)*(v >> i & 1))*(B >> k & 1)
               for k, (i, j) in enumerate(itertools.combinations(range(4), 2))) % 2


def symplectic_gs(B):
    remaining = [1, 2, 4, 8]
    pairs = []
    while True:
        choice = next(((a, b) for a, b in itertools.combinations(remaining, 2)
                       if bil(a, b, B)), None)
        if choice is None:
            break
        x, z = choice
        pairs.append((x, z))
        remaining = [w ^ (x if bil(w, z, B) else 0) ^
                     (z if bil(w, x, B) else 0)
                     for w in remaining if w not in (x, z)]
    assert all(w and all(bil(w, e, B) == 0 for e in [1, 2, 4, 8])
               for w in remaining)
    return pairs, remaining


def projector_basis(projector, count):
    """Solve commuting Pauli eigen-equations by projected coordinate columns."""
    columns = []
    for j in range(projector.shape[0]):
        v = projector[:, j].copy()
        for previous in columns:
            v -= previous * np.vdot(previous, v)
        norm = np.linalg.norm(v)
        if norm > TOL:
            v /= norm
            first = next(z for z in v if abs(z) > TOL)
            v *= np.conj(first)/abs(first)
            columns.append(v)
        if len(columns) == count:
            break
    assert len(columns) == count
    return np.stack(columns, axis=1)


def scalar_json(z):
    return [float(np.real(z)), float(np.imag(z))]


def dump(path, value):
    with Path(path).open('x') as out:
        json.dump(value, out, indent=2)
        out.write('\n')


def checked(residuals):
    assert all(np.isfinite(x) and x < TOL for x in residuals), max(residuals)


def encode_case(row, orbit, out):
    B, q = row['B'], row['q']
    pairs, radical = symplectic_gs(B)
    k, rdim = len(pairs), len(radical)
    d, m = 2**k, 2**(3-k-rdim)
    tags = [physical_tag(v, row['basis']) for v in range(16)]
    assert row['rank'] == 2*k
    for v, tag in enumerate(tags):
        expected_q = ((v & q).bit_count() + sum(
            (v >> i & 1)*(v >> j & 1)*(B >> bit & 1)
            for bit, (i, j) in enumerate(itertools.combinations(range(4), 2)))) % 2
        assert tag.count('Y') % 2 == expected_q
        for w, other in enumerate(tags):
            actual_comm = sum(BITS[a][0]*BITS[b][1] + BITS[a][1]*BITS[b][0]
                              for a, b in zip(tag, other)) % 2
            assert actual_comm == bil(v, w, B)
    pm = [dense(tag) for tag in tags]
    identity = np.eye(8, dtype=np.complex128)
    sectors, encodings, projectors, eigen_residuals = [], [], [], []
    sector_bits = list(itertools.product((0, 1), repeat=rdim))
    for bits in sector_bits:
        P = identity.copy()
        for bit, r in zip(bits, radical):
            P = P @ (identity + (-1)**bit * pm[r])/2
        vacuum = P.copy()
        for _, z in pairs:
            vacuum = vacuum @ (identity + pm[z])/2
        V = projector_basis(vacuum, m)
        columns = []
        for logical_bits in itertools.product((0, 1), repeat=k):
            block = V.copy()
            for bit, (x, _) in zip(logical_bits, pairs):
                if bit:
                    block = pm[x] @ block
            columns.extend(block[:, mu] for mu in range(m))
        E = np.stack(columns, axis=1)
        encodings.append(E)
        projectors.append(P)
        sectors.append({'bits': list(bits), 'central_eigenvalues': [(-1)**b for b in bits]})
        eigen_residuals.extend([float(np.linalg.norm(P @ E-E)),
                               float(np.linalg.norm(E @ E.conj().T-P))])
        for j, (x, z) in enumerate(pairs):
            for v, char in ((x, 'X'), (z, 'Z')):
                logical_tag = ''.join(char if t == j else 'I' for t in range(k))
                expected = np.kron(dense(logical_tag), np.eye(m))
                eigen_residuals.append(float(np.linalg.norm(pm[v] @ E-E @ expected)))
    C = np.concatenate(encodings, axis=1)
    unitary_residual = float(np.linalg.norm(C.conj().T @ C-identity))
    input_encoding = C.conj().T
    transpose_sector_permutation = []
    for bits in sector_bits:
        target = tuple(bit ^ (tags[r].count('Y') % 2) for bit, r in zip(bits, radical))
        transpose_sector_permutation.append(sector_bits.index(target))
    permutation_residuals = [float(np.linalg.norm(P.T-projectors[t]))
                             for P, t in zip(projectors, transpose_sector_permutation)]
    # Parameter map is sector-dependent: each original Hermitian grid term
    # maps to one signed logical Hermitian Pauli, with no discarded center.
    maps, reconstruction_residuals = [], []
    for v in range(16):
        sector_maps, rec = [], np.zeros((8, 8), dtype=np.complex128)
        for sector, E in enumerate(encodings):
            M = E.conj().T @ pm[v] @ E
            best = None
            for letters in itertools.product('IXYZ', repeat=k):
                logical_tag = ''.join(letters)
                L = np.kron(dense(logical_tag), np.eye(m))
                coefficient = np.trace(L.conj().T @ M)/(d*m)
                if abs(abs(coefficient)-1) < TOL:
                    sign = 1 if coefficient.real > 0 else -1
                    error = float(np.linalg.norm(M-sign*L))
                    best = {'sector': sector, 'logical_pauli': logical_tag,
                            'sign': sign, 'residual': error}
                    rec += E @ (sign*L) @ E.conj().T
                    break
            assert best is not None
            sector_maps.append(best)
        error = float(np.linalg.norm(rec-pm[v]))
        reconstruction_residuals.append(error)
        maps.append({'abstract_label': v, 'physical_pauli': tags[v], 'sectors': sector_maps,
                     'reconstruction_residual': error})
    # Algebra matrix units: all sectors and all logical i,j. Multiplicity is
    # retained coherently as I_m (rank4: M4 tensor I2).
    units, labels, unit_residuals = [], [], []
    for s, E in enumerate(encodings):
        for i in range(d):
            for j in range(d):
                eij = np.zeros((d, d), dtype=np.complex128)
                eij[i, j] = 1
                canonical = np.zeros((8, 8), dtype=np.complex128)
                sl = slice(s*d*m, (s+1)*d*m)
                canonical[sl, sl] = np.kron(eij, np.eye(m))
                physical = E @ np.kron(eij, np.eye(m)) @ E.conj().T
                labels.append((s, i, j))
                units.append(physical)
                errors = {
                    'encoding': float(np.linalg.norm(physical-C @ canonical @ input_encoding)),
                    'transpose': float(np.linalg.norm(physical.T-C.conj() @ canonical.T @ C.T)),
                    'star': float(np.linalg.norm(physical.conj()-C.conj() @ canonical.conj() @ C.T)),
                    'dagger': float(np.linalg.norm(physical.conj().T-C @ canonical.conj().T @ C.conj().T)),
                    'trace': float(abs(np.trace(physical)-(m if i == j else 0)))}
                unit_residuals.append({'sector': s, 'i': i, 'j': j, 'residuals': errors})
    multiplication_residuals = []
    for (s, i, j), F in zip(labels, units):
        for (t, a, b), H in zip(labels, units):
            expected = units[labels.index((s, i, b))] if s == t and j == a else np.zeros_like(F)
            multiplication_residuals.append(float(np.linalg.norm(F @ H-expected)))
    # Full physical input units include off-diagonal center/multiplicity
    # coherences. They are data states, not claimed oracle algebra elements.
    coherence_units = []
    for i in range(8):
        for j in range(8):
            unit = np.zeros((8, 8), dtype=np.complex128)
            unit[i, j] = 1
            physical = C @ unit @ C.conj().T
            coherence_units.append({'i': i, 'j': j, 'residuals': {
                'input_round_trip': float(np.linalg.norm(C.conj().T @ physical @ C-unit)),
                'transpose': float(np.linalg.norm(physical.T-C.conj() @ unit.T @ C.T)),
                'star': float(np.linalg.norm(physical.conj()-C.conj() @ unit.conj() @ C.T)),
                'dagger': float(np.linalg.norm(physical.conj().T-C @ unit.conj().T @ C.conj().T))}})
    all_errors = ([unitary_residual] + eigen_residuals + permutation_residuals +
                  reconstruction_residuals + multiplication_residuals +
                  [e for record in unit_residuals for e in record['residuals'].values()] +
                  [e for record in coherence_units for e in record['residuals'].values()] +
                  [a['residual'] for rec in maps for a in rec['sectors']])
    checked(all_errors)
    name = f'B{B:02d}_q{q:02d}'
    raw_path = out / f'{name}_raw.npz'
    with raw_path.open('xb') as handle:
        np.savez_compressed(handle, C=C, input_encoding=input_encoding,
                            transpose_output=C.conj(), transpose_input=C.T,
                            star_output=C.conj(), star_input=C.T,
                            dagger_output=C, dagger_input=C.conj().T,
                            sector_isometries=np.stack(encodings),
                            central_projectors=np.stack(projectors),
                            matrix_units=np.stack(units))
    result = {'B': B, 'q': q, 'rank': 2*k, 'orbit_size': orbit['size'],
              'grid': row['grid'], 'physical_basis': row['basis'],
              'symplectic_pairs': [list(p) for p in pairs], 'radical_basis': radical,
              'exact_input_checks': {'quadratic_values': 16, 'commutator_pairs': 256, 'passed': True},
              'logical_dimension': d, 'multiplicity': m, 'sectors': sectors,
              'transpose_sector_permutation': transpose_sector_permutation,
              'transpose_projector_residuals': permutation_residuals,
              'parameter_sign_map': [maps[v] for v in G], 'all_pauli_maps': maps,
              'matrix_unit_labels': [list(label) for label in labels],
              'matrix_unit_residuals': unit_residuals,
              'matrix_unit_multiplication_residuals': multiplication_residuals,
              'coherent_input_full_matrix_unit_residuals': coherence_units,
              'Pauli_equation_residuals': eigen_residuals,
              'unitarity_residual': unitary_residual,
              'max_residual': max(all_errors), 'raw_arrays': raw_path.name,
              'raw_sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest(),
              'encoding_convention': 'C maps canonical (sector,logical,multiplicity) to physical; columns solve Pauli equations',
              'target_encoding': {'T': 'C* V^T C^T', '*': 'C* V* C^T', 'dagger': 'C V^dagger C^dagger'},
              'query_contract': 'One original physical 8x8 forward oracle; block representation is not a free smaller oracle',
              'coherence': 'All center sectors and multiplicity retained by the same unitary C; no center measurement'}
    dump(out / f'{name}.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--representatives', choices=['quadratic37'], required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.input/'exact/embedding1024.json'
    emb = json.loads(source.read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    rows = {(r['B'], r['q']): r for r in emb['cases']}
    physical_orbits = [o for o in emb['orbits'] if o['physical_n3']]
    assert len(physical_orbits) == 37
    # Cheapest false-transfer control, evaluated before the larger audit.
    S = np.diag([1, 1j]).astype(np.complex128)
    angle = .37
    U = np.cos(angle)*SINGLE['I']-1j*np.sin(angle)*SINGLE['X']
    changed = S @ U @ S.conj().T
    naive = float(np.linalg.norm(changed.T-S @ U.T @ S.conj().T))
    corrected = float(np.linalg.norm(changed.T-S.conj() @ U.T @ S.T))
    assert naive > .1 and corrected < TOL
    controls = {'C': 'diag(1,i)', 'theta': angle,
                'naive_transpose_residual': naive,
                'corrected_transpose_residual': corrected,
                'expected': 'naive fails; target-aware passes'}
    dump(args.output/'S_gate_control.json', controls)
    results = [encode_case(rows[tuple(o['representative'])], o, args.output)
               for o in physical_orbits]
    summary = {'status': 'VERIFIED_FINITE_NUMERICAL', 'representatives_completed': len(results),
               'method': 'symplectic Gram-Schmidt + center projectors + Pauli-equation isometries',
               'arithmetic': 'complex128', 'tolerance': TOL, 'max_matrix_dimension': 8,
               'rank_histogram': {str(r): sum(x['rank'] == r for x in results) for r in (2, 4)},
               'matrix_units_checked': sum(len(x['matrix_unit_labels']) for x in results),
               'coherent_input_full_matrix_units_checked': sum(len(x['coherent_input_full_matrix_unit_residuals']) for x in results),
               'max_residual': max(r['max_residual'] for r in results),
               'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
               'S_gate_control': controls,
               'limitations': ['Numerical linear certificates at stated tolerance',
                               'Encoding gates have not been synthesized or optimized',
                               'No ancilla or known-gate optimality claim']}
    dump(args.output/'summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
