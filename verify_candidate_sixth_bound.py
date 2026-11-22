"""Complete Arb sixth-order separation audit for the finite LP candidate."""
import argparse,hashlib,json,multiprocessing,sys
from concurrent.futures import ProcessPoolExecutor,as_completed
from math import comb
from pathlib import Path
from flint import arb,arb_mat,ctx
from audit_complete_sixth_moments import canonical_ensemble,orbit_keys,burnside,ROOT
from ising_fourth_moments import representative
from screen_ising_sixth_moments import orbit,target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
BANK=[];CFG=None;SIG=None

def kh(keys): return hashlib.sha256(json.dumps(keys,separators=(',',':')).encode()).hexdigest()
def initialize(cfg,sig):
 global BANK,CFG,SIG;CFG=cfg;SIG=sig;ctx.prec=cfg['precision_bits']
 src=ROOT/'evidence/joint_low_six_eighth_lp_n21.json';assert hashlib.sha256(src.read_bytes()).hexdigest()==cfg['source_sha256']
 allc,_,_=canonical_ensemble();BANK=[(ball(r['probability']),rotation_entries_exact(allc[int(r['column'])])) for r in cfg['exact_probabilities']]
def minor(E,I): return arb_mat([[E[i][j] for j in I] for i in I]).det()
def shard(i,start,keys):
 cap=ball(CFG['strict_upper']);count=0;worst=None;where=None
 for off,key in enumerate(keys):
  I=representative(key);O=orbit(I);q=arb(0)
  for w,E in BANK:q+=w*sum((minor(E,J) for J in O),arb(0))/len(O)
  e=(q-ball(target(I)))/ball(abs(target(I)));a=abs(e)
  if not (a<cap):return {'passed':False,'shard':i,'start':start,'failure_orbit':start+off,'indices':list(I),'error':str(e),'error_abs_lower':str(a.lower())}
  count+=len(O)
  if worst is None or float(a)>float(abs(worst)):worst=e;where=list(I)
 return {'passed':True,'shard':i,'start':start,'stop':start+len(keys),'orbits':len(keys),'six_sets':count,'key_sha256':kh(keys),'input_sha256':SIG,'largest_midpoint_probe':where,'largest_midpoint_residual':str(worst),'strict_error_upper':CFG['strict_upper']}
def verify(workers=8,limit=None):
 raw=(ROOT/'evidence/candidate_joint_input_n21.json').read_bytes();cfg=json.loads(raw);sig=hashlib.sha256(raw).hexdigest();keys=orbit_keys(42);full=len(keys)
 assert len(keys)==burnside(42)['orbits']==63133 and cfg['support_size']==29 and cfg['exact_probability_sum']=='1'
 if limit:keys=keys[:limit]
 b=[len(keys)*i//workers for i in range(workers+1)];res=[]
 with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),initializer=initialize,initargs=(cfg,sig)) as pool:
  fut=[pool.submit(shard,i,a,keys[a:z]) for i,(a,z) in enumerate(zip(b,b[1:])) if a<z]
  for f in as_completed(fut):res.append(f.result())
 res.sort(key=lambda x:x['start'])
 if any(not x['passed'] for x in res):return {'base_commit':cfg['base_commit'],'input_sha256':sig,'complete':False,'failed':res}
 cursor=0;sets=0
 for x in res:assert x['start']==cursor and x['input_sha256']==sig and x['key_sha256']==kh(keys[x['start']:x['stop']]);cursor=x['stop'];sets+=x['six_sets']
 complete=cursor==full
 return {'base_commit':cfg['base_commit'],'input_sha256':sig,'precision_bits':cfg['precision_bits'],'complete':complete,'certified_orbits':len(keys),'certified_six_sets':sets,'strict_error_upper':cfg['strict_upper'] if complete else None,'shards':res}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=8);p.add_argument('--limit',type=int);a=p.parse_args();print(json.dumps(verify(a.workers,a.limit),indent=2))
