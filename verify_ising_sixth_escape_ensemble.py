"""Complete low-order plus fixed-sixth-set certificate of an exact ensemble."""
import hashlib
import json
import sys
from fractions import Fraction
from flint import arb,ctx
from verify_full_low_moment_certificate import inputs,all_features,ROOT
from verify_ising_sixth_escape import rotation_entries_exact
from verify_full_low_moment_certificate import fourth_sum as principal_sum
from verify_ising_moment_pricing import ball
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit,target


def verify():
    cfg=json.loads((ROOT/'evidence/sixth_escape_ensemble_certificate_input_n21.json').read_text());ctx.prec=cfg['precision_bits']
    for name,sha in cfg['source_sha256'].items():assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    _,cs,_,reference,_,_=inputs();esc=json.loads((ROOT/'evidence/sixth_pricing_escape_n21.json').read_text())
    study=json.loads((ROOT/'evidence/sixth_pricing_escape_reweight_n21.json').read_text())
    screen=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text())
    couplings=[[Fraction.from_float(float(v)) for v in c] for c in cs]
    couplings += [list(map(Fraction,r['couplings'])) for r in esc['candidates']];assert len(couplings)==1641
    raw={r['column']:Fraction.from_float(float(r['weight'])) for r in study['weights']}
    assert len(raw)==len(study['weights']) and all(v>0 for v in raw.values())
    total=sum(raw.values(),Fraction(0));mix=Fraction(cfg['reference_mix_weight']);assert 0<mix<1
    weights={j:(1-mix)*raw.get(j,0)/total+mix*reference.get(j,0) for j in set(raw)|set(reference)}
    assert all(w>0 for w in weights.values()) and sum(weights.values(),Fraction(0))==1
    s=FourthMoments(21);s.exact_target_check();low=[arb(0) for _ in s.target]
    O=[orbit(r['indices']) for r in screen['records']];six=[arb(0) for _ in O]
    for step,(j,p) in enumerate(sorted(weights.items()),1):
        c=couplings[j];assert len(c)==42 and c[-1]==0 and all(c[:-1])
        E=rotation_entries_exact(c);w=ball(p);f=all_features(s,E)
        for k,v in enumerate(f):low[k]+=w*v
        for k,group in enumerate(O):six[k]+=w*principal_sum(E,group)/len(group)
        print(f'Certified ensemble column {step}/{len(weights)} (source {j})',file=sys.stderr,flush=True)
    lowcap=ball(cfg['low_error_upper']);highcap=ball(cfg['tested_sixth_error_upper'])
    lowworst=None;li=None;highworst=None;hi=None
    for k,(v,t) in enumerate(zip(low,s.rational_target)):
        e=(v-ball(t))*(41 if k<21 else 533);assert -lowcap<e<lowcap,(k,e)
        if lowworst is None or float(abs(e))>float(abs(lowworst)):lowworst=e;li=k
    for k,(v,r) in enumerate(zip(six,screen['records'])):
        t=target(r['indices']);e=(v-ball(t))/ball(abs(t));assert -highcap<e<highcap,(k,e)
        if highworst is None or float(abs(e))>float(abs(highworst)):highworst=e;hi=k
    prior=json.loads((ROOT/'evidence/fixed_pool_tradeoff_certificate_n21.json').read_text())
    gap=Fraction(prior['exact_conditional_lower'])-Fraction(cfg['tested_sixth_error_upper']);assert gap>Fraction(38,100)
    return {'base_commit':cfg['base_commit'],'precision_bits':ctx.prec,'support_seed_orbits':len(weights),
            'physical_dihedral_atoms_at_most':84*len(weights),'exact_probability_sum':'1',
            'raw_lp_weight_sum':str(total),'reference_mix_weight':str(mix),
            'exact_probabilities':[{'column':j,'probability':str(p)} for j,p in sorted(weights.items())],
            'certified_low_rows':1461,'certified_sixth_orbits':len(O),'distinct_six_sets':sum(map(len,O)),
            'strict_low_error_upper':cfg['low_error_upper'],'strict_tested_sixth_error_upper':cfg['tested_sixth_error_upper'],
            'low_largest_midpoint_index':li,'low_largest_midpoint_residual':str(lowworst),
            'sixth_largest_midpoint_index':hi,'sixth_largest_midpoint_residual':str(highworst),
            'gap_below_old_family_conditional_lower':str(gap),
            'scope':'Certified complete second/fourth plus 256 fixed sixth orbits; no full sixth-order, full program uniformity, channel-error or global optimality theorem.'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
