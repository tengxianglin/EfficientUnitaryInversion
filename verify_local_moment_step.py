"""Interval proof of frozen local scalar gains; no minimax descent theorem."""
import argparse
import json
import numpy as np
from fractions import Fraction
from flint import ctx
from batch_ising_moment_pricing import ROOT
from ising_moment_pricing import MomentFunctional
from ising_fourth_moments import seed_pool
from verify_ising_moment_pricing import ball_functional


def verify(cache=None):
    data=json.loads((ROOT/'evidence/local_moment_step_n21.json').read_text())
    assert data['run_complete'];ctx.prec=192;f=MomentFunctional(data['direction'])
    parents={};old=seed_pool()
    for r in data['selected']:
        c=[float(x) for x in r['initial_couplings']]
        assert c==old[r['column']].tolist()
        parents[r['column']]=ball_functional(f,[Fraction.from_float(x) for x in c])
    out={'base_commit':data['base_commit'],'precision_bits':192,'parent_interpretation':'Exact binary64 values via Fraction.from_float',
         'candidate_interpretation':'Exact decimal-rational values','certified_local_gains':[]}
    for r in data['candidates']:
        c=list(map(Fraction,r['couplings']));assert len(c)==42 and c[-1]==0 and all(x!=0 for x in c[:-1])
        value=ball_functional(f,c);gain=value-parents[r['parent_column']]
        assert gain>0
        out['certified_local_gains'].append({'parent_column':r['parent_column'],'radius':r['radius'],
            'score':str(value),'gain':str(gain)})
    out['scope']='Certified gains of one frozen scalar functional only; no interval-certified minimax or uniform design result.'
    if cache:
        from local_ising_moment_step import pool
        from batch_ising_moment_pricing import fingerprint
        s,cs,W=pool(cache)
        for r in data['candidates']:
            col=s.features(list(map(float,r['couplings'])))
            assert fingerprint(col)==r['feature_sha256_le_f64']
            assert abs(f.value_gradient(list(map(float,r['couplings'])),False)-r['score_numerical'])<1e-9
            W=np.r_[W,[col]]
        assert len(W)==data['final_columns']==1627
        p=np.zeros(len(W))
        for r in data['final']['weights']:p[r['column']]=r['weight']
        assert min(p)>=0 and abs(sum(p)-1)<1e-10
        scale=np.r_[np.full(21,41),np.full(1440,533)]
        err=float(max(abs(p@W-s.target)*scale))
        assert abs(err-data['final']['objective'])<1e-10
        assert abs(err-data['final']['full_scaled_residual'])<1e-12
        assert abs(sum(p[1615:])-data['final']['local_total_weight'])<1e-12
        out['finite_replay']={'columns':len(W),'evaluated_all_row_residual':err,
                             'local_weight':float(sum(p[1615:]))}
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache');a=p.parse_args()
    print(json.dumps(verify(a.cache),indent=2))
