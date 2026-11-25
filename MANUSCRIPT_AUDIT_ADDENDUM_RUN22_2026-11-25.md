# Manuscript/repository audit addendum — Run 22 (2026-11-25)

## Repository state inspected

Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.

The recursive Git tree was read without truncation. The current repository contains the 201-column LP, exact rational dual, program-mass TV post-processing, the 201-column reoptimizer/verifier, and the new continuous torus-pricing scripts/workflow. No editable manuscript or supplementary source files (`.tex`, `.bib`, `.pdf`, `.doc`, `.docx`) are present in the repository.

Recent work relevant to this run includes:
- `6243c9a`: 201-column binary64 LP diagnostic;
- `90e4b51`: initial 201-column rational/Arb verifier and workflow;
- `996fe98`: 201-column rational dual certificate;
- `7ba2472`: exact program-mass TV evidence;
- `41c71e8`, `11339e64`, `431e5eab`, `c316460`, `8706d4f`: TV verifier/workflow and corrections;
- `9006ed9`, `69c4262`, `6370183`, `3ee151c`: 201-column continuous torus discovery, Arb verifier, and workflow;
- `b9e3b8a`: 201-column theory note.

Open issues inspected:
- #5: finite-pool minimax obstruction and full-family EUI gap (updated with the 201-column discovery and theorem);
- #6: Appendix B per-instance (L_1) noise normalization (the code normalization has been unified; full Appendix B Monte Carlo re-generation remains open);
- #3: type-1.2 Hamiltonian classification correctness audit.

## New proved finite-pool result

The 201-column pool contains 183 canonical columns, nine earlier exact-rational gapped paths, and nine uniform open-path columns. The last column (label 1658) is the exact finite-time escape of the 200-column dual:
[
c_0=\cdots=c_{40}=t_*,\quad c_{41}=0,\quad
t_* = \frac{133290887822869233787}{200000000000000}>0.
]
All 41 internal couplings are strictly positive.

The fixed 2,113-row design is:
- 21 complete second-order rows;
- 1,440 complete fourth-order dihedral-orbit rows;
- 645 selected/cut sixth-order rows;
- 7 selected eighth-order rows.

The floating LP discovery returned objective 0.39283056306574515, recomputed maximum 0.39283056309822917, primal-dual gap (1.291189377639057\times10^{-12}), and support size 62. This was only discovery.

The exact rationalized dual has
[
\|z\|_1=\frac{4611686018393898135}{4611686018427387904}<1,
\quad
\lambda+z^Tb=\frac{1811611215307209993}{4611686018427387904},
\quad
\delta=10^{-8}.
]
Independent 128-bit Arb checked all 201 column inequalities. The maximum shifted-column upper endpoint is (-8.902968402615641\times10^{-9}). Consequently,
[
\boxed{
\min_{p\in\Delta_{201}}\|b-Ap\|_\infty
\ge\frac{707660612964980394033641}{1801439850948198400000000}
=0.3928305530670364\ldots>\frac13.
}
]

The exact bounded-character coefficient norm is
[
M=\frac{92530165274588371116657}{23058430092136939520},
]
yielding the exact program-mass TV lower bound
[
\boxed{
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{707660612964980394033641}{14457838324154432986977656250}
=4.8946502035695432\times10^{-5}.
}
]
This is for the balanced program-label distribution (equivalently the dephased label-register trace distance) in one selected parity sector. It is not a Choi-state or channel diamond-distance lower bound.

## Reproducibility

- 201-column LP: [45598370006](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45598370006), success.
- 201-column rational dual and Arb certificate: [45599105012](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45599105012), success.
- 201-column exact TV corollary: [45599717698](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45599717698), success.
- 201-column continuous torus pricing: [45600250848](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45600250848), running at the time of this audit.

The theory statement and limitations are recorded in `THEORY_201COL_MIXED_ORDER_RATIONAL_DUAL_AUDIT_N21.md`.

## Manuscript audit

The public manuscript remains arXiv:2506.20570v1. Appendix B's Gaussian-noise notation must distinguish raw Gaussian coefficients from the per-instance (L_1)-normalized coefficients used in the code; this is tracked in Issue #6. The five robustness protocols now share a single normalization helper, but their full QuAIRKit/Choi-fidelity tables have not yet been regenerated in this environment.

No editable paper/supplement source was found in the repository, so no claim is made that the formal manuscript was edited.

## What remains unresolved

1. The new 201-column dual still needs its own continuous physical pricing. A positive torus interval would imply a finite positive equal-coupling path by the dense-ray theorem; an explicit finite-time Arb certificate is preferable.
2. The complete all-even-principal-minor positive-ensemble problem at (n=21) remains open.
3. Sixth/eighth-order rows in this 2,113-row design are selected/cut, not complete.
4. No full continuous-family global converse has been established.
5. No valid bridge from the program-mass TV witness to Choi or diamond distance has been established.
6. Full Appendix B numerical regeneration still requires the pinned QuAIRKit runtime.

## Next highest-value action

Complete 201-dual continuous torus pricing. If a positive candidate is found, certify its exact phase vector with Arb, then search for and certify an explicit finite positive uniform-path time. Append that path as column 202 and rerun the fixed 2,113-row LP. If the torus search fails, treat that only as a bounded-search result, not as a global separation proof.
