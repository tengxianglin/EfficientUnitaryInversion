# Exact worst case of physical program-syndrome recovery

The [program-syndrome recovery](THEORY_ODD_CYCLE_PROGRAM_SYNDROME_RECOVERY.md) lowers the six-query error at the identity ideal oracle. We now determine its worst case over the entire physical Ising family.

**Theorem.** For the classical parity-balanced syndrome recovery at any odd \(n\ge21\), put
\[
 g(\epsilon)=\tfrac14e^{-6i\epsilon}+\tfrac34e^{2i\epsilon}.
\]
The exact worst-case diamond error, without a factor of one half, is
\[
 \sup_H\|\Phi^{\rm syndrome}_{H,\epsilon}
              -\operatorname{Ad}_{e^{iH}}\|_\diamond
 =|1-g(\epsilon)|+\frac38\sin^2(4\epsilon).
\]
The physical field Hamiltonian \(H=(\pi/2)X_0\) attains the supremum for every real \(\epsilon\). In particular the worst-case quadratic coefficient is exactly 12, independently of ring length.

The [old balanced inverse decoder](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md) has the uniformly attained error
\[
 |1-g(\epsilon)|+\frac32(1-f_n)\sin^2(4\epsilon),
 \qquad f_n=1-\frac{2\binom{2n}{n}}{4^n}>\frac34 .
\]
Thus the new recovery has strictly larger worst-case error whenever \(\sin(4\epsilon)\ne0\), at every admitted finite ring length. Its identity-oracle improvement remains valid. The difference of the worst-case errors is exactly
\(\frac32(f_n-\frac34)\sin^2(4\epsilon)\).
This resolves the proposed uniform-improvement test for this recovery.

## 1. Residual Kraus decomposition at an arbitrary physical oracle

Consider the plus-program orientation, including a coherent split/preferred flag with \(p=3/(4f)\). Write \(V\) for the intended inverse on the data and \(v=\operatorname{vec}(\bar U_+)/\sqrt D\) for its ideal program. In the Pauli Bell basis let \(v_R=\langle R|v\rangle\). The physical program-span theorem gives \(v_R=0\) outside the fixed protected subspace \(\mathcal S\).

After the canonical inverse encoding, let \(L_R\) be the data Kraus matrix obtained by applying the joint ideal unitary to the shared projector \(Q\), with initial Bell program, and projecting the program onto Bell label \(R\). We take the plus input block in this calculation. The isometric shared-projector construction gives
\[
 \sum_R L_R^\dagger L_R=fI,\qquad
 \sum_R\bar v_R L_R=fV .
\]
The first identity uses \(Q^2=Q\) and \(\operatorname{Tr}_E Q/D=fI\). The second contracts the program with its ideal vector, reducing again to the normalized partial trace of \(Q\). The two ideal joint unitaries factor and \(Q\) commutes with their plus joint action.

