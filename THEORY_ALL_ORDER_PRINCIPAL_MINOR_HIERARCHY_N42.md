# All-order principal-minor incidence hierarchy and the N=42 orbit-rank audit

Date: 2026-11-27. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), [fourth/second hierarchy](THEORY_FOURTH_MOMENT_HIERARCHY.md), [sixth-order audit](THEORY_SIXTH_MOMENT_AUDIT.md), and [N=42 perfect-matching target](THEORY_PERFECT_MATCHING_BALANCED_SLICE_ENSEMBLE_N42.md).

## Result and scope

This note extends the repository's fourth/second and sixth/fourth principal-minor identities to every adjacent even order. It also proves the exact rank of each corresponding dihedral-orbit incidence map and computes its N=42 orbit counts.

The N=42 reduction to 20 pair coordinates, 1,293 quartic coordinates, and normalization (1,314 equations) is only the first two levels of the all-order hierarchy. After imposing only the consecutive odd-to-even incidence identities and complementary-minor reduction, **3,204,236,778** D_42-orbit coordinates remain across orders 2 through 20. This is not a claim that all remaining coordinates are algebraically independent; further determinant identities or physical constraints may reduce them. It does establish that the 1,314-row second/fourth system is not a full all-even-moment certificate.

The determinant-generating identity and its degree-4/6 special cases already appear in the repository. No novelty is claimed for those ingredients. The contribution here is the all-order formulation, invariant-subspace rank proof, and exact N=42 dimension audit.

## 1. All-order adjacent incidence identity

Let \(N=2n\), and let \(Q\in\mathbb R^{N\times N}\) satisfy
\[
Q=Q^{\mathsf T},\qquad Q^2=I,\qquad \operatorname{tr}Q=0.
\]
Thus Q has n eigenvalues +1 and n eigenvalues -1. Write \(Q_I=Q_{I,I}\).

**Theorem 1 (odd-to-even principal-minor incidence).** For every odd-cardinality subset S, with \(|S|=s\),
\[
\boxed{\sum_{\substack{I\supset S\\|I|=s+1}}\det Q_I
=-\sum_{\substack{J\subset S\\|J|=s-1}}\det Q_J.}
\tag{1}
\]
For s=1, the right side is minus the empty minor, namely -1.

**Proof.** The principal-minor generating identity is
\[
\sum_{I\supseteq S}t^{|I|}\det Q_I
=\det(I+tQ)\det[tQ(I+tQ)^{-1}]_{S,S}.
\tag{2}
\]
It follows by differentiating \(\det(I+t\,\mathrm{diag}(x)Q)\) once in each \(x_i\), \(i\in S\), at \(x_i=1\). Since Q is a balanced symmetric involution,
\[
\det(I+tQ)=(1-t^2)^n,\qquad
tQ(I+tQ)^{-1}=\frac{tQ-t^2I}{1-t^2}.
\]
Hence
\[
\sum_{I\supseteq S}t^{|I|}\det Q_I
=t^s(1-t^2)^{n-s}\det(Q_S-tI_s).
\tag{3}
\]
The coefficient of \(t^{s+1}\), for odd s, is the coefficient of t in \(\det(Q_S-tI_s)\), namely minus the sum of the \((s-1)\)-principal minors of Q_S. This proves (1). \(\square\)

For the EUI cycle family, \(D=\mathrm{diag}(1,-1,\ldots,1,-1)\), \(R=e^{A(c)}\), and \(Q=RD\). Bipartite anticommutation \(DAD=-A\) gives \(Q=Q^{\mathsf T}\), \(Q^2=I\), and \(\operatorname{tr}Q=0\), so (1) holds for every physical atom and every mixture.

## 2. Balanced target and normalized error propagation

For N=2n, the balanced-slice target in Q-coordinates is
\[
\tau_{2r}=(-1)^r a_r,\qquad
a_r=\frac{\binom nr}{\binom{2n}{2r}}.
\]
For s=2r-1 it satisfies
\[
(2n-2r+1)\tau_{2r}=-(2r-1)\tau_{2r-2},
\tag{4}
\]
by the binomial identity
\[
(2n-2r+1)\frac{\binom nr}{\binom{2n}{2r}}
=(2r-1)\frac{\binom n{r-1}}{\binom{2n}{2r-2}}.
\]
Thus the target itself obeys every identity (1).

For a normalized ensemble, define
\[
F_{2r}(I)=\frac{\mathbb E\det Q_I-\tau_{2r}}{a_r}.
\]
Subtracting (4) from (1), and using \(a_{r-1}/a_r=(2n-2r+1)/(2r-1)\), gives
\[
\boxed{
\frac1{2n-2r+1}\sum_{\substack{I\supset S\\|I|=2r}}F_{2r}(I)
=-\frac1{2r-1}\sum_{\substack{J\subset S\\|J|=2r-2}}F_{2r-2}(J).
}
\tag{5}
\]
A uniform bound \(|F_{2r-2}(J)|\le\epsilon\) therefore bounds each signed average on the left by epsilon, but does not bound each individual higher-order error. This is the all-order form of the limitation recorded in the sixth-moment audit.

## 3. Exact rank of the dihedral orbit-incidence map

