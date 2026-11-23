# Fifth strict continuous-path escape from the 187-column dual

Date: 2026-11-23

## Result

The exact 187-column mixed-order dual certificate is valid for its pinned finite pool, but it is not a separator for the full positive 41-edge path family. A deterministic 10-start differentiable search on
\[
10^{-4}\le c_j\le100,\qquad j=0,\ldots,40,\qquad c_{41}=0
\]
found an exact-decimal-rational path with all 41 open-edge couplings strictly positive.

The candidate is
\[
\begin{aligned}
c={}&(
1.635512245944,\ 0.002878204976,\ 0.187740986991,\ 0.007123673714,\\
&1.575635659055,\ 0.037667922327,\ 0.001035308803,\ 0.016437007768,\\
&0.084403170422,\ 38.845090456503,\ 5.757806884892,\ 0.001580874363,\\
&92.890015573910,\ 0.029694158500,\ 0.271481819954,\ 1.528907588132,\\
&0.035356946759,\ 4.736257385450,\ 0.021585007165,\ 0.150968288864,\\
&7.988562680285,\ 9.433568840462,\ 8.329227415212,\ 0.066247874897,\\
&1.571752230549,\ 0.002975626348,\ 1.971435771370,\ 15.571628759131,\\
&0.004987900580,\ 1.570464440760,\ 0.010830287726,\ 0.633587842177,\\
&4.677185870615,\ 0.003156305401,\ 0.030754989339,\ 0.001525963478,\\
&70.683607516976,\ 0.003168248530,\ 0.011752150351,\ 1.543297055304,\\
&0.002938196468,\ 0).
\end{aligned}
\]
All decimals are exact rational inputs, not rounded display approximations.

The candidate SHA256 is
\[
\texttt{7565cc9aa5240c5c42b8692e97381c4415061403e2bddf4563c03fc779e9a9e8}.
\]

## Strict Arb counterexample

Let \(S_{187}(c)=z^\mathsf Ta(c)+\lambda-\delta\) be the exact pricing functional of the certified 187-column dual. An independent 128-bit Arb calculation gives
\[
\boxed{
S_{187}(c)\in
[216.2699462606013389218645814697156
\pm6.50\times10^{-32}]>0.
}
\]
The lower endpoint is strictly positive:
\[
216.26994626060133892186458146971553506
\quad\text{(with an enclosing Arb radius }2.85\times10^{-37}\text{)}.
\]
Therefore the 187-column dual inequality fails for this legal continuous path. This is a rigorous counterexample to extending this *particular dual* from its finite 187-column pool to all positive 41-edge paths.

## Search and derivative diagnostics

The search used the cofactor determinant derivative and the adjoint Frechet derivative of the matrix exponential. The analytic gradient was checked against complex-step differentiation at coordinates 0, 20, and 40. The maximum relative defect was
\[
4.4930725806580085\times10^{-13}.
\]
The best discovery came from start 2, with binary64 score 216.2699462605962 after 100 iterations; the optimizer reported its iteration limit rather than convergence. This optimizer status is not part of the proof. The exact-rational input and independent Arb interval are the proof.

The previously certified fourth path (column 1644) was used as the starting point and reproduced the 187-dual Arb pricing interval to within the search program's \(10^{-8}\) regression tolerance. The candidate is distinct from all four prior continuous paths and from the frozen canonical inventory.

## Reproducibility

- 187-column dual certificate: \(\texttt{evidence/55probe\_187col\_fourth\_continuous\_escape\_dual\_certificate\_n21.json}\), SHA256 \(\texttt{475346510c8d0e7d52031cb21d694f91230beb60}\)
- Parent LP transcript: \(\texttt{evidence/joint\_low\_six\_eighth\_lp\_187col\_fourth\_continuous\_escape\_n21.json}\), SHA256 \(\texttt{8a63fdbec151593e1c52cf3e55585d6c8760d6b3536564812758526ccdbbe245}\)
- Search program: \(\texttt{discover\_187col\_continuous\_dual\_escape.py}\)
- Independent verifier: \(\texttt{verify\_187col\_continuous\_dual\_escape\_arb.py}\)
- Search transcript SHA256: \(\texttt{b37ba7c81ae78f32e41741e68038eac6dd726b64}\)
- Arb certificate SHA256: \(\texttt{d84f7b32f0748a3e7433c990b3f82469a178dd4c}\)
- Candidate SHA256: \(\texttt{7565cc9aa5240c5c42b8692e97381c4415061403e2bddf4563c03fc779e9a9e8}\)
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45134044907

The workflow re-certified the frozen seed pool, orbit enumeration, all four prior continuous escapes, and the 187-column parent dual; compiled both new programs; ran the 10-start search; and independently certified the exact candidate with 128-bit Arb.

## Scope

This result does not invalidate the finite 187-column minimax theorem. It does not show that a probability mixture over the continuous path family attains \(1/3\), nor does it prove a full-family minimax value. A positive pricing score only disproves this particular dual's global separation. The next decisive step is to add this path as column 1645, reoptimize the 2,113-row LP, and independently certify the resulting finite-pool branch.
