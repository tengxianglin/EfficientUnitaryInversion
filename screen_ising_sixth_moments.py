"""Finite degree-six orbit screen; no complete sixth-order optimization."""
import json
from fractions import Fraction
from math import comb
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from verify_full_low_moment_certificate import inputs,ROOT
from ising_fourth_moments import orbit_key,representative


def orbit(I,N=42):
    return sorted({tuple(sorted((s+sign*j)%N for j in I)) for s in range(N) for sign in (-1,1)})


def target(I):return Fraction((-1)**(sum(i%2 for i in I)+3)*comb(21,3),comb(42,6))


def screen():
    cfg,cs,old,new,_,_=inputs();keys=set();rng=np.random.default_rng(202611211836)
    for d in range(1,8):keys.add(orbit_key(tuple(j*d for j in range(6)),42))
    while len(keys)<256:keys.add(orbit_key(tuple(sorted(rng.choice(42,6,replace=False))),42))
    reps=[representative(k) for k in sorted(keys)];orbits=[orbit(I) for I in reps]
    arrays=np.array([I for O in orbits for I in O]);ids=np.repeat(np.arange(len(reps)),[len(O) for O in orbits])
    counts=np.bincount(ids);mold=np.zeros(len(reps));mnew=np.zeros(len(reps))
    for j in sorted(set(old)|set(new)):
        A=np.zeros((42,42));ii=np.arange(42);jj=(ii+1)%42;A[ii,jj]=2*cs[j];A[jj,ii]=-2*cs[j]
        R=expm(A);vals=np.linalg.det(R[arrays[:,:,None],arrays[:,None,:]])
        feat=np.bincount(ids,weights=vals,minlength=len(reps))/counts
        mold+=float(old.get(j,0))*feat;mnew+=float(new.get(j,0))*feat
    records=[]
    for I,a,b in zip(reps,mold,mnew):
        t=target(I);scale=1/abs(float(t));ea=abs(a-float(t))*scale;eb=abs(b-float(t))*scale
        records.append({'indices':list(I),'target':str(t),'old_moment':float(a),'new_moment':float(b),
                        'old_relative_residual':float(ea),'new_relative_residual':float(eb),
                        'change_in_relative_residual':float(eb-ea)})
    return {'base_commit':'9477d4f5d7938e63bc2d242b1417f430f01795dd','rng_seed':202611211836,
            'orbits_screened':len(records),'distinct_six_sets':len(arrays),
            'status':'Finite floating screen of 256 orbits; no full sixth-order maximum or optimality claim.',
            'worst_new_index':int(np.argmax([r['new_relative_residual'] for r in records])),
            'largest_increase_index':int(np.argmax([r['change_in_relative_residual'] for r in records])),
            'records':records}


if __name__=='__main__':print(json.dumps(screen(),indent=2))
