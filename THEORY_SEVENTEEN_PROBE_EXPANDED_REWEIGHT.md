# Seventeen-probe reweighting after the first 93-column expansion

Date: 2026-11-22

## Parent candidate and new strict separators

The first dual-priced 93-column LP used the original 83-column pool plus ten 128-bit Arb-priced physical path columns. It produced a 42-support rational candidate with selected-row maximum below 1/3, but the fresh 1,024-orbit sixth-order Arb prefix rejected it.

The exact candidate input SHA256 is

\`0c7425d053162e48afd9c10e85b20ac39e54c8896ceb9bad03da3647abada4e6\`.

Two new strict violations were certified:

| Sixth-order orbit | Target | Relative-error interval midpoint |
|---|---:|---:|
| (0,1,2,3,20,21) | +5/19721 | 0.3889655822859805491 |
| (0,1,2,4,15,40) | -5/19721 | 0.3379934846756004382 |

Both Arb absolute-error lower endpoints are strictly above 1/3. The full 1,024-orbit prefix transcript is pinned by Git blob SHA1 \`520c98d1d6bfea8f3b5676cdece12de7ff0ec7c8\`.

## New finite design

The next LP retains the same 93 physical columns and all previous rows, and appends these two certified sixth-order separators:

- 1,461 second/fourth-order rows;
- 256 frozen sixth-order screen rows;
- 17 Arb-certified sixth-order separators;
- 7 selected eighth-order rows.

This gives 1,741 rows and 93 physical columns. HiGHS is used only for finite binary64 discovery. The candidate weights are converted to exact rational probabilities before the Arb selected-row audit.

## Evidence ladder

A successful selected-row audit is not a complete sixth-order certificate. A fresh prefix is required; if it finds another strict violation, append that row and reweight again. Only a passing prefix justifies the full 63,133-orbit Arb scan. No complete eighth-order maximum or operational inversion-error bound follows from these checks.

## Reproduction

The workflow \`.github/workflows/eui-expanded-pool-seventeen-probe.yml\` reruns the pinned 15-probe parent checks, solves the 17-probe expanded LP, freezes exact weights, verifies selected rows with Arb, and runs the next sixth-order prefix.
