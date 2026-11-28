# N=42 involution moment sum rules and complement reduction

Date: 2026-11-28. Run 75. Related: Issue #7 and the Run 74 mixed nonperiodic partial ensemble.

## Scope and notation

For the fixed even cycle, let
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j,
\]
with indices modulo 42, and define
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\qquad
R(c)=e^{A(c)},\qquad Q(c)=R(c)D.
\]
Since \(D A(c)D=-A(c)\), we have \(Q(c)^T=Q(c)\) and \(Q(c)^2=I\). To establish the trace condition explicitly, write the skew generator in even/odd block form
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},\qquad
D=\begin{pmatrix}I_{21}&0\\0&-I_{21}\end{pmatrix}.
\]
Every odd power of \(A\) is off diagonal. For \(k\ge0\),
\[
A^{2k}=(-1)^k\begin{pmatrix}(BB^T)^k&0\\0&(B^TB)^k\end{pmatrix},
\]
and
\[
\operatorname{tr}(A^{2k}D)
=(-1)^k\left[\operatorname{tr}(BB^T)^k-\operatorname{tr}(B^TB)^k\right]=0
\]
by cyclicity of trace (also for \(k=0\), since both blocks have size 21). Thus the power series gives \(\operatorname{tr}(e^A D)=0\). Consequently \(Q(c)\) has 21 eigenvalues \(+1\) and 21 eigenvalues \(-1\), and \(\det Q(c)=-1\).

The target used for the even principal minors of \(Q\) is
\[
\tau_I=(-1)^r\frac{\binom{21}{r}}{\binom{42}{2r}},
\qquad |I|=2r.
\]
In particular, the pair and quartic targets are \(-1/41\) and \(+1/533\).
This note concerns \(Q=RD\), not the un-gauged matrix \(R\).

## Theorem 1 — global principal-minor sum rules

For every real symmetric trace-zero involution \(Q\in\mathbb R^{42\times42}\),
\[
\boxed{
\sum_{|I|=2r}\det Q_{I,I}=(-1)^r\binom{21}{r},
\qquad r=0,1,\ldots,21.
}
\]
All odd-order sums vanish.

### Proof

The eigenvalues are 21 copies each of \(+1\) and \(-1\), so
\[
\det(I+tQ)=(1+t)^{21}(1-t)^{21}=(1-t^2)^{21}.
\]
On the other hand, the principal-minor expansion gives
\[
\det(I+tQ)=
\sum_{k=0}^{42}t^k\sum_{|I|=k}\det Q_{I,I}.
\]
Comparing coefficients of \(t^{2r}\) proves the identity; odd coefficients are zero.

The target is constant over all subsets of a fixed even size. Hence
\[
\binom{42}{2r}\tau_I=(-1)^r\binom{21}{r},
\]
so its aggregate agrees exactly with the value forced by the involution for every atom. Consequently every probability mixture of physical atoms automatically matches the all-ones aggregate direction at each even order. The remaining moment problem is entirely in the coordinate fluctuations around that fixed aggregate.

## Theorem 2 — complementary principal minors

For every subset \(I\subseteq[42]\),
\[
\boxed{\det Q_{I,I}=-\det Q_{I^c,I^c}.}
\]

### Proof

Jacobi's complementary-minor identity states
\[
\det Q_{I,I}
=\det Q\,\det (Q^{-1})_{I^c,I^c}
\]
for a principal minor. Here \(Q^{-1}=Q\) and \(\det Q=-1\), giving the result.

The target obeys the same relation:
\[
\tau_{42-2r}=-\tau_{2r},
\]
because
\[
(-1)^{21-r}\binom{21}{21-r}
=-(-1)^r\binom{21}{r}.
\]
Therefore matching all even principal-minor coordinates of orders
\[
0,2,4,\ldots,20
\]
automatically matches the complementary orders
\[
42,40,38,\ldots,22.
\]
The full even-order hierarchy has only eleven distinct degree levels, not twenty-two.

## Corollary — exact reduction of cyclic-orbit constraints

For a cyclic-orbit measure, let \(m_{\mathcal O}\) denote the mean principal minor over a translation orbit \(\mathcal O\) of subsets of a fixed size. Theorem 1 implies
\[
\boxed{
\sum_{\mathcal O}|\mathcal O|
\left(m_{\mathcal O}-\tau_{|\mathcal O|}\right)=0
}
\]
at every even order. Thus, once probability normalization is imposed, one weighted orbit equation per degree is redundant.

At degree four, exact bit-mask enumeration gives:
- 2,670 cyclic translation orbits;
- orbit sizes 21 (10 orbits) and 42 (2,660 orbits);
- 111,930 four-subsets covered;
- only 2,669 independent quartic orbit coordinates after the global sum rule.

At degree two there are 21 cyclic orbits: one of size 21 (opposite pairs) and twenty of size 42. The global pair sum is \(-21\), equivalently
\[
2\sum_{d=1}^{20}p_d+p_{21}=-1.
\]

**Important normalization caveat.** Run 74's 21 pair equations imply that its 30 weights sum to one through the pair identity. If a future LP drops one pair equation, it must add an explicit weight-sum equation. For quartic constraints, the pair equations already provide normalization, so one quartic orbit equation may be omitted without changing feasibility.

## Relation to Run 74

Run 74 constructed a 220-atom strictly-positive physical ensemble matching all 861 pair coordinates and 357 quartic coordinates in nine translation orbits. The present sum rules explain which aggregate constraints are automatic and provide an exact reduction for the next quartic-orbit cutting-plane search. They do not repair the two Run 74 quartic misses and do not imply that the full cycle-family target is feasible.

## Reproducibility

- Exact standard-library verifier: `verify_n42_involution_moment_sum_rules.py`
- Machine certificate: `evidence/n42_involution_moment_sum_rules.json`
- Workflow: `.github/workflows/eui-n42-involution-moment-sum-rules.yml`

The verifier recomputes all 22 exact rational target levels, the complement sign relation, and the complete cyclic-orbit partitions for pairs and quartets. It does not numerically sample a matrix exponential; the universal identities are proved above.

## Scope and novelty boundary

The characteristic-polynomial and Jacobi identities are standard linear algebra, not claimed as a new general theorem. The EUI-specific contribution is the exact reduction of the fixed-cycle balanced-slice moment hierarchy and the corresponding count of independent cyclic quartic constraints. No convex-hull feasibility or operational channel-distance conclusion follows from this reduction.
