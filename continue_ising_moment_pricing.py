"""Checkpointed numerical column generation for the complete n=21 fourth system.

This search does not certify a global maximum or full moment feasibility.
Frozen columns have a separate interval verifier.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,minimize
from ising_fourth_moments import FourthMoments,seed_pool
from ising_moment_pricing import MomentFunctional

BASE='a1207766abb8c3470016d7addbb6bc31305ae5ed'


def freeze_direction(s,y):
    z=np.round(y,6)
    return {'n':s.n,'second_coefficients':[str(Fraction(str(float(x)))) for x in z[:s.n]],
            'terms':[{'indices':list(s.representatives[j]),'coefficient':str(Fraction(str(float(x))))}
                     for j,x in enumerate(z[s.n:]) if x!=0]}


def dual(s,W):
    cols=s.reduced_indices();scale=np.array([41 if j<21 else 533 for j in cols])
    V=W[:,cols]*scale;t=s.target[cols]*scale;p=len(cols)
    r=linprog(np.r_[-t,t,1],A_ub=np.r_[np.c_[V,-V,-np.ones(len(W))],np.r_[np.ones(2*p),0][None,:]],
              b_ub=np.r_[np.zeros(len(W)),1],bounds=[(0,None)]*(2*p)+[(None,None)],
              method='highs-ipm',options={'time_limit':120})
    if not r.success:raise RuntimeError(('dual solver did not succeed',r.status,r.message))
    y=np.zeros(len(s.target));y[cols]=(r.x[:p]-r.x[p:2*p])*scale
    return y,float(-r.fun)


def primal(s,W):
    cols=s.reduced_indices();scale=np.array([41 if j<21 else 533 for j in cols])
    r=linprog(np.zeros(len(W)),A_eq=np.r_[W[:,cols].T*scale[:,None],np.ones((1,len(W)))],
              b_eq=np.r_[s.target[cols]*scale,1],bounds=(0,None),method='highs-ipm',options={'time_limit':120})
    result={'status':int(r.status),'message':r.message}
    if r.success:
        result['full_max_residual']=float(np.max(abs(W.T@r.x-s.target)))
        result['positive_weights']=[{'column':int(j),'weight':float(x)} for j,x in enumerate(r.x) if x>1e-10]
    return result


def run(cache,output,rounds,resume=False):
    s=FourthMoments(21);old=np.load(cache);cs=seed_pool();np.testing.assert_array_equal(old['couplings'],cs)
    W=old['W'];assert hashlib.sha256(W.astype('<f8').tobytes()).hexdigest()=='3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5'
    first=json.loads((Path(__file__).parent/'evidence/directed_fourth_pricing_n21.json').read_text())
    firstc=np.array(list(map(float,first['witness_couplings'])))
    W=np.r_[W,[s.features(firstc)]];cs=np.r_[cs,[firstc]]
    path=Path(output)
    data=json.loads(path.read_text()) if resume and path.exists() else {
        'base_commit':BASE,'initial_columns':1601,'records':[],
        'status':'Finite numerical directed column generation; interval inequalities are verified separately.'}
    if data['base_commit']!=BASE or data['initial_columns']!=1601:
        raise ValueError('Checkpoint origin does not match this experiment')
    if rounds<len(data['records']):
        raise ValueError('Requested rounds precede the saved checkpoint')
    for key in ('final_normalized_dual_gap','final_columns','next_direction','final_primal','stop_reason'):
        data.pop(key,None)
    data['requested_rounds']=rounds;data['run_complete']=False
    path.write_text(json.dumps(data,indent=2))
    for record in data['records']:
        c=np.array(list(map(float,record['witness_couplings'])))
        W=np.r_[W,[s.features(c)]];cs=np.r_[cs,[c]]
    for step in range(len(data['records']),rounds):
        y,gap=dual(s,W)
        print(f'Round {step}: columns={len(W)}, normalized finite dual gap={gap:.12g}',flush=True)
        if gap<1e-8:break
        direction=freeze_direction(s,y);f=MomentFunctional(direction);vector=np.r_[f.second,f.coefficients]
        scores=W@vector;upper=float(max(scores));target=float(f.exact_target())
        assert target-upper>0
        best_index=int(np.flatnonzero(scores>=upper-1e-8)[0])
        rng=np.random.default_rng(202611210840+step)
        starts=[cs[best_index,:-1],cs[-1,:-1]+rng.normal(size=41)*.5]
        trials=[];best=None
        for start_id,x in enumerate(starts):
            def loss(z):
                value,g=f.value_gradient(np.r_[z,0]);return -value,-g
            r=minimize(loss,x,jac=True,method='L-BFGS-B',options={'maxiter':120,'ftol':1e-12,'gtol':1e-8})
            c=np.r_[np.round(r.x,6),0];value=f.value_gradient(c,False)
            trials.append({'start':start_id,'iterations':int(r.nit),'score':float(value),'message':r.message})
            print(f'Round {step}, restart {start_id}: rounded price={value:.12g}, target={target:.12g}',flush=True)
            if best is None or value>best[0]:best=(value,c)
        if best[0]<=target+1e-4:
            data['stop_reason']='Local pricing did not cross target; not a global no-go';break
        c=best[1];feature=s.features(c)
        assert abs(vector@feature-best[0])<1e-9
        record={'round':step,'columns_before':len(W),'normalized_dual_gap_before':gap,
                'direction':direction,'exact_target_score':str(f.exact_target()),
                'finite_pool_upper_numerical':upper,'witness_couplings':list(map(lambda x:str(float(x)),c)),
                'witness_score_numerical':float(best[0]),'pricing_margin_numerical':float(best[0]-target),
                'best_start_pool_index':best_index,'restarts':trials,
                'new_column_sha256_le_f64':hashlib.sha256(feature.astype('<f8').tobytes()).hexdigest()}
        data['records'].append(record);path.write_text(json.dumps(data,indent=2))
        W=np.r_[W,[feature]];cs=np.r_[cs,[c]]
    y,gap=dual(s,W);data['final_normalized_dual_gap']=gap;data['final_columns']=len(W)
    data['next_direction']=freeze_direction(s,y);data['final_primal']=primal(s,W)
    data['run_complete']=True
    path.write_text(json.dumps(data,indent=2));return data


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('--output',required=True)
    p.add_argument('--rounds',type=int,default=4);p.add_argument('--resume',action='store_true');a=p.parse_args()
    result=run(a.cache,a.output,a.rounds,a.resume)
    print('Completed columns',result['final_columns'],'final gap',result['final_normalized_dual_gap'],
          'primal status',result['final_primal']['status'],flush=True)
