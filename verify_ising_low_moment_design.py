"""Interval certificate for n=21 second moments and one fourth moment.

This is not a full program-uniformity certificate. A second fourth-order
probe is certified to fail. Frozen decimal couplings are exact rationals.
"""
import json
from fractions import Fraction
from pathlib import Path
from flint import arb,arb_mat,fmpq,ctx
from verify_ising_two_mirror_obstruction import permutation

N=42


def rational(x):
    x=Fraction(x)
    return arb(fmpq(x.numerator,x.denominator))


def build_rotation(atom):
    if atom['kind']=='perfect':
        p,s=permutation(atom['seed'])
        return arb_mat([[int(s[i]) if j==p[i] else 0 for j in range(N)] for i in range(N)])
    if atom['kind']=='fractional':
        L=atom['length'];alpha=rational(atom['alpha'])
        c=[alpha*arb.pi()/4*arb((j+1)*(L-j-1)).sqrt() for j in range(L-1)]
        c += [arb(0)]*(N-len(c))
    elif atom['kind']=='gapped':
        c=list(map(rational,atom['couplings']))
        assert len(c)==N and Fraction(atom['couplings'][-1])==0
    else:raise ValueError(atom['kind'])
    assert len(c)==N and c[-1].is_zero()
    A=arb_mat(N,N)
    for j in range(N-1):
        A[j,j+1]=2*c[j];A[j+1,j]=-2*c[j]
    return A.exp()


def minor(R,indices):
    return arb_mat([[R[i,j] for j in indices] for i in indices]).det()


def probe(R,indices):
    return sum((minor(R,[(shift+sign*j)%N for j in indices])
                for shift in range(N) for sign in (-1,1)),arb(0))/(2*N)


def features(R):
    m=[sum((R[i,i]*R[(i+d)%N,(i+d)%N]-R[i,(i+d)%N]*R[(i+d)%N,i]
            for i in range(N)),arb(0))/N for d in range(1,22)]
    q=probe(R,[0,1,2,3])
    # Finite interval consistency check of the analytic identity used to
    # infer the omitted equation after the exact square system is solved.
    relation=sum(((-1)**(d+1)*m[d-1] for d in range(1,21)),arb(0))+m[-1]/2-rational('1/2')
    assert relation.contains(0)
    return m+[q]


def verify(path):
    data=json.loads(Path(path).read_text());ctx.prec=data['precision_bits']
    assert len(data['atoms'])==22
    rots=[build_rotation(a) for a in data['atoms']]
    cols=[features(R) for R in rots]
    rows=list(range(20))+[21]
    A=arb_mat([[cols[j][i] for j in range(22)] for i in rows]+[[1]*22])
    rhs=arb_mat([[rational(Fraction((-1)**(d+1),41))] for d in range(1,21)]
                +[[rational('1/533')],[arb(1)]])
    det=A.det();assert not det.contains(0)
    p=A.solve(rhs);floor=rational(data['weight_floor'])
    assert all(p[j,0]>floor for j in range(22))
    assert sum((p[j,0] for j in range(22)),arb(0)).contains(1)
    # Check all 22 moment equations, including the analytically redundant one.
    for i in range(22):
        target=rational(Fraction((-1)**(i+2),41)) if i<21 else rational('1/533')
        assert (sum((p[j,0]*cols[j][i] for j in range(22)),arb(0))-target).contains(0)
    higher=[probe(R,[0,1,2,4]) for R in rots]
    moment=sum((p[j,0]*higher[j] for j in range(22)),arb(0))
    target=rational('-1/533');residual=moment-target
    assert not residual.contains(0)
    distant=[probe(R,[0,2,21,23]) for R in rots]
    distant_moment=sum((p[j,0]*distant[j] for j in range(22)),arb(0))
    distant_residual=distant_moment-rational('1/533')
    assert distant_residual>rational('1/100')
    return {'distant_probe':[0,2,21,23],
            'distant_probe_moment':str(distant_moment),
            'distant_probe_residual':str(distant_residual),
            'precision_bits' :ctx.prec,'atoms':22,'determinant':str(det),
            'minimum_weight':str(min((p[j,0] for j in range(22)),key=float)),
            'weight_floor':data['weight_floor'],'passed_moment_equations':22,
            'weights':[str(p[j,0]) for j in range(22)],
            'failed_probe':[0,1,2,4],'failed_probe_moment':str(moment),
            'failed_probe_target':'-1/533','failed_probe_residual':str(residual),
            'status':'Certified low-order existence, certified failure of full uniformity for this ensemble.'}


def audit_fourth(path,certificate):
    """All 1440 degree-four dihedral orbits, finite floating diagnostic."""
    import numpy as np
    from itertools import combinations
    from verify_ising_minor_obstruction import target
    atoms=json.loads(Path(path).read_text())['atoms']
    weights=[float(v.strip('[]').split(' +/- ')[0]) for v in certificate['weights']]
    indices=np.array(list(combinations(range(N),4)))
    def canonical(row):
        g=tuple(np.diff((*row,N+row[0])))
        return min(h[j:]+h[:j] for h in (g,g[::-1]) for j in range(4))
    keys=[canonical(tuple(r)) for r in indices]
    orbits=sorted(set(keys));lookup={key:i for i,key in enumerate(orbits)}
    ids=np.array([lookup[k] for k in keys]);counts=np.bincount(ids)
    representatives=[indices[np.flatnonzero(ids==i)[0]].tolist() for i in range(len(orbits))]
    moment=np.zeros(len(orbits))
    for atom,w in zip(atoms,weights):
        ball=build_rotation(atom)
        R=np.array([[float(ball[i,j]) for j in range(N)] for i in range(N)])
        values=np.linalg.det(R[indices[:,:,None],indices[:,None,:]])
        moment+=w*np.bincount(ids,weights=values,minlength=len(orbits))/counts
    required=np.array([float(target(21,r)) for r in representatives])
    residual=moment-required;i=int(np.argmax(abs(residual)))
    assert len(orbits)==1440 and representatives[i]==[0,2,21,23]
    assert sum(abs(residual)>1e-8)==1439
    return {'status':'Finite floating diagnostic; exact selected witnesses are certified separately.',
            'orbits':len(orbits),'quartets':len(indices),
            'max_abs_residual':float(abs(residual[i])),
            'worst_probe':representatives[i],
            'worst_moment':float(moment[i]),'worst_target':float(required[i]),
            'orbits_with_abs_residual_above_1e-8':int(sum(abs(residual)>1e-8))}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--audit-fourth',action='store_true')
    path=Path(__file__).parent/'evidence/ising_low_moment_design_n21.json'
    result=verify(path)
    if parser.parse_args().audit_fourth:result=audit_fourth(path,result)
    print(json.dumps(result,indent=2))
