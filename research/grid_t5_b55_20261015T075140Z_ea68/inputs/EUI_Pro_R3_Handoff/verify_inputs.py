#!/usr/bin/env python3
"""Verify this packet and its exact read-only scientific input projection."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path

def verify(root: Path, name: str) -> dict:
    manifest=json.loads((root/name).read_text(encoding='utf-8'))
    checks=[]
    for item in manifest['files']:
        rel=Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError(f'Unsafe manifest path: {rel}')
        path=root/rel
        try:
            data=path.read_bytes()
            actual=hashlib.sha256(data).hexdigest()
            ok=len(data)==item['bytes'] and actual==item['sha256']
            checks.append({'path':str(rel),'ok':ok,'actual_sha256':actual})
        except OSError as exc:
            checks.append({'path':str(rel),'ok':False,'error':str(exc)})
    return {'manifest':name,'passed':all(c['ok'] for c in checks),'files_checked':len(checks),'checks':checks}

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet',type=Path,required=True)
    args=ap.parse_args()
    root=args.packet.resolve()
    try:
        reports=[verify(root,'INPUT_MANIFEST.json'),verify(root,'HANDOFF_MANIFEST.json')]
    except (OSError,ValueError,KeyError) as exc:
        print(json.dumps({'passed':False,'error':str(exc)})); return 2
    print(json.dumps({'passed':all(x['passed'] for x in reports),'reports':reports},indent=2))
    return 0 if all(x['passed'] for x in reports) else 1
if __name__=='__main__':
    sys.exit(main())
