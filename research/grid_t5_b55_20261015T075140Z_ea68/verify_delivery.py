import hashlib,json,pathlib,zipfile
r=pathlib.Path(__file__).resolve().parent
m=json.loads((r/'BUILD_MANIFEST.json').read_text())
for e in m['files']:
 p=r/e['path'];assert p.is_file() and p.stat().st_size==e['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'],e['path']
for p in (r/'inputs').glob('*.zip'):
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
print('PASS',len(m['files']),'hashed files and incoming ZIP CRC')
