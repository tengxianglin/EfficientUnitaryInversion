# N=42 path-perfect-transfer 1-factorization: pair-optimal, but far from the target

Date: 2026-11-28. Run 72. Related: Issue #7; Run 71 local sixth-harmonic pricing oracle.

## Result and scope

The Run 71 follow-up proposed a pair-balanced mixture of non-periodic path/block perfect-transfer atoms. This note constructs the natural exact design and resolves what it can and cannot do.

**Construction.** Twenty-one cyclic translates of one engineered 42-site path-perfect-transfer atom form a 1-factorization of the complete bipartite graph \(K_{21,21}\) between even and odd sites. Each atom is a physical cycle exponential when zero couplings are allowed. The equal mixture makes every even--odd matching edge occur with probability \(1/21\), and every same-parity edge with probability zero.

**No-go.** This is the unique pair-marginal minimizer among *all* mixtures of bipartite perfect-matching atoms, but it cannot match the balanced-slice target: its pair character moments are \(0\) on same-parity pairs and \(-1/21\) on cross-parity pairs, whereas the target is \(-1/41\) on every pair. The minimum squared degree-two residual norm is exactly \(20/41\), giving the universal matching-subfamily bound
\[
\boxed{\chi^2(q\Vert u)\ge \frac{13}{28}.}
\]

For the explicit 21-atom 1-factorization mixture, the *full* program-label divergence is much larger and can be computed exactly:
\[
\boxed{
\chi^2(q\Vert u)
=\frac{839949975821189}{68719476736}
\approx 12222.88084421873.
}
\]
A support-size argument also gives
\[
\boxed{
\operatorname{TV}(q,u)\ge
\frac{22425576427}{22427411435}
\approx0.9999181801250082.
}
\]
These are classical program-label distribution statements, not Choi trace-distance or diamond-distance bounds.

The result closes the proposed matching-design branch: no reweighting of physically reachable signed matching atoms can solve the full target. The next search must include non-permutation cycle exponentials.

## 1. Twenty-one path-transfer atoms form a 1-factorization

