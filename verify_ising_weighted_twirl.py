"""Weighted program twirl: exact counting and physical small-ring CP checks.

Run OPENBLAS_NUM_THREADS=2 python verify_ising_weighted_twirl.py.
Long-ring outputs are certificates, not exact diamond norm optima.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb

import numpy as np
from verify_ising_program_twirl import coefficients, complementary_weight, verify_effect


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def intersection_certificate(n):
    """Exact L_max using intersection counts; no exponential label enumeration."""
    a = list(map(abs, coefficients(n)))
    cn = [comb(n, k) for k in range(n+1)]

    @lru_cache(None)
    def poly(i, k):
        return [(u, choose(i, u)*choose(n-i, k-u))
                for u in range(max(0, k-n+i), min(i, k)+1)]

    def row(i, j, k):
        return sum(x*y*a[(i+j+2*k)//2-u-v]
                   for u, x in poly(i, k) for v, y in poly(j, k))

    numerators = [0]*(n+1)
    for i in range(n+1):
        for j in range(n+1):
            if i == j or (i+j) % 2:
                continue
            w = [row(i, j, k) for k in range(n+1)]
            assert sum(w) % 2 == 0
            z = sum(w)//2  # quotient T by full Majorana complementation
            for k, wk in enumerate(w):
                numerators[k] += cn[i]*cn[j]*wk*z
    values = [Fraction(x, 2*cn[k]**2) for k, x in enumerate(numerators)]
    assert all(x.denominator == 1 for x in values)
    return max(values), values



def certificate(n):
    """Optimal support-only synthesis denominator via the middle Hamming layer."""
    a = list(map(abs, coefficients(n)))
    s = comb(2*n, n)//2
    numerator = 0
    for ell in range(1, 2*n, 2):
        if ell == n:
            continue
        z_twice = sum(choose(ell, u)*choose(2*n-ell, n-u)*a[(ell+n-2*u)//2]
                      for u in range(max(0, ell-n), min(ell, n)+1))
        assert z_twice % 2 == 0
        z = z_twice//2
        numerator += comb(2*n, ell)*z*z
    value = Fraction(numerator, 2*s)
    assert value.denominator == 1
    return value, [value]*(n+1)


def enumerate_certificate(n):
    """Independent exact enumeration; dimensions n=3,5,7 only."""
    labels = [m for m in range(1 << (2*n-1)) if m.bit_count() % 2 == 0]
    def balanced(m):
        return sum((m >> (2*j)) & 1 for j in range(n)) == sum(
            (m >> (2*j+1)) & 1 for j in range(n))
    ts = [m for m in labels if balanced(m)]
    rs = [m for m in labels if not balanced(m)]
    a = list(map(abs, coefficients(n)))
    w = [[a[(r ^ t).bit_count()//2] for t in ts] for r in rs]
    z = list(map(sum, w))
    values = [sum(row[j]*zr for row, zr in zip(w, z)) for j in range(len(ts))]
    M = complementary_weight(n)
    # Stronger than required: tests constant complementary weight on all
    # balanced Pauli labels at these finite sizes, not just physical generators.
    assert all(sum(row[j]**2 for row in w) == M for j in range(len(ts)))
    return max(values)


class PhysicalCheck:
    def __init__(self):
        self.cache = {}
        self.minimum = 0.
        self.max_trace_defect = 0.

    def __call__(self, n, sample, V, Q, operators, corrected, protected):
        d = len(V)
        if n not in self.cache:
            one = (np.eye(2), np.array([[0, 1], [1, 0]]),
                   np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]))
            paulis = []
            for factors in product(one, repeat=n-1):
                p = np.ones((1, 1))
                for factor in factors:
                    p = np.kron(p, factor)
                paulis.append(p)
            paulis = np.stack(paulis)
            vectors = paulis.reshape(d*d, d*d)/np.sqrt(d)
            selected = np.flatnonzero(np.einsum('ri,ij,rj->r',
                vectors.conj(), protected, vectors).real > 0.5)
            r_indices = np.argmax(abs(operators.reshape(-1, d*d)@vectors.conj().T), axis=1)
            # Contract the actual Q with every program Pauli at V=I.
            amplitudes = Q.reshape(d,d,d,d).transpose(1,3,0,2).reshape(d*d,d*d)
            ls = (vectors.conj()@amplitudes/np.sqrt(d)).reshape(-1,d,d)
            a = np.rint(d*d*abs(np.einsum('rij,rij->r', paulis.conj(), ls)/d)).astype(np.int64)
            weights = a[r_indices[:, None] ^ selected[None, :]]
            assert np.all(weights > 0)
            probs = weights/weights.sum(axis=1, keepdims=True)
            M = complementary_weight(n)
            Lmax, _ = certificate(n)
            cp_weight = float(Fraction(M*M, d**4)/Lmax)
            self.cache[n] = paulis[selected], probs, cp_weight, M/d**4
        recovery, probs, cp_weight, beta = self.cache[n]
        columns = np.einsum('tij,rjk->rtik', recovery, corrected)
        columns *= np.sqrt(probs)[:, :, None, None]
        columns = columns.reshape(-1,d*d).T
        J = columns@columns.conj().T
        target = V.reshape(-1)
        residual = J-cp_weight*np.outer(target,target.conj())
        smallest = np.linalg.eigvalsh(residual).min()
        self.minimum = min(self.minimum, smallest)
        assert smallest > -2e-12
        effect = np.einsum('aiaj->ij', residual.reshape(d,d,d,d)).T
        defect = np.linalg.norm(effect-(beta-cp_weight)*np.eye(d))
        self.max_trace_defect = max(self.max_trace_defect, defect)
        assert defect < 2e-12


if __name__ == '__main__':
    for n in (3, 5, 7):
        Lmax, values = certificate(n)
        assert enumerate_certificate(n) == Lmax
        assert intersection_certificate(n) == (Lmax, values)
        print(n, 'exact enumeration/counting agreement; distinct L_k', len(set(values)))
    check = PhysicalCheck()
    for n in (3, 5):
        verify_effect(n, callback=check)
    print('Weighted physical CP minimum eigenvalue/trace defect',
          f'{check.minimum:.3g}', f'{check.max_trace_defect:.3g}')
    for n in (21, 23, 83):
        d = 2**(n-1)
        s = comb(2*n,n)//2
        r = d*d-s
        M = complementary_weight(n)
        Lmax, values = certificate(n)
        gain = Fraction(18*M*M,r*r)/Lmax
        uniform_gain = Fraction(18*M,r*r*s)
        assert gain > uniform_gain > 0
        print(n, 'L_max', Lmax, 'distinct L_k', len(set(values)))
        print(n, 'certified quadratic gain', f'{float(gain):.12g}',
              'gain/uniform', f'{float(gain/uniform_gain):.12g}')
