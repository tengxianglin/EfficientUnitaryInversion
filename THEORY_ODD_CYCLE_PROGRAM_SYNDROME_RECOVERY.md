# Recovery on the physical program complement

The [physical program-span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) identifies exactly the ideal programs of a fixed parity block: they lie in the span \(\mathcal S\) of Pauli Bell states labelled by balanced Majorana monomials. This allows a recovery to read additional syndromes without disturbing any ideal physical oracle. We give such a fixed recovery for the coherent six-query encoder.

**Result.** For odd \(n\ge21\), the recovery below preserves exact ideal inversion and uniform \(O(\epsilon^2)\) common parity-drift error on the full physical Ising promise. At the identity ideal Hamiltonian, its classical parity-balanced version has exact diamond error
\[
 {\cal E}_{I}^{\rm new}(\epsilon)
 =1-\cos^3(2\epsilon)
   +\frac{9S_{\rm phys}}{8r^2}\sin^2(4\epsilon),
\]
where \(r=fD^2\), \(D=2^{n-1}\), and
\[
 f=1-\frac{2\binom{2n}{n}}{4^n},\qquad
 S_{\rm phys}=\frac12\sum_{k=0}^n\binom nk^2 a_k^2-r^2,\qquad
 a_k=\sum_{\substack{\ell<n\\\ell\ {\rm odd}}}
          \sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}.
\]
The identity-oracle quadratic coefficient is \(6+18S_{\rm phys}/r^2=6+B_n^{\rm phys}/4\). At \(n=21\) it is \(7.926781949080\ldots\), compared with \(11.874512219889\ldots\) for the [prior balanced decoder](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md).

This is a proved improvement at \(H=0\). For other \(H\) the added correction depends on the actual syndrome amplitudes. The [exact worst-case theorem](THEORY_ODD_CYCLE_SYNDROME_WORST_CASE.md) now shows that the full-family quadratic coefficient is 12, attained by \(H=(\pi/2)X_0\), exceeding that of the old balanced inverse decoder. Uniform partial mixing with the old decoder also has its minimum at the old decoder. Every run still uses six unconditional forward queries. The recovery includes a Bell syndrome measurement on the decoded program and its purifier, and keeps the split-choice flag coherent until that recovery.

## 1. Fixed recovery

Use the plus-program orientation first. Apply the canonical inverse encoding after the oracle layer, as a fixed change of coordinates. Let \(F\) be the split/preferred flag and
\[
 |\eta\rangle=\sqrt p\,|\mathrm{split}\rangle+\sqrt{1-p}\,|\mathrm{preferred}\rangle,
 \qquad p=\frac3{4f}.
\]
The coherent encoder prepares this flag with a retained purification, so the recovery may use it. Write \(P_{\mathcal S}\) for the projector onto the balanced-Majorana program Bell states in \(E\otimes R\). The logical Pauli label convention and this projector are fixed and independent of \(H,\epsilon\).

The recovery measures the flag in the basis \(\eta,\eta^\perp\).
- On outcome \(\eta\), it first measures the two-outcome projection \(P_{\mathcal S},I-P_{\mathcal S}\). For the first outcome it leaves data unchanged and discards the program. For the second outcome it measures the program in its Pauli Bell basis and applies the inverse of its label Pauli to plus data.
- On outcome \(\eta^\perp\), it measures the entire program in the Pauli Bell basis and applies the inverse label Pauli to plus data.
The Pauli correction is controlled on data parity and is identity on minus data. All syndrome and flag outcomes are discarded. The mirror orientation exchanges the parity roles. Choose the two orientations with equal input-independent probabilities.

For every ideal physical \(U\), the program is \(\operatorname{vec}(\bar U_+)/\sqrt D\in\mathcal S\), and the flag is \(\eta\). The recovery therefore acts as identity on data and preserves all coherences in the ideal program subspace. Exact inversion follows.

After removing the ideal target, the component outside this subspace or outside the ideal flag has amplitude \(O(\epsilon)\), uniformly, because it vanishes at zero drift and the slot charge is bounded. A recovery can change its positive output contribution only at \(O(\epsilon^2)\). Cross terms between the syndrome subspaces disappear under the original program and flag trace as well as the measured recovery. Inside the ideal flag and program subspace the data action is unchanged. The original first derivative was zero, so this recovery also has zero first derivative. Uniformity follows from bounded finite slot charges and compactness of the Gaussian closure.

