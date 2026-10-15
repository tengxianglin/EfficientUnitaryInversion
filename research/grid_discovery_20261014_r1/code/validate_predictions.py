#!/usr/bin/env python3
"""Dense-matrix corroboration, exact phase/gauge tests and Fourier kill gates.

This module never infers general exactness from random exponentials. The
analytic proofs are in THEORY.md; numerical tests are finite-support evidence.
"""
from __future__ import annotations
import argparse, itertools, json, time
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.linalg import expm, block_diag
import sympy as sp
from grid_check import (G,J,LINES,PAIRS,BITS,from_tag,to_tag,mul_tag,comm_tag,
    bil,qval,rad,rank,linmap,physical_features,line_phases,power_support,write_fresh,sha)

SINGLE_M={'I':np.eye(2,dtype=np.complex128),'X':np.array([[0,1],[1,0]],dtype=np.complex128),
          'Y':np.array([[0,-1j],[1j,0]],dtype=np.complex128),'Z':np.diag([1,-1]).astype(np.complex128)}

def dense(s):
    out=np.ones((1,1),dtype=np.complex128)
    for p in s:out=np.kron(out,SINGLE_M[p])
    return out

def spectrum_shift_intersection(S,target):
    """a(t)=sum_gamma c_gamma exp(-i gamma t). Exact integer frequencies."""
    S=set(S)
    if target=='transpose':sets=[{x-y for x in S} for y in S]
    elif target in ('dagger','star'):sets=[{x+y for x in S} for y in S]
    else:raise ValueError(target)
    return sorted(set.intersection(*sets))

def real_gauge_certificate(B,q,base,n):
    # Abstract real-generator section: R_i=i^{-q_i}P_i, R(v)=ordered product.
    eta=[];phys=[to_tag(linmap(v,base),n) for v in range(16)]
    for v in range(16):
        tag='I'*n;e=qval(v,B,q)-sum((q>>i&1)*(v>>i&1) for i in range(4))
        for i in range(4):
            if v>>i&1:
                ee,tag=mul_tag(tag,to_tag(base[i],n));e+=ee
        assert tag==phys[v] and e%2==0
        eta.append(e%4)
    for u in range(16):
        for v in range(16):
            C=sum((u>>i&1)*(q>>i&1)*(v>>i&1) for i in range(4))
            C+=sum((u>>i&1)*(v>>j&1)*bil(1<<i,1<<j,B) for i in range(4) for j in range(i))
            abstract=(qval(u,B,q)+qval(v,B,q)-qval(u^v,B,q)+2*C)%4
            physical=mul_tag(phys[u],phys[v])[0]
            assert abstract==(physical+eta[u]+eta[v]-eta[u^v])%4
    return eta

