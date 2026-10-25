import importlib.util,json
from pathlib import Path
import sympy as S
p=Path(__file__).resolve().parent/'verify_t4.py'
s=importlib.util.spec_from_file_location('independent',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
root=p.parents[1];o=json.loads((root/'results/T4/B4q0_column.json').read_text());beta=(1,2,3);H=sum((sum(o['C'][j][s]*beta[s] for s in range(3))*m.mat(w) for j,w in enumerate(sum(o['grid'],[]))),S.zeros(8));power=H**3;expected=S.zeros(8)
for row in o['coefficient_rows']:
 if row['degree']!=3:continue
 value=1
 for b,e in zip(beta,row['exponents']):value*=b**e
 for k,x in row['coefficients'].items():expected+=value*x*m.PA[int(k)]
result={'structural_equality':power==expected,'expanded_difference':str((power-expected).applyfunc(S.expand)),'expanded_zero':(power-expected).applyfunc(S.expand)==S.zeros(8),'beta':beta,'degree':3}
(root/'results/T4_equality_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
