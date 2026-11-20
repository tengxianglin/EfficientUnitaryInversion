"""Sparse Pauli coefficients and physical dihedral orbit reduction for odd rings."""
from functools import lru_cache
from fractions import Fraction
import numpy as np
from scipy.linalg import eigh


class CycleProgramOrbits:
    def __init__(self,n):
        if n < 3 or n % 2 == 0:
            raise ValueError('An odd ring of at least three sites is required')
        self.n,self.N,self.size = n,2*n,1 << n
        self.D = 1 << (n-1)
        self.full = (1 << self.N)-1
        self.basis = np.array([x for x in range(self.size) if x.bit_count() % 2 == 0])
        self.lookup = {int(x):i for i,x in enumerate(self.basis)}
        self.labels = [m for m in range(1 << (self.N-1)) if m.bit_count() % 2 == 0
                       and sum((m >> (2*j)) & 1 for j in range(n)) ==
                           sum((m >> (2*j+1)) & 1 for j in range(n))]
        self.index = {m:j for j,m in enumerate(self.labels)}
        self.rows = np.stack([self.sparse(m)[0] for m in self.labels])
        self.phases = np.stack([self.sparse(m)[1] for m in self.labels])
        self.cols = np.broadcast_to(np.arange(self.D),self.rows.shape)
        unseen = set(self.labels)
        self.orbits = []
        while unseen:
            orbit = sorted({self.transform_label(min(unseen),s,sign)
                            for s in range(self.N) for sign in (-1,1)})
            assert set(orbit) <= set(self.labels)
            unseen -= set(orbit)
            self.orbits.append(orbit)
        self.member = np.empty(len(self.labels),int)
        for i,orbit in enumerate(self.orbits):
            self.member[[self.index[x] for x in orbit]] = i
        self.target = np.array([len(o) for o in self.orbits])/len(self.labels)
        self.Hbasis = []
        for j in range(self.N):
            u,v = j,(j+1) % self.N
            rows,phase = self.sparse((1 << u) | (1 << v))
            h = np.zeros((self.D,self.D),complex)
            h[rows,np.arange(self.D)] = phase*(1j if u < v else -1j)
            assert np.array_equal(h,h.T) and np.all(h.imag == 0)
            self.Hbasis.append(h.real)
        self.Hbasis = np.stack(self.Hbasis)
        self.entries = [[(int(i),int(j),int(h[i,j])) for i,j in zip(*h.nonzero())]
                        for h in self.Hbasis]
        # Every cycle bilinear is an allowed local field or Ising edge in
        # the selected parity block; the closing edge may carry a minus sign.
        for j,h in enumerate(self.Hbasis):
            site = j//2
            if j % 2 == 0:
                expected = np.diag([(-1)**((int(x) >> (n-1-site)) & 1) for x in self.basis])
            else:
                mask = (1 << (n-1-site)) | (1 << (n-1-((site+1) % n)))
                expected = np.zeros_like(h)
                expected[[self.lookup[int(x)^mask] for x in self.basis],np.arange(self.D)] = 1
            assert np.array_equal(h,expected) or np.array_equal(h,-expected)

    @lru_cache(None)
    def sparse(self,mask):
        perm = np.arange(self.size)
        phase = np.ones(self.size,complex)
        inputs = np.arange(self.size)
        for j in range(self.N):
            if (mask >> j) & 1:
                site = j//2
                bit = 1 << (self.n-1-site)
                prefix = ((1 << self.n)-1)^((1 << (self.n-site))-1)
                gamma = np.array([(-1)**(int(x)&prefix).bit_count() for x in inputs],complex)
                if j % 2:
                    gamma *= np.array([-1j*(-1)**int(bool(x&bit)) for x in inputs])
                shifted = inputs^bit
                perm,phase = perm[shifted],gamma*phase[shifted]
        return np.array([self.lookup[int(x)] for x in perm[self.basis]]),phase[self.basis]

    def transform_label(self,mask,shift,sign):
        value = sum(1 << ((shift+sign*j) % self.N) for j in range(self.N) if (mask >> j) & 1)
        return min(value,value^self.full)

    def transform_couplings(self,theta,shift,sign):
        permutation = [(shift+sign*j) % self.N for j in range(self.N)]
        inversions = sum(permutation[i] > permutation[j] for i in range(self.N) for j in range(i+1,self.N))
        signs = np.ones(self.N,int)
        signs[0] = (-1)**inversions  # signed permutation has determinant +1
        result = np.zeros(self.N,dtype=np.asarray(theta).dtype)
        for j in range(self.N):
            k = (j+1) % self.N
            edge = permutation[j] if sign == 1 else permutation[k]
            result[edge] = sign*signs[j]*signs[k]*theta[j]
        return result

    def masses(self,theta,reduce=True):
        h = np.einsum('a,aij->ij',theta,self.Hbasis)
        ev,u = eigh(h)
        v = (u*np.exp(1j*ev))@u.T
        coeff = np.sum(self.phases.conj()*v[self.rows,self.cols],axis=1)/self.D
        masses = abs(coeff)**2
        assert abs(masses.sum()-1) < 1e-10
        return np.bincount(self.member,weights=masses,minlength=len(self.orbits)) if reduce else masses

    def ball_orbit_masses(self,theta):
        from flint import acb,acb_mat,arb,fmpq
        theta = list(map(Fraction,theta))
        assert len(theta) == self.N
        h = [[Fraction(0) for _ in range(self.D)] for _ in range(self.D)]
        for x,entries in zip(theta,self.entries):
            for i,j,value in entries:
                h[i][j] += x*value
        v = acb_mat([[acb(0,fmpq(x.numerator,x.denominator)) for x in row] for row in h]).exp()
        result = [arb(0) for _ in self.orbits]
        factors = {1:acb(1),-1:acb(-1),1j:acb(0,-1),-1j:acb(0,1)}
        for rows,phases,orbit in zip(self.rows,self.phases,self.member):
            z = acb(0)
            for col,(row,phase) in enumerate(zip(rows,phases)):
                z += factors[complex(phase)]*v[int(row),col]
            z /= self.D
            result[orbit] += z.real*z.real+z.imag*z.imag
        assert sum(result,arb(0)).contains(1)
        return result


def self_check():
    from verify_ising_nonradial_matching import matrices
    rng = np.random.default_rng(202611201445)
    for n in (3,5):
        model = CycleProgramOrbits(n)
        dense,_ = matrices(n,model.labels)
        sparse = np.zeros_like(dense)
        for j,(rows,phase) in enumerate(zip(model.rows,model.phases)):
            sparse[j,rows,np.arange(model.D)] = phase
        assert np.array_equal(sparse,dense)
        theta = rng.normal(size=model.N)
        original = model.masses(theta,reduce=False)
        for shift in range(model.N):
            for sign in (-1,1):
                image = model.masses(model.transform_couplings(theta,shift,sign),reduce=False)
                indices = [model.index[model.transform_label(m,shift,sign)] for m in model.labels]
                np.testing.assert_allclose(image[indices],original,atol=2e-12,rtol=0)
        assert len(model.orbits) == (3 if n == 3 else 13)
        print(n,'exact sparse/dense Pauli agreement and all physical dihedral maps checked',flush=True)
    seven = CycleProgramOrbits(7)
    assert (len(seven.labels),len(seven.orbits)) == (1716,85)
    print('7-site orbit dimensions:',len(seven.labels),'->',len(seven.orbits),flush=True)


if __name__ == '__main__':
    self_check()
