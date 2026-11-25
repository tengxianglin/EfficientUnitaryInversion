# Exact N=42 no-go for a single period-two cycle atom

Date: 2026-11-26.

## Main theorem

Let \(N=42=2n\), \(n=21\), and let the cycle-supported real skew generator be
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with cyclic indices. Put
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\qquad
R=e^{A(c)},\qquad Q=RD.
\]
The balanced-slice target in \(Q\)-coordinates has pair moments
\[
\tau_{\{i,j\}}=-\frac1{41}\qquad(i\ne j).
\]

**Theorem.** There are no real \(a,b\) such that the period-two couplings
\[
c_{2j}=a,\qquad c_{2j+1}=b,\qquad j=0,\ldots,20,
\]
produce a single physical atom \(Q=e^{A(c)}D\) satisfying
\[
\det Q_{\{i,j\},\{i,j\}}=-\frac1{41}
\quad\text{for every pair }i\ne j.
\]
Consequently, no single period-two physical atom can realize the complete balanced-slice even-principal-minor hierarchy. The proof already uses only its second-order coordinates.

This is a **single-atom** theorem. It does not exclude positive mixtures of period-two atoms, nor ensembles with non-period-two cycle couplings.

## Geometric meaning of the target

Because the cycle is even, \(DAD=-A\). Hence
\[
Q=e^A D=e^{A/2}D e^{-A/2}.
\]
Thus \(Q\) is a symmetric orthogonal involution with 21 eigenvalues \(+1\) and 21 eigenvalues \(-1\). Equivalently,
\[
P=\frac{I+Q}{2}
\]
is a rank-21 real orthogonal projector, a point of the real Grassmannian
\(\mathrm{Gr}_{\mathbb R}(21,42)\).

The target is exactly the Haar-Grassmannian average of these principal-minor observables. Indeed, for Haar \(O\in O(42)\), let \(Q_{\rm H}=ODO^T\). Orthogonal invariance makes
\(\mathbb E\det (Q_{\rm H})_{I,I}\) depend only on \(|I|=k\). On the other hand,
\[
\det(I+tQ_{\rm H})=(1+t)^{21}(1-t)^{21}=(1-t^2)^{21},
\]
so the sum of all order-\(2r\) principal minors is \((-1)^r\binom{21}{r}\). Dividing by \(\binom{42}{2r}\) gives
\[
\boxed{\mathbb E_{\rm Haar}\det (Q_{\rm H})_{I,I}
=(-1)^r\frac{\binom{21}{r}}{\binom{42}{2r}},
\qquad |I|=2r.}
\]
The physical family is the restricted orbit \(P=e^{A(c)/2}P_0e^{-A(c)/2}\), where \(P_0=(I+D)/2\) and \(A(c)\) is constrained to the 42 cycle edges. The convex-hull question is therefore a Grassmannian cubature problem with a highly restricted one-exponential support.

## Proof of the period-two no-go

### 1. Parity-block form

Order the even vertices before the odd vertices. For period-two couplings,
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},
\qquad B=2(aI-bT),
\]
where \(T\) is the 21-cycle shift. The matrix \(B\) is real normal and circulant. Define
\[
C=\cos\sqrt{BB^T},\qquad
S=B\,\frac{\sin\sqrt{B^TB}}{\sqrt{B^TB}},
\]
with the quotient interpreted by continuity at zero. Then \(C\) is symmetric circulant, \(S\) is circulant, and
\[
R=e^A=\begin{pmatrix}C&S\\-S^T&C\end{pmatrix},
\qquad
Q=RD=\begin{pmatrix}C&-S\\-S^T&-C\end{pmatrix},
\qquad C^2+SS^T=I.
\]

Let \(x=C_{00}\) and \(\rho=1/41\). Every even-even pair minor gives
\[
x^2-C_{0d}^2=-\rho\quad(d\ne0),
\]
so
\[
C=xI+cF,\qquad c^2=x^2+\rho,
\]
where \(F\) is a symmetric circulant sign matrix with zero diagonal and every off-diagonal entry in \(\{\pm1\}\). Every even-odd pair minor gives
\[
-x^2-S_{0d}^2=-\rho\quad(d=0,\ldots,20),
\]
so
\[
S=sG,\qquad s^2=\rho-x^2,
\]
where \(G\) is a circulant sign matrix (all entries \(\pm1\)). In particular \(0\le x^2\le\rho\).

If \(s=0\), then \(S=0\), \(C^2=I\), and the diagonal of \(C^2=I\) gives \(x^2=\rho\). Since \(C\) is a symmetric involution, \(\operatorname{tr}C\) is an integer, whereas
\[
\operatorname{tr}C=21x=\pm\frac{21}{\sqrt{41}}
\]
is irrational. Thus \(s>0\).

### 2. Fourier phase compatibility reduces the sign patterns

