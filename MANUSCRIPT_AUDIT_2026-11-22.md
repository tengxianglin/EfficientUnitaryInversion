# Manuscript and supplementary-material audit (2026-11-22)

## Source inspected

The README identifies the project as accompanying **“Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians.”** The current repository tree contains no manuscript .tex, .bib, .pdf, or separately versioned supplementary source. The accessible manuscript and appendices are the arXiv HTML version:

- https://arxiv.org/html/2506.20570v1
- *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*
- Yin Mo, Tengxiang Lin, Xin Wang
- Version date shown in the HTML: 25 June 2025

This audit is limited to that version and the repository state inspected on 2026-11-22; it does not assert that no later manuscript exists elsewhere.

## Claims and assumptions relevant to EUI

### Appendix A: exact structured inversion

- Theorem A1 gives a one-query, ancilla-free inverse criterion: a Pauli operator V must anticommute with every Pauli term in the known support S, yielding VUV†=U†.
- Corollary A2 restates the criterion as the absence of an odd-cardinality subset of support terms whose product is proportional to identity.
- Theorem A3 gives a (2^L-1)-query recurrence for pairwise-commuting support terms covered by an anticommuting set W.
- Theorem A4 extends the recurrence to a commuting decomposition (S-hat_0,S-hat_1).

These are exact protocol statements under known Pauli support and their stated commutation/anticommutation assumptions. The finite moment-dual computations below neither prove nor refute those algebraic theorems.

### Appendix B: robustness evidence

Appendix B models support mismatch as
\[
H=\sum_{P\in S}\alpha_P P
+\delta\sum_{P\in S'}\beta_P P,
\]
where S' is the complement of the ideal support and delta is defined through an L1-coefficient ratio. It reports 10,000 random instances and average Choi-state fidelities for several comb protocols and noise levels.

This is finite Monte Carlo evidence for average Choi fidelity. The inspected appendix does not provide a uniform worst-case channel-distance theorem, nor a theorem connecting the moment residuals in the current Ising/path analysis to the operational Choi fidelity of an implemented inverse circuit.

## Current finite-pool moment evidence (2026-11-22)

### Earlier 103-column result and its escape

A 128-bit Arb dual certificate for a frozen 103-column / 1,762-row pool proved a lower bound 0.3368495129681047... > 1/3. That theorem was restricted to those 103 columns and rows. Dual pricing then found ten additional canonical physical columns with strictly positive Arb reduced-cost intervals, so the 103-column dual did not separate the expanded pool. This history is recorded in THEORY_103COL_38PROBE_DUAL_OBSTRUCTION.md and its evidence files.

### Current 113-column / 55-separator result

The latest finite LP uses 113 pinned legal 42-site path generators and 1,779 normalized rows:

- 1,461 second-/fourth-order rows;
- 311 sixth-order rows (256 screened, 38 parent probes, eight separators from the rejected 38-probe candidate, one prefix separator from the rejected 46-probe candidate, and eight separators from the rejected 47-probe candidate);
- seven selected eighth-order rows.

Its binary64 HiGHS objective is 0.36575443678254027... > 1/3. A separate exact-rational dual certificate, independently checked with 128-bit Arb against all 113 physical columns, proves
\[
\min_{p\in\Delta_{113}}\|Ap-y\|_\infty
\ge
\frac{4118028861881514868548001}
{11258999068426240000000000}
=0.3657544366825429...
>\frac13.
\]
The exact dual has ||z||_1=1152921504606844607/1152921504606846976<1, slack delta=10^-10, and a strictly negative Arb upper endpoint for every pinned column inequality (maximum upper endpoint approximately -8.24778e-11). See THEORY_55PROBE_113COL_DUAL_OBSTRUCTION.md and evidence/55probe_113col_dual_certificate_n21.json.

This rejects every convex mixture of the pinned 113 columns for this exact 1,779-row constraint set. It does not reject the remaining 1,528 canonical columns or all physical generators. The 311 sixth-order rows are not the complete set of 63,133 sixth-order dihedral orbits. The LP did not produce an admissible 1/3-candidate.

The 128-bit Arb pricing workflow has now screened all 1,528 unused canonical columns in the frozen 1,641-column pool. The binary64 screen found 66 positive reduced-cost candidates; the ten highest were independently checked with 128-bit Arb and all ten had strictly positive interval lower endpoints (columns 1191, 916, 700, 974, 127, 889, 910, 107, 902, 355). This invalidates the 113-column separator for any expanded pool containing one of those columns, but does not prove an improved ensemble. See evidence/55probe_113col_dual_pricing_screen_n21.json and evidence/55probe_113col_dual_pricing_arb_n21.json. The 123-column reoptimization over the same 1,779 rows has now been completed. Its binary64 HiGHS objective is 0.3511700099912447, above 1/3, so it produces no admissible candidate. A 128-bit Arb rational dual certificate verifies all 123 column inequalities and proves
\[
\min_{p\in\Delta_{123}}\|Ap-y\|_\infty
\ge
\frac{202435727565723844694298279}
{576460752305701721000000000}
=0.35117000898331857\ldots
>\frac13.
\]
The exact dual has \(\|z\|_1=1\), uses slack \(10^{-9}\), and the maximum Arb upper endpoint of \(A^Tz+\lambda-\delta\) over the 123 columns is below \(-2.60568\times10^{-10}\). This is a theorem for the pinned 123-column pool and 1,779 rows only. See THEORY_55PROBE_123COL_DUAL_OBSTRUCTION.md and evidence/55probe_123col_dual_certificate_n21.json.

Workflow 45018694807 has now screened all 1,518 unused columns in the frozen 1,641-column canonical pool. The binary64 screen found 34 positive reduced-cost candidates; the ten highest were independently recomputed with 128-bit Arb, and all ten intervals are strictly positive: columns 1610, 1640, 367, 433, 388, 253, 368, 87, 743, and 69. The largest Arb pricing score is 10.7288893003344779... (column 1610), and the second is 2.5544859328709926... (column 1640). These are certified escapes of the 123-column dual, not yet an improved ensemble. A 133-column reoptimization using these ten columns is running in workflow 45018951320. Any nonpositive binary64 score is only a screen result; it is not a rigorous all-column exclusion.

## Consequence for manuscript claims

The finite-pool dual certificate is a minimax theorem for a pinned finite set of physical generators and moment rows, not an operational inversion-error bound. It does not imply a Choi-fidelity statement. The manuscript-level bridge remains open:

1. Specify the exact random/physical ensemble and the map from its moment constraints to the implemented inverse channel.
2. Derive an explicit inequality from the relevant moment residuals to a Choi-state trace distance, diamond norm, or fidelity loss, with all dimension and normalization factors.
3. Separate average-over-ensemble guarantees from worst-case-over-Hamiltonian guarantees.
4. If no such bridge is available, present the moment-dual result as a distinct auxiliary theorem rather than using it to support Appendix B's robustness claim.

The 113-column lower bound is restricted to its pinned rows and columns. It must not be presented as a lower bound over the full canonical pool or over all physical generators.
