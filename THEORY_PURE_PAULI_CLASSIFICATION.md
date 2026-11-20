# Complete static Pauli-oracle classification and an all-length seed-weight bound

Date: 2026-11-21. Base: `1d339a919d837269161dc6ac2732c137d809ed90`.
Related: Issue #3, the [matching-recovery diagnostic](THEORY_NONRADIAL_MATCHING_COUNTEREXAMPLE.md),
and the [joint uniform ensemble question](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md).

## Scientific result and precise scope

Earlier work generated 91 legal matching Pauli labels at n=5 but explicitly
left open whether other static physical Hamiltonians realize additional
pure Pauli programs. We close that completeness gap for every odd n>=3.

**Theorem.** Let a single static physical odd-cycle Ising Hamiltonian act
in either fixed parity sector. Label a logical Pauli by an even Majorana
subset T, modulo full complementation. Its selected-sector unitary can
be proportional to that Pauli if and only if the cycle induced by T or
the cycle induced by T^c has a perfect matching (the empty graph counts).
Equivalently, T or T^c has only even-length occupied runs around the
Majorana cycle, with empty and full sets allowed. Thus the matching
construction is exhaustive, including arbitrary noncommuting static
couplings and arbitrary evolution time, not just matching Hamiltonians.

The number of distinct realizable logical Pauli classes is

\[
 b_n=L_{2n}-2^n,                                      \tag{1}
\]

where L_m is the Lucas sequence, L_0=2,L_1=1. All these labels are
balanced and lie in the s_n=binom(2n,n)/2 program span.

**Uniform-ensemble consequence.** Any full uniform balanced program-mass
ensemble has probability at most b_n/s_n on physical oracles whose
selected-sector program is a single logical Pauli. At n=21 this is

\[
 \Pr(\text{pure Pauli program})\le
 \frac{596977426}{269128937220}
 =\frac{298488713}{134564468610}
 \simeq0.0022181837158298575.                         \tag{2}
\]

Hence at least 99.7781816284% of its probability must be on non-Pauli
programs. This is an exact necessary condition for *full* uniformity,
not an existence theorem, a bound on quantum circuit gate counts, or a
statement about non-Clifford resources. Gaussian Clifford unitaries can
have non-Pauli programs and are not excluded by this bound.

## 1. Why a pure parity-sector Pauli forces a diagonal Majorana rotation

Write N=2n and, in the selected quadratic representative,
H=i sum_j c_j gamma_j gamma_(j+1), with the known wrap-sector sign absorbed
in c. Evolution time is absorbed into these unrestricted real couplings.
The corresponding rotation is R=exp(A), A_(j,j+1)=2c_j,
A_(j+1,j)=-2c_j, with cyclic indices. The adjoint/transpose convention does
not affect the following diagonal-rotation statement.

Let D_T be diagonal with entries -1 on T and +1 elsewhere. If the chosen
chiral spinor block of V is e^(i phi) P_T, its adjoint action on every
bilinear gamma_i gamma_j equals that of P_T: its sign is
(-1)^(1_(i in T)+1_(j in T)). Gaussian conjugation on bilinears is the
exterior-square action of R. The restricted bilinears are linearly
independent for N>=6: chiral trace pairing can identify only complementary
Majorana supports, and a two-set cannot be the complement of a two-set
unless N=4. Thus equality on the one parity sector already implies

\[
 \wedge^2 R=\wedge^2 D_T.
\]

For an orthogonal S, exterior-square action is conjugation on real
antisymmetric matrices. Its kernel consists of S=+I,-I: an S in that
kernel commutes with every elementary plane rotation; their commutant
on the real defining representation is scalar, and orthogonality then
forces the scalar to be +/-1. Applying this to S=R D_T gives

\[
 R=D_T\quad\hbox{or}\quad R=-D_T=D_{T^c}.            \tag{3}
\]

The second possibility is essential. A selected parity block cannot
distinguish complementary Majorana monomials up to phase; excluding it
would incorrectly discard physically realizable labels.

