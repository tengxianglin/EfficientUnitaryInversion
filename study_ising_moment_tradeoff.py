"""Fixed-pool low/sixth-order tradeoff; numerical discovery only."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog
from verify_full_low_moment_certificate import inputs,ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit,target
from batch_ising_moment_pricing import fingerprint


def study(cache,output,six_cache):
    cfg,cs,old,new,_,_=inputs();s=FourthMoments(21)
    prior=np.load(cache);assert fingerprint(prior['couplings'])==cfg['pool_couplings_sha256_le_f64']
    assert fingerprint(prior['W'])=='3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5'
    W=np.r_[prior['W'],[s.features(c) for c in cs[1600:]]]
    screen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text());reps=[r['indices'] for r in screen['records']]
    O=[orbit(I) for I in reps];I=np.array([J for group in O for J in group]);ids=np.repeat(np.arange(len(O)),list(map(len,O)));counts=np.bincount(ids)
    if Path(six_cache).exists():
        saved=np.load(six_cache);np.testing.assert_array_equal(saved['couplings'],cs)
        np.testing.assert_array_equal(saved['probes'],reps);F=saved['F']
    else:
        rows=[];ii=np.arange(42);jj=(ii+1)%42
        for j,c in enumerate(cs):
            A=np.zeros((42,42));A[ii,jj]=2*c;A[jj,ii]=-2*c;R=expm(A)
            values=np.linalg.det(R[I[:,:,None],I[:,None,:]])
            rows.append(np.bincount(ids,weights=values,minlength=len(O))/counts)
            if (j+1)%200==0:print('sixth columns',j+1,flush=True)
        F=np.array(rows);np.savez(six_cache,couplings=cs,probes=reps,F=F)
    assert F.shape==(1639,256)
    assert fingerprint(F)=='9d5c0e6998f8f475762eabb7d0b372dd50d7e3b9add87baa37f705cdf1571b1f'
    scale24=np.r_[np.full(21,41),np.full(1440,533)];a=abs(float(target(reps[0])))
    V=W*scale24;t=s.target*scale24;Z=F/a;u=np.array([float(target(J))/a for J in reps]);m=len(W);d=len(t);k=len(u);cap=.218
    A=np.r_[np.c_[V.T,np.zeros(d)],np.c_[-V.T,np.zeros(d)],np.c_[Z.T,-np.ones(k)],np.c_[-Z.T,-np.ones(k)]]
    r=linprog(np.r_[np.zeros(m),1],A_ub=A,b_ub=np.r_[t+cap,-t+cap,u,-u],A_eq=np.r_[np.ones(m),0][None,:],b_eq=[1],bounds=(0,None),method='highs-ipm',options={'time_limit':120})
    assert r.success,(r.status,r.message)
    mu=r.ineqlin.marginals;y=mu[:d]-mu[d:2*d];z=mu[2*d:2*d+k]-mu[2*d+k:]
    # Rational freezing applies to scaled coordinates.
    y=np.round(y,6);z=np.round(z,6);scores=V@y+Z@z;upper=float(max(scores));lt=float(t@y+u@z)
    p=r.x[:-1]
    assert min(p)>=0 and abs(sum(p)-1)<1e-8
    assert max(abs(p@V-t))<cap+1e-7 and max(abs(p@Z-u))<r.fun+1e-7
    data={'base_commit':'0e03837f17d3196856f28e4fc679fe34dbc03485','columns':m,'sixth_probes':k,'low_cap':'109/500',
          'numerical_optimum_sixth_error':float(r.fun),'evaluated_low_error':float(max(abs(p@V-t))),
          'evaluated_sixth_error':float(max(abs(p@Z-u))),
          'weights':[{'column':j,'weight':float(w)} for j,w in enumerate(p) if w!=0],
          'feature_sha256_le_f64':fingerprint(F),'direction_24':list(map(str,y)),'direction_6':list(map(str,z)),
          'rounded_target_score':lt,'rounded_pool_upper':upper,
          'rounded_tradeoff_lower_numerical':(lt-upper-cap*sum(abs(y)))/sum(abs(z)),
          'status':'Finite floating pool tradeoff, not an interval or global physical certificate.'}
    Path(output).write_text(json.dumps(data,indent=2)+'\n');print({q:v for q,v in data.items() if q not in ['weights','direction_24','direction_6']},flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('--output',required=True);p.add_argument('--six-cache',required=True);a=p.parse_args();study(a.cache,a.output,a.six_cache)
