#!/usr/bin/env python3
"""Serial CPU experiment runner. Fresh runs, cumulative CPU budgets, no credentials."""
import argparse,datetime,fcntl,json,os,platform,resource,signal,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAPS={'R1':120,'T1':480,'T2':300,'T3':420,'T4':480}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 p=argparse.ArgumentParser();p.add_argument('--group',choices=CAPS,required=True);p.add_argument('--id',required=True);p.add_argument('--ram-mib',type=int,default=1024);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args();cmd=a.command
 if cmd and cmd[0]=='--':cmd=cmd[1:]
 with (ROOT/'runs/.serial.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  statuses=[json.loads(x.read_text()) for x in (ROOT/'runs').glob('*/status.json')]
  used=sum(x.get('cpu_seconds',0) for x in statuses if x['group']==a.group);total=sum(x.get('cpu_seconds',0) for x in statuses)
  remain=min(CAPS[a.group]-used,1800-total)
  if remain<=1:raise SystemExit('CPU budget exhausted')
  out=ROOT/'runs'/a.id;out.mkdir()
  affinity=sorted(os.sched_getaffinity(0));core=affinity[-1]
  env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
  def limits():
   os.setsid();os.sched_setaffinity(0,{core});resource.setrlimit(resource.RLIMIT_CPU,(int(remain),int(remain)+1));resource.setrlimit(resource.RLIMIT_AS,(a.ram_mib*1024**2,)*2)
  (out/'command.txt').write_text(json.dumps(cmd)+'\n');(out/'environment.txt').write_text(json.dumps({'host':'quair07-local','device':'CPU','python':platform.python_version(),'platform':platform.platform(),'affinity':[core],'thread_limits':1,'GPU':0,'RAM_MiB':a.ram_mib,'group_cap_cpu_seconds':CAPS[a.group],'remaining_cpu_seconds':remain},indent=2)+'\n')
  before=resource.getrusage(resource.RUSAGE_CHILDREN);start=time.monotonic();started=now()
  state='failed';rc=None
  with (out/'stdout.txt').open('x') as so,(out/'stderr.txt').open('x') as se:
   proc=subprocess.Popen(cmd,stdout=so,stderr=se,env=env,preexec_fn=limits)
   try:rc=proc.wait(timeout=min(remain*2+30,1000));state='completed' if rc==0 else ('timeout' if rc in (-24,-9) else 'failed')
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait();state='timeout'
  after=resource.getrusage(resource.RUSAGE_CHILDREN)
  status={'run_id':a.id,'group':a.group,'host':'quair07-local','device':'CPU','start_utc':started,'end_utc':now(),'state':state,'exit_code':rc,'command':cmd,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'wall_seconds':time.monotonic()-start,'budget':{'group_cpu_seconds':CAPS[a.group],'remaining_before':remain,'ram_mib':a.ram_mib,'concurrency':1,'gpu':0},'artifact_paths':[str((out/x).relative_to(ROOT)) for x in ('stdout.txt','stderr.txt','command.txt','environment.txt')]}
  (out/'status.json').write_text(json.dumps(status,indent=2)+'\n');(out/'result.json').write_text(json.dumps({'state':state,'exit_code':rc,'science_artifacts':'See command output and results/; completion of a process alone is not a claim verdict.'},indent=2)+'\n');print(json.dumps(status))
  if state!='completed':raise SystemExit(1)
if __name__=='__main__':main()
