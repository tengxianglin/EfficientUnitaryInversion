# EUI manuscript and evidence audit — run 15 (2026-11-25)

## Manuscript inspected

The public manuscript located for this project is [arXiv:2506.20570v1, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*](https://arxiv.org/html/2506.20570v1), dated 2025-06-25. The HTML includes Appendices A–E; Appendix B is the robustness experiment section.

The manuscript's main text describes the robustness error as \(O(\delta^2)\) in **average fidelity**. Appendix B states that it generates 10,000 random unitaries with the in-support and out-of-support Pauli coefficients sampled independently from standard normal distributions, then reports average Choi-state fidelity at four values of \(\delta\). This is finite-sample, distribution-dependent average evidence. It is not a worst-case-over-Hamiltonians statement, a worst-case-over-inputs statement, or a channel diamond-norm guarantee.

The EUI repository's current joint-parity diamond-converse notes concern a separate fixed six-query architecture and a conditional all-moment ensemble hypothesis. They must not be conflated with the broader robustness experiment in Appendix B.

## Repository manuscript-source audit

The default-branch code search for documentclass, bibliography, and supplementary-manuscript terms found audit notes but no tracked TeX/Bib manuscript source or separate supplementary source. The repository therefore still does not contain an editable formal manuscript body; this run updates theory/evidence notes only and does not claim a manuscript-text revision.

## New certified finite-pool result

The 6,135-column full-second-/fourth-order obstruction is independently Arb-certified in [the committed certificate](evidence/ising_full_fourth_plus_twelve_gapped_arb_n21.json), produced by [workflow 45519860433](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45519860433) and committed at [f38a793](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f38a7933b954abc454315c5b25a21141cdb3c97c).

The exact pool has 22 base atoms, 6,101 fractional single-open-path grid atoms, and 12 exact-rational gapped paths. The feature system is complete at second and fourth order: 21 second-order distance coordinates and all 1,440 fourth-order dihedral orbits. The rationalized 101-term dual has exact scaled \(\ell_1\) norm 1 and full-coordinate \(\ell_1\) norm 533. The minimum stored Arb lower endpoint is greater than \(23879/100000\), giving
\[
\|b-Ap\|_\infty>\frac{23879}{53300000},\qquad
\operatorname{TV}(w_p,u_{\rm bal})>\frac{23879}{106600000}
\]
for every mixture on this exact finite pool. The TV conclusion concerns the balanced program-label distribution / dephased register, not Choi or diamond distance.

The independent verifier now selects the sharper rational floor automatically (commit [fbfa21c](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fbfa21c63b0adba7e3f08de0b03f9d9574029e1b)); its full reproducibility rerun is pending.

## Continuous-family test staged

A deterministic connected/multi-segment search, independent 256-bit Arb escape verifier, and CI workflow are committed:
- [Search](search_ising_full_fourth_plus_twelve_gapped_n21.py)
- [Arb verifier](verify_ising_full_fourth_plus_twelve_gapped_escape_arb_n21.py)
- [Workflow](.github/workflows/eui-full-fourth-plus-twelve-gapped-search-n21.yml)

These scripts price the new 101-term 6,135-column dual. Search output alone is not evidence of escape or global separation; any candidate must be frozen as exact rational couplings and pass independent Arb orthogonality, determinant-one, and exact-dual pricing checks.

## Remaining paper-level blockers

1. Construct an exact positive physical ensemble satisfying every even-principal-minor condition at \(n=21\), or prove a global obstruction for the full allowed physical family.
2. Establish a rigorous, correctly quantified bridge from program-mass/moment discrepancy to Choi-state trace distance or channel diamond error. The present finite-pool TV theorem is not that bridge.
3. Obtain the editable manuscript and supplement sources before claiming formal paper-body revisions.
