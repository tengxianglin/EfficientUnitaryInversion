# 6,131-column full-second/fourth finite-pool obstruction at n=21

**Status (2026-11-25): rigorous finite-pool theorem; independently certified with python-flint / Arb.** The certificate is committed at [053032e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/053032e2fbe094448076e29883fa8f7285f40920), produced by successful [workflow 45469881533](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45469881533). The particular dual has since been escaped by two exact physical paths, independently certified at 256-bit Arb; see [the escape note](THEORY_6131COL_DUAL_GAPPED_ESCAPE.md).

**Not claimed:** a continuum obstruction, an all-even-principal-minor obstruction, a positive ensemble, or a Choi/diamond-distance lower bound.

## 1. Exact finite physical pool

Let \(N=42\) (\(n=21\)) and
\[
R(c)=e^{A(c)}\in SO(42),\qquad
A(c)_{j,j+1}=2c_j,\quad A(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,\quad c_{41}=0.
\]

The certified pool has exactly
\[
22+6101+8=6131
\]
columns:

1. **22 pinned base atoms**, inherited from the 41-atom low-moment Arb certificate;
2. **6,101 corrected fractional single-open-path grid atoms**, with \(\alpha=k/100\):
   - \(L=2\): \(k=0,\ldots,200\);
   - odd \(L=3,5,\ldots,41\), and \(L=42\): \(k=1,\ldots,100\);
   - even \(L=4,6,\ldots,40\): \(k=1,\ldots,200\);
3. **Eight exact-rational gapped paths**: six inherited paths and two new paths that escaped the preceding 6,129-column dual. The eight comprise five connected paths and three segmented paths. Every path has the closing edge \(c_{41}=0\); all internal couplings are nonnegative, with the zero-edge pattern frozen in the diagnostic.

The 6,101 grid count is \(201+20(100)+100+19(200)=6101\). The diagnostic and its complete gapped coupling list are frozen in [the LP record](evidence/ising_full_fourth_plus_eight_gapped_n21.json).

## 2. Complete second-/fourth-order feature system

For \(R\in SO(42)\), let \(F(R)\in\mathbb R^{1461}\) contain:

- all 21 distance-averaged second moments;
- all 1,440 dihedral orbits of fourth-order principal minors, covering all
  \[
  \binom{42}{4}=111930
  \]
  quartets.

The exact incidence hierarchy has 1,313 independent moment coordinates; adding normalization gives 1,314 equalities. The pinned exact hierarchy pivot-minor determinant is
\[
824633720832\ne0.
\]
Let \(b\in\mathbb Q^{1461}\) be the exact balanced target and \(A_{6131}\) the matrix whose columns are the 6,131 listed feature vectors.

This is the **complete second-/fourth-order** feature system. It does not include sixth- or eighth-order constraints.

## 3. Exact rational dual and Arb certificate

The floating HiGHS solve is discovery only. The independent verifier freezes the 82 nonzero printed dual decimals as exact rational numbers and normalizes them using
\[
D=\operatorname{diag}(41I_{21},533I_{1440}),\qquad
\boxed{\|D^{-1}y\|_1=1}.
\]
The exact full-coordinate norm is
\[
\|y\|_1=
\frac{93744873970464755319593}
{177666666666666580821}
<533.
\]

The verifier independently prices:

- 22 base atoms at 512-bit Arb;
- all 6,101 fractional-grid atoms at 128-bit Arb;
- all eight exact-rational gapped paths at 512-bit Arb.

The minimum certified column-gap lower endpoint is
\[
0.2396341325267923622380270022592260250\ldots>\frac15,
\]
attained at the \(L=41,\alpha=1/2\) fractional-grid column. Thus every one of the 6,131 listed columns obeys
\[
\boxed{y^{\mathsf T}(b-F(R_j))>\frac15.}
\]

The certificate pins the LP diagnostic by SHA-256
c2d86c213d2f0fe4c3784251dc3922a6e517d8debdf5d0b3b6dcaf4fd5cab9ea,
the 6,129-column parent diagnostic/certificate, both 6,129-dual escape artifacts, and the warm positive 41-atom certificate. The independent verifier also runs five active-block-vs-full-matrix pricing self-tests; all five pass.

### Theorem 1 — 6,131-column finite-pool moment obstruction

For every probability vector \(p\in\Delta_{6131}\),
\[
y^{\mathsf T}(b-A_{6131}p)
=\sum_{j=1}^{6131}p_j\,y^{\mathsf T}(b-F(R_j))
>\frac15.
\]
By Hölder and the exact norm bound \(\|y\|_1<533\),
\[
\boxed{
\|b-A_{6131}p\|_\infty>\frac1{2665}.
}
\]
No nonnegative mixture of the exact 6,131 listed physical columns can match all 1,461 retained second-/fourth-order coordinates within this residual.

### Corollary 1 — finite-pool program-label TV obstruction

For every even Majorana index set \(I\), the exact DPP / Pauli-character identity gives
\[
\mathbb E_{[T]\sim w_R}(-1)^{|I\cap T|}
=\det R_{I,I}.
\]
For each retained second- or fourth-order dihedral orbit \(O\), its feature is therefore the expectation of the bounded orbit test
\[
\phi_O([T])=\frac1{|O|}\sum_{I\in O}(-1)^{|I\cap T|},
\qquad \|\phi_O\|_\infty\le1.
\]
The target coordinate is the same expectation under the uniform balanced-label law \(u_{\rm bal}\). The moment residual implies that at least one retained test has expectation gap greater than \(1/2665\). Since
\[
|\mathbb E_P f-\mathbb E_Q f|
\le 2\,\mathrm{TV}(P,Q)
\quad\text{for }\|f\|_\infty\le1,
\]
every mixture on this exact pool satisfies
\[
\boxed{\mathrm{TV}(w_p,u_{\rm bal})>\frac1{5330}.}
\]
Equivalently, the corresponding dephased program-label registers have trace distance greater than \(1/5330\).

This is a **finite-pool classical program-mass** statement. It is not a Choi-state trace-distance or channel diamond-distance lower bound.

## 4. Reproducibility

- LP discovery: [discover_ising_full_fourth_plus_eight_gapped_n21.py](discover_ising_full_fourth_plus_eight_gapped_n21.py)
- Independent 128-/512-bit Arb verifier: [verify_ising_full_fourth_plus_eight_gapped_arb_n21.py](verify_ising_full_fourth_plus_eight_gapped_arb_n21.py)
- Floating diagnostic: [ising_full_fourth_plus_eight_gapped_n21.json](evidence/ising_full_fourth_plus_eight_gapped_n21.json)
- Rational Arb certificate: [ising_full_fourth_plus_eight_gapped_arb_n21.json](evidence/ising_full_fourth_plus_eight_gapped_arb_n21.json)
- Successful CI: [45469881533](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45469881533)
- Certificate commit: [053032e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/053032e2fbe094448076e29883fa8f7285f40920)

The verifier checks all 6,131 columns, the exact scaled-\(\ell_1\) normalization, the full-coordinate norm, and the strict \(1/5\) common gap. The workflow pins NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0, and Python 3.12.14.

## 5. Scope, certified continuous escapes, and next decisive test

Theorem 1 is a finite-pool statement. It does not cover arbitrary nonuniform positive couplings or all multi-segment open paths. The eight gapped paths are witnesses, not an exhaustive parameterization of that continuum. It does not impose every even principal minor and does not imply an operational Choi/diamond converse.

The 82-term dual has now been **defeated as a global separator** by two exact paths, independently certified at 256-bit Arb: one connected path with all 41 internal couplings strictly positive, and one multi-segment path with cuts \([12,17,29,37]\). Their target-minus-score intervals are strictly negative:
\[
-26.44327687623536845\ldots<0,
\qquad
-30.37726183060399288\ldots<0.
\]
Both pass all 1,764 interval orthogonality checks and determinant-one certification. This does not invalidate Theorem 1; both paths are outside its exact 6,131-column pool. See [the escape note](THEORY_6131COL_DUAL_GAPPED_ESCAPE.md), [search transcript](evidence/ising_full_fourth_plus_eight_gapped_search_n21.json), [256-bit Arb certificate](evidence/ising_full_fourth_plus_eight_gapped_escape_arb_n21.json), and [successful workflow 45483583523](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45483583523).

The next decisive experiment is to append both exact rational paths and reoptimize the complete 1,461-coordinate LP on 6,133 columns. A new dual must again be independently rationalized and Arb-verified; a primal is only a discovery candidate until its exact weights and all coordinates are interval-verified.

The paper-central problem remains an exact positive ensemble satisfying every even-principal-minor constraint at \(n=21\), or a genuinely global obstruction for the intended continuous physical family, followed by an operational bridge to Choi/channel diamond error.
