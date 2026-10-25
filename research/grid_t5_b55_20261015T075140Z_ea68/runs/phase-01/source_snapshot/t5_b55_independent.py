#!/usr/bin/env python3
"""Independent literal-tensor exact verifier for the bounded B55 T5 certificate.

This module deliberately imports no producer, T4, or pro_checks implementation.
Dense JSON matrices use row-major ``{rows,cols,entries:[str(expr),...]}``.
The parser admits only SymPy arithmetic names and never evaluates Python code.
"""
import argparse
import ast
import json
import traceback
from pathlib import Path

import sympy as s

I = s.I
P2 = {
    "I": s.eye(2),
    "X": s.Matrix([[0, 1], [1, 0]]),
    "Y": s.Matrix([[0, -I], [I, 0]]),
    "Z": s.Matrix([[1, 0], [0, -1]]),
}
GRID = [["XII", "ZII", "YII"], ["ZXI", "YIY", "XXY"],
        ["YXI", "XIY", "ZXY"]]
WORDS = [a+b+c for a in "IXYZ" for b in "IXYZ" for c in "IXYZ"]


def ex(x):
    return s.expand(x)


def zero(x):
    return all(ex(t) == 0 for t in x)


def must(ok, label, failures, detail=None):
    if not ok:
        failures.append({"label": label, "detail": detail})


def same(a, b, label, failures):
    if a.shape != b.shape:
        must(False, label, failures, {"actual_shape": a.shape, "expected_shape": b.shape})
        return
    d = a-b
    if not zero(d):
        for k, v in enumerate(d):
            if ex(v) != 0:
                must(False, label, failures, {"row": k//d.cols, "col": k%d.cols,
                                              "residual": str(ex(v))})
                break


def expr(node):
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return s.Integer(node.value)
    if isinstance(node, ast.Name) and node.id == "I":
        return I
    if isinstance(node, ast.Name) and node.id == "x":
        return s.Symbol("x")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -expr(node.operand)
    if isinstance(node, ast.BinOp):
        a, b = expr(node.left), expr(node.right)
        if isinstance(node.op, ast.Add): return a+b
        if isinstance(node.op, ast.Sub): return a-b
        if isinstance(node.op, ast.Mult): return a*b
        if isinstance(node.op, ast.Div): return a/b
        if isinstance(node.op, ast.Pow) and b.is_Integer and abs(b) <= 8: return a**b
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        args = [expr(a) for a in node.args]
        if node.keywords: raise ValueError("keyword expression")
        if node.func.id == "sqrt" and len(args) == 1: return s.sqrt(args[0])
        if node.func.id == "Rational" and len(args) == 2: return s.Rational(*args)
        if node.func.id == "Integer" and len(args) == 1: return s.Integer(args[0])
        if node.func.id == "Mul": return s.Mul(*args)
        if node.func.id == "Add": return s.Add(*args)
        if node.func.id == "Pow" and len(args) == 2: return args[0]**args[1]
    raise ValueError("unsupported exact expression: " + ast.dump(node))


def number(st):
    if type(st) is int: return s.Integer(st)
    if not isinstance(st, str) or len(st) > 512: raise ValueError("invalid scalar")
    return expr(ast.parse(st, mode="eval").body)


def matrix(obj):
    if not isinstance(obj, dict) or set(obj) != {"rows", "cols", "entries"}:
        raise ValueError("invalid dense matrix schema")
    r, c = obj["rows"], obj["cols"]
    if type(r) is not int or type(c) is not int or r*c != len(obj["entries"]) or r*c > 4096:
        raise ValueError("invalid dense matrix dimensions")
    return s.Matrix(r, c, [number(t) for t in obj["entries"]])


def pauli(word):
    if len(word) != 3 or any(q not in P2 for q in word): raise ValueError(word)
    return s.kronecker_product(*(P2[q] for q in word))


def kron(*a):
    return s.kronecker_product(*a)


def vec(m):
    return s.Matrix(list(m))


def basis_from_json(group):
    out = []
    for v in group["echelon_basis"]:
        out.append(sum((number(c)*pauli(WORDS[int(k)]) for k,c in v.items()), s.zeros(8)))
    return out


