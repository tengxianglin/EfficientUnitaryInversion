# A certified n=21 low-moment ensemble and strict improvement

2026-11-21; base `32da6c3dacd9fc175920e782c5b4d3c1776a4611`;
Issue #3. Follow-up to the [all-row linearization study](THEORY_LINEARIZED_MOMENT_STEP.md).

## Computer-assisted theorem

There is an explicit positive, normalized physical ensemble at n=21,
formed from 70 zero-edge seed orbits, whose complete second/fourth
Majorana principal-minor moments satisfy

\[
 G_{\rm new}:=\max\left\{
  \max_{1\le d\le21}41|m_d-m_d^*|,
  \max_{o\in\mathcal O_4}533|q_o-q_o^*|\right\}
 <\frac{217405}{1000000},
\]

where m_d*=(-1)^(d+1)/41, q_o*=(-1)^v/533 and there are 1440 fourth
orbits. For a specified preceding 67-seed-orbit ensemble,

\[
 G_{\rm old}>\frac{226230}{1000000}.
\]

Consequently these exact ensembles obey

\[
 G_{\rm old}-G_{\rm new}>\frac{353}{40000}=0.008825,
 \qquad
 \frac{G_{\rm old}-G_{\rm new}}{G_{\rm old}}
 >\frac{1765}{45246}>0.039.
\]

This upgrades one previously floating improvement to a strict
computer-assisted result. It is an existence/comparison theorem for
these two specified ensembles, not a theorem that the finite-pool LP
optimum or its optimizer is exact. No optimizer status or Taylor bound
is used in the proof.

It remains an **approximate low-moment** construction. It does not give
zero residual, higher even moments, full uniform program masses,
off-diagonal program moments, a diamond/channel error bound, or the
conditional long-ring minimax extension. The certified 3.90% relative
improvement refers only to G as explicitly defined above.

## 1. Exact inputs and normalization

The discovery inputs live in five frozen evidence JSONs ending with
`linearized_moment_step_n21.json`. The new certificate input
[evidence/full_low_moment_certificate_input_n21.json](evidence/full_low_moment_certificate_input_n21.json)
records their SHA256 hashes, the original 1600-coupling fingerprint,
precision, target bounds and the selected old lower-bound coordinate.
Those hashes are verified before any proof calculation.

The column indexing is inherited from the prior studies: original pool
0..1599; first directed column 1600; iterative columns 1601..1608; batch
1609..1614; support deformations 1615..1626; all-row linearized candidates
1627..1638. No cache of floating feature vectors is required.

The convention is uniform for this certificate: **every** source
coupling is converted to its reconstructed binary64 value and then to
an exact rational with Fraction.from_float. This includes appended
columns originally discovered using decimal rounding. We certify these
explicit canonical exact realizations, rather than silently identifying
binary64 and decimal-rational numbers. Each selected input has 42
couplings, its closing coupling exactly zero, and all 41 internal
couplings nonzero.

For each source floating weight w_j, set a_j=Fraction.from_float(w_j),
and define p_j=a_j/sum_l a_l using exact rational arithmetic. The verifier
checks every a_j>0 and sum p_j=1 exactly. It normalizes the old and new
ensembles separately. The complete 70 new rational probabilities and
both exact raw normalization sums are recorded in
[evidence/full_low_moment_certificate_n21.json](evidence/full_low_moment_certificate_n21.json).
This is not a claim that the raw floating LP weights sum to exactly one.

## 2. Physical orbit averaging and parity scope

For each seed, form A with A_{j,j+1}=2c_j and A_{j+1,j}=-2c_j,
and R=exp(A). Each real nearest-neighbor coupling vector has the legal
Ising-field/edge realization established in the
[physical dihedral reduction](THEORY_ODD_CYCLE_ORBIT_DESIGN.md).
The physical ensemble averages every seed over all 84 signed dihedral
images of the 42-cycle, with probability p_j/84 each. It therefore has
at most 5880 atoms counting multiplicity; 70 is the number of seed
orbits, not a claim of only 70 unsymmetrized Hamiltonians.

