# A quadratic error floor for fixed recovery of the six-query encoder

The [balanced six-query recovery](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md) improves the long-ring quadratic diamond coefficient. Can a different fixed decoder eliminate the quadratic term while retaining its encoder? We answer this for the independent Gaussian-sector promise, allowing coherent preparation of the encoder flag and arbitrary recovery on all registers accessible to the circuit.

**Proposition.** Let \(n\ge21\) be odd and \(f=1-2\binom{2n}{n}/4^n\), \(p=3/(4f)\). Fix the plus-program encoder that coherently chooses the split and all-preferred encodings with amplitudes \(\sqrt p,\sqrt{1-p}\), as in the [six-query construction](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md). Let a fixed trace-preserving recovery implement exact ideal entrywise conjugation for every oracle in the independent \(\mathrm{Spin}(2n)\times\mathrm{Spin}(2n)\) promise. Then already at the ideal identity oracle its common parity-drift error obeys
\[
 \left\|\Phi_\epsilon-\mathrm{id}\right\|_\diamond
 \ \ge\ \frac{9(1-f)}{2f}\sin^2(4\epsilon).
\]
Consequently its leading quadratic coefficient is at least \(72(1-f)/f>0\). No fixed recovery for this encoder can achieve \(o(\epsilon^2)\) uniformly on this group promise. At \(n=21\) the lower coefficient is \(23.335365368545\ldots\); the original inverse decoder gives \(23.498048879555\ldots\).

For the balanced encoder with a classical fair choice of plus and minus program orientation, even allowing recovery conditioned on the orientation, the analogous lower coefficient is at least \(36(1-f)/f\). At \(n=21\) this is \(11.667682684273\ldots\), compared with the attained coefficient \(11.874512219889\ldots\). The balanced coefficient is therefore within a factor of \(1.018\) of the best possible for this classical encoder on the group promise at that size.

For the physical fully fielded Ising promise, the same fixed plus-program encoder has a strictly positive quadratic floor
\[
 B_n=\frac{72}{r^2}
 \left[\frac12\sum_{k=0}^n\binom nk a_k^2-r^2\right],\qquad
 r=fD^2,\quad
 a_k=\sum_{\substack{\ell<n\\\ell\ {\rm odd}}}
       \sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}.
\]
Out-of-range binomial coefficients in the inner sum are zero. In fact its finite-drift diamond error is at least
\( (B_n/16)\sin^2(4\epsilon)\).
At \(n=21\), \(B_{21}=0.100884111690\ldots>0\). The [physical program-span refinement](THEORY_ODD_CYCLE_PHYSICAL_PROGRAM_SPAN.md) strengthens this coefficient to \(2.249999602402\ldots\) using independently rotated physical root tori. The classical balanced encoder has at least half this coefficient. Thus changing only the fixed recovery cannot yield cubic suppression for these encoders on the physical promise either.

The recovery can keep both the program and its purifying register, the coherent split flag, and all ideal scratch registers. The statement fixes the encoder and the group promise. A general physical Ising decoder and a new encoder require further analysis.

## 1. Exactness on the ideal orbit fixes recovery on its linear span

Use the canonical fixed inverse encoder only as a change of coordinates on the queried registers before an arbitrary proposed recovery. It outputs logical data, a program register \(E\), its purifying register \(R\), a split flag and fixed scratch at zero drift. In these coordinates the ideal states are
\[
 |\psi\rangle_{\rm data}\otimes|v_g\rangle_{ER}\otimes|\eta\rangle_F,\qquad
 |v_g\rangle=\operatorname{vec}(\bar U_+(g_+))/\sqrt D,\quad
 |\eta\rangle=\sqrt p\,|\mathrm{split}\rangle+\sqrt{1-p}\,|\mathrm{preferred}\rangle ,
\]
where \(D=2^{n-1}\). The vector \(\psi\) is arbitrary, since the intended data unitary is invertible for every fixed oracle. The physical pre-inverse-encoder states for these vectors are all contained in the full joint encoded image. Ideal exactness of the proposed recovery forces its data output to be the pure state \(|\psi\rangle\langle\psi|\).

