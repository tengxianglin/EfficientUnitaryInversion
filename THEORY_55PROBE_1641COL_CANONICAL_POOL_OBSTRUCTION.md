# Full 1,641-column canonical-pool minimax obstruction

Date: 2026-11-22

## Main result

Let $C_{1641}$ be the complete frozen canonical pool of 1,641 legal 42-site path generators returned by `canonical_ensemble()`. Its little-endian float64 array is pinned by SHA256

`f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98`.

Let $A\in\mathbb R^{1779\times1641}$ be the normalized feature matrix and $y\in\mathbb Q^{1779}$ the normalized target vector for the exact 1,779-row design below. Define

$$
\eta_{1641,55}:=\min_{p\in\Delta_{1641}}\|Ap-y\|_\infty.
$$

The 1,779 rows consist of:

- 1,461 second-/fourth-order rows;
- 311 sixth-order rows: 256 frozen screening rows, 38 parent probes, eight strict separators from the rejected 113-column 38-probe candidate, one strict prefix separator from the rejected 113-column 46-probe candidate, and eight additional strict separators from the rejected 113-column 47-probe candidate;
- seven selected eighth-order rows.

**Theorem.** The frozen 1,641-column canonical pool obeys the rigorous lower bound

$$
\boxed{
\eta_{1641,55}\ge
\frac{3963617383802565315392938733}
{11529215046070612670000000000}
=0.3437890062735403\ldots
>\frac13.
}
$$

The exact gap above $1/3$ is

$$
\frac{361637105337083276178816199}
{34587645138211838010000000000}
=0.010455672940206988\ldots.
$$

Consequently, no probability distribution over the 1,641 canonical generators can meet the $1/3$ normalized-error cap on these rows. Any larger moment objective whose row set contains these 1,779 normalized constraints inherits the same lower bound for mixtures supported on this canonical pool.

## Certificate and exhaustive column audit

The proof uses the exact rational dual vector and multiplier from the 151-column certificate, not a newly fitted dual. The dual satisfies

$$
\|z\|_1=1,\qquad
\lambda=\frac{1326094327570048000}{1152921504607061267},\qquad
\delta=10^{-10}.
$$

Its exact objective before slack is

$$
\lambda+z^Ty=
\frac{396361738495548682}{1152921504607061267}.
$$

The 151 active columns were independently certified with 128-bit Arb in the original certificate. The remaining 1,490 columns were then each evaluated with 128-bit Arb; all 1,490 interval upper endpoints are strictly negative. Thus the union covers all 1,641 columns.

The worst unused-column upper endpoint is

$$
-0.0063598756997121345226805282951280191785\ldots
$$

at canonical column 1632. The worst of the 151 active-column inequalities is still the tighter margin, with Arb upper endpoint below

$$
-8.3697181614344422517024875091804297213\times10^{-11}.
$$

The exhaustive unused-column audit reports:

- status: `strict_full_canonical_pool_separation`;
- completed: `true`;
- canonical columns: 1,641;
- previously certified active columns: 151;
- newly Arb-audited unused columns: 1,490;
- strictly negative unused intervals: 1,490;
- nonnegative unused intervals: 0;
- precision: 128 bits, python-flint 0.8.0 / Arb.

## Reproducibility pins

- 151-column dual certificate SHA256: `e7d7fc4e798ba9f746bac295572e8ad60b1fe2f3b6e080da46412d9ae213d2c6`;
- LP transcript SHA256: `341247c5ceddd5d07b1758b56ff6a7ed1f01f4c05e3e5dd83ead0319046fbaa0`;
- binary64 pricing screen SHA256: `c5c38e4e44616013b7654c71946e99ebbc9332d3ee6449671557b049fbd7ff78`;
- frozen seed-pool SHA256: `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`;
- 151-column index SHA256: `a9168d9f704817bc73bc7ee9a84683820cae5756b83521fd090c77898e6a4d93`;
- unused-column index SHA256: `d02ad9c3e2bc11f70dcd26ce6b42407ec6fd7efb28d1ace5d9c5c113f6e4b4f8`;
- full-pool Arb evidence: `evidence/55probe_151col_full_canonical_pool_arb_n21.json`;
- full-pool Arb workflow: [45034448993](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45034448993), completed successfully;
- evidence commit: [1cd365d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1cd365d7254643132d784926904e315a23096e21).

The workflow also passed frozen-seed verification and the exact orbit-enumeration unit tests before running the 1,490-column Arb audit.

## Proof

For every canonical column $a_j$, the active-column certificate or the full-pool Arb audit establishes

$$
a_j^Tz+\lambda-\delta<0.
$$

For any $p\in\Delta_{1641}$, Hölder's inequality and the simplex constraint give

$$
\|Ap-y\|_\infty
\ge z^T(y-Ap)
=z^Ty-\sum_{j=1}^{1641}p_j a_j^Tz.
$$

Since every column obeys $a_j^Tz\le-\lambda+\delta$,

$$
-\sum_jp_ja_j^Tz\ge\lambda-\delta.
$$

Therefore

$$
\|Ap-y\|_\infty\ge z^Ty+\lambda-\delta,
$$

which is exactly the boxed rational lower bound. This proves the theorem.

## Scope and limitations

**Proved:** the $1/3$ cap is impossible for every convex mixture over the entire frozen 1,641-column canonical 42-site path pool on the pinned 1,779-row design. Any all-moment objective that contains these same normalized rows is also bounded below by this value for mixtures from this pool.

**Not proved:** the same obstruction for physical generators outside the frozen canonical pool; a no-go theorem for every legal Hamiltonian in a continuous or larger discrete family; an operational Choi/diamond-norm lower bound; or the optimal minimax value over the full physical family.

The 311 sixth-order and seven eighth-order rows remain a selected subset of their complete orbit domains. The proof does not claim that these selected rows certify a particular ensemble's complete sixth/eighth moments; it is a dual lower bound applying to every mixture in the pinned pool.

## Reproduction

```bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python verify_151col_55probe_dual_certificate.py
python verify_55probe_151col_full_canonical_pool_arb.py
```

The final command checks all 1,490 columns not already included in the 151-column certificate and exits nonzero unless every Arb upper endpoint is strictly negative.
