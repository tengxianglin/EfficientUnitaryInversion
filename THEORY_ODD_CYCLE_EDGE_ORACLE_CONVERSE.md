# An edge oracle fixes the minimax value of diagonal syndrome recovery

The [maximum-likelihood diagonal decoder](THEORY_ODD_CYCLE_CONDITIONAL_SYNDROME.md) improves every field-Pauli oracle and retains a pointwise safety bound over the full physical family. The remaining question is its full-family supremum. A single physical edge oracle answers it for the entire diagonal correction class.

**Theorem.** Fix the coherent six-query encoder on an odd ring \(n\ge21\), the fair classical choice of program parity, and the selective recovery architecture. The recovery preserves the ideal-flag physical program subspace coherently, discards the orthogonal split-flag branch without data correction, and on an ideal-flag complementary Bell syndrome \(R\) applies
\[
 A_{R,\alpha}R^\dagger,\qquad
 A_{R,\alpha}\text{ diagonal in the field-occupation basis},\quad
 \sum_\alpha A_{R,\alpha}^\dagger A_{R,\alpha}=I
\]
to the selected data parity block, with the outcomes \(\alpha\) discarded. The diagonal channel may depend arbitrarily on \(R\), orientation and drift-independent design parameters. This includes fixed label correction, fixed or conditional random diagonal Paulis, arbitrary random diagonal unitaries, and diagonal Kraus channels.

For every such decoder and every real \(\epsilon\), its exact worst-case diamond error over the physical Ising family is
\[
 \sup_H {\cal E}_{H}(\epsilon)
 =\left|1-\tfrac14e^{-6i\epsilon}-\tfrac34e^{2i\epsilon}\right|
   +\frac32(1-f_n)\sin^2(4\epsilon),\qquad
 f_n=1-\frac{2\binom{2n}{n}}{4^n}.
\]
The legal edge Hamiltonian \(H_{\rm edge}=(\pi/2)Z_0Z_1\) attains this bound for all drift amplitudes. Thus this entire recovery class has the same minimax value as the old balanced inverse decoder, although individual oracles can improve. At \(n=21\) the worst-case quadratic coefficient is \(11.874512219889\ldots\).

In particular the field-Pauli gain \(0.148358524720\ldots\) of the maximum-likelihood rule remains valid on that test family, while its full-family worst case is now resolved. Further improvement of the minimax error requires leaving the diagonal correction class or changing the coherent flag treatment or encoder. The unrestricted physical pentagon query minimum and the global six-query quadratic optimum remain open.

## 1. The selective residual bound extends to diagonal channels

