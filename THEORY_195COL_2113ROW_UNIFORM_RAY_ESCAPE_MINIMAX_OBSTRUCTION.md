# 195-column / 2,113-row uniform-ray minimax obstruction

## Theorem

Let \(A_{195}\in\mathbb R^{2113\times195}\) and \(y\in\mathbb R^{2113}\) be the frozen mixed-order design and target recorded in:

- evidence/joint_low_six_eighth_lp_195col_uniform_ray_escape_n21.json
- evidence/55probe_195col_uniform_ray_escape_dual_certificate_n21.json

The 195 physical columns consist of 183 selected canonical generators, nine previously Arb-certified nonuniform positive-coupling paths, and three explicit equal-coupling paths. The last is physical column 1652, with all 41 couplings equal to

\[
t_* = 5918.073474550670653
=\frac{5918073474550670653}{10^{15}}>0.
\]

Then every probability vector \(p\in\Delta_{195}\) obeys

\[
\boxed{
\|A_{195}p-y\|_\infty
\ge
\frac{2803294808039097361653228789}
{6588122883467712110000000000}
=0.42550736493906444\ldots
>\frac13.
}
\]

This is a finite-pool theorem for exactly these 195 columns and this 2,113-row design.

## Exact dual certificate

The verifier reconstructs a rational vector \(z\in\mathbb Q^{2113}\), scalar \(\lambda\in\mathbb Q\), and slack

\[
\delta=10^{-10},
\]

with

\[
\|z\|_1=1,
\qquad
\beta:=\lambda+z^\mathsf T y
=\frac{280329480869790965}{658812288346771211}.
\]

For every listed physical column \(a_j\), the 128-bit Arb verifier encloses

\[
z^\mathsf T a_j+\lambda-\delta
\]

in a strictly negative interval. All 195 intervals are checked independently. The largest upper endpoint among them is

\[
-7.804834406606967\times10^{-11}<0.
\]

Consequently, for every \(p\in\Delta_{195}\),

\[
z^\mathsf T A_{195}p+\lambda\le\delta,
\]

and hence

\[
z^\mathsf T(A_{195}p-y)\le\delta-\beta<0.
\]

Hölder's inequality gives

\[
\beta-\delta
\le |z^\mathsf T(A_{195}p-y)|
\le \|z\|_1\,\|A_{195}p-y\|_\infty
=\|A_{195}p-y\|_\infty,
\]

which proves the claimed bound. The displayed rational lower bound is exactly \(\beta-\delta\); its excess over \(1/3\) is

\[
\frac{1821761540649579974959686367}
{19764368650403136330000000000}>0.
\]

## Numerical discovery versus proof

The deterministic binary64 HiGHS discovery run reported:

- objective: \(0.4255073650390678\);
- independently recomputed maximum residual: \(0.4255073650390957\);
- primal/dual diagnostic gap: approximately \(2.28\times10^{-15}\);
- positive support size: 64.

These are optimization diagnostics, not the proof. The theorem above follows from the exact rational dual and the independent 128-bit Arb column checks.

The dual support has 64 nonzero coordinates: 2 low-order rows, 61 selected/cut sixth-order rows, and 1 selected eighth-order row. The full row design contains 1,461 low-order rows, 645 selected/cut sixth-order rows, and 7 selected eighth-order rows.

## Reproducibility and provenance

- Parent 194-column LP SHA256: c6dec42436d0181a9ff5012153d1896f4fcb0ca8a28cf39c6cdb321440dd7a66
- Parent 194-column dual certificate SHA256: 7864da033a71d7d2666cde32cf7f900c9a9a30893cbc7b90942fa09517cab474
- Base 192-column LP SHA256: ed966f1c3f755b1910f7f34be978af88ee290821ea643cb7690d83c7aeab686a
- Current 195-column LP transcript SHA256: 0d5b2d821b95e3229b3ffbcbfd3dafacd80cb76ba1aba55e2858183d53792908
- Successful 195-column reoptimization and Arb workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45242902521
- Evidence commit: https://github.com/tengxianglin/EfficientUnitaryInversion/commit/93c2903e4de3f57dba28e2599841efb0a3fc9471

Reproduce with the pinned environment in .github/workflows/eui-reoptimize-195col-uniform-ray.yml. The workflow rechecks the 193- and 194-column parent dual/time certificates, rebuilds the 195-column LP, and runs verify_195col_uniform_ray_dual_arb.py.

## Scope and limitations

This theorem does **not** establish any of the following:

1. separation of the full 1,641-column canonical inventory;
2. a minimax obstruction or feasibility theorem for the entire continuous positive-coupling family;
3. completeness of the sixth- or eighth-order orbit constraints (the current design uses selected/cut sixth-order rows and seven selected eighth-order rows);
4. a Choi-infidelity or diamond-distance operational error guarantee.

The next decisive question is whether this new 195-column dual itself escapes somewhere on the exact 21-dimensional uniform-path torus. A positive Arb point would refute global separation by this particular dual only; failure of a finite multi-start search would not prove global separation.
