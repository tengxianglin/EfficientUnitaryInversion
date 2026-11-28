# Manuscript audit addendum — Run 76

Date: 2026-11-28. Repository: tengxianglin/EfficientUnitaryInversion.

## Repository and manuscript inspection

Inspected main HEAD \`ba0ed6059e733a2cdf90ceb720ea1e79867f43df\`, the recent Run 74–75 commits, open Issues #3/#5/#6/#7, the Issue #7 discussion through the Run 74–75 update, the Run 74 frozen nonperiodic ensemble and Arb certificate, the Run 75 involution hierarchy note and exact verifier, and the recent GitHub Actions inventory. The latest committed Run 75 workflow (46129841167) reports SUCCESS.

The public preprint record inspected is arXiv:2506.20570v1, submitted 2025-06-25. The repository root/README contains code and audit records but no editable manuscript TeX/BibTeX or standalone supplementary source; no formal manuscript edit is claimed.

## Highest-leverage issue

Issue #7 remains the central unresolved question: whether the complete balanced-slice even-principal-minor target lies in the closed convex hull of the fixed-cycle physical feature family. Run 74 gives a certified partial positive ensemble; Run 75 removes aggregate and complementary-order redundancies. The next search should exploit every exact symmetry of the physical feature map before spending resources on new candidate atoms.

## Run 76 — proved dihedral symmetry reduction

For rotations \(r_s(i)=i+s\) and reflection \(\rho(i)=-i\), the coupling transformations are
\[
c^{(s)}_j=c_{j-s},\qquad c^{(\rho)}_j=c_{-j-1}.
\]
The exact matrix identities are
\[
P_{r_s}Q(c)P_{r_s}^T=(-1)^sQ(c^{(s)}),
\qquad
P_\rho Q(c)P_\rho^T=DQ(c^{(\rho)})D.
\]
The first global sign disappears from every even-order principal minor; the diagonal \(D\)-conjugation also leaves every principal minor unchanged. Both coupling transformations are permutations, so strict positivity is preserved. Therefore the even-minor feature family is \(D_{42}\)-equivariant, and any feasible probability measure can be averaged over the 84-element dihedral group without changing its target moments.

Exact bit-mask enumeration gives:
- pairs: 21 \(D_{42}\) orbits, covering all 861 pairs;
- quartets: 1,440 \(D_{42}\) orbits, with sizes \(10\times21\), \(200\times42\), \(1,230\times84\), covering all 111,930 quartets;
- the 2,670 cyclic quartic orbits split into 210 reflection-stable orbits and 1,230 reflection pairs;
- after the Run 75 global quartic sum rule, at most 1,439 independent quartic orbit coordinates remain.

This reduces the known quartic search coordinates by 1,230 (about 46.1%) relative to the cyclic-only formulation. It is a symmetry reduction, not a feasibility theorem and not a claim that the remaining feature matrix has full row rank.

## Verification

- Standard-library verifier: \`verify_n42_dihedral_quartic_orbits.py\`
- Machine certificate: \`evidence/n42_dihedral_quartic_orbits.json\`
- Workflow: \`eui-n42-dihedral-quartic-orbits.yml\`
- Local run: \`py_compile\` passed; exact enumeration passed in 0.85 s.
- Pair orbit histogram: \`{21: 1, 42: 20}\`.
- Quartic orbit histogram: \`{21: 10, 42: 200, 84: 1230}\`.
- Representative hashes: pair \`f619fa393fbab48168e426bab53d1e63189b807312cf860b082acd8afdfed6bf\`; quartic \`54772a1b434e848b065cd53807a4f8733cf3afdc83b60d67680f2a208f80b121\`.
- Independent floating sanity check on one random strictly-positive coupling vector gave infinity-norm defects \(6.42\times10^{-15}\) for the rotation identity and \(4.57\times10^{-15}\) for the reflection/gauge identity. These are implementation checks only; the identities are proved algebraically above.

## Scope and next action

The full physical convex-hull question, complete quartic feasibility, all-even-moment feasibility, a global separator, and the program-label-to-Choi/diamond operational bridge remain unresolved. The next search should parameterize one \(D_{42}\)-averaged column per positive seed, use the 1,440 quartic orbit representatives, retain all 21 pair orbit constraints, and apply exact interval verification to any frozen positive support. A finite candidate-pool failure remains non-global evidence.

The general group-averaging principle is standard. The EUI-specific contribution is the exact gauged reflection identity that preserves the strictly-positive cycle family and the resulting certified orbit reduction.
