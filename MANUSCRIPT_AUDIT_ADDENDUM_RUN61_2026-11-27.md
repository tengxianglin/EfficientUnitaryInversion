# Manuscript / repository audit — Run 61 (2026-11-27)

## Repository snapshot

- Repository: tengxianglin/EfficientUnitaryInversion
- Default branch: main
- Pre-run HEAD: 70b4c796ae9f83d6fa889d018f071979a17f7cdf
- Run-61 scientific additions now extend through commit fb76cc1db059c911066f8efe745f848035183e86.
- The repository tree contained 1,297 entries at the initial audit and was not truncated.
- No tracked TeX, Bib/Bbl, PDF, DOCX, or separate supplementary-source file was found. The public manuscript remains arXiv:2506.20570v1; this run did not edit manuscript text.

## Issues inspected

- Issue #7: physical reachability; latest prior result was the exact N=8 unrestricted-cycle positive ensemble.
- Issue #5: 6,153-column finite-pool separator and continuous-family gap; its finite-pool and continuous-escape scopes remain distinct.
- Issue #6: Appendix B per-instance L1 normalization; QuAIRKit table regeneration remains pending.
- Issue #3: type-1.2 classifier regression passes; QuAIRKit runtime smoke test remains pending.
- Issue #4 is closed and was not duplicated.

## Run-61 result A: exact N=10 block-mirror no-go

A seven-orbit rational functional excludes the complete contiguous perfect-transfer block-reversal ansatz at N=10. It covers all 512 ordered compositions, arbitrary dihedral orientations, and vertex-sign gauges.

- Target score: -74/2205.
- Maximum score over the 512 block atoms: -2/35.
- Exact L-infinity moment discrepancy lower bound: 52/2205.
- Dual coefficients are nonnegative and have exact L1 norm one.
- Every signed-permutation atom was checked for R in SO(10), Q symmetric, Q squared equals identity, and trace Q zero.

The exact integer/Fraction verifier and its frozen summary are in:
- THEORY_N10_BLOCK_MIRROR_SUBFAMILY_NO_GO.md
- verify_n10_block_mirror_subfamily_separator.py
- evidence/n10_block_mirror_subfamily_separator.json

Workflow 45969533826 passed the exhaustive recomputation and semantic evidence comparison.

## Run-61 result B: the block separator is escaped by a connected physical cycle

The exact rational uniform cycle c_0=...=c_9=409/100 was priced independently at 256-bit Arb precision. The certified score is
\[
S(R)\in[-0.0029736260361924988743358517869826031222995682174649011732303449734630080
\pm 6.02\times10^{-74}].
\]
This is strictly above both the block-family ceiling -2/35 and the target score -74/2205. The Arb verifier also checks R orthogonal, det R=1, Q symmetric, Q squared equals identity, and trace Q=0.

Artifacts:
- verify_n10_uniform_cycle_escape_arb.py
- evidence/n10_uniform_cycle_escape_arb.json
- .github/workflows/eui-n10-uniform-cycle-escape.yml
- Workflow 45969973861 passed the independent recomputation and frozen-evidence comparison.

This escape refutes only the seven-orbit functional as a global separator. It does not construct a target ensemble and does not prove full N=10 convex-hull feasibility.

## Commits

- b32486a4be94aa45240e562d3922429566efec4d — exact block-family verifier
- 259ce54e71077e980155b6ef5199edfdc8bf9eb4 — block-family evidence
- 3b7a339c991a5797a1b3c398e383e5661c75462a — block-family theory
- 017d68441425664ae749239cb9b892a79d2376dd — exact enumeration CI
- ed0f514dba5faacac7973832b5667870ff90d6b2 — connected-cycle Arb verifier
- 172df48b7bdbb01e4c3c4ef3dd1060f9ef56e28a — connected-cycle workflow
- 8a0ceeaa47e1c425f3d8e108faa0c61c4821805f — connected-cycle Arb evidence
- fef6874eb3c6fa25d30e28b74c339ea22ba5e9fb — frozen Arb evidence comparison
- fb76cc1db059c911066f8efe745f848035183e86 — theory note updated with the connected escape

## Next highest-value action

Use N=10 as a tractable full-cycle test bed: search for a small positive ensemble of non-perfect-transfer cycle exponentials matching the complete even-minor target, or develop a global separator that survives the connected uniform-cycle escape. A finite search remains discovery only; any positive result must check every even subset/order, and any negative result must cover the continuous coupling family.
