import argparse,json,hashlib
from pathlib import Path
import sympy as S
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();cases=[]
for fp in sorted(a.input.glob('*_*.json')):
 o=json.loads(fp.read_text())
 if o.get('schema')!='tied-span-v1' or o['constraint']=='independent':continue
 rows=[];targets=[];selected=[]
 for sign,kind in [(1,'even'),(-1,'odd')]:
  for raw in o[kind]['echelon_basis']:
   row=[S.Rational(raw.get(str(j),'0')) for j in range(64)];rows.append(row);targets.append([sign*v for v in row])
 V=S.Matrix(rows);Y=S.Matrix(targets);rank=V.rank();aug=V.row_join(Y).rank();consistent=aug==rank
 intersection=o['even']['rank']+o['odd']['rank']-rank
 assert rank==o['full']['rank']
 record={'file':fp.name,'source_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'graded_union_rank':rank,'even_odd_intersection_dimension':intersection,'fixed_complex_linear_dagger_map_exists':consistent,'coefficient_matrix_rows':[[str(v) for v in row] for row in rows],'dagger_target_rows':[[str(v) for v in row] for row in targets],'augmented_rank':aug,'interpretation':'Diagnostic extension on actual span, not a CP supermap certificate or probability optimization.'}
 if consistent:
  record['star_target_rows']=[[str(v*(-1)**sum(((j>>(2*k))&3)==2 for k in range(3))) for j,v in enumerate(row)] for row in targets]
  record['amplitude_condition']='A fixed-amplitude linear map is consistent. Any parameter-dependent alternative must satisfy one-query Fourier intersection and cross-direction phase compatibility; no improved physical comb follows from this diagnostic.'
 cases.append(record)
with a.output.open('x') as f:json.dump({'status':'completed','cases':cases,'limitation':'For B55 tied subfamilies, R1 all-independent star/dagger protocols already imply existence once T2/T3 pass. These diagnostics do not optimize them.'},f,indent=2);f.write('\n')
print(json.dumps({'families':len(cases),'fixed_maps_consistent':sum(x['fixed_complex_linear_dagger_map_exists'] for x in cases)}))
