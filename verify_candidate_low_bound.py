"""Arb certificate for all 21 second and 1440 fourth rows of LP candidate."""
import hashlib,json
from fractions import Fraction
from flint import arb,arb_mat,ctx
from audit_complete_sixth_moments import canonical_ensemble,ROOT
from ising_fourth_moments import FourthMoments
from verify_ising_moment_pricing import ball

def entries(c):
 A=arb_mat(42,42)
 for j in range(41):A[j,j+1]=2*ball(c[j]);A[j+1,j]=-2*ball(c[j])
 R=A.exp();return [[R[i,j] for j in range(42)] for i in range(42)]
def verify():
 raw=(ROOT/'evidence/candidate_joint_input_n21.json').read_bytes();cfg=json.loads(raw);ctx.prec=128
 allc,_,_=canonical_ensemble();s=FourthMoments(21);mix=[arb(0) for _ in s.target]
 for rec in cfg['exact_probabilities']:
  E=entries(allc[rec['column']]);w=ball(rec['probability'])
  second=[]
  for d in range(1,22):second.append(sum((E[i][i]*E[(i+d)%42][(i+d)%42]-E[i][(i+d)%42]*E[(i+d)%42][i] for i in range(42)),arb(0))/42)
  fourth=[arb(0) for _ in s.keys]
  for I,j in zip(s.indices,s.ids):fourth[int(j)]+=arb_mat([[E[int(i)][int(k)] for k in I] for i in I]).det()
  feats=second+[v/int(n) for v,n in zip(fourth,s.counts)]
  for k,v in enumerate(feats):mix[k]+=w*v
  assert len(feats)==1461
 cap=ball('1/3');worst=arb(0);wi=None
 for k,(a,t) in enumerate(zip(mix,s.rational_target)):
  scale=41 if k<21 else 533;e=(a-ball(t))*scale
  assert abs(e)<cap,(k,e)
  if abs(e)>abs(worst):worst=e;wi=k
 return {'base_commit':cfg['base_commit'],'input_sha256':hashlib.sha256(raw).hexdigest(),'precision_bits':128,'support_size':cfg['support_size'],'certified_second_rows':21,'certified_fourth_rows':1440,'strict_all_low_error_upper':'1/3','largest_midpoint_feature_index':wi,'largest_midpoint_scaled_residual':str(worst),'scope':'All second/fourth rows only; no optimality, higher-order, or operational error theorem.'}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
