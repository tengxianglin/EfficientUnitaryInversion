# Z2 holonomy normal form for the real cycle-coupling family

Date: 2026-11-28. Run 77. Related: Issue #7, Run 66, Run 76.

## Setup

Let N be even, with cyclic indices modulo N, and define
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j,
\qquad D=\operatorname{diag}(1,-1,\ldots,1,-1),
\qquad Q(c)=e^{A(c)}D.
\]
For the EUI problem N=42. Let
\[
v(c)=\bigl(\det Q(c)_{I,I}\bigr)_{|I|\ {\rm even}}
\]
be the complete even-principal-minor feature vector. The same argument below actually preserves principal minors of every order.

Run 66 already identified the legal vertex-sign gauge. This note classifies its orbits exactly and identifies the residual Z2 invariant that is not removed by gauge transformations.

## Lemma 1 — exact gauge covariance

For any vertex signs \(\epsilon_j\in\{-1,+1\}\), let
\[
S_\epsilon=\operatorname{diag}(\epsilon_0,\ldots,\epsilon_{N-1}),
\qquad
c^\epsilon_j=\epsilon_j\epsilon_{j+1}c_j.
\]
Then
\[
S_\epsilon A(c)S_\epsilon=A(c^\epsilon).
\]
Because S_epsilon commutes with D,
\[
Q(c^\epsilon)=S_\epsilon Q(c)S_\epsilon.
\]
Consequently, for every subset I, with no restriction on its size,
\[
\boxed{\det Q(c^\epsilon)_{I,I}=\det Q(c)_{I,I}.}
\]
Indeed, the principal block is conjugated by the diagonal matrix S_epsilon restricted to I, whose determinant is squared.

Thus the entire principal-minor feature vector, not only its even-order part, is exactly gauge invariant.

## Theorem 1 — complete gauge-orbit classification on a cycle

Fix the magnitudes |c_j| and let the support graph contain the cycle edges j--(j+1) for which c_j is nonzero.

1. If at least one coupling is zero, the support graph is a forest (a disjoint union of paths and isolated vertices). All nonzero edge signs can be removed by a vertex-sign gauge. There is exactly one gauge orbit for the fixed magnitudes.
2. If every coupling is nonzero, there are exactly two gauge orbits. They are distinguished by the Z2 cycle holonomy
   \[
   h(c)=\prod_{j=0}^{N-1}\operatorname{sgn}(c_j)\in\{-1,+1\}.
   \]
   This product is invariant because
   \[
   \prod_j(\epsilon_j\epsilon_{j+1})=1.
   \]

### Proof

For a proper support, choose one root in each connected component of the support forest and set its vertex sign to +1. Propagate along each present edge j--(j+1) by choosing
\[
\epsilon_{j+1}=\epsilon_j\operatorname{sgn}(c_j).
\]
Then the transformed edge sign is
\[
\epsilon_j\epsilon_{j+1}\operatorname{sgn}(c_j)=+1.
\]
A forest has no cycle-consistency obstruction, so this defines a gauge on every component. This proves transitivity when at least one edge is absent.

For full support, set epsilon_0=1 and propagate along edges j=0,...,N-2 using the same rule. The first N-1 transformed couplings are positive. The remaining edge has sign
\[
\epsilon_{N-1}\epsilon_0\operatorname{sgn}(c_{N-1})
=\prod_{j=0}^{N-1}\operatorname{sgn}(c_j)=h(c).
\]
The holonomy is gauge invariant, so the two canonical sign patterns cannot be gauge equivalent. The construction shows that every full-support sign pattern belongs to one of these two orbits. QED.

## Corollary 1 — canonical representatives

Every real coupling vector is feature-equivalent to exactly one of the following canonical sign forms at its fixed magnitude vector:

- If at least one edge is zero: c_j^can=|c_j| for every j, retaining the zero entries.
- If all edges are nonzero:
  \[
  c_j^{\rm can}=|c_j|\quad (j=0,\ldots,N-2),\qquad
  c_{N-1}^{\rm can}=h(c)|c_{N-1}|.
  \]

Thus the real parameter domain has only two full-support sign sectors after gauge reduction: positive cycle holonomy and negative cycle holonomy. The negative sector can be represented by the single fixed seam c_{N-1}<0, with all other couplings positive.

The holonomy is the product of edge signs around the unique cycle. It is the residual Z2 gauge invariant; it must not be silently discarded when the model allows arbitrary real couplings.

