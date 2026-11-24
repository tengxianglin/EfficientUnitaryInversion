# 197-column, 2,113-row mixed-order finite-pool minimax obstruction at n=21

## Theorem (exact finite-pool statement)

Let \(A\in\mathbb R^{2113\times197}\) be the ordered physical-feature matrix and let \(b\in\mathbb Q^{2113}\) be the exact target vector reconstructed by `verify_197col_uniform_ray_dual_arb.py`. The row design consists of:

- 1,461 complete low-order coordinates: all 21 distance-averaged second moments and all 1,440 fourth-order dihedral-orbit averages;
- 645 selected/cut sixth-order orbit coordinates;
- 7 selected eighth-order orbit coordinates.

Let \(\Delta_{197}=\{p\in\mathbb R^{197}:p_j\ge0,\sum_jp_j=1\}\). The exact rational dual certificate and 128-bit Arb interval verification establish
\[
\boxed{
\min_{p\in\Delta_{197}}\|Ap-b\|_\infty
\ge
\frac{9347391123134860821080377}
{22517998136852480000000000}
=0.415107553803245\ldots>\frac13.
}
\]

This is a theorem for the **exact 197-column pool and exact 2,113-row design pinned below**. It is not a theorem for the full continuous physical family, the complete sixth/eighth-order orbit inventories, or the full all-even-principal-minor system.

## Exact dual and proof

The certificate freezes a rational vector \(z\in\mathbb Q^{2113}\), rational scalar \(\lambda\), and rational slack \(\delta\):
\[
\|z\|_1=
\frac{2305843009213687359}{2305843009213693952}<1,
\]
\[
\lambda=\frac{1508567587773281}{1125899906842624},
\qquad
\beta:=\lambda+z^{\mathsf T}b
=\frac{957172851239594049}{2305843009213693952},
\]
\[
\delta=10^{-10},\qquad
\beta-\delta=
\frac{9347391123134860821080377}
{22517998136852480000000000}.
\]

For every one of the 197 physical columns \(a_j\), the independent 128-bit Arb verifier encloses
\[
\lambda+z^{\mathsf T}a_j-\delta
\]
in a certified interval whose upper endpoint is negative. The largest of the 197 upper endpoints is
\[
-6.236499982702207\times10^{-11}<0.
\]
All 197 intervals are stored in the certificate JSON.

For any \(p\in\Delta_{197}\), convexity gives
\[
\lambda+z^{\mathsf T}Ap
=\sum_{j=1}^{197}p_j(\lambda+z^{\mathsf T}a_j)
<\delta.
\]
Consequently,
\[
z^{\mathsf T}(b-Ap)>\beta-\delta.
\]
Hölder's inequality and \(\|z\|_1<1\) imply
\[
\|b-Ap\|_\infty
\ge\frac{z^{\mathsf T}(b-Ap)}{\|z\|_1}
>\beta-\delta.
\]
Taking the minimum over the compact simplex proves the stated conservative rational lower bound. \(\square\)

The exact dual support has 63 nonzero coordinates: 2 low-order, 59 sixth-order, and 2 eighth-order rows. The HiGHS binary64 solve was used only to discover the dual; the theorem uses the exact rationalized vector, exact rational target, and independent Arb interval inequalities.

## Physical pool and reproducibility pins

The 197th physical column appends the fifth explicitly certified equal-positive-coupling open path:
\[
c_1=\cdots=c_{41}=t_*,
\qquad
t_*=
\frac{1535392895240590633}{500000000000000}
=3070.785790481181266>0.
\]
Its rotation is independently represented through the exact 21-frequency spectral form. The exact ordered column list is pinned by
`column_order_sha256` in the certificate.

- LP transcript SHA256: `721b9b3e373a53dbeed8b2500f246acb7270037e2db8b82db9bbb1d678964e47`
- 197-column certificate JSON SHA256: `9a0b5bff2a99e8482e6bc2421529482e0232026b`
- frozen seed-pool SHA256 (little-endian f64): `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`
- canonical all-column array SHA256: `f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98`
- ordered-column SHA256: `117c9f37f43827f27534b117af9a6413eb7af4c42b078137621fc2940df2dc20`
- sixth-row inventory SHA256: `5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb`
- eighth-row inventory SHA256: `c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0`

Reproduction:

- [197-column HiGHS discovery transcript](evidence/joint_low_six_eighth_lp_197col_uniform_ray_escape_n21.json)
- [197-column exact rational dual + all 197 Arb intervals](evidence/55probe_197col_uniform_ray_escape_dual_certificate_n21.json)
- [Independent 128-bit Arb verifier](verify_197col_uniform_ray_dual_arb.py)
- [Reoptimizer](reoptimize_197col_uniform_ray_escape.py)
- [Successful reoptimization workflow 45420486905](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45420486905)
- [Certificate commit 3ba48b8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/3ba48b8ee85f69906613c817e20e69e1c05bea10)

