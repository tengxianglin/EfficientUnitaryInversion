"""Exact n=21 obstruction for at most two disjoint perfect-mirror segments.

LP discovery is optional; the certificate verifier uses integer/rational
arithmetic and no optimizer. See THEORY_TWO_MIRROR_OBSTRUCTION.md.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
import numpy as np
from verify_ising_minor_obstruction import (mirror, pair_sums,
                                          signed_permutation_minor, target)

N = 42
COEFFICIENTS = [-209,198,-201,209,-3,0,6,11,181,-12,15,-36,42,-52,
                44,-23,206,-209,54,-19,4,-209]
BASE = '7468a5fbb07c6c00bdd2b16fce226409312248af'


def seeds():
    # Segment A, idle gap g, segment B, remaining idle gap. Rotation/reflection
    # images are included through invariant averaged features, not extra columns.
    for a in range(1,N):
        for b in range(1,N-a+1):
            for gap in range(N-a-b+1):
                yield a,b,gap
    yield N,0,0  # full open mirror; all shorter single mirrors have b=1 copies


def permutation(seed):
    a,b,gap = seed
    p = np.arange(N)
    signs = np.ones(N,dtype=np.int64)
    for start,L in ((0,a),(a+gap,b)):
        p[start:start+L] = start+np.arange(L)[::-1]
        signs[start:start+L] = (-1)**np.arange(L)
    return p,signs


def numerator_rows():
    i,j = np.triu_indices(N,1)
    distance = np.minimum(j-i,N-j+i)
    quartets = (np.arange(N)[:,None]+np.arange(4)) % N
    quartets.sort(axis=1)
    rows = []
    for seed in seeds():
        p,s = permutation(seed)
        fixed = (p==np.arange(N))*s
        minors = fixed[i]*fixed[j]-((p[i]==j)&(p[j]==i))*s[i]*s[j]
        m = np.array([minors[distance==d].sum() for d in range(1,22)],dtype=np.int64)
        m[-1] *= 2  # antipodal pairs occur twice in the distance average
        image = p[quartets]
        closed = np.all(np.sort(image,axis=1)==quartets,axis=1)
        inversions = sum(image[:,u]>image[:,v] for u,v in combinations(range(4),2))
        q = np.sum(closed*(1-2*(inversions%2))*np.prod(s[quartets],axis=1))
        rows.append(np.r_[m,q])
    return np.array(rows,dtype=np.int64)


def audit_rows(rows):
    seedlist = list(seeds())
    for seed in ((1,1,0),(1,41,0),(5,31,3),(20,21,0),(7,12,11),(42,0,0)):
        p,s = permutation(seed)
        R = np.zeros((N,N),dtype=int)
        R[np.arange(N),p] = s
        # Compare against pre-existing independent pair enumeration, and all
        # 84 dihedral images using the exact principal-minor implementation.
        expected = pair_sums(R)
        expected[-1] *= 2
        expected.append(sum(signed_permutation_minor(R,[(shift+sign*j)%N for j in range(4)])
                            for shift in range(N) for sign in (-1,1))//2)
        np.testing.assert_array_equal(rows[seedlist.index(seed)],expected)
    np.testing.assert_array_equal(rows[-1,:21],
                                 np.array(pair_sums(mirror(21,42)))*np.r_[np.ones(20,dtype=int),2])


def verify(discover=False):
    rows = numerator_rows()
    assert rows.shape == (12342,22)
    audit_rows(rows)
    y = np.array(COEFFICIENTS,dtype=np.int64)
    scores = rows@y
    assert int(scores.max()) == -126
    t = [Fraction((-1)**(d+1),41) for d in range(1,22)] + [target(21,[0,1,2,3])]
    target_score = sum(int(c)*x for c,x in zip(y,t))
    assert target_score == Fraction(727,533)
    upper = Fraction(int(scores.max()),N)
    assert upper == -3
    gap = target_score-upper
    assert gap == Fraction(2326,533) > 0
    if discover:
        from scipy.optimize import linprog
        result = linprog(np.zeros(len(rows)),
                         A_eq=np.r_[(rows/N).T,np.ones((1,len(rows)))],
                         b_eq=np.r_[np.array(t,float),1],bounds=(0,None),method='highs')
        assert result.status == 2  # corroboration only, not the proof
    return {'base_commit':BASE,'n':21,'N':N,'columns':len(rows),
            'feature_denominator':N,'coefficients':COEFFICIENTS,
            'fourth_probe':[0,1,2,3], 'max_integer_score':int(scores.max()),
            'class_upper':str(upper),'target_score':str(target_score),'gap':str(gap),
            'saturated_columns':int(np.sum(scores==scores.max())),
            'maximizer':list(list(seeds())[int(scores.argmax())]),
            'integer_rows_sha256_le_i64':hashlib.sha256(rows.astype('<i8').tobytes()).hexdigest(),
            'status':'Exact finite-family convex-hull separation; general physical designs unresolved.'}


def fractional_screen():
    # Finite floating-point diagnostic, deliberately separate from exact proof.
    from verify_ising_minor_obstruction import rotation
    results = []
    for length in (10,21,30,41,42):
        for alpha in (Fraction(1,8),Fraction(1,4),Fraction(1,2),
                      Fraction(3,4),Fraction(5,4),Fraction(3,2)):
            c = np.zeros(N)
            c[:length-1] = [float(alpha)*np.pi/4*np.sqrt((j+1)*(length-j-1))
                           for j in range(length-1)]
            R = rotation(c)
            m = [sum(R[i,i]*R[(i+d)%N,(i+d)%N]-R[i,(i+d)%N]*R[(i+d)%N,i]
                     for i in range(N))/N for d in range(1,22)]
            q = sum(np.linalg.det(R[np.ix_([(i+j)%N for j in range(4)],
                                           [(i+j)%N for j in range(4)])]) for i in range(N))/N
            results.append({'length':length,'time_factor':str(alpha),
                            'score':float(np.dot(COEFFICIENTS,np.r_[m,q]))})
    best = max(results,key=lambda x:x['score'])
    assert best['length']==41 and best['time_factor']=='5/4'
    assert best['score'] > 13 and best['score'] > 727/533
    return {'base_commit':BASE,'status':'Finite floating diagnostic; not a full moment design or interval certificate.',
            'cases':results,'best':best,'uniform_target_score':727/533}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--discover',action='store_true',help='also rerun the floating feasibility LP')
    parser.add_argument('--fractional',action='store_true',help='run separate 30-case floating pre-screen')
    args=parser.parse_args()
    print(json.dumps(fractional_screen() if args.fractional else verify(args.discover),indent=2))
