# Seven queries are necessary and sufficient for parity-drift suppression on the Ising triangle

Let \(H=\sum_{i=0}^2 h_i X_i+\sum_{i=0}^2 J_i Z_iZ_{i+1\bmod3}\), with independent real coefficients, and let \(P=X_0X_1X_2\). Take a deterministic fixed-order circuit with \(m\) unconditional forward calls to the same oracle \(W_\epsilon(H)=e^{-i(H+\epsilon P)}\). Any finite memory, intermediate controls and measurements, and discarded systems are allowed. All operations outside the oracle are independent of \(H,\epsilon\). Write \(\Phi_{H,\epsilon}\) for the resulting channel on the data.

**Theorem.** The minimum \(m\) for which \(\|\Phi_{H,\epsilon}-\operatorname{Ad}_{e^{iH}}\|_\diamond=o(|\epsilon|)\) as \(\epsilon\to0\) for every \(H\) is seven. The [seven-query deterministic recovery](THEORY_ODD_CYCLE_DETERMINISTIC_RECOVERY.md) attains \(28|\epsilon|^3+O(|\epsilon|^4)\) uniformly in \(H\), using the diamond norm without a factor of one half. The ideal-only minimum is [three queries](THEORY_ODD_CYCLE_THREE_QUERIES.md). Six queries suffice on a [single certified diagonal torus in a known basis](THEORY_ISING_TRIANGLE_FOUR_FIVE_DRIFT.md#where-the-six-query-proof-stops).

The premise only requires the linear channel derivative to vanish for each fixed \(H\). The new step is to compare the six-query equality conditions in different physical eigenbases.

## 1. Extending the ray argument to limiting eigenbases

The [three-query note](THEORY_ISING_TRIANGLE_SEQUENTIAL_DRIFT.md#a-ray-with-independent-sector-phases) certifies a Hamiltonian \(H_*\) whose only integer eigenvalue relations are the two parity-block traces. Such Hamiltonians are dense in the real promise. To see this, choose any \(H_0\) in the promise and form the pencil \((1-t)H_*+tH_0\). Apply Rellich's one-parameter analytic eigenvalue theorem separately in the two parity blocks on an interval containing \([0,1]\). The local analytic eigenvalue branches extend along the interval by matching them on overlaps. Every fixed integer relation whose coefficients are nonconstant on at least one block gives an analytic function of \(t\) that is nonzero at \(t=0\). Its zero set is discrete, and the union over all such relations is countable. One can therefore take a sequence of points outside that union tending to \(t=1\). In particular, if \(H_0\) has simple spectrum within each sector, its parity-labelled eigenbasis is a limit of eigenbases with the stated phase independence, choosing the labels and phases continuously near \(H_0\).

For a parity-labelled basis \(B\), let \(D_B(z)\) be the diagonal oracle in this basis with \(\prod_{j\in +}z_j=\prod_{j\in -}z_j=1\). For a Hamiltonian with the stated independence, the phases of its scaled ray are dense on this torus. Exact inversion and zero channel derivative therefore hold on the entire torus in its basis. Both identities pass to limits of bases since the fixed Stinespring isometry \(V(W)\) is a polynomial in the entries of \(W\), and the channel and its drift derivative for \(W=D_B(z)e^{-i\epsilon P}\) are continuous in \(B\). Consequently the two identities hold on every torus of a simple-in-sector physical eigenbasis, and on every limit of those tori.

## 2. What equality at six calls implies

Assume a six-query circuit meets the premise. Fix any torus from Section 1. The ideal output is
\[
V(D_B(z))|j\rangle=z_j^{-1}|j\rangle\otimes v(z),\qquad
\|v(z)\|=1.
\]
Use the [degree-six Parseval calculation](THEORY_ISING_TRIANGLE_FOUR_FIVE_DRIFT.md#normalization-bounds-the-alternate-response). In its notation, each opposite-sector slope gives \(\beta_i+\beta_j=3/4\). Thus \(\sum_j\beta_j=3\), saturating the total support bound. Every occupied environment exponent is squarefree of degree three, and the alternate amplitude at each input is exactly the orthogonal projection of the ideal amplitude onto the frequencies admitting an alternate lift. In particular an ideal amplitude that vanishes, including every wrong-data amplitude, has both lifts zero. These conditions give the entire drifted Stinespring amplitude on this torus,
\[
V(D_B(z)e^{-i\epsilon P})|j\rangle
 =z_j^{-1}|j\rangle\otimes\sum_{\nu} z^\nu
 e^{-i\epsilon(2r_j(\nu)-6)}v_\nu,
 \qquad v(z)=\sum_{\nu}z^\nu v_\nu,
\]
where the sum is over squarefree degree-three exponents. With \(A=\sum_{j\in+}\nu_j\), the number of plus queries in the surviving lift is
\[
\begin{array}{c|cc}
 &\nu_j=0 &\nu_j=1\\\hline
j\in+ & A+3 & A-1\\
j\in- & A & A+4
\end{array}
\]
For each input sector, the possible counts in the two columns are disjoint. Each count in the \(\nu_j=1\) column singles out one \(A\). These formulas also apply to the limiting tori because the Parseval calculation uses only the two identities from Section 1 and isometry for every queried unitary.

## 3. Comparing two eigenbases forces coefficients to vanish

Suppose that \(B\) and \(B'\) are two bases available in Section 1, and \(B'\) mixes just a pair \(j,k\) in one sector of \(B\) by a rotation with both coefficients nonzero. On \(z_j=z_k\), the two tori contain the same \(D_B(z)=D_{B'}(z)\) with the same labels on the complement. The drift operator \(P\) is also the same. By Section 2, \(V(D_B(z)e^{-i\epsilon P})\) maps each of the two original basis vectors into itself tensored with an environment vector. The same property holds for the rotated basis. Apply linearity to a rotated vector with both components nonzero. Its environment vector must equal both original environment vectors. This is an identity in \(z,\epsilon\) for the single fixed dilation \(V\).

On this intersection, cancel the common \(z_j^{-1}=z_k^{-1}\) and extract the drift Fourier coefficient of the \(\nu_j=1\) column at each \(A\). This gives
\[
\sum_{\nu:\,|\nu_+|=A}(\nu_j-\nu_k)z^\nu v_\nu=0
\quad\text{when }z_j=z_k .
\]
Indeed the two inputs are in the same sector so the same charge singles out the same \(A\) for each. On the restricted torus the two coordinates merge. The determinant relation in their block has exponent vector \((2,1,1)\) and the other block retains \((1,1,1,1)\). The two block totals are fixed at \(A\) and \(3-A\) within this equation. Equal characters must then have exactly equal merged rows, as a determinant shift changes a block total by four. For the terms selecting exactly one of \(j,k\), the only equal-character pairing swaps the two labels. Let \(\sigma\) denote that swap. Fourier independence implies \(v_\nu=v_{\sigma\nu}\) for each such term.

Now take the coefficient of \(z_jz_k^{-1}\) in \(\|v(z)\|^2=1\) on the original torus. The frequency is nontrivial. No determinant shifts contribute to the coefficient, since the difference of two degree-three exponent block totals has magnitude at most three. With the inner product conjugate-linear in its first argument, the coefficient is
\[
0=\sum_{\mu:\,\mu_j=0,\,\mu_k=1}\langle v_\mu,v_{\sigma\mu}\rangle
 =\sum_{\mu:\,\mu_j=0,\,\mu_k=1}\|v_\mu\|^2 .
\]
So every coefficient selecting exactly one member of the rotated pair vanishes.

## 4. Isolating a pair by a physical Hamiltonian

Work in the sitewise Hadamard basis, so the allowed terms are \(Z_i\) and \(X_iX_{i+1\bmod3}\), and parity is \(Z_0Z_1Z_2\). Take \(B\) to be the computational basis, realized by simple fields \((1,2,4)\). In the following, spin labels are the eigenvalues of the three \(Z_i\).

For \(c\in\{+1,-1\}\), the pair \((+,-,c),(-,+,c)\) lies in sector \(-c\). In \(H_0=Z_0+Z_1+3Z_2\), the energy of the pair is \(E_c=3c\). The two other states in that sector are \((+,+,-c),(-,-,-c)\), with energies \(2-3c,-2-3c\). For a chosen \(c_0\), consider
\[
H(\tau)=H_0+\tau (X_0X_2+X_1X_2)
 +\tau^2\big(Z_0-Z_1+e X_0X_1\big),
 \qquad e=3c_0/8 .
\]
The term linear in \(\tau\) connects each pair member to both other states with amplitude one and has zero restriction to the pair. For an eigenvalue \(E\) near \(E_c\), eliminate the components on the other two states by the Schur complement. If \(D(\tau)\) is their block and \(B_1\) is the \(2\times2\) all-ones cross-coupling matrix, the effective matrix is the direct pair block plus \(\tau^2 B_1(E-D(\tau))^{-1}B_1^\top\). After subtracting \(E_c I\) and dividing by \(\tau^2\), its limit is
\[
\begin{pmatrix}2& e\\ e&-2\end{pmatrix}
+ F_c\begin{pmatrix}1&1\\1&1\end{pmatrix},
\qquad F_c=\frac{1}{6c-2}+\frac{1}{6c+2}=\frac{3c}{8}.
\]
Both limiting matrices have distinct eigenvalues. Their off-diagonal entry is zero in the sector \(c=-c_0\), and is \(3c_0/4\) in the sector \(c=c_0\). The perturbed pair eigenvectors converge to the respective eigenbases of these effective matrices: their components outside the pair tend to zero by the elimination formula, and any limits of their pair projections are orthogonal eigenvectors of the limiting matrix. This also gives simple spectra within each sector for sufficiently small nonzero \(\tau\). The simple states outside the pair converge to the original basis vectors. Thus the limiting basis mixes the selected pair and leaves the other six basis vectors unchanged, up to phases and labels.

Any two distinct computational basis states in the same parity sector differ in precisely two sites. Permute those sites into positions 0 and 1, and if the spins there agree in one state, flip one site by conjugating by its \(X\). These transformations preserve the Hamiltonian promise in this basis, with a spin flip interchanging the parity labels. The construction allows either parity label. Undoing the transformation supplies the required limiting basis for every same-sector pair in \(B\).

By Section 3, any nonzero \(\nu\) coefficient would have to select either all four or none of the four labels in each sector. This is impossible for a squarefree exponent of weight three, contradicting \(\|v(z)\|=1\). This excludes six queries. The [one- and two-query ideal obstruction](THEORY_ODD_CYCLE_THREE_QUERIES.md), the [three-query drift theorem](THEORY_ISING_TRIANGLE_SEQUENTIAL_DRIFT.md), and the [four- and five-query obstruction](THEORY_ISING_TRIANGLE_FOUR_FIVE_DRIFT.md) give the remaining lower bounds.

## Scope, related work, and next step

The result is for a common static parity drift of the same sign and magnitude in each slot, on the full triangle, with deterministic fixed-order queries. Extending the lower bound to longer odd cycles and quantifying the smallest worst-case linear coefficient at six queries remain open. For five sites, the two sector spectra are spinor weights of the two quadratic Majorana blocks. A concrete next step is to write the characters in terms of those Majorana eigenphases and enumerate the distinct parity charges that can alias at degree six. The triangle argument uses its block size and its accessible pair rotations explicitly.

The [EUI preprint and its appendices](https://arxiv.org/html/2506.20570v1) provide the Hamiltonian inversion setting and numerical robustness context. [Odake, Yoshida and Murao, PRL 135, 230603 (2025)](https://doi.org/10.1103/drp2-rzzw) provide differentiation-based lower bounds for transformations of unknown unitaries, including subgroup promises. The present converse uses the common drift response together with compatibility across inequivalent physical eigenbases. The analytic eigenvalue theorem in Section 1 is from [Rellich, *Perturbation Theory of Eigenvalue Problems*](https://books.google.com/books/about/Perturbation_Theory_of_Eigenvalue_Proble.html?id=VjbvAAAAMAAJ).

## Exact checks

Run the command below from the repository root with Python 3. It reconstructs the two effective matrices using exact fractions, checks the symmetry coverage of all 12 pairs, and verifies the lift table and the two character matchings for all 56 squarefree degree-three exponents. The theorem uses the analytic argument above.

~~~bash
python - <<'PY'
from pathlib import Path

source = Path("THEORY_ISING_TRIANGLE_SEVEN_DRIFT.md").read_text()
exec(source.split("~~~python\n", 1)[1].split("\n~~~", 1)[0])
PY
~~~

~~~python
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from math import prod

for target in (1, -1):
    direct = Fraction(3 * target, 8)
    for c in (1, -1):
        pair = ((1, -1, c), (-1, 1, c))
        others = ((1, 1, -c), (-1, -1, -c))
        energies = [x[0] + x[1] + 3*x[2] for x in others]
        cross = [
            [sum(tuple(sorted(i for i in range(3) if x[i] != y[i])) == edge
                 for edge in ((0, 2), (1, 2))) for y in others]
            for x in pair
        ]
        effective = [
            [(pair[i][0] - pair[i][1] if i == j else direct)
             + sum(Fraction(cross[i][k] * cross[j][k], 3*c - energies[k])
                   for k in range(2)) for j in range(2)]
            for i in range(2)
        ]
        shift = Fraction(3*c, 8)
        coupling = Fraction(3*c, 4) if c == target else 0
        assert effective == [[2 + shift, coupling], [coupling, -2 + shift]]
        assert len(set([3*c, *energies])) == 3

spins = list(product((1, -1), repeat=3))
spins.sort(key=prod, reverse=True)
pairs = [(j, k) for j, k in combinations(range(8), 2) if j//4 == k//4]
covered = set()
for c, order, sign in product((1, -1), permutations(range(3)), (1, -1)):
    images = []
    for spin in ((1, -1, c), (-1, 1, c)):
        transformed = (sign * spin[0], spin[1], spin[2])
        images.append(spins.index(tuple(transformed[i] for i in order)))
    covered.add(tuple(sorted(images)))
assert covered == set(pairs)


def canonical(row):
    return tuple(x - min(row[:4]) for x in row[:4]) + tuple(
        x - min(row[4:]) for x in row[4:]
    )


def difference(left, right):
    return tuple(a - b for a, b in zip(left, right))


def swap(row, j, k):
    result = list(row)
    result[j], result[k] = row[k], row[j]
    return tuple(result)


aliases = defaultdict(list)
for labels in combinations_with_replacement(range(8), 6):
    row = tuple(labels.count(i) for i in range(8))
    aliases[canonical(row)].append(sum(row[:4]))

modes = [tuple(int(i in labels) for i in range(8))
         for labels in combinations(range(8), 3)]
units = [tuple(int(i == j) for i in range(8)) for j in range(8)]
for j, unit in enumerate(units):
    preferred_counts, alternate_counts = set(), set()
    for nu in modes:
        plus = sum(nu[:4])
        counts = sorted(aliases[canonical(difference(nu, unit))])
        preferred = plus + 3 if j < 4 else plus
        alternate = plus - 1 if j < 4 else plus + 4
        expected = sorted([preferred, alternate] if nu[j] else [preferred])
        assert counts == expected
        if nu[j]:
            alternate_counts.add(alternate)
        else:
            preferred_counts.add(preferred)
    assert preferred_counts.isdisjoint(alternate_counts)
    assert len(alternate_counts) == 3

for j, k in pairs:
    merged = defaultdict(list)
    for nu in modes:
        if nu[j] != nu[k]:
            coordinates = list(nu)
            coordinates[j] += coordinates[k]
            del coordinates[k]
            merged[sum(nu[:4]), tuple(coordinates)].append(nu)
    assert all(len(group) == 2 and swap(group[0], j, k) == group[1]
               for group in merged.values())
    character = canonical(difference(units[j], units[k]))
    matching = {(left, right) for left, right in product(modes, repeat=2)
                if canonical(difference(right, left)) == character}
    expected = {(nu, swap(nu, j, k)) for nu in modes if nu[j] == 0 and nu[k] == 1}
    assert matching == expected
assert not any(all(nu[j] == nu[k] for j, k in pairs) for nu in modes)
print(f"Exact checks passed for both effective rotations, {len(pairs)} pairs, and {len(modes)} modes.")
~~~
