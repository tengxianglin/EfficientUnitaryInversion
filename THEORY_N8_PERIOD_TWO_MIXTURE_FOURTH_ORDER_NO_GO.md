# N=8 no-go for every period-two mixture at fourth order

Date: 2026-11-27. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), [the N=8 single-atom second-order no-go](THEORY_N8_ALTERNATING_CYCLE_SECOND_ORDER_NO_GO.md), and [the N=42 period-two partial ensemble](THEORY_N42_PERIOD_TWO_PAIR_PLUS_QUARTIC_ENSEMBLE.md).

## Theorem

Consider the eight-cycle generator
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with cyclic indices, and restrict to period-two couplings
\[
c_{2j}=a,\qquad c_{2j+1}=b,\qquad a,b\in\mathbb R.
\]
Let \(R=e^{A(c)}\), \(D=\operatorname{diag}(1,-1,\ldots,1,-1)\), and \(Q=RD\). Then **no probability measure supported on this two-parameter period-two family can reproduce the complete balanced-slice even-principal-minor target**.

A quantitative form is stronger. After cyclic symmetrization, let
\[
P=\mathbb E\det Q_{\{0,4\},\{0,4\}},\qquad
K=\mathbb E\det Q_{\{0,1,4,5\},\{0,1,4,5\}}.
\]
For every period-two ensemble,
\[
K\ge |P|.
\]
The balanced-slice target requires
\[
P_*=-\frac17,\qquad K_*=\frac3{35},
\]
which violates this inequality. In fact, for the full second-/fourth-order feature vector \(v\) and target \(\tau\),
\[
\boxed{\|\,\mathbb E v-\tau\,\|_\infty\ge\frac1{35}.}
\]
Equivalently, the two-coordinate dual \(y=-\tfrac12(e_{\{0,4\}}+e_{\{0,1,4,5\}})\) has \(\|y\|_1=1\) and a uniform separation margin at least \(1/35\) on the cyclically symmetrized period-two family.

This excludes arbitrary positive mixtures, not just a single period-two atom. It strengthens the existing N=8 single-atom no-go.

## Fourier reduction and the two exact features

Order the even sites first and the odd sites second. With \(T\) the four-cycle shift,
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},
\qquad B=2(aI-bT).
\]
The four singular frequencies are
\[
\mu_0=2|a-b|,\qquad
\mu_1=\mu_3=2\sqrt{a^2+b^2},\qquad
\mu_2=2|a+b|.
\]
Write \(\omega=2\sqrt{a^2+b^2}\), and let \(C,S\) be the real circulant blocks in
\[
Q=\begin{pmatrix}C&-S\\-S^T&-C\end{pmatrix}.
\]
For the first-row coefficients \(C_0,C_2,S_0,S_2\), Fourier inversion gives
\[
\begin{aligned}
C_0+C_2&=\cos(2a)\cos(2b),\\
C_0-C_2&=\cos\omega,\\
S_0+S_2&=\sin(2a)\cos(2b),\\
S_0-S_2&=\frac{a}{\sqrt{a^2+b^2}}\sin\omega
\end{aligned}
\]
when \(a^2+b^2>0\), with the zero point understood by continuity.

The pair minor is therefore
\[
\boxed{P(a,b)=\det Q_{\{0,4\},\{0,4\}}
=\cos(2a)\cos(2b)\cos\omega.}
\]
The four-site submatrix on \(I=\{0,1,4,5\}\), after applying the two-site Hadamard transform to its even and odd coordinates, splits into two \(2\times2\) blocks. Its determinant is
\[
\begin{aligned}
K(a,b)
&=\big((C_0+C_2)^2+(S_0+S_2)^2\big)
  \big((C_0-C_2)^2+(S_0-S_2)^2\big)\\
&=\boxed{\cos^2(2b)
 \left(\cos^2\omega+\frac{a^2}{a^2+b^2}\sin^2\omega\right).}
\end{aligned}
\]
The formula extends continuously to \(a=b=0\), where \(P=K=1\). These identities are for the repository's \(Q=RD\) convention.

## Cyclic symmetrization and the key inequality

