# EUI manuscript/research audit — Run 41 (2026-11-26)

## Repository and issue audit

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- HEAD before this audit note: `11a253b3893aa001d5df83a82780d86a3e209e51`.
- Recursive tree at the preceding experiment commit: 1,169 entries, `truncated=false`.
- Open scientific/correctness tracks rechecked: #5 (finite-pool/full-family gap), #7 (physical reachability), #6 (Appendix B noise normalization), and #3 (type-1.2 classifier correctness). Issue #5 remains the highest-leverage current track because a 6,143-column LP discovery and independent interval verification are actively being advanced.
- README and the latest audit note were inspected. The recursive tree still contains no editable manuscript or supplementary source in `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` format. The public manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, arXiv:2506.20570v1. No formal manuscript text was edited.

## Rechecked 6,141-column parent and escape chain

The 6,141-column parent certificate remains pinned and reports:
- 22 base atoms, 6,101 fractional-grid atoms, 18 exact-rational gapped paths;
- 1,461 second-/fourth-order features (21 second-order plus all 1,440 fourth-order dihedral orbits);
- 1,313 independent moment equations / 1,314 equalities including normalization;
- Arb status `arb_certified_finite_6141_column_full_fourth_plus_eighteen_gapped_separator`, with common dual gap (1/5).

The separate 256-bit Arb escape certificate remains `arb_certified_6141_dual_general_gapped_escape`, with connected and multi-segment paths. These refute only that particular 6,141-column dual on those continuous paths; they do not invalidate its finite-pool theorem.

## Run 40: 6,143-column discovery result

The first hosted 6,143-column run, [45745598002](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45745598002), completed the LP discovery step successfully and committed its diagnostic at [7fe64039df2192aba7b7b0796c3344d7a28d5c15](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/7fe64039df2192aba7b7b0796c3344d7a28d5c15).

The diagnostic is explicitly labelled `floating_full_fourth_6143_column_separator_candidate_not_arb_certified`. It reports:
- HiGHS dual solve: optimal;
- normalized scaled-(L_1) upper bound: 0.999999999999999;
- target score: 0.22331252019032463;
- maximum candidate score: -0.01059778857121127;
- threshold: -0.010597788571348389;
- recomputed floating gap: 0.233910308761673;
- maximum floating pricing-constraint violation: (1.3711948243511074\times10^{-13});
- 103 nonzero dual coefficients;
- the primal feasibility LP reports infeasible.

These are floating discovery diagnostics only. The independent Arb verifier failed before evaluating any column because its initial status guard mistakenly expected the 6,141-column status string rather than the 6,143-column status string. This is a verifier bookkeeping bug, not a failed interval inequality and not a mathematical counterexample.

## Run 41 repair and current hosted verification

The verifier status pin and stale “eighteen paths” docstring/count message were corrected in commit `11a253b3893aa001d5df83a82780d86a3e209e51`.

The corrected workflow [45756549750](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45756549750) has passed:
- pinned dependency installation;
- Python compilation;
- block-minor, spin-symmetry, and serialization self-tests.

At the time of this audit, the hosted 6,143-column reoptimization step is still running; independent Arb certification is pending. The run must not be described as successful until the verifier certifies all 6,143 columns.

A small non-mathematical metadata discrepancy remains in the discovery script's diagnostic prose: its human-readable `scope` field still says “6,141 columns total” although the machine fields and actual pool are 6,143. This should be corrected after the active workflow finishes, to avoid cancelling/restarting the current run.

## Evidence classification and next action

- **Previously interval-certified:** the finite 6,141-column full-second-/fourth-order separator and the two continuous escape paths for that particular dual.
- **Floating discovery only:** the new 6,143-column LP dual candidate and its reported 0.2339103 gap.
- **Verified in Run 41:** the stale verifier status guard is fixed; current hosted compile and deterministic regressions pass.
- **Still pending:** independent 512-bit/128-bit Arb pricing of all 6,143 columns and publication of the certificate.
- **Not proved:** a global separator for every allowed coupling; a positive (n=21) ensemble matching all even principal-minor moments; complete sixth/eighth-order control; or a Choi/diamond lower bound from program-mass TV.
- **Next highest-value action:** complete workflow 45756549750. If Arb passes, record the exact rational dual, certified common gap, residual/TV corollaries with their finite-pool scope, then continuously price this new dual. If Arb fails, preserve the failure and diagnose the first interval obstruction before making any theorem claim.
