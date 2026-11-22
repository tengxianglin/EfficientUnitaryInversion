import json,hashlib
from fractions import Fraction
from pathlib import Path
from audit_complete_sixth_moments import canonical_ensemble,ROOT
src=ROOT/'evidence/joint_low_six_eighth_lp_n21.json';d=json.loads(src.read_text());allc,_,_=canonical_ensemble()
raw=[(int(i),Fraction.from_float(float(x))) for i,x in d['lp_positive_weights']]
total=sum((x for _,x in raw),Fraction(0));p={i:x/total for i,x in raw}
out={'base_commit':'3ef509d07fa2189956e08aae669f61428202c0ed','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'precision_bits':64,'strict_upper':'31/20','columns':sorted(p),'exact_probabilities':[{'column':i,'probability':str(p[i])} for i in sorted(p)],'exact_probability_sum':str(sum(p.values(),Fraction(0))),'support_size':len(p)}
Path('evidence/candidate_joint_input_n21.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['support_size'],out['exact_probability_sum'])
