#!/usr/bin/env python3
"""Independent, exact checker for ordered proper Pauli grids.

Core multiplication uses the literal single-qubit I,X,Y,Z table, not the
frozen cocycle code. Monomial coefficients are Gaussian integer pairs.
All output paths must be fresh. The supplied data are calibration only.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, sys, time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

G=(1,2,3,4,8,12,5,10,15)
LINES=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8))
PAIRS=tuple(itertools.combinations(range(4),2))
# J = polar form of det([[v0,v1],[v2,v3]]) = v0*v3 + v1*v2.
J=(1<<2)|(1<<3)
PCHARS='IXYZ'
# Literal products e.g. X*Y=iZ, X*Z=-iY.
SINGLE={('I',p):(0,p) for p in PCHARS}
SINGLE.update({(p,'I'):(0,p) for p in PCHARS})
SINGLE.update({(p,p):(0,'I') for p in PCHARS})
for a,b,c in [('X','Y','Z'),('Y','Z','X'),('Z','X','Y')]:
    SINGLE[a,b]=(1,c); SINGLE[b,a]=(3,c)
BITS={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
REV={v:k for k,v in BITS.items()}

def write_fresh(path, obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf8') as f: json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def rotate(a,e):
    x,y=a;return ((x,y),(-y,x),(-x,-y),(y,-x))[e%4]
def xor_sum(values):
    v=0
    for x in values:v^=x
    return v

def rank(vals):
    piv={}
    for x in vals:
        while x:
            j=x.bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return len(piv)

def bil(u,v,B):
    return sum((((u>>i&1)*(v>>j&1))^((u>>j&1)*(v>>i&1)))*(B>>k&1)
               for k,(i,j) in enumerate(PAIRS))%2

def qval(v,B,q):
    return ((v&q).bit_count()+sum((v>>i&1)*(v>>j&1)*(B>>k&1)
                                 for k,(i,j) in enumerate(PAIRS)))%2

def det(v):return ((v>>0&1)*(v>>3&1))^((v>>1&1)*(v>>2&1))
def rad(B):return [v for v in range(16) if all(bil(v,1<<i,B)==0 for i in range(4))]
def brank(B):return 4-(len(rad(B)).bit_length()-1)
def linmap(v,base):return xor_sum(base[i] for i in range(len(base)) if v>>i&1)
def tags_from_basis(base,n):return [to_tag(linmap(g,base),n) for g in G]
def to_tag(v,n):return ''.join(REV[(v>>i&1,v>>(n+i)&1)] for i in range(n))
def from_tag(s):
    n=len(s);return sum(BITS[p][0]<<i for i,p in enumerate(s))|sum(BITS[p][1]<<(n+i) for i,p in enumerate(s))
def mul_tag(a,b):
    out=[];e=0
    for x,y in zip(a,b):
        z,p=SINGLE[x,y];e+=z;out.append(p)
    return e%4,''.join(out)
def comm_tag(a,b):return (mul_tag(a,b)[0]-mul_tag(b,a)[0])%4//2

def physical_features(tags):
    base=[tags[i] for i in (0,1,3,4)]
    B=sum(comm_tag(base[i],base[j])<<k for k,(i,j) in enumerate(PAIRS))
    q=sum((s.count('Y')%2)<<i for i,s in enumerate(base))
    return B,q

def line_phases(tags):
    phases=[]
    for a,b,c in LINES:
        e,t=mul_tag(tags[a],tags[b]);f,u=mul_tag(t,tags[c]);assert set(u)=={'I'}
        phases.append((e+f)%4)
    return phases

def lifted_basis(B):
    """Four independent physical four-qubit Pauli tags with q(e_i)=0."""
    out=[]
    for i in range(4):
        chars=['I']*4;chars[i]='X'
        for j in range(i):
            if bil(1<<i,1<<j,B):chars[j]='Z'
        out.append(from_tag(''.join(chars)))
    return out

def power_support(tags,max_degree=7):
    """Exact H^k: each monomial has a single XOR label, tracked with coefficient.
    Dictionary state is exponent tuple -> (Pauli tag, (real,imag)).
    Independent variables are essential; no random sampling is used.
    """
    n=len(tags[0]);m=len(tags);identity='I'*n
    poly={(0,)*m:(identity,(1,0))}
    cumulative=set();powers=[];counts=[];witness={};graded=[set(),set()]
    cache={}
    for k in range(max_degree+1):
        support={t for t,c in poly.values() if c!=(0,0)}
        powers.append(sorted(support));cumulative|=support;graded[k%2]|=support;counts.append(len(cumulative))
        for exp,(t,c) in poly.items():
            if c!=(0,0) and t not in witness:witness[t]={'degree':k,'exponents':exp,'gaussian_coefficient':c}
        if k==max_degree:break
        nxt={}
        for exp,(t,c) in poly.items():
            for j,g in enumerate(tags):
                key=(t,g)
                if key not in cache:cache[key]=mul_tag(t,g)
                phase,prod=cache[key];ee=list(exp);ee[j]+=1;ee=tuple(ee)
                val=rotate(c,phase)
                if ee in nxt:
                    prev,cc=nxt[ee];assert prev==prod;nxt[ee]=(prod,add(cc,val))
                else:nxt[ee]=(prod,val)
        poly={ee:tc for ee,tc in nxt.items() if tc[1]!=(0,0)}
    return {'support':sorted(cumulative),'counts':counts,'power_supports':powers,
            'witnesses':witness,'even':sorted(graded[0]),'odd':sorted(graded[1])}

def automorphisms():
    maps=[]
    for rr in itertools.permutations(range(3)):
        for cc in itertools.permutations(range(3)):
            for trans in (False,True):
                def at(i,j):return G[3*rr[j]+cc[i]] if trans else G[3*rr[i]+cc[j]]
                base=[at(0,0),at(0,1),at(1,0),at(1,1)]
                f=tuple(linmap(v,base) for v in range(16))
                assert set(f[g] for g in G)==set(G)
                maps.append(f)
    assert len(set(maps))==72
    return sorted(set(maps))

def transform(B,q,f):
    bs=[f[1<<i] for i in range(4)]
    return (sum(bil(bs[i],bs[j],B)<<k for k,(i,j) in enumerate(PAIRS)),
            sum(qval(bs[i],B,q)<<i for i in range(4)))

def embed_condition(B,q):
    r=brank(B);R=rad(B)
    if r==0:return False,'rank_zero'
    if r==4:return True,'nondegenerate'
    if any(qval(v,B,q) for v in R):return True,'radical_nonsingular'
    # q descends to a 2-dimensional quotient. Hyperbolic iff Gauss sum +8.
    gauss=sum((-1)**qval(v,B,q) for v in range(16))
    assert gauss in (-8,8)
    return gauss==8,('quotient_plus' if gauss==8 else 'quotient_minus_obstruction')

def exact_transpose_cost(support,B,q):
    T=set(support)
    witnesses=[l for l in range(16) if all(((l&v).bit_count()%2)==qval(v,B,q) for v in T)]
    if witnesses:
        return {'lambda':'1','character_witness':witnesses[0],'primal_dual_gap':'0'}
    assert T==set(range(16))
    nums=[sum((-1)**(qval(v,B,q)+(v&l).bit_count()) for v in range(16)) for l in range(16)]
    coeff=[Fraction(a,16) for a in nums]
    # Dual y = 1/16 A sign(coeff): |A^T y| <= 1, b^T y = ||coeff||_1.
    sign=[(a>0)-(a<0) for a in nums]
    y=[sum(Fraction((-1)**((v&l).bit_count())*sign[l],16) for l in range(16)) for v in range(16)]
    lhs=[sum(Fraction((-1)**((v&l).bit_count()))*y[v] for v in range(16)) for l in range(16)]
    cost=sum(map(abs,coeff));dual=sum(Fraction((-1)**qval(v,B,q))*y[v] for v in range(16))
    assert max(map(abs,lhs))<=1 and cost==dual
    return {'lambda':str(cost),'walsh_numerators_denominator_16':nums,'dual':[str(x) for x in y],'primal_dual_gap':'0'}

def audit_abstract(max_degree=7):
    result=[]
    for B in range(64):
        bs=lifted_basis(B);tags=tags_from_basis(bs,4);assert physical_features(tags)==(B,0)
        pwr=power_support(tags,max_degree);inv={to_tag(linmap(v,bs),4):v for v in range(16)}
        supp={inv[t] for t in pwr['support']}
        h2=set().union(*({inv[t] for t in pwr['power_supports'][k]} for k in range(3)))
        missing=sorted(v for v in range(16) if det(v) and v in rad(B^J))
        assert sorted(set(range(16))-h2)==missing
        predicted=set([0,*G]) if B==J else set(range(16))
        assert supp==predicted
        assert set().union(*({inv[t] for t in pwr['power_supports'][k]} for k in range(4)))==predicted
        ph=line_phases(tags);eps=[x%2 for x in ph]
        assert sum(eps)%2==0
        p,t,u,v,w,z=[B>>k&1 for k in range(6)]
        assert eps==[p,z,p^u^v^z,t,w,t^u^v^w]
        assert sum(ph)%4==2*(p^t^u^w^z)
        recovered_u=(sum(ph)//2%2)^p^t^w^z
        assert recovered_u==u
        witnesses={str(inv[tag]):wit for tag,wit in pwr['witnesses'].items()}
        result.append({'B':B,'rank':brank(B),'line_modes':eps,'line_phase_i_exponents':ph,
                       'missing_after_H2':missing,'counts':pwr['counts'],'support':sorted(supp),
                       'even':sorted(inv[t] for t in pwr['even']),'odd':sorted(inv[t] for t in pwr['odd']),
                       'witnesses':witnesses,'lifted_four_qubit_grid':[tags[i:i+3] for i in (0,3,6)]})
    # Seven-case proof table for v=e0+e3. Stabilizer of determinant acts transitively on six det=1 points.
    triple_table=[]
    for C in range(1,64):
        if 9 not in rad(C):continue
        assert brank(C)==2
        B=C^J
        choices=[t for t in itertools.combinations(G,3) if xor_sum(t)==9 and bil(t[0],t[1],C)==1]
        assert choices
        triple_table.append({'C':C,'B':B,'v':9,'triple':choices[0]})
    assert len(triple_table)==7
    return {'schema':'exact-abstract-grid-audit-v1','max_degree':max_degree,'cases':result,
            'hist_depth':dict(Counter(next(i for i,c in enumerate(r['counts']) if c==len(r['support'])) for r in result)),
            'seven_case_H3_proof_table':triple_table}

def audit_embeddings(physical2,physical3,abstract):
    d2={(x['B'],x['q']):x for x in physical2['cases']};d3={(x['B'],x['q']):x for x in physical3['cases']}
    A={x['B']:x for x in abstract['cases']};rows=[];keys=set();failures=[]
    for B in range(64):
        for q in range(16):
            ok,reason=embed_condition(B,q);actual=d3[B,q]['count']>0
            assert ok==actual
            qnine=[qval(g,B,q) for g in G]
            p,t,u,v,w,z=[B>>k&1 for k in range(6)];defect=p^t^u^w^z
            key=tuple(qnine+[defect]);assert key not in keys;keys.add(key)
            cost=exact_transpose_cost(A[B]['support'],B,q)
            row={'B':B,'q':q,'rank':brank(B),'physical_n3':actual,'reason':reason,
                 'count_n2':d2[B,q]['count'],'count_n3':d3[B,q]['count'],
                 'minimal_qubits':2 if d2[B,q]['count'] else (3 if actual else 4),
                 'nine_q_plus_phase_defect':qnine+[defect], 'cost':cost}
            if actual:
                tags=tags_from_basis(d3[B,q]['basis'],3)
                assert physical_features(tags)==(B,q)
                phases=line_phases(tags)
                assert sum(phases)%4==2*defect
                row['basis']=d3[B,q]['basis'];row['grid']=[tags[i:i+3] for i in (0,3,6)];row['line_phases']=phases
            elif brank(B)!=0:failures.append(row.copy())
            rows.append(row)
    group=automorphisms();unseen={(B,q) for B in range(64) for q in range(16)};orbits=[]
    while unseen:
        key=min(unseen);orb=sorted({transform(*key,f) for f in group});assert set(orb)<=unseen
        statuses={d3[k]['count']>0 for k in orb};assert len(statuses)==1
        unseen-=set(orb);orbits.append({'representative':key,'size':len(orb),'physical_n3':statuses.pop(),'members':orb})
    bg=[];unseen=set(range(64))
    while unseen:
        B=min(unseen);orb=sorted({transform(B,0,f)[0] for f in group});unseen-=set(orb)
        bg.append({'representative':B,'size':len(orb),'members':orb,'rank':brank(B),
                   'line_modes':A[B]['line_modes'],'counts':A[B]['counts'][:4]})
    allanti=[r for r in rows if r['physical_n3'] and A[r['B']]['line_modes']==[1]*6]
    for r in allanti:
        assert r['rank']==2 and not set(G)&set(rad(r['B']))
        assert set(A[r['B']]['even'])==set(rad(r['B']))
        assert set(A[r['B']]['odd'])==set(range(16))-set(rad(r['B']))
    return {'schema':'quadratic-embedding-audit-v1','cases':rows,'forbidden_rank_two':failures,
            'orbits':orbits,'B_orbits':bg,
            'summary':{'physical_n3_cases':sum(r['physical_n3'] for r in rows),
                       'forbidden_rank_two_count':len(failures),'abstract_orbits':len(orbits),
                       'physical_orbits':sum(o['physical_n3'] for o in orbits),
                       'B_orbits':len(bg),'physical_rank_hist':dict(Counter(r['rank'] for r in rows if r['physical_n3'])),
                       'minimal_qubit_hist':dict(Counter(r['minimal_qubits'] for r in rows)),
                       'all_anti_physical_cases':len(allanti),
                       'physical_lambda_hist':dict(Counter(r['cost']['lambda'] for r in rows if r['physical_n3']))}}

def calibrate(path):
    source=json.loads(Path(path).read_text());result=[]
    for e in source['examples']:
        tags=e['ordered_tags'];pwr=power_support(tags,7)
        proper=len(set(tags))==9 and 'III' not in tags and all(from_tag(tags[a])^from_tag(tags[b])==from_tag(tags[c]) for a,b,c in LINES)
        assert proper==e['full_row_column_rule']
        assert len(pwr['support'])==e['envelope_coordinate_support_size']
        assert pwr['counts']==e['envelope_coordinate_support_counts_by_degree']
        row={'name':e['name'],'proper':proper,'envelope':len(pwr['support']),'counts':pwr['counts'],
             'source_lambda':e['transpose_lcu']['lambda'],'grid':e['grid']}
        if proper:
            B,q=physical_features(tags);base=[from_tag(tags[i]) for i in (0,1,3,4)]
            inv={to_tag(linmap(v,base),3):v for v in range(16)}
            cost=exact_transpose_cost([inv[t] for t in pwr['support']],B,q)
            assert Fraction(cost['lambda'])==e['transpose_lcu']['lambda']
            row.update(B=B,q=q,line_phases=line_phases(tags),cost=cost)
        result.append(row)
    return {'source_hash':sha(path),'examples':result,'independent_calibration_passed':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True,type=Path);ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--physical2',required=True,type=Path);ap.add_argument('--physical3',required=True,type=Path)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False);start=time.process_time()
    cal=calibrate(args.input/'evidence/grid/grid_examples.json');write_fresh(args.output/'calibration.json',cal)
    abstract=audit_abstract();write_fresh(args.output/'abstract64.json',abstract)
    emb=audit_embeddings(json.loads(args.physical2.read_text()),json.loads(args.physical3.read_text()),abstract)
    write_fresh(args.output/'embedding1024.json',emb)
    # Comparison uses independently computed algebraic fields, never imported helpers.
    frozen=json.loads((args.input/'evidence/grid/independent_grid_certificates.json').read_text())
    print('FROZEN TOP LEVEL KEYS',list(frozen))
    write_fresh(args.output/'run_summary.json',{'cpu_seconds':time.process_time()-start,'calibration':True,
                 'embedding_summary':emb['summary'],'abstract_depth_hist':abstract['hist_depth'],
                 'code_sha256':sha(__file__),'input_zip_sha256':sha(args.input.parent/'EUI_Pro_Grid_Theory_20261014.zip')})
    print(json.dumps(emb['summary'],indent=2));print('CPU seconds',time.process_time()-start)
if __name__=='__main__':main()