Let \(V\) be the intended inverse on the selected parity, \(v_R\) its ideal program coefficients, and \(L_R\) the data amplitude from the shared projector on Bell label \(R\). The [selective recovery proof](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md#1-the-recovery-and-its-residual-channels) gives
\[
 \sum_RL_R^\dagger L_R=fI,\qquad
 \sum_R\bar v_RL_R=fV .
\]
For \(R\) outside the physical ideal-program span, \(v_R=0\). Replacing its amplitude by the collection \(A_{R,\alpha}R^\dagger L_R\) preserves the squared Kraus sum by completeness and leaves its contraction with the ideal program zero. On protected labels no measurement within the protected subspace or data correction is performed. The orthogonal flag remains uncorrected.

Consequently each orientation's noisy selected-sector channel, after removal of the intended inverse, has form
\[
 (1-\gamma)\,\mathrm{id}+\gamma\mathcal N_{H,s},\qquad
 \gamma=3(1-f)\sin^2(4\epsilon),
\]
with \(\mathcal N_{H,s}\) trace preserving and completely positive. The cross-parity coherence multiplier is \(g=\frac14e^{-6i\epsilon}+\frac34e^{2i\epsilon}\). The two-orientation bound is at most \(|1-g|+\gamma/2\), using \(|1-g|\ge\gamma/2\). This proves the asserted uniform upper bound for all diagonal channels, and would in fact hold for arbitrary trace-preserving corrections supported on those complementary outcomes.

Ideal exactness and zero first derivative are preserved, since ideal physical inputs lie in the untouched ideal-flag protected subspace, and any corrected complementary amplitude vanishes at zero drift. All calls remain unconditional and forward, and the recovery is fixed independently of \(H,\epsilon\).

## 2. A legal physical oracle with zero field-basis diagonal

Under the sitewise Hadamard transformation used to define occupations, \(Z_0Z_1\) becomes \(X_0X_1\). It flips exactly two occupation bits, preserves total parity, and has no diagonal entry in either parity block. The intended inverse at \(H_{\rm edge}\) is
\(V=iB\), with \(B=Z_0Z_1\) in the physical basis and \(B=X_0X_1\) in occupation coordinates. The scalar phase is immaterial below.

This oracle's ideal program is the Bell state labelled by \(B\). It belongs to the physical protected program subspace because \(B\) is a balanced Majorana bilinear, \(B=i b_0a_1\) up to the chosen convention. For a shared-projector Pauli term \(P\), the syndrome is \(R=BP\) up to phase and its data matrix is proportional to \(BP\).

On a protected ideal-flag label, the only component aligned with \(V\) is \(P=I\), whose residual is removed by the aligned-term subtraction. Every remaining relative data operator is a nonidentity Pauli, hence has zero trace. The same statement holds for residuals in the uncorrected orthogonal flag.

On a corrected complementary syndrome,
\[
 A_{R,\alpha}R^\dagger(BP)
\]
is proportional to \(A_{R,\alpha}\). Relative to the desired inverse it is proportional to \(B^\dagger A_{R,\alpha}\). Since \(B\) has zero diagonal and \(A_{R,\alpha}\) is diagonal,
\[
 \operatorname{Tr}(B^\dagger A_{R,\alpha})=0
\]
for every syndrome and every channel Kraus outcome. Thus every Kraus operator in both normalized residual channels \(\mathcal N_{H_{\rm edge},s}\) is traceless. This remains true even when the residual channel is not a Pauli mixture.

## 3. Attainment of the diamond upper bound

A traceless error operator maps a maximally entangled input vector to a vector orthogonal to the original Bell vector. Take equal superposition of a maximally entangled input in each parity sector, with the two reference supports disjoint. The two residual outputs have total trace \(\gamma/2\) and are supported orthogonally to the two ideal Bell components. The remaining two-dimensional error matrix is
\[
 \begin{pmatrix}-\gamma/4&(g-1)/2\\
                 (\bar g-1)/2&-\gamma/4\end{pmatrix},
\]
whose trace norm is \(|1-g|\) because \(|1-g|\ge\gamma/2\). Orthogonality makes the norms add, giving \(|1-g|+\gamma/2\). This is the uniform upper bound from Section 1 and therefore the exact physical supremum. The construction supplies one physical maximizer for the entire class rather than an instance chosen after fixing the diagonal channel.

The proof needs the complementary syndrome to be read and the orthogonal flag to remain uncorrected. A coherent transformation mixing different syndromes or flag subspaces can escape these assumptions. The [complement-depolarizing recovery](THEORY_ODD_CYCLE_COMPLEMENT_DEPOLARIZATION.md) leaves this diagonal-channel class and gives a strict, dimension-suppressed improvement of the exact full physical minimax error. Its proof uses a constant program-complement probability for every physical oracle and data input. More informative non-diagonal recovery remains a route to larger gains while retaining improved field-Pauli performance. The identity, field-Pauli and edge-Pauli test families can then serve as explicit necessary constraints.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) provide the physical inversion setting. This result combines its legal edge coupling with the repository's [selective recovery identity](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md) and [program-span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md).

## Verification

The code builds both parity orientations at finite drift with a non-diagonal Pauli oracle and admissible two-qubit Bell projector ranks. It tests fixed, uniform and syndrome-dependent maximum-likelihood diagonal Pauli corrections, arbitrary diagonal phases, and a nonunitary diagonal channel. Each Kraus set is checked for completeness and for exact attainment of the claimed reference-assisted norm. These are finite matrix checks of the general trace obstruction. The analytic proof gives the result for every allowed odd ring length.

~~~python
from fractions import Fraction
from itertools import product
from math import comb

import numpy as np


for n in (21, 23, 83):
    f = 1-Fraction(2*comb(2*n, n), 4**n)
    print(n, "class minimax quadratic coefficient", f"{float(6+24*(1-f)):.12f}")

