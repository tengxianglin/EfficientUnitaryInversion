# A diagonal Pauli twirl improves every field-Pauli oracle

The [selective syndrome recovery](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md) is pointwise no worse than the old balanced decoder, but its minimax error is still attained by a nonidentity Pauli field. We modify only its correction on the ideal-flag program complement, and determine the best fixed diagonal randomization on the complete field-Pauli test family.

Let \(n\ge21\) be odd, \(D=2^{n-1}\), \(r=fD^2\), and \(p=3/(4f)\), with \(f=1-2\binom{2n}{n}/4^n\). Define
\[
 S=\frac12\sum_{k=0}^n\binom nk^2 a_k^2-r^2,\qquad
 M=r(D^2-r)-S>0,\qquad
 a_k=\sum_{\substack{\ell<n\\\ell\ {\rm odd}}}
       \sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}.
\]
The \(D\) logical diagonal Paulis, denoted \(\mathcal Z\), are products of the physical fields \(X_j\), modulo the total parity. Every \(T\in\mathcal Z\) is realized up to phase by a physical Hamiltonian \(H_T=(\pi/2)\sum_{j\in A}X_j\).

**Construction.** On the ideal split-flag outcome \(\eta\) and a program Bell syndrome \(R\) outside the physical ideal-program space \(\mathcal S\), choose \(Z\in\mathcal Z\) with a fixed probability distribution \(\mu\), independent of \(R,H\) and the input. Apply \(ZR^\dagger\) to data in the selected parity. Preserve the ideal program subspace coherently, and keep the orthogonal flag branch uncorrected. Choose the two parity orientations fairly. This is the selective decoder with an additional known random diagonal Pauli; it still uses six unconditional forward queries.

For every physical Hamiltonian and every drift, the modified decoder is pointwise no worse than the old balanced inverse decoder. On the field-Pauli oracle \(T\), its exact diamond error is
\[
 {\cal E}_{T,\mu}(\epsilon)
 =|1-g(\epsilon)|+\frac32(1-f)\sin^2(4\epsilon)
  -\frac{9\mu(T)M}{8r^2}\sin^2(4\epsilon),
 \quad g=\tfrac14e^{-6i\epsilon}+\tfrac34e^{2i\epsilon}.
\]
Uniform \(\mu(T)=1/D\) therefore strictly improves all \(D\) field-Pauli oracles whenever \(\sin(4\epsilon)\ne0\). It has the best worst-case value on that test family among all such fixed diagonal distributions. Its quadratic coefficient on every member is
\[
 6+24(1-f)-\frac{18M}{r^2D}.
\]
At \(n=21\), the coefficient decreases from \(11.874512219889\ldots\) to \(11.874508493827\ldots\). The guaranteed test-family gain is \(3.7260622\times10^{-6}\). Its exponential \(1/D\) factor limits this fixed-distribution approach.

These are exact field-Pauli errors and a uniform pointwise upper bound on the full physical family. The full-family worst-case coefficient for this modified decoder remains open. Improving the old maximizers alone does not prove a smaller supremum.

## 1. Uniform pointwise safety of the random correction

