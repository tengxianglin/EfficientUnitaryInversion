# Aggregate quartic-orbit Gram certificate for the frozen N=42 candidate

Date: 2026-11-28. Run 67. Base: main after the Run 66 Plucker/frame-potential audit.

## Scope

This note combines all 1,440 D_42 fourth-order residuals of the frozen 37-base / 74-labelled period-two candidate into one explicit quadratic-form witness. It is a candidate-specific discrepancy certificate. It is not a no-go theorem for all period-two measures or for the full continuous cycle-exponential family.

The complement-folded program-label distribution is denoted q, and u is uniform on the 21-subsets of [42], with complementary subsets identified in the physical label distribution. We use the balanced-slice sign representation
\[
x_i(S)=2\mathbf 1_{i\in S}-1,\qquad f_I(S)=\prod_{i\in I}x_i(S).
\]
For every even I, the complement-folded projection-DPP identity gives
\[
\mathbb E_q f_I=\bar m_I,
\qquad
\mathbb E_u f_I=\tau_I.
\]
For |I|=4, \(\tau_I=1/533\).

## 1. Exact balanced-slice kernel

For a uniformly random balanced sign vector x in {+1,-1}^42 with sum_i x_i=0, let
\[
\mu_{2r}=\mathbb E\prod_{i\in A}x_i,
\qquad |A|=2r.
\]
By exchangeability this depends only on r. Fix a set B of size 2r-1. Since sum_i x_i=0 and x_i^2=1,
\[
0=\mathbb E\left[\left(\sum_i x_i\right)\prod_{j\in B}x_j\right]
=(2r-1)\mu_{2r-2}+(42-2r+1)\mu_{2r}.
\]
Thus
\[
\mu_{2r}=-\frac{2r-1}{43-2r}\mu_{2r-2},\qquad \mu_0=1.
\]
For r=0,...,4,
\[
(\mu_0,\mu_2,\mu_4,\mu_6,\mu_8)
=\left(
1,-\frac1{41},\frac1{533},
-\frac{15}{41\cdot39\cdot37},
\frac{105}{41\cdot39\cdot37\cdot35}
\right).
\]

## 2. Orbit features and their exact Gram matrix

Let \(\mathcal O\) range over the 1,440 orbits of 4-subsets under D_42. Define
\[
\phi_{\mathcal O}(S)=\frac1{|\mathcal O|}
\sum_{I\in\mathcal O}f_I(S),
\qquad
\delta_{\mathcal O}=\mathbb E_q\phi_{\mathcal O}
-\mathbb E_u\phi_{\mathcal O}.
\]
The frozen ensemble is D_42-invariant, so \(\delta_{\mathcal O}\) is exactly the representative residual already enclosed by the 256-bit Arb all-orbit certificate.