## Theorem 2 — exact reduction of the closed convex-hull question to two orthants

Let
\[
\mathcal V_{\mathbb R}=\{v(c):c\in\mathbb R^N\},
\]
\[
\mathcal V_+=\{v(a):a_j>0\ \text{for all }j\},
\]
and
\[
\mathcal V_-=
\{v(a_0,\ldots,a_{N-2},-a_{N-1}):a_j>0\ \text{for all }j\}.
\]
Then
\[
\boxed{
\overline{\operatorname{conv}}\mathcal V_{\mathbb R}
=
\overline{\operatorname{conv}}(\mathcal V_+\cup\mathcal V_-).
}
\]

### Proof

By Theorem 1 and Lemma 1, every full-support real coupling vector has the same feature vector as a point in either the positive orthant or the fixed-negative-seam orthant. If at least one coupling is zero, it is feature-equivalent to a nonnegative vector a. For every t>0, the vector a+t(1,...,1) is strictly positive and converges to a as t tends to zero. Matrix exponentiation and determinants are continuous, so v(a) lies in the closure of V_+.

Therefore every point of V_R lies in the closure of V_+ union V_-. Taking closed convex hulls gives one inclusion. The reverse inclusion follows because both orthants are subsets of R^N. QED.

This is an exact statement about the closed convex hull, not merely a numerical parameter heuristic. Zero-edge boundary atoms add no further closed-convex-hull sector beyond the closure of the positive orthant.

## Compatibility with the D42 reduction

The Run 76 rotation and reflection maps permute the 42 coupling coordinates:
\[
c_j\mapsto c_{j-s},\qquad c_j\mapsto c_{-j-1}.
\]
They therefore preserve the full-support holonomy h(c). After gauge canonicalization, the complete real-coupling search can be organized into two D42-symmetrized families:

- positive holonomy: all 42 canonical couplings positive;
- negative holonomy: the first 41 canonical couplings positive and the final seam negative.

For a D42-averaged feature column, gauge-equivalent vectors give exactly the same column, and dihedrally related magnitude patterns give the same averaged column. Thus the natural search labels are a D42 orbit of the magnitude vector together with the holonomy bit when support is full.

## Consequences for the current EUI evidence

1. The Run 74 ensemble of 220 strictly-positive atoms lies entirely in the positive-holonomy sector. Its certified partial moment match remains valid, but it does not price or exclude the negative-holonomy sector.
2. Run 76's D42 symmetry reduction is valid in both sectors, but D42 itself does not change h(c). It does not identify the positive and negative sectors.
3. If the physical model explicitly imposes c_j>0, the positive sector is the full allowed domain. If Issue #7 retains c in R^42, a global separator must be checked on both canonical sectors.
4. A separator proved only for c_j>0 is not a separator for the real-coupling family. Conversely, a certified positive ensemble is already sufficient to prove membership for the larger real-coupling family.
5. The next decisive finite-pool experiment should append D42-averaged columns from the fixed-negative-seam sector to the existing positive-sector pool while retaining all 21 pair constraints and the complete quartic-orbit coordinates. Any finite-pool infeasibility remains non-global evidence.

## Verification and scope

The dependency-free verifier exhausts all 3^N sign/zero patterns for N=4,6,8,10, checks the one-or-two gauge-orbit classification for every fixed support, and checks compatibility with rotations and reflection. It additionally performs 4,096 deterministic N=42 sign-pattern smoke tests. The all-N theorem is proved above; the finite enumeration is an implementation audit, not an extrapolation-based proof.

A separate local binary64 sanity check evaluated all principal minors for random N=4,6,8,10 matrices before and after random vertex gauges; the observed maximum discrepancy was zero at printed precision. This numerical check is not used in the proof.

The gauge-orbit classification is a standard graph-theoretic Z2 holonomy fact. The EUI-specific consequence is the exact two-sector reduction of the complete cycle-exponential principal-minor convex-hull problem, including the zero-edge closure argument and its interaction with the Run 76 D42 quotient.

No complete N=42 moment ensemble, global separator, Choi trace-distance bound, or channel diamond-distance bound is established by this note.

## Reproduction

Run from the repository root:

    python -m py_compile verify_n42_cycle_z2_holonomy_gauge.py
    python verify_n42_cycle_z2_holonomy_gauge.py
    git diff --exit-code -- evidence/n42_cycle_z2_holonomy_gauge.json

The verifier uses only the Python standard library.
