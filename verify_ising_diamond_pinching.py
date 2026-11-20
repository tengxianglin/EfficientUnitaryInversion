"""Independent parity and full-Kraus checks of the balanced pinching converse.

Small matrices test identities; the all-H converse uses the joint ensemble
and analytic pinching proof. No diamond SDP or sampled norm is treated as a
proof of a supremum.
"""
from itertools import combinations
from math import comb
import numpy as np
from scipy.linalg import expm,block_diag
from ising_cycle_program_orbits import CycleProgramOrbits
from verify_ising_radial_twirl import radial_gain


def setup(n):
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    gamma=[]
    for site in range(n):
        for local in (X,-Y):
            p=np.ones((1,1))
            for j in range(n):p=np.kron(p,Z if j<site else local if j==site else I)
            gamma.append(p)
    basis=[[x for x in range(1<<n) if x.bit_count()%2==s] for s in (0,1)]
    masks=[m for m in range(1<<(2*n-1)) if m.bit_count()%2==0]
    balanced=[j for j,m in enumerate(masks) if sum((m>>(2*k))&1 for k in range(n))==sum((m>>(2*k+1))&1 for k in range(n))]
    raw=[]
    for m in masks:
        p=np.eye(1<<n,dtype=complex)
        for j in range(2*n):
            if (m>>j)&1:p=p@gamma[j]
        raw.append(p)
    ps=[np.stack([p[np.ix_(b,b)] for p in raw]) for b in basis]
    C=np.eye(1<<n,dtype=complex)
    for g in gamma[1::2]:C=C@g
    Q=[]
    for b in basis:
        columns=[]
        for degree in range(1,n,2):
            for labels in combinations(range(2*n),degree):
                p=C.copy()
                for j in reversed(labels):p=gamma[j]@p
                columns.append(p[np.ix_(b,b)].conj().reshape(-1)/np.sqrt(len(b)))
        frame=np.column_stack(columns);Q.append(frame@frame.conj().T)
    return basis,masks,balanced,ps,Q


def physical_h_from_c(n,c,model):
    # Construct the global spin Hamiltonian, not a common quadratic spinor
    # Hamiltonian incorrectly shared between the physical parity sectors.
    size=1<<n;h=np.zeros((size,size),complex)
    for j in range(n):
        bit=1<<(n-1-j)
        h+=c[2*j]*np.diag([(-1)**int(bool(x&bit)) for x in range(size)])
        mask=bit|(1<<(n-1-((j+1)%n)))
        expected=np.zeros((model.D,model.D))
        expected[[model.lookup[int(x)^mask] for x in model.basis],np.arange(model.D)]=1
        sign=int(round(np.trace(model.Hbasis[2*j+1]@expected)/model.D))
        edge=np.zeros((size,size));edge[np.arange(size)^mask,np.arange(size)]=1
        h+=sign*c[2*j+1]*edge
    return h


def parity_check():
    rng=np.random.default_rng(202611201642)
    worst=0.
    for n in (3,5):
        m=CycleProgramOrbits(n);basis,masks,balanced,ps,Q=setup(n)
        theta=rng.normal(size=2*n);theta[-1]=0
        for shift in range(m.N):
            for reflection in (-1,1):
                c=m.transform_couplings(theta,shift,reflection)
                h=physical_h_from_c(n,c,m)
                masses=[]
                for s in (0,1):
                    v=expm(1j*h[np.ix_(basis[s],basis[s])])
                    coefficients=np.einsum('tij,ij->t',ps[s].conj(),v)/m.D
                    masses.append(abs(coefficients)**2)
                defect=max(abs(masses[0]-masses[1]));worst=max(worst,defect)
                assert defect<2e-12
                np.testing.assert_allclose(masses[0][balanced],m.masses(c,reduce=False),atol=2e-12,rtol=0)
        print(n,'gapped physical parity masses agree for every dihedral image',flush=True)
    print('Maximum parity-mass defect',worst,flush=True)