Let \(E_a=2a\) and \(O_b=2b+1\), with \(a,b\in\mathbb Z_{21}\). On the open path with vertices \(0,\ldots,41\), take
\[
c_j^*=\frac{\pi}{4}\sqrt{(j+1)(41-j)},\quad j=0,\ldots,40,
\qquad c_{41}^*=0.
\]
The standard engineered-chain perfect-transfer identity (Christandl et al., *Phys. Rev. Lett.* **92**, 187902 (2004), DOI [10.1103/PhysRevLett.92.187902](https://doi.org/10.1103/PhysRevLett.92.187902)) gives
\[
R^*e_j=(-1)^j e_{41-j}.
\]
For \(D=\operatorname{diag}(1,-1,\ldots,1,-1)\), the involution \(Q^*=R^*D\) is the unsigned reversal permutation, with matching
\[
M_0=\{\{i,41-i\}:i=0,\ldots,20\}.
\]

Translate the path atom by \(2t\) sites, \(t=0,\ldots,20\). Since an even translation commutes with \(D\), its involution is the matching
\[
M_t=\bigl\{\{2a,\,2(20-a+2t)+1\}:a\in\mathbb Z_{21}\bigr\}.
\]
Equivalently, \(E_a\) is matched to \(O_{20-a+2t}\). For fixed \(a\), the value \(20-a+2t\) runs through all of \(\mathbb Z_{21}\), because \(2\) is invertible modulo \(21\). Therefore every one of the \(21^2=441\) even--odd edges appears in exactly one \(M_t\). The \(M_t\) are distinct perfect matchings and form a 1-factorization of \(K_{21,21}\).

Each \(M_t\) has exactly two physical cycle edges, the translates of \(\{0,41\}\) and \(\{20,21\}\). All other path couplings are positive; one translated closing-edge coupling is zero. Thus these atoms belong to the real-coupling cycle family stated in Issue #7. If the intended physical domain is strictly positive on every edge, these exact atoms are boundary points; a positive-edge perturbation is only approximate and does not preserve the exact matching formulas.

## 2. Pair moments and the exact pair-level minimax

For a matching involution \(Q=P_M\), the rank-21 projector
\[
P=\frac{I+Q}{2}
\]
is a direct sum of 21 rank-one blocks \(\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}\). Its projection-DPP law chooses exactly one endpoint from each matching edge, independently and uniformly. Thus \(q_M\) is uniform on the \(2^{21}\) transversals of \(M\).

For \(I=\{i,j\}\), the balanced-sign character moment is
\[
\mathbb E_{q_M}[x_ix_j]=\det Q_{I,I}
=\begin{cases}-1,&\{i,j\}\in M,\\0,&\{i,j\}\notin M.\end{cases}
\]
The equal 1-factorization mixture consequently has
\[
\mathbb E_q[x_ix_j]=
\begin{cases}
0,&i,j\text{ have the same parity},\\
-1/21,&i,j\text{ have opposite parity}.
\end{cases}
\]
The uniform balanced-slice target has \(\mathbb E_u[x_ix_j]=-1/41\) for every pair. There are 420 same-parity pairs and 441 cross-parity pairs, so the explicit mixture's degree-two residual obeys
\[
\|\delta_2\|_2^2
=420\left(\frac1{41}\right)^2
+441\left(\frac1{41}-\frac1{21}\right)^2
=\frac{20}{41}.
\]

More generally, let \(p_{ab}\) be the probability that an arbitrary mixture of bipartite perfect matchings uses edge \(E_aO_b\). The matrix \(p\) is doubly stochastic. Its pair residual norm is
\[
\|\delta_2\|_2^2
=\frac{420}{41^2}
+\sum_{a,b=0}^{20}\left(p_{ab}-\frac1{41}\right)^2.
\]
Since \(\sum_{a,b}p_{ab}=21\),
\[
\sum_{a,b}\left(p_{ab}-\frac1{41}\right)^2
=\sum_{a,b}\left(p_{ab}-\frac1{21}\right)^2
+441\left(\frac1{21}-\frac1{41}\right)^2.
\]
Hence
\[
\boxed{\|\delta_2\|_2^2\ge\frac{20}{41},}
\]
with equality iff \(p_{ab}=1/21\) for all \(a,b\). The 21 translated path atoms attain equality. This proves pair-level optimality over the entire bipartite-matching subfamily, not just over the chosen cyclic orbit.

## 3. Convert the pair residual into a chi-square lower bound

For every balanced sign vector \(x\), and each fixed \(i\),
\[
\sum_{j\ne i}x_ix_j=-1.
\]
Therefore the degree-two residual satisfies the down relation \(D_2\delta_2=0\), i.e. every row sum of its pair-coefficient array is zero.

The uniform balanced-slice character Gram kernel on pairs is
\[
K_{I,J}=\mathbb E_u[f_I f_J]=\mu_{4-2|I\cap J|},
\qquad
(\mu_0,\mu_2,\mu_4)=\left(1,-\frac1{41},\frac1{533}\right).
\]
For any coefficient array \(a\) with zero row sums, the sum over \(J\) sharing exactly one vertex with fixed \(I=\{i,j\}\) is \(-2a_I\), and the sum over disjoint \(J\) is \(a_I\). Consequently
\[
Ka=\left(\mu_0-2\mu_2+\mu_4\right)a
=\frac{560}{533}a.
\]
Cauchy--Schwarz in the chi-square inner product, with \(a=\delta_2\), yields
\[
\chi^2(q\Vert u)\ge
\frac{\|\delta_2\|_2^2}{560/533}
\ge \frac{20}{41}\frac{533}{560}
=\boxed{\frac{13}{28}}.
\]
The bound applies to every probability mixture supported on physically reachable matching atoms, because the cycle-reachability theorem in THEORY_CYCLE_MATCHING_ATOM_REACHABILITY_N42.md proves that every such atom is bipartite. It is not a bound for arbitrary non-permutation cycle exponentials.

## 4. Exact full chi-square of the 21-atom design

For two perfect matchings \(M_t,M_s\), their union is a disjoint union of alternating even cycles (a common matching edge is a two-vertex component). Following two alternating edges maps
\[
E_a\longmapsto E_{a+2(s-t)}.
\]
Thus the number of connected components is
\[
c(t,s)=\gcd(21,2(s-t))=\gcd(21,t-s).
\]
A common transversal must alternate around each component, giving exactly \(2^{c(t,s)}\) common transversals. Since each \(q_{M_t}\) assigns probability \(2^{-21}\) to each of its transversals,
\[
\sum_S q(S)^2
=\frac1{21^2}\sum_{t,s}2^{c(t,s)-42}
=\frac{1}{21\cdot2^{42}}
\sum_{r=0}^{20}2^{\gcd(21,r)}.
\]
The exact divisor count is
\[
\sum_{r=0}^{20}2^{\gcd(21,r)}
=2^{21}+12\cdot2+6\cdot8+2\cdot128
=2,097,480=21\cdot99,880.
\]
Therefore
\[
\sum_Sq(S)^2=\frac{99,880}{2^{42}}.
\]
With \(d=\binom{42}{21}=538,257,874,440\),
\[
\chi^2(q\Vert u)=d\sum_Sq(S)^2-1
=\boxed{\frac{839949975821189}{68719476736}}.
\]
The complement-folded Plücker frame-potential identity gives
\[
\mathrm{FP}=4\sum_Sq(S)^2
=\boxed{\frac{12485}{137438953472}}.
\]

Finally, each of the 21 atoms has \(2^{21}\) transversals, so the support of their mixture has size at most \(21\cdot2^{21}=44,040,192\). The uniform target is supported on all \(d\) balanced labels. Hence
\[
\operatorname{TV}(q,u)\ge1-\frac{21\cdot2^{21}}{\binom{42}{21}}
=\boxed{\frac{22425576427}{22427411435}}.
\]
The support bound is deliberately conservative; no exact support-union count is needed.

## 5. Consequence for Issue #7

The suggested pair-balanced matching-design search is now resolved:

- a physical 21-atom 1-factorization exists and exactly minimizes the degree-two residual over all reachable matching atoms;
- it still misses the target pair moments by an unavoidable amount, with \(\chi^2\ge13/28\) for every matching-only mixture;
- the explicit design has exact full \(\chi^2\approx1.2223\times10^4\) and program-label TV at least \(0.999918\).

Therefore no reweighting, 1-factorization, or other mixture of signed perfect-matching atoms can solve Issue #7. Further effort should target genuinely non-permutation matrices \(e^{A(c)}D\), with pair constraints enforced while pricing the Run 70/71 harmonic coordinates.

## Reproducibility

- Exact verifier: verify_n42_path_matching_1_factorization_pair_minimax.py
- Machine certificate: evidence/n42_path_matching_1_factorization_pair_minimax.json
- CI workflow: .github/workflows/eui-n42-path-matching-pair-minimax.yml
- Run audit: MANUSCRIPT_AUDIT_ADDENDUM_RUN72_2026-11-28.md

The verifier uses only Python's standard library and recomputes the 21 matchings, the 441-edge factorization, all 441 ordered matching-pair union component counts, the rational pair minimax, the full chi-square, frame potential, and support-TV bound.
