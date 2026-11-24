# Exact symmetry reduction and full fourth-order fractional-grid test (n=21)

Date: 2026-11-24. Related: Issue #5, the 41-atom two-probe ensemble, and the complete fourth-order hierarchy.

## Exact reduction of the fractional-path parameter interval

For a length-\(L\) open path, the fractional rotation is the spin-\(j\) representation
\[
R_{L,\alpha}=\exp(\alpha\pi J_y^{(j)}),\qquad j=(L-1)/2.
\]
The \(2\pi\) spin-periodicity gives
\[
R_{L,2-\alpha}=
\begin{cases}
R_{L,\alpha}^{\mathsf T},&j\in\mathbb Z,\\
-R_{L,\alpha}^{\mathsf T},&j\in\mathbb Z+\tfrac12.
\end{cases}
\]
For every even-order principal minor,
\[
\det((-R)_{I,I})=\det(R_{I,I}),\qquad
\det((R^{\mathsf T})_{I,I})=\det(R_{I,I}).
\]
Thus every even-principal-minor feature vector at \(\alpha\in[1,2]\) is exactly duplicated by \(2-\alpha\in[0,1]\). The earlier grid \(L=2,\ldots,42\), \(\alpha=k/100\), \(k=0,\ldots,200\), can therefore be reduced without loss to \(k=0,\ldots,100\). The \(\alpha=0\) identity column is common to all lengths and is retained once. This leaves 4,101 distinct labelled fractional candidates rather than 8,241.

This is an exact feature identity, not a numerical near-duplicate claim. It applies to every even order, not only the fourth-order screen.

## Full fourth-order finite-pool experiment

The target vector contains 21 distance-averaged second moments and all 1,440 fourth-order dihedral-orbit moments. The exact incidence identity in the fourth-moment hierarchy reduces the equality system to 1,313 independent moment rows plus normalization, i.e. 1,314 equations. The modular rank-147 certificate and exact pivot-minor determinant \(824633720832\) justify this reduction.

The candidate pool consists of:

- the 22 base physical atoms from the certified 41-atom construction;
- all 4,101 symmetry-reduced fractional open paths.

Every fractional path has an exactly zero closing edge. The 19 fractional atoms in the 41-atom certificate are already represented in the reduced grid; the script checks their feature identity against the frozen Arb certificate before solving.

To avoid repeatedly forming all 111,930 four-by-four determinants of the \(42\times42\) matrix, the implementation uses the exact block structure \(R_{L,\alpha}\oplus I_{42-L}\). For a quartet \(I\), its principal determinant is the principal minor indexed by \(I\cap\{0,\ldots,L-1\}\) of the active \(L\times L\) block. The script precomputes the quartet-to-active-subset map for each \(L\), evaluates only active principal minors of orders zero through four, and then aggregates over all 1,440 dihedral orbits.

The floating HiGHS solve is a discovery experiment. A feasible result is only a candidate until its frozen support and weights are independently reconstructed and certified with Arb. An infeasible status and floating dual are only finite-grid numerical evidence until the dual is rationally frozen and every candidate inequality is interval-verified. Neither outcome is a theorem about continuous \(\alpha\) or arbitrary gapped couplings.

## Reproduction

Pinned environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0.

~~~bash
OPENBLAS_NUM_THREADS=1 python discover_ising_full_fourth_fractional_grid_n21.py --self-test-only
OPENBLAS_NUM_THREADS=1 python discover_ising_full_fourth_fractional_grid_n21.py
~~~

The self-test compares the block-minor implementation against the independent full \(42\times42\) feature routine and checks the \(\alpha\leftrightarrow2-\alpha\) identity at five path lengths and five nontrivial parameters. The full run freezes the feature hash, the 41-atom warm-start audit, the primal solver status, and—if available—the finite-pool dual direction.

## Current status

The experiment is queued by the accompanying GitHub Actions workflow. No full fourth-order feasibility or obstruction claim is made until its result is observed and, where possible, independently interval-certified.