The half-spin representation of \(\mathrm{Spin}(2n)\) on the plus sector is irreducible. Schur orthogonality shows that its matrix coefficients are linearly independent, so the vectors \(\operatorname{vec}(\bar U_+(g_+))\) span all \(D^2\) dimensions of \(E\otimes R\). For completeness, if a matrix were orthogonal to every \(U_+(g_+)\), multiply the resulting zero matrix coefficient function by the conjugate of each irreducible entry and integrate Haar measure. Each coefficient of that matrix vanishes.

Take a Stinespring isometry \(T\) of the proposed recovery. Purity and linearity give
\[
 T(|\psi\rangle\otimes|v_g\rangle\otimes|\eta\rangle)
    =|\psi\rangle\otimes|w_g\rangle
\]
with an environment vector independent of \(\psi\). This follows by testing coherent superpositions of data basis inputs. Since the program vectors span the whole program space, there is a linear isometry \(F\) on \(E\otimes R\) such that
\[
 T|_{\mathcal H_{\rm data}\otimes(E\otimes R)\otimes|\eta\rangle}
  =I_{\rm data}\otimes F .
\]
Well-definedness follows by applying any linear dependence among the \(v_g\) to one fixed nonzero data vector, and isometry follows from that of \(T\). The image of this subspace is the full data space tensored with \(\operatorname{ran}F\). Its orthogonal complement is the full data space tensored with an orthogonal environment subspace. Isometry forces all other input subspaces into that complement. After tracing the recovery environment, cross terms between the two subspaces vanish. Thus the recovery leaves the data channel of the \(|\eta\rangle\) component fixed, while its complementary components add positive outputs.

## 2. Unavoidable population outside a Bell test state

Evaluate the oracle at \(U=I\), with drift \(e^{-i\epsilon P}\), and take a maximally entangled plus-data input with an external reference. The program is another Bell state on \(E,R\). In canonical decoded coordinates the split part applies
\[
 aI+bQ,\qquad a=e^{-6i\epsilon},\quad b=e^{2i\epsilon}-e^{-6i\epsilon},
\]
to plus data and \(E\); the all-preferred part applies \(aI\). The component along the ideal flag \(\eta\) is therefore
\[
 M_{00}=aI+p b Q .
\]
The remainder is orthogonal to \(\eta\). The shared Bell projector satisfies \(Q^2=Q\), both normalized single-register partial traces equal \(fI\), and hence on the product of the two Bell states
\[
 \|Q|\Phi_{\rm data}\rangle|\Phi_{\rm prog}\rangle\|^2=f .
\]
Projecting the data and its external reference back onto their original Bell state reduces \(Q\) to \(\operatorname{Tr}_{\rm data}Q/D=fI_E\). Thus the squared norm of the part outside that data Bell state, still in the ideal flag, is exactly
\[
 |p b|^2(f-f^2).
\]
Section 1 fixes the reduced data output of this component. The complementary flag component can only add a positive contribution to this same population. The data–reference entanglement infidelity of any exact recovery is at least \(|p b|^2f(1-f)\). A two-outcome measurement of the target Bell projector lower-bounds trace distance without a factor of one half by twice the infidelity. Since \(|b|^2=4\sin^2(4\epsilon)\), this gives the stated finite-drift diamond lower bound.

For the classical balanced encoder, exactness of the averaged ideal output forces exactness of both conditional recoveries, since a convex combination of density matrices can equal a pure state only if each term equals it. Use the same plus-data Bell test. With probability one half the plus-program encoder is used and has the unavoidable population above. The other conditional output is positive and cannot remove that population. This gives half of the preceding finite-drift bound, and therefore the balanced quadratic lower coefficient.

## 3. A physical floor from the field torus alone

