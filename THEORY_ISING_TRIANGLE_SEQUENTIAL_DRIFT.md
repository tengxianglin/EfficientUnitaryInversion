# Three-query parity drift in arbitrary causal combs on an Ising triangle

We consider the fully fielded three-site cycle with independent real couplings, fixed-order access, and exactly three unconditional calls to the same unitary. The comb may have arbitrary ancillary memory, interleaving operations, intermediate measurements, and an oracle-dependent discarded environment. It must implement deterministic exact inversion for the entire ideal Hamiltonian family.

**Result.** There is an explicit one-parameter ray in this physical promise on which every such comb induces exactly the channel of $U^\dagger e^{-i3\epsilon P}$ under common parity drift $\epsilon P$, where $P=X_0X_1X_2$. Its diamond error on that ray is $2|\sin(3\epsilon)|$. Thus three queries cannot suppress the linear drift for the full three-site promise, even with sequential controls and an arbitrary output environment. This extends the [clean parallel three-query obstruction](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md) for this system size.

## A ray with independent sector phases

Take the fixed fields $(1,2,3)$ and cyclic edge coefficients $(4,5,6)$, and scale all six by $t\in\mathbb R$. Write $H_*$ for the unscaled Hamiltonian. Its two four-dimensional parity blocks have characteristic polynomials
$$
f_+(z)=z^4-182z^2-1008z-671,\qquad
f_-(z)=z^4-182z^2-912z-671.
$$
The blocks are traceless. Reduction modulo $17$ for $f_+$ and modulo $19$ for $f_-$ is irreducible. Both polynomials have factor degrees $1,3$ modulo $5$. None of these primes divides the corresponding discriminant. The unramified factor-degree criterion therefore supplies a 4-cycle and a 3-cycle in each Galois group. A subgroup of $S_4$ containing both has order divisible by 12 and cannot be $A_4$, so both groups are $S_4$.

The discriminants have different rational square classes, as seen from the prime $691$ occurring to odd exponent only for $f_+$. The two splitting fields therefore have different unique quadratic subfields. Their intersection is Galois and its group is a common quotient of $S_4$. Every nontrivial quotient of $S_4$ has a quotient of order two. A nontrivial intersection would thus give a shared quadratic subfield, so the intersection is trivial and the compositum group is $S_4\times S_4$.

In a rational relation among the eight eigenvalues, apply a transposition of any two roots of one polynomial while fixing all the roots of the other. Subtracting the relation shows that the two corresponding coefficients agree. Hence the only rational relations are multiples of the two sums of all four roots in each block, both of which are zero.

In a common eigenbasis of $H_*$ and $P$, write the oracle on this ray as diagonal phases $z_{s,j}(t)=e^{-it\lambda_{s,j}}$. The rational-relation calculation allows us to treat these phases as independent subject to $\prod_j z_{s,j}=1$ in each sector. Specifically, any finite Laurent identity on the ray extends to this product torus. Two exponent vectors have the same ray frequency exactly when they differ by constant integer vectors within the two separate blocks. Fourier independence for distinct real frequencies then shows that all Laurent coefficients vanish after grouping by torus character. This argument does not require querying any oracle outside the stated family.

## Why the comb has a fixed drift slope

Take a fixed Stinespring realization of the comb with all measurements deferred and all discarded systems retained in the environment. For diagonal oracle phases $z$, its isometric action $V_\epsilon(z)$ with common parity drift is a homogeneous polynomial of degree three in the eight phases. Every query contributes one diagonal entry. A monomial with nonnegative count vector $a$ and total count three picks up the extra scalar $e^{-i\epsilon q(a)}$, where $q(a)=\sum_j a_{+,j}-\sum_j a_{-,j}$. These facts apply to arbitrary parameter-independent interleaving maps.

Exact inversion on the ray requires
$$
V_0(z)|s,j\rangle=z_{s,j}^{-1}|s,j\rangle\otimes v(z)
$$
with the same environment vector for every input basis state. This follows from the purity of the unitary output channel and linearity on coherent superpositions. All off-diagonal data amplitudes vanish on the ray. The diagonal environment factors become equal after multiplication by $z_{s,j}$, so the finite Laurent identities extend to the torus. The resulting common $v(z)$ is a finite Laurent polynomial.

