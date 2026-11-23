# Strict continuous-path escape from the 186-column mixed-order dual

Date: 2026-11-23

## Result

The exact rational dual certificate for the fixed 186-column / 2,113-row mixed-order minimax LP is not a global separator over the positive 41-edge open-path family.

The 186-column finite-pool theorem remains valid for its pinned 186 physical generators. Its exact dual and 186 Arb column intervals are frozen in evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json; its LP transcript is evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json.

A deterministic 10-start differentiable search over
\[
10^{-4}\le c_j\le100,\qquad j=0,\ldots,40,
\]
found a fourth continuous path, distinct from the three previously certified continuous paths and from the frozen canonical inventory. The exact-decimal-rational couplings are
\[
\begin{aligned}
c=(&0.434695801528,\ 0.003695222946,\ 0.216590546521,\ 0.009536987933,\\
&1.582741746908,\ 0.052404116295,\ 0.001035618851,\ 0.019198225618,\\
&0.061366207153,\ 35.748807739560,\ 5.259283087920,\ 0.001258399855,\\
&73.822485245050,\ 0.034270082906,\ 0.461989255005,\ 1.523653045027,\\
&0.028881779235,\ 4.695601361192,\ 0.021476079005,\ 0.136575073076,\\
&8.794202254384,\ 12.496156874612,\ 9.234941690299,\ 0.064802535827,\\
&1.589867387486,\ 0.002493757677,\ 1.941178759297,\ 25.048820353218,\\
&0.004291040767,\ 1.647100983413,\ 0.016834603493,\ 1.584295553370,\\
&6.066897905792,\ 0.001972589892,\ 0.032826820493,\ 0.001021607509,\\
&54.985618845816,\ 0.003341829314,\ 0.008744905068,\ 1.528087910796,\\
&0.003280423248,\ 0).
\end{aligned}
\]
All 41 open-path edge magnitudes are strictly positive; the final zero is the terminal padding coordinate. The exact candidate SHA256 is
\[
\texttt{f9c28135608deb0c687407a8cc71e58bf7f3bb5763ab8f997fd3b1141625c24d}.
\]

The search uses the cofactor determinant derivative and adjoint Frechet derivative of the matrix exponential. The maximum relative complex-step gradient defect on coordinates 0, 20, and 40 is \(1.098600377336112\times10^{-14}\). The already-included third escape (column 1643) is reproduced by the binary64 pricing function at \(-1.2151701866969233\times10^{-10}\), consistent with the midpoint of its Arb interval \([-1.2385191934701026011473\times10^{-10}\pm5.54\times10^{-33}]\). These are implementation checks, not the proof.

## Strict Arb certificate

An independent 128-bit Arb verifier reconstructs the exact rational coupling input, matrix exponential, all 54 active dual features, and the exact rational 186-column dual. It certifies
\[
\boxed{
S_{186}(c)\in
[281.0783501949911583545100045096690
\pm1.26\times10^{-32}]>0.
}
\]
The lower endpoint is strictly positive. Thus the attempted universal inequality \(S_{186}(c)\le0\) fails on the unrestricted positive 41-edge path family.

## Reproducibility

- Search program: discover_186col_continuous_dual_escape.py
- Independent Arb verifier: verify_186col_continuous_dual_escape_arb.py
- Search transcript: evidence/186col_continuous_dual_search_n21.json
- Arb certificate: evidence/186col_continuous_dual_escape_arb_n21.json
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45130632601
- Search transcript SHA256: 5f92901fe1191394191c1750f7f4de2d35c6d39c
- Arb certificate SHA256: 5d7b25dfc15e9183bf1a06672479bdd8a4cd515b
- Parent 186-column dual SHA256: 365dc82f4540cb6821038da3059efeb8cb8205b3
- Parent 186-column LP SHA256: 8fdaf824fa742ae34a5a156c251feadd59b0047b
- Candidate SHA256: f9c28135608deb0c687407a8cc71e58bf7f3bb5763ab8f997fd3b1141625c24d

The workflow rechecked the frozen seed pool and orbit-enumeration regression, re-certified all three prior continuous escapes and the 186-column parent dual, compiled both new scripts, ran the 10-start search, and passed the independent Arb gate.

## Scope

This is a strict counterexample to extending this particular 186-column dual over the full positive-coupling path family. It does not invalidate the 186-column finite-pool minimax theorem, construct a feasible probability ensemble for the unrestricted family, prove a global minimax value, or establish a Choi-fidelity/diamond-norm guarantee.

The next decisive step is to append this exact path as column 1644, re-solve the same 2,113-row mixed-order LP, and independently Arb-certify the resulting finite-pool dual or exact-probability candidate. A failed local search against the next dual will not be treated as a global separation proof.
