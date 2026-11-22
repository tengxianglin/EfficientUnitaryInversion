"""Complete dihedral degree-four features and exact odd-cycle dependencies."""
from itertools import combinations
from fractions import Fraction
from math import comb
import hashlib
from pathlib import Path
import numpy as np
from verify_ising_minor_obstruction import rotation


def orbit_key(indices,N):
    I=sorted(indices);g=tuple(I[j+1]-I[j] for j in range(len(I)-1))+(N+I[0]-I[-1],)
    return min(h[j:]+h[:j] for h in (g,g[::-1]) for j in range(len(I)))


def representative(gaps):
    return tuple(int(x) for x in np.cumsum((0,*gaps[:-1])))


def rank_certificate(M,prime=65521):
    A=np.asarray(M,dtype=np.int64).copy()%prime;row=0;pivots=[];determinant=1
    for j in range(A.shape[1]):
        nz=np.flatnonzero(A[row:,j])
        if not len(nz):continue
        k=row+int(nz[0])
        if k!=row:A[[row,k]]=A[[k,row]];determinant=-determinant
        value=int(A[row,j]);determinant=determinant*value%prime
        A[row]=A[row]*pow(value,-1,prime)%prime
        for k in range(len(A)):
            if k!=row:A[k]=(A[k]-A[k,j]*A[row])%prime
        pivots.append(j);row+=1
        if row==len(A):break
    return {'rank':row,'prime':prime,'pivot_columns':pivots,
            'pivot_minor_determinant_mod_prime':determinant%prime}


class FourthMoments:
    def __init__(self,n):
        if n<3 or n%2==0:raise ValueError('Require odd n>=3')
        self.n=n;self.N=N=2*n
        self.indices=np.array(list(combinations(range(N),4)))
        keys=[orbit_key(I,N) for I in self.indices]
        self.keys=sorted(set(keys));lookup={g:i for i,g in enumerate(self.keys)}
        self.ids=np.array([lookup[g] for g in keys]);self.counts=np.bincount(self.ids)
        self.representatives=[representative(g) for g in self.keys]
        triples=sorted({orbit_key((0,*J),N) for J in combinations(range(1,N),2)})
        self.triples=[representative(g) for g in triples]
        self.C=np.zeros((len(triples),len(self.keys)),dtype=np.int64)
        self.D=np.zeros((len(triples),n),dtype=np.int64)
        for row,K in enumerate(self.triples):
            for j in range(N):
                if j not in K:
                    I=(*K,j)
                    self.C[row,lookup[orbit_key(I,N)]]+=(-1)**sum(i%2 for i in I)
            for i,j in combinations(K,2):
                d=min(j-i,N-j+i);self.D[row,d-1]+=(-1)**d
        self.certificate=rank_certificate(self.C)
        self.rational_target=[Fraction((-1)**(d+1),N-1) for d in range(1,n+1)]
        self.rational_target += [Fraction((-1)**sum(i%2 for i in I)*comb(n,2),comb(N,4))
                                 for I in self.representatives]
        self.target=np.array(list(map(float,self.rational_target)))

    def features(self,c):
        R=rotation(c);N=self.N;i=np.arange(N);a=R.diagonal()
        second=[np.mean(a*a[(i+d)%N]-R[i,(i+d)%N]*R[(i+d)%N,i]) for d in range(1,self.n+1)]
        I=self.indices;values=np.linalg.det(R[I[:,:,None],I[:,None,:]])
        fourth=np.bincount(self.ids,weights=values,minlength=len(self.keys))/self.counts
        return np.r_[second,fourth]

    def reduced_indices(self):
        pivots=set(self.certificate['pivot_columns'])
        return list(range(self.n-1))+[self.n+j for j in range(len(self.keys)) if j not in pivots]

    def hierarchy_residual(self,W):
        W=np.atleast_2d(W)
        return self.C@W[:,self.n:].T+self.D@W[:,:self.n].T

    def second_relation_residual(self,W):
        W=np.atleast_2d(W)
        signs=np.array([(-1)**(d+1) for d in range(1,self.n)])
        return W[:,:self.n-1]@signs+W[:,self.n-1]/2-.5

    def exact_target_check(self):
        assert sum(((-1)**(d+1)*self.rational_target[d-1] for d in range(1,self.n)),Fraction(0))+self.rational_target[self.n-1]/2==Fraction(1,2)
        for C,D in zip(self.C,self.D):
            value=sum((int(a)*self.rational_target[self.n+j] for j,a in enumerate(C) if a),Fraction(0))
            value+=sum((int(a)*self.rational_target[j] for j,a in enumerate(D) if a),Fraction(0))
            assert value==0


def seed_pool(count=1600):
    frozen=Path(__file__).resolve().parent/'evidence/seed_pool_n21_frozen.npy'
    if count==1600 and frozen.exists():
        rows=np.load(frozen,allow_pickle=False)
        digest=hashlib.sha256(rows.astype('<f8',copy=False).tobytes()).hexdigest()
        if rows.shape!=(1600,42) or digest!='93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315':
            raise RuntimeError('frozen seed-pool shape or SHA256 mismatch')
        return rows
    rng=np.random.default_rng(202611210435);rows=[]
    for k in range(count):
        sigma=(0,.02,.1,.3,.7)[min(k//320,4)]
        tau=np.exp(rng.uniform(np.log(3),np.log(500)))
        rows.append(np.r_[tau*(1+sigma*rng.normal(size=41)),0])
    return np.array(rows)
