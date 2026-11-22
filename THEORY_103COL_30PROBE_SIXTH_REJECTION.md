# Eight new strict sixth-order separators for the 103-column / 30-probe candidate

Date: 2026-11-22

## Candidate rejection

The exact rational 41-support candidate from the 103-column / 30-probe LP is rejected by eight strict 128-bit Arb sixth-order witnesses, one in each of eight deterministic shards. The frozen transcript records `status=strict_violation`, `complete=false`. Each shard stops at its first strict violation, so this is a candidate-specific rejection, not a completed maximum scan.

Pinned inputs:

- Candidate SHA256: `40f34cd00bea83a8ef9ed188dbbc6e2d4b2e777c5700d92e78b3964db8539073`.
- LP transcript SHA256: `82652994e0e60bdaf480240ef6279f00500d0d356b952a3379e3ae0b0a6b6ff2`.
- Full-audit commit: [`40e303ff8f05cea324aac18595d47f4b58bf7fc1`](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/40e303ff8f05cea324aac18595d47f4b58bf7fc1).
- Full-audit workflow: [45004684065](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45004684065).

## Strict Arb counterexamples

All eight representatives have target (+5/19721). Every reported absolute-error lower endpoint is strictly greater than (1/3).

| Shard | Canonical representative (I) | Relative-error midpoint |
|---:|---|---:|
| 0 | (0,1,2,5,20,37) | -0.33597915568916825 |
| 1 | (0,1,3,17,20,40) | +0.40642826364422556 |
| 2 | (0,1,4,17,29,30) | +0.35454676648002454 |
| 3 | (0,1,6,16,19,21) | -0.35285128993685323 |
| 4 | (0,1,9,16,26,33) | +0.36598532699479685 |
| 5 | (0,2,5,13,18,31) | +0.34050758989270514 |
| 6 | (0,2,8,13,16,26) | +0.37512547153174929 |
| 7 | (0,3,7,16,19,26) | +0.34268669869657545 |

Full Arb intervals, lower/upper endpoints, orbit keys, and shard hashes are in `evidence/candidate_103col_30probe_complete_sixth_arb_n21.json`.

## Coverage accounting

- Total domain: 63,133 sixth-order dihedral orbits / 5,245,786 six-subsets.
- Evaluated before the eight shard-local first violations: 5,952 orbit visits, 496,482 six-subsets, and 20,355,762 principal-minor determinant evaluations.
- All eight shards returned a strict violation; none completed its assigned range.

The successful workflow means the interval verifier correctly rejected this exact candidate. It does not mean the candidate passed a complete sixth-order audit, and it does not prove a no-go theorem for the 103-column pool.

## Next cutting-plane problem

The eight new rows are distinct from the 256 screened sixth rows and the 30 already certified sixth probes. They are being added to the same 103-column physical pool, giving a 38-probe finite design with:

- 1,461 complete second/fourth rows;
- 256 screened sixth rows;
- 38 Arb-certified sixth rows;
- seven selected eighth rows;
- 1,762 total normalized rows.

The next HiGHS solve and exact-rational/Arb selected-row verification are running in [workflow 45005091230](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45005091230).

## Scope

These witnesses reject only the exact pinned 41-support distribution. They do not rule out another distribution on the same 103 columns, any other legal path generators, or another Hamiltonian family. The next candidate, if one is produced, must pass exact rational normalization, all selected Arb rows, a fresh sixth-prefix audit, and then the full sixth-order Arb audit. Eighth-order completeness, higher moments, global physical optimality, and an operational Choi/diamond-norm inversion bound remain open.
