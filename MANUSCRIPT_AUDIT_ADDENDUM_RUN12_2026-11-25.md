# Manuscript audit addendum — EUI run 12 (2026-11-25)

## Repository/source audit

The current main tree contains 935 tracked files. A recursive tracked-path scan found no .tex, .bib, .bbl, .bst, .pdf, .docx, .odt, or .rtf manuscript/supplement source. The externally available manuscript remains [arXiv:2506.20570v1](https://arxiv.org/abs/2506.20570). This run updated theory/audit documentation and reproducibility code; it did not modify the external arXiv manuscript or a tracked TeX manuscript.

## New verified result: 6,131-column finite-pool theorem

The complete second-/fourth-order finite-pool obstruction is independently Arb-certified:

- exact pool: 22 base atoms + 6,101 corrected fractional single-open-path grid atoms + 8 exact-rational gapped paths;
- feature system: all 21 distance-averaged second moments and all 1,440 fourth-order dihedral orbits (111,930 quartets), 1,461 coordinates / 1,313 independent moment coordinates;
- rationalized dual: 82 nonzero coefficients, exact scaled norm \(\|D^{-1}y\|_1=1\), exact full-coordinate \(\|y\|_1<533\);
- Arb precision: 512 bits for base/gapped columns and 128 bits for all 6,101 grid columns;
- all 6,131 strict column inequalities certified with common gap \(>1/5\);
- finite-pool moment residual:
  \[
  \|b-Ap\|_\infty>\frac1{2665};
  \]
- finite-pool program-label TV:
  \[
  \mathrm{TV}(w_p,u_{\rm bal})>\frac1{5330}.
  \]

Evidence: [certificate commit 053032e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/053032e2fbe094448076e29883fa8f7285f40920), [successful CI 45469881533](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45469881533), and [formal theory note](THEORY_6131COL_FULL_FOURTH_PLUS_EIGHT_GAPPED_REOPTIMIZATION_N21.md).

## New verified counterexamples: this 6,131 dual is not global

The deterministic pricing search [45483583523](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45483583523) evaluated 520 initial candidates, optimized eight starts per class, and passed the gradient self-test (maximum absolute defect \(1.1421\times10^{-10}\)). Two exact rational candidates were then independently certified at 256-bit Arb:

- a connected path with all 41 internal couplings strictly positive:
  \[
  y^{\mathsf T}(b-F(R(c)))\in[-26.44327687623536845\ldots\pm6.42\times10^{-72}]<0;
  \]
- a five-segment path with cuts \(\{12,17,29,37\}\):
  \[
  y^{\mathsf T}(b-F(R(c)))\in[-30.37726183060399288\ldots\pm1.73\times10^{-69}]<0.
  \]

Both pass all 1,764 interval orthogonality checks and determinant-one certification. They refute extension of this **particular** 6,131-column dual to the tested connected/multi-segment general-gapped family. They do not invalidate the finite-pool theorem.

Evidence: [escape commit 4991341](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4991341eb3e95325cd8817c1de3c402094c95fd3), [escape theory note](THEORY_6131COL_DUAL_GAPPED_ESCAPE.md), [search transcript](evidence/ising_full_fourth_plus_eight_gapped_search_n21.json), and [256-bit Arb certificate](evidence/ising_full_fourth_plus_eight_gapped_escape_arb_n21.json).

## Claim language required in any manuscript

The 6,131-column result is a **finite-pool** theorem for the exact listed columns and complete second-/fourth-order moment design. It is not:

- a separator for all continuous nonuniform positive couplings or all multi-segment paths;
- a constraint on every even principal minor;
- a positive-ensemble construction or a proof of full-family infeasibility;
- a Choi-state trace-distance or channel diamond-distance converse.

The program-mass TV statement concerns the dephased balanced-label distribution only. It must not be promoted to an operational channel guarantee without an additional theorem.

The finite-pool theorem is a reproducible certified benchmark and a source of exact dual witnesses, but by itself it is not the paper's central physical result. A Nature Physics-level claim still requires either an exact positive ensemble satisfying the full all-even-principal-minor system at \(n=21\), or a genuinely global obstruction for the intended continuous physical family, together with a rigorous operational error bridge.

## Active next test

Both exact 256-bit Arb escapes have been appended to the finite pool. [Workflow 45484523550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45484523550) is reoptimizing the complete 1,461-coordinate LP on 6,133 columns (22 base + 6,101 fractional-grid + 10 gapped). Compilation and dependency-light regressions have passed; the LP step is still running. If a dual candidate is returned, the independent 512-/128-bit Arb verifier will check every column. A floating primal, if returned, will remain discovery-only until exact weights and all 1,461 coordinates are independently interval-verified.