The [selective decoder proof](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md#1-the-recovery-and-its-residual-channels) uses only the following facts about corrected ideal-flag labels: the corrections are trace preserving, are unitary within each classical branch, and are applied where the ideal program coefficient \(v_R\) vanishes. Randomizing over \(Z\) retains all these properties. Kraus refinement by \(Z\) therefore preserves the residual identities and the sector decomposition
\[
 (1-\gamma)\mathrm{id}+\gamma\mathcal N_{H,s},
 \qquad \gamma=3(1-f)\sin^2(4\epsilon),
\]
with \(\mathcal N_{H,s}\) trace preserving and completely positive. The cross-parity factor is still \(g\). The balanced reference-assisted norm bound is at most \(|1-g|+\gamma/2\). This equals the old decoder's exact norm at every physical oracle, proving pointwise non-increase, exact ideal inversion and first-order drift suppression.

## 2. The complementary syndrome weight is constant over field Paulis

At a field-Pauli oracle \(T\), the shared-projector term labelled by a logical Pauli \(P\) has program syndrome \(R=TP\) up to phase. Its ideal-flag squared coefficient is \(p^2|b|^2a_P^2/D^4\), where \(|b|^2=4\sin^2(4\epsilon)\). The squared coefficient \(a_P^2\) depends only on the even Majorana grade of \(P\). Let
\[
 M_T=\sum_{P:\,TP\notin\mathcal S}a_P^2.
\]
We claim \(M_T=M\) for every diagonal \(T\), including identity.

A diagonal \(T\) contains both Majoranas at each selected site. Multiplication by it toggles both occupations of a Majorana monomial at those sites. On a site containing exactly one Majorana, this swaps \(a\) and \(b\); on the empty or double sites, it interchanges empty and double. Only the single sites contribute to the difference between the number of \(a\)'s and \(b\)'s. Thus the condition \(TP\in\mathcal S\) is the same as balance after swapping only the single sites selected by \(T\). That swap preserves the total grade of \(P\) and commutes with full complementation, so it is a bijection of logical Pauli labels preserving \(a_P^2\). The weighted protected sum is consequently independent of \(T\), equal to the full balanced sum at \(T=I\). The full Pauli sum is \(rD^2\), and the balanced sum is \(r^2+S\). Hence
\(M_T=rD^2-r^2-S=M\).

In particular \(M>0\) because an unbalanced grade-four monomial has nonzero coefficient \(a_2\), as established in the [selective correction note](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md#3-identity-oracle-improvement).

## 3. Exact field-Pauli error and optimal fixed distribution

For \(R=TP\notin\mathcal S\), the data before correction is proportional to \(TP\). Correcting with \(ZR^\dagger\) leaves data proportional to \(Z\); relative to the intended inverse \(T\), the residual error is \(T^\dagger Z\). It is identity precisely when \(Z=T\). The corrected ideal-flag complementary syndromes therefore contribute identity weight \(p^2|b|^2\mu(T)M/D^4\), reducing the nonidentity noise probability by this amount. Protected residuals and the uncorrected orthogonal flag contain only nonidentity Paulis, since the aligned component was already removed in the selective decomposition.

The reduced residual noise remains a Pauli mixture, and the total plus-sector nonidentity probability is
\[
 \gamma_T=\gamma-\frac{9\mu(T)M}{4r^2}\sin^2(4\epsilon).
\]
The same value holds in the mirrored minus orientation. Since \(\gamma_T\le\gamma\) and \(|1-g|\ge\gamma/2\), the exact balanced norm is \(|1-g|+\gamma_T/2\), attained by the equal two-sector Bell input. This proves the formula.

The only dependence on the fixed random distribution is through \(\mu(T)\), with a common strictly positive multiplier on the test family. The maximum field-Pauli error is minimized by maximizing \(\min_T\mu(T)\). Since \(\sum_T\mu(T)=1\), its maximum is \(1/D\), achieved uniquely by the uniform distribution. Thus syndrome-independent guessing within the diagonal Pauli class has exactly the \(1/D\) limitation stated above.

## Implication and next step

The Pauli-field counterexample is not an invariant of all pointwise-safe recovery rules: this decoder reduces its error while preserving the safety proof for the entire physical family. However, fixed syndrome-independent diagonal guessing has a small guaranteed gain. The [syndrome-conditioned optimization](THEORY_ODD_CYCLE_CONDITIONAL_SYNDROME.md) is now solved analytically using the explicit integer likelihoods \(a_{TR}^2\). A maximum-likelihood rule attains the same optimal gain on all field-Pauli hypotheses and removes the exponential fixed-distribution limitation. At \(n=21\) its quadratic gain is \(0.148358524720\ldots\). Testing non-Pauli physical oracles remains necessary to determine its full-family minimax value. The full physical pentagon query minimum and all-encoder quadratic optimum remain open.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) provide the structured inversion setting. This decoder uses the [exact physical program span](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) and the [selective residual-channel identity](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md).

## Exact and finite verification

The script enumerates Majorana Pauli labels modulo complementation at \(n=3,5,7\), checks the constant complementary weight for every field Pauli, and evaluates exact long-ring arithmetic. The smaller lengths verify the combinatorics; the first-order-canceling six-query mixture is asserted only for \(n\ge21\). A separate finite Kraus calculation uses logical two-qubit Bell projectors with admissible rank fractions and checks every diagonal Pauli oracle under the random correction. Those projectors verify the dimension-independent channel formula; the all-length physical syndrome weight is established above.

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


def verify_fields(n):
    full = (1 << (2*n))-1
    a = coefficients(n)
    labels = [mask for mask in range(1 << (2*n-1)) if mask.bit_count() % 2 == 0]

    def canonical(mask):
        return min(mask, full ^ mask)

    def protected(mask):
        na = sum((mask >> (2*j)) & 1 for j in range(n))
        nb = sum((mask >> (2*j+1)) & 1 for j in range(n))
        return na == nb

    squared = {mask: a[mask.bit_count()//2]**2 for mask in labels}
    expected = sum(value for mask, value in squared.items() if not protected(mask))
    D = 2**(n-1)
    assert len(labels) == D*D
    for chosen in range(1 << (n-1)):
        field = sum(3 << (2*j) for j in range(n-1) if (chosen >> j) & 1)
        actual = sum(
            value for mask, value in squared.items()
            if not protected(canonical(mask ^ field))
        )
        assert actual == expected > 0
    print(n, "field-Pauli labels checked", D, "constant weight", expected)


for n in (3, 5, 7):
    verify_fields(n)
for n in (21, 23, 83):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    a = coefficients(n)
    S = sum(comb(n, k)**2*a[k]**2 for k in range(n+1))//2-r*r
    M = r*(D*D-r)-S
    gain = Fraction(18*M, r*r*D)
    old = 6+24*Fraction(D*D-r, D*D)
    assert M > 0 and 0 < gain < old
    print(n, "all-field quadratic gain", f"{float(gain):.12g}",
          "all-field coefficient", f"{float(old-gain):.12f}")

# Finite Kraus verification of the uniform diagonal twirl.
from itertools import product

import numpy as np

single = (
    np.eye(2), np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
d = 4
diagonal = [p for p in paulis if np.count_nonzero(p-np.diag(np.diag(p))) == 0]
assert len(diagonal) == d
bells = [p.reshape(-1)/np.sqrt(d) for p in paulis]
protected = {i for i, p in enumerate(paulis) if np.array_equal(p, p.T)}
tolerance = 4e-11
for rank in (12, 13, 15):
    f, p = rank/16, 12/rank
    frame = np.column_stack(bells[:rank])
    q = frame@frame.conj().T
    a_pauli = [
        sum(int(round(float(np.trace(a@b@a@b).real/d))) for b in paulis[:rank])
        for a in paulis
    ]
    for field in diagonal:
        complementary_weight = 0
        for pauli, coefficient in zip(paulis, a_pauli):
            overlaps = [abs(np.trace(r.conj().T@pauli.conj()@field))/d for r in paulis]
            syndrome = int(np.argmax(overlaps))
            assert abs(overlaps[syndrome]-1) < tolerance
            if syndrome not in protected:
                complementary_weight += coefficient**2
        for eps in (0.013, 0.17, 0.41):
            a = np.exp(-6j*eps)
            b = np.exp(2j*eps)-a
            g = (np.exp(-6j*eps)+3*np.exp(2j*eps))/4
            gamma = 3*(1-f)*np.sin(4*eps)**2
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
                    joint = (np.kron(field, field)@amplitude).reshape(d, d, d, d)
                    for label, operator in enumerate(paulis):
                        block = np.einsum(
                            "er,aeir->ai", operator.conj()/np.sqrt(d), joint
                        )/np.sqrt(d)
                        correction = flag == 0 and label not in protected
                        for z in (diagonal if correction else (np.eye(d),)):
                            matrix = np.zeros((2*d, 2*d), complex)
                            matrix[chosen, chosen] = (
                                z@operator.conj().T@block if correction else block
                            )
                            if flag == 0:
                                component = np.vdot(
                                    bells[label], field.reshape(-1)/np.sqrt(d)
                                )
                                matrix[other, other] = component*field
                            kraus.append(matrix/np.sqrt(2*(d if correction else 1)))
            np.testing.assert_allclose(
                sum(k.conj().T@k for k in kraus), np.eye(2*d), atol=tolerance
            )
            state = np.eye(2*d)/np.sqrt(2*d)
            target = (np.kron(np.eye(2), field)@state).reshape(-1)
            output = sum(
                np.outer((k@state).reshape(-1), (k@state).reshape(-1).conj())
                for k in kraus
            )
            norm = np.abs(np.linalg.eigvalsh(output-np.outer(target, target.conj()))).sum()
            expected = abs(1-g)+gamma/2-p*p*abs(b)**2*complementary_weight/(2*d**5)
            assert abs(norm-expected) < tolerance
    print("Uniform-twirl Kraus certificate passed at Bell rank", rank)
~~~
