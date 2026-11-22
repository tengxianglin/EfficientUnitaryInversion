# 162-column mixed-order minimax obstruction on a 2,113-row design

## Theorem

Fix the 162 physical generators whose column order is recorded in
evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json: 151 frozen
canonical path generators, one exact-rational continuous-path escape
generator (label 1641), and ten further frozen canonical path generators.
Let \(A\in\mathbb R^{2113\times162}\) be the normalized feature matrix and
\(y\in\mathbb Q^{2113}\) the target vector, with rows ordered as:

- 1,461 complete second-/fourth-order rows;
- 645 sixth-order rows (311 original selected rows plus 334 distinct cuts);
- seven selected eighth-order rows.

Then every probability vector \(p\in\Delta_{162}\) satisfies
\[
\boxed{
\|Ap-y\|_\infty\ge
\frac{1421382955036825653848272131}
{2882303761517278690000000000}
=0.493141276091106\ldots>\frac13.
}
\]

Thus no reweighting of these fixed 162 generators can satisfy the \(1/3\)
cap on this exact mixed-order 2,113-row design.

The rational dual has 40 nonzero coordinates: 38 sixth-order and two
eighth-order coordinates, with no active low-order coordinates. Since two
eighth-order coordinates are nonzero, this is **not** a sixth-only
certificate and does not establish the same lower bound after deleting the
seven eighth-order rows. A separate 2,106-row sixth-only LP is required for
that claim.

## Exact dual certificate

The committed certificate gives
\[
\|z\|_1=1,
\qquad
\lambda+z^\mathsf Ty
=
\frac{142138295532505603}{288230376151727869},
\qquad
\delta=10^{-10}.
\]
For every one of the 162 physical columns \(a_j\), a 128-bit Arb interval
computation proves
\[
a_j^\mathsf Tz+\lambda-\delta<0.
\]
The largest interval upper endpoint is
\[
-7.5752412530783022251271948310938060447\times10^{-11}.
\]
Consequently, for every \(p\in\Delta_{162}\),
\[
z^\mathsf TAp
=\sum_jp_jz^\mathsf Ta_j
\le-\lambda+\delta,
\]
and Hölder's inequality yields
\[
\|Ap-y\|_\infty
\ge z^\mathsf T(y-Ap)
\ge z^\mathsf Ty+\lambda-\delta.
\]
The resulting exact lower bound is the fraction stated in the theorem. Its
exact gap above \(1/3\) is
\[
\frac{1381845103593198271544816393}
{8646911284551836070000000000}
=0.15980794275777266\ldots.
\]

## Discovery LP and independent verification

The binary64 HiGHS discovery LP has objective
\(0.4931412761911509\), independently recomputed maximum
\(0.49314127619252646\), support size 40, and primal-dual discovery gap
\(1.73\times10^{-14}\). These are discovery values only. The exact rational
dual and 128-bit Arb column inequalities, not the floating LP objective,
establish the theorem.

Evidence:
- LP transcript: evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json.
- Exact certificate: evidence/55probe_162col_full_sixth_cut_dual_certificate_n21.json.
- Arb verifier: verify_162col_full_sixth_cut_dual_arb.py.
- Successful workflow: [45060433409](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45060433409).
- Certificate commit: [4d382ab](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4d382ab33e52d4785e314a088402cccffc9a0ed6).

## Scope

This is a rigorous finite-pool minimax theorem for the specified 162
generators and the pinned 2,113-row mixed-order design. It applies to any
objective whose row set contains all 2,113 rows. It does not establish a
sixth-only lower bound, does not rule out other canonical or continuous path
generators, and does not establish a result for the unrestricted continuous
physical family. The seven eighth-order rows are part of the certified
objective and must not be silently dropped from the theorem statement.
