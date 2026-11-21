# Certified obstruction to repairing the sixth moment by weights alone

Certified escape: [new physical columns and a low/sixth repair ensemble](THEORY_SIXTH_PRICING_ESCAPE.md).

2026-11-21; base `0e03837f17d3196856f28e4fc679fe34dbc03485`; Issue #3.
Follows the [sixth-order audit](THEORY_SIXTH_MOMENT_AUDIT.md).

## Computer-assisted finite-family theorem

Let F be the 1639 frozen physical seeds constructed in the previous
studies, together with their signed dihedral images and vertex-sign
gauges. Use the same exact binary64-rational coupling convention and
physical orbit averages as the preceding certificates. For **every**
positive normalized mixture supported in F,

\[
 G_{24}\le\frac{109}{500}=0.218
 \quad\Longrightarrow\quad
 E_6(0,1,2,3,4,5)>
 \frac{482748063}{250000000}=1.930992252>1.93.       \tag{1}
\]

Here G_24 is the complete all-row low-order scaled maximum, and
E_6(I)=(q_I-t_I)/|t_I| is the signed sixth residual. For this probe,
t_I=5/19721. In particular, neither this probe's absolute relative
error nor the maximum over the 256 tested sixth orbits can be <=1.93
while keeping G_24<=0.218 in this family.

This answers the fixed-pool repair question rigorously: mere reweighting
cannot remove the identified sixth-order error at this low-order budget.
The hypothesis is nonvacuous: the preceding canonical physical ensemble
has certified G_24<0.217405 and is supported in this same pool.

This is **not a global physical no-go**. It excludes no seed outside
this finite family, no different low-order error budget, and no more
general recovery construction. In particular it does not establish
nonexistence of an exact physical joint-uniform ensemble. The family is
a discovery pool, not the full continuous zero-edge physical promise.

## 1. One frozen rational functional

Write V(c) for all 21 second moments scaled by 41 and all 1440 fourth
orbit moments scaled by 533, and t for their exact uniform targets
(each coordinate is +/-1). Let Z(c) be the contiguous sixth orbit moment
scaled by 19721/5, with target u=1. A fixed rational vector y defines

\[
 L(c)=y\cdot V(c)-Z(c).
\]

The numerical LP used all 256 sixth probes, but its frozen sixth dual
has only the contiguous coefficient -1 nonzero. The certificate explicitly
checks this fact. There are 65 nonzero low-order coefficients. Their
complete rational decimal encoding is in
[evidence/fixed_pool_tradeoff_n21.json](evidence/fixed_pool_tradeoff_n21.json).
The exact identities used in the bound are

\[
 L_*:=y\cdot t-1=-\frac{28043981}{250000},\qquad
 \|y\|_1=\frac{101696293}{500000}.
\]

At 128-bit Arb precision, every one of the 1639 exact input seeds satisfies

\[
 L(c_j)<U=-\frac{316893}{2000}=-158.4465.           \tag{2}
\]

There are 3171 weighted principal determinants per seed (sizes 2,4,6),
for 5,197,269 determinant evaluations in total. The certificate regenerates
and fingerprint-checks the original couplings, hash-checks the appended
source parameters, and rebuilds every exact-input matrix exponential.
No floating moment matrix, LP status or optimizer is needed for (2).

All terms of L are cyclic/dihedral orbit averages and are invariant under
vertex-sign conjugation. Thus (2) includes the specified images/gauges.
Every normalized convex mixture of this family also has L_mix<U.
The largest-midpoint diagnostic is source column 1614, with enclosure

\[
 [-158.4466898299418537495989539683788\ \pm2.93\times10^{-32}].
\]

Its exact maximizing status is neither needed nor asserted; the common
strict bound U is checked separately for every seed.

## 2. Tradeoff proof and a concrete next search threshold

For any mixture with ||V_mix-t||_infinity<=b=109/500,

\[
 Z_{\rm mix}-1
  = y\cdot V_{\rm mix}-L_{\rm mix}-1
  > y\cdot t-b\|y\|_1-U-1
  = L_*-U-b\|y\|_1.
\]

