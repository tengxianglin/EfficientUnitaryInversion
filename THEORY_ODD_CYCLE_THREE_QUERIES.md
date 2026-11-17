# Three-query exact inversion of the fully fielded odd Ising cycle

Let $n\geq3$ be odd and let
$$
H=\sum_{j=0}^{n-1}h_jX_j+\sum_{j=0}^{n-1}J_jZ_jZ_{j+1\bmod n},\qquad U=e^{-iH},
$$
with all coefficients real and independently tunable. The oracle supplies unconditional forward calls to the same $U$. **Exactly three calls are necessary and sufficient for deterministic exact inversion in the fixed-order model.** The upper bound uses two extra $n$-qubit registers, both restored at the end. The fixed encoding below also preserves superpositions of the two parity sectors. The [prior lower bound](THEORY_HERALDED_COMMUTING.md#restricting-a-heralded-converse-to-a-commuting-slice) applies to heralded protocols with nonzero success somewhere.

## Quadratic representation in the two sectors

Set $P=\prod_j X_j$, and let $S_s$ be its eigenspace with eigenvalue $s\in\{+1,-1\}$. Each $S_s$ has dimension $D=2^{n-1}$ and admits a real orthonormal basis. Use the Majoranas
$$
a_j=(X_0\cdots X_{j-1})Z_j,\qquad b_j=(X_0\cdots X_{j-1})Y_j.
$$
They are Hermitian, square to the identity and anticommute at distinct labels. They each flip the parity $P$. We have $X_j=i a_j b_j$, $Z_jZ_{j+1}=i b_j a_{j+1}$ for $j<n-1$, and $Z_{n-1}Z_0=-iP b_{n-1}a_0$. With $P$ replaced by $s$ in the last term, let $g^{(s)}$ be the exponential of the resulting real linear combination of Majorana products in $-iH$, acting on the full $n$-qubit space. Then $U|_{S_s}=g^{(s)}|_{S_s}$. The two values of $s$ need not give the same $g^{(s)}$.

## A fixed encoding for odd numbers of fermionic modes

Write $\gamma_0,\ldots,\gamma_{2n-1}=(a_0,b_0,\ldots,a_{n-1},b_{n-1})$ and fix $C=b_0\cdots b_{n-1}$. Since $n$ is odd, $C$ flips parity and $C\overline{\gamma_j}C^\dagger=-\gamma_j$ for all $j$. Indeed, $a_j$ is real and anticommutes with all $n$ factors of $C$, while $b_j$ is imaginary and anticommutes with the other $n-1$ factors. It follows that $C\overline{g}C^\dagger=g$ for every $g=e^{\sum_{p<q}r_{pq}\gamma_p\gamma_q}$ with real $r_{pq}$. In this section write $g_s=g|_{S_s}$ for the two blocks of any one such $g$.

Conjugation by $g$ preserves the real span of the Majoranas and acts there by an orthogonal matrix $R$, with $g\gamma_jg^\dagger=\sum_k R_{kj}\gamma_k$. Closure follows from the commutator with each bilinear generator, and orthogonality follows from preservation of the Majorana anticommutators. For fixed $s$, set $T_j=(\gamma_j C)|_{S_s}$. The charge-conjugation identity gives
$$
g_s T_j=\sum_k R_{kj} T_k\,\overline{g_s},\qquad
(g_s\otimes g_s)\operatorname{vec}(T_j)=\sum_k R_{kj}\operatorname{vec}(T_k),
$$
using the convention $\operatorname{vec}(T)=\sum_{ab}T_{ab}|a\rangle|b\rangle$ in the real sector basis.

Define the parameter-independent map
$$
W_s|\psi\rangle=\frac{1}{\sqrt{2nD}}
\sum_j(T_j|\psi\rangle)\otimes\operatorname{vec}(T_j)
\quad:\quad S_s\longrightarrow S_s^{\otimes3}.
$$
The vectors $\operatorname{vec}(T_j)$ are orthogonal with norm $\sqrt D$. Their inner products reduce to sector traces of $\gamma_j\gamma_k$ by unitarity of $C$. For $j\ne k$ those traces vanish, since $\operatorname{Tr}(\gamma_j\gamma_k)=\operatorname{Tr}(P\gamma_j\gamma_k)=0$. The second identity uses $n\geq 3$, so the two-Majorana product is distinct from the full parity product. Each $T_j$ is unitary on its sector. Thus $W_s^\dagger W_s=I_{S_s}$. The two displayed transformation laws and $R^\mathsf{T}R=I$ give the exact intertwiner
$$
(g_s^{\otimes3}) W_s=W_s\,\overline{g_s}.
$$

## Coherent use of the physical oracle

Apply the intertwiner with $g=g^{(s)}$ for each $s$. Every term of $W_s$ lies in the same parity sector on all three query registers, so in that branch the physical oracle acts as $(g^{(s)}|_{S_s})^{\otimes3}$. Combine the two encodings into $W=W_+\oplus W_-$. The images are orthogonal and their intertwining identities have no relative phase, giving $U^{\otimes3}W=W\overline U$ on the whole input space. Since $H$ is real symmetric in the physical basis, $\overline U=U^\dagger$.

Extend $W$ to a fixed unitary on the data register and two blank $n$-qubit registers. Encode, make one forward call on each register, and decode with the inverse fixed unitary. The three calls can also be made sequentially on the three registers. This counts oracle calls and workspace qubits. It leaves the cost of compiling the known encoding gates open.

For the matching lower bound, the commuting restriction sets all $h_j=0$. The odd-cycle edge signs then give the three-call lower bound, which [the heralded slice theorem](THEORY_HERALDED_COMMUTING.md#restricting-a-heralded-converse-to-a-commuting-slice) transfers to the full linear promise. Combined with the [system-only Pauli lower bound](THEORY_ODD_CYCLE_PAULI.md), the result separates a three-call coherent encoding from Pauli-only control, which requires at least five calls.

## Reproduction

The check omits the known normalization and Hadamard-rotates each physical qubit so that parity sectors are computational-basis subsets. It verifies each sector Gram matrix and the full generator intertwining identities for $n=3,5$. Gaussian-integer matrices are evaluated in exact range of complex128. The proof above covers all odd $n$.

~~~python
from functools import reduce

import numpy as np


def verify(n):
    # Hadamard on each site: X -> Z, Z -> X, Y -> -Y.
    identity = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1]).astype(complex)

    def word(ops):
        return reduce(np.kron, (ops.get(j, identity) for j in range(n)))

    majoranas = [
        word({**{k: z for k in range(j)}, j: op})
        for j in range(n)
        for op in (x, -y)
    ]
    charge = reduce(np.matmul, majoranas[1::2])
    parity = np.array([(-1) ** i.bit_count() for i in range(2**n)])
    terms = [word({j: z}) for j in range(n)] + [
        word({j: x, (j + 1) % n: x}) for j in range(n)
    ]
    for s in (1, -1):
        indices = np.flatnonzero(parity == s)
        block = np.ix_(indices, indices)
        factors = [(gamma @ charge)[block] for gamma in majoranas]
        # W with its common normalization omitted. All entries below are
        # Gaussian integers small enough for exact complex128 arithmetic.
        encoding = sum(np.einsum("ai,bc->abci", m, m) for m in factors)
        flat = encoding.reshape(len(indices)**3, len(indices))
        scale = 2 * n * len(indices)
        np.testing.assert_array_equal(flat.conj().T @ flat, scale * np.eye(len(indices)))
        for term in terms:
            h = term[block]
            residual = (
                np.einsum("ad,dbci->abci", h, encoding)
                + np.einsum("bd,adci->abci", h, encoding)
                + np.einsum("cd,abdi->abci", h, encoding)
                + np.einsum("abci,ij->abcj", encoding, h)
            )
            assert not np.any(residual), (n, s)
    print(f"L={n}: both isometries and all {2*n} generator identities verified")


for length in (3, 5):
    verify(length)
~~~

[Mo, Lin and Wang, arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1), Section IV and Appendix A, discuss the odd-cycle family and give a three-call Pauli construction for a restricted-field example. The encoding above instead exploits covariance of Clifford multiplication, for which [Deligne's Notes on Spinors, Section 4.9](https://publications.ias.edu/sites/default/files/79_NotesOnSpinors.pdf) provides representation-theoretic context. The result here makes no priority claim for the intertwiner as a representation-theoretic fact.
