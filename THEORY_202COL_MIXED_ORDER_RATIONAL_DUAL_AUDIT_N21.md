# 202-column mixed-order rational dual audit (n=21)

## Scope

This note records a **finite-pool** minimax obstruction for the exact 202 physical columns listed in:

- `evidence/joint_low_six_eighth_lp_202col_uniform_ray_escape_n21.json`
- `evidence/55probe_202col_uniform_ray_escape_dual_certificate_n21.json`

It is not a converse for the full continuous physical family. The moment design contains complete second- and fourth-order rows, but only selected/cut sixth-order rows and selected eighth-order rows.

The 202-column pool consists of 183 canonical columns, nine previously certified nonuniform positive 41-edge open paths, and ten uniform positive 41-edge open paths (labels 1650--1659). The newly appended column 1659 is the finite-time escape of the 201-column dual:
[
t_{201}=\frac{988116600191002478823}{250000000000000}
=3952466.400764009915292,
]
with (c_0=\cdots=c_{40}=t_{201}>0) and closing edge (c_{41}=0).

## Fixed 2,113-row design

| Block | Rows | Status |
|---|---:|---|
| Second order | 21 | Complete |
| Fourth order | 1,440 | Complete |
| Sixth order | 645 | Selected/cut |
| Eighth order | 7 | Selected |
| **Total** | **2,113** | Mixed-order finite design |

The exact row scales used by the LP and the TV post-processing are:
[
s_i=\begin{cases}
1/41 & \text{second order},\\
1/533 & \text{fourth order},\\
5/19721 & \text{sixth order},\\
1/19721 & \text{eighth order}.
\end{cases}
]

For the fixed matrix (A\in\mathbb R^{2113\times202}) and target (y\in\mathbb R^{2113}), the discovery LP targets
[
\eta_{202}=\min_{p\in\Delta_{202}}\|Ap-y\|_\infty.
]

## Exact rational dual and Arb certificate

The binary64 HiGHS discovery returned objective (0.3883774420090974), recomputed maximum residual (0.38837744201062696), primal-dual gap (5.306866057708248\times10^{-14}), and support size 66. These are discovery diagnostics, not the proof.

The independently rationalized dual has:
[
\|z\|_1=1,
\qquad
\lambda+z^Ty=
\frac{895537409593096709}{2305843009214427131}.
]
With exact rational slack (\delta=10^{-9}), the certified lower bound is
[
\boxed{
\eta_{202}\ge
\frac{895537407287253699785572869}
{2305843009214427131000000000}
=0.3883774410090271\ldots>\frac13.
}
]

The 128-bit Arb verifier evaluated all 202 physical columns. The largest shifted-column upper endpoint is
[
-8.472548623521715\times10^{-10}<0.
]
The dual has 66 active rows: four low-order, 59 sixth-order, and three eighth-order.

Evidence provenance:
- LP transcript SHA-256: `98b07b734dcb86c4bff1a28d550d1b1a3dda64857d05d2c38c8136c10de280ba`.
- Rational Arb dual certificate SHA-256: `e76b964f36192069070647964c415c0f87308c26552ca718aa119acf62586187`.
- The certificate pins the LP transcript and the 2,113-row cut design.

## Exact program-mass TV corollary

For each retained row (i), the verifier uses the dihedral-orbit average (\phi_i) of the even-parity character, so (\|\phi_i\|_\infty\le1). With
[
M=\sum_i\frac{|z_i|}{s_i}
=\frac{48920213618867443846539}{11529215046072135655},
]
the bounded-character witness gives
[
\boxed{
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{298512469095751233261857623}
{6522695149182325846205200000000}
=4.5765203227866974\times10^{-5}\ldots
}
]
for every probability mixture over exactly these 202 columns in the selected parity sector.

This is a lower bound for the balanced program-label mass distribution (equivalently, the dephased label-register trace distance). It is **not** a Choi trace-distance or channel diamond-distance lower bound.

## Reproducibility

- 202-column LP reoptimization: [workflow 45617194808](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45617194808), success.
- 202-column rational dual and TV certification: [workflow 45617814843](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45617814843), success.
- Pinned numerical stack: Python 3.11, NumPy 2.3.5, SciPy 1.15.3, python-flint 0.8.0.
- Regression tests: eighth-orbit enumeration and uniform-path torus basis passed.

## What this does not prove

1. It does not cover all 1,641 canonical columns simultaneously, much less the full continuous physical family.
2. It does not complete the 63,133-orbit sixth-order system or the eighth-order orbit system.
3. It does not prove full-family feasibility or a global physical-family converse.
4. It does not imply a Choi or diamond operational error bound.

The 202-column dual's continuous uniform-path pricing is a separate question. A positive torus Arb interval would refute global separation by this particular dual; a subsequent exact finite-time Arb witness would make that escape explicit. Until those checks finish, no continuous-family conclusion is asserted.
