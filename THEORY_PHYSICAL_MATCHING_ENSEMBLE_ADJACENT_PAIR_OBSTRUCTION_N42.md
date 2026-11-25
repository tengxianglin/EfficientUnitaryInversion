# Adjacent-pair obstruction for physical perfect-matching atoms

Date: 2026-11-26.

## Main theorem

Let \(N=2n=4m+2\ge 6\), with vertices \(0,\ldots,N-1\) on the cycle \(C_N\). Let
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with cyclic indices and arbitrary real couplings, including zero couplings. Let \(M\) be a perfect matching, \(P_M\) its endpoint-swap permutation matrix, and
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\qquad R_M=P_MD.
\]

Write
\[
\nu(M)=\#\bigl\{\{j,j+1\}\in M: j\in\mathbb Z/N\mathbb Z\bigr\}
\]
for the number of matching edges that are also edges of the physical cycle.

**Theorem.** If \(R_M=e^{A(c)}\) for any real cycle coupling vector \(c\), then
\[
\boxed{\nu(M)\ge 2.}
\]
Consequently no positive probability measure supported on physically reachable perfect-matching atoms can reproduce even the complete second-order balanced-slice target.

The result is stronger than the earlier parity obstruction: it does not merely show that most unrestricted perfect matchings are unreachable. It gives a linear functional that separates the balanced target from the convex hull of all physically reachable matching atoms.

## Proof

Let \(p\) be the fixed-point-free involution underlying \(P_M\), and suppose \(R_M=e^A\).

### 1. The support graph is preserved componentwise

Since \(A\) commutes with its exponential,
\[
R_M A R_M^{-1}=A.
\]
Conjugation by the signed permutation \(P_MD\) permutes matrix-entry locations according to \(p\), changing only signs. Therefore the nonzero-edge support graph
\[
G_A=(V,\{\{j,j+1\}:c_j\ne0\})
\]
is invariant under \(p\).

Also, \(A\) is block diagonal across the connected components of \(G_A\), hence so is \(e^A=R_M\). Since \(R_M\) is a signed permutation, \(p\) maps every vertex into the same support component. Thus \(p\) preserves each connected component and acts as a graph automorphism on it.

There can be no isolated component: componentwise preservation would force its unique vertex to be fixed by \(p\), contrary to the perfect-matching condition.

### 2. Proper support gives at least two adjacent matched pairs

If \(G_A\) is a proper subgraph of the cycle, every component is a path. A path has only the identity and reversal as automorphisms. Because \(p\) is fixed-point-free, it must act by reversal, and the path must have an even number of vertices.

Every even path component has a central edge whose two endpoints are exchanged by reversal. This is a cycle edge and therefore a matching edge.

If there are at least two path components, their distinct central edges already give \(\nu(M)\ge2\).

If there is exactly one component, it contains all \(N\) vertices and is the path obtained by deleting one cycle edge. Reversal pairs the two endpoints of this path across the deleted cycle edge, giving one adjacent matching edge; it also pairs the two central path vertices, giving a second, distinct adjacent matching edge. Again \(\nu(M)\ge2\).

### 3. Full support: reflections have two adjacent pairs

If \(G_A=C_N\), then \(p\) is a fixed-point-free involutive automorphism of the cycle. The dihedral possibilities are:
- an edge-axis reflection \(p(j)=a-j\pmod N\), with \(a\) odd;
- the half-turn \(p(j)=j+n\pmod N\).

Every edge-axis reflection has exactly two adjacent matched pairs, namely the two pairs lying on its reflection axis. Hence \(\nu(M)=2\) in this case.

It remains to exclude the half-turn.

### 4. The half-turn is impossible by a complex-trace congruence

Suppose \(p(j)=j+n\), where \(n\) is odd. Put \(J=R_M=P_MD\). Then
\[
J^2=-I,
\]
so \(J\) defines an orthogonal complex structure on \(\mathbb R^{2n}\), with multiplication by \(i\) represented by \(J\).

Because \(A\) commutes with \(e^A=J\), it is complex-linear. Since \(A\) is real skew-symmetric, it is skew-Hermitian on the resulting \(n\)-dimensional complex space. Let its complex eigenvalues be \(i\theta_1,\ldots,i\theta_n\), with \(\theta_k\in\mathbb R\). The identity \(e^A=J=iI\) implies
\[
e^{i\theta_k}=i,\qquad
\theta_k=\frac{\pi}{2}+2\pi q_k,\quad q_k\in\mathbb Z.
\]

