"""Positive determinant representation and sampler for odd-cycle programs.

Exact-arithmetic law is proved in THEORY_PROGRAM_DPP.md. The NumPy sampler
is a finite floating implementation; it does not certify full uniformity.
"""
import numpy as np
from scipy.linalg import expm


def generator(couplings):
    c=np.asarray(couplings,float);N=len(c)
    if N<6 or N%4!=2:raise ValueError('Require N=2n with odd n>=3')
    i=np.arange(N);j=(i+1)%N
    A=np.zeros((N,N));A[i,j]=2*c;A[j,i]=-2*c
    return A


def program_projection(couplings):
    A=generator(couplings)
    U=expm(-A/2)[:,::2]
    return U@U.T


def folded_label(S,N):
    initial=sum(1<<j for j in range(0,N,2));full=(1<<N)-1
    T=S^initial
    return min(T,T^full)


def probability(P,label):
    N=len(P);initial=sum(1<<j for j in range(0,N,2));S=label^initial
    i=[j for j in range(N) if S>>j&1];ic=[j for j in range(N) if not S>>j&1]
    if len(i)!=N//2:raise ValueError('Require a balanced even Majorana label')
    return np.linalg.det(P[np.ix_(i,i)])+np.linalg.det(P[np.ix_(ic,ic)])


def sample_programs(P,count,rng,batch_size=256):
    """O(N^3) work/sample, O(batch_size*N^2) memory, no label enumeration.

    Schur-complement rank reduction samples the projection DPP. Tiny negative
    diagonals are clipped only after a diagnostic bound; this is not a
    certified floating-point total-variation guarantee.
    """
    N=len(P);n=N//2;out=[]
    for start in range(0,count,batch_size):
        size=min(batch_size,count-start);K=np.broadcast_to(P,(size,N,N)).copy()
        selected=np.zeros((size,N),bool);masks=[0]*size;rows=np.arange(size)
        for rank in range(n,0,-1):
            diagonal=np.diagonal(K,axis1=1,axis2=2).copy()
            assert diagonal.min()>-1e-7
            diagonal[selected]=0;diagonal=np.maximum(diagonal,0)
            weights=diagonal/diagonal.sum(axis=1)[:,None]
            cumulative=np.cumsum(weights,axis=1);cumulative[:,-1]=1
            chosen=np.sum(rng.random(size)[:,None]>cumulative,axis=1)
            assert not np.any(selected[rows,chosen])
            pivot=K[rows,chosen,chosen]
            assert np.all(pivot>0)
            column=K[rows,:,chosen].copy()
            K-=column[:,:,None]*column[:,None,:]/pivot[:,None,None]
            selected[rows,chosen]=True
            for r,j in enumerate(chosen):masks[r]|=1<<int(j)
        out.extend(folded_label(S,N) for S in masks)
    return out
