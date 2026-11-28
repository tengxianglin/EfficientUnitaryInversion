# Mixed nonperiodic physical ensemble: all pair moments plus nine quartic translation orbits (N=42)

Date: 2026-11-28. Run 74. Related: Issue #7; Run 73 matching-only minimax.

## Statement and scope

Let
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with cyclic indices modulo 42, and let
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\quad
R(c)=e^{A(c)},\quad Q(c)=R(c)D.
\]
Because \(D A(c)D=-A(c)\), every \(Q(c)\) is a symmetric involution with trace zero.

For a seed \(c\), define its cyclic-orbit measure by
\[
\mu_c=\frac1{42}\sum_{s=0}^{41}\delta_{\operatorname{shift}_s(c)}.
\]
The certified ensemble below is a positive mixture of 30 such orbit measures:
- 26 strictly-positive period-two seeds, each with two distinct translates;
- 4 strictly-positive primitive-period-42 seeds, each with 42 distinct translates.

The 220 distinct physical cycle atoms are all strictly positive. The four genuinely nonperiodic orbit families carry more than \(1/20\) of the total probability.

## Exact moment system

For \(d=1,\ldots,20\), define the cyclic pair-distance orbit moment
\[
p_d(c)=\frac1{42}\sum_{s=0}^{41}
\det Q(c)_{\{s,s+d\},\{s,s+d\}},
\]
and for the opposite distance
\[
p_{21}(c)=\frac1{21}\sum_{s=0}^{20}
\det Q(c)_{\{s,s+21\},\{s,s+21\}}.
\]
A cyclic-orbit mixture is translation invariant. Hence matching
\[
\mathbb E p_d=-\frac1{41},\qquad d=1,\ldots,21,
\]
matches every one of the \(\binom{42}{2}=861\) pair coordinates.

For a four-set \(I\), define
\[
m_I(c)=\frac1{42}\sum_{s=0}^{41}\det Q(c)_{I+s,I+s}.
\]
Translation invariance makes this the expectation of every translate of \(I\). The nine frozen representatives are
\[
\begin{aligned}
&(0,1,2,3),\ (0,3,10,15),\ (0,2,4,6),\\
&(0,10,20,30),\ (0,2,21,23),\ (6,13,14,30),\\
&(0,3,19,26),\ (0,8,20,28),\ (0,4,8,12).
\end{aligned}
\]
Their disjoint cyclic orbits contain 357 distinct four-subsets. The target for each is
\[
\mathbb E m_I=\frac1{533}.
\]

For the 30 seed orbits, form the \(30\times30\) matrix whose columns contain the 21 pair-distance moments followed by these nine quartic-orbit moments. The target vector contains 21 copies of \(-1/41\) and nine copies of \(1/533\).

## Normalization identity

For every symmetric involution \(Q\) with trace zero,
\[
\sum_{j\ne i}\det Q_{\{i,j\},\{i,j\}}
=Q_{ii}\sum_{j\ne i}Q_{jj}-\sum_{j\ne i}Q_{ij}^2=-1.
\]
Summing over \(i\), and grouping unordered pairs by cyclic distance, gives
\[
2\sum_{d=1}^{20}p_d+p_{21}=-1.
\]
Consequently, if all 21 pair-distance moments equal \(-1/41\), the total seed-orbit weights necessarily sum to one. The verifier checks the weight sum independently as a consistency test.

## Computer-assisted exact existence statement

The frozen rational-decimal couplings are in
evidence/n42_mixed_cycle_nine_quartic_atoms.json. The weights are not claimed to be rational: they are the unique exact-real solution of the frozen 30-by-30 moment system.

The independent 256-bit Arb verifier reconstructs each period-two seed through its Fourier representation and each nonperiodic seed through the full 42-by-42 matrix exponential. It then:
1. proves the 30-by-30 determinant interval excludes zero;
2. solves for all 30 exact-real weights and certifies each exceeds \(1/2000\);
3. certifies the weight sum is one;
4. certifies all 21 pair-distance moments, hence all 861 pair coordinates;
5. certifies all nine quartic translation-orbit moments, hence all 357 listed quartic coordinates;
6. certifies all four nonperiodic seeds have primitive period 42 and all 42 couplings positive;
7. certifies the total nonperiodic mass exceeds \(1/20\).

