import sympy as s, itertools, json
from pathlib import Path
r=Path('/mnt/data/eui_r2/cycle/results/T4_final')
M={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Y':s.Matrix([[0,-s.I],[s.I,0]]),'Z':s.diag(1,-1)}
def P(word):
 a=s.ones(1,1)
 for c in word:a=s.kronecker_product(a,M[c])
 return a
for mode in ['row','column']:
 d=json.loads((r/f'B55q0_{mode}.json').read_text()); grid=d['grid'];
 print('\n',mode)
 for rv,sv in itertools.product([1,-1],repeat=2):
  vecs=[]
  for k in range(3):
   v=[0,0,0]
   for j,w in enumerate(sum(grid,[])):
    if d['C'][j][k]:v['XYZ'.index(w[0])]+=(rv if w[1]=='X' else 1)*(sv if w[2]=='Y' else 1)
   vecs.append(v)
  A=s.Matrix.hstack(*[s.Matrix(v) for v in vecs]);print(rv,sv,'A=',str(A.tolist()),'det',A.det(),'Gram',str((A.T*A).tolist()))
 basis=[]
 for row in d['full']['echelon_basis']:
  mat=s.zeros(8)
  for ind,coef in row.items():
   w=''.join('IXYZ'[(int(ind)>>(2*j))&3] for j in [2,1,0]);mat+=s.Rational(coef)*P(w)
  basis.append(mat)
 B=s.Matrix.hstack(*[x.reshape(64,1) for x in basis]);out=[]
 for i,a in enumerate(basis):
  for j,b in enumerate(basis):
   if B.row_join((a*b).reshape(64,1)).rank()>6:out.append((i,j));break
  if out:break
 print('closed algebra?',not out,'first',out)
