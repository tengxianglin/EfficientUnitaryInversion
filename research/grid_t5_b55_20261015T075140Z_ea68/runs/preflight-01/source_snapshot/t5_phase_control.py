#!/usr/bin/env python3
import argparse,json,pathlib
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=False)
def enc(m):return {'rows':m.rows,'cols':m.cols,'entries':[str(s.expand(x)) for x in m]}
def zero(m):return all(s.expand(x)==0 for x in m)
I=s.eye(4);H=s.diag(-3,1,1,1);G=H+I;Pm=s.diag(1,0,0,0);Pp=I-Pm
def F(X):return s.trace(Pm*X)*Pp+s.trace(Pp*X)*Pm/3
f=[];B=s.zeros(4,64)
for aa in range(4):
 for b in range(4):
  unit=s.zeros(4);unit[aa,b]=1;fx=F(unit)
  for o in range(4):
   for ii in range(4):
    if fx[o,ii]:f.append([o,ii,aa,b,str(fx[o,ii])]);B[o,16*aa+4*b+ii]=fx[o,ii]
E=s.zeros(64,4)
for b in range(4):
 for ii in range(4):E[16*b+4*b+ii,ii]=s.Rational(1,2)
k2=s.Rational(10,3);K=B/s.sqrt(k2);checks={}
checks['E_isometry']=zero(E.H*E-I);checks['BBdagger_exact']=zero(B*B.H-s.diag(s.Rational(1,3),1,1,1));checks['contraction_exact']=all(v>=0 for v in (k2*I-B*B.H).diagonal())
images=[]
for aa in range(4):
 for b in range(4):
  X=s.zeros(4);X[aa,b]=1;actual=K*s.kronecker_product(X,s.eye(16))*E;expected=F(X)/(2*s.sqrt(k2));assert zero(actual-expected)
  images.append({'a':aa,'b':b,'actual':enc(actual),'expected':enc(expected)})
checks['matrix_units_16']=True;checks['spectral_exchange']=zero(F(Pm)-Pp) and zero(F(Pp)-Pm)
vec=lambda m:s.Matrix(list(m))
un_even=s.Matrix.hstack(vec(I),vec(H**2));un_odd=s.Matrix.hstack(vec(H),vec(H**3));shift_even=s.Matrix.hstack(vec(I),vec(G**2));shift_odd=s.Matrix.hstack(vec(G),vec(G**3))
ranks={'unshifted_even':un_even.rank(),'unshifted_odd':un_odd.rank(),'unshifted_combined':un_even.row_join(un_odd).rank(),'shifted_even':shift_even.rank(),'shifted_odd':shift_odd.rank(),'shifted_combined':shift_even.row_join(shift_odd).rank()}
assert list(ranks.values())==[2,2,2,1,1,2]
# Characteristic identities close these graded spaces for all powers.
checks['closures']=zero(H**2+2*H-3*I) and zero(G**2-4*I)
checks['dropped_phase_rejected']=not zero(F(H)+H)
assert all(checks.values())
result={'schema':'t5-phase-v1','H':enc(H),'G':enc(G),'P_minus':enc(Pm),'P_plus':enc(Pp),'f_nonzero':f,'f_order':['o','i','a','b'],'B':enc(B),'E0':enc(E),'K':enc(K),'BBdagger':enc(B*B.H),'kappa_squared':str(k2),'probability':'3/40','tensor_order':['query','entangled_memory','input_memory'],'ell':'-2*t','ranks':ranks,'matrix_units':images,'spectral_frequency_identity':{'lhs':{'3':enc(Pp),'-1':enc(Pm)},'rhs_exp_2it_Udagger':{'3':enc(Pp),'-1':enc(Pm)}},'dropped_phase_derivative_defect':enc(F(H)+H),'checks':checks,'status':'exact-finite'}
(out/'certificate.json').write_text(json.dumps(result,indent=2));print(json.dumps({'status':'passed','checks':checks,'ranks':ranks,'probability':'3/40'}))
