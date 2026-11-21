"""Interval certificates for frozen pricing columns and symmetry averaging.

Optional cached prefix/final LP checks are numerical and do not prove a
uniform ensemble or a general physical obstruction.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from flint import ctx
from ising_moment_pricing import MomentFunctional
from ising_fourth_moments import FourthMoments,seed_pool
from verify_ising_moment_pricing import ball,ball_functional
from continue_ising_moment_pricing import dual,primal

ROOT=Path(__file__).parent


def reflection_certificate():
    d=json.loads((ROOT/'evidence/reflection_averaging_counterexample_n21.json').read_text())
    ctx.prec=d['precision_bits'];f=MomentFunctional(d['direction'])
    c=list(map(Fraction,d['positive_couplings']));cr=list(map(Fraction,d['reflected_couplings']))
    cb=list(map(Fraction,d['averaged_couplings']))
    assert c[-1]==cr[-1]==cb[-1]==0 and all(x>0 for x in c[:-1])
    assert cr[:-1]==c[:-1][::-1] and cb==[(a+b)/2 for a,b in zip(c,cr)]
    a=ball_functional(f,c);b=ball_functional(f,cr);m=ball_functional(f,cb)
    target=ball(f.exact_target());mixture=(a+b)/2;loss=mixture-m
    assert (a-b).contains(0)
    assert mixture>ball(d['mixture_score_floor']) and m<ball(d['averaged_score_ceiling'])
    assert loss>ball(d['loss_floor']) and mixture>target and m<target
    return {'precision_bits':ctx.prec,'target_score':str(f.exact_target()),
            'positive_seed_score':str(a),'reflected_seed_score':str(b),
            'oracle_mixture_score':str(mixture),'averaged_generator_score':str(m),
            'mixture_minus_generator_average':str(loss),'certified_loss_floor':d['loss_floor'],
            'status':'Certified failure of parameter averaging to preserve reflection-averaged program moments.'}


def verify(cache=None,replay=False):
    data=json.loads((ROOT/'evidence/iterated_fourth_pricing_n21.json').read_text())
    assert data['run_complete'] and len(data['records'])==8
    assert data['final_columns']==data['initial_columns']+len(data['records'])==1609
    ctx.prec=192;out={'base_commit':data['base_commit'],'certified_new_columns':[]}
    for record in data['records']:
        f=MomentFunctional(record['direction']);target=f.exact_target()
        assert target==Fraction(record['exact_target_score'])
        c=list(map(Fraction,record['witness_couplings']));assert len(c)==42 and c[-1]==0
        score=ball_functional(f,c);margin=score-ball(target)
        assert margin>1
        identity=sum(f.rational_coefficients.values(),Fraction(0))+sum(f.second_rationals,Fraction(0))
        connected=all(v!=0 for v in c[:-1])
        if connected:assert not (score-ball(identity)).contains(0)
        out['certified_new_columns'].append({'round':record['round'],
            'fourth_terms':len(f.rational_coefficients),'target_score':str(target),
            'witness_score':str(score),'pricing_margin':str(margin),
            'certified_margin_floor':'1','connected_path':connected,
            'non_pauli_by_connected_path_test':connected})
    reflection=json.loads((ROOT/'evidence/reflection_averaging_counterexample_n21.json').read_text())
    assert reflection['direction']==data['records'][0]['direction']
    assert list(map(Fraction,reflection['positive_couplings']))==[abs(Fraction(c)) for c in data['records'][0]['witness_couplings']]
    out['reflection_averaging_counterexample']=reflection_certificate()
    out['scope']='Certified individual physical columns and a symmetry counterexample; no full uniform design.'
    if cache:
        old=np.load(cache);cs=seed_pool();np.testing.assert_array_equal(old['couplings'],cs)
        W=old['W'];assert hashlib.sha256(W.astype('<f8').tobytes()).hexdigest()=='3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5'
        s=FourthMoments(21)
        first=json.loads((ROOT/'evidence/directed_fourth_pricing_n21.json').read_text())
        W=np.r_[W,[s.features(list(map(float,first['witness_couplings'])))]]
        prefix=[]
        for record in data['records']:
            assert len(W)==record['columns_before']
            f=MomentFunctional(record['direction']);vec=np.r_[f.second,f.coefficients]
            upper=float(max(W@vec));gap=float(f.exact_target())-upper
            assert abs(upper-record['finite_pool_upper_numerical'])<1e-9 and gap>0
            col=s.features(list(map(float,record['witness_couplings'])))
            assert hashlib.sha256(col.astype('<f8').tobytes()).hexdigest()==record['new_column_sha256_le_f64']
            assert abs(vec@col-record['witness_score_numerical'])<1e-9
            prefix.append({'round':record['round'],'rounded_direction_finite_pool_gap':gap})
            W=np.r_[W,[col]]
        out['numerical_prefix_checks']={'columns':len(W),'steps':prefix,
                'status':'Finite floating checks; prefix inequalities are not interval-certified here.'}
        if replay:
            y,gap=dual(s,W);p=primal(s,W)
            assert abs(gap-data['final_normalized_dual_gap'])<1e-8
            assert p['status']==data['final_primal']['status']
            out['numerical_final_replay']={'normalized_dual_gap':gap,'primal':p}
    elif replay:raise ValueError('--replay-final requires the previous feature cache')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache');p.add_argument('--replay-final',action='store_true');a=p.parse_args()
    print(json.dumps(verify(a.cache,a.replay_final),indent=2))
