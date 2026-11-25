# Manuscript audit addendum — Run 26 (2026-11-25)

## 203-column finite-pool theorem

The explicit 202-dual finite-time escape was appended as physical column 1660. The fixed mixed-order LP was reoptimized on 203 physical columns and then independently rationalized and certified.

The binary64 discovery LP reported:
- dimensions: 2,113 rows × 203 columns;
- objective: 0.38670687143193666;
- recomputed maximum residual: 0.38670687143626825;
- primal/dual discovery gap: 1.4449552665496412e-13;
- positive support size: 68.

These are solver diagnostics, not the theorem. The exact rational dual has \(\|z\|_1=1\), objective
\[
\frac{19815229691242147}{51240955760304989},
\]
and exact rational slack \(10^{-9}\). The 128-bit Arb verifier checks all 203 physical columns and certifies the maximum shifted-column upper endpoint is \(-8.650750565965185\times10^{-10}<0\). Hence
\[
\eta_{203}\ge
\frac{19815229640001191239695011}{51240955760304989000000000}
=0.3867068704317870026\ldots>\frac13.
\]

The exact-rational program-mass corollary is
\[
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{19815229640001191239695011}{422945788402254629538000000000}
=4.685051886875713\ldots\times10^{-5}.
\]
It applies to mixtures over the exact 203-column pool in one selected parity sector and to the corresponding dephased program-label register, not to Choi trace distance or channel diamond distance.

## Evidence and CI

- 203-column LP: `evidence/joint_low_six_eighth_lp_203col_uniform_ray_escape_n21.json`
- rational dual: `evidence/55probe_203col_uniform_ray_escape_dual_certificate_n21.json`
- TV certificate: `evidence/203col_program_mass_tv_bound_n21.json`
- reoptimization run [45622431946](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45622431946): success
- rational/Arb certification run [45624017940](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45624017940): success
- theory note: `THEORY_203COL_MIXED_ORDER_RATIONAL_DUAL_AUDIT_N21.md`

The finite-time path added at column 1660 is
\[
t_{202}=\frac{2906260875695546623319}{1000000000000000}>0,
\quad c_0=\cdots=c_{40}=t_{202},\ c_{41}=0.
\]
Its positive pricing for the 202-column dual is already independently Arb-certified. The 203-column dual itself has **not yet** been priced over the continuous torus; this is the next decisive check.

## Manuscript boundary

The repository still has no editable TeX/Bib/PDF manuscript source. This addendum records a verified repository theorem and does not claim the public arXiv manuscript has been edited. The finite-pool theorem does not settle the full all-even-principal-minor positive-ensemble problem at n=21, and the selected/cut sixth/eighth rows are not complete orbit systems.
