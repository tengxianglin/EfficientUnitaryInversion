# Parity-drift lower bounds for fixed-order inversion on odd Ising cycles

Let \(n\ge3\) be odd and \(H=\sum_j h_j X_j+\sum_j J_j Z_j Z_{j+1\bmod n}\), with all coefficients real and independently tunable. Put \(P=\prod_j X_j\). A deterministic circuit makes \(m\) unconditional forward calls to \(W_\epsilon(H)=e^{-i(H+\epsilon P)}\), with arbitrary finite memory, parameter-independent controls and measurements, and a discarded environment. Assume that its data channel \(\Phi_{H,0}\) is exactly \(\operatorname{Ad}_{e^{iH}}\) for every \(H\). Write \(D=2^{n-1}\), and use the diamond norm without a factor of one half.

**Theorem.** At \(m=3\), for every \(H,\epsilon\), the data channel is \(\operatorname{Ad}_{e^{iH}e^{-3i\epsilon P}}\), with diamond error \(2|\sin(3\epsilon)|\). At \(m=4,5\) the worst-case linear diamond error coefficients are at least \(6-8/D\) and \(2\), respectively, where the worst case is the supremum over \(H\) of the pointwise coefficient. Thus first-order suppression takes at least six calls at every odd length. The [deterministic seven-call recovery](THEORY_ODD_CYCLE_DETERMINISTIC_RECOVERY.md) works at every odd length. A six-query construction on a fixed, known eigenbasis torus shows that a single such torus cannot raise the bound to seven. At \(n\ge5\), a six-query protocol suppressing the first order must place at least half its ideal environment Fourier norm on exponents given by the negatives of single spinor weights. The [full triangle minimum is seven](THEORY_ISING_TRIANGLE_SEVEN_DRIFT.md).

## Independent Majorana eigenphases on a physical ray

