# 152-column mixed-order minimax obstruction on a 2,113-row cut design

## Theorem

Fix the 152 physical generators consisting of the 151 frozen canonical path
columns listed in
`evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json`
together with the exact-rational continuous-path escape generator at column
1641. Let \(A\in\mathbb R^{2113\times152}\) be their normalized feature matrix
and \(y\in\mathbb R^{2113}\) the exact target vector, with rows ordered as:

- 1,461 complete second-/fourth-order rows;
- 645 sixth-order rows (the original 311 selected rows plus all 334 distinct
  sixth-order orbits found violating the previous candidate);
- seven selected eighth-order rows.

Then every probability vector \(p\in\Delta_{152}\) satisfies
\[
\boxed{
\|Ap-y\|_\infty\ge
\frac{31229779445108377178763165603}
{61489146912368343970000000000}
=0.5078909208094186\ldots>\frac13.
}
\]

Consequently, no reweighting of these fixed 152 physical generators can meet
the \(1/3\) cap on this finite mixed-order row set. The certificate has 40
nonzero dual coordinates: one low-order, 37 sixth-order, and two eighth-order
coordinates. Because the dual uses eighth-order rows, it is **not** a
sixth-only certificate and does not by itself prove a lower bound for the
objective with all eighth-order rows removed. It does give a lower bound for
any objective whose row set contains all 2,113 rows listed above.

## Dual certificate and proof

The frozen certificate contains a rational vector \(z\in\mathbb Q^{2113}\)
and \(\lambda\in\mathbb Q\) with
\[
\|z\|_1=
1,
\]
\[
z^\mathsf Ty+\lambda-\delta
=
\frac{36597397722434817858556439}
{72057594037927936000000000},
\qquad \delta=10^{-9}.
\]
For each of the 152 physical columns \(a_j\), a 128-bit Arb computation
certifies
\[
a_j^\mathsf Tz+\lambda-\delta<0.
\]
The largest interval upper endpoint over all columns is
\[
-4.2492156984681046212238277835698169369\times10^{-11}
\]
(up to the Arb interval radius recorded in the certificate).

For any \(p\in\Delta_{152}\), convexity gives
\[
z^\mathsf TAp
=\sum_jp_jz^\mathsf Ta_j
\le-\lambda+\delta.
\]
By Hölder's inequality and \(\|z\|_1\le1\),
\[
\|Ap-y\|_\infty
\ge z^\mathsf T(y-Ap)
\ge z^\mathsf Ty+\lambda-\delta,
\]
which is the stated bound.

The exact dual objective before slack is
\[
\lambda+z^\mathsf Ty
=\frac{3122977945125729187}{6148914691236834397},
\]
and the certified gap above \(1/3\) is
\[
\frac{32200191422956787566289496809}
{184467440737105031910000000000}
=0.17455758747608527\ldots.
\]

The rational dual has only 40 nonzero coordinates: one low-order row, 37
sixth-order rows, and two eighth-order rows. The remaining 2,073 zero
coordinates contribute exactly nothing and are not evaluated in the Arb
column sums.

## Evidence and scope

- 128-bit Arb verifier: `verify_152col_full_sixth_cut_dual.py`
- Exact LP transcript, including rationalizable HiGHS dual multipliers:
  `evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json`
- Strict certificate:
  `evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json`
- Arb workflow and committed certificate: [45058397922](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45058397922)
- Certificate commit: [d27ff52](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d27ff52bd8c21315e4534fd56bf5942630cc3c73)

This is a strict mixed-order minimax no-go only for the specified 152-column
pool and the exact 2,113-row design. It does **not** rule out additional
canonical columns, other continuous path generators, other Hamiltonian
families, or the unrestricted continuous physical family. It is not a
sixth-only lower-bound certificate because two active dual coordinates are
eighth-order rows. The 334 cuts were identified by a complete binary64 scan;
the dual certificate rigorously uses the exact 645-row inventory pinned in
the LP transcript, so it does not require treating all 334 individual screen
values as Arb-certified counterexamples.