A one-site cyclic shift exchanges \(a\) and \(b\). Averaging each physical atom over its eight cyclic shifts therefore leaves the pair feature equal to \(P(a,b)=P(b,a)\), and replaces the selected quartic feature by
\[
\bar K(a,b)=\frac{K(a,b)+K(b,a)}2.
\]
This symmetrization preserves the balanced-slice target. It also cannot increase the \(\ell_\infty\) distance to that cyclically invariant target.

Set
\[
\alpha=\frac{a^2}{a^2+b^2},\quad
\beta=\frac{b^2}{a^2+b^2},\quad
x=\cos\omega,\quad z=\sin^2\omega,
\quad X=\cos^2(2a),\quad Y=\cos^2(2b).
\]
For \(a^2+b^2>0\), \(\alpha+\beta=1\), and
\[
\bar K=\frac12\left[
Y(x^2+\alpha z)+X(x^2+\beta z)
\right],\qquad
P^2=XYx^2.
\]
The crucial scalar identity is
\[
(x^2+\alpha z)(x^2+\beta z)
=x^2+\alpha\beta z^2\ge x^2.
\]
Arithmetic-geometric mean now gives
\[
\begin{aligned}
\bar K
&\ge \sqrt{XY(x^2+\alpha z)(x^2+\beta z)}\\
&\ge \sqrt{XY}\,|x|
=|P|.
\end{aligned}
\]
The origin follows by continuity. Thus the inequality holds for every real \(a,b\), including zero and negative couplings.

For any probability measure over period-two atoms, average first over the cyclic orbit of each atom. Then
\[
K=\mathbb E\bar K(a,b)
\ge \mathbb E|P(a,b)|
\ge |\mathbb E P(a,b)|
=|P|.
\]
The target values are
\[
P_*=-\frac{\binom41}{\binom82}=-\frac17,
\qquad
K_*=\frac{\binom42}{\binom84}=\frac3{35}.
\]
They would require \(K_*=3/35<1/7=|P_*|\), a contradiction.

For the quantitative residual, if both selected coordinates were within \(\delta\) of target, then
\[
K\le\frac3{35}+\delta,\qquad
|P|\ge\frac17-\delta
\]
whenever \(\delta<1/7\). Since \(K\ge|P|\), this forces
\[
\delta\ge\frac12\left(\frac17-\frac3{35}\right)=\frac1{35}.
\]
For \(\delta\ge1/7\) the same lower bound is immediate. Hence the full feature-vector \(\ell_\infty\) discrepancy is at least \(1/35\).

Equivalently, on the symmetrized two-coordinate feature vector,
\[
y=-\frac12(e_P+e_K),\qquad \|y\|_1=1,
\]
and
\[
y^T(\tau-\mathbb E v)
=\frac12\left(P+K+\frac2{35}\right)\ge\frac1{35}.
\]
For an unsymmetrized ensemble, cyclic averaging is an \(\ell_\infty\)-contraction and fixes \(\tau\), so the same distance lower bound holds.

## Consequence and scope

- The N=8 period-two obstruction is now a **mixture no-go**: no support size, positive reweighting, or continuous probability measure over \((a,b)\) can match the complete even-principal-minor target.
- The proof uses only one pair and one fourth-order principal-minor coordinate. The sixth-order target is complementary to the pair target by Jacobi's identity for the symmetric involution \(Q\), and the full determinant is fixed, so the two selected constraints already suffice.
- This does **not** exclude non-period-two N=8 cycle couplings, nor does it prove a no-go for the full N=42 cycle family. In particular, it does not invalidate the N=42 period-two partial ensemble: that construction matches only four selected quartic orbits and does not constrain the witness \(\{0,1,4,5\}\).
- For the N=42 programme, the result is a methodological warning: extending the period-two construction to all fourth-order orbits cannot work by merely adding more period-two atoms. A full construction must leave the period-two subfamily, or a converse must exploit additional structure of the unrestricted cycle family.

## Reproducibility

- Independent 256-bit Arb formula/matrix regression: verify_n8_period_two_mixture_fourth_order_no_go.py.
- Machine-readable output: evidence/n8_period_two_mixture_fourth_order_no_go.json.
- Hosted verification workflow: .github/workflows/eui-n8-period-two-mixture-fourth-order-no-go.yml.

The analytic inequality above is the proof. The Arb script checks the Fourier-to-minor formulas against direct \(8\times8\) matrix exponentials at frozen exact-rational sample couplings; finite samples are regression evidence, not the continuum argument.
