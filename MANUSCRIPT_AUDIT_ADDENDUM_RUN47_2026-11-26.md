# Run 47 — corrected 6,147-column certificate and continuous-pricing rerun (2026-11-26)

## Repository state inspected

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Main head before this run's change: `125845d249d8eddbf82570c32efc0ba6d3112987`.
- Latest preceding commits include the 6,147-column certificate record, public-manuscript audit, deterministic continuous-pricing search, independent Arb escape verifier, and its workflow.
- Open scientific issues inspected: #5 (finite-pool/global physical-family gap), #7 (physical reachability of the perfect-matching ensemble), and #6 (Appendix B noise normalization). #5 is the highest-leverage active thread because a corrected 6,147-column certificate is now available and its new dual can be priced continuously.
- Recursive Git tree at the inspected head: 1,200 entries, not truncated. The repository contains no editable `.tex`, `.bib`, `.bbl`, manuscript PDF, Word, or supplementary archive. The public manuscript remains arXiv:2506.20570v1; no manuscript text was changed.

## Corrected 6,147-column finite-pool result

Hosted workflow [45822057718](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45822057718) completed successfully. The job passed compilation, deterministic block-minor/spin-symmetry/serialization regressions, the full 1,461-coordinate LP, and independent Arb certification.

The exact pool is:
- 22 base atoms;
- 6,101 fractional single-open-path grid atoms;
- 24 exact-rational gapped paths;
- 6,147 columns total.

The design contains 21 second-order coordinates and 1,440 fourth-order dihedral orbits (111,930 four-subsets), with 1,313 independent moment rows and 1,314 equalities including normalization.

The corrected Arb certificate reports:
- 111 nonzero exact-rational dual coefficients;
- exact scaled dual norm `||D^{-1}y||_1 = 1`;
- exact full-coordinate dual norm `||y||_1 = 533`;
- common rational column gap `1/5`;
- minimum certified Arb lower endpoint approximately `0.2204310259634118986356653...`;
- moment-residual lower bound `1/2665`;
- balanced program-label TV lower bound `1/5330`.

Thus every probability mixture over this exact pinned 6,147-column pool obeys the stated finite-pool bounds. The TV statement concerns the balanced program-label distribution / dephased classical label register, not Choi trace distance or channel diamond distance.

A prior generated proof/scope string had stale pool counts. The corrected run confirms the proof text and machine fields now agree on 22 / 6,101 / 24 / 6,147. This was a provenance/reporting correction, not a change to the LP or the finite-pool inequality.

## Continuous pricing launched

The pricing script now records the stable label `run47_2026-11-26_reprice_corrected_6147_certificate`. This is a provenance-only addition; the random seed, objective, candidate generation, optimization, and Arb verifier are unchanged.

- Commit: [6ccac3f00899a24979b07b1ee26e65fa71b64791](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6ccac3f00899a24979b07b1ee26e65fa71b64791).
- Workflow: [45824486175](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45824486175).
- Search seed: `202611262037`.
- Candidate families: frozen seed-pool starts, connected positive open paths, fractional-profile perturbations, multi-segment open paths, and all 24 pinned gapped paths.
- Search: deterministic finite multistart with L-BFGS-B and analytic Fréchet gradients.
- Independent verifier: 256-bit Arb; candidate decimal couplings are parsed as exact rationals, all 1,764 orthogonality entries and determinant one are checked, and the exact rational 111-term dual is repriced.

Workflow [45824486175](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45824486175) completed successfully. It evaluated 1,816 initial candidates (512 frozen seed-pool, 512 random connected, 256 fractional-profile, and 523 multi-segment including pinned paths), optimized 16 starts per class, and passed a gradient finite-difference self-test with maximum absolute defect (1.643934988138085\\times10^{-10}).

The independent 256-bit Arb certificate proves two exact-rational escapes from the 6,147 dual:
- Connected: all 41 internal couplings strictly positive; minimum (19999999999999999/20000000000000000000000\\approx10^{-6}); target-minus-score interval ([-27.2455780603332145899570\\ldots\\pm6.53\\times10^{-73}]<0).
- Two-segment: one internal cut at edge 35; minimum positive coupling (10^{-8}); target-minus-score interval ([-26.1266278136225508061655\\ldots\\pm3.35\\times10^{-71}]<0).

Both exact-rational paths passed all 1,764 Arb orthogonality consistency checks and determinant-one interval checks; exact skew-symmetry of the generator gives the structural (SO(42)) property. These witnesses refute extending this particular 6,147-column dual unchanged to the connected/general-gapped family. They do not invalidate its finite-pool theorem or settle global convex-hull membership.

A formal scope note is now committed: [THEORY_6147COL_FINITE_POOL_DUAL_AND_CONTINUOUS_ESCAPE_N21.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_6147COL_FINITE_POOL_DUAL_AND_CONTINUOUS_ESCAPE_N21.md).

## Proof boundary and next action

- **Proved, finite scope:** strict second-/fourth-order separation for exactly the pinned 6,147-column pool.
- **Proved counterexamples to that dual's global extension:** one connected and one two-segment exact-rational physical path, each independently Arb-priced below the 6,147 dual target.
- **Not proved:** a separator for all real cycle/path couplings; a positive physical ensemble matching every even principal minor at n=21; complete sixth/eighth/higher-order control; or a program-label-to-Choi/diamond operational bridge.

The two escapes have been appended to the 24 inherited gapped paths, giving a 6,149-column pool (22 base + 6,101 fractional grid + 26 gapped). New discovery and independent Arb-verification files are committed:
- `discover_ising_full_fourth_plus_twenty_six_gapped_n21.py`
- `verify_ising_full_fourth_plus_twenty_six_gapped_arb_n21.py`
- [workflow 45826172005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45826172005)

At the time of this audit update, compilation and deterministic block-minor/spin-symmetry/serialization regressions had passed; the 6,149-column LP was still running. No 6,149-column theorem is claimed until independent Arb certification completes.

Issue #5 was updated in comments [7192731781](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5#issuecomment-7192731781) and [7192928947](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5#issuecomment-7192928947).
