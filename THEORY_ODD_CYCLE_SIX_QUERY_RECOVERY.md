# Six queries attain first-order parity-drift suppression on long odd Ising cycles

Let \(n\) be odd and set \(H=\sum_j h_jX_j+\sum_j J_j Z_jZ_{j+1\bmod n}\) and \(P=\prod_jX_j\). All fields and edges are independently tunable. The task is to invert \(e^{-iH}\) by deterministic fixed-order access to the same noisy oracle \(W_\epsilon=e^{-i(H+\epsilon P)}\), with no postselection. Every known operation is independent of \(H,\epsilon\), and all calls are unconditional and forward.

**Theorem.** For every odd \(n\ge21\), exactly six calls are necessary and sufficient for ideal exact inversion and zero first-order diamond error in the common static drift \(\epsilon P\). The six calls can be parallel, with fixed encoding and decoding and a discarded, oracle-dependent environment. The constructed channel has \(\Theta(\epsilon^2)\) diamond error, uniformly in \(H\). Together with the [triangle converse](THEORY_ISING_TRIANGLE_SEVEN_DRIFT.md), this proves that the minimum drops from seven at \(n=3\) to six for all odd \(n\ge21\). For odd \(5\le n\le19\) the full-promise minimum remains six or seven.

The lower bound is the [arbitrary fixed-order odd-cycle converse](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md). The new ingredient is a two-call realization of part of the tensor product of two inverse spinors. This part is large enough on long rings to supply an opposite-sign drift charge with the required average.

## A shared two-spinor subspace

