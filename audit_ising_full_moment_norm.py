"""Numerical norm audit: all moment rows versus an exact-feasibility reduction."""
import argparse
import json
import numpy as np
from batch_ising_moment_pricing import prefix,ROOT,fingerprint
from verify_batch_moment_pricing import approximate_primal


def audit(cache):
    s,cs,W,direction=prefix(cache)
    baseline=approximate_primal(s,W,full=True)
    d=json.loads((ROOT/'evidence/batch_fourth_pricing_n21.json').read_text())
    for r in d['records']:
        col=s.features(list(map(float,r['couplings'])))
        assert fingerprint(col)==r['feature_sha256_le_f64']
        if r['accepted']:W=np.r_[W,[col]]
    final=approximate_primal(s,W,full=True)
    return {'base_commit':d['base_commit'],'status':'Floating all-row minimax LPs; no interval or global physical certificate.',
        'baseline_columns':1609,'final_columns':len(W),'feature_count':1461,
        'scaling':{'second':41,'fourth':533},'baseline_full_norm':baseline,'final_full_norm':final}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);a=p.parse_args()
    print(json.dumps(audit(a.cache),indent=2))
