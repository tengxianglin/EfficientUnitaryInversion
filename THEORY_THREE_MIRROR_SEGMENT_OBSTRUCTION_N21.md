# Exact three-segment perfect-mirror obstruction at n=21

Date: 2026-11-25. This note extends the single-perfect-mirror obstruction in
[THEORY_PROGRAM_MINOR_OBSTRUCTION.md](THEORY_PROGRAM_MINOR_OBSTRUCTION.md).
It is a finite-family theorem with exact rational arithmetic, not a claim
about arbitrary multi-segment couplings.

## 1. Physical seed family

Let n=21 and N=42. For a composition
\[
(L_1,L_2,L_3)\in\mathbb N^3,\qquad L_1+L_2+L_3=42,
\]
partition the open path into three consecutive blocks. On a block of length
L beginning at site s, use the engineered perfect-mirror generator
\[
 A_{s+r,s+r+1}=\frac{\pi}{2}\sqrt{(r+1)(L-r-1)},\qquad
 A_{s+r+1,s+r}=-A_{s+r,s+r+1},
\]
for r=0,...,L-2, with all inter-block and wrap couplings zero. Equivalently,
the physical Ising/Majorana couplings are
\[
 c_{s+r}=\frac{\pi}{4}\sqrt{(r+1)(L-r-1)}.
\]
The standard spin-\((L-1)/2\) pi rotation gives the exact signed reversal
\[
 R^{(L)}_{r,L-1-r}=(-1)^r,
 \qquad R^{(L)}_{ij}=0\text{ otherwise}.
\]
For L=1 this is the identity on a singleton. The full R is the direct sum
of the three signed reversals. It is a signed permutation in SO(42), so
orthogonality and determinant one are exact.

There are \(\binom{41}{2}=820\) ordered positive compositions. Each is a
legal gapped physical seed: the wrap edge is zero and the two cuts between
blocks are zero. Dihedral images remain in the same physical family. A
vertex-sign gauge R -> SRS, S=diag(±1), leaves every principal minor
unchanged.

## 2. Complete second-order orbit moments and an exact dual

For d=1,...,21 define
\[
 m_d(R)=\frac1{42}\sum_{i=0}^{41}
 \det R_{\{i,i+d\},\{i,i+d\}},
 \qquad
 t_d=\frac{(-1)^{d+1}}{41},
\]
with cyclic indices. The target t_d is the exact uniform balanced-program
moment from Eq. (3) of
[THEORY_PROGRAM_MINOR_OBSTRUCTION.md](THEORY_PROGRAM_MINOR_OBSTRUCTION.md).
The 21 coordinates are the complete distance orbits of all second-order
principal minors.

Set
\[
 47y=(-10,8,-6,6,-4,2,-2,2,0,2,0,0,0,0,0,0,2,-2,0,0,1).
\]
Then \(\|y\|_1=1\) exactly. The standard exact verifier
[verify_ising_three_mirror_segment_obstruction.py](verify_ising_three_mirror_segment_obstruction.py)
enumerates every one of the 820 compositions, constructs its signed
permutation, checks determinant one, and computes all 21 moments with
fractions.Fraction (no floating-point arithmetic). It establishes
\[
 \boxed{
 \min_{L_1+L_2+L_3=42}
 y^{\mathsf T}(t-m(R_{L_1,L_2,L_3}))
 =\frac{2}{40467}>0.
 }
\]
Exactly 117 compositions attain the minimum; there are 15 distinct exact
slack values. The complete machine-readable output is
[evidence/ising_three_mirror_segment_obstruction_n21.json](evidence/ising_three_mirror_segment_obstruction_n21.json).

**Theorem.** For every probability measure supported on these 820
three-block perfect-mirror seeds, their dihedral images, and their
vertex-sign gauges,
\[
 \boxed{
 \left\|t-\mathbb E_\mu m(R)\right\|_\infty
 \ge \frac{2}{40467}.
 }
\]
Indeed, linearity preserves the exact dual gap under convex mixtures, and
Hölder gives
\[
 y^{\mathsf T}(t-\mathbb E m)
 \le \|y\|_1\,\|t-\mathbb E m\|_\infty
 =\|t-\mathbb E m\|_\infty.
\]
The gap is invariant under dihedral images because m_d is a cyclic
distance average, and under vertex-sign gauges because principal minors
are unchanged by diagonal sign conjugation.

## 3. Program-mass TV corollary

For each distance d, let I_{i,d}={i,i+d} modulo 42 and define the bounded
balanced-label character
\[
 \phi_d([T])=\frac1{42}\sum_{i=0}^{41}
 (-1)^{|I_{i,d}\cap T|},\qquad |\phi_d|\le1.
\]
The exact program/principal-minor identity gives
\[
 \mathbb E_{w_R}\phi_d=m_d(R),\qquad
 \mathbb E_{u_{\rm bal}}\phi_d=t_d.
\]
Thus G=\sum_d y_d\phi_d obeys \(\|G\|_\infty\le\|y\|_1=1, while
\[
 \mathbb E_{u_{\rm bal}}G-\mathbb E_{w_\mu}G
 \ge \frac{2}{40467}.
\]
The total-variation dual inequality yields
\[
 \boxed{\operatorname{TV}(w_\mu,u_{\rm bal})\ge\frac1{40467}.}
\]
Equivalently, the trace distance (one-half trace norm convention) between
the associated dephased classical program-label registers is at least
1/40467. This is not a Choi-state trace-distance or channel diamond-norm
bound.

## 4. Scope and next step

This excludes one natural extension of the perfect-transfer seed family:
three independently mirrored contiguous blocks covering the 42-site path.
It does not exclude arbitrary three-segment couplings, arbitrary
multi-segment paths, the full continuous physical family, or the full
all-even-principal-minor moment problem. It is not a global no-go theorem.

The next useful extension is to derive a symbolic formula for the dual slack
as a function of block lengths and test whether the certificate extends to
four or more perfect-mirror blocks. In parallel, the 6,141-column
finite-pool dual should be priced continuously; a finite-pool certificate
must not be extrapolated to the continuum.
