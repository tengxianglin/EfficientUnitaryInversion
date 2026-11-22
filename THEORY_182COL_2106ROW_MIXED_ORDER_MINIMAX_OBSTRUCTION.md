# Strict 182-column mixed-order minimax obstruction

Date: 2026-11-23

## Theorem

Let \(\mathcal P_{182}\) be the fixed set of 182 physical 42-site path generators pinned by
`evidence/joint_low_six_lp_182col_sixth_only_n21.json`. It consists of:

1. the 151-column canonical base inventory;
2. the exact rational continuous-path generator certified in `evidence/continuous_path_dual_escape_arb_n21.json`;
3. the twenty earlier canonical additions recorded in the LP transcript;
4. the ten further canonical additions
   \[
   (544,420,398,352,629,668,347,425,296,844).
   \]

Canonical indices are zero-based in the frozen 1,641-column canonical pool. For each coupling vector \(c=(c_0,\ldots,c_{40},0)\), the path-skew generator is the \(42\times42\) real matrix
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j
\quad (j=0,\ldots,40),
\]
with all other entries zero, and \(R(c)=e^{K(c)}\).

Let \(\mathcal R\) be the 2,106-row normalized constraint inventory used by the LP: all 1,461 second-/fourth-order rows and 645 pinned sixth-order \(D_{42}\)-orbit rows. For \(c\in\mathcal P_{182}\), write \(a(c)\in\mathbb R^{2106}\) for its normalized feature column, and let \(y\in\mathbb Q^{2106}\) be the exact normalized target. For \(p\in\Delta(\mathcal P_{182})\), define the selected-row residual
\[
e(p)=\sum_{c\in\mathcal P_{182}}p_c a(c)-y.
\]

Then every probability distribution on this fixed physical pool satisfies
\[
\boxed{
\|e(p)\|_\infty
\ge
\frac{1727085050310122398125808297}
{3689348814741917030000000000}
=0.468127340903367\ldots
>\frac13.
}
\]

Since \(\mathcal R\) is a subset of the full moment-constraint inventory, the same lower bound also applies to any larger moment objective that contains all these 2,106 normalized rows. The theorem is mixed-order: its dual uses two low-order rows and fifty sixth-order rows.

## Proof

The 128-bit Arb certificate supplies an exact rational vector \(z\in\mathbb Q^{2106}\), a rational scalar \(\lambda\), and slack
\[
\delta=\frac1{10^{10}}.
\]
It verifies
\[
\|z\|_1=1,
\]
\[
\lambda=
\frac{245960609898981376}{167697673397359865},
\qquad
\lambda+z^\mathsf Ty=
\frac{4317712626697643199}{9223372036854792575},
\]
and hence
\[
\lambda+z^\mathsf Ty-\delta
=
\frac{1727085050310122398125808297}
{3689348814741917030000000000}.
\]

The support of \(z\) has 52 coordinates: two low-order coordinates (zero-based row indices 233 and 1265) and fifty sixth-order coordinates. Thus this certificate is not a sixth-only certificate.

For every one of the 182 physical columns, independent 128-bit Arb evaluation proves
\[
a(c)^\mathsf Tz+\lambda-\delta<0.
\]
The largest certified interval upper endpoint over all columns is
\[
-7.9382193303777883336833217916209471162\times10^{-11}<0.
\]

For any \(p\in\Delta(\mathcal P_{182})\), Hölder's inequality and the exact \(L_1\) normalization give
\[
\|e(p)\|_\infty\ge z^\mathsf T(y-\sum_c p_ca(c)).
\]
Using the certified column inequalities and \(\sum_c p_c=1\),
\[
\begin{aligned}
z^\mathsf T(y-\sum_c p_ca(c))
&=z^\mathsf Ty-\sum_c p_c\,a(c)^\mathsf Tz\\
&\ge z^\mathsf Ty+\lambda-\delta.
\end{aligned}
\]
The right-hand side is the exact rational lower bound displayed in the theorem. This proves the claim.

## Reproducibility and evidence

- Binary64 LP discovery transcript: `evidence/joint_low_six_lp_182col_sixth_only_n21.json`.
- Exact rational dual and all 182 Arb intervals: `evidence/55probe_182col_sixth_only_dual_certificate_n21.json`.
- Verifier: `verify_182col_sixth_only_dual_arb.py`.
- Automated workflow: [182-column Arb certification workflow](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/workflows/eui-182col-sixth-only-dual.yml).
- Successful certificate commit: [be82f21777e8ae1714fc4c488528a5374e50d942](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/be82f21777e8ae1714fc4c488528a5374e50d942).

The certificate records 128-bit Arb / python-flint 0.8.0, exact \(\|z\|_1=1\), 182 strictly negative column-inequality intervals, and the exact lower bound. The raw HiGHS dual is used only for discovery; the theorem relies on the rationalized certificate and independent interval evaluation.

## Scope and limitations

This is a rigorous minimax lower bound for mixtures over the **specified 182-generator pool** and the pinned 2,106-row design. It is mixed-order, not a complete-sixth-order theorem. It does not exclude the remaining canonical generators, arbitrary additional continuous path generators, or the unrestricted physical family. It is not an operational Choi-fidelity or diamond-norm theorem.
