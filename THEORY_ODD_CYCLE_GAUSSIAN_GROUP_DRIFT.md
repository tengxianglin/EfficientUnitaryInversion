# Sharp six-query drift bound for independent Gaussian parity sectors

Let \(n\ge3\) be odd, \(D=2^{n-1}\), and let \(G=G_+\times G_-\) be two independent copies of \(\mathrm{Spin}(2n)\). Let \(\pi_s\) be the parity-\(s\) half-spin representation of its respective copy. The oracle is \(U(g)=\pi_+(g_+)\oplus\pi_-(g_-)\) on data \(S_+\oplus S_-\), and \(P\) acts by \(s\) on \(S_s\). Under common static drift each oracle call is to \(U(g)e^{-i\epsilon P}\). The ideal target on this group is entrywise conjugation \(\overline{U(g)}\) in the real parity bases used for the physical Ising Hamiltonian. It agrees with inversion on that real-symmetric Hamiltonian promise.

**Theorem.** Among all deterministic fixed-order six-query combs exact at \(\epsilon=0\) on \(G\), the infimum of the worst-case linear diamond error coefficient is
\[
 \max(0,6-8f_n),\qquad
 f_n=1-2\binom{2n}{n}/4^n .
\]
Here the worst case is the supremum over \(g\) of the pointwise slope, with no factor of one half in the diamond norm. Thus the first-order query minimum on this group promise is seven for \(n=3,5,\ldots,19\) and six for all odd \(n\ge21\). At five sites the sharp six-query coefficient is \(31/16\). The same sharp six-query bound holds on the physical Ising family for the fixed parallel encoders that intertwine a joint data and spectator unitary defined below. The five-site physical case for general combs remains open.

## 1. Haar bound for a six-query comb

Denote the normalized Haar measure by \(dg\). A fixed Stinespring realization has output amplitudes that are homogeneous degree-six polynomials in the oracle entries. Group its amplitudes by the plus count \(k\); the corresponding functions of \(g\) are matrix coefficients of \(\pi_+^{\otimes k}\boxtimes\pi_-^{\otimes(6-k)}\). This holds for sequential controls as well, since contracting a product of matrix entries with any fixed controls leaves a linear combination of those entries. The drift factor of that group is \(e^{-i\epsilon(2k-6)}\).

In each copy of \(G_s\), choose the generator of the order-four center whose \(\pi_s\) phase is \(i\). Its eigencharacters separate query counts modulo four, so each center character of an output has at most two charge lifts. On input in sector \(s\) call the lift with the larger own-sector count preferred and the lower one alternate. This choice refers to counts allowed by the center and total degree; a missing amplitude can be set to zero. At any character with just one possible lift use that lift. Let \(a_j(g)=\overline{U(g)}|j\rangle\otimes v(g)\) be the ideal Stinespring output for a normalized input basis state \(j\); the environment vector \(v(g)\) is common to all inputs and pointwise normalized. Since \(v\) can be recovered by contracting \(a_j\) with \(\overline{U(g)}|j\rangle\), it is a finite sum of matrix coefficients. Write \(a_j=b_j+c_j\) with the preferred and alternate contributions. Unitarity for every real drift and orthogonality of center characters give
\[
 1=\|b_j+e^{\pm8i\epsilon}c_j\|_{L^2(G)}^2,\qquad
 \langle a_j,c_j\rangle=\|c_j\|^2=\beta_j.
\]
That norm identity removes the preferred phase in each orthogonal character block. If \(\mathcal P_s\) is the union, over all center characters, of coefficient spaces permitted by the alternate lift on input \(s\), then
\[
 \beta_j\le\|\operatorname{Proj}_{\mathcal P_s}a_j\|^2 .
\]
This follows by Cauchy–Schwarz since \(c_j\) has support only in \(\mathcal P_s\).

