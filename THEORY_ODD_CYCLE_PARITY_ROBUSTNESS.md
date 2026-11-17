# Quadratic response to parity-breaking oracle errors

This note concerns the [three-query odd-cycle protocol](THEORY_ODD_CYCLE_THREE_QUERIES.md) with ideal encoding and decoding. It bounds the error relative to inversion of the intended Hamiltonian. The noisy evolution itself is generally outside the exact-inversion promise.

## Error model and result

Let $U=e^{-iH}$ be an ideal oracle from the fully fielded odd Ising cycle. Write $P=\prod_j X_j$ for the physical parity. In slot $i$ the actual oracle is $V_i=e^{-i(H+\Delta_i)}$ with $\Delta_i=\Delta_i^\dagger$ and $P\Delta_iP=-\Delta_i$. The errors can differ across slots and need not commute with $H$. Set $\epsilon_i=\|\Delta_i\|$ in operator norm, absorbing the evolution time into the Hamiltonians. Let $W$ denote the encoding isometry, so $U^{\otimes3}W=WU^\dagger$. Checking that both auxiliary registers return to zero after decoding gives the successful Kraus operator $K=W^\dagger(V_1\otimes V_2\otimes V_3)W$.

Set
$$
\eta=\frac12\sum_{i=1}^3\epsilon_i^2+\epsilon_1\epsilon_2\epsilon_3,
\qquad \delta=\sum_{i=1}^3\epsilon_i .
$$
Then $\|K-U^\dagger\|\leq\eta$ and the success probability on any input is at least $1-\delta^2$. The success map differs from the ideal inverse channel by at most $2\eta$ in diamond norm. For any data and reference input with success probability $p>0$, the conditioned output has trace distance at most $\eta/\sqrt p$ from the ideal inverse output, using the convention $D(\rho,\sigma)=\|\rho-\sigma\|_1/2$. Even with no success check, decoding and tracing out the auxiliaries gives diamond error at most $2\eta+\delta^2$. The constants are uniform in $H$, system size and input, including coherent superpositions of the two parity sectors.

## Proof

Split each slot into its parity-even and parity-odd parts $E_i=(V_i+PV_iP)/2$ and $O_i=(V_i-PV_iP)/2$. Duhamel's formula gives $\|V_i-U\|\leq\epsilon_i$, hence $\|O_i\|\leq\epsilon_i$. Applying the second-order Taylor remainder to $F_i(a)=e^{-i(H+a\Delta_i)}$ on the real interval $[-1,1]$ gives
$$
\|E_i-U\|=\bigl\|\tfrac12(F_i(1)+F_i(-1))-F_i(0)\bigr\|\leq \tfrac12\epsilon_i^2 .
$$
Indeed each of the two ordered second-derivative insertions is a product of unitaries with two factors of $\Delta_i$. Their integration over the unit-time simplex gives $\|F_i''(a)\|\leq\epsilon_i^2$ for real $a$. The signs follow from $[H,P]=0$.

The range of $W$ is contained in the direct sum of the three-register parity sectors $(+,+,+)$ and $(-,-,-)$. Every term with exactly one or two odd factors maps this subspace to an orthogonal parity sector, so
$$
K=W^\dagger(E_1\otimes E_2\otimes E_3+O_1\otimes O_2\otimes O_3)W .
$$
Each $E_i$ is a contraction. Telescoping the even product against $U^{\otimes3}$ and bounding the odd product proves the bound $\eta$. For the rejection probability, the leakage operator is $L=(I-WW^\dagger)(V_1\otimes V_2\otimes V_3)W$. The ideal product has zero leakage, and telescoping gives $\|L\|\leq\delta$. The decoded successful and leaked parts have orthogonal auxiliary labels. Tracing out those labels gives the successful map plus a CP map for the leakage with diamond norm at most $\|L\|^2$. The success-map bound follows by expanding $K(\cdot)K^\dagger-U^\dagger(\cdot)U$ as two left-right multiplications and using $\|K\|\leq1$. For a purified input, the component of $K|\psi\rangle$ perpendicular to $U^\dagger|\psi\rangle$ has norm at most $\eta$. After dividing by $\sqrt p$ this is the pure-state trace distance. Tracing out the purifying system gives the stated bound for mixed inputs as well.

## A tight quadratic example

