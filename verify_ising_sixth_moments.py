"""Arb verification of two fixed degree-six diagnostics, not a full screen."""
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from flint import arb,ctx
from verify_full_low_moment_certificate import inputs,rotation_entries,fourth_sum as principal_sum,ROOT
from verify_ising_moment_pricing import ball
from screen_ising_sixth_moments import orbit,target


def verify():
    cfg=json.loads((ROOT/'evidence/sixth_moment_certificate_input_n21.json').read_text())
    for name,key in [('full_low_moment_certificate_input_n21.json','prior_input_sha256'),('sixth_moment_screen_n21.json','screen_sha256')]:
        assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==cfg[key]
    screen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text())
    assert cfg['outlier_indices']==screen['records'][screen['worst_new_index']]['indices']
    assert cfg['tradeoff_indices']==screen['records'][screen['largest_increase_index']]['indices']
    prior=json.loads((ROOT/'evidence/full_low_moment_certificate_input_n21.json').read_text())
    assert Fraction(cfg['outlier_new_relative_error_lower'])>10*Fraction(prior['new_scaled_residual_upper'])
    _,cs,old,new,_,_=inputs();ctx.prec=cfg['precision_bits']
    probes=[cfg['outlier_indices'],cfg['tradeoff_indices']]
    assert all(len(I)==len(set(I))==6 and I==sorted(I) and all(0<=j<42 for j in I) for I in probes)
    orbits=[orbit(I) for I in probes]
    moments=[[arb(0),arb(0)] for _ in probes]
    for j in sorted(set(old)|set(new)):
        E=rotation_entries(cs[j])
        for k,O in enumerate(orbits):
            value=principal_sum(E,O)/len(O)
            if j in old:moments[k][0]+=ball(old[j])*value
            if j in new:moments[k][1]+=ball(new[j])*value
    out={'base_commit':cfg['base_commit'],'precision_bits':ctx.prec,'certified_orbits':[]}
    errors=[]
    for I,O,(a,b) in zip(probes,orbits,moments):
        t=target(I);assert t==Fraction(5,19721)
        ea=abs(a-ball(t))/ball(abs(t));eb=abs(b-ball(t))/ball(abs(t));errors.append((ea,eb))
        out['certified_orbits'].append({'indices':I,'orbit_size':len(O),'target':str(t),
            'old_moment':str(a),'new_moment':str(b),'old_relative_error':str(ea),'new_relative_error':str(eb)})
    assert errors[0][1]>ball(cfg['outlier_new_relative_error_lower'])
    assert errors[1][0]<ball(cfg['tradeoff_old_relative_error_upper'])
    assert errors[1][1]>ball(cfg['tradeoff_new_relative_error_lower'])
    gain=Fraction(cfg['tradeoff_new_relative_error_lower'])-Fraction(cfg['tradeoff_old_relative_error_upper'])
    assert gain==Fraction(13,200)
    out.update(outlier_new_strict_lower=cfg['outlier_new_relative_error_lower'],
        tradeoff_old_strict_upper=cfg['tradeoff_old_relative_error_upper'],
        tradeoff_new_strict_lower=cfg['tradeoff_new_relative_error_lower'],tradeoff_strict_increase_lower=str(gain))
    checks=[]
    for n in (5,7,21):
        N=2*n;K=tuple(range(5));six=Fraction(comb(n,3),comb(N,6));four=Fraction(comb(n,2),comb(N,4))
        left=sum(((-1)**sum(i%2 for i in (*K,j))*Fraction((-1)**(sum(i%2 for i in (*K,j))+3))*six for j in range(N) if j not in K),Fraction(0))
        right=-sum(((-1)**sum(i%2 for i in J)*Fraction((-1)**(sum(i%2 for i in J)+2))*four for J in combinations(K,4)),Fraction(0))
        assert left==right and (N-5)*six==5*four
        checks.append({'n':n,'Q_signed_target_sum':str(left),'normalized_ratio':str(four/six)})
    out['exact_target_hierarchy_checks']=checks
    out['scope']='Certified two-orbit sixth-order lower bounds/tradeoff; no complete sixth-order maximum, exact low-order counterexample, or global physical no-go.'
    return out


if __name__=='__main__':print(json.dumps(verify(),indent=2))