This uses the standard Gaussian orthogonal action (see Bravyi,
[quant-ph/0404180v2, Eq. 5 and Eq. 16](https://arxiv.org/html/quant-ph/0404180v2)).
The restriction-to-one-sector and graph arguments here are explicit;
no literature-wide novelty claim is made for the Gaussian primitive.

## 2. Necessity and sufficiency of a matching

Let U denote T or T^c according to which diagonal rotation occurs in
(3). Since A commutes with exp(A), it commutes with D_U. Entrywise this
forces A_ij=0 whenever exactly one of i,j is in U. All nonzero couplings
therefore remain inside the induced U and U^c subgraphs.

For a proper nonempty U on a cycle, each induced connected component is
a path. On a component contained in U, exp(A_component) must equal -I.
A real antisymmetric matrix of odd order has a zero eigenvalue and hence
its exponential has eigenvalue +1. Every such negative component must
therefore have even length. Each even path has a unique perfect matching.
The empty set is trivial; the full N-cycle has a perfect matching because
N is even. This proves necessity, without any numerical optimization or
assumption that the original c_j form a matching.

Conversely, choose a perfect matching of the induced graph on U. Set its
edge couplings to pi/2 and all other couplings to zero. The disjoint
2-by-2 generator blocks each exponentiate to -I, giving R=D_U exactly.
Equivalently the commuting bilinear exponentials multiply to the raw
Majorana monomial Gamma_U up to phase. In the selected parity sector
Gamma_U is the desired label P_T for either U=T or U=T^c. This proves
sufficiency, with an explicit physical realization. These realizing
Hamiltonians can be chosen gapped, so the earlier gap/gauge argument
also provides parity-compatible program masses.

The theorem concerns a *single static* Ising exponential in a selected
parity sector, up to scalar phase. It does not restrict products of
different Hamiltonian evolutions or identify relative phases between
physical parity sectors. Those are different oracle promises.

## 3. Counting complementary classes without overcounting

Let A be the family of vertex subsets covered by some cycle matching.
There are F_(N-1)+F_(N+1)=L_N cycle matchings: split by whether they use
the closing edge, leaving a path on N or N-2 vertices. A path on m vertices
has F_(m+1) matchings by its elementary first-vertex recurrence.

A proper covered subset has a unique matching: each even occupied path
must be matched consecutively. The full cycle has two perfect matchings
with the same covered subset. Therefore |A|=L_N-1.

The intersection A intersect {U^c: U in A} consists of cyclic bit strings
whose occupied and unoccupied runs are all even, including the two
constant strings. Their run boundaries all have the same edge parity.
They are exactly the union of the two families of bit strings constant
on one of the two alternating perfect-match dimers. Each such family
has 2^n strings, and their intersection is just the two constant strings.
Thus this intersection has 2^(n+1)-2 elements. The realizable labels are
complementary pairs in A union {U^c: U in A}, so their number is

\[
 \tfrac12\{2(L_{2n}-1)-(2^{n+1}-2)\}=L_{2n}-2^n.
\]

Every even occupied run contains equally many even and odd vertices;
covered subsets and their complements are balanced. This independently
confirms compatibility with the previously proved balanced program span.

For a concrete balanced but impossible label, take T={0,2,3,5} for any
odd n>=5. Both T and T^c have odd occupied runs. At n=5, for example,
T has isolated 0 and 5 while T^c has isolated 1 and 4. Neither possibility
in (3) can arise from a static nearest-neighbor generator. This is a
missing pure label, not a missing direction in the linear program span:
non-Pauli physical unitaries can still have a nonzero coefficient there.

## 4. Exact and robust probability budgets

Let B be the complete realizable pure-Pauli label set, and for any legal
program define m_B(V)=sum_(T in B)|v_T|^2. For a full uniform ensemble,
E m_B=b_n/s_n. Every pure Pauli program has m_B=1 by the theorem, while
all programs have m_B>=0. Equation (2) follows immediately.
More generally, for 0<tau<=1,

\[
 \Pr\{m_{\mathcal B}(V)\ge\tau\}
 \le\min\{1,b_n/(s_n\tau)\}.                        \tag{4}
\]

Thus the argument also controls mixtures concentrating on the matching
label subspace, rather than only exact Pauli atoms. No claim is made
that m_B is cheap to evaluate at n=21; B itself is large.

| n | Complete pure-Pauli classes b_n | Balanced classes s_n | b_n/s_n |
|---|---:|---:|---:|
| 3 | 10 | 10 | 1 |
| 5 | 91 | 126 | 13/18 |
| 7 | 715 | 1716 | 5/12 |
| 9 | 5266 | 24310 | 2633/12155 |
| 21 | 596977426 | 269128937220 | about 0.00221818 |

Writing phi=(1+sqrt(5))/2 gives b_n/s_n asymptotic to
2 sqrt(pi n) (phi^2/4)^n. The fraction is exponentially small. The
n=5 matching-subspace threshold 13/18 in the older non-radial diagnostic
therefore had a complete pure-Pauli interpretation, not just an
arbitrarily chosen realizable list.

The certified 22-feature n=21 ensemble from the previous run is not a
full uniform ensemble, so this budget must not be imposed on it as a
claim it already satisfies. It is a necessary target constraint for the
remaining full-moment problem. It also does not prevent using a few
pure-Pauli columns for numerical conditioning; it bounds their total
physical mixture probability in any eventual exact full design.

## 5. Reproduction, verification classes and next action

Run:

```
python verify_ising_pure_pauli_classification.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_pure_pauli_classification.py --matrices
```

The default has only Python standard-library dependencies. It enumerates
all logical Pauli classes at n=3,5,7,9 and compares three independent
finite descriptions: recursively generated cycle matching endpoints,
even-run recognition, and a recursive graph perfect-matching test. It
checks both complementary representatives, the intersection count, the
balanced-space count and the closed formula. It also checks the explicit
unrealizable label and evaluates exact all-n formulas at larger sizes.
These are finite consistency checks of the all-n proof above.

The optional NumPy/SciPy check constructs all 10/91 realizing physical
oracles at n=3/5, verifies their selected-sector program masses and their
diagonal Majorana rotations, and independently verifies exact Gram
orthogonality of all 15/45 restricted bilinears. The matrix-exponential
checks are finite floating checks, not the proof of necessity.
Frozen outputs are
[evidence/ising_pure_pauli_classification.json](evidence/ising_pure_pauli_classification.json)
and [evidence/ising_pure_pauli_matrix_checks.json](evidence/ising_pure_pauli_matrix_checks.json).

The next high-value action remains full fourth-order column generation
at n=21. This result supplies a structural guardrail: the complete pure
Pauli list cannot be mistaken for the complete oracle family, and an
ultimate full design must put almost all probability on superposition
programs. Target the independent distant fourth-order violations using
general gapped couplings; the present classification does not solve
that search or the higher-moment closure problem.

The repository manuscript sources are absent; the external
[manuscript and supplementary appendices](https://arxiv.org/html/2506.20570v1)
were inspected. This note concerns a narrower static odd-ring oracle and
program-moment question, not the manuscript's broader robustness model.
