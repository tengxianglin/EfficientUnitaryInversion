"""Exact-input interval witnesses; optional complete numerical batch replay."""
import argparse
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from flint import ctx
from ising_moment_pricing import MomentFunctional
from verify_ising_moment_pricing import ball,ball_functional
from batch_ising_moment_pricing import prefix,fingerprint,ROOT
from continue_ising_moment_pricing import dual,primal


def approximate_primal(s,W,full=False):
    cols=np.arange(len(s.target)) if full else np.array(s.reduced_indices());scale=np.where(cols<21,41,533)
    V=W[:,cols]*scale;t=s.target[cols]*scale;m=len(W)
    r=linprog(np.r_[np.zeros(m),1],A_ub=np.r_[np.c_[V.T,-np.ones(len(t))],np.c_[-V.T,-np.ones(len(t))]],
        b_ub=np.r_[t,-t],A_eq=np.r_[np.ones(m),0][None,:],b_eq=[1],bounds=(0,None),
        method='highs-ipm',options={'time_limit':120})
    assert r.success,(r.status,r.message)
    weights=r.x[:-1];err=float(max(abs(weights@V-t)))
    assert abs(sum(weights)-1)<1e-8 and min(weights)>=0 and abs(err-r.fun)<1e-7
    return {'objective':float(r.fun),'evaluated_scaled_residual':err,
            'full_unscaled_residual':float(max(abs(weights@W-s.target))),
            'full_scaled_residual':float(max(abs(weights@W-s.target)*np.r_[np.full(21,41),np.full(1440,533)])),
            'weights':[{'column':j,'weight':float(w)} for j,w in enumerate(weights) if w!=0],
            'new_batch_total_weight':float(sum(weights[1609:]))}


def verify(cache=None):
    data=json.loads((ROOT/'evidence/batch_fourth_pricing_n21.json').read_text())
    assert data['run_complete'] and len(data['records'])==6
    f=MomentFunctional(data['direction']);target=f.exact_target()
    assert target==Fraction(data['exact_target']);ctx.prec=192
    out={'base_commit':data['base_commit'],'exact_target':str(target),'precision_bits':192,'interval_witnesses':[]}
    for r in data['records']:
        c=list(map(Fraction,r['couplings']));assert len(c)==42 and c[-1]==0
        assert all(x!=0 for x in c[:-1])
        score=ball_functional(f,c);margin=score-ball(target)
        if r['accepted']:assert margin>1
        identity=sum(f.rational_coefficients.values(),Fraction(0))+sum(f.second_rationals,Fraction(0))
        assert not (score-ball(identity)).contains(0)
        out['interval_witnesses'].append({'start':r['start'],'accepted':r['accepted'],
            'score':str(score),'margin':str(margin),'non_pauli_by_connected_path_test':True})
    out['scope']='Individual connected gapped physical columns only; no uniform design or global optimizer certificate.'
    if cache:
        s,cs,W,direction=prefix(cache);assert direction==data['direction']
        vec=np.r_[f.second,f.coefficients];upper=float(max(W@vec))
        assert abs(upper-data['finite_pool_upper_numerical'])<1e-9
        for r in data['records']:
            col=s.features(list(map(float,r['couplings'])))
            assert fingerprint(col)==r['feature_sha256_le_f64']
            assert abs(vec@col-r['score_numerical'])<1e-9
            if r['accepted']:W=np.r_[W,[col]]
        assert len(W)==data['final_columns']
        y,gap=dual(s,W);p=primal(s,W)
        assert abs(gap-data['final_normalized_gap'])<1e-8 and p['status']==data['final_primal']['status']
        approx=approximate_primal(s,W);assert abs(approx['objective']-gap)<1e-7
        out['finite_numerical_replay']={'columns':len(W),'dual_gap':gap,'primal':p,
            'approximate_mixture':approx,'primal_dual_defect':abs(approx['objective']-gap)}
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache');a=p.parse_args()
    print(json.dumps(verify(a.cache),indent=2))
