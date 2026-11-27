# EUI research audit — Run 56 (2026-11-27)

## Repository and issue selection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- Starting HEAD: 9842f64a8783daf24059de4c5521687f2f8c2c92.
- Recent main commits were inspected through the Run 55 N=8 period-two mixture theorem and its successful Arb evidence commit.
- Open research issues rechecked: #5 (full physical-family convex hull), #7 (physical reachability / positive ensembles), #6 (Appendix B noise normalization), and #3 (Hamiltonian classifier correctness).
- Issue #7 remains the highest-leverage target for this run: the N=42 period-two construction matched all pair moments and four quartic translation orbits, while its fifth witness was support-specifically mismatched. The decisive next experiment was to search for a new positive support that matches the fifth witness without dropping the four existing targets.

## New N=42 five-quartic candidate

A deterministic HiGHS feasibility search over 100,000 strictly positive period-two candidates, sampled uniformly from [0,100]^2 with seed 351, found a 36-base-atom support satisfying:
- all 30 independent pair equations (the 31st follows from the exact row-norm identity);
- five quartic orbit equations;
- normalization.

The five quartic representatives are:
- [0,1,2,3]
- [0,3,10,15]
- [0,2,4,6]
- [0,10,20,30]
- [0,2,21,23]

The first four have 42 distinct translates each; the last has 21. The five translation orbits are pairwise disjoint, giving 189 distinct quartic coordinates.

Each base atom (a,b) is symmetrized with its one-site translate (b,a), producing an explicit 72-atom positive ensemble. The 36 frozen base pairs are all strictly positive. The binary64 selected-equation residual is 2.926825448668069e-14; the floating support weights range from approximately 2.8786574e-4 to 9.0536672e-2. These are discovery diagnostics only.

The frozen exact-decimal support is:
- evidence/n42_period_two_five_quartic_atoms.json

The independent verifier:
- reconstructs the unique exact-real weights from a 36x36 system using exact-rational coupling inputs and 256-bit Arb;
- checks the determinant interval excludes zero and every weight exceeds 1/10000;
- checks all 861 pair principal-minor coordinates;
- checks all 189 distinct translated quartic coordinates for the explicitly symmetrized ensemble.

The hosted workflows are:
- .github/workflows/eui-n42-period-two-five-quartic.yml
- .github/workflows/eui-n42-period-two-six-quartic.yml

The five-orbit 256-bit Arb verifier passed in PR workflow run 45930804656; its exact certificate is committed at e2c83f63eb0c924e66a05a8e38db6a44f81ec93d. The follow-up six-orbit search below further strengthens this result.

## Relation to Run 55

The N=8 period-two arbitrary-mixture theorem remains correctly scoped to N=8 and the period-two subfamily. The N=42 candidate does not follow from that theorem. It is an independent construction at N=42.

The 36-base-atom candidate includes the former mismatched witness [0,2,21,23] while retaining the four previous representatives; its 72-atom symmetrization was Arb-certified for 861 pairs and 189 quartic coordinates. A second 100,000-candidate search then found a 37-base-atom support with one additional orbit [6,13,14,30]. Its 74-atom symmetrization was independently certified at 256 bits for all 861 pair coordinates and 231 distinct quartic coordinates. The six orbit sizes are 42,42,42,42,21,42.

## Manuscript and supplementary-source audit

The public manuscript remains Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians, arXiv:2506.20570v1. The repository's recent research tree and manuscript-related paths were checked; no editable tracked TeX/Bib source or independent supplementary source was found. No formal manuscript text was changed. Issue #6 remains open for the Appendix B normalization description and the unregenerated QuAIRKit-backed robustness table.

## Changes and verification status

Changed:
- evidence/n42_period_two_five_quartic_atoms.json
- verify_n42_period_two_five_quartic_ensemble_arb.py
- .github/workflows/eui-n42-period-two-five-quartic.yml
- THEORY_N42_PERIOD_TWO_FIVE_QUARTIC_ENSEMBLE.md

Verified locally in the analysis:
- the 100,000-candidate LP is feasible;
- its support has 36 strictly positive base atoms;
- the floating 36x36 selected system has condition number about 1.74e4;
- the five symmetrized quartic targets are met to binary64 residual below 3e-14;
- the five distinct full translation orbits contain 189 unique subsets.

Verified by hosted 256-bit Arb:
- five-orbit certificate: 36x36 determinant interval excludes zero; minimum weight exceeds 1/10000; all 861 pair and 189 quartic coordinates pass;
- six-orbit certificate: 37x37 determinant interval excludes zero; minimum weight exceeds 1/10000; all 861 pair and 231 quartic coordinates pass;
- all base couplings are strictly positive, and the one-site symmetrizations have 72 and 74 atoms respectively.

The six-orbit certificate has minimum exact coupling 27757624598893029/5000000000000000, minimum weight approximately 3.52877614818587e-4, and determinant interval centered at -6.65787118905551e-42 with radius 6.21e-109. The verifier passed in workflow run 45931260609. A stale five-orbit scope string in the first six-orbit evidence serialization was corrected in commit c57dba80805be1a1d127ae7a3521e2ce61452913; the numerical certificate and 231-coordinate count were unchanged.

## Next highest-value action

Continue from the certified six-orbit design: add quartic orbit constraints incrementally, and for the first infeasible finite pool extract a dual and run continuous pricing before making any global claim. The six-orbit result is still only a partial fourth-order design, not a complete physical ensemble or operational channel bound.


## Six-orbit certificate and final run status

- Six-orbit verifier: verify_n42_period_two_six_quartic_ensemble_arb.py.
- Frozen support: evidence/n42_period_two_six_quartic_atoms.json.
- Certified evidence: evidence/n42_period_two_six_quartic_ensemble_arb.json.
- Six-orbit CI: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45931260609 (SUCCESS).
- Six-orbit evidence commit: c14b86d7ccee852b06f98cfce9323bf01866144f, with scope metadata corrected in c57dba80805be1a1d127ae7a3521e2ce61452913.
- PR #9 merged as 6ac328517830524f93b511faa3821ee977e6f029.

Final verified result: a 74-atom strictly-positive period-two ensemble matches all 861 pair principal-minor coordinates and 231 fourth-order coordinates in six full translation orbits. The exact-real weights are reconstructed from the frozen rational couplings by a 37x37 Arb-certified system. This is not a full fourth-order design.
