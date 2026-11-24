# Manuscript and evidence audit — EUI run 13 (2026-11-25)

## Repository and source audit

The current main tree has 946 tracked paths (recursive Git tree, not truncated). No tracked `.tex`, `.bib`, `.bbl`, `.bst`, `.pdf`, `.docx`, `.odt`, or `.rtf` manuscript/supplement source is present. The repository's manuscript-level scientific claims therefore remain documented in theory notes and audit addenda; this run did not modify a tracked TeX manuscript. The externally available manuscript remains [arXiv:2506.20570](https://arxiv.org/abs/2506.20570).

## New verified result: 6,133-column complete second-/fourth-order finite-pool obstruction

Workflow [45484523550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45484523550) completed successfully, including the LP, independent Arb verifier, evidence commit, and artifact upload.

The exact finite pool is 22 pinned base atoms + 6,101 corrected fractional single-open-path grid atoms + ten exact-rational gapped paths = 6,133 columns. The feature system is complete at second and fourth order: 21 distance-averaged second moments plus all 1,440 fourth-order dihedral orbits (111,930 quartets), for 1,461 full coordinates, 1,313 independent moment coordinates, and 1,314 equalities including normalization.

The exact rational dual has 85 nonzero coefficients and
\[
\|D^{-1}y\|_1=1,\qquad D=\operatorname{diag}(41I_{21},533I_{1440}),\qquad \|y\|_1=533.
\]
The last equality is exact. An automatically generated proof sentence incorrectly said \(\|y\|_1<533\); the certificate JSON proof text has been corrected to \(\|y\|_1=533\) in commit [706487f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/706487ff00380d4f4cfc6fd82e4ac5817ee7ad29). The verifier itself already checked \(\|y\|_1\le533\), so the strict residual conclusion is valid:
\[
y^{\mathsf T}(b-F(R_j))>1/5\quad (j=1,\ldots,6133),
\]
with minimum Arb lower endpoint
\[
0.22948739235422886048519109417616827\ldots>1/5.
\]
Consequently, for every probability mixture on this exact pool,
\[
\|b-A_{6133}p\|_\infty>1/2665,
\qquad \operatorname{TV}(w_p,u_{\rm bal})>1/5330.
\]
The TV statement concerns the balanced program-label distribution / dephased register, not a Choi-state or channel diamond-distance guarantee.

Formal note: [THEORY_6133COL_FULL_FOURTH_PLUS_TEN_GAPPED_FINITE_POOL_N21.md](THEORY_6133COL_FULL_FOURTH_PLUS_TEN_GAPPED_FINITE_POOL_N21.md), commit [c42e291](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/c42e2910b8b38c92e7ff3a8993604c19c8e8b3ec). Exact diagnostic and Arb certificate: `evidence/ising_full_fourth_plus_ten_gapped_n21.json` and `evidence/ising_full_fourth_plus_ten_gapped_arb_n21.json`; evidence commit [65fe242](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/65fe24253ede8010ea2a8a0dcf43f14c7297d34e).

## Continuous pricing of the new 85-term dual

A deterministic connected/multi-segment search and independent 256-bit Arb escape verifier have been added. The search uses 256 frozen-seed-pool starts, 256 independent connected starts, 128 fractional-profile perturbations, 256 random multi-segment starts, 12 local optimizations per class, and at most 160 L-BFGS-B iterations per start. This is finite multistart discovery only; any positive pricing result must be frozen as exact rationals and independently Arb-verified. Failure to find an escape is not a continuum upper bound.

The first launch failed before pricing because the copied parent script still expected eight gapped paths. The search and verifier guards were corrected to ten. Corrected run [45503337509](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45503337509) is the authoritative search attempt; a workflow-file refresh queued [45503445659](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45503445659). No continuous-family conclusion is claimed pending these results.

## Claim scope and paper blockers

The 6,133-column theorem is only for the exact listed finite pool and the complete second-/fourth-order feature design. It is not a continuum obstruction, does not include every even principal minor, and does not yield a Choi/diamond converse. The all-even-principal-minor positive ensemble (or a genuinely global physical-family obstruction) and the operational channel-error bridge remain unresolved.