Signed permutation conjugation permutes principal index sets; the two
vertex-sign factors cancel in every principal determinant. Thus the
moment of any pair at a fixed distance is m_d and the moment of any
four-set in orbit o is q_o after averaging. All target signs are constant
on these even-cardinality orbits. Certifying all 21+1440 orbit rows
therefore covers every second/fourth index set of this symmetrized
ensemble. It does not cover all higher-cardinality program probes.

All seeds have an exact zero edge; signed dihedral images retain a zero
edge. The [gap/gauge lemma](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md)
therefore makes the program masses identical in the two physical parity
sectors, so the same low-moment bounds apply jointly. Here zero-edge
refers to the coupling graph; no spectral energy-gap assumption is made.
The ensemble is a physical witness distribution, not a new inversion
circuit or a resource/optimality theorem.

## 3. Complete interval verification

At 128-bit Arb precision the verifier reconstructs each selected exact
rational-input 42-by-42 matrix exponential. For each of the 70 new seed
orbits it computes:

- all 21 cyclic second-minor averages, including the antipodal row;
- all 111930 principal four-by-four determinants;
- their sums/averages over the complete 1440 dihedral orbits.

This is 7,835,100 fourth determinants in total, with no sampled probes
or dropped hierarchy rows. All averages and positive weighted sums use
ball arithmetic with exact rational factors. For every coordinate it
then verifies that its scaled residual lies strictly between
-217405/1000000 and +217405/1000000. A common strict bound is the
certificate; identifying an exact maximizing coordinate is unnecessary.
The transcript's largest-midpoint label is descriptive, not a proof
that this row uniquely maximizes the exact norm.

For the old ensemble only a lower bound is required. Coordinate 1357
(zero-based full-feature indexing), fourth orbit represented by
(0,7,14,21), is recomputed for all 67 old seeds with exact normalized
probabilities. Its absolute scaled residual is certified strictly
greater than 226230/1000000. This single row lower-bounds G_old. We do
not assert a certified all-row upper bound for the old ensemble.

The upper/lower comparison proves strict improvement regardless of the
floating LP objective, discovery Jacobian, or preceding loose Taylor
bound. Normalizing exact rational weights and canonicalizing couplings
are part of the proof inputs. The resulting theorem is a finite
computer-assisted result, not a claim that all couplings have been
searched or that every nearby ensemble has the same bound.

## 4. Reproduction and remaining blocker

Python 3.12.14 / NumPy 2.3.5 / SciPy 1.17.0 / python-flint 0.9.0
were used (SciPy is imported by shared modules; Arb evaluates every proof
exponential). With the
repository present, no optimizer, LP solution, floating feature cache,
Jacobian, or saved rotation matrix is needed:

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_full_low_moment_certificate.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

The verifier regenerates/hash-checks source couplings, creates exact
positive probabilities, and rebuilds every exponential and determinant.
Progress goes to stderr; the JSON proof transcript goes to stdout.
The source certificate is [verify_full_low_moment_certificate.py](verify_full_low_moment_certificate.py).
The preceding Taylor analysis remains correct; its conservative constants
are no longer the evidence for this specific strict improvement.

**Still blocked:** an exact second/fourth design, all higher even moments
for full joint uniformity, and the consequent long-ring minimax theorem.
The present bound remains about 21.74% of the target magnitude in the
specified low-moment coordinates; it is not a comparable bound on
individual program probabilities or operational inversion error.
**Next highest-value action:** run a bounded sequence of accepted all-row
updates with measured/model gain checks, then re-certify a materially
better ensemble using this complete verifier. If that search plateaus,
seek an analytic physical constraint; numerical stagnation alone cannot
establish nonexistence. The current result supplies rigorous evidence,
not an original Nature Physics-level core claim.

Current main, recent/open Issues, relevant theory/code/evidence and the
[manuscript and appendices](https://arxiv.org/html/2506.20570v1) were
inspected. No manuscript source files are present. The static-oracle
moment-design promise remains distinct from broader robustness and
unrestricted query-optimality claims. Standard interval arithmetic,
convex normalization and symmetry averaging are not asserted as new
mathematical discoveries.
