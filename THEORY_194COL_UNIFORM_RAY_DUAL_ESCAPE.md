# 194-column dual escape on the uniform positive-coupling ray

**Status:** the exact rationalized 194-column dual has a strictly positive uniform-torus pricing point and an explicit finite positive uniform-coupling escape. A 128-bit Arb verifier certifies the exact rational time \(t_*=5918073474550670653/10^{15}=5918.073474550670653\), with all 41 couplings equal and pricing interval `[0.533171018619275430607761736493 +/- 5.01e-31] > 0` (workflow [45230548697](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45230548697), evidence `evidence/194col_uniform_ray_time_arb_n21.json`).

This result does **not** invalidate the finite 194-column minimax theorem. It shows that its particular dual is not a separator of the full continuous positive-coupling path family.

## 1. Fixed finite-pool theorem remains valid

The 194-column / 2,113-row mixed-order design has the exact rational dual and 128-bit Arb certificate in THEORY_194COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md. It proves

\[
\min_{p\in\Delta_{194}}\|A p-y\|_\infty
\ge
\frac{4860517923600091274798001}
{11258999068426240000000000}
=0.4317007128307263\ldots>\frac13.
\]

All 194 listed physical-column inequalities are strictly Arb-certified. This finite-pool theorem is unchanged by the continuous escape below.

## 2. Uniform-path torus and pricing functional

Let \(K_*\in\mathbb R^{42\times42}\) be the skew-symmetric uniform path generator with nearest-neighbor entries \(2\) and \(-2\). The explicit orthogonal basis in THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md gives

