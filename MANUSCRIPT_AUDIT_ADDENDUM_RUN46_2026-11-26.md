# Run 46 — 6,147-column certificate audit and continuous-pricing handoff (2026-11-26)

## Repository state inspected

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Prior evidence commit: [`d5d31ac08186d36efef9961b65279beb12b0e8dc`](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d5d31ac08186d36efef9961b65279beb12b0e8dc).
- Latest code/workflow commits at this audit: `b4f7938` (certificate wording), `caefc0f` (discovery provenance wording), `ec46d8c` (6,147-dual search), `5fa1b4f` (independent escape verifier), `3f96792` (verifier count message), and `076b8b0` (pricing workflow).
- Relevant open tracks: Issue [#5](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5), Issue [#7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), plus correctness audits #3 and #6. This run prioritizes #5 because the new full-second/fourth-order dual is now finite-pool certified and can be priced against the continuous physical family.

## 6,147-column finite-pool result

The original workflow [45805694896](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45805694896) completed successfully. Its job passed compilation, block-minor/spin-symmetry/serialization regressions, the full 1,461-coordinate LP, and independent Arb pricing.

The pinned pool has:
- 22 base atoms;
- 6,101 corrected fractional single-open-path grid atoms;
- 24 exact-rational gapped paths (22 inherited from the certified 6,145-column pool and two new escapes from the 6,145-column dual);
- 6,147 columns total.

The design has 21 second-order coordinates and 1,440 fourth-order dihedral orbits (111,930 four-subsets), 1,313 independent moment rows, and 1,314 equalities including normalization.

The independently generated certificate reports:
- 111 nonzero exact-rational dual coefficients;
- exact scaled dual norm `||D^{-1} y||_1 = 1`;
- exact full-coordinate norm `||y||_1 = 533`;
- common rational column gap `1/5`;
- minimum Arb lower endpoint approximately `0.2204310259488606080...`;
- moment-residual lower bound `1/2665`;
- program-label TV lower bound `1/5330`.

The TV conclusion concerns the balanced program-label distribution / corresponding dephased classical register, not Choi trace distance or channel diamond distance.

## Evidence-quality correction

A source audit found stale copied prose in the first 6,147 certificate generator output: the machine fields correctly said 22 base atoms, 6,101 grid atoms, 24 gapped atoms, and 6,147 columns, while the generated `proof`/ `scope` strings incorrectly said 6,143 columns, 24 base atoms, and 20 gapped paths. This was a reporting inconsistency, not a failed Arb inequality: the hosted job had in fact priced 22 + 6,101 + 24 = 6,147 columns.

Corrected:
- `verify_ising_full_fourth_plus_twenty_four_gapped_arb_n21.py`: proof/scope now state 6,147 columns, 22 base atoms, and 24 gapped paths; inherited/new path provenance and error messages are corrected.
- `discover_ising_full_fourth_plus_twenty_four_gapped_n21.py`: parent and inherited-path counts now correctly state 22, and the two new escapes are attributed to the 6,145-column dual.

The corrected full workflow is [45822057718](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45822057718). At audit time it had passed compilation and all deterministic regressions; the LP was still running, with independent Arb certification pending. No corrected rerun success is claimed here.

## Continuous pricing handoff for the new 6,147 dual

Added:
- `search_ising_full_fourth_plus_twenty_four_gapped_n21.py`;
- `verify_ising_full_fourth_plus_twenty_four_gapped_escape_arb_n21.py`;
- `.github/workflows/eui-full-fourth-plus-twenty-four-gapped-search-n21.yml`.

The search reconstructs the exact 111-term dual from the 6,147 finite certificate, then performs deterministic connected and multi-segment open-path pricing. Seed: `202611262037`; up to 512 frozen seed-pool starts, 512 random connected starts, 256 fractional-profile perturbations, 512 random multi-segment starts, and all 24 pinned gapped paths; 16 optimized starts per class, L-BFGS-B with analytic Fréchet gradients, 180 iterations maximum. Search is discovery only. Any escape is frozen as exact decimal/rational input and independently checked at 256-bit Arb, including all 1,764 orthogonality entries and determinant one.

The pricing workflow is deliberately path-filtered on the search/verifier/evidence inputs (not on its own workflow-file creation). It has not yet been observed running at this audit. Once the corrected 6,147 certificate is committed, touch the search script only if the evidence commit did not trigger the pricing workflow; the pricing script pins both diagnostic and certificate hashes and refuses stale results.

## Proof boundary

- **Proved, finite scope:** strict second-/fourth-order separation for exactly the pinned 6,147-column pool.
- **Already proved separately:** the 6,145-column dual has two continuous physical escapes, one connected with all 41 internal couplings positive and one multi-segment; these refute only that particular 6,145 dual.
- **Not yet tested:** continuous pricing of the new 6,147-column dual.
- **Not proved:** a global separator for all cycle/path couplings, a positive physical ensemble matching every even principal minor at (n=21), complete sixth/eighth/higher-order control, or an operational program-label-to-Choi/diamond bridge.

## Next action

Complete [workflow 45822057718](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45822057718), verify that the regenerated certificate prose agrees with its 6,147 / 22 / 6,101 / 24 machine counts, then run the new deterministic continuous-pricing workflow and independently certify any candidate escape. A no-escape multistart result must remain explicitly non-global.


## Manuscript / appendix check

The public manuscript was opened directly as [arXiv:2506.20570v1](https://arxiv.org/pdf/2506.20570), dated 25–26 June 2025, 13 pages. The PDF itself maps Appendix A to inversion proofs and the F2 Gaussian-elimination construction, Appendix B to robustness numerics, Appendix C to complex conjugation, Appendix D to PQComb-generated conjugation protocols, and Appendix E to transpose decompositions / modified QURA. No separate supplementary-information file is linked from the repository tree; the recursive tree has 1,200 entries and no `.tex`, `.bib`, `.bbl`, `.pdf`, Word, or archive manuscript/supplement files. The current EUI moment/finite-pool research is not part of that public v1 manuscript, and no claim is made that the paper text has been updated.