Let \(S_s\) be the parity-\(s\) space of dimension \(D=2^{n-1}\), in a fixed real basis. Use the [Majoranas and charge conjugation](THEORY_ODD_CYCLE_THREE_QUERIES.md#a-fixed-encoding-for-odd-numbers-of-fermionic-modes) \(\gamma=(a_0,b_0,\ldots,a_{n-1},b_{n-1})\), \(C=b_0\cdots b_{n-1}\). For an odd subset \(I\subset\{0,\ldots,2n-1\}\) write \(\Gamma_I\) for the ordered Majorana product. The operators \(T_I=(\Gamma_I C)|_{S_+}\) are unitary on \(S_+\), as both factors flip parity. For an even Majorana Gaussian \(g\) with vector rotation \(R\), charge conjugation gives \(C\overline g C^\dagger=g\). Hence, with \(g_+=g|_{S_+}\),
\[
 (g_+\otimes g_+)\operatorname{vec}(T_I)
 =\sum_{|J|=|I|}(\wedge^{|I|}R)_{JI}\operatorname{vec}(T_J).
\]
Indeed the conjugated product of distinct orthonormal Majoranas transforms by the degree-\(|I|\) exterior power. The matrix on that grade is real. Use \(\operatorname{vec}T=\sum_{ab}T_{ab}|a\rangle|b\rangle\).

For odd grades \(1\le |I|<n\), the normalized vectors \(f_I=\operatorname{vec}(T_I)/\sqrt D\) are mutually orthogonal, including across grades. For distinct \(I,J\), the product \(\Gamma_I^\dagger\Gamma_J\) is proportional to a nonempty Majorana monomial of degree strictly less than \(2n\). Its trace in either parity block vanishes, since the projected trace is half the sum of the full trace and the trace with \(P\) inserted, and both are nonidentity Majorana monomials. Conjugation by \(C\) just swaps sector traces. This establishes the orthogonality.

Let \(Q\) be the projector onto the span of the \(\overline f_I\) in \(S_+\otimes S_+\), and \(A=\sum_I |f_I\rangle\langle\overline f_I|\), an isometry on \(\operatorname{ran}Q\). Conjugating the covariance equation shows that \(Q\) commutes with \(\overline{g_+}^{\otimes2}\) and
\[
 (g_+\otimes g_+)A=A(\overline{g_+}\otimes\overline{g_+}).
\]
The rank and normalized marginal of \(Q\) are
\[
 r=\sum_{\substack{k<n\\k\text{ odd}}}\binom{2n}{k}
   =D^2-\tfrac12\binom{2n}{n},\qquad
 \frac{\operatorname{Tr}_2Q}{D}=f_n I,\qquad f_n=\frac{r}{D^2}.
\]
The rank identity pairs odd grades above and below \(n\). The marginal follows since each \(f_I\) is the normalized vectorization of a unitary and has maximally mixed one-register marginals.

## Six unconditional calls and a fixed decoder

The logical input is the data \(S_+\oplus S_-\) and a spectator \(E\cong S_+\). Initialize \(E\) as half of a fixed maximally entangled state with an unqueried reference, to be discarded together with \(E\) at the end. The desired logical unitary before discarding is \(\overline U\otimes\overline U_+\), where \(U=e^{-iH}\) and \(\overline U=U^\dagger\) since \(H\) is real. Thus the ideal spectator/reference state is generally oracle dependent.

Use the prior three-call sector encoders \(W_+,W_-\), and the fixed [four-call invariant spectator state](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#exact-drift-response-and-a-seven-query-construction) \(\Omega_-\in S_-^{\otimes4}\). The following three maps act coherently on orthogonal subspaces of the joint input. All six slots are queried in every case.

| Joint input subspace | Fixed encoding into the six queried registers | Slot parities | Drift charge |
|---|---|---|---|
| Plus data and spectator in \(\operatorname{ran}Q\) | \(A\) on the pair, then append \(\Omega_-\) | \(++----\) | \(-2\) |
| Plus data and spectator in \(\ker Q\) | \(W_+\otimes W_+\) | \(++++++\) | \(6\) |
| Minus data and plus spectator | \(W_+\) on spectator and \(W_-\) on data, in that register order | \(+++---\) | \(0\) |

Each map is isometric on its subspace. The three images are orthogonal by their distinct slot parities. They carry the same desired joint unitary restricted to the corresponding logical projections, by the intertwiner for \(A\), invariance of \(\Omega_-\), and the identities for \(W_s\). The \(Q\) and \(\ker Q\) subspaces are invariant under \(\overline U_+^{\otimes2}\). Thus the single encoder formed by summing these maps is an isometry. Its inverse on the encoded image is a fixed decoder, extendible to a unitary with blank output registers. The noisy oracle preserves all three images, and the decoder coherently returns their outputs to the joint data/spectator space. In particular it does not leave any flag that records membership in \(Q\) versus \(\ker Q\). There is also an all-preferred variant, using \(W_+\otimes W_+\) on all plus data and spectator inputs, with the same minus-data encoding.

The joint decoded unitary is the desired joint unitary times \(M_\epsilon\), where \(M_\epsilon=I\) on minus data, and on plus data and spectator
\[
 M_\epsilon=aI+bQ,\qquad a=e^{-6i\epsilon},\quad b=e^{2i\epsilon}-e^{-6i\epsilon}
\]
in the split variant. In the all-preferred variant \(M_\epsilon=aI\) on plus data. Since the spectator's desired output unitary disappears under the partial trace, the data error channel before the intended inverse is independent of \(H\). In the split variant the first-order joint generator is \(6I-8Q\) on plus data and zero on minus data. Partial trace on a spectator initialized in \(I/D\) gives the data generator \((6-8f_n)\Pi_+\), where \(\Pi_+\) projects onto plus data. This follows by differentiating the joint conjugation and taking the spectator trace of the commutator.

Choose the split variant with probability \(p=3/(4f_n)\), and the all-preferred variant otherwise. This choice uses an input-independent flag that is discarded. The mean first-order generator vanishes because \(pf_n=3/4\). An admissible probability exists when \(f_n\ge3/4\). Exactly,
\[
 f_n=1-2\binom{2n}{n}/4^n .
\]
The central-binomial fraction decreases with \(n\), since its ratio at \(n+1\) versus \(n\) is \((2n+1)/(2n+2)\). Exact integer comparison gives \(f_{19}<3/4<f_{21}\). Thus every odd \(n\ge21\) admits the protocol, and the prior fixed-order lower bound makes six optimal for this objective.

## Error order and scope

For any plus-to-minus input coherence, the resulting error channel multiplies it by
\[
 (1-p f_n)e^{-6i\epsilon}+p f_n e^{2i\epsilon}
   =\tfrac14e^{-6i\epsilon}+\tfrac34e^{2i\epsilon}.
\]
Its departure from one is \(-6\epsilon^2+O(|\epsilon|^3)\), a diamond lower bound in magnitude using a trace-norm-one coherence. The finite-dimensional error channel is analytic in \(\epsilon\), \(H\)-independent and has zero linear term, giving the matching \(O(\epsilon^2)\) order. The [full diamond-error calculation](THEORY_ODD_CYCLE_SIX_QUERY_DIAMOND.md) gives the exact finite-drift norm for this construction. At \(n=21\) its leading quadratic coefficient is \(23.498048879555\ldots\), because within-sector noise dominates the cross-sector test. The optimal second-order coefficient over all six-query protocols remains open. The known seven-query protocol gives cubic suppression when that stronger objective is needed.

At six calls the decoder restores the working registers while retaining an oracle-dependent spectator state. This is compatible with the [clean parallel query congruence](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md), whose ideal output workspace is required to be fixed. The exact threshold \(n=21\) belongs to this construction. Lowering it or proving a converse for \(5\le n\le19\) requires controlling other possible oracle-dependent environments. The next step for \(n=5\) is to bound how much weight a general six-call comb can route through the two-query branch when the environment transforms across physical eigenbases. A separate implementation problem is to compile the fixed projector split into elementary gates.

The [EUI preprint](https://arxiv.org/html/2506.20570v1) gives the structured-Hamiltonian setting and numerical robustness tests under support perturbations. The exterior-power action is standard Clifford algebra, as treated in [Deligne's *Notes on Spinors*, §4](https://publications.ias.edu/sites/default/files/79_NotesOnSpinors.pdf). The protocol uses these common tensor components to reroute forward calls coherently and cancel a specific physical drift.

## Verification

The exact arithmetic check below establishes the size threshold and drift moments. The finite NumPy check constructs the shared subspace at \(n=3,5\), checks its orthonormality, maximally mixed marginal and two-query intertwiner for every quadratic Majorana generator, and checks the decoded coherence under drift. The threshold at \(n=21\) follows by the rank formula and exact arithmetic.

Run the fenced Python block with NumPy installed. From the repository root it can be extracted with:
~~~bash
sed -n '/^~~~python$/,/^~~~$/p' THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md | sed '1d;$d' | python
~~~

~~~python
from fractions import Fraction
from itertools import combinations
from math import comb

import numpy as np


def shared_fraction(n):
    return 1 - Fraction(2 * comb(2 * n, n), 4**n)


assert shared_fraction(19) < Fraction(3, 4) < shared_fraction(21)
for n in (3, 5, 19, 21, 23):
    rank = sum(comb(2*n, k) for k in range(1, n, 2))
    assert Fraction(rank, 4**(n-1)) == shared_fraction(n)
    if n >= 21:
        p = Fraction(3, 4) / shared_fraction(n)
        assert 0 < p <= 1
        charges = ((1 - p * shared_fraction(n), 6), (p * shared_fraction(n), -2))
        assert sum(weight * q for weight, q in charges) == 0
        assert sum(weight * q**2 for weight, q in charges) == 12
print("Exact ranks, size threshold (19 < threshold <= 21), and drift moments verified.")


def local_majoranas(n):
    identity = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1])
    for site in range(n):
        for local in (x, -y):
            matrix = np.ones((1, 1))
            for k in range(n):
                matrix = np.kron(matrix, z if k < site else local if k == site else identity)
            yield matrix


def verify(n):
    gammas = list(local_majoranas(n))
    size = 2**n
    plus = [i for i in range(size) if i.bit_count() % 2 == 0]
    dim = len(plus)
    sector = np.ix_(plus, plus)
    c = np.eye(size, dtype=complex)
    for g in gammas[1::2]:
        c = c @ g

    columns = []
    for k in range(1, n, 2):
        for labels in combinations(range(2*n), k):
            monomial = np.eye(size, dtype=complex)
            for j in labels:
                monomial = monomial @ gammas[j]
            columns.append((monomial @ c)[sector].reshape(-1) / np.sqrt(dim))

    f = np.column_stack(columns)
    fbar = f.conj()
    rank = f.shape[1]
    np.testing.assert_allclose(f.conj().T @ f, np.eye(rank), atol=1e-12, rtol=0)
    q = fbar @ fbar.conj().T
    route = f @ fbar.conj().T
    marginal = np.trace(q.reshape(dim, dim, dim, dim), axis1=1, axis2=3) / dim
    fraction = float(shared_fraction(n))
    np.testing.assert_allclose(marginal, fraction * np.eye(dim), atol=1e-12, rtol=0)

    for j, k in combinations(range(2*n), 2):
        block = (gammas[j] @ gammas[k])[sector]
        generator = np.kron(block, np.eye(dim)) + np.kron(np.eye(dim), block)
        np.testing.assert_allclose(generator @ route, route @ generator.conj(),
                                   atol=1e-12, rtol=0)

    eps = 0.013
    preferred, alternate = np.exp(-6j * eps), np.exp(2j * eps)
    decoded = preferred * np.eye(dim**2) + (alternate - preferred) * q
    np.testing.assert_allclose(decoded.conj().T @ decoded, np.eye(dim**2),
                               atol=1e-12, rtol=0)
    coherence = np.trace(decoded.reshape(dim, dim, dim, dim), axis1=1, axis2=3) / dim
    expected = (1 - fraction) * preferred + fraction * alternate
    np.testing.assert_allclose(coherence, expected * np.eye(dim), atol=1e-12, rtol=0)
    print(n, rank, f"{fraction:.10f}", "all quadratic generators and decoded coherence verified")


for n in (3, 5):
    verify(n)
~~~
