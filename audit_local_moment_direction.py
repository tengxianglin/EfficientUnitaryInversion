"""All-feature directional derivative audit at a frozen approximate mixture."""
import argparse
import json
import numpy as np
from scipy.linalg import expm_frechet
from local_ising_moment_step import pool,ROOT


def feature_jvp(s,c,direction):
    N=s.N;ii=np.arange(N);jj=(ii+1)%N
    A=np.zeros((N,N));E=np.zeros_like(A)
    A[ii,jj]=2*c;A[jj,ii]=-2*c
    E[ii,jj]=2*direction;E[jj,ii]=-2*direction
    R,B=expm_frechet(A,E)
    second=[]
    for d in range(1,s.n+1):
        j=(ii+d)%N
        second.append(np.mean(B[ii,ii]*R[j,j]+R[ii,ii]*B[j,j]-B[ii,j]*R[j,ii]-R[ii,j]*B[j,ii]))
    I=s.indices;blocks=R[I[:,:,None],I[:,None,:]];db=B[I[:,:,None],I[:,None,:]]
    val=np.zeros(len(I))
    for u in range(4):
        for v in range(4):
            cof=(-1)**(u+v)*np.linalg.det(np.delete(np.delete(blocks,u,axis=1),v,axis=2))
            val+=cof*db[:,u,v]
    return np.r_[second,np.bincount(s.ids,weights=val,minlength=len(s.keys))/s.counts]


def audit(cache):
    s,cs,W=pool(cache)
    step=json.loads((ROOT/'evidence/local_moment_step_n21.json').read_text())
    saved=json.loads((ROOT/'evidence/full_moment_norm_audit_n21.json').read_text())['final_full_norm']
    p=np.zeros(len(W))
    for item in saved['weights']:p[item['column']]=item['weight']
    scale=np.r_[np.full(21,41),np.full(1440,533)]
    residual=(p@W-s.target)*scale;g=max(abs(residual));dphi=np.zeros(len(s.target));checks=[]
    from ising_moment_pricing import MomentFunctional
    f=MomentFunctional(step['direction'])
    for rec in step['selected']:
        j=rec['column'];assert abs(p[j]-rec['weight'])<1e-12
        _,gradient=f.value_gradient(cs[j]);d=np.r_[p[j]*gradient/step['weighted_gradient_max'],0]
        v=feature_jvp(s,cs[j],d);h=1e-5
        fd=(s.features(cs[j]+h*d)-s.features(cs[j]-h*d))/(2*h)
        defect=float(max(abs(v-fd)));assert defect<1e-5
        dphi+=p[j]*v;checks.append({'column':j,'jvp_finite_difference_defect':defect})
    slopes=np.sign(residual)*dphi*scale
    rows=np.flatnonzero(g-abs(residual)<1e-8)
    fixed=[]
    for radius in step['radii']:
        updated=residual.copy()
        for r in step['candidates']:
            if r['radius']!=radius:continue
            j=r['parent_column'];col=s.features(list(map(float,r['couplings'])))
            updated+=p[j]*(col-W[j])*scale
        fixed.append({'radius':radius,'all_row_residual':float(max(abs(updated))),
                      'change_from_baseline':float(max(abs(updated))-g)})
    return {'fixed_weight_replacements':fixed,'base_commit':step['base_commit'],'baseline_residual':float(g),'jvp_checks':checks,
            'near_active_tolerance':1e-8,'near_active_rows':len(rows),
            'near_active_signed_slope_min':float(min(slopes[rows])),
            'near_active_signed_slope_max':float(max(slopes[rows])),
            'near_active_positive_slopes':int(sum(slopes[rows]>1e-8)),
            'status':'Floating near-active-set diagnostic, not a certified exact directional derivative of the optimized value.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);a=p.parse_args()
    print(json.dumps(audit(a.cache),indent=2))
