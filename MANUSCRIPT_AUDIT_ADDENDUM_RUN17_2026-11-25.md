# EUI manuscript and evidence audit — run 17 (2026-11-25)

## Repository and manuscript inspection

The default branch was inspected through the recursive Git tree (977 paths; tree response not truncated), the latest commits, open Issues, Issue #5 comments, the 6,137-column theory note, the exact finite-pool certificate, the 256-bit continuous-escape certificate, and the 6,139-column workflow.

The public manuscript remains [arXiv:2506.20570v1, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*](https://arxiv.org/html/2506.20570v1). The tracked tree contains no `.tex`, `.bib`, `.bbl`, `.bst`, `.pdf`, `.docx`, `.doc`, `.odt`, or `.rtf` source. Thus no editable main-manuscript or separate supplement source is available in this repository. Prior Appendix B audit remains applicable: its 10,000 random instances report distribution-dependent average Choi fidelity, not a worst-case Hamiltonian guarantee or a diamond-norm theorem.

## Verified 6,137-column finite-pool theorem

The authoritative [workflow 45539976654](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45539976654) succeeded. The exact pool contains 22 pinned base atoms, 6,101 fractional single-open-path grid atoms, and 14 exact-rational gapped paths. It uses all 1,461 second-/fourth-order coordinates (21 second-order distances and all 1,440 fourth-order dihedral orbits).

The 94-term rational dual satisfies
\[
\|D^{-1}y\|_1=1,\qquad \|y\|_1=533.
\]
The independent Arb verifier certifies every listed column with common gap greater than (1/5), so for every mixture on this exact pool,
\[
\|b-Ap\|_\infty>1/2665,\qquad
\operatorname{TV}(w_p,u_{\rm bal})>1/5330.
\]
The TV conclusion is for the balanced program-label distribution / dephased register, not Choi trace distance or channel diamond distance.

## New continuous escape of the 6,137 dual

The 94-term dual was then strictly escaped by two exact-rational physical paths. [Workflow 45541488163](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45541488163) completed successfully; evidence was committed in [649cc8f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/649cc8f9f70688f21aa74c2054a59f430246028f).

- Connected open path: all 41 internal couplings are strictly positive, with minimum (9.9999999999999995\times10^{-7}). Its 256-bit Arb target-minus-score interval is centered at (-19.964971496200965374\ldots).
- Three-segment path: internal zero edges are ({4,5}), minimum positive coupling (10^{-8}). Its 256-bit Arb target-minus-score interval is centered at (-24.358461528831097759\ldots).

Both pass all 1,764 interval orthogonality-entry checks and determinant-one interval checks. These are strict escapes from this particular dual; they neither invalidate the 6,137 finite-pool theorem nor prove full-family feasibility/infeasibility.

The theory note [THEORY_6137COL_FULL_FOURTH_FINITE_POOL_N21.md](THEORY_6137COL_FULL_FOURTH_FINITE_POOL_N21.md) now records this escape and the updated next step.

## 6,139-column reoptimization

The two new exact-rational paths were appended to the fourteen existing gapped paths. The new pool has 22 base atoms + 6,101 fractional-grid atoms + 16 gapped paths = 6,139 candidates, retaining the complete 1,461-coordinate second-/fourth-order design.

New artifacts:
- `discover_ising_full_fourth_plus_sixteen_gapped_n21.py`
- `verify_ising_full_fourth_plus_sixteen_gapped_arb_n21.py`
- `.github/workflows/eui-reoptimize-6139-full-fourth.yml`

The first run exposed two metadata-pin/count mistakes before any mathematical conclusion; these were corrected in [0234e78](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/0234e78beefa237b5807acc8e0217676d5b0968b) and [85414be](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/85414be96052c2496166307b620b941628c29f57). The corrected authoritative run [45545125000](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45545125000) passed compilation and dependency-light regressions; the 6,139-column LP was still running at the time of this audit. No 6,139-column LP or Arb theorem is claimed yet.

## Open paper-level blockers

1. Construct an exact positive physical ensemble satisfying every even-principal-minor constraint at (n=21), or prove a genuinely global obstruction for the full allowed physical family.
2. Establish a rigorous quantitative bridge from the program-mass/moment discrepancy to Choi-state trace distance or channel diamond error.
3. Obtain the editable manuscript and supplementary source files before claiming formal paper-body revisions.

The next action is to inspect the final 6,139 LP and Arb result. If a dual is certified, continuously price that specific dual; if a primal appears, freeze exact rational weights and verify all 1,461 coordinates independently. A floating LP status alone is not a theorem.
