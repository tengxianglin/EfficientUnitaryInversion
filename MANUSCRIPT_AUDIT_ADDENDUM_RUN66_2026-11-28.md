# Manuscript/research audit — Run 66 (2026-11-28)

## Repository state inspected

- Default branch: main.
- Starting HEAD: 15832cb21b9ec601bf8e1dc35c1a3997e59d1341.
- Recursive tree: 1,322 entries; no manuscript .tex/.bib/PDF or separate supplementary source was found.
- Recent commits and Actions were inspected. Latest relevant successful runs include 46036218302 (matching cycle-edge distribution), 46022836608 (complete N=42 quartic audit), 46003193864 (all-order incidence hierarchy), and 45985463935 (N=10 positive cycle ensemble).
- Open scientific tracks remain #7 (N=42 physical reachability/convex hull), #5 (finite-pool versus full-family gap), #6 (Appendix B normalization/QuAIRKit rerun), and #3 (QuAIRKit runtime smoke test).

## Selected issue

Issue #7 remains the highest-leverage scientific blocker. The new work derives an exact complement-folded Plucker/fusion-frame reformulation of the full program-mass target and a frame-potential statistic that can reject nonuniform candidate ensembles without enumerating all binom(42,21) labels.

## What changed

- Added THEORY_COMPLEMENT_FOLDED_PLUCKER_FRAME_N42.md.
- Added verify_complement_folded_plucker_frame.py.
- Added evidence/complement_folded_plucker_frame_n4.json.
- Added .github/workflows/eui-complement-folded-plucker-frame.yml.

## What is proved

1. For a physical seed, the auxiliary complement-symmetrized Slater projector sum Pi_c has rank two.
2. Uniform complement-folded program masses are equivalent to the exact tight fusion-frame identity E Pi_{c,epsilon}=(2/d)I after legal vertex-sign gauge randomization.
3. The frame potential equals 4/d times one plus the chi-square divergence of the mean complement-folded DPP distribution.
4. A random overlap sample is in [0,2], admits the stated Hoeffding bound, and can provide a one-sided statistical falsifier when its validated lower confidence bound exceeds 4/d.

## Exact finite verification

The dependency-free Fraction verifier checks all three N=4 perfect matchings, their exact cycle-exponential polynomial identities, all 16 vertex-sign gauges per seed, every 2x2 Plucker minor, the rank-two projector identities, the exact mean projector I_6/3, and the exact frame-potential values. It also checks the single-seed diagnostic (FP=1, chi-square=1/2, TV=1/3).

This is a finite exact verification of the general identities, not an N=42 physical construction.

## Limitations retained

- No N=42 positive all-moment physical ensemble is produced.
- A frame-potential estimate that fails to reject does not certify uniformity; the target baseline 4/binom(42,21) is exponentially small.
- The complement Slater line is auxiliary, not a second physical oracle.
- No Choi-state trace-distance or channel diamond-distance theorem follows.
- The public manuscript remains arXiv:2506.20570v1 in the inspected source record; no editable manuscript or supplementary source is in the repository, so no formal manuscript text was changed.

## Next highest-value action

Apply the frame-potential falsifier to the broadest available N=42 general-cycle candidate pools, using validated determinant overlaps and a pre-registered sample budget. Candidates that survive should still be subjected to the complete 1,440-quartic-orbit audit and then higher even-order checks; the frame potential is a screening tool, not a replacement for the all-moment theorem.
