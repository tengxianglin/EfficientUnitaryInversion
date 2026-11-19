# Complement depolarization strictly lowers the full physical minimax error

The [edge-oracle converse](THEORY_ODD_CYCLE_EDGE_ORACLE_CONVERSE.md) rules out a minimax improvement within diagonal complementary-syndrome corrections. A full logical Pauli twirl leaves that class. A constant-probability identity for the physical program complement makes its full-family performance exactly calculable.

Let \(n\ge21\) be odd, \(D=2^{n-1}\), \(r=fD^2\), \(p=3/(4f)\), and
\[
 f=1-\frac{2\binom{2n}{n}}{4^n},\quad
 S=\frac12\sum_{k=0}^n\binom nk^2a_k^2-r^2,\quad
 M=r(D^2-r)-S,\quad \beta=M/D^4>0,
\]
where
\(a_k=\sum_{\ell<n,\ \ell\ {\rm odd}}\sum_j(-1)^j\binom{2k}{j}\binom{2n-2k}{\ell-j}\).
Write \(g=\frac14e^{-6i\epsilon}+\frac34e^{2i\epsilon}\).

**Recovery.** Use the same coherent six-query encoder and fair choice of program parity. On the ideal split flag, preserve the physical ideal-program subspace \(\mathcal S\) coherently. On its complement, discard the selected-parity data and replace it by \(I/D\). Equivalently apply a uniform full logical Pauli twirl there. Leave the orthogonal flag branch unchanged, as in the [selective recovery](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md). The program complement measurement is fixed. It suffices to measure the protected/complementary subspaces; the individual Bell labels need not be read.

**Theorem.** This recovery implements exact ideal inversion and zero first-order common parity-drift error on every physical Ising Hamiltonian. Its exact worst-case diamond error is
\[
 \sup_H{\cal E}^{\rm depol}_{H}(\epsilon)
 =|1-g|+\frac32(1-f)\sin^2(4\epsilon)
       -\frac{9M}{8r^2D^2}\sin^2(4\epsilon).
\]
The identity oracle attains the bound, as does the edge oracle \(H=(\pi/2)Z_0Z_1\). Thus the coefficient of the full physical worst-case quadratic error decreases by \(18M/(r^2D^2)\) relative to the old balanced decoder. At \(n=21\) the decrease is about \(3.55345\times10^{-12}\). This is a strict full-family minimax improvement with a dimension-suppressed guarantee, rather than a practically large reduction. Optimality across all recoveries or encoders remains open.

The new decoder is pointwise no worse than the old one. Its exact norm at individual non-Pauli oracles may be smaller than the displayed supremum. It is not asserted to dominate the earlier field-optimized decoder pointwise; that decoder gives a larger gain on its narrower field-Pauli test family.

## 1. Constant complementary probability

Let \(V=\bar U_+\) be the intended inverse in the selected plus sector, and \(Q\) the shared two-program Bell projector of the coherent encoder. With a Bell program \(\Phi_{ER}\), define the ideal shared-projector amplitudes
\[
 L_R=(I\otimes\langle R|_{ER})(V\otimes V\otimes I)
          (Q\otimes I)(I\otimes|\Phi\rangle_{ER}).
\]
Here \(R\) ranges over Pauli Bell program labels. Let \(\Pi_{\mathcal S^\perp}\) be the projector onto the complementary physical program space. We claim
\[
 \sum_{R\notin\mathcal S}L_R^\dagger L_R=\beta I
 \quad\text{for every physical }H .
\]

