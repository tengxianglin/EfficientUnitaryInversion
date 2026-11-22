"""128-bit Arb check of selected eighth rows for the LP candidate."""
import hashlib,json
from fractions import Fraction
from flint import arb,arb_mat,ctx
from audit_complete_sixth_moments import canonical_ensemble,ROOT
from screen_ising_sixth_moments import orbit
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
ROWS=[[0,1,2,3,4,5,6,7],[0,5,10,15,20,25,30,35],[0,1,8,9,16,17,24,25],[0,4,12,16,20,28,32,36],[0,2,6,14,22,30,34,40],[0,3,9,14,21,27,33,39]]
def minor(E,I):return arb_mat([[E[i][j] for j in I] for i in I]).det()
def verify():
 raw=(ROOT/'evidence/candidate_joint_input_n21.json').read_bytes();cfg=json.loads(raw);assert hashlib.sha256((ROOT/'evidence/joint_low_six_eighth_lp_n21.json').read_bytes()).hexdigest()==cfg['source_sha256'];ctx.prec=128
 allc,_,_=canonical_ensemble();BANK=[(ball(x['probability']),rotation_entries_exact(allc[x['column']])) for x in cfg['exact_probabilities']];out=[]
 for I in ROWS:
  O=orbit(I);q=arb(0)
  for w,E in BANK:q+=w*sum((minor(E,J) for J in O),arb(0))/len(O)
  target=ball(Fraction(1,19721));e=(q-target)/target;out.append({'indices':I,'orbit_size':len(O),'moment':str(q),'relative_error':str(e),'abs_upper':str(abs(e).upper())})
  assert abs(e)<ball('1/3')
 return {'base_commit':cfg['base_commit'],'input_sha256':hashlib.sha256(raw).hexdigest(),'precision_bits':128,'strict_selected_eighth_upper':'1/3','rows':out,'scope':'Six selected eighth rows only; no complete degree-eight certificate.'}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
