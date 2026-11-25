# EUI research audit — Run 36 (2026-11-26)

## Selection

Issue #7 remains the highest-value unresolved scientific track. Run 35 established exact pair-level convex-hull feasibility for the N=42 period-two family. The next question is whether positive mixtures can satisfy any nontrivial fourth-order constraints without losing the complete pair design.

## New discovery

A HiGHS search over 5,000 strictly positive period-two atoms in \([0,50]^2\), seed 350, found a 35-atom support matching:
- all 30 independent pair equations (the 31st follows from row orthogonality);
- four selected quartic coordinates, represented by four distinct translation-by-two orbits.

The 35 coupling pairs were frozen as exact decimal rationals. The final proof is not the floating LP: the Arb verifier rebuilds the exact-real 35-by-35 system and solves for its unique weights.

## Exact verification target

- All 861 pair principal-minor coordinates equal \(-1/41\).
- Four quartic orbit representatives are matched: [0,1,2,3], [0,3,10,15], [0,2,4,6], [0,10,20,30].
- Their 21 translations by two are checked directly (84 quartic coordinates).
- Every one of the 42 couplings in every atom is strictly positive.
- A fifth quartic witness [0,2,21,23] is required to fail by more than 1/400, making the limitation explicit.

## Interpretation

This is a partial moment design, not a full fourth-order or all-even-principal-minor design. It demonstrates that the period-two convex hull is substantially richer than the single-atom theorem: mixtures can satisfy all pair moments and multiple quartic orbit constraints. The unmatched witness is a limitation of this support only, not a global no-go.

## Reproducibility

- evidence/n42_period_two_pair_plus_quartic_atoms.json
- verify_n42_period_two_pair_plus_quartic_ensemble_arb.py
- evidence/n42_period_two_pair_plus_quartic_ensemble_arb.json
- THEORY_N42_PERIOD_TWO_PAIR_PLUS_QUARTIC_ENSEMBLE.md
- .github/workflows/eui-n42-period-two-pair-plus-quartic.yml

The next step is to increase the set of quartic orbit constraints while allowing additional positive period-two atoms. Finite-pool LPs are discovery only; any existence claim requires the same exact-real Arb solve and explicit scope limits.
