# Finite joint low/sixth/eighth LP diagnostic

2026-11-22; base `9f26680c96c269eb5ad0e84fd8ee5efacff132ee`; Issue #3.

The selected eighth-order audit identified a concrete failure mode of the
current fixed witness. As a smallest decisive design experiment, this note
adds six eighth-order rows to a finite minimax LP over the same 83 physical
seed columns.

## Setup

`joint_low_six_eighth_lp.py` reconstructs the 83 exact-probability columns
from the hash-pinned ensemble input. It forms 1,461 low-order rows (all
second/fourth dihedral features), the 256 sixth-order rows in the frozen
floating screen, and the six eighth-order rows from
`THEORY_SELECTED_EIGHTH_AUDIT.md`. Each row is normalized by its target
magnitude. The LP minimizes the maximum absolute normalized residual over
these 1,723 rows, subject to nonnegative weights summing to one.

This is a binary64 SciPy/HiGHS discovery calculation. It is not an interval
certificate and does not add new Hamiltonian columns.

## Result

| block | current 83-column witness | LP over the same 83 columns |
|---|---:|---:|
| all 1,461 low rows | 0.2179999940 | 0.3259801370 |
| 256 screened sixth rows | 1.5486211350 | 0.3259801370 |
| six selected eighth rows | 6.2020415242 | 0.3259801370 |
| joint objective | 6.2020415242 | 0.3259801370 |

The finite LP therefore demonstrates a real tradeoff: within the frozen
column pool, the severe selected eighth-order residuals can be reduced to
about 0.326 while keeping the screened sixth rows and all low rows in the
same joint finite objective. The candidate uses 29 positive columns; its
weights are frozen in `evidence/joint_low_six_eighth_lp_n21.json`.

## What this does and does not establish

This is evidence that the sixth-order repair's poor eighth-order behavior is
not forced by the current 83-column pool under the *screened* constraints.
It is not a proof of a valid new EUI ensemble: the LP has not been checked
against all 63,133 sixth orbits, all eighth orbits, exact rational
probabilities, or orders 10--20. It also does not prove a global physical
optimum or an operational inversion/channel-error bound. The candidate must
be treated as a proposal for the next separation-oracle iteration.

## Reproduction and next action

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python joint_low_six_eighth_lp.py
```

The transcript pins the complete-input and sixth-screen SHA256 values. The
next decisive check is to evaluate this 29-column candidate on all sixth
orbits with Arb intervals, then audit additional eighth rows. If it fails,
add the violated rows to the LP; if it passes, freeze exact probabilities
and rerun the complete sixth certificate before making any improvement claim.
