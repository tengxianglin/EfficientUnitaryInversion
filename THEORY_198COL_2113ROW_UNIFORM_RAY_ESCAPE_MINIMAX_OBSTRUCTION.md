# 198-column, 2,113-row mixed-order finite-pool minimax obstruction at n=21

## Exact finite-pool theorem

Let \(A\in\mathbb R^{2113\times198}\) be the ordered physical-feature matrix and \(b\in\mathbb Q^{2113}\) the exact normalized target reconstructed by [`verify_198col_uniform_ray_dual_arb.py`](verify_198col_uniform_ray_dual_arb.py). The row design is fixed:

- 1,461 complete low-order coordinates (all 21 distance-averaged second moments and all 1,440 fourth-order dihedral-orbit averages);
- 645 selected/cut sixth-order orbit coordinates;
- 7 selected eighth-order orbit coordinates.

For \(\Delta_{198}=\{p\ge0:\sum_jp_j=1\}\), the exact rational dual and independent 128-bit Arb verification establish
\[
\boxed{
\min_{p\in\Delta_{198}}\|Ap-b\|_\infty
\ge
\frac{368059798280886313618383}
{900719925474099200000000}
=0.4086284624903306\ldots>\frac13.
}
\]
This is a theorem for the exact 198-column pool and the exact 2,113-row design pinned below. It is not a full continuous-family no-go, not a complete sixth/eighth-order orbit theorem, and not a Choi/diamond bound.

## Exact dual and proof

The certificate freezes \(z\in\mathbb Q^{2113}\), \(\lambda\in\mathbb Q\), and \(\delta\in\mathbb Q\):
\[
\|z\|_1=
\frac{2305843009202236569}{2305843009213693952}<1,
\]
\[
\beta:=\lambda+z^{\mathsf T}b
=\frac{942233106657499055}{2305843009213693952},
\qquad
\delta=10^{-8},
\]
\[
\beta-\delta=
\frac{368059798280886313618383}
{900719925474099200000000}.
\]
For all 198 exact physical columns \(a_j\), the independent Arb verifier encloses \(\lambda+z^{\mathsf T}a_j-\delta\) in a strictly negative interval. The maximum of the 198 certified upper endpoints is
\[
-1.978441155579956\times10^{-9}<0.
\]
All 198 intervals are stored in the exact certificate JSON.

For any \(p\in\Delta_{198}\), convexity yields
\[
\lambda+z^{\mathsf T}Ap
=\sum_jp_j(\lambda+z^{\mathsf T}a_j)<\delta,
\]
so \(z^{\mathsf T}(b-Ap)>\beta-\delta\). Hölder and \(\|z\|_1<1\) imply
\[
\|Ap-b\|_\infty
\ge\frac{z^{\mathsf T}(b-Ap)}{\|z\|_1}
>\beta-\delta.
\]
Taking the minimum over the compact simplex proves the stated conservative rational lower bound. \(\square\)

The dual has 66 nonzero coordinates: 5 low-order, 58 sixth-order, and 3 eighth-order rows. HiGHS binary64 duals are used only for discovery; the theorem uses the exact rationalized dual, exact target, and 128-bit Arb intervals.

## Exact physical pool and evidence

The 198-column pool is the exact 197-column parent plus the newly certified equal-positive-coupling open path at physical column 1655:
\[
c_1=\cdots=c_{41}=t_*,
\qquad
t_*=
\frac{14386899302852951223}{250000000000000}
=57547.597211411804892>0,
\]
with closing edge zero. The new time itself has a separate 128-bit Arb escape certificate against the 197-column dual; it is included here as a column before reoptimizing.

- 198-column LP transcript SHA256: `b2bf21c4656b0e46e544a3fe1f72ffea651ea7f138e2c518b17609c6633ddf00`
- exact cut-design LP SHA256: `d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f`
- ordered-column SHA256: `7e450afe0d98dbb35811c3dbb4d261f6396be55e98ecff61a2e59372f59a494c`
- frozen seed-pool SHA256: `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`
- canonical inventory SHA256: `f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98`
- sixth-row inventory SHA256: `5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb`
- eighth-row inventory SHA256: `c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0`