Let \(\zeta=e^{2\pi i/21}\), and use the Fourier convention
\[
\widehat g(k)=\sum_{j=0}^{20}g_j\zeta^{jk},\qquad
\widehat B(k)=2(a-b\zeta^k).
\]
The exponential formula gives
\[
\widehat S(k)=\widehat B(k)
\frac{\sin|\widehat B(k)|}{|\widehat B(k)|},
\]
where the scalar factor is real. Since \(S=sG\),
\[
\widehat G(k)\overline{\widehat B(k)}
=\overline{\widehat G(k)}\widehat B(k).
\]
Fourier inversion yields the exact integer equations
\[
a\,u_j-b\,v_j=0,\qquad
u_j=g_j-g_{-j},\qquad
v_j=g_{j+1}-g_{1-j}.
\]

The entries of \(u,v\) belong to \(\{0,\pm2\}\). An exact enumeration of all \(2^{21}=2,097,152\) sign rows gives:

| Phase pattern | Count |
|---|---:|
| \(u=v=0\) | 2 |
| \(u=0\), \(v\ne0\) | 2,046 |
| \(v=0\), \(u\ne0\) | 2,046 |
| \(u=-v\ne0\) | 2,046 |
| \(u=v\ne0\) | 0 |
| all other nonproportional cases | 2,091,012 |

The \(u=0\ne v\) branch forces \(b=0\), and \(v=0\ne u\) forces \(a=0\). Either makes \(S\) a scalar multiple of \(I\) or of \(T\), contradicting the fact that every entry of \(S=sG\) is nonzero. If \(u=v=0\), then \(g_{j+1}=g_{j-1}\); because 21 is odd, \(g\) is constant. The only nonconstant branch left is \(u=-v\ne0\), which forces \(b=-a\). Thus it remains to check the constant-\(G\) branch and the \(b=-a\) branch.

### 3. Exact exhaustion of the orthogonality equations

Set
\[
X=\frac{x^2}{\rho}\in[0,1],\qquad
Y=\frac{xc}{\rho},\qquad
Y^2=X(X+1).
\]
For each nonzero cyclic displacement \(d=1,\ldots,10\), the off-diagonal equation in \(C^2+SS^T=I\) becomes
\[
A_dX+B_dY+C_d=0,
\]
where the integer coefficients are
\[
A_d=(F^2-GG^T)_{0d},\qquad
B_d=2F_{0d},\qquad
C_d=(F^2+GG^T)_{0d}.
\]
There are exactly \(2^{10}=1,024\) possible symmetric circulant sign matrices \(F\). The verifier uses integer arithmetic only, solves the resulting linear systems exactly, and then imposes both \(0\le X\le1\) and \(Y^2=X(X+1)\).

**Constant-\(G\) branch.** Here \(G=\pm J\), so \(GG^T=21J\). Across all 1,024 \(F\)-patterns, the only consistent rank-one systems reduce to
\[
-2X\pm2Y+40=0,
\]
which is impossible because \(0\le X\le1\) and \(|Y|\le\sqrt2<3/2\). The rank-two systems yield no point satisfying the range and quadratic constraint.

**Nonconstant branch \(b=-a\).** There are 2,046 admissible \(G\)-patterns, hence 2,095,104 \((F,G)\)-pairs. The exact enumeration gives:

| Exact linear-system class | Count |
|---|---:|
| rank-two inconsistent | 2,086,892 |
| rank-two consistent but failing range/quadratic constraint | 4,096 |
| rank-two satisfying all constraints | 24 |
| rank-one inconsistent | 4,088 |
| rank-one consistent | 4 |

The four consistent rank-one systems reduce to
\[
2X\pm2Y+36=0,
\]
again impossible since \(|Y|<3/2\). All 24 rank-two feasible systems have exactly
\[
X=Y=0.
\]
Consequently every remaining candidate sign pattern forces
\[
x=0,\qquad c=s=\frac1{\sqrt{41}}.
\]

The complete enumeration, including all 24 surviving mask pairs and all rank-one residual equations, is reproduced by the exact verifier.

### 4. Gelfond–Schneider contradiction

Now assume \(b=-a\ne0\). The Fourier symbol is
\[
\widehat B(k)=2a(1+\zeta^k).
\]
At \(k=0\), \(\widehat B(0)=4a\), so
\[
e^{i4a}=\widehat C(0)+i\widehat S(0)
=\frac{f_{\rm sum}+ig_{\rm sum}}{\sqrt{41}},
\]
where \(f_{\rm sum}\) is the sum of the 21 entries in the first row of \(F\), and \(g_{\rm sum}\) is the sum of the 21 entries in the first row of \(G\). Hence \(f_{\rm sum}\) is even, \(g_{\rm sum}\) is odd, and
\[
f_{\rm sum}^2+g_{\rm sum}^2=41.
\]
The only possibilities are \(f_{\rm sum}=\pm4\), \(g_{\rm sum}=\pm5\). Therefore
\[
\alpha:=e^{i4a}=\frac{\pm4\pm5i}{\sqrt{41}}
\]
is algebraic and \(\alpha\ne0,1\).

