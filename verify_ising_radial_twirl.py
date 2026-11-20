"""Radial complementary recovery: exact gains and physical Choi eigenvectors.

Run OPENBLAS_NUM_THREADS=2 python verify_ising_radial_twirl.py.
Small physical sizes test identities, not the n>=21 cancellation protocol.
"""
from fractions import Fraction
from math import comb
from itertools import product
import numpy as np
from verify_ising_program_twirl import coefficients, verify_effect
from verify_ising_weighted_twirl import PhysicalCheck, choose


def radial_gain(n, rule):
    """G(q), exactly, using antipodally identified middle-layer counts."""
    a = list(map(abs, coefficients(n)))
    s = comb(2*n, n)//2
    total = Fraction(0)
    for ell in range(1, 2*n, 2):
        if ell == n:
            continue
        if rule == 'ml':
            row = Fraction(a[abs(ell-n)//2]**2)
        elif rule == 'weighted':
            den = num = 0
            for u in range(max(0, ell-n), min(ell, n)+1):
                count = choose(ell, u)*choose(2*n-ell, n-u)
                h = a[(ell+n-2*u)//2]
                den += count*h
                num += count*h**3
            row = Fraction(num, den)
        else:
            raise ValueError(rule)
        total += comb(2*n, ell)*row
    return total/(2*s)


class RadialCheck(PhysicalCheck):
    def __init__(self):
        super().__init__()
        self.eigen_defect = 0.
        self.residual_min = 0.
        self.optimum_defect = 0.
        self.results = []
        self.commutator_defect = 0.

    def __call__(self, n, sample, V, Q, operators, corrected, protected):
        super().__call__(n, sample, V, Q, operators, corrected, protected)
        recovery, weighted, old_cert, beta = self.cache[n]
        d = len(V)
        if sample == 3:
            one = (np.eye(2), np.array([[0,1],[1,0]]),
                   np.array([[0,-1j],[1j,0]]), np.diag([1,-1]))
            paulis = []
            for factors in product(one, repeat=n-1):
                matrix = np.ones((1,1))
                for factor in factors:
                    matrix = np.kron(matrix, factor)
                paulis.append(matrix)
            paulis = np.stack(paulis)
            vectors = paulis.reshape(d*d,d*d)/np.sqrt(d)
            amp = Q.reshape(d,d,d,d).transpose(1,3,0,2).reshape(d*d,d*d)
            ls = (vectors.conj()@amp/np.sqrt(d)).reshape(-1,d,d)
            alpha = d*d*np.einsum('rij,rij->r', paulis.conj(), ls)/d
            # Bell contraction includes a Pauli transpose sign; undo it to
            # reconstruct the actual P tensor conjugate(P) coefficients.
            alpha *= np.array([round(np.trace(p.T@p).real/d) for p in paulis])
            reconstructed = sum(a*np.kron(p,p.conj())/d**2 for a,p in zip(alpha,paulis))
            np.testing.assert_allclose(reconstructed, Q, atol=2e-12, rtol=0)
            joint = np.kron(V,V)
            for value in np.unique(np.rint(abs(alpha))):
                mask = np.isclose(abs(alpha), value)
                radial = sum(a*np.kron(p,p.conj())/d**2
                             for a,p in zip(alpha[mask],paulis[mask]))
                comm = np.linalg.norm(radial@joint-joint@radial)/(1+np.linalg.norm(radial))
                self.commutator_defect = max(self.commutator_defect, comm)
                assert comm < 2e-12
        for rule in ('weighted', 'ml'):
            probs = weighted.copy()
            if rule == 'ml':
                # At these sizes the integer likelihood ratios have gaps much
                # larger than binary64 rounding; identify all tied maximizers.
                probs = np.isclose(probs, probs.max(axis=1, keepdims=True),
                                   rtol=1e-13, atol=0).astype(float)
                probs /= probs.sum(axis=1, keepdims=True)
            columns = np.einsum('tij,rjk->rtik', recovery, corrected)
            columns *= np.sqrt(probs)[:, :, None, None]
            columns = columns.reshape(-1, d*d).T
            J = columns@columns.conj().T
            target = V.reshape(-1)
            weight = float(radial_gain(n, rule))/d**4
            defect = np.linalg.norm(J@target-d*weight*target)
            self.eigen_defect = max(self.eigen_defect, defect)
            assert defect < 2e-12
            residual = J-weight*np.outer(target, target.conj())
            smallest = np.linalg.eigvalsh(residual).min()
            self.residual_min = min(self.residual_min, smallest)
            assert smallest > -2e-12
            effect = np.einsum('aiaj->ij', residual.reshape(d,d,d,d)).T
            np.testing.assert_allclose(effect, (beta-weight)*np.eye(d), atol=2e-12, rtol=0)
            # Independently measure the maximal rank-one subtractable weight.
            eigenvalues, vectors = np.linalg.eigh(J)
            coordinates = vectors.conj().T@target
            supported = eigenvalues > 1e-11*eigenvalues.max()
            assert np.linalg.norm(coordinates[~supported]) < 1e-9
            measured = 1/np.sum(abs(coordinates[supported])**2/eigenvalues[supported])
            self.optimum_defect = max(self.optimum_defect, abs(measured-weight))
            assert abs(measured-weight) < 2e-12
            self.results.append((n, sample, rule, weight/old_cert))


def enumerate_ml(n):
    """Exact check of all ML sets and constant gain on every balanced label."""
    labels = [m for m in range(1 << (2*n-1)) if m.bit_count() % 2 == 0]
    def balance(m):
        return sum((m >> (2*j)) & 1 for j in range(n)) == sum(
            (m >> (2*j+1)) & 1 for j in range(n))
    ts = [m for m in labels if balance(m)]
    rs = [m for m in labels if not balance(m)]
    a = list(map(abs, coefficients(n)))
    gains = [Fraction(0)]*len(ts)
    bayes = 0
    for r in rs:
        row = [a[(r ^ t).bit_count()//2] for t in ts]
        best = max(row)
        winners = [j for j, h in enumerate(row) if h == best]
        imbalance = abs(sum((r >> (2*j)) & 1 for j in range(n))-
                        sum((r >> (2*j+1)) & 1 for j in range(n)))
        assert best == a[imbalance//2]
        for j in winners:
            gains[j] += Fraction(best*best, len(winners))
        bayes += best*best
    exact = radial_gain(n, 'ml')
    assert all(x == exact for x in gains)
    assert Fraction(bayes, len(ts)) == exact


if __name__ == '__main__':
    for n in (3, 5, 7):
        enumerate_ml(n)
        print(n, 'exact ML sets and constant-gain enumeration passed')
    check = RadialCheck()
    for n in (3, 5):
        verify_effect(n, callback=check)
    print('Radial eigen/PSD/optimal-weight defects', check.eigen_defect,
          check.residual_min, check.optimum_defect)
    print('Radial shared-kernel commutator defect', check.commutator_defect)
    for n in (21, 23, 83):
        d = 2**(n-1)
        s = comb(2*n, n)//2
        r = d*d-s
        a1 = comb(2*n-2, n-1)//n
        lower = Fraction(36*n*(n-1)*a1*a1, (n+1)*(n+2)*r*r)
        weighted = 18*radial_gain(n, 'weighted')/r**2
        ml = 18*radial_gain(n, 'ml')/r**2
        assert ml > weighted > 0 and ml >= lower
        print(n, 'weighted exact gain', f'{float(weighted):.12g}',
              'ML exact gain', f'{float(ml):.12g}',
              'inverse-cube lower term', f'{float(lower):.12g}')
