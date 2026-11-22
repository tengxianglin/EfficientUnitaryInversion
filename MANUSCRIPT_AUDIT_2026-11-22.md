# Manuscript and supplementary-material audit (2026-11-22)

## Source inspected

The README identifies the project as accompanying **“Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians.”** The current repository tree contains no manuscript `.tex`, `.bib`, `.pdf`, or separately versioned supplementary source. The accessible manuscript and appendices are the arXiv HTML version:

- https://arxiv.org/html/2506.20570v1
- *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*
- Yin Mo, Tengxiang Lin, Xin Wang
- Version date shown in the HTML: 25 June 2025

This audit is limited to that version and the repository state inspected on 2026-11-22; it does not assert that no later manuscript exists elsewhere.

## Claims and assumptions relevant to EUI

### Appendix A: exact structured inversion

- Theorem A1 gives a one-query, ancilla-free inverse criterion: a Pauli operator (V) must anticommute with every Pauli term in the known support (mathcal S), yielding (VUV^dagger=U^dagger).
- Corollary A2 restates the criterion as the absence of an odd-cardinality subset of support terms whose product is proportional to identity.
- Theorem A3 gives a ((2^L-1))-query recurrence for pairwise-commuting support terms covered by an anticommuting set (mathcal W).
- Theorem A4 extends the recurrence to a commuting decomposition ((hat{mathcal S}_0,hat{mathcal S}_1)).

These are exact protocol statements under known Pauli support and their stated commutation/anticommutation assumptions. The finite moment-dual computations below neither prove nor refute those algebraic theorems.

### Appendix B: robustness evidence

Appendix B models support mismatch as
[
H=sum_{Pinmathcal S}alpha_P P
+deltasum_{Pinmathcal S'}eta_P P,
]
where (mathcal S') is the complement of the ideal support and (delta) is defined through an (L^1)-coefficient ratio. It reports 10,000 random instances and average Choi-state fidelities for several comb protocols and noise levels.

This is finite Monte Carlo evidence for average Choi fidelity. The inspected appendix does not provide a uniform worst-case channel-distance theorem, nor a theorem connecting the moment residuals in the current Ising/path analysis to the operational Choi fidelity of an implemented inverse circuit.

## Current finite-pool moment evidence (2026-11-22)

The latest certified finite minimax problem uses 103 pinned legal 42-site path generators and 1,762 normalized rows:

- 1,461 complete second-/fourth-order rows;
- 256 screened sixth-order rows;
- 38 additional sixth-order rows;
- 7 selected eighth-order rows.

Its binary64 HiGHS discovery objective is (0.336849522971994). A separate exact-rational dual certificate, checked with 128-bit Arb against all 103 columns, proves
[
min_{pinDelta_{103}}|Ap-y|_infty
ge
rac{828503567612290605891211277}
{2459565876500878872300000000}
approx 0.3368495129681047
>rac13.
]
The certificate has exact (|z|_1=1), slack (delta=10^{-8}), and strictly negative Arb upper bound for every pinned column inequality. See `THEORY_103COL_38PROBE_DUAL_OBSTRUCTION.md` and `evidence/38probe_103col_dual_certificate_n21.json`.

The dual was then priced against all 1,538 unused columns in the frozen 1,641-column canonical path pool. The binary64 screen found 40 positive reduced-cost columns; the ten highest were independently recomputed with 128-bit Arb and all ten had strictly positive interval lower endpoints. This invalidates the 103-column dual inequalities for an expanded pool containing any of those columns; it does **not** prove an improved ensemble. The frozen evidence is in `evidence/38probe_103col_dual_pricing_screen_n21.json` and `evidence/38probe_103col_dual_pricing_arb_n21.json`.

A 113-column reweighting and candidate-verification workflow has been added. Until its LP and Arb run complete, no 113-column candidate claim is made. Even if its selected rows and a sixth-order prefix pass, the complete sixth-order maximum and all eighth-/higher-order moments remain separate obligations.

## Consequence for manuscript claims

The current dual certificate is a finite-pool minimax theorem, not an operational inversion-error bound. It does not imply a Choi-fidelity statement. The manuscript-level bridge remains open:

1. Specify the exact random/physical ensemble and the map from its moment constraints to the implemented inverse channel.
2. Derive an explicit inequality from the relevant moment residuals to a Choi-state trace distance, diamond norm, or fidelity loss, with all dimension and normalization factors.
3. Separate average-over-ensemble guarantees from worst-case-over-Hamiltonian guarantees.
4. If no such bridge is available, present the moment-dual result as a distinct auxiliary theorem rather than using it to support Appendix B's robustness claim.

The 103-column lower bound is restricted to its pinned rows and columns. The ten Arb-positive priced columns show why it must not be presented as a lower bound over the full canonical pool, let alone over all physical generators.
