# Certified ninth continuous-path escape from the 191-column EUI dual

## Proposition and scope

The exact 191-column mixed-order dual certificate is valid for its 191 pinned physical generators on the fixed 2,113-row design. It is **not** a global separator for the positive 41-edge open-path family.

Let
\[
c=(c_0,\ldots,c_{40},0),\qquad c_j>0,
\]
and define
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,
\]
with \(R(c)=e^{K(c)}\). Let \(a(c)\in\mathbb R^{2113}\) denote the exact normalized mixed-order moment-feature vector in the pinned LP. For the rational dual \(z\), equality multiplier \(\lambda\), and slack \(\delta\) in the 191-column certificate, set
\[
S_{191}(c)=z^\mathsf T a(c)+\lambda-\delta.
\]

**Proposition (strict escape of the 191-column dual).** For the exact-decimal-rational path listed below, the independent 128-bit Arb verifier encloses
\[
\boxed{
S_{191}(c)\in
[240.12916173240860667511831935153365\pm7.55\times10^{-33}]>0.
}
\]
The lower endpoint is strictly positive. Hence the particular 191-column dual certificate cannot be extended as a separating inequality to the full positive 41-edge path family.

## Exact path input

The 42 stored components (the final zero is the open-path terminal sentinel) are
\[
\begin{aligned}
c={}&(
29.842071045900,\ 0.147173701121,\ 0.017034025682,\ 4.711960864374,\\
&0.001404267798,\ 0.028420214383,\ 0.002486734119,\ 0.013598934033,\\
&0.002773668873,\ 1.607509554348,\ 0.006807625309,\ 0.127298024879,\\
&10.995062300499,\ 0.000285424656,\ 0.004324218591,\ 1.095629112887,\\
&12.516325680784,\ 0.180085528035,\ 0.002103857099,\ 0.000100000000,\\
&0.001736601635,\ 1.584900017519,\ 0.001549162883,\ 0.000100000000,\\
&0.120113545713,\ 7.852340480089,\ 0.115247520361,\ 4.714186494418,\\
&0.001256258171,\ 7.849934746856,\ 0.176335383210,\ 0.003838747535,\\
&0.016156676987,\ 1.569316104431,\ 0.022485184411,\ 0.003278378287,\\
&1.567442750433,\ 0.002718889085,\ 1.565726569714,\ 0.048242163363,\\
&0.000179562578,\ 0).
\end{aligned}
\]
All 41 physical edge magnitudes are strictly positive. Two coordinates equal the discovery box's lower boundary \(10^{-4}\); this is allowed by the open-path physical domain and does not weaken the strict Arb sign. The exact decimal strings are parsed as rational numbers by the verifier.

Candidate SHA256:
\[
\texttt{0464f35ac416c7a89979e573d82f8e00da5c7700cc07e0122221d1088ca8de36}.
\]
The candidate differs from all eight earlier Arb-certified escapes and is outside the frozen 1,641-column canonical inventory.

## Discovery diagnostics (not the proof)

The deterministic discovery search used ten starts in
\[
10^{-4}\le c_j\le100,\quad j=0,\ldots,40,
\]
with at most 100 L-BFGS-B iterations per start. The score gradient used cofactor determinant derivatives and the adjoint Frechet derivative of the matrix exponential. The maximum relative defect against complex-step differentiation at coordinates \(0,20,40\) was
\[
2.765565554341265\times10^{-13}.
\]
Two starts reported optimizer success; the best positive candidate came from a run that reached its iteration limit. Optimizer convergence is not claimed. The binary64 score is discovery only; the proposition is established by the independent exact-input Arb evaluation.

## Independent certificate and provenance

The verifier used 128-bit Arb (python-flint 0.8.0). The rational 191-column dual has
\[
\|z\|_1=\frac{576460752303381559}{576460752303423488}<1
\]
and 59 active rows: two complete low-order rows, 55 selected/cut sixth-order rows, and two selected eighth-order rows.

Pinned inputs:
- 191-column dual certificate SHA256: 1cae877a2ac8d9e58e4d286ed388475c65a1a03ab50e635fc0ad88c5919d497e;
- 191-column LP transcript SHA256: e39f101e0b681e827d253b51c3753d2e58013d7dcf2d61156b8d7ea3eeee7efc;
- 2,113-row cut-design transcript SHA256: d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f;
- discovery transcript SHA256: 451e26f8caee7ed4505847ab5fc3631ad6eb8abfcf9f41cd5a130b98927eda79;
- candidate SHA256: 0464f35ac416c7a89979e573d82f8e00da5c7700cc07e0122221d1088ca8de36.

Evidence:
- Discovery: evidence/191col_continuous_dual_search_n21.json
- Independent Arb certificate: evidence/191col_continuous_dual_escape_arb_n21.json
- Verifier: verify_191col_continuous_dual_escape_arb.py
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45178729623
- Evidence commit: https://github.com/tengxianglin/EfficientUnitaryInversion/commit/cf142f3b96476a3385aa6bb296e37e811948ee53

## Logical consequences and limitations

This result:
1. strictly refutes global separation by this particular 191-column dual over the positive 41-edge open-path family;
2. leaves the finite 191-generator minimax theorem unchanged;
3. does not prove feasibility or infeasibility of the full continuous-family minimax problem;
4. does not certify the complete sixth/eighth orbit objective (the pinned design still has 645 selected/cut sixth rows and seven selected eighth rows);
5. does not establish an EUI-specific Choi-infidelity or diamond-distance guarantee.

The next decisive finite computation is to append this path as physical column 1649 and reoptimize the same 2,113-row LP, producing a 192-column discovery transcript. If the new LP remains above one third, its newly rationalized dual must be independently certified against all 192 physical columns. If it falls below one third, the exact rationalized primal must pass Arb on all pinned rows and then the complete sixth-order orbit audit.
