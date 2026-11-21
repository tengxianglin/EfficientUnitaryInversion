"""All-row local minimax model with bounded physical coupling changes.

Numerical discovery and replay, not an exact uniform design certificate.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm,expm_frechet
from scipy.optimize import linprog
from local_ising_moment_step import pool,ROOT
from batch_ising_moment_pricing import fingerprint
from verify_batch_moment_pricing import approximate_primal

BASE='5a0dc205791de699a6f6374656ded6c3fc51a67a'


def baseline(cache):
    s,cs,W=pool(cache)
    d=json.loads((ROOT/'evidence/local_moment_step_n21.json').read_text())
    for r in d['candidates']:
        c=np.array(list(map(float,r['couplings'])));col=s.features(c)
        assert fingerprint(col)==r['feature_sha256_le_f64']
        cs=np.r_[cs,[c]];W=np.r_[W,[col]]
    p=np.zeros(len(W))
    for r in d['final']['weights']:p[r['column']]=r['weight']
    return s,cs,W,p


def feature_jacobian(s,c):
    N=s.N;i=np.arange(N);j=(i+1)%N
    A=np.zeros((N,N));A[i,j]=2*c;A[j,i]=-2*c;R=expm(A)
    I=s.indices;blocks=R[I[:,:,None],I[:,None,:]];cof=np.empty_like(blocks)
    for u in range(4):
        for v in range(4):cof[:,u,v]=(-1)**(u+v)*np.linalg.det(np.delete(np.delete(blocks,u,axis=1),v,axis=2))
    J=np.empty((len(s.target),N-1))
    for k in range(N-1):
        E=np.zeros_like(A);E[k,k+1]=2;E[k+1,k]=-2
        B=expm_frechet(A,E,compute_expm=False)
        second=[]
        for dist in range(1,s.n+1):
            jj=(i+dist)%N
            second.append(np.mean(B[i,i]*R[jj,jj]+R[i,i]*B[jj,jj]-B[i,jj]*R[jj,i]-R[i,jj]*B[jj,i]))
        dv=np.einsum('ijk,ijk->i',cof,B[I[:,:,None],I[:,None,:]])
        J[:,k]=np.r_[second,np.bincount(s.ids,weights=dv,minlength=len(s.keys))/s.counts]
    return J


def run(cache,output,jac_cache=None):
    s,cs,W,p=baseline(cache);scale=np.r_[np.full(21,41),np.full(1440,533)]
    residual=(p@W-s.target)*scale;g=float(max(abs(residual)))
    chosen=sorted(range(len(W)),key=lambda j:(-p[j],j))[:4]
    checks=[];jac=[]
    for j in chosen:
        J=feature_jacobian(s,cs[j]);direction=np.random.default_rng(202611211443+j).normal(size=41)
        direction/=max(abs(direction));d=np.r_[direction,0];h=1e-5
        fd=(s.features(cs[j]+h*d)-s.features(cs[j]-h*d))/(2*h)
        defect=float(max(abs(J@direction-fd)));assert defect<1e-5
        jac.append(J);checks.append({'column':j,'weight':float(p[j]),'jvp_check_defect':defect})
        print('Jacobian checked',j,defect,flush=True)
    B=np.c_[tuple(p[j]*J*scale[:,None] for j,J in zip(chosen,jac))]
    if jac_cache:np.savez(jac_cache,B=B,chosen=chosen)
    data={'base_commit':BASE,'baseline_all_row_residual':g,'selected':checks,
          'jacobian_shape':list(B.shape),'weighted_scaled_jacobian_sha256_le_f64':fingerprint(B),
          'rounding_decimals':9,'radii':[.001,.01,.1],'trials':[],'run_complete':False}
    for radius in data['radii']:
        r=linprog(np.r_[np.zeros(B.shape[1]),1],A_ub=np.r_[np.c_[B,-np.ones(len(residual))],np.c_[-B,-np.ones(len(residual))]],
            b_ub=np.r_[-residual,residual],bounds=[(-radius,radius)]*B.shape[1]+[(0,None)],method='highs-ipm')
        assert r.success,(r.status,r.message)
        actual=residual.copy();trial={'radius':radius,'predicted_residual':float(r.fun),'candidates':[]}
        rounded_change=[]
        for q,j in enumerate(chosen):
            c=np.r_[np.round(cs[j,:-1]+r.x[q*41:(q+1)*41],9),0]
            assert all(c[:-1]!=0);col=s.features(c)
            actual+=p[j]*(col-W[j])*scale
            rounded_change.extend(c[:-1]-cs[j,:-1])
            trial['candidates'].append({'parent_column':j,'couplings':list(map(str,c)),
                                       'feature_sha256_le_f64':fingerprint(col)})
        linear=residual+B@np.array(rounded_change)
        trial['rounded_prediction_residual']=float(max(abs(linear)))
        trial['actual_fixed_weight_residual']=float(max(abs(actual)))
        trial['max_model_defect']=float(max(abs(actual-linear)))
        trial['uniform_taylor_bound']=float(68224*sum(p[j]*max(abs(np.array(rounded_change)[q*41:(q+1)*41]))**2 for q,j in enumerate(chosen)))
        assert trial['max_model_defect']<=trial['uniform_taylor_bound']+1e-9
        data['trials'].append(trial)
        Path(output).write_text(json.dumps(data,indent=2)+'\n')
        print('radius',radius,'prediction',r.fun,'actual',trial['actual_fixed_weight_residual'],flush=True)
    for trial in data['trials']:
        for r in trial['candidates']:W=np.r_[W,[s.features(list(map(float,r['couplings'])))]]
    final=approximate_primal(s,W,full=True);final['columns_1609_onward_weight']=final.pop('new_batch_total_weight')
    final['new_linearized_weight']=sum(r['weight'] for r in final['weights'] if r['column']>=1627)
    data.update(final=final,final_columns=len(W),run_complete=True)
    Path(output).write_text(json.dumps(data,indent=2)+'\n')
    print('final',final['objective'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('--output',required=True);p.add_argument('--jac-cache')
    a=p.parse_args();run(a.cache,a.output,a.jac_cache)
