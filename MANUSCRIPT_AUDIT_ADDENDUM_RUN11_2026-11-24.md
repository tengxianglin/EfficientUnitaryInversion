# Manuscript and claim-scope audit addendum — 2026-11-24 (run 11)

## Source rechecked

The repository still has no tracked manuscript `.tex`, `.bib`, compiled `.pdf`, or separate supplement source. The source inspected for this audit is the public arXiv HTML version:

- [Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians](https://arxiv.org/html/2506.20570v1), version dated 25 June 2025.
- Authors: Yin Mo, Tengxiang Lin, Xin Wang.
- Appendix B (HTML lines 292–313) defines a support-mismatch perturbation and reports 10,000 independently sampled random Hamiltonians, with **average Choi-state fidelity** at selected noise strengths.

The manuscript's Appendix B is finite Monte Carlo average-fidelity evidence. It does not establish a worst-case-over-Hamiltonian channel bound, a worst-case-over-input diamond bound, or a bridge from the current moment LP residuals to per-instance Choi/diamond error.

## Paper-central theorem map

The tracked note [THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md) states an exact conditional full diamond-minimax formula for the fixed six-query architecture, allowing arbitrary non-radial and orientation-dependent stochastic logical-Pauli correction tables. Its hypothesis is one legal physical ensemble with exactly uniform diagonal program masses in both parity sectors. The repository records computer-assisted exact positive ensemble certificates at n=5 and n=7. At admissible long rings n>=21, the required joint uniform ensemble is not yet constructed or ruled out.

The all-even-principal-minor target remains
\[
\mathbb E\det R_{I,I}
=(-1)^{v(I)+k}\frac{\binom nk}{\binom{2n}{2k}},
\qquad |I|=2k.
\]
A selected-row LP, finite-pool dual, low-order approximation, or escape from a particular dual is not a substitute for an exact positive solution of this full system or a global physical-family obstruction.

## Latest mixed-order finite-pool result and its escape

The 196-column / 2,113-row design is a finite-pool mixed-order diagnostic: 1,461 complete second-/fourth-order rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. Its exact rational 128-bit Arb dual proves
\[
\min_{p\in\Delta_{196}}\|A p-y\|_\infty
\ge 0.41973861353658526\ldots>\frac13.
\]
This is a theorem only for the exact 196 listed columns and 2,113 listed rows; sixth/eighth-order rows are not exhaustive.

The same 196-column dual has now been escaped by an explicitly certified **strictly positive equal-coupling path**:
\[
c_1=\cdots=c_{41}=t_*,
\qquad
t_* = \frac{1535392895240590633}{500000000000000}
=3070.785790481181266>0.
\]
At 128-bit Arb precision,
\[
S_{196}(e^{t_*K_*})
\in[0.3637338868622431662555343998069\pm6.07\times10^{-32}]>0.
\]
This refutes global separation by that particular 196-column dual. It does not invalidate the finite-pool theorem and does not prove full continuous-family feasibility or infeasibility.

Evidence:
- [196-column finite-pool theorem](THEORY_196COL_2113ROW_FOURTH_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md)
- [Uniform-path escape theorem](THEORY_196COL_UNIFORM_TORUS_DUAL_ESCAPE.md)
- [128-bit finite-time Arb certificate](evidence/196col_uniform_ray_time_arb_n21.json)
- [128-bit torus Arb certificate](evidence/196col_uniform_torus_arb_n21.json)
- [Exact dense-torus theorem](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)

## Current executable follow-up

The explicit finite-time path above is appended as column 1654. A reproducible 197-column / 2,113-row reoptimization has been committed and launched:

- [Reoptimizer](reoptimize_197col_uniform_ray_escape.py)
- [Workflow](.github/workflows/eui-reoptimize-197col-uniform-ray.yml)
- [Run 45418660688](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45418660688)

At the time of this addendum, the workflow has passed Python compilation, the eighth-order enumeration regression, the uniform-path torus regression, and the 193-column ancestor re-certification; the 194-/195-/196-column re-certification and 197-column LP are still running. No 197-column result is claimed.

If the LP is above 1/3, its floating dual is only a discovery candidate and requires a new exact-rational dual plus independent Arb pricing of all 197 columns. If it is below 1/3, the rationalized primal requires interval verification on every pinned row and a complete 63,133-orbit sixth-order audit.

## Separate 6,129-column low-order track

The 6,129-column full-second/fourth workflow has produced a diagnostic JSON with 6,129 candidates, but its status remains explicitly `floating_full_fourth_6125_column_separator_candidate_not_arb_certified`. It is not a theorem and is not used to support any manuscript claim in this addendum. The metadata-consistent rerun 45398176444 failed at the artifact-commit step after the LP step completed; the earlier 45397929610 run committed the diagnostic. A new exact-rational/Arb certificate is required before any finite-pool claim is made for this expanded pool.

## Manuscript claim discipline

1. Keep the 196-column theorem attached to its exact 196-column pool and 2,113-row design.
2. Keep the uniform-path result attached to the particular 196-column dual it escapes.
3. Do not call the 2,113-row design a complete sixth/eighth-order certificate.
4. Do not infer Choi-state trace distance or channel diamond distance from the program-label TV/moment bounds without a separate operational theorem.
5. Do not describe Appendix B's average over 10,000 random Hamiltonians as a worst-case guarantee.
6. No manuscript-source edit is claimed because manuscript and supplement source files are not tracked in this repository.
