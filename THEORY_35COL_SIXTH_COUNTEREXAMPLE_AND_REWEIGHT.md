# Fourteen Arb-certified sixth-order separators and the next reweighting

## Parent-candidate failures

The 35-column candidate with SHA256 `ced62e0ef71f384056cd535d2294f3af52875c75497df7a1815bf8d3c0ca135e` has six new strict sixth-order violations in its 1,024-orbit 128-bit Arb prefix. They are frozen in `evidence/candidate_sixth_prefix_8probe_n21.json`, Git blob SHA1 `6b655f83d87b9ea24f9394355ef1aa8c4633136e`.

Together with five separators from the 32-column parent and three from the 34-column parent, there are now fourteen strict Arb-certified sixth-order separator rows. The three prefix transcripts are pinned by Git blob SHA1s:
- `6604c6727b075b79ceca438b01faadbbb0ebbd19`
- `4827a61b30abdfdab2675eac6df557e71081294e`
- `6b655f83d87b9ea24f9394355ef1aa8c4633136e`

These are candidate-specific rejections, not a full sixth-order maximum or a no-go theorem.

## Finite reweighting

The next LP includes all fourteen certified sixth-order separators, the 256 frozen sixth screen rows, all 1,461 low rows, and seven selected eighth rows. It is a binary64 discovery calculation. A candidate is frozen only if the objective is strictly below 1/3; exact rationalization and 128-bit Arb selected-row checks remain separate gates.

## Reproduction

```bash
python joint_low_six_eighth_lp_with_fourteen_sixth_probes.py
python freeze_joint_candidate_with_fourteen_sixth_probes.py
python verify_candidate_fourteen_probes_arb.py
```

The full sixth-order scan must be repeated for any replacement. A selected-row pass does not imply the complete sixth-order maximum.