In a \(J\)-adapted orthonormal basis,
\[
\operatorname{tr}_{\mathbb C}A
=\frac12\left(\operatorname{tr}_{\mathbb R}A
-i\operatorname{tr}_{\mathbb R}(JA)\right).
\]
The first real trace vanishes because \(A\) is skew-symmetric. The second also vanishes: \(J\) only connects antipodal vertices \(j\) and \(j+n\), while \(A\) has support only on nearest-neighbour cycle edges; for \(N\ge6\), antipodal vertices are not neighbours. Thus
\[
\operatorname{tr}_{\mathbb C}A=0.
\]

On the other hand,
\[
\operatorname{tr}_{\mathbb C}A
=i\sum_{k=1}^n\theta_k
=\frac{i\pi}{2}\left(n+4\sum_{k=1}^n q_k\right).
\]
The integer in parentheses is odd because \(n\) is odd, so it cannot be zero. This contradiction excludes the half-turn.

All possible support cases therefore give \(\nu(M)\ge2\). \(\square\)

## A strict convex separator for the matching-atom subfamily

For \(Q=R D\), define the adjacent-pair functional
\[
\Lambda(Q)=
-\sum_{j=0}^{N-1}
\det Q_{\{j,j+1\},\{j,j+1\}},
\]
with cyclic indices.

For a matching atom \(R_M=P_MD\), one has \(Q=P_M\). Its two-site principal minor is \(-1\) if \(\{j,j+1\}\in M\), and zero otherwise. Hence
\[
\Lambda(P_M)=\nu(M)\ge2
\]
for every physically reachable matching atom, and by linearity the same lower bound holds for every positive mixture of such atoms.

The balanced-slice target in \(Q\)-coordinates has
\[
\mathbb E\det Q_{\{j,j+1\},\{j,j+1\}}=-\frac1{N-1}
\]
for each of the \(N\) cycle edges. Therefore
\[
\Lambda(\tau_{\rm bal})=\frac{N}{N-1}<2.
\]
The exact separation margin is
\[
\boxed{2-\Lambda(\tau_{\rm bal})=\frac{N-2}{N-1}.}
\]
At \(N=42\),
\[
\Lambda(\tau_{\rm bal})=\frac{42}{41},\qquad
\boxed{\text{gap}=\frac{40}{41}.}
\]

Thus no reweighting or pruning of the perfect-matching representation onto physically reachable matching atoms can repair even the adjacent-pair moments.

## Exact checks and the modulo-four boundary

For \(N=42\), all 21 edge-axis reflections were checked and each has exactly two adjacent matched pairs. The half-turn has zero adjacent matched pairs but is excluded by the complex-trace argument. Proper-support components correspond to compositions of \(n=21\) into positive even path half-lengths; there are \(2^{20}=1{,}048{,}576\) such compositions, and the component-count formula gives a minimum adjacent-pair count of two.

The hypothesis \(N=4m+2\) is essential. At \(N=4\), the same-parity antipodal matching \(M=\{(0,2),(1,3)\}\) is physically reachable with
\[
A=\frac{\pi}{2}K,\qquad
K=\begin{pmatrix}
0&1&0&1\\
-1&0&1&0\\
0&-1&0&-1\\
-1&0&1&0
\end{pmatrix},
\]
because \(K^T=-K\), \(K^3=-4K\), and
\[
e^{(\pi/2)K}=I+\frac12K^2=P_MD.
\]
That matching has zero cycle-adjacent matched edges. The exact integer verifier checks these identities.

## Scope

**Proved:** for every \(N=4m+2\ge6\), every physically reachable signed perfect-matching atom has at least two cycle-adjacent matched pairs; hence no positive mixture of such atoms matches even all adjacent-pair target coordinates. At \(N=42\), the matching-subfamily separation margin is exactly \(40/41\).

**Not proved:** the same inequality for general physical matrices \(Q=e^{A(c)}D\) that are not signed matching permutations. In particular, this does not settle the full physical convex-hull question in Issue #7. It also gives no Choi- or diamond-distance bound.

## Reproducibility

- Exact arithmetic verifier: verify_physical_matching_ensemble_adjacent_pair_obstruction.py
- Machine-readable evidence: evidence/physical_matching_ensemble_adjacent_pair_obstruction_n42.json
- CI: .github/workflows/eui-physical-matching-adjacent-pair-obstruction.yml
