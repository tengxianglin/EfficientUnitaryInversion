"""Regression gates; independent discovery checker still required in next round."""
from pathlib import Path
import itertools,json,sys
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import grid_check as g
from comb_certificate import certify
from validate_predictions import dense,four_qubit_basis,real_gauge_certificate,spectrum_shift_intersection

@pytest.mark.parametrize('B',range(64))
def test_geometry_phases_and_quadratic_reconstruction(B):
    tags=g.tags_from_basis(g.lifted_basis(B),4)
    ph=g.line_phases(tags);eps=[x%2 for x in ph]
    p,t,u,v,w,z=[B>>k&1 for k in range(6)]
    assert eps==[p,z,p^u^v^z,t,w,t^u^v^w]
    assert sum(eps)%2==0
    assert sum(ph)%4==2*(p^t^u^w^z)
    assert ((sum(ph)//2)%2)^p^t^w^z==u
    for q in range(16):
        for x,y in itertools.product(range(16),repeat=2):
            assert g.qval(x^y,B,q)==g.qval(x,B,q)^g.qval(y,B,q)^g.bil(x,y,B)


def test_quadric_and_missing_pair_span():
    assert set(g.G)=={x for x in range(1,16) if g.det(x)==0}
    maps=g.automorphisms();assert len(maps)==72
    assert {f[9] for f in maps}=={x for x in range(16) if g.det(x)}
    for x in range(16):
        if not g.det(x):continue
        pairs=[(a,b) for a,b in itertools.combinations(g.G,2) if a^b==x]
        assert len(pairs)==3 and g.rank([a for ab in pairs for a in ab])==4


def test_embedding_counts_and_minimal_counterexample():
    assert sum(g.embed_condition(B,q)[0] for B in range(64) for q in range(16))==973
    assert g.embed_condition(1,3)==(False,'quotient_minus_obstruction')
    grid=['YIII','XYII','ZYII','IIZI','IIIZ','IIZZ','YIZI','XYIZ','ZYZZ']
    assert g.physical_features(grid)==(1,3)
    g.line_phases(grid)
    assert g.rank([g.from_tag(grid[i]) for i in (0,1,3,4)])==4


def test_H2_failure_and_repaired_cubic():
    tags=['XII','IXI','XXI','IIX','ZII','ZIX','XIX','ZXI','YXX']
    assert g.physical_features(tags)==(4,0)
    assert g.power_support(tags,3)['counts']==[1,10,15,16]
    rec=json.loads((ROOT/'results/validation/H3_seven_case_coefficients.json').read_text())
    assert len(rec)==7
    assert {r['C'] for r in rec}=={C for C in range(1,64) if 9 in g.rad(C)}
    assert all(abs(r['gaussian_coefficient'][0]) in (2,6) for r in rec)

@pytest.mark.parametrize('B',[55,59])
def test_all_anti_structure(B):
    R=g.rad(B)
    assert g.brank(B)==2 and not (set(g.G)&set(R))
    assert sum(g.embed_condition(B,q)[0] for q in range(16))==15
    pwr=g.power_support(g.tags_from_basis(g.lifted_basis(B),4),7)
    base=g.lifted_basis(B);rev={g.to_tag(g.linmap(v,base),4):v for v in range(16)}
    assert {rev[t] for t in pwr['even']}==set(R)
    assert {rev[t] for t in pwr['odd']}==set(range(16))-set(R)


def test_literal_products_against_kronecker_matrices():
    tags=[''.join(a) for a in itertools.product('IXYZ',repeat=2)]
    for a,b in itertools.product(tags,repeat=2):
        e,t=g.mul_tag(a,b)
        assert np.array_equal(dense(a)@dense(b),(1j)**e*dense(t))


def test_parameter_phase_controls_preserved():
    assert spectrum_shift_intersection([1,-3],'dagger')==[-2]
    assert spectrum_shift_intersection([9,-3,-15],'dagger')==[-6]
    assert spectrum_shift_intersection([7,-5,-3,1],'dagger')==[]

@pytest.mark.parametrize('d,target',[(2,'transpose'),(4,'transpose'),(2,'adjugate2')])
def test_exact_comb(d,target):
    assert certify(d,target)['status']=='exact_integer_certificate'


def test_fresh_output_contract(tmp_path):
    p=tmp_path/'x.json';g.write_fresh(p,{'ok':True})
    with pytest.raises(FileExistsError):g.write_fresh(p,{'ok':False})
    assert json.loads(p.read_text())=={'ok':True}


def test_calibration_controls_not_in_proper_population():
    c=json.loads((ROOT/'results/exact/calibration.json').read_text())
    # Inspect the recorded flags; do not rename custom_S1 to frozen S1.
    if isinstance(c,dict):c=c['cases']
    assert len(c)==8
    names=[r.get('name',r.get('id')) for r in c]
    assert 'custom_S1' in names and 'frozen_S1_control' in names
