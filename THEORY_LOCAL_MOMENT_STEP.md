# Support deformation with full corrective weights

Follow-up: [all-row bounded linearization and analytic remainder bound](THEORY_LINEARIZED_MOMENT_STEP.md).

2026-11-21; base `47c88cf7ce88a39f209e38d3f2b06c469452f75c`; Issue #3.
Continuation of the [all-row norm audit](THEORY_BATCH_FOURTH_PRICING.md).

## Results and scope

**Finite numerical progress:** use the previous 1615-column all-row
minimax mixture, deform its four largest-weight physical seeds, retain
all old columns, and optimize all nonnegative weights again. The all-1461-row
scaled residual decreases from 0.23439547110533737 to 0.2262303074224086,
about 3.48%. The final weights directly evaluate to residual
0.22623030742241432. The four radius-.1 deformations receive total weight
0.2475036511040986; the smaller-radius candidates receive zero weight in
this returned solution. No uniqueness or necessity claim follows.

**Interval-certified scalar gains:** all twelve frozen rational candidates
increase one fixed rational moment functional relative to their exact
binary64 parent inputs. The smallest certified gain is approximately
9.60590224894e-5, strictly positive. These are existence inequalities for
legal connected, gapped physical columns, not interval-certified minimax
improvements or an exact uniform ensemble.

**Important local diagnostic:** a fixed dual ascent direction need not be
a descent direction for the original mixture's maximum residual. Among
67 numerically near-active rows, 17 have positive signed directional
slopes; the largest is about 0.12593076. This is a floating diagnostic of
near-active rows, not a proof identifying the exact active set. The
actual finite replacements at fixed old weights are recorded separately.
The achieved improvement uses retained old columns and corrective weights.
Replacing all four parents while keeping their old weights actually
increases the all-row residual at every tested radius:

| Radius | Fixed-weight replacement residual |
| --- | --- |
| .001 | 0.23452124997187682 |
| .01 | 0.2356347117328899 |
| .1 | 0.2524239598092343 |

The original value is 0.23439547110534373. This is an explicit finite
numerical example where every selected seed improves the frozen scalar
functional while the original mixture's maximum error worsens. It is
not an interval-certified counterexample for the maximum norm.

## Experiment definition

All physical conventions, target moments and dihedral averaging are as
in the preceding note: n=21, N=42, R=exp(A), upper path entries 2c_j,
lower entries -2c_j, and c_41=0. There are 21 second moments scaled by
41 and 1440 fourth moments scaled by 533. Every new internal edge is
checked nonzero, so the zero-edge parity compatibility guarantee applies.
No higher even moments are imposed in this experiment.

The all-row epigraph LP supplies weights p, objective g, and an optimal
floating dual y in scaled coordinates, with ||y||_1 approximately one.
The implementation explicitly evaluates y.t-max_j y.V_j and compares it
to the primal objective (defect about 3.30e-13); it also checks the actual
weighted feature residual. Six-decimal rounding then defines an exact
rational functional L, including both second and fourth coefficients.
Do not identify that rounded functional with the unrounded LP dual.

The selected columns, weights and scalar-gradient finite-difference
checks (coordinates 0,20,40) are:

| Parent | Old weight | Maximum scalar-gradient defect |
| --- | --- | --- |
| 630 | 0.06349207243818328 | 1.12e-11 |
| 573 | 0.05334876705410939 | 1.24e-9 |
| 264 | 0.04969099928119884 | 8.94e-11 |
| 726 | 0.04789668521550936 | 4.40e-11 |

Set u_j=p_j grad L(c_j)/M, where M=max_{j,k}|p_j grad_k L(c_j)|.
For radii h=.001,.01,.1, append round_6(c_j+h u_j), preserving the zero
closing edge. This adds twelve columns, giving 1627 in total. Rounding
can change the step by at most 5e-7 per edge; the exact frozen rational
parameters, rather than the ideal unrounded step, enter the certificate.
All old columns remain available. The final LP can change every weight;
it is not a joint nonlinear optimization over all 67 old support points.
No matched-cost comparison with sequential column generation was run.

