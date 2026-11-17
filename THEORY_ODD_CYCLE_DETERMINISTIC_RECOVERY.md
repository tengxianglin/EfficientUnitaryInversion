# Deterministic recovery for common parity drift

The [conditional hierarchy](THEORY_ODD_CYCLE_DRIFT_HIERARCHY.md) uses $m=4k-1$ parallel queries and suppresses common parity drift $\epsilon P$ to order $2k-1$ after checking clean return. We show that a fixed decoder can attain the same order without postselection. We also give a matching lower bound over arbitrary fixed decoders whenever the encoding satisfies the clean parallel parity-sector constraint.

The target is inversion of the intended fully fielded odd-cycle Hamiltonian $H$. The actual oracle is $e^{-i(H+\epsilon P)}$ in all slots. Gates outside the oracle are ideal and independent of $H,\epsilon$. The error below is the diamond norm of the deterministic decoded channel relative to the intended inverse, with no factor of one half.

## Lower bound for encoders with the clean parallel charge constraint

Write $Q=\sum_{j=1}^m P_j$. The [central congruence](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#why-three-queried-sectors-must-agree) forces the encoding of input parity $s$ to lie in the physical charge set $s\mathcal Q_k$, where $\mathcal Q_k=\{6-m+8j:0\leq j<k\}$. Consider any encoder with that support property and any fixed trace-preserving decoder that is correct on ideal queries. Allow unqueried workspace and arbitrary decoder environments.

For any unit vectors $u$ and $v$ in opposite logical parity sectors, test the channel at $H=0$ on the operator $|u\rangle\langle v|$, whose trace norm is one. The output matrix element between $u$ and $v$ is a function $f(\epsilon)$ with $f(0)=1$. By expanding the encoded operator in the charge projectors before decoding, $f$ is a linear combination of exponentials $e^{-i\omega\epsilon}$ with
$$
\omega\ \in\ \mathcal F_k=\{12-2m+8j:0\leq j\leq 2k-2\}.
$$
These are the sums of a charge in $\mathcal Q_k$ and the negative of a charge in $-\mathcal Q_k$. The $2k-1$ frequencies are distinct and none is zero. The channel diamond error is at least $|f(\epsilon)-1|$. Vandermonde invertibility on $\{0\}\cup\mathcal F_k$ forbids vanishing past order $2k-1$. If an optimal-order decoder cancels orders $1,\ldots,2k-2$, its amplitudes on the frequencies must reproduce evaluation at zero for every polynomial of degree at most $2k-2$. Apply that interpolation identity to the lower-degree coefficients of $\prod_{\omega\in\mathcal F_k}(x-\omega)$. The magnitude of the remaining Taylor coefficient of $f-1$ is
$$
D_k=\frac{\left|\prod_{\omega\in\mathcal F_k}\omega\right|}{(2k-1)!}.
$$
Consequently this value lower-bounds the optimal leading diamond coefficient for fixed decoders in the stated encoder class.

## Fixed deterministic decoder

Take the encoder built in the conditional hierarchy, with positive probabilities $p_j$ on charges $q_j\in\mathcal Q_k$. It consists of a superposition of orthogonal branch isometries. For input parity $s$, branch $j$ applies the three-call encoder in that sector and appends a fixed tensor product of four-call invariant states, giving total charge $sq_j$. Every such branch implements the same intended inverse on ideal queries. A fixed decoder can map the image of branch $j$ to its data state with a flag $|j\rangle$, since all branches and both logical sectors have orthogonal images. One may extend this mapping to an isometry on the full input space. After the noisy oracle the flag amplitudes before further decoding are $\sqrt{p_j}e^{-isq_j\epsilon}$, independent of $H$. The flag is never measured.

Let $h_0=1,h_1,\ldots,h_{k-1}$ be the real orthonormal polynomials obtained from Gram–Schmidt for the measure $\sum_j p_j\delta_{q_j}$, ordered by degree. Change flag basis to the vectors with components $\sqrt{p_j}h_\ell(q_j)$. The ideal flag is now $|0\rangle$. On the negative logical sector only, multiply flag $\ell$ by $(-1)^\ell$. This is a fixed controlled unitary on the flags and leaves the ideal flag alone. Denote the sign operator on flags by $R$.

In this basis the charge operator for the positive sector is a real symmetric tridiagonal matrix $J$. Tridiagonality follows from orthogonality and multiplication by $q$ raising degree by at most one. The odd moments through degree $2k-3$ vanish by construction. Even and odd polynomials up to degree $k-1$ therefore remain separate in Gram–Schmidt, and every diagonal entry of $J$ except possibly the last is zero. Specifically, the diagonal entry of index $\ell\le k-2$ is the mean of the odd polynomial $q h_\ell(q)^2$, of degree at most $2k-3$. Hence after the controlled sign, the negative flag evolves with $J_-=-RJR=J-2J_{k-1,k-1}|k-1\rangle\langle k-1|$ while the positive flag evolves with $J$.

Discarding the flag gives the intended inverse followed by a channel which leaves both diagonal parity blocks unchanged and multiplies the positive-to-negative block by
$$
g(\epsilon)=\langle 0|e^{i\epsilon J_-}e^{-i\epsilon J}|0\rangle.
$$
The diamond distance of this channel from identity is exactly $|1-g|$. For the upper bound, the off-diagonal block projection is $(\mathrm{id}-\operatorname{Ad}_P)/2$ and has diamond norm at most one. A diagonal phase conjugation allows the factor $g-1$ and its conjugate to be applied with common magnitude $|g-1|$. A balanced superposition of one vector from each sector gives the matching trace-norm lower bound.

Differentiating the product of exponentials in $g$ inserts the sole diagonal difference between $J_-$ and $J$, at index $k-1$. Each matrix element from $0$ to $k-1$ of either tridiagonal exponential is $O(|\epsilon|^{k-1})$. Integration gives $g-1=O(|\epsilon|^{2k-1})$. Its frequencies belong to $\mathcal F_k$, so the lower-bound interpolation identity gives the exact leading magnitude $D_k$. This achieves the optimal order and leading coefficient uniformly in $H$, with no rejected runs. The deterministic leading coefficients are $6,28,308,3960$ at $m=3,7,11,15$ respectively. In particular eleven queries suffice for deterministic fifth-order suppression.

This lower bound uses the physical charge support of a clean parallel encoder, but leaves its recovery decoder unrestricted. It does not classify arbitrary ideal processors whose encoders have no known clean parallel realization, or sequential combs. Compiling the added flag basis and controlled decoder into elementary hardware gates remains open. For general coherent-error recovery context see [Beale et al., arXiv:1805.08802](https://arxiv.org/abs/1805.08802). The recovery here addresses the specific charges of the odd-cycle inverter.

## Exact check

The script implements the flag operation using rational orthogonal polynomials with their squared norms. It checks the full set of coherence-factor coefficients and moments without floating-point extrapolation.

~~~python
from collections import defaultdict
from fractions import Fraction
from math import factorial, prod


def verify(k):
    m = 4 * k - 1
    charges = list(range(6 - m, m + 1, 8))
    raw = [
        Fraction(1, q * prod(q*q - r*r for r in charges if r != q))
        for q in charges
    ]
    weights = [p / sum(raw) for p in raw]
    assert all(p > 0 for p in weights)

    def inner(left, right):
        return sum(p*a*b for p, a, b in zip(weights, left, right))

    orthogonal = []
    for degree in range(k):
        values = [Fraction(q**degree) for q in charges]
        for previous, norm in orthogonal:
            factor = inner(values, previous) / norm
            values = [a - factor*b for a, b in zip(values, previous)]
        orthogonal.append((values, inner(values, values)))

    coeffs = defaultdict(Fraction)
    for i, qi in enumerate(charges):
        for j, qj in enumerate(charges):
            kernel = sum(
                (-1)**ell * values[i] * values[j] / norm
                for ell, (values, norm) in enumerate(orthogonal)
            )
            coeffs[qi + qj] += weights[i] * weights[j] * kernel
    assert len(coeffs) == 2*k-1 and 0 not in coeffs
    assert sum(coeffs.values()) == 1
    for degree in range(1, 2*k-1):
        assert sum(c*w**degree for w, c in coeffs.items()) == 0
    leading = sum(c*w**(2*k-1) for w, c in coeffs.items())
    assert leading == prod(coeffs)
    return Fraction(abs(leading), factorial(2*k-1))


for k in range(1, 13):
    result = verify(k)
    if k <= 4:
        print(4*k-1, 2*k-1, result)
~~~
