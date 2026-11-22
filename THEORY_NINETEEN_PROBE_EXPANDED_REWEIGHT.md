# Nineteen-probe active-set reweight after the 17-probe prefix rejection

Date: 2026-11-22

## Frozen parent and strict new separators

The 93-column / 17-probe LP produced an exact 39-support rational candidate. Its selected-row 128-bit Arb verifier passed all 1,461 low rows, 273 sixth rows (256 screen + 17 certified separators), and seven selected eighth rows, all with strict upper bound 1/3. The exact probabilities sum to one.

That selected-row success was not a complete sixth-order result. The fresh 1,024-orbit Arb prefix in `evidence/candidate_sixth_prefix_17probe_expanded_n21.json` rejected the candidate at two further rows:

| Orbit | Target | Relative-error interval midpoint | Certified status |
|---|---:|---:|---|
| (0,1,2,3,21,22) | +5/19721 | 0.3479107455083803422 | strict Arb violation |
| (0,1,2,4,11,18) | -5/19721 | 0.3353292745783166523 | strict Arb violation |

The prefix uses 128-bit Arb, covers the first 1,024 canonical dihedral orbits (73,500 six-subsets), and pins the parent candidate SHA256 `028b3d27e291bb6963d247ee41ef8e7728c5a044b09c8c6fd02a12d2e349bfaa`. Its Git blob SHA1 is `4c4ba9931ecaf8c5b0878831d7e687ff7f5a7137`.

These are candidate-specific counterexamples. They do not establish a no-go for the expanded physical pool or for other legal ensembles.

## New 19-probe finite design

The next deterministic active-set LP appends both rows to the existing 17-probe design while retaining:
- 1,461 exact low-order rows (all second and fourth);
- 256 frozen sixth-order screen rows;
- 19 Arb-certified sixth-order separators;
- seven selected eighth-order rows;
- the same 93 legal physical columns (83 original columns plus ten columns with positive 128-bit Arb reduced-cost certificates).

The LP has 1,743 rows. HiGHS binary64 is used only for candidate discovery. Any returned weights are converted to exact rational probabilities summing to one, then independently checked with 128-bit Arb. A fresh sixth-order prefix is required before any complete sixth-order claim.

## Evidence ladder and scope

- **Proved for the parent candidate:** the two named sixth-order rows violate the strict 1/3 cap, by Arb interval lower endpoints.
- **Finite numerical design only:** the 19-probe LP objective and its support are not a certificate.
- **Required next checks:** exact rational freeze; Arb checks of every low, screened sixth, 19 separator, and seven selected eighth rows; fresh 1,024-orbit Arb prefix; full 63,133-orbit Arb scan only if the prefix passes.
- **Not implied:** complete eighth-order control, moments above order eight, global optimality over all legal generators, or an operational Choi/diamond-norm inversion bound.

## Reproduction

The workflow `.github/workflows/eui-expanded-pool-nineteen-probe.yml` reruns the 17-probe parent checks, solves the 19-probe LP, freezes exact weights, runs selected-row Arb checks, and runs the next sixth-order prefix. The workflow records the LP and any candidate/prefix evidence even when the new candidate is rejected.
