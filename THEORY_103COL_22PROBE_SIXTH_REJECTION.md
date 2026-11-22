# Eight strict sixth-order separators for the 103-column / 22-probe candidate

Date: 2026-11-22

## Decision

The exact rational 44-support candidate from the 103-column / 22-probe LP is rejected by eight independent, strict 128-bit Arb sixth-order witnesses. The complete-sixth workflow evaluated the eight deterministic orbit shards in parallel; each shard stopped at its first strict violation. This is enough to reject this candidate, but it is **not** a full evaluation of all 63,133 orbits.

Pinned inputs:

- Parent LP transcript SHA256: `c300ced6d07b7257ed086de5f747f5dd3e0cb2854228ce9d8179823ad6408380`.
- Exact 44-support candidate SHA256: `3a5f46cfe253cd11a1319bb967a80cf73ab46825a22bfc3176167e6fc82a29a1`.
- Frozen 1,600-by-42 seed pool SHA256 (little-endian float64): `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`.
- Arb evidence commit: [`6cfcd4f7551bf90050330cf45777812ce86097cc`](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6cfcd4f7551bf90050330cf45777812ce86097cc).
- CI run: [45000754288](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45000754288).

## Strict Arb counterexamples

Every row has target (+5/19721). The listed error intervals are relative errors; the certified absolute-error lower endpoint is strictly greater than (1/3).

| Shard | Canonical representative (I) | Orbit size | Relative-error midpoint |
|---:|---|---:|---:|
| 0 | (0,1,2,7,8,9) | 42 | +0.48448295844595247 |
| 1 | (0,1,3,12,19,24) | 84 | -0.35762424695225622 |
| 2 | (0,1,4,17,26,39) | 42 | +0.35961421784016124 |
| 3 | (0,1,6,19,24,37) | 42 | +0.48062444062884235 |
| 4 | (0,1,9,16,26,27) | 84 | +0.38378424454250665 |
| 5 | (0,2,5,12,18,34) | 84 | +0.34073129058020233 |
| 6 | (0,2,7,20,29,31) | 84 | +0.38835985174491497 |
| 7 | (0,3,7,15,22,34) | 84 | +0.33422417626114355 |

The full 128-bit Arb enclosures, lower/upper endpoints, shard ranges, and per-shard prefix hashes are frozen in `evidence/candidate_103col_22probe_complete_sixth_arb_n21.json`.

## Coverage accounting

- Group-theoretic total: 63,133 sixth-order dihedral orbits and 5,245,786 six-subsets.
- Evaluated before the eight shard-local first violations: 4,406 orbit visits, 367,752 six-subsets, and 16,181,088 principal-minor determinant evaluations.
- All eight shards returned a strict violation; none completed its assigned range.

Thus the workflow's overall job success means the verifier successfully established a candidate rejection, not that the candidate passed a complete sixth-order maximum test. The transcript correctly records `status=strict_violation` and `complete=false`.

## Reweighting step

The eight rows are all distinct from the previous 256 screened sixth rows and 22 certified sixth probes. The next finite design therefore has:

- 103 legal physical columns;
- 1,461 complete second/fourth rows;
- 256 frozen sixth screening rows;
- 30 Arb-certified sixth rows (22 inherited plus eight new);
- seven selected eighth rows;
- 1,754 total normalized LP rows.

The reweighting is a binary64 HiGHS discovery step. Any resulting weights are converted to exact rational probabilities and must independently pass 128-bit Arb checks on every selected row and a fresh 1,024-orbit sixth-order prefix before they are accepted as the next candidate.

## Scope

These eight witnesses reject only the exact pinned 44-support distribution. They do not prove a no-go theorem for the 103-column pool, all legal physical generators, or other Hamiltonian families. A passing selected-row/prefix audit would still not prove the complete sixth-order maximum, any eighth-order maximum, moments of order ten or higher, or an operational Choi/diamond-norm inversion bound.
