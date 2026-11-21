# A six-column pricing batch and an explicit approximate mixture

Follow-up: [support deformation and all-row corrective weights](THEORY_LOCAL_MOMENT_STEP.md).

Date: 2026-11-21. Base: `6a7d4f6b54f0343fe711eeb681738357dd728d8c`.
Issue #3; continuation of [iterated pricing](THEORY_ITERATED_FOURTH_PRICING.md).

## Question and outcome

Can several seeds priced against the same separating functional give
useful simultaneous progress toward the physical n=21 second/fourth
moment target? This run executes the preceding note's proposed batch test.

**Certified individual existence:** all six frozen rational seeds exceed
the same exact target by more than one at 192-bit Arb precision. All are
connected gapped physical paths, with non-Pauli programs by the existing
classification. **Finite numerical outcome:** the batch increases the pool
from 1609 to 1615 and decreases its retained/scaled minimax residual from
0.22447532395677383 to 0.22113318589786912 (about 1.49%). The full reduced
feasibility LP still reports status 2, infeasible. This is not an exact
finite-pool exclusion or a physical no-go theorem.

An additional approximate-primal solve constructs explicit nonnegative
numerical weights, rather than relying on the dual objective alone.
The verifier checks normalization and evaluates both retained and all
1461 feature residuals. The numerical primal and dual objectives must
agree within 1e-7. These floating weights are an approximate candidate,
not a certified exact moment design.

## All-row norm audit: the approximation metric matters

The exact row reduction is valid for deciding zero residual. It is not
an isometry for approximate errors. In this concrete numerical study:

| Objective / mixture | 1609 columns | 1615 columns |
| --- | --- | --- |
| Best retained/scaled residual | 0.22447532395677383 | 0.22113318589786912 |
| Best all-1461-row/scaled residual | 0.23672570645671698 | 0.23439547110533737 |

The retained-optimal 1615-column mixture has all-row scaled residual
0.36927944038017757, about 67% above its retained residual. Reoptimizing
all rows reduces that to 0.23439547110534373 (direct evaluation), with
solver objective 0.23439547110533737. Thus the all-row objective improves
by about 0.98%, rather than the retained objective's 1.49%. These are
finite floating LP results, not interval-certified optima.

The retained-optimal mixture has 66 nonzero weights; four batch columns
receive total probability about 0.0004357320. The all-row optimum has
67 nonzero weights; batch probability is about 0.0003190986. The saved
weights are concrete numerical candidates, not uniqueness/necessity
claims. The maximum unscaled residual actually increases from about
0.00319290 to 0.00363026 between the two all-row optimizers; improvement
of one chosen scaled norm does not imply improvement of every norm.

The all-row formulation retains every second/fourth coordinate and uses
its own epsilon slack. It does not change the exact moment hierarchy or
its correctness. It reveals an approximation-quality distinction that
the earlier note warned about but had not quantified. Prefer this
all-row metric for future approximate-design comparisons. This is a
project-specific numerical audit, not a claim that norm dependence or
LP row scaling is a new mathematical discovery.

Frozen all-row weights and residual checks are in
[evidence/full_moment_norm_audit_n21.json](evidence/full_moment_norm_audit_n21.json).
Reproduce with:

```
python audit_ising_full_moment_norm.py --cache /tmp/eui-pool.npz
```

## Fixed experiment and proof inputs

Use the same convention as the preceding note: N=42, A_{j,j+1}=2c_j,
A_{j+1,j}=-2c_j, R=exp(A), closing coupling c_41=0. The features are all
21 cyclic second moments m_d and 1440 dihedral fourth moments q_o. The
exact target is m_d*=(-1)^(d+1)/41 and q_o*=(-1)^v/533.

The previous saved `next_direction` defines a fixed rational functional
L=sum b_d m_d+sum a_o q_o, with exact target

\[
 L_*=-83988271/106600000.
\]

No dual is recomputed between the six pricing starts. Start zero is the
first old-pool maximizer within 1e-8 of the largest floating score.
The other starts perturb old appended seeds numbered 0,2,4,6,7 by
independent normal vectors with scales .2,.5,1,2,4, using RNG 202611211034.
All 41 internal couplings vary freely; the closing edge stays zero.
L-BFGS-B has maxiter=80, ftol=1e-12, gtol=1e-8. No reflection constraint is
imposed. Every initial vector, optimizer stopping message, rounded final
coupling vector and complete-feature fingerprint is frozen in
[evidence/batch_fourth_pricing_n21.json](evidence/batch_fourth_pricing_n21.json).
Iteration-limit exits are not treated as global maxima.