def kraus_check():
    n=3;d=4;f=6/16
    basis,masks,protected,ps,Q=setup(n);outside=[j for j in range(len(masks)) if j not in protected]
    rng=np.random.default_rng(202611201643);model=CycleProgramOrbits(n)
    minimum_gap=1.;worst_block=0.;cases=0
    for sample in range(5):
        theta=np.zeros(2*n) if sample==0 else rng.normal(size=2*n)
        h=physical_h_from_c(n,theta,model)
        v=[expm(1j*h[np.ix_(b,b)]) for b in basis]
        target=block_diag(*v).reshape(-1)/np.sqrt(2*d)
        bell=[]
        for s in (0,1):
            mat=np.zeros((2*d,2*d),complex);mat[s*d:(s+1)*d,s*d:(s+1)*d]=v[s]/np.sqrt(d)
            bell.append(mat.reshape(-1))
        frame=np.column_stack(bell);proj=frame@frame.conj().T
        for p in (.2,.6,1.):
            for eps in (.013,.17,.41):
                a=np.exp(-6j*eps);b=np.exp(2j*eps)-a;g=a+p*f*b
                gamma=p*abs(b)**2*f*(1-f);c=abs(1-g)
                assert 1-abs(g)**2-gamma>=-2e-12 and c>=gamma/2-2e-12
                for rule in ('ml','random'):
                    K=[];F=[]
                    for s in (0,1):
                        q=rng.random((len(outside),len(masks)))
                        if rule=='ml':
                            q[:]=0;q[:,protected]=1
                        q/=q.sum(axis=1,keepdims=True)
                        aa,bb=(a,b) if s==0 else (a.conjugate(),b.conjugate())
                        Fs=0.
                        for flag,amplitude in enumerate((aa*np.eye(d*d)+p*bb*Q[s],np.sqrt(p*(1-p))*bb*Q[s])):
                            joint=(np.kron(v[s],v[s])@amplitude).reshape(d,d,d,d)
                            qjoint=(np.kron(v[s],v[s])@Q[s]).reshape(d,d,d,d)
                            for label,R in enumerate(ps[s]):
                                block=np.einsum('er,aeir->ai',R.conj()/np.sqrt(d),joint)/np.sqrt(d)
                                if flag==0 and label in outside:
                                    oi=outside.index(label)
                                    L=np.einsum('er,aeir->ai',R.conj()/np.sqrt(d),qjoint)/np.sqrt(d)
                                    for t,T in enumerate(ps[s]):
                                        if q[oi,t]==0:continue
                                        correction=T@R.conj().T
                                        mat=np.zeros((2*d,2*d),complex)
                                        mat[s*d:(s+1)*d,s*d:(s+1)*d]=np.sqrt(q[oi,t])*correction@block
                                        K.append(mat/np.sqrt(2))
                                        Fs+=q[oi,t]*abs(np.trace(v[s].conj().T@correction@L)/d)**2
                                else:
                                    mat=np.zeros((2*d,2*d),complex)
                                    mat[s*d:(s+1)*d,s*d:(s+1)*d]=block
                                    if flag==0:
                                        component=np.trace(R.conj().T@v[s])/d
                                        mat[(1-s)*d:(2-s)*d,(1-s)*d:(2-s)*d]=component*v[1-s]
                                    K.append(mat/np.sqrt(2))
                        F.append(Fs)
                    np.testing.assert_allclose(sum(k.conj().T@k for k in K),np.eye(2*d),atol=3e-12,rtol=0)
                    vectors=np.stack([k.reshape(-1)/np.sqrt(2*d) for k in K])
                    change=vectors.T@vectors.conj()-np.outer(target,target.conj())
                    sigma=gamma-p*p*abs(b)**2*np.array(F)
                    expected=np.array([[-sigma[0]/4,(g-1)/2],[(g.conjugate()-1)/2,-sigma[1]/4]])
                    defect=np.linalg.norm(frame.conj().T@change@frame-expected);worst_block=max(worst_block,defect)
                    assert defect<3e-12
                    other=(np.eye(len(target))-proj)@change@(np.eye(len(target))-proj)
                    assert np.linalg.eigvalsh(other).min()>-3e-12
                    assert abs(np.trace(other).real-sum(sigma)/4)<3e-12
                    observed=abs(np.linalg.eigvalsh(change)).sum()
                    lower=c+gamma/2-p*p*abs(b)**2*sum(F)/4
                    assert observed>=lower-3e-12
                    if rule=='ml':
                        expected_norm=c+gamma/2-p*p*abs(b)**2*float(radial_gain(n,'ml'))/(2*d**4)
                        assert abs(observed-expected_norm)<3e-12
                    minimum_gap=min(minimum_gap,observed-lower);cases+=1
    print('Full balanced Kraus/pinching cases',cases,'max block defect',worst_block,'minimum norm-minus-bound',minimum_gap,flush=True)


if __name__=='__main__':
    parity_check()
    kraus_check()
