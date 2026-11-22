# Escaping the 83-column dual separator by pricing existing physical columns

Date: 2026-11-22

## Certified starting point

The exact 83-column pool has a 128-bit Arb dual certificate for 1,739 pinned normalized rows. Its certified minimax lower bound is

$$
L=\frac{15505334789199137791566220521}
{46116860184337794790000000000}
=0.33621835327082955\ldots>\frac13.
$$

The dual has only 34 nonzero row multipliers: 14 low-order, 16 sixth-order, and 4 selected eighth-order rows. The exact dual coefficients and all 83 certified column inequalities are frozen in \`evidence/fifteen_probe_dual_certificate_n21.json\`.

## Deterministic pricing of the remaining canonical pool

The current canonical constructor returns 1,641 legal 42-site path columns. The weighted pool contains 83, leaving 1,558 unused columns. The all-column binary64 screen found 102 positive reduced-cost candidates; the largest screen score was 2.844672258972245 at column 969.

The top ten candidates were independently recomputed at 128-bit Arb precision. All ten satisfy the strict inequality

$$
a(c)^Tz+\lambda-\delta>0,
$$

with the exact dual vector from the 83-column certificate. The certified Arb lower endpoints are:

| Canonical column | Arb lower endpoint |
|---:|---:|
| 969 | 2.8446722589726182387838539654096637371 |
| 1087 | 1.0120273858076214208370649455115860684 |
| 1282 | 0.64787847294676969802347145997465011886 |
| 679 | 0.64093542409643488399688671033092427511 |
| 727 | 0.45010235240720137438107722371254565286 |
| 780 | 0.40481631141503575601524166696035897854 |
| 779 | 0.34464795105070739919034093782826573925 |
| 906 | 0.29562777544218595465223774552490770664 |
| 796 | 0.29023486875315997614993288390059549209 |
| 890 | 0.27231308158582196485028224972041840610 |

The Arb pricing transcript pins the dual certificate SHA256, LP transcript SHA256, pricing-screen SHA256, canonical all-column SHA256, exact candidate couplings, and 128-bit interval endpoints.

## Correct interpretation

A positive priced column violates the *specific* dual inequality used to prove the 83-column lower bound. Therefore that dual witness cannot be extended unchanged to a pool containing the priced column. This does **not** by itself prove that the expanded pool has minimax error below 1/3, nor does it invalidate the theorem for the original 83 columns. A new finite primal design and a separate exact verification are required.

## Next experiment: 93-column expanded LP

The next script adds the ten Arb-certified columns to the original 83, preserving all 1,739 rows:

- 1,461 second/fourth-order rows;
- 256 frozen sixth-order screening rows;
- 15 Arb-certified sixth-order separators;
- 7 selected eighth-order rows.

It solves the 93-column binary64 minimax LP, freezes positive weights as exact rational probabilities, and checks every selected row with Arb. If the selected checks pass, it runs a fresh sixth-order prefix and then the complete 63,133-orbit audit only if the prefix passes.

## Reproduction

The complete run is encoded in \`.github/workflows/eui-expanded-pool-fifteen-probe.yml\`. The key scripts are:

- \`joint_low_six_eighth_lp_with_fifteen_sixth_probes_expanded.py\`
- \`freeze_expanded_candidate_with_fifteen_sixth_probes.py\`
- \`verify_expanded_candidate_fifteen_probes_arb.py\`
- \`verify_expanded_candidate_35_fifteen_probe_sixth_bound.py\`

The 83-column theorem, the priced-column certificates, the expanded LP objective, selected-row Arb checks, and complete sixth-order audit are kept as separate evidence layers.
