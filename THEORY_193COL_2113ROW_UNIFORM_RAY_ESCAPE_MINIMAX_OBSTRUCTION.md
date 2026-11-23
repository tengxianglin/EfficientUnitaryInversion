# 193-column / 2,113-row uniform-ray minimax obstruction

**Status:** strict finite-pool minimax obstruction proved by an exact rational dual and independent 128-bit Arb verification of all 193 physical columns.

The new column is the explicit uniform positive-coupling path with all 41 couplings equal to

\[
t_* = 14425.249926691145447
=\frac{14425249926691145447}{10^{15}}>0.
\]

This path was itself found by a strict Arb-positive pricing witness against the 192-column dual. The 193-column result below is a new finite-pool theorem; it is not a continuous-family theorem.

## 1. Fixed pool and row design

The 193 columns consist of 183 selected canonical generators and ten certified continuous-path generators (the previous nine nonuniform escapes plus the new uniform-ray path, labelled physical column 1650).

The mixed-order design has 2,113 rows:

- 1,461 complete second/fourth-order rows;
- 645 selected sixth-order rows, including the frozen sixth-order cuts;
- 7 selected eighth-order rows.

The exact LP transcript pins:
- the 192-column parent LP;
- the 192-column parent dual certificate;
- the 152-column cut LP and cut dual;
- all nine prior continuous-path Arb certificates;
- the explicit uniform-ray time Arb certificate;
- the frozen seed pool and full canonical inventory hashes;
- the exact parent column order and new column label 1650.

The large-time uniform path is evaluated using the explicit 21-torus spectral representation for **all** moment orders. The binary64 orthogonality defect of that rotation is \(5.21\times10^{-15}\). The low-order features are computed from the same spectral rotation used for sixth/eighth features; no generic matrix exponential is mixed into part of the new column.

## 2. HiGHS discovery (not the proof)

The binary64 193-column LP reports

\[
\eta_{\mathrm{LP}}=0.4348371573809519,
\]

with independently recomputed maximum residual

\[
0.4348371573809968.
\]

Block maxima are 0.43483715738095197 (low), 0.4348371573809968 (sixth), and 0.4348371573809675 (eighth). The primal support size is 63 and the floating primal/dual objective gap is \(8.60\times10^{-15}\).

These are optimization diagnostics only. The theorem uses the rationalized dual and the Arb column inequalities below.

## 3. Exact rational dual

The independent verifier reconstructs an exact rational dual vector \(z\in\mathbb Q^{2113}\) and scalar \(\lambda\) from the HiGHS marginals. The exact quantities are

\[
\|z\|_1=
\frac{18446744073709358785}{18446744073709551616}<1,
\]

\[
\lambda=
\frac{3087754810774421}{2251799813685248},
\]

\[
\beta=\lambda+z^\mathsf T y
=
\frac{8021329755945624383}{18446744073709551616}.
\]

Choose the exact rational slack

\[
\delta=10^{-10}.
\]

The certified lower bound is

\[
\boxed{
\eta_{193}\ge\beta-\delta
=
\frac{78333298379892089605752391}
{180143985094819840000000000}
=
0.43483715728094335\ldots
>
\frac13.
}
\]

The active dual support has 63 entries: two low-order, 59 sixth-order, and two eighth-order rows.

## 4. Strict Arb verification of all 193 columns

The independent verifier uses 128-bit Arb interval arithmetic. It reconstructs the exact row design, exact rational dual, and all physical columns. For the new uniform path it evaluates the exact algebraic-frequency torus representation at the rational time \(t_*\); the other 192 columns are independently reconstructed from their pinned exact coupling inputs.

For every \(j=1,\ldots,193\), it certifies

\[
z^\mathsf T a_j+\lambda-\delta<0.
\]

All 193 intervals are present in the certificate. The maximum upper endpoint after subtracting the exact slack is

\[
-5.7674808073103104\times10^{-11}<0.
\]

Thus for every probability vector \(p\in\Delta_{193}\),

\[
z^\mathsf T A p+\lambda\le\delta,
\]

and hence

\[
\|Ap-y\|_\infty
\ge
\frac{\beta-\delta}{\|z\|_1}
\ge \beta-\delta
>
\frac13.
\]

This is a strict finite-pool minimax theorem for exactly the 193 listed physical columns and the fixed 2,113-row mixed-order design.

## 5. Scope and unresolved claims

**Proved:**
- The 193-column / 2,113-row minimax lower bound above \(1/3\).
- All 193 column inequalities, exact dual normalization, and the rational lower bound are independently Arb-certified.
- The new uniform path is included and its large-time matrix is evaluated consistently from the spectral torus representation.

**Not proved:**
- A lower bound for the full 1,641-column canonical inventory by this particular 193-column dual.
- A minimax theorem over the entire continuous positive-coupling path family.
- Complete sixth/eighth orbit control.
- Feasibility or infeasibility of a mixture over all continuous paths.
- A Choi-infidelity or diamond-distance operational guarantee.

In particular, the fact that the 193-column dual separates its 193 listed columns does not imply it separates the continuous family. The uniform-path 21-torus test and an explicit finite uniform-coupling witness have both been strictly Arb-certified; see THEORY_193COL_UNIFORM_RAY_DUAL_ESCAPE.md. The next finite-pool experiment is to append the exact path t=588.216987832015661 as physical column 1651 and reoptimize the same 2,113-row design. A failed bounded search over the full 41-dimensional family would not prove global separation.

## 6. Reproducibility

- LP transcript: evidence/joint_low_six_eighth_lp_193col_uniform_ray_escape_n21.json
- 128-bit Arb certificate: evidence/55probe_193col_uniform_ray_escape_dual_certificate_n21.json
- Reoptimizer: reoptimize_193col_uniform_ray_escape.py
- Independent verifier: verify_193col_uniform_ray_dual_arb.py
- Reoptimization workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45222472885
- Arb workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45223141522
- LP transcript SHA256: 92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981
- Parent 192-column LP SHA256: ed966f1c3f755b1910f7f34be978af88ee290821ea643cb7690d83c7aeab686a
- Parent 192-column dual SHA256: 2b3891b88f40627458764821142f6a83e039fd051795d4146895de68f5c5a308
- Uniform-ray time certificate SHA256: a246d7423bc60f78aa6a528188a7065c4c5a0a45a51edb5e4931ee1111b3437c
- Certificate commit: 0bf2b18708f278968163700a718a90fdb413ec0e


## 7. Continuous uniform-ray escape of this 193-column dual

The exact 21-torus pricing search and independent Arb verifier now certify a positive point. The dense-orbit theorem therefore implies existence of a finite t>0 with positive pricing along the uniform path. The complete statement, exact phase vector, interval, provenance hashes, proof, and scope limitations are in THEORY_193COL_UNIFORM_RAY_DUAL_ESCAPE.md. This does not change the finite 193-column minimax theorem.


## 8. Explicit finite uniform-ray witness

The 193-column dual has a directly certified physical escape at t=588.216987832015661, with all 41 couplings equal. The independent 128-bit Arb interval is recorded in THEORY_193COL_UNIFORM_RAY_DUAL_ESCAPE.md and evidence/193col_uniform_ray_time_arb_n21.json. This leaves the finite 193-column minimax theorem intact.
