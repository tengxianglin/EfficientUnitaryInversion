# Physical program spans and stronger six-query recovery floors

Let \(n\) be odd, \(D=2^{n-1}\), and let \(\mathcal V_n\) be the complex linear span of the plus-block physical Ising matrices \(U_+(H)=e^{-iH}|_{S_+}\), with all real fields and cyclic edge coefficients independently tunable. The ideal program states of the [six-query encoder](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md) span \(\operatorname{vec}(\overline{\mathcal V_n})\). This span controls the action of every exact fixed recovery through the [purity and linearity argument](THEORY_ODD_CYCLE_SIX_QUERY_DECODER_BOUND.md#1-exactness-on-the-ideal-orbit-fixes-recovery-on-its-linear-span).

**Results.** The physical program space contains all field-basis diagonal matrices and every real symmetric matrix unit joining two occupation rows of the same parity that differ on two sites. In particular,
\[
 \dim\mathcal V_n\ge D+\frac D2\binom n2.
\]
For the fixed plus-program six-query encoder with coherent split flag, any fixed exact physical recovery has diamond error at the identity oracle at least \((B_n^{(2)}/16)\sin^2(4\epsilon)\), where
\[
 B_n^{(2)}
 =\frac{72}{r^2}
 \left[
 \frac12\sum_{k=0}^n\binom nk a_k^2-r^2
 +\binom n2\sum_{k=0}^{n-2}\binom{n-2}{k}a_{k+1}^2
 \right],
\quad r=D^2-\tfrac12\binom{2n}{n},
\]
and
\[
 a_k=\sum_{\substack{\ell<n\\\ell\ {\rm odd}}}
       \sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}.
\]
For \(n=21\) the quadratic floor increases from \(0.100884111690\ldots\) to \(2.249999602402\ldots\). For the classical balanced encoder, even allowing an orientation-dependent recovery, half of this floor applies. These bounds concern the existing encoders; the full physical pentagon query count and global six-query quadratic optimum remain open.

There is also an all-length ceiling
\[
 \dim\mathcal V_n\le\frac12\binom{2n}{n}.
\]
Exact modular resolvent checks saturate that ceiling at \(n=3,5,7\), giving dimensions \(10,126,1716\). The full complex symmetric matrix spaces have dimensions \(10,136,2080\), respectively. Thus the physical program space at five and seven sites is strictly smaller than the whole symmetric space. The [all-length span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) now proves saturation of the displayed ceiling for every odd length using only the open-chain subfamily.

## 1. Matrix units supplied by physical root tori

The field torus has pairwise distinct spinor weight characters, so Fourier extraction places every field-basis rank-one diagonal projector in \(\mathcal V_n\). The [physical root tori](THEORY_ODD_CYCLE_PHYSICAL_ROOT_TORI.md) are limits of actual physical oracles. Finite-dimensional linear subspaces are closed, so their oracle matrices also lie in \(\mathcal V_n\). Their spinor characters are again distinct. Fourier extraction on a root torus therefore places each rotated rank-one eigenprojector in \(\mathcal V_n\).

Given same-parity rows \(x,y\) differing at sites \(i,j\), use either the number-conserving or particle–hole root rotation at those sites to mix them. Although the rotation acts on several pairs simultaneously, the individual rank-one projectors are separately Fourier coefficients. Subtracting their original diagonal components gives a nonzero multiple of \(|x\rangle\langle y|+|y\rangle\langle x|\). This gives all the claimed symmetric matrix units. There are \(D\binom n2/2\) unordered pairs, proving the dimension bound.

## 2. Counting the additional uncorrectable Pauli components

