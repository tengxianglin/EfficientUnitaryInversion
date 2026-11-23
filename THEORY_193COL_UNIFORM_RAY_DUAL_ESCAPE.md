# 193-column dual escape on the uniform positive-coupling ray

**Status:** a strictly positive uniform-ray pricing value is proved for the particular exact rationalized 193-column dual. The proof combines a 128-bit Arb-certified point on the exact 21-torus with the dense-orbit theorem for the uniform positive-coupling path.

This result does **not** invalidate the finite 193-column minimax theorem. It proves that its particular dual vector cannot be extended to a separator of the full continuous positive-coupling path family.

## 1. Fixed finite-pool theorem remains valid

The 193-column / 2,113-row mixed-order design consists of 183 selected canonical generators and ten certified continuous-path generators. Its exact rational dual satisfies

\[
\|z\|_1=
\frac{18446744073709358785}{18446744073709551616}<1,
\]

\[
\beta=\lambda+z^\mathsf Ty
=\frac{8021329755945624383}{18446744073709551616},
\qquad
\delta=10^{-10}.
\]

The finite-pool theorem is

\[
\min_{p\in\Delta_{193}}\|A p-y\|_\infty
\ge
\frac{78333298379892089605752391}
{180143985094819840000000000}
=0.43483715728094335\ldots>\frac13.
\]

The independent 128-bit Arb certificate checks all 193 physical-column inequalities. The maximum shifted upper endpoint is \(-5.7674808073103104\times10^{-11}<0\).

This finite-pool result is unchanged by the continuous escape below.

## 2. Uniform-path torus

Let \(K_*\in\mathbb R^{42\times42}\) be the real skew-symmetric path generator

\[
(K_*)_{j,j+1}=2,\qquad (K_*)_{j+1,j}=-2,
\quad j=0,\ldots,40.
\]

The explicit real orthogonal basis \(Q\) in THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md gives

