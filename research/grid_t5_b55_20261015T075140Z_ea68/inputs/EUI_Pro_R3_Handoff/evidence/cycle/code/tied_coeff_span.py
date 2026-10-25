#!/usr/bin/env python3
"""Exact tied-parameter power coefficients, rational spans and phase-aware spectral kills.
No R1 mathematical helper is imported. Pauli coordinates are base-4 I,X,Y,Z,
left-to-right tensor order. All coefficient arithmetic uses Python integers.
"""
import argparse,hashlib,itertools,json,time
from fractions import Fraction
from pathlib import Path
import sympy as sp
LET='IXYZ'
# Single-letter products: index, power of i. XY=iZ, YZ=iX, ZX=iY.
TAB=[[(j,0) for j in range(4)],[(1,0),(0,0),(3,1),(2,3)],[(2,0),(3,3),(0,0),(1,1)],[(3,0),(2,1),(1,3),(0,0)]]
def tag(s):
 v=0
 for q in s:v=4*v+LET.index(q)
 return v
def word(v,n=3):return ''.join(LET[(v>>(2*j))&3] for j in reversed(range(n)))
def prod(a,b):
 out=0;e=0
 for j in range(3):
  t,p=TAB[(a>>(2*j))&3][(b>>(2*j))&3];out|=t<<(2*j);e+=p
 return out,e%4
MUL=[[prod(a,b) for b in range(64)] for a in range(64)]
def add_power(poly,terms,m):
 out={}
 for ex,vec in poly.items():
  for s,p in terms:
   ee=list(ex);ee[s]+=1;ee=tuple(ee);row=out.setdefault(ee,{})
   for t,val in vec.items():
    q,e=MUL[t][p];r,im=row.get(q,(0,0))
    if e==0:r+=val
    elif e==2:r-=val
    elif e==1:im+=val
    else:im-=val
    row[q]=(r,im)
 result={}
 for ex,row in out.items():
  assert all(im==0 for r,im in row.values()),'Hermitian coefficient has imaginary part'
  rr={t:r for t,(r,im) in row.items() if r}
  if rr:result[ex]=rr
 return result
class ExactBasis:
 def __init__(self):self.rows={};self.sources=[]
 def reduce(self,row):
  v={k:Fraction(x) for k,x in row.items() if x};co={}
  for p,b in sorted(self.rows.items()):
   a=v.get(p,0)
   if a:
    co[p]=a
    for j,x in b.items():
     v[j]=v.get(j,0)-a*x
     if not v[j]:v.pop(j)
  return v,co
 def add(self,row,source):
  v,_=self.reduce(row)
  if not v:return False
  p=min(v);a=v[p];self.rows[p]={j:x/a for j,x in v.items()};self.sources.append(source);return True
 def dump(self):return {'rank':len(self.rows),'pivot_coordinates':sorted(self.rows),'echelon_basis':[{str(j):str(v) for j,v in row.items()} for p,row in sorted(self.rows.items())],'independent_coefficient_rows':self.sources}
def sparse(row):return {str(k):v for k,v in sorted(row.items())}
def pauli(s):
 mats=[sp.eye(2),sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)];r=sp.ones(1,1)
 for a in s:r=sp.kronecker_product(r,mats[LET.index(a)])
 return r
X=sp.Symbol('x')
def spectrum(H):
 f=sp.Poly(H.charpoly(X).as_expr(),X).sqf_part().monic();D=f.degree();gamma=-2*f.nth(D-1)/D
 delta=sp.Poly(f.as_expr().subs(X,gamma-X)-(-1)**D*f.as_expr(),X)
 return {'characteristic_polynomial':str(H.charpoly(X).as_expr()),'squarefree_monic_coefficients':[str(x) for x in f.all_coeffs()],'distinct_eigenvalue_count':D,'candidate_gamma':str(gamma),'reflection_identity':delta.is_zero,'reflection_defect_coefficients':[str(x) for x in delta.all_coeffs()]}
def controls():
 A=sp.kronecker_product(pauli('ZII')[:2,:2],sp.eye(1)) if False else pauli('ZII');B=pauli('IZI')
 uniform=spectrum(A+B+A*B);ind=spectrum(A+2*B+4*A*B)
 assert uniform['reflection_identity'] and uniform['candidate_gamma']=='2'
 assert not ind['reflection_identity']
 return {'uniform_commuting_triple':uniform,'independent_1_2_4':ind,'status':'passed','scope':'Exact spectra ignoring multiplicities; necessary amplitude condition only.'}
