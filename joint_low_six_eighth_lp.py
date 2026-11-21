"""Finite numerical low/sixth/eighth minimax LP on the frozen 83-column pool.

This is a design diagnostic only.  It does not certify the full sixth orbit
set or interval arithmetic, and it does not optimize over new physical
columns.
"""
import hashlib,json
from fractions import Fraction
from math import comb
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog
from audit_complete_sixth_moments import canonical_ensemble,ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit

EIGHTH_ROWS=[
 [0,1,2,3,4,5,6,7], [0,5,10,15,20,25,30,35],
 [0,1,8,9,16,17,24,25], [0,4,12,16,20,28,32,36],
 [0,2,6,14,22,30,34,40], [0,3,9,14,21,27,33,39]]

def orbit_minor(R,I):
    O=orbit(I)
    return float(np.mean([np.linalg.det(R[np.ix_(J,J)]) for J in O]))

def matrix(c):
    A=np.zeros((42,42));
    for i,x in enumerate(map(float,c[:-1])):
        A[i,i+1]=2*x;A[i+1,i]=-2*x
    return expm(A)

def run():
    allc,_,prob=canonical_ensemble(); keys=sorted(prob); cs=[allc[j] for j in keys]
    s=FourthMoments(21); low=np.array([s.features(np.array(list(map(float,c)))) for c in cs])
    low_target=s.target.copy(); low_scale=np.r_[np.full(21,1/41),np.full(len(s.keys),comb(21,2)/comb(42,4))]
    screen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text())['records']
    sixth_rows=[r['indices'] for r in screen]; six_target=np.array([float(Fraction(r['target'])) for r in screen])
    six=np.empty((len(cs),len(sixth_rows))); eighth=np.empty((len(cs),len(EIGHTH_ROWS)))
    for j,c in enumerate(cs):
        R=matrix(c)
        six[j]=[orbit_minor(R,I) for I in sixth_rows]
        eighth[j]=[orbit_minor(R,I) for I in EIGHTH_ROWS]
    eighth_target=np.full(len(EIGHTH_ROWS),1/19721)
    A=np.vstack([low.T/low_scale[:,None],six.T/(5/19721),eighth.T/(1/19721)])
    y=np.r_[low_target/low_scale,six_target/(5/19721),eighth_target/(1/19721)]
    m=A.shape[0];n=A.shape[1]
    aub=np.vstack([np.c_[A,-np.ones(m)],np.c_[-A,-np.ones(m)]])
    bub=np.r_[y,-y]
    result=linprog(np.r_[np.zeros(n),1],A_ub=aub,b_ub=bub,
                   A_eq=np.r_[np.ones(n),0][None,:],b_eq=[1],
                   bounds=[(0,None)]*n+[(0,None)],method='highs')
    assert result.success
    w=result.x[:-1];base=np.array([float(prob[j]) for j in keys])
    rb=np.abs(A@base-y);ro=np.abs(A@w-y)
    split=[len(low_target),len(six_target),len(eighth_target)]
    cuts=np.cumsum([0]+split)
    return {'base_commit':'9f26680c96c269eb5ad0e84fd8ee5efacff132ee',
      'input_sha256':hashlib.sha256((ROOT/'evidence/complete_sixth_certificate_input_n21.json').read_bytes()).hexdigest(),
      'sixth_screen_sha256':hashlib.sha256((ROOT/'evidence/sixth_moment_screen_n21.json').read_bytes()).hexdigest(),
      'columns':n,'rows':m,'row_blocks':{'low':split[0],'sixth_screen':split[1],'selected_eighth':split[2]},
      'solver':'scipy.optimize.linprog(method=highs), binary64 finite design only',
      'baseline_max':float(rb.max()),'lp_max':float(ro.max()),
      'baseline_low_max':float(rb[cuts[0]:cuts[1]].max()),'lp_low_max':float(ro[cuts[0]:cuts[1]].max()),
      'baseline_sixth_screen_max':float(rb[cuts[1]:cuts[2]].max()),'lp_sixth_screen_max':float(ro[cuts[1]:cuts[2]].max()),
      'baseline_selected_eighth_max':float(rb[cuts[2]:cuts[3]].max()),'lp_selected_eighth_max':float(ro[cuts[2]:cuts[3]].max()),
      'lp_objective':float(result.fun),
      'lp_positive_weights':[[int(j),float(x)] for j,x in zip(keys,w) if x>1e-8],
      'selected_eighth_rows':EIGHTH_ROWS,
      'scope':'Finite LP over frozen 83-column pool and 256 sixth rows; no complete sixth/eighth certification, exact feasibility, or physical global optimum.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
