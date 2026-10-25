import ast,hashlib,json,pathlib
r=pathlib.Path(__file__).resolve().parents[1]
assert json.loads((r/'results/T5_independent/verification.json').read_text())['status']=='PASS'
for source,run in [('t5_b55_producer.py','producer-02-artifact-repair'),('t5_b55_independent.py','independent-01'),('t5_phase_control.py','phase-01')]:
 p=r/'code'/source; snap=r/'runs'/run/'source_snapshot'/source
 assert p.read_bytes()==snap.read_bytes(),source
 tree=ast.parse(p.read_text())
 imports=[x.module for x in ast.walk(tree) if isinstance(x,ast.ImportFrom)]
 assert not any(x and ('t5_' in x or 't4' in x or 'pro_checks' in x) for x in imports)
for name in ['T5_candidate_complete','T5_phase']:
 x=json.loads((r/'results'/name/'certificate.json').read_text());assert x
print('PASS final executed sources, independent import boundaries, accepted artifacts')
