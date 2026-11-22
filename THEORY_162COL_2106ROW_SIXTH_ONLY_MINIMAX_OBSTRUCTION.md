# 162-column sixth-only minimax obstruction

## Theorem

Fix the 162 physical generators in the column order recorded by
evidence/joint_low_six_lp_162col_sixth_only_n21.json: 151 frozen canonical
path generators, one exact-rational continuous-path generator (label 1641),
and ten further frozen canonical path generators. Let \(R_6^{\mathrm{cut}}\)
be the 645 distinct sixth-order \(D_{42}\) orbits in the pinned cut
inventory, and let \(R_{\le4}\) be the complete 1,461 second-/fourth-order
rows. The 2,106-row design contains **no eighth-order rows**.

For every probability vector \(p\in\Delta_{162}\), the exact rational
certificate proves
\[
\max_{r\in R_{\le4}\cup R_6^{\mathrm{cut}}}
| (Ap-y)_r |
\ge
\frac{10977154378457033940786269263}
{23058430092137307370000000000}
=0.47605818499326774\ldots>\frac13.
\]

More strongly, the certified dual vector has **zero coordinates on all
second-/fourth-order rows** and is supported on exactly 45 of the 645
sixth-order rows. Hence the same bound is already a sixth-only statement:
\[
\max_{r\in R_6^{\mathrm{cut}}}|(Ap-y)_r|
\ge 0.47605818499326774\ldots.
\]
Since \(R_6^{\mathrm{cut}}\) is a subset of the complete 63,133-orbit
sixth-order \(D_{42}\) domain, it follows that
\[
\boxed{
\max_{r\in R_6^{\mathrm{all}}}|(Ap-y)_r|
\ge 0.47605818499326774\ldots>\frac13
}
\]
for every mixture over this fixed 162-generator pool.

## Exact dual certificate

The rationalized dual satisfies
\[
\|z\|_1=1,
\qquad
\lambda+z^\mathsf Ty
=
\frac{1097715438076287695}{2305843009213730737},
\qquad
\delta=10^{-10}.
\]
Its support has 45 nonzero coordinates, all in sixth-order rows:
\[
|\operatorname{supp}(z)|=45,\quad
|\operatorname{supp}(z)\cap R_{\le4}|=0,\quad
|\operatorname{supp}(z)\cap R_6^{\mathrm{cut}}|=45.
\]
For every one of the 162 physical columns \(a_j\), a 128-bit Arb
computation certifies
\[
a_j^\mathsf Tz+\lambda-\delta<0.
\]
The largest interval upper endpoint after slack is
\[
-9.4121757377289108485479722255741978272\times10^{-11}.
\]
The exact lower-bound gap above \(1/3\) is
\[
\frac{9873033043233794452358807789}
{69175290276411922110000000000}
=0.1427248516599344\ldots.
\]

For any \(p\in\Delta_{162}\),
\[
z^\mathsf TAp=\sum_jp_jz^\mathsf Ta_j\le-\lambda+\delta,
\]
so by Hölder's inequality,
\[
\|Ap-y\|_\infty\ge z^\mathsf T(y-Ap)
\ge z^\mathsf Ty+\lambda-\delta.
\]
Because every nonzero coordinate of \(z\) is a sixth-order row, this
inequality does not rely on any eighth-order constraint.

## Numerical discovery versus proof

The binary64 HiGHS discovery LP has objective \(0.47605818509327597\),
independently recomputed maximum \(0.47605818509336406\), support size 45,
and primal-dual discovery gap \(6.11\times10^{-16}\). The floating dual
L1 norm is slightly above one; these values are not the theorem. The theorem
uses the exact rationalized dual with L1 norm exactly one and the Arb
interval checks for all 162 columns.

## Evidence

- Sixth-only LP transcript: evidence/joint_low_six_lp_162col_sixth_only_n21.json.
- Strict certificate: evidence/55probe_162col_sixth_only_dual_certificate_n21.json.
- Arb verifier: verify_162col_sixth_only_dual_arb.py.
- Workflow: [45061253393](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45061253393).
- Certificate commit: to be recorded from the successful workflow commit.

## Scope

This is a rigorous minimax obstruction for the specified 162 physical
generators. It does not rule out additional canonical columns, other
continuous path generators, other Hamiltonian families, or the unrestricted
continuous physical family. The complete-sixth conclusion is valid because
the dual uses only 45 sixth-order rows, each belonging to the complete
63,133-orbit sixth-order domain; no eighth-order rows enter the certificate.
