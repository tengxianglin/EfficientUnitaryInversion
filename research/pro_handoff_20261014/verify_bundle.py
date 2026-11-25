"""Verify this immutable handoff inventory; does not run research experiments."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
expected = set()
for item in manifest['files']:
    rel = PurePosixPath(item['path'])
    if rel.is_absolute() or '..' in rel.parts or str(rel) in expected:
        raise SystemExit('Unsafe or duplicate manifest path')
    expected.add(str(rel))
    path = root / str(rel)
    if not path.is_file() or path.is_symlink():
        raise SystemExit('Missing or unsafe file: ' + str(rel))
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != item['sha256'] or path.stat().st_size != item['size_bytes']:
        raise SystemExit('Inventory mismatch: ' + str(rel))
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual != expected | {'BUILD_MANIFEST.json'}:
    raise SystemExit('Unexpected or unlisted files')
print('PASS: complete file inventory and SHA-256 hashes; scientific claims not re-proved')
