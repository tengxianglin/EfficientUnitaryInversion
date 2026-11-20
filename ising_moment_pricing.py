"""Fixed fourth-moment functionals and a Frechet-gradient pricing oracle.

The optimizer is a discovery tool, not a global maximizer certificate.
"""
from fractions import Fraction
import numpy as np
from scipy.linalg import expm,expm_frechet
from ising_fourth_moments import FourthMoments,orbit_key


class MomentFunctional:
    def __init__(self,data):
        self.system=FourthMoments(data['n']);s=self.system;self.N=s.N
        self.second_rationals=list(map(Fraction,data.get('second_coefficients',['0']*s.n)))
        assert len(self.second_rationals)==s.n
        self.second=np.array(list(map(float,self.second_rationals)))
        self.coefficients=np.zeros(len(s.keys))
        self.rational_coefficients={}
        lookup={key:j for j,key in enumerate(s.keys)}
        for term in data['terms']:
            j=lookup[orbit_key(term['indices'],s.N)]
            assert j not in self.rational_coefficients
            q=Fraction(term['coefficient']);self.rational_coefficients[j]=q
            self.coefficients[j]=float(q)
        mask=self.coefficients[s.ids]!=0
        self.indices=s.indices[mask]
        self.orbit_ids=s.ids[mask]
        self.weights=self.coefficients[self.orbit_ids]/s.counts[self.orbit_ids]

    def value_gradient(self,couplings,gradient=True):
        c=np.asarray(couplings,float);N=self.N;ii=np.arange(N);jj=(ii+1)%N
        assert len(c)==N and c[-1]==0
        A=np.zeros((N,N));A[ii,jj]=2*c;A[jj,ii]=-2*c
        R=expm(A);I=self.indices;B=R[I[:,:,None],I[:,None,:]]
        value=float(self.weights@np.linalg.det(B))
        G=np.zeros((N,N)) if gradient else None
        diagonal=R.diagonal()
        for d,a in enumerate(self.second,1):
            if not a:continue
            j=(ii+d)%N
            value+=a*np.mean(diagonal*diagonal[j]-R[ii,j]*R[j,ii])
            if gradient:
                G[ii,ii]+=a*diagonal[j]/N;G[j,j]+=a*diagonal/N
                G[ii,j]-=a*R[j,ii]/N;G[j,ii]-=a*R[ii,j]/N
        if not gradient:return value
        for u in range(4):
            for v in range(4):
                cof=(-1)**(u+v)*np.linalg.det(np.delete(np.delete(B,u,axis=1),v,axis=2))
                np.add.at(G,(I[:,u],I[:,v]),self.weights*cof)
        adjoint=expm_frechet(A.T,G,compute_expm=False)
        grad=2*(adjoint[ii,jj]-adjoint[jj,ii])
        return value,grad[:-1]

    def exact_target(self):
        s=self.system
        return sum((a*s.rational_target[s.n+j] for j,a in self.rational_coefficients.items()),Fraction(0))+sum((a*s.rational_target[j] for j,a in enumerate(self.second_rationals)),Fraction(0))
