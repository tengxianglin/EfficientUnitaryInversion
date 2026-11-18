# Balanced six-query recovery halves the long-ring leading error

For the fully fielded odd Ising cycle, let \(P=\prod_j X_j\) and suppose every query uses \(W_\epsilon=e^{-i(H+\epsilon P)}\). The existing [six-query construction](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md) is correct at zero drift and cancels the first order for odd \(n\ge21\). Its [exact error calculation](THEORY_ODD_CYCLE_SIX_QUERY_DIAMOND.md) shows a larger quadratic error inside its selected parity sector than the cross-sector coherence test suggests. We can reduce that worst-case error by balancing the two parity choices.

**Construction and exact error.** Choose the prior six-query protocol with a maximally mixed plus-sector program with probability \(1/2\). With probability \(1/2\), choose its mirrored version using a minus-sector program, with the charge signs reversed. The choice is independent of the input and the oracle, and every run uses six unconditional forward queries. Set
\[
 f_n=1-\frac{2\binom{2n}{n}}{4^n}.
\]
For every odd \(n\ge21\), the resulting deterministic decoded channel has exact diamond error
\[
 \boxed{\quad
 {\cal E}^{\rm bal}_n(\epsilon)
 =1-\cos^3(2\epsilon)
  +\frac32(1-f_n)\sin^2(4\epsilon)
 \quad}
\]
relative to the intended inverse, uniformly in \(H\), without a factor of one half. In particular,
\[
 {\cal E}^{\rm bal}_n(\epsilon)
 =[6+24(1-f_n)]\epsilon^2+O(\epsilon^4).
\]
At \(n=21\) the coefficient is \(11.874512219889\ldots\), compared with \(23.498048879555\ldots\) for the prior unbalanced protocol. The balanced construction retains the six-query optimum for first-order suppression on these ring lengths. Optimal second-order error over all six-query protocols remains open.

## Circuit implementation and full reduced channel

