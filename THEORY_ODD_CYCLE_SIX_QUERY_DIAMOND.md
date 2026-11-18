# Exact diamond error of the six-query parity-drift recovery

The [six-query recovery](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md) proves a first-order query advantage on fully fielded odd Ising rings of length \(n\ge21\). Its previous error statement was \(\Theta(\epsilon^2)\). Here we compute its complete diamond error under common static parity drift, including noise within the plus sector.

Let
\[
 f=f_n=1-2\binom{2n}{n}/4^n,\qquad
 \gamma=3(1-f)\sin^2(4\epsilon),\qquad
 c=\left|1-\tfrac14e^{-6i\epsilon}-\tfrac34e^{2i\epsilon}\right|.
\]
For the fixed six-query construction with the split encoder selected with probability \(3/(4f)\), the diamond distance from the intended inverse, with no factor of one half, is exactly
\[
 {\cal E}_n(\epsilon)=
 \begin{cases}
 2\gamma,&\gamma\ge c,\\
 2c^2/(2c-\gamma),&\gamma<c .
 \end{cases}
\]
The first branch includes \(c=\gamma=0\), and all quantities are independent of the intended Hamiltonian. The leading coefficient is consequently
\[
 {\cal E}_n(\epsilon)=C_n\epsilon^2+O(|\epsilon|^3),\qquad
 C_n=
 \begin{cases}
 96(1-f_n),&f_n\le7/8,\\
 72/[12-48(1-f_n)],&f_n>7/8 .
 \end{cases}
\]
At the first admissible ring size \(n=21\), \(C_{21}=23.498048879555\ldots\). The plus-to-minus coherence alone gives leading coefficient six. The stronger coefficient comes from a reference-entangled input in the plus sector. Among odd sizes the branch changes at \(n=83\), and \(C_n\to6\) as \(n\to\infty\).

The formulas concern the stated construction. They do not establish an optimal second-order coefficient over all six-query protocols.

## Bell projectors and the reduced channel

In a fixed real basis for the plus parity space \(S_+\) of dimension \(D=2^{n-1}\), the shared-space projector of the construction is
\[
 Q=\sum_{I}|f_I^*\rangle\langle f_I^*|,\qquad
 f_I=\operatorname{vec}(T_I)/\sqrt D .
\]
Every \(T_I\), an odd Majorana monomial times charge conjugation restricted to \(S_+\), is a logical Pauli up to phase. Choose the computational parity basis to identify \(S_+\) with \(n-1\) logical qubits. The orthogonal \(f_I^*\) therefore form a subset of a full logical Pauli Bell basis. If \(r=\operatorname{rank}Q=fD^2\), then for Hermitian logical Paulis \(P\)
\[
 Q=\frac1{D^2}\sum_P a_P P\otimes\bar P,\qquad
 a_P=\sum_{I}\chi(P,T_I^*) .
\]
Here \(\chi\in\{\pm1\}\) is the Pauli commutation character. Thus \(a_I=r\) for the identity Pauli. Orthogonality of the two-register Pauli basis gives \(\sum_Pa_P^2=D^2r\).

Define the completely positive map
\[
 T_Q(\rho)=\operatorname{Tr}_{E}[Q(\rho\otimes I/D)Q]
          =\sum_P\frac{a_P^2}{D^4}P\rho P .
\]
In particular its total Pauli weight is \(f\), its identity weight is \(f^2\), and its nonidentity weight is \(f(1-f)\). Write \(\mathcal N\) for the normalized mixture of the nonidentity Pauli conjugations, when \(f<1\).

On the plus joint space the split decoder acts as \(M=aI+bQ\), where \(a=e^{-6i\epsilon}\) and \(b=e^{2i\epsilon}-e^{-6i\epsilon}\). Since \(|a|^2=|a+b|^2=1\) and \(\operatorname{Tr}_EQ/D=fI\), its reduced plus channel is
\[
 \rho\longmapsto \rho+|b|^2[T_Q(\rho)-f\rho].
\]
After mixing with the all-preferred decoder, the plus error is therefore \(\gamma(\mathcal N-\mathrm{id})\), since
\(p|b|^2 f(1-f)=3(1-f)\sin^2(4\epsilon)=\gamma\).
The minus block is unchanged. An off-diagonal parity block is multiplied by \(g=\frac14e^{-6i\epsilon}+\frac34e^{2i\epsilon}\). These formulas give the full error channel. The ideal joint unitary disappears under the program trace except for the intended data conjugation, so the diamond error is uniform in \(H\).

## Reference-assisted maximization

For a pure data–reference input, let \(u\) and \(v\) be its plus and minus components, with \(\|u\|^2=t\), \(\|v\|^2=1-t\). The difference from identity splits into a positive error output of trace \(\gamma t\), obtained from \(\mathcal N\) on \(|u\rangle\langle u|\), and the operator
\[
 -\gamma|u\rangle\langle u|
 +(g-1)|u\rangle\langle v|
 +(\bar g-1)|v\rangle\langle u| .
\]
The latter acts in a two-dimensional span and has trace norm
\(\sqrt{\gamma^2t^2+4c^2t(1-t)}\).
The triangle inequality bounds the output norm by
\[
 F(t)=\gamma t+\sqrt{\gamma^2t^2+4c^2t(1-t)} .
\]
For a difference of channels it suffices to optimize over pure inputs with a reference, so this is a diamond upper bound after maximizing \(t\).

