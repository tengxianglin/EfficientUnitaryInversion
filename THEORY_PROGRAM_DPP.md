# Positive determinant representation of an odd-cycle program distribution

Date: 2026-11-21. Base: `d5b58da9529823fefb77e4a66f8915cadf6dd8d8`.
Related: Issue #3, [minor criterion](THEORY_PROGRAM_MINOR_OBSTRUCTION.md),
[pure-Pauli classification](THEORY_PURE_PAULI_CLASSIFICATION.md), and the
[full uniform-ensemble blocker](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md).

## Result and novelty boundary

**Derived exact identity.** Every selected-parity program distribution of
an odd-cycle physical Ising exponential is a complement-folded rank-n
projection determinantal distribution on 2n sites. Individual program
probabilities can be evaluated, and program labels sampled, using only
2n-by-2n matrices. This avoids constructing a 2^(n-1)-dimensional spinor
matrix or enumerating binom(2n,n)/2 labels for these operations.

**Full ensemble equivalence.** Uniform balanced program masses are exactly
equivalent to uniformity of a *complement-symmetrized* n-particle
occupation distribution defined below. This is an all-moment statement,
not just a degree-two or degree-four relaxation.

Projection DPPs and their efficient samplers are established tools.
Moreover, Collura, De Nardis, Alba and Lami already use determinantal
sampling of Gaussian-state Pauli spectra in
[Quantum 10, 2036 (2026)](https://quantum-journal.org/papers/q-2026-03-23-2036/),
[arXiv:2412.05367v4](https://arxiv.org/abs/2412.05367), including Eq. (6)
and the sampling construction in their full text. **Generic efficient
Gaussian Pauli sampling must not be presented as an EUI innovation.**
The result recorded here specializes the earlier EUI Fourier/minor
criterion to its balanced labels, chiral complement quotient, static
physical generator and joint-parity design question, with a reproducible
implementation. No literature-wide originality claim is made even for
that specialization. EUI still needs a substantive original physical
construction, converse, or separation beyond this tool adaptation.

## 1. A positive rank-n projection from the physical generator

Let n>=3 be odd, N=2n, and use zero-based Majorana indices. In the chosen
parity block absorb the known wrap-edge sign into c. Define
A_(j,j+1)=2c_j, A_(j+1,j)=-2c_j, cyclically, R=exp(A), and
Z=diag(1,-1,...,1,-1). Bipartiteness gives ZAZ=-A. Therefore

\[
 Q=ZR=e^{-A/2}Ze^{A/2},\qquad
 P=\frac{I+Q}{2}=e^{-A/2}P_0e^{A/2},\quad P_0=(I+Z)/2.       \tag{1}
\]

Q is a symmetric involution with n eigenvalues of each sign; P is an
orthogonal rank-n projection. In practice set U=exp(-A/2)[:,even indices]
and P=UU^T. The diagonal occupation model is an *auxiliary* Slater state
of n particles on 2n sites, initially occupying alternating sites and
rotated by exp(-A/2). It is a classical representation, not an additional
physical inversion protocol or a change of the original oracle promise.

For each n-subset S define

\[
 p_c(S)=\det P_{S,S}\ge0,\qquad \sum_{|S|=n}p_c(S)=1.          \tag{2}
\]

Indeed det P_S=(det U_S)^2 and normalization is Cauchy--Binet. Its inclusion
probabilities satisfy Pr(I subset S)=det P_I. A self-contained generating
identity is

\[
 \mathbb E_S\prod_i(1+z_i1_{i\in S})
 =\det(I_n+U^T\operatorname{diag}(z)U),
\]

whose coefficients give those inclusion probabilities. Projection-DPP
and exterior-algebra constructions are standard; primary references
include [Lyons, Determinantal probability](https://rdlyons.pages.iu.edu/pdf/icm-pub.pdf),
Secs. 1--2, and [Kulesza--Taskar](https://arxiv.org/pdf/1207.6083),
Sec. 2.4.4 and its projection-process proof.

## 2. Exact pointwise program probability, including the complement

Let E be the even-index subset {0,2,...,2n-2}. Map an occupation set to
T=S symmetric-difference E, and fold T with T^c to a logical Pauli label.
Since |S|=|E|=n, T contains equally many even and odd indices, and its
cardinality is even. This maps complementary n-subsets to a balanced
Pauli class [T].

If w_[T](c) is the squared selected-sector Pauli coefficient of the
physical unitary, the identity is

\[
 \boxed{w_{[T]}(c)=p_c(T\mathbin\triangle E)
                      +p_c((T\mathbin\triangle E)^c).}       \tag{3}
\]

Proof: for an even Majorana probe I, write v=|I intersect odd indices|.
The DPP inclusion identity gives

\[
 \mathbb E_S(-1)^{|I\cap S|}=\det(I-2P_I)=\det Q_I,
\]

because |I| is even. Consequently

\[
 \mathbb E_S(-1)^{|I\cap(S\triangle E)|}
 =(-1)^v\det Q_I=\det R_I.
\]

These characters are invariant under T -> T^c. The prior Fourier/minor
identity gives the same characters for the actual program masses.
All even I modulo complementation form the complete character group of
the logical Pauli labels. Character inversion therefore proves (3),
including zeros outside the balanced span. Thus the positive determinant
formula is derived from the physical program, not assumed from a
Gaussian-state analogy.

For an ensemble of physical c, (3) implies exact equivalence

\[
 \mathbb E_c w_{[T]}=\frac{1}{s},\quad s=\tfrac12\binom{2n}{n}
 \quad\Longleftrightarrow\quad
 \frac12\mathbb E_c[p_c(S)+p_c(S^c)]
       =\binom{2n}{n}^{-1}\quad\text{for every }|S|=n.         \tag{4}
\]

Uniformity of the *unfolded* mean p_c(S) is stronger and is not required.
A fair complement coin is just classical bookkeeping for (4); it does
not assert that P -> I-P is realized by another legal static oracle.
Equation (3) needs no such physical implementation.

All identities hold in a selected parity sector for arbitrary closed or
gapped cycles. Joint-parity use still requires the same legal ensemble
in both physical sectors. For gapped seeds, the existing gap/gauge lemma
supplies this compatibility. Nothing here removes the opposite-wrap-flux
issue for ungapped periodic seeds.

## 3. Sampler, its exact-arithmetic proof and computational limits

Start with K=P of rank k=n. Repeatedly select i with probability K_ii/k,
then update

\[
 K\ \leftarrow\ K-K_{:,i}K_{i,:}/K_{ii},\qquad k\leftarrow k-1.
\]

This is the projection onto the remaining subspace perpendicular to the
chosen coordinate. It has rank k-1, keeps chosen coordinates zero, and
normalizes each next choice. For any ordering of an n-subset S, the
product of its pivot probabilities is det P_S/n!, by Schur complements.
Summing its n! orderings proves (2). Finally fold S symmetric-difference
E to obtain a program label with law (3).

The rank-one update costs O(N^2) per selection and there are n selections:
O(n^3) arithmetic work per program sample, after O(n^3) preprocessing,
with O(n^2) storage for one sample. Evaluating one given w_[T] uses two
n-by-n determinants. These costs count dense arithmetic at fixed working precision; no exact
bit-complexity bound is asserted. They are classical computation bounds,
not unitary query bounds. Polynomial-time sampling does **not** provide polynomial
sample complexity for certifying uniformity over an exponentially large
label set, nor exact computation of every nonlinear functional.

The implemented NumPy routine batches Schur updates and diagnoses large
negative diagonals, clips tiny roundoff values, and prevents duplicate
selections. Its floating arithmetic has no certified total-variation
error bound. The exact sampler law above must be distinguished from the
finite implementation and its Monte Carlo output.

## 4. Checks and an n=21 global-mass screen

The verifier independently compares (3) against all actual Pauli
coefficients at n=3,5,7, for one closed and one gapped seeded Hamiltonian
at each size: 10,126,1716 labels per instance. The maximum numerical
identity defect across these six instances is below 5.7e-15. It also
checks projection idempotence, rank and determinant normalization.
These are finite floating checks of the analytic identity.

A separate exact-rational test forms a rank-three projection from
rational orthogonal rotations on six sites. It enumerates all 120 ordered
selection paths, checks each 3-subset's Schur-sampling probability against
its determinant, and proves their total equals one using fractions.
This validates the sampling law in a finite exact instance independently
of exponentials and random histograms. A 40,000-sample three-site test of
the actual floating implementation has maximum frequency defect
0.0026604946413346375; this is a diagnostic, not a rigorous error bound.

At n=21, folding a DPP sample and applying the exact even-run classifier
allows estimation of the total matching-label mass m_B without listing
its 596,977,426 labels. For full uniformity its mean must equal
298488713/134564468610, about 0.00221818. The six-case screen used 10,000
samples per case; all seeds have exactly zero wrap coupling.

| Open-path couplings c_0,...,c_40 | Matching hits / 10,000 |
|---|---:|
| all 1 | 1886 |
| all 3 | 27 |
| all 10 | 25 |
| all 30 | 34 |
| all 100 | 14 |
| seeded disorder of standard deviation 10 | 4429 |

The promising-looking 14/10,000 count for the all-100 path was then
rechecked independently with 100,000 samples: **204 hits**, empirical
mass 0.00204. This is near the target scale and does not certify an exact
inequality on either side of it. The empirical masses, including the
large disordered-path value, are Monte Carlo observations. They are not
interval bounds, exact oracle exclusions, or full-uniformity evidence.

The code freezes all coupling strings, RNG seeds, sample counts and
outputs. Standard projection-DPP sampling is the reused primitive; the
experiment applies the EUI folding and complete matching-label
classification to screen the physical long-ring design problem.

## 5. Reproduce and next action

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_program_dpp.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_program_dpp.py --screen
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_program_dpp.py --refine
```

Dependencies used: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. No optimization
solver, spinor matrix or exponentially large label list is needed for
the n=21 screens. The default small-size check constructs spinor matrices
only as an independent validation. Frozen results are in
[evidence/program_dpp_verification.json](evidence/program_dpp_verification.json),
[evidence/program_dpp_screen_n21.json](evidence/program_dpp_screen_n21.json), and
[evidence/program_dpp_refined_screen_n21.json](evidence/program_dpp_refined_screen_n21.json).

The next highest-value action is to use the sampler as a coarse global
filter for general gapped seeds, then optimize exact fourth-order minors
against all orbit constraints. Equation (4) also supplies an explicit
positive-distribution formulation for analytic constructions. Any
candidate ensemble still needs rigorous all-moment control before the
long-ring minimax theorem can be extended. The present tool and finite
screen do not establish that ensemble.

The manuscript and Appendix B at
[arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1) were rechecked;
no manuscript TeX/PDF is present in the repository. Its broader robustness
promise remains distinct from this static program-design problem.

## Follow-up: full moments reject the six screening seeds

The [fourth-moment hierarchy and seed-pool audit](THEORY_FOURTH_MOMENT_HIERARCHY.md) certifies that all six fixed screening seeds, and any positive mixture of their dihedral images, fail a distance-two moment. Thus the near-target matching-mass observations do not yield a uniform construction. It also provides exact fourth/second-order dependency reduction and a separately labeled 1600-column numerical full-fourth-order experiment.
