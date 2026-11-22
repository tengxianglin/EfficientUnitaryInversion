# Five certified sixth-order separators and the next physical reweighting

## Parent-candidate rejection

The exact 32-column candidate from the seven-row LP has candidate-input SHA256

`403614d80d8c5eeb15d56960fc7503103f8d376a7ab990fcb8988b1850d1a54d`.

A 128-bit Arb prefix scan of the canonical sixth-order orbit list found five strict violations before orbit index 1,024. The first is (I=(0,1,2,3,5,12)), with target (+5/19721) and relative error

`[-0.358516863520777043612390863200011 +/- 1.97e-34]`.

Its absolute-error lower endpoint is strictly above (1/3). Four more strict violations are frozen in `evidence/candidate_sixth_prefix_7row_n21.json`. The exact Git blob SHA-1 of that transcript is `6604c6727b075b79ceca438b01faadbbb0ebbd19`.

This rejects only the proposed (G_6<1/3) claim for that 32-column candidate. It is not the full sixth-order maximum and not a no-go theorem for the physical family.

## New finite design step

The next LP adds all five certified sixth-order rows to the frozen 83-column pool while retaining:
- all 1,461 second/fourth rows;
- all 256 frozen sixth-order screen rows;
- the seven selected eighth-order rows, including the earlier Arb-certified eighth-order separator.

The LP is a binary64 discovery step. A candidate is frozen only if its finite objective is below (1/3); the exact rationalized candidate must then pass a separate 128-bit Arb check on every included row. A complete sixth-order scan must be rerun for any replacement.

## Reproduction

```bash
python joint_low_six_eighth_lp_with_sixth_probes.py
python freeze_joint_candidate_with_sixth_probes.py
python verify_candidate_joint_probes_arb.py
```

The second command is conditional on the finite LP objective being strictly below (1/3). The Arb transcript distinguishes the complete low block, the 261 selected sixth rows, and seven selected eighth rows. None of these selected-row checks is a complete sixth/eighth maximum.

## Next decisive action

If the finite LP remains below (1/3) and the selected Arb checks pass, run the full 63,133-orbit sixth-order verifier on the newly frozen exact candidate. Add any new strict separator to the LP. If the finite objective is not below (1/3), the frozen 83-column pool has failed this particular finite design step; search for new physical columns rather than presenting the failed LP as a witness.