On the ideal-flag branch, the recovery leaves \(L_R\) alone for \(R\in\mathcal S\), and multiplies it on the left by its inverse label Pauli for \(R\notin\mathcal S\). Call the result \(L'_R\). These unitary corrections preserve \(\sum_R L_R^\dagger L_R\), and they preserve the second identity because \(v_R=0\) on every corrected label. Put
\[
 E_R=L'_R-fv_RV.
\]
Then
\[
 \sum_R\bar v_RE_R=0,\qquad
 \sum_R E_R^\dagger E_R=f(1-f)I.
\]
Consequently the ideal-flag Kraus matrices are
\[
 a v_RV+pbL'_R=g v_RV+pbE_R,
 \qquad a=e^{-6i\epsilon},\quad b=e^{2i\epsilon}-a,
\]
since \(a+pbf=g\). The cross terms vanish after summing \(R\). On the orthogonal-flag branch every label is corrected; its Kraus matrices have the form \(\sqrt{p(1-p)}\,bL''_R\), where the corrections are unitary and \(\sum_R(L''_R)^\dagger L''_R=fI\).

After removing the intended inverse, the full plus-data channel therefore has a decomposition
\[
 |g|^2\,\mathrm{id}+w\,\mathcal N_{H,+},\qquad
 w=|b|^2[p^2 f(1-f)+p(1-p)f]
   =\frac3{16}|b|^2=\frac34\sin^2(4\epsilon),
\]
for some trace-preserving completely positive channel \(\mathcal N_{H,+}\) independent of \(\epsilon\). The operator corrections define that channel even where the displayed weight vanishes, by the normalized residual Kraus matrices. The minus data is unchanged in this orientation. Its cross-parity coherence is multiplied by \(g\): residual Kraus matrices have zero contraction with \(v\), and the orthogonal flag has no minus-data amplitude. The mirror has the same cross-parity factor and a channel \(\mathcal N_{H,-}\) in the minus block.

## 2. Uniform diamond upper bound

After the fair parity choice, each diagonal block has error \((w/2)(\mathcal N_{H,s}-\mathrm{id})\), and the off-diagonal block is multiplied by \(g\). For a pure input with a reference, let its plus and minus parts have squared norms \(t,1-t\). The difference output is a positive residual-channel output with trace \(w/2\), plus a two-dimensional operator
\[
 \begin{pmatrix}
 -\frac w2 t&(g-1)\sqrt{t(1-t)}\\
 (\bar g-1)\sqrt{t(1-t)}&-\frac w2(1-t)
 \end{pmatrix}.
\]
Set \(c=|1-g|\). We have \(c\ge w/2\): writing \(x=\cos(2\epsilon)\),
\[
 1-\operatorname{Re}g-w/2
 =1-x^3-\tfrac32x^2(1-x^2)
 =\tfrac12(x-1)^2(3x^2+4x+2)\ge0 .
\]
The two-dimensional trace norm is at most \(c\), with maximum at \(t=1/2\). The total output trace norm is at most \(c+w/2\). This holds for every reference input, every physical \(H\), and every real drift, giving the uniform diamond upper bound. It uses only positivity and normalization of the residual channels.

## 3. A physical Pauli field attains the bound

Take \(H=(\pi/2)X_0\). Its intended inverse restricted to either parity sector is \(iX_0\), a scalar phase times a nonidentity, traceless diagonal logical Pauli \(Z_0\). The ideal program is the Bell vector labelled by \(Z_0\), which belongs to \(\mathcal S\).

The shared projector has expansion \(Q=D^{-2}\sum_P a_PP\otimes\bar P\). For this ideal program, the term \(P\) has Bell syndrome \(R=Z_0P\) up to phase and data matrix proportional to \(Z_0P\). On the ideal-flag protected labels, the only term aligned with the ideal data unitary is \(P=I\), at \(R=Z_0\), and its residual \(E_R\) vanishes by subtraction of \(fv_RV\). Every other protected term, after removing the intended data unitary, is the nonidentity Pauli \(P\).

On every corrected label, applying the inverse label Pauli to the data matrix gives a scalar identity. Relative to the desired data unitary, this is the nonidentity Pauli \(Z_0\). This applies also to all orthogonal-flag labels. Thus both residual channels \(\mathcal N_{H,\pm}\) are mixtures of nonidentity Pauli conjugations only.

Use equal superposition of a maximally entangled plus data/reference state and a maximally entangled minus data/reference state, with disjoint reference supports. Each residual-channel output is then orthogonal to both ideal Bell components. The positive residual output and the two-dimensional operator in Section 2 have orthogonal support, so their trace norms add. At \(t=1/2\) the result is \(c+w/2\), attaining the upper bound.

Expanding \(w/2=6\epsilon^2+O(\epsilon^4)\) and \(c=6\epsilon^2+O(\epsilon^4)\) gives coefficient 12. The earlier seeded three-site experiments saw increased Choi infidelity at some nonzero fields; the present theorem supplies a deterministic all-length counterexample at every valid cancellation length.

## 4. Partial mixing cannot improve the worst case

Suppose the whole syndrome recovery is used with fixed probability \(q\in[0,1]\), and the old balanced inverse decoder is used otherwise. Convexity of the diamond norm bounds its worst-case error by the corresponding mixture of the two proved norms. The same Pauli field attains both bounds with nonidentity Pauli residuals, and their noise outputs are orthogonal to the same two ideal Bell states. The upper bound is therefore attained:
\[
 \sup_H{\cal E}^{(q)}_{H}(\epsilon)
 =|1-g|+\frac12\left[(1-q)\,3(1-f_n)+q\,\frac34\right]\sin^2(4\epsilon).
\]
For \(f_n>3/4\) and \(\sin(4\epsilon)\ne0\), the unique minimum within this family is \(q=0\). The leading worst-case coefficient is
\[
 (1-q)[6+24(1-f_n)]+12q .
\]
Thus uniform partial mixing cannot turn the identity-oracle gain into a worst-case gain.

## Consequence for the project

The decoder remains exact on ideal physical inputs and retains first-order cancellation. For worst-case performance, however, the old balanced inverse decoder has the smaller proved error. The program-complement syndrome rule should therefore be retained as a scoped identity-oracle improvement and an explicit counterexample to choosing recovery solely by performance at \(H=0\).

A next recovery search must change the rule across individual syndromes or use a different coherent action. The identity and Pauli fields give compulsory constraints, and the uniform mixture in Section 4 already has its exact optimum at the old decoder. Its objective must be the worst-case coefficient over physical \(H\), including syndrome-label mismatch. A different encoder remains another possible improvement. The physical pentagon query minimum and all-encoder quadratic optimum remain open.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) provide the systematic-error context. The proof here uses the [physical ideal-program span](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) and the [explicit syndrome recovery](THEORY_ODD_CYCLE_PROGRAM_SYNDROME_RECOVERY.md).

