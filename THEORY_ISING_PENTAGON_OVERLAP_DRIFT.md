# Four active modes and overlapping physical triples on the Ising pentagon

The [fixed-block construction](THEORY_ODD_CYCLE_ACTIVE_MODE_DRIFT.md) cancels linear parity drift with six queries on any one known three-mode block of the pentagon. It gives a \(3/16\) six-query slope on an enlarged four-active-mode group when the ideal spectator is an inverse-spinor Bell state. Here we remove the spectator restriction on that group and identify a small set of physical limiting tori that already forces the bound for joint-intertwining parallel encoders.

## Results

1. **Four-active-mode group.** In each parity sector independently, let the oracle range over arbitrary \(\mathrm{Spin}(8)\) evolutions on the same designated four modes and an arbitrary phase of the fifth mode. The target is entrywise conjugation, which coincides with inversion on the physical real-symmetric unitaries. For arbitrary deterministic fixed-order six-forward-query combs exact at zero common parity drift, the minimum worst-case linear diamond coefficient is \(3/16\). The ideal environment can be arbitrary. In this model the first-order robust query minimum is seven.
2. **Overlapping physical triples.** Fix four consecutive modes, with triples \(\{0,1,2\}\) and \(\{1,2,3\}\) in that order. Consider the independently phased field-basis torus and the root tori for the three pairs \((0,1),(1,2),(2,3)\), both particle and hole rotations at angle \(\pi/4\), in either parity sector separately. These 13 tori are limits of physical Ising oracles. For fixed parallel encoders that intertwine the whole data–spectator space with a factored ideal unitary, with fixed inverse decoding on the encoded image, the minimum worst-case six-query linear coefficient on this test family is also \(3/16\). The ideal spectator unitary and its initial state can be arbitrary. Input-independent mixtures are included.

The diamond norm has no factor of one half. These results leave the six-or-seven question open for arbitrary combs under the physical five-site exponential promise.

## 1. Haar bound with arbitrary ideal environment

