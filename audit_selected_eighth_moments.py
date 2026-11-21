"""Arb audit of selected independent eighth-order moment rows.

This is a deliberately small diagnostic, not a complete degree-eight
separation certificate.  It uses the exact 83-seed ensemble from the
sixth-order certificate and proves strict lower bounds on six fixed rows.
"""
import hashlib,json
from fractions import Fraction
from math import comb
from pathlib import Path
from flint import arb,arb_mat,ctx
from audit_complete_sixth_moments import canonical_ensemble,ROOT
from screen_ising_sixth_moments import orbit
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CASES=[
 ([0,1,2,3,4,5,6,7],Fraction(6)),
 ([0,5,10,15,20,25,30,35],Fraction(1)),
 ([0,1,8,9,16,17,24,25],Fraction(9,10)),
 ([0,4,12,16,20,28,32,36],Fraction(2)),
 ([0,2,6,14,22,30,34,40],Fraction(6,5)),
 ([0,3,9,14,21,27,33,39],Fraction(3,10)),
]

def minor(E,I): return arb_mat([[E[i][j] for j in I] for i in I]).det()

def verify():
    raw=(ROOT/'evidence/complete_sixth_certificate_input_n21.json').read_bytes()
    cfg=json.loads(raw)
    for name,sha in cfg['source_sha256'].items():
        assert hashlib.sha256((ROOT/'evidence'/name).read_bytes()).hexdigest()==sha
    ctx.prec=128;c,_,p=canonical_ensemble()
    magnitude=Fraction(comb(21,4),comb(42,8))
    rows=[]
    for I,threshold in CASES:
        assert I==sorted(I) and len(I)==8 and len(set(I))==8
        O=orbit(I);q=arb(0)
        for j,w in sorted(p.items()):
            E=rotation_entries_exact(c[j])
            q+=ball(w)*sum((minor(E,J) for J in O),arb(0))/len(O)
        target=(-1)**(sum(i%2 for i in I)+4)*magnitude
        e=(q-ball(target))/ball(magnitude)
        assert abs(e)>ball(threshold),(I,e,threshold)
        rows.append({'indices':I,'orbit_size':len(O),'target':str(target),'moment':str(q),
                     'relative_error':str(e),'absolute_error_strict_lower':str(threshold)})
    return {'base_commit':'334d1ef5e1819bc1ab72a1f770b362d687436e5d',
            'precision_bits':128,'input_sha256':hashlib.sha256(raw).hexdigest(),
            'target_magnitude':str(magnitude),'cases':rows,
            'scope':'Six fixed eighth-order rows only; no complete degree-eight upper bound or optimization claim.'}

if __name__=='__main__': print(json.dumps(verify(),indent=2))