## Verification

The arithmetic check compares exact leading coefficients and the finite-drift scalar inequality. The independent Kraus construction below uses two logical qubits, with Bell projector ranks 12,13,15 giving admissible encoder mixtures. It explicitly applies both orientations and syndrome corrections with a nonidentity diagonal Pauli ideal oracle. It checks completeness, the residual nonidentity Pauli property through reference outputs, and attainment of the analytic norm at finite drift. These finite checks support the all-length analytic proof.

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
for n in (21, 23, 83):
    f = 1-Fraction(2*comb(2*n, n), 4**n)
    old = 6+24*(1-f)
    assert old < 12
    print(n, "old balanced coefficient", f"{float(old):.12f}",
          "syndrome worst-case coefficient", 12)

single = (
    np.eye(2), np.array([[0, 1], [1, 0]]),
    np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]),
)
paulis = [np.kron(a, b) for a, b in product(single, repeat=2)]
d = 4
v = paulis[3]
assert np.trace(v) == 0 and np.array_equal(v, v.T)
bells = [p.reshape(-1)/np.sqrt(d) for p in paulis]
protected = {i for i, p in enumerate(paulis) if np.array_equal(p, p.T)}
tolerance = 3e-11

for rank in (12, 13, 15):
    f = rank/16
    p = 3/(4*f)
    bell_frame = np.column_stack(bells[:rank])
    q = bell_frame@bell_frame.conj().T
    for eps in (0.001, 0.013, 0.17, 0.41, 1.2):
        a = np.exp(-6j*eps)
        b = np.exp(2j*eps)-a
        w = 3/4*np.sin(4*eps)**2
        g = (np.exp(-6j*eps)+3*np.exp(2j*eps))/4
        kraus = []
        for mirrored in (False, True):
            aa, bb = (a.conjugate(), b.conjugate()) if mirrored else (a, b)
            selected, other = (slice(d, 2*d), slice(0, d)) if mirrored else (
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
                        program_component = np.vdot(bells[label], v.reshape(-1)/np.sqrt(d))
                        matrix[other, other] = program_component*v
                    if flag == 1 or label not in protected:
                        block = operator.conj().T@block
                    matrix[selected, selected] = block
                    kraus.append(matrix/np.sqrt(2))

        np.testing.assert_allclose(
            sum(k.conj().T@k for k in kraus), np.eye(2*d), atol=tolerance
        )
        ideal = np.zeros((2*d, 2*d), complex)
        ideal[:d, :d] = v
        ideal[d:, d:] = v
        input_matrix = np.eye(2*d)/np.sqrt(2*d)
        target = (ideal@input_matrix).reshape(-1)
        output = sum(
            np.outer((k@input_matrix).reshape(-1), (k@input_matrix).reshape(-1).conj())
            for k in kraus
        )
        change = output-np.outer(target, target.conj())
        measured = float(np.abs(np.linalg.eigvalsh(change)).sum())
        assert abs(measured-(abs(1-g)+w/2)) < tolerance
        target_probability = float(np.vdot(target, output@target).real)
        assert abs((1-target_probability)-(w/4+(1-g.real)/2)) < tolerance
    print("Pauli-field worst-case Kraus certificate verified at Bell rank", rank)
~~~
