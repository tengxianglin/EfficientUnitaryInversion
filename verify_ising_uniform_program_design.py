"""Computer-assisted n=5 converse for arbitrary stochastic Pauli corrections.

The physical prior weights are the unique exact solution of A p = 1/126.
Arb enclosures verify invertibility and strict positivity, so this is an
existence certificate, not an approximately uniform sampled ensemble.
Dependencies: NumPy, SciPy (shared helpers), python-flint. No optimizer needed.
"""
import json
from fractions import Fraction
from pathlib import Path
from flint import acb, acb_mat, arb, arb_mat, fmpq, ctx
from verify_ising_nonradial_matching import matrices, matching_labels
from verify_ising_program_twirl import coefficients
from verify_ising_radial_twirl import radial_gain


def fq(x):
    x = Fraction(x)
    return fmpq(x.numerator,x.denominator)


def masses(theta,n,paulis,basis):
    d = len(basis)
    H = [[Fraction(0) for _ in range(d)] for _ in range(d)]
    for col,row in enumerate(basis):
        H[col][col] = sum(theta[j]*(-1)**((row >> j) & 1) for j in range(n))
        for j in range(n):
            flipped = row ^ (1 << j) ^ (1 << ((j+1) % n))
            H[basis.index(flipped)][col] += theta[n+j]
    V = acb_mat([[acb(0,fq(x)) for x in row] for row in H]).exp()
    result = []
    for p in paulis:
        z = acb(0)
        for i in range(d):
            for j in range(d):
                value = p[i,j].conjugate()
                if value:
                    z += acb(int(round(value.real)),int(round(value.imag)))*V[i,j]/d
        result.append(z.real*z.real+z.imag*z.imag)
    assert sum(result,arb(0)).contains(1)
    return result


def verify(path):
    data = json.loads(Path(path).read_text())
    n = data['n']
    assert n == 5 and len(data['atoms']) == 126
    ctx.prec = data['precision_bits']
    d = 2**(n-1)
    def balanced(m):
        return sum((m >> (2*j)) & 1 for j in range(n)) == sum(
            (m >> (2*j+1)) & 1 for j in range(n))
    labels = [m for m in range(1 << (2*n-1)) if m.bit_count() % 2 == 0]
    S = [m for m in labels if balanced(m)]
    R = [m for m in labels if not balanced(m)]
    assert (len(S),len(R)) == (126,130)
    paulis,basis = matrices(n,S)
    legal = set(matching_labels(n))
    columns = []
    matching = 0
    for atom in data['atoms']:
        if atom['kind'] == 'matching_pauli':
            assert atom['label'] in legal
            column = [arb(int(t == atom['label'])) for t in S]
            matching += 1
        elif atom['kind'] == 'hamiltonian':
            theta = list(map(Fraction,atom['coefficients']))
            assert len(theta) == 2*n
            column = masses(theta,n,paulis,basis)
        else:
            raise ValueError('Unknown physical oracle atom')
        columns.append(column)
    A = arb_mat([[column[j] for column in columns] for j in range(len(S))])
    determinant = A.det()
    assert not determinant.contains(0)
    rhs = arb_mat([[arb(fmpq(1,len(S)))] for _ in S])
    weights = A.solve(rhs)
    assert all(weights[i,0] > 0 for i in range(len(S)))
    # Strong, portable lower margin; exact normalization follows analytically
    # from unit column sums and A p = 1/126, not just from these ball checks.
    assert all(weights[i,0] > arb(fmpq(7,100000)) for i in range(len(S)))
    assert sum((weights[i,0] for i in range(len(S))),arb(0)).contains(1)
    residual = A*weights-rhs
    assert all(residual[i,0].contains(0) for i in range(len(S)))
    a = coefficients(n)
    adversary_bound = Fraction(sum(max(a[(r ^ t).bit_count()//2]**2 for t in S) for r in R),len(S))
    assert adversary_bound == radial_gain(n,'ml') == Fraction(3980,21)
    print('Certified physical design:',matching,'matching Paulis,',126-matching,'rational Hamiltonians')
    print('Determinant enclosure:',determinant)
    print('All exact prior weights > 7/100000; sum = 1 by exact column normalization')
    print('Minimum weight enclosure:',min((weights[i,0] for i in range(len(S))),key=float))
    print('Exact all-Pauli target-component optimum:',adversary_bound/Fraction(d**4))
    return weights


if __name__ == '__main__':
    verify(Path(__file__).parent/'evidence/physical_uniform_program_design_n5.json')
