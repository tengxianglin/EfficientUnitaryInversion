#!/usr/bin/env python3
"""Exact affine-spectrum controls and a one-workspace-qubit triangle encoder."""
import argparse
import json
from pathlib import Path
import time
import numpy as np
import sympy as sp
from scipy.linalg import expm
from verify_heisenberg_tied_inversion import matrix
from run_heisenberg_followup_extensions import triangle


def verify():
    rows=[]
    x=sp.Symbol('x')
    for row in triangle()['rays']:
        p=sp.Poly.from_list(list(map(sp.Integer,row['minimal_polynomial'])),x)
        center=-p.all_coeffs()[1]/p.degree()
        shifted=sp.Poly(sp.expand(p.as_expr().subs(x,x+center)),x)
        pure=len({i%2 for i,c in enumerate(reversed(shifted.all_coeffs())) if c})==1
        s,d=row['sum_J'],row['D']
        assert pure==(s==0 or d==0 or d==s*s or s*s==9*d)
        rows.append({'J':row['J'],'sum_J':s,'D':d,'distinct_spectrum_center':str(center),
                     'centered_minimal_polynomial':list(map(str,shifted.all_coeffs())),
                     'affine_spectrum_symmetric':pure})
    B=[sum((matrix(w) for w in words),sp.zeros(8)) for words in [('XXI','YYI','ZZI'),('IXX','IYY','IZZ'),('XIX','YIY','ZIZ')]]
    h=B[0]+4*B[1]+4*B[2]
    eigenvalues=[];columns=[];groups={}
    for value,multiplicity,vectors in h.eigenvects():
        orthogonal=sp.GramSchmidt(vectors,True)
        assert len(orthogonal)==multiplicity
        groups[value]=list(range(len(columns),len(columns)+multiplicity))
        columns.extend(orthogonal);eigenvalues.extend([value]*multiplicity)
    basis=sp.Matrix.hstack(*columns)
    clean=lambda m:m.applyfunc(sp.simplify)
    assert clean(basis.H*basis)==sp.eye(8)
    assert set(groups)=={sp.Integer(-15),sp.Integer(-3),sp.Integer(9)}
    kappa=sp.Integer(-6)
    workspace=2
    mapping={}
    for value,indices in groups.items():
        reflected=groups[kappa-value]
        for local,index in enumerate(indices):
            q=reflected[local%len(reflected)];a=local//len(reflected)
            assert a<workspace
            mapping[index*workspace]=q*workspace+a
    assert len(set(mapping.values()))==8
    remaining_in=[i for i in range(16) if i not in mapping]
    remaining_out=[i for i in range(16) if i not in mapping.values()]
    mapping.update(zip(remaining_in,remaining_out))
    permutation=sp.zeros(16)
    for source,target in mapping.items():permutation[target,source]=1
    b=sp.kronecker_product(basis,sp.eye(workspace))
    encoder=clean(b*permutation*b.H)
    initial=sp.kronecker_product(sp.eye(8),sp.eye(2)[:,0])
    assert clean(encoder.H*encoder)==sp.eye(16)
    assert clean(encoder.H*sp.kronecker_product(h,sp.eye(2))*encoder*initial-initial*(kappa*sp.eye(8)-h))==sp.zeros(16,8)
    en=np.array(encoder,dtype=np.complex128);hn=np.array(h,dtype=np.complex128);jn=np.array(initial,dtype=np.complex128)
    maximum=leakage=0.
    for a in [0.,*np.random.default_rng(20260909).normal(size=16)]:
        u=expm(-1j*a*hn);out=en.conj().T@np.kron(u,np.eye(2))@en@jn
        target=np.exp(6j*a)*u.conj().T
        maximum=max(maximum,float(np.linalg.norm(jn.conj().T@out-target)))
        leakage=max(leakage,float(np.linalg.norm(out-jn@target)))
    assert max(maximum,leakage)<1e-12
    return {'status':'VERIFIED_AFFINE_SPECTRUM_CONTROLS','rays':rows,
            'ray_scope':'49 primitive directions in [-2,2]^3, sign identified; affine property only, not a full channel classification',
            'representative':{'J':[1,4,4],'spectrum_multiplicities':{str(k):len(v) for k,v in groups.items()},
                              'kappa':str(kappa),'encoder_matrix':[[str(encoder[i,j]) for j in range(16)] for i in range(16)],
                              'generator_identity':'W^dagger(H tensor I2)W J=J(-6I8-H)',
                              'output':'exp(6ia)*U(a)^dagger','queries':1,'workspace_qubits':1,'success_probability':1,
                              'workspace_returned_to_0':True,'numerical_trials':17,'seed':20260909,
                              'max_residual':maximum,'max_leakage':leakage},
            'limits':'Extra ray spectral controls and one explicit encoding; no necessity theorem for arbitrary multi-Kraus channels, no minimal-workspace proof, no novelty claim'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('output exists')
    start=time.monotonic();r=verify();r['elapsed_seconds']=time.monotonic()-start
    with a.output.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print(r['status'])


if __name__=='__main__':main()