Write \(D=16\) and \(d=8\) for the dimensions of a parity sector and an active half-spin. If the full parity is \(s=\pm1\), the representation on that block is
\[
 \pi_s=(S_s\otimes z)\oplus(S_{-s}\otimes z^{-1}),
\]
where \(S_\sigma\) is an eight-dimensional half-spin of \(\mathrm{Spin}(8)\), and \(z^{t}\) is the spectator-mode character at sign \(t=\pm1\). The active half-spins are self-dual. Each block has the full field torus available. In particular it has an order-four scalar phase \(iI\) independent of the other block. The central lift selection and Haar norm inequality of the [full Gaussian-group proof](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md#1-haar-bound-for-a-six-query-comb) apply. That argument only needs the torus weight support to classify the ideal environment, and conjugacy into the field torus in each compact factor. In particular:
- Each ideal environment center class has preferred own-sector counts \((6,3),(3,6),(5,4)\) or \((4,5)\).
- In a \((6,3)\)-type class, the environment depends only on the copy with \(p_s=6\), and its entries lie in the matrix coefficient space of \(\pi_s^{\otimes3}\). The other copy has no alternate lift.
- The average opposite-sector drift slope bounds the worst-case diamond coefficient from below by \(6-8D^{-1}\sum_j\beta_j\), where \(\beta_j\) is the Haar squared norm of the alternate amplitudes on input \(j\). Each \(\beta_j\) is bounded by the squared norm of the ideal output projected to the alternate coefficient space.

We use the [left–right Haar projection identity](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md#2-dimension-formula-for-the-projected-ideal-amplitude). For a spectator irrep \(R\) on the same copy as the data, the fraction retained by the own-copy projection to a set \(\mathcal A\) of irreps is
\[
 F_s(R,\mathcal A)=\frac{\dim[(\overline{\pi_s}\otimes R)_{\mathcal A}]}{D\dim R}.
\]
The identity applies to this reducible data representation as written. Multiplying by the full unitary matrix \(\overline{\pi_s}\) still commutes with the left–right actions up to constant unitary data factors. Averaging the projected norm of individual matrix coefficients of \(R\) gives the dimension ratio, including all isotypic multiplicities in the tensor product. Alternatively apply the identity to each of the two eight-dimensional data irreps and average. Spectator irreps diagonalize this quadratic form. In bounding a class we can ignore the constraint on the other copy.

### The \((6,3)\) classes

For the copy with \(p_s=6\), write the spectator irrep as \(R=R_0\otimes z^r\), with \(R_0\) an active irrep from the spinor cube and \(r=\pm1,\pm3\). An incoming data charge \(t=\pm1\) contributes target charge \(r-t\); the two-query alternate can carry charge \(2,0,-2\).

If \(|r|=3\), at most one of the two equally sized data blocks can contribute. This bounds \(F_s\) by \(1/2\).

For \(r=\pm1\), the \(\mathrm{Spin}(8)\) center character of \(R_0\) is that of \(S_{-sr}\). Indeed the cube has two tag contributions \(r\) and one tag \(-r\), and the active center characters have order two. With \(R_0=S_{-sr}\), the data block \(t=r\) has mixed active chirality and charge zero. Its full dimension \(d^2=64\) occurs in the two-query representation. The block \(t=-r\) has two equal active chiralities \(S_{-sr}\) and charge \(2r\); the two queries at that charge have chirality \(S_{sr}\). The two squares share dimension \(29\), the scalar plus the adjoint, as in the [fixed Bell-spectator calculation](THEORY_ODD_CYCLE_ACTIVE_MODE_DRIFT.md#3-four-active-modes-on-the-pentagon). This gives \(F_s=(64+29)/(16\cdot8)=93/128\).

Any other \(R_0\) in this center class has \(\dim R_0\ge 2d=16\). Its highest weight is spinorial, with half-integer coordinates. If its coordinate magnitudes differ, the orbit under permutations and even sign changes has at least \(4d\) weights. Equal magnitudes \(1/2\) would give one of the fundamental half-spins, and only \(S_{-sr}\) has the required center character. For equal magnitudes at least \(3/2\), a simple-root string at the corresponding spin node gives a second Weyl orbit with at least \(d\) weights, in addition to the first \(d\). The contribution to the numerator is at most \(2d^2=128\). In fact each half-spin times \(R_0\) is multiplicity-free by the minuscule rule. At charge zero the query support comes from a mixed product of dimension \(d^2\) (either slot order gives the same support). At charge \(2r\) it comes from a same-chirality square of dimension \(d^2\). The two target charges are distinct. Consequently \(F_s\le 128/(16\dim R_0)\le1/2\). Both \((6,3)\)-type classes therefore have alternate bound \(93/128\).

### The \((4,5)\) classes

For \(p_s=4\) only the trivial representation is available in the own-copy alternate. It can occur in \(\bar\pi_s\otimes R\) only if \(R\) is one of the two distinct eight-dimensional data irreps. The contribution is at most \(1/(16\cdot 8)\).

For \(p_s=5\), an own-copy alternate uses one query. If \(R_0\) is nontrivial, multiplicity freedom for each active data half-spin gives a numerator at most \(16\), since each input tag fixes at most one output tag \(r-t\). Here \(\dim R_0\ge4\) already follows from simplicity and \(\dim\mathfrak{so}(8)=28\), so the contribution is at most \(1/4\). If \(R_0\) is trivial, matching the same active chirality requires the output tag to equal the input tag. Thus \(r=2t\), which is possible for at most one input tag. This gives contribution at most \(1/2\). The sum over the two copies is at most \(1/2+1/128<93/128\).

As the center-class environment norm squares sum to one, the Haar inequality gives \(D^{-1}\sum_j\beta_j\le 93/128\) and a slope of at least \(3/16\). The [unmixed four-active split encoder](THEORY_ODD_CYCLE_ACTIVE_MODE_DRIFT.md#3-four-active-modes-on-the-pentagon) attains the bound and works even with a full independent Gaussian group on the minus side. The all-sector field torus rules out up to five calls for first-order suppression, and the [seven-query Gaussian recovery](THEORY_ODD_CYCLE_DETERMINISTIC_RECOVERY.md) supplies the matching upper bound.

## 2. A test on two overlapping triples

The [physical root construction](THEORY_ODD_CYCLE_PHYSICAL_ROOT_TORI.md) allows independent one-sector rotations in either of the two occupancy types. The 13 selected tori generate the four-active-mode group in both parity sectors. To see this, work with real anti-Hermitian Majorana bilinears \(a_i b_i\) from the field torus. Rotating a pair \(i,j\) by \(\pi/4\) simultaneously in the \(a\) and \(b\) modes adds the off-diagonal generator \(a_i b_j+a_j b_i\) to the span after removing diagonal terms. The particle–hole rotation gives the relative minus combination. A local endpoint flip changes one of the relative signs, as both Majoranas on intervening sites and the \(b\) Majorana on the flipped site change signs in field-basis coordinates. The span then contains \(a_i b_j\) and \(a_j b_i\) separately. Together with the diagonal edges, the three selected pairs connect the eight active Majorana indices. The relation \([\gamma_i\gamma_j,\gamma_j\gamma_k]=2\gamma_i\gamma_k\) generates all active bilinears from this connected graph. The spectator bilinear remains independent. The induction works separately in both physical parity sectors by fixing the other sector's phases at the identity. Conversely every selected torus belongs to that group.

For a fixed joint-intertwining encoder \(E\), the ideal action on the whole encoded image takes the form \((U^{\otimes6}\otimes I)E=E(\bar U\otimes R_U)\) with \(R_U\) unitary. Exact intertwining on the test tori extends to their generated group by multiplying these identities and using continuity. The first-order data channel relative to the ideal target is independent of the ideal oracle: the common charge \(K=\sum_{\ell=1}^6P_\ell\) commutes with the ideal slot action. The derivative compresses to \(E^\dagger K E\) on the code, with leaked terms orthogonal to the ideal scratch state after fixed inverse decoding, as in the [joint-encoder transfer argument](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md#4-transfer-to-joint-encoders-on-the-physical-promise). Thus the group lower bound applies already on the test family. The same split encoder attains the slope there.

The transfer step here requires whole-space joint intertwining. A general fixed-order circuit on one physical oracle at a time can have environment amplitudes that do not compose in this way. The next test is to impose pointwise isometry and derivative identities on all 13 tori for a single polynomial dilation, allowing general output environment amplitudes.

The [EUI preprint and Appendix B](https://arxiv.org/html/2506.20570v1) give the physical setting and robustness context. [Odake, Yoshida and Murao](https://arxiv.org/abs/2405.07625) and [Grinko et al.](https://arxiv.org/abs/2510.07100) give related frameworks for group promises and symmetric combs. Here the two-group Haar calculation isolates the spectator restriction, and the physical transfer uses generation only for the class whose joint encoded image is invariant.

## Exact verification

The Python 3 block enumerates the spinor-square and spinor-cube supports by active highest weight and spectator charge. It checks the maximum alternate fraction for each charge in both sectors. It also checks the Majorana commutator closure for the selected pairs.

~~~python
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import prod


@lru_cache(maxsize=None)
def spinor_weights(chirality):
    return tuple(w for w in product((1, -1), repeat=4) if prod(w) == chirality)


@lru_cache(maxsize=None)
def tensor_spinor(row, chirality):
    candidates = (tuple(a + b for a, b in zip(row, w)) for w in spinor_weights(chirality))
    return {w for w in candidates if w[0] >= w[1] >= w[2] >= abs(w[3])}


@lru_cache(maxsize=None)
def dimension(row):
    rho = (6, 4, 2, 0)
    shifted = tuple(a + b for a, b in zip(row, rho))
    value = prod(
        Fraction(shifted[i]**2 - shifted[j]**2, rho[i]**2 - rho[j]**2)
        for i in range(4) for j in range(i + 1, 4)
    )
    assert value > 0 and value.denominator == 1
    return value.numerator


def verify_cube(sector):
    states = {(0, (0, 0, 0, 0))}
    for _ in range(2):
        states = {
            (r + t, row) for r, weight in states for t in (1, -1)
            for row in tensor_spinor(weight, sector * t)
        }
    square = states
    cube = {
        (r + t, row) for r, weight in square for t in (1, -1)
        for row in tensor_spinor(weight, sector * t)
    }
    outcomes = defaultdict(list)
    for r, weight in cube:
        numerator = sum(
            dimension(row) for t in (1, -1)
            for row in tensor_spinor(weight, sector * t)
            if (r - t, row) in square
        )
        outcomes[r].append((Fraction(numerator, 16 * dimension(weight)), dimension(weight)))

    maxima = {}
    for r, data in sorted(outcomes.items()):
        assert len(data) == 4
        best = max(fraction for fraction, _ in data)
        assert best == (Fraction(93, 128) if abs(r) == 1 else Fraction(1, 2))
        assert [dim for fraction, dim in data if fraction == best] == [8]
        maxima[r] = best
    assert 6 - 8 * max(maxima.values()) == Fraction(3, 16)
    print(f"Sector {sector:+}: {maxima}")


def verify_root_graph():
    active_pairs = ((0, 1), (1, 2), (2, 3))
    # Majorana labels 2*i and 2*i+1 are a_i and b_i.
    edges = {frozenset((2*i, 2*i + 1)) for i in range(5)}
    for i, j in active_pairs:
        edges.update((frozenset((2*i, 2*j + 1)), frozenset((2*j, 2*i + 1))))

    while True:
        generated = {u ^ v for u, v in combinations(edges, 2) if len(u & v) == 1}
        if generated <= edges:
            break
        edges.update(generated)
    expected = {frozenset(pair) for pair in combinations(range(8), 2)}
    expected.add(frozenset((8, 9)))
    assert edges == expected
    print(f"{1 + len(active_pairs)*2*2} tori generate {len(edges)} bilinears per sector.")


for parity in (1, -1):
    verify_cube(parity)
verify_root_graph()
~~~