Use the [quadratic Majorana representation](THEORY_ODD_CYCLE_THREE_QUERIES.md#quadratic-representation-in-the-two-sectors). In sector \(s\) the Hamiltonian is the restriction of \(i\sum_{ab}(K_s)_{ab}a_a b_b\); the support of the real matrix \(K_s\) is diagonal plus a cyclic shift and its wrap entry has opposite signs for the two sectors. Work near positive, distinct fields with all edge couplings small so that \(\det K_s>0\). Oriented singular-vector bases diagonalize the quadratic forms with positive singular values \(\lambda_{s,i}\) labelled continuously by the fields. The two orthogonal transformations have determinant \(+1\) and preserve the parity product of the Majoranas. Since each \(ia_i b_i\) has eigenvalues \(\pm1\), the sector's energies are \(\lambda_s\cdot w\) for
\[
W_s=\{w\in\{-1,1\}^n:\ \prod_i w_i=s\}.
\]

The \(2n\) positive singular values are jointly rationally independent on a dense subset of a connected open box around simple positive fields and zero couplings. Here is a proof ruling out each nonzero candidate relation as an analytic identity on that box. At zero couplings, the two boundary-sign spectra both reduce to the freely varying fields \(h_i\), so the coefficients on the two sectors must be negatives of each other. To test their differences, differentiate at zero wrap coupling \(J_{n-1}\) with the interior couplings nonzero. For \(p_s(x)=\det(xI-K_s K_s^\top)\), every coefficient except the constant depends only on the squared matrix entries. Indeed Cauchy–Binet expresses these coefficients as sums of squares of proper minors of \(K_s\). The bipartite support graph is a \(2n\)-cycle. A proper induced subgraph is a forest and has at most one perfect matching, since two distinct matchings would make an alternating cycle. For the full determinant, the two matchings instead give \(\det K_s=\prod_i h_i+s\eta\prod_i J_i\) for a fixed sign \(\eta\). At zero wrap coupling, the two \(p_s\) coincide, and their derivatives with respect to that coupling are opposite nonzero constants in \(x\). This constant is nonzero for nonzero interior couplings and positive fields.

By implicit differentiation of the roots \(\lambda_{s,i}^2\), any putative identity \(\sum_i u_i(\lambda_{+,i}-\lambda_{-,i})=0\) gives, after removing a common nonzero factor,
\[
\sum_i \frac{u_i}{\lambda_i\prod_{j\ne i}(\lambda_i^2-\lambda_j^2)}=0
\]
for the common cut-chain singular values \(\lambda_i\). Let the interior couplings tend to zero to replace \(\lambda_i\) by \(h_i\). The resulting rational identity holds on an open set of distinct positive fields. After clearing denominators it holds wherever the denominators are nonzero. Multiply by \(h_i\) and send that field to zero holding the other fields positive and distinct, to obtain \(u_i=0\). This rules out every nontrivial relation. The square roots of the simple positive eigenvalues are real analytic on the box, so the countable union of zero sets of nonzero integer relations has dense complement by the Baire category theorem.

For one such \(H\), the ray \(tH\) fills densely the two independent tori of Majorana eigenphases \(\theta_+,\theta_-\in(\mathbb R/2\pi)^n\). In its fixed eigenbasis the ideal diagonal oracle has eigenvalues \(e^{-i w\cdot\theta_s}\) on input \((s,w)\). Any channel identity on the ray, including ideal inversion or zero first-order drift, extends continuously to that torus. Below the Fourier label of \(e^{-i x\cdot\theta_+-i y\cdot\theta_-}\) is written \(\nu=(x,y)\).

## Allowed phase lifts through six queries

A fixed Stinespring implementation gives an isometry polynomial of degree \(m\) in the oracle entries. On the torus a path using \(k\) plus labels and \(m-k\) minus labels has frequency in \(S_+(k)\times S_-(m-k)\), where \(S_s(k)\) is the set of sums of \(k\) weights in \(W_s\) and \(S_s(0)=\{0\}\). Its drift factor is \(e^{-i\epsilon(2k-m)}\). Aggregate all paths at a given Fourier frequency and count into one environment/data amplitude. For a fixed frequency, the query count in either sector is unique modulo four: the sum of the coordinates of each weight is \(c_s\bmod4\), with \(c_+=n,\ c_-=n-2\), both units modulo four. At \(m\le6\) there are at most two counts per frequency, separated by four.

Ideal inversion on the torus implies that the Stinespring output on input \((s,w)\) is the ideal inverse phase times the same normalized environment vector \(v(\theta)\) for all inputs. Write \(v(\theta)\) as a finite Fourier series with coefficients \(v_\nu\), so \(\sum_\nu\|v_\nu\|^2=1\). For each coefficient \(v_\nu\ne0\), write \(x_s\) for its sector-\(s\) row. On input \((s,w)\) the output character has sector rows \(x_s-w,x_{-s}\).

Let \(p_s\in\{3,4,5,6\}\) be congruent to \(c_s^{-1}\sum_i (x_s)_i-1\bmod4\). For each \(s\) at least one input in that sector needs at least \(p_s\) calls in its own sector. To prove this, it suffices to rule out that all \(w\in W_s\) have \(x_s-w\in S_s(k)\) for any \(k=0,1,2\).
- At \(k=0\), this would require every \(w=x_s\).
- At \(k=1\), it would give \(x_s-W_s=W_s\). Averaging the weights gives \(x_s=0\), but \(-W_s=W_{-s}\) as \(n\) is odd.
- At \(k=2\), every \(x_s-w\) would be an even row with coordinates of magnitude at most two. Each coordinate of \(w\) has both signs as \(w\) varies, so \(x_s\in\{-1,1\}^n\). Its coordinate sum is \(3c_s\equiv-c_s=c_{-s}\bmod4\), implying \(x_s\in W_{-s}\). Choose \(w=-x_s\in W_s\). The row \(x_s-w=2x_s\) can be a sum of two sign rows only if both are \(x_s\), which is unavailable in \(W_s\).

Since \(m\le6\), that input needs exactly \(p_s\), so \(p_s\le m\) and \(x_{-s}\in S_{-s}(m-p_s)\). In fact \(p_s\) is available on every input \((s,w)\): any lower lift uses \(p_s-4\) own-sector calls, to which one can append a zero sum of four weights. To construct this zero sum, express \(-u\) for any \(u\in W_s\) as a sum of three weights in \(W_s\). Start the three rows at \(-u\), partition the \(n\) coordinates into three odd subsets, and flip one subset in each row. The rows now have parity \(s\) and their sum is \(-u\). Add \(u\). A lower lift with count \(p_s-4\) therefore always coexists with the larger lift. The residues also imply \(p_++p_-\equiv m-1\bmod4\), using any plus input to infer the total residue of the common environment row. Since \(6\le p_++p_-\le2m\), for \(3\le m\le6\) the sum is \(m+3\).

For an ideal output amplitude choose the lift with \(p_s\) calls to the input's own sector as the preferred one. The other is available only if \(x_s-w\in S_s(p_s-4)\) with \(p_s\ge4\). It is then available, since the opposite block can append four zero-sum weights. Off-ideal frequencies also have at most two lifts, and we always prefer the higher own-sector count when both exist. For the same \(\nu\) the two opposite-sector preferred charges have difference \(2p_+-m-(m-2p_-)=6\).

## Norm bound and drift response

For a fixed input \(j\), collect preferred and alternate amplitudes over output Fourier labels and over both data and environment into vectors \(b_j,c_j\), respectively. The ideal amplitude collection is \(a_j=b_j+c_j\). Haar Parseval and isometry for every drift phase give
\[
1=\|b_j+e^{\pm 8i\epsilon}c_j\|^2,\qquad
\langle a_j,c_j\rangle=\|c_j\|^2=\beta_j .
\]
Here the preferred phase has been removed separately at each frequency and the sign is constant for the input sector. By Cauchy–Schwarz on the projection to frequencies admitting a second lift,
\[
\beta_j\le \sum_{\nu:\,j\ {\rm admits\ an\ alternate\ at}\ \nu}\|v_\nu\|^2 .
\]
The ideal phase-corrected channel coherence between a plus input \(i\) and a minus input \(j\), differentiated and Haar-averaged, is \(-i[6-8(\beta_i+\beta_j)]\). The preferred charge difference is six, and switching to the other lift changes the charge by \(-8\) on plus inputs and \(+8\) on minus inputs. Thus the supremum of the linear diamond coefficient on the physical ray is at least \(6-8D^{-1}\sum_j\beta_j\), by testing opposite-sector coherences (input operators of trace norm one), averaging over the \(D^2\) pairs, and using continuity and ray density.

If \(p_s=4\) the alternate has zero own-sector queries and is available for at most one input. If \(p_s=5\), it is available only if both \(w\) and \(x_s-w\) lie in \(W_s\). This is impossible for \(x_s=0\); otherwise at least one coordinate has \(x_s=\pm2\) and pins the input's sign there. Its availability is therefore at most \(D/2\). At \(m=4\) the two \(p_s\) values are 3 and 4; at \(m=5\) they are 3 and 5 or both 4. Thus \(\sum_j\beta_j\le1,D/2\) respectively, proving the stated bounds. The [ideal inversion lower bound](THEORY_ODD_CYCLE_THREE_QUERIES.md) already excludes fewer than three calls.

At \(m=3\) the preferred same-sector count is three in both sectors and each output frequency has a single count, so there are no hidden wrong-data terms at nonzero \(\epsilon\). The output is exactly the ideal inverse times \(e^{-3i\epsilon P}\), at every \(H\) from the dense subset of the open box. For each real \(\epsilon\) both channels are analytic in the \(2n\) real parameters (the oracle is a matrix exponential and the circuit is fixed). By continuity and the analytic identity theorem equality holds throughout the full promise. The exact norm follows from the [two-sector calculation](THEORY_ODD_CYCLE_PARALLEL_DRIFT.md#exact-drift-response-and-a-seven-query-construction).

## What six queries can do on one torus

For \(m=6\), the \(p_s\) pairs are \((4,5),(5,4),(3,6),(6,3)\). In the last two cases a row with \(p_s=6\) can admit an alternate on at most \(D/2\) inputs if any coordinate has magnitude \(\ge3\): the condition \(|(x_s)_i-w_i|\le2\) pins at least one input sign or is impossible. Otherwise every coordinate of \(x_s\) is \(\pm1\) by its query-count parity, and the congruence of its coordinate sum implies \(x_s\in W_{-s}=-W_s\). The opposite row is zero since a preferred \(p_s=6\) input made no calls in that block. These are the only exponents with more than \(D/2+1\) eligible inputs. Each such exponent \((-u,0)\) in sector \(s\), \(u\in W_s\), has exactly \(D-1\) eligible inputs. Indeed \(w=u\) is impossible in \(S_s(2)\) by the argument for \(2x_s\) above. For \(w\ne u\), the vector \(-u-w\) has entries \(\pm2\) where \(u,w\) agree and zero elsewhere. On the zero entries, choose the two summands to have opposite signs. There are a positive even number of these entries, so the two summands have the same product and one free sign fixes that product to \(s\). This yields a two-query lift for precisely those inputs.

If the channel derivative vanishes, then \(\sum_j\beta_j=3D/4\). Writing \(\rho\) for the Fourier norm squared on the exponents formed by negating one weight in its own sector and taking zero in the other, the eligibility bound gives
\[
3D/4\ \le\ (D-1)\rho+(D/2+1)(1-\rho).
\]
For \(n\ge5\) this implies \(\rho\ge1/2\) on every independently phased torus of a physical Hamiltonian. The same condition holds for limits of such tori by continuity of the polynomial coefficients, with phase-coordinate labels carried along.

A six-query circuit can satisfy the first-order condition on any one torus with a **known fixed eigenbasis**. Choose \(u\in W_+\) uniformly and use ideal spectator exponent \(x_+=-u,\ x_-=0\). On a plus input \(w\ne u\), select the two-plus/four-minus lift with probability \(3D/[4(D-1)]\), implemented by an input-independent random flag with alternate routing only when eligible. Otherwise use six plus calls, which is possible since \(-u\) and \(-w\) are each sums of three plus weights. The two-plus lift uses the decomposition above and four minus weights summing to zero. On every minus input use three plus weights for \(-u\) and three minus weights for \(-w\). All routing within a random branch is coherent on the data input and returns scratch registers, since the oracle is diagonal in the known basis. Each branch implements the same ideal inverse channel with a common spectator phase. The probability of using the alternate on any plus input is \(3/4\), so its mean charge is \((3/4)(-2)+(1/4)(6)=0\). Each minus input has charge zero. Averaging gives zero derivative on every data coherence. Thus six is optimal on this torus for the stated objective.

## Scope and next step

The argument gives a single-ray lower bound for arbitrary deterministic fixed-order combs on every odd ring. [A fixed six-query recovery](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md) attains this lower bound for every odd \(n\ge21\). The full noncommuting promise has a six-or-seven gap for odd \(5\le n\le19\). A next step is to constrain the forced single-weight environment exponents across physically accessible basis rotations. A proof based only on the charge counts in one known eigenbasis would also have to admit the explicit torus circuit above.

The [EUI manuscript](https://arxiv.org/html/2506.20570v1) discusses odd-cycle inversion and averages Choi fidelities under random support-breaking errors in Appendix B. The common parity-drift diamond objective here concerns a specific systematic error direction. The quadratic Ising reduction is standard, as in [Pfeuty, Ann. Phys. 57, 79–90 (1970)](https://doi.org/10.1016/0003-4916(70)90270-8). [Odake, Yoshida and Murao, PRL 135, 230603 (2025)](https://doi.org/10.1103/drp2-rzzw) use differentiation for lower bounds on unitary transformations. Here the independent eigenphase directions follow from the cut-chain polynomial, and a Haar normalization constraint bounds the response to parity drift.

## Exact verification at three and five sites

Run this block with Python 3 and SymPy. It checks the characteristic-polynomial identity for explicit interior couplings and a symbolic wrap coupling, then enumerates all compatible ideal environment characters and lift counts at \(m=3,4,5,6\). These finite checks support the algebra above.

~~~python
from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import prod

import sympy as sp


def verify_polynomial(n):
    fields = tuple(range(2, n + 2))
    edges = tuple(range(3, n + 2))
    z, wrap = sp.symbols("z wrap")
    base = sp.diag(*fields)
    for i, edge in enumerate(edges):
        base[i + 1, i] = edge
    polynomials = []
    for sign in (1, -1):
        matrix = base.copy()
        matrix[0, n - 1] = sign * wrap
        polynomials.append((matrix * matrix.T).charpoly(z).as_expr())
    difference = sp.expand(polynomials[0] - polynomials[1])
    assert difference == (-1)**n * 4 * wrap * prod(fields) * prod(edges)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def verify_aliases(n):
    zero = (0,) * n
    weights = {s: set() for s in (1, -1)}
    for row in product((-1, 1), repeat=n):
        weights[prod(row)].add(row)
    sums = {}
    counts = {}
    for s, rows in weights.items():
        sums[s] = [{zero}]
        for _ in range(6):
            sums[s].append({add(x, w) for x in sums[s][-1] for w in rows})
        counts[s] = defaultdict(set)
        for k, level in enumerate(sums[s]):
            for x in level:
                counts[s][x].add(k)

    inputs = [(s, w) for s in weights for w in sorted(weights[s])]
    first = inputs[0][1]
    dim = len(weights[1])
    expected = {3: (1, 8, 36, 120), 5: (1, 32, 468, 4256)}

    for m in range(3, 7):
        characters = {(add(x, first), y) for k in range(m + 1)
                      for x in sums[1][k] for y in sums[-1][m - k]}
        common = 0
        special_count = 0
        max_eligible = 0
        for x, y in characters:
            eligible = 0
            preferred = {}
            for s, w in inputs:
                a, b = (subtract(x, w), y) if s == 1 else (x, subtract(y, w))
                lifts = [
                    k for k in counts[1].get(a, ())
                    if m - k in counts[-1].get(b, ())
                ]
                if not lifts:
                    break
                own = max(lifts) if s == 1 else m - min(lifts)
                assert preferred.setdefault(s, own) == own
                if len(lifts) > 1:
                    assert len(lifts) == 2 and max(lifts) - min(lifts) == 4
                    eligible += 1
            else:
                common += 1
                assert sum(preferred.values()) == m + 3
                max_eligible = max(max_eligible, eligible)
                if m == 6:
                    special = (x in weights[-1] and y == zero) or (
                        y in weights[1] and x == zero
                    )
                    if special:
                        special_count += 1
                        assert eligible == dim - 1
                    else:
                        assert eligible <= dim // 2 + 1

        assert common == expected[n][m - 3]
        assert max_eligible == {3: 0, 4: 1, 5: dim // 2, 6: dim - 1}[m]
        if m == 6:
            assert special_count == 2 * dim
            alternate = Fraction(3 * dim, 4 * (dim - 1))
            assert 0 < alternate <= 1
            assert 6 - 8 * Fraction(dim - 1, dim) * alternate == 0
        print(n, m, common, max_eligible, special_count)


print("sites queries compatible_characters max_alternate_inputs single_weight_characters")
for size in (3, 5):
    verify_polynomial(size)
    verify_aliases(size)
~~~
