# Independent parity-sector mode rotations in physical Ising tori

For the fully fielded odd Ising cycle with independently tunable real coefficients and \(P=\prod_j X_j\), the [six-query problem on five sites](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md) has a sharp solution on the larger independent Gaussian group. A physical comb only has to handle single exponentials from the cyclic Ising family. This note gives explicit noncommuting tori available as limits of that family.

**Proposition.** Choose any two sites, either parity sector, and any real angle for an orthogonal rotation of the two site modes. Up to eigenvector labels and signs, the full product of the independent spinor phase tori with those two modes rotated in the chosen sector, and all other mode vectors in both sectors fixed at their field-only values, is a limit of physical Ising eigenphase tori. Exact ideal inversion and zero first-order common \(P\)-drift on the full physical promise imply the same identities on each such torus. The construction also gives the tori with a two-mode particle–hole rotation by conjugating with a known local Pauli.

At five sites one such rotation acts in four two-dimensional spaces inside one physical parity block of dimension 16 and fixes the complementary eight basis states there, as well as all 16 states of the other block. The result supplies basis comparisons for general fixed-order circuits without assuming the oracle ranges over the full independent Gaussian group.

## 1. One-sector rotation from interference of the two paths

Use the [quadratic Majorana representation](THEORY_ODD_CYCLE_THREE_QUERIES.md#quadratic-representation-in-the-two-sectors), \(H|_{S_s}=i\sum_{ij}(K_s)_{ij}a_i b_j|_{S_s}\). By cycling the site order, the chosen sites are \(0,d\) with \(1\le d\le n-1\) and the signed wrap is adjacent to site \(0\). Write the entries of \(K_s\) as
\[
 (K_s)_{ii}=h_i,\quad (K_s)_{i+1,i}=t_i\quad(0\le i<n-1),
 \qquad (K_s)_{0,n-1}=s t_{n-1}.
\]
Here \(t_i=-J_i\) for \(i<n-1\) and \(t_{n-1}=J_{n-1}\) in this convention. Put \(M_s=K_sK_s^\top\). Its diagonal is \(h_i^2+t_{i-1}^2\), with cyclic indices. Its consecutive off-diagonals are \(h_it_i\), with a factor \(s\) on the wrap edge.

Set \(h_0,h_d\to a>0\), and fix all other fields \(b_i>0\) distinct and different from \(a\). Write \(h_i^{(0)}\) for these limiting values. On the forward path of length \(d\) set \(t_i=\tau^{n-d}\) for \(0\le i<d\). On the backward path of length \(n-d\) set \(t_i=\tau^d\) for \(d\le i<n-1\) and \(t_{n-1}=e\tau^d\). Thus the product of couplings on either path has the same power \(L=d(n-d)\). The coefficient \(e\) is a fixed real number to be set below.

Separate the pair indices \(A=\{0,d\}\) from their complement \(B\). For eigenvalues \(E\) near \(a^2\), the pair components obey the effective eigenvalue equation for the Schur matrix
\[
 F_s(E)=M_{s,AA}+M_{s,AB}(E-M_{s,BB})^{-1}M_{s,BA}.
\]
In \(B\), the interiors of the two paths are disconnected, and the sign \(s\) is on an edge incident to \(A\). Hence the diagonal entries of \(F_s(E)\) are exactly independent of \(s\). If either path has length one it contributes directly from \(M_{s,AA}\). Otherwise its first contribution to the off-diagonal comes from the unique walk through its interior in the resolvent expansion. At \(E=a^2\) this gives
\[
 (F_s(a^2))_{0d}=\tau^L(A_0+s e B_0)+o(\tau^L),\qquad
 A_0=\frac{\prod_{i=0}^{d-1}h_i^{(0)}}{\prod_{i=1}^{d-1}(a^2-b_i^2)},\quad
 B_0=\frac{\prod_{i=d}^{n-1}h_i^{(0)}}{\prod_{i=d+1}^{n-1}(a^2-b_i^2)} .
\]
Indeed each edge on the path gives its \(h_i t_i\) factor, and each interior vertex gives its diagonal resolvent factor. Every walk with a backtrack contributes an additional positive power of \(\tau\). Empty products are one. Both constants are nonzero.

For a target sector \(s_0\), choose \(e=s_0 A_0/B_0\). Set the two fields at the pair sites as real analytic functions of \(\tau\) by requiring the common diagonal entries of \(F_s(a^2)\) to equal \(a^2+\Delta\tau^L\) and \(a^2-\Delta\tau^L\). The implicit function theorem applies at \((h_0,h_d,\tau)=(a,a,0)\) because the two-by-two field Jacobian is \(2a I\). This prescription cancels the larger diagonal shifts without using any parity-dependent physical coefficients. With \(\Delta\ne0\), the two leading effective matrices after subtracting \(a^2I\) and dividing by \(\tau^L\) are
\[
 \begin{pmatrix}\Delta&2A_0\\2A_0&-\Delta\end{pmatrix}
 \quad(s=s_0),\qquad
 \begin{pmatrix}\Delta&0\\0&-\Delta\end{pmatrix}
 \quad(s=-s_0).
\]
Replacing \(a^2\) by a nearby true eigenvalue in \(F_s\) does not change the limiting matrices. The derivative of \(F_s\) in \(E\) is \(O(\|M_{s,AB}\|^2)=o(1)\) uniformly near \(a^2\); the effective eigenvalue equation then gives \(|E-a^2|=O(\tau^L)\). The complementary eigenvector component is \(o(1)\) from the same resolvent. Since both limiting matrices have simple spectra, the left singular vectors converge to the two displayed eigenbases on the pair. The other singular vectors converge to their original site vectors since their squared singular values \(b_i^2\) are distinct. All singular values remain positive. A right singular vector is obtained by applying \(K_s^\top\) to its left partner and dividing by the singular value. As \(K_s\) tends to the positive field diagonal, the right and left vectors have the same limits. Their signs can be chosen to give orientation-preserving bases on both sides.

Varying \(\Delta\) produces all two-dimensional rotation eigenbases up to signs and permutation, with an equal-weight rotation obtained in the closure \(\Delta\to0\). Equivalently the selected sector rotates the \(a\)- and \(b\)-modes of the pair by the same real angle. For the associated fermions this is an ordinary number-conserving mode rotation. It acts only on states with one occupied mode in the pair. In either total parity sector, fixing that pair occupancy leaves \(2^{n-3}\) spectator spin configurations, each giving one two-dimensional rotation. The physical field-only basis is the common site-occupation basis. In the sitewise Hadamard basis, conjugating by the Pauli \(X\) on one chosen site flips the sign of that site's field and exchanges the physical parity labels while preserving the Ising family. This exchanges equal and opposite pair occupations and gives the variant on the equal-occupation spaces. Both versions allow selection of either final parity sector.

## 2. From physical Hamiltonians to full product tori

The [cut-edge spectral argument](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md#independent-majorana-eigenphases-on-a-physical-ray) supplies a positive-field Hamiltonian with \(2n\) independent positive singular values in the two parity sectors and arbitrarily small couplings. Such phase-independent Hamiltonians approximate every simple-mode point in the above positive-field construction. For this extension, interpolate by a real pencil from a certified point with small couplings and positive fields to the chosen point of the construction at small nonzero \(\tau\). The couplings can be chosen small enough relative to the minimum field on the segment that all \(K_s\) are nonsingular throughout. Apply Rellich's analytic eigenvalue theorem to \(\begin{psmallmatrix}0&K_s\\K_s^\top&0\end{psmallmatrix}\) on the segment, following its positive eigenvalues separately in each sector. Each nonzero integer relation is an analytic function nonzero at the certified end. Their countable union of zero sets can be avoided along a sequence approaching the chosen endpoint. Simple mode spectra there let the singular frames converge up to labels and signs.

Each approximant gives by scaling the Hamiltonian a ray dense in the full product of the two independent spinor phase tori in its own basis. The drifted oracle on a torus is \(D_B(z)e^{-i\epsilon P}\), where \(D_B\) is diagonal in the corresponding physical parity bases. Its fixed-comb Stinespring map is a polynomial in the oracle entries, so exact ideal inversion and the vanishing channel derivative extend by continuity to these tori and to their limits. Sending \(\tau\) to zero therefore gives the independently rotated tori of the proposition.

## 3. The common phase face for the five-site compatibility test

For the number-conserving rotation of sites \(0,d\) in sector \(s_0\), restrict its Majorana phase vector to the face \(\theta_{s_0,0}=\theta_{s_0,d}\). The field-basis torus and rotated-basis torus then have the same physical oracle, since in each affected two-dimensional space the two spinor eigenphases coincide. The other sector is unrestricted. The same equality holds with drift, so the corresponding Stinespring amplitudes are related on this face by an exact basis change of input and output, with the same environment. In particular, Fourier coefficients in drift charge must obey this basis change. The particle–hole variant gives the opposite-sign face in suitable signed phase coordinates. These are finite-label constraints at degree six. Explicitly, write \(C_{k,\nu}\) and \(C'_{k,\nu}\) for the Stinespring amplitude operators in the two coordinate bases, where \(k\) is the number of plus queries and \(\nu\) the pair of Majorana phase exponents of their output. On the face \(\theta_{s_0,d}=\eta\theta_{s_0,0}\) with \(\eta=\pm1\), let \(L_\eta\) replace \((\nu_{s_0,0},\nu_{s_0,d})\) by \(\nu_{s_0,0}+\eta\nu_{s_0,d}\). If \(R\) maps the field basis to the rotated basis, the equations are
\[
 \sum_{L_\eta\nu=\lambda} C'_{k,\nu}
  =(R^\dagger\otimes I)\left(\sum_{L_\eta\nu=\lambda} C_{k,\nu}\right)R
 \quad\text{for every }k,\lambda .
\]
Here coefficients not available at a given count are zero. Orthogonality in the independent drift phase selects \(k\) separately. For a five-site sector with \(\ell=0,\ldots,6\) own-sector calls, exact enumeration gives \(1,12,60,192,475,996,1862\) distinct restricted phase characters per face, in either parity and for either sign. The largest fiber has \(\ell+1\) elements, since each of the merged coordinates ranges from \(-\ell\) to \(\ell\) in steps of two.

This provides independently rotatable comparisons for each pair of mode indices on the pentagon. At five sites the rotation mixes four pairs of data basis states at once in the selected parity block, and general six-call saturation of the single-torus normalization inequality is not available. The new tori therefore do not by themselves establish the \(31/16\) group bound on the physical promise. The next step is to impose the common-face relations on the preferred and alternate degree-six amplitudes of the 32 single-weight environment modes and test whether their total permitted alternate norm can reach \(3/4\).

The [EUI preprint and Appendix B](https://arxiv.org/html/2506.20570v1) give the odd-cycle setting and robustness motivation. The quadratic reduction is standard in the [Ising solution](https://doi.org/10.1016/0003-4916(70)90270-8). The analytic eigenvalue step uses [Rellich's theorem](https://books.google.com/books/about/Perturbation_Theory_of_Eigenvalue_Proble.html?id=VjbvAAAAMAAJ).

## 4. Obstruction to extending monomial routing across the tori

Consider a six-query circuit that on the field-basis torus is a fixed input-independent mixture of coherent monomial routings. By this we mean that each branch gives the correct inverse phase times a single common spectator phase character at \(\epsilon=0\), and, under drift, multiplies each input basis state by a single charge phase \(e^{-i\epsilon q_{s,w}}\). Within a branch the phase character and all charges are fixed. This includes the [known-basis optimal routing](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md#what-six-queries-can-do-on-one-torus).

**Corollary.** Such a circuit cannot both cancel first-order drift on the physical promise and preserve all data eigenstates in all the independently rotated bases under drift. Preservation here means that the data channel fixes each basis-state density matrix at the common ideal oracle \(U=I\), with the noisy query \(e^{-i\epsilon P}\), for small real \(\epsilon\).

For a rotation and a pair of basis states it mixes with nonzero coefficients, the rotated pure state at \(U=I\) must stay pure and equal to itself. The output is a mixture of the branch outputs on the original two states, evolving their relative coherence by \(e^{-i\epsilon(q_{s,w}-q_{s,w'})}\). An average of unit phases equals one only when every phase of positive weight is one. For all small \(\epsilon\) this requires \(q_{s,w}=q_{s,w'}\) in every such branch. The particle and hole rotation graphs together connect all occupation rows in each parity sector: any two rows in that sector differ in an even number of bits, and the differing bits can be flipped in pairs. Hence the charges are constant on each parity sector in each branch.

For a given spectator character, an alternate lift is unavailable for at least one input of each sector. This is the \(k=0,1,2\) obstruction in the [phase lift lemma](THEORY_ODD_CYCLE_CAUSAL_DRIFT.md#allowed-phase-lifts-through-six-queries). Constant branch charges then force the preferred lift on every input of either sector, with their opposite-sector charge difference equal to six. Off-diagonal parity coherences at \(U=I\) consequently have slope of magnitude six. In particular a six-query candidate built from such field-basis monomial routings must either abandon first-order cancellation or change some data populations in a physically reachable eigenbasis under nonzero drift.

For the explicit optimal routing on one torus this can also be seen directly. It chooses one plus label uniformly and attempts its alternate with probability \(p=3D/[4(D-1)]\) on the eligible inputs. The resulting within-plus coherence factor for two different field-basis states is \(1-(2p/D)(1-\cos8\epsilon)\). The same recipe in a basis rotated by \(\pi/4\) would fix the rotated superpositions on the common phase face. On one such superposition the field-basis recipe instead gives trace-norm error \((2p/D)(1-\cos8\epsilon)\) relative to the ideal inverse, after removal of the common ideal phase. This difference is a finite-\(\epsilon\) incompatibility of the two recipes. A general comb can use coherent superpositions of charge lifts or change populations under drift, so the corollary leaves the unrestricted five-site query count open.

## Verification

The SymPy check evaluates the Schur complement with frozen limiting fields to certify the path prefactors, parity-independent diagonal tuning targets, and canceling off-diagonal sign at every five-site separation. It then checks the spinor phase-face equality and enumerates all charge-resolved face characters using exact integer rows.

~~~python
from collections import Counter
from fractions import Fraction
from itertools import product
from math import prod

import sympy as sp


def check_paths(n, d):
    tau = sp.symbols("tau")
    a = 1
    h = [a if i in (0, d) else i + 1 for i in range(n)]
    forward = Fraction(prod(h[:d]), prod(a*a - h[i]**2 for i in range(1, d)))
    backward = Fraction(prod(h[d:]), prod(a*a - h[i]**2 for i in range(d + 1, n)))
    order = d * (n - d)
    pair = [0, d]
    rest = [i for i in range(n) if i not in pair]

    for target in (1, -1):
        e = target * forward / backward
        effective = {}
        for sector in (1, -1):
            matrix = sp.diag(*h)
            for i in range(n - 1):
                matrix[i + 1, i] = tau**(n - d if i < d else d)
            matrix[0, n - 1] = sector * sp.Rational(e) * tau**d
            m = matrix * matrix.T
            cross = m.extract(pair, rest)
            inverse = (a*a * sp.eye(n - 2) - m.extract(rest, rest)).inv()
            effective[sector] = m.extract(pair, pair) + cross * inverse * cross.T
        for i in range(2):
            assert sp.cancel(effective[1][i, i] - effective[-1][i, i]) == 0
        for sector in (1, -1):
            off_diagonal = sp.cancel(effective[sector][0, 1])
            leading = sp.limit(off_diagonal / tau**order, tau, 0)
            assert leading == (2 * forward if sector == target else 0)
    print(n, d, order, forward, backward)


def check_faces(n):
    rows = list(product((1, -1), repeat=n))
    for d in range(1, n):
        for s, occupation_type in product((1, -1), repeat=2):
            # occupation_type=-1 selects opposite occupations, +1 equal.
            pairs = []
            for w in rows:
                if prod(w) != s or w[0] != 1 or w[0] * w[d] != occupation_type:
                    continue
                other = tuple(-v if i in (0, d) else v for i, v in enumerate(w))
                assert prod(other) == s
                delta = tuple(a - b for a, b in zip(w, other))
                assert delta[0] == 2 and delta[d] == 2 * occupation_type
                assert sum(v != 0 for v in delta) == 2
                pairs.append((w, other))
            assert len(pairs) == 2**(n - 3)
            assert len({w for pair in pairs for w in pair}) == 2**(n - 2)
    print("Both occupation faces act on the stated number of pairs.")


def check_face_characters(n):
    expected = [1, 12, 60, 192, 475, 996, 1862]
    for s in (1, -1):
        rows = [w for w in product((1, -1), repeat=n) if prod(w) == s]
        sums = {(0,) * n}
        for k in range(7):
            for sign in (1, -1):
                fibers = Counter((x[0] + sign*x[1], *x[2:]) for x in sums)
                assert len(fibers) == expected[k]
                assert max(fibers.values()) == k + 1
            if k < 6:
                sums = {tuple(a+b for a, b in zip(x, w)) for x in sums for w in rows}
    print("Five-site charge-resolved face character counts:", expected)


for separation in range(1, 5):
    check_paths(5, separation)
check_faces(5)
check_face_characters(5)
~~~
