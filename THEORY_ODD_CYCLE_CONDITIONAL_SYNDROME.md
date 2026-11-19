# Optimal syndrome-conditioned diagonal recovery on field-Pauli oracles

The [fixed diagonal twirl](THEORY_ODD_CYCLE_DIAGONAL_SYNDROME_TWIRL.md) improves every field-Pauli oracle, with an exponentially small guaranteed gain when the random distribution is independent of the syndrome. Conditioning on the observed syndrome removes that limitation. The optimization has an exact solution.

Let \(n\ge21\) be odd, \(D=2^{n-1}\), \(r=fD^2\), \(p=3/(4f)\), \(f=1-2\binom{2n}{n}/4^n\). Use the coherent six-query encoder and the [selective decoder](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md): the orthogonal split-flag branch is discarded without data correction, and the ideal flag is corrected only on program syndromes outside the physical program space \(\mathcal S\). The correction on such a syndrome \(R\) is \(Z R^\dagger\), where \(Z\) is a logical diagonal Pauli chosen by a distribution \(\mu_R\).

**Theorem.** Within this entire class of syndrome-dependent diagonal distributions, the optimal worst-case error on the field-Pauli family is
\[
 |1-g(\epsilon)|+\frac32(1-f)\sin^2(4\epsilon)
       -\frac{9W_n}{8r^2}\sin^2(4\epsilon),
 \qquad g=\tfrac14e^{-6i\epsilon}+\tfrac34e^{2i\epsilon},
\]
where
\[
 W_n=\sum_{\substack{2\le m<n\\m\ {\rm even}}}
    \binom nm\left[1-\frac{\binom m{m/2}}{2^m}\right]a_{m/2}^2 ,
 \qquad
 a_k=\sum_{\substack{\ell<n\\\ell\ {\rm odd}}}
       \sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}.
\]
An attaining rule is to choose uniformly among the field labels \(T\) maximizing \(a_{TR}^2\) for the observed syndrome \(R\). It gives exactly the same gain \(W_n\) on every field-Pauli oracle. This rule preserves exact ideal inversion, first-order drift cancellation, and the pointwise no-worse bound relative to the old balanced inverse decoder on *every* physical Hamiltonian.

At \(n=21\), the field-Pauli quadratic coefficient is reduced by \(18W_n/r^2=0.148358524720\ldots\), from \(11.874512219889\ldots\) to \(11.726153695169\ldots\). The previous syndrome-independent twirl gave a gain of \(3.7260622\times10^{-6}\). This proves a larger improvement on the entire field-Pauli family. The [edge-oracle converse](THEORY_ODD_CYCLE_EDGE_ORACLE_CONVERSE.md) now determines the full physical-family supremum: it equals the old balanced decoder's error, attained by \(H=(\pi/2)Z_0Z_1\).

## 1. Exact finite optimization

Represent a parity-preserving logical Pauli by an even Majorana subset, modulo full complementation. The physical ideal program space consists of the balanced subsets with equally many \(a\) and \(b\) labels. For a diagonal field-Pauli oracle \(T\), the shared-projector term \(P\) produces program syndrome \(R=TP\). The ideal-flag squared amplitude is \(p^2|b|^2a_P^2/D^4\), with \(|b|^2=4\sin^2(4\epsilon)\). The correction \(ZR^\dagger\) removes the data error exactly when \(Z=T\).

