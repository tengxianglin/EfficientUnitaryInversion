"""Local physical escape from a certified finite-pool tradeoff functional."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from ising_sixth_pricing import SixthPricing
from verify_full_low_moment_certificate import inputs,ROOT


def discover(output):
    raw=(ROOT/'evidence/fixed_pool_tradeoff_n21.json').read_bytes();data=json.loads(raw);f=SixthPricing(data)
    _,cs,_,_,_,_=inputs();rng=np.random.default_rng(202611212242)
    check=np.r_[rng.normal(size=41)*.3,0];value,g=f.value_gradient(check);errors=[]
    for j in (0,20,40):
        d=np.zeros(42);d[j]=1e-5
        fd=(f.value_gradient(check+d,False)-f.value_gradient(check-d,False))/2e-5
        errors.append(abs(fd-g[j]))
    assert max(errors)<1e-4
    result={'base_commit':'2c458d8d9cb27f1e1c904970f1417606e1949dd8',
        'functional_source_sha256':hashlib.sha256(raw).hexdigest(),'rng_seed':202611212242,
        'parent_column':1614,'max_iterations':100,'finite_gradient_defect':max(errors),'candidates':[],'run_complete':False}
    starts=[cs[1614,:-1],cs[1614,:-1]+rng.normal(size=41)*.2]
    for j,start in enumerate(starts):
        def loss(z):
            v,g=f.value_gradient(np.r_[z,0]);return -v,-g
        r=minimize(loss,start,jac=True,method='L-BFGS-B',options={'maxiter':100,'ftol':1e-12,'gtol':1e-8})
        c=np.r_[np.round(r.x,9),0];assert all(c[:-1]!=0)
        score=f.value_gradient(c,False)
        result['candidates'].append({'start':j,'initial_couplings':list(map(str,start)),
            'iterations':int(r.nit),'message':r.message,'couplings':list(map(str,c)),'score_numerical':score})
        Path(output).write_text(json.dumps(result,indent=2)+'\n');print(j,score,flush=True)
    result['best_candidate']=int(np.argmax([r['score_numerical'] for r in result['candidates']]));result['run_complete']=True
    Path(output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();discover(a.output)