Substitution gives exactly 482748063/250000000, proving (1).
The proof is deterministic rational algebra plus the interval inequalities
(2). LP optimality is not an assumption. A rounded or nonoptimal
functional would work equally well if these verified inequalities hold.

The functional supplies an executable necessary condition for expanding
the pool. If an enlarged mixture is to achieve G_24<=0.218 and the
contiguous absolute sixth error <=1, then

\[
 L_{\rm mix}\ge L_*-b\|y\|_1-1
 =-\frac{39378876937}{250000000}
 =-157.515507748.
\]

At least one seed in such a mixture must have L at least this value,
strictly above the old-family ceiling U. Finding a legal seed above
that threshold is necessary, not sufficient, for this repair goal.
Thus another probability solve over unchanged columns cannot solve it;
a coupling-pricing search must cross the displayed threshold, or the
low-order budget/goal must be changed. This conclusion does not assert
that the physical threshold is unattainable.

## 3. Numerical discovery, separate from the theorem

The study computes all 1461 low-order coordinates and the previously
frozen 256 sixth orbit coordinates on every pool seed. The sixth matrix
covers 21091 distinct six-sets per seed. It then solves the epigraph LP

\[
 \min_{p\ge0,\sum p=1,\epsilon\ge0}\epsilon,
 \quad |V^T p-t|\le0.218,
 \quad |Z_{256}^T p-u|\le\epsilon.
\]

HiGHS-IPM reports objective 1.931381887620645. Direct numerical evaluations
are 0.21800000000000286 for G_24 and 1.931381887620645 for the tested
sixth maximum. These values/weights are floating diagnostics. In
particular the tiny low-budget overshoot is not silently treated as an
exact feasible witness or certified upper bound on the optimum.

The dual coefficients are rounded to six-decimal rationals, and the
common threshold U is selected with a strict margin. The exact proof
then verifies them independently. The numerical matrix SHA256 is frozen;
its cache is optional reproducible intermediate data, not a proof input.
The theorem only requires the contiguous sixth probe, not completeness
of the 256-probe screen. It does not identify a global sixth maximum.
Generic LP duality/separation is standard and is not claimed as an
original EUI mathematical mechanism.

## 4. Reproduction and evidence

[study_ising_moment_tradeoff.py](study_ising_moment_tradeoff.py) is discovery.
[verify_ising_pool_tradeoff.py](verify_ising_pool_tradeoff.py) is the independent
fixed-functional interval verifier. The
[input](evidence/fixed_pool_tradeoff_certificate_input_n21.json) pins source
hashes, thresholds and precision; the
[proof transcript](evidence/fixed_pool_tradeoff_certificate_n21.json)
records every exact constant and the certified finite-family scope.

Environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0;
OPENBLAS_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1. No numerical cache
or LP is required for the certificate:

```
python verify_ising_pool_tradeoff.py
python -m unittest discover -s tests -v
```

For discovery, first generate the prior 1600-column full-feature cache
as documented in earlier notes, then:

```
python study_ising_moment_tradeoff.py --cache /tmp/eui-pool.npz --six-cache /tmp/eui-six-pool.npz --output /tmp/eui-tradeoff.json
```

The verifier reads the frozen study evidence, not an arbitrary rediscovery
output. The tested sixth-matrix SHA256 is
`9d5c0e6998f8f475762eabb7d0b372dd50d7e3b9add87baa37f705cdf1571b1f`.
Identical numerical trajectories on other solver/BLAS versions are not
required for the mathematical fixed-input bound.

**Next highest-value action:** extend the physical scalar pricing oracle
to the contiguous sixth determinant, optimize this frozen L over legal
zero-edge couplings, and interval-certify a column crossing the necessary
repair threshold. Append it and re-solve the complete low/selected-sixth
constraints. If a local optimizer fails, do not infer a global bound.
**Still blocked:** new physical columns enabling joint accuracy, exact
low-order feasibility, all higher-moment closure and full joint uniformity.
This finite-family theorem is not an original Nature Physics-level core
result or a claimed resolution of unrestricted inversion optimality.

Current main/recent Issues, relevant manuscript/appendices, research notes,
physical minor/parity identities and code/evidence were inspected.
No manuscript sources are present; the static-oracle moment-design study
remains distinct from broader manuscript robustness claims.