def coords(target, basis, failures, label):
    mat = s.Matrix.hstack(*[vec(x) for x in basis])
    try:
        sol, params = mat.gauss_jordan_solve(vec(target))
        must(params.rows == 0, label+" unique", failures)
        return [ex(z) for z in sol]
    except ValueError:
        must(False, label+" membership", failures)
        return None


def gram_basis(m00):
    vectors = []
    for k in range(8):
        v = m00[:, k]
        for u in vectors: v -= u*(u.conjugate().T*v)[0]
        if zero(v): continue
        norm2 = ex((v.conjugate().T*v)[0])
        v = v/s.sqrt(norm2)
        lead = next(z for z in v if ex(z) != 0)
        v *= s.conjugate(lead)/s.sqrt(ex(s.conjugate(lead)*lead))
        vectors.append(v.applyfunc(ex))
        if len(vectors) == 3: break
    return vectors


def candidate_matrix(container, key, expected, failures, prefix):
    must(key in container, prefix+" missing "+key, failures)
    if key in container: same(matrix(container[key]), expected, prefix+" "+key, failures)


def sparse_matrix(obj):
    if not isinstance(obj,dict):raise ValueError("invalid Pauli map")
    out=s.zeros(8)
    for word,value in obj.items():out+=number(value)*pauli(word)
    return out


def candidate_sparse(container,key,expected,failures,prefix):
    must(key in container,prefix+" missing "+key,failures)
    if key in container:same(sparse_matrix(container[key]),expected,prefix+" "+key,failures)


def compare_coords(container,name,actual,failures,prefix):
    must(name in container,prefix+" missing coords "+name,failures)
    if name not in container:return
    must(set(container[name])==set(actual),prefix+" coords spaces "+name,failures)
    for space,vec0 in actual.items():
        if space in container[name] and vec0 is not None:
            must([ex(number(z)-v)==0 for z,v in zip(container[name][space],vec0)]==[True]*len(vec0)
                 and len(container[name][space])==len(vec0),
                 prefix+" coords "+name+" "+space,failures)


