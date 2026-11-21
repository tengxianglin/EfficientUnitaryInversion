"""Finite floating low/sixth reweighting after appending two physical seeds."""
import argparse
import json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog
from batch_ising_moment_pricing import fingerprint
from ising_fourth_moments import FourthMoments
from verify_full_low_moment_certificate import inputs,ROOT
from screen_ising_sixth_moments import orbit,target


def study(cache,six_cache,replay=False):
    cfg,cs,_,_,_,_=inputs();old=np.load(cache);six=np.load(six_cache)
    assert fingerprint(old['W'])=='3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5'
    assert fingerprint(old['couplings'])==cfg['pool_couplings_sha256_le_f64']
    np.testing.assert_array_equal(six['couplings'],cs)
    assert fingerprint(six['F'])=='9d5c0e6998f8f475762eabb7d0b372dd50d7e3b9add87baa37f705cdf1571b1f'
    s=FourthMoments(21);W=np.r_[old['W'],[s.features(c) for c in cs[1600:]]];F=six['F']
    screen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text());reps=[r['indices'] for r in screen['records']]
    np.testing.assert_array_equal(six['probes'],reps)
    O=[orbit(I) for I in reps];I=np.array([J for group in O for J in group]);ids=np.repeat(np.arange(len(O)),list(map(len,O)));counts=np.bincount(ids)
    data=json.loads((ROOT/'evidence/sixth_pricing_escape_n21.json').read_text());checks=[]
    for r in data['candidates']:
        c=np.array(list(map(float,r['couplings'])));w=s.features(c);A=np.zeros((42,42));i=np.arange(42);j=(i+1)%42
        A[i,j]=2*c;A[j,i]=-2*c;R=expm(A);values=np.linalg.det(R[I[:,:,None],I[:,None,:]])
        f=np.bincount(ids,weights=values,minlength=len(O))/counts
        W=np.r_[W,[w]];F=np.r_[F,[f]];checks.append({'low_features_sha256':fingerprint(w),'sixth_features_sha256':fingerprint(f)})
    V=W*np.r_[np.full(21,41),np.full(1440,533)];t=s.target*np.r_[np.full(21,41),np.full(1440,533)]
    a=abs(float(target(reps[0])));Z=F/a;u=np.array([float(target(J))/a for J in reps]);d=len(t);k=len(u);m=len(W);cap=.218
    if replay:
        saved=json.loads((ROOT/'evidence/sixth_pricing_escape_reweight_n21.json').read_text())
        assert saved['columns']==m and saved['new_column_hashes']==checks and saved['sixth_probes']==k
        p=np.zeros(m)
        for w in saved['weights']:p[w['column']]=w['weight']
        assert min(p)>=0 and abs(sum(p)-1)<1e-8
        low=float(max(abs(p@V-t)));high=float(max(abs(p@Z-u)))
        assert abs(low-saved['evaluated_low_error'])<1e-12 and abs(high-saved['evaluated_sixth_error'])<1e-12
        assert abs(high-saved['numerical_sixth_objective'])<1e-10
        assert abs(sum(p[1639:])-saved['new_weight'])<1e-12
        return {'columns':m,'replayed_low_error':low,'replayed_sixth_error':high,'new_weight':float(sum(p[1639:])),
                'status':'Frozen floating weights/features reproduced; no interval or LP optimality certificate.'}
    r=linprog(np.r_[np.zeros(m),1],A_ub=np.r_[np.c_[V.T,np.zeros(d)],np.c_[-V.T,np.zeros(d)],np.c_[Z.T,-np.ones(k)],np.c_[-Z.T,-np.ones(k)]],
        b_ub=np.r_[t+cap,-t+cap,u,-u],A_eq=np.r_[np.ones(m),0][None,:],b_eq=[1],bounds=(0,None),method='highs-ipm',options={'time_limit':120})
    assert r.success,(r.status,r.message);p=r.x[:-1]
    assert min(p)>=0 and abs(sum(p)-1)<1e-8
    return {'base_commit':data['base_commit'],'columns':m,'low_cap':'109/500','sixth_probes':k,'new_column_hashes':checks,
        'numerical_sixth_objective':float(r.fun),'evaluated_low_error':float(max(abs(p@V-t))),
        'evaluated_sixth_error':float(max(abs(p@Z-u))),'new_weight':float(sum(p[1639:])),
        'weights':[{'column':j,'weight':float(w)} for j,w in enumerate(p) if w!=0],
        'status':'Finite floating reweighting; neither exact feasibility nor an interval-certified optimum.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('--six-cache',required=True);p.add_argument('--replay',action='store_true');a=p.parse_args()
    print(json.dumps(study(a.cache,a.six_cache,a.replay),indent=2))
