"""Arb certificate for a complete n=21 second/fourth-moment ensemble.

No floating feature cache, LP, optimizer, or Taylor model enters the proof.
"""
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
import numpy as np
from flint import arb,arb_mat,ctx
from ising_fourth_moments import FourthMoments,seed_pool
from verify_ising_moment_pricing import ball

ROOT=Path(__file__).parent


def inputs():
    cfg=json.loads((ROOT/'evidence/full_low_moment_certificate_input_n21.json').read_text())
    data={}
    for name,sha in cfg['source_sha256'].items():
        raw=(ROOT/'evidence'/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==sha
        data[name]=json.loads(raw)
    cs=seed_pool();assert hashlib.sha256(cs.astype('<f8').tobytes()).hexdigest()==cfg['pool_couplings_sha256_le_f64']
    extra=[data['directed_fourth_pricing_n21.json']['witness_couplings']]
    extra += [r['witness_couplings'] for r in data['iterated_fourth_pricing_n21.json']['records']]
    extra += [r['couplings'] for r in data['batch_fourth_pricing_n21.json']['records'] if r['accepted']]
    extra += [r['couplings'] for r in data['local_moment_step_n21.json']['candidates']]
    extra += [r['couplings'] for t in data['linearized_moment_step_n21.json']['trials'] for r in t['candidates']]
    cs=np.r_[cs,np.array([[float(x) for x in c] for c in extra])]
    assert cs.shape==(1639,42)
    def distribution(records):
        q={int(r['column']):Fraction.from_float(float(r['weight'])) for r in records}
        assert len(q)==len(records) and all(v>0 for v in q.values())
        assert all(0<=j<len(cs) for j in q)
        total=sum(q.values(),Fraction(0));p={j:w/total for j,w in q.items()}
        assert sum(p.values(),Fraction(0))==1
        return p,total
    old,total_old=distribution(data['local_moment_step_n21.json']['final']['weights'])
    new,total_new=distribution(data['linearized_moment_step_n21.json']['final']['weights'])
    return cfg,cs,old,new,total_old,total_new


def rotation_entries(c):
    c=[Fraction.from_float(float(v)) for v in c]
    assert c[-1]==0 and all(v!=0 for v in c[:-1])
    A=arb_mat(42,42)
    for j in range(41):A[j,j+1]=2*ball(c[j]);A[j+1,j]=-2*ball(c[j])
    R=A.exp();return [[R[i,j] for j in range(42)] for i in range(42)]


def fourth_sum(entries,indices):
    return sum((arb_mat([[entries[int(i)][int(j)] for j in I] for i in I]).det() for I in indices),arb(0))


def all_features(s,entries):
    second=[]
    for d in range(1,22):
        second.append(sum((entries[i][i]*entries[(i+d)%42][(i+d)%42]-entries[i][(i+d)%42]*entries[(i+d)%42][i] for i in range(42)),arb(0))/42)
    fourth=[arb(0) for _ in s.keys]
    for I,j in zip(s.indices,s.ids):
        fourth[int(j)]+=arb_mat([[entries[int(i)][int(k)] for k in I] for i in I]).det()
    return second+[v/int(n) for v,n in zip(fourth,s.counts)]


def verify():
    cfg,cs,old,new,total_old,total_new=inputs();ctx.prec=cfg['precision_bits']
    s=FourthMoments(21);s.exact_target_check()
    assert len(s.indices)==111930 and len(s.keys)==1440 and len(s.target)==1461
    cache={};mixture=[arb(0) for _ in s.target]
    for step,(j,p) in enumerate(sorted(new.items()),1):
        E=rotation_entries(cs[j]);cache[j]=E;features=all_features(s,E);w=ball(p)
        for k,value in enumerate(features):mixture[k]+=w*value
        print(f'Certified complete column {step}/{len(new)} (source {j})',file=sys.stderr,flush=True)
    cap=ball(cfg['new_scaled_residual_upper']);worst=None;where=None;worstvalue=None
    for k,(actual,target) in enumerate(zip(mixture,s.rational_target)):
        value=(actual-ball(target))*(41 if k<21 else 533)
        assert value<cap and value>-cap,(k,value,cap)
        if worst is None or float(abs(value))>worst:
            worst=float(abs(value));where=k;worstvalue=value
    index=cfg['old_lower_feature_index'];assert index>=21
    indices=s.indices[s.ids==index-21];old_feature=arb(0)
    for j,p in sorted(old.items()):
        E=cache[j] if j in cache else rotation_entries(cs[j])
        old_feature+=ball(p)*fourth_sum(E,indices)/len(indices)
    old_residual=(old_feature-ball(s.rational_target[index]))*533
    lower=ball(cfg['old_scaled_residual_lower']);assert abs(old_residual)>lower
    improvement=Fraction(cfg['old_scaled_residual_lower'])-Fraction(cfg['new_scaled_residual_upper'])
    assert improvement==Fraction(353,40000)>0
    return {'base_commit':cfg['base_commit'],'precision_bits':ctx.prec,
        'new_support_size':len(new),'old_support_size':len(old),'quartets_per_column':len(s.indices),
        'certified_second_rows':21,'certified_fourth_rows':1440,
        'new_raw_weight_sum':str(total_new),'old_raw_weight_sum':str(total_old),
        'new_normalized_probability_sum':'1','old_normalized_probability_sum':'1',
        'new_probability_weights':[{'column':j,'probability':str(p)} for j,p in sorted(new.items())],
        'new_strict_all_row_upper':cfg['new_scaled_residual_upper'],
        'largest_midpoint_feature_index':where,'largest_midpoint_scaled_residual':str(worstvalue),
        'old_lower_feature_index':index,'old_lower_orbit_representative':list(s.representatives[index-21]),
        'old_selected_scaled_residual':str(old_residual),'old_strict_max_lower':cfg['old_scaled_residual_lower'],
        'strict_decrease_lower':str(improvement),
        'strict_relative_decrease_lower':str(improvement/Fraction(cfg['old_scaled_residual_lower'])),
        'dihedral_group_order':84,'new_dihedral_atoms_at_most':84*len(new),
        'scope':'Certified physical second/fourth-moment approximation and strict improvement between two specified ensembles; no exact uniform design, optimality, channel-error bound, or global no-go.'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
