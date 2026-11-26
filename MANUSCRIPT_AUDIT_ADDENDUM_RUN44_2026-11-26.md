# EUI research audit — Run 44 (2026-11-26)

## Run selection and repository state

Issue #5 remains the highest-leverage active scientific track. The prior run's 6,143-column finite-pool certificate succeeded; the next logically decisive step was continuous pricing of that exact rational dual, not another finite-pool LP before testing its scope.

## Continuous pricing of the 6,143-column dual

Workflow [45785906516](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45785906516) completed successfully.

Deterministic discovery settings:
- RNG seed: `202611260641`;
- 256 sampled frozen seed-pool candidates;
- 256 random connected starts;
- 128 fractional-transfer-profile-plus-positive-background starts;
- 256 random multi-segment starts;
- 916 initial candidates evaluated;
- 12 best starts optimized per class with L-BFGS-B and analytic Fréchet gradient;
- 160 iterations maximum per optimized start;
- gradient finite-difference regression maximum absolute defect: (2.6438207179069195\times10^{-10});
- elapsed search time: 97.416 s.

The floating search found:
- best connected score (22.313363079759249), versus exact target score (0.22331252019032463\ldots);
- best multi-segment score (26.769887655434061).

The independent 256-bit Arb verifier then reconstructed both candidates from exact rational decimal couplings and checked all 1,764 entries of each (42\times42) orthogonality matrix plus determinant one.

**Connected escape:**
- all 41 interior couplings strictly positive;
- minimum coupling (19999999999999999/20000000000000000000000\approx10^{-6});
- Arb target-minus-score interval:
  [
  [-22.09005055956690912168578229660331296613459108528699898549299997601959335\pm4.43\times10^{-72}]<0.
  ]

**Multi-segment escape:**
- internal zero edges ({1,31,32});
- minimum positive coupling (10^{-8});
- Arb target-minus-score interval:
  [
  [-26.54657513524354876757981913391961689610564143783197345348108272387935518\pm8.96\times10^{-72}]<0.
  ]

Machine evidence:
- search: `evidence/ising_full_fourth_plus_twenty_gapped_search_n21.json`;
- independent escape certificate: `evidence/ising_full_fourth_plus_twenty_gapped_escape_arb_n21.json`;
- workflow: [45785906516](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45785906516).

**Logical conclusion:** the 6,143-column rational dual is not a separator for the continuous connected/multi-segment physical family. The exact finite-pool theorem for its pinned 6,143 columns is unaffected. The two exact-rational paths are concrete physical counterexamples to extending this particular dual, not witnesses of a positive ensemble and not a global converse.

## 6,145-column cutting-plane extension

Both independently certified paths have been appended to the previous 6,143-column pool. Added:
- `discover_ising_full_fourth_plus_twenty_two_gapped_n21.py`;
- `verify_ising_full_fourth_plus_twenty_two_gapped_arb_n21.py`;
- `.github/workflows/eui-reoptimize-6145-full-fourth.yml`.

Commits:
- discovery: `9e54ed125694874b203d0e945288e32e0b28fb69`;
- independent verifier: `2e9ede7c3d05caf10b362caa26c599e51f87ab53`;
- workflow: `e76584bca118722e393d182a59fddc19549bb7d4`.

Workflow [45787634578](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45787634578) was observed in progress. Python compilation and deterministic block-minor, restricted-spin-symmetry, and JSON-serialization regressions all passed. The 6,145-column LP was still running at the latest check; no LP or Arb result is claimed yet.

## Current proof boundary and next action

- **Proved:** finite-pool 6,143-column second-/fourth-order separation.
- **Proved:** two explicit exact-rational continuous physical escapes from that particular 6,143 dual, each with 256-bit Arb orthogonality/determinant/score certification.
- **Pending:** 6,145-column reoptimization and independent Arb certification.
- **Still open:** all-even-principal-minor positive ensemble at (n=21); a global converse over all legal physical couplings; complete sixth/eighth and higher moments; and the operational Choi/diamond bridge.

Next action: finish workflow 45787634578. If its new dual certifies, immediately price it continuously; if it has another escape, append it and repeat. If a positive primal is found, independently certify all weights and all 1,461 moment coordinates before claiming feasibility.