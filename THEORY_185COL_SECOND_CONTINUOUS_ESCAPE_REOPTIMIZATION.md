# Second continuous-path escape: 185-column reoptimization protocol

Date: 2026-11-23

## Established parent result

The 184-column / 2,113-row mixed-order LP has a strict rational dual certificate. The certificate proves a minimax lower bound only for its pinned 184 physical generators and pinned row design. It is not a global separator over the positive 41-edge open-path family.

The exact rational path in `THEORY_184COL_CONTINUOUS_PATH_DUAL_ESCAPE.md` is a second continuous-family escape. Its independent 128-bit Arb score is

\[
S_{184}(c)\in[558.5197275383090425573204756469618\pm6.20\times10^{-32}]>0.
\]

This is a strict counterexample to the global inequality for that particular dual. It is not a feasible ensemble and is not a full-family minimax result.

## New finite optimization problem

Let \(\mathcal P_{184}\) be the exact column ordering pinned by
`evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json`. Let \(c^{(2)}\) be the second Arb-certified continuous escape. Define

\[
\mathcal P_{185}=\mathcal P_{184}\cup\{c^{(2)}\}.
\]

The reoptimization keeps the row design unchanged:

- 1,461 complete second-/fourth-order rows;
- 645 selected sixth-order rows (311 original rows plus 334 cuts);
- seven selected eighth-order rows;
- 2,113 normalized residual coordinates in total.

The optimization is

\[
\min_{p\in\Delta(\mathcal P_{185})}\|A_{185}p-y\|_\infty.
\]

The new path is assigned column label 1642; the first continuous escape remains label 1641. The 1,641 canonical inventory keeps its frozen index range 0--1640.

## Reproducibility and independent branch verification

- Parent LP: `evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json`
- Parent dual: `evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json`
- First escape input: `evidence/continuous_path_dual_escape_arb_n21.json`
- Second escape input: `evidence/184col_continuous_dual_escape_arb_n21.json`
- Reoptimizer: `reoptimize_185col_second_continuous_escape.py`
- Above-cap dual verifier: `verify_185col_second_continuous_escape_dual_arb.py`
- Below-cap exact-mixture verifier: `verify_185col_second_continuous_escape_candidate_arb.py`
- Workflow: [45126903168](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45126903168)

The workflow rechecks the frozen seed-pool hash, orbit-enumeration regression, parent 184-column Arb certificate, and second-path Arb certificate before solving. It then branches:

1. If HiGHS finds an objective below \(1/3\), rationalize the probabilities and independently Arb-check all 2,113 pinned rows.
2. Otherwise, rationalize the dual and independently Arb-check all 185 physical columns.

The HiGHS objective is discovery evidence only. A selected-row candidate is not a complete sixth/eighth certificate; a finite-pool dual is not a continuous-family no-go.

## Status at note creation

**Pending.** Workflow 45126903168 has passed setup, dependency installation, seed/orbit checks, parent dual and escape verification, and Python compilation. The 185-column feature construction and HiGHS solve are running. No 185-column objective, candidate, or theorem is asserted in this note until the workflow's independent branch verifier completes.

## Scope

Even if the 185-column branch is certified, it will concern only the finite pool \(\mathcal P_{185}\) and the pinned 2,113-row mixed-order objective. It will not establish a global result over all positive couplings, complete sixth/eighth-order uniformity, or an operational Choi/diamond-norm guarantee.
