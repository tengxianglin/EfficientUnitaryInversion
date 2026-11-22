# Twenty-probe active-set reweight after the 19-probe prefix rejection

Date: 2026-11-22

## Frozen 19-probe parent and strict new separator

The 93-column / 1,743-row HiGHS LP produced an exact 38-support rational candidate. Its selected-row 128-bit Arb verifier passed all 1,461 low rows, all 275 sixth rows (256 screen + 19 certified separators), and all seven selected eighth rows. The exact probabilities sum to one. The finite LP objective was 0.3304689299508032.

The fresh 1,024-orbit Arb prefix (81,606 six-subsets) rejected that candidate at one additional sixth-order orbit:

| Orbit | Orbit size | Target | Relative-error interval midpoint |
|---|---:|---:|---:|
| (0,1,2,3,21,24) | 42 | +5/19721 | 0.4575741982584978891 |

The absolute-error interval lower endpoint is strictly greater than 1/3. The parent candidate SHA256 is `661ebd7cb07afbaf0ecc493f76c7497bdfb69e532e7bcc537136a017a5bf11ad`; the prefix transcript Git blob SHA1 is `0e773617d93444ffbc7fcc4ee8fef4f5db2be08d`.

This is a candidate-specific Arb counterexample, not a no-go theorem for the 93-column pool or other legal physical ensembles.

## New 20-probe finite design

The next deterministic active-set LP appends this row to the 19-probe design while retaining:
- 1,461 exact low-order rows (all second and fourth);
- 256 frozen sixth-order screen rows;
- 20 Arb-certified sixth-order separators;
- seven selected eighth-order rows;
- the same 93 legal physical path columns (83 original plus ten Arb-priced columns).

The LP has 1,744 rows. HiGHS binary64 is candidate discovery only. Any returned weights are frozen as exact rational probabilities and independently checked with 128-bit Arb. A fresh sixth-order prefix is required before any complete sixth-order claim.

## Evidence ladder and scope

- **Proved for the parent candidate:** the named sixth-order row violates the strict 1/3 cap, by an Arb interval lower endpoint.
- **Finite numerical design only:** the 20-probe LP objective and support are not a certificate.
- **Required next checks:** exact rational freeze; Arb checks of every low, screened sixth, 20 separator, and seven selected eighth rows; fresh 1,024-orbit Arb prefix; full 63,133-orbit Arb scan only if the prefix passes.
- **Not implied:** complete eighth-order control, moments above order eight, global optimality over all legal generators, or an operational Choi/diamond-norm inversion bound.

## Reproduction

The workflow `.github/workflows/eui-expanded-pool-twenty-probe.yml` reruns the 19-probe parent checks, solves the 20-probe LP, freezes exact weights, verifies selected rows with Arb, and runs the next sixth-order prefix. Evidence is committed even when the candidate is rejected.
