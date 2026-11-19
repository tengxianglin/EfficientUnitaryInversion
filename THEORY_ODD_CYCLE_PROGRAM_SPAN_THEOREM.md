# Exact physical program span for every odd Ising cycle

Let \(n\ge3\) be odd and \(\mathcal V_{n,s}\) be the complex linear span of \(e^{-iH}|_{S_s}\), where
\[
 H=\sum_{j=0}^{n-1}h_jX_j+\sum_{j=0}^{n-1}J_jZ_jZ_{j+1\bmod n},\qquad
 S_s=\ker(P-sI),\quad P=\prod_jX_j ,
\]
and the real fields and couplings are independently tunable. Use the [Majoranas](THEORY_ODD_CYCLE_THREE_QUERIES.md#quadratic-representation-in-the-two-sectors)
\(a_j=(X_0\cdots X_{j-1})Z_j\), \(b_j=(X_0\cdots X_{j-1})Y_j\).
Write \(\Gamma_{A,B}\) for the ordered monomial with \(a\)-indices \(A\) and \(b\)-indices \(B\).

**Theorem.** In either parity sector,
\[
 \mathcal V_{n,s}
 =\operatorname{span}_{\mathbb C}
   \{\Gamma_{A,B}|_{S_s}: |A|=|B|\},\qquad
 \dim\mathcal V_{n,s}=\tfrac12\binom{2n}{n}.
\]
The open-chain subfamily \(J_{n-1}=0\) already attains this same span. Thus the [program-span saturation conjecture](THEORY_ODD_CYCLE_PHYSICAL_PROGRAM_SPAN.md) is resolved at every odd length, extending the prior exact rank certificates at \(n=3,5,7\).

For the existing plus-program six-query encoder at odd \(n\ge21\), any fixed recovery exact for every physical ideal oracle has quadratic diamond error coefficient at least
\[
 B_n^{\rm phys}=\frac{72}{r^2}
    \left[\frac12\sum_{k=0}^n\binom nk^2a_k^2-r^2\right],
 \quad
 r=2^{2n-2}-\tfrac12\binom{2n}{n},
\]
with the \(a_k\) defined below. The lower bound is witnessed at the identity ideal oracle. At \(n=21\), \(B_{21}^{\rm phys}=7.707127796320\ldots\), improving the previous proven physical coefficient \(2.249999602402\ldots\). The classical balanced encoder has at least half this floor. This constrains recovery for the fixed encoders; the best error over all six-query encoders remains open.

## 1. Upper inclusion and Pauli separation

For a fixed parity, the quadratic representative of \(H\) has the form \(i\sum K_{ij}a_i b_j\) for real \(K\), with the parity sign in its wrap entry. A real SVD \(K=L\Sigma R^{\mathsf T}\) gives
\[
 e^{-iH}
 =\prod_{j=1}^{n}
  [\cos\sigma_j+\sin\sigma_j\,a'_jb'_j]
\]
on the full quadratic representative, where \(a'\) and \(b'\) are orthonormal frames in their respective original spans. Each term has equal numbers of \(a\) and \(b\) Majoranas, and the separate orthogonal frame changes preserve these numbers. Restriction to \(S_s\) gives the upper inclusion.

On a parity sector, complementary Majorana monomials restrict to the same logical Pauli up to a nonzero phase. Distinct complementary classes are trace-orthogonal. Since \(n\) is odd, each balanced class has a unique representative with \(|A|=|B|\le(n-1)/2\). Their number is
\[
 \sum_{k=0}^{(n-1)/2}\binom nk^2=\tfrac12\binom{2n}{n}.
\]

The physical family, including its open-chain subfamily, is invariant under conjugation by any parity-preserving physical Pauli: this only changes signs of the fields and of the supported edges. Every logical Pauli in \(S_s\) is the restriction of such a physical Pauli, since even Majorana monomials supply a complete logical Pauli basis. Therefore \(\mathcal V_{n,s}\) is invariant under the entire logical Pauli conjugation group. For a fixed Hermitian logical Pauli \(M\), the map
\[
 X\ \longmapsto\ D^{-2}\sum_{P\ {\rm logical\ Pauli}}\chi(P,M)\,PXP,
 \qquad D=2^{n-1},
\]
projects onto the coefficient of \(M\), where \(\chi(P,M)=\pm1\) is the commutation character. Thus it suffices to show that every balanced monomial has a nonzero coefficient in at least one physical open-chain exponential.

## 2. An open-chain ray with independent phases

Choose positive fields and positive open-chain off-diagonal entries, so that \(K\) is lower bidiagonal, with positive diagonal and strictly positive subdiagonal. These are valid physical parameters after setting the signs of the \(J_j\) appropriately. Both
\(M_L=KK^{\mathsf T}\) and \(M_R=K^{\mathsf T}K\)
are symmetric tridiagonal matrices with strictly positive off-diagonals. Their spectra are simple, positive and equal; write their singular values \(\sigma_1>\cdots>\sigma_n>0\).

We can choose such parameters with the \(\sigma_j\) rationally independent. Work in a connected small box around distinct positive diagonal fields and zero subdiagonals, with the singular-value order fixed. The singular values are real analytic on the box. For any nonzero integer row \(q\), the function \(\sum_j q_j\sigma_j\) is nonzero as an analytic function: at zero subdiagonals it is a nontrivial linear function of the freely variable fields. Its zero set is closed with empty interior. By the Baire category theorem, the complement of the countable union of these zero sets is dense, also in the open part where every subdiagonal is positive.

Fix one such \(K\). Scaling its fields and edges by a real \(t\) gives a physical open-chain ray. Rational independence makes \((t\sigma_1,\ldots,t\sigma_n)\) dense in the full \(n\)-phase torus. A finite trigonometric identity valid on this ray therefore holds on the torus.

## 3. Nonzero minors of the top singular frames

Let \(M\) be a real symmetric tridiagonal matrix with strictly positive off-diagonals. Its \(k\)th additive compound \(M^{[k]}\), in the ordered \(k\)-subset basis, represents the infinitesimal action of \(M\) on \(\wedge^k\mathbb R^n\). The only off-diagonal entries move one occupied index to an unoccupied adjacent site. Their values are the corresponding positive off-diagonals of \(M\); there is no reordering sign for an adjacent allowed move. This subset graph is connected for \(1\le k<n\).

Adding a sufficiently large scalar multiple of the identity makes \(M^{[k]}\) nonnegative and irreducible. Perron–Frobenius then gives a strictly positive vector for its largest eigenvalue. That eigenvalue is the sum of the \(k\) largest, distinct eigenvalues of \(M\), uniquely maximized by that subset. Its eigenvector is the wedge of those \(k\) eigenvectors. The wedge coordinates are the determinants of all \(k\)-row minors of their frame. All such minors are therefore nonzero. For \(k=0,n\) the statement is immediate.

Apply this separately to \(M_L\) and \(M_R\). If \(J_k=\{1,\ldots,k\}\) indexes the largest singular values, then
\[
 \det L_{A,J_k}\ne0,\qquad \det R_{B,J_k}\ne0
 \quad\text{for every }|A|=|B|=k.
\]
The signs chosen to pair the left and right singular vectors do not affect nonvanishing. The additive-compound argument is the standard positivity mechanism for Jacobi matrices; related total-positivity results are proved by [Schwarz (1970)](https://msp.org/pjm/1970/32-1/pjm-v32-n1-p20-s.pdf).

## 4. Fourier extraction supplies every balanced monomial

Before restricting parity, the coefficient of \(\Gamma_{A,B}\) with \(|A|=|B|=k\), up to a nonzero sign fixed by the ordering of Majoranas, is
\[
 \sum_{|J|=k}\det L_{A,J}\det R_{B,J}
   \prod_{j\in J}\sin\theta_j
   \prod_{j\notin J}\cos\theta_j .
\]
This is the exterior-power expansion of the product in Section 1. By Section 3, its coefficient at \(J_k\) is nonzero.

The \(2^n\) trigonometric functions
\(\prod_{j\in J}\sin\theta_j\prod_{j\notin J}\cos\theta_j\)
are linearly independent on the full torus: in each coordinate the sine and cosine are independent, and their tensor products form an independent family. For \(k\le(n-1)/2\), the complementary physical monomial contributes only terms with \(|J|=n-k\), so restriction to a parity sector cannot cancel the displayed nonzero size-\(k\) term. All other monomials have zero overlap with the chosen logical Pauli by trace orthogonality of complementary classes. Hence the coefficient of that logical Pauli is nonzero somewhere on the torus, and therefore somewhere on the dense physical ray. Pauli separation from Section 1 puts the monomial itself in the physical span. This proves the lower inclusion, for each parity separately and using only the open-chain subfamily.

## 5. Consequence for exact fixed recovery

The [fixed-encoder decoder bound](THEORY_ODD_CYCLE_SIX_QUERY_DECODER_BOUND.md) projects the drift error onto the ideal program span and the ideal flag. Exactness forces recovery to preserve the data action of that component; other components add positive population outside the target Bell state.

For the plus-program encoder the shared projector is
\(Q=D^{-2}\sum_P a_P P\otimes\bar P\).
Its error amplitude in the ideal flag is \(p b Q\), with \(p=3/(4f)\), \(f=r/D^2\), and \(|b|^2=4\sin^2(4\epsilon)\). The theorem identifies the program subspace exactly: it keeps the Pauli labels represented by balanced monomials. For a monomial of grade \(2k\), \(|a_P|^2=a_k^2\), where
\[
 a_k=\sum_{\substack{\ell<n\\\ell\ {\rm odd}}}
          \sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}.
\]
There are \(\binom nk^2\) balanced monomials before identifying complements. Removing the identity leaves the squared sum
\[
 S_{\rm phys}=\tfrac12\sum_{k=0}^n\binom nk^2 a_k^2-r^2 .
\]
The unavoidable Bell infidelity is at least \(p^2|b|^2S_{\rm phys}/D^4\). Twice this quantity lower-bounds the diamond error, giving the exact finite-drift lower bound
\[
 \|\Phi_\epsilon-\mathrm{id}\|_\diamond
 \ge \frac{B_n^{\rm phys}}{16}\sin^2(4\epsilon).
\]
This proves the asserted quadratic coefficient. For the classical fair mixture of the two program orientations, each conditional recovery must be exact because the ideal average output is pure. A plus-sector Bell test then inherits at least one half of the displayed bound.

At \(n=21\) this gives physical coefficients \(7.707127796320\ldots\) for the plus-program encoder and \(3.853563898160\ldots\) for the classical balanced encoder. The attained balanced coefficient is \(11.874512219889\ldots\). The stronger group-promise floor remains \(11.667682684273\ldots\) for the balanced encoder. The different floors reflect different ideal-program spans.

## Verification and next step

The proof is all-length and analytic. The accompanying checks build positive bidiagonal matrices at \(n=3,5,7,9\), construct their additive-compound graphs, and check their connected positive edge structure. They also numerically inspect every top-frame minor for a conditioned example at \(n=5\), and evaluate the exact rational error coefficients at larger lengths. The [modular resolvent verifier](verify_ising_program_span.py) independently checks the physical span dimensions at \(n=3,5,7\).

The next optimization is to determine the best recovery on the remaining program subspace, orthogonal to the balanced Majorana span, while preserving exact physical ideal outputs. The theorem determines that subspace explicitly and the new floor rules out cubic suppression for these fixed encoders. Changing the encoder remains a separate route. The unrestricted physical pentagon is still six versus seven.

The [EUI preprint](https://arxiv.org/html/2506.20570v1) gives the structured physical setting. The Majorana representation and sparse parameter family are developed in the repository's [three-query construction](THEORY_ODD_CYCLE_THREE_QUERIES.md). The present span theorem uses separate singular frames, additive-compound positivity and logical Pauli character projection.

~~~python
from fractions import Fraction
from itertools import combinations
from math import comb

import numpy as np


def compound_graph(n, k):
    subsets = tuple(combinations(range(n), k))
    lookup = {row: i for i, row in enumerate(subsets)}
    adjacency = [set() for _ in subsets]
    for i, row in enumerate(subsets):
        for old in row:
            for new in (old-1, old+1):
                if 0 <= new < n and new not in row:
                    column = lookup[tuple(sorted((set(row)-{old})|{new}))]
                    adjacency[i].add(column)
    reached, pending = {0}, [0]
    while pending:
        vertex = pending.pop()
        for other in adjacency[vertex]-reached:
            reached.add(other)
            pending.append(other)
    assert len(reached) == len(subsets)
    assert all(i in adjacency[j] for i, neighbors in enumerate(adjacency) for j in neighbors)


for n in (3, 5, 7, 9):
    assert sum(comb(n, k)**2 for k in range((n+1)//2)) == comb(2*n, n)//2
    for k in range(1, n):
        compound_graph(n, k)
    print("Connected additive-compound graphs verified at n =", n)

K = np.diag(np.linspace(1, 2, 5))+np.diag(np.full(4, 0.8), -1)
left, sigma, right_transpose = np.linalg.svd(K)
assert np.all(sigma[:-1] > sigma[1:]) and np.all(sigma > 0)
for frame in (left, right_transpose.T):
    for k in range(1, 6):
        minors = [np.linalg.det(frame[list(rows), :k]) for rows in combinations(range(5), k)]
        assert min(abs(value) for value in minors) > 1e-10
        assert all(value*minors[0] > 0 for value in minors)
print("All top-frame minors verified in a numerical five-site example.")

for n in (21, 23, 83):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    a = [
        sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-2*n+2*k), min(2*k, ell)+1)
        )
        for k in range(n+1)
    ]
    squared = sum(comb(n, k)**2*value**2 for k, value in enumerate(a))
    assert squared % 2 == 0
    S = squared//2-r*r
    physical = Fraction(72*S, r*r)
    group = Fraction(72*(D*D-r), r)
    assert 0 < physical <= group
    print(n, "physical plus-program floor", f"{float(physical):.12f}",
          "classical balanced floor", f"{float(physical/2):.12f}")
~~~
