# Six-query recovery with two fixed spectator modes

The physical five-site Ising problem asks whether six queries suffice for exact ideal inversion and zero first-order response to common parity drift. The [root-torus construction](THEORY_ODD_CYCLE_PHYSICAL_ROOT_TORI.md) gives physical bases obtained by rotating one pair of Majorana modes. The [21-basis projection calculation](THEORY_ISING_PENTAGON_ROOT_PROJECTION.md) leaves open whether such basis comparisons can support a pointwise isometry. Here a six-query circuit handles every comparison supported on one fixed block with at least two spectator modes.

**Theorem.** Fix an odd number \(n\ge5\) of modes and an odd number \(3\le k\le n-2\) of active modes, in known positions. On plus data the oracle may act by an arbitrary \(\mathrm{Spin}(2k)\) Gaussian unitary on those modes and arbitrary diagonal phases on the other \(n-k\) modes. On minus data it may act by an independent arbitrary \(\mathrm{Spin}(2n)\) Gaussian unitary. The oracle is drifted by \(e^{-i\epsilon P}\) with \(P=+I\) on plus data and \(-I\) on minus data. There is a deterministic six-forward-query protocol, with parameter-independent controls and no postselection, that implements entrywise conjugation exactly at zero drift and has diamond error \(O(\epsilon^2)\) uniformly on this promise. On real-symmetric unitaries the ideal target is the inverse.

At \(n=5\), any *fixed* three-mode block can mix arbitrarily and the circuit still suppresses the linear drift. Thus even enforcing the full pointwise normalization, exactness and zero derivative on all root tori supported within that block cannot establish a seven-query minimum. The unrestricted physical pentagon can mix modes outside any such fixed block.

## 1. Match the two-query representation on each spectator label

