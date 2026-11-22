# A rational continuous-path escape from the 151-column dual

Date: 2026-11-23

## Finding

The exact rational dual certified against the frozen 1,641-column canonical pool is **not** a global separator for the full continuous positive-coupling path family.

The dual score is
\[
S(c)=\lambda-\delta+z^\mathsf T a(c),
\]
where \(z\), \(\lambda\), \(\delta=10^{-10}\), the 1,779 normalized rows, and their ordering are pinned by the files **evidence/55probe_151col_dual_certificate_n21.json** and **evidence/joint_low_six_eighth_lp_151col_55probe_n21.json**.

## Explicit physical witness

Let
\[
m=(6,0,14,0,0,26,0,10,0,32,0,18,0,34,0,30,2,6,0,7,23,0,28,0,10,0,32,0,20,2,4,1,32,0,68,0,2,0,26,0,30).
\]
Define the 41 open-path edge magnitudes exactly by
\[
c_j=\begin{cases}
1/1000,&m_j=0,\\
3927m_j/5000,&m_j>0,
\end{cases}
\qquad j=0,\ldots,40,
\]
and set \(c_{41}=0\). Thus every one of the 41 path edges is strictly positive; the witness lies in the positive orthant left after the exact sign-gauge reduction. Its largest edge magnitude is \(53.4072\).

The multi-start differentiable search was used only to discover the near signed-permutation pattern. The final witness is rational; no optimizer output enters the proof.

## 128-bit Arb certificate

The verifier rebuilds \(R(c)=e^{K(c)}\) from the exact rational couplings using Arb, reconstructs all 52 nonzero entries of the exact dual against the pinned low/sixth/eighth row inventory, and evaluates \(S(c)\) as an interval.

The successful workflow [45045453133](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45045453133) completed successfully. It certifies
\[
S(c)\in
[500.2406414402261032179394993312647\ \pm\ 3.03\times10^{-32}],
\]
with the Arb enclosure for the lower endpoint strictly positive:
\[
\underline{S(c)}\in
[500.24064144022610321793949933126466979\ \pm\ 3.52\times10^{-36}].
\]
The candidate is verified to be outside the frozen 1,641-column pool. Its exact input SHA256 is
0221d6eb7570d87ef52bd17eff30e83ff1fcc2ae765dc86f582b2f3c30082e08.

Evidence: **evidence/continuous_path_dual_escape_arb_n21.json**. The verifier is **verify_continuous_path_dual_escape_arb.py** and the workflow is **.github/workflows/eui-continuous-path-dual-escape-arb.yml**. Evidence commit: [d8a4df8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d8a4df8530d2084629af5575fa2f2d6af7848df6).

Reproduce with:

~~~bash
python freeze_seed_pool.py
python verify_continuous_path_dual_escape_arb.py
~~~

## Consequences and scope

- **Disproved:** the current 151-column rational dual cannot be promoted to a global separator over all strictly positive 41-edge path couplings. The required inequality \(a(c)^\mathsf Tz+\lambda-\delta<0\) fails by more than 500 at this explicit physical generator.
- **Unaffected:** the previously certified lower bound over the frozen 1,641-column canonical pool remains valid. The witness is rigorously checked to be outside that pool.
- **Not proved:** existence of a convex mixture over the full continuous family achieving the \(1/3\) cap; nonexistence of a different global dual; a full-family minimax value; complete moment control; or a Choi/diamond-norm operational guarantee.

The next step is to include this certified generator in a new finite minimax reoptimization. This tests whether the continuous escape is useful for constructing a better ensemble, rather than merely invalidating the old dual's global extension. The binary64 152-column reoptimization is running separately; it is discovery evidence only until a candidate is rationalized and independently Arb-certified.


## A 152-column exact candidate now passes the pinned selected-row design

The certified escape was added to the 151-column active pool. The 1,779-row binary64 HiGHS reoptimization found objective \(0.329769894504226\), with recomputed maximum \(0.329769894504254\), support 51, new-column weight \(4.7680963914\times10^{-5}\), and primal-dual gap \(2.55\times10^{-15}\). This is only the discovery stage.

The 51 positive weights were rationalized exactly and sum to one. A separate 128-bit Arb run then certified every row:
- all 1,461 second-/fourth-order rows;
- all 311 selected sixth-order rows;
- all seven selected eighth-order rows.

The strict result is
\[
\max_{r\in\mathcal R_{1779}}|e_r|
\le
0.329769894504730415
<\frac13,
\]
with a certified margin to \(1/3\) of
\[
0.0035634388286029185\ldots.
\]
The Arb enclosure for the maximum absolute-error upper endpoint is
\[
[0.32976989450473041482078054778650805091\pm3.67\times10^{-40}],
\]
and the margin enclosure is
\[
[0.00356343882860291851255278554682528242\pm3.46\times10^{-39}].
\]

Evidence: **evidence/candidate_152col_selected_rows_arb_n21.json**; exact rational input: **evidence/candidate_joint_input_152col_continuous_escape_n21.json**; LP transcript: **evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json**; verifier: **verify_152col_continuous_escape_candidate_arb.py**; successful workflow [45046016471](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45046016471); evidence commit [55ec898](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/55ec8985979af1563022d4f6e5ce1404d4b3148b).

This is a rigorous exact-probability witness for the **pinned 1,779-row design**. The 1,461 second/fourth rows are complete, but the 311 sixth and seven eighth rows are selected subsets. It therefore does not establish the complete sixth/eighth maxima, all-moment control, full-family optimality, or an operational Choi/diamond-norm bound. The next decisive task is a complete 63,133-orbit sixth-order audit of this exact mixture, followed by an eighth-order strategy.