Define the gain
\[
 G_T(\mu)=\sum_{R\notin\mathcal S}a_{TR}^2\mu_R(T),
 \qquad \mu_R(T)\ge0,\quad \sum_T\mu_R(T)=1 .
\]
As in the [twirl proof](THEORY_ODD_CYCLE_DIAGONAL_SYNDROME_TWIRL.md#3-exact-field-pauli-error-and-optimal-fixed-distribution), the exact balanced field-Pauli diamond error is the old error minus \(9G_T/(8r^2)\sin^2(4\epsilon)\). The task is thus
\(\max_\mu\min_T G_T(\mu)\).
There are \(D\) logical diagonal field labels. For any decoder in this class,
\[
 \min_TG_T
 \le\frac1D\sum_TG_T
 \le\frac1D\sum_{R\notin\mathcal S}\max_T a_{TR}^2 .
\]
The right-hand side is a Bayesian upper bound for the uniform field prior. We show that maximum-likelihood selection attains it equally for every field label, giving a minimax certificate with matching lower and upper values.

## 2. Which fields maximize a syndrome likelihood?

For a Majorana syndrome \(R\), let \(m\) be the number of sites containing exactly one Majorana. It is even. A complementary syndrome is unbalanced, so \(m\ge2\); since \(n\) is odd, \(m\le n-1\). Multiplying by a diagonal field label toggles both Majoranas at each selected site. It swaps the \(a,b\) choice at the \(m\) single sites without changing the count there; at any other site it interchanges empty and double. The possible degrees of \(TR\) are consequently \(m,m+2,\ldots,2n-m\).

For \(1\le k\le n-1\), the coefficients have the closed form
\[
 a_k=(-1)^{k+1}\frac{\binom{2n}{n}\binom nk}{2\binom{2n}{2k}},
 \qquad
 \left|\frac{a_{k+1}}{a_k}\right|=\frac{2k+1}{2n-2k-1}.
\]
The first formula follows from the central coefficient of
\((1-x)^{2k}(1+x)^{2n-2k}\): its total odd-degree sum is zero, and its symmetry about the odd center gives \(a_k\) as negative half the central coefficient. The central coefficient is
\((-1)^k\binom{2n}{n}\binom nk/\binom{2n}{2k}\), obtained by binomial convolution. The ratio follows directly. Hence \(|a_k|\) decreases towards the middle and is symmetric under \(k\mapsto n-k\). The maximum for this syndrome occurs exactly at degree \(m\) or \(2n-m\), with squared value \(a_{m/2}^2\).

Choose the representative of the field label that clears every double site of \(R\) and leaves every empty site empty. At each single site choose the field bit freely. These \(2^m\) choices are distinct logical field labels, since at least one nonsingle site remains and full field complementation would change that bit. They include both endpoint-degree choices after the full-complement identification. Thus the maximum-likelihood decoder is executable by fixing the field bits on nonsingle sites and drawing \(m\) fair bits on the single sites. It requires no knowledge of \(H\).

## 3. Equal gain and minimax optimality

Fix a true field label \(T\). Its error term \(P\) is decoded correctly by the maximum-likelihood rule precisely when it has only single sites and no double sites, using the representative whose nonsingle sites are empty. The complementary endpoint case gives the same logical labels. For a fixed set of \(m\) single sites there are \(2^m\) choices of their \(a,b\) labels. Multiplication by \(T\) just permutes those choices. Exactly \(\binom m{m/2}\) produce a balanced syndrome \(R\), where no correction is applied. The remaining \(2^m-\binom m{m/2}\) syndromes are corrected with probability \(2^{-m}\). Their error degree is \(m\), so all have weight \(a_{m/2}^2\). Summing over the \(\binom nm\) choices of sites gives \(G_T=W_n\), independently of \(T\).

There are
\(\binom nm[2^m-\binom m{m/2}]\,2^{n-m-1}\)
logical complementary syndrome labels with \(m\) single sites: choose the single sites and their unbalanced signs, then the empty/double labels on the other sites, and identify the full complement. Thus the Bayesian upper bound is
\[
 \frac1D\sum_m
   \binom nm[2^m-\binom m{m/2}]\,2^{n-m-1}a_{m/2}^2
 =W_n .
\]
The fieldwise attaining gain and the Bayesian upper bound match, proving the all-length minimax statement for the stated decoder class.

The guarantee is no longer exponentially small. Its \(m=2\) term alone gives
\[
 \frac{18W_n}{r^2}
 \ge \frac92\,n(n-1)\left[\frac{\binom{2n-2}{n-1}}{nr}\right]^2
 \sim\frac9{2\pi n}.
\]
The displayed asymptotic is for this lower bound, using the central-binomial estimate. It shows an inverse-length guaranteed gain; it does not give the complete asymptotic expansion of \(W_n\).

## 4. Full physical-family safety and remaining blocker

All correction operations still occur only on ideal-flag syndromes where the ideal physical program amplitude vanishes. Their random probabilities may depend on the label, but Kraus completeness and the zero contraction with the ideal program remain true separately for every label. The [selective residual identity](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md#1-the-recovery-and-its-residual-channels) therefore holds with the old noise weight and a new CPTP residual channel. It gives the same pointwise upper bound as the old balanced decoder for all physical \(H,\epsilon\). Exact ideal inversion and zero first derivative are preserved.

The strict decrease of every field-Pauli error removes those explicit maximizers. The [physical edge oracle](THEORY_ODD_CYCLE_EDGE_ORACLE_CONVERSE.md) still saturates the old upper bound for this rule and, more generally, every selective syndrome decoder whose additional channel is diagonal in the occupation basis. A further minimax improvement requires non-diagonal action, a different coherent treatment of syndromes or flags, or a changed encoder. The global six-query quadratic optimum and the physical pentagon query minimum remain open.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) motivate the structured inversion and noise objective. The exact optimization here uses the [physical program span](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) and the integer Pauli weights of the [fixed diagonal twirl](THEORY_ODD_CYCLE_DIAGONAL_SYNDROME_TWIRL.md).

## Exact verification

The script enumerates every complementary Majorana syndrome and every field hypothesis at \(n=3,5,7\). It checks the complete maximizing sets, their sizes, the equal achieved gain for all hypotheses, and the matching Bayesian upper bound, using exact fractions. The small sizes check the algebra; the cancellation protocol itself is asserted at \(n\ge21\). Exact long-ring coefficients are then evaluated without enumerating exponentially many labels.

~~~python
from fractions import Fraction
from math import comb


def coefficients(n):
    return [
        sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-2*n+2*k), min(2*k, ell)+1)
        )
        for k in range(n+1)
    ]


