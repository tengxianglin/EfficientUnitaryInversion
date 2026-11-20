# Principal-minor criterion and an all-odd-ring mirror obstruction

Run date: 2026-11-20 (Asia/Shanghai). Starting revision:
`c294b68b6bcbc787684405d13780fb68551bf3d2`.
Related: Issue #3 and [joint-parity converse](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md).

**Proved here:** a Fourier/principal-minor characterization of the uniform
program-mass condition, and an exact separating inequality excluding every
convex mixture of single perfect-mirror segments, for every odd n >= 5.
**Not proved:** existence or nonexistence of a general joint uniform physical
ensemble, or unrestricted optimality of an inversion protocol. The existing
five/seven-site certificates remain valid and use more general seeds.

## 1. The moment problem without exponentially large physical matrices

Let n >= 3 be odd, N = 2n, and D = 2^(n-1). Use zero-based Majorana indices,
with a indices even and b indices odd. In the selected parity block write
H = i sum_j c_j gamma_j gamma_(j+1), including the selected wrap sign in c.
Set V = exp(iH). Let R = exp(A), where A_(j,j+1) = 2c_j and
A_(j+1,j) = -2c_j, with cyclic indices. Transposing this convention has no
effect on principal minors.

Even Majorana subsets modulo full complementation label the D^2 logical
Paulis. Choose Hermitian representatives P_I. The balanced subset labels
T have equally many a and b indices; denote their quotient by S. Its size
is s = binom(2n,n)/2. By the existing
[program-span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md), physical V
has expansion V = sum_(T in S) v_T P_T, with w_T = |v_T|^2 summing to one.
For any even I, the following identity holds:

\[
 \widehat w(I)=\sum_{T\in\mathcal S}w_T(-1)^{|I\cap T|}
 =D^{-1}\operatorname{Tr}(V^\dagger P_I V P_I)
 =\det R_{I,I}.                                      \tag{1}
\]

