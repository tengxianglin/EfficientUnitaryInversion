# Run 51 — repair the 6,151 verifier's parent-certificate pin

Date: 2026-11-27

## Repository state inspected

- Default branch: `main`.
- Main HEAD before this repair: `fddfce80cb7936f331a63f7ec70722832ba79f5b`.
- Open scientific tracks inspected: #5 (finite-pool versus full physical-family convex-hull question), #7 (physical reachability of the unrestricted-SO perfect-matching ensemble), #6 (Appendix B noise normalization), and #3 (type-1.2 classifier correctness).
- The active highest-leverage item remains #5: the 6,151-column LP diagnostic had been produced and committed, but its independent verifier stopped at a parent-certificate metadata guard before evaluating any 6,151-column interval inequalities.

## What the 6,151 LP actually returned

Workflow [45843103615](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45843103615) completed its compilation and structural regression steps, then ran the full 1,461-coordinate LP and committed diagnostic `evidence/ising_full_fourth_plus_twenty_eight_gapped_n21.json` at commit [fddfce8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fddfce80cb7936f331a63f7ec70722832ba79f5b).

The committed diagnostic records:

- 6,151 columns = 22 base + 6,101 fractional-grid + 28 exact-rational gapped paths;
- 1,461 complete second-/fourth-order coordinates, 1,440 fourth-order orbits, 111,930 four-subsets, 1,313 independent moment rows and 1,314 equalities including normalization;
- HiGHS primal feasibility status: infeasible (floating LP result only);
- HiGHS dual status: optimal (floating candidate only);
- target score: 0.2489408753607058;
- maximum candidate score: 0.022660757845013157;
- recomputed floating gap: 0.22628011751580016;
- maximum floating pricing-constraint violation: 1.0749734435933078e-13.

These are discovery diagnostics, **not** an exact or Arb-certified theorem.

## Root cause of the verifier failure

The job log for run 45843103615 shows the verifier stopped at line 110 with:

```
RuntimeError: the 6,149-column parent certificate is invalid
```

Inspection of the pinned parent file `evidence/ising_full_fourth_plus_twenty_six_gapped_arb_n21.json` confirms its actual status is:

```
arb_certified_finite_6149_column_full_fourth_plus_twenty_six_gapped_separator
```

The child verifier incorrectly expected the *child* label `arb_certified_finite_6151_column_full_fourth_plus_twenty_eight_gapped_separator` on this 6,149-column parent certificate. This was a copied metadata guard, not a failed moment inequality: the verifier exited before reconstructing and pricing the 6,151 columns.

## Repair committed

Updated `verify_ising_full_fourth_plus_twenty_eight_gapped_arb_n21.py` to require the exact, observed 6,149-parent status. Also corrected the verifier module docstring and child-diagnostic status error text to say 6,151 where appropriate.

- Repair commit: [a1ac264](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a1ac2644e682c870bba66dbd8d3b69b184c35353)
- Previous verifier blob: `fa6c36418cb1ce80a5010285ef706d4bcd8898ef`
- New verifier blob: `19fb941de2fa7110a7e781594cb8cc3e5817c76b`

The push modifies a path watched by `.github/workflows/eui-reoptimize-6151-full-fourth.yml`, so it triggers a fresh workflow. At the time this note was written, the rerun's final LP/Arb status had not yet been observed.

## Scope and next action

- **Verified:** the 6,151 floating LP diagnostic exists and is pinned; the parent certificate is genuinely a complete 6,149-column Arb certificate; the failure was an incorrect parent status string.
- **Not yet verified:** the 6,151-column exact-rational dual and all 6,151 interval inequalities. No 6,151 finite-pool theorem is claimed.
- **Still unresolved:** full continuous-family separation or a complete physical positive ensemble; all-even-principal-minor feasibility at (n=21); higher-order moment closure; and the operational bridge to Choi/diamond distance.

Next action: inspect the workflow triggered by repair commit `a1ac264`. If independent Arb certification succeeds, run continuous pricing on that newly certified dual. If it fails, classify the actual arithmetic/coverage failure from the verifier log before changing any scientific claim.