Use $H=0$ and perturb only the data-labelled first slot, with $\Delta_1=\epsilon B$ and $B=(Z_0+Z_1)/2$. Put $F=Z_0Z_1$. Since $B^2=(I+F)/2$ and $B$ has spectrum in $\{-1,0,1\}$, the even part of that slot is $I+(\cos\epsilon-1)(I+F)/2$.

Using the Majorana isometry and orthogonality of the second and third register factors, the compression of $F$ applied in the first register is $(2n)^{-1}\sum_j T_j^\dagger F T_j=-(1-2/n)F$. Here $F$ is a real Majorana bilinear, exactly two Majoranas anticommute with it, and charge conjugation negates it. Thus
$$
K=I+\tfrac{\cos\epsilon-1}{2}\bigl[I-(1-2/n)F\bigr].
$$
For any pure input with $\langle F\rangle=0$, the accepted output has trace distance $(1-2/n)\epsilon^2/4+O(\epsilon^4)$ from the ideal output. Thus the uniform exponent two cannot be improved under this error model even with the clean-return check.

## Evidence and scope

The script below uses the repository's gate generator and dense small-system matrix exponentials. Its nonzero-$H$ example has independent parity-odd perturbations in the three slots. The separate tightness check evaluates the closed form above. These are finite checks. The operator-norm and diamond-norm claims follow from the proof.

~~~python
from functools import reduce

import numpy as np
from scipy.linalg import expm

from odd_cycle_encoder import apply_gate, encoder_gates

n = 3
d = 1 << n
rng = np.random.default_rng(194)
eye = np.eye(d)
i2 = np.eye(2)
x = np.array([[0, 1], [1, 0]])
z = np.diag([1, -1])
gates = list(encoder_gates(n))
w = np.zeros((d**3, d), complex)

for column in range(d):
    state = {column: 1}
    for gate in gates:
        state = apply_gate(state, gate)
    for row, amplitude in state.items():
        w[row, column] = amplitude


def word(sites, p):
    return reduce(np.kron, (p if j in sites else i2 for j in reversed(range(n))))


def tensor_abc(a, b, c):
    # The encoder wire indices are little endian, so A is the last factor.
    return np.kron(c, np.kron(b, a))


p = word(set(range(n)), z)
h = sum(a * word({j}, z) for j, a in enumerate(rng.normal(size=n)))
h += sum(a * word({j, (j + 1) % n}, x) for j, a in enumerate(rng.normal(size=n)))
odd = []
for _ in range(3):
    m = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    m = (m + m.conj().T) / 2
    m = (m - p @ m @ p) / 2
    m /= np.linalg.norm(m, ord=2)
    np.testing.assert_allclose(p @ m @ p, -m, atol=1e-13)
    odd.append(m)
ideal = expm(1j * h)
np.testing.assert_allclose(
    w.conj().T @ tensor_abc(ideal.conj().T, ideal.conj().T, ideal.conj().T) @ w,
    ideal,
    atol=1e-12,
)
for epsilon in (0.04, 0.02, 0.01):
    k = w.conj().T @ tensor_abc(*(expm(-1j * (h + epsilon * v)) for v in odd)) @ w
    error = np.linalg.norm(k - ideal, ord=2)
    failure = 1 - np.linalg.svd(k, compute_uv=False)[-1] ** 2
    assert error <= 1.5 * epsilon**2 + epsilon**3 + 1e-12
    assert failure <= 9 * epsilon**2 + 1e-12
    print(f"eps={epsilon:.2f}  accepted operator error={error:.8e}  worst rejection={failure:.8e}")

zz = word({0, 1}, x)
b = (word({0}, x) + word({1}, x)) / 2
for epsilon in (0.04, 0.02, 0.01):
    k = w.conj().T @ tensor_abc(expm(-1j * epsilon * b), eye, eye) @ w
    exact = eye + (np.cos(epsilon) - 1) * (eye - (1 - 2 / n) * zz) / 2
    np.testing.assert_allclose(k, exact, atol=1e-12)
    v = k[:, 0]
    distance = np.linalg.norm(v[1:]) / np.linalg.norm(v)
    print(f"tight example eps={epsilon:.2f}  conditional distance/eps²={distance/epsilon**2:.8f}")
~~~

Parity-preserving model errors and faults in the known encoding gates are outside this theorem. The absence of linear error here comes from relative parity of the three query registers. Measuring the parity of the input data would generally disturb its sector coherence. For general symmetry-verification background, see [Bonet-Monroig et al., Phys. Rev. A 98, 062339 (2018)](https://doi.org/10.1103/PhysRevA.98.062339).