The [unbalanced decoder](THEORY_ODD_CYCLE_SIX_QUERY_DIAMOND.md#bell-projectors-and-the-reduced-channel) uses the shared Bell projector \(Q_+\) on two plus registers, with \(\operatorname{Tr}_2Q_+/D=f_n I\) and \(D=2^{n-1}\). The same odd-grade Majorana construction in the minus block gives \(Q_-\) with identical rank and marginal. Its fixed two-query intertwiner and its four-query invariant spectators are defined by the same formulas with the parity label reversed. The mirror uses the same split probability \(p=3/(4f_n)\). In a split branch, plus data carries charge zero and minus data has charges \(2,-6\), the negatives of the original plus charges. All the encoders, decoder and flag preparation are independent of \(H,\epsilon\). The only added operation is a classical fair choice of the two known fixed circuits, which can also be prepared as a flag and discarded.

The ideal program's unitary depends on the chosen parity block but remains independent of the data input. Thus both branches implement the same ideal data inverse coherently across the two sectors. Mixing preserves the ideal target.

Define
\[
 \gamma=3(1-f_n)\sin^2(4\epsilon),\qquad
 g=\tfrac14 e^{-6i\epsilon}+\tfrac34 e^{2i\epsilon},\qquad
 c_0=1-\operatorname{Re}g .
\]
Let \(\mathcal N_+\) and \(\mathcal N_-\) be the nonidentity logical Pauli channels obtained from \(Q_+\) and \(Q_-\), respectively. Their detailed Pauli weights may differ, but they are normalized mixtures with no identity component. Removing the ideal inverse, the balanced error channel acts as follows:
\[
 \rho_{++}\mapsto \rho_{++}+\tfrac{\gamma}{2}(\mathcal N_+-\mathrm{id})(\rho_{++}),\qquad
 \rho_{--}\mapsto \rho_{--}+\tfrac{\gamma}{2}(\mathcal N_--\mathrm{id})(\rho_{--}),
\]
and \(\rho_{+-}\mapsto(\operatorname{Re}g)\rho_{+-}\). For the mirror, reversing both charge signs replaces \(g\) by \(\bar g\) on this coherence. The average removes its imaginary part exactly. The identity \(\operatorname{Re}g=\cos^3(2\epsilon)\) follows from the triple-angle formula.

## Diamond-norm maximization

For a pure input with a reference, let \(u,v\) be its plus and minus components, with \(\|u\|^2=t\), \(\|v\|^2=1-t\). The error operator is a positive Pauli-noise output with total trace \(\gamma/2\), plus an operator in the two-dimensional span of \(u,v\). In the normalized basis of those two vectors, the latter matrix is
\[
 \begin{pmatrix}
 -\frac{\gamma}{2}t&-c_0\sqrt{t(1-t)}\\
 -c_0\sqrt{t(1-t)}&-\frac{\gamma}{2}(1-t)
 \end{pmatrix}.
\]
We have \(c_0\ge\gamma/2\). To prove it, put \(x=\cos(2\epsilon)\). Since \(f_n\ge3/4\),
\[
 c_0-\gamma/2
 \ge 1-x^3-\tfrac32x^2(1-x^2)
 =\tfrac12(x-1)^2(3x^2+4x+2)\ge0 .
\]
The two-dimensional matrix therefore has nonpositive determinant. Its trace norm is
\[
 \sqrt{\tfrac{\gamma^2}{4}(2t-1)^2+4c_0^2t(1-t)}
 \ \le\ c_0,
\]
with equality at \(t=1/2\). The total trace norm is at most \(\gamma/2+c_0\). For a difference of channels it suffices to consider such reference-assisted pure inputs.

Take equal superposition of a maximally entangled plus input and a maximally entangled minus input, with the two reference spaces orthogonal. Every nonidentity Pauli maps its Bell vector to an orthogonal vector in the same parity block. The positive noise output is then orthogonal to the two-dimensional span above, and the norm equals \(\gamma/2+c_0\). A reference of dimension \(2D\), equal to the data dimension, suffices. This proves the exact formula. Its Taylor series contains only even powers.

Balancing is also guaranteed to be no worse than either orientation at every drift. Each orientation has the same exact error, since its noise weight and cross-sector magnitude agree. Convexity of the diamond norm bounds the error of their average by that common value. The explicit formula quantifies the improvement, including the smaller leading coefficient.

## Consequences and next verification

The leading coefficient decreases monotonically from its \(n=21\) value towards six with increasing odd ring size. For the unbalanced construction, write \(\lambda=48(1-f_n)\). When \(\lambda\ge6\) its coefficient is \(2\lambda\), while balancing gives \(6+\lambda/2\), improving by a factor close to two at the first allowed size. When \(0<\lambda<6\), the difference of the unbalanced coefficient and the balanced one is
\[
 \frac{72}{12-\lambda}-(6+\lambda/2)
 =\frac{\lambda^2}{2(12-\lambda)}>0.
\]
Thus balancing strictly improves the leading coefficient at every finite allowed odd size.

The deterministic [seven-query recovery](THEORY_ODD_CYCLE_DETERMINISTIC_RECOVERY.md) has cubic leading error \(28|\epsilon|^3\). The balanced six-query result sharpens the explicit query-versus-error comparison. The next optimization is to determine whether a different six-query decoder can improve the balanced quadratic coefficient. The separate physical pentagon problem remains six versus seven; its next constraint test is the [13 physical tori](THEORY_ISING_PENTAGON_OVERLAP_DRIFT.md) with a common polynomial Stinespring map and pointwise isometry and derivative conditions.

The [EUI manuscript and robustness appendix](https://arxiv.org/html/2506.20570v1) motivate quantitative noise comparisons. The use of a reference in the exact norm follows standard channel-discrimination theory as presented by [Watrous, Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/).

## Verification

The script checks exact leading coefficients and the polynomial inequality, then tests the complete finite-drift formula with logical two-qubit Pauli Bell projectors of ranks 12, 13 and 15. The two sector projectors are chosen differently. It verifies that the error output on the proposed maximizing input has the stated norm and that sampled reference weights obey the bound. These are finite matrix checks of the norm argument; the all-length statement follows from the formulas above.

~~~python
from fractions import Fraction
from itertools import product
from math import comb

import numpy as np
import sympy as sp


x = sp.symbols("x")
assert sp.expand(
    1-x**3-sp.Rational(3, 2)*x*x*(1-x*x)
    -(x-1)**2*(3*x*x+4*x+2)/2
) == 0
for n in (21, 23, 81, 83, 163):
    f = 1-Fraction(2*comb(2*n, n), 4**n)
    lam = 48*(1-f)
    balanced = 6+lam/2
    previous = 2*lam if lam >= 6 else 72/(12-lam)
    assert 0 < balanced < previous
    print(n, f"{float(previous):.12f}", f"{float(balanced):.12f}")

single = (
    np.eye(2),
    np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]),
    np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
dim, refdim = 4, 8
tolerance = 3e-11
for rank in (12, 13, 15):
    f = Fraction(rank, 16)
    sector_weights = []
    for labels in (paulis[:rank], list(reversed(paulis))[:rank]):
        amplitudes = [
            sum(int(round(float(np.trace(p@q@p@q).real/dim))) for q in labels)
            for p in paulis
        ]
        weights = [Fraction(a*a, dim**4) for a in amplitudes]
        assert weights[0] == f*f and sum(weights) == f
        sector_weights.append([float(w/(f*(1-f))) for w in weights[1:]])

    for eps in (0.001, 0.013, 0.17, 0.41, 1.2):
        gamma = 3*float(1-f)*np.sin(4*eps)**2
        g = (np.exp(-6j*eps)+3*np.exp(2j*eps))/4
        c0 = 1-g.real
        assert c0 >= gamma/2-tolerance
        formula = c0+gamma/2
        assert abs(formula-(1-np.cos(2*eps)**3+gamma/2)) < tolerance
        for t in (*np.linspace(0, 1, 9), 0.5):
            u, v = np.zeros(2*dim*refdim, complex), np.zeros(2*dim*refdim, complex)
            for i in range(dim):
                u[i*refdim+i] = np.sqrt(t/dim)
                v[(dim+i)*refdim+dim+i] = np.sqrt((1-t)/dim)
            change = -gamma/2*(np.outer(u, u.conj())+np.outer(v, v.conj()))
            change -= c0*(np.outer(u, v.conj())+np.outer(v, u.conj()))
            for sector, vector in enumerate((u, v)):
                for p, probability in zip(paulis[1:], sector_weights[sector]):
                    transformed = vector.reshape(2*dim, refdim).copy()
                    transformed[sector*dim:(sector+1)*dim] = (
                        p @ transformed[sector*dim:(sector+1)*dim]
                    )
                    transformed = transformed.reshape(-1)
                    change += gamma/2*probability*np.outer(transformed, transformed.conj())
            observed = float(np.abs(np.linalg.eigvalsh(change)).sum())
            bound = gamma/2+np.sqrt(
                gamma*gamma/4*(2*t-1)**2+4*c0*c0*t*(1-t)
            )
            assert abs(observed-bound) < tolerance
            assert observed <= formula+tolerance
            if t == 0.5:
                assert abs(observed-formula) < tolerance
    print("Balanced finite-drift norm verified at Bell projector rank", rank)
~~~
