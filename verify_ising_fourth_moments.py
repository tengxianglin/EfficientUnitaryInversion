"""Fourth-moment hierarchy checks and a certified six-seed rejection.

--search is an optional finite numerical LP study, not a physical no-go proof.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from flint import arb,arb_mat,fmpq,fmpz_mat,ctx
from ising_fourth_moments import FourthMoments,seed_pool

BASE='13a15652b9c752207869aeedbf95b6e0a85151e2'


def ball(x):
    q=Fraction(x);return arb(fmpq(q.numerator,q.denominator))


def six_seed_certificate(cases):
    ctx.prec=192;out=[]
    for case in cases:
        c=list(map(Fraction,case['exact_decimal_couplings']))
        assert len(c)==42 and c[-1]==0
        A=arb_mat(42,42)
        for j in range(41):A[j,j+1]=2*ball(c[j]);A[j+1,j]=-2*ball(c[j])
        R=A.exp()
        m=sum((R[i,i]*R[(i+2)%42,(i+2)%42]-R[i,(i+2)%42]*R[(i+2)%42,i] for i in range(42)),arb(0))/42
        assert m>ball('-17/1000')
        out.append({'name':case['name'],'distance_two_moment':str(m),
                    'residual_above_target':str(m+ball('1/41'))})
    return {'precision_bits':192,'cases':out,'class_strict_lower':'-17/1000',
            'target':'-1/41','certified_gap_above_target':'303/41000',
            'status':'Exact finite six-seed mixture rejection, including dihedral images.'}


def checks():
    output={'base_commit':BASE,'hierarchy_checks':[]}
    for n in (3,5,7,21):
        s=FourthMoments(n);s.exact_target_check()
        c=np.random.default_rng(202611210436+n).normal(size=2*n);c[-1]=0
        f=s.features(c);defect=float(np.max(abs(s.hierarchy_residual(f))))
        assert defect<1e-10
        second_defect=float(np.max(abs(s.second_relation_residual(f))))
        assert second_defect<1e-10
        output['hierarchy_checks'].append({'n':n,'quartets':len(s.indices),
             'fourth_orbits':len(s.keys),'triple_orbits':len(s.triples),
             'exact_rank_certificate':s.certificate,'finite_hierarchy_defect':defect,'finite_second_relation_defect':second_defect,
             'reduced_equations_including_normalization':len(s.reduced_indices())+1})
    s=FourthMoments(21)
    assert s.C.shape==(147,1440) and s.certificate['rank']==147
    assert len(s.reduced_indices())+1==1314
    minor_det=fmpz_mat(s.C[:,s.certificate['pivot_columns']].tolist()).det()
    assert minor_det==824633720832
    assert int(minor_det)%65521==s.certificate['pivot_minor_determinant_mod_prime']
    output['n21_exact_pivot_minor_determinant']=str(minor_det)
    path=Path(__file__).parent/'evidence/program_dpp_screen_n21.json'
    cases=json.loads(path.read_text())['cases']
    output['six_seed_certificate']=six_seed_certificate(cases)
    audit=[]
    for case in cases:
        f=s.features(list(map(float,case['exact_decimal_couplings'])));e=f-s.target
        j=int(np.argmax(abs(e[21:])))
        audit.append({'name':case['name'],'max_abs_second_residual':float(max(abs(e[:21]))),
                      'max_abs_fourth_residual':float(abs(e[21+j])),
                      'worst_fourth_probe':list(s.representatives[j])})
    output['six_seed_full_orbit_audit']=audit
    return output


def search(cache=None):
    from scipy.optimize import linprog
    s=FourthMoments(21);cs=seed_pool()
    if cache and Path(cache).exists():
        data=np.load(cache);np.testing.assert_array_equal(data['couplings'],cs);W=data['W']
        assert W.shape==(1600,1461)
        for j in (0,319,320,1599):np.testing.assert_allclose(W[j],s.features(cs[j]),atol=1e-12,rtol=0)
    else:
        import sys
        rows=[]
        for k,c in enumerate(cs):
            rows.append(s.features(c))
            if (k+1)%200==0:print(f"Computed {k+1}/{len(cs)} complete fourth-order columns",file=sys.stderr,flush=True)
        W=np.array(rows)
        if cache:np.savez(cache,couplings=cs,W=W)
    defect=float(np.max(abs(s.hierarchy_residual(W))))
    assert defect<1e-8
    second_defect=float(np.max(abs(s.second_relation_residual(W))))
    assert second_defect<1e-8
    cols=s.reduced_indices();scale=np.array([41 if j<21 else 533 for j in cols])
    A=W[:,cols].T*scale[:,None];rhs=s.target[cols]*scale
    result=linprog(np.zeros(len(W)),A_eq=np.r_[A,np.ones((1,len(W)))],
                   b_eq=np.r_[rhs,1],bounds=(0,None),method='highs-ipm',options={'time_limit':120})
    out={'base_commit':BASE,'n':21,'seed_count':len(W),'rng_seed':202611210435,
         'recipe':'320 each at relative disorder 0,.02,.1,.3,.7; log-uniform scale 3..500; wrap zero',
         'full_feature_count':1461,'reduced_equations_including_normalization':len(cols)+1,
         'couplings_sha256_le_f64':hashlib.sha256(cs.astype('<f8').tobytes()).hexdigest(),
         'features_sha256_le_f64':hashlib.sha256(W.astype('<f8').tobytes()).hexdigest(),
         'max_hierarchy_defect':defect,'max_second_relation_defect':second_defect,'solver':'scipy.linprog highs-ipm, scaled rows, 120-second limit',
         'solver_status':int(result.status),'solver_message':result.message,
         'solver_success':bool(result.success),
         'status':'Finite numerical convex-hull diagnostic only; not an exact certificate or general physical no-go.'}
    if result.success:
        out['full_max_residual']=float(np.max(abs(W.T@result.x-s.target)))
        out['positive_weight_count']=int(np.sum(result.x>1e-8))
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--search',action='store_true');p.add_argument('--cache')
    args=p.parse_args();print(json.dumps(search(args.cache) if args.search else checks(),indent=2))
