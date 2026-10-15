import sympy as s,json,itertools,time
from pathlib import Path
start=time.time()
D=Path('/mnt/data/eui_r2/cycle/results/T4_final')
p2={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Y':s.Matrix([[0,-s.I],[s.I,0]]),'Z':s.diag(1,-1)}
def P(w):
 a=s.ones(1,1)
 for c in w:a=s.kronecker_product(a,p2[c])
 return a
I=s.eye(8); R=P('IXI'); S=P('IIY'); Pi0=(I+R+S+R*S)/4; Pc=I-Pi0
W=(P('XII')-P('YIY'))/s.sqrt(2); Q=P('YIX')
grid=json.loads((D/'B55q0_row.json').read_text())['grid']; pp=[P(w) for row in grid for w in row]; H0=sum(pp,s.zeros(8))
out={'pro_exploratory_not_independent_codex_certificate':True,'grid':grid,'W_unitary':s.simplify(W*W)==I,'W_anticommutes_H0':s.simplify(W*H0+H0*W)==s.zeros(8),'star_generator_checks':[Q*x*Q==-x.conjugate() for x in pp], 'charpoly':str(s.factor(H0.charpoly().as_expr())), 'projector_ranks':[Pi0.rank(),Pc.rank()]}
A0=s.Matrix([[1,-1,-1],[1,-1,1],[1,1,-1]])
out['A0_inverse']=[[str(x) for x in A0.inv().row(i)] for i in range(3)]
for mode in ['row','column']:
 d=json.loads((D/f'B55q0_{mode}.json').read_text())
 h=[sum([d['C'][k][j]*pp[k] for k in range(9)],s.zeros(8)) for j in range(3)]
 b=[sum([A0.inv()[j,a]*Pc*h[j] for j in range(3)],s.zeros(8)) for a in range(3)]
 relations=[]
 for a in range(3):
  for c in range(3):
   rhs=(Pc if a==c else s.zeros(8))+sum([s.I*s.LeviCivita(a,c,e)*b[e] for e in range(3)],s.zeros(8))
   relations.append(s.simplify(b[a]*b[c]-rhs)==s.zeros(8))
 basis=[]
 for row in d['full']['echelon_basis']:
  mat=s.zeros(8)
  for ind,coef in row.items():mat+=s.Rational(coef)*P(''.join('IXYZ'[(int(ind)>>(2*j))&3] for j in [2,1,0]))
  basis.append(mat)
 E=s.Matrix.hstack(*[x.reshape(64,1) for x in basis])
 corners=[(Pc+b[2])/2,(b[0]+s.I*b[1])/2,(b[0]-s.I*b[1])/2,(Pc-b[2])/2]
 coords=[]
 for x in corners:
  sol=E.gauss_jordan_solve(x.reshape(64,1))[0]
  coords.append([str(y) for y in sol])
 out[mode]={'pauli_product_checks':relations,'corner_matrix_unit_coordinates':coords, 'corner_checks':[corners[i*2+j]*corners[k*2+l]==(corners[i*2+l] if j==k else s.zeros(8)) for i,j,k,l in itertools.product(range(2),repeat=4)],'Pi0_generators':[s.simplify(Pi0*x-Pi0*(P('XII')+P('YII')+P('ZII')))==s.zeros(8) for x in h], 'W_wrongly_generalized_fails':s.simplify(W*h[0]+h[0]*W)!=s.zeros(8)}
out['elapsed_seconds']=time.time()-start
Path('/mnt/data/pro_b55_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
