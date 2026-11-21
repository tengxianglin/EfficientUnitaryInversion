# Complete sixth-order interval certificate for the physical repair ensemble

2026-11-22; base `72521b5e8971e8ed92a1be4203da01c7fad1f887`; Issue #3.
This closes the interval-upper-bound gap identified by the
[complete floating audit](THEORY_COMPLETE_SIXTH_AUDIT.md).

## Computer-assisted theorem and scope

For the same exact 83-seed-orbit physical ensemble defined in the
[repair certificate](THEORY_SIXTH_PRICING_ESCAPE.md),

\[
 \boxed{G_6:=\max_{|I|=6}
 \frac{|\mathbb E\det R_{I,I}-t_I|}{5/19721}<\frac{31}{20}=1.55,}
 \qquad t_I=(-1)^{v(I)+3}\frac5{19721}.
\]

This now covers **every** sixth-order index set, not just the original
256 probes. The previously certified complete low-order bound G_24<.218
continues to hold for these same exact probabilities/couplings. The
zero-edge physical symmetry/parity lemmas make both statements valid
in both physical parity sectors after the declared dihedral averaging.

The result is a rigorous approximation bound through degree six for one
specified ensemble. It is not exact target matching, full program-mass
uniformity, an operational inversion/channel/diamond error bound, a
sixth-order optimum, or a general theorem for other Hamiltonians.
The independent orders 8,10,...,20 remain uncontrolled.
Jacobi complementarity supplies an automatic corollary: R is orthogonal
with det R=1, so det R_I=det R_(I^c). At n=21 the targets also obey
t_I=t_(I^c). Consequently the bounds for orders 2/4/6 also hold for
orders 40/38/36 respectively, while orders 0/42 are trivial. This does
not close any of the remaining independent orders. In particular the relative
sixth error bound still exceeds one; this is a rigor milestone, not the
missing exact all-moment construction or Nature Physics-level core claim.

## 1. Exact physical inputs

The [new proof input](evidence/complete_sixth_certificate_input_n21.json)
pins the source hashes of the preceding exact ensemble definition and
probability transcript. The canonical reconstruction checks every source
hash, exact positive probability, exact sum of one and its agreement
with the recorded 83 probabilities. Old couplings retain their exact
binary64-rational convention; the new seed retains its exact decimal-
rational convention. These conventions are not silently interchanged.

Every selected seed has 41 nonzero internal edges and an exact zero
closing edge. Each real vector gives a legal static field/Ising-edge
Hamiltonian in the established physical model. An exact uniform average
over the 84 signed dihedral images gives at most 6972 atoms counting
multiplicity. Principal minors are invariant under the vertex-sign
factors and permuted by the cycle symmetry. The ensemble moment of any
six-set is therefore its orbit average. The zero-edge gap/gauge identity
ensures the same program masses in the two physical parity sectors.
No spectral energy-gap assumption is made, and the ensemble is a
mathematical witness distribution rather than an added inversion circuit.

## 2. Complete coverage and interval test

The existing exact canonical-gap enumeration gives 63133 distinct sixth
dihedral orbits. Independent Burnside counting gives
(5247312+55860)/84=63133. Their explicitly enumerated group images sum
to all binom(42,6)=5245786 six-sets; shorter orbits/stabilizers are not
approximated by a generic size of 84.

For each orbit representative I the verifier computes, with Arb balls,

\[
 q_I=\sum_{j=1}^{83}p_j\frac1{|\mathcal O(I)|}
       \sum_{J\in\mathcal O(I)}\det\exp(A(c_j))_{J,J},
 \qquad e_I=(q_I-t_I)/(5/19721).
\]

Every acceptance test is the definite interval inequality
-31/20 < e_I < 31/20. Uncertain/overlapping comparisons are not accepted.
Since the set is finite and every orbit passes, the maximum is strictly
below 31/20. An exact maximizing orbit is not identified or needed.
Largest-midpoint entries in the transcript are diagnostics only.
A separate 128-bit recomputation of the eight selected shard diagnostic
rows is enclosed by their reported 64-bit balls. Its contiguous probe
also gives the strict lower bound 7743/5000=1.5486 on G_6; hence
1.5486<G_6<1.55. A probe lower-bounds the maximum without proving it is
an exact maximizer. The cross-check is recorded in
[evidence/complete_sixth_extrema_crosscheck_n21.json](evidence/complete_sixth_extrema_crosscheck_n21.json).

