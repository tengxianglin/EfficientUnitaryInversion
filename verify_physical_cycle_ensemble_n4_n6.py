"""Exact symbolic verification of physical cycle realizations at N=4 and N=6."""
from __future__ import annotations
import itertools, json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/"evidence/physical_cycle_ensemble_n4_n6.json"

def interleave(C,S):
    n=C.rows
    block=C.row_join(-S).col_join((-S).row_join(-C))
    order=[j for k in range(n) for j in (k,n+k)]
    return block.extract(order,order)

def audit(Q):
    N,n=Q.rows,Q.rows//2
    if Q!=Q.T or Q*Q!=sp.eye(N) or sp.trace(Q)!=0:
        raise AssertionError("Q must be a trace-zero symmetric involution")
    if sp.factor(Q.det())!=(-1)**n:
        raise AssertionError("wrong det(Q)")
    D=sp.diag(*[(-1)**i for i in range(N)])
    R=Q*D
    if R.T*R!=sp.eye(N) or sp.factor(R.det())!=1 or D*R*D!=R.T:
        raise AssertionError("R=QD failed SO(N) or chiral checks")
    orders,checked={},0
    for r in range(1,n+1):
        target=sp.Rational((-1)**r*sp.binomial(n,r),sp.binomial(N,2*r))
        values=[sp.factor(Q.extract(I,I).det()) for I in itertools.combinations(range(N),2*r)]
        if any(v!=target for v in values):
            raise AssertionError(f"N={N}, order={2*r}: target mismatch")
        orders[str(2*r)]={"subset_count":len(values),"exact_target":str(target),
                          "distinct_observed_values":sorted({str(v) for v in values})}
        checked+=len(values)
    return {"N":N,"Q_exact_matrix":[[str(v) for v in Q.row(i)] for i in range(N)],
            "symmetric":True,"involution":True,"trace":"0","determinant":str(Q.det()),
            "R_QD_determinant":str(R.det()),"R_QD_orthogonal":True,
            "chiral_identity":"D R D = R^T","even_principal_minor_orders":orders,
            "nonempty_even_subsets_checked":checked}

def build_n4():
    theta=sp.acos(sp.Rational(1,3))
    a,b=(sp.pi+theta)/4,(sp.pi-theta)/4
    if sp.simplify(2*(a-b)-theta)!=0 or sp.simplify(2*(a+b)-sp.pi)!=0:
        raise AssertionError("N=4 singular frequencies mismatch")
    if sp.simplify(sp.cos(theta)-sp.Rational(1,3))!=0 or sp.simplify(sp.sin(theta)-2*sp.sqrt(2)/3)!=0:
        raise AssertionError("N=4 trig identities mismatch")
    B=2*sp.Matrix([[a,-b],[-b,a]])
    u,v=sp.Matrix([1,1])/sp.sqrt(2),sp.Matrix([1,-1])/sp.sqrt(2)
    if any(sp.simplify(x)!=0 for x in B*u-theta*u) or any(sp.simplify(x)!=0 for x in B*v-sp.pi*v):
        raise AssertionError("N=4 singular-mode decomposition failed")
    J=sp.ones(2)
    Q=interleave(-sp.eye(2)+sp.Rational(2,3)*J,sp.sqrt(2)/3*J)
    p={"theta":"arccos(1/3)","c_even":"(pi + theta)/4","c_odd":"(pi - theta)/4",
       "singular_frequencies":["theta","pi"],"C_block":"-I_2 + (2/3) J_2",
       "S_block":"(sqrt(2)/3) J_2","numeric_c_even":str(sp.N(a,18)),
       "numeric_c_odd":str(sp.N(b,18))}
    return Q,p

def build_n6():
    theta=sp.acos(sp.Rational(4,5)); d=theta/2
    a=(3*d+sp.sqrt(3*(sp.pi**2-d**2)))/6; b=a-d
    if sp.simplify(2*(a-b)-theta)!=0 or sp.simplify(a**2+a*b+b**2-sp.pi**2/4)!=0:
        raise AssertionError("N=6 singular frequency identities mismatch")
    if sp.simplify(sp.cos(theta)-sp.Rational(4,5))!=0 or sp.simplify(sp.sin(theta)-sp.Rational(3,5))!=0:
        raise AssertionError("N=6 trig identities mismatch")
    B=2*sp.Matrix([[a,0,-b],[-b,a,0],[0,-b,a]])
    P=sp.ones(3)/3
    spectral=theta**2*P+sp.pi**2*(sp.eye(3)-P)
    if any(sp.simplify(x)!=0 for x in B*B.T-spectral) or any(sp.simplify(x)!=0 for x in B.T*B-spectral):
        raise AssertionError("N=6 parity-block spectral identity failed")
    if any(sp.simplify(x)!=0 for x in B*sp.ones(3)/sp.sqrt(3)-theta*sp.ones(3)/sp.sqrt(3)):
        raise AssertionError("N=6 uniform mode mismatch")
    J=sp.ones(3)
    Q=interleave(-sp.eye(3)+sp.Rational(3,5)*J,sp.Rational(1,5)*J)
    p={"theta":"arccos(4/5)","d":"theta/2",
       "c_even":"(3*d + sqrt(3*(pi^2-d^2)))/6","c_odd":"c_even - d",
       "singular_values":["theta","pi","pi"],"C_block":"-I_3 + (3/5) J_3",
       "S_block":"(1/5) J_3","numeric_c_even":str(sp.N(a,18)),
       "numeric_c_odd":str(sp.N(b,18))}
    return Q,p

def main():
    Q4,p4=build_n4(); Q6,p6=build_n6()
    result={"status":"exact_physical_cycle_balanced_slice_ensembles_N4_N6","complete":True,
      "construction":"For N=4 and N=6, alternating real cycle couplings c_(2j)=a, c_(2j+1)=b produce Q=exp(A(c))D with every even principal minor equal to (-1)^r*C(n,r)/C(2n,2r).",
      "N4":{"parameters":p4,**audit(Q4)},"N6":{"parameters":p6,**audit(Q6)},
      "scope":"These are exact physical constructions for N=4 and N=6 only. They do not establish a construction or a no-go theorem for N=42."}
    if json.loads(EVIDENCE.read_text())!=result:
        raise AssertionError("committed N4/N6 evidence differs from exact symbolic recomputation")
    print(json.dumps({"status":result["status"],
      "N4_orders":result["N4"]["even_principal_minor_orders"],
      "N6_orders":result["N6"]["even_principal_minor_orders"],
      "N4_c":[p4["numeric_c_even"],p4["numeric_c_odd"]],
      "N6_c":[p6["numeric_c_even"],p6["numeric_c_odd"]]},indent=2))

if __name__=="__main__":
    main()
