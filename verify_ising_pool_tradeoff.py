"""Interval certificate for a fixed physical-pool low/sixth-moment tradeoff.

This proves only a finite-family convex-hull bound, never a global physical
no-go. The LP output is used to select a frozen rational functional only.
"""
import hashlib
import json
from fractions import Fraction
from flint import arb,arb_mat,ctx
from verify_full_low_moment_certificate import inputs,rotation_entries,ROOT
from verify_ising_moment_pricing import ball
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit,target
import sys


def verify():
    cfg=json.loads((ROOT/'evidence/fixed_pool_tradeoff_certificate_input_n21.json').read_text())
    for name,sha in cfg['source_sha256'].items():assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    data=json.loads((ROOT/'evidence/fixed_pool_tradeoff_n21.json').read_text())
    screen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text())
    _,cs,_,_,_,_=inputs();s=FourthMoments(21);s.exact_target_check();ctx.prec=cfg['precision_bits']
    y=list(map(Fraction,data['direction_24']));z=list(map(Fraction,data['direction_6']))
    assert len(y)==1461 and len(z)==256 and len(cs)==data['columns']==1639
    assert z[0]==-1 and all(v==0 for v in z[1:])
    assert screen['records'][0]['indices']==[0,1,2,3,4,5]
    alpha=sum(map(abs,y),Fraction(0));beta=sum(map(abs,z),Fraction(0));assert beta==1
    target_value=sum((v*(41 if k<21 else 533)*s.rational_target[k] for k,v in enumerate(y)),Fraction(0))
    target_value+=sum((v*Fraction(19721,5)*target(r['indices']) for v,r in zip(z,screen['records'])),Fraction(0))
    cap=Fraction(data['low_cap']);upper=Fraction(cfg['pool_upper']);bound=(target_value-upper-cap*alpha)/beta
    assert bound>Fraction(cfg['sixth_error_lower'])
    terms=[]
    for d,v in enumerate(y[:21],1):
        if not v:continue
        O=sorted({tuple(sorted((i,(i+d)%42))) for i in range(42)})
        terms.extend((I,ball(v*41/len(O))) for I in O)
    for k,v in enumerate(y[21:]):
        if not v:continue
        O=s.indices[s.ids==k]
        terms.extend((tuple(map(int,I)),ball(v*533/len(O))) for I in O)
    for v,r in zip(z,screen['records']):
        if not v:continue
        O=orbit(r['indices']);terms.extend((I,ball(v*Fraction(19721,5)/len(O))) for I in O)
    best=None;where=None;threshold=ball(upper)
    for j,c in enumerate(cs):
        E=rotation_entries(c)
        score=sum((w*arb_mat([[E[i][k] for k in I] for i in I]).det() for I,w in terms),arb(0))
        assert score<threshold,(j,score,upper)
        if best is None or float(score)>float(best):best=score;where=j
        if (j+1)%100==0:print(f'Certified {j+1}/{len(cs)} finite-pool scores',file=sys.stderr,flush=True)
    return {'base_commit':cfg['base_commit'],'precision_bits':ctx.prec,'certified_columns':len(cs),
        'nonzero_low_coefficients':sum(v!=0 for v in y),'nonzero_sixth_coefficients':sum(v!=0 for v in z),
        'principal_determinants_per_column':len(terms),'target_functional':str(target_value),
        'low_coefficient_l1':str(alpha),'sixth_coefficient_l1':str(beta),'low_cap':str(cap),
        'strict_pool_upper':str(upper),'exact_conditional_lower':str(bound),
        'sixth_strict_error_lower':cfg['sixth_error_lower'],'largest_midpoint_column':where,
        'largest_midpoint_score':str(best),
        'scope':'If a mixture of this pool and its signed dihedral/gauge images has G24<=cap, its tested sixth error exceeds the stated bound. Other physical seeds are not excluded.'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
