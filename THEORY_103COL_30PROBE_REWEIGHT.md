# 103-column / 30-probe reweighting: exact candidate and Arb prefix pass

Date: 2026-11-22

## Result

Eight strict 128-bit Arb sixth-order counterexamples to the preceding 103-column / 22-probe candidate were added to the active constraint set. Reoptimizing over the same 103 legal physical path columns produced a finite HiGHS objective below the target cap:

[
t_{mathrm{LP}}=0.33149366359306937<rac13.
]

The binary64 LP has 1,754 normalized rows: 1,461 complete second/fourth, 256 screened sixth, 30 Arb-certified sixth, and seven selected eighth rows. Its positive support has 41 columns. The weights were converted to exact rational probabilities with exact sum one.

Pinned candidate/evidence:

- Candidate input SHA256: `40f34cd00bea83a8ef9ed188dbbc6e2d4b2e777c5700d92e78b3964db8539073`.
- LP transcript SHA256: `82652994e0e60bdaf480240ef6279f00500d0d356b952a3379e3ae0b0a6b6ff2`.
- Parent 22-probe full-sixth rejection SHA256: `84801a36cb6ba9456d98bcc9bfb59b716574c2b19e97d83290c50b5235db5caa`.
- Frozen seed pool SHA256 (little-endian float64): `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`.
- Reweighting workflow: [45004015852](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45004015852).

## 128-bit Arb checks already passed

For the exact rational 41-support candidate, the selected-row verifier certifies strict normalized error below (1/3) on:

| Block | Rows | Worst absolute-error midpoint |
|---|---:|---:|
| All second/fourth | 1,461 | 0.33149366359104027 |
| Sixth screen + all 30 certified probes | 286 | 0.33149366359444800 |
| Selected eighth probes | 7 | 0.33149366359409658 |

A separate prefix scan passes the first 1,024 of 63,133 canonical sixth-order dihedral orbits, covering 85,050 six-subsets and 3,487,050 principal-minor determinant evaluations. Its worst midpoint is 0.33176668203811874 at representative ((0,1,2,3,6,25)).

Evidence:
- `evidence/joint_low_six_eighth_lp_103col_30probe_n21.json`
- `evidence/candidate_joint_input_103col_30probe_n21.json`
- `evidence/candidate_103col_30probe_selected_and_sixth_prefix_arb_n21.json`

## Full sixth-order audit

The 1,024-orbit prefix is not a complete maximum certificate. A new 128-bit Arb run is auditing all 63,133 sixth-order orbits / 5,245,786 six-subsets with eight workers:

[Workflow 45004684065](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45004684065).

If every interval upper endpoint is below (1/3), the result will certify (G_6<1/3) for this exact rational candidate. If a strict violation is found, it rejects this candidate only; the certified row can be added to the next cutting-plane LP. If an interval overlaps the cap, precision or exact enclosure must be improved before any decision.

## Scope

The HiGHS objective is finite binary64 discovery, not a proof. Exact rationalization plus the listed Arb checks proves only the selected rows and the 1,024-orbit prefix. No complete sixth-order maximum is established yet; the complete eighth-order maximum, higher moments, global optimization over legal generators, and an operational Choi/diamond-norm inversion bound remain open.
