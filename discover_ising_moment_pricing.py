"""Reproducible local pricing and one-column finite LP diagnostics.

The independently verified fixed witness does not depend on rerunning this
optimizer. Local convergence or an infeasible finite LP is not a global proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,minimize
from ising_fourth_moments import seed_pool
from ising_moment_pricing import MomentFunctional

INPUT=Path(__file__).parent/'evidence/directed_fourth_pricing_n21.json'


def pricing():
    data=json.loads(INPUT.read_text());f=MomentFunctional(data)
    start=seed_pool()[data['discovery']['start_pool_index']]
    def loss(x):
        value,gradient=f.value_gradient(np.r_[x,0])
        return -value,-gradient
    result=minimize(loss,start[:-1],jac=True,method='L-BFGS-B',
                    options={'maxiter':100,'ftol':1e-12,'gtol':1e-8})
    c=np.r_[np.round(result.x,6),0]
    return {'base_commit':data['base_commit'],'status':'Local floating discovery, not global optimization.',
            'iterations':int(result.nit),'optimizer_message':result.message,
            'rounded_couplings':list(map(lambda x:str(float(x)),c)),
            'rounded_score':f.value_gradient(c,False),'target_score':str(f.exact_target())}


def study(cache):
    data=json.loads(INPUT.read_text());f=MomentFunctional(data);s=f.system
    if not cache:raise ValueError('Use the prior complete fourth-order feature cache')
    cached=np.load(cache);cs=seed_pool();np.testing.assert_array_equal(cached['couplings'],cs)
    W=cached['W'];assert W.shape==(1600,1461)
    assert hashlib.sha256(W.astype('<f8').tobytes()).hexdigest()=='3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5'
    c=list(map(float,data['witness_couplings']));new=s.features(c)
    direct=f.value_gradient(c,False)
    assert abs(direct-(np.r_[f.second,f.coefficients]@new))<1e-9
    W=np.r_[W,[new]];cols=s.reduced_indices();scale=np.array([41 if j<21 else 533 for j in cols])
    V=W[:,cols]*scale;target=s.target[cols]*scale
    primal=linprog(np.zeros(len(W)),A_eq=np.r_[V.T,np.ones((1,len(W)))],
                   b_eq=np.r_[target,1],bounds=(0,None),method='highs-ipm',options={'time_limit':120})
    p=len(cols)
    dual=linprog(np.r_[-target,target,1],
                A_ub=np.r_[np.c_[V,-V,-np.ones(len(V))],np.r_[np.ones(2*p),0][None,:]],
                b_ub=np.r_[np.zeros(len(V)),1],bounds=[(0,None)]*(2*p)+[(None,None)],
                method='highs-ipm',options={'time_limit':120})
    out={'base_commit':data['base_commit'],'columns':len(W),'full_feature_count':1461,
         'new_column_sha256_le_f64':hashlib.sha256(new.astype('<f8').tobytes()).hexdigest(),
         'primal_status':int(primal.status),'primal_message':primal.message,
         'dual_status':int(dual.status),'dual_message':dual.message,
         'status':'Finite numerical augmentation only; full uniformity remains unresolved.'}
    if primal.success:out['full_max_residual']=float(np.max(abs(W.T@primal.x-s.target)))
    if dual.success:
        y=np.zeros(1461);y[cols]=(dual.x[:p]-dual.x[p:2*p])*scale
        out['normalized_finite_pool_dual_gap']=float(-dual.fun)
        out['next_second_direction']=[{'distance':j+1,'coefficient':float(x)} for j,x in enumerate(y[:21]) if abs(x)>1e-7]
        out['next_fourth_direction']=[{'indices':list(s.representatives[j]),'coefficient':float(x)} for j,x in enumerate(y[21:]) if abs(x)>1e-7]
        out['next_direction_status']='Floating suggestion only; needs rational freezing and independent verification.'
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study',action='store_true');p.add_argument('--cache')
    a=p.parse_args();print(json.dumps(study(a.cache) if a.study else pricing(),indent=2))
