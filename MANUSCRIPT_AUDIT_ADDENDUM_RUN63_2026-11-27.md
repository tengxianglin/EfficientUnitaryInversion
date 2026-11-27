# EUI manuscript/research audit — Run 63 (2026-11-27)

## Repository state inspected

- Starting main HEAD: 9e79ba093fc0df856254f39bfc26fbcb815687ee (Run 62 N=10 full-cycle positive ensemble).
- Recent commit history, open Issues, and latest Issue #7 comments were inspected. Open scientific tracks include #7 (physical cycle-family convex hull), #5 (finite-pool versus full-family gap), #6 (Appendix B normalization), and #3 (classifier/runtime audit). Issue #7 was selected because the new N=10 full-cycle existence theorem makes the remaining N=42 all-moment question the highest-leverage mathematical blocker.
- Run 62's N=10 workflow 45985463935 was independently rechecked through its hosted job list: verifier, Arb certificate generation, and artifact upload all completed successfully.
- The current public manuscript remains arXiv:2506.20570v1. Repository search still found no editable TeX/Bib or separate supplementary source; no manuscript-source edit is claimed.

## New result

Added an all-order adjacent principal-minor incidence theorem for every balanced symmetric involution Q:
\[
\sum_{I\supset S,\ |I|=|S|+1}\det Q_I
=-\sum_{J\subset S,\ |J|=|S|-1}\det Q_J
\]
for every odd subset S. The proof is the coefficient of t^(|S|+1) in the existing principal-minor generating identity.

A Boolean-lattice up/down-operator commutator proves that the incidence map from (k+1)-subsets to k-subsets is surjective for k<N/2. Averaging preimages over D_N proves that the D_N-invariant orbit-incidence matrix has full row rank O_k. This generalizes the rank-147 triple/quartet fact and the 4th/2nd and 6th/4th special cases already in the repository.

For N=42, exact Burnside counts and the rank theorem give:
- order 2: 20 residual pair-orbit coordinates;
- order 4: 1,293 residual quartic-orbit coordinates;
- order 6: 52,911 residual sixth-orbit coordinates;
- all even orders 2 through 20 together: 3,204,236,778 residual orbit coordinates after only these adjacent identities and complement reduction.

This residual count is exact for the specified linear hierarchy only; it is not a claim of algebraic independence or a full physical obstruction. The target satisfies all ten adjacent identities exactly.

## Reproducibility

Added:
- THEORY_ALL_ORDER_PRINCIPAL_MINOR_HIERARCHY_N42.md
- verify_all_order_principal_minor_hierarchy.py
- evidence/all_order_principal_minor_hierarchy_n42.json
- .github/workflows/eui-all-order-principal-minor-hierarchy.yml

Exact regression coverage:
- Burnside versus explicit D_N orbit enumeration for all subset sizes at N=4,6,8,10,12;
- exact rational ranks of all odd-to-even orbit-incidence matrices for odd k<N/2 at those sizes;
- every odd-subset incidence identity checked by exact Fraction determinants for rational balanced involutions at N=4,6,8,10;
- all ten N=42 target identities checked exactly.

Hosted workflow 46003193864 completed SUCCESS on commit de685ca6e2dcf4dc5f83a1038c99cfc1d36f449d. Its steps include compilation, exact recomputation, and frozen-evidence diff check.

## Remaining blockers and next action

- N=42 exact positive physical ensemble matching every even principal minor remains open.
- The 1,314-row second/fourth system is a low-order relaxation only; it does not control the 3.2-billion residual coordinates in the adjacent hierarchy.
- No global physical-family separator and no moment-to-Choi/diamond operational bridge were established.
- Next highest-value action: exploit the complement-folded projection-DPP representation to identify additional structure beyond consecutive incidence identities, or derive a global physical constraint that controls higher-order orbit moments. Do not describe low-order feasibility as full design feasibility.
