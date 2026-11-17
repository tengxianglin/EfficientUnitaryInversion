# Slot-resolved first-order error response of the odd-cycle inverter

This calculation concerns the physical oracle slots of the [three-query encoder](THEORY_ODD_CYCLE_THREE_QUERIES.md). The encoder and decoder are ideal. The target is inversion of the intended Hamiltonian. The [parity-breaking error bound](THEORY_ODD_CYCLE_PARITY_ROBUSTNESS.md) gives quadratic protection for parity-odd additive errors. Here we classify the first-order response to arbitrary additive Hermitian errors.

## First-order logical Hamiltonian

Write $\mathcal M_i(E)=W^\dagger E^{(i)} W$, with slots $A,B,C$ ordered as the registers in the definition of the isometry $W$. Let the actual slot-$i$ oracle be $e^{-i(H+\epsilon\Delta_i)}$, for real $\epsilon$ and fixed Hermitian $\Delta_i$. Set
$$
G_i=\int_0^1 e^{itH}\Delta_i e^{-itH}\,dt,\qquad
L=\mathcal M_A(G_A)+\mathcal M_B(G_B)+\mathcal M_C(G_C).
$$
The clean-return Kraus operator is $K_\epsilon=U^\dagger(I-i\epsilon L)+O(\epsilon^2)$ in operator norm. This follows by differentiating each slot and using $U^{\otimes3}W=WU^\dagger$. The range of $W$ is invariant under the ideal triple oracle and its adjoint, so the identity also gives $W^\dagger U^{\otimes3}=U^\dagger W^\dagger$. Leakage from the code has probability $O(\epsilon^2)$, by the norm of the first-order off-code component.

The unconditional output channel after tracing out the auxiliary registers has diamond distance
$$
\|\mathcal E_\epsilon-\operatorname{Ad}_{U^\dagger}\|_\diamond
=|\epsilon|\bigl(\lambda_{\max}(L)-\lambda_{\min}(L)\bigr)+O(\epsilon^2).
$$
The first derivative is the commutator by $L$ composed with the target channel. Subtracting the spectral midpoint gives the upper bound by the spectral diameter, and a balanced superposition of extremal eigenvectors attains it. The clean-return success map has the same derivative. In particular, the response is quadratic exactly when $L$ is scalar. This criterion includes cancellations between different slots.

## Compression by Majorana degree

Use the real physical basis for entrywise conjugation and define the Hermitian monomials $M_I=i^{k/2}\prod_{j\in I}\gamma_j$ for even $k=|I|$, with the product in increasing order. For any operator $E$ in a homogeneous even degree, the compression maps are given below. Degree $2n$ is the parity line, the real span of $P=\prod_j X_j$.

| Degree of $E$ | $\mathcal M_A(E)$ | $\mathcal M_B(E)$ and $\mathcal M_C(E)$ individually |
|---|---|---|
| $0,2n$ | $E$ | $E$ |
| $2,2n-2$ | $-(1-2/n)\overline E$ | $-\overline E/n$ |
| $4,6,\ldots,2n-4$ | $(1-k/n)(-1)^{k/2}\overline E$ | $0$ |

Every parity-odd operator has zero compression in each register since an isolated parity flip leaves the equal-parity sectors.

**Proof of the table.** In sector $S_s$, put $D=2^{n-1}$ and write $Q$ for the fixed charge-conjugation Pauli and $T_j=(\gamma_jQ)|_{S_s}$. Orthogonality of the vectorized $T_j$ gives the slot-$A$ map as the average of $T_j^\dagger E T_j$. For degree $k$, a Majorana negates the monomial if it belongs to the set of its $k$ factors, and otherwise fixes it. The average of these signs is $1-k/n$. Also $Q^\dagger E Q=(-1)^{k/2}\overline E$ by the charge-conjugation identity and the phase $i^{k/2}$. This proves the first-column formula. The identity and parity line can be evaluated directly because the three encoded registers always have the input parity.

For slot $B$, the coefficients of the operators $T_j^\dagger T_\ell$ are $(2nD)^{-1}\operatorname{Tr}_{S_s}(T_j^\dagger E T_\ell)$. Cyclicity through $Q$ puts the trace of $\gamma_j E\gamma_\ell$ in $S_{-s}$. Such a trace is zero unless the product is scalar or proportional to physical parity, because the sector projector is $(I-sP)/2$ and the full Majorana monomials are trace-orthogonal. In the intermediate degrees the trace is therefore zero. Slot $C$ gives the coefficients $(2nD)^{-1}\operatorname{Tr}_{S_s}(T_j^\dagger T_\ell E^\mathsf{T})$. Here $T_j^\dagger T_\ell$ has degree zero or two, and transposition preserves the degree of each monomial, giving the same vanishing.

