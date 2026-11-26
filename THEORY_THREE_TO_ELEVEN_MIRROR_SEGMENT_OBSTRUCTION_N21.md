# Exact extension of the perfect-mirror obstruction to 3–11 segments at n=21

Date: 2026-11-26.

This note extends the earlier [3–7 segment theorem](THEORY_THREE_TO_SEVEN_MIRROR_SEGMENT_OBSTRUCTION_N21.md) using the same rational separator, but an independently implemented C++17 exhaustive verifier. It is a finite-family computer-assisted theorem; it is not a global obstruction for arbitrary physical couplings.

## Theorem

Let \(N=42\), and let \((L_1,\ldots,L_k)\) be any ordered positive composition of 42 with \(3\le k\le11\). Partition the open path into consecutive blocks of these lengths. On a block of length \(L\), starting at site \(s\), choose
\[
c_{s+r}=\frac{\pi}{4}\sqrt{(r+1)(L-r-1)},\qquad 0\le r\le L-2,
\]
and set every inter-block and closing-edge coupling to zero. The resulting orthogonal matrix is the direct sum of signed reversals
\[
R^{(L)}_{r,L-1-r}=(-1)^r.
\]
Length-one blocks are identity spectators. Each block has determinant \(+1\), so every seed belongs to \(SO(42)\).

For \(d=1,\ldots,21\), define the cyclic distance-averaged second moment
\[
m_d(R)=\frac1{42}\sum_{i=0}^{41}
\det R_{\{i,i+d\},\{i,i+d\}},\qquad
t_d=\frac{(-1)^{d+1}}{41}.
\]
Let
\[
q=(-10,8,-6,6,-4,2,-2,2,0,2,0,0,0,0,0,0,2,-2,0,0,1),
\qquad y=q/47.
\]
Since \(\|q\|_1=47\), \(\|y\|_1=1\).

**Certified result.** For every such composition,
\[
\boxed{y^{\mathsf T}(t-m(R))\ge\frac{2}{40467}.}
\]
Consequently every probability measure supported on the union of these \(1,594,831,694\) seeds obeys
\[
\|t-\mathbb E_\mu m(R)\|_\infty\ge\frac{2}{40467},
\qquad
\operatorname{TV}(w_\mu,u_{\rm bal})\ge\frac1{40467}.
\]
The TV bound concerns the balanced program-label distribution, equivalently its dephased classical register; it is not a Choi-state trace-distance or channel diamond-distance bound.

## Exact score reduction

Write \(S_d(R)=42m_d(R)\). A length-\(L\) signed reversal has transposition pairs at separations \(L-1,L-3,\ldots\), each with two-site principal minor \((-1)^L\). If \(L\) is odd it also has a fixed centre at \(s+(L-1)/2\), with sign \((-1)^{(L-1)/2}\). A two-site principal minor of the full block-diagonal signed permutation is nonzero only for one transposition pair or for two fixed centres.

Thus the weighted sum \(\sum_d q_dS_d\) is the sum of:
1. a precomputed internal contribution for each block length \(L\);
2. pair interactions between the signed centres of odd-length blocks, at their cyclic separation, with multiplicity two only at antipodal distance 21.

It follows that every slack is the exact rational
\[
\Delta(L_1,\ldots,L_k)
=y^{\mathsf T}(t-m(R))
=\frac{\sum_{d=1}^{21}q_d\bigl(42(-1)^{d+1}-41S_d(R)\bigr)}
{47\cdot41\cdot42}.
\]
No trigonometric or floating-point evaluation is used in this enumeration.

The integer implementation is safe in signed 64-bit arithmetic: each \(|S_d|\le42\), so \(|\sum_dq_dS_d|\le42\|q\|_1=1974\), and the slack numerator is bounded by \(47\cdot42\cdot(1+41)=82,908\).

## Exhaustive exact census

The C++17 verifier enumerates every positive composition for each \(k=3,\ldots,11\), evaluates the integer score, and records exact rational extrema.

| Blocks \(k\) | Compositions | Minimum slack | Attainers | Maximum slack | Nonpositive |
|---:|---:|---:|---:|---:|---:|
| 3 | 820 | \(2/40467\) | 117 | \(192/13489\) | 0 |
| 4 | 10,660 | \(2/40467\) | 38 | \(1027/40467\) | 0 |
| 5 | 101,270 | \(4/1927\) | 30 | \(1478/40467\) | 0 |
| 6 | 749,398 | \(4/1927\) | 6 | \(86/1927\) | 0 |
| 7 | 4,496,388 | \(166/40467\) | 7 | \(299/5781\) | 0 |
| 8 | 22,481,940 | \(248/40467\) | 16 | \(2257/40467\) | 0 |
| 9 | 95,548,245 | \(110/13489\) | 27 | \(2462/40467\) | 0 |
| 10 | 350,343,565 | \(412/40467\) | 10 | \(2749/40467\) | 0 |
| 11 | 1,121,099,408 | \(494/40467\) | 11 | \(2872/40467\) | 0 |

The total is \(1,594,831,694\) compositions. The common minimum remains \(2/40467\), attained only in the \(k=3,4\) families (155 compositions total).

The verifier also checks the fast block/centre formula against a direct signed-permutation construction for 1,000 deterministic random compositions (seed \(202611260834\)), including \(\det R=1\). It reproduces the earlier 3–7 extrema exactly.

## Convex and distributional consequences

Because \(\Delta\) is affine in \(m\), the same lower bound holds for arbitrary positive mixtures over the entire enumerated union. Since \(\|y\|_1=1\), Hölder gives the stated infinity-norm moment gap.

For the program-mass distribution, the bounded characters
\[
\phi_d([T])=\frac1{42}\sum_{i=0}^{41}(-1)^{|\{i,i+d\}\cap T|},
\qquad |\phi_d|\le1,
\]
satisfy \(\mathbb E_{w_R}\phi_d=m_d(R)\) and \(\mathbb E_{u_{\rm bal}}\phi_d=t_d\). Therefore \(G=\sum_dy_d\phi_d\) has \(\|G\|_\infty\le1\), and
\[
|\mathbb E_{u_{\rm bal}}G-\mathbb E_{w_\mu}G|\ge2/40467.
\]
The standard TV dual inequality gives \(\operatorname{TV}(w_\mu,u_{\rm bal})\ge1/40467\).

## Scope and relation to adjacent results

- The same dual fails for two blocks: \((1,41)\) has exact slack \(-80/40467\). The separate [two-mirror theorem](THEORY_TWO_MIRROR_OBSTRUCTION.md) uses a different degree-two/fourth-order separator to exclude that family.
- The earlier [all-odd single-mirror theorem](THEORY_PROGRAM_MINOR_OBSTRUCTION.md) is stronger in length generality for one segment.
- This result does not cover \(k\ge12\), fractional-transfer blocks, arbitrary within-block couplings, general gapped paths, or the full continuous physical family.
- In particular, it does not contradict the 35-atom period-two partial design: the families are different, and that design is not a perfect-mirror block ensemble.
- No Choi/diamond operational lower bound is inferred.

## Reproduction

~~~bash
g++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  verify_ising_three_to_eleven_mirror_segment_obstruction.cpp \
  -o /tmp/verify_three_to_eleven
/tmp/verify_three_to_eleven --output /tmp/evidence.json
~~~

The verifier uses only the C++ standard library and integer arithmetic. The committed evidence is evidence/ising_three_to_eleven_mirror_segment_obstruction_n21.json; the GitHub Actions workflow compiles the source, reruns all \(1.59\) billion cases, and compares the generated JSON exactly.
