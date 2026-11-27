# Exact cycle-edge count distribution of the uniform perfect-matching ensemble

Date: 2026-11-28. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7) and [the physical-matching adjacent-pair obstruction](THEORY_PHYSICAL_MATCHING_ENSEMBLE_ADJACENT_PAIR_OBSTRUCTION_N42.md).

## Result and scope

Let \(C_N\) be the fixed physical Hamiltonian cycle on \(N=2n\) labelled vertices, and let \(M\) be uniform over the \((N-1)!!\) perfect matchings of the complete graph \(K_N\). Define
\[
X_N(M)=|M\cap E(C_N)|,
\]
the number of matching edges that are also physical cycle edges.

The existing reachability theorem proves that, for \(N=4m+2\ge 6\), every perfect-matching atom \(R_M=P_MD\) that is reachable as \(e^{A(c)}\) by a real skew generator supported on \(C_N\) must satisfy \(X_N(M)\ge2\).

This note gives the **exact distribution** of \(X_N\), quantifies how much of the unrestricted uniform matching representation is therefore excluded from physical matching-atom support, and proves a Poisson(1) limit. It does not extend the reachability theorem from matching permutations to general cycle exponentials.

## 1. Exact distribution by binomial inversion

Let \(m_k(C_N)\) be the number of \(k\)-edge matchings of the cycle. For \(0\le k\le n\),
\[
m_k(C_N)=
\begin{cases}
1,&k=0,\\[2mm]
\displaystyle\frac{N}{N-k}\binom{N-k}{k},&k\ge1.
\end{cases}
\tag{1}
\]
For \(k\ge1\), this follows by choosing \(k\) cyclically ordered selected edges with positive gaps between consecutive selected edges: the \(k\) gaps sum to \(N-k\). Counting rooted selections and dividing by the \(k\) possible roots gives \(N\binom{N-k-1}{k-1}/k\), equal to (1).

For a fixed set of \(k\) pairwise-disjoint cycle edges, the number of perfect matchings of \(K_N\) containing all of them is \((N-2k-1)!!\), with \((-1)!!=1\). Therefore the unnormalized binomial moments are
\[
B_k:=\sum_{M\in\mathcal M_N}\binom{X_N(M)}{k}
=m_k(C_N)(N-2k-1)!!.
\tag{2}
\]
Writing \(C_j=\#\{M:X_N(M)=j\}\), binomial inversion gives the exact count
\[
\boxed{
C_j=\sum_{k=j}^{n}(-1)^{k-j}\binom{k}{j}
m_k(C_N)(N-2k-1)!!,\qquad 0\le j\le n.
}
\tag{3}
\]
This is an integer identity; no floating-point computation is involved.

## 2. N=42 exact count

For \(N=42\),
\[
|\mathcal M_{42}|=41!!
=13113070457687988603440625.
\]
Equation (3) gives
\[
\begin{aligned}
C_0&=4649413893260078385217444,\\
C_1&=4878759342216072267293262.
\end{aligned}
\]
Thus
\[
\boxed{
\Pr_{\mathrm{unif}}(X_{42}\le1)
=\frac{9528173235476150652510706}
{13113070457687988603440625}
=0.7266164904871636\ldots .
}
\tag{4}
\]

Every physically reachable matching atom has \(X_{42}\ge2\). Hence at least 72.66% of the unrestricted uniform perfect-matching atoms are individually unreachable. At most
\[
1-\Pr(X_{42}\le1)
=\frac{3584897222211837950929919}
{13113070457687988603440625}
=0.2733835095128364\ldots
\]
of the matching atoms even pass this necessary edge-count test. Passing it is not sufficient for physical reachability.

A measure-level corollary is immediate. If \(\nu\) is any probability measure supported on physically reachable matching atoms, then \(\nu(\{X\le1\})=0\), so
\[
\boxed{
\|\nu-\mathrm{Unif}(\mathcal M_{42})\|_{\mathrm{TV}}
\ge \Pr_{\mathrm{unif}}(X_{42}\le1).
}
\tag{5}
\]
This TV distance is between probability measures on the discrete matching-atom space. It is not a program-label, Choi, or diamond-distance statement.

The existing moment-space separator remains complementary: for \(Q=P_M\),
\[
\Lambda(Q)=-\sum_{j=0}^{N-1}\det Q_{\{j,j+1\}}=X_N(M).
\]
Physical matching atoms have \(\Lambda\ge2\), whereas the balanced-slice target has \(\Lambda=N/(N-1)\). At N=42 the exact moment-functional gap is \(40/41\).

## 3. Poisson(1) limit

For fixed \(k\), (2) gives
\[
\mathbb E[(X_N)_k]
=k!\,m_k(C_N)\frac{(N-2k-1)!!}{(N-1)!!},
\tag{6}
\]
where \((x)_k=x(x-1)\cdots(x-k+1)\). Using (1), for every fixed \(k\),
\[
\mathbb E[(X_N)_k]\longrightarrow1
\qquad(N\to\infty,\ N\ \mathrm{even}).
\]
These are the factorial moments of a Poisson random variable of mean one. The factorial-moment method therefore yields
\[
X_N\xrightarrow{\ d\ }\operatorname{Poisson}(1),
\qquad
\boxed{\Pr(X_N\le1)\longrightarrow 2e^{-1}.}
\tag{7}
\]
The limiting excluded mass is \(2/e=0.7357588823428847\ldots\); the N=42 exact value in (4) is already 0.7266.

## 4. Exact verification

Run:
\`\`\`bash
python -m py_compile verify_perfect_matching_cycle_edge_distribution.py
python verify_perfect_matching_cycle_edge_distribution.py
\`\`\`

The dependency-free verifier:
1. computes (1)–(3) using Python integers;
2. checks the binomial-inversion identities and total \((N-1)!!\);
3. independently enumerates every perfect matching for N=4,6,8,10,12,14 and compares the complete edge-count distribution;
4. freezes the complete N=42 distribution, the exact \(X\le1\) mass, and the first six factorial moments.

Machine evidence: [evidence/perfect_matching_cycle_edge_distribution_n42.json](evidence/perfect_matching_cycle_edge_distribution_n42.json).

## 5. Scope boundary

**Proved:** exact matching-count distribution; the N=42 72.66% support-exclusion fraction for physically reachable matching atoms; the TV lower bound (5) on the discrete matching space; and the Poisson(1) asymptotic.

**Not proved:** that arbitrary physical cycle exponentials \(e^{A(c)}\) must satisfy the matching-atom functional \(\Lambda\ge2\); that the complete cycle-exponential convex hull excludes the balanced target; or any Choi/diamond-distance consequence. Issue #7 remains open.
