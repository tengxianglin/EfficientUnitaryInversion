# Fifteen-separator active-set reweighting

2026-11-22. This note records the next exact-input reweighting step after
the 35-column fourteen-probe candidate was rejected by a fresh Arb prefix.

## New certified separator

The parent candidate input is
`ac789d6fa678a4759c13d3d5588253e57d63e5a448946bdd9bb915369d401d80`.
Its 128-bit Arb prefix transcript is
`evidence/candidate_sixth_prefix_14probe_n21.json`, Git blob SHA1
`8578b04b4af392e34b57673a24e83c0c710f8563`.

The first newly exposed sixth-order orbit is

[
I=(0,1,2,3,19,26),qquad |\mathcal O(I)|=42,
qquad t_I=+5/19721.
]

The frozen Arb transcript reports

[
e_I\in[0.441009680048281548907798123619898\pm1.54\times10^{-34}],
]

with the absolute-error lower endpoint strictly above (1/3). This is a
candidate-specific strict counterexample. It does not imply a lower bound
for other physical ensembles or for the 83-column pool.

The parent candidate had passed selected-row Arb checks for all 1,461
second/fourth rows, 270 selected sixth rows (256 screen + fourteen
separators), and seven selected eighth rows. The prefix then rejected its
complete sixth-order cap before the full 63,133-orbit scan was warranted.

## Finite reweighting question

Add the new row to the fourteen earlier Arb-certified sixth-order separators
and solve the same finite minimax problem over the frozen 83-column physical
pool:

- 1,461 complete low-order rows;
- 256 frozen sixth-order screening rows;
- fifteen Arb-certified sixth-order separator rows;
- seven selected eighth-order rows.

The LP therefore has 1,739 rows and 83 nonnegative weights summing to one.
HiGHS is used only for binary64 discovery. The resulting positive weights are
converted exactly with `Fraction.from_float` and normalized as rational
probabilities. No LP objective is itself an interval certificate.

## Evidence ladder

The new workflow keeps these claims separate:

1. The LP transcript records the finite binary64 objective, row-block maxima,
   all fifteen source separators, and the positive support.
2. The candidate JSON pins the LP transcript hash, four Arb prefix blob
   hashes, and exact rational probabilities summing to one.
3. A 128-bit Arb selected-row verifier checks every low row, all 271 selected
   sixth rows (256 + 15), and the seven selected eighth rows.
4. A fresh 1,024-orbit Arb prefix tests whether reweighting moved the active
   sixth-order obstruction. Only if that prefix passes does the workflow run
   the complete 63,133-orbit sixth-order scan.

A prefix pass is not a complete sixth-order certificate. A strict interval
violation is candidate-specific. Even a complete sixth-order pass would not
establish the full eighth-order maximum, higher moments, exact program
uniformity, global optimality, or an operational inversion/channel-error
bound.

## Reproduction

The GitHub Actions workflow pins Python 3.11, NumPy 2.3.5, SciPy 1.15.3,
and python-flint 0.8.0. Its main commands are:

```bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python joint_low_six_eighth_lp_with_fifteen_sixth_probes.py \
  > evidence/joint_low_six_eighth_lp_with_fifteen_sixth_probes_n21.json
python freeze_joint_candidate_with_fifteen_sixth_probes.py
python verify_candidate_fifteen_probes_arb.py
python verify_candidate_35_fifteen_probe_sixth_bound.py \
  --workers 8 --limit 1024 \
  --output evidence/candidate_sixth_prefix_15probe_n21.json
```

The exact candidate, LP transcript, selected-row Arb transcript, and prefix
transcript are committed by the workflow even when the prefix finds a new
strict separator. A new separator is returned to the finite LP; it is not
silently discarded or relabelled as a pass.
