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

The hosted workflow is:
- .github/workflows/eui-n42-period-two-five-quartic.yml

At audit time the expected Arb certificate had not yet appeared in the repository. Therefore this run claims a floating discovery and a frozen verification pipeline, not an exact existence theorem. The verifier/CI result must be inspected before upgrading the claim.

## Relation to Run 55

The N=8 period-two arbitrary-mixture theorem remains correctly scoped to N=8 and the period-two subfamily. The N=42 candidate does not follow from that theorem. It is an independent construction at N=42.

The new 36-atom candidate includes the former mismatched witness [0,2,21,23] while retaining the four previously matched quartic representatives. If the Arb certificate passes, it removes the support-specific limitation of the earlier 35-atom ensemble, but it still covers only 189 of the full fourth-order coordinates.

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

Not yet verified:
- 256-bit Arb invertibility and strict positivity of the exact-real weights;
- the 861 pair checks and 189 quartic checks with interval enclosures;
- hosted workflow completion and committed machine certificate.

## Next highest-value action

Inspect the new hosted Arb workflow. If it succeeds, update Issue #7 and freeze the exact certificate, then add further quartic orbit constraints using the 100,000-candidate discovery framework. If it fails, diagnose the exact interval or matrix issue; do not describe the floating LP as a theorem.