Represent every torus exponent by the unique integer row with minimum zero separately in each four-entry block. Let $\nu$ be any nonzero-coefficient exponent of $v$. Choose a plus-sector coordinate $j$ at which its minimum is zero. In $z_{+,j}^{-1}v$ the exponent $\nu-e_{+,j}$ requires a minimal nonnegative representative of total count $|\nu|+3$. Indeed, one coordinate decreases by one and then all four coordinates in that block must be raised by one. Since degree three is the entire query budget, $|\nu|=0$. Thus the environment is constant in this fixed dilation, even though the model permits an oracle-dependent environment.

Finally, every exponent of an ideal degree-three monomial has at least one zero per block. Each such monomial therefore already equals its canonical representative and distinct degree-three count vectors cannot alias on the torus. For input $|s,j\rangle$ the unique inverse monomial is the product of the other three phases in the same sector. Its charge is $3s$. The drift multiplies this input component by $e^{-i3s\epsilon}$ and leaves the same environment vector. The output channel of the full comb is therefore exactly $\operatorname{Ad}_{U^\dagger e^{-i3\epsilon P}}$ on the ray. A balanced input across the sectors gives the diamond distance $2|\sin(3\epsilon)|$, as in the [parallel norm calculation](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#exact-drift-response-and-a-seven-query-construction).

## Scope and reproduction

The three-query minimum for ideal inversion is known from the [explicit three-query construction](THEORY_ODD_CYCLE_THREE_QUERIES.md) and its matching lower bound. With the present obstruction, deterministic first-order drift suppression on the three-site full promise requires at least four calls, and the existing deterministic seven-call construction remains an upper bound. The present argument does not decide four through six calls. At four calls a count vector can differ by a full sector determinant without changing its torus character, so the degree-three uniqueness step no longer applies. The all-length problem also requires further work. See [Mo, Lin and Wang](https://arxiv.org/html/2506.20570v1) for the structured Hamiltonian promise, and [Odake, Yoshida and Murao](https://arxiv.org/abs/2405.07625) for a separate general quantum-query lower-bound framework.

This check builds the blocks directly in the sitewise Hadamard basis, where $P$ is computational parity. It certifies the modular factor degrees and discriminant factorizations, then enumerates all degree-three characters and their drift charges. No floating-point eigenvalues are used.

~~~python
from itertools import combinations_with_replacement

import sympy as s

z = s.symbols("z")
quartics = {}
for parity, h, j, prime in ((1, (1, 2, 3), (4, 5, 6), 17), (-1, (1, 2, 3), (4, 5, 6), 19)):
    basis = [x for x in range(8) if (-1)**x.bit_count() == parity]
    matrix = s.zeros(4)
    for col, x in enumerate(basis):
        matrix[col, col] = sum(h[i] * (-1)**((x >> i) & 1) for i in range(3))
        for i in range(3):
            y = x ^ (1 << i) ^ (1 << ((i + 1) % 3))
            matrix[basis.index(y), col] += j[i]
    f = matrix.charpoly(z).as_expr()
    discr = s.discriminant(f, z)
    assert discr % 5 and discr % prime
    assert s.Poly(f, z, modulus=prime).is_irreducible
    linear = z - parity
    cubic, remainder = s.div(f, linear, z, modulus=5)
    assert remainder == 0 and s.Poly(cubic, z, modulus=5).is_irreducible
    quartics[parity] = (f, s.factorint(discr))

assert quartics[1] == (
    z**4 - 182*z**2 - 1008*z - 671, {2: 14, 3: 2, 691: 1, 7159: 1}
)
assert quartics[-1] == (
    z**4 - 182*z**2 - 912*z - 671, {2: 14, 3: 3, 23: 1, 29: 1, 7589: 1}
)


def normalize(row):
    a, b = row[:4], row[4:]
    return tuple(x - min(a) for x in a) + tuple(x - min(b) for x in b)


monomials = {}
for positions in combinations_with_replacement(range(8), 3):
    counts = tuple(positions.count(i) for i in range(8))
    monomials.setdefault(normalize(counts), []).append(counts)

translated = []
for i in range(8):
    row = tuple(-int(j == i) for j in range(8))
    inverse = normalize(row)
    witnesses = monomials[inverse]
    assert len(witnesses) == 1
    assert sum(witnesses[0][:4]) - sum(witnesses[0][4:]) == (3 if i < 4 else -3)
    translated.append({
        normalize(tuple(value + int(j == i) for j, value in enumerate(freq)))
        for freq in monomials
    })
assert set.intersection(*translated) == {(0,) * 8}
print("Two quartic S4 certificates; unique common frequency and per-input parity charge.")
~~~