There are 435400238 six-by-six determinant evaluations. Each worker
reconstructs all 83 exact-input 42-by-42 matrix exponentials itself;
no floating moment vector, optimizer, LP result or cached rotation
matrix is a proof input. Floating conversion is used only in the
hash-checked canonical source reconstruction and diagnostic midpoint
selection; all moment evaluations and accepted inequalities use balls.

## 3. Working precision and parallel proof structure

The working precision is 64 **Arb midpoint bits**, with outward error
radii carried through rational conversion, matrix exponentials,
determinants, averages and weighted sums. It is not a binary64
floating determinant pass with an assumed tolerance. Exact source
rationals are enclosed even when they cannot be represented exactly
at the working precision. A two-orbit development check includes the
near-threshold contiguous probe and passes at this precision.

The method follows established ball arithmetic, e.g. Johansson,
[Arb: Efficient Arbitrary-Precision Midpoint-Radius Interval Arithmetic](https://arxiv.org/abs/1611.02831),
IEEE Transactions on Computers 66(8), 1281–1292 (2017). The standard
interval method and process parallelism are not asserted as new
mathematical or EUI mechanisms.

Eight independent spawned processes verify contiguous, disjoint ranges
of the sorted canonical orbit keys. Each process:

- checks the pinned source hashes and reconstructs exact probabilities;
- creates its own interval rotations at the declared precision;
- evaluates every assigned orbit and verifies the strict inequalities;
- returns its start/stop range, exact set count, key SHA256 and input SHA256.

The parent checks signatures, key hashes, sorted range continuity,
complete coverage and the total count 5245786 before returning
`complete: true` and the full bound. A failed worker raises an error;
it cannot yield a completed certificate. The `--limit` development mode
reports `complete: false` and a null full-bound field when a proper
prefix is checked. Such a partial output is not a full certificate.

The [proof transcript](evidence/complete_sixth_bound_n21.json) contains all
shard ranges/counts/hashes and the common strict bound. Shard midpoint
labels do not establish an exact global maximum or solver optimality.
This is a computer-assisted theorem using the stated arithmetic library,
not a formal proof-assistant development.

## 4. Reproduction and remaining scientific blocker

Python 3.12.14 / NumPy 2.3.5 / SciPy 1.17.0 / python-flint 0.9.0.
The shared modules import SciPy, but every proof exponential is evaluated
by Arb. No numerical feature cache is required:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python verify_complete_sixth_bound.py --workers 8
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python verify_complete_sixth_bound.py --workers 1 --limit 2
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python verify_sixth_shard_extrema.py
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

The second command is only a development/prefix check. Worker counts
between one and eight are supported; a different count partitions the
same full problem differently and therefore changes the shard transcript,
not the theorem. The published default uses eight. Proof success is the
complete coverage and strict inequalities, not a requirement that
formatting/diagnostic midpoints match on every platform.

The previous complete G_24 proof is reused with pinned identical input
probabilities. The earlier finite-family obstruction and its certified
physical escape remain valid; this result strengthens the new witness's
sixth coverage, not the old family's allowed support. Earlier notes that
list this full-sixth interval upper bound as pending are historical;
this certificate supplies it for the exact declared ensemble only.

**Next highest-value action:** improve the coupled low/sixth design using
new active dual directions and the complete sixth orbit audit as a
separation oracle after updates. Test selected degree-eight directions
before making any beyond-sixth claim. **Remaining blockers:** exact
low-order feasibility, higher-even-moment closure and full joint
uniformity/minimax. No positive finite residual or failed local search
would prove global physical nonexistence.

Latest main/recent Issues, proof/code/evidence, manuscript/Appendix B and
the primary ball-arithmetic reference were inspected. No manuscript
sources are present. The static-oracle moment-design scope remains
separate from the paper's broader robustness/unrestricted-query claims.