Define the uniform Gram matrix
\[
G_{\mathcal O,\mathcal O'}
=\mathbb E_u[
\phi_{\mathcal O}(S)\phi_{\mathcal O'}(S)].
\]
Since \(f_I f_J=f_{I\triangle J}\), if \(s=|I\cap J|\) then
\[
\mathbb E_u[f_I f_J]=\mu_{8-2s}.
\]
D_42 invariance lets us fix one representative I in \(\mathcal O\) and average J over \(\mathcal O'\):
\[
G_{\mathcal O,\mathcal O'}
=\frac1{|\mathcal O'|}
\sum_{J\in\mathcal O'}\mu_{8-2|I\cap J|}.
\]
This formula is exact and symmetric in the two orbit labels.

All entries have a common rational denominator
\[
D=41\cdot39\cdot37\cdot35=2,070,705.
\]
For r=0,...,4, the integer numerators \(D\mu_{2r}\) are
\[
(D\mu_0,D\mu_2,D\mu_4,D\mu_6,D\mu_8)
=(2,070,705,-50,505,3,885,-525,105).
\]
Every D_42 orbit size divides 84, so the complete Gram quadratic form can be accumulated as one exact integer over denominator 84D. The verifier also checks exact Gram symmetry before evaluating the quadratic form.

## 3. A valid aggregate chi-square witness without a pseudoinverse

Let
\[
g_A(S)=\sum_{\mathcal O}A_{\mathcal O}\phi_{\mathcal O}(S)
\]
for any fixed real coefficient vector A. Since u is strictly positive on the finite balanced slice,
\[
\mathbb E_qg_A-\mathbb E_ug_A
=\mathbb E_u\left[\left(\frac qu-1\right)g_A\right].
\]
Cauchy-Schwarz gives
\[
\boxed{
\chi^2(q\Vert u)
\ge
\frac{(A^T\delta)^2}{A^TGA}
}
\tag{1}
\]
whenever \(A^TGA>0\). No inverse or pseudoinverse of the singular orbit Gram matrix is needed.

For a reproducible explicit witness, the verifier chooses
\[
A_{\mathcal O}
=\operatorname{round}_{\rm ties\text{-}even}
\left(10^9\,\operatorname{midpoint}(\delta_{\mathcal O})\right).
\]
The midpoint is used only to select integer coefficients. The final numerator \(A^T\delta\) is recomputed from the full frozen Arb intervals, and \(A^TGA\) is computed exactly as a rational number. Thus the coefficient-selection heuristic does not enter the certification step.

## 4. Certified N=42 result

The verifier reconstructs the 1,440 D_42 quartic orbits and checks their sizes against the frozen all-orbit evidence. It uses all 1,440 residual intervals (including the six defining equations whose intervals contain zero).

The deterministic integer coefficient vector has:
- length: 1,440;
- L1 norm: 1,029,450,893;
- SHA-256: `6480bd06e7e2dd8d78d1bd35c22e089be4b4085d4020cea1c1fab505ea1098d4`.

The Arb-enclosed linear form is
\[
A^T\delta\in
[1,816,610.709896652076354873848403984073487425305061829725750688012766228
\ \pm 6.58\times10^{-64}]>0.
\]
The exact Gram quadratic form is
\[
A^TGA=\frac{6214441155444128863}{138047}.
\]
Substitution in (1), with 256-bit Arb interval division, yields
\[
\boxed{
\chi^2(q\Vert u)>
0.0733075379017796406817054805625287.
}
\]
The previous best single-quartet consequence was only
\(\chi^2>3.03546316365989\times10^{-5}\). The aggregate orbit witness strengthens that candidate-specific chi-square lower bound by a factor exceeding 2,415.

By the exact Plucker frame-potential identity,
\[
\operatorname{FP}=\frac4{\binom{42}{21}}
(1+\chi^2(q\Vert u)),
\]
so the certified lower interval is
\[
\operatorname{FP}>
7.976158557965858567675768273986785847653014832763640808877121940091909
\times10^{-12},
\]
compared with the uniform target
\[
\frac4{\binom{42}{21}}
=7.431382223923010964580659670172348923453308318310907496251881494350740
\times10^{-12}.
\]

The existing bounded single-character witness remains the stronger direct TV certificate:
\[
\operatorname{TV}(q,u)>0.00275.
\]
The aggregate chi-square bound is **not** converted into a TV lower bound here. In particular, neither statement is a Choi trace-distance or channel diamond-distance bound.

## 5. Reproduction and evidence

Run:
\
    python -m pip install python-flint==0.9.0
    python verify_n42_quartic_orbit_gram_chi_square.py

The verifier reads the frozen 256-bit residual intervals from
`evidence/n42_period_two_six_quartic_all_orbits_arb.json`, enumerates all 111,930 quartets, checks all 1,440 orbit representatives and orbit sizes, constructs the exact Gram quadratic, and writes
`evidence/n42_quartic_orbit_gram_chi_square_arb.json`.

CI:
- Workflow: [46065596600](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46065596600), SUCCESS.
- Verifier: `verify_n42_quartic_orbit_gram_chi_square.py`.
- Machine certificate: `evidence/n42_quartic_orbit_gram_chi_square_arb.json`.

## 6. Interpretation and next step

This is a stronger, all-orbit certificate against one frozen 37-base / 74-labelled candidate. It does not rule out:
- a different period-two positive measure;
- a general non-period-two positive measure over the 42-cycle exponential family;
- membership of the full target in the closed convex hull of all cycle exponentials.

The next high-value task remains the full-cycle positive-measure/global-separator question in Issue #7. The Gram witness can serve as a candidate-specific rejection metric, but it is not a global separator because its coefficients were priced only against this candidate residual vector and no inequality over all physical couplings has been proved.
