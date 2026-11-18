# Four- and five-query drift obstruction for the Ising triangle

This note advances the [arbitrary causal three-query converse](THEORY_ISING_TRIANGLE_SEQUENTIAL_DRIFT.md). We require deterministic exact inversion on the full ideal Ising triangle promise. The model allows arbitrary finite quantum memory, known interleaving operations, intermediate measurements and discarded output environment. There are $m$ unconditional forward queries to the same oracle. Under common drift the oracle is $e^{-i(H+\epsilon P)}$, with $P=X_0X_1X_2$.

**Result.** Four and five queries are insufficient for first-order drift suppression, even for sequential combs. More precisely, for $3\leq m\leq6$, the supremum, over the certified ray of ideal Hamiltonians, of the leading diamond error coefficient is at least $12-2m$. The six-query case gives an equality condition and an exact six-query protocol on the diagonal torus alone. The deterministic first-order suppression cost for the full triangle is now either six or seven.

## Fourier setup

Use the [explicit certified ray](THEORY_ISING_TRIANGLE_SEQUENTIAL_DRIFT.md#a-ray-with-independent-sector-phases), on which ideal identities extend to the torus of eight eigenphases $z_{s,j}$ with determinant one separately in each four-dimensional parity sector. Canonical character exponents are nonnegative integer rows with minimum zero in each four-entry block. Write $|\nu|$ for their total weight and $A(\nu)$ for the weight in the plus block.

The output of a fixed Stinespring implementation on basis input $j$ is a vector-valued homogeneous polynomial of degree $m$ in the eight phases. Under drift the query monomial with count vector $a$ picks up the factor $e^{-i\epsilon q(a)}$, where $q(a)$ is its plus count minus its minus count. This follows slot by slot regardless of the comb's interleaving gates. The same physical implementation is isometric at every torus point for every real $\epsilon$, since all diagonal query unitaries considered in this calculation are unitary.

At ideal inversion the output on $j$ is $z_j^{-1}|j\rangle\otimes v(z)$ with the same environment vector for all $j$. Write $v(z)=\sum_\nu z^\nu v_\nu$. Haar normalization gives $\sum_\nu\|v_\nu\|^2=1$. For each $\nu$ with nonzero coefficient, pick a coordinate $j$ with $\nu_j=0$. The canonical representative of $\nu-e_j$ then has weight $|\nu|+3$. Any lift to a count vector consists of adding multiples of the two block determinant vectors. Thus $m-|\nu|-3$ is nonnegative and divisible by four. For $3\leq m\leq6$, this forces $|\nu|=m-3$.

For any fixed input $j$ and any output frequency (including off-target data amplitudes), there are at most two lifts of a canonical frequency to degree $m$. With two, the plus counts differ by four, so their drift charges differ by eight. For input in the plus sector choose as the preferred lift the one with larger plus count, and for input in the minus sector choose the smaller. Choose the unique lift at a single-lift frequency. The other lift, when it exists, will be called the alternate.

On a correct ideal frequency $\nu-e_j$, the preferred charge is $q_+(\nu)=2(A(\nu)+3)-m$ for a plus input, and $q_-(\nu)=2A(\nu)-m$ for a minus input. The frequency has an alternate exactly when $\nu_j>0$. Indeed if $\nu_j=0$ the canonical weight is already $m$. If $\nu_j>0$ it is $m-4$, so one block determinant can be placed in either sector. This also proves the preferred charge formulas.

## Normalization bounds the alternate response

Fix input $j$. Use the Hilbert space of output vectors indexed by the canonical frequency, including all data and environment components. Let $b_j$ collect the preferred amplitudes and $c_j$ the alternate amplitudes. Let $a_j=b_j+c_j$ be the ideal amplitude vector. Parseval's identity and Stinespring normalization for every $\epsilon$ give
$$
1=\|b_j+e^{\pm8i\epsilon}c_j\|^2
$$
where the sign depends only on the input sector. The preferred phases can be removed separately at each Fourier frequency, which preserves this norm. Therefore $\langle b_j,c_j\rangle=0$ and $\langle a_j,c_j\rangle=\|c_j\|^2$. Write $\beta_j=\|c_j\|^2$. The vector $c_j$ lives on frequencies admitting an alternate. The projection of $a_j$ onto those frequencies has squared norm $\sum_{\nu:\nu_j>0}\|v_\nu\|^2$. By Cauchy–Schwarz,
$$
0\leq\beta_j\leq\sum_{\nu:\nu_j>0}\|v_\nu\|^2,\qquad
\sum_{j=1}^8\beta_j\leq m-3 .
$$
The last step uses that a normalized exponent of weight $m-3$ has at most $m-3$ nonzero coordinates. This inequality allows coherent interference between the two lifts. It does not treat the lifts as classical paths.

For a plus input $i$ and a minus input $j$, evaluate the output matrix element of the channel on $|i\rangle\langle j|$ and remove its ideal diagonal-oracle phase. Haar averaging its first derivative over the torus gives the imaginary phase slope with magnitude governed by the real number
$$
6-8(\beta_i+\beta_j).
$$
To see the signs, the derivative of the phase-corrected output amplitude for each basis state is obtained by multiplying its Fourier amplitudes by $-i$ times the appropriate drift charge. Paired with the ideal environment vector and averaged, it gives the expectation of the preferred charges and the alternate shift $-8\beta_i$ for plus or $+8\beta_j$ for minus. The preferred expectations differ by six, and only the correct-data amplitudes pair with the ideal vector. Taking the complex conjugate for the minus input gives the displayed difference.

Average this slope over all 16 opposite-sector pairs. The result is at least $6-2(m-3)=12-2m$. A single matrix element on an input operator of trace norm one lower-bounds the diamond response. The ray is dense in the torus, since its only integer phase relations are the two block traces, or one can average the finite Fourier sum directly over long intervals on the ray. Thus the supremum of the physical ray responses is at least the displayed number. For four and five queries this is positive.

## Where the six-query proof stops

If a six-query comb suppresses the first order on the full triangle, it must saturate both inequalities above on the certified torus. Every occupied $\nu$ then has three distinct occupied coordinates, and for every input the entire weight on alternate-eligible ideal frequencies must use the alternate lift. In fact Cauchy–Schwarz equality with $\langle a_j,c_j\rangle=\|c_j\|^2$ implies that $c_j$ is exactly the projection of $a_j$ onto that space. Also $\beta_i+\beta_j=3/4$ for every opposite-sector pair. These are necessary conditions that any proposed six-query full-promise circuit must satisfy on each certified ray.

They are attainable on the commuting diagonal torus in this fixed, known basis. Choose uniformly a three-element subset $S$ of the four plus labels and route coherently according to the input eigenlabel. For plus input $j\in S$, query the other two plus labels in $S$ and all four minus labels. For plus input $j\notin S$, query the three plus labels of $S$ and the three plus labels distinct from $j$. For minus input, query the three plus labels of $S$ and the three minus labels distinct from $j$. Every branch gives ideal inversion up to the shared phase $\prod_{\ell\in S}z_\ell$. Their drift charges are $-2$, $6$, and $0$, respectively. Averaging over $S$ sets the mean drift charge of every input label to zero, so the mixed channel has no first-order error. The torus lower bound makes six optimal for first-order suppression on that commuting family.

That routing uses a known eigenbasis and does not implement a circuit on the full noncommuting promise. The [fixed seven-query deterministic recovery](THEORY_ODD_CYCLE_DETERMINISTIC_RECOVERY.md) remains the full-promise upper bound. The remaining problem is whether the six-query saturation conditions for different eigenbases are compatible in one comb.

## Exact verification

The following check enumerates character aliases for all $m=3,\ldots,6$ and verifies the charge formulas, eligible counts and the six-query torus construction. The coefficient bound uses the normalization proof above, which is independent of enumeration.

~~~python
from itertools import combinations, combinations_with_replacement


def canonical(a):
    p, n = min(a[:4]), min(a[4:])
    return tuple(v - (p if i < 4 else n) for i, v in enumerate(a))


def charge(a):
    return sum(a[:4]) - sum(a[4:])


for m in (3, 4, 5, 6):
    aliases = {}
    for word in combinations_with_replacement(range(8), m):
        a = tuple(word.count(i) for i in range(8))
        aliases.setdefault(canonical(a), []).append(charge(a))
    compatible = []
    for j in range(8):
        compatible.append({
            canonical(tuple(x + int(i == j) for i, x in enumerate(a)))
            for a in aliases
        })
    common = set.intersection(*compatible)
    assert common and all(sum(nu) == m - 3 for nu in common)
    for nu in common:
        total_eligible = 0
        for j in range(8):
            f = canonical(tuple(x - int(i == j) for i, x in enumerate(nu)))
            values = sorted(aliases[f])
            expected = 2 * sum(nu[:4]) - m + (6 if j < 4 else 0)
            preferred = values[-1] if j < 4 else values[0]
            assert preferred == expected
            assert len(values) == (2 if nu[j] else 1)
            if len(values) == 2:
                assert values[1] - values[0] == 8
            total_eligible += len(values) == 2
        assert total_eligible == sum(x > 0 for x in nu) <= m - 3
    print(m, len(common), 12 - 2*m)

routing_charges = [[] for _ in range(8)]
for subset in combinations(range(4), 3):
    spectator = tuple(int(i in subset) for i in range(8))
    for j in range(8):
        if j < 4 and j in subset:
            word = [i for i in subset if i != j] + list(range(4, 8))
        elif j < 4:
            word = list(subset) + [i for i in range(4) if i != j]
        else:
            word = list(subset) + [i for i in range(4, 8) if i != j]
        a = tuple(word.count(i) for i in range(8))
        assert len(word) == 6
        assert canonical(a) == canonical(tuple(x - int(i == j) for i,x in enumerate(spectator)))
        routing_charges[j].append(charge(a))
assert all(sum(values) == 0 for values in routing_charges)
print("Six-call diagonal-torus routing has zero average charge for all eight inputs.")
~~~
