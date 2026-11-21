"""Frozen all-row replay and exact arithmetic for the analytic remainder bound.

The matrix features/Jacobians below are floating: this is not an interval
certificate of minimax descent or exact moment feasibility.
"""
import argparse
import json
from fractions import Fraction
import numpy as np
from linearized_ising_moment_step import baseline,feature_jacobian,ROOT
from batch_ising_moment_pricing import fingerprint


def verify(cache):
    d=json.loads((ROOT/'evidence/linearized_moment_step_n21.json').read_text());assert d['run_complete']
    s,cs,W,p=baseline(cache);scale=np.r_[np.full(21,41),np.full(1440,533)]
    residual=(p@W-s.target)*scale;g=float(max(abs(residual)))
    assert abs(g-d['baseline_all_row_residual'])<1e-12
    chosen=[r['column'] for r in d['selected']]
    assert chosen==sorted(range(len(W)),key=lambda j:(-p[j],j))[:4]
    B=np.c_[tuple(p[j]*feature_jacobian(s,cs[j])*scale[:,None] for j in chosen)]
    assert fingerprint(B)==d['weighted_scaled_jacobian_sha256_le_f64']
    out={'base_commit':d['base_commit'],'baseline_residual':g,'trials':[],
         'status':'Finite floating replay; rational remainder bounds apply to exact ideal moments, not floating evaluation errors.'}
    for trial in d['trials']:
        updated=residual.copy();changes=[];bound=Fraction(0)
        for r,j in zip(trial['candidates'],chosen):
            assert r['parent_column']==j
            c=list(map(Fraction,r['couplings']));assert len(c)==42 and c[-1]==0 and all(c[:-1])
            delta=[x-Fraction.from_float(float(y)) for x,y in zip(c[:-1],cs[j,:-1])]
            h=max(map(abs,delta));assert h<=Fraction(str(trial['radius']))+Fraction(1,2*10**9)
            bound+=Fraction.from_float(float(p[j]))*h*h*68224
            cf=np.array(list(map(float,c)));col=s.features(cf)
            assert fingerprint(col)==r['feature_sha256_le_f64']
            updated+=p[j]*(col-W[j])*scale;changes.extend(cf[:-1]-cs[j,:-1])
        linear=residual+B@changes;actual=float(max(abs(updated)));model=float(max(abs(updated-linear)))
        assert abs(actual-trial['actual_fixed_weight_residual'])<1e-12
        assert abs(max(abs(linear))-trial['rounded_prediction_residual'])<1e-12
        assert abs(model-trial['max_model_defect'])<1e-12
        assert model<float(bound)+1e-9 and actual<g
        out['trials'].append({'radius':trial['radius'],'actual_residual':actual,'max_model_defect':model,
                            'exact_ideal_taylor_bound':str(bound)})
    for trial in d['trials']:
        for r in trial['candidates']:W=np.r_[W,[s.features(list(map(float,r['couplings'])))]]
    weights=np.zeros(len(W))
    for r in d['final']['weights']:weights[r['column']]=r['weight']
    assert len(W)==d['final_columns']==1639 and min(weights)>=0 and abs(sum(weights)-1)<1e-10
    err=float(max(abs(weights@W-s.target)*scale))
    assert abs(err-d['final']['objective'])<1e-10
    assert abs(err-d['final']['full_scaled_residual'])<1e-12
    assert abs(sum(weights[1627:])-d['final']['new_linearized_weight'])<1e-12
    out['final_replay']={'columns':len(W),'evaluated_all_row_residual':err,
                         'new_weight':float(sum(weights[1627:]))}
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);a=p.parse_args()
    print(json.dumps(verify(a.cache),indent=2))