def run_family(name,grid,constraint,out):
 tags=[tag(p) for p in sum(grid,[])];m=9 if constraint=='independent' else 1 if constraint=='uniform' else 3
 C=[[int((constraint=='independent' and j==s) or constraint=='uniform' or (constraint=='row' and j//3==s) or (constraint=='column' and j%3==s)) for s in range(m)] for j in range(9)]
 terms=[(s,tags[j]) for j in range(9) for s in range(m) if C[j][s]]
 maxk=3 if constraint=='independent' else 15
 full=ExactBasis();even=ExactBasis();odd=ExactBasis();polys=[];allrows=[];support=set();first=None
 poly={(0,)*m:{0:1}};counts=[]
 for k in range(maxk+1):
  if k:poly=add_power(poly,terms,m)
  rows=[]
  for ex,vec in sorted(poly.items()):
   src={'degree':k,'exponents':list(ex)};idx=len(allrows);allrows.append({'degree':k,'exponents':list(ex),'coefficients':sparse(vec)})
   if k<=7:
    full.add(vec,idx);support.update(vec)
   (even if k%2==0 else odd).add(vec,idx)
  counts.append({'degree':k,'nonzero_monomials':len(poly),'full_rank_through_degree7':len(full.rows),'even_rank':len(even.rows),'odd_rank':len(odd.rows),'union_support_through_degree7':len(support)})
  if first is None and k<=7 and len(support)>len(full.rows):first={'degree':k,'support_size':len(support),'span_rank':len(full.rows)}
 sign={p:(-1)**word(p).count('Y') for p in range(64)};trans=[];invariant=True
 for p,row in sorted(full.rows.items()):
  image={j:sign[j]*v for j,v in row.items()};rem,co=full.reduce(image);invariant &= not rem
  trans.append({'input_pivot':p,'ambient_image':{str(j):str(x) for j,x in image.items()},'image_coordinates_in_echelon_basis':{str(j):str(x) for j,x in co.items()},'outside_span_remainder':{str(j):str(x) for j,x in rem.items()}})
 rays=[]
 if constraint!='independent':
  mats=[pauli(p) for p in sum(grid,[])];Hs=[sum((mats[j]*C[j][s] for j in range(9)),sp.zeros(8)) for s in range(m)]
  for beta in itertools.product((-1,0,1),repeat=m):
   if not any(beta):continue
   H=sum((v*h for v,h in zip(beta,Hs)),sp.zeros(8));r=spectrum(H);r['beta']=list(beta);rays.append(r)
 firstkill=next((r for r in rays if not r['reflection_identity']),None)
 obj={'schema':'tied-span-v1','grid_name':name,'constraint':constraint,'grid':grid,'C':C,'coordinates':'64 Hermitian Pauli IXYZ base4; gaussian integer coefficients imaginary part proved zero by exact recurrence','full_degree_bound':3 if constraint=='independent' else 7,'graded_degree_bound':None if constraint=='independent' else {'even':14,'odd':15},'independent_graded_status':'not_claimed' if constraint=='independent' else 'not_applicable','full':full.dump(),'even':even.dump(),'odd':odd.dump(),'union_support_size':len(support),'support_equals_span_dimension':len(support)==len(full.rows),'first_support_span_gap':first,'coverage':counts,'coefficient_rows':allrows,'transpose':{'span_invariant':invariant,'images':trans},'rays':rays,'first_phase_aware_kill':firstkill,'claim_status':'exact-finite','amplitude_condition_unclosed':('Dagger/star killed by exact nonsymmetric admissible tied ray and the all-real-ray/shared-I amplitude lemma. Nine independent coefficients are not needed for this implication.' if firstkill else 'Finite ray passes alone establish no instrument. For these B55 subfamilies, the enclosing independent family already supplies star p1 and dagger p1/4 after T2/T3 verification. Improved probabilities or alternative phase-dependent instruments require global cross-direction amplitude compatibility and CP comb certificates.'),'limitations':'No support-union rank substitution. Degree7 CH applies full span only; parity uses CH of H² through14/15. Independent graded closure not inferred.'}
 target=out/(name+'_'+constraint+'.json');target.write_text(json.dumps(obj,indent=2)+'\n')
 return {'grid':name,'constraint':constraint,'full_rank':len(full.rows),'even_rank':None if constraint=='independent' else len(even.rows),'odd_rank':None if constraint=='independent' else len(odd.rows),'support_size':len(support),'transpose_invariant':invariant,'ray_count':len(rays),'spectral_kills':sum(not r['reflection_identity'] for r in rays),'first_kill_beta':None if firstkill is None else firstkill['beta'],'artifact':target.name,'state':'completed','sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--grids',nargs='+');ap.add_argument('--constraints',nargs='+',default=['independent','row','column','uniform']);ap.add_argument('--span-max-degree',type=int,default=7);ap.add_argument('--graded-max-degree',type=int,default=15);ap.add_argument('--rays',default='ternary');a=ap.parse_args();assert a.span_max_degree==7 and a.graded_max_degree==15 and a.rays=='ternary'
 assert a.grids is None or a.grids==['matched_q4','B4q0','B55q0'], 'Only the four registered grid inputs are authorized'
 a.output.mkdir(parents=True,exist_ok=False);start=time.process_time();control=controls();(a.output/'controls.json').write_text(json.dumps(control,indent=2)+'\n')
 cal=json.loads((a.input/'exact/calibration.json').read_text())['examples'];anti=json.loads((a.input/'validation/all_anti_grids.json').read_text());grids={x['name']:x['grid'] for x in cal if x['name'] in ('same_W_q4_partial','same_W_q4_saturated')}
 grids['B4q0']=[['XII','IXI','XXI'],['IIX','ZII','ZIX'],['XIX','ZXI','YXX']];grids['B55q0']=next(x['grid'] for x in anti if x['B']==55 and x['q']==0)
 rows=[]
 for name,grid in grids.items():
  for co in a.constraints:
   row=run_family(name,grid,co,a.output);rows.append(row)
   summary={'state':'running','families':rows,'expected_families':len(grids)*len(a.constraints),'cpu_seconds':time.process_time()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_hashes':{str(p.relative_to(a.input)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [a.input/'exact/calibration.json',a.input/'validation/all_anti_grids.json']}}
   (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(row),flush=True)
 summary['state']='completed';(a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()
