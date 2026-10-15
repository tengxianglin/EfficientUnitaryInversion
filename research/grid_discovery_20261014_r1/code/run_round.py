#!/usr/bin/env python3
"""Bounded reproduction. Requires an already extracted, immutable handoff.
Never installs packages, accesses a network, or overwrites an existing run.
"""
from __future__ import annotations
import argparse,hashlib,json,os,platform,resource,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    source=args.input.resolve();out=args.output.resolve()
    if source in out.parents or source==out:raise SystemExit('Output must not be inside frozen input')
    if out.exists():raise SystemExit('Output must be fresh; refusing overwrite')
    if not (source/'verify_bundle.py').is_file():raise SystemExit('Missing frozen verifier')
    if hashlib.sha256((source/'NEXT_PRO_PROMPT.md').read_bytes()).hexdigest()!='90794f527ec34639451c51036653f3123c8f29981cf39fad2790a7b5abb4d3b0':
        raise SystemExit('Wrong input prompt hash')
    compiler=shutil.which('c++')
    if not compiler:raise SystemExit('C++ compiler unavailable; do not silently replace enumeration')
    for name in ('numpy','scipy','sympy'):
        __import__(name)
    out.mkdir(parents=True);(out/'logs').mkdir();records=[]
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    def run(name,cmd,stdout_path=None,timeout=40):
        before=resource.getrusage(resource.RUSAGE_CHILDREN);start=time.monotonic()
        fp=stdout_path or out/'logs'/f'{name}.stdout.txt'
        with fp.open('x') as stdout,(out/'logs'/f'{name}.stderr.txt').open('x') as stderr:
            try:
                p=subprocess.run(list(map(str,cmd)),stdout=stdout,stderr=stderr,env=env,timeout=timeout,check=False)
                status='passed' if p.returncode==0 else 'failed';code=p.returncode
            except subprocess.TimeoutExpired:
                status='timeout';code=None
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        records.append({'id':name,'command':list(map(str,cmd)),'status':status,'returncode':code,
            'wall_seconds':time.monotonic()-start,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
            'timeout_seconds':timeout,'stdout':str(fp),'stderr':str(out/'logs'/f'{name}.stderr.txt')})
        (out/'run_ledger.json').write_text(json.dumps(records,indent=2)+'\n')
        if status!='passed':raise SystemExit(f'{name}: {status}; stopped, raw logs retained')
    run('verify_frozen',[sys.executable,source/'verify_bundle.py'])
    run('compile',[compiler,'-O2','-std=c++17',ROOT/'code/physical_census.cpp','-o',out/'physical_census'])
    for n in (2,3):run(f'physical_n{n}',[out/'physical_census',n],out/f'physical_n{n}.json')
    run('exact',[sys.executable,ROOT/'code/grid_check.py','--input',source,'--output',out/'exact',
        '--physical2',out/'physical_n2.json','--physical3',out/'physical_n3.json'])
    run('validation',[sys.executable,ROOT/'code/validate_predictions.py','--exact',out/'exact','--frozen',source,
        '--output',out/'validation','--seed','20261014'])
    run('comb',[sys.executable,ROOT/'code/comb_certificate.py','--output',out/'comb_certificates.json'])
    versions={'python':sys.version,'platform':platform.platform()}
    for name in ('numpy','scipy','sympy'):versions[name]=__import__(name).__version__
    (out/'software.json').write_text(json.dumps(versions,indent=2)+'\n')
    print(json.dumps({'status':'passed','output':str(out),'timed_child_cpu_seconds':sum(r['cpu_seconds'] for r in records)}))
if __name__=='__main__':main()
