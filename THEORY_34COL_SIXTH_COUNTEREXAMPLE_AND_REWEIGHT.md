# Eight Arb-certified sixth-order separators and the next reweighting

## Parent-candidate failures

The 34-column exact-rational candidate has SHA256 `00ba81adfcbebb02137e02b75a7f180d0bf528f71a4bdaa8afe9b9e2b19b7e99`. Its 128-bit Arb prefix scan found three new strict sixth-order violations:
- (0,1,2,3,19,22), target +5/19721, relative error about +0.339513774786;
- (0,1,2,4,7,15), target +5/19721, relative error about -0.338448395190;
- (0,1,2,4,22,40), target +5/19721, relative error about -0.371485187426.

Their strict lower bounds are frozen in `evidence/candidate_sixth_prefix_12row_n21.json`. The exact Git blob SHA1 is `4827a61b30abdfdab2675eac6df557e71081294e`. The preceding 32-column parent contributes five earlier strict separators in `candidate_sixth_prefix_7row_n21.json` (blob SHA1 `6604c6727b075b79ceca438b01faadbbb0ebbd19`).

These are candidate-specific rejections, not a full sixth-order maximum or a no-go theorem.

## Finite reweighting

The new LP includes all eight certified sixth-order separators, the 256 frozen sixth screen rows, all 1,461 low rows, and seven selected eighth rows. It is a binary64 discovery calculation. A candidate is frozen only if the objective is strictly below 1/3; exact rationalization and 128-bit Arb selected-row checks remain separate gates.

## Reproduction

```bash
python joint_low_six_eighth_lp_with_eight_sixth_probes.py
python freeze_joint_candidate_with_eight_sixth_probes.py
python verify_candidate_eight_probes_arb.py
```

The full sixth-order scan must be repeated for any replacement. A selected-row pass does not imply the complete sixth-order maximum.
