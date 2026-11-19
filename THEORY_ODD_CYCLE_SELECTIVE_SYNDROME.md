# Selective program correction gives pointwise improvement without a worst-case penalty

The [full program-syndrome decoder](THEORY_ODD_CYCLE_SYNDROME_WORST_CASE.md) improves the identity oracle but has a larger worst-case coefficient, 12, on every allowed long odd ring. The penalty comes from correcting the orthogonal split-flag branch. Keeping that branch unchanged yields a stronger comparison with the old balanced inverse decoder.

**Theorem.** For odd \(n\ge21\), use the coherent six-query encoder and correct a program Bell syndrome only if both (i) the split flag is in its ideal state \(\eta\), and (ii) the syndrome is outside the physical ideal-program span \(\mathcal S\). In the orthogonal flag branch, leave the data unchanged and discard the program. Choose plus and minus orientations with equal probabilities as before. This fixed decoder is exact on every ideal physical Ising oracle, suppresses linear common parity drift, and for every physical \(H,\epsilon\) satisfies
\[
 {\cal E}^{\rm selective}_{H}(\epsilon)
 \le |1-g(\epsilon)|+\frac32(1-f_n)\sin^2(4\epsilon)
 ={\cal E}^{\rm old}_{H}(\epsilon),
\]
where \(g=\frac14e^{-6i\epsilon}+\frac34e^{2i\epsilon}\) and \(f_n=1-2\binom{2n}{n}/4^n\). The right side is the exact error of the old balanced decoder, independent of \(H\). The Pauli field \(H=(\pi/2)X_0\) attains equality, so the worst-case error is the same as the old decoder.

At \(H=0\) the selective decoder has strictly smaller error whenever \(\sin(4\epsilon)\ne0\). Its quadratic coefficient at \(n=21\) is \(7.967452826832\ldots\), compared with the old \(11.874512219889\ldots\). Thus this decoder is pointwise no worse over the entire physical family and strictly better at some members, using the same six queries. Its minimax value is unchanged. Optimality among all recoveries or encoders remains open.

## 1. The recovery and its residual channels

Take the same fixed plus-program coherent encoder as in the [program-syndrome construction](THEORY_ODD_CYCLE_PROGRAM_SYNDROME_RECOVERY.md), with \(p=3/(4f)\). After canonical inverse encoding, measure the split flag in its known basis \(\eta,\eta^\perp\). On \(\eta\), preserve the physical program subspace \(\mathcal S\) coherently and read only its complement's Pauli Bell labels, applying the matching inverse label Pauli to plus data. On \(\eta^\perp\), discard the program without applying any syndrome correction. These are trace-preserving known operations. Ideal inputs always have flag \(\eta\) and program in \(\mathcal S\), so they are undisturbed. The mirror exchanges plus and minus roles.

