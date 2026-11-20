"""Certified orbit-reduced physical program ensemble at seven sites.

Run with OPENBLAS_NUM_THREADS=2. Dependencies: NumPy, SciPy, python-flint.
No optimizer or discovery search is needed for verification.
"""
import json
from fractions import Fraction
from pathlib import Path
from flint import arb,arb_mat,fmpq,ctx
from ising_cycle_program_orbits import CycleProgramOrbits
from verify_ising_nonradial_matching import matching_labels
from verify_ising_radial_twirl import radial_gain


def verify(path):
    data = json.loads(Path(path).read_text())
    assert data['n'] == 7
    model = CycleProgramOrbits(data['n'])
    assert (len(model.labels),len(model.orbits),len(data['atoms'])) == (1716,85,85)
    ctx.prec = data['precision_bits']
    matching = set(matching_labels(model.n))
    columns = []
    n_matching = n_ham = 0
    for atom in data['atoms']:
        if atom['kind'] == 'matching_pauli':
            label = atom['label']
            assert label in matching
            orbit = model.member[model.index[label]]
            column = [arb(int(j == orbit)) for j in range(len(model.orbits))]
            n_matching += 1
        elif atom['kind'] == 'majorana_hamiltonian':
            column = model.ball_orbit_masses(atom['couplings'])
            n_ham += 1
        else:
            raise ValueError('Unknown physical seed')
        columns.append(column)
        if len(columns) % 10 == 0:
            print('Certified orbit-mass columns',len(columns),'of',len(data['atoms']),flush=True)
    A = arb_mat([[c[j] for c in columns] for j in range(len(model.orbits))])
    rhs = arb_mat([[arb(fmpq(len(o),len(model.labels))) ] for o in model.orbits])
    determinant = A.det()
    assert not determinant.contains(0)
    weights = A.solve(rhs)
    floor = Fraction(data['weight_floor'])
    assert all(weights[i,0] > arb(fmpq(floor.numerator,floor.denominator)) for i in range(len(model.orbits)))
    assert sum((weights[i,0] for i in range(len(model.orbits))),arb(0)).contains(1)
    residual = A*weights-rhs
    assert all(residual[i,0].contains(0) for i in range(len(model.orbits)))
    gain = radial_gain(model.n,'ml')
    assert gain == Fraction(8840048,429)
    assert len(model.labels)*gain == 35360192
    optimum = gain/Fraction(model.D**4)
    print('Physical orbit design:',n_matching,'matching seed orbits,',n_ham,'rational Hamiltonian seed orbits')
    print('Determinant enclosure:',determinant)
    print('Minimum exact seed weight enclosure:',min((weights[i,0] for i in range(len(model.orbits))),key=float))
    print('All exact seed weights >',data['weight_floor'])
    print('Exact seven-site all-Pauli target-component optimum:',optimum)
    return weights


if __name__ == '__main__':
    verify(Path(__file__).parent/'evidence/physical_orbit_program_design_n7.json')
