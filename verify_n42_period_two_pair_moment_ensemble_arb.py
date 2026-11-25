"""256-bit Arb certificate for a positive N=42 period-two pair-moment ensemble."""
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
from flint import arb, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_pair_moment_atoms.json"
OUTPUT = ROOT / "evidence/n42_period_two_pair_moment_ensemble_arb.json"

def rational(value):
    q = Fraction(value)
    return arb(fmpq(q.numerator, q.denominator))

def build_tables(n):
    two_pi = 2 * arb.pi()
    cosine, sine = [], []
    for k in range(n):
        row_c, row_s = [], []
        for d in range(n):
            angle = two_pi * (k * d) / n
            row_c.append(angle.cos())
            row_s.append(angle.sin())
        cosine.append(row_c)
        sine.append(row_s)
    return cosine, sine

def build_atom(atom, n, cosine, sine):
    a, b = rational(atom["a"]), rational(atom["b"])
    if not (a > 0 and b > 0):
        raise AssertionError("all frozen cycle couplings must be strictly positive")
    c_symbol, sinc_symbol = [], []
    for k in range(n):
        ck, sk = cosine[k][1], sine[k][1]
        mu_sq = 4 * (a*a + b*b - 2*a*b*ck)
        if not (mu_sq > 0):
            raise AssertionError(f"nonpositive Fourier singular value at mode {k}")
        mu = mu_sq.sqrt()
        cm, sm = mu.cos(), mu.sin()
        if not (cm*cm + sm*sm).contains(1):
            raise AssertionError("Fourier-mode trigonometric identity failed")
        c_symbol.append(cm)
        sinc_symbol.append(sm / mu)
    C, S = [], []
    for d in range(n):
        cd, sd = arb(0), arb(0)
        for k in range(n):
            co, si = cosine[k][d], sine[k][d]
            cd += c_symbol[k] * co
            sd += 2 * sinc_symbol[k] * (
                (a - b*cosine[k][1]) * co + b*sine[k][1] * si
            )
        C.append(cd / n)
        S.append(sd / n)
    x = C[0]
    same = [x*x - C[d]*C[d] for d in range(1, n//2 + 1)]
    cross = [-x*x - S[d]*S[d] for d in range(n)]
    features = same + cross
    row_norm = x*x + 2*sum((C[d]*C[d] for d in range(1, n//2 + 1)), arb(0))
    row_norm += sum((S[d]*S[d] for d in range(n)), arb(0))
    if not (row_norm - 1).contains(0):
        raise AssertionError("period-two Fourier blocks failed the row-norm identity")
    identity = 2*sum(same, arb(0)) + sum(cross, arb(0))
    if not (identity + 1).contains(0):
        raise AssertionError("pair-feature linear identity failed")
    return {"a":a,"b":b,"C":C,"S":S,"features":features}

def q_entry(i, j, C, S, n):
    if i%2==0 and j%2==0:
        return C[(j//2-i//2)%n]
    if i%2==1 and j%2==1:
        return -C[(j//2-i//2)%n]
    if i%2==0 and j%2==1:
        return -S[(j//2-i//2)%n]
    return -S[(i//2-j//2)%n]

def pair_feature_index(i, j, n):
    if i%2 == j%2:
        p,q=i//2,j//2
        d=(q-p)%n
        d=min(d,n-d)
        if not (1<=d<=n//2):
            raise AssertionError("invalid same-parity pair displacement")
        return d-1
    even=i if i%2==0 else j
    odd=j if i%2==0 else i
    p,q=even//2,odd//2
    return n//2+(q-p)%n

def verify():
    data=json.loads(INPUT.read_text())
    n,N=data["n"],data["N"]
    ctx.prec=data["precision_bits"]
    assert (n,N)==(21,42)
    atoms=data["atoms"]
    m=len(atoms)
    assert m==31
    assert len({(x["a"],x["b"]) for x in atoms})==m
    cosine,sine=build_tables(n)
    built=[build_atom(atom,n,cosine,sine) for atom in atoms]
    columns=[item["features"] for item in built]
    target=rational("-1/41")
    floor=rational(data["weight_floor"])
    selected=list(range(10))+list(range(10,30))
    A=arb_mat([[columns[j][i] for j in range(m)] for i in selected]+[[arb(1) for _ in range(m)]])
    rhs=arb_mat([[target] for _ in selected]+[[arb(1)]])
    determinant=A.det()
    if determinant.contains(0):
        raise AssertionError("the frozen 31x31 pair-moment matrix is not certified invertible")
    weights=A.solve(rhs)
    if not all(weights[j,0]>floor for j in range(m)):
        raise AssertionError("strict positive weight floor was not certified")
    weight_sum=sum((weights[j,0] for j in range(m)),arb(0))
    if not weight_sum.contains(1):
        raise AssertionError("weights do not sum to one")
    residual=A*weights-rhs
    if not all(residual[i,0].contains(0) for i in range(m)):
        raise AssertionError("selected pair-moment equations failed")
    averaged=[]
    for i in range(len(columns[0])):
        averaged.append(sum((weights[j,0]*columns[j][i] for j in range(m)),arb(0)))
        if not (averaged[-1]-target).contains(0):
            raise AssertionError(f"pair-feature coordinate {i} misses the target")
    pair_count=0
    for i,j in combinations(range(N),2):
        feature=pair_feature_index(i,j,n)
        if not (averaged[feature]-target).contains(0):
            raise AssertionError(f"pair ({i},{j}) misses the target")
        pair_count+=1
    assert pair_count==comb(N,2)==861
    witness=[0,1,2,3]
    fourth_moment=arb(0)
    for j,item in enumerate(built):
        Q4=arb_mat([[q_entry(i,k,item["C"],item["S"],n) for k in witness] for i in witness])
        fourth_moment+=weights[j,0]*Q4.det()
    fourth_target=rational(Fraction(comb(n,2),comb(N,4)))
    fourth_residual=fourth_moment-fourth_target
    if not (fourth_residual>rational("1/200")):
        raise AssertionError("the selected fourth-order mismatch was not certified above 1/200")
    min_index=min(range(m),key=lambda j:float(weights[j,0]))
    max_index=max(range(m),key=lambda j:float(weights[j,0]))
    result={
      "status":"certified_positive_N42_period_two_pair_moment_ensemble","complete":True,
      "N":N,"family":"c_(2j)=a, c_(2j+1)=b with all a,b>0",
      "atom_count":m,"all_42_couplings_strictly_positive":True,"precision_bits":ctx.prec,
      "weight_floor_exact":data["weight_floor"],"moment_matrix_determinant":str(determinant),
      "minimum_weight":str(weights[min_index,0]),"minimum_weight_atom_index":min_index,
      "maximum_weight":str(weights[max_index,0]),"weight_sum":str(weight_sum),
      "weights":[str(weights[j,0]) for j in range(m)],
      "selected_pair_equations":30,"omitted_cross_displacement":20,
      "omitted_equation_identity":"2*sum_{d=1}^{10}(x^2-C_d^2)+sum_{d=0}^{20}(-x^2-S_d^2)=-1",
      "all_unordered_pair_coordinates_certified":pair_count,
      "Q_pair_target":"-1/41","R_pair_target":"(-1)^(i+j+1)/41",
      "fourth_order_witness":witness,"fourth_order_target":str(fourth_target),
      "fourth_order_moment":str(fourth_moment),"fourth_order_residual":str(fourth_residual),
      "scope":"Exact positive ensemble for all N=42 second-order principal-minor coordinates only. The displayed fourth-order witness is rigorously mismatched; this is not a full even-moment design.",
      "discovery":data["discovery"]
    }
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"atom_count":m,
      "determinant":result["moment_matrix_determinant"],"minimum_weight":result["minimum_weight"],
      "weight_floor":result["weight_floor_exact"],"pair_coordinates":pair_count,
      "fourth_order_residual":result["fourth_order_residual"],
      "output":str(OUTPUT.relative_to(ROOT))},indent=2),flush=True)

if __name__=="__main__":
    verify()
