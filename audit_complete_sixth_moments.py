"""Exhaustive floating degree-six audit; selected rows need separate proof."""
import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from math import comb,gcd
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from ising_fourth_moments import orbit_key,representative
from screen_ising_sixth_moments import orbit,target
from verify_full_low_moment_certificate import inputs,ROOT
from batch_ising_moment_pricing import fingerprint


def canonical_ensemble():
    cfg=json.loads((ROOT/'evidence/sixth_escape_ensemble_certificate_input_n21.json').read_text())
    for name,sha in cfg['source_sha256'].items():assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    _,cs,_,reference,_,_=inputs();esc=json.loads((ROOT/'evidence/sixth_pricing_escape_n21.json').read_text())
    c=[[Fraction.from_float(float(v)) for v in row] for row in cs]+[list(map(Fraction,r['couplings'])) for r in esc['candidates']]
    study=json.loads((ROOT/'evidence/sixth_pricing_escape_reweight_n21.json').read_text())
    raw={r['column']:Fraction.from_float(float(r['weight'])) for r in study['weights']};total=sum(raw.values(),Fraction(0));delta=Fraction(cfg['reference_mix_weight'])
    p={j:(1-delta)*raw.get(j,0)/total+delta*reference.get(j,0) for j in set(raw)|set(reference)}
    proof=json.loads((ROOT/'evidence/sixth_escape_ensemble_certificate_n21.json').read_text())
    assert p=={r['column']:Fraction(r['probability']) for r in proof['exact_probabilities']}
    assert sum(p.values(),Fraction(0))==1 and all(v>0 for v in p.values())
    return c,reference,p


def orbit_keys(N):return sorted({orbit_key((0,*J),N) for J in combinations(range(1,N),5)})


def burnside(N):
    assert N>=6 and N%2==0
    rotations=sum(comb(gcd(N,s),6//(N//gcd(N,s))) for s in range(N) if 6%(N//gcd(N,s))==0)
    vertex=sum(comb(2,a)*comb((N-2)//2,(6-a)//2) for a in (0,2) if (6-a)//2<=(N-2)//2)
    edge=comb(N//2,3)
    reflections=(N//2)*(vertex+edge)
    assert (rotations+reflections)%(2*N)==0
    return {'rotations_fixed_sum':rotations,'reflections_fixed_sum':reflections,'orbits':(rotations+reflections)//(2*N)}


def orbit_size_from_gaps(key,N=42):
    stabilizer=sum(key==g[j:]+g[:j] for g in (key,key[::-1]) for j in range(6))
    assert (2*N)%stabilizer==0
    return 2*N//stabilizer


def audit(output,vector_cache=None,replay_cache=None):
    c,reference,p=canonical_ensemble();keys=orbit_keys(42);counts_cert=burnside(42)
    assert len(keys)==counts_cert['orbits']==63133
    small=[]
    for N in (10,14):
        ks=orbit_keys(N);count=len(ks);assert count==burnside(N)['orbits']
        assert all(orbit_size_from_gaps(k,N)==len(orbit(representative(k),N)) for k in ks)
        assert sum(orbit_size_from_gaps(k,N) for k in ks)==comb(N,6)
        small.append({'N':N,'sixth_orbits':count})
    oldscreen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text())
    oldkeys={orbit_key(r['indices'],42) for r in oldscreen['records']}
    if replay_cache:
        saved=np.load(replay_cache)
        np.testing.assert_array_equal(saved['keys'],keys)
        old=saved['reference'];new=saved['repair']
        assert old.shape==new.shape==(len(keys),) and np.isfinite(old).all() and np.isfinite(new).all()
        set_count=sum(orbit_size_from_gaps(k) for k in keys)
    else:
        matrices=[];indices=sorted(p)
        for j in indices:
            A=np.zeros((42,42));ii=np.arange(42);jj=(ii+1)%42;v=np.array(list(map(float,c[j])));A[ii,jj]=2*v;A[jj,ii]=-2*v
            matrices.append(expm(A))
        old=np.zeros(len(keys));new=np.zeros(len(keys));set_count=0
        for start in range(0,len(keys),256):
            batch=keys[start:start+256];O=[orbit(representative(k)) for k in batch]
            I=np.array([J for group in O for J in group]);ids=np.repeat(np.arange(len(batch)),list(map(len,O)));counts=np.bincount(ids);set_count+=len(I)
            for j,R in zip(indices,matrices):
                vals=np.linalg.det(R[I[:,:,None],I[:,None,:]])
                f=np.bincount(ids,weights=vals,minlength=len(batch))/counts
                old[start:start+len(batch)]+=float(reference.get(j,0))*f
                new[start:start+len(batch)]+=float(p[j])*f
            if start%4096==0:print('orbits',min(start+256,len(keys)),'/',len(keys),flush=True)
    assert set_count==comb(42,6)==5245786
    reps=[representative(k) for k in keys];t=np.array([float(target(I)) for I in reps]);a=5/19721
    sizes=np.array([orbit_size_from_gaps(k) for k in keys]);assert sum(sizes)==set_count
    parity=np.array([(-1)**sum(i%2 for i in I) for I in reps])
    check_old=float((sizes*parity)@old);check_new=float((sizes*parity)@new)
    assert abs(check_old+comb(21,3))<1e-7 and abs(check_new+comb(21,3))<1e-7
    eo=abs(old-t)/a;en=abs(new-t)/a;outside=np.array([k not in oldkeys for k in keys]);idx=np.flatnonzero(outside)
    selected={'reference_global_max':int(np.argmax(eo)),'repair_global_max':int(np.argmax(en)),
              'repair_outside_max':int(idx[np.argmax(en[idx])]),'outside_largest_increase':int(idx[np.argmax((en-eo)[idx])])}
    records={label:{'orbit_index':j,'indices':list(reps[j]),'target':str(target(reps[j])),
                   'reference_moment':float(old[j]),'repair_moment':float(new[j]),
                   'reference_relative_error':float(eo[j]),'repair_relative_error':float(en[j]),
                   'in_original_256':keys[j] in oldkeys} for label,j in selected.items()}
    result={'base_commit':'301e20b14aed72f362764624447482e29e1ccaa4','reference_seed_orbits':len(reference),
        'repair_seed_orbits':len(p),'sixth_orbits':len(keys),'six_sets':set_count,'burnside':counts_cert,'small_orbit_checks':small,
        'reference_vector_sha256_le_f64':fingerprint(old),'repair_vector_sha256_le_f64':fingerprint(new),
        'outside_original_256_over_155':int(sum(en[outside]>1.55)),'selected':records,
        'sixth_elementary_symmetric_target':-comb(21,3),'reference_signed_minor_sum':check_old,'repair_signed_minor_sum':check_new,
        'status':'Exhaustive floating sixth-order audit; no interval global maximum or complete sixth upper certificate.'}
    if vector_cache:np.savez(vector_cache,reference=old,repair=new,keys=np.array(keys))
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(records,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--vector-cache');p.add_argument('--replay-vector-cache');a=p.parse_args();audit(a.output,a.vector_cache,a.replay_vector_cache)
