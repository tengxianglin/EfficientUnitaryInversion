"""Physical small-ring checks of the program-supported Pauli-twirl certificate.

The CP certificate is independent of the split probability. n=3,5 check its
algebra, not first-order cancellation of the long-ring six-query protocol.
Dependencies: NumPy and SciPy. Run with OPENBLAS_NUM_THREADS=2.
"""
from fractions import Fraction
from itertools import combinations
from math import comb

import numpy as np
from scipy.linalg import expm


def coefficients(n):
    return [
        sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-2*n+2*k), min(2*k, ell)+1)
        )
        for k in range(n+1)
    ]


def complementary_weight(n):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    a = coefficients(n)
    S = sum(comb(n, k)**2*a[k]**2 for k in range(n+1))//2-r*r
    return r*(D*D-r)-S


def verify_effect(n, callback=None):
    size = 2**n
    basis = [x for x in range(size) if x.bit_count() % 2 == 0]
    D = len(basis)
    sector = np.ix_(basis, basis)
    identity = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1])
    majoranas = []
    for site in range(n):
        for local in (x, -y):
            matrix = np.ones((1, 1))
            for j in range(n):
                matrix = np.kron(matrix, z if j < site else local if j == site else identity)
            majoranas.append(matrix)
    C = np.eye(size, dtype=complex)
    for g in majoranas[1::2]:
        C = C@g
    columns = []
    for degree in range(1, n, 2):
        for labels in combinations(range(2*n), degree):
            matrix = C.copy()
            for j in reversed(labels):
                matrix = majoranas[j]@matrix
            columns.append(matrix[sector].conj().reshape(-1)/np.sqrt(D))
    columns = np.column_stack(columns)
    Q = columns@columns.conj().T

    outside = []
    for mask in range(1 << (2*n-1)):
        if mask.bit_count() % 2:
            continue
        na = sum((mask >> (2*j)) & 1 for j in range(n))
        nb = sum((mask >> (2*j+1)) & 1 for j in range(n))
        if na == nb:
            continue
        matrix = np.eye(size, dtype=complex)
        for j in range(2*n):
            if (mask >> j) & 1:
                matrix = matrix@majoranas[j]
        outside.append(matrix[sector].reshape(-1)/np.sqrt(D))
    outside = np.stack(outside).conj()
    protected = np.eye(D*D)-outside.conj().T@outside
    # These dyadic projector entries are exact in binary64 at these sizes.
    pairs = [(basis[e], basis[r]) for e in range(D) for r in range(D)]
    for i, (e, r) in enumerate(pairs):
        F = e ^ r
        expected = Fraction(comb(F.bit_count(), F.bit_count()//2), 2**F.bit_count())
        assert protected[i, i] == float(expected)
        for j, (t, u) in enumerate(pairs):
            if (t ^ u) != F or ((r & F) == (u & F) and r != u):
                assert protected[i, j] == 0
    rows, columns = Q.nonzero()
    for row, column in zip(rows, columns):
        y, e = basis[row//D], basis[row % D]
        x, t = basis[column//D], basis[column % D]
        assert all(
            ((y >> k) & 1)+((e >> k) & 1)
            == ((x >> k) & 1)+((t >> k) & 1)
            for k in range(n)
        )
    beta = float(Fraction(complementary_weight(n), D**4))
    rng = np.random.default_rng(20261120+n)
    sdim = comb(2*n, n)//2
    assert abs(np.trace(protected).real-sdim) < 1e-10
    pe, pv = np.linalg.eigh(protected)
    recovery = pv[:, pe > 0.5].T.reshape(-1, D, D)*np.sqrt(D/sdim)
    np.testing.assert_allclose(
        sum(k.conj().T@k for k in recovery), np.eye(D), atol=2e-12, rtol=0
    )
    operators = outside.conj().reshape(-1, D, D)*np.sqrt(D)
    worst_support, worst_eigen, worst_negative = 0., 0., 0.
    for sample in range(7):
        fields = rng.normal(size=n)
        edges = rng.normal(size=n)
        if sample < 3:
            edges[:] = 0
            if sample != 1:
                fields[:] = 0
            if sample == 2:
                edges[0] = np.pi/2
        H = np.diag([
            sum(fields[j]*(-1)**((row >> j) & 1) for j in range(n)) for row in basis
        ]).astype(complex)
        for column, row in enumerate(basis):
            for j in range(n):
                flipped = row ^ (1 << j) ^ (1 << ((j+1) % n))
                H[basis.index(flipped), column] += edges[j]
        V = expm(1j*H)
        joint = (np.kron(V, V)@Q).reshape(D, D, D, D)
        amplitudes = joint.transpose(1, 3, 0, 2).reshape(D*D, D*D)
        kraus = (outside@amplitudes/np.sqrt(D)).reshape(-1, D, D)
        effect = np.einsum("rai,raj->ij", kraus.conj(), kraus)
        np.testing.assert_allclose(effect, beta*np.eye(D), atol=2e-12, rtol=0)

        corrected = np.einsum('rji,rjk->rik', operators.conj(), kraus)
        if callback is not None:
            callback(n, sample, V, Q, operators, corrected, protected)
        for a in corrected:
            vector = (V@a.conj().T).reshape(-1)
            defect = np.linalg.norm(vector-protected@vector)
            worst_support = max(worst_support, defect)
            assert defect < 2e-12
        columns = np.einsum('aij,rjk->arik', recovery, corrected).reshape(-1, D*D).T
        J = columns@columns.conj().T  # unnormalized Choi convention
        target = V.reshape(-1)
        weight = beta/sdim
        defect = np.linalg.norm(J@target-D*weight*target)
        worst_eigen = max(worst_eigen, defect)
        assert defect < 2e-12
        residual = J-weight*np.outer(target, target.conj())
        smallest = np.linalg.eigvalsh(residual).min()
        worst_negative = min(worst_negative, smallest)
        assert smallest > -2e-12
        # CP residual has the uniform trace effect (beta-weight) I.
        trace_effect = np.einsum('aiaj->ij', residual.reshape(D,D,D,D)).T
        np.testing.assert_allclose(trace_effect, (beta-weight)*np.eye(D), atol=2e-12, rtol=0)
    print(n, 'sites; 7 physical oracles; support/eigen/PSD defects',
          f'{worst_support:.3g}', f'{worst_eigen:.3g}', f'{worst_negative:.3g}')





if __name__ == '__main__':
    for n in (3, 5):
        verify_effect(n)
    for n in (21, 23, 83):
        D = 2**(n-1)
        sdim = comb(2*n, n)//2
        r = D*D-sdim
        reset_gain = Fraction(18*complementary_weight(n), r*r*D*D)
        twirl_gain = Fraction(18*complementary_weight(n), r*r*sdim)
        assert twirl_gain/reset_gain == Fraction(D*D, sdim) > 1
        assert twirl_gain <= Fraction(18, D*D-sdim)
        print(n, 'quadratic gain', f'{float(twirl_gain):.12g}',
              'gain/reset', f'{float(twirl_gain/reset_gain):.12g}')