For a bilinear $E=i\gamma_p\gamma_q$ with $p\ne q$, the only two nonzero slot-$B$ traces have $(j,\ell)=(p,q)$ or $(q,p)$, giving $iD$ and $-iD$. Thus $\mathcal M_B(E)=Q^\dagger E Q/n=-\overline E/n$. To compute slot $C$, apply the intertwiner to $g=e^{-itE}$, which is a quadratic Majorana evolution in both sectors. Differentiation at zero gives $\sum_i\mathcal M_i(E)=-\overline E$. Subtracting the slot-$A$ and slot-$B$ formulas gives the same coefficient for $C$. Multiplication by physical parity takes bilinears to the complementary degree $2n-2$, and each compression commutes with multiplication by $P$ because every output register has the input parity. This proves the complementary formula, including its phase. The calculation in the two real sector bases combines into the stated whole-register identity.

## Consequences for oracle drift

- A perturbation only in slot $B$ or $C$ has a quadratic response when its time-averaged operator $G_i$ lies entirely in the indicated intermediate degrees. Such degrees first occur at $n=5$. In slot $A$ the multiplier is never zero on any even degree for odd $n$.
- A common perturbation $\Delta$ in all slots yields the same $G$ in each. The collective map is invertible on the traceless parity-even subspace, since the multipliers in the table sum to a nonzero number on every degree. In particular it is $-\overline E$ for degree two and its complement, and $3P$ for an error $P$. Thus the only parity-even time-averaged common errors with quadratic output response are scalar.
- If the eigenvalue differences of $H$ avoid nonzero integer multiples of $2\pi$, the time average is invertible. In the energy basis its entrywise factors are $\int_0^1 e^{it(E_a-E_b)}dt$. Therefore every nonscalar common parity-even perturbation produces linear error in this nonresonant regime. This holds at $H=0$ and, for example, if $\|H\|<\pi$.

These conclusions concern ideal known controls and a fixed calibrated encoding. They identify why a common static drift preserving global parity is fundamentally different from the parity-odd errors in the preceding bound.

## Finite verification

The script below evaluates all even monomials in each slot for $n=3,5$ using the repository's explicit encoder. It rescales away the common normalization, checks that the gate-generated amplitudes recover the Gaussian-integer columns within tolerance, and then compares the compression in integer arithmetic.

~~~python
from collections import defaultdict
from math import sqrt

from odd_cycle_encoder import apply_gate, encoder_gates, majorana


def verify(n):
    dimension = 1 << n
    scale = 2 * n * (dimension // 2)
    gates = list(encoder_gates(n))
    columns = []
    lookup = defaultdict(list)
    for x in range(dimension):
        state = {x: 1}
        for gate in gates:
            state = apply_gate(state, gate)
        integer_column = {}
        for row, amplitude in state.items():
            coefficient = amplitude * sqrt(scale)
            nearest = round(coefficient.real)
            assert abs(coefficient - nearest) < 1e-12
            if nearest:
                integer_column[row] = nearest
                lookup[row].append((x, nearest))
        columns.append(integer_column)

    for mask in range(1 << (2 * n)):
        degree = mask.bit_count()
        if degree % 2:
            continue
        # Conjugation changes i to -i and negates each odd-index Majorana.
        imaginary_count = sum((mask >> j) & 1 for j in range(1, 2 * n, 2))
        conjugate = (-1) ** (degree // 2 + imaginary_count)
        action = []
        for x in range(dimension):
            y, phase = x, 1j ** (degree // 2)
            for j in reversed(range(2 * n)):
                if (mask >> j) & 1:
                    y, local = majorana(y, j // 2, j % 2)
                    phase *= local
            action.append((y, phase))
        for slot in range(3):
            if degree in (0, 2 * n):
                multiplier = n
            elif slot == 0:
                multiplier = (n - degree) * (-1) ** (degree // 2) * conjugate
            elif degree in (2, 2 * n - 2):
                multiplier = -conjugate
            else:
                multiplier = 0
            shift = n * slot
            for x, column in enumerate(columns):
                actual = defaultdict(complex)
                for row, coefficient in column.items():
                    local_input = (row >> shift) & (dimension - 1)
                    y, phase = action[local_input]
                    moved = row ^ ((local_input ^ y) << shift)
                    for output, left in lookup.get(moved, ()):
                        actual[output] += n * left * phase * coefficient
                target, phase = action[x]
                assert actual.pop(target, 0) == scale * multiplier * phase
                assert all(value == 0 for value in actual.values()), (n, mask, slot)
    print(f"L={n}: all {1 << (2*n-1)} even monomials verified in all three slots")


for length in (3, 5):
    verify(length)
~~~
