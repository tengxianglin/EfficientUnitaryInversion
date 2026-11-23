# Certified continuous-path escape from the 190-column EUI dual

## Result and scope

The exact 190-column mixed-order dual certificate is valid for its 190 pinned physical generators on the fixed 2,113-row design. It is **not** a global separator for the positive 41-edge open-path family.

Let \(c=(c_0,\ldots,c_{40},0)\), with all \(c_j>0\), define
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,
\]
and \(R(c)=e^{K(c)}\). Let \(a(c)\in\mathbb R^{2113}\) be the normalized moment-feature vector used in the 190-column LP. For the exact rational dual vector \(z\), equality multiplier \(\lambda\), and slack \(\delta=10^{-10}\) stored in the 190-column certificate, define
\[
S_{190}(c)=z^\mathsf T a(c)+\lambda-\delta.
\]

**Proposition (strict escape of the 190-column dual).** For the exact-decimal-rational path below, the independent 128-bit Arb evaluation gives
\[
\boxed{
S_{190}(c)\in
[345.1964392867855698654219114260899
\pm2.12\times10^{-32}]>0.
}
\]
Consequently, this particular 190-column dual cannot be extended as a separating dual inequality to the unrestricted positive 41-edge path family.

## Exact path input

The 42 stored components (the last zero is the open-path terminal sentinel) are
\[
\begin{aligned}
c={}&(
14.134437492174,\ 0.190261470888,\ 0.411466773086,\ 10.972725485567,\\
&0.606259159424,\ 0.021846481920,\ 0.001882603399,\ 0.015099366508,\\
&0.003421680612,\ 1.598319987193,\ 0.010187180784,\ 0.106997242451,\\
&15.468112506162,\ 2.739706004316,\ 0.006857550879,\ 0.580395668787,\\
&45.545087354604,\ 0.114975523359,\ 0.002950193993,\ 1.511597663984,\\
&0.001173109292,\ 1.578199624532,\ 0.095968472018,\ 1.572224130816,\\
&0.856839796083,\ 7.817500373972,\ 1.379809549137,\ 23.521812911275,\\
&0.001348563474,\ 20.413670699821,\ 0.256062462844,\ 0.008176316485,\\
&0.010677814958,\ 1.607996676897,\ 0.033068070601,\ 0.006954713395,\\
&1.570818832017,\ 0.002568130286,\ 1.602169484759,\ 0.162466823699,\\
&0.000290289601,\ 0).
\end{aligned}
\]
Every one of the 41 physical edge magnitudes is strictly positive. The exact decimal strings are interpreted as rational numbers by the Arb verifier. Candidate SHA256:
\[
\texttt{6abd599d3f0ee33e411492ab07cf0cc69c6dce446e10328333ff5c55c3a5bf41}.
\]
The path is distinct from all seven earlier Arb-certified escapes and outside the frozen 1,641-column canonical inventory.

## Discovery diagnostics (not the proof)

The deterministic search used 10 starts in
\[
10^{-4}\le c_j\le100,\qquad j=0,\ldots,40,
\]
with 100 L-BFGS-B iterations per start. It used the cofactor determinant derivative and the adjoint Frechet derivative of the matrix exponential. The maximum relative defect between the analytic gradient and complex-step differentiation at coordinates \(0,20,40\) was
\[
2.5868335251644226\times10^{-12}.
\]
The best rounded binary64 discovery score was \(345.1964392867765\). The best run reached its iteration limit; optimizer convergence is **not** claimed. None of these floating-point diagnostics is used as the proof.

## Independent certificate and provenance

The 128-bit Arb transcript records:
- 190-column dual-certificate SHA256: `e0893ebde8e7974712bfdf89a6d65fcb1d374a32692810f474e6c453d699b568`;
- 190-column LP transcript SHA256: `2a4ca0caab7c7ed5dab24f07e51c121e03e49236da98cbc59809d96868e94307`;
- 2,113-row cut-design SHA256: `d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f`;
- prior seventh-escape certificate SHA256: `c39aa30c96fa526ac6113dd79387f6637fb7ede959eba56a4835987be22f2f34`;
- exact candidate SHA256: `6abd599d3f0ee33e411492ab07cf0cc69c6dce446e10328333ff5c55c3a5bf41`.

The dual has exact \(\|z\|_1=1\) and active support on two fourth-order, 54 selected sixth-order, and two selected eighth-order rows. The Arb computation evaluates all 58 active contributions using the exact rational path input. The strict positive lower endpoint, rather than the optimizer's binary64 score, is the counterexample certificate.

Evidence:
- [Discovery transcript](evidence/190col_continuous_dual_search_n21.json)
- [128-bit Arb certificate](evidence/190col_continuous_dual_escape_arb_n21.json)
- [Successful workflow 45159106797](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45159106797)

## Logical consequences and limitations

This result strictly refutes global separation by the **particular 190-column dual**. It does **not**:
1. invalidate the finite 190-column minimax theorem;
2. prove that a probability mixture over the full continuous family reaches \(1/3\);
3. prove a global continuous-family minimax lower or upper bound;
4. certify complete sixth- or eighth-order orbit control (the design still uses 645 selected/cut sixth rows and seven selected eighth rows);
5. imply a Choi-infidelity or diamond-norm operational guarantee.

The next finite experiment appends this path as column 1648 and reoptimizes the same 2,113-row objective in a 191-column pool. A new above-cap result requires a newly rationalized dual and independent Arb checks of all 191 columns. A below-cap HiGHS result remains discovery only until an exact rational primal passes Arb and the complete sixth-order orbit audit.
