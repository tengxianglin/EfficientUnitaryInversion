# Sixth strict continuous-path escape from the 188-column dual

Date: 2026-11-23

## Result

The exact 188-column mixed-order dual certificate is valid for its pinned finite pool, but it is not a separator for the full positive 41-edge path family. A deterministic 10-start differentiable search on
\\[
10^{-4}\\le c_j\\le100,\\qquad j=0,\\ldots,40,\\qquad c_{41}=0
\\]
found a sixth exact-decimal-rational path. Every one of its 41 open-edge couplings is strictly positive.

The exact candidate is
\\[
\\begin{aligned}
c={}&(
1.557693687547,\;0.002877357763,\;0.021190764638,\;0.007114110334,\\
&1.484155521983,\;0.037308109473,\;0.001035347640,\;0.016290725399,\\
&0.084652416481,\;39.206065874702,\;2.111454577257,\;0.001580874601,\\
&94.249378266275,\;0.029695790857,\;0.055301952344,\;1.576351817092,\\
&0.035353211565,\;4.685922713622,\;0.021559439312,\;0.148517670497,\\
&8.016797597760,\;9.440638294227,\;8.249678117505,\;0.066244509277,\\
&1.572134969248,\;0.002974546059,\;2.029403391754,\;15.588566238536,\\
&0.004987857535,\;1.570439790764,\;0.010792803743,\;0.251785375663,\\
&5.272497080353,\;0.003156249080,\;0.030690048066,\;0.001525963444,\\
&70.683176931881,\;0.003168248219,\;0.011728013760,\;1.566626530533,\\
&0.002937588474,\;0).
\\end{aligned}
\\]
All decimals are exact rational inputs, not rounded display approximations. The candidate SHA256 is
``68baf2aa6667b3b0eb597ef576e114b37f3c6dc790f28068dfd1c74059724680``.

## Strict Arb counterexample

Let \\(S_{188}(c)=z^\\mathsf T a(c)+\\lambda-\\delta\\) be the exact pricing functional of the certified 188-column dual. An independent 128-bit Arb calculation gives
\\[
\\boxed{
S_{188}(c)\\in
[229.8600847483890088894499687466130
\\pm3.31\\times10^{-32}]>0.
}
\\]
The enclosing lower endpoint is strictly positive:
\\[
229.86008474838900888944996874661296698>0.
\\]
Therefore the 188-column dual inequality fails for this legal continuous path. This is a rigorous counterexample to extending this *particular dual* from its finite 188-column pool to all positive 41-edge paths.

## Search and derivative diagnostics

The search used the cofactor determinant derivative and the adjoint Frechet derivative of the matrix exponential. The analytic gradient was checked against complex-step differentiation at coordinates 0, 20, and 40. The maximum relative defect was
\\[
1.8853041827096364\\times10^{-14}.
\\]
The best discovery came from start 0, with binary64 score 229.86008474837345 after 100 iterations; the optimizer reported its iteration limit rather than convergence. This optimizer status is not part of the proof. The exact-rational input and independent Arb interval are the proof. Two other starts converged to a negative local value, illustrating that the search is not a global optimization certificate.

The previous fifth path (column 1645) was used as the starting point and reproduced the 188-dual pricing value within the search program's regression tolerance. The candidate is distinct from all five prior continuous paths and outside the frozen canonical inventory.

## Reproducibility

- 188-column dual certificate: ``evidence/55probe_188col_fifth_continuous_escape_dual_certificate_n21.json``, SHA256 ``eed80945f8ae5875c7fbad6f4d760c934654eaf44ce22a4bf373f4358ccedef5``
- Parent LP transcript: ``evidence/joint_low_six_eighth_lp_188col_fifth_continuous_escape_n21.json``, SHA256 ``f512d8fa40887d84a3274c7dd5f4716b841573e90adcd2ff7f12d191c2bf8297``
- Search program: ``discover_188col_continuous_dual_escape.py``
- Independent verifier: ``verify_188col_continuous_dual_escape_arb.py``
- Search transcript SHA256: ``772d3df9da55e83431e2652cc2bf46b17ee24b195abc751074edc1673a6f30e2``
- Arb certificate SHA256: ``d3bb1345d95d305cc48ca1cb491257e6c868bef9``
- Candidate SHA256: ``68baf2aa6667b3b0eb597ef576e114b37f3c6dc790f28068dfd1c74059724680``
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45142329253

The workflow re-certified the frozen seed pool, orbit-enumeration regression, all five prior continuous escapes, and the 188-column parent dual; compiled both new programs; ran the deterministic 10-start search; and independently certified the exact candidate with 128-bit Arb.

## Scope

This result does not invalidate the finite 188-column minimax theorem. It does not show that a probability mixture over the full continuous path family attains \\(1/3\\), nor does it prove a full-family minimax value. A positive pricing score only disproves this particular dual's global separation. The sixth path is now appended as column 1646 for a 189-column reoptimization on the unchanged 2,113-row design.
