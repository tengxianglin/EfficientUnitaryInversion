# 152-column minimax obstruction from the complete-sixth cutting-plane set

## Theorem

Fix the 152 physical generators consisting of the 151 frozen canonical path
columns listed in
`evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json`
together with the exact-rational continuous-path escape generator at column
1641. Let (Ainmathbb R^{2113	imes152}) be their normalized feature matrix
and (yinmathbb R^{2113}) the exact target vector, with rows ordered as:

- 1,461 complete second-/fourth-order rows;
- 645 sixth-order rows (the original 311 selected rows plus all 334 distinct
  sixth-order orbits found violating the previous candidate);
- seven selected eighth-order rows.

Then every probability vector (pinDelta_{152}) satisfies
[
oxed{
|Ap-y|_inftyge
rac{31229779445108377178763165603}
{61489146912368343970000000000}
=0.5078909208094186ldots>rac13.
}
]

Consequently, no reweighting of these fixed 152 physical generators can meet
the (1/3) cap on this finite row set. Since the complete sixth-order maximum
contains all 645 sixth-order rows above, the same lower bound applies to the
complete-sixth objective restricted to this fixed 152-column pool.

## Dual certificate and proof

The frozen certificate contains a rational vector (zinmathbb Q^{2113})
and (lambdainmathbb Q) with
[
|z|_1=1,qquad
z^mathsf Ty+lambda-delta
=
rac{31229779445108377178763165603}
{61489146912368343970000000000},
quad delta=10^{-10}.
]
For each of the 152 physical columns (a_j), a 128-bit Arb computation
certifies
[
a_j^mathsf Tz+lambda-delta<0.
]
The largest interval upper endpoint over all columns is
[
-4.2492156984681046212238277835698169369	imes10^{-11}
]
(up to the Arb interval radius recorded in the certificate).

For any (pinDelta_{152}), convexity gives
[
z^mathsf TAp
=sum_jp_jz^mathsf Ta_j
le-lambda+delta.
]
By Hölder's inequality and (|z|_1=1),
[
|Ap-y|_infty
ge z^mathsf T(y-Ap)
ge z^mathsf Ty+lambda-delta,
]
which is the stated bound.

The exact dual objective before slack is
[
lambda+z^mathsf Ty
=rac{3122977945125729187}{6148914691236834397},
]
and the certified gap above (1/3) is
[
rac{32200191422956787566289496809}
{184467440737105031910000000000}
=0.17455758747608527ldots.
]

## Evidence and scope

- 128-bit Arb verifier: `verify_152col_full_sixth_cut_dual.py`
- Exact LP transcript, including rationalizable HiGHS dual multipliers:
  `evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json`
- Strict certificate:
  `evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json`
- Arb workflow: [45057772894](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45057772894)
- Conflict-safe reproducibility workflow: [45058397922](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45058397922)

This is a strict minimax no-go only for the specified 152-column pool. It
does **not** rule out additional canonical columns, other continuous path
generators, other Hamiltonian families, or the unrestricted continuous
physical family. The 334 cuts were identified by a complete binary64 scan;
the dual certificate rigorously uses the exact 645-row inventory pinned in
the LP transcript, so it does not require treating all 334 individual screen
values as Arb-certified counterexamples.