def four_qubit_basis(B,q):
    base=[]
    for i in range(4):
        chars=['I']*4;chars[i]='Y' if q>>i&1 else 'X'
        for j in range(i):
            if bil(1<<i,1<<j,B):chars[j]='Z'
        base.append(from_tag(''.join(chars)))
    return base

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--exact',required=True,type=Path)
    ap.add_argument('--frozen',required=True,type=Path);ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--seed',type=int,default=20261014);args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=False);start=time.process_time()
    emb=json.loads((args.exact/'embedding1024.json').read_text());a=json.loads((args.exact/'abstract64.json').read_text())
    abst={c['B']:c for c in a['cases']};rng=np.random.default_rng(args.seed)
    matrices={to_tag(v,3):dense(to_tag(v,3)) for v in range(64)}
    controls={};gauges=[];raw=[];circuit_records=[];gates=[]
    maxerrs=Counter();kill_count=0;phase_gauges=0;allanti_examples=[]
    # All 1024 cases compared with historical records, without running their helpers.
    old=json.loads((args.frozen/'evidence/grid/independent_grid_certificates.json').read_text())['all_cases']
    bykey={(r['B'],r['q']):r for r in emb['cases']}
    for c in old:
        k=(c['form_mask'],c['linear_refinement_mask']);r=bykey[k];b=abst[k[0]]
        assert c['T_L']==b['support']
        assert c['lambda_fraction'][0]/c['lambda_fraction'][1]==float(r['cost']['lambda'])
        # Cardinalities are gauge-independent; the stored tag strings themselves are not.
    for r in emb['cases']:
        B,q=r['B'],r['q'];b=abst[B]
        base=r.get('basis',four_qubit_basis(B,q));n=3 if r['physical_n3'] else 4
        tags=[to_tag(linmap(v,base),n) for v in G]
        assert physical_features(tags)==(B,q)
        eta=real_gauge_certificate(B,q,base,n)
        gauges.append({'B':B,'q':q,'n':n,'basis':base,'phase_gauge_exponents':eta})
        if not r['physical_n3']:continue
        phases=line_phases(tags)
        # Exhaustive all 2^9 sign flips: product of all six context phases unchanged.
        for s in range(512):
            flipped=[(phases[k]+2*sum(s>>i&1 for i in line))%4 for k,line in enumerate(LINES)]
            assert sum(flipped)%4==sum(phases)%4
            phase_gauges+=1
        mats=[matrices[t] for t in tags]
        coeff=rng.integers(-4,5,size=9).tolist();theta=0.137
        H=sum(x*M for x,M in zip(coeff,mats));U=expm(-1j*theta*H)
        character_to_tag={}
        for w in range(64):
            t=to_tag(w,3)
            l=sum(comm_tag(t,to_tag(v,3))<<i for i,v in enumerate(base))
            character_to_tag.setdefault(l,t)
        assert len(character_to_tag)==16
        cost=r['cost'];lam=float(cost['lambda'])
        if 'character_witness' in cost:branches=[(cost['character_witness'],1.)]
        else:branches=[(l,num/16) for l,num in enumerate(cost['walsh_numerators_denominator_16']) if num]
        L=sum(c*matrices[character_to_tag[l]]@U@matrices[character_to_tag[l]] for l,c in branches)
        err=float(np.linalg.norm(L-U.T));p=1/lam**2;K=L/lam
        prob_err=float(np.linalg.norm(K.conj().T@K-p*np.eye(8)))
        vec=K.reshape(-1);tv=U.T.reshape(-1)
        choi_err=float(np.linalg.norm(np.outer(vec,vec.conj())-p*np.outer(tv,tv.conj())))
        assert max(err,prob_err,choi_err)<1e-11
        maxerrs['transpose_operator']=max(maxerrs['transpose_operator'],err)
        maxerrs['success_probability']=max(maxerrs['success_probability'],prob_err)
        maxerrs['transpose_choi']=max(maxerrs['transpose_choi'],choi_err)
        row={'B':B,'q':q,'coefficients':coeff,'theta':theta,'lambda_T':lam,'transpose_error':err,
             'success_probability_error':prob_err,'choi_error':choi_err}
        if b['line_modes']==[1]*6:
            star=[t for t in matrices if all(comm_tag(t,g)==(g.count('Y')+1)%2 for g in tags)]
            assert star
            w=star[0];Q=matrices[w];star_err=float(np.linalg.norm(Q@U@Q-U.conj()))
            A=mats[0];D=mats[1];C=A@D
            dag=(-U+A@U@A+D@U@D+C@U@C.conj().T)/2
            dag_err=float(np.linalg.norm(dag-U.conj().T));assert max(star_err,dag_err)<1e-11
            # Real one-query, two-ancilla SELECT construction, no controlled oracle.
            S=block_diag(np.eye(8),A,D,C)
            ha=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
            HH=np.kron(np.kron(ha,ha),np.eye(8))
            F=np.kron(np.diag([-1,1,1,1]),np.eye(8))
            V=HH@F@S@np.kron(np.eye(4),U)@S.conj().T@HH
            K0=V[:8,:8];cirerr=float(np.linalg.norm(K0-U.conj().T/2));assert cirerr<1e-11
            maxerrs['star']=max(maxerrs['star'],star_err);maxerrs['dagger']=max(maxerrs['dagger'],dag_err)
            maxerrs['dagger_circuit_block']=max(maxerrs['dagger_circuit_block'],cirerr)
            row.update(star_witness=w,star_error=star_err,dagger_error=dag_err,dagger_circuit_error=cirerr)
            allanti_examples.append({'B':B,'q':q,'grid':r['grid'],'star_witness':w,'dagger_conjugators':['III',tags[0],tags[1],mul_tag(tags[0],tags[1])[1]],
                'dagger_coefficients':['-1/2','1/2','1/2','1/2'],'phase_exponents':phases})
        else:
            line=next(line for k,line in enumerate(LINES) if not b['line_modes'][k])
            a0,b0,c0=line;A=mats[a0];D=mats[b0]
            HH=A+2*D+4*A@D
            I=np.eye(8);poly=(HH-7*I)@(HH+5*I)@(HH+3*I)@(HH-I)
            assert np.array_equal(poly,np.zeros((8,8)))
            # Exact complex-integer operations stored in complex128; values below 2^53.
            moments=[int(np.trace(np.linalg.matrix_power(HH,k)).real) for k in range(5)]
            assert moments==[2*sum(t**k for t in (7,-5,-3,1)) for k in range(5)]
            assert spectrum_shift_intersection([7,-5,-3,1],'dagger')==[]
            row['kill_line']=line;row['kill_spectrum']=[-5,-3,1,7];row['kill_moments']=moments;kill_count+=1
        raw.append(row)
    # Exact SymPy charpoly for the commuting-triple kill ray.
    X=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1);I=sp.eye(2)
    A=sp.kronecker_product(Z,I,I);B=sp.kronecker_product(I,Z,I);H=A+2*B+4*A*B
    spectrum={str(k):int(v) for k,v in H.eigenvals().items()}
    assert spectrum=={'7':2,'-5':2,'-3':2,'1':2}
    controls['commuting_kill']={'spectrum':spectrum,'gamma':spectrum_shift_intersection([7,-5,-3,1],'dagger')}
    controls['single_edge_XYZ_phase_control']={'distinct_spectrum':[1,-3],'gamma':spectrum_shift_intersection([1,-3],'dagger')}
    controls['J_1_4_4_phase_control']={'distinct_spectrum':[9,-3,-15],'gamma':spectrum_shift_intersection([9,-3,-15],'dagger')}
    assert controls['single_edge_XYZ_phase_control']['gamma']==[-2]
    assert controls['J_1_4_4_phase_control']['gamma']==[-6]
    # Target-aware covariance failure and repair for a genuinely complex Clifford.
    S=np.diag([1,1j]);Xn=SINGLE_M['X'];Un=expm(-0.37j*Xn);Vp=S@Un@S.conj().T
    naive=S@Un.T@S.conj().T;correct=S.conj()@Un.T@S.T
    controls['transpose_naive_covariance']={'theta':0.37,'naive_residual':float(np.linalg.norm(naive-Vp.T)),
                                           'correct_residual':float(np.linalg.norm(correct-Vp.T))}
    assert controls['transpose_naive_covariance']['naive_residual']>0.1
    assert controls['transpose_naive_covariance']['correct_residual']<1e-14
    # Failed H2-only conjecture: smallest mask with an actual 3-qubit witness.
    bad=next(r for r in emb['cases'] if r['physical_n3'] and abst[r['B']]['counts'][2] not in (10,16))
    controls['H2_only_counterexample']={k:bad[k] for k in ('B','q','grid')}
    controls['H2_only_counterexample']['counts']=abst[bad['B']]['counts'][:4]
    controls['H2_only_counterexample']['missing_after_H2']=abst[bad['B']]['missing_after_H2']
    # Full seven-case symbolic cubic coefficients, independent of random exponentials.
    proof=[]
    for rec in a['seven_case_H3_proof_table']:
        B=rec['B'];base=four_qubit_basis(B,0);tags=[to_tag(linmap(v,base),4) for v in G]
        pwr=power_support(tags,3);tag=to_tag(linmap(9,base),4)
        # Evaluate the six orders of the chosen distinct triple directly.
        coeff=0j
        for order in itertools.permutations(rec['triple']):
            t='IIII';e=0
            for v in order:
                z,t=mul_tag(t,to_tag(linmap(v,base),4));e+=z
            assert t==tag;coeff+=(1j)**(e%4)
        assert abs(coeff) in (2,6) and coeff.imag==0
        proof.append({**rec,'gaussian_coefficient':[int(coeff.real),0]})
    write_fresh(args.output/'matrix_raw.json',raw)
    write_fresh(args.output/'gauge_certificates.json',gauges)
    write_fresh(args.output/'all_anti_grids.json',allanti_examples)
    write_fresh(args.output/'controls.json',controls)
    write_fresh(args.output/'H3_seven_case_coefficients.json',proof)
    summary={'schema':'prediction-validation-v1','seed':args.seed,'dtype':'complex128','tolerance':1e-11,
             'physical_cases_tested':len(raw),'anti_cases_tested':len(allanti_examples),
             'commuting_kill_cases':kill_count,'phase_sign_gauges_tested':phase_gauges,
             'cocycle_gauges_cases':len(gauges),'cocycle_pair_equations':len(gauges)*256,
             'max_errors':dict(maxerrs),'cpu_seconds':time.process_time()-start,
             'historical_case_support_and_LCU_comparisons':len(old),'code_sha256':sha(__file__),
             'numerical_status':'finite-support','analytic_claims':'see THEORY.md, not inferred from numerical samples'}
    write_fresh(args.output/'summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
