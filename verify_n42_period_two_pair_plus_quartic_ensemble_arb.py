"""256-bit Arb certificate for N=42 period-two pair plus selected quartic moments."""
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
from flint import arb, arb_mat, fmpq, ctx

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/"evidence/n42_period_two_pair_plus_quartic_atoms.json"
OUTPUT=ROOT/"evidence/n42_period_two_pair_plus_quartic_ensemble_arb.json"

def rational(value):
    q=Fraction(value)
    return arb(fmpq(q.numerator,q.denominator))

def build_tables(n):
    two_pi=2*arb.pi()
    cosine,sine=[],[]
    for k in range(n):
        rc,rs=[],[]
        for d in range(n):
            angle=two_pi*(k*d)/n
            rc.append(angle.cos());rs.append(angle.sin())
        cosine.append(rc);sine.append(rs)
    return cosine,sine

def build_atom(atom,n,cosine,sine):
    a,b=rational(atom["a"]),rational(atom["b"])
    if not (a>0 and b>0):
        raise AssertionError("all cycle couplings must be strictly positive")
    c_symbol,sinc_symbol=[],[]
    for k in range(n):
        ck,sk=cosine[k][1],sine[k][1]
        mu_sq=4*(a*a+b*b-2*a*b*ck)
        if not (mu_sq>0):
            raise AssertionError(f"nonpositive Fourier singular value at mode {k}")
        mu=mu_sq.sqrt()
        cm,sm=mu.cos(),mu.sin()
        if not (cm*cm+sm*sm).contains(1):
            raise AssertionError("Fourier-mode trigonometric identity failed")
        c_symbol.append(cm);sinc_symbol.append(sm/mu)
    C,S=[],[]
    for d in range(n):
        cd,sd=arb(0),arb(0)
        for k in range(n):
            co,si=cosine[k][d],sine[k][d]
            cd+=c_symbol[k]*co
            sd+=2*sinc_symbol[k]*(
                (a-b*cosine[k][1])*co+b*sine[k][1]*si
            )
        C.append(cd/n);S.append(sd/n)
    x=C[0]
    same=[x*x-C[d]*C[d] for d in range(1,n//2+1)]
    cross=[-x*x-S[d]*S[d] for d in range(n)]
    features=same+cross
    row_norm=x*x+2*sum((C[d]*C[d] for d in range(1,n//2+1)),arb(0))
    row_norm+=sum((S[d]*S[d] for d in range(n)),arb(0))
    if not (row_norm-1).contains(0):
        raise AssertionError("row-norm identity failed")
    identity=2*sum(same,arb(0))+sum(cross,arb(0))
    if not (identity+1).contains(0):
        raise AssertionError("pair-feature identity failed")
    return {"C":C,"S":S,"features":features}

def q_entry(i,j,C,S,n):
    if i%2==0 and j%2==0:return C[(j//2-i//2)%n]
    if i%2==1 and j%2==1:return -C[(j//2-i//2)%n]
    if i%2==0 and j%2==1:return -S[(j//2-i//2)%n]
    return -S[(i//2-j//2)%n]

def pair_feature_index(i,j,n):
    if i%2==j%2:
        d=(j//2-i//2)%n
        d=min(d,n-d)
        if not (1<=d<=n//2):raise AssertionError("bad same-parity displacement")
        return d-1
    even=i if i%2==0 else j
    odd=j if i%2==0 else i
    return n//2+((odd//2-even//2)%n)

def quartic_moment(indices,built,weights,n):
    total=arb(0)
    for j,item in enumerate(built):
        M=arb_mat([[q_entry(i,k,item["C"],item["S"],n) for k in indices] for i in indices])
        total+=weights[j,0]*M.det()
    return total

def verify():
    data=json.loads(INPUT.read_text())
    n,N=data["n"],data["N"]
    ctx.prec=data["precision_bits"]
    assert (n,N)==(21,42)
    atoms=data["atoms"];m=len(atoms)
    assert m==35 and len({(a["a"],a["b"]) for a in atoms})==m
    cosine,sine=build_tables(n)
    built=[build_atom(atom,n,cosine,sine) for atom in atoms]
    columns=[item["features"] for item in built]
    pair_target=rational("-1/41")
    quartic_target=rational(Fraction(comb(n,2),comb(N,4)))
    selected=list(range(30))
    matched=[list(map(int,I)) for I in data["matched_quartic_witnesses"]]
    assert len(matched)==4
    matrix_rows=[[columns[j][i] for j in range(m)] for i in selected]
    for I in matched:
        matrix_rows.append([
            arb_mat([[q_entry(i,k,built[j]["C"],built[j]["S"],n) for k in I] for i in I]).det()
            for j in range(m)
        ])
    matrix_rows.append([arb(1) for _ in range(m)])
    A=arb_mat(matrix_rows)
    rhs=arb_mat([[pair_target] for _ in selected]+[[quartic_target] for _ in matched]+[[arb(1)]])
    determinant=A.det()
    if determinant.contains(0):
        raise AssertionError("35x35 pair-plus-quartic matrix is not certified invertible")
    weights=A.solve(rhs)
    floor=rational(data["weight_floor"])
    if not all(weights[j,0]>floor for j in range(m)):
        raise AssertionError("strict positive weight floor was not certified")
    weight_sum=sum((weights[j,0] for j in range(m)),arb(0))
    if not weight_sum.contains(1):
        raise AssertionError("weights do not sum to one")
    residual=A*weights-rhs
    if not all(residual[i,0].contains(0) for i in range(m)):
        raise AssertionError("selected linear equations failed")

    averaged=[]
    for i in range(len(columns[0])):
        avg=sum((weights[j,0]*columns[j][i] for j in range(m)),arb(0))
        if not (avg-pair_target).contains(0):
            raise AssertionError(f"pair feature {i} misses target")
        averaged.append(avg)
    pair_count=0
    for i,j in combinations(range(N),2):
        feature=pair_feature_index(i,j,n)
        if not (averaged[feature]-pair_target).contains(0):
            raise AssertionError(f"pair ({i},{j}) misses target")
        pair_count+=1
    assert pair_count==comb(N,2)==861

    # Directly certify all 21 even translations of each of the four quartets.
    translated_checks=0
    matched_records=[]
    for I in matched:
        vals=[]
        for shift in range(n):
            J=sorted((i+2*shift)%N for i in I)
            value=quartic_moment(J,built,weights,n)
            if not (value-quartic_target).contains(0):
                raise AssertionError(f"matched quartic translate {J} misses target")
            vals.append(value)
            translated_checks+=1
        matched_records.append({"representative":I,"translation_count":n,
                                "first_translate_moment":str(vals[0]),
                                "last_translate_moment":str(vals[-1])})
    assert translated_checks==84

    mismatch=list(map(int,data["mismatched_quartic_witness"]))
    mismatch_value=quartic_moment(mismatch,built,weights,n)
    mismatch_residual=mismatch_value-quartic_target
    if not (mismatch_residual>rational("1/400")):
        raise AssertionError("unmatched quartic witness was not separated by >1/400")

    min_index=min(range(m),key=lambda j:float(weights[j,0]))
    max_index=max(range(m),key=lambda j:float(weights[j,0]))
    result={
      "status":"certified_N42_period_two_pair_plus_four_quartic_orbits",
      "complete":True,"N":N,"atom_count":m,
      "all_42_couplings_strictly_positive":True,"precision_bits":ctx.prec,
      "moment_matrix_determinant":str(determinant),
      "weight_floor_exact":data["weight_floor"],
      "minimum_weight":str(weights[min_index,0]),"minimum_weight_atom_index":min_index,
      "maximum_weight":str(weights[max_index,0]),"weight_sum":str(weight_sum),
      "weights":[str(weights[j,0]) for j in range(m)],
      "pair_target_Q":"-1/41","all_unordered_pair_coordinates_certified":pair_count,
      "quartic_target":str(quartic_target),
      "matched_quartic_orbits":matched_records,
      "matched_quartic_translation_checks":translated_checks,
      "mismatched_quartic_witness":mismatch,
      "mismatched_quartic_moment":str(mismatch_value),
      "mismatched_quartic_residual":str(mismatch_residual),
      "scope":"Exact positive ensemble for every pair coordinate and four specified fourth-order translation orbits only. It is not a full fourth-order or all-even-moment design.",
      "discovery":data["discovery"]
    }
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"atoms":m,
      "determinant":result["moment_matrix_determinant"],
      "minimum_weight":result["minimum_weight"],"weight_floor":result["weight_floor_exact"],
      "pair_coordinates":pair_count,"matched_quartic_translates":translated_checks,
      "unmatched_quartic_residual":result["mismatched_quartic_residual"]},indent=2),flush=True)

if __name__=="__main__":
    verify()