First take \(V\) diagonal in the field-occupation basis, with arbitrary independent mode phases. The [shared spinor-square projector](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md#a-shared-two-spinor-subspace) commutes with \(V\otimes V\). A nonzero matrix coefficient \(Q_{y,e;x,t}\) must therefore satisfy equality of the two summed occupation-weight rows. If \(F\) is the set of sites where \(y\) differs from \(x\), then \(F\) has even size. On those sites the program output row is forced to equal \(x\), and its purifier/input row is forced to be opposite \(x\); on other sites the program and purifier rows agree.

The protected program projector preserves each program bit-flip support \(F\). Within that support its Pauli Bell labels have exactly half their single Majoranas of type \(a\) and half of type \(b\). The empty/double choices on all other sites are unrestricted. Summing those diagonal Pauli factors shows that the protected projector has no matrix elements between two program matrix units with different occupation rows on the complement of \(F\). Its diagonal entries in the matrix-unit basis are
\[
 \kappa_F=\binom{|F|}{|F|/2}/2^{|F|}.
\]
For \(F=\varnothing\), this value is one. This also follows by the ratio of balanced labels to all labels with that bit-flip support:
\(\binom{|F|}{|F|/2}2^{n-|F|-1}/D=\kappa_F\).
The sum over unrestricted empty/double factors gives the claimed matrix-element zeros, including the parity constraint. The assumption that \(n\) is odd leaves at least one unflipped site whenever \(F\ne\varnothing\).

For a fixed input row \(x\) and output row \(y\), all program amplitudes forced by \(Q\) have the same row on \(F\). On their support, the quadratic form of the protected projector is exactly \(\kappa_F\) times the norm. Multiplication by arbitrary diagonal phases therefore does not change the complementary probability. Matrix elements between different data inputs vanish because, at a common data output, their program bit-flip supports differ and the protected projector preserves those supports. Hence the data effect is diagonal and phase independent. At \(V=I\), the Pauli Bell expansion of \(Q\) gives the effect explicitly as
\[
 D^{-4}\sum_{P\notin\mathcal S}a_P^2\,I=M D^{-4}I.
\]
This proves the identity for all diagonal mode phases.

For a general physical \(V\), the bipartite Majorana coefficient matrix has a real signed SVD. The diagonalizing frame lies in \(\mathrm{SO}(n)\times\mathrm{SO}(n)\), acting separately on the \(a\) and \(b\) frames. Its spin representation \(G\) is real orthogonal in the field parity basis, since the \(aa\) and \(bb\) generators are real antisymmetric. Thus \(V=GV_{\rm diag}G^{\mathsf T}\). The protected program space is invariant under \(G\otimes G\), as conjugation by \(G\) preserves the two separate Majorana counts. The shared projector is invariant under the corresponding two-copy Gaussian action. The Bell program is invariant under \(G\otimes G\) as well. The complementary data effect therefore transforms by \(G(\beta I)G^{\mathsf T}=\beta I\), proving the identity. Signed singular values include singular matrices and all field signs by continuity.

To verify strict positivity at every odd size analytically, choose any two distinct \(a\)-Majoranas, or any two distinct \(b\)-Majoranas. Each resulting degree-two Pauli lies outside the balanced protected space. There are \(2\binom n2=n(n-1)\) distinct such sector Paulis for odd \(n\ge3\), and their shared-projector coefficient is
\[
 a_1=[x^{\text{odd}\le n-2}](1-x)^2(1+x)^{2n-2}
 =\binom{2n-3}{n-2}-\binom{2n-3}{n-3}
 =\frac1n\binom{2n-2}{n-1}>0.
\]
Here the bracket denotes the sum of the indicated odd coefficients. Consequently \(M=\sum_{P\notin\mathcal S}a_P^2\ge n(n-1)a_1^2>0\). This positivity argument is independent of the finite numerical checks.

## 2. A uniform identity component after depolarization

In the ideal-flag branch, each complementary amplitude is \(pbL_R\), because the ideal program has no support there. The completely positive map formed by these outcomes has trace effect \(p^2|b|^2\beta I\), where \(b=e^{2i\epsilon}-e^{-6i\epsilon}\). Complete depolarization of its data output gives
\[
 \delta\,\mathcal D,\qquad
 \delta=p^2|b|^2\beta,\qquad
 \mathcal D(\rho)=\operatorname{Tr}(\rho)I/D .
\]
The constancy of the data effect is essential here: it makes this contribution proportional to the trace-preserving depolarizing channel, rather than an input-dependent discard map.

The original balanced construction in one selected sector has identity weight \(1-\gamma\) with
\(\gamma=3(1-f)\sin^2(4\epsilon)\).
Its remaining completely positive nonidentity contribution contains the complementary outcomes, since the ideal coefficient there is zero. Removing them leaves a completely positive residual of trace factor \(\gamma-\delta\). The uniform logical Pauli representation
\[
 \mathcal D=D^{-2}\,\mathrm{id}+(1-D^{-2})\mathcal N_{\rm unif}
\]
contains an explicit identity component. The new selected-sector channel consequently has form
\[
 (1-\gamma')\,\mathrm{id}+\gamma'\mathcal N_H,\qquad
 \gamma'=\gamma-\delta/D^2
  =\left[3(1-f)-\frac{9M}{4r^2D^2}\right]\sin^2(4\epsilon),
\]
with \(\mathcal N_H\) trace preserving and completely positive. The cross-parity coherence remains \(g\), since the modified complementary outcomes have zero ideal program amplitude and no opposite-parity data amplitude.

The balanced two-sector norm bound is at most \(|1-g|+\gamma'/2\), because \(\gamma'\le\gamma\le2|1-g|\). At \(H=0\), and at the physical edge Pauli oracle, all unmodified residuals are mixtures of nonidentity Paulis after removing the target. The depolarizing part contributes a uniform nonidentity Pauli mixture once its identity component is removed. Thus \(\mathcal N_H\) contains only nonidentity Paulis at those oracles, and the equal two-sector Bell input attains the bound. This proves the exact physical supremum and its strict reduction for \(\sin(4\epsilon)\ne0\).

## Implications and next step

The edge obstruction covered only diagonal complementary correction channels. Complete depolarization uses the full logical Pauli group and escapes that premise. The constant complementary-probability identity supplies a uniform guarantee, so this establishes a strict minimax gain over the old balanced decoder on the full physical family. The gain is smaller than the fixed-diagonal test-family gain by another factor of \(D\); it is a proof of principle.

The next step is to replace complete depolarization by a more informative non-diagonal recovery while retaining a certified identity component in the residual channel. The shared-projector and protected-space symmetries can constrain such a channel without full exponential register simulation. The physical pentagon six-versus-seven problem and the optimal quadratic error over all six-query encoders remain open.

The [EUI manuscript and robustness appendix](https://arxiv.org/html/2506.20570v1) give the physical setting. This proof uses the [physical program-span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md), the [selective residual decomposition](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md), and the [balanced diamond-norm argument](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md).

## Verification

The script reconstructs the actual shared projector and balanced program space at three and five sites. It checks the exact protected-projector matrix-unit zeros, the shared-projector weight-conservation support, and the constant-probability identity for seeded noncommuting physical Hamiltonians and diagonal fields. These sizes check the dimension-independent identity; the first-order-canceling decoder requires \(n\ge21\). The long-ring coefficient improvement is evaluated by exact fractions.

~~~python
from fractions import Fraction
from itertools import combinations
from math import comb

import numpy as np
from scipy.linalg import expm


def coefficients(n):
    return [
        sum(
            (-1)**j*comb(2*k, j)*comb(2*n-2*k, ell-j)
            for ell in range(1, n, 2)
            for j in range(max(0, ell-2*n+2*k), min(2*k, ell)+1)
        )
        for k in range(n+1)
    ]


def complementary_weight(n):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    a = coefficients(n)
    S = sum(comb(n, k)**2*a[k]**2 for k in range(n+1))//2-r*r
    return r*(D*D-r)-S


def verify_effect(n):
    size = 2**n
    basis = [x for x in range(size) if x.bit_count() % 2 == 0]
    D = len(basis)
    sector = np.ix_(basis, basis)
    identity = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1])
    majoranas = []
    for site in range(n):
        for local in (x, -y):
            matrix = np.ones((1, 1))
            for j in range(n):
                matrix = np.kron(matrix, z if j < site else local if j == site else identity)
            majoranas.append(matrix)
    C = np.eye(size, dtype=complex)
    for g in majoranas[1::2]:
        C = C@g
    columns = []
    for degree in range(1, n, 2):
        for labels in combinations(range(2*n), degree):
            matrix = C.copy()
            for j in reversed(labels):
                matrix = majoranas[j]@matrix
            columns.append(matrix[sector].conj().reshape(-1)/np.sqrt(D))
    columns = np.column_stack(columns)
    Q = columns@columns.conj().T

    outside = []
    for mask in range(1 << (2*n-1)):
        if mask.bit_count() % 2:
            continue
        na = sum((mask >> (2*j)) & 1 for j in range(n))
        nb = sum((mask >> (2*j+1)) & 1 for j in range(n))
        if na == nb:
            continue
        matrix = np.eye(size, dtype=complex)
        for j in range(2*n):
            if (mask >> j) & 1:
                matrix = matrix@majoranas[j]
        outside.append(matrix[sector].reshape(-1)/np.sqrt(D))
    outside = np.stack(outside).conj()
    protected = np.eye(D*D)-outside.conj().T@outside
    # These dyadic projector entries are exact in binary64 at these sizes.
    pairs = [(basis[e], basis[r]) for e in range(D) for r in range(D)]
    for i, (e, r) in enumerate(pairs):
        F = e ^ r
        expected = Fraction(comb(F.bit_count(), F.bit_count()//2), 2**F.bit_count())
        assert protected[i, i] == float(expected)
        for j, (t, u) in enumerate(pairs):
            if (t ^ u) != F or ((r & F) == (u & F) and r != u):
                assert protected[i, j] == 0
    rows, columns = Q.nonzero()
    for row, column in zip(rows, columns):
        y, e = basis[row//D], basis[row % D]
        x, t = basis[column//D], basis[column % D]
        assert all(
            ((y >> k) & 1)+((e >> k) & 1)
            == ((x >> k) & 1)+((t >> k) & 1)
            for k in range(n)
        )
    beta = float(Fraction(complementary_weight(n), D**4))
    rng = np.random.default_rng(20261120+n)
    for sample in range(5):
        fields = rng.normal(size=n)
        edges = np.zeros(n) if sample == 0 else rng.normal(size=n)
        H = np.diag([
            sum(fields[j]*(-1)**((row >> j) & 1) for j in range(n)) for row in basis
        ]).astype(complex)
        for column, row in enumerate(basis):
            for j in range(n):
                flipped = row ^ (1 << j) ^ (1 << ((j+1) % n))
                H[basis.index(flipped), column] += edges[j]
        V = expm(1j*H)
        joint = (np.kron(V, V)@Q).reshape(D, D, D, D)
        amplitudes = joint.transpose(1, 3, 0, 2).reshape(D*D, D*D)
        kraus = (outside@amplitudes/np.sqrt(D)).reshape(-1, D, D)
        effect = np.einsum("rai,raj->ij", kraus.conj(), kraus)
        np.testing.assert_allclose(effect, beta*np.eye(D), atol=2e-12, rtol=0)
    print(n, "constant complementary effect verified:", f"{beta:.12f}")


for n in (3, 5):
    verify_effect(n)
for n in (21, 23, 83):
    D = 2**(n-1)
    r = D*D-comb(2*n, n)//2
    assert coefficients(n)[1] == comb(2*n-2, n-1)//n
    assert complementary_weight(n) >= n*(n-1)*coefficients(n)[1]**2 > 0
    gain = Fraction(18*complementary_weight(n), r*r*D*D)
    old = 6+24*Fraction(D*D-r, D*D)
    assert 0 < gain < old
    print(n, "strict full-family quadratic gain", f"{float(gain):.12g}",
          "new coefficient", f"{float(old-gain):.12f}")
~~~
