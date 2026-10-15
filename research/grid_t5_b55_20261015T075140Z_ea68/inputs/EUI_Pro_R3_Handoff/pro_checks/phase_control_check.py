"""Reproducible source of Pro's small exact phase-control check, not Codex's verifier."""
import json
from pathlib import Path
import sympy as s
pm=s.diag(1,0,0,0); pp=s.eye(4)-pm
F=lambda x:s.trace(pm*x)*pp+s.trace(pp*x)*pm/3
B=s.zeros(4,64)
for a in range(4):
 for r in range(4):
  x=s.zeros(4);x[a,r]=1;fx=F(x)
  for o in range(4):
   for ss in range(4):B[o,(a*4+r)*4+ss]=fx[o,ss]
E=s.zeros(64,4)
for b in range(4):
 for i in range(4):E[(b*4+b)*4+i,i]=s.Rational(1,2)
checks=[]
for a in range(4):
 for b in range(4):
  x=s.zeros(4);x[a,b]=1; checks.append(B*s.kronecker_product(x,s.eye(16))*E==F(x)/2)
res={'status':'pro-local-exact-not-codex-independent','BBdagger':[[str(B.row(i).dot(B.row(j).conjugate())) for j in range(4)] for i in range(4)], 'kappa_squared':str(s.trace(B*B.H)),'p':'3/40','E_isometry':E.H*E==s.eye(4),'matrix_unit_composition_checks':checks,'F_Pminus_equals_Pplus':F(pm)==pp,'F_Pplus_equals_Pminus':F(pp)==pm}
print(json.dumps(res,indent=2))