\[
Q^\mathsf T K_*Q
=\bigoplus_{k=1}^{21}\omega_kJ,
\qquad
\omega_k=4\cos\left(\frac{k\pi}{43}\right),
\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

The 21 frequencies are linearly independent over \(\mathbb Q\). Hence the positive uniform ray \(e^{tK_*}\), \(t\ge0\), is dense in the exact 21-torus

\[
\mathbb T_*=
\left\{
Q\left(\bigoplus_{k=1}^{21}
\begin{pmatrix}
\cos\theta_k&\sin\theta_k\\
-\sin\theta_k&\cos\theta_k
\end{pmatrix}\right)Q^\mathsf T:
\theta\in\mathbb T^{21}
\right\}.
\]

For the exact rationalized 194-column dual, define

\[
S_{194}(R)=\lambda-\delta+z^\mathsf T a(R),
\]

where \(a(R)\in\mathbb R^{2113}\) is the pinned normalized mixed-order feature vector.

## 3. Exact positive torus point

A deterministic 12-start L-BFGS-B search over \([-\pi,\pi]^{21}\), with at most 120 iterations per start, found the exact-decimal phase vector

\[
\begin{aligned}
\theta_* = (&-2.737240787735,\;-2.657969920577,\;-2.635609624404,\\
&-2.617732159414,\;-2.581906537802,\;-2.123917706611,\\
&-0.653154449663,\;-0.497390685488,\;-0.202350815348,\\
&0.072209913140,\;0.303521738140,\;0.255543241323,\\
&0.312040171726,\;0.559504604358,\;1.165269995626,\\
&1.345773668794,\;1.226301342681,\;1.275687234308,\\
&3.013601419280,\;3.141592653590,\;3.141592653590).
\end{aligned}
\]

The exact phase-vector SHA256 is

f45e6dc6d84e196e9989351d5901dd2a694b7dda8cedb0ca98da69acfaddbdce.

The maximum relative defect in the recorded analytic-gradient regression is \(5.0922\times10^{-10}\). This is an implementation check, not the proof.

The independent 128-bit Arb verifier reconstructs the exact-decimal rational phases, the exact torus basis and rotation blocks, the rational dual, and all 65 active dual-row contributions. It certifies

\[
\boxed{
S_{194}(R(\theta_*))
\in
[4.165518912347934438721938898592883
\pm7.17\times10^{-34}]>0.
}
\]

The lower endpoint is strictly positive. The verifier pins:

- 194-column dual SHA256:
  7864da033a71d7d2666cde32cf7f900c9a9a30893cbc7b90942fa09517cab474;
- 194-column LP SHA256:
  c6dec42436d0181a9ff5012153d1896f4fcb0ca8a28cf39c6cdb321440dd7a66;
- parent 193-column LP SHA256:
  92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981;
- parent 193-column dual SHA256:
  70c0ab689e7112c70a10eb75d051b43c686d3b6656d4aed37238f10ee5516799;
- previous 192-column time certificate SHA256:
  a246d7423bc60f78aa6a528188a7065c4c5a0a45a51edb5e4931ee1111b3437c;
- 193-column finite-time certificate SHA256:
  3358b8dc1e42eb8e1c4d5d04a722de107a188640fb032ca8c85a7f244e3a11dd.

## 4. Theorem: the 194-column dual does not separate the continuous uniform ray

**Theorem.** There exists a finite \(t>0\) such that

\[
S_{194}(e^{tK_*})>0.
\]

**Proof.** The Arb interval above proves \(S_{194}(R(\theta_*))>0\). The pricing functional is a finite linear combination of matrix minors and is therefore continuous on \(\mathbb T_*\). Thus it is strictly positive on a nonempty open neighborhood of \(R(\theta_*)\). The positive-time uniform orbit is dense in \(\mathbb T_*\), so it intersects this neighborhood at a finite \(t>0\). \(\square\)

For the corresponding physical path, all 41 couplings are exactly the same positive number \(t\). Since the 194-column certificate proves strictly negative pricing on every listed column, this path lies outside that finite pool.

This refutes **only** global separation by this particular 194-column dual. It does not invalidate the finite 194-column minimax theorem.

## 5. Scope

**Proved:**
- The finite 194-column / 2,113-row minimax lower bound above \\(1/3\\).
- A strictly positive value of the exact 194-column dual pricing functional at an exact-decimal point of the uniform-path torus, independently certified by 128-bit Arb.
- Existence of a finite positive uniform coupling escaping this particular dual, by continuity and density of the uniform ray.
- An explicit finite witness with all 41 couplings equal to \\(t_*=5918073474550670653/10^{15}\\), independently certified by 128-bit Arb with pricing interval `[0.533171018619275430607761736493 +/- 5.01e-31]`.

**Not yet proved or supplied:**
- Feasibility or infeasibility of a probability mixture over the full continuous physical family.
- A continuous-family minimax lower or upper bound.
- Complete sixth/eighth orbit control beyond the pinned design.
- A Choi-infidelity or diamond-distance operational guarantee.


## 6. Reproducibility

- Finite-pool theorem: THEORY_194COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md
- Search: discover_194col_uniform_torus_pricing.py
- Independent Arb verifier: verify_194col_uniform_torus_pricing_arb.py
- Search transcript: evidence/194col_uniform_torus_search_n21.json
- 128-bit Arb certificate: evidence/194col_uniform_torus_arb_n21.json
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45227944554
- Evidence commit: 2972334d665c4882060cd887277cc4a0ec1e364c

The next computational step is to append this exact Arb-certified path as physical column 1652 and reoptimize the 2,113-row LP. Any new above-cap result still requires a fresh rational dual and independent Arb checks of all 195 columns; a below-cap candidate still requires exact-probability and complete-orbit audits.


## 7. Explicit finite-time uniform-path escape (2026-11-24)

The bounded one-dimensional search selected the exact decimal

\[
t_*=5918.073474550670653
=\frac{5918073474550670653}{10^{15}}>0.
\]

All 41 physical edge couplings are exactly this same positive rational number. The independent verifier reconstructs \(e^{t_*K_*}\) from the exact real orthogonal spectral basis and the algebraic frequencies \(\omega_k=4\cos(k\pi/43)\), then evaluates the same 65 nonzero rows of the 194-column dual using python-flint 0.8.0 / Arb at 128-bit precision. It certifies

\[
\boxed{
S_{194}(e^{t_*K_*})
\in[0.533171018619275430607761736493
\pm5.01\times10^{-31}]>0.
}
\]

The recorded lower and upper endpoint enclosures are respectively
\[
[0.53317101861927543060776173649331919247\pm2.02\times10^{-39}]
\quad\text{and}\quad
[0.53317101861927543060776173649350020527\pm3.95\times10^{-39}].
\]

The verifier pins the exact 194-column dual SHA256
`7864da033a71d7d2666cde32cf7f900c9a9a30893cbc7b90942fa09517cab474`,
the LP transcript SHA256
`c6dec42436d0181a9ff5012153d1896f4fcb0ca8a28cf39c6cdb321440dd7a66`,
the torus certificate SHA256
`aa5c6abb839f7cdb91175db6fef519dc66246e970dfd2de122440a9cc3a3a292`,
and the exact search transcript SHA256
`3ae391fb4773fff1f02f85be2ab0c23d5b7bf3aadecf186e3cec4e9c7cb59058`.
The dual has exact \(\|z\|_1=1152921504606836423/1152921504606846976<1\), and all 194 listed columns have strictly negative shifted pricing intervals. Thus the new uniform path is a genuine physical column outside the pinned 194-column pool.

The first attempt at this verification failed because of six undefined `time_cert` references; they were corrected to the already-loaded torus certificate in commit [60dd9a5](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/60dd9a523de4a774c93e1272cc1309c2614f506e). The corrected complete workflow [45230548697](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45230548697) passed every step, including all parent dual/time recertifications, deterministic bounded search, the independent Arb finite-time check, and artifact commit. Evidence commit: [30b7145](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/30b7145063d63f664a2dc7b24ac599b826f2429c).

**Scope:** this proves that the particular 194-column dual is not a separator of the full continuous physical family, with an explicit equal-coupling path witness. It does not invalidate the 194-column finite-pool minimax theorem, prove full-family feasibility/infeasibility, or supply an operational Choi/diamond-norm guarantee.
