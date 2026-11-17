# Optimal cancellation order for parallel parity-phase drift

Consider the fully fielded odd Ising cycle and the clean parallel architecture of [the query-count theorem](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md). Its encoder $E$ is a fixed isometry into $m$ query registers and any unqueried workspace, with the inverse decoder and clean-return success check. In each slot the oracle is $e^{-i(H+\epsilon P)}$ with $P=\prod_j X_j$. Ideal inversion at $\epsilon=0$ is required on the entire Hamiltonian promise. We compare the accepted output against the ideal inverse and allow coherent inputs across the two parity sectors.

**Result.** With $m=4k-1$, the best possible worst-case conditional error order is $|\epsilon|^{2k-1}$. In particular, eleven queries are necessary and sufficient for fifth-order suppression, even with unrestricted unqueried workspace. The order bound applies when success is input dependent. The construction attains it with input-independent success, so its conditional error has a well-defined channel diamond norm.

## Reduction to finite charge distributions

Let $Q=\sum_{j=1}^m P_j$ be the total query parity. The congruences proved in [the query-count theorem](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#why-three-queried-sectors-must-agree) imply that input parity $s$ can use only charges $sq$, where
$$
\mathcal Q_k=\{6-m+8j:0\le j\le k-1\}.
$$
A possible global phase in the exact ideal relation cancels from the channel and will be omitted. The drift commutes with every query and factors from the ideal oracle. Thus the accepted operator in the frame of the ideal inverse is exactly $E^\dagger e^{-i\epsilon Q}E$. It preserves input parity because the two code sectors are supported on disjoint charge sets $\mathcal Q_k$ and $-\mathcal Q_k$. In fact elements of the two sets have residues modulo eight that differ.

For any chosen unit vectors $u$ in the positive input sector and $v$ in the negative input sector, let $p_q$ and $r_q$ be the charge distributions of $Eu$ on $q$ and $Ev$ on $-q$, respectively. They are probabilities even when the encoder stores extra workspace. Define
$$
f_u(\epsilon)=\sum_q p_q e^{-i q\epsilon},\qquad
f_v(\epsilon)=\sum_q r_q e^{i q\epsilon}.
$$
On the balanced input $\psi=(u+v)/\sqrt2$, the component of the accepted operator along $(u-v)/\sqrt2$ has amplitude $(f_u-f_v)/2$. This component is orthogonal to the ideal output in this frame. Normalizing the accepted state can only increase its magnitude because the accepted operator is a contraction. Thus its conditional trace distance from the target on this input is at least $|f_u-f_v|/2$. The success probability is positive near zero by ideal exactness.

The two distributions are supported on $2k$ distinct charges altogether. If $f_u-f_v$ vanished to order greater than $2k-1$, the difference of the distributions would have zero moments of degrees $0,\ldots,2k-1$. The Vandermonde matrix on the distinct charges is invertible, so the signed measure would be zero. This is impossible for disjoint normalized distributions. Hence every encoder has a worst-case conditional error at least of order $|\epsilon|^{2k-1}$ near zero. This proof needs only a pure logical input and therefore also lower-bounds worst-case performance with a reference.

## Constructing the optimal distribution

Sort the $k$ charges by increasing absolute value as $q_0,\ldots,q_{k-1}$ and put $x_j=q_j^2$. Their signs alternate in that order and the largest charge is positive. To check the alternation, when $k$ is odd the positive magnitudes are $3,11,\ldots,m$ and the negative magnitudes are $5,13,\ldots,m-6$. When $k$ is even the negative magnitudes are $1,9,\ldots,m-6$ and the positive magnitudes are $7,15,\ldots,m$. Both lists interleave.

Define a normalized probability distribution by
$$
w_j=\frac{1}{q_j\prod_{\ell\ne j}(x_j-x_\ell)},\qquad p_j=\frac{w_j}{\sum_\ell w_\ell}.
$$
Each $w_j$ is positive because the sign of $q_j$ and the sign of its Vandermonde product are both $(-1)^{k-1-j}$. The leading coefficients of the Lagrange interpolation polynomials for $x^a$ imply
$$
\sum_j p_j q_j^{2a+1}=0\quad (0\le a<k-1),\qquad
\sum_j p_j q_j^{2k-1}=\frac{1}{\sum_\ell w_\ell}.
$$

To implement the distribution, use the existing three-query isometry in sector $s$ and append $k-1$ blocks of the four-query invariant states $\Omega_+$ and $\Omega_-$ from [the prior construction](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#exact-drift-response-and-a-seven-query-construction). A component with $j$ blocks in sector $s$ and $k-1-j$ blocks in sector $-s$ realizes charge $s(6-m+8j)$. For each charge fix the block ordering, and superpose these mutually orthogonal components with the square roots of their assigned probabilities. Every appended component is invariant under the ideal oracle. The relative phase between the two data parity sectors is retained.

The accepted factor on the positive sector is $F(\epsilon)=\sum_j p_j e^{-iq_j\epsilon}$ and the factor on the negative sector is its conjugate. Thus the success probability $|F|^2$ is the same for every input, and the conditional diamond error is $2|\sin(\arg F)|$. For $k\ge2$, the leading error and success are
$$
\frac{2|\epsilon|^{2k-1}}{(2k-1)!\sum_j w_j}+O(|\epsilon|^{2k+1}),
\qquad
1-\epsilon^2\sum_j p_j q_j^2+O(\epsilon^4).
$$
For $k=1$ the factor is $e^{-3i\epsilon}$ and acceptance is certain.

The charge distributions of an encoder attaining the optimal order are also fixed. For every pair of opposite-sector input vectors, the signed measure in the lower-bound proof must vanish on moments of degrees $0$ through $2k-2$. The rectangular Vandermonde matrix has a one-dimensional nullspace. The constructed signed difference is a nonzero vector in it, and the requirement that each sector's probabilities sum to one fixes the scale. This forces the constructed probabilities on every unit vector in its sector. By polarization the compressed charge projectors are scalar within each sector. Consequently every order-optimal clean parallel encoder has the same accepted factors and success probability for this drift, even if its encoding gates or extra workspace differ.

For $m=11$ the probabilities on charges $3,-5,11$ are $55/96,77/192,5/192$. The conditional diamond error is $(154/3)|\epsilon|^5+O(|\epsilon|^7)$ and the success probability is $1-(55/3)\epsilon^2+O(\epsilon^4)$. The seven-query cubic behavior from the previous note is the case $k=2$.

## Scope and reproduction

The order improvement concerns the clean-return conditional protocol. Leakage and known-gate compilation costs require separate analysis. The result relies on the sector congruence for clean parallel access. Sequential protocols or decoding with an oracle-dependent output environment are outside the lower bound. [Brown, Harrow and Chuang](https://doi.org/10.1103/PhysRevA.70.052318) give broader context for high-order coherent error cancellation. The query count here follows from the discrete charges available in the odd-cycle oracle model.

The following exact rational check verifies the moment identities through $k=20$.

~~~python
from fractions import Fraction
from math import prod


def weights(k):
    m = 4 * k - 1
    charges = sorted(range(6 - m, m + 1, 8), key=abs)
    squares = [q * q for q in charges]
    unnormalized = [
        Fraction(1, q * prod(x - y for j, y in enumerate(squares) if j != i))
        for i, (q, x) in enumerate(zip(charges, squares))
    ]
    assert all(p > 0 for p in unnormalized)
    normalizer = sum(unnormalized)
    probabilities = [p / normalizer for p in unnormalized]
    for power in range(1, 2 * k - 1, 2):
        assert sum(p * q**power for p, q in zip(probabilities, charges)) == 0
    leading = sum(p * q**(2 * k - 1) for p, q in zip(probabilities, charges))
    assert leading == 1 / normalizer
    return charges, probabilities, leading


for k in range(1, 21):
    q, p, leading = weights(k)
    assert len(q) == k and len(set(q) | {-x for x in q}) == 2 * k
    if k <= 4:
        variance = sum(weight * charge**2 for weight, charge in zip(p, q))
        print(4 * k - 1, q, [str(x) for x in p], leading, variance)
~~~