def check_phase(phase, failures):
    h = s.diag(-3, 1, 1, 1); one = s.eye(4)
    pm = s.diag(1,0,0,0); pp = one-pm
    def f(x): return s.trace(pm*x)*pp+s.trace(pp*x)*pm/3
    b = s.zeros(4, 64)
    e = s.zeros(64,4)
    for q in range(4):
        for a in range(4):
            for r in range(4):
                for t in range(4):
                    x = s.zeros(4); x[a,r] = 1
                    b[q, a*16+r*4+t] = f(x)[q,t]
    for t in range(4):
        for r in range(4): e[r*16+r*4+t,t] = s.Rational(1,2)
    k = b/s.sqrt(s.Rational(10,3))
    same(e.conjugate().T*e, one, "phase E isometry", failures)
    same(b*b.conjugate().T,s.diag(s.Rational(1,3),1,1,1),"phase BBdagger",failures)
    must(all(ex(z)>=0 for z in (s.Rational(10,3)*one-b*b.conjugate().T).diagonal()),
         "phase B contraction", failures)
    for a in range(4):
        for r in range(4):
            x=s.zeros(4);x[a,r]=1
            same(k*kron(x,s.eye(16))*e, f(x)/(2*s.sqrt(s.Rational(10,3))),
                 f"phase composition {a},{r}", failures)
    must(s.Matrix.hstack(vec(one),vec(h)).rank()==2 and
         s.Matrix.hstack(vec(one),vec(h),vec(h*h)).rank()==2,
         "phase unshifted intersection",failures)
    g=h+one
    must(zero(g*g-4*one) and s.Matrix.hstack(vec(one),vec(g)).rank()==2,
         "phase centred disjoint",failures)
    same(f(pm),pp,"phase spectral minus",failures)
    same(f(pp),pm,"phase spectral plus",failures)
    g=h+one
    for key, value in {"H":h,"G":g,"P_minus":pm,"P_plus":pp,"B":b,"E0":e,"K":k,
                       "BBdagger":b*b.conjugate().T,
                       "dropped_phase_derivative_defect":f(h)+h}.items():
        candidate_matrix(phase,key,value,failures,"phase")
    must(number(phase.get("kappa_squared","0"))==s.Rational(10,3),"phase kappa",failures)
    must(number(phase.get("probability","0"))==s.Rational(3,40),"phase probability",failures)
    expect_f=[]
    for o in range(4):
        for i in range(4):
            for a in range(4):
                for bb in range(4):
                    x=s.zeros(4);x[a,bb]=1
                    z=f(x)[o,i]
                    if z!=0:expect_f.append((o,i,a,bb,z))
    got_f={(int(o),int(i),int(a),int(bb)):number(v) for o,i,a,bb,v in phase.get("f_nonzero",[])}
    must(len(got_f)==len(expect_f) and all(got_f.get((o,i,a,bb))==z for o,i,a,bb,z in expect_f),
         "phase tensor f",failures)
    for key in ("lhs","rhs_exp_2it_Udagger"):
        container=phase.get("spectral_frequency_identity",{}).get(key,{})
        candidate_matrix(container,"3",pp,failures,"phase spectral "+key)
        candidate_matrix(container,"-1",pm,failures,"phase spectral "+key)
    must(all(phase.get("checks",{}).values()) and len(phase.get("checks",{}))>=6,
         "phase producer checks",failures)
    must(phase.get("schema")=="t5-phase-v1","phase schema",failures)
    must(phase.get("ranks")=={"unshifted_even":2,"unshifted_odd":2,
          "unshifted_combined":2,"shifted_even":1,"shifted_odd":1,"shifted_combined":2},
         "phase ranks",failures)
    units=phase.get("matrix_units",[])
    must(len(units)==16,"phase emitted matrix units",failures)
    for u in units:
        a0,b0=u["a"],u["b"]
        xx=s.zeros(4);xx[a0,b0]=1
        same(matrix(u["actual"]),k*kron(xx,s.eye(16))*e,
             f"phase emitted actual {a0},{b0}",failures)
        same(matrix(u["expected"]),f(xx)/(2*s.sqrt(s.Rational(10,3))),
             f"phase emitted expected {a0},{b0}",failures)


