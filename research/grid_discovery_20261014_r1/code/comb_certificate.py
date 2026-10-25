#!/usr/bin/env python3
"""Exact integer primal/dual one-query comb certificates, no SDP solver.

Tensor order is (external output o, oracle output a, oracle input b,
external input i), C-order indexing. The successful Kraus coefficient is t.
After proving every successful Kraus equals a constant times the target
linear map, C_success = p |t><t|. This script does NOT prove that premise
for a promise family; see THEORY.md and the independent Codex audit.
"""
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np


def certify(d: int, target: str = 'transpose') -> dict:
    if d not in (2, 4):
        raise ValueError('Bounded certificate supports d=2,4 only')
    if target not in ('transpose', 'adjugate2') or (target == 'adjugate2' and d != 2):
        raise ValueError('adjugate2 is defined only for d=2')
    t = np.zeros((d,d,d,d), dtype=np.int64)
    for o,a,b,i in np.ndindex(t.shape):
        t[o,a,b,i] = int(o==b and a==i) if target=='transpose' else int(a==b and o==i)-int(o==a and b==i)
    v=t.reshape(-1); T=np.outer(v,v)
    # Q = Tr_o |t><t|, integer matrix on (a,b,i).
    Q=np.trace(T.reshape((d,)*8),axis1=0,axis2=4).reshape(d**3,d**3)
    M=d*np.eye(d**3,dtype=np.int64)-Q
    assert np.array_equal(Q,Q.T) and np.array_equal(Q@Q,d*Q)
    assert np.array_equal(M,M.T) and np.array_equal(M@M,d*M)
    # These polynomial identities prove Q,M PSD: symmetric eigenvalues {0,d}.
    assert np.array_equal(np.trace(Q.reshape((d,)*6),axis1=0,axis2=3).reshape(d*d,d*d),np.eye(d*d,dtype=np.int64))
    # C_success=T/d^2, C1=I_(b,i)/d, Cdet=D/d^3.
    D=d*T+np.kron(np.eye(d,dtype=np.int64),M)
    assert np.array_equal(np.trace(D.reshape((d,)*8),axis1=0,axis2=4).reshape(d**3,d**3),d*d*np.eye(d**3,dtype=np.int64))
    assert int(np.trace(Q@Q))==d**3
    assert int(v@v)==d*d
    # Matrix-unit coefficient check (not random U samples).
    for a,b in np.ndindex((d,d)):
        X=np.zeros((d,d),dtype=np.int64);X[a,b]=1
        pred=X.T if target=='transpose' else np.trace(X)*np.eye(d,dtype=np.int64)-X
        assert np.array_equal(t[:,a,b,:],pred)
    nz=np.flatnonzero(v)
    return {'d':d,'target':target,'status':'exact_integer_certificate',
        'tensor_order':['o','a','b','i'],'flattening':'C-order',
        't_nonzero':[[int(k),int(v[k])] for k in nz],
        'primal_p':f'1/{d*d}','dual_upper_p':f'1/{d*d}',
        'Q_definition':'Tr_o(t t^T)', 'M_definition':'d I_(a,b,i) - Q',
        'C1_definition':'I_(b,i)/d','Cdet_definition':'(d t t^T + I_o tensor M)/d^3',
        'exact_checks':{'Q_squared_equals_d_Q':True,'M_squared_equals_d_M':True,
            'Tr_a_Q_equals_I_bi':True,'Tr_o_Cdet_equals_I_a_tensor_C1':True,
            'Tr_b_C1_equals_I_i':'symbolic identity','Tr_Q_squared':int(np.trace(Q@Q)),
            't_norm_squared':int(v@v),'matrix_units_checked':d*d},
        'upper_bound_reason':'Tr[Q Tr_o(Cdet)] = Tr(C1) = d >= p Tr(Q^2) = p d^3',
        'limitation':'Promise-family constant-amplitude and span reduction must be proved separately.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    start=time.process_time(); records=[certify(2),certify(4),certify(2,'adjugate2')]
    obj={'schema':'exact-comb-certificates-v1','cases':records,'dtype':'int64',
         'seed':None,'cpu_seconds':time.process_time()-start,
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'solver':'none; exact identities plus analytic positive-semidefiniteness proof'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
    print(json.dumps({'cases':len(records),'status':obj['schema'],'cpu_seconds':obj['cpu_seconds']}))
if __name__=='__main__':main()
