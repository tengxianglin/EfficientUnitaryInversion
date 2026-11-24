# Manuscript audit addendum — EUI run 12 (2026-11-25)

## Repository/source audit

The current `main` tree contains 930 tracked files. A recursive tracked-path scan found no `.tex`, `.bib`, `.bbl`, `.bst`, `.pdf`, `.docx`, `.odt`, or `.rtf` manuscript/supplement source. The externally available manuscript remains [arXiv:2506.20570v1](https://arxiv.org/abs/2506.20570); this run did not modify that external manuscript and must not be described as a manuscript-text revision.

## New verified result

The 6,131-column complete second-/fourth-order finite-pool obstruction is now independently Arb-certified:

- exact pool: 22 base atoms + 6,101 corrected fractional single-open-path grid atoms + 8 exact-rational gapped paths;
- feature system: all 21 distance-averaged second moments and all 1,440 fourth-order dihedral orbits (111,930 quartets), 1,461 coordinates / 1,313 independent moment coordinates;
- rationalized dual: 82 nonzero coefficients, exact scaled norm `||D^{-1} y||_1 = 1`, exact full-coordinate `||y||_1 < 533`;
- Arb precision: 512 bits for base/gapped columns and 128 bits for all 6,101 grid columns;
- all 6,131 strict column inequalities certified with common gap (>1/5);
- finite-pool moment residual: (\|b-Ap\|_\infty>1/2665);
- finite-pool program-label TV: (\mathrm{TV}(w_p,u_{\rm bal})>1/5330).

Evidence: [certificate commit 053032e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/053032e2fbe094448076e29883fa8f7285f40920), [successful CI 45469881533](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45469881533), and [formal theory note](THEORY_6131COL_FULL_FOURTH_PLUS_EIGHT_GAPPED_REOPTIMIZATION_N21.md).

## Claim language required in any manuscript

The result is a **finite-pool** theorem for the exact 6,131 listed columns and the complete second-/fourth-order moment design. It is not:

- a separator for all continuous nonuniform positive couplings or all multi-segment paths;
- a constraint on every even principal minor;
- a positive-ensemble construction or a proof of full-family infeasibility;
- a Choi-state trace-distance or channel diamond-distance converse.

The program-mass TV statement concerns the dephased balanced-label distribution only. It must not be promoted to an operational channel guarantee without an additional theorem.

The finite-pool theorem is useful as a reproducible certified benchmark and as a source of exact dual witnesses, but by itself it is not the paper's central physical result. A Nature Physics-level claim still requires either an exact positive ensemble satisfying the full all-even-principal-minor system at (n=21), or a genuinely global obstruction for the intended continuous physical family, together with a rigorous operational error bridge.

## Active next test

A deterministic connected/multi-segment general-gapped pricing search against the frozen 6,131-column dual is running in [workflow 45483583523](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45483583523). The search is discovery only; any candidate escape must pass the independent 256-bit Arb verifier. No conclusion about the continuous family is recorded until that verification finishes.
