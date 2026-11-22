# 103-column / 38-probe dual obstruction

**Evidence snapshot:** 2026-11-22  
**LP transcript:** `evidence/joint_low_six_eighth_lp_103col_38probe_n21.json`  
**Arb certificate:** `evidence/38probe_103col_dual_certificate_n21.json`

## Finite minimax problem

Let the 103 columns be the pinned legal 42-site path generators listed in the certificate. Let (A\in\mathbb R^{1762\times 103}) contain the normalized moment features, and let (y\in\mathbb Q^{1762}) be the normalized target. The row blocks are:

- 1,461 second-/fourth-order rows;
- 256 screened sixth-order rows;
- 38 additional sixth-order rows, each added after a strict 128-bit Arb witness against the preceding candidate;
- 7 selected eighth-order rows.

For a probability vector (p\in\Delta_{103}), define
\[
R(p)=\|Ap-y\|_\infty.
\]

The binary64 HiGHS LP is only the discovery step. Its objective is (0.336849522971994), above (1/3). The exact rational dual is then independently checked using 128-bit Arb against all 103 physical columns.

## Certified dual statement

The frozen certificate has an exact rational vector (z\in\mathbb Q^{1762}), exact (\|z\|_1=1), rational (\lambda), and slack
\[
\delta=10^{-8}.
\]
For every one of the 103 pinned columns (a_j), Arb certifies
\[
a_j^Tz+\lambda-\delta\le 0.
\]
Consequently, for every (p\in\Delta_{103}),
\[
R(p)\ge \lambda+z^Ty-\delta
=\frac{828503567612290605891211277}
{2459565876500878872300000000}
\approx 0.3368495129681047
>\frac13.
\]
The exact certified gap above (1/3) is
\[
\frac{2882758481776993930403759}
{819855292166959624100000000}>0.
\]

This is a rigorous finite-pool minimax obstruction for the stated 1,762 normalized rows and exactly these 103 columns. It is not a no-go theorem for the other canonical columns, newly generated physical paths, other Hamiltonian families, all moments, or operational Choi/diamond error.

## Why the next step is column pricing

The previous 93-column dual was escaped by ten additional legal columns. The current 103-column dual therefore must be tested against the remaining 1,538 columns in the frozen 1,641-column canonical path pool. A binary64 screen ranks all unused columns; the top positive reduced-cost candidates are then recomputed with Arb before any is admitted to an expanded pool. Positive certified pricing invalidates this dual only for the expanded pool; it does not itself prove a feasible ensemble.

Reproduce the pricing ladder with:

```bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python price_unused_columns_against_38probe_103col_dual.py
python verify_38probe_103col_dual_pricing_arb.py
```

The scripts pin the LP and dual-certificate hashes, row dimensions, canonical-column hash, and 103-column index hash. The Arb stage checks the exact matrix exponential and normalized feature functional for the leading screened candidates.