The field-only physical oracles, with all edge couplings zero, already constrain recovery on a useful subspace. In the field-parity basis the distinct sign weights give linearly independent phase functions, so the ideal vectors \(v_H\) span the diagonal program space
\(\mathcal D=\operatorname{span}\{|j,j\rangle_{ER}:1\le j\le D\}\).
The argument in Section 1 then fixes the recovery on the full data space tensored with \(\mathcal D\) and the ideal flag. Other components map into an orthogonal environment space. This conclusion follows from exactness on the field torus, which is part of the physical promise.

Use the logical Pauli expansion from the [exact noise calculation](THEORY_ODD_CYCLE_SIX_QUERY_DIAMOND.md#bell-projectors-and-the-reduced-channel),
\[
 Q=D^{-2}\sum_P a_P P\otimes\bar P .
\]
On the product of the data and program Bell states, each term is an orthogonal pair of Pauli Bell states. Projecting the program onto \(\mathcal D\) keeps just the diagonal logical Paulis \(Z\). Projecting the data away from its target Bell state removes only the identity term. The unavoidable squared norm is consequently
\[
 |p b|^2D^{-4}\sum_{Z\ne I}a_Z^2 .
\]
The same two-outcome measurement gives a finite-drift distance at least twice this quantity.

Diagonal logical Paulis are products of the physical \(X_i\) modulo total parity. A subset of \(k\) sites anticommutes with precisely the Majoranas on those sites, and its commutation character against \(T_I=\Gamma_I C\) is \((-1)^{k+|I\cap\{\text{Majoranas on the chosen sites}\}|}\). Its Pauli expansion coefficient is therefore \((-1)^k a_k\) with \(a_k\) as stated above. The site subset and its complement give the same logical operator. This yields
\(\sum_{Z\ne I}a_Z^2=\frac12\sum_k\binom nk a_k^2-r^2\), proving \(B_n\).

This sum is positive for every odd \(n\ge3\). In particular \(a_1=\binom{2n-2}{n-1}/n>0\), and the single-site diagonal Paulis are nonidentity on the parity space. To derive the value, the coefficients in \((1-x)^2(1+x)^{2n-2}\) are symmetric about degree \(n\); their total over odd degrees is zero. The central coefficient at odd degree \(n\) is \(-2\binom{2n-2}{n-1}/n\). Half of the remaining odd coefficients, at degrees less than \(n\), sum to its negative half, which is \(a_1\).

## Scope and next step

The group floor uses the full ideal-program space, while the physical floor uses its diagonal subspace. Physical Ising matrices are symmetric, so their program vectors can lie in a larger symmetric matrix subspace. Quantifying the additional part of the shared-projector error forced inside the full physical ideal-program span is the next test for strengthening the numerical floor. The strict positive bound above already rules out cubic suppression by changing only the fixed recovery for these encoders.

For the independent Gaussian promise the remaining optimization is quantitative: the lower bound leaves a small interval between the best possible recovery for the balanced classical encoder and its known inverse decoder at \(n=21\). A recovery acting on the orthogonal flag component can only change the positive contribution left outside the fixed ideal-orbit subspace. This identifies the remaining degrees of freedom directly.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) provide the structured inversion setting. [Odake, Yoshida and Murao](https://arxiv.org/abs/2405.07625) study differentiated transformation bounds with group promises. The ideal-orbit argument here constrains recovery by linearity and purity of its exact outputs, and uses the Bell-projector marginal to measure an unavoidable second-order data error.

## Verification

The exact arithmetic check compares the decoder lower bounds with the attained coefficients. The finite matrix check builds logical two-qubit Bell projectors and evaluates the unavoidable population of the ideal flag component for several admissible rank fractions. It also checks the ideal-program span for the full logical Pauli representation, which illustrates the linear-span step. The all-length span statement uses Schur orthogonality above.

~~~python
from fractions import Fraction
from itertools import combinations, product
from math import comb

import numpy as np


for n in (21, 23, 83):
    f = 1-Fraction(2*comb(2*n, n), 4**n)
    lam = 48*(1-f)
    old = 2*lam if lam >= 6 else 72/(12-lam)
    floor = 72*(1-f)/f
    balanced_floor = floor/2
    balanced = 6+lam/2
    assert floor <= old and balanced_floor <= balanced
    if n == 21:
        assert balanced/balanced_floor < Fraction(1018, 1000)
    print(n, *(f"{float(x):.12f}" for x in (floor, old, balanced_floor, balanced)))

def physical_floor(n):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    values = []
    for k in range(n+1):
        value = sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-(2*n-2*k)), min(2*k, ell)+1)
        )
        values.append(value)
    assert values[0] == r and values[-1] == -r
    assert values[1] == comb(2*n-2, n-1)//n > 0
    weighted = sum(comb(n, k)*a*a for k, a in enumerate(values))
    assert weighted % 2 == 0
    nonidentity = weighted//2-r*r
    assert nonidentity > 0
    return Fraction(72*nonidentity, r*r)


