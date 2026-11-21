"""Independent Arb inequalities for frozen rows selected by an exhaustive audit."""
import hashlib
import json
from fractions import Fraction
from flint import arb,ctx
from audit_complete_sixth_moments import canonical_ensemble,ROOT
from verify_ising_sixth_escape import rotation_entries_exact
from verify_full_low_moment_certificate import fourth_sum as principal_sum
from verify_ising_moment_pricing import ball
from screen_ising_sixth_moments import orbit,target
from ising_fourth_moments import orbit_key


def verify():
    cfg=json.loads((ROOT/'evidence/complete_sixth_outlier_input_n21.json').read_text())
    for name,sha in cfg['source_sha256'].items():assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    c,reference,p=canonical_ensemble();assert set(reference)<=set(p);ctx.prec=cfg['precision_bits']
    prior=json.loads((ROOT/'evidence/sixth_moment_screen_n21.json').read_text())
    oldkeys={orbit_key(r['indices'],42) for r in prior['records']}
    audit=json.loads((ROOT/'evidence/complete_sixth_audit_n21.json').read_text())
    probes=cfg['cases']
    assert all(r['indices']==audit['selected'][r['selection']]['indices'] for r in probes)
    O=[orbit(r['indices']) for r in probes];moments=[[arb(0),arb(0)] for _ in probes]
    for j,w in sorted(p.items()):
        E=rotation_entries_exact(c[j])
        for k,group in enumerate(O):
            v=principal_sum(E,group)/len(group);moments[k][1]+=ball(w)*v
            if j in reference:moments[k][0]+=ball(reference[j])*v
    out={'base_commit':cfg['base_commit'],'precision_bits':ctx.prec,'certified_probes':[]}
    for case,group,(a,b) in zip(probes,O,moments):
        I=case['indices'];assert len(I)==len(set(I))==6 and I==sorted(I) and all(0<=v<42 for v in I)
        t=target(I);ea=abs(a-ball(t))/ball(abs(t));eb=abs(b-ball(t))/ball(abs(t))
        assert eb>ball(case['repair_error_lower'])
        outside=orbit_key(I,42) not in oldkeys
        if case.get('outside_original_256'):assert outside
        item={'indices':I,'orbit_size':len(group),'outside_original_256':outside,'target':str(t),
              'reference_moment':str(a),'repair_moment':str(b),'reference_relative_error':str(ea),
              'repair_relative_error':str(eb),'repair_strict_lower':case['repair_error_lower']}
        if 'repair_error_upper' in case:
            assert eb<ball(case['repair_error_upper']);item['repair_strict_upper']=case['repair_error_upper']
        if case.get('repair_moment_positive'):
            assert b>0 and t<0;item['opposite_target_sign']=True
        if 'reference_error_upper' in case:
            assert ea<ball(case['reference_error_upper'])
            gap=Fraction(case['repair_error_lower'])-Fraction(case['reference_error_upper']);assert gap>0
            item.update(reference_strict_upper=case['reference_error_upper'],strict_error_increase_lower=str(gap))
        out['certified_probes'].append(item)
    out['scope']='Only the frozen row inequalities are interval-certified. Exhaustive floating maxima are not exact/global upper certificates; no uniformity or physical no-go theorem follows.'
    return out


if __name__=='__main__':print(json.dumps(verify(),indent=2))
