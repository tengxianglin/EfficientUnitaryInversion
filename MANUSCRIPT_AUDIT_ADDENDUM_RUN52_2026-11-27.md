# EUI manuscript/evidence audit — Run 52 (2026-11-27)

## Repository and issue state

- Repository: `tengxianglin/EfficientUnitaryInversion`
- Default branch: `main`
- Previous inspected HEAD before this run's additions: `f163790724dd4bd132591a7413b3809adb02088d`
- Highest-leverage open scientific track: [Issue #5](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5), the finite-pool/full-family convex-hull gap.
- Also rechecked the active context of Issue #7 (physical reachability of the perfect-matching ensemble) and Issue #6 (Appendix B noise normalization). Neither supersedes the immediate #5 certification/pricing handoff.

## 1. 6,151-column finite-pool certification

The corrected 6,151-column workflow [45861230625](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45861230625) completed with SUCCESS. The job log confirms that compilation, deterministic regressions, the complete 1,461-coordinate LP, independent Arb certification, evidence commit, and artifact upload all succeeded.

The committed certificate is `evidence/ising_full_fourth_plus_twenty_eight_gapped_arb_n21.json` at commit `f163790724dd4bd132591a7413b3809adb02088d`. It certifies exactly 6,151 columns = 22 base + 6,101 fractional-grid + 28 exact-rational gapped paths; 1,461 full coordinates; 1,313 independent moment equations / 1,314 equalities including normalization; 118 exact-rational dual coefficients; exact scaled L1 norm 1; exact full-coordinate L1 norm 533; and common rational column gap 1/5. The certificate's scope remains this exact finite pool, not the continuous physical family.

## 2. Continuous pricing of the newly certified dual

Added a deterministic search, an independent 256-bit Arb escape verifier, and a dedicated workflow:

- `search_ising_full_fourth_plus_twenty_eight_gapped_n21.py`
- `verify_ising_full_fourth_plus_twenty_eight_gapped_escape_arb_n21.py`
- `.github/workflows/eui-full-fourth-plus-twenty-eight-gapped-search-n21.yml`

The search reconstructs the 118-term rational dual from the Arb certificate and prices connected and multi-segment open paths. It uses a new deterministic seed, includes all 28 pinned gapped paths as starts, and checks the analytic Fréchet gradient by finite differences. The independent verifier rebuilds candidate rotations from exact rational couplings and checks all orthogonality entries and determinant one before deciding whether the dual is escaped.

Workflow [45879531992](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45879531992) is currently in progress. Setup, pinned dependency installation, and Python compilation have passed; the continuous pricing search is running; the Arb stage is pending. No 6,151-dual continuous escape or no-escape result is claimed yet.

## 3. Manuscript and supplementary-material audit

The repository still has no editable manuscript/supplementary source (`.tex`, `.bib`, or independent supplementary source) in the inspected research tree. The public manuscript remains [arXiv:2506.20570](https://arxiv.org/abs/2506.20570). This run does not alter the published manuscript or claim that the finite-pool result is a global EUI converse.

## 4. Changes made in this run

- Added deterministic 6,151-dual continuous-pricing search.
- Added independent 256-bit Arb verifier.
- Added pinned GitHub Actions workflow; current run ID 45879531992.
- Added `THEORY_6151COL_FINITE_POOL_DUAL_AND_CONTINUOUS_PRICING_N21.md`.
- Added this Run 52 audit note.

## 5. Proof boundary and next action

**Proved:** the rational dual separates every column in the exact 6,151-element pinned pool with common gap at least 1/5.

**Finite numerical discovery:** the LP and continuous multistart optimizer are floating-point discovery tools; only the independent Arb verifier can certify a specific frozen physical escape.

**Not proved:** separation of the full continuous gapped family; existence or nonexistence of a positive physical measure matching every even principal minor; a complete all-order physical converse; or a moment-residual-to-Choi/diamond bound.

Next action: inspect workflow 45879531992. If an escape is Arb-certified, state precisely that this particular dual is not global and then decide whether one more finite-pool reoptimization has value. If no escape is found, do not claim a continuum theorem. Independently, continue the complete positive-ensemble and operational-bridge derivations rather than treating an expanding sequence of finite duals as the paper's final result.


## 6. Continuous pricing of the 6,151 dual — completed after initial audit

Workflow [45879531992](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45879531992) completed SUCCESS. It evaluated 1,820 deterministic starts and passed the analytic-gradient finite-difference check (maximum defect (1.947994265893982\times10^{-10})). The independent 256-bit Arb verifier certified two escapes:
- connected, all 41 internal couplings strictly positive (minimum approximately (10^{-6})), with target-minus-score ([-33.1812592736687668\ldots\pm6.65\times10^{-73}]<0);
- multi-segment with internal cut ({32}), minimum positive coupling (10^{-8}), with target-minus-score ([-24.3211293146278320\ldots\pm4.64\times10^{-71}]<0).

Both checks included all 1,764 orthogonality entries and determinant one. This refutes only the 6,151 dual as a global separator; the finite-pool theorem remains valid.

## 7. 6,153-column continuation status

The two new exact-rational paths are now appended, producing 6,153 columns (22 base + 6,101 grid + 30 gapped). The first attempt [45880306574](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880306574) stopped before the LP at a copied parent-status label check. The parent is the 6,151 diagnostic, so the correct expected status is `floating_full_fourth_6151_column_separator_candidate_not_arb_certified`, not the child 6,153 label. This metadata-only guard was fixed in commit [2733809](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/273380954425bedc055bd61d02098443c40f9304). Corrected workflow [45880550567](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880550567) has passed setup, dependency installation, compilation, and structural regressions; the 6,153-column LP is running and independent Arb certification is pending. No 6,153-column theorem is claimed yet.