On the product of a data Bell state and the initial program Bell state, the shared projector has the logical Pauli expansion
\[
 Q=D^{-2}\sum_P a_P P\otimes\bar P .
\]
The resulting Pauli Bell products are mutually orthogonal. The [fixed recovery argument](THEORY_ODD_CYCLE_SIX_QUERY_DECODER_BOUND.md#3-a-physical-floor-from-the-field-torus-alone) forces recovery to preserve the data channel of the component in the ideal program span and ideal split flag. The diagonal program subspace keeps the zero-bit-flip logical Paulis. The matrix units from Section 1 additionally keep exactly the real symmetric logical Paulis that flip two occupation bits.

A parity-preserving logical Pauli is an even Majorana monomial modulo the full parity monomial. On each site it contains no Majorana, both Majoranas, only \(a_i\), or only \(b_i\). The single-Majorana sites are exactly its occupation-flip support. For two such sites the remaining \(k\) occupied sites contribute both Majoranas, so its total grade is \(2(k+1)\). Its transpose is symmetric precisely when one single site has an \(a\) and the other a \(b\). This follows from the transpose of a grade-\(2j\) Hermitian Majorana monomial: the sign is \((-1)^{j+\#b}\). The two choices at the single sites cancel the factor of two from identifying a monomial with its parity complement. The squared Pauli coefficient depends only on the grade; it equals \(a_{k+1}^2\), since the extra commutation sign of charge conjugation disappears upon squaring. Counting the remaining \(k\) double sites gives
\[
 \sum_{\text{symmetric, two flips}}a_P^2
   =\binom n2\sum_{k=0}^{n-2}\binom{n-2}{k}a_{k+1}^2 .
\]
Adding the diagonal nonidentity sum and using the same Bell-infidelity test as before gives \(B_n^{(2)}\). All terms are nonnegative, so the new floor strengthens the diagonal one at every odd \(n\ge21\). The statement permits arbitrary fixed recovery on the program, purifier, coherent flag and scratch.

## 3. A Clifford ceiling for the physical ideal-program space

For each fixed parity replace the boundary parity in the Hamiltonian by its sign to obtain a real matrix \(K\) in \(i\sum_{ij}K_{ij}a_i b_j\). Use a real singular-value decomposition \(K=L\Sigma R^{\mathsf T}\). The two new Majorana frames \(a'_i,b'_i\) stay in their respective \(a\) and \(b\) spans, and the bilinears \(a'_i b'_i\) commute. The corresponding full-space Gaussian is a product of factors
\(\cos\sigma_i+\sin\sigma_i\,a'_i b'_i\).
Each term of degree \(2k\) contains exactly \(k\) \(a\)-Majoranas and \(k\) \(b\)-Majoranas. Orthogonal change of frame preserves this property in each grade. Degenerate or zero singular values follow by continuity.

Thus physical program matrices lie in the span of the restrictions of balanced monomials \(\Gamma_{A,B}\) with \(|A|=|B|=k\). In a parity sector, a monomial and its full complement restrict to the same operator up to phase. They pair grades \(k\) and \(n-k\). For odd \(n\) there is no self-pair. Distinct complementary classes are trace-orthogonal Pauli labels. The balanced space therefore has dimension
\[
 \frac12\sum_{k=0}^n\binom nk^2=\frac12\binom{2n}{n}.
\]
Every balanced monomial is transpose-symmetric, but there are additional symmetric monomials with unequal \(a,b\) counts. The SVD argument excludes those from physical single-exponential program states.

## 4. Exact span certificates at three, five and seven sites

The standalone [verifier](verify_ising_program_span.py) builds rational resolvents \((zI-H_+)^{-1}\) for reproducible integer parameters, and row-reduces their symmetric entries modulo the prime 65521. Each resolvent lies in \(\mathcal V_n\): for fixed Hermitian \(H_+\), its spectral projectors lie in the span of \(e^{-itH_+}\) as \(t\) varies, because exponentials of distinct eigenvalues are linearly independent; the resolvent is a linear combination of those projectors. These scaled Hamiltonians remain in the physical promise. A modularly invertible denominator also certifies invertibility over the rationals. Independent modular rows therefore certify independent rational resolvents. The rank stops as soon as it meets the analytic ceiling. The computations use integer modular arithmetic with intermediates below the signed 64-bit range.

Run the default small cases with
~~~bash
python verify_ising_program_span.py
~~~
and include seven sites with
~~~bash
python verify_ising_program_span.py --sizes 3 5 7
~~~
These certificates establish the span equality at those lengths without assuming that the physical oracles form a group. The [analytic all-length theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) proves equality at every odd length by additive-compound positivity and Pauli coefficient separation.

Using that all-length equality, the fixed-encoder floor strengthens further to
\[
 B_n^{\rm balanced\ span}
  =\frac{72}{r^2}
     \left[\frac12\sum_{k=0}^n\binom nk^2 a_k^2-r^2\right],
\]
since precisely the balanced logical Pauli monomials lie in the ideal-program span. At \(n=21\) this proven coefficient is \(7.707127796320\ldots\), strengthening the earlier two-flip bound \(B_{21}^{(2)}=2.249999602402\ldots\). The next step is to optimize recovery on the complementary program subspace while preserving exact ideal outputs, or to improve the encoder itself.

The [EUI preprint and robustness appendix](https://arxiv.org/html/2506.20570v1) give the physical inversion setting. [Pfeuty's Ising solution](https://doi.org/10.1016/0003-4916(70)90270-8) supplies the quadratic-fermion context. The span bound here follows directly from the SVD of the two Majorana frames; it is narrower than a group-generation argument.

## Exact coefficient checks

This Python 3 block verifies the derived arithmetic bounds and dimensions. Coefficients at \(n<21\) are algebraic values used for cross-checking; the six-query mixture requiring \(f_n\ge3/4\) is asserted only for \(n\ge21\).

~~~python
from fractions import Fraction
from math import comb


def floors(n):
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
    diagonal = sum(comb(n, k)*value**2 for k, value in enumerate(a))//2-r*r
    two_flips = comb(n, 2)*sum(comb(n-2, k)*a[k+1]**2 for k in range(n-1))
    balanced = sum(comb(n, k)**2*value**2 for k, value in enumerate(a))//2-r*r
    assert 0 < diagonal < diagonal+two_flips <= balanced <= r*(D*D-r)
    return tuple(Fraction(72*s, r*r) for s in (diagonal, diagonal+two_flips, balanced))


for n in (3, 5, 7, 21, 23, 83):
    D = 2**(n-1)
    lower = D+D*comb(n, 2)//2
    upper = comb(2*n, n)//2
    assert lower <= upper <= D*(D+1)//2
    print(n, lower, upper, *(f"{float(x):.12f}" for x in floors(n)))
~~~
