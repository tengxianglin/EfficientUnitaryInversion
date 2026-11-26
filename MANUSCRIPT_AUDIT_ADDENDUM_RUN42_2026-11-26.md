# EUI manuscript/research audit — Run 42 (2026-11-26)

## Repository and issue selection

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Run 41's latest experiment commit was `d1c4187843ec8df77472cb4a11f40b11b6a044dc`.
- Open tracks rechecked: #5 (finite-pool/full-family gap), #7 (physical reachability), #6 (Appendix B noise normalization), and #3 (type-1.2 classifier correctness). #5 remains the highest-leverage active scientific track because the 6,143-column full-second-/fourth-order reoptimization has produced a new dual candidate and is at its independent interval-certification gate.
- The Run 41 audit and public-manuscript status were re-read. The repository's existing audit reports no editable `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplementary source. No formal manuscript text was changed in this run.

## Run 41 workflow result — precise failure diagnosis

Workflow [45756549750](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45756549750) completed:
- dependency installation;
- Python compilation;
- deterministic block-minor, restricted spin-symmetry, and serialization regressions;
- the 6,143-column HiGHS reoptimization.

The independent Arb verifier then stopped at its parent-diagnostic status guard, before evaluating any candidate-column interval. The verifier incorrectly expected the 6,141-column *parent diagnostic* to have the 6,143 status label. The actual parent diagnostic correctly has:
`floating_full_fourth_6141_column_separator_candidate_not_arb_certified`
and `candidate_count = 6141`. Its separate, hash-pinned parent certificate has status:
`arb_certified_finite_6141_column_full_fourth_plus_eighteen_gapped_separator`.

The failure was therefore a second verifier bookkeeping error, not a failed Arb inequality and not a mathematical counterexample.

## Run 42 repair

Changed exactly one expected string in `verify_ising_full_fourth_plus_twenty_gapped_arb_n21.py`: the parent diagnostic guard now expects the 6,141 diagnostic status while retaining the 6,141 candidate-count check.

- Repair commit: [8dcd436b47199bb2490a9aa6e7f2a45d66552de2](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8dcd436b47199bb2490a9aa6e7f2a45d66552de2).
- The push modifies a path listed in `.github/workflows/eui-reoptimize-6143-full-fourth.yml`, so it triggers a fresh full reoptimization/verification run.
- No LP coefficients, candidate atoms, moment definitions, or interval tolerances were changed.

## Evidence classification

**Finite-pool results already proved:** the parent 6,141-column separator remains independently Arb-certified for exactly its pinned pool and 1,461 second-/fourth-order coordinates.

**New 6,143-column discovery only:** the committed diagnostic reports an optimal HiGHS dual, 103 nonzero coefficients, scaled-(L_1) upper bound approximately 1, target score approximately 0.2233125201903, maximum candidate score approximately -0.0105977885712, and recomputed floating gap approximately 0.2339103087617. The primal feasibility LP reports infeasible. These are floating-point discovery diagnostics only.

**Not yet certified:** the 6,143-column dual. Workflow 45756549750 did not reach any Arb pricing loop. The repaired verifier has not yet been observed completing in a fresh workflow.

**Not proved:** a separator for the full continuous physical family; existence of a positive (n=21) ensemble matching all even principal-minor moments; complete sixth/eighth-order control; or a Choi/diamond lower bound from program-mass TV.

## Next highest-value action

Inspect the fresh workflow triggered by commit `8dcd436`. If it independently certifies all 22 base, 6,101 fractional-grid, and 20 exact-rational gapped columns, freeze the resulting rational dual and certificate. Then perform continuous pricing against that new dual. A finite-pool certificate must remain explicitly finite-pool; any continuous escape must be frozen and independently Arb-certified before it is used to extend the candidate pool.