## 2. Exact channel at the identity oracle

For this section let \(H=0\). The shared Bell projector has Pauli expansion
\[
 Q=D^{-2}\sum_Pa_PP\otimes\bar P,\qquad a_I=r.
\]
On plus data the joint flag-\(\eta\) amplitude is \(aI+p b Q\), with \(a=e^{-6i\epsilon}\), \(b=e^{2i\epsilon}-e^{-6i\epsilon}\). The flag-\(\eta^\perp\) amplitude is \(\sqrt{p(1-p)}\,bQ\). On minus data only the ideal flag is present, with identity action. With the program initialized in its Bell state, the amplitude labelled by program Pauli \(P\) in the first branch is
\[
 \delta_{P,I}a I+p b\,a_P P/D^2
\]
on plus data, and \(\delta_{P,I}I\) on minus data. In the second branch it is \(\sqrt{p(1-p)}\,b a_PP/D^2\) on plus data and zero on minus data. Consistent Pauli Bell labels may absorb harmless transpose signs; the matching inverse correction removes the data Pauli in each corrected branch.

Thus every nonidentity syndrome is corrected except the \(P\in\mathcal S\), \(P\ne I\) terms in the ideal flag. Their total uncorrected probability is
\[
 \gamma_{\rm new}
 =p^2|b|^2S_{\rm phys}/D^4
 =\frac{9S_{\rm phys}}{4r^2}\sin^2(4\epsilon).
\]
The resulting plus block is identity plus \(\gamma_{\rm new}(\mathcal N_{\mathcal S}-\mathrm{id})\), where \(\mathcal N_{\mathcal S}\) is the normalized nonidentity Pauli mixture restricted to those labels. On cross-parity coherence only the identity-program, ideal-flag branch contributes, and its amplitude is
\[
 a+pbf=\tfrac14e^{-6i\epsilon}+\tfrac34e^{2i\epsilon}=g .
\]
The classical parity-balanced channel therefore has nonidentity probability \(\gamma_{\rm new}/2\) in each sector and coherence multiplier \(g\). In the mirrored branch the selected minus block has amplitude \(\bar g\), so its action on a plus-to-minus coherence is again \(g\).

Since \(S_{\rm phys}\le f(1-f)D^4\), we have
\(\gamma_{\rm new}\le p\,\gamma_{\rm old}\le\gamma_{\rm old}\), where \(\gamma_{\rm old}=3(1-f)\sin^2(4\epsilon)\). The prior [balanced norm argument](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md#diamond-norm-maximization) then applies with \(|1-g|\ge1-\operatorname{Re}g\ge\gamma_{\rm new}/2\). Its upper bound is attained by equal superposition of plus and minus maximally entangled inputs, as the uncorrected nonidentity Paulis give orthogonal Bell errors. This proves the displayed exact identity-oracle formula.

At the identity oracle the leading uncorrectable within-plus Bell-infidelity contribution is \(B_n^{\rm phys}/2\) for this decoder, precisely the population used in the [physical fixed-encoder floor](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md#5-consequence-for-exact-fixed-recovery). The full balanced norm also includes the remaining parity coherence error of coefficient six. We make no optimality claim for the full norm of this recovery.

## 3. What remains to optimize

At a general physical \(U\), a syndrome outside \(\mathcal S\) comes from \(P\bar U_+\), so its Bell label need not equal the Pauli \(P\) acting on data. Correcting that label can change the data error in a way that depends on \(U\). The pointwise ideal correctness and linear cancellation proved above remain valid; the exact identity-oracle improvement does not supply a uniform quantitative improvement by itself.

The [seeded three-site check](verify_ising_program_recovery.py) uses the valid coherent mixture \(p=0.6\) at that size. Its ten nonzero-H samples preserve ideal exactness and the original linear derivative, but their Choi entanglement infidelity at \(\epsilon=0.001\) increases by factors from \(1.0508\) to \(1.2306\). This small-system analogue has a nonzero linear drift and is not the \(n\ge21\) cancellation protocol. It demonstrates that correction on the program complement can worsen a nonzero-H observable. The [all-length worst-case proof](THEORY_ODD_CYCLE_SYNDROME_WORST_CASE.md) resolves the larger-length test analytically and supplies an explicit Pauli-field maximizer. A proof of a uniform improvement would require controlling the syndrome-label mismatch, possibly using the singular-frame invariance of the physical program space. **Correction to the earlier balanced finite-drift formula.** Directly forming both orientation Kraus maps gives the same cross-parity factor \(g\) in each orientation. The earlier expression \(1-\operatorname{Re}g\) must be replaced by \(|1-g|\) in the old balanced exact diamond error as well. The mirror has selected-minus amplitude \(\bar g\), whose conjugate acts on the plus-to-minus coherence. Its imaginary part is retained by the average. This correction preserves the earlier quadratic coefficients.

The known all-encoder query bounds and the pentagon six-versus-seven gap are unaffected by this fixed-encoder recovery construction.

The [EUI preprint and Appendix B](https://arxiv.org/html/2506.20570v1) supply the physical inversion and noise context. This recovery uses the program space established by the repository's [all-length theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md), and turns its orthogonal complement into measurable error syndromes.

## Verification

The first check evaluates the exact all-length formulas. The finite matrix check uses two-qubit Pauli Bell projectors with admissible rank fractions, retains a coherent split flag and explicitly constructs the recovered channel's Kraus operators at the identity. It compares their action on maximally entangled test inputs against the claimed formula. The protected program labels in this test are a chosen Bell subspace containing identity; the all-length physical choice is established analytically above.

~~~python
from fractions import Fraction
from itertools import product
from math import comb

import numpy as np


for n in (21, 23, 83):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    coeffs = [
        sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-2*n+2*k), min(2*k, ell)+1)
        )
        for k in range(n+1)
    ]
    S = sum(comb(n, k)**2*value**2 for k, value in enumerate(coeffs))//2-r*r
    new = 6+Fraction(18*S, r*r)
    old = 6+24*Fraction(D*D-r, D*D)
    assert new < old
    print(n, "identity-oracle coefficient", f"{float(new):.12f}",
          "old uniform coefficient", f"{float(old):.12f}")

