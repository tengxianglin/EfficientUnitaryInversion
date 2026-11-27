# Manuscript and research audit — Run 68 (2026-11-28)

## Repository and issue inspection

- Repository: `tengxianglin/EfficientUnitaryInversion`; default branch `main`.
- Pre-run HEAD: `b44d75ddcdbacac48e8d0bebb4454ded0f16d4a0`.
- Inspected the latest 12 commits, open/recent Issues #7, #5, #6, and #3, Issue #7's full comment history, the Run 67 theory/verifier/certificate, the all-orbit Arb audit, the Plucker frame note, and the program-DPP derivation.
- Issue #7 remains the highest-leverage scientific track: the complete N=42 balanced-slice target is feasible over unrestricted SO(42), but its membership in the closed convex hull of the fixed cycle-exponential family remains open.
- The public manuscript remains arXiv:2506.20570v1. GitHub code search for TeX document source found no `\\documentclass` occurrence; no editable TeX/Bib or separately versioned supplementary source is present. No formal manuscript-body edit is claimed. Appendix B's normalization/table issue remains separately tracked in Issue #6.

## Selected question

Run 67 had a valid all-1,440-orbit Gram chi-square certificate, but its chosen coefficient vector was not optimal. Can the balanced-slice Gram kernel be diagonalized on the fourth harmonic subspace to obtain the best possible Cauchy–Schwarz bound from all quartic moments without a dense pseudoinverse?

## What changed

- Added `THEORY_N42_OPTIMAL_QUARTIC_CHI_SQUARE.md`.
- Added `verify_n42_optimal_quartic_chi_square.py`.
- Added `.github/workflows/eui-n42-optimal-quartic-chi-square.yml`.
- Added the frozen machine certificate `evidence/n42_optimal_quartic_chi_square_arb.json`.
- Generalized the fourth-order eigenvalue argument to an exact even-degree balanced-slice harmonic hierarchy (degrees 0, 2, 4, 6, 8).

## Mathematical result

For quartet characters (f_I(x)=\prod_{i\in I}x_i), define the residual vector (delta_I=\mathbb E_q f_I-\mathbb E_u f_I). Because the candidate matches all 861 pair coordinates, the balanced-sign identity proves (D_4\delta=0), where
[
(D_4a)_J=\sum_{i\notin J}a_{J\cup\{i\}},\qquad |J|=3.
]

The balanced-slice Gram kernel (K_{I,J}=\mathbb E_u[f_If_J]=\mu_{8-2|I\cap J|}) acts on (ker D_4) as the exact scalar
[
\lambda_4=\sum_{j=0}^4(-1)^j\binom4j\mu_{2j}=\frac{21888}{19721}.
]
This follows by expanding the intersection kernel in the binomial basis and using the iterated down relations. Hence the optimal degree-four character Cauchy–Schwarz bound is
[
\chi^2(q\Vert u)\ge
\frac{\sum_{|I|=4}\delta_I^2}{\lambda_4}
=\frac{19721}{21888}\sum_{\mathcal O}|\mathcal O|\delta_{\mathcal O}^2.
]
It is optimal among all degree-four character witnesses; it is not the full chi-square unless higher harmonic discrepancies vanish.

For every even degree (m\le n), the same argument gives
[
\lambda_m=\sum_{j=0}^m(-1)^j\binom mj\mu_{2j}
=4^m\frac{\binom{N-2m}{n-m}}{\binom Nn}.
]
The verifier checks this exact formula at (N=42), (m=0,2,4,6,8).

## Certified N=42 result

The 256-bit Arb certificate records:

- all 861 pair moments independently recomputed;
- all 111,930 quartets grouped into 1,440 D42 orbits;
- all 11,480 fourth-to-third down relations interval-checked;
- exact (lambda_4=21888/19721);
- (sum_{|I|=4}\delta_I^2\in[0.09140488998805873205537629\ldots\pm7.66\times10^{-71}]);
- optimal quartic-only bound
[
\boxed{\chi^2(q\Vert u)>
0.0823554383888206439539508334768407205232\ldots}
]
- improvement factor over Run 67's arbitrary-coefficient bound:
[
1.1234238762617255\ldots>1.12;
]
- corresponding Plucker frame-potential lower bound:
[
\operatorname{FP}>
8.0433969648090794326211907557789651\times10^{-12}.
]

The previous Run 67 bound remains valid; it was simply suboptimal. The direct bounded-character program-label TV lower bound remains (>0.00275). The improved chi-square certificate does not imply a stronger TV, Choi, or diamond-distance bound.

## Reproducibility

- First complete certificate workflow [46078549522](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46078549522): SUCCESS.
- Final workflow including the general eigenvalue hierarchy [46078659186](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46078659186): SUCCESS.
- Both workflows pin `python-flint==0.9.0), regenerate the exact-real positive weights, rerun the 861-pair and 1,440-orbit audits, and create the Arb certificate.
- Final certificate commit: `630fd2f` (full SHA recorded in Git history).
- The intermediate run `46078516302` was cancelled after a workflow simplification; it is not counted as a failed mathematical check.

## Remaining blockers

- No complete N=42 physical positive ensemble.
- No global separator valid for every real 42-cycle coupling vector.
- No proof that a different period-two or non-period-two physical measure is impossible.
- No Choi/diamond operational bridge.
- No editable manuscript/supplement source.

## Next highest-value action

Extend the harmonic decomposition to degree six without assuming the candidate matches all quartic moments. Compute the degree-six harmonic projection of the sixth-order residual after removing its lower-degree components, then add its nonnegative contribution to the chi-square lower bound. This requires a structured (D_6D_6^\mathsf T) solve on the D42-invariant 5-subset orbit space; do not treat raw sixth-order residuals as harmonic while the quartic residual is nonzero.
