# Manuscript / repository audit — Run 61 (2026-11-27)

## Repository snapshot

- Repository: tengxianglin/EfficientUnitaryInversion
- Default branch: main
- Pre-run HEAD: 70b4c796ae9f83d6fa889d018f071979a17f7cdf
- Current Run-61 head after additions: 017d68441425664ae749239cb9b892a79d2376dd
- The current repository tree contains 1,297 entries and is not truncated.
- No tracked TeX, Bib/Bbl, PDF, DOCX, or separate supplementary-source file was found. The public manuscript remains arXiv:2506.20570v1; this run did not edit manuscript text.

## Issues inspected

- Issue #7: physical reachability; latest prior scientific result was the exact N=8 unrestricted-cycle positive ensemble.
- Issue #5: 6,153-column finite-pool separator and continuous-family gap; its finite-pool and continuous-escape scopes remain distinct.
- Issue #6: Appendix B per-instance L1 normalization; QuAIRKit table regeneration remains pending.
- Issue #3: type-1.2 classifier regression passes; QuAIRKit runtime smoke test remains pending.
- Issue #4 is closed and was not duplicated.

## Run-61 scientific result

A new exact rational separator excludes the complete N=10 contiguous perfect-transfer block-reversal ansatz from the balanced-slice target. It covers all 512 ordered compositions of 10, arbitrary dihedral orientations, and vertex-sign gauges. The certified moment L-infinity gap is 52/2205.

This result is deliberately restricted. It does not exclude non-permutation cycle exponentials or the full continuous N=10 physical family, and it says nothing directly about N=42 feasibility.

## Files added

- THEORY_N10_BLOCK_MIRROR_SUBFAMILY_NO_GO.md
- verify_n10_block_mirror_subfamily_separator.py
- evidence/n10_block_mirror_subfamily_separator.json
- .github/workflows/eui-n10-block-mirror-subfamily-separator.yml

## Verification

- Exact integer/Fraction verifier exhausts 512 compositions with no floating-point arithmetic.
- All 512 block matrices pass R in SO(10), Q symmetric, Q squared equals identity, and trace Q equals zero.
- Seven D10 orbit coordinates define a nonnegative dual with exact L1 norm one.
- Target score: -74/2205.
- Maximum block-family score: -2/35.
- Strict gap: 52/2205.
- Exact score-table SHA256: 79911ca8a15b51b84eab95720c0265dc52b7f9db6c44feab26b7d11ea5e16804.
- GitHub Actions run 45969533826 passed both recomputation and semantic comparison against the frozen JSON.

## Commits

- b32486a4be94aa45240e562d3922429566efec4d — exact verifier
- 259ce54e71077e980155b6ef5199edfdc8bf9eb4 — frozen evidence
- 3b7a339c991a5797a1b3c398e383e5661c75462a — theory note
- 017d68441425664ae749239cb9b892a79d2376dd — CI workflow

## Next highest-value action

Search for the smallest non-perfect-transfer physical cycle atom or continuous one-parameter family that violates the seven-orbit block separator. This will determine whether the N=10 obstruction is only an ansatz limitation or can be extended to a larger physical family. Any finite search remains discovery only; a global physical-family claim requires an analytic bound or a certified continuum argument.
