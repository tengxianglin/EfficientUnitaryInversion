"""Pauli Fourier/minor criterion and exact single-mirror obstruction.

NumPy/SciPy checks are finite consistency checks, not proof by sampling.
The all-odd-n proof is in THEORY_PROGRAM_MINOR_OBSTRUCTION.md.
"""
import json
import platform
from fractions import Fraction
from itertools import combinations
from math import comb
import numpy as np
import scipy
from scipy.linalg import expm
from ising_cycle_program_orbits import CycleProgramOrbits


def rotation(c):
    N = len(c)
    A = np.zeros((N, N))
    for j, value in enumerate(c):
        k = (j + 1) % N
        A[j, k] += 2 * value
        A[k, j] -= 2 * value
    return expm(A)


def target(n, indices):
    k = len(indices) // 2
    v = sum(i % 2 for i in indices)
    return Fraction((-1) ** (v + k) * comb(n, k), comb(2*n, 2*k))


def mirror(n, length):
    R = np.eye(2*n, dtype=int)
    R[:length, :length] = 0
    for i in range(length):
        R[i, length-1-i] = (-1) ** i
    return R


def pair_sums(R):
    """Each unordered pair once, including antipodal pairs."""
    N = len(R)
    out = [0] * (N // 2)
    for i, j in combinations(range(N), 2):
        d = min(j-i, N-j+i)
        out[d-1] += int(R[i, i]*R[j, j] - R[i, j]*R[j, i])
    return out


def mirror_B_formula(n, L):
    N = 2*n
    outside = max(N-L-1, 0) - int(L == n)
    center = 2 * int(L in (1, N-1))
    transpositions = (1 + int(L == N) + 2*int(L >= n+1)) if L % 2 == 0 else (int(L >= n) + int(L >= n+2))
    return outside + center + transpositions


def two_segment(n, a, b):
    R = np.eye(2*n, dtype=int)
    for start, L in ((0, a), (a, b)):
        R[start:start+L, start:start+L] = mirror(n, L)[:L, :L]
    return R


def signed_permutation_minor(R, indices):
    indices = sorted(indices)
    columns = [int(np.flatnonzero(R[i])[0]) for i in indices]
    if set(columns) != set(indices):
        return 0
    inversions = sum(columns[i] > columns[j] for i in range(len(columns))
                     for j in range(i+1, len(columns)))
    return (-1)**inversions * int(np.prod([R[i,j] for i,j in zip(indices,columns)]))


def two_segment_screen():
    # Frozen basic solution discovered by HiGHS from all 861 pairs a,b>=1,
    # a+b<=42; only exact rational verification below is used as evidence.
    atoms = [(1,1,13),(1,39,84),(1,41,588),(3,35,84),(3,38,252),
             (4,37,168),(5,36,420),(6,35,504),(7,34,252),(8,33,672),
             (9,32,420),(10,31,252),(11,30,588),(12,29,420),(13,28,420),
             (14,27,336),(15,26,252),(16,25,504),(17,24,840),
             (18,23,336),(20,21,672)]
    assert sum(w for a,b,w in atoms) == 8077
    moments = [Fraction(0) for _ in range(21)]
    degree4 = Fraction(0)
    for a,b,w in atoms:
        R = two_segment(21,a,b)
        S = pair_sums(R)
        for d in range(1,22):
            moments[d-1] += Fraction(w,8077)*Fraction(S[d-1]*(2 if d==21 else 1),42)
        total = sum(signed_permutation_minor(R,[(shift+sign*j)%42 for j in range(4)])
                    for shift in range(42) for sign in (-1,1))
        degree4 += Fraction(w,8077)*Fraction(total,84)
    assert all(v == Fraction((-1)**(d+1),41) for d,v in enumerate(moments,1))
    t4 = target(21,[0,1,2,3])
    assert degree4 == Fraction(1,41) and t4 == Fraction(1,533)
    assert degree4-t4 == Fraction(12,533)
    return {'n':21, 'denominator':8077, 'atoms':atoms,
            'degree2_all_exact':True, 'degree4_probe':[0,1,2,3],
            'degree4_moment':str(degree4), 'degree4_target':str(t4),
            'degree4_residual':str(degree4-t4),
            'status':'Necessary degree-two screen passed; full uniformity disproved for this frozen ensemble.'}


def verify():
    output = {'base_commit': 'c294b68b6bcbc787684405d13780fb68551bf3d2',
              'python': platform.python_version(), 'numpy': np.__version__,
              'scipy': scipy.__version__, 'fourier_checks': [], 'mirror_checks': []}
    for n in (3, 5):
        model = CycleProgramOrbits(n)
        c = np.random.default_rng(112+n).normal(size=2*n)
        R = rotation(c)
        w = model.masses(c, reduce=False)
        maxerr = 0.0
        count = 0
        for mask in range(1 << (2*n-1)):
            if mask.bit_count() % 2:
                continue
            ix = [i for i in range(2*n) if mask >> i & 1]
            chars = np.array([(-1)**((mask & T).bit_count()) for T in model.labels])
            determinant = np.linalg.det(R[np.ix_(ix, ix)])
            maxerr = max(maxerr, abs(float(chars @ w) - determinant))
            assert Fraction(int(chars.sum()), len(model.labels)) == target(n, ix)
            count += 1
        assert maxerr < 1e-11
        output['fourier_checks'].append({'n': n, 'characters': count, 'max_error': maxerr})
        # Independent matrix exponential check of signed mirror formula.
        for L in range(1, 2*n+1):
            c = np.zeros(2*n)
            c[:L-1] = [np.pi/4*np.sqrt((j+1)*(L-j-1)) for j in range(L-1)]
            assert np.max(abs(rotation(c)-mirror(n, L))) < 1e-12
            exact = mirror(n,L)
            for ix in combinations(range(2*n),4):
                assert signed_permutation_minor(exact,ix) == round(np.linalg.det(exact[np.ix_(ix,ix)]))
        # Symmetric involution identity for a general closed physical cycle.
        Z = np.diag([(-1)**i for i in range(2*n)])
        Q = Z @ R
        np.testing.assert_allclose(Q, Q.T, atol=1e-12, rtol=0)
        np.testing.assert_allclose(Q@Q, np.eye(2*n), atol=1e-12, rtol=0)
        weighted = sum(-(-1)**(i+j)*(R[i,i]*R[j,j]-R[i,j]*R[j,i])
                       for i,j in combinations(range(2*n),2))
        assert abs(weighted-n) < 1e-11
    for n in (*range(5, 42, 2), 101):
        N = 2*n
        y = [Fraction((-1)**(d+1)) for d in range(1,n+1)]
        y[0], y[-2], y[-1] = Fraction(-1,2), Fraction(1,2), Fraction(-1)
        upper = Fraction(n-6, N)
        desired = sum(y[d-1]*Fraction((-1)**(d+1), N-1) for d in range(1,n+1))
        assert desired == Fraction(n-5, N-1)
        assert desired-upper == Fraction(3*(n-2), N*(N-1)) > 0
        actual_max = None
        for L in range(1,N+1):
            S = pair_sums(mirror(n,L))
            B = S[0]-S[-2]+2*S[-1]
            assert B == mirror_B_formula(n,L) >= 4
            phi = sum(y[d-1]*Fraction(S[d-1]*(2 if d==n else 1), N) for d in range(1,n+1))
            assert phi == Fraction(1,2)-Fraction(3*B,4*n) <= upper
            actual_max = phi if actual_max is None else max(actual_max,phi)
        assert actual_max == upper
        output['mirror_checks'].append({'n': n, 'lengths': N, 'target': str(desired),
                                       'sharp_upper': str(upper), 'gap': str(desired-upper)})
    output['two_segment_screen'] = two_segment_screen()
    return output


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
