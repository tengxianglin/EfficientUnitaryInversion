"""Frechet/cofactor pricing for the frozen low/contiguous-sixth functional."""
from fractions import Fraction
import numpy as np
from scipy.linalg import expm,expm_frechet
from ising_moment_pricing import MomentFunctional
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit


class SixthPricing:
    def __init__(self,data):
        s=FourthMoments(21);y=list(map(Fraction,data['direction_24']));z=list(map(Fraction,data['direction_6']))
        assert len(y)==1461 and len(z)==256 and z[0]==-1 and all(v==0 for v in z[1:])
        self.low=MomentFunctional({'n':21,'second_coefficients':[str(a*41) for a in y[:21]],
             'terms':[{'indices':list(s.representatives[j]),'coefficient':str(a*533)} for j,a in enumerate(y[21:]) if a]})
        self.indices=np.array(orbit(range(6)));self.coefficient=-Fraction(19721,5)

    def value_gradient(self,c,gradient=True):
        c=np.asarray(c,float);assert len(c)==42 and c[-1]==0
        value=self.low.value_gradient(c,gradient)
        if gradient:value,g=value
        N=42;i=np.arange(N);j=(i+1)%N;A=np.zeros((N,N));A[i,j]=2*c;A[j,i]=-2*np.asarray(c)
        R=expm(A);I=self.indices;B=R[I[:,:,None],I[:,None,:]]
        factor=float(self.coefficient)/len(I);value+=factor*sum(np.linalg.det(B))
        if not gradient:return float(value)
        G=np.zeros_like(R)
        for u in range(6):
            for v in range(6):
                cof=(-1)**(u+v)*np.linalg.det(np.delete(np.delete(B,u,axis=1),v,axis=2))
                np.add.at(G,(I[:,u],I[:,v]),factor*cof)
        adjoint=expm_frechet(A.T,G,compute_expm=False)
        return float(value),g+2*(adjoint[i,j]-adjoint[j,i])[:-1]
