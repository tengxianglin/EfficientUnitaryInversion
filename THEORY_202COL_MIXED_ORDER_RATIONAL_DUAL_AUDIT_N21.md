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


## Continuous uniform-path pricing of the 202-column dual

The 21-dimensional torus search used eight deterministic starts and at most 120 L-BFGS-B iterations per start. The best binary64 discovery score was 0.9971550877716457. Analytic-gradient checks against complex-step and central differences had maximum reported relative defect (2.1910138333004715\times10^{-9}).

The exact decimal phase vector was independently evaluated with 128-bit Arb:
[
S_{202}(R(\theta_*))\in
[0.997155087771645424273385402820507
\pm5.10\times10^{-34}]>0.
]
The interval lower endpoint is strictly positive. The Arb output pins the 202-column dual SHA-256
`e76b964f36192069070647964c415c0f87308c26552ca718aa119acf62586187`
and LP SHA-256
`98b07b734dcb86c4bff1a28d550d1b1a3dda64857d05d2c38c8136c10de280ba`.

Together with the rational-independence/dense-ray result in `THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md`, continuity implies that **some finite positive equal-coupling open-path time exists** at which this particular 202-column dual has positive pricing. This is an existential conclusion, not yet an explicit rational-time certificate. The dedicated finite-time search and Arb verifier are running separately; no numerical finite-time claim should be made until their evidence is committed.


## Explicit finite-time physical escape of the 202-column dual (Run 25, 2026-11-25)

The positive torus pricing certificate above has now been strengthened to an explicit finite-time witness. The deterministic one-dimensional search used 12 starts, at most 400 L-BFGS-B iterations per start, and seed `202611251840`. It selected
\[
 t_{202}=2906260.875695546623319
 =\frac{2906260875695546623319}{1000000000000000}>0.
\]
For the 42-site open path,
\[
 c_0=\cdots=c_{40}=t_{202},\qquad c_{41}=0,
\]
so all 41 internal couplings are strictly positive. The independent 128-bit Arb verifier (python-flint 0.8.0) certifies
\[
 S_{202}(e^{t_{202}K_*})
 \in[0.1751293387639196832622918436\pm5.42\times10^{-29}]>0.
\]
Its lower-endpoint enclosure is
\[
 [0.17512933876391968326229184354589133476\pm1.71\times10^{-39}],
\]
which is strictly positive. The certificate pins the 202-column rational dual, 202-column LP, cut design, torus certificate and deterministic search transcript by SHA-256. The successful end-to-end workflow is [45618890398](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45618890398); the earlier attempt [45618516687](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45618516687) failed on a verifier-dimension bug, corrected in commit [dd27977](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/dd2797752e177b4a339279ee27c3a254e9168bc1).

**Interpretation.** This is a direct physical counterexample to global separation by this particular 202-column dual. It does not invalidate the exact 202-column finite-pool minimax theorem, prove feasibility or infeasibility of the full continuous family, complete the selected sixth/eighth moments, or imply a Choi/diamond bound.

The next finite-pool cutting-plane step is now implemented in `reoptimize_203col_uniform_ray_escape.py`: append this exact path as physical column 1660 and rerun the same 2,113-row mixed-order LP. Its pinned workflow is `.github/workflows/eui-reoptimize-203col-uniform-ray.yml`. A binary64 result remains discovery only; any above-cap result must be rationalized and independently Arb-certified on all 203 columns, while any below-cap result requires an exact primal audit and full sixth-order separation.