def run(args, failures, results):
    root = Path(args.evidence_root)
    source = {f:json.loads((root/"results"/"T4_final"/("B55q0_"+f+".json")).read_text())
              for f in ("row","column","uniform")}
    grid = [w for row in GRID for w in row]
    for f,d in source.items():
        must(d["grid"]==GRID,"saved grid "+f,failures)
        expected_c = [[int((k//3 if f=="row" else k%3 if f=="column" else 0)==j)
                       for j in range(3 if f!="uniform" else 1)] for k in range(9)]
        must(d["C"]==expected_c,"saved binding "+f,failures)
    p={w:pauli(w) for w in set(grid+["IXI","IIY","YIX","III"])}
    must(zero(P2["X"]*P2["Y"]-I*P2["Z"]) and
         zero(P2["Y"]*P2["Z"]-I*P2["X"]) and
         zero(P2["Z"]*P2["X"]-I*P2["Y"]),"Pauli convention",failures)
    one=s.eye(8); h0=sum((p[w] for w in grid),s.zeros(8))
    w=(p["XII"]-p["YIY"])/s.sqrt(2); q=p["YIX"]
    same(w*w,one,"uniform W square",failures);same(w,w.conjugate().T,"uniform W Hermitian",failures)
    same(w*h0+h0*w,s.zeros(8),"uniform anticommutator",failures)
    for word in grid: same(q*p[word]*q,-p[word].conjugate(),"Q0 "+word,failures)
    must(not zero(w*sum((p[grid[k]] for k in range(3)),s.zeros(8))+
                  sum((p[grid[k]] for k in range(3)),s.zeros(8))*w),"row W negative control",failures)
    must(not zero(w*sum((p[grid[k]] for k in (0,3,6)),s.zeros(8))+
                  sum((p[grid[k]] for k in (0,3,6)),s.zeros(8))*w),"column W negative control",failures)
    x=s.Symbol("x")
    must(s.expand(h0.charpoly(x).as_expr()-(x*x-27)*(x*x-3)**3)==0,"uniform characteristic polynomial",failures)
    candidate=json.loads((Path(args.candidate)/"certificate.json").read_text())
    results["candidate_schema"]=candidate.get("schema")
    must(candidate.get("schema")=="t5-sparse-v1","candidate schema",failures)
    must(candidate.get("grid")==GRID,"candidate grid",failures)
    for key,value in {"H0":h0,"W":w,"Q0":q}.items():
        candidate_sparse(candidate.get("uniform",{}),key,value,failures,"uniform")
        candidate_matrix(candidate.get("uniform",{}),key+"_dense",value,failures,"uniform")
    must(ex(number(candidate.get("uniform",{}).get("characteristic_polynomial","0"))-
            (x*x-27)*(x*x-3)**3)==0,"candidate charpoly",failures)
    must(candidate.get("uniform",{}).get("multiplicities")=={"-3*sqrt(3)":1,"-sqrt(3)":3,
          "sqrt(3)":3,"3*sqrt(3)":1},"candidate multiplicities",failures)
    must(candidate.get("uniform",{}).get("operations_time_order")=={
         "dagger":["W","U","W"],"star":["Q0","U","Q0"],
         "transpose":["Q0","W","U","W","Q0"]},"candidate operation sequence",failures)
    r=p["IXI"]; t=p["IIY"]
    projectors={(a,b):(one+a*r)*(one+b*t)/4 for a in (1,-1) for b in (1,-1)}
    pc=one-projectors[(1,1)]
    for ab,value in projectors.items():
        candidate_sparse(candidate.get("projectors",{}),f"{ab[0]:+d},{ab[1]:+d}",value,failures,"projector")
    candidate_sparse(candidate,"Pi0",projectors[(1,1)],failures,"candidate")
    candidate_sparse(candidate,"Pic",pc,failures,"candidate")
    for (a,b),v in projectors.items():
        same(v*v,v,f"projector square {a},{b}",failures)
        same(v,v.conjugate().T,f"projector Hermitian {a},{b}",failures)
        same(v.T,projectors[(a,-b)],f"projector transpose {a},{b}",failures)
        must(s.trace(v)==2,f"projector rank {a},{b}",failures)
        for (c,d),u in projectors.items():
            if (a,b)!=(c,d):same(v*u,s.zeros(8),f"projector orthogonality {a},{b} {c},{d}",failures)
    same(sum(projectors.values(),s.zeros(8)),one,"projector sum",failures)
    must(s.trace(pc)==6,"corner rank",failures)
    a0=s.Matrix([[1,-1,-1],[1,-1,1],[1,1,-1]])
    for f in ("row","column"):
        d=source[f]
        hs=[sum((number(d["C"][k][j])*p[grid[k]] for k in range(9)),s.zeros(8)) for j in range(3)]
        fc=candidate.get("families",{}).get(f,{})
        must(fc.get("C")==d["C"],f+" candidate C",failures)
        must(len(fc.get("H",[]))==3,f+" candidate H count",failures)
        for k,hj in enumerate(hs):
            if k<len(fc.get("H",[])):same(sparse_matrix(fc["H"][k]),hj,f+f" H{k}",failures)
        first=hs[0]
        controls=candidate.get("negative_W_generator_controls",{}).get(f,{})
        candidate_sparse(controls,"first_generator",first,failures,f+" negative W")
        candidate_sparse(controls,"anticommutator",w*first+first*w,failures,f+" negative W")
        a_by_sector={}
        for ab,v in projectors.items():
            entries=[]
            for axis in ("XII","YII","ZII"):
                entries.append([ex(s.trace(v*p[axis]*hj)/2) for hj in hs])
            aa=s.Matrix(entries);a_by_sector[ab]=aa
            candidate_matrix(fc.get("A",{}),f"{ab[0]:+d},{ab[1]:+d}",aa,failures,f+" A")
            must(all(z.is_real for z in aa),f+" A real "+str(ab),failures)
            if ab!=(1,1):
                same(aa.T*aa,4*s.eye(3)-s.ones(3),f+" A Gram "+str(ab),failures)
                must(aa.det()==-4,f+" A det "+str(ab),failures)
                rot=aa*a0.inv();same(rot.T*rot,s.eye(3),f+" rotation "+str(ab),failures)
                must(rot.det()==1,f+" rotation orientation "+str(ab),failures)
                candidate_matrix(fc.get("rotations",{}),f"{ab[0]:+d},{ab[1]:+d}",rot,failures,f+" rotation")
        same(a_by_sector[(1,1)],s.ones(3),f+" A++",failures)
        same(a_by_sector[(1,-1)],a0,f+" A0",failures)
        candidate_matrix(fc,"A0_inverse",a0.inv(),failures,f)
        bb=[sum((a0.inv()[j,k]*pc*hs[j] for j in range(3)),s.zeros(8)) for k in range(3)]
        bx,by,bz=bb
        for name,value in zip("xyz",bb):candidate_sparse(fc.get("B",{}),name,value,failures,f+" B")
        for k,v in enumerate(bb):same(v,v.conjugate().T,f+" B Hermitian {k}",failures)
        for k in range(3):
            for l in range(3):
                eps=sum((s.LeviCivita(k,l,m)*bb[m] for m in range(3)),s.zeros(8))
                same(bb[k]*bb[l],int(k==l)*pc+I*eps,f+f" B product {k},{l}",failures)
        mm={"M00":(pc+bz)/2,"M11":(pc-bz)/2,
            "M01":(bx+I*by)/2,"M10":(bx-I*by)/2}
        for name,value in mm.items():candidate_sparse(fc.get("M",{}),name[1:],value,failures,f+" M")
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        same(mm[f"M{i}{j}"]*mm[f"M{k}{l}"],
                             (mm[f"M{i}{l}"] if j==k else s.zeros(8)),f+f" units {i}{j}{k}{l}",failures)
        must(s.trace(mm["M00"])==s.trace(mm["M11"])==3,f+" unit ranks",failures)
        vs=gram_basis(mm["M00"])
        must(len(vs)==3,f+" Gram Schmidt",failures)
        if len(vs)!=3:continue
        jmat=s.Matrix.hstack(*(vs+[bx*v for v in vs]))
        candidate_matrix(fc,"J",jmat,failures,f)
        candidate_matrix(fc,"transpose_naive_residual",pc.T-pc,failures,f)
        candidate_matrix(fc,"full_oracle_at_zero_defect",one-pc,failures,f)
        same(jmat.conjugate().T*jmat,s.eye(6),f+" J isometry",failures)
        same(jmat*jmat.conjugate().T,pc,f+" J range",failures)
        for a in range(2):
            for b in range(2):
                eij=s.zeros(2);eij[a,b]=1
                same(jmat*kron(eij,s.eye(3))*jmat.conjugate().T,mm[f"M{a}{b}"],f+f" J unit {a}{b}",failures)
                corner=jmat*kron(eij,s.eye(3))*jmat.conjugate().T
                same(corner.T,jmat.conjugate()*kron(eij.T,s.eye(3))*jmat.T,
                     f+f" transpose unit {a}{b}",failures)
        must(not zero(pc.T-pc),f+" naive transpose negative control",failures)
        must(not zero(one-pc),f+" corner replacement negative control",failures)
        full=basis_from_json(d["full"]); even=basis_from_json(d["even"]); odd=basis_from_json(d["odd"])
        for space,basis in (("full",full),("even",even),("odd",odd)):
            must(fc.get("saved_basis_pointers",{}).get(space)==d[space]["independent_coefficient_rows"],
                 f+" pointers "+space,failures)
            saved=fc.get("saved_basis",{}).get(space,[])
            must(len(saved)==len(basis),f+" basis length "+space,failures)
            for k,val in enumerate(basis):
                if k<len(saved):same(sparse_matrix(saved[k]),val,f+f" basis {space}{k}",failures)
        must(len(full)==6 and len(even)==2 and len(odd)==4,f+" saved dimensions",failures)
        must(s.Matrix.hstack(*[vec(z) for z in even+odd]).rank()==6,f+" parity independent",failures)
        witnesses={"Pi0":projectors[(1,1)],"Pic":pc,
                   "Pi0_sumXYZ":projectors[(1,1)]*(p["XII"]+p["YII"]+p["ZII"]),
                   "Bx":bx,"By":by,"Bz":bz,**mm}
        coordinates={}
        for name,value in witnesses.items():
            coordinates[name]={"full":coords(value,full,failures,f+" {name} full")}
            parity="even" if name in ("Pi0","Pic") else "odd" if name in ("Pi0_sumXYZ","Bx","By","Bz") else None
            if parity:coordinates[name][parity]=coords(value,even if parity=="even" else odd,failures,f+" {name} {parity}")
            candidate_sparse(fc.get("named",{}),name,value,failures,f+" named")
            compare_coords(fc.get("coordinates",{}),name,coordinates[name],failures,f)
        for name,value in mm.items():
            if name in ("M00","M11"):
                ve=pc/2;vo=(bz/2 if name=="M00" else -bz/2)
            else:ve=s.zeros(8);vo=value
            parity=fc.get("unit_parity_coordinates",{}).get(name[1:],{})
            for space,target,basis in (("even",ve,even),("odd",vo,odd)):
                actual=coords(target,basis,failures,f+" unit parity "+name+space)
                must(space in parity and actual is not None and len(parity[space])==len(actual) and
                     all(ex(number(z)-v)==0 for z,v in zip(parity[space],actual)),
                     f+" unit parity coordinates "+name+space,failures)
        sigma=[one,p["XII"],p["YII"],p["ZII"]]
        elcu=s.Matrix.vstack(*[z/2 for z in sigma])
        klcu=s.Matrix.hstack(*[sgn*z/2 for sgn,z in zip((-1,1,1,1),sigma)])
        same(elcu.conjugate().T*elcu,one,f+" LCU E isometry",failures)
        same(klcu*klcu.conjugate().T,one,f+" LCU K contraction",failures)
        candidate_matrix(fc.get("LCU",{}),"E",elcu,failures,f+" LCU")
        candidate_matrix(fc.get("LCU",{}),"K",klcu,failures,f+" LCU")
        for space,basis,sgn in (("even",even,1),("odd",odd,-1)):
            for idx,value in enumerate(basis):
                actual=klcu*kron(s.eye(4),value)*elcu
                same(actual,sgn*value/2,f+f" LCU parity {space}{idx}",failures)
                candidate_matrix(fc.get("LCU",{}).get("basis_contractions",{}),
                                 f"{space}_{idx}",actual,failures,f+" LCU basis")
        must(fc.get("ranks")=={"full":6,"even":2,"odd":4,"combined":6,"intersection":0},
             f+" ranks",failures)
        results[f]={"A":{str(k):[[str(z) for z in row] for row in a_by_sector[k].tolist()] for k in a_by_sector},
                    "coordinates":{n:{g:([str(z) for z in c] if c else None) for g,c in v.items()} for n,v in coordinates.items()}}
    phase_path=Path(args.phase) if args.phase else Path(args.candidate).parent/"T5_phase"/"certificate.json"
    if phase_path.is_dir():phase_path/= "certificate.json"
    must(phase_path.exists(),"phase certificate present",failures,str(phase_path))
    if phase_path.exists():check_phase(json.loads(phase_path.read_text()),failures)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence-root",required=True)
    ap.add_argument("--candidate",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--phase")
    args=ap.parse_args()
    out=Path(args.output)
    out.mkdir(parents=True,exist_ok=False)
    failures=[];results={}
    try:run(args,failures,results)
    except Exception as e:
        failures.append({"label":"verifier exception","detail":str(e),"traceback":traceback.format_exc()})
    (out/"verification.json").write_text(json.dumps({"status":"PASS" if not failures else "FAIL",
        "failures":failures,"results":results},indent=2)+"\n")
    if failures:raise SystemExit(1)


if __name__=="__main__":main()
