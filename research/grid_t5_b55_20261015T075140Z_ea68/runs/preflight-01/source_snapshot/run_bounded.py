#!/usr/bin/env python3
"""Single scientific child, cumulative nonrenewable T5 caps, no hidden retries."""
import argparse, datetime, fcntl, hashlib, json, math, os, pathlib, resource, shlex, signal, subprocess, time, socket
p=argparse.ArgumentParser(); p.add_argument('--group',required=True); p.add_argument('--run-id',required=True); p.add_argument('cmd',nargs=argparse.REMAINDER); a=p.parse_args()
r=pathlib.Path(__file__).resolve().parents[1]; limits={'preflight':(20,40),'producer':(60,150),'phase':(40,100),'independent':(100,240),'packaging':(20,70)}
lock=open(r/'budget.lock','a'); fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
ledger=r/'budget_ledger.jsonl'; prev=[json.loads(x) for x in ledger.read_text().splitlines()] if ledger.exists() else []
group=[x for x in prev if x['group']==a.group]; assert len(group)<2,'at most one diagnosed repair rerun per group'
cpu=limits[a.group][0]-sum(x['cpu_seconds'] for x in group); wall=limits[a.group][1]-sum(x['wall_seconds'] for x in group)
assert cpu>1 and wall>1 and sum(x['cpu_seconds'] for x in prev)<240 and sum(x['wall_seconds'] for x in prev)<600
run=r/'runs'/a.run_id; run.mkdir(); cmd=a.cmd[1:] if a.cmd[0]=='--' else a.cmd
core=min(os.sched_getaffinity(0)); env=os.environ.copy(); env.update({x:'1' for x in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']}); env['PYTHONDONTWRITEBYTECODE']='1'
def digest(q):return hashlib.sha256(q.read_bytes()).hexdigest()
source={str(q.relative_to(r)):digest(q) for q in (r/'code').glob('*.py')}
inputs={str(q.relative_to(r)):digest(q) for q in (r/'inputs').rglob('*') if q.is_file()}
(run/'source_snapshot').mkdir()
for q in (r/'code').glob('*.py'):(run/'source_snapshot'/q.name).write_bytes(q.read_bytes())
(run/'source_hashes.json').write_text(json.dumps(source,indent=2)); (run/'input_hashes.json').write_text(json.dumps(inputs,indent=2))
(run/'command.txt').write_text(shlex.join(cmd)+'\n')
meta={'host':socket.gethostname(),'device':'CPU','python':os.sys.version,'affinity':[core],'threads':{x:env[x] for x in env if x in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},'limits':{'cpu_remaining':cpu,'wall_remaining':wall,'address_space_bytes':2*1024**3,'disk_bytes':96*1024**2}}
(run/'environment.txt').write_text(json.dumps(meta,indent=2))
def setup():
 os.setsid(); os.sched_setaffinity(0,{core}); resource.setrlimit(resource.RLIMIT_CPU,(max(1,math.ceil(cpu)-1),math.ceil(cpu))); resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3)); resource.setrlimit(resource.RLIMIT_FSIZE,(96*1024**2,96*1024**2))
def size():return sum(q.stat().st_size for q in r.rglob('*') if q.is_file())
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic(); state='completed'; reason=''; before=resource.getrusage(resource.RUSAGE_CHILDREN)
with open(run/'stdout.txt','w') as out,open(run/'stderr.txt','w') as err:
 child=subprocess.Popen(cmd,cwd=r,env=env,stdout=out,stderr=err,preexec_fn=setup)
 while child.poll() is None:
  if time.monotonic()-t>=wall or size()>96*1024**2:
   reason='wall_or_disk_limit'; state='timeout'; os.killpg(child.pid,signal.SIGKILL); break
  time.sleep(.05)
 rc=child.wait()
after=resource.getrusage(resource.RUSAGE_CHILDREN); elapsed=time.monotonic()-t; used=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
if rc and state=='completed':state='timeout' if rc in (-9,-24) else 'failed'
record={'run_id':a.run_id,'group':a.group,'state':state,'exit_code':rc,'command':cmd,'host':meta['host'],'device':'CPU','start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cpu_seconds':used,'wall_seconds':elapsed,'max_rss_kib':after.ru_maxrss,'disk_bytes':size(),'budget':meta['limits'],'reason':reason,'artifact_paths':[str(run.relative_to(r))]}
(run/'status.json').write_text(json.dumps(record,indent=2)); (run/'result.json').write_text(json.dumps({'state':state,'exit_code':rc,'reason':reason},indent=2))
with open(ledger,'a') as f:f.write(json.dumps(record)+'\n')
print(json.dumps(record)); raise SystemExit(0 if state=='completed' else 1)