## Scope and next continuum test

**Proved:** the finite 197-column / 2,113-row minimax residual exceeds \(1/3\), for exactly the pinned pool and row design.

**Not proved:** a global separator for all positive-coupling paths; infeasibility of mixtures over the full continuous physical family; complete sixth/eighth-order moment matching or obstruction; an all-even-principal-minor obstruction; or any Choi-state trace-distance / channel diamond-distance bound.

The 21-dimensional uniform-path torus parameterization and rational independence of its 21 frequencies are treated in [`THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md`](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md). A positive exact torus-pricing point for this new 197-column dual would, by continuity and density, prove that this particular dual also fails to separate the continuous equal-positive-coupling ray. A finite multi-start search with no positive point would **not** prove global separation.

The new search and independent verifier are:

- [`discover_197col_uniform_torus_pricing.py`](discover_197col_uniform_torus_pricing.py)
- [`verify_197col_uniform_torus_pricing_arb.py`](verify_197col_uniform_torus_pricing_arb.py)
- [workflow run 45422332355](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422332355)

The search is a discovery stage only. A continuum escape is recorded only if the exact decimal phase vector receives a strictly positive 128-bit Arb interval.


## Certified escape of the 197-column dual on the continuous uniform-coupling ray

The newly frozen rational 197-column dual is itself **not** a separator of the full continuous physical family. A deterministic 12-start L-BFGS-B search over the 21-dimensional uniform-path torus found an exact-decimal phase vector. The search gradient passed independent complex-step and central-difference checks, with maximum relative defect
\[
2.4667717161121613\times10^{-9}.
\]
The optimizer is discovery only. The proof is the separate 128-bit Arb evaluation of the exact rational phase strings:
\[
\theta_* = (
-0.396819635825,
-0.010513288335,
3.097354079828,
-1.055750489362,
3.037776511219,
0.150879565875,
-0.049742897977,
3.038323614830,
3.085793963585,
-3.126156664827,
3.025512989235,
-0.021788906516,
0.156030082012,
2.982820215056,
3.123052097334,
-3.141592653590,
0.174125508937,
0.160694546368,
0.023571325984,
0.044955335158,
-3.141592653590
).
\]
For the exact torus rotation
\[
R(\theta_*)=Q\left(\bigoplus_{k=1}^{21}
\begin{pmatrix}
\cos\theta_{*,k}&\sin\theta_{*,k}\\
-\sin\theta_{*,k}&\cos\theta_{*,k}
\end{pmatrix}\right)Q^{\mathsf T},
\]
the independent verifier certifies
\[
\boxed{
S_{197}(R(\theta_*))
\in
[1.7152449127664802147236733367025386
\pm5.20\times10^{-35}]>0.
}
\]
Here \(S_{197}(R)=\lambda-\delta+z^{\mathsf T}a(R)\) is the exact rational-dual pricing functional, with the same 2,113 normalized moment rows and \(\delta=10^{-10}\) as in the finite-pool theorem.

By the rational independence of \(\omega_k=4\cos(k\pi/43)\) proved in [`THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md`](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md), the positive-time equal-coupling orbit is dense in this torus. Since \(S_{197}\) is continuous and strictly positive at \(R(\theta_*)\), it is positive on an open neighborhood; density therefore proves that **there exists some finite \(t>0\)** for which the admissible physical open path
\[
c_1=\cdots=c_{41}=t>0
\]
has \(S_{197}(e^{tK_*})>0\).

This is a rigorous continuum escape of the particular 197-column dual, while leaving the exact 197-column finite-pool theorem intact. The torus certificate does not yet identify an explicit finite decimal time. A separate bounded one-dimensional search and Arb verifier are now running:

- [Exact 128-bit Arb torus certificate](evidence/197col_uniform_torus_arb_n21.json)
- [12-start search transcript](evidence/197col_uniform_torus_search_n21.json)
- [Independent Arb verifier](verify_197col_uniform_torus_pricing_arb.py)
- [Reproducible workflow 45422332355](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422332355)
- [Evidence commit 13fc703](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/13fc7038e?plain=1)

The finite-time search is [workflow 45422810828](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422810828). If it finds a candidate, only an independent Arb interval strictly above zero will promote it to an explicit physical-time certificate. Failure to find such a time in the bounded search does not weaken the dense-torus existence proof.

**Scope:** this escape refutes global separation by the *particular 197-column rational dual*. It does not invalidate the finite 197-column minimax theorem, prove full-family feasibility/infeasibility, complete sixth/eighth-order orbit control, establish an all-even-minor result, or imply a Choi/diamond operational bound.
