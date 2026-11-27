# Exact N=10 obstruction for the contiguous perfect-transfer block ansatz

Date: 2026-11-27. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), [the exact N=8 physical ensemble](THEORY_PHYSICAL_CYCLE_ENSEMBLE_N8.md), and [the N=8 period-two mixture no-go](THEORY_N8_PERIOD_TWO_MIXTURE_FOURTH_ORDER_NO_GO.md).

## Result and scope

For \(N=10\), write
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j,
\quad R(c)=e^{A(c)},\quad
D=\operatorname{diag}(1,-1,\ldots,1,-1),\quad Q=RD.
\]
The balanced-slice target is
\[
\tau_I=(-1)^r\frac{\binom5r}{\binom{10}{2r}},
\qquad |I|=2r.
\]

We prove the following restricted-family no-go:

**Theorem.** No probability mixture of contiguous perfect-transfer block-reversal atoms (nor of any of their dihedral conjugates or vertex-sign gauges) can match the complete N=10 balanced-slice even-principal-minor target. More quantitatively, for every such mixture \(\mu\),
\[
\boxed{\|v(\mu)-\tau\|_\infty\ge \frac{52}{2205}.}
\]
This is a theorem about the finite signed-reversal block ansatz, **not** about all cycle exponentials \(e^{A(c)}\). General non-permutation cycle exponentials remain outside the excluded family.

## 1. The physical block-reversal family

For an ordered composition \(L=(L_1,\ldots,L_m)\) of 10, partition the path obtained by cutting the cycle edge \((9,0)\) into contiguous blocks of lengths \(L_j\). For a block of length \(L\) starting at \(s\), set
\[
c_{s+r}=\frac{\pi}{4}\sqrt{(r+1)(L-r-1)},
\qquad r=0,\ldots,L-2,
\]
and set every cut edge to zero. The corresponding block generator is the spin-\((L-1)/2\) rotation through angle \(\pi\), so
\[
e^{A_L}|s+r\rangle=(-1)^r|s+L-1-r\rangle.
\]
Thus each composition gives an exact signed-permutation \(R_L\in SO(10)\), and \(Q_L=R_LD\) is a symmetric involution with trace zero.

There are exactly \(2^{9}=512\) ordered compositions of 10. Every contiguous partition of the cycle into one or more path blocks is a dihedral image of one of these representatives. Reflection and rotation conjugation preserve physical cycle-exponential reachability. A vertex-sign gauge also preserves all principal minors, since it conjugates \(Q\) by a diagonal \(\pm1\) matrix.

For a subset \(I\), \(\det(Q_L)_{I,I}\) is zero unless \(I\) is invariant under the block-reversal involution. If invariant, it is the sign of the induced permutation times the product of the selected signed-permutation entries. Hence every feature used below is exactly \(0,\pm1\).

## 2. An exact seven-orbit separator

For a subset orbit \(\mathcal O\) under \(D_{10}\), define
\[
\bar v_{\mathcal O}(Q)=\frac1{|\mathcal O|}
\sum_{I\in\mathcal O}\det Q_{I,I}.
\]
Use the following seven orbit representatives and nonnegative rational coefficients:

| \(\mathcal O\) representative | Orbit size | \(z_{\mathcal O}\) | Target moment |
|---|---:|---:|---:|
| \(\{0,1\}\) | 10 | \(3/35\) | \(-1/9\) |
| \(\{0,2\}\) | 10 | \(3/35\) | \(-1/9\) |
| \(\{0,1,2,3,4,5\}\) | 10 | \(11/35\) | \(-1/21\) |
| \(\{0,1,2,4,5,6\}\) | 10 | \(8/35\) | \(-1/21\) |
| \(\{0,1,2,3,4,7\}\) | 10 | \(3/35\) | \(-1/21\) |
| \(\{0,1,2,5,6,7\}\) | 5 | \(3/70\) | \(-1/21\) |
| \(\{0,1,2,3,5,6,7,8\}\) | 5 | \(11/70\) | \(+1/9\) |

The coefficients sum exactly to one, so \(\|z\|_1=1\). The target score is
\[
z\cdot\tau
= -\frac{2}{105}-\frac{47}{1470}+\frac{11}{630}
= -\frac{74}{2205}.
\]

