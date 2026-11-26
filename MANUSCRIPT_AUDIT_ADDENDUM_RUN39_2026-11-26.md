# EUI research audit — Run 39 (2026-11-26)

## Repository and issue selection

Inspected the current default branch, recent commits, all open issues (#3, #5, #6, #7), Issue #5's global-family frontier, Issue #7's matching-reachability work, the existing 3–7 perfect-mirror theorem, the two-mirror and single-mirror obstructions, the DPP representation, the conditional joint-parity diamond theorem, and the current manuscript audit.

- Main HEAD before this run: c5fef893166c95158b063c72c1234904122cd0e5.
- Selected Issue #5 because the remaining paper-central problem is still an exact long-ring physical ensemble or a global physical-family converse.
- The recursive Git tree contains 1,163 entries and is not truncated. No .tex, .bib, .pdf, .doc, or .docx manuscript/supplementary source is present. The public manuscript remains arXiv:2506.20570v1; no manuscript text was edited in this run.

## New exact result

The same rational distance-moment dual as the previous 3–7 theorem was exhaustively checked on every ordered composition of 42 into k=3,...,11 consecutive perfect-mirror blocks.

The exact dual is
\[
y=\frac1{47}(-10,8,-6,6,-4,2,-2,2,0,2,0,0,0,0,0,0,2,-2,0,0,1),
\qquad \|y\|_1=1.
\]

A new C++17 integer-only verifier enumerated **1,594,831,694** compositions in 29.60 seconds locally. The common exact minimum remains
\[
y^{\mathsf T}(t-m(R))\ge\frac2{40467}>0,
\]
with 155 attaining compositions (117 at k=3 and 38 at k=4); there were zero nonpositive cases. The per-k minima for k=5,...,11 are all strictly larger.

The score reduction adds each block's exact transposition contribution and each pair interaction of odd-block fixed centres. A separate direct signed-permutation implementation checked 1,000 deterministic random compositions (seed 202611260834), including determinant +1. The new scan reproduces the earlier 3–7 extrema exactly.

The convex-mixture consequences are
\[
\|t-\mathbb E_\mu m(R)\|_\infty\ge\frac2{40467},
\qquad
\operatorname{TV}(w_\mu,u_{\rm bal})\ge\frac1{40467}.
\]
The TV statement is only for the classical balanced program-label distribution / dephased register, not a Choi or diamond bound.

## Hosted reproducibility

Workflow [45731124882](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45731124882) completed successfully on commit 52e638458edee27da606ef76f8dad4bc18dd4f59. It passed:
- C++17 compilation with -O3 -Wall -Wextra -pedantic;
- the full 1,594,831,694-composition integer scan;
- exact regenerated-JSON comparison.

Commits:
- verifier: 7fbf488773dbc7e4d8b43fa3bdc4e5d1c02d9e4f;
- evidence: 7155d5005a462a7e5478dc7badebce7454550ce4;
- theory note: 2d495ad7a7bc52c369128f383eda0ffa5a9230f5;
- workflow: 52e638458edee27da606ef76f8dad4bc18dd4f59.

Issue #5 received the Run 39 progress comment (comment ID 7179125618).

## Exact scope boundary

The same dual fails on the two-block composition (1,41), with slack -80/40467; the separate two-mirror theorem is required for that family. This result does not cover k>=12, fractional-transfer blocks, arbitrary within-block couplings, general gapped paths, or the full continuous physical family. It does not resolve the all-even-principal-minor ensemble/global-converse question and does not imply a Choi/diamond lower bound.

## Next highest-value action

Leave exact perfect-mirror blocks. Test fractional-transfer and general gapped physical seeds against the complete moment/DPP criterion, using finite pools only for discovery and exact dual/primal certification for any claimed finite-family conclusion. The paper-central target remains an exact all-even-moment positive ensemble at n=21 or a separator valid for every allowed physical coupling vector.
