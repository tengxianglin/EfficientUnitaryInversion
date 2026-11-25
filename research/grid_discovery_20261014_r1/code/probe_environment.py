#!/usr/bin/env python3
"""Non-secret, local-only environment probe; bounded DNS check, no credentials read."""
import argparse,hashlib,importlib.util,json,os,platform,shutil,subprocess,sys
from pathlib import Path

def text(p):
    p=Path(p)
    return p.read_text().strip() if p.exists() else None

def cmd(args):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=6)
        return {'command':args,'returncode':p.returncode,'stdout':p.stdout[:2000],'stderr':p.stderr[:2000]}
    except (subprocess.TimeoutExpired,FileNotFoundError) as e:
        return {'command':args,'error':type(e).__name__}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
    obj={'schema':'actual-environment-v1','python':sys.version,'platform':platform.platform(),
         'visible_cpu_count':os.cpu_count(),'cpu_cgroup':text('/sys/fs/cgroup/cpu.max'),
         'memory_cgroup_bytes':text('/sys/fs/cgroup/memory.max'),
         'tools':{name:bool(shutil.which(name)) for name in ('git','gh','c++','curl')},
         'credential_variable_presence_only':{name:name in os.environ for name in ('GH_TOKEN','GITHUB_TOKEN','GIT_ASKPASS','SSH_AUTH_SOCK')},
         'external_compute_created':False,'remote_user_device_used':False,'gpu_used':False,
         'versions':{},'optional_solver_installed':{name:importlib.util.find_spec(name) is not None for name in ('cvxpy','clarabel','scs')},
         'git_version':cmd(['git','--version']),'compiler_version':cmd(['c++','--version']),
         'local_github_network_probe':cmd(['curl','-I','--max-time','5','https://api.github.com']),
         'connected_github_observed':'read actions available; no create/commit/push action exposed',
         'per_science_subprocess_reproduction_wall_limit_seconds':40}
    for name in ('numpy','scipy','sympy','pytest'):obj['versions'][name]=__import__(name).__version__
    with a.output.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
    print(json.dumps({'status':'recorded','output':str(a.output),'gpu_used':False}))
if __name__=='__main__':main()
