# Manuscript audit addendum — Run 74

Date: 2026-11-28. EUI repository: tengxianglin/EfficientUnitaryInversion.

## Selection

Rechecked the current mainline, recent commits, open Issues #7/#5/#6/#3, Issue #7 comments through Run 73, the Run 73 bipartite-matching minimax theorem, the Run 70/71 sixth-harmonic pricing results, the existing N=42 period-two pair and nine-quartic certificates, and the current workflow inventory.

Run 73 quantitatively closed the bipartite perfect-matching convex hull, but explicitly left non-permutation cycle exponentials as the escape route. The highest-leverage next step was therefore constructive: add genuinely nonperiodic, strictly-positive cycle atoms while preserving the already matched pair and quartic coordinates.

The repository still has no editable manuscript TeX/BibTeX, PDF, or standalone supplementary source. The public manuscript was not modified.

## Discovery

A deterministic binary64 discovery used 3,000 positive 42-edge cycle seeds after a 120-seed warm-up block (NumPy/SciPy, RNG seed 20261128). The LP maximized mass on nonperiodic cyclic-orbit seeds while retaining all pair-distance constraints and nine quartic translation-orbit constraints.

The frozen support contains:
- 26 period-two seed orbits;
- 4 primitive-period-42 seed orbits;
- 220 distinct physical cycle atoms after cyclic expansion.

The approximate total mass assigned to the four nonperiodic orbit families is 0.06981604735. The full-orbit binary64 screen evaluated all 2,670 cyclic translation orbits of quartets (111,930 four-sets) and identified (0,1,6,7) as the largest absolute residual, about 0.00462167363619. These are discovery diagnostics, not proof.

## Certified result

The independent 256-bit Arb verifier reconstructs all entries from exact-rational decimal coupling inputs and solves a 30-by-30 exact-real moment system. Workflow [46128674321](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46128674321) completed successfully; I inspected the completed job steps and the committed machine certificate.

Certified:
- the 30-by-30 determinant interval excludes zero:
  \[
  [-6.178383682608817535937694562703590719062047946330618475182622559141\times10^{-39}
  \pm3.92\times10^{-106}];
  \]
- every exact-real weight is strictly above 1/2000; the minimum enclosure is approximately 0.0008891094648702215;
- the weights sum to one;
- the four primitive-period-42 orbit families carry mass
  \[
  [0.06981604734786188502231445203212434131817526623576506399557910824831696
  \pm4.53\times10^{-72}]>1/20;
  \]
- all 220 distinct atoms have strictly positive couplings, with minimum coupling exactly 6388147249/125000000000;
- all 21 cyclic pair-distance orbits match -1/41, which covers all 861 unordered pairs;
- all nine selected quartic translation orbits match 1/533, covering 357 distinct four-subsets.

The same exact-real weights certify two additional quartic misses:
- orbit representative (0,3,18,21): residual greater than 1/500;
- orbit representative (0,1,6,7): residual greater than 1/250.

Thus this is a genuine positive physical construction with nonperiodic atoms, but only for all pair moments and 357 selected quartic coordinates. It is not a complete quartic design.

## Artifacts and commits

- Frozen input: evidence/n42_mixed_cycle_nine_quartic_atoms.json
- Verifier: verify_n42_mixed_cycle_nine_quartic_ensemble_arb.py
- Arb certificate: evidence/n42_mixed_cycle_nine_quartic_ensemble_arb.json
- Theory: THEORY_N42_MIXED_NONPERIODIC_NINE_QUARTIC_ENSEMBLE.md
- Workflow: .github/workflows/eui-n42-mixed-cycle-nine-quartic.yml
- CI: workflow 46128674321 — SUCCESS.
- Certificate commit: 9b08b428e757628b9ab7a4fe7db75d3bf278d31c.

## Scope and next action

This construction disproves the idea that the current pair-plus-nine-quartic feasible region is confined to period-two atoms. It does not solve the full cycle-family convex-hull question, prove a global separator, match all fourth-order moments, or establish a Choi/diamond-distance bound.

Next highest-value action: use the certified 220-atom mixture as the seed of a quartic-orbit cutting-plane search. Add the largest unresolved quartic orbits (starting with (0,1,6,7)), introduce new primitive-period-42 seeds, and re-solve the positive weights while preserving all 861 pair coordinates and every previously certified quartic orbit. Every proposed improvement must be rechecked with Arb; finite-pool infeasibility remains discovery only.
