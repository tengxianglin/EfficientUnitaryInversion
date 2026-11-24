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
not the global negative transpose. A quartet may contain an odd number of active vertices and the remaining vertices in the idle identity block. Its principal determinant then changes sign. The same issue already appears in degree two. The CI self-test exposed this: at \(L=2,\alpha=0.17\), the full feature vectors at \(\alpha\) and \(2-\alpha\) differ by \(0.36745044512677993\) in maximum norm, while the block-minor implementation agrees with the independent full-matrix computation. Thus the overbroad all-\(L\) reduction is false and is not used.

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
