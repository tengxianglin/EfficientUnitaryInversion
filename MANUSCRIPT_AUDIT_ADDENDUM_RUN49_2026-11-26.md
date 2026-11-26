# Run 49 — 6,149-column exact finite-pool certificate and continuous-pricing handoff

Date: 2026-11-26

## Repository inspection

- Default branch: `main`.
- Main HEAD before this run's new pricing files: `9df5080c0d55e3578f509a9866adee4071d0bfd6`.
- Latest reoptimization commit: [`9df5080`](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/9df5080c0d55e3578f509a9866adee4071d0bfd6), which added the 6,149-column diagnostic and independent Arb certificate.
- Recursive Git tree: 1,209 entries, not truncated.
- Open scientific tracks inspected: Issues #5, #7, #6, and #3. Issue #5 remains the central full-family convex-hull problem; Issue #7 records the unrestricted-SO matching construction and its physical-reachability obstruction; Issues #6 and #3 are manuscript/noise-normalization and Hamiltonian-classifier correctness tracks.

## Verified result: 6,149-column finite-pool theorem

GitHub Actions [45826172005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45826172005) completed with conclusion SUCCESS. All job steps passed, including the full 1,461-coordinate LP and independent Arb verification.

Exact pool:
- 22 base atoms;
- 6,101 fractional-grid atoms;
- 26 exact-rational gapped paths;
- 6,149 columns total.

Moment design:
- 21 second-order coordinates;
- 1,440 fourth-order dihedral orbits;
- 111,930 four-subsets;
- 1,313 independent moment rows;
- 1,314 equalities including normalization.

The floating HiGHS diagnostic reports:
- dual status optimal;
- primal status infeasible for this finite LP;
- target score approximately 0.16629302177823072;
- maximum candidate score approximately -0.06196490200679568;
- recomputed floating gap approximately 0.22825792378508636;
- maximum floating pricing-constraint violation approximately (6.0\times10^{-14}).

These floating numbers are discovery metadata, not the proof.

The independent Arb certificate pins the diagnostic SHA-256
`f5ed3c323420e6b7e11c147d8cc778aab05212b5bb9a52e373f842bc44f9184d`
and certifies:
- 106 exact-rational nonzero dual coefficients;
- exact scaled (L_1) norm 1;
- exact full-coordinate (L_1) norm 533;
- 128-bit Arb for 6,101 fractional-grid columns;
- 512-bit Arb for 22 base and 26 gapped columns;
- every one of the 6,149 column inequalities has a certified lower bound at least (1/5);
- minimum reported Arb lower-endpoint interval is centered near 0.2101530855777222, strictly above (1/5).

Consequences for mixtures supported on this exact pool:
[
\|b-Ap\|_\infty\ge 1/2665,
\qquad
\operatorname{TV}(w_p,u_{\rm bal})\ge 1/5330.
]
The TV bound concerns the balanced program-label/dephased-label register only, not Choi trace distance or channel diamond distance.

Evidence files:
- [diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_n21.json);
- [Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_arb_n21.json).

## Work completed in this run

Added a deterministic continuous-pricing pipeline for the newly certified 6,149-column dual:
- `search_ising_full_fourth_plus_twenty_six_gapped_n21.py`;
- `verify_ising_full_fourth_plus_twenty_six_gapped_escape_arb_n21.py`;
- `.github/workflows/eui-full-fourth-plus-twenty-six-gapped-search-n21.yml`.

The pricing script reconstructs the exact 106-term rational dual from the Arb certificate, pins both diagnostic and finite-certificate hashes, and searches connected and multi-segment open-path couplings. It includes frozen seed-pool starts, random connected starts, fractional-profile perturbations, random multi-segment starts, analytic Fréchet gradients, and a finite-difference gradient self-test.

The independent escape verifier reconstructs candidate couplings from frozen decimal strings as exact rationals, evaluates the rotation and score with 256-bit Arb, checks all 1,764 orthogonality entries and determinant one, and only labels an escape when the interval upper endpoint of target-minus-score is strictly negative.

A workflow-trigger correction was also committed: the workflow file is included in its own push-path filter so that the first run is triggered when the new workflow is installed.

Commits:
- search script initial: `5790fe9a15769b19686756ab0dd516e559e5051c`; pool-count fix: `3caa37d198573bf906ea6a502b0dd7112fcef3e1`;
- Arb escape verifier initial: `e96cd1629588f8c679972a9b33b26dedf3ce507a`; pool-count fix: `3aff95336236abd7eab1f51a487433d984c8e8ab`;
- workflow: `b0947ad2c91bc4b132279b65cfd2a033b02dce5e`; self-trigger correction: `dff7ded93ce99b9aa90c68657ec4f80ef89734fc`; concurrency-group correction: `2809a895268e3cc6369c2068d1d20067e487d85c`;
- theory note: `382bce0a629ac2f4424c1db054e6f4912e510d72`; audit: `3c0b496111220f1f0a1bd12a089afdfd4b12e662`.

Continuous-pricing workflow [45841951059](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45841951059) was observed queued at the end of this run. Its search and Arb outcome are therefore not yet claimed.

## Remaining blockers

- No exact positive physical ensemble matching all even-principal-minor coordinates at (n=21).
- No global separator valid for every allowed real coupling vector.
- Complete sixth-, eighth-, and higher-order moment control remains open.
- Program-label TV has not been bridged to Choi trace distance or channel diamond distance.
- No editable complete manuscript TeX/Bib source was found in the repository tree.

## Next highest-value action

Inspect workflow [45841951059](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45841951059). If it finds a candidate, accept it as a continuous physical escape only after the independent 256-bit Arb certificate passes. If it finds none, report only a finite multistart negative result; do not call it a global separator. Then decide whether to continue the cutting-plane sequence or pivot effort toward the exact positive-ensemble / DPP formulation tracked by Issue #7.
