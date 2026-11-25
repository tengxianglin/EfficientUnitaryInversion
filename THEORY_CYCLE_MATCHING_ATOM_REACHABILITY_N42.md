# Cycle-exponential reachability of perfect-matching atoms on the 42-cycle

## Result and scope

Let \(N=42=2n\), \(n=21\), with vertices indexed modulo \(42\). Define
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j,
\]
and all other entries zero. Let
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1).
\]
For a perfect matching \(M\), let \(f\) be its fixed-point-free involution, \(P_M e_j=e_{f(j)}\), and \(R_M=P_MD\).

The theorem below concerns **only these signed-permutation matching atoms**. It is not a theorem about arbitrary cycle exponentials and does not settle the full physical convex-hull problem.

## Theorem 1 — every reachable matching atom is bipartite

If
\[
R_M=e^{A(c)}
\]
for any real cycle-coupling vector \(c\), then every matched pair has one even and one odd endpoint.

More precisely:

1. If at least one coupling vanishes, the zero-edge set \(Z=\{j:c_j=0\}\) is a nonempty subset of either the even-indexed cycle edges or the odd-indexed cycle edges. Removing \(Z\) partitions the cycle into even-length path components, and \(f\) reverses each component.
2. If all 42 couplings are nonzero, \(f\) is a fixed-point-free involutive dihedral automorphism of \(C_{42}\): one half-turn or one of the 21 reflections through opposite edges. Every such map exchanges parity.

### Proof

Let \(G_c\) be the graph consisting of the cycle edges with \(c_j\ne0\). After permuting vertices by connected components, \(A(c)\) is block diagonal, so \(e^{A(c)}\) is block diagonal. If \(R_M=e^{A(c)}\), its unique nonzero entry in column \(j\) is in row \(f(j)\); hence \(f\) preserves every connected component of \(G_c\).

Also \(R_M\) commutes with its logarithm \(A(c)\), so
\[
R_M A(c)R_M^{-1}=A(c).
\]
Conjugation by the signed permutation \(R_M=P_MD\) maps the skew edge supported on \(\{j,j+1\}\) to a signed skew edge supported on \(\{f(j),f(j+1)\}\). Distinct unordered edges have distinct images under the permutation \(f\). Thus every active edge is mapped to an active cycle edge. Consequently \(f\) is a graph automorphism of each component of \(G_c\).

If \(Z\ne\varnothing\), every component is a path or an isolated vertex. An isolated vertex is impossible because \(f\) has no fixed point. The only fixed-point-free automorphism of a path is reversal, and reversal has no fixed vertex only when the path has even cardinality. Reversal of an even contiguous interval exchanges the two vertex parities. The gaps between consecutive zero edges therefore all have even length, which is equivalent to all indices in \(Z\) having the same parity.

If \(Z=\varnothing\), \(G_c=C_{42}\). The fixed-point-free involutions in the dihedral group are the half-turn \(j\mapsto j+21\) and the reflections \(j\mapsto a-j\) with \(a\) odd. Since 21 and \(a\) are odd, all these maps exchange parity. This proves the theorem. \(\square\)

## Exact support-count consequence

For nonempty \(Z\), there are at most
\[
2(2^{21}-1)=4,194,302
\]
possible zero-edge sets: a nonempty subset of the 21 even edges or of the 21 odd edges. Each such set determines at most one matching, because every path component must be reversed.

For \(Z=\varnothing\), there are at most \(21+1=22\) fixed-point-free involutive dihedral maps. Therefore
\[
\boxed{\#\{M:R_M=e^{A(c)}\text{ for some }c\}
\le 4,194,324.}
\]

There are
\[
41!!=13,113,070,457,687,988,603,440,625
\]
perfect matchings in total. Hence the fraction of atoms in the uniform perfect-matching ensemble that could possibly be cycle-reachable is at most
\[
\frac{4,194,324}{41!!}
=
\frac{466036}{1457007828631998733715625}
\approx 3.1985826763715231\times10^{-19}.
\]
Equivalently, the uniform matching measure assigns at least
\[
\frac{1457007828631998733249589}
{1457007828631998733715625}
\]
of its mass to atoms that are not in the fixed-cycle exponential family.

This is an upper bound on the number of reachable matching atoms, not an exact count; the 22 full-cycle candidates have not all been proved reachable.

## The proper-support path candidates are genuinely reachable

The path-reversal condition is not merely necessary. For any nonempty cut set \(Z\) contained in one parity class, each component is an even path. On a component \(a,a+1,\ldots,a+L-1\), \(L\) even, use the engineered mirror generator
\[
(A_{\rm block})_{a+r,a+r+1}
=(-1)^{a+1}\frac{\pi}{2}
\sqrt{(r+1)(L-r-1)},\qquad 0\le r<L-1,
\]
with the opposite lower-triangular entries. Its exponential obeys
\[
e^{A_{\rm block}}e_{a+r}
=(-1)^{a+r}e_{a+L-1-r}.
\]
Thus it realizes exactly the matching reversal on that component. Setting the cut-edge couplings to zero and taking the direct sum over components realizes the matching associated with \(Z\).

## Corollary — no matching-atom mixture can be the target

Put \(Q=RD\). For a matching atom \(R_M=P_MD\), this gives \(Q=P_M\). The balanced-slice target in the \(Q\)-coordinates is
\[
\mathbb E\det Q_{I,I}
=(-1)^r\frac{\binom{21}{r}}{\binom{42}{2r}},
\qquad |I|=2r.
\]
For any same-parity pair \(I=\{i,j\}\), the target is \(-1/41\). But every physically reachable matching atom is bipartite, so its \(2\times2\) principal submatrix on two same-parity vertices is zero and its determinant is zero. Therefore **no probability measure supported only on physically reachable perfect-matching atoms can reproduce the complete target**.

This does not exclude a measure supported on non-permutation matrices \(e^{A(c)}D\). That is the remaining convex-hull question in Issue #7.

## Auxiliary exact commutant-rank formula

For a matching involution \(f\), call a cycle edge \(i\) good if \(\{f(i),f(i+1)\}\) is again a cycle edge. On the good edges, the induced map \(\phi(i)\) is an involution. The dimension of the cycle-generator commutant
\[
\{c:[A(c),R_M]=0\}
\]
equals the number of \(\phi\)-orbits on the good edges. Bad-edge images lie off the cycle and cannot cancel because \(f\) is a permutation; each good orbit contributes one free coefficient.

The verifier cross-checks this formula against exact rational commutator ranks for every perfect matching at \(N=4,6,8\) (3, 15, and 105 matchings respectively), and checks the cut-set and full-cycle parity classifications at \(N=4,6,8,10,42\).

## Reproducibility

- Verifier: verify_cycle_matching_atom_reachability.py
- Exact evidence: evidence/cycle_matching_atom_reachability_n21.json
- Workflow: .github/workflows/eui-cycle-matching-atom-reachability.yml

The exact commutant calculation supplements the graph proof; the 42-site reachability theorem itself is analytic. The result is deliberately limited to signed perfect-matching atoms. It is not a global no-go theorem for the continuous physical family.