\[
Q^\mathsf T K_*Q
=\bigoplus_{k=1}^{21}\omega_k J,
\qquad
\omega_k=4\cos\left(\frac{k\pi}{43}\right),
\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

The 21 frequencies are linearly independent over \(\mathbb Q\), as proved in that note. Kronecker's theorem therefore implies that

\[
\{e^{tK_*}:t\ge0\}
\]

is dense in the conjugate maximal torus

\[
\mathbb T_*=
\left\{
Q\left(\bigoplus_{k=1}^{21}R(\theta_k)\right)Q^\mathsf T:
\theta\in\mathbb T^{21}
\right\},
\quad
R(\theta_k)=
\begin{pmatrix}
\cos\theta_k&\sin\theta_k\\
-\sin\theta_k&\cos\theta_k
\end{pmatrix}.
\]

The positive-time tail is dense as well: for every \(T>0\), the set \(\{e^{tK_*}:t\ge T\}\) is the translate of the dense positive semiorbit by \(e^{TK_*}\).

## 3. Exact positive torus point

For the exact rationalized 193-column dual, define the continuous pricing functional

\[
S_{193}(R)=\lambda-\delta+z^\mathsf T a(R),
\]

where \(a(R)\in\mathbb R^{2113}\) is the pinned normalized mixed-order feature vector.

A deterministic 12-start L-BFGS-B discovery search over \([-\pi,\pi]^{21}\) found the following exact-decimal phase vector:

\[
\begin{aligned}
\theta_* = (&2.434635604798,\;2.294400386942,\;2.223190652262,\\
&2.236880291558,\;2.409188896868,\;2.510697569184,\\
&0.663275313899,\;0.326734494421,\;0.090102821606,\\
&-0.096821357444,\;-0.253469020117,\;-0.235527730557,\\
&-0.335930322130,\;-0.637859280271,\;-1.291952294347,\\
&-1.541911431772,\;-1.038662518707,\;-0.803190879403,\\
&-3.141592653590,\;-3.141592653590,\;-3.141592653590).
\end{aligned}
\]

The exact phase-vector SHA256 is

115a8091de0d2d8b18136c8e74823adb2e5771d70e9270120c39248158962c25.

The optimizer is discovery only. The independent verifier reconstructs the exact rational phase inputs, the explicit \(Q\) basis, all 21 rotation blocks, the exact rational dual, and the active low-/sixth-/eighth-order row contributions using 128-bit Arb. It certifies

\[
\boxed{
S_{193}(R(\theta_*))
\in
[3.042070453078681243432558976616809
\pm4.22\times10^{-34}]>0.
}
\]

The lower endpoint is strictly positive. The verifier pins:

- 193-column dual certificate SHA256:
  70c0ab689e7112c70a10eb75d051b43c686d3b6656d4aed37238f10ee5516799;
- 193-column LP transcript SHA256:
  92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981;
- 2,113-row cut-design SHA256:
  d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f.

The discovery gradient's maximum relative defect across the recorded complex-step/central-difference checks is \(4.1551\times10^{-10}\). This is an implementation regression, not the mathematical proof; strict positivity follows from the independent Arb interval.

## 4. Theorem: the 193-column dual does not separate the continuous uniform ray

**Theorem.** There exists a finite \(t>0\) such that

\[
S_{193}(e^{tK_*})>0.
\]

**Proof.** The Arb certificate gives \(S_{193}(R(\theta_*))>0\). Since \(S_{193}\) is a finite linear combination of minors, it is continuous in the matrix entries. Hence there is a nonempty open neighborhood \(U\subset\mathbb T_*\) of \(R(\theta_*)\) on which \(S_{193}>0\). The positive-time uniform orbit is dense in \(\mathbb T_*\), so it intersects \(U\) at some finite \(t>0\). Thus \(S_{193}(e^{tK_*})>0\). \(\square\)

For this uniform path, all 41 edge couplings are exactly the same strictly positive number \(t\). Because the 193-column certificate proves strictly negative pricing on every listed column, the new path lies outside that finite pool.

This refutes **only** global separation by this particular 193-column dual. It does not invalidate the finite 193-column minimax theorem.

## 5. Scope

**Proved:**
- The finite 193-column / 2,113-row minimax lower bound above \(1/3\).
- A strictly positive value of the exact 193-column dual pricing functional at an exact-decimal point of the uniform-path torus, independently certified by 128-bit Arb.
- Existence of a finite strictly positive uniform coupling \(t\) that escapes this particular dual, by continuity and the dense-orbit theorem.

**Not proved:**
- An explicit decimal value of the finite \(t\) (a bounded one-dimensional search and separate Arb verifier are now running).
- Feasibility or infeasibility of a probability mixture over the full continuous physical family.
- A continuous-family minimax upper or lower bound.
- Complete sixth/eighth orbit control.
- A Choi-infidelity or diamond-distance operational guarantee.

A failed bounded finite-time search would not refute the dense-torus existence theorem and would not establish global separation.

## 6. Reproducibility

- Dense-torus derivation: THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md
- 193-column finite-pool theorem: THEORY_193COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md
- Torus search: discover_193col_uniform_torus_pricing.py
- Independent Arb verifier: verify_193col_uniform_torus_pricing_arb.py
- Search transcript: evidence/193col_uniform_torus_search_n21.json
- Arb certificate: evidence/193col_uniform_torus_arb_n21.json
- Successful search/verification workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45223892005
- Evidence commit: 6b8cabddaad3648323343fd8fbc1b671afc2d18f

An explicit finite physical witness has now been certified:
\[
t_* = 588.216987832015661
=\frac{588216987832015661}{10^{15}}>0,
\]
with all 41 edge couplings equal to this value, and
\[
S_{193}(e^{t_*K_*})
\in[0.44956324068539347204794614417071
\pm8.33\times10^{-33}]>0.
\]
The exact decimal is reconstructed as a rational input by the independent 128-bit Arb verifier. Workflow 45224963117 completed successfully. The next finite-pool experiment is to append this path as physical column 1651 and reoptimize the same 2,113-row design.


## 7. Explicit finite uniform-coupling witness

The dense-torus theorem and positive torus interval already imply existence of a finite positive uniform coupling. A deterministic differential-evolution search over four bounded intervals,
\[
[10^{-3},10^3],\quad[10^3,10^4],\quad[10^4,10^5],\quad[10^5,10^6],
\]
found
\[
t_*=588.216987832015661
=\frac{588216987832015661}{10^{15}}>0.
\]
The 41 physical edge couplings are all exactly this rational decimal.

The search's best binary64 score is 0.44956324068536085; this is a discovery diagnostic only. The independent 128-bit Arb verifier reconstructs the exact uniform-ray matrix and all 63 active dual-row contributions and certifies
\[
\boxed{
S_{193}(e^{t_*K_*})
\in[0.44956324068539347204794614417071
\pm8.33\times10^{-33}]>0.
}
\]
The exact time is \(588216987832015661/10^{15}\). The Arb output pins the 193-column dual SHA256, LP transcript SHA256, torus Arb certificate SHA256, and phase-vector SHA256 recorded above.

This is a directly replayable finite physical path, not only a density corollary. It lies outside the 193-column pool because all 193 listed columns have strictly negative certified pricing. It refutes this particular 193-column dual as a separator of the continuous family, but does not invalidate the finite 193-column theorem or settle the continuous-family minimax problem.

Reproduction:
- Search: evidence/193col_uniform_ray_time_search_n21.json
- Arb: evidence/193col_uniform_ray_time_arb_n21.json
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45224963117
- Evidence commit: 5d9bc186a82d4b331930069764344e14367ea55c
- Search script: discover_193col_uniform_ray_time_escape.py
- Verifier: verify_193col_uniform_ray_time_arb.py
