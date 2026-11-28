# Exact minimax obstruction for all bipartite perfect-matching mixtures (N=42)

Date: 2026-11-28. Run 73. Related: Issue #7; Run 72 matching-only pair minimax.

## Theorem and scope

Let \(N=2n\), with a fixed bipartition \(E\sqcup O\), \(|E|=|O|=n\). A bipartite perfect matching \(M\) defines a program-label law \(q_M\) that is uniform on the \(2^n\) transversals of \(M\): a label contains exactly one endpoint of each matched edge. This is the projection-DPP law of the signed matching involution; the signs do not change its transversal probabilities.

Let \(u\) be uniform on the balanced slice \(\Omega_{2n,n}\), so \(u(S)=1/\binom{2n}{n}\). For any probability mixture \(q=\sum_M w_Mq_M\) over bipartite perfect matchings, define
\[
\chi^2(q\Vert u)=\sum_{S\in\Omega_{2n,n}}\frac{(q(S)-u(S))^2}{u(S)},
\qquad
\operatorname{TV}(q,u)=\frac12\sum_S|q(S)-u(S)|.
\]

**Theorem.** The unique output law minimizing \(\chi^2(q\Vert u)\) over the full convex hull of bipartite matching-transversal laws is the uniform mixture over all \(n!\) bipartite matchings. It also minimizes total variation. Its probability at a fixed balanced label \(S\), with \(k=|S\cap E|\), is
\[
q_*(S)=\frac{1}{2^n\binom nk}.
\]
Consequently every bipartite matching mixture obeys
\[
\boxed{\chi^2(q\Vert u)\ge (n+1)\frac{\binom{2n}{n}}{4^n}-1,}
\]
and
\[
\boxed{\operatorname{TV}(q,u)\ge
\frac12\sum_{k=0}^n\left|
\frac{\binom nk}{2^n}-\frac{\binom nk^2}{\binom{2n}{n}}
\right|.}
\]
The chi-square minimizer is unique as an output distribution. The TV minimum is attained by the same symmetrized law, though TV need not have a unique minimizer.

For \(n=21\),
\[
\boxed{\chi^2(q\Vert u)\ge
\frac{465226670411}{274877906944}
\approx1.6924847674490593,}
\]
\[
\boxed{\operatorname{TV}(q,u)\ge
\frac{452040940614809}{2713482158407680}
\approx0.1665907178398677.}
\]
These improve the earlier pair-harmonic \(13/28\) chi-square floor and the unrelated finite-pool \(1/5330\) TV floor, but apply only to mixtures of matching atoms.

## Proof

The group \(G=S_E\times S_O\) acts on labels by permuting even and odd vertices separately. It preserves the uniform balanced-slice law \(u\), and it acts transitively on the set of all bipartite perfect matchings (which are exactly bijections \(E\to O\)). If \(q=\sum_Mw_Mq_M\) is any matching mixture, its group symmetrization is
\[
\bar q=\frac1{|G|}\sum_{g\in G}g\cdot q.
\]
Because the action is transitive on matchings, \(\bar q\) is exactly the uniform mixture over all \(n!\) bipartite matchings. Convexity and invariance give
\[
\operatorname{TV}(\bar q,u)
\le\frac1{|G|}\sum_g\operatorname{TV}(g\cdot q,u)
=\operatorname{TV}(q,u),
\]
and, since \(\chi^2(q\Vert u)=\sum_Sq(S)^2/u(S)-1\),
\[
\chi^2(\bar q\Vert u)
\le\frac1{|G|}\sum_g\chi^2(g\cdot q\Vert u)
=\chi^2(q\Vert u).
\]
Strict convexity of \(\sum_Sq(S)^2/u(S)\) makes \(\bar q\) the unique minimizing output law for chi-square.

Now fix a balanced label \(S\) and put \(k=|S\cap E|\). For \(S\) to be a transversal of a matching, the \(k\) even vertices in \(S\) must be matched to the \(k\) odd vertices outside \(S\), and the remaining \(n-k\) even vertices must be matched to the \(n-k\) odd vertices in \(S\). The number of such matchings is \(k!(n-k)!\). Therefore
\[
q_*(S)=\frac{k!(n-k)!}{n!2^n}
=\frac{1}{2^n\binom nk}.
\]
There are \(\binom nk^2\) balanced labels with exactly \(k\) even vertices. Thus the orbit masses are
\[
q_*(k)=\frac{\binom nk}{2^n},\qquad
u(k)=\frac{\binom nk^2}{\binom{2n}{n}}.
\]
It follows that
\[
\sum_S\frac{q_*(S)^2}{u(S)}
=\frac{\binom{2n}{n}}{4^n}\sum_{k=0}^n1
=(n+1)\frac{\binom{2n}{n}}{4^n},
\]
which gives the chi-square formula. The TV formula follows by grouping the absolute difference by \(k\). This completes the proof.

## N=42 exact specialization

For \(n=21\), \(\binom{42}{21}=538257874440\). The sign of \(q_*(k)-u(k)\) is positive for \(k\in\{0,\ldots,8,13,\ldots,21\}\) and negative for \(k\in\{9,10,11,12\}\). Hence an equivalent exact TV expression is
\[
2\sum_{k=0}^{8}\left[
\frac{\binom{21}{k}}{2^{21}}-
\frac{\binom{21}{k}^2}{\binom{42}{21}}
\right]
=\frac{452040940614809}{2713482158407680}.
\]
The exact chi-square expression is
\[
22\frac{\binom{42}{21}}{2^{42}}-1
=\frac{465226670411}{274877906944}.
\]

## Relation to the cycle-exponential family

The existing analytic reachability theorem \`THEORY_CYCLE_MATCHING_ATOM_REACHABILITY_N42.md\` proves that every signed perfect-matching atom equal to \(e^{A(c)}\) on the 42-cycle must be bipartite. The present inequalities therefore apply to every probability measure supported only on cycle-reachable perfect-matching atoms, including any subset of the bipartite matching family.

The minimizer \(q_*\) is attained in the *full bipartite matching convex hull* by averaging all \(21!\) matchings. This note does **not** claim that all those matchings are cycle-reachable, nor that \(q_*\) is attainable by the cycle-exponential subfamily. Thus the displayed values are universal lower bounds for the physical matching-only subfamily, not necessarily its sharp minima.

The theorem says nothing about non-permutation matrices \(e^{A(c)}D\). Those are precisely the remaining escape route for Issue #7. No Choi trace-distance or channel diamond-distance conclusion follows from these classical program-label divergences.

## Reproducibility

- Dependency-free exact verifier: \`verify_n42_bipartite_matching_minimax.py\`
- Machine-readable exact certificate: \`evidence/n42_bipartite_matching_minimax.json\`
- CI workflow: \`.github/workflows/eui-n42-bipartite-matching-minimax.yml\`

The verifier explicitly enumerates every bipartite matching and every transversal for \(n=1,\ldots,5\), checks the closed-form law label-by-label, and independently recomputes the exact chi-square and TV values. The \(n=21\) constants are then evaluated using exact integer and rational arithmetic.