Take \(u/\sqrt t\) maximally entangled between \(S_+\) and a \(D\)-dimensional reference subspace, and \(v/\sqrt{1-t}\) a minus data state with a reference orthogonal to that subspace. Each nonidentity Pauli maps this \(u\) to an orthogonal Bell state. The positive error term is then orthogonal to both \(u,v\), so the triangle bound is attained for every \(t\). A reference of dimension \(D+1\le2D\) is sufficient. Direct one-variable optimization gives \(t=1\) if \(\gamma\ge c\), and \(t=c/(2c-\gamma)\) otherwise, proving the displayed exact expression. At \(c=\gamma=0\) every input gives zero.

Taylor expansion yields \(\gamma=48(1-f)\epsilon^2+O(\epsilon^4)\) and \(c=6\epsilon^2+O(|\epsilon|^3)\), producing \(C_n\). The exact central-binomial comparisons at \(n=81,83\) locate the change of branch. The central-binomial ratio decreases with \(n\), so this is the only size transition.

## Implication for the query comparison

The deterministic seven-query construction has cubic leading error \(28|\epsilon|^3\). At small drift the six-query construction has the explicitly quantified quadratic cost above. This gives a reproducible comparison of query count against error order and magnitude, extending the earlier exact three-query response \(2|\sin(3\epsilon)|\).

The physical pentagon six-versus-seven problem remains open. For it, the next theoretical test remains the common polynomial dilation on the 13 physical tori in the [overlapping-block note](THEORY_ISING_PENTAGON_OVERLAP_DRIFT.md), including pointwise isometry and derivative constraints. For the long-ring construction, the exact channel formula allows direct comparison with noisy gate implementations once a compilation of its shared-projector decoder is available.

The [EUI manuscript and robustness appendix](https://arxiv.org/html/2506.20570v1) motivate comparing inversion errors under support perturbations. The common parity drift here admits a full channel formula and a reference-assisted worst-case norm. General channel-norm facts used in the maximization are given in [Watrous, *The Theory of Quantum Information*, Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/).

## Verification

The exact arithmetic checks evaluate the size thresholds and leading constants. The finite matrix check uses two logical qubits and Pauli Bell projectors of ranks 12, 13 and 15, whose fractions permit the same decoder mixture. It compares the proposed optimal reference input with the trace norm of the full error output at finite drift, and samples other input weights. These matrix checks verify the dimension-independent norm argument without constructing \(2^{21}\)-dimensional registers.

~~~python
from fractions import Fraction
from itertools import product
from math import comb

import numpy as np


def fraction(n):
    return 1 - Fraction(2 * comb(2*n, n), 4**n)


def leading(n):
    loss = 48 * (1 - fraction(n))
    return 2 * loss if loss >= 6 else Fraction(72, 1) / (12 - loss)


assert fraction(19) < Fraction(3, 4) < fraction(21)
assert fraction(81) < Fraction(7, 8) < fraction(83)
for size in (21, 23, 81, 83, 163):
    print(size, f"{float(fraction(size)):.12f}", f"{float(leading(size)):.12f}")

identity = np.eye(2)
single = (
    identity,
    np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]),
    np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
dim, refdim = 4, 5
tol = 2e-11
for rank in (12, 13, 15):
    f = Fraction(rank, 16)
    amplitudes = []
    for p in paulis:
        character_sum = sum(
            int(round(float(np.trace(p @ q @ p @ q).real / dim)))
            for q in paulis[:rank]
        )
        amplitudes.append(character_sum)
    weights = [Fraction(a*a, 256) for a in amplitudes]
    assert weights[0] == f*f and sum(weights) == f
    assert sum(weights[1:]) == f*(1-f)
    noise_weights = [float(w/(f*(1-f))) for w in weights[1:]]

    for eps in (0.001, 0.013, 0.17, 0.41):
        gamma = 3 * float(1-f) * np.sin(4*eps)**2
        g = 0.25 * np.exp(-6j*eps) + 0.75 * np.exp(2j*eps)
        c = abs(g-1)
        exact = 2*gamma if gamma >= c else 2*c*c/(2*c-gamma)
        optimum = 1.0 if gamma >= c else c/(2*c-gamma)
        for t in (*np.linspace(0, 1, 9), optimum):
            u = np.zeros(2*dim*refdim, dtype=complex)
            v = np.zeros_like(u)
            for i in range(dim):
                u[i*refdim+i] = np.sqrt(t/dim)
            v[dim*refdim+dim] = np.sqrt(1-t)
            change = -gamma * np.outer(u, u.conj())
            change += (g-1) * np.outer(u, v.conj())
            change += (g.conjugate()-1) * np.outer(v, u.conj())
            for p, weight in zip(paulis[1:], noise_weights):
                transformed = u.copy().reshape(2*dim, refdim)
                transformed = np.vstack((p @ transformed[:dim], transformed[dim:])).reshape(-1)
                change += gamma * weight * np.outer(transformed, transformed.conj())
            observed = float(np.abs(np.linalg.eigvalsh(change)).sum())
            bound = gamma*t + np.sqrt(gamma*gamma*t*t+4*c*c*t*(1-t))
            assert abs(observed-bound) < tol
            assert observed <= exact + tol
            if t == optimum:
                assert abs(observed-exact) < tol
    print("Finite-drift Pauli Bell projector rank", rank, "verified.")
~~~