Reproduction:
- [198-column LP transcript](evidence/joint_low_six_eighth_lp_198col_uniform_ray_escape_n21.json)
- [198-column exact rational dual and all 198 Arb intervals](evidence/55probe_198col_uniform_ray_escape_dual_certificate_n21.json)
- [Independent 128-bit Arb verifier](verify_198col_uniform_ray_dual_arb.py)
- [198-column reoptimizer](reoptimize_198col_uniform_ray_escape.py)
- [Successful reoptimization workflow 45424946690](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45424946690)
- [Successful dual-certification workflow 45425975195](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45425975195)
- [Dual certificate commit fa265bd](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fa265bdd0215706f547fa5ed00b8e8cff9c0ae4b)

## Scope and next continuum pricing

**Proved:** the exact 198-column / 2,113-row finite-pool minimax residual is at least the displayed rational number, strictly above \(1/3\).

**Not proved:** separation of the full continuous physical family; feasibility/infeasibility for all positive-coupling paths; complete sixth/eighth-order orbit control; a full all-even-principal-minor result; or a Choi/diamond operational bound.

The continuous uniform-torus pricing test has now completed and found a strictly positive exact phase point. The resulting finite physical escape is established by the dense-ray theorem; an explicit finite rational time remains a useful strengthening. See the new section below.


## 198-dual continuous uniform-ray escape (completed 2026-11-24)

The 21-dimensional uniform-path torus pricing test has now found an exact-decimal phase point with a strictly positive 128-bit Arb interval for the **new 198-column dual**. The exact phase vector and interval are recorded in [the independent Arb certificate](evidence/198col_uniform_torus_arb_n21.json); the discovery transcript is [here](evidence/198col_uniform_torus_search_n21.json).

The certified shifted pricing interval is
\[
S_{198}(\theta_*)\in
[1.3026969054283107647764243746907199\pm8.46\times10^{-35}]>0.
\]
The 21 rational decimal phases are frozen in the certificate. The search used 16 deterministic starts, including the previously Arb-certified 197-column torus witness as a warm start; the analytic cofactor gradient passed complex-step/central checks with maximum relative defect \(6.98\times10^{-10}\). The optimizer is discovery only; the exact phase point is what Arb certifies.

By the pinned dense-torus theorem in [THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md), the equal-positive-coupling ray is dense in this 21-torus. Since \(S_{198}\) is continuous and strictly positive at \(\theta_*\), it is positive on a neighborhood, and the dense ray enters that neighborhood at some finite \(t>0\). Thus there exists a finite physical open path with all 41 internal couplings equal and positive for which this particular 198-column dual has positive shifted pricing.

This **refutes global separation by the particular 198-column dual**. It does not invalidate the exact 198-column/2,113-row finite-pool minimax theorem above, prove feasibility or infeasibility for the full physical family, complete all sixth/eighth-order orbit constraints, establish an all-even-principal-minor ensemble, or imply a Choi/diamond operational bound. The finite time has not yet been explicitly isolated; the current conclusion is existence via density plus a strict Arb torus point.

Reproduction:
- [198-column torus discovery](discover_198col_uniform_torus_pricing.py)
- [Independent 128-bit Arb verifier](verify_198col_uniform_torus_pricing_arb.py)
- [Workflow 45428424440](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45428424440), success
- [Search/certificate commit 7d8ebf3](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/7d8ebf3fb454b0342cb8138ccb6a7006263c51c4)
- Dual certificate SHA256:  d5bc214a70bdb610c034ef673252be8d7109d31b18a33d4bc5ac25e9c993e06f
- LP transcript SHA256:  b2bf21c4656b0e46e544a3fe1f72ffea651ea7f138e2c518b17609c6633ddf00
- Phase-vector SHA256:  dfc9860be79dcaad49971cbc28f0ad5fe9fa0eca77475fcda7f848a782138813

The next useful step is a bounded one-dimensional search for an explicit rational finite time \(t\), followed by an independent Arb certificate of the equal-coupling physical path. Such a search can produce a concrete witness, but a failure to find one would not undo the existence result already implied by density.