single = (
    np.eye(2), np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
d = 4
protected = {i for i, p in enumerate(paulis) if np.array_equal(p, p.T)}
assert 0 in protected and len(protected) == 10

for rank in (12, 13, 15):
    f = rank/16
    p = 3/(4*f)
    coeffs = [
        sum(int(round(float(np.trace(a@b@a@b).real/d))) for b in paulis[:rank])
        for a in paulis
    ]
    S = sum(a*a for i, a in enumerate(coeffs) if i in protected and i != 0)
    for eps in (0.001, 0.013, 0.17, 0.41):
        a, b = np.exp(-6j*eps), np.exp(2j*eps)-np.exp(-6j*eps)
        orientations = []
        for flipped in (False, True):
            if flipped:
                a, b = a.conjugate(), b.conjugate()
            selected, other = (slice(d, 2*d), slice(0, d)) if flipped else (
                slice(0, d), slice(d, 2*d)
            )
            kraus = []
            for flag in (0, 1):
                for label, operator in enumerate(paulis):
                    matrix = np.zeros((2*d, 2*d), complex)
                    if flag == 0:
                        block = p*b*coeffs[label]/(d*d)*operator
                        if label == 0:
                            block += a*np.eye(d)
                            matrix[other, other] = np.eye(d)
                        if label not in protected:
                            block = operator.conj().T@block
                    else:
                        block = np.sqrt(p*(1-p))*b*coeffs[label]/(d*d)*np.eye(d)
                    matrix[selected, selected] = block
                    kraus.append(matrix/np.sqrt(2))
            orientations.extend(kraus)
        np.testing.assert_allclose(
            sum(k.conj().T@k for k in orientations), np.eye(2*d), atol=2e-12
        )

        refdim = 2*d
        state = np.zeros((2*d, refdim), complex)
        for i in range(d):
            state[i, i] = state[d+i, d+i] = 1/np.sqrt(2*d)
        vector = state.reshape(-1)
        output = sum(
            np.outer((k@state).reshape(-1), (k@state).reshape(-1).conj())
            for k in orientations
        )
        difference = output-np.outer(vector, vector.conj())
        measured = np.abs(np.linalg.eigvalsh(difference)).sum()
        gamma = p*p*abs(b)**2*S/(d**4)
        g = (np.exp(-6j*eps)+3*np.exp(2j*eps))/4
        expected = abs(1-g)+gamma/2
        assert abs(measured-expected) < 3e-11
    print("Recovered identity channel verified at Bell projector rank", rank)
~~~
