# Corrected spin-symmetry reduction and full fourth-order fractional-grid test (n=21)

Date: 2026-11-24. Related: Issue #5, the 41-atom two-probe ensemble, and the complete fourth-order hierarchy.

## Exact symmetry, with the necessary parity qualification

For a length-\(L\) open path,
\[
R_{L,\alpha}=\exp(\alpha\pi J_y^{(j)}),\qquad j=(L-1)/2.
\]
Spin periodicity gives
\[
R_{L,2-\alpha}=
\begin{cases}
R_{L,\alpha}^{\mathsf T},&L\text{ odd},\\
-R_{L,\alpha}^{\mathsf T},&L\text{ even}.
\end{cases}
\]

The first line is an exact symmetry of the **full** \(42\times42\) block-diagonal path rotation \(R_{L,\alpha}\oplus I_{42-L}\): transposition preserves every principal minor. Hence for odd \(L\), the interval \([1,2]\) is covered by \([0,1]\).

For even \(L=42\), the active block is the full matrix. The global minus sign also leaves every even-order principal minor unchanged, so \([0,1]\) again suffices.

For even \(L<42\), however, the full matrix is
\[
(-R_{L,\alpha}^{\mathsf T})\oplus I_{42-L},
\]
not the global negative transpose. A quartet may contain an odd number of active vertices and the remaining vertices in the idle identity block. Its principal determinant then changes sign. This has an exact two-index witness already at \(L=2\): with \(\theta=\pi\alpha/2\),
\[
R_{2,\alpha}\oplus I_{40}
=\begin{pmatrix}\cos\theta&\sin\theta\\-\sin\theta&\cos\theta\end{pmatrix}\oplus I_{40},
\qquad
\det R_{\{0,2\},\{0,2\}}=\cos\theta.
\]
At \(2-\alpha\), the same principal minor is \(-\cos\theta\), so it is not invariant unless \(\cos\theta=0\). The CI self-test also found that the full feature vectors at \(L=2,\alpha=0.17\) and \(2-\alpha\) differ by \(0.36745044512677993\) in maximum norm, while the block-minor implementation agrees with the independent full-matrix computation. Thus the overbroad all-\(L\) reduction is false and is not used.

The corrected exact grid is:
- odd \(L=3,5,\ldots,41\): \(\alpha=k/100,\ k=0,\ldots,100\);
- even \(L=2,4,\ldots,40\): \(\alpha=k/100,\ k=0,\ldots,200\);
- \(L=42\): \(\alpha=k/100,\ k=0,\ldots,100\).

The common \(\alpha=0\) identity column is retained once. This leaves 6,101 fractional candidates. The 22 base atoms from the certified 41-atom construction are added separately, giving 6,123 candidate columns.

## Full fourth-order finite-pool experiment

The target vector contains 21 distance-averaged second moments and all 1,440 fourth-order dihedral-orbit moments. The exact incidence identity in the fourth-moment hierarchy reduces the equality system to 1,313 independent moment rows plus normalization, i.e. 1,314 equations. The modular rank-147 certificate and exact pivot-minor determinant \(824633720832\) justify this reduction.

Every fractional path has an exactly zero closing edge. The 19 fractional atoms in the 41-atom certificate are represented in the corrected grid; the script maps only those lengths for which the spin symmetry is valid and checks the resulting feature vectors against the frozen Arb certificate.

To avoid repeatedly forming all 111,930 four-by-four determinants of the \(42\times42\) matrix, the implementation uses the exact block structure \(R_{L,\alpha}\oplus I_{42-L}\). For a quartet \(I\), its principal determinant is the principal minor indexed by \(I\cap\{0,\ldots,L-1\}\) of the active \(L\times L\) block. The script precomputes the quartet-to-active-subset map for each \(L\), evaluates only active principal minors of orders zero through four, and then aggregates over all 1,440 dihedral orbits.

The floating HiGHS solve is a discovery experiment. A feasible result is only a candidate until its frozen support and weights are independently reconstructed and certified with Arb. An infeasible status and floating dual are only finite-grid numerical evidence until the dual is rationally frozen and every candidate inequality is interval-verified. Neither outcome is a theorem about continuous \(\alpha\) or arbitrary gapped couplings.

## Reproduction

Pinned environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0.

~~~bash
OPENBLAS_NUM_THREADS=1 python discover_ising_full_fourth_fractional_grid_n21.py --self-test-only
OPENBLAS_NUM_THREADS=1 python discover_ising_full_fourth_fractional_grid_n21.py
~~~

The self-test compares the block-minor implementation against the independent full \(42\times42\) feature routine at five path lengths and five parameters. It tests the valid \(\alpha\leftrightarrow2-\alpha\) identity for odd \(L\) and \(L=42\), and retains an explicit even-\(L<42\) counterexample to prevent over-reduction.

## Current status

The corrected experiment is queued by the accompanying GitHub Actions workflow. No full fourth-order feasibility or obstruction claim is made until its result is observed and, where possible, independently interval-certified.


## 2026-11-24 finite-grid LP result and independent Arb follow-up

The corrected 6,123-column / 1,314-equality discovery run is
[workflow 45342873531](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45342873531).
Its block-minor/spin-symmetry/JSON self-test passed. HiGHS reported the
primal equality system **infeasible** and returned a floating separator
candidate with 80 nonzero coefficients. In the row-scaled feature
coordinates used by the discovery LP, the reported target score is
0.3487804171641443, the largest candidate score is 0.08174401205804915,
and the recomputed gap is 0.2670364051060969. The frozen output is
[evidence/ising_full_fourth_fractional_grid_n21.json](evidence/ising_full_fourth_fractional_grid_n21.json).

This is **not yet a theorem**: the HiGHS dual was originally binary64.
The exact decimal coefficients have been frozen as rational inputs, and
the independent verifier
[verify_ising_full_fourth_fractional_grid_dual_arb.py](verify_ising_full_fourth_fractional_grid_dual_arb.py)
checks the separator score against every one of the 6,123 physical columns
using 128-bit Arb. The corresponding workflow is
[.github/workflows/eui-full-fourth-fractional-grid-arb-n21.yml](.github/workflows/eui-full-fourth-fractional-grid-arb-n21.yml).
It uses the exact block-minor reduction to price only the 80 nonzero
fourth-order orbit coefficients, plus the selected second moments. The
proof target is the strict finite-pool inequality
\[
y^{\mathsf T}b>\max_{1\le j\le6123}y^{\mathsf T}a_j,
\]
which alone excludes every probability mixture on this exact finite pool.
No \(\ell_1\)-norm or continuous-parameter claim is needed for this
finite convex-hull separation.

A workflow plumbing defect was also fixed: \`solve_full_grid\` now returns
its diagnostic to \`main\` after writing it, instead of returning \`None\`.
The earlier run had completed the LP and printed the full JSON before
failing at that missing return. This does not change the numerical result.

Even if Arb confirms the separator, its scope remains exactly the 22
pinned base atoms plus the corrected 6,101-column fractional
single-open-path grid. It will not exclude intermediate alpha values,
arbitrary gapped couplings, or multi-segment paths outside the grid, and
it does not resolve the continuous-family ensemble question.
