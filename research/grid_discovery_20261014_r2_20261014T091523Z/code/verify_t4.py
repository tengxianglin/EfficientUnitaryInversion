#!/usr/bin/env python3
"""Independent dense symbolic verification of saved exact power vectors and ranks."""
import argparse,json,hashlib
from pathlib import Path
import sympy as S
from fractions import Fraction
M={'I':S.eye(2),'X':S.Matrix([[0,1],[1,0]]),'Y':S.Matrix([[0,-S.I],[S.I,0]]),'Z':S.diag(1,-1)}
def mat(word):
 r=S.ones(1)
 for a in word:r=S.kronecker_product(r,M[a])
 return r
PA=[]
for t in range(64):PA.append(mat(''.join('IXYZ'[(t>>(2*j))&3] for j in (2,1,0))))
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();results=[]
 for fp in sorted(a.input.glob('*_*.json')):
  o=json.loads(fp.read_text())
  if o.get('schema')!='tied-span-v1':continue
  rows=o['coefficient_rows'];coords=sorted({int(k) for row in rows for k in row['coefficients']})
  def rank(sub):return S.polys.matrices.DomainMatrix.from_Matrix(S.Matrix([[row['coefficients'].get(str(k),0) for k in coords] for row in sub])).convert_to(S.QQ).rank()
  full=[r for r in rows if r['degree']<=7];rr=rank(full);assert rr==o['full']['rank']
  ranks={'full':rr}
  if o['constraint']!='independent':
   for kind,parity in [('even',0),('odd',1)]:
    ranks[kind]=rank([r for r in rows if r['degree']%2==parity]);assert ranks[kind]==o[kind]['rank']
  m=len(o['C'][0]);betas=[tuple((j%3)+1 for j in range(m)),tuple((-1)**j for j in range(m))]
  dense_checks=0
  for beta in betas:
   H=S.zeros(8)
   for j,w in enumerate(sum(o['grid'],[])):H+=sum(o['C'][j][s]*beta[s] for s in range(m))*mat(w)
   power=S.eye(8)
   for degree in range(max(r['degree'] for r in rows)+1):
    if degree:power=(power*H).applyfunc(S.expand)
    coeff={k:0 for k in coords}
    for row in rows:
     if row['degree']!=degree:continue
     v=1
     for b,e in zip(beta,row['exponents']):v*=b**e
     for k,x in row['coefficients'].items():coeff[int(k)]+=v*x
    expected=sum((v*PA[k] for k,v in coeff.items() if v),S.zeros(8))
    assert (power-expected).applyfunc(S.expand)==S.zeros(8),(fp.name,beta,degree)
    dense_checks+=1
  transrows=[[row['coefficients'].get(str(k),0)*(-1)**''.join('IXYZ'[(k>>(2*j))&3] for j in (2,1,0)).count('Y') for k in coords] for row in full]
  orig=[[row['coefficients'].get(str(k),0) for k in coords] for row in full]
  invariant=S.polys.matrices.DomainMatrix.from_Matrix(S.Matrix(orig+transrows)).convert_to(S.QQ).rank()==rr
  assert invariant==o['transpose']['span_invariant']
  results.append({'file':fp.name,'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'independent_ranks':ranks,'dense_integer_power_checks':dense_checks,'transpose_invariance_matched':True,'status':'passed'})
 assert len(results)==16
 expected={'same_W_q4_partial':10,'same_W_q4_saturated':16,'B4q0':16,'B55q0':16}
 for name,rank0 in expected.items():assert json.loads((a.input/(name+'_independent.json')).read_text())['full']['rank']==rank0
 out={'status':'passed','families':results,'checks':'Dense SymPy exact matrix powers at two fixed integer beta vectors per family, all retained degrees; independent DomainMatrix rational ranks; transpose augmented rank. Sampling power equality corroborates recurrence; exact full coefficient generation and CH bound are separate arguments.'}
 with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps({'status':'passed','families':len(results),'dense_power_checks':sum(x['dense_integer_power_checks'] for x in results)}))
if __name__=='__main__':main()
