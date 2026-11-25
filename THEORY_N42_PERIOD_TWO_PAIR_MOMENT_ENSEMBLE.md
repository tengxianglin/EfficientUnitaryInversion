# Exact positive period-two ensemble for all N=42 pair moments

Date: 2026-11-26.

## Result

Let \(N=42=2n\), \(n=21\), and let the physical cycle generator be
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with cyclic indices. Define
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\quad R(c)=e^{A(c)},\quad Q(c)=R(c)D.
\]

There is an **exact positive probability measure supported on 31 period-two cycle Hamiltonians**, all with strictly positive couplings, such that
\[
\boxed{\mathbb E\det Q(c)_{\{i,j\},\{i,j\}}=-\frac1{41}
\quad\text{for every }0\le i<j<42.}
\]
Equivalently,
\[
\mathbb E\det R(c)_{\{i,j\},\{i,j\}}
=\frac{(-1)^{i+j+1}}{41}.
\]

The weights are not asserted to be rational. They are defined as the unique exact-real solution of a frozen \(31\times31\) linear system. A 256-bit Arb certificate proves that the matrix is invertible, the weights sum to one, and every weight is strictly larger than \(1/2000\).

This result is deliberately limited to **second-order principal-minor moments**. The same certificate also exhibits a fourth-order coordinate that this particular 31-atom ensemble fails by a strictly positive margin. No full even-moment feasibility claim is made.

## Fourier reduction

Take period-two couplings
\[
c_{2j}=a,\qquad c_{2j+1}=b,\qquad j=0,\ldots,20,
\]
with \(a,b>0\). In even/odd ordering,
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},\qquad B=2(aI-bT),
\]
where \(T\) is the 21-cycle shift. For \(\phi_k=2\pi k/21\),
\[
\widehat B_k=2(a-be^{i\phi_k}),\qquad
\mu_k=|\widehat B_k|
=2\sqrt{a^2+b^2-2ab\cos\phi_k}.
\]
The exponential has blocks
\[
R=e^A=\begin{pmatrix}C&S\\-S^T&C\end{pmatrix},
\]
whose circulant Fourier symbols are
\[
\widehat C_k=\cos\mu_k,\qquad
\widehat S_k=\widehat B_k\frac{\sin\mu_k}{\mu_k}.
\]
Let \(C_d,S_d\) denote the first-row coefficients. The inverse Fourier formulas used by the verifier are
\[
C_d=\frac1{21}\sum_{k=0}^{20}\cos\mu_k\cos(d\phi_k),
\]
\[
S_d=\frac2{21}\sum_{k=0}^{20}\frac{\sin\mu_k}{\mu_k}
\left[(a-b\cos\phi_k)\cos(d\phi_k)
+b\sin\phi_k\sin(d\phi_k)\right].
\]
Since \(Q=RD\), in parity-block ordering
\[
Q=\begin{pmatrix}C&-S\\-S^T&-C\end{pmatrix}.
\]

Thus every pair principal minor belongs to one of 31 displacement classes:
\[
m_d(a,b)=x^2-C_d^2,\quad d=1,\ldots,10,\qquad x=C_0,
\]
for same-parity pairs, and
\[
n_d(a,b)=-x^2-S_d^2,\quad d=0,\ldots,20,
\]
for even-odd pairs.

## Why only 30 moment equations are independent

The even row of the orthogonal matrix \(Q\) has norm one:
\[
x^2+2\sum_{d=1}^{10}C_d^2+\sum_{d=0}^{20}S_d^2=1.
\]
Consequently every period-two atom obeys the exact linear identity
\[
\boxed{2\sum_{d=1}^{10}m_d+\sum_{d=0}^{20}n_d=-1.}
\]
The target sets all 31 pair coordinates to \(-1/41\), and its values satisfy the same identity because \(2\cdot10+21=41\). Hence it suffices to impose the ten \(m_d\) equations and any twenty of the twenty-one \(n_d\) equations; the last follows exactly.

## Frozen 31-atom construction

The file evidence/n42_period_two_pair_moment_atoms.json freezes 31 pairs \((a_\ell,b_\ell)\) as exact finite decimals, interpreted as rational numbers. Every pair has \(a_\ell,b_\ell>0\), so every atom uses 42 strictly positive cycle couplings.

