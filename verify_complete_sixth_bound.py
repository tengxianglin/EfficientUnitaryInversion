"""Complete Arb sixth-order bound, split into independent process shards.

Every shard recomputes exact-input rotations and all assigned principal
minors. No numerical vector cache, optimizer or floating error bound enters
this certificate. --limit is a development check and cannot certify full
coverage unless it includes every orbit.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib
import json
from math import comb
import multiprocessing
from pathlib import Path
import sys
from flint import arb,ctx
from audit_complete_sixth_moments import canonical_ensemble,orbit_keys,burnside,ROOT
from ising_fourth_moments import representative
from screen_ising_sixth_moments import orbit,target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

BANK=None
CFG=None
SIGNATURE=None


def key_hash(keys):return hashlib.sha256(json.dumps(keys,separators=(',',':')).encode()).hexdigest()


def initialize(cfg,signature):
    global BANK,CFG,SIGNATURE
    CFG=cfg;SIGNATURE=signature;ctx.prec=cfg['precision_bits']
    for name,sha in cfg['source_sha256'].items():assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    c,_,p=canonical_ensemble();assert len(p)==cfg['expected_seed_orbits']
    BANK=[]
    for j,w in sorted(p.items()):
        row=c[j];assert len(row)==42 and row[-1]==0 and all(row[:-1])
        BANK.append((ball(w),rotation_entries_exact(row)))


def certify_shard(index,start,keys):
    cap=ball(CFG['sixth_error_upper']);count=0;worst=None;where=None
    for offset,key in enumerate(keys):
        I=representative(key);group=orbit(I);value=arb(0)
        for w,E in BANK:
            total=sum((__minor(E,J) for J in group),arb(0))
            value+=w*total/len(group)
        t=target(I);error=(value-ball(t))/ball(abs(t))
        assert -cap<error<cap,(index,start+offset,I,error)
        count+=len(group)
        if worst is None or float(abs(error))>float(abs(worst)):worst=error;where=list(I)
        if (offset+1)%256==0:print(f'Shard {index}: {offset+1}/{len(keys)} orbits certified',file=sys.stderr,flush=True)
    return {'shard':index,'start':start,'stop':start+len(keys),'orbits':len(keys),'six_sets':count,
            'key_sha256':key_hash(keys),'input_sha256':SIGNATURE,'strict_error_upper':CFG['sixth_error_upper'],
            'largest_midpoint_probe':where,'largest_midpoint_residual':str(worst),'passed':True}


def __minor(E,I):
    from flint import arb_mat
    return arb_mat([[E[i][j] for j in I] for i in I]).det()


def verify(workers=8,limit=None):
    raw=(ROOT/'evidence/complete_sixth_certificate_input_n21.json').read_bytes();cfg=json.loads(raw)
    signature=hashlib.sha256(raw).hexdigest();keys=orbit_keys(42)
    assert len(keys)==burnside(42)['orbits']==cfg['expected_sixth_orbits']
    full_count=len(keys)
    if limit is not None:
        assert 0<limit<=full_count;keys=keys[:limit]
    assert 1<=workers<=8
    boundaries=[len(keys)*i//workers for i in range(workers+1)];tasks=[];results=[]
    with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),
                             initializer=initialize,initargs=(cfg,signature)) as pool:
        for i,(a,b) in enumerate(zip(boundaries,boundaries[1:])):
            if a<b:tasks.append(pool.submit(certify_shard,i,a,keys[a:b]))
        for future in as_completed(tasks):
            result=future.result();results.append(result)
            print(f'Finished shard {result["shard"]}: {result["orbits"]} certified orbits',file=sys.stderr,flush=True)
    results.sort(key=lambda r:r['start']);cursor=0
    for r in results:
        assert r['passed'] and r['start']==cursor and r['input_sha256']==signature
        assert r['key_sha256']==key_hash(keys[r['start']:r['stop']]);cursor=r['stop']
    assert cursor==len(keys)
    sets=sum(r['six_sets'] for r in results);complete=len(keys)==full_count
    if complete:assert sets==comb(42,6)==cfg['expected_six_sets']
    return {'base_commit':cfg['base_commit'],'input_sha256':signature,'precision_bits':cfg['precision_bits'],
            'complete':complete,'certified_orbits':len(keys),'expected_orbits':full_count,'certified_six_sets':sets,
            'seed_orbits':cfg['expected_seed_orbits'],'principal_determinants':sets*cfg['expected_seed_orbits'],
            'strict_all_sixth_error_upper':cfg['sixth_error_upper'] if complete else None,'shards':results,
            'scope':'Complete sixth-order upper certificate for one exact physical ensemble only when complete=true. No exact uniformity, higher-order, channel-error or global optimality theorem.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=8);p.add_argument('--limit',type=int);a=p.parse_args()
    print(json.dumps(verify(a.workers,a.limit),indent=2))