This is an exact-real, interval-certified positive physical ensemble for the stated partial moment system. It is not merely a floating LP fit.

## Explicit quartic incompleteness

The same exact-real weights certify two additional quartic translation-orbit residuals:
\[
\mathbb E m_{(0,3,18,21)}-\frac1{533}>\frac1{500},
\]
and
\[
\mathbb E m_{(0,1,6,7)}-\frac1{533}>\frac1{250}.
\]
Thus this mixed ensemble is not a complete fourth-order design. The second witness is also the largest absolute quartic-orbit residual in the binary64 full-orbit discovery screen; that ranking is discovery evidence only, while the displayed strict residual is independently Arb-certified.

## Discovery versus proof

The frozen support was discovered by a binary64 SciPy/HiGHS LP over 3,000 random positive 42-edge cycle seeds, after a 120-seed warm-up block, with RNG seed 20261128. The objective maximized the total mass assigned to nonperiodic seed orbits while preserving the pair and nine quartic constraints.

The floating search and its support selection are discovery only. The proof is the separate Arb reconstruction from exact-rational decimal couplings and the interval-certified 30-by-30 solve.

## Scope limitations

Proved by the Arb certificate:
- a positive ensemble of 220 distinct strictly-positive physical cycle atoms exists;
- it matches all 861 pair coordinates;
- it matches 357 quartic coordinates in nine full cyclic translation orbits;
- it assigns more than 5% probability to four primitive-period-42 orbit families.

Not proved:
- a complete fourth-order design;
- any sixth- or higher-order all-coordinate match;
- membership of the complete balanced-slice target in the closed convex hull of all cycle exponentials;
- a global separating inequality for every real coupling vector;
- a program-label TV to Choi trace-distance or channel diamond-distance implication.

The two certified quartic misses are candidate-specific and do not exclude a different physical ensemble.

## Reproducibility

- Frozen input: evidence/n42_mixed_cycle_nine_quartic_atoms.json
- Independent verifier: verify_n42_mixed_cycle_nine_quartic_ensemble_arb.py
- Machine certificate: evidence/n42_mixed_cycle_nine_quartic_ensemble_arb.json
- CI: .github/workflows/eui-n42-mixed-cycle-nine-quartic.yml



## Final 256-bit Arb certificate

The independent verifier completed in GitHub Actions [46128674321](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46128674321), against the corrected frozen input. It certified:

- moment-matrix determinant:
  \[
  [-6.178383682608817535937694562703590719062047946330618475182622559141\times10^{-39}
  \ \pm 3.92\times10^{-106}],
  \]
  which excludes zero;
- minimum exact-real weight:
  \[
  [0.000889109464870221522803618559222143270398729262057262495186926153844640
  \ \pm 6.76\times10^{-73}]>\frac1{2000};
  \]
- total weight:
  \[
  [1.0000000000000000000000000000000000000000000000000000000000000000000000
  \ \pm3.58\times10^{-71}],
  \]
  which contains exactly one;
- total mass on the four primitive-period-42 seeds:
  \[
  [0.06981604734786188502231445203212434131817526623576506399557910824831696
  \ \pm4.53\times10^{-72}]>\frac1{20};
  \]
- minimum coupling over all 220 distinct atoms:
  \[
  \frac{6388147249}{125000000000}>0.
  \]

The two independently certified quartic misses are:
\[
\mathbb E m_{(0,3,18,21)}-\frac1{533}
=
[0.003543333344852453513810911961835713748324339484852944816801231133077765
\ \pm6.21\times10^{-73}]>\frac1{500},
\]
and
\[
\mathbb E m_{(0,1,6,7)}-\frac1{533}
=
[0.004621673636191943613782702414344518917298679980578209751137610452220608
\ \pm5.65\times10^{-73}]>\frac1{250}.
\]

The machine certificate is evidence/n42_mixed_cycle_nine_quartic_ensemble_arb.json. The workflow's environment check, compilation, full Arb reconstruction, deterministic certificate commit, and artifact upload all passed.

The binary64 discovery screen additionally evaluated all 2,670 cyclic translation orbits of four-subsets (all 111,930 four-sets). It ranked \((0,1,6,7)\) as the largest absolute residual, approximately \(0.00462167363619\). This ranking is discovery evidence only; the strict lower bound for that named witness is the Arb-certified statement above.
