"""Certified gapped seed ensembles uniform in both parity sectors.

A zero cycle edge removes the flux distinction between the physical sectors;
the accompanying proof derives equal coefficient masses. Verification of
positive orbit weights uses exact rational inputs and 192-bit ball arithmetic.
"""
import json
from fractions import Fraction
from pathlib import Path
from flint import arb,arb_mat,fmpq,ctx
from ising_cycle_program_orbits import CycleProgramOrbits
from verify_ising_nonradial_matching import matching_labels


def verify(path):
    data=json.loads(Path(path).read_text())
    ctx.prec=data['precision_bits']
    for case in data['cases']:
        m=CycleProgramOrbits(case['n'])
        assert len(case['atoms'])==len(m.orbits)
        legal=set(matching_labels(m.n));columns=[];n_matching=0
        for atom in case['atoms']:
            if atom['kind']=='matching_pauli':
                assert atom['label'] in legal
                j=m.member[m.index[atom['label']]]
                col=[arb(int(i==j)) for i in range(len(m.orbits))]
                n_matching+=1
            else:
                theta=list(map(Fraction,atom['couplings']))
                assert len(theta)==m.N and any(x==0 for x in theta)
                col=m.ball_orbit_masses(theta)
            columns.append(col)
        A=arb_mat([[col[i] for col in columns] for i in range(len(m.orbits))])
        rhs=arb_mat([[arb(fmpq(len(o),len(m.labels)))] for o in m.orbits])
        det=A.det();assert not det.contains(0)
        p=A.solve(rhs)
        floor=Fraction(case['weight_floor'])
        assert all(p[i,0]>arb(fmpq(floor.numerator,floor.denominator)) for i in range(len(m.orbits)))
        assert sum((p[i,0] for i in range(len(m.orbits))),arb(0)).contains(1)
        residual=A*p-rhs
        assert all(residual[i,0].contains(0) for i in range(len(m.orbits)))
        print(m.n,'sites; matching/gapped seed orbits',n_matching,len(columns)-n_matching,flush=True)
        print('determinant',det,flush=True)
        print('minimum seed weight',min((p[i,0] for i in range(len(m.orbits))),key=float),flush=True)
        print('joint-parity normalization follows from the gap/gauge lemma; all p >',case['weight_floor'],flush=True)


if __name__=='__main__':
    verify(Path(__file__).parent/'evidence/joint_parity_program_designs.json')
