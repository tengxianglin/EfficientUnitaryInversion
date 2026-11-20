"""Interval verification of a finite-pool separator and a new physical column."""
import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
import numpy as np
from flint import arb,arb_mat,fmpq,ctx
from ising_fourth_moments import seed_pool
from ising_moment_pricing import MomentFunctional

INPUT=Path(__file__).parent/'evidence/directed_fourth_pricing_n21.json'


def ball(q):
    q=Fraction(q);return arb(fmpq(q.numerator,q.denominator))


def ball_functional(functional,couplings):
    N=functional.N;c=list(map(Fraction,couplings))
    assert len(c)==N and c[-1]==0
    A=arb_mat(N,N)
    for j in range(N-1):A[j,j+1]=2*ball(c[j]);A[j+1,j]=-2*ball(c[j])
    R=A.exp();entries=[[R[i,j] for j in range(N)] for i in range(N)]
    s=functional.system
    factors={j:ball(q)/int(s.counts[j]) for j,q in functional.rational_coefficients.items()}
    score=arb(0)
    for d,a in enumerate(functional.second_rationals,1):
        if a:
            score+=ball(a)*sum((R[i,i]*R[(i+d)%N,(i+d)%N]-R[i,(i+d)%N]*R[(i+d)%N,i] for i in range(N)),arb(0))/N
    for I,j in zip(functional.indices,functional.orbit_ids):
        score+=factors[int(j)]*arb_mat([[entries[i][k] for k in I] for i in I]).det()
    return score


def verify(pool=False):
    data=json.loads(INPUT.read_text());f=MomentFunctional(data)
    exact=f.exact_target();assert exact==Fraction(data['target_score'])>Fraction(data['pool_bound'])
    ctx.prec=data['witness_precision_bits']
    witness=ball_functional(f,data['witness_couplings'])
    assert witness>ball(data['witness_floor']) and witness-ball(exact)>1
    identity=sum(f.rational_coefficients.values(),Fraction(0))+sum(f.second_rationals,Fraction(0))
    assert not (witness-ball(identity)).contains(0)
    assert all(Fraction(c)>0 for c in data['witness_couplings'][:-1])
    assert data['witness_couplings'][:-1]==data['witness_couplings'][:-1][::-1]
    out={'base_commit':data['base_commit'],'fourth_orbits':len(f.rational_coefficients),
         'distinct_quartets':len(f.indices),'target_score':str(exact),
         'pool_bound':data['pool_bound'],'target_minus_pool_bound':str(exact-Fraction(data['pool_bound'])),
         'witness_precision_bits':ctx.prec,'witness_score':str(witness),
         'witness_minus_target':str(witness-ball(exact)),
         'witness_floor':data['witness_floor'],'identity_score':str(identity),
         'witness_status':'Certified gapped physical column above target; connected path and nonidentity imply non-Pauli program.'}
    # This check validates the discovery gradient, not the existence proof.
    c=np.r_[np.random.default_rng(202611210641).normal(size=41),0]
    value,g=f.value_gradient(c);err=0
    for j in (0,20,40):
        d=np.zeros(42);d[j]=1e-5
        fd=(f.value_gradient(c+d,False)-f.value_gradient(c-d,False))/2e-5
        err=max(err,abs(fd-g[j]))
    assert err<1e-6
    out['finite_gradient_check_max_error']=float(err)
    if pool:
        cs=seed_pool();fingerprint=hashlib.sha256(cs.astype('<f8').tobytes()).hexdigest()
        assert fingerprint==data['pool_couplings_sha256_le_f64']
        ctx.prec=data['pool_precision_bits'];bound=ball(data['pool_bound']);worst=None;where=None
        for k,c in enumerate(cs):
            score=ball_functional(f,[Fraction.from_float(float(x)) for x in c])
            assert score<bound,(k,score,bound)
            if worst is None or float(score)>float(worst):worst=score;where=k
            if (k+1)%100==0:print(f'Certified {k+1}/{len(cs)} pool columns',file=sys.stderr,flush=True)
        out['finite_pool_certificate']={'columns':len(cs),'precision_bits':ctx.prec,
              'couplings_sha256_le_f64':fingerprint,'parameter_interpretation':data['pool_parameter_interpretation'],'all_scores_strictly_below':data['pool_bound'],
              'largest_midpoint_index':where,'largest_midpoint_score':str(worst),
              'status':'Certified finite-pool convex-hull separation; no global physical upper bound.'}
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pool',action='store_true')
    print(json.dumps(verify(p.parse_args().pool),indent=2))
