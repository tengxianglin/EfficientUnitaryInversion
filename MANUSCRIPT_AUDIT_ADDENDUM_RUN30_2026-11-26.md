# EUI manuscript/research audit — Run 30 (2026-11-26)

## Repository state inspected

- Repository: tengxianglin/EfficientUnitaryInversion
- Default branch: main
- HEAD before this run's changes: 9de5eb293879deac94450a83feb22fb24168aa5f
- Latest inspected commits concerned the exact SO(42) perfect-matching ensemble and the exact commutant exclusion of one matching atom.
- Open research issues inspected: #7 (physical reachability / convex hull), #5 (finite-pool obstruction and full-family gap), #6 (Appendix B noise normalization), and #3 (type-1.2 classifier audit).
- Issue #7's previous exact evidence: one matching atom is unreachable by a full-rank modular commutant certificate; small-N commutant nullities were 0/3 at N=4, 0/15 at N=6, and 8/105 at N=8. The previous successful workflow was 45660576732.

## Manuscript/source audit

Default-branch code search for documentclass and Appendix B terms found audit notes but no editable TeX/Bib manuscript or separate supplementary source. The accessible paper remains Yin Mo, Tengxiang Lin, Xin Wang, “Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians,” arXiv:2506.20570v1. The repository's Issue #6 records the Appendix B raw-Gaussian versus per-instance L1-normalized coefficient distinction and the successful normalization regression. The full QuAIRKit Choi-fidelity table has not been regenerated.

## Scientific progress selected for this run

Two exact advances were made on Issue #7:

1. A graph-support theorem classifies the possible form of any perfect-matching atom that can be a fixed 42-cycle exponential. Such an atom must be bipartite; with a nonempty zero-edge set, it must reverse even contiguous path components. This gives an upper bound of 4,194,324 reachable matching atoms out of 41!!, i.e. at most 3.1986e-19 of the uniform matching support. No mixture of reachable matching atoms can reproduce the target, because same-parity pair minors vanish on all such atoms while the target is -1/41 in Q=RD coordinates.
2. Exact physical single-atom constructions were found for the complete balanced-slice even-principal-minor target at N=4 and N=6. Alternating cycle couplings yield explicit symmetric involutions Q=exp(A(c))D. Every even principal minor was checked exactly. This proves small-size physical feasibility and demonstrates that excluding matching atoms does not settle the convex hull of general cycle exponentials.

The N=4 and N=6 constructions do not prove N=42 feasibility. The full N=42 physical convex-hull question remains open.

## Reproducibility artifacts added in this run

- THEORY_CYCLE_MATCHING_ATOM_REACHABILITY_N42.md
- verify_cycle_matching_atom_reachability.py
- evidence/cycle_matching_atom_reachability_n21.json
- .github/workflows/eui-cycle-matching-atom-reachability.yml
- THEORY_PHYSICAL_CYCLE_ENSEMBLE_N4_N6.md
- verify_physical_cycle_ensemble_n4_n6.py
- evidence/physical_cycle_ensemble_n4_n6.json
- .github/workflows/eui-physical-cycle-ensemble-n4-n6.yml

## Evidence classes

- Proved analytically: the 42-cycle matching-atom parity/path-reversal theorem and its support-count bound.
- Exact symbolic verification: all even principal minors of the N=4 and N=6 physical constructions, plus their orthogonality, determinant, and chiral identities.
- Exhaustive finite checks: exact commutant-rank formula for all matchings at N=4,6,8; cut-set construction checks at N=4,6,8,10; fixed-point-free dihedral classification checks at N=6,10,42.
- Not proved: N=42 physical convex-hull membership or a global separating inequality; operational conversion to Choi/diamond distance.

## Next highest-value action

Use the N=4/N=6 exact constructions as a guide to derive the full N=42 parity-block spectral constraints. First test whether the complete second-order target can be matched by a positive measure on the 42-cycle family; then extend to fourth and higher even principal-minor orders. Do not infer N=42 feasibility or infeasibility from the small-N constructions.