The nonzero center classes of \(v\) have preferred counts \((p_+,p_-)\) in \(\{(6,3),(3,6),(5,4),(4,5)\}\), with \(p_s\) the number of own-sector queries on input \(s\). To see this, restrict to any pair of maximal tori, with any fixed conjugations. The [spinor-weight lift lemma](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md#allowed-phase-lifts-through-six-queries) applies. Every occupied ideal environment Fourier mode has \(p_++p_-=9\), with \(3\le p_s\le6\); \(p_s\) depends only on the center character of \(v\) via \(i^{p_s+1}\) on copy \(s\). Every element is in such a pair of tori, so any center class with other counts vanishes on \(G\). For \((p_s,p_{-s})=(6,3)\) all environment torus exponents on copy \(-s\) are zero, as seen by testing input \(s\), whose preferred lift has no calls to copy \(-s\). Applying this on every pair of tori proves the environment class depends only on \(g_s\). Testing input \(-s\) and setting \(g_{-s}=I\) shows this class is in the coefficient space of \(\pi_s^{\otimes3}\), since the only count on copy \(s\) is then three.

The preferred charges on opposite inputs have difference \(2p_+-6-(6-2p_-)=6\) for each environment class. Test the linear channel derivative on \(|i\rangle\langle j|\) for plus input \(i\) and minus input \(j\), and take the output matrix element between their ideal output vectors \(\overline U|i\rangle,\overline U|j\rangle\). The Haar average is \(-i[6-8(\beta_i+\beta_j)]\). Indeed the derivative in each class multiplies the preferred amplitude by its charge times \(-i\), and changes that by \(+8i\) for the plus alternate and \(-8i\) for the minus alternate. The contraction with the ideal outputs gives \(\langle a_k,c_k\rangle=\beta_k\). The test operator has trace norm one, so the worst-case diamond slope is at least
\[
 6-\frac{8}{D}\sum_{j=1}^{2D}\beta_j .
\]

## 2. Dimension formula for the projected ideal amplitude

For each center class of \(v\), upper-bound the alternate projection by ignoring the query constraint on the other copy and retaining the condition on the input's own copy \(G_s\). If \(p_s\ge4\), the allowable own-copy irreducibles are those in \(\pi_s^{\otimes(p_s-4)}\); if \(p_s=3\) there is no alternate. Let \(\mathcal A\) be any such set of irreducibles of \(G_s\). When \(v\) belongs to the coefficient space of an own-copy irrep \(R\) of dimension \(d_R\), the fraction of the ideal amplitude squared that survives the projection, averaged over the \(D\) data basis inputs, is
\[
 F_s(R,\mathcal A)
 =\frac{\dim[(\overline{\pi_s}\otimes R)_{\mathcal A}]}{D\,d_R}.
\]
The numerator includes all isotypic multiplicities in the joint representation. This formula also diagonalizes the quadratic form for an arbitrary \(v\) across the different \(R\) of that copy and holds with any untouched other-copy variables and environment components.

For the proof, first take scalar \(v(g_s)\) and consider the map \(v\mapsto v\overline{\pi_s}\) to matrix-valued \(L^2(G_s)\) with the normalized Hilbert–Schmidt norm. The map is an isometry. The projected norm form is invariant under independent left and right translations of \(v\). Under such a translation, \(v\overline{\pi_s}\) is translated and multiplied by fixed unitary data matrices, which commute with the entrywise coefficient projection and preserve its norm. By Peter–Weyl and Schur's lemma the form is scalar on each coefficient space \(R\boxtimes\bar R\) of the left-right action, with no cross terms. To compute the scalar, average over the \(d_R^2\) orthonormal functions \(\sqrt{d_R}R_{ab}\). Projecting the matrix entries of \(\overline{\pi_s}\otimes R\) retains precisely its \(\mathcal A\)-isotypic part. Its squared Hilbert–Schmidt norm at any \(g_s\) is its dimension. Accounting for the \(1/D\) data normalization and the factors of \(d_R\) gives the displayed fraction. For general \(v\), sum over environment coordinates and integrate the other copy.

## 3. Bounds by center class

We use the multiplicity-free rule for tensoring any irrep with a half-spin representation. In ordinary weight coordinates the half-spin weights are the rows \((\pm1/2)^n\) of a fixed sign parity, with each weight appearing once. If \(\lambda\) is dominant, the highest weights in \(\lambda\otimes\pi_s\) are \(\lambda+w\) over those half-spin weights \(w\) for which \(\lambda+w\) is dominant. This follows from the Weyl character formula: multiplying the alternating numerator for \(\lambda+\rho\) by the invariant half-spin weight sum gives the sum of alternating numerators for \(\lambda+\rho+w\). Each such row is weakly dominant because half-spin weights pair with simple coroots in \(\{-1,0,1\}\). Singular rows vanish and the others are dominant after subtracting \(\rho\). In particular all resulting multiplicities are one.

**Mixed classes \((4,5),(5,4)\).** On the \(p_s=4\) side the alternate uses zero own-sector calls. The trivial rep appears in \(\overline{\pi_s}\otimes R\) only for \(R=\pi_s\), with multiplicity one, giving a fraction at most \(1/D^2\). On the \(p_s=5\) side the alternate uses one own-sector call. By the multiplicity-free rule its contribution is at most \(1/d_R\) when \(\pi_s\) occurs. The center character of \(R\) here is \(i^6=-1\), so \(R\) is nontrivial and \(d_R\ge4\). In fact any nontrivial differential embeds the simple Lie algebra of dimension \(n(2n-1)\ge15\) into the Lie algebra of \(U(d_R)\). Connectedness ensures a nontrivial representation has nontrivial differential. The two sides contribute at most \(1/D^2+1/4\) times the norm squared of the environment class.

**Classes \((6,3),(3,6)\).** Only the \(p_s=6\) side has an alternate. The other copy is trivial in this environment class and \(R\) on copy \(s\) occurs in \(\pi_s^{\otimes3}\) by Section 1. The allowable own-copy irreps are those in \(\pi_s^{\otimes2}\). If \(R=\overline{\pi_s}\), the shared dimension in \(\overline{\pi_s}^{\otimes2}\) and \(\pi_s^{\otimes2}\) is exactly \(D^2-\frac12\binom{2n}{n}\). The [lower odd exterior grades](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md#a-shared-two-spinor-subspace) give shared subspaces of that dimension. The irrep with highest weight twice the highest weight of \(\overline{\pi_s}\) is in its square and absent from \(\pi_s^{\otimes2}\): to double a half-spin weight by summing two half-spin weights requires the identical weight in both slots, and the chirality is opposite. The Weyl dimension of this missing irrep is \(\frac12\binom{2n}{n}\). For highest weight \((1,\ldots,1)\) the Weyl product reduces to \(\prod_{0\le a<b<n}(a+b+2)/(a+b)\), whose factors at each \(b\) multiply to \(2(2b+1)/(b+1)\); the other chirality has the same dimension. This exhausts the complement. The fraction for this spectator irrep is therefore \(f_n\).

For any other \(R\) in the cube, its highest weight has all half-integer coordinates. If all absolute values equal \(1/2\), it is a fundamental half-spin, and the prescribed center character \(i^3\) selects only \(\overline{\pi_s}\). If the absolute values are not all identical, the Weyl orbit has at least \(nD\) elements by signed permutations with even sign changes, so \(d_R\ge nD\). If all absolute values equal \(a\ge3/2\), a simple root at the appropriate end of the type-\(D_n\) diagram decreases the magnitude of two coordinates by one. This weight is present by the root-string rule and lies in a different Weyl orbit. Each of the two orbits has at least \(D\) elements from sign changes alone, so \(d_R\ge2D\). The joint representation \(\overline{\pi_s}\otimes R\) is multiplicity-free. Its allowed dimension is at most \(D^2\), giving \(F_s\le1/2\). For \(n\ge5\), \(f_n\ge65/128>1/2\), so the other cube irreps cannot improve the bound. For \(n=3\) the exact weight calculation in the verification gives a maximum \(1/5\) among the other cube irreps, also below \(f_3=3/8\).

In all classes, the sum of the two projection bounds is at most \(f_n\) times the environment class norm squared. The classes are orthogonal and their norm squares sum to one. This proves \(D^{-1}\sum_j\beta_j\le f_n\) and gives the asserted diamond slope lower bound. For attainment, use the [fixed joint six-query construction](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md). Its intertwiners and invariant states are Gaussian-group identities, so they apply to independent elements of the two copies. For \(f_n<3/4\), use its split encoder alone. The reduced first-order generator is \((6-8f_n)\Pi_+\), giving diamond slope \(6-8f_n\) since the diamond norm of the commutator with a nontrivial projection is one. For \(f_n\ge3/4\) the input-independent mixture cancels the slope exactly. The query lower bound through five already holds on the physical subset. The seven-call deterministic recovery intertwiners also extend to this group.

## 4. Transfer to joint encoders on the physical promise

This corollary concerns physical protocols with a fixed isometry \(E\) from data and a spectator into the six query registers and unused workspace, a fixed inverse decoding of the encoded image, and some fixed spectator state. Assume that at every physical ideal \(U\) the whole joint space satisfies
\[
 (U^{\otimes6}\otimes I)E=E(\bar U\otimes R_U)
\]
for a spectator unitary \(R_U\). The condition is on all joint data/spectator inputs. Input-independent flagged mixtures of these procedures are included.

The physical generators [generate the two independently supported Gaussian Lie algebras](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#why-three-queried-sectors-must-agree). The encoded space is invariant under products of their exponentials, and the recovered joint action stays factored, since the data conjugation map is a representation and products of spectator unitaries are spectator unitaries. The property extends continuously over the generated compact group. Write the total query charge as \(K=\sum_\ell P_\ell\). It commutes with ideal queries, so the drift can be moved before the ideal transversal action. The ideal action preserves the encoded subspace and its orthogonal complement. At first order any leaked component is orthogonal in the decoded scratch registers to the ideal scratch state, and disappears when they are traced out. The recovered first-order action on the joint input is thus obtained by compressing the charge to \(E^\dagger K E\), then applying the factored ideal unitary. After the spectator trace the data slope relative to the ideal conjugation is independent of the ideal oracle. Accordingly the sharp group bound applies to this class on the physical Ising family, with the construction above saturating it.

For a general comb a single physical exponential need only give the correct data channel on its prescribed initial state. Arbitrary products of physical exponentials in one slot are a stronger query promise. To close the physical five-site problem, the next step is to replace the group coefficient projection inequality by one on the union of tori attained by physical five-site bases, or find a six-query construction that exploits precisely that restriction. The group benchmark gives the sharp target \(31/16\) for such a comparison.

The [EUI preprint](https://arxiv.org/html/2506.20570v1) motivates the structured inversion problem and treats conjugation in its supplement. [Odake, Yoshida and Murao](https://doi.org/10.1103/drp2-rzzw) develop differentiation-based query lower bounds for unitary transformations with group promises. The parity drift bound here combines the center count constraint with a projection onto the irreps present in the lower own-sector query lift. For an independent group-theoretic check of the \(\mathrm{Spin}(10)\) spinor square dimensions, see [Slansky](https://doi.org/10.1016/0370-1573(81)90092-2).

## Exact verification

The following Python 3 block uses doubled highest-weight coordinates and rational Weyl products. It enumerates every irrep in the spinor cube at \(n=3,5,7,9\), checks the shared square dimension and the alternate dimension fraction for each cube irrep, and certifies the \(n=3\) exception in the bound for nondual spectators. These are finite exact calculations.

~~~python
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, prod


@lru_cache(maxsize=None)
def weights(n, chirality):
    return tuple(w for w in product((1, -1), repeat=n) if prod(w) == chirality)


def is_dominant(row):
    return (all(a >= b for a, b in zip(row[:-2], row[1:-1]))
            and row[-2] >= abs(row[-1]))


def tensor_spinor(row, chirality):
    candidates = (tuple(a + b for a, b in zip(row, w))
                  for w in weights(len(row), chirality))
    return {highest for highest in candidates if is_dominant(highest)}


@lru_cache(maxsize=None)
def dimension(row):
    n = len(row)
    rho = [2 * (n - i - 1) for i in range(n)]
    shifted = [a + b for a, b in zip(row, rho)]
    value = prod(
        Fraction(shifted[i]**2 - shifted[j]**2, rho[i]**2 - rho[j]**2)
        for i in range(n) for j in range(i + 1, n)
    )
    assert value.denominator == 1 and value > 0
    return value.numerator


for n in (3, 5, 7, 9):
    dim = 2**(n - 1)
    spinor = (1,) * n
    dual = spinor[:-1] + (-1,)
    square = tensor_spinor(spinor, 1)
    dual_square = tensor_spinor(dual, -1)
    assert sum(map(dimension, square)) == sum(map(dimension, dual_square)) == dim**2
    shared = sum(map(dimension, square & dual_square))
    assert shared == dim**2 - comb(2*n, n) // 2
    cube = Counter(row for highest in square for row in tensor_spinor(highest, 1))
    assert sum(dimension(row)*multiplicity for row, multiplicity in cube.items()) == dim**3

    fractions = {}
    for row in cube:
        target_irreps = tensor_spinor(row, -1)
        assert sum(map(dimension, target_irreps)) == dim * dimension(row)
        fractions[row] = Fraction(
            sum(map(dimension, target_irreps & square)), dim * dimension(row)
        )
    two_copy_fraction = Fraction(shared, dim**2)
    assert max(fractions.values()) == fractions[dual] == two_copy_fraction
    nondual_max = max(value for row, value in fractions.items() if row != dual)
    if n == 3:
        assert nondual_max == Fraction(1, 5)
    if n == 5:
        assert sorted(map(dimension, square)) == [10, 120, 126]
        assert 6 - 8 * two_copy_fraction == Fraction(31, 16)
    print(n, sorted(map(dimension, square)), len(cube), two_copy_fraction, nondual_max)

assert 2 * Fraction(comb(38, 19), 4**19) > Fraction(1, 4)
assert 2 * Fraction(comb(42, 21), 4**21) < Fraction(1, 4)
~~~
