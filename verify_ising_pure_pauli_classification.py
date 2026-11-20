"""Exact static odd-cycle Pauli-oracle classification and counting checks.

All-n necessity is analytic (THEORY_PURE_PAULI_CLASSIFICATION.md).
Finite enumeration is exact; optional matrix checks use floating arithmetic.
"""
import argparse
import json
from fractions import Fraction
from functools import lru_cache
from math import comb

BASE='1d339a919d837269161dc6ac2732c137d809ed90'


def lucas(k):
    a,b=2,1
    for _ in range(k):a,b=b,a+b
    return a


def path_matching_endpoints(vertices):
    if not vertices:
        yield 0
        return
    first=vertices[0]
    yield from path_matching_endpoints(vertices[1:])
    if len(vertices)>1:
        edge=(1<<first)|(1<<vertices[1])
        for rest in path_matching_endpoints(vertices[2:]):yield edge|rest


def cycle_matching_endpoints(N):
    # Separate matchings by whether they contain the closing edge.
    yield from path_matching_endpoints(tuple(range(N)))
    wrap=(1<<(N-1))|1
    for rest in path_matching_endpoints(tuple(range(1,N-1))):yield wrap|rest


def even_runs(mask,N):
    """Induced cycle admits a perfect matching iff every proper run is even."""
    full=(1<<N)-1
    if mask in (0,full):return True
    start=next(j for j in range(N) if not (mask>>j)&1)
    run=0
    for step in range(1,N+1):
        if (mask>>((start+step)%N))&1:run+=1
        else:
            if run%2:return False
            run=0
    return True


@lru_cache(None)
def graph_matching(mask,N):
    """Independent recursion on available neighbors, returning an edge witness."""
    if not mask:return ()
    i=(mask&-mask).bit_length()-1
    for j in ((i-1)%N,(i+1)%N):
        if (mask>>j)&1:
            rest=graph_matching(mask^(1<<i)^(1<<j),N)
            if rest is not None:return ((i,j),)+rest
    return None


def balanced(mask,n):
    return sum((mask>>(2*j))&1 for j in range(n))==sum((mask>>(2*j+1))&1 for j in range(n))


def exact_checks():
    enumerations=[]
    for n in (3,5,7,9):
        N=2*n;full=(1<<N)-1
        endpoints=list(cycle_matching_endpoints(N));covered=set(endpoints)
        labels={min(m,m^full) for m in covered}
        expected=lucas(N)-(1<<n)
        assert len(endpoints)==lucas(N)
        assert len(covered)==lucas(N)-1 and len(labels)==expected
        both={m for m in covered if (m^full) in covered}
        assert len(both)==(1<<(n+1))-2
        checked=0;balanced_checked=0
        for m in range(1<<(N-1)):
            if m.bit_count()%2:continue
            balanced_checked+=int(balanced(m,n))
            condition=even_runs(m,N) or even_runs(m^full,N)
            assert condition==(m in labels)
            assert even_runs(m,N)==(graph_matching(m,N) is not None)
            assert even_runs(m^full,N)==(graph_matching(m^full,N) is not None)
            checked+=1
        assert checked==4**(n-1) and balanced_checked==comb(N,n)//2
        assert all(balanced(m,n) for m in labels)
        enumerations.append({'n':n,'all_logical_paulis_checked':checked,'balanced_labels_checked':balanced_checked,
                             'all_cycle_matchings':len(endpoints),
                             'pure_pauli_classes':len(labels),'both_covers':len(both)})
        graph_matching.cache_clear()
    T=sum(1<<j for j in (0,2,3,5))
    for n in (5,7,21):
        assert balanced(T,n)
        assert not even_runs(T,2*n) and not even_runs(T^((1<<(2*n))-1),2*n)
    counts=[]
    for n in (3,5,7,9,11,21,51):
        b=lucas(2*n)-(1<<n);s=comb(2*n,n)//2
        counts.append({'n':n,'pure_pauli_classes':b,'balanced_classes':s,
                       'pure_atom_weight_upper':str(Fraction(b,s)),
                       'non_pure_atom_weight_lower':str(1-Fraction(b,s))})
    return {'base_commit':BASE,'exact_enumerations':enumerations,
            'unrealizable_balanced_label_indices':[0,2,3,5],
            'all_n_formula_checks':counts,
            'status':'Finite exact consistency checks of an analytic all-odd-n classification.'}


def matrix_checks():
    import numpy as np
    from ising_cycle_program_orbits import CycleProgramOrbits
    from verify_ising_minor_obstruction import rotation
    result=[]
    for n in (3,5):
        N=2*n;full=(1<<N)-1;model=CycleProgramOrbits(n)
        labels=sorted({min(m,m^full) for m in cycle_matching_endpoints(N)})
        max_mass_error=0.0;max_rotation_error=0.0
        for T in labels:
            chosen=T if even_runs(T,N) else T^full
            matching=graph_matching(chosen,N)
            c=np.zeros(N)
            for i,j in matching:
                edge=i if j==(i+1)%N else j
                c[edge]=np.pi/2
            R=rotation(c);expected=np.diag([-1 if (chosen>>i)&1 else 1 for i in range(N)])
            max_rotation_error=max(max_rotation_error,float(np.max(abs(R-expected))))
            mass=model.masses(c,reduce=False);target=np.zeros(len(model.labels));target[model.index[T]]=1
            max_mass_error=max(max_mass_error,float(np.max(abs(mass-target))))
        assert max_mass_error<1e-11 and max_rotation_error<1e-11
        # The independence of the grade-two restrictions used in the proof.
        bilinears=[]
        for i in range(N):
            for j in range(i+1,N):
                rows,phase=model.sparse((1<<i)|(1<<j));B=np.zeros((model.D,model.D),complex)
                B[rows,np.arange(model.D)]=phase;bilinears.append(B.ravel())
        B=np.array(bilinears)
        np.testing.assert_array_equal(B.conj()@B.T,model.D*np.eye(len(B)))
        result.append({'n':n,'all_pure_classes_realized':len(labels),
                       'max_program_mass_error':max_mass_error,'max_rotation_error':max_rotation_error,
                       'independent_bilinears':len(B)})
        graph_matching.cache_clear()
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--matrices',action='store_true')
    output=exact_checks()
    if parser.parse_args().matrices:output['finite_matrix_checks']=matrix_checks()
    print(json.dumps(output,indent=2))