Let \(V_k\) be the real functions on k-subsets. Define the up operator
\[
(U_k f)(T)=\sum_{\substack{S\subset T\\|S|=k}}f(S),\quad |T|=k+1,
\]
and let \(D_{k+1}=U_k^{\mathsf T}\) be the down/incidence operator. Direct counting gives the Boolean-lattice commutator
\[
D_{k+1}U_k-U_{k-1}D_k=(N-2k)I_{V_k}.
\tag{6}
\]
Consequently
\[
\|U_k f\|^2=\|D_k f\|^2+(N-2k)\|f\|^2.
\tag{7}
\]
For k<N/2, U_k is injective, so D_{k+1}:V_{k+1}\to V_k is surjective.

The dihedral action commutes with incidence. Surjectivity persists on invariant subspaces: if y is invariant and D_{k+1}x=y, average x over D_N; its image remains y. Since the dimension of \(V_k^{D_N}\) is the number \(O_k\) of D_N-orbits of k-subsets, we obtain:

**Theorem 2.** For every k<N/2, the D_N-orbit incidence matrix from (k+1)-subset orbits to k-subset orbits has rank exactly \(O_k\).

This proves full row rank 147 for the existing N=42 triple/quartet incidence reduction. The previously stored integer pivot determinant remains an independent finite certificate.

## 4. N=42 orbit counts and residual coordinates

For even N, Burnside's lemma gives
\[
O_k=\frac1{2N}\left[
\sum_{q=0}^{N-1}{\bf1}_{L_q\mid k}\binom{\gcd(N,q)}{k/L_q}
+\frac N2(V_k+E_k)\right],
\]
where \(L_q=N/\gcd(N,q)\), \(\gcd(N,0)=N\), and
\[
V_k=\sum_{j=0}^{(N-2)/2}\binom{(N-2)/2}{j}\binom2{k-2j},
\qquad
E_k={\bf1}_{2\mid k}\binom{N/2}{k/2}.
\]
The two reflection terms are for axes through opposite vertices and opposite edges.

For N=42, Jacobi's complementary-minor identity gives
\[
\det Q_I=\det(Q)\det Q_{I^c}=-\det Q_{I^c},
\tag{8}
\]
so only orders 2,4,...,20 need be retained; empty and full moments are fixed. The exact orbit counts are:

| Even order m | Odd-subset orbits O_(m-1) | Even-subset orbits O_m | Incidence rank | Coordinates left |
|---:|---:|---:|---:|---:|
| 2 | 1 | 21 | 1 | 20 |
| 4 | 147 | 1,440 | 147 | 1,293 |
| 6 | 10,222 | 63,133 | 10,222 | 52,911 |
| 8 | 321,741 | 1,408,185 | 321,741 | 1,086,444 |
| 10 | 5,310,667 | 17,527,595 | 5,310,667 | 12,216,928 |
| 12 | 50,966,816 | 131,672,051 | 50,966,816 | 80,705,235 |
| 14 | 303,813,800 | 629,347,967 | 303,813,800 | 325,534,167 |
| 16 | 1,174,710,565 | 1,982,362,758 | 1,174,710,565 | 807,652,193 |
| 18 | 3,031,752,594 | 4,210,830,549 | 3,031,752,594 | 1,179,077,955 |
| 20 | 5,318,837,680 | 6,116,747,312 | 5,318,837,680 | 797,909,632 |

Across orders 2 through 20:
- orbit coordinates before these incidence reductions: **13,089,961,011**;
- independent adjacent-incidence equations: **9,885,724,233**;
- residual coordinates after these equations: **3,204,236,778**.

At orders 2 and 4 this gives
\[
(21-1)+(1440-147)+1=1314
\]
equations including normalization, exactly the reduced system used by the N=42 second/fourth workflows. For N=10 the same count gives 4 pair coordinates and 8 quartic coordinates, explaining the 12 moment coordinates plus normalization in the certified 13-by-13 construction.

The residual count is exact for the linear subspace defined by these adjacent incidence identities and complement symmetry alone. It is not a claim that all residual coordinates are algebraically independent or that additional identities cannot reduce them.

## 5. Exact verification and reproduction

Run:

    python -m py_compile verify_all_order_principal_minor_hierarchy.py
    python verify_all_order_principal_minor_hierarchy.py

The dependency-free verifier:
1. computes N=42 orbit counts with exact Burnside sums;
2. compares Burnside counts with explicit D_N orbit enumeration for every subset size at N=4,6,8,10,12;
3. computes restricted orbit-incidence ranks over exact rational arithmetic for all odd k<N/2 at those sizes;
4. constructs rational orthogonal O, sets Q=ODO^T, and checks every identity (1) for every odd subset at N=4,6,8,10 using exact Fraction determinants;
5. checks all ten N=42 target identities (4) exactly.

Machine output: [evidence/all_order_principal_minor_hierarchy_n42.json](evidence/all_order_principal_minor_hierarchy_n42.json). The N=42 rank statement is proved by (6)-(7) and group averaging; small exact ranks are regression checks, not the proof.

## 6. Scientific consequence and next step

The 1,314-row N=42 second/fourth system is an exact and useful low-order relaxation, but cannot be promoted to the complete all-even-principal-minor design. The hierarchy gives signed averages of higher-order errors, not pointwise control. This is consistent with the sixth-order counterexamples already recorded in THEORY_SIXTH_MOMENT_AUDIT.md.

The next high-value step is to find additional structure controlling the residual higher-order coordinates, most naturally through the complement-folded projection-DPP representation or a genuinely global physical-family inequality. This note establishes no N=42 positive all-moment ensemble, global physical separator, or Choi/diamond-distance consequence.
