# Seventh strict continuous-path escape from the 189-column dual

Date: 2026-11-23

## Result

The exact 189-column mixed-order dual is valid for its pinned finite physical
pool, but it does not separate the full positive 41-edge path family. A
deterministic 10-start differentiable search over
\[
10^{-4}\le c_j\le100,\qquad j=0,\ldots,40,\qquad c_{41}=0
\]
found a seventh exact-decimal-rational path. All 41 open-edge couplings are
strictly positive. The candidate is distinct from all six previously certified
continuous paths and is outside the frozen canonical inventory.

The exact 42-component input is
\[
\begin{aligned}
c={}&(
18.226529769971,\;4.821263136368,\;0.598200923905,\;17.233306031547,\\
&1.091379592135,\;0.022137505570,\;0.001823476210,\;0.431910510900,\\
&0.004073996441,\;1.597059649468,\;0.009728628717,\;0.108615304897,\\
&26.391809032704,\;4.025630558753,\;0.005983810954,\;0.563838691000,\\
&64.390209492732,\;0.102115709420,\;0.002731166785,\;1.559852852927,\\
&0.001325933145,\;1.559944870579,\;0.188956943699,\;1.572304810615,\\
&0.785369817612,\;6.287155881465,\;1.126975918369,\;20.384514425276,\\
&0.001416435098,\;17.247697272313,\;0.252742803531,\;0.008204716134,\\
&0.011689223034,\;1.470868974873,\;0.035066498687,\;0.006848539775,\\
&1.557729543832,\;0.002336395382,\;1.651119569834,\;0.235991941821,\\
&1.217512490554,\;0).
\end{aligned}
\]
The 41 decimal entries are exact rational inputs with denominator \(10^{12}\);
the last zero is the path-padding coordinate. Candidate SHA256:
2dcdd30f2a0c9fbb901c9f63748ca2ca5151e770b92b93255a0cb36324d734c8.

## Strict Arb counterexample

Let
\[
S_{189}(c)=z^\mathsf T a(c)+\lambda-\delta
\]
be the exact pricing functional of the 189-column dual certified in
THEORY_189COL_2113ROW_SIXTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md.
The independent 128-bit Arb verifier gives
\[
\boxed{
S_{189}(c)\in
[207.4357421969902709413811580245091
\pm2.10\times10^{-32}]>0.
}
\]
Its enclosing lower endpoint is itself strictly positive:
\[
[207.43574219699027094138115802450907910
\pm8.74\times10^{-37}]>0.
\]
Thus the 189-column dual inequality fails for this legal continuous path.
This is a rigorous counterexample to extending this particular finite-pool
dual to all positive 41-edge couplings.

## Search and derivative diagnostics

The discovery program used the cofactor determinant derivative and the
adjoint Frechet derivative of the matrix exponential. The analytic gradient
was checked against complex-step differentiation at coordinates 0, 20, and
40; the maximum relative defect was
\[
1.0714305862054578\times10^{-13}.
\]
The best point came from start 8, with binary64 score 207.43574219722365 after
100 iterations. The optimizer reported its iteration limit, not convergence.
This is discovery evidence only; the proof is the exact-rational input and
independent Arb interval.

As a pricing implementation regression, the search re-evaluated the sixth
path (column 1646). Its binary64 score against the new 189-column dual was
\(-8.934698314533307\), consistent with the certified column interval
\[
[-8.9418568666754042859550\times10^{-9}
\pm5.14\times10^{-32}]<0.
\]
The candidate is not a duplicate of any of the six prior paths.

## Reproducibility

- 189-column exact dual certificate:
  **evidence/55probe_189col_sixth_continuous_escape_dual_certificate_n21.json**
- Parent 189-column LP transcript:
  **evidence/joint_low_six_eighth_lp_189col_sixth_continuous_escape_n21.json**
- Search program: **discover_189col_continuous_dual_escape.py**
- Independent verifier: **verify_189col_continuous_dual_escape_arb.py**
- Search transcript:
  **evidence/189col_continuous_dual_search_n21.json**
- Arb certificate:
  **evidence/189col_continuous_dual_escape_arb_n21.json**
- Successful search and Arb workflow:
  https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45147006543
- Search transcript SHA256:
  2862b1fc35e1739bed710f9b2059b1b5c855e57a975a091247e8aab7417a9900
- 189-column dual certificate SHA256:
  14fc8281a35b95d737885fc673f1e4b667848c35afe03a6e3eb277ada9fcdc2c
- Sixth prior escape certificate SHA256:
  31749b9038749e77371b47fc5a45a87c5d7e9b7580bfedace9894ab36f6b8ca7
- Candidate SHA256:
  2dcdd30f2a0c9fbb901c9f63748ca2ca5151e770b92b93255a0cb36324d734c8
- Search/verifier/workflow commits:
  [1fd531a](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1fd531a121e88332c685e9558967a6e829dd76ff),
  [64b7b52](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/64b7b5283a7be21d4417e4935e0593fbb6d994c6),
  [5198789](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5198789cdcb6dd41c08756257304454aaf3c1e43).

The workflow re-certified the 189-column dual and all six earlier continuous
escapes, compiled the search and verifier, ran the deterministic 10-start
search, and independently verified the exact candidate with 128-bit Arb.

## Scope

This result does not invalidate the finite 189-column minimax theorem. It
does not show that a probability mixture over the full continuous path family
attains \(1/3\), nor does it determine the full-family minimax value. A
strictly positive pricing value only disproves global separation by this
particular dual. The seventh path is the next column-generation input, label
1647, for a 190-column reoptimization on the unchanged 2,113-row design.
