# EUI manuscript/evidence audit — Run 54 (2026-11-27)

## Repository and selection

- Repository: `tengxianglin/EfficientUnitaryInversion`; default branch `main`.
- HEAD at start of this run: [`a25e50b8a31fb750e60f8802aa641e44a580764d`](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a25e50b8a31fb750e60f8802aa641e44a580764d).
- Recent commits and the open/recent issue set were inspected. Issue [#5](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5) remains the highest-leverage scientific track: the finite-pool/full-cycle-family convex-hull gap.
- Issues #7 (physical reachability of the perfect-matching ensemble), #6 (Appendix B noise normalization), #4 (complete eighth-order audit of the 29-column witness), and #3 (type-1.2 classifier correctness) were also rechecked. Their scopes remain distinct; none supersedes #5 for the present result.

## 1. Current finite-pool theorem remains valid

The 6,153-column full-second-/fourth-order finite-pool theorem is independently Arb-certified at 128 bits for the 6,101 fractional-grid columns and 512 bits for the 22 base plus 30 exact-rational gapped columns. The exact dual has 116 nonzero coefficients, exact full-coordinate (L_1) norm 533, and a common rational column gap (1/5). Therefore, for mixtures over those exact 6,153 columns only,
[
\|b-Ap\|_\infty>1/2665,\qquad
\operatorname{TV}(w_p,u_{\rm bal})>1/5330.
]
The TV statement is for the program-label/dephased classical register, not a Choi trace-distance or diamond-distance bound.

Evidence:
- [Finite-pool diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_n21.json)
- [Finite-pool Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_arb_n21.json)
- [Finite-pool workflow 45880800772](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880800772)
- [Finite-pool evidence commit e705c3d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e705c3de4eb65f43009d382caed904cf8b62fa3f)

## 2. Completed continuous pricing: the 6,153 dual is not global

The continuous-pricing workflow [45892294782](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45892294782) completed successfully. The job log shows that dependency installation, compilation, deterministic search, independent Arb verification, evidence pin checks, and evidence commit all completed.

Discovery used seed `202611270434`, 1,822 starts, L-BFGS-B with analytic Fréchet gradients, and a maximum finite-difference gradient defect (1.816526928877238\times10^{-10}). This finite multistart is discovery only.

The independent 256-bit Arb verifier certified:

- **Connected open-path witness:** all 41 internal couplings are strictly positive; the exact minimum is (19999999999999999/20000000000000000000000\approx10^{-6}), with wrap edge (c_{41}=0). Its target-minus-score interval is
  [
  [-20.32400371225355344245\ldots\pm3.92\times10^{-72}]<0.
  ]
- **Four-segment witness:** internal cuts ({12,30,33}), minimum positive coupling (10^{-8}), and target-minus-score interval
  [
  [-27.88470464737509788381\ldots\pm6.17\times10^{-73}]<0.
  ]

For each witness the verifier checked all 1,764 orthogonality entries by Arb and certified determinant one. It also pins the exact 6,153 diagnostic, finite certificate, and search transcript by SHA256.

Evidence:
- [Search transcript](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_search_n21.json)
- [256-bit Arb escape certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_escape_arb_n21.json)
- [Workflow 45892294782](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45892294782)
- [Evidence commit a25e50b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a25e50b8a31fb750e60f8802aa641e44a580764d)

## 3. New analytic result: open full-cycle positive-coupling region

The connected witness is not merely a boundary artifact with a zero wrap edge. The exact rational 116-term dual has (|y|_1=533), and every retained feature is an average of principal minors of order two or four.

For the cyclic skew generator, perturbing every coupling by at most (delta) changes each row/column absolute sum of the generator by at most (4delta). Hence
[
\|A(c)-A(c^*)\|_2\le4\delta.
]
Because both generators are skew-symmetric, Duhamel's formula gives
[
\|e^{A(c)}-e^{A(c^*)}\|_2\le4\delta.
]
Multilinearity and Hadamard's inequality bound the change of every order-two/order-four principal minor, and hence every averaged feature, by (4\|e^{A(c)}-e^{A(c^*)}\|_2). Thus the dual score changes by at most
[
4\|y\|_1\cdot4\delta=8528\delta.
]

Choose (delta=1/2,000,000). The exact minimum base internal coupling exceeds (delta); allow
[
|c_j-c_j^*|<\delta\ (j=0,\ldots,40),\qquad 0<c_{41}<\delta.
]
This is a full-dimensional open region with all 42 cycle couplings strictly positive. The score variation is at most (8528\delta=533/125000=0.004264), whereas the base-point target-minus-score is below (-20.324). Therefore every point in this region still has target-minus-score (< -20.319736<0).

This is a proof that the **particular 6,153-column dual** fails on an open set of fully connected positive cycle couplings. It is not a global convex-hull theorem and does not establish the existence or nonexistence of a positive physical ensemble.

A new exact-rational/Arb checker and small CI workflow were added:
- `verify_6153_connected_escape_neighborhood.py`
- `.github/workflows/eui-6153-connected-escape-neighborhood.yml`
- output: `evidence/ising_full_fourth_plus_thirty_gapped_open_box_arb_n21.json`

## 4. Manuscript and supplementary-source audit

The repository's default-branch code search for `documentclass`, bibliography, and supplementary-source terms still finds audit notes but no editable tracked TeX/Bib manuscript or separate supplementary source. The public manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, [arXiv:2506.20570v1](https://arxiv.org/abs/2506.20570). Appendix B's normalization and average-Choi-fidelity scope remain tracked in Issue #6; the full QuAIRKit-backed table has not been regenerated. No formal manuscript text or numerical table was changed in this run.

## 5. Changes, blockers, next action

- Updated the 6,153 theory note with the completed continuous escape and the open-box proof.
- Added the exact-rational/Arb neighborhood checker and its CI workflow.
- Added this audit note.
- The finite-pool theorem remains proved only for its exact pinned columns.
- The global physical convex-hull question, exact all-even-principal-minor positive physical ensemble, and operational moment-to-Choi/diamond bridge remain unresolved.

**Next highest-value action:** do not blindly add another pair of columns. Use the complement-folded projection-DPP formulation and the small-(N) reachability track to seek an exact positive measure for the full cycle family, or derive a structural inequality valid for every cyclic coupling. Any new finite-pool dual must be treated as a diagnostic until it survives continuous pricing.
