#!/usr/bin/env python3
"""Exact one-query phase-covariant inverter for a single isotropic edge.

H=XX+YY+ZZ, U(a)=exp(-iaH). Two clean workspace qubits permit a fixed
encoding with output exp(2ia)U(a)^dagger. No controlled unknown U is used.
"""

import argparse
import json
from pathlib import Path
import time

import numpy as np
import sympy as sp
from scipy.linalg import expm

from verify_heisenberg_tied_inversion import matrix


def verify():
    h = matrix("XX") + matrix("YY") + matrix("ZZ")
    i4 = sp.eye(4)
    e = [i4[:,i] for i in range(4)]
    basis = sp.Matrix.hstack(e[0], (e[1]+e[2])/sp.sqrt(2), e[3], (e[1]-e[2])/sp.sqrt(2))
    assert basis.H*basis==i4 and basis.H*h*basis==sp.diag(1,1,1,-3)
    prescribed = {0:12, 4:13, 8:14, 12:0}
    unused_in = [i for i in range(16) if i not in prescribed]
    unused_out = [i for i in range(16) if i not in prescribed.values()]
    permutation = prescribed | dict(zip(unused_in,unused_out))
    p = sp.zeros(16)
    for source,target in permutation.items():
        p[target,source]=1
    b = sp.kronecker_product(basis,i4)
    encoder = b*p*b.H
    assert encoder.H*encoder==sp.eye(16)
    initial = sp.kronecker_product(i4,e[0])
    dressed_h = encoder.H*sp.kronecker_product(h,i4)*encoder
    assert dressed_h*initial == initial*(-2*i4-h)
    assert h*h+2*h-3*i4==sp.zeros(4) and h!=sp.zeros(4)
    en = np.array(encoder,dtype=np.complex128)
    initialn = np.array(initial,dtype=np.complex128)
    hn = np.array(h,dtype=np.complex128)
    rows=[]
    for a in [0.,*np.random.default_rng(20260909).normal(size=34)]:
        u=expm(-1j*a*hn)
        full=en.conj().T@np.kron(u,np.eye(4))@en@initialn
        clean=initialn.conj().T@full
        target=np.exp(2j*a)*u.conj().T
        residual=float(np.linalg.norm(clean-target))
        leakage=float(np.linalg.norm(full-initialn@clean))
        unitarity=float(np.linalg.norm(clean.conj().T@clean-np.eye(4)))
        assert max(residual,leakage,unitarity)<1e-12
        rows.append({"a":float(a),"phase_covariant_residual":residual,"workspace_leakage":leakage,
                     "successful_block_unitarity_residual":unitarity})
    return {"status":"VERIFIED_EXACT_PHASE_COVARIANT_DETERMINISTIC_INVERTER",
            "family":"H=XX+YY+ZZ, U(a)=exp(-iaH), all real a",
            "constant_amplitude_obstruction":"H^2-3I=-2H !=0; forbids fixed c linear operator equality",
            "actual_output":"exp(2ia)*U(a)^dagger",
            "channel_output":"rho -> U(a)^dagger rho U(a), probability 1",
            "encoding_basis_eigenvalues":[1,1,1,-3],
            "query_times_workspace_basis":"query eigenvector index *4 + workspace index",
            "encoding_permutation":permutation,
            "encoder_matrix":[[str(encoder[i,j]) for j in range(16)] for i in range(16)],
            "exact_generator_intertwining":"W^dagger(H tensor I4)W J=J(-2I4-H), J=I4 tensor |00>",
            "exact_checks":{"encoder_unitary":True,"invariant_code_subspace":True,"generator_identity":True},
            "resources":{"unknown_queries":1,"workspace_qubits":2,"workspace_dimension":4,
                         "success_probability":1,"sequence":"W -> (U tensor I4) -> W^dagger",
                         "workspace_returned_to_00":True,"controlled_unknown_U":False},
            "numerical":{"seed":20260909,"dtype":"complex128","trials":rows,"tolerance":1e-12},
            "limits":"Single known isotropic-edge direction only; does not invert an arbitrary independent XYZ family; no minimal-workspace or elementary-gate-optimality claim; novelty unverified"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.output.exists():p.error('output exists')
    start=time.monotonic();result=verify();result['elapsed_seconds']=time.monotonic()-start
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(result['status'])


if __name__=='__main__':main()
