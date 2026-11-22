# Strict sixth-order minimax obstruction for the 172-column physical pool

Date: 2026-11-23

## Theorem

Let \(\mathcal P_{172}\) be the following fixed set of 172 physical 42-site path generators:

1. the 151 canonical generators in the frozen base inventory;
2. the exact rational continuous-path generator in \`evidence/continuous_path_dual_escape_arb_n21.json\`;
3. the ten earlier canonical additions
   \[
   (1603,886,565,682,472,525,434,487,80,145);
   \]
4. the ten new canonical additions
   \[
   (1613,1412,1383,1580,195,221,424,655,614,635).
   \]

Canonical indices are zero-based in the frozen 1,641-column pool. The complete column order and exact physical inputs are pinned by the LP transcript and Arb certificate cited below.

For a path generator \(c\), let \(R(c)=e^{K(c)}\), with the path-skew generator convention used by the repository. For a six-subset \(I\subset\mathbb Z_{42}\), let \(\mathcal O(I)\) be its \(D_{42}\)-orbit and define the orbit-averaged principal-minor feature
\[
m_I(c)=\frac{1}{|\mathcal O(I)|}
\sum_{J\in\mathcal O(I)}\det R(c)_{J,J}.
\]
Let \(\tau_I\) be the exact sixth-order target and let
\[
\sigma_6=\frac{5}{19721},\qquad
e_I(p)=\frac{\sum_{c\in\mathcal P_{172}}p_c m_I(c)-\tau_I}{\sigma_6},
\quad p\in\Delta(\mathcal P_{172}).
\]

Then every probability distribution over this fixed physical pool obeys
\[
\boxed{
\max_{I\in\binom{\mathbb Z_{42}}6/D_{42}}|e_I(p)|
\ge
\frac{1324494537887082708836219}
{2814749767106560000000000}
=0.4705549862247987\ldots
>\frac13.
}
\]

The result is a complete-sixth-order lower bound: the certified dual vector has support on only 50 sixth-order orbit rows and has exactly zero coefficients on all 1,461 second-/fourth-order rows. Those 50 rows are members of the full \(D_{42}\) sixth-order orbit domain (63,133 orbits).

## Proof

The 172-column discovery LP uses 2,106 normalized rows: all 1,461 second-/fourth-order rows and 645 pinned sixth-order orbit rows. Write its column feature matrix and target as \(A\) and \(y\). The 128-bit Arb certificate supplies an exact rational vector \(z\in\mathbb Q^{2106}\), an exact rational \(\lambda\), and slack
\[
\delta=10^{-10}.
\]
The certificate verifies
\[
\|z\|_1=
\frac{288230376151706861}{288230376151711744}<1,
\]
\[
\lambda=\frac{413924430527507}{281474976710656},
\]
and
\[
\lambda+z^\mathsf Ty
=
\frac{135628240708460307}{288230376151711744}.
\]

All 172 physical columns pass the independent 128-bit Arb interval check
\[
(A^\mathsf Tz)_j+\lambda-\delta<0.
\]
The largest certified interval upper endpoint is
\[
-7.6774063738680112067944501056\times10^{-11}<0.
\]
The vector \(z\) has exactly 50 nonzero coordinates, all in the sixth-order block; its low-order coordinates vanish exactly.

For any probability vector \(p\in\Delta(\mathcal P_{172})\),
\[
\begin{aligned}
\max_{I\in\mathcal O_6}|e_I(p)|
&\ge z^\mathsf T(y-Ap)\\
&=z^\mathsf Ty-\sum_jp_j(A^\mathsf Tz)_j\\
&\ge z^\mathsf Ty+\lambda-\delta\\
&=
\frac{1324494537887082708836219}
{2814749767106560000000000}.
\end{aligned}
\]
The first inequality follows from \(\|z\|_1<1\) and the fact that \(z\) is supported only on sixth-order rows. The second uses the certified column inequalities and \(\sum_jp_j=1\). This proves the theorem.

## Exact certificate and reproducibility

- LP discovery transcript: \`evidence/joint_low_six_lp_172col_sixth_only_n21.json\`.
- Exact rational dual and all 172 Arb intervals: \`evidence/55probe_172col_sixth_only_dual_certificate_n21.json\`.
- Parent 162-column physical inventory: \`evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json\`.
- Sixth-row inventory: \`evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json\`.
- Continuous-path generator certificate: \`evidence/continuous_path_dual_escape_arb_n21.json\`.
- Verifier: \`verify_172col_sixth_only_dual_arb.py\`.
- Workflow: [45068269670](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45068269670).
- Certificate commit: [288a253](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/288a2534356453e5c05e5b64a9ba4aaaabe9eb26).

The exact lower-bound margin above \(1/3\) is
\[
\frac{1158733846554688126508657}
{8444249301319680000000000}
=0.13722165289146537\ldots.
\]

## Scope and limitations

This theorem excludes every convex mixture over the **specified 172 generators** from achieving a sixth-order worst-orbit normalized error at or below \(1/3\). It does not exclude the remaining 1,470 canonical generators, any other continuous path generator, or the unrestricted physical family. It is not a no-go theorem for EUI as a whole, and it does not establish a Choi-fidelity or diamond-norm guarantee. The next step is to price all remaining canonical generators against this new exact dual and independently Arb-check the leading positive candidates.
