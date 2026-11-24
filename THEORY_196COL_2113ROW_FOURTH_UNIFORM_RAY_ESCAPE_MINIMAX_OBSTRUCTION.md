# 196-column, 2,113-row minimax obstruction after the fourth uniform-ray path

## Status

An exact rational dual has been independently checked with python-flint/Arb at 128-bit precision against all 196 listed physical columns of the pinned 2,113-row mixed-order design. The resulting finite-pool theorem is

\[
\boxed{
\min_{p\in\Delta_{196}}\|A_{2113\times196}p-y\|_\infty
\ge
\frac{18903346635163739503488879}
{45035996273704960000000000}
=0.41973861353658526\ldots>\frac13.
}
\]

This is a finite-pool result only. Separate 128-bit Arb certificates now prove that the same dual has positive pricing on the uniform-path torus and at an explicit finite equal-positive-coupling time \(t_*=3070.785790481181266\); see [the torus theorem](THEORY_196COL_UNIFORM_TORUS_DUAL_ESCAPE.md) and [the finite-time certificate](evidence/196col_uniform_ray_time_arb_n21.json).

## 1. Pinned physical pool and row design

The 196 physical columns consist of:
- 183 selected canonical physical generators;
- nine previously Arb-certified nonuniform positive-coupling paths;
- four explicit equal-coupling positive paths.

The fourth uniform path was certified for the 195-column dual and is appended as physical column 1653:
\[
c_1=\cdots=c_{41}=t_*,
\qquad
t_*=\frac{2901925271922439151}{500000000000000}
=5803.850543844878302>0.
\]

The 2,113 rows are:
- 1,461 complete second-/fourth-order rows;
- 645 selected/cut sixth-order rows;
- seven selected eighth-order rows.

This is not the complete sixth- or eighth-order orbit inventory.

## 2. Exact rational dual certificate

The 128-bit Arb certificate records
\[
\|z\|_1=
\frac{4611686018427369049}{4611686018427387904}<1,
\]
\[
\lambda=
\frac{1509960951366323}{1125899906842624},
\qquad
\beta=\lambda+z^{\mathsf T}y
=
\frac{1935702695901935527}{4611686018427387904},
\]
and the strict slack
\[
\delta=10^{-10}.
\]

Every one of the 196 physical columns is checked using the shifted inequality
\[
z^{\mathsf T}a_j+\lambda-\delta<0.
\]
The certificate contains 196 Arb column intervals. The maximum shifted column-LHS upper bound reported by the independent verifier is
\[
-4.4216806140854604\times10^{-11}<0.
\]
The largest unshifted upper interval is on column 1647 and is approximately \(5.57831938591454\times10^{-11}<\delta\).

The exact dual support has 63 nonzero coordinates:
- five low-order rows;
- 57 sixth-order rows;
- one eighth-order row.

The binary64 HiGHS discovery objective is \(0.41973861363658294\); the independently recomputed maximum residual is \(0.4197386136366168\). These are discovery diagnostics, not the proof.

## 3. Proof of the finite-pool lower bound

For every listed column,
\[
z^{\mathsf T}a_j+\lambda<\delta.
\]
For any probability vector \(p\in\Delta_{196}\), convexity gives
\[
z^{\mathsf T}A p+\lambda
=\sum_j p_j(z^{\mathsf T}a_j+\lambda)
<\delta.
\]
Therefore
\[
z^{\mathsf T}(y-Ap)
=\lambda+z^{\mathsf T}y-(z^{\mathsf T}Ap+\lambda)
>\beta-\delta.
\]
Hölder's inequality yields
\[
\|y-Ap\|_\infty
\ge
\frac{z^{\mathsf T}(y-Ap)}{\|z\|_1}
>
\frac{\beta-\delta}{\|z\|_1}
>
\beta-\delta,
\]
because \(0<\|z\|_1<1\). The exact rational value of \(\beta-\delta\) is the boxed lower bound above. Hence the minimax residual for this exact 196-column, 2,113-row design is strictly larger than \(1/3\). \(\square\)

## 4. Provenance and reproduction

The 196-column LP and dual pin:
- 195-column parent LP SHA256: 0d5b2d821b95e3229b3ffbcbfd3dafacd80cb76ba1aba55e2858183d53792908;
- 195-column parent dual SHA256: 8371f7f2d4d866839b223dbe1b0c3e872a220092bc22b7cbc69384f08acb456c;
- fourth uniform-ray finite-time certificate SHA256: 26200d428d7a38fa68d1f6ff45cb4c44aac2a82b2965163a647ea95f6cc78ee1;
- frozen seed-pool SHA256: 93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315;
- cut-design SHA256: d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f.

Evidence:
- [196-column LP transcript](evidence/joint_low_six_eighth_lp_196col_uniform_ray_escape_n21.json)
- [128-bit Arb dual certificate](evidence/55probe_196col_uniform_ray_escape_dual_certificate_n21.json)
- [Independent verifier](verify_196col_uniform_ray_dual_arb.py)
- [Reoptimizer](reoptimize_196col_uniform_ray_escape.py)
- [Reproducible workflow](.github/workflows/eui-reoptimize-196col-uniform-ray.yml)
- [Evidence commit 3ef1287](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/3ef1287d4dcecc7bdf21cc5cbf4efaf09f33cecf)

## 5. Scope and continuous uniform-ray escape

**Proved finite-pool statement:** the exact 196-column / 2,113-row minimax residual is greater than \(1/3\), for exactly the listed columns and selected rows.

**New proved continuous-pricing statement:** the same exact 196-column dual has a strictly positive 128-bit Arb pricing interval at an exact rational point of the 21-dimensional uniform-path torus. By the rational independence of the 21 path frequencies and continuity of the pricing functional, some finite \(t>0\) on the equal-positive-coupling ray has positive pricing. See [the separate torus-escape theorem](THEORY_196COL_UNIFORM_TORUS_DUAL_ESCAPE.md) and its [Arb certificate](evidence/196col_uniform_torus_arb_n21.json).

These statements are compatible: the escaping physical path is outside the 196 listed columns. The positive torus point refutes global separation by this particular dual, not the finite-pool minimax theorem.

**Still not proved:** separation of the full 1,641-column canonical inventory; a global separator for all continuous positive-coupling paths; complete sixth/eighth orbit control; feasibility or infeasibility of mixtures over the full continuous physical family; any Choi-infidelity or diamond-distance guarantee.


## Explicit finite-time physical escape (2026-11-24)

The exact rational time is
\[
t_*=3070.785790481181266=\frac{1535392895240590633}{500000000000000}>0,
\]
with all 41 path couplings equal to \(t_*\). The independent 128-bit Arb certificate gives
\[
S_{196}(e^{t_*K_*})\in[0.3637338868622431662555343998069\pm6.07\times10^{-32}]>0.
\]
The certificate pins the current 196-column dual, LP, torus certificate, and 193/194/195-column parent time certificates by SHA256. It is committed in [6e6a670](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6e6a6705fd44b85b1274132d7530796145c7b3a1) after [successful workflow 45283332130](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45283332130).
