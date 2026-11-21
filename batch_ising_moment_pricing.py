"""Fixed-direction multi-start pricing. Discovery and finite LP evidence only."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from ising_fourth_moments import FourthMoments, seed_pool
from ising_moment_pricing import MomentFunctional
from continue_ising_moment_pricing import dual, primal, freeze_direction

ROOT=Path(__file__).parent
BASE='6a7d4f6b54f0343fe711eeb681738357dd728d8c'
FEATURE_SHA='3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5'


def fingerprint(a):
    return hashlib.sha256(np.asarray(a,dtype='<f8').tobytes()).hexdigest()


def prefix(cache):
    s=FourthMoments(21);a=np.load(cache);cs=seed_pool()
    np.testing.assert_array_equal(a['couplings'],cs)
    W=a['W'];assert fingerprint(W)==FEATURE_SHA
    old=json.loads((ROOT/'evidence/directed_fourth_pricing_n21.json').read_text())
    history=json.loads((ROOT/'evidence/iterated_fourth_pricing_n21.json').read_text())
    extra=[old['witness_couplings']]+[r['witness_couplings'] for r in history['records']]
    for c in extra:
        c=np.array(list(map(float,c)));cs=np.r_[cs,[c]];W=np.r_[W,[s.features(c)]]
    assert W.shape==(1609,1461)
    return s,cs,W,history['next_direction']


def run(cache,output):
    s,cs,W,direction=prefix(cache);f=MomentFunctional(direction)
    vec=np.r_[f.second,f.coefficients];scores=W@vec
    best=int(np.flatnonzero(scores>=max(scores)-1e-8)[0])
    data={'base_commit':BASE,'direction':direction,'exact_target':str(f.exact_target()),
          'initial_columns':len(W),'finite_pool_upper_numerical':float(max(scores)),
          'rng_seed':202611211034,'max_iterations':80,'records':[],'run_complete':False}
    rng=np.random.default_rng(data['rng_seed'])
    starts=[cs[best,:-1]]+[cs[1601+j,:-1]+rng.normal(size=41)*scale for j,scale in zip((0,2,4,6,7),(.2,.5,1,2,4))]
    for j,start in enumerate(starts):
        def loss(z):
            v,g=f.value_gradient(np.r_[z,0]);return -v,-g
        r=minimize(loss,start,jac=True,method='L-BFGS-B',options={'maxiter':80,'ftol':1e-12,'gtol':1e-8})
        c=np.r_[np.round(r.x,6),0];col=s.features(c);value=float(vec@col)
        accepted=value>float(f.exact_target())+1e-4
        data['records'].append({'start':j,'initial_couplings':list(map(str,start)),
            'iterations':int(r.nit),'solver_message':r.message,'accepted':accepted,
            'couplings':list(map(str,c)),'score_numerical':value,'feature_sha256_le_f64':fingerprint(col)})
        if accepted:W=np.r_[W,[col]]
        Path(output).write_text(json.dumps(data,indent=2)+'\n')
        print('start',j,'score',value,'accepted',accepted,flush=True)
    y,gap=dual(s,W);data.update(final_columns=len(W),final_normalized_gap=gap,
            final_primal=primal(s,W),next_direction=freeze_direction(s,y),run_complete=True)
    Path(output).write_text(json.dumps(data,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();run(a.cache,a.output)
