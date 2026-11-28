# Manuscript audit addendum — Run 77

Date: 2026-11-28. Repository: tengxianglin/EfficientUnitaryInversion.

## State inspected

- Default branch: main.
- HEAD before this run: 9a569471b508168e0ebb959aab7534f98c3d8fa5 (Run 76 D42 workflow commit).
- Recent commits: Run 75 hierarchy identities and Run 76 D42 orbit reduction.
- Open issues: #7 (physical convex-hull membership), #5 (finite-pool versus full-family gap), #6 (Appendix B normalization), #3 (type-1.2 classifier audit).
- Read Issue #7 and its Run 72–76 discussion, the Run 74 frozen positive ensemble/theory, the Run 76 D42 proof/verifier/workflow, the Run 66 vertex-sign gauge/Plucker note, and README.
- Code search for manuscript TeX commands found only audit notes; no editable manuscript or standalone supplementary source was found. No manuscript edit is claimed.

## Highest-leverage unresolved point

Issue #7 is still the central scientific question: membership of the complete balanced-slice even-principal-minor target in the closed convex hull of the fixed 42-cycle exponential family with real couplings.

Run 76 proved D42 equivariance but did not identify the residual sign-gauge sectors. Run 66 stated the vertex-sign gauge covariance but did not classify its orbits on the cycle. This matters because the current Run 74 constructive ensemble uses strictly-positive couplings, whereas Issue #7 still quantifies over all real couplings.

## Run 77 result — exact Z2 holonomy reduction

For S_epsilon=diag(epsilon_j), define c_epsilon,j=epsilon_j epsilon_(j+1)c_j. Then
\[
Q(c^\epsilon)=S_\epsilon Q(c)S_\epsilon,
\]
so every principal minor at every order is exactly unchanged.

For fixed coupling magnitudes:
- if at least one edge coupling is zero, the support graph is a forest and all edge signs can be gauged positive;
- if all 42 couplings are nonzero, there are exactly two gauge classes, distinguished by h(c)=product_j sign(c_j).

A canonical representative is:
- c_j=|c_j| for j=0,...,40;
- c_41=h(c)|c_41| for full support.

Since the Run 76 D42 action permutes the coupling entries, it preserves h(c). The real-coupling closed convex-hull problem therefore reduces exactly to two D42-symmetrized sectors:
\[
(0,\infty)^{42}
\quad\text{and}\quad
(0,\infty)^{41}\times(-\infty,0).
\]
Vectors with zero couplings add no third sector: their canonical nonnegative representatives are limits of strictly-positive vectors, and v(c) is continuous.

This is an all-N algebraic theorem for even cycles, not a numerical observation. It is a reduction, not a feasibility or no-go result.

## Verification

- New theory: THEORY_N42_CYCLE_Z2_HOLONOMY_GAUGE_REDUCTION.md
- Standard-library verifier: verify_n42_cycle_z2_holonomy_gauge.py
- Machine certificate: evidence/n42_cycle_z2_holonomy_gauge.json
- Workflow: .github/workflows/eui-n42-cycle-z2-holonomy-gauge.yml
- Exhaustive signed/zero edge patterns:
  - N=4: 81 patterns, 17 gauge classes over all supports;
  - N=6: 729 patterns, 65 classes;
  - N=8: 6,561 patterns, 257 classes;
  - N=10: 59,049 patterns, 1,025 classes.
- For every fixed support, exhaustive enumeration found one gauge orbit unless the support is the full cycle, where it found exactly two.
- Combined gauge/D_N orbit counts for sign/zero patterns were 7, 14, 31, 79 for N=4,6,8,10.
- N=42 deterministic smoke check: 4,096 patterns, seed 20261128, passed.
- Separate local binary64 matrix-exponential sanity check: all principal minors for three random vectors at each N=4,6,8,10 were unchanged under random vertex gauges; maximum reported discrepancy 0.0. This is implementation evidence only.

The finite verifier supports the algebraic proof; the proof itself supplies the all-N result.

## Consequence for the next experiment

Do not describe the positive-coupling Run 74 pool as covering the real-coupling family. For a full-family cutting-plane or separator audit, append D42-averaged negative-holonomy columns with c_0,...,c_40>0 and c_41<0. Keep the 21 pair constraints and complete quartic orbit system. A separator must be priced on both sectors; finite-pool infeasibility remains non-global evidence.

If the physical model is explicitly restricted to c_j>0, the negative sector is outside the model and the positive search is sufficient. Issue #7 currently states c in R^42, so both sectors are required for a real-domain converse.

## Scope limitations

- No complete quartic or all-even-moment physical ensemble was constructed.
- No global separator was proved.
- No program-label TV to Choi trace-distance or channel diamond-distance bridge was added.
- No formal manuscript source was present, so only theory, verification, and audit records were changed.
- No model-routing control was available to select GPT-6.1-sol Max; no model switch is claimed.
