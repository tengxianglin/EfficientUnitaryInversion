import hashlib,json,pathlib,platform,os,resource,runpy,sys
import sympy
r=pathlib.Path(__file__).resolve().parents[1]; packet=r/'inputs'/'EUI_Pro_R3_Handoff'
for name in ['INPUT_MANIFEST.json','HANDOFF_MANIFEST.json']:
 manifest=json.loads((packet/name).read_text())
 for e in manifest['files']:
  q=packet/e['path']; assert q.is_file() and q.stat().st_size==e['bytes'] and hashlib.sha256(q.read_bytes()).hexdigest()==e['sha256'],str(q)
 print(name,'verified',len(manifest['files']))
sys.argv=['verify_inputs.py','--packet',str(packet)];runpy.run_path(str(packet/'verify_inputs.py'),run_name='__main__')
print(json.dumps({'sympy':sympy.__version__,'python':platform.python_version(),'host':platform.node(),'affinity':list(os.sched_getaffinity(0)),'address_space':resource.getrlimit(resource.RLIMIT_AS)}))
