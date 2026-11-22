# Manuscript and supplementary-material audit (2026-11-22)

## Source inspected

The repository README identifies this project as the code accompanying
**“Efficient Inversion of Unknown Unitary Operations with Structured
Hamiltonians.”** The current repository tree contains no manuscript
`.tex`, `.bib`, `.pdf`, or separately versioned supplementary source.
The accessible manuscript and appendices are the arXiv HTML version:

- https://arxiv.org/html/2506.20570v1
- Title: *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*
- Authors: Yin Mo, Tengxiang Lin, Xin Wang
- Version date shown in the HTML: 25 June 2025

## Claims and assumptions relevant to the current EUI evidence

### Appendix A: exact structured inversion

- Theorem A1 states a one-query, ancilla-free inverse criterion: a Pauli
  operator (V) must anticommute with every Pauli term in the known support
  (mathcal S), giving (VUV^dagger=U^dagger).
- Corollary A2 restates the criterion as the absence of an odd-cardinality
  subset of support terms whose product is proportional to identity.
- Theorem A3 gives a (2^L-1)-query recurrence for pairwise-commuting support
  terms covered by an anticommuting set (mathcal W).
- Theorem A4 extends the recurrence to a commuting decomposition
  (hat{mathcal S}_0,hat{mathcal S}_1).

These are exact protocol statements under a known Pauli support and their
stated commutation/anticommutation assumptions. The present 83-column
moment-dual result does not challenge those algebraic theorems.

### Appendix B: robustness evidence

The appendix models support mismatch as

[
H=\sum_{P\in\mathcal S}\alpha_P P
+\delta\sum_{P\in\mathcal S'}\beta_P P,
]

with (mathcal S') the complement of the ideal support and (delta)
defined through an (L^1)-coefficient ratio. It reports 10,000 random
instances and average Choi-state fidelities for several comb protocols and
noise levels.

This is finite Monte Carlo evidence for average Choi fidelity. The inspected
appendix does not provide a uniform worst-case channel-distance theorem, nor
a theorem connecting the moment residuals in the current Ising/path analysis
to the operational Choi fidelity of the inverse circuit.

## Consequence for the current research claim

The new dual certificate proves a finite-pool lower bound for 1,739 normalized
moment constraints. It is **not** an operational inversion-error bound and
does not imply a Choi-fidelity statement. The manuscript-level bridge remains
open:

1. Specify the exact random/physical ensemble and the map from its moment
   constraints to the implemented inverse channel.
2. Derive an explicit inequality from the relevant moment residuals to a
   Choi-state trace distance, diamond norm, or fidelity loss, with all
   dimension and normalization factors.
3. Separate average-over-ensemble guarantees from worst-case-over-Hamiltonian
   guarantees.
4. If no such bridge is available, present the moment-dual problem as a
   distinct auxiliary theorem rather than using it to support the Appendix B
   robustness claim.

This audit is deliberately limited to arXiv v1 and the current repository
contents; it does not assert that no later manuscript version exists elsewhere.
