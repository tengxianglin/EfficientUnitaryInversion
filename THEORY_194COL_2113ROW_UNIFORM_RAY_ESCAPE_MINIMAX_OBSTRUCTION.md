# 194-column, 2,113-row uniform-ray minimax obstruction

**Status:** exact rational dual and independent 128-bit Arb certificate complete. The theorem covers exactly the 194 physical columns in the pinned LP and the fixed 2,113-row mixed-order design.

## 1. Physical pool

The 194-column pool is obtained from the preceding 193-column pool by appending the explicit uniform positive-coupling path

\[
t_*=588.216987832015661
=\frac{588216987832015661}{10^{15}}>0,
\]

as physical column 1651. All 41 edge couplings of this path equal \(t_*\). The preceding uniform path at column 1650 has exact time

\[
t_{\mathrm{old}}=
\frac{14425249926691145447}{10^{15}}
=14425.249926691145447.
\]

The pool contains 183 selected canonical columns, nine strictly certified nonuniform positive 41-edge paths, and these two uniform paths. The column ordering and all parent hashes are frozen in the LP transcript.

## 2. Binary64 discovery (not the proof)

The 2,113-row HiGHS LP gives

\[
\eta_{\mathrm{LP}}=0.4317007129307349,
\]

with independently recomputed maximum residual

\[
0.4317007129309698.
\]

The block maxima are:

| Block | Maximum residual |
|---|---:|
| 1,461 low-order rows | 0.4317007129307364 |
| 645 selected/cut sixth-order rows | 0.4317007129309698 |
| 7 selected eighth-order rows | 0.43170071293073553 |

The binary64 primal support size is 65 and the reported primal-dual gap is \(8.72\times10^{-15}\). These are discovery diagnostics only.

## 3. Exact rational dual

The independently reconstructed rational dual has

\[
\|z\|_1=
\frac{1152921504606836423}{1152921504606846976}<1,
\]

\[
\beta=\lambda+z^\mathsf Ty
=\frac{497717035491941497}{1152921504606846976},
\qquad
\delta=\frac1{10^{10}}.
\]

The exact lower bound recorded by the verifier is

\[
\boxed{
\eta_{194}\ge
\frac{4860517923600091274798001}
{11258999068426240000000000}
=0.4317007128307263\ldots>\frac13.
}
\]

The certificate checks, with 128-bit Arb, every one of the 194 column inequalities

\[
z^\mathsf T a_j+\lambda-\delta<0.
\]

The maximum Arb upper endpoint over all 194 shifted column LHS values is

\[
-7.63322083947767\times10^{-11}<0.
\]

The dual has 65 nonzero coordinates: 2 low-order, 61 sixth-order, and 2 eighth-order rows.

The newly added column 1651 is close to active. Its unshifted dual LHS interval is

\[
[-3.46880890753216023\times10^{-14}
\pm1.96\times10^{-32}],
\]

whose upper endpoint is still strictly negative. This near-saturation is important for subsequent pricing; it must not be rounded to zero.

## 4. Proof

For every listed column \(j\), the Arb certificate proves

\[
z^\mathsf T a_j+\lambda\le\delta.
\]

For any probability vector \(p\in\Delta_{194}\),

\[
z^\mathsf T A p+\lambda\le\delta.
\]

Using \(\beta=\lambda+z^\mathsf Ty\),

\[
z^\mathsf T(Ap-y)\le\delta-\beta,
\qquad
-z^\mathsf T(Ap-y)\ge\beta-\delta.
\]

Hence, by Hölder,

\[
\|Ap-y\|_\infty
\ge
\frac{\beta-\delta}{\|z\|_1}
\ge \beta-\delta
=
\frac{4860517923600091274798001}
{11258999068426240000000000}
>\frac13,
\]

where the second inequality uses the exact certificate \(\|z\|_1<1\). This proves the stated finite-pool minimax obstruction.

## 5. What this does and does not establish

**Proved:**
- The exact rational lower bound above \(1/3\) for the pinned 194-column, 2,113-row problem.
- Strict Arb verification of all 194 physical-column inequalities.
- The new uniform path at column 1651 is included and its inequality is strictly satisfied.

**Not proved:**
- Separation of all 1,641 canonical generators.
- Separation of the full continuous positive-coupling path family.
- A continuous-family minimax lower bound or feasibility theorem.
- Complete sixth/eighth orbit control beyond the pinned selected/cut design.
- A Choi-infidelity or diamond-distance operational guarantee.

In particular, the 194-column dual must be priced over the uniform-path 21-torus and, if a positive point is found, over an explicit finite uniform time. The fact that the previous 193-column dual had a positive uniform-ray escape does not imply that this new 194-column dual does.

## 6. Reproducibility and provenance

- LP transcript: evidence/joint_low_six_eighth_lp_194col_uniform_ray_escape_n21.json
- Exact rational dual and Arb intervals: evidence/55probe_194col_uniform_ray_escape_dual_certificate_n21.json
- Reoptimizer: reoptimize_194col_uniform_ray_escape.py
- Independent verifier: verify_194col_uniform_ray_dual_arb.py
- Parent 193-column LP SHA256: 92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981
- Parent 193-column dual SHA256: 70c0ab689e7112c70a10eb75d051b43c686d3b6656d4aed37238f10ee5516799
- 194-column LP SHA256: c6dec42436d0181a9ff5012153d1896f4fcb0ca8a28cf39c6cdb321440dd7a66
- 193-column explicit finite-time certificate SHA256: 3358b8dc1e42eb8e1c4d5d04a722de107a188640fb032ca8c85a7f244e3a11dd
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45226334693
- Evidence commit: 1c10c6c7a796999448430d6ef9a8141e52b1112c