def optimum(n, a):
    return sum(
        Fraction(comb(n, m)*(2**m-comb(m, m//2))*a[m//2]**2, 2**m)
        for m in range(2, n, 2)
    )


def verify(n):
    full = (1 << (2*n))-1
    labels = [mask for mask in range(1 << (2*n-1)) if mask.bit_count() % 2 == 0]
    fields = [
        sum(3 << (2*j) for j in range(n-1) if (bits >> j) & 1)
        for bits in range(1 << (n-1))
    ]
    a = coefficients(n)
    gains = [Fraction(0) for _ in fields]
    bayes_sum = 0
    for syndrome in labels:
        na = sum((syndrome >> (2*j)) & 1 for j in range(n))
        nb = sum((syndrome >> (2*j+1)) & 1 for j in range(n))
        if na == nb:
            continue
        singles = [
            j for j in range(n) if ((syndrome >> (2*j)) & 3) in (1, 2)
        ]
        m = len(singles)
        likelihoods = [
            a[min(syndrome ^ field, full ^ syndrome ^ field).bit_count()//2]**2
            for field in fields
        ]
        maximum = max(likelihoods)
        choices = [i for i, value in enumerate(likelihoods) if value == maximum]
        assert len(choices) == 2**m and maximum == a[m//2]**2
        # All minimum-degree representatives give exactly the maximizing set.
        candidates = set()
        for bits in range(1 << m):
            field = sum(
                3 << (2*j) for j in range(n)
                if ((syndrome >> (2*j)) & 3) == 3
            )
            for k, j in enumerate(singles):
                if (bits >> k) & 1:
                    field ^= 3 << (2*j)
            candidates.add(min(field, full ^ field))
        assert candidates == {fields[i] for i in choices}
        for i in choices:
            gains[i] += Fraction(maximum, len(choices))
        bayes_sum += maximum
    target = optimum(n, a)
    assert all(value == target for value in gains)
    assert Fraction(bayes_sum, len(fields)) == target
    print(n, "all hypotheses", len(fields), "exact minimax gain weight", target)


for n in (3, 5, 7):
    verify(n)
for n in (21, 23, 83):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    a = coefficients(n)
    for k in range(1, n):
        closed = (-1)**(k+1)*Fraction(comb(2*n, n)*comb(n, k), 2*comb(2*n, 2*k))
        assert a[k] == closed
    W = optimum(n, a)
    S = sum(comb(n, k)**2*a[k]**2 for k in range(n+1))//2-r*r
    M = r*(D*D-r)-S
    independent = Fraction(18*M, r*r*D)
    conditional = 18*W/r**2
    old = 6+24*Fraction(D*D-r, D*D)
    assert conditional > independent > 0
    assert conditional >= Fraction(9*n*(n-1)*a[1]**2, 2*r*r)
    print(n, "fixed-distribution gain", f"{float(independent):.12g}",
          "conditioned gain", f"{float(conditional):.12f}",
          "field-Pauli coefficient", f"{float(old-conditional):.12f}")
~~~