for n in (21, 23, 83):
    print("Physical quadratic floor", n, f"{float(physical_floor(n)):.12f}")

single = (
    np.eye(2),
    np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]),
    np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
D = 4
bell_vectors = np.column_stack([p.reshape(-1)/np.sqrt(D) for p in paulis])
np.testing.assert_allclose(bell_vectors.conj().T@bell_vectors, np.eye(D*D), atol=1e-12)
assert np.linalg.matrix_rank(bell_vectors) == D*D

# Tensor ordering is data, external reference, program, program purifier.
initial = np.einsum("ij,kl->ijkl", np.eye(D), np.eye(D))/D
def verify_physical_paulis(n):
    size = 2**n
    plus = [i for i in range(size) if i.bit_count() % 2 == 0]
    d = len(plus)
    gammas = []
    for site in range(n):
        for local in (single[1], -single[2]):
            matrix = np.ones((1, 1))
            for j in range(n):
                matrix = np.kron(
                    matrix, single[3] if j < site else local if j == site else single[0]
                )
            gammas.append(matrix)
    c = np.eye(size, dtype=complex)
    for g in gammas[1::2]:
        c = c@g
    diagonal_counts = np.zeros((d, d), dtype=np.int64)
    for degree in range(1, n, 2):
        for labels in combinations(range(2*n), degree):
            matrix = c.copy()
            for j in reversed(labels):
                matrix = gammas[j]@matrix
            entries = matrix[np.ix_(plus, plus)]
            diagonal_counts += np.rint(np.abs(entries)**2).astype(np.int64)
    r = d*d-comb(2*n, n)//2
    squared = 0
    for mask in range(2**n):
        signs = np.array([(-1)**((i & mask).bit_count()) for i in plus])
        numerator = int(signs@diagonal_counts@signs)
        assert numerator % d == 0
        observed = numerator//d
        k = mask.bit_count()
        expected = (-1)**k*sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-(2*n-2*k)), min(2*k, ell)+1)
        )
        assert observed == expected
        squared += observed**2
    assert Fraction(72*(squared//2-r*r), r*r) == physical_floor(n)
    print("Physical diagonal coefficients verified from Majoranas at n =", n)


for n in (3, 5):
    verify_physical_paulis(n)

for rank in (12, 13, 15):
    f = rank/(D*D)
    p = 3/(4*f)
    assert p <= 1
    q = bell_vectors[:, :rank]@bell_vectors[:, :rank].conj().T
    q_tensor = q.reshape(D, D, D, D)
    projected = np.einsum("acbd,bjdl->ajcl", q_tensor, initial)
    np.testing.assert_allclose(np.vdot(projected, projected), f, atol=1e-12)
    for eps in (0.001, 0.013, 0.17, 0.41):
        a = np.exp(-6j*eps)
        b = np.exp(2j*eps)-a
        ideal_flag = a*initial+p*b*projected
        data_overlap = np.einsum("aacl->cl", ideal_flag)/np.sqrt(D)
        total = float(np.vdot(ideal_flag, ideal_flag).real)
        target_population = float(np.vdot(data_overlap, data_overlap).real)
        outside = total-target_population
        expected = abs(p*b)**2*f*(1-f)
        assert abs(outside-expected) < 2e-12
    print("Ideal-flag leakage identity verified at Bell projector rank", rank)
~~~
