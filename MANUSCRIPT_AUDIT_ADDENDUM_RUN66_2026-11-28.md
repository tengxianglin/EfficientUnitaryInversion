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

The dependency-free Fraction verifier checks all three N=4 perfect matchings, their exact cycle-exponential polynomial identities, all 16 vertex-sign gauges per seed, every 2x2 Plucker minor, the rank-two projector identities, the exact mean projector I_6/3, the exact frame-potential values, and the four-determinant overlap formula for all 2,304 pairs of gauge-expanded states. It also checks the single-seed diagnostic (FP=1, chi-square=1/2, TV=1/3).

This is a finite exact verification of the general identities, not an N=42 physical construction.

## Limitations retained

- No N=42 positive all-moment physical ensemble is produced.
- A frame-potential estimate that fails to reject does not certify uniformity; the target baseline 4/binom(42,21) is exponentially small.
- The complement Slater line is auxiliary, not a second physical oracle.
- No Choi-state trace-distance or channel diamond-distance theorem follows.
- The public manuscript remains arXiv:2506.20570v1 in the inspected source record; no editable manuscript or supplementary source is in the repository, so no formal manuscript text was changed.

## Next highest-value action

Apply the frame-potential falsifier to the broadest available N=42 general-cycle candidate pools, using validated determinant overlaps and a pre-registered sample budget. Candidates that survive should still be subjected to the complete 1,440-quartic-orbit audit and then higher even-order checks; the frame potential is a screening tool, not a replacement for the all-moment theorem.


## Final repository and CI identifiers

- Initial theory/evidence commit: 95abd399de18d418ca08aeecb6d4b93b280405a0.
- Verifier assertion cleanup: 54cbd4b003921cc0b1ed7e50cfb1d26243aed4e5.
- Q=RD versus Q=DR convention note: 38fb9d514fc03fcdc6c14b4fd3bad0a48d229087.
- Main HEAD at the final workflow-verification point, before appending audit metadata: 38fb9d514fc03fcdc6c14b4fd3bad0a48d229087.
- Exact workflow 46055397840 passed both compilation and exact Fraction recomputation; earlier pushes 46055308217 and 46055394899 also completed successfully.
- The verifier was independently reviewed against the N=4 exact calculation; the hosted CI recomputation is the repository execution record.

## Run 65 matching-edge distribution clarification

The Run 65 cycle-edge distribution and its 72.6616% exclusion bound are correct, but they are strictly weaker than the already-existing reachability theorem in THEORY_CYCLE_MATCHING_ATOM_REACHABILITY_N42.md. That theorem bounds the number of cycle-reachable signed matching atoms by 4,194,324 out of 41!!, so the uniform matching measure's unreachable mass is at least 0.9999999999999999996801417. The Run 65 edge-count statement should be treated as a transparent combinatorial corollary, not the strongest available matching-atom bound. Neither statement excludes non-permutation cycle-exponential mixtures.
