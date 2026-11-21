"""Small simultaneous support deformations, followed by all-row correction.

Numerical discovery only; a fixed dual gradient is not a derivative of the
optimized minimax value when the dual optimizer is nonunique.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from batch_ising_moment_pricing import prefix,fingerprint,ROOT
from continue_ising_moment_pricing import freeze_direction
from ising_moment_pricing import MomentFunctional
from verify_batch_moment_pricing import approximate_primal

BASE='47c88cf7ce88a39f209e38d3f2b06c469452f75c'


def pool(cache):
    s,cs,W,_=prefix(cache)
    b=json.loads((ROOT/'evidence/batch_fourth_pricing_n21.json').read_text())
    for r in b['records']:
        c=np.array(list(map(float,r['couplings'])));v=s.features(c)
        assert fingerprint(v)==r['feature_sha256_le_f64']
        if r['accepted']:cs=np.r_[cs,[c]];W=np.r_[W,[v]]
    return s,cs,W


def saddle(s,W):
    scale=np.r_[np.full(21,41),np.full(1440,533)];V=W*scale;t=s.target*scale;m=len(W);d=len(t)
    r=linprog(np.r_[np.zeros(m),1],A_ub=np.r_[np.c_[V.T,-np.ones(d)],np.c_[-V.T,-np.ones(d)]],
        b_ub=np.r_[t,-t],A_eq=np.r_[np.ones(m),0][None,:],b_eq=[1],bounds=(0,None),
        method='highs-ipm',options={'time_limit':120})
    assert r.success,(r.status,r.message)
    y=r.ineqlin.marginals[:d]-r.ineqlin.marginals[d:]
    upper=max(V@y);lower=float(t@y-upper)
    assert sum(abs(y))<=1+1e-8 and abs(lower-r.fun)<1e-7
    assert max(abs(r.x[:-1]@V-t))<r.fun+1e-7
    return r.x[:-1],y*scale,{'objective':float(r.fun),'evaluated_dual_lower':lower,
        'dual_l1_norm':float(sum(abs(y))),'active_residual_rows':int(sum(abs(abs(r.x[:-1]@V-t)-r.fun)<1e-7))}


def run(cache,output):
    s,cs,W=pool(cache);weights,y,base=saddle(s,W)
    f=MomentFunctional(freeze_direction(s,y))
    chosen=sorted(range(len(W)),key=lambda j:(-weights[j],j))[:4]
    records=[];gradients=[]
    for j in chosen:
        value,g=f.value_gradient(cs[j]);errs=[]
        for k in (0,20,40):
            d=np.zeros(42);d[k]=1e-5
            fd=(f.value_gradient(cs[j]+d,False)-f.value_gradient(cs[j]-d,False))/2e-5
            errs.append(abs(fd-g[k]))
        assert max(errs)<1e-5
        gradients.append(weights[j]*g)
        records.append({'column':j,'weight':float(weights[j]),'initial_couplings':list(map(str,cs[j])),
                        'initial_score_numerical':value,'finite_gradient_defect':max(errs)})
    norm=max(np.max(abs(g)) for g in gradients);assert norm>0
    result={'base_commit':BASE,'baseline':base,'direction':freeze_direction(s,y),'selected':records,
            'weighted_gradient_max':float(norm),'radii':[.001,.01,.1],'candidates':[],'run_complete':False}
    for radius in result['radii']:
        for rec,g in zip(records,gradients):
            j=rec['column'];c=np.r_[np.round(cs[j,:-1]+radius*g/norm,6),0]
            col=s.features(c);v=f.value_gradient(c,False)
            result['candidates'].append({'parent_column':j,'radius':radius,'couplings':list(map(str,c)),
                'score_numerical':v,'score_gain_numerical':v-rec['initial_score_numerical'],
                'feature_sha256_le_f64':fingerprint(col)})
            W=np.r_[W,[col]]
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    result['final']=approximate_primal(s,W,full=True)
    result['final']['columns_1609_onward_weight']=result['final'].pop('new_batch_total_weight')
    result['final']['local_total_weight']=sum(r['weight'] for r in result['final']['weights'] if r['column']>=1615)
    result['final_columns']=len(W);result['run_complete']=True
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print('baseline',base,'final objective',result['final']['objective'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();run(a.cache,a.output)