The first equality with the trace follows from Pauli orthogonality and
the commutation sign for two even monomials. Gaussian conjugation acts on
grade-|I| monomials by the exterior power of R, whose diagonal coefficient
is its principal minor. In a chiral block, only I and its complement can
have nonzero trace pairing with P_I. Conjugation preserves grade; since
n is odd and |I| is even, |I| != |I^c|. The complement therefore contributes
nothing. This establishes the last equality despite parity restriction.
Standard Gaussian orthogonal action is reviewed in Bravyi,
[quant-ph/0404180v2](https://arxiv.org/html/quant-ph/0404180v2); (1) is derived
here for the present coefficient problem.

For |I| = 2k and v = number of b indices in I, the uniform target is

\[
 t_I=\frac1s\sum_{T\in\mathcal S}(-1)^{|I\cap T|}
 =(-1)^{v+k}\frac{\binom nk}{\binom{2n}{2k}}.          \tag{2}
\]

To derive it, XOR T with the full b subset B. Balanced T become all subsets
of size n, modulo complement. The character picks up (-1)^v. Averaging a
weight-2k character on this middle layer gives
K_(2k)(n)/binom(2n,2k). Its numerator is the coefficient of x^(2k) in
(1-x)^n(1+x)^n = (1-x^2)^n, namely (-1)^k binom(n,k).

Consequently **E det R_(I,I) = t_I for every even I modulo complement is
necessary and sufficient** for E w_T = 1/s. Sufficiency is full character
inversion on the logical Pauli group, extending w by zero outside S;
checking only degree two is necessary but generally insufficient. This
avoids D-by-D exponentials for individual tests, not the exponential
number of constraints in the full criterion.

For physical periodic chains the two parity blocks have opposite wrap
flux. In general both R matrices must be tested. When any cycle edge is
exactly zero, the existing gap/gauge lemma proves equal sector masses, so
one sector's full criterion suffices jointly. Every segment used below
has such a gap, including L=N (the closing edge remains zero).

## 2. Degree-two conditions and a universal linear identity

For d=1,...,n define the dihedrally averaged degree-two moment

\[
 m_d(R)=\frac1N\sum_{i=0}^{N-1}
 \det R_{\{i,i+d\},\{i,i+d\}},\qquad
 t_d=\frac{(-1)^{d+1}}{2n-1}.                         \tag{3}
\]

Indices are cyclic. Let S_d be the sum over *unordered* pairs at circular
distance d, each counted once. Then m_d=S_d/N for d<n, whereas m_n=2S_n/N.
The factor of two for antipodal pairs is essential.

Let Z=diag(1,-1,...,1,-1). A is bipartite, so ZAZ=-A. Thus Q=ZR is symmetric,
Q^2=I, and Q=exp(-A/2) Z exp(A/2) has trace zero. Its second elementary
symmetric polynomial is e_2(Q)=((Tr Q)^2-Tr Q^2)/2=-n. Since
its two-by-two principal minors equal (-1)^(i+j) times those of R,

\[
 \sum_{i<j}-(-1)^{i+j}\det R_{\{i,j\},\{i,j\}}=n.    \tag{4}
\]

For odd n>=5 choose y_1=-1/2, y_d=(-1)^(d+1) for 2<=d<=n-2,
y_(n-1)=1/2, y_n=-1. Equation (4), with the antipodal multiplicity above,
gives the useful identity

\[
 \Phi(R):=\sum_d y_dm_d(R)
 =\frac12-\frac{3}{4n}B(R),\qquad
 B(R)=S_1-S_{n-1}+2S_n.                              \tag{5}
\]

The required uniform target has Phi(t)=(n-5)/(2n-1).

## 3. Exact obstruction for a single perfect-mirror segment

Take one contiguous segment of L vertices (1<=L<=N), with couplings
c_j = (pi/4) sqrt((j+1)(L-j-1)), j=0,...,L-2, and all other edges zero.
This is the standard spin-(L-1)/2 pi rotation, in a real basis:

\[
 (R_L)_{i,L-1-i}=(-1)^i\quad(0\le i<L),\qquad
 (R_L)_{ii}=1\quad(i\ge L),                          \tag{6}
\]

with all other entries zero. The generator has upper diagonal
(pi/2)sqrt((j+1)(L-j-1)), namely the spin representation of a pi rotation.
Engineered perfect-transfer chains are an established primitive:
Christandl et al., [PRL 92, 187902 (2004)](https://arxiv.org/abs/quant-ph/0309131).
No novelty is claimed for (6).

**Theorem.** For every odd n>=5, every convex mixture of these seeds,
their dihedral images, and their vertex-sign gauges satisfies

\[
 \mathbb E\Phi(R_L)\le\frac{n-6}{2n}
 <\frac{n-5}{2n-1}=\Phi(t),\qquad
 \Phi(t)-\frac{n-6}{2n}=\frac{3(n-2)}{2n(2n-1)}.       \tag{7}
\]

It therefore cannot satisfy even the degree-two uniform conditions,
and cannot provide the joint ensemble needed for the long-ring converse.

Proof: a two-by-two principal minor of a signed permutation is nonzero
only for two fixed points or a transposed pair. With M=N-L, enumeration of
these three types gives B_L = B_out+B_center+B_trans, where

- B_out = max(M-1,0) - 1_(L=n), for two idle outside vertices;
- B_center = 2*1_(L=1 or L=N-1), for a segment's central fixed point paired
  with an outside fixed point;
- if L is even, B_trans = 1+1_(L=N)+2*1_(L>=n+1);
- if L is odd, B_trans = 1_(L>=n)+1_(L>=n+2).

For clarity, outside vertices form a contiguous path of length M:
there are max(M-1,0) nearest-neighbor pairs; pairs at distance n-1 and n
cancel except when M=n, giving the stated subtraction. Central/outside
terms vanish except for L=1,N-1. Mirror transpositions have separations
L-1,L-3,...,1 (even L), or L-1,L-3,...,2 (odd L). Counting separations
1,N-1,n-1,n+1,n with their weights in B gives the displayed expressions.

These formulas imply B_L>=4 without any numerical extrapolation:
L=1 gives B=N; L=N,N-1 give B=4. For even L<N,
B=M+2*1_(L>=n+1), which is >=4. For odd 3<=L<=N-3,
B=M-1>=n+1 when L<=n-2; B=n-1>=4 when L=n;
and B=M+1>=4 when L>=n+2. Equations (5) and (2) prove (7).
Vertex-sign conjugation leaves every principal minor invariant, dihedral
images preserve every m_d, and averaging preserves the bound. QED.

For n=21 the target is 16/41, the sharp class upper bound is 5/14, and the
gap is 19/574. This is an exact exclusion of an entire continuous-weight
mixture class, not infeasibility of a sampled linear program. The n=3
case is deliberately excluded. Multiple simultaneously active segments,
fractional transfer times, and arbitrary couplings are outside the theorem.

## 4. Reproducibility and next step

Run `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_minor_obstruction.py`.
Output is frozen in [evidence/program_minor_obstruction.json](evidence/program_minor_obstruction.json).
The verifier independently compares all 16/256 logical Pauli Fourier
characters with principal minors at n=3/5, checks (2) by exact counting,
checks (6) against matrix exponentials for every segment at these sizes,
and checks (4) for general closed cycles. These floating-point checks
support the derivation; they are not interval proofs.

It also uses exact integer minors and rational arithmetic to check all
segment lengths for every odd n=5,...,41 and n=101, including the sharp
upper bound, B formula, and separation gap. These are finite consistency
checks of the all-n proof in Section 3. NumPy/SciPy/Python versions and
starting revision are recorded in the evidence JSON.

## 5. Small decisive n=21 bypass screen: degree two is insufficient

A follow-up screen uses two adjacent disjoint mirror segments of lengths
(a,b), followed by 42-a-b idle vertices. The active edges stay inside each
segment, so every seed is gapped and sector-compatible. Searching all 861
integer pairs a,b>=1, a+b<=42 by a floating-point HiGHS LP found a
21-atom positive mixture. The verifier freezes the atoms in
`two_segment_screen()` and checks its weights **exactly** as integers over
8077: they are positive, sum to one, and satisfy all 21 degree-two moment
conditions after dihedral averaging. The evidence JSON records every atom.
This is an exact finite degree-two feasibility certificate, not a full
program-uniformity certificate.

The smallest higher-degree check already rejects this particular mixture.
For I={0,1,2,3}, exact signed-permutation minors and all 84 dihedral images
give E det R_(I,I)=1/41, while (2) requires 1/533. The residual is 12/533.
Thus two segments can bypass the single-segment separating inequality,
but this frozen ensemble cannot extend the minimax theorem. No general
two-segment impossibility follows from rejecting one LP solution.

The next highest-value action is to add degree-four probes to the n=21
two-segment feasibility screen, starting with this explicit failing
probe. A positive solution must then be tested against all degree-four
orbits; a negative result needs an exact dual certificate for that seed
pool. Ultimately all even minors, or an analytic implication controlling
them, are required before claiming the full joint uniform ensemble.

## 6. Follow-up: the two-mirror screen is now excluded

The [exact fourth-order obstruction](THEORY_TWO_MIRROR_OBSTRUCTION.md) completes the proposed next screen at n=21 and strengthens it to all two-segment placements with both idle gaps. A single fourth-order probe together with the 21 degree-two conditions has an exact separating certificate over all 12,342 configurations. The earlier degree-two certificate remains valid; the general physical uniform-ensemble question remains unresolved.