For each of the 512 compositions, compute the exact score
\[
S(L)=\sum_{\mathcal O}z_{\mathcal O}\bar v_{\mathcal O}(Q_L).
\]
Exhaustive integer/Fraction enumeration gives
\[
\boxed{\max_{L\vdash10}S(L)=-\frac2{35}},
\qquad
\min_{L\vdash10}S(L)=-\frac{38}{175}.
\]
The maximum is attained by 82 of the 512 compositions; there are 24 distinct exact score values. The full deterministic score table has SHA256
79911ca8a15b51b84eab95720c0265dc52b7f9db6c44feab26b7d11ea5e16804.

Consequently every probability mixture of these atoms satisfies
\[
z\cdot v(\mu)\le-\frac2{35}.
\]
Since \(z\ge0\) and \(\|z\|_1=1\),
\[
\|v(\mu)-\tau\|_\infty
\ge z\cdot(\tau-v(\mu))
\ge -\frac{74}{2205}+\frac2{35}
=\boxed{\frac{52}{2205}}.
\]
The same inequality applies to arbitrary orientations of the block atoms because the score uses dihedral orbit averages; it therefore excludes mixtures of all rotations/reflections and all vertex-sign gauges of the 512 representatives.

## 3. Exact reproduction

Run:

~~~bash
python verify_n10_block_mirror_subfamily_separator.py
~~~

The dependency-free verifier:
1. generates all 512 compositions from their nine cut bits;
2. reconstructs the exact signed-reversal permutation and \(Q=RD\) entry signs;
3. checks \(R\in SO(10)\), \(Q=Q^T\), \(Q^2=I\), and \(\operatorname{tr}Q=0\) for every composition;
4. enumerates the seven \(D_{10}\) subset orbits;
5. evaluates all 512 rational scores with fractions.Fraction;
6. checks the exact maximum, minimum, gap, multiplicity, and SHA256 of the full score table.

Machine summary: [evidence/n10_block_mirror_subfamily_separator.json](evidence/n10_block_mirror_subfamily_separator.json). Workflow: [.github/workflows/eui-n10-block-mirror-subfamily-separator.yml](.github/workflows/eui-n10-block-mirror-subfamily-separator.yml).

## 4. Interpretation

The N=8 construction is not a general block-composition recipe that extends automatically to the next even size. At N=10, the entire contiguous perfect-transfer signed-reversal ansatz is separated from the target by a strict rational margin.

This does **not** imply that the N=10 target is outside the convex hull of all physical cycle exponentials. In particular, non-permutation exponentials and continuously varying couplings are not covered.

## 5. A connected physical cycle escapes this restricted dual

The seven-orbit functional is not a global separator for the full N=10 cycle family. Set every coupling equal to the exact rational
\[
c_0=\cdots=c_9=\frac{409}{100}.
\]
The independent 256-bit Arb verifier reconstructs \(R=e^{A(c)}\), forms \(Q=RD\), checks \(R^TR=I\), \(Q=Q^T\), \(Q^2=I\), \(\operatorname{tr}Q=0\), and \(\det R=1\), and directly evaluates all seven orbit averages. It certifies
\[
S(R)\in[-0.0029736260361924988743358517869826031222995682174649011732303449734630080
\pm 6.02\times10^{-74}],
\]
which is strictly greater than both the block-family ceiling \(-2/35\) and the target score \(-74/2205\).

Evidence: [256-bit Arb certificate](evidence/n10_uniform_cycle_escape_arb.json), [independent verifier](verify_n10_uniform_cycle_escape_arb.py), [CI workflow](.github/workflows/eui-n10-uniform-cycle-escape.yml), [workflow run 45969851019](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45969851019).

This connected atom only disproves global validity of the block-family dual. It does **not** put the target in the full physical convex hull and does not weaken the exact block-family no-go.

The next physical question is whether mixtures of non-perfect-transfer cycle atoms can match the target. Any finite search is discovery only; a positive answer needs an all-moment positive certificate, while a negative answer needs a separator valid over the full continuous coupling family.