Put \(\beta=\cos(\pi/21)\). It is algebraic and irrational: \(2\beta=\xi+\xi^{-1}\), with \(\xi=e^{i\pi/21}\) a 42nd root of unity, is an algebraic integer strictly between 1 and 2, hence is not rational. At Fourier mode \(k=1\),
\[
\widehat B(1)=4a\beta e^{i\pi/21},
\]
and therefore
\[
e^{i4a\beta}
=\widehat C(1)+i e^{-i\pi/21}\widehat S(1).
\]
The right-hand side is algebraic: \(\widehat C(1)=\widehat F(1)/\sqrt{41}\) and \(\widehat S(1)=\widehat G(1)/\sqrt{41}\), with \(\widehat F(1),\widehat G(1)\) cyclotomic algebraic numbers. Thus one value of \(\alpha^\beta\), using the logarithm \(\log\alpha=i4a\), would be algebraic.

This contradicts the **Gelfond–Schneider theorem**: if \(\alpha\) is algebraic with \(\alpha\notin\{0,1\}\), and \(\beta\) is algebraic irrational, every value of \(\alpha^\beta\) is transcendental. The contradiction proves the theorem.

## Reproducibility

- Exact verifier: verify_n42_period_two_single_atom_no_go.py.
- Machine-readable evidence: evidence/n42_period_two_single_atom_no_go.json.
- CI workflow: .github/workflows/eui-n42-period-two-single-atom-no-go.yml.
- The verifier exhausts all 2,097,152 Fourier-phase sign rows, all 1,024 symmetric \(F\)-patterns, and all 2,095,104 nonconstant \((F,G)\)-pairs in the \(b=-a\) branch. All matrix correlations, determinants, and rational constraints are exact integers/rationals; no floating-point optimization is used.

Classical transcendence references:
- A. O. Gelfond, “Sur le septième problème de D. Hilbert,” *C. R. Acad. Sci. URSS* **2** (1934), 1–6.
- T. Schneider, “Transzendenzuntersuchungen periodischer Funktionen. I. Transzendenz von Potenzen,” *J. Reine Angew. Math.* **172** (1934), 65–69.

## Scope and next question

**Proved:** no single period-two 42-cycle exponential matches even the complete second-order balanced-slice target.

**Not proved:** no positive mixture of period-two atoms; no impossibility for general non-periodic 42-cycle couplings; no global physical-family convex-hull separator; and no Choi/diamond operational bound.

The next useful test is the convex hull of the period-two family, not another single-atom search. Any such mixture must average the displacement-resolved pair-minor functions to the constant \(-1/41\); a valid exclusion must therefore be a linear inequality holding for every \((a,b)\), not an extrapolation from this single-atom theorem.


## Literature positioning (checked 2026-11-26)

This result should be positioned as a **restricted-support obstruction**, not as a new general Grassmannian-design theorem.

1. Ehler and Gräf study polynomial spaces, cubatures, and \(t\)-designs on real Grassmannians, including orthogonally invariant Haar measures and analytic low-degree design families (*Constructive Approximation* 49, 29–58 (2019), [DOI 10.1007/s00365-018-9443-5](https://doi.org/10.1007/s00365-018-9443-5)). This is the natural general mathematical setting for the Haar target identified above.
2. Wan et al., “Matchgate Shadows for Fermionic Quantum Simulation,” prove that the first three moments of Haar-random matchgate circuits agree with a discrete Clifford-matchgate ensemble (*Communications in Mathematical Physics* 404, 629–700 (2023), [DOI 10.1007/s00220-023-04844-0](https://doi.org/10.1007/s00220-023-04844-0)). Their ensemble uses the full continuous matchgate group and a discrete subgroup; it does not address the one-exponential, fixed-cycle-edge support \(e^{A(c)}\) studied here, nor the present all-even-principal-minor target.
3. Boccato, Pieroni, and Trevisan relate distances between Slater determinant states and their induced determinantal point processes, with trace/total-variation and Wasserstein estimates ([arXiv:2504.08971](https://arxiv.org/abs/2504.08971)). This is potentially relevant to a future classical/quantum distance bridge, but it is not a channel diamond-norm bound for EUI.

The specific gap isolated here is therefore: **can the Haar-Grassmannian principal-minor moment vector be represented by a positive measure supported on the fixed-cycle one-exponential orbit?** The theorem above excludes only a single period-two atom. It does not settle the period-two convex hull, much less the full physical orbit. No broad novelty claim is made from this literature check alone.