single = (
    np.eye(2), np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
d = 4
edge = paulis[1]
assert np.all(np.diag(edge) == 0) and np.array_equal(edge, edge.T)
diagonal = [p for p in paulis if np.array_equal(p, np.diag(np.diag(p)))]
bells = [p.reshape(-1)/np.sqrt(d) for p in paulis]
protected = {i for i, p in enumerate(paulis) if np.array_equal(p, p.T)}
tolerance = 4e-11
rng = np.random.default_rng(20261119)


def correction_operators(strategy, label, coefficients):
    if strategy == "fixed":
        return (np.eye(d),)
    if strategy == "uniform":
        return tuple(p/np.sqrt(d) for p in diagonal)
    if strategy == "likelihood":
        scores = []
        for field in diagonal:
            overlaps = [abs(np.trace(p.conj().T@field@paulis[label]))/d for p in paulis]
            scores.append(coefficients[int(np.argmax(overlaps))]**2)
        chosen = [p for p, score in zip(diagonal, scores) if score == max(scores)]
        return tuple(p/np.sqrt(len(chosen)) for p in chosen)
    if strategy == "phases":
        return (np.diag(np.exp(1j*rng.normal(size=d))),)
    if strategy == "diagonal_channel":
        return tuple(np.diag(np.eye(d)[i]) for i in range(d))
    raise ValueError(strategy)


for rank in (12, 13, 15):
    f, p = rank/16, 12/rank
    frame = np.column_stack(bells[:rank])
    q = frame@frame.conj().T
    coefficients = [
        sum(int(round(float(np.trace(a@b@a@b).real/d))) for b in paulis[:rank])
        for a in paulis
    ]
    for strategy in ("fixed", "uniform", "likelihood", "phases", "diagonal_channel"):
        for eps in (0.013, 0.17, 0.41, 1.2):
            a = np.exp(-6j*eps)
            b = np.exp(2j*eps)-a
            gamma = 3*(1-f)*np.sin(4*eps)**2
            g = (np.exp(-6j*eps)+3*np.exp(2j*eps))/4
            kraus = []
            for mirrored in (False, True):
                aa, bb = (a.conjugate(), b.conjugate()) if mirrored else (a, b)
                chosen, other = (slice(d, 2*d), slice(0, d)) if mirrored else (
                    slice(0, d), slice(d, 2*d)
                )
                for flag, amplitude in enumerate((
                    aa*np.eye(d*d)+p*bb*q,
                    np.sqrt(p*(1-p))*bb*q,
                )):
                    joint = (np.kron(edge, edge)@amplitude).reshape(d, d, d, d)
                    for label, syndrome in enumerate(paulis):
                        block = np.einsum(
                            "er,aeir->ai", syndrome.conj()/np.sqrt(d), joint
                        )/np.sqrt(d)
                        corrected = flag == 0 and label not in protected
                        operators = correction_operators(
                            strategy, label, coefficients
                        ) if corrected else (np.eye(d),)
                        for operator in operators:
                            matrix = np.zeros((2*d, 2*d), complex)
                            matrix[chosen, chosen] = (
                                operator@syndrome.conj().T@block if corrected else block
                            )
                            if flag == 0:
                                component = np.vdot(bells[label], edge.reshape(-1)/np.sqrt(d))
                                # On corrected outcomes component is exactly zero.
                                matrix[other, other] = component*edge
                            kraus.append(matrix/np.sqrt(2))

            np.testing.assert_allclose(
                sum(k.conj().T@k for k in kraus), np.eye(2*d), atol=tolerance
            )
            state = np.eye(2*d)/np.sqrt(2*d)
            target = (np.kron(np.eye(2), edge)@state).reshape(-1)
            output = sum(
                np.outer((k@state).reshape(-1), (k@state).reshape(-1).conj())
                for k in kraus
            )
            observed = np.abs(np.linalg.eigvalsh(output-np.outer(target, target.conj()))).sum()
            assert abs(observed-(abs(1-g)+gamma/2)) < tolerance
        print("Edge-oracle Kraus certificate:", rank, strategy)
~~~