| Start | Rounded candidate's numerical L |
| --- | --- |
| 0 | 11.996238424636143 |
| 1 | 11.638124058743509 |
| 2 | 17.068876169341557 |
| 3 | 12.475003879412654 |
| 4 | 22.54199354772716 |
| 5 | 22.905512793042316 |

The independent proof interprets the six-decimal parameters and direction
coefficients as exact rational numbers, rebuilds the matrix exponential
with Arb, and verifies L(c)-L_*>1 for each candidate. It does not use the
saved binary64 feature vector. All internal couplings are checked nonzero.
For a connected-path pure Pauli program, the previous classification
would force R=+/-I. The corresponding exact functional value is
sum b_d+sum a_o, disjoint from each witness interval; hence each program
is non-Pauli. The zero edge retains the existing compatibility guarantee
between physical parity sectors. No non-Clifford requirement is inferred.

## What the approximate mixture checks

For the retained index set J from the exact hierarchy, define
V_j=(s_i W_{ji})_{i in J}, t=(s_i target_i)_{i in J}, with s_i=41 for
second moments and 533 for fourth moments. The added LP is

\[
 \min_{p\ge0,\;\sum_jp_j=1,\;\epsilon\ge0}\epsilon,
 \qquad -\epsilon\le\sum_jp_jV_{ji}-t_i\le\epsilon.
\]

It is the approximate primal of the previous l1-normalized dual. Its
returned weights are saved in the verification transcript, with explicit
column indices: 0..1599 are the original pool, 1600 the first directed
seed, 1601..1608 the eight iterative seeds, and 1609..1614 this batch.
All nonzero numerical weights are retained, without a small-weight cutoff.
The evaluator checks nonnegativity and normalization, recomputes the
residual from the complete feature matrix, and compares it to the
objective and to the independent dual solve. It also reports the total
weight assigned to the new batch.

The all-feature scaled residual is reported separately. Removing dependent
rows preserves exact feasibility but changes an approximate infinity norm;
one must not identify the retained residual with every moment's error,
or with a diamond/channel norm. Neither the LP equality nor a large
pricing score proves that all six added columns are necessary. A matched
single-column ablation was not run, so no speedup over sequential pricing
is asserted. The modest 1.49% change, despite large scalar pricing margins,
shows why scalar pricing success alone is insufficient as a progress metric.

## Reproduction, evidence and next step

Use Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0.
Set OPENBLAS_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1. The proof alone
requires no pool cache or optimizer solve:

```
python verify_batch_moment_pricing.py
```

For full numerical replay, regenerate the previous cache if needed:

```
python verify_ising_fourth_moments.py --search --cache /tmp/eui-pool.npz
python verify_batch_moment_pricing.py --cache /tmp/eui-pool.npz
```

The old cache feature SHA256 must equal
`3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5`.
All new complete-feature hashes are checked individually. The frozen
[evidence/batch_fourth_pricing_verification_n21.json](evidence/batch_fourth_pricing_verification_n21.json)
keeps interval witnesses and floating replay/weights in separate fields.
To repeat discovery, with optimizer trajectories potentially dependent on
BLAS/solver versions, run:

```
python batch_ising_moment_pricing.py --cache /tmp/eui-pool.npz --output /tmp/eui-batch.json
python -m unittest discover -s tests -v
```

**Still blocked:** complete fourth-order feasibility and all higher even
moments needed for full joint uniformity. The long-ring minimax extension
remains conditional. The explicit approximate mixture now provides a
concrete state from which to inspect active constraints and seed weights.
**Next highest-value action:** identify its active residual constraints
and jointly optimize the positively weighted physical seeds and weights,
then compare against further one-direction pricing under a matched budget.
Any improvement must be measured by the complete moment system; exact
feasibility needs certified positive weights and higher-moment closure.

The latest main, recent/open Issue progress, relevant theory/code/evidence,
and [manuscript and appendices](https://arxiv.org/html/2506.20570v1) were
rechecked. No manuscript source files are in this repository. This remains
a static-oracle moment-design study; it does not establish the broader
robustness claims or Nature Physics readiness. Generic column generation
and LP duality are not claimed as original EUI mechanisms.
