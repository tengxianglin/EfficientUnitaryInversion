"""Higher-precision cross-check of the complete certificate's diagnostic rows."""
import hashlib
import json
from fractions import Fraction
from flint import arb,ctx
from audit_complete_sixth_moments import canonical_ensemble,ROOT
from screen_ising_sixth_moments import orbit,target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_full_low_moment_certificate import fourth_sum as principal_sum
from verify_ising_moment_pricing import ball


def verify():
    raw=(ROOT/'evidence/complete_sixth_certificate_input_n21.json').read_bytes();cfg=json.loads(raw)
    data=json.loads((ROOT/'evidence/complete_sixth_bound_n21.json').read_text())
    assert data['complete'] and data['certified_orbits']==63133 and data['certified_six_sets']==5245786
    assert data['input_sha256']==hashlib.sha256(raw).hexdigest()
    for name,sha in cfg['source_sha256'].items():assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    ctx.prec=128;c,_,p=canonical_ensemble();groups=[orbit(r['largest_midpoint_probe']) for r in data['shards']]
    values=[arb(0) for _ in groups]
    for j,w in sorted(p.items()):
        E=rotation_entries_exact(c[j])
        for k,O in enumerate(groups):values[k]+=ball(w)*principal_sum(E,O)/len(O)
    out={'input_sha256':data['input_sha256'],'precision_bits':128,'checked_rows':[]};have_lower=False
    for record,value in zip(data['shards'],values):
        I=record['largest_midpoint_probe'];t=target(I);e=(value-ball(t))/ball(abs(t));cap=ball(cfg['sixth_error_upper'])
        assert -cap<e<cap
        if I==[0,1,2,3,4,5]:
            assert abs(e)>ball('7743/5000');have_lower=True
        # Arb's displayed ball is an outward decimal enclosure. Compare to its
        # exact rational endpoints; no float parsing enters this check.
        text=record['largest_midpoint_residual'].strip('[]');m,r=map(lambda x:Fraction(x.strip()),text.split('+/-'))
        assert e>ball(m-r) and e<ball(m+r)
        out['checked_rows'].append({'shard':record['shard'],'probe':I,'residual_128_bits':str(e),
                                    'contained_in_reported_64_bit_enclosure':True})
    assert have_lower;out['complete_norm_strict_lower']='7743/5000'
    out['scope']='Higher-precision subset consistency check; the separate complete pass supplies the global upper certificate.'
    return out


if __name__=='__main__':print(json.dumps(verify(),indent=2))
