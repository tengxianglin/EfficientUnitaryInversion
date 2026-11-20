"""Exact finite-oracle LP certificate and certified out-of-family CP obstruction.

Dependencies: NumPy, SciPy, python-flint. No optimization solver is needed:
the rational primal rule and matching averaging bound are checked exactly.
Run with OPENBLAS_NUM_THREADS=2; --ball-only skips the floating training checks.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import acb, acb_mat, arb, fmpq, ctx
from verify_ising_program_twirl import coefficients, verify_effect
from verify_ising_weighted_twirl import PhysicalCheck
from verify_ising_radial_twirl import radial_gain


def matching_labels(n):
    full = (1 << (2*n))-1
    result = set()
    for edges in range(1 << (2*n)):
        covered = 0
        for j in range(2*n):
            if (edges >> j) & 1:
                edge = (1 << j) | (1 << ((j+1) % (2*n)))
                if covered & edge:
                    break
                covered |= edge
        else:
            result.add(min(covered, covered ^ full))
    return sorted(result)


def matrices(n, labels):
    one = np.eye(2)
    x = np.array([[0,1],[1,0]])
    y = np.array([[0,-1j],[1j,0]])
    z = np.diag([1,-1])
    gammas = []
    for site in range(n):
        for local in (x, -y):
            matrix = np.ones((1,1))
            for j in range(n):
                matrix = np.kron(matrix, z if j < site else local if j == site else one)
            gammas.append(matrix)
    basis = [i for i in range(1 << n) if i.bit_count() % 2 == 0]
    result = []
    for label in labels:
        matrix = np.eye(1 << n, dtype=complex)
        for j in range(2*n):
            if (label >> j) & 1:
                matrix = matrix@gammas[j]
        result.append(matrix[np.ix_(basis,basis)])
    result = np.stack(result)
    assert np.all(np.isin(result.real, (-1,0,1)))
    assert np.all(np.isin(result.imag, (-1,0,1)))
    assert np.all(np.count_nonzero(result,axis=2) == 1)
    return result, basis


def exact_rule(data):
    n = data['n']
    R, B = data['r_labels'], data['t_labels']
    assert B == matching_labels(n) and len(B) == 91 and len(R) == 130
    def balanced(m):
        return sum((m >> (2*j)) & 1 for j in range(n)) == sum(
            (m >> (2*j+1)) & 1 for j in range(n))
    expected = [m for m in range(1 << (2*n-1))
                if m.bit_count() % 2 == 0 and not balanced(m)]
    assert R == expected and all(balanced(t) for t in B)
    q = [[Fraction(0)]*len(B) for _ in R]
    for i, j, value in data['probabilities']:
        q[i][j] = Fraction(value)
    assert all(all(x >= 0 for x in row) and sum(row) == 1 for row in q)
    a = coefficients(n)
    weights = [[a[(r ^ t).bit_count()//2]**2 for t in B] for r in R]
    gains = [sum(q[i][j]*weights[i][j] for i in range(len(R))) for j in range(len(B))]
    upper = Fraction(sum(max(row) for row in weights), len(B))
    assert set(gains) == {upper} and upper == Fraction(23880,91)
    assert upper/radial_gain(n, 'ml') == Fraction(18,13)
    print('Exact matching-ensemble optimum', upper, '; ratio to radial ML', Fraction(18,13))
    return np.array([[float(x) for x in row] for row in q])


def ball_witness(data, paulis, basis):
    n, d = data['n'], len(basis)
    theta = list(map(Fraction, data['witness_fields']+data['witness_edges']))
    H = [[Fraction(0) for _ in range(d)] for _ in range(d)]
    for column, row in enumerate(basis):
        H[column][column] = sum(theta[j]*(-1)**((row >> j) & 1) for j in range(n))
        for j in range(n):
            flipped = row ^ (1 << j) ^ (1 << ((j+1) % n))
            H[basis.index(flipped)][column] += theta[n+j]
    ctx.prec = 192
    V = acb_mat([[acb(0, fmpq(v.numerator,v.denominator)) for v in row] for row in H]).exp()
    mass = arb(0)
    for p in paulis:
        coefficient = acb(0)
        for i in range(d):
            for j in range(d):
                value = p[i,j].conjugate()
                if value:
                    coefficient += acb(int(round(value.real)),int(round(value.imag)))*V[i,j]/d
        # Multiplication rather than generic real exponentiation also handles
        # balls centered at zero, including cancellation in imaginary parts.
        mass += coefficient.real*coefficient.real+coefficient.imag*coefficient.imag
    assert mass < arb(fmpq(13,18))
    assert mass > arb(fmpq(5414777,10000000))
    assert mass < arb(fmpq(5414778,10000000))
    eta_fraction = Fraction(data['mixture_eta'])
    eta = fmpq(eta_fraction.numerator,eta_fraction.denominator)
    ratio = 1-eta+eta*fmpq(18,13)*mass
    assert ratio < arb(fmpq(98,100))
    print('Certified matching-support mass', mass)
    print('Certified mixture Bell upper / radial target weight', ratio)


class TrainingCheck(PhysicalCheck):
    def __init__(self, paulis, q, eta):
        super().__init__()
        self.paulis, self.q, self.eta = paulis, q, eta
        self.ratios = []
        self.residual_min = 0.

    def __call__(self, n, sample, V, Q, operators, A, protected):
        super().__call__(n, sample, V, Q, operators, A, protected)
        d = len(V)
        recovery, weighted, _, beta = self.cache[n]
        ml = np.isclose(weighted, weighted.max(axis=1,keepdims=True), rtol=1e-13, atol=0).astype(float)
        ml /= ml.sum(axis=1,keepdims=True)
        def choi(ops, probs):
            columns = np.einsum('tij,rjk->rtik', ops, A)*np.sqrt(probs)[:,:,None,None]
            columns = columns.reshape(-1,d*d).T
            return columns@columns.conj().T
        J = (1-self.eta)*choi(recovery,ml)+self.eta*choi(self.paulis,self.q)
        v = V.reshape(-1)
        ev, vectors = np.linalg.eigh(J)
        coords = vectors.conj().T@v
        support = ev > 1e-12*ev.max()
        assert np.linalg.norm(coords[~support]) < 1e-7
        weight = 1/np.sum(abs(coords[support])**2/ev[support])
        baseline = float(radial_gain(n,'ml'))/d**4
        self.ratios.append(float(weight/baseline))
        # Verify the reported finite weight directly, rather than relying only
        # on the inverse formula near a rank change.
        residual = J-weight*np.outer(v,v.conj())
        smallest = np.linalg.eigvalsh(residual).min()
        self.residual_min = min(self.residual_min,smallest)
        assert smallest > -2e-12
        assert weight > baseline*1.009


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ball-only', action='store_true')
    args = parser.parse_args()
    path = Path(__file__).parent/'evidence/nonradial_matching_n5.json'
    data = json.loads(path.read_text())
    q = exact_rule(data)
    paulis, basis = matrices(data['n'],data['t_labels'])
    ball_witness(data,paulis,basis)
    if not args.ball_only:
        training = TrainingCheck(paulis,q,float(Fraction(data['mixture_eta'])))
        verify_effect(5,callback=training)
        print('Training Choi weight ratios', training.ratios)
        print('Training minimum ratio/residual eigenvalue', min(training.ratios), training.residual_min)
