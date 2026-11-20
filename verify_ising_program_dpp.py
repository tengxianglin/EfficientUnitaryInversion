"""Independent checks of the program/DPP correspondence and sampling law."""
import argparse
import json
from fractions import Fraction as F
from itertools import combinations,permutations
from math import comb
import numpy as np
from ising_program_dpp import program_projection,probability,sample_programs
from ising_cycle_program_orbits import CycleProgramOrbits
from verify_ising_pure_pauli_classification import even_runs,lucas

BASE='d5b58da9529823fefb77e4a66f8915cadf6dd8d8'


def det(M):
    n=len(M)
    return sum(((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
                *np.prod([M[i][p[i]] for i in range(n)]) for p in permutations(range(n))),F(0))


def exact_sampling_check():
    # A rational orthogonal frame: tests the sampler law independently of
    # physical exponentials or rounded projection matrices.
    N=6;n=3;E=[[F(int(i==j)) for j in range(N)] for i in range(N)]
    for i in range(N-1):
        a,b=E[i][:],E[i+1][:]
        E[i]=[F(3,5)*x+F(4,5)*y for x,y in zip(a,b)]
        E[i+1]=[-F(4,5)*x+F(3,5)*y for x,y in zip(a,b)]
    P=[[sum((E[i][k]*E[j][k] for k in range(0,N,2)),F(0)) for j in range(N)] for i in range(N)]
    total=F(0);ordered=0
    for S in combinations(range(N),n):
        expected=det([[P[i][j] for j in S] for i in S]);actual=F(0)
        for order in permutations(S):
            K=[row[:] for row in P];q=F(1)
            for rank,i in zip(range(n,0,-1),order):
                pivot=K[i][i]
                if not pivot:q=F(0);break
                q*=pivot/rank
                K=[[K[u][v]-K[u][i]*K[i][v]/pivot for v in range(N)] for u in range(N)]
            actual+=q;ordered+=1
        assert actual==expected and actual>=0;total+=actual
    assert total==1
    return {'N':N,'subsets':comb(N,n),'ordered_paths':ordered,'normalization':str(total),
            'status':'Exact rational Schur-sampling law verified.'}


def checks():
    result={'base_commit':BASE,'exact_sampler_check':exact_sampling_check(),'finite_checks':[]}
    for n in (3,5,7):
        model=CycleProgramOrbits(n);rng=np.random.default_rng(202611210243+n)
        for gap in (False,True):
            c=rng.normal(size=2*n)
            if gap:c[-1]=0
            P=program_projection(c);w=model.masses(c,reduce=False)
            errors=[abs(probability(P,T)-v) for T,v in zip(model.labels,w)]
            error=max(errors)
            assert error<1e-11
            assert np.max(abs(P@P-P))<1e-12 and abs(np.trace(P)-n)<1e-12
            mass=sum(np.linalg.det(P[np.ix_(S,S)]) for S in combinations(range(2*n),n))
            assert abs(mass-1)<1e-11
            result['finite_checks'].append({'n':n,'gapped':gap,'all_program_labels':len(w),
                                           'max_mass_identity_error':float(error),'dpp_normalization':float(mass)})
    n=3;model=CycleProgramOrbits(n);c=np.random.default_rng(112358).normal(size=6)
    P=program_projection(c);expected=model.masses(c,reduce=False)
    samples=sample_programs(P,40000,np.random.default_rng(202611210244))
    empirical=np.array([samples.count(T)/len(samples) for T in model.labels])
    error=float(np.max(abs(empirical-expected)));assert error<.02
    result['finite_sampler_histogram']={'n':3,'samples':len(samples),'max_absolute_frequency_error':error,
                                       'status':'Finite floating diagnostic, not a sampling-error certificate.'}
    return result


def screen(samples=10000):
    n=21;N=42;full=(1<<N)-1;cases=[]
    for scale in (1,3,10,30,100):
        c=[scale]*41+[0];cases.append(('uniform_open_'+str(scale),list(map(str,c))))
    rng=np.random.default_rng(202611210245)
    c=rng.normal(size=N)*10;c[-1]=0
    cases.append(('disordered_open',list(map(lambda x:str(float(x)),c))))
    result={'base_commit':BASE,'n':n,'samples_per_case':samples,'sampler_rng_seed':202611210246,
            'uniform_matching_mass_target':str(F(lucas(N)-(1<<n),comb(N,n)//2)),
            'status':'Finite Monte Carlo screen using a floating sampler; no interval or full-design certificate.',
            'cases':[]}
    rng=np.random.default_rng(202611210246)
    for name,c in cases:
        labels=sample_programs(program_projection(list(map(float,c))),samples,rng)
        count=sum(even_runs(T,N) or even_runs(T^full,N) for T in labels)
        result['cases'].append({'name':name,'exact_decimal_couplings':c,
                                'matching_hits':count,'empirical_matching_mass':count/samples})
    return result


def refine_screen():
    N=42;count=100000
    labels=sample_programs(program_projection([100]*41+[0]),count,np.random.default_rng(202611210247))
    hits=sum(even_runs(T,N) or even_runs(T^((1<<N)-1),N) for T in labels)
    return {'base_commit':BASE,'case':'uniform_open_100','samples':count,
            'sampler_seed':202611210247,'couplings':['100']*41+['0'],
            'matching_hits':hits,'empirical_matching_mass':hits/count,
            'status':'Finite floating Monte Carlo diagnostic only; no interval probability bound.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();group=p.add_mutually_exclusive_group()
    group.add_argument('--screen',action='store_true');group.add_argument('--refine',action='store_true');args=p.parse_args()
    print(json.dumps(refine_screen() if args.refine else screen() if args.screen else checks(),indent=2))
