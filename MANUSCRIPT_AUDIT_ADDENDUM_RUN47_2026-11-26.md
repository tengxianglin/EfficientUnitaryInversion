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

At the time of this audit, dependency installation and compilation passed; the pricing step was running. No continuous escape or global no-escape claim is made until the transcript and Arb result are inspected. A no-escape finite multistart outcome is not a continuum proof.

## Proof boundary and next action

- **Proved:** strict second-/fourth-order separation for exactly the pinned 6,147-column pool.
- **Not proved:** a separator for all real cycle/path couplings; a positive physical ensemble matching every even principal minor at n=21; complete sixth/eighth/higher-order control; or a program-label-to-Choi/diamond operational bridge.
- **Next:** inspect workflow 45824486175; if an escape is certified, append the exact rational path and reoptimize; if no escape is found, retain the result strictly as finite multistart evidence and move to a genuinely global analytic pricing bound or positive-ensemble construction.

Issue #5 was updated in comment [7192731781](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5#issuecomment-7192731781).
