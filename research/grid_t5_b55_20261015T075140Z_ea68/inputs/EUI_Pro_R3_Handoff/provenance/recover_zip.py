from pathlib import Path
import struct,zlib,hashlib,json
p=Path('/mnt/data/EUI_Grid_Codex_Audit_20261014_R2_20261014T091523Z.zip'); b=p.read_bytes(); root=Path('/mnt/data/eui_r2'); pos=0; records=[]; err=None
while pos < len(b):
 if b[pos:pos+4]!=b'PK\x03\x04':err=f'Not a local header at {pos}'; break
 if pos+30>len(b): err=f'Truncated header at {pos}'; break
 sig,ver,flags,method,time,date,crc,csize,usize,nlen,elen=struct.unpack_from('<IHHHHHIIIHH',b,pos)
 name=b[pos+30:pos+30+nlen].decode('utf-8'); start=pos+30+nlen+elen; end=start+csize
 if flags & 8: err=f'Unsupported descriptor {name}'; break
 if end>len(b):err=f'Truncated member {name}: need bytes through {end}, have {len(b)}'; break
 raw=b[start:end]; data=zlib.decompress(raw,-15) if method==8 else raw
 assert len(data)==usize and zlib.crc32(data)&0xffffffff==crc,name
 out=(root/name).resolve(); assert out.is_relative_to(root.resolve()),name
 if name.endswith('/'):out.mkdir(exist_ok=True,parents=True)
 else:out.parent.mkdir(exist_ok=True,parents=True);out.write_bytes(data)
 records.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc_verified':True}); pos=end
print('RECOVERED',len(records),'ISSUE',err)
Path('/mnt/data/recovery_report.json').write_text(json.dumps({'input_sha256':hashlib.sha256(b).hexdigest(),'input_bytes':len(b),'terminal_error':err,'files':records},indent=2))
print('\n'.join(x['path'] for x in records if any(y in x['path'] for y in ['MANIFEST','verdict','ledger','proofs','NEXT_PRO','T4_final','plan','revision'])))
