"""Exact-input scalar escape certificates, independent of local optimization."""
import hashlib
import json
from fractions import Fraction
from flint import ctx
from ising_sixth_pricing import SixthPricing
from verify_ising_moment_pricing import ball,ball_functional
from verify_full_low_moment_certificate import rotation_entries,fourth_sum as principal_sum,ROOT
from screen_ising_sixth_moments import orbit


def verify():
    data=json.loads((ROOT/'evidence/sixth_pricing_escape_n21.json').read_text());assert data['run_complete']
    raw=(ROOT/'evidence/fixed_pool_tradeoff_n21.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==data['functional_source_sha256']
    f=SixthPricing(json.loads(raw));ctx.prec=192
    prior=json.loads((ROOT/'evidence/fixed_pool_tradeoff_certificate_n21.json').read_text())
    source=json.loads(raw);alpha=sum((abs(Fraction(x)) for x in source['direction_24']),Fraction(0))
    exact_target=f.low.exact_target()+f.coefficient*Fraction(5,19721)
    assert exact_target==Fraction(prior['target_functional']) and alpha==Fraction(prior['low_coefficient_l1'])
    threshold=exact_target-Fraction(prior['low_cap'])*alpha-1
    assert threshold==Fraction(-39378876937,250000000)
    identity=sum(f.low.rational_coefficients.values(),Fraction(0))+sum(f.low.second_rationals,Fraction(0))+f.coefficient
    out={'base_commit':data['base_commit'],'precision_bits':192,'old_pool_upper':prior['strict_pool_upper'],
         'necessary_repair_threshold':str(threshold),'identity_functional':str(identity),'certified_candidates':[]}
    for r in data['candidates']:
        c=list(map(Fraction,r['couplings']));assert len(c)==42 and c[-1]==0 and all(c[:-1])
        E=rotation_entries_exact(c)
        value=ball_functional(f.low,c)+ball(f.coefficient)*principal_sum(E,orbit(range(6)))/42
        assert value>3700 and value>ball(threshold) and value>ball(prior['target_functional'])
        assert not (value-ball(identity)).contains(0)
        out['certified_candidates'].append({'start':r['start'],'functional_value':str(value),'strict_floor':'3700',
                                          'non_pauli_by_connected_path_test':True})
    out['scope']='Physical columns outside the old finite moment hull; crossing a necessary scalar threshold does not prove a uniform or repaired ensemble.'
    return out


def rotation_entries_exact(c):
    from flint import arb_mat
    A=arb_mat(42,42)
    for j in range(41):A[j,j+1]=2*ball(c[j]);A[j+1,j]=-2*ball(c[j])
    R=A.exp();return [[R[i,j] for j in range(42)] for i in range(42)]


if __name__=='__main__':print(json.dumps(verify(),indent=2))
