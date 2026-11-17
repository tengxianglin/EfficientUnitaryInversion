# Heralded inversion of commuting Hamiltonian families

This note addresses the multi-query converse discussed in [Issue #3](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/3). [Lai et al., arXiv:2607.29382v2](https://arxiv.org/abs/2607.29382v2) give the joint-spectrum sumset criterion for clean deterministic inversion. The extension below shows that allowing the protocol to discard memory or herald success cannot lower the query count under the same forward-call promise.

## Exact query count with a success flag

Let the known Hermitian generators commute and let their distinct joint eigenvalue vectors form a finite set $W\subset\mathbb R^p$. Write $U(x)=\sum_{w\in W} e^{-i w\cdot x}\Pi_w$ for $x\in\mathbb R^p$. A fixed-order circuit calls the same $U(x)$ exactly $m$ times and may use arbitrary fixed operations, ancillas, intermediate measurements and a success flag. An adaptive circuit bounded by $m$ calls can be padded by routing unused calls into a known joint eigenstate on halted branches. Any extra phase on a halted branch leaves its output channel and outcome probabilities intact.

Let the successful CP map equal $p(x)\operatorname{Ad}_{U(x)^\dagger}$ throughout the promise, with $p(x)\geq 0$ and $p$ nonzero somewhere. This allows zero-probability parameters and imposes no positive worst-case success threshold. Define $mW$ as the set of sums of exactly $m$ vectors of $W$, with repetitions allowed and $0W=\{0\}$. Then such a protocol exists exactly when

$$
C_m := \bigcap_{w\in W}(w+mW)\ne\varnothing .
$$

The same criterion therefore gives the minimum query count for clean deterministic and nonzero heralded channel inversion.

**Necessity.** Expand each forward slot in the joint spectral projectors. After deferring measurements and projecting onto the success flag, every entry of every success Kraus operator is a finite sum of exponentials $e^{-i v\cdot x}$ with $v\in mW$. This representation uses one fixed dilation and one fixed basis for its environment. The successful map has Choi rank at most one, so every success Kraus operator is $K_j(x)=a_j(x)U(x)^\dagger$, including $a_j(x)=0$ at zero-probability parameters. For any unit eigenvector of weight $w$, multiply its diagonal entry of $K_j(x)$ by $e^{-i w\cdot x}$ to obtain the same scalar function $a_j(x)$. Its frequencies therefore belong to $w+mW$ for every $w$. Distinct finite real frequencies are linearly independent, as seen by restriction to a line whose direction separates the frequencies. At least one $a_j$ is nonzero, hence $C_m$ contains a frequency. The argument does not assume a clean output or a nonvanishing success amplitude at every parameter.

**Sufficiency.** Use the deterministic routing construction of Lai et al. Choose $c\in C_m$. For each input weight $w$, choose a tuple of $m$ oracle weights summing to $c-w$. Retain the input coherently in a memory register and, conditioned on its known spectral label, prepare the selected joint eigenstate in the query register for each call and unprepare it after the call. The memory component picks up $e^{-i(c-w)\cdot x}$, with the same global factor $e^{-i c\cdot x}$ for every weight. Return the input to the output register and reset the workspace. This construction counts queries and leaves known-gate cost unoptimized.

## Restricting a heralded converse to a commuting slice

**Proof gap in the previous revision.** A success probability that is nonzero somewhere on the full promise can vanish identically when the added couplings are set to zero. Direct restriction transfers deterministic lower bounds, but a heralded lower bound requires a separate argument. The following perturbation argument supplies it for real linear Hamiltonian families.

For example, for $U=e^{-i(xZ+yX)}$, one call conjugated by $Y$ inverts the data exactly. A separate call on $\lvert0\rangle$ can provide a success flag by measuring $\lvert1\rangle$. This valid two-call exact instrument has zero success on the entire slice $y=0$, so the distinction matters even for a single qubit.

Let $\mathcal L$ be a real linear space of finite-dimensional Hermitian matrices. Suppose a fixed-order protocol with at most $m$ forward calls to $e^{-iH}$ gives an exact success branch across all $H\in\mathcal L$, with nonzero success probability at some $H_*\in\mathcal L$. Then for **every** $A\in\mathcal L$, the set $\Lambda=\operatorname{spec}(A)$ of distinct eigenvalues obeys
$
\bigcap_{\lambda\in\Lambda}(\lambda+m\Lambda)\ne\varnothing.
$
Here $m\Lambda$ denotes sums of exactly $m$ eigenvalues with repetition. Padding a halted classical branch to $m$ calls uses a fresh dummy query register and discards it. This leaves the reduced data channel and the recorded success probability unchanged. Keep the branch record in the dilation. No common eigenstate of the full family is needed.

**Proof.** Fix $A$, put $B=H_*-A$, and restrict the full protocol to $U(t,\epsilon)=e^{-it(A+\epsilon B)}$. Choose a fixed success Kraus operator $K(t,\epsilon)$ with nonzero value at $(1,1)$. Exactness gives $K(t,\epsilon)=a(t,\epsilon)U(t,\epsilon)^\dagger$ for real parameters, with $a=d^{-1}\operatorname{Tr}(K U)$, where $d$ is the system dimension. Analyticity of this scalar in $\epsilon$ implies that some Taylor coefficient at $\epsilon=0$ is a nonzero function of $t$, since $a(1,1)\ne0$. Let $r$ be the least such order, and write $a_r(t)=[\epsilon^r]a(t,\epsilon)$. Then
$
[\epsilon^r]K(t,\epsilon)=a_r(t)e^{itA}.
$

To bound the frequencies of the left-hand side, use the contour formula for the matrix exponential. With $R(z)=(zI-A)^{-1}$ and a contour enclosing the spectrum for $\epsilon$ near zero, the $k$th Taylor coefficient of one query is
$
[\epsilon^k]U(t,\epsilon)=\frac{1}{2\pi i}\oint e^{-itz}R(z)\bigl(BR(z)\bigr)^k\,dz.
$
The rational matrix factor has poles only at $\Lambda$, of order at most $k+1$. Taking residues shows that each matrix entry is a sum of polynomials in $t$ times $e^{-it\lambda}$ with $\lambda\in\Lambda$. This includes repeated eigenvalues of $A$. Multiplying the $m$ query factors and taking the order-$r$ coefficient places every frequency of that Kraus coefficient in $m\Lambda$. Contracting with the fixed gates and memory indices preserves that set.

For a unit eigenvector of $A$ with eigenvalue $\lambda$, multiply the corresponding diagonal entry of the order-$r$ Kraus coefficient by $e^{-it\lambda}$ to obtain $a_r(t)$. Its frequencies lie in $\lambda+m\Lambda$. A polynomial-exponential expansion with distinct frequencies has unique coefficients. For instance, applying powers of the differential operators $D+i\mu$ eliminates any prescribed other modes while acting invertibly on the remaining polynomial factor. Since $a_r$ is nonzero, its frequency support gives the claimed common point.

**Commuting slice.** Let $A=\sum_i b_i A_i$, with commuting generators $A_i\in\mathcal L$ and joint weight set $W$. Choose $b$ so that projection $v\mapsto b\cdot v$ is injective on the finite set $(m+1)W$. Such a choice exists outside finitely many hyperplanes. The spectral criterion for this $A$ then lifts to a point in $\bigcap_{w\in W}(w+mW)$. Thus the clean deterministic optimum on any commuting linear slice lower-bounds exact heralded inversion on the full linear family, even when success on the slice is identically zero.

## Exact cost for odd cycles with independent ZZ couplings

For the field-free odd cycle of length $L\geq 3$, let $H(x)=\sum_{j=0}^{L-1}x_j Z_j Z_{j+1\bmod L}$. Its joint spectrum is $W=\{w\in\{\pm 1\}^L:\prod_j w_j=1\}$. The product condition telescopes in the computational basis, and all such sign patterns are realized by recursively assigning spins around the cycle.

- **Zero calls.** Multiple distinct weights give $C_0=\varnothing$.
- **One call.** Every coordinate attains both signs, forcing any $c\in C_1$ to be zero. For odd $L$, the all-minus vector is absent, so the all-plus weight cannot be completed to zero.
- **Two calls.** Both signs in each input coordinate force $c_j\in\{-1,+1\}$. A triple of signs with sum $c_j$ has product $-c_j$. Any decomposition of $c$ into three rows of $W$ therefore gives $-c\in W$, since $W$ is closed under coordinatewise product. Now choose $w=-c$ in the defining condition for $C_2$. Its two completing rows must sum to $2c$, so both rows equal $c$. This contradicts $c\notin W$ for odd $L$.
- **Three calls.** Properly color the cycle with three colors. Let $V_a$ apply $X$ to every vertex of color $a$. For each edge, its endpoints have different colors, so exactly two of the three conjugations $V_a H V_a$ flip its sign. These Hamiltonians all commute. Thus the product of the three conjugated oracle calls implements $U^\dagger$ on the full register, without ancillas, for arbitrary integrated couplings.

The exact cost is three calls, including for heralded circuits with unrestricted memory. More generally, a non-bipartite graph with a known proper coloring using at most four colors has exact cost three in the edge-only model. For the upper bound, label the colors by distinct two-bit vectors. For each of the three nonzero two-bit vectors, flip the sites where its dot product with the color label is one. Every edge has a nonzero color difference, so two of the three flips negate the edge term. For the lower bound, restrict to the commuting slice supported on any odd cycle and use the restriction theorem above. The added spectator qubits leave the distinct joint weight set unchanged. Independent transverse-field terms are outside this graph corollary.

## Matching lower bounds for the manuscript's mixed examples

The restriction theorem above transfers the seven-site cycle lower bound to the manuscript's noncommuting odd-cycle example in Appendix A. The commuting slice sets the five independent transverse fields on sites 1 through 5 to zero. The manuscript's three-call circuit supplies the matching upper bound for the full mixed promise. The optimum is therefore three for that example, including nonzero heralded circuits.

The second mixed example in the same appendix has a three-qubit Hamiltonian with the term $Z_0 X_1 Z_2$ and all seven nonidentity $X$-strings. Apply the restriction theorem to the commuting slice with the coefficient of $Z_0 X_1 Z_2$ set to zero. The remaining joint weights are the eight rows of the three-bit Walsh matrix with the constant column removed. They are affinely independent because putting the constant column back gives an invertible Walsh matrix. For any $c\in C_m$, each decomposition of $c$ into $m+1$ weights has the same multiplicities, by affine independence and the fixed total count. A decomposition can be chosen to contain each prescribed input weight. Thus every multiplicity is at least one, giving $m+1\ge 8$. The manuscript's seven-call construction supplies the matching upper bound for the full mixed promise. The optimum is seven for that example, including nonzero heralded circuits. This argument also gives the lower bound $2^n-1$ for the full diagonal Pauli family in a known product basis, consistent with the full diagonal result of Odake et al.

## Reproduction

The following integer-only check enumerates the small-cycle joint spectra directly in the computational basis, then computes the intersections for zero through three calls. The finite enumeration checks the examples. The argument above covers all odd lengths.

~~~python
from itertools import product


def cycle_weights(length):
    return {
        tuple(spins[j] * spins[(j + 1) % length] for j in range(length))
        for spins in product((-1, 1), repeat=length)
    }


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


for length in (3, 5, 7):
    weights = cycle_weights(length)
    assert len(weights) == 2 ** (length - 1)
    sums = {(0,) * length}
    feasible = []
    for calls in range(4):
        common = set.intersection(*({add(w, s) for s in sums} for w in weights))
        feasible.append(bool(common))
        if calls < 3:
            sums = {add(w, s) for w in weights for s in sums}
    assert feasible == [False, False, False, True], (length, feasible)
    print(length, len(weights), feasible)


# Check all eight three-bit Walsh weights with the constant column omitted.
weights = {
    tuple((-1) ** (x & mask).bit_count() for mask in range(1, 8))
    for x in range(8)
}
sums = {(0,) * 7}
for calls in range(8):
    common = set.intersection(*({add(w, s) for s in sums} for w in weights))
    assert bool(common) == (calls == 7), calls
    if calls < 7:
        sums = {add(w, s) for w in weights for s in sums}
print('three-bit Walsh spectrum: first feasible at 7 calls')
~~~

## Relation to the literature

[Mo, Lin and Wang, arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1), Section IV and Appendix A, give constructive Pauli recurrences for commuting supports and for certain mixed supports. The converse here uses the joint spectrum of the actual commuting promise. [Odake, Yoshida and Murao, Phys. Rev. Lett. 135, 230603 (2025)](https://doi.org/10.1103/drp2-rzzw) give a general differentiable lower-bound framework, including promised subgroups and probabilistic transformations. Their [Supplemental Material, Section C.2](https://journals.aps.org/prl/supplemental/10.1103/drp2-rzzw/sm.pdf) gives the deterministic lower bound for the full diagonal group. The present extension uses common frequency support of success Kraus operators and treats commuting subfamilies with a parameter-dependent success probability. No priority claim is made.

The fully fielded odd cycle remains open under this argument. The edge-only restriction proves a three-call lower bound there, and the construction for the manuscript's restricted-field example depends on the missing endpoint fields.
