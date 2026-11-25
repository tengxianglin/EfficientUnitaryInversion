# Exact N=8 obstruction for a single alternating-coupling cycle exponential

## Theorem

Consider the 8-cycle generator
[
A(c)_{j,j+1}=2c_j,qquad A(c)_{j+1,j}=-2c_j
]
with cyclic indices and alternating real couplings
[
c_0=c_2=c_4=c_6=a,qquad
c_1=c_3=c_5=c_7=b.
]
Let (R=e^{A(c)}), (D=operatorname{diag}(1,-1,ldots,1,-1)), and (Q=RD).

**There are no real (a,b) for which every two-site principal minor of (Q) equals the balanced-slice target (-1/7).** In particular, no single alternating-coupling physical cycle exponential at (N=8) can realize the complete balanced-slice even-principal-minor hierarchy.

This theorem concerns one physical atom with period-two couplings. It does not exclude a positive mixture of alternating-coupling atoms, non-period-two couplings, or the full cycle-family convex hull.

## Proof

Order even vertices before odd vertices. Then
[
A=egin{pmatrix}0&B\-B^T&0end{pmatrix},
qquad B=2(aI-bT),
]
where (T) is the 4-cycle shift. Thus (B) is real normal and circulant, so (BB^T=B^TB). Define
[
C=cossqrt{BB^T},qquad
S=B,rac{sinsqrt{B^TB}}{sqrt{B^TB}}.
]
Both (C) and (S) are real circulant, (C) is symmetric, and
[
Q=egin{pmatrix}C&-S\-S^T&-Cend{pmatrix},
qquad C^2+SS^T=I.
]

Assume for contradiction that all order-two target minors equal (-1/7). Let (x=C_{00}). Translation invariance gives the same diagonal (x) in both parity blocks. For an even-even pair at cyclic parity-block displacement (d=1,2,3),
[
x^2-C_{0d}^2=-rac17.
]
Since (C) is symmetric circulant, its first row must therefore be
[
(x, arepsilon c, f c, arepsilon c),
qquad
c^2=x^2+ho,quad ho=rac17,quad
arepsilon,fin{-1,1}.
]
For an even-odd pair at displacement (d=0,1,2,3), the principal minor is (-x^2-S_{0d}^2). Hence every entry of (S) has the same magnitude (s), with
[
s^2=ho-x^2.
]
Put (z=x^2), so (0le zleho). Since (S) is circulant, (S=sF) for a circulant sign matrix (F) with first row ((g,h,i,j)in{-1,1}^4), provided (s>0).

The case (s=0) is impossible: then (C^2=I), while the displacement-two entry of (C^2) is (2xc f+2c^2). Its vanishing forces (xf=-c), hence (z=c^2=z+ho), a contradiction. Thus (s>0).

Write
[
R_1=rac12(FF^T)_{01}
=rac{(g+i)(h+j)}2,
qquad
R_2=rac12(FF^T)_{02}=gi+hj.
]
Direct enumeration of the 16 sign rows gives exactly
[
(R_1,R_2)in
{(2,2),(-2,2),(0,0),(0,-2)}.
]

Now use the off-diagonal entries at displacements one and two of (C^2+SS^T=I):
[
xc\varepsilon+c^2\varepsilon f+s^2R_1=0,
qquad
xcf+c^2+s^2R_2=0.
]
Multiplying the first equation by (arepsilon), the second by (f), and subtracting yields
[
arepsilon R_1=fR_2.
]
This rules out ((R_1,R_2)=(0,-2)), so necessarily (R_2in{0,2}).

Multiplying the second equation by (f), substituting (c^2=z+ho) and (s^2=ho-z), and squaring gives
[
z(z+ho)=igl(z+ho+(ho-z)R_2igr)^2.
]
If (R_2=0), this reduces to (z(z+ho)=(z+ho)^2), impossible because (ho>0). If (R_2=2), it gives
[
z(z+ho)=(3ho-z)^2
quadLongrightarrowquad
z=rac{9ho}{7}=rac9{49}>ho=rac17,
]
contradicting (s^2=ho-zge0). Both cases are impossible. Therefore no such (a,b) exist. (square)

## Interpretation

This is stronger than the rank-one spectral-collapse obstruction: it allows arbitrary real alternating couplings and makes no assumption that the nonuniform singular frequencies are odd multiples of (pi). The obstruction already appears in the complete order-two target.

It is still only a **single-atom, period-two** no-go. Convex mixtures can average different displacement-dependent minors, and general non-period-two cycle couplings do not have the circulant block structure used here. The (N=42) physical convex-hull problem in Issue #7 remains open.

## Exact reproducibility

- Verifier: `verify_n8_alternating_cycle_second_order_no_go.py`
- Evidence: `evidence/n8_alternating_cycle_second_order_no_go.json`
- Workflow: `.github/workflows/eui-n8-alternating-cycle-second-order-no-go.yml`

The verifier exhausts all 16 sign rows of (F), checks the exact correlation-pair set, and verifies the two remaining rational/algebraic cases.