For the plus block write \(V\) for its ideal inverse and \(v_R\) for the Bell coefficients of its ideal program. As in the [worst-case calculation](THEORY_ODD_CYCLE_SYNDROME_WORST_CASE.md#1-residual-kraus-decomposition-at-an-arbitrary-physical-oracle), the shared-projector amplitudes \(L_R\) obey
\[
 \sum_RL_R^\dagger L_R=fI,\qquad
 \sum_R\bar v_RL_R=fV .
\]
The corrected \(L'_R\) on the ideal flag obey the same two identities, because \(v_R=0\) on every corrected label and the corrections are unitary. Define
\[
 E'_R=L'_R-fv_RV,\qquad E_R=L_R-fv_RV .
\]
Both families have zero contraction with \(v\) and squared norm sum \(f(1-f)I\).

With \(a=e^{-6i\epsilon}\), \(b=e^{2i\epsilon}-a\), the two flag branches have Kraus matrices
\[
 K_{0,R}=g v_RV+pbE'_R,\qquad
 K_{1,R}=\sqrt{p(1-p)}\,b(fv_RV+E_R).
\]
The cross terms vanish when summed over program labels. Thus after removing the intended inverse the plus data channel is
\[
 (|g|^2+p(1-p)|b|^2f^2)\,\mathrm{id}
   +p^2|b|^2\mathcal F'_H+p(1-p)|b|^2\mathcal F_H,
\]
where both \(\mathcal F'_H,\mathcal F_H\) are completely positive with constant trace factor \(f(1-f)\). It follows that this is
\[
 (1-\gamma)\,\mathrm{id}+\gamma\,\mathcal N_{H,+},\qquad
 \gamma=p|b|^2f(1-f)=3(1-f)\sin^2(4\epsilon),
\]
for a trace-preserving completely positive residual channel \(\mathcal N_{H,+}\). The mirror gives an analogous channel \(\mathcal N_{H,-}\). The cross-parity factor remains \(g\) in both orientations.

The identity weight \(p(1-p)|b|^2f^2\) in this decomposition is precisely the part lost by the earlier full correction of the orthogonal flag branch. Keeping that branch unchanged supplies the old noise weight \(\gamma\) at every physical oracle, while allowing the residual channel to improve.

## 2. Exact minimax value and pointwise comparison

The balanced channel has diagonal errors \(\frac\gamma2(\mathcal N_{H,s}-\mathrm{id})\) and coherence multiplier \(g\). For a reference-assisted pure input with parity weight \(t\), the error splits into a positive residual output of trace \(\gamma/2\) and a two-dimensional operator. Its norm is at most
\[
 \frac\gamma2+
 \sqrt{\frac{\gamma^2}{4}(2t-1)^2+4|1-g|^2t(1-t)}
 \le\frac\gamma2+|1-g|.
\]
The final inequality uses \(|1-g|\ge\gamma/2\), established in the [balanced norm proof](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md#diamond-norm-maximization). The old decoder attains this value at every physical \(H\), since its residual noise is a mixture of nonidentity logical Paulis. Hence the upper bound proves pointwise non-increase of the diamond norm, a stronger statement than retaining the same worst-case coefficient.

At \(H=(\pi/2)X_0\), let \(Z_0\) be the nonidentity diagonal Pauli representing \(X_0\) in each parity block. The ideal program label is \(Z_0\). On ideal-flag protected labels, subtracting \(fv_RV\) removes the \(P=I\) component, leaving only nonidentity relative Paulis. On ideal-flag corrected labels the relative error becomes \(Z_0\), also nonidentity. On the uncorrected orthogonal flag, subtracting the aligned identity component leaves only nonidentity relative Paulis. Thus both residual channels contain only nonidentity Pauli noise. Equal superposition of two maximally entangled parity inputs attains the upper bound. This proves the exact minimax value.

## 3. Identity-oracle improvement

At \(H=0\) the only nonidentity noise in the ideal flag has labels in the physical protected span; all its complementary labels are corrected. The untouched orthogonal flag contributes its original nonidentity Pauli weight. With \(D=2^{n-1}\), \(r=fD^2\) and \(S_{\rm phys}\) from the [span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md#5-consequence-for-exact-fixed-recovery), the total plus noise probability is
\[
 \gamma_I
 =|b|^2\left[p^2\frac{S_{\rm phys}}{D^4}
             +p(1-p)f(1-f)\right]
 =\gamma-p^2|b|^2
       \left[f(1-f)-\frac{S_{\rm phys}}{D^4}\right].
\]
The balanced identity-oracle error is exactly \(|1-g|+\gamma_I/2\), by the Pauli Bell maximizing input. Its quadratic coefficient is
\[
 C_n^{\rm selective}(I)
 =6+24(1-f_n)
   -\frac{18}{r^2}\big[r(D^2-r)-S_{\rm phys}\big].
\]
The subtracted quantity is strictly positive. For example the nonidentity monomial with four \(a\)-Majoranas lies outside the balanced program span and has nonzero squared coefficient \(a_2^2\). The binomial coefficient formula gives
\(a_2=-\binom{2n}{n}\binom n2/[2\binom{2n}4]\ne0\).
This identity follows by the central coefficient of \((1-x)^4(1+x)^{2n-4}\) and symmetry of its odd coefficients. Thus at every finite allowed odd ring size the identity improvement is strict away from the zeros of \(\sin(4\epsilon)\).

## Next step and evidence scope

The recovery settles the decoder-class question posed by the previous counterexample: preserving the uncorrected flag branch gives a uniform pointwise improvement while the Pauli field fixes the minimax value. A further minimax improvement must also reduce that field's residual error, possibly through syndrome-dependent operations that preserve the aligned component across several ideal program vectors. Uniformly mixing this selective decoder with the old one leaves the same minimax value because both have the same Pauli-field maximizer.

The [seeded finite verifier](verify_ising_program_recovery.py) now has a selective mode. At three sites it uses a valid coherent probability \(p=0.6\), so the model is an analogue with nonzero linear drift. The ten tested nonzero physical Hamiltonians retain exact ideal output and the original derivative, while their Choi infidelities decrease relative to the original decoder. The all-length diamond comparison comes from the analytic decomposition above, not these finite samples.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) give the structured inversion and noise setting. The [physical program-span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) supplies the protected subspace needed for the recovery.

## Verification

Run the physical three-site comparison with:
~~~bash
OPENBLAS_NUM_THREADS=2 python verify_ising_program_recovery.py --selective
~~~
The default verifier still reproduces the earlier full-correction counterexamples. The checks below verify exact long-ring arithmetic and build the two-orientation selective Kraus maps at identity, Pauli, and noncommuting symmetric unitary examples. The latter use two logical qubits and Bell ranks 12,13,15 with admissible mixtures. They test the dimension-independent residual-channel and norm calculation.

~~~python
from fractions import Fraction
from itertools import product
from math import comb

import numpy as np
from scipy.linalg import expm


for n in (21, 23, 83):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    a = [
        sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-2*n+2*k), min(2*k, ell)+1)
        )
        for k in range(n+1)
    ]
    S = sum(comb(n, k)**2*a[k]**2 for k in range(n+1))//2-r*r
    assert a[2] == -Fraction(comb(2*n, n)*comb(n, 2), 2*comb(2*n, 4))
    old = 6+24*Fraction(D*D-r, D*D)
    new = old-Fraction(18*(r*(D*D-r)-S), r*r)
    assert 6 < new < old
    print(n, "old coefficient", f"{float(old):.12f}",
          "selective identity coefficient", f"{float(new):.12f}")

single = (
    np.eye(2), np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
d = 4
bells = [p.reshape(-1)/np.sqrt(d) for p in paulis]
protected = {i for i, p in enumerate(paulis) if np.array_equal(p, p.T)}
rng = np.random.default_rng(20261119)
real = rng.normal(size=(d, d))
examples = (
    ("identity", np.eye(d)),
    ("Pauli", paulis[3]),
    ("symmetric", expm(0.3j*(real+real.T))),
)
tolerance = 4e-11
for rank in (12, 13, 15):
    f, p = rank/16, 12/rank
    frame = np.column_stack(bells[:rank])
    q = frame@frame.conj().T
    coefficients = [
        sum(int(round(float(np.trace(a@b@a@b).real/d))) for b in paulis[:rank])
        for a in paulis
    ]
    S = sum(a*a for i, a in enumerate(coefficients) if i in protected and i != 0)
    for name, v in examples:
        for eps in (0.013, 0.17, 0.41):
            a = np.exp(-6j*eps)
            b = np.exp(2j*eps)-a
            g = (np.exp(-6j*eps)+3*np.exp(2j*eps))/4
            gamma = 3*(1-f)*np.sin(4*eps)**2
            old_bound = abs(1-g)+gamma/2
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
                    joint = (np.kron(v, v)@amplitude).reshape(d, d, d, d)
                    for label, operator in enumerate(paulis):
                        matrix = np.zeros((2*d, 2*d), complex)
                        block = np.einsum(
                            "er,aeir->ai", operator.conj()/np.sqrt(d), joint
                        )/np.sqrt(d)
                        if flag == 0:
                            component = np.vdot(bells[label], v.reshape(-1)/np.sqrt(d))
                            matrix[other, other] = component*v
                        if flag == 0 and label not in protected:
                            block = operator.conj().T@block
                        matrix[chosen, chosen] = block
                        kraus.append(matrix/np.sqrt(2))
            np.testing.assert_allclose(
                sum(k.conj().T@k for k in kraus), np.eye(2*d), atol=tolerance
            )
            ideal = np.kron(np.eye(2), v)
            inputs = [np.eye(2*d)/np.sqrt(2*d)]
            for _ in range(2):
                state = rng.normal(size=(2*d, 2*d))+1j*rng.normal(size=(2*d, 2*d))
                inputs.append(state/np.linalg.norm(state))
            for state in inputs:
                target = (ideal@state).reshape(-1)
                output = sum(
                    np.outer((k@state).reshape(-1), (k@state).reshape(-1).conj())
                    for k in kraus
                )
                difference = output-np.outer(target, target.conj())
                measured = float(np.abs(np.linalg.eigvalsh(difference)).sum())
                assert measured <= old_bound+tolerance
                if state is inputs[0]:
                    if name == "Pauli":
                        assert abs(measured-old_bound) < tolerance
                    if name == "identity":
                        gamma_I = abs(b)**2*(p*p*S/d**4+p*(1-p)*f*(1-f))
                        assert abs(measured-(abs(1-g)+gamma_I/2)) < tolerance
    print("Selective two-orientation Kraus and norm checks passed at Bell rank", rank)
~~~
