# Manuscript and research audit — Run 67 (2026-11-28)

## Repository and issue inspection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- Pre-run HEAD: be900738624b601aaaaff3418b2d7377e1961418.
- Recent commits and open Issues #7, #5, #6, and #3 were inspected. Issue #7 remains the selected highest-leverage scientific track: the exact N=42 unrestricted balanced-slice moment target is known, but its membership in the closed convex hull of the fixed cycle-exponential family remains unresolved.
- The latest Run 66 Plucker/fusion-frame note, N=42 all-quartic Arb evidence, verifier, and Issue #7 comments were read.
- The public manuscript is still identified as arXiv:2506.20570v1, “Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians” (Yin Mo, Tengxiang Lin, Xin Wang; submitted 25 June 2025). The paper includes appendices A–E in the manuscript record. The repository has no editable TeX/Bib manuscript or separately versioned supplementary source; no formal manuscript-body edit is claimed. The manuscript's Appendix B normalization issue remains tracked in Issue #6.

## Selected scientific question

Can all 1,440 quartic orbit residuals of the frozen N=42 period-two candidate be combined into one stronger exact discrepancy certificate, rather than retaining only the largest single-quartet witness?

## What changed

- Added `verify_n42_quartic_orbit_gram_chi_square.py`.
- Added `.github/workflows/eui-n42-quartic-orbit-gram.yml`.
- Added `THEORY_N42_QUARTIC_ORBIT_GRAM_CHI_SQUARE.md`.
- Added the generated exact/Arb certificate `evidence/n42_quartic_orbit_gram_chi_square_arb.json`.

## What is proved

1. For uniform balanced signs on 42 sites, the even moments through order eight obey the exact recurrence
   `mu_(2r)=-(2r-1)/(43-2r) mu_(2r-2)`.
2. The D42-orbit Gram entries of the averaged quartic characters are exact rational numbers determined only by quartet intersection sizes.
3. The exact Gram quadratic form for the frozen integer coefficient vector is
   `6214441155444128863/138047`.
4. Cauchy–Schwarz gives `chi^2(q||u) >= (A^T delta)^2/(A^T G A)`.
5. Using all 1,440 Arb residual intervals, the aggregate certificate proves
   `chi^2(q||u) > 0.0733075379017796406817054805625287`.
6. The Plucker frame-potential identity therefore gives the stated candidate-specific frame-potential lower bound.

## What was verified

- All 111,930 four-subsets were enumerated and grouped into exactly 1,440 D42 orbits.
- Orbit-size sum is exactly 111,930.
- Every orbit representative and orbit size matches the frozen 256-bit Arb audit.
- Exact Gram symmetry was checked using integer arithmetic.
- The Gram quadratic form was computed as an exact rational, not by floating-point matrix inversion.
- The final linear form and chi-square ratio were enclosed at 256-bit Arb precision.
- Workflow [46065596600](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46065596600) completed SUCCESS.
- Generated certificate commit: `2a70fb845cd30fc81f51f1751edf48fe199e9d06`.

## What remains blocked

- No complete N=42 physical positive ensemble.
- No global separator valid for every real 42-cycle coupling vector.
- No extension of this candidate-specific quartic Gram witness to a family-wide no-go theorem.
- No Choi trace-distance or diamond-distance operational bridge.
- No editable manuscript/supplementary source in the repository; Issue #6 remains open.

## Next highest-value action

Use the aggregate quartic Gram construction as a discovery metric for new general-cycle candidate pools, but do not mistake it for a global certificate. The decisive scientific target remains either (i) a strictly positive general-cycle ensemble matching the full even-minor hierarchy, or (ii) a global inequality valid for all real cycle couplings. Continue to use complete quartic-orbit checks and higher-even-order verification for every surviving candidate.