Inputs, selected weights, gradients' check defects, candidate complete-feature
hashes and explicit final weights are frozen in
[evidence/local_moment_step_n21.json](evidence/local_moment_step_n21.json).
The parent's encoding is deliberately distinct from the candidate's:
`Fraction.from_float(float(parent_string))` recovers the exact original
binary64 seed, checked against `seed_pool()`; candidate decimal strings
are interpreted directly as exact rationals. The interval verifier
rebuilds four parent and twelve candidate exponentials at 192 bits and
proves each L(candidate)-L(parent)>0. No saved floating feature vectors,
LP status or gradient accuracy are needed for those inequalities.
See [the interval transcript](evidence/local_moment_step_verification_n21.json).

## Why scalar improvement is not a minimax descent theorem

For fixed weights, define scaled residual r_i(c)=sum_j p_j phi_i(c_j)-t_i
and G(c)=max_i |r_i(c)|. If G(c)>0 and the exact active set is
I={i:|r_i(c)|=G(c)}, smoothness of the matrix exponential and determinants
gives the one-sided derivative

\[
 D G(c)[u]=\max_{i\in I}\operatorname{sign}(r_i(c))
                  \sum_j p_j D\phi_i(c_j)[u_j].
\]

This follows by the directional derivative of a finite maximum: inactive
rows have a strict gap and cannot determine the derivative at zero;
the derivative of |r_i| is sign(r_i) Dr_i for active, nonzero r_i.
Thus every active signed slope must be negative for strict first-order
descent at fixed weights. Improving a weighted dual combination does
not impose this condition on each active row. This standard maximum-rule
argument is not claimed as a new mathematical theorem.

The implementation computes all-feature Jacobian-vector products using
D exp(A)[E], then determinant cofactors, without inverse principal-block
assumptions. A central-difference check of each complete 1461-feature JVP
has maximum defect below 3.41e-11. At tolerance 1e-8, the observed signed
slopes range from -0.25455497 to +0.12593076, with 17 positive rows.
These facts warn against interpreting a frozen dual direction as the
exact derivative of the optimized value when weights/duals can change.
They do not establish local optimality, global nonexistence, or the
exact active set. The finite LP reweighting result remains the evidence
of numerical improvement.

Diagnostic values and actual fixed-weight replacements are in
[evidence/local_moment_direction_audit_n21.json](evidence/local_moment_direction_audit_n21.json).
Generic LP duality and support deformation are discovery methods, not
claims of literature-wide EUI novelty.

## Reproduction and next action

Python 3.12.14 / NumPy 2.3.5 / SciPy 1.17.0 / python-flint 0.9.0;
OPENBLAS_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1. The fixed scalar proof
needs no feature cache or LP:

```
python verify_local_moment_step.py
```

For discovery or the all-feature directional audit, generate the prior
cache as documented in the preceding note (its fingerprint is checked):

```
python local_ising_moment_step.py --cache /tmp/eui-pool.npz --output /tmp/eui-local.json
python audit_local_moment_direction.py --cache /tmp/eui-pool.npz
python verify_local_moment_step.py --cache /tmp/eui-pool.npz
python -m unittest discover -s tests -v
```

The audit reads the frozen experiment in evidence; it does not read an
arbitrary newly discovered output. BLAS/solver-dependent rediscovery is
separate from verification of fixed exact inputs. Final weights are
floating approximate candidates, not certified exact designs. The final
positive residual alone is not a general impossibility theorem.

**Still blocked:** full fourth-order feasibility and higher moments for
joint uniformity. **Next highest-value action:** construct a local minimax
linearization using all active signed moment rows, rather than one fixed
dual gradient, with bounded physical coupling changes and full corrective
weight updates. Test its predicted descent against all 1461 actual
moments; certify any accepted finite designs or separating bounds separately.

Current main/recent Issues, theory/code/evidence and the
[manuscript/appendices](https://arxiv.org/html/2506.20570v1) were inspected.
No manuscript source files are present. The static-oracle design promise
remains separate from broader manuscript robustness and unrestricted
query-optimality claims. This update does not establish journal readiness.