Let \(m=n-k\) be the even number of spectator modes. Write \(D=2^{n-1}\) and \(d=2^{k-1}\). The plus space decomposes as \(\bigoplus_t S_{\sigma(t)}^{(k)}\), where \(t\in\{+1,-1\}^m\) is the spectator sign row and \(\sigma(t)=\prod_i t_i\) is the required active chirality. This follows by factoring the total parity into active and spectator parity. For an ideal plus oracle \(U_+\), each block acts as
\[
 e^{-it\cdot\theta}\,\pi_{\sigma(t)}(g),\qquad
 g\in\mathrm{Spin}(2k).
\]
The two active half-spin representations \(\pi_\sigma\) are dual since \(k\) is odd. Equivalently the odd-mode charge conjugation in the [three-query note](THEORY_ODD_CYCLE_THREE_QUERIES.md#a-fixed-encoding-for-odd-numbers-of-fermionic-modes) exchanges their chiralities. The spectator labels and active sectors are fixed spaces independent of the oracle.

Consider the joint logical target \(\bar U_+\otimes\bar U_+\), on plus data and a plus program register. On spectator labels \((t,t')\) its torus character is \(e^{+i(t+t')\cdot\theta}\) and both active chiralities are conjugated. A two-plus-query realization can choose query spectator labels \((u,u')\) with \(u+u'=-(t+t')\).

- If \(t\ne t'\) and the two spectator parities are opposite, take \(u=-t,\ u'=-t'\). Negation preserves spectator parity since \(m\) is even. Swapping the two active factors matches the conjugate target.
- If \(t\ne t'\) and the spectator parities agree, start with \((-t,-t')\). Exchange the two signs in any one coordinate where \(t,t'\) differ. The sum is unchanged and both spectator parities flip, matching the conjugate active chiralities without a swap.
- If \(t=t'\), the character forces \(u=u'=-t\) in every coordinate. The query active chirality equals the original chirality. The [common half-spin square subspace](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md#3-bounds-by-center-class) has rank \(r_k=d^2-\frac12\binom{2k}{k}\), with normalized active-program marginal \(\operatorname{Tr}_2 Q_k/d=(r_k/d^2)I\) by its [orthonormal unitary-vector construction](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md#a-shared-two-spinor-subspace). At \(k=3\) the shared space is the six-dimensional antisymmetric square.

Let \(Q\) on the joint plus data and plus program space be the identity on all ordered unequal-label blocks and \(Q_k\) on each equal-label block. Blockwise isometries give a single two-forward-query intertwiner \(A\) on \(\operatorname{ran}Q\) into two plus registers with an unqueried flag recording the ordered input labels, so possible repetitions of the same query labels cause no conflict. The spectra and the flag are fixed except for the action of the oracle. The flag is uncomputed by inverse decoding on the encoded image. \(Q\) commutes with \(\bar U_+^{\otimes2}\). After tracing a maximally mixed plus program its marginal is
\[
 \frac{\operatorname{Tr}_2 Q}{D}=\alpha_{n,k} I,\qquad
 \alpha_{n,k}=1-\frac{d^2-r_k}{dD}
             =1-2^{k-n}\left(2\binom{2k}{k}/4^k\right).
\]
Indeed each input spectator label has just one equal-label partner. All other program labels contribute the identity. The loss on the equal block is \((d^2-r_k)/d\) times the identity on the active input. Since \(k\le n-2\), \(\alpha_{n,k}\ge27/32\), using \(2\binom{2k}{k}/4^k\le5/8\) for \(k\ge3\). In the pentagon \(D=16,d=4\), and \(Q\) has rank \(4\cdot6+12\cdot16=216\), giving \(\alpha_{5,3}=27/32\).

## 2. Pointwise recovery and query count

Use the fixed encoders and decoder of the [six-query split construction](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md#six-unconditional-calls-and-a-fixed-decoder), substituting the projector \(Q\) and the flagged two-query intertwiner \(A\) above. Prepare the plus program as half of a maximally entangled state. On the joint plus input, route \(\operatorname{ran}Q\) through two plus calls and four minus calls on the invariant state, and route \(\ker Q\) through two three-plus-call encodings. The two branches lie in distinct slot-parity sectors and decode coherently to the same joint target. Their common-drift charges are \(-2\) and \(6\). On minus data, use three minus calls on data and three plus on the program, with charge zero. The program acts by \(\bar U_+\) on every ideal branch regardless of the input sector. The three-query intertwiner and the four-query invariant state are valid for all Gaussian unitaries in those parity blocks, so the minus oracle needs no additional promise.

For the split encoder, the first-order generator on plus data and program is \(6I-8Q\). The ideal joint unitary factors and remains unitary on this entire encoded space. Taking the program trace gives \((6-8\alpha_{n,k})\Pi_+\) on data, with \(\Pi_+\) the plus projector. Choose this encoder with input-independent probability \(p=3/(4\alpha_{n,k})\), and otherwise use the encoder that sends all plus inputs through the six-plus branch. Then the mean first-order generator is zero. At \(n=5,k=3\), \(p=8/9\). Every run makes six queries. The ideal channel is exact for every promised oracle and the drifted channel is trace preserving for every \(\epsilon\). Its Taylor remainder is uniform because decoding leaves a channel independent of the ideal oracle after correcting by the target.

This promise includes the full independently phased field torus. The [Fourier lower bound on that torus](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md#norm-bound-and-drift-response) excludes three through five queries for first-order suppression. Fewer than three already fail the ideal support constraint: the [same-sector lift argument](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md#allowed-phase-lifts-through-six-queries) shows that a common ideal spectator frequency needs at least three same-sector calls for some input. Thus the restricted promise has minimum six.

## 3. Four active modes on the pentagon

There is a sharp comparison for \(n=5,k=4\) when the exact ideal environment in a fixed Stinespring dilation is the inverse-spinor Bell state \(v(U)=\operatorname{vec}(\bar U_+)/4\), up to a fixed environmental isometry. The plus oracle may range over \(\mathrm{Spin}(8)\) on a fixed set of four active modes with an independent phase on the remaining mode, and the minus oracle remains independent \(\mathrm{Spin}(10)\). For this promise and spectator condition, the optimal six-query worst-case linear diamond coefficient is \(3/16\), even allowing general deterministic fixed-order circuits.

There are now two spectator labels and the active half-spins are each self-dual. For an equal-label block the two-query alternative must reverse that label on both slots, so it must use the other chirality. The two squares share the scalar and adjoint representations of dimensions \(1,28\), and have different \(35\)-dimensional remaining representations. This follows from the two-spinor weight rule in the [Gaussian-group note](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md#3-bounds-by-center-class) and is checked exactly below. For unequal labels the opposite-chirality product can match the whole block. The shared joint rank is \(2(29)+2(64)=186\), out of 256.

For the converse, use the Haar charge-lift argument of the [Gaussian-group bound](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md#1-haar-bound-for-a-six-query-comb) on \(\mathrm{Spin}(8)\) times the spectator phase circle on plus data and the full minus group. The independent scalar order-four phases on the two parity blocks remain in this promise. With this single environment character, the plus target can use plus counts \(6,2\) and the minus target plus count \(3\) only. The projected squared norm of the plus ideal amplitude, averaged over inputs, is exactly \(186/256\). Indeed its entries are those of \(\bar U_+^{\otimes2}\) scaled by \(1/4\). The alternate projection keeps exactly the matrix coefficient spaces shared with \(U_+^{\otimes2}\), so that the retained mean squared norm divided by the joint dimension is the shared rank fraction. The four minus queries admit a constant coefficient by the invariant state. The minus target has no alternate. The averaged slope bound gives \(6-8(186/256)=3/16\).

The split encoding attains this slope on the prescribed promise. The shared marginal on an equal-label block is \(29/8\) times the identity by irreducibility of its active input and invariance of the shared projector. Including the unequal block gives the normalized marginal \(186/256\) on each spectator label. The split encoder alone therefore has first-order generator \((3/16)\Pi_+\) and the requested slope. This converse takes the four-active-mode group as its oracle promise and fixes the ideal spectator; the physical pentagon and unrestricted ideal environments require further constraints.

## 4. Physical implication and remaining test

For the physical pentagon, a root rotation with endpoints in the chosen triple is a Gaussian component supported on that active block, with independent phases on the remaining two modes. The circuit handles all such tori at all phase values and all real rotation angles, with a shared exact ideal map and vanishing pointwise derivative. The restricted model even includes arbitrary compositions of active Gaussian rotations within that triple. One cannot use a different circuit for each triple in a proof about a fixed unknown oracle. A next finite test is to couple constraints from two overlapping active blocks whose union has four sites, so that the six-query circuits for one isolated triple cannot certify feasibility across the whole test.

The [EUI manuscript and Appendix B](https://arxiv.org/html/2506.20570v1) provide the structured inversion and error context. The [group-symmetric comb framework](https://arxiv.org/abs/2510.07100) gives a general setting for symmetry-adapted isometries. Here the relevant difference between the active-block model and the full Gaussian model is the extra two-query intertwiners supplied by distinct spectator labels.

## Exact verification

The following Python 3 block enumerates the available irreducibles at each spectator character using the minuscule tensor rule and rational Weyl dimensions. It verifies the two active-block cases at five sites and checks the two-spectator odd-mode formula at seven sites.

~~~python
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, prod


@lru_cache(maxsize=None)
def half_spin_weights(k, parity):
    return tuple(row for row in product((1, -1), repeat=k) if prod(row) == parity)


@lru_cache(maxsize=None)
def square_irreps(k, left, right):
    highest = (1,) * (k - 1) + (left,)
    result = set()
    for weight in half_spin_weights(k, right):
        row = tuple(a + b for a, b in zip(highest, weight))
        if all(a >= b for a, b in zip(row[:-2], row[1:-1])) and row[-2] >= abs(row[-1]):
            result.add(row)
    return result


@lru_cache(maxsize=None)
def dimension(row):
    rho = tuple(2 * (len(row) - i - 1) for i in range(len(row)))
    shifted = tuple(a + b for a, b in zip(row, rho))
    value = prod(
        Fraction(shifted[i]**2 - shifted[j]**2, rho[i]**2 - rho[j]**2)
        for i in range(len(row)) for j in range(i + 1, len(row))
    )
    assert value.denominator == 1
    return value.numerator


def verify(n, k, sector):
    d, D = 2**(k - 1), 2**(n - 1)
    labels = tuple(product((1, -1), repeat=n - k))

    def chirality(row):
        return sector * prod(row)

    available = defaultdict(set)
    for u, v in product(labels, repeat=2):
        summed = tuple(a + b for a, b in zip(u, v))
        available[summed].update(square_irreps(k, chirality(u), chirality(v)))

    dual_sign = (-1)**k
    total = 0
    for t, t_prime in product(labels, repeat=2):
        opposite = tuple(-a - b for a, b in zip(t, t_prime))
        target = square_irreps(k, dual_sign * chirality(t), dual_sign * chirality(t_prime))
        assert sum(map(dimension, target)) == d*d
        shared = sum(map(dimension, target & available[opposite]))
        expected = d*d - comb(2*k, k)//2 if t == t_prime else d*d
        assert shared == expected
        total += shared

    fraction = Fraction(total, D*D)
    assert fraction == 1 - Fraction(comb(2*k, k), 2*d*D)
    return total, fraction, Fraction(3, 4) / fraction


for n, k in ((5, 3), (5, 4), (7, 3), (7, 5)):
    result = verify(n, k, 1)
    assert verify(n, k, -1) == result
    print(n, k, *result)
assert verify(5, 3, 1) == (216, Fraction(27, 32), Fraction(8, 9))
assert verify(5, 4, 1) == (186, Fraction(93, 128), Fraction(32, 31))
assert 6 - 8 * verify(5, 4, 1)[1] == Fraction(3, 16)
~~~