Let \(F_\ell\in\mathbb R^{31}\) contain
\[
(m_1,\ldots,m_{10},n_0,\ldots,n_{19},1)
\]
for atom \(\ell\). The exact weights are defined by
\[
\begin{pmatrix}F_1&\cdots&F_{31}\end{pmatrix}w
=\left(-\frac1{41},\ldots,-\frac1{41},1\right)^T.
\]
The verifier evaluates all Fourier sums with Arb balls, forms this matrix, and solves it with Arb interval linear algebra. It requires:
- the determinant interval to exclude zero;
- every weight interval to lie strictly above \(1/2000\);
- the weight sum interval to contain exactly one;
- all selected equations to have residual intervals containing zero;
- the omitted \(n_{20}\) equation to follow from the row-norm identity;
- all 861 unordered pairs in the original site indexing to meet the target.

The discovery LP is not part of the proof. It only supplied the frozen atom parameters. The verifier reconstructs the exact-real weights from the frozen rational couplings.

## A certified fourth-order limitation of this particular ensemble

For \(I=\{0,1,2,3\}\), the balanced-slice target is
\[
\tau_I=\frac{\binom{21}{2}}{\binom{42}{4}}.
\]
Using the same certified weights, the Arb verifier computes
\[
\sum_{\ell=1}^{31}w_\ell\det Q_\ell[I,I]-\tau_I
\]
and certifies that this residual is greater than \(1/200\). Thus the 31-atom measure is an exact pair design, not a complete second/fourth-order design. This is a limitation of this frozen construction, not a no-go theorem for other period-two mixtures.

## Scientific consequence

The earlier theorem excluding every **single** period-two atom at \(N=42\) remains correct. The present result shows that its conclusion does not extend to positive mixtures even at second order: the period-two convex hull already contains the full pair-moment target, with a finite exact positive certificate and strictly positive couplings.

Therefore a global physical-family obstruction cannot be proved from second-order coordinates alone. The next decisive task is to add fourth-order orbit constraints to the positive-mixture problem, starting from this pair-feasible support and then allowing new period-two atoms. A finite candidate LP is discovery only; any claimed construction must be re-certified with exact-real weights and interval-enclosed Fourier moments.

## Reproducibility

- Frozen exact-decimal atoms: evidence/n42_period_two_pair_moment_atoms.json
- Independent 256-bit Arb verifier: verify_n42_period_two_pair_moment_ensemble_arb.py
- Arb certificate output: evidence/n42_period_two_pair_moment_ensemble_arb.json
- Workflow: .github/workflows/eui-n42-period-two-pair-moment-ensemble.yml

The certificate is a computer-assisted exact existence proof for pair moments only. It makes no Choi trace-distance or channel diamond-distance claim.


## Final 256-bit Arb certificate (verified 2026-11-26)

The hosted verifier completed successfully in workflow [45699551876](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45699551876). Its committed output is [evidence/n42_period_two_pair_moment_ensemble_arb.json](evidence/n42_period_two_pair_moment_ensemble_arb.json).

Certified enclosures:
- Moment-matrix determinant:
  \[
  [-8.2205599158252913008515952819085205385928775913251855325745736876337\times10^{-28}
  \ \pm 1.41\times10^{-96}],
  \]
  which excludes zero.
- Minimum weight:
  \[
  [0.000565383615274248869213747056131438992031541456272600328248238144429088
  \ \pm 2.67\times10^{-73}]>\frac1{2000}.
  \]
- Weight sum contains exactly one.
- All 861 unordered pair coordinates pass the interval target check.

For the explicitly non-target quartic witness \(I=\{0,1,2,3\}\):
\[
\mathbb E\det Q_{I,I}
\in[0.008326548825640481438490900780228651616527824966606615752786109235715705
\pm4.40\times10^{-73}],
\]
whereas
\[
\tau_I=\frac{\binom{21}{2}}{\binom{42}{4}}
=0.001876172607879924953095684803001876\ldots.
\]
The residual is certified:
\[
[0.006450376217760556485395215977226775443919945041653520067983107359543097
\pm5.60\times10^{-73}]>\frac1{200}.
\]

Thus the pair-level convex-hull feasibility statement is rigorous, while this particular support is rigorously not a full fourth-order design.
