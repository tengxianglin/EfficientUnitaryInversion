# EUI manuscript/evidence audit — Run 53 (2026-11-27)

## Repository and issue state

- Repository: `tengxianglin/EfficientUnitaryInversion`
- Default branch: `main`
- Inspected main head before this run's additions: `e705c3de4eb65f43009d382caed904cf8b62fa3f`
- Highest-leverage open scientific track: [Issue #5](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5), the finite-pool/full-continuous-family convex-hull gap.
- Also rechecked [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), which has an exact perfect-matching ensemble for unrestricted SO(42), a commutant-rank exclusion of one matching atom, and an adjacent-pair separator for the physically reachable matching-atom subfamily. That does not cover arbitrary non-matching cycle exponentials.

## 1. 6,153-column finite-pool theorem completed

Workflow [45880800772](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880800772) completed SUCCESS. The job log confirms that:
- dependency installation and compilation passed;
- block-minor, restricted spin-symmetry, and serialization regressions passed;
- the complete 1,461-coordinate LP ran;
- the independent Arb verifier completed successfully;
- both diagnostic and certificate were committed and uploaded.

The exact pool is 6,153 columns = 22 base + 6,101 fractional-grid + 30 exact-rational gapped paths. The complete feature system has 1,461 coordinates (21 second-order + 1,440 fourth-order orbits), 1,313 independent moment equations / 1,314 equalities including normalization. The exact rational dual has 116 nonzero coefficients, scaled L1 norm 1, full-coordinate L1 norm 533, and common Arb-certified rational column gap 1/5. Thus, for this exact finite pool only,
\[
\|b-Ap\|_\infty>1/2665,\qquad
\operatorname{TV}(w_p,u_{\rm bal})>1/5330.
\]
The TV is for the balanced program-label/dephased classical register, not Choi trace distance or channel diamond distance.

Evidence:
- [Diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_n21.json)
- [Independent Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_arb_n21.json)
- [Workflow](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880800772)
- [Evidence commit](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e705c3de4eb65f43009d382caed904cf8b62fa3f)

## 2. Scientific boundary

The certificate is finite-pool only. It does not prove a global converse for all real/nonnegative cycle couplings, does not settle the complete all-even-principal-minor positive-measure problem, and does not imply a Choi/diamond lower bound. The previous 6,151-column dual had two independent 256-bit Arb-certified continuous escapes (one with all 41 internal couplings strictly positive), which is why the new 6,153 dual is being priced over the continuous family before any global interpretation.

## 3. Changes made in this run

- Added a deterministic finite-multistart continuous-pricing search for the exact 116-term 6,153-column dual.
- Added an independent 256-bit Arb verifier for frozen rational escape candidates.
- Added a dedicated GitHub Actions workflow with pinned numerical/interval dependencies, gradient self-test, exact parent hashes, and race-safe evidence commit.
- Added a 6,153-column theory note with the theorem's exact scope and the next decision rule.

## 4. Current status and next action

The finite-pool theorem is proved by the committed exact rational dual and independent Arb certificate. The new continuous search is finite multistart discovery; its output is not yet known. The independent verifier, if a candidate exists, is the only step that can certify a particular escape.

Next: inspect the 6,153-dual continuous-pricing workflow. If it certifies a connected escape, document that this particular dual is not global and decide whether another finite reoptimization is scientifically useful. If it finds no escape, do not call that a global separation proof. In parallel, the higher-value theorem problem remains a positive physical ensemble for all even principal minors or a global inequality covering the full allowed cycle family.
