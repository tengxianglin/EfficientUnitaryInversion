# Manuscript audit addendum — Run 73

Date: 2026-11-28. Base repository HEAD: \`b286d33b29051aef93de07ae342ae2b0c56d2744d\`.

## Selection

Rechecked the current \`main\` head and recent commits, open Issues #7/#5/#6/#3, Issue #7 comments through Run 72, the cycle-matching reachability theorem, the Run 72 1-factorization theorem/verifier/evidence, the period-two pair-ensemble certificate, the Run 71 sixth-harmonic local-pricing oracle, and the repository manuscript/audit inventory. The repository still contains no editable TeX/BibTeX manuscript or standalone supplementary source; the public paper is not modified by this run.

Run 72 proved a pair-level lower bound \`chi^2 >= 13/28\` for every mixture of bipartite perfect-matching atoms and computed the much larger divergence of one 21-atom 1-factorization. A stronger exact question remained: what is the *best possible full program-label distribution* anywhere in the entire bipartite-matching convex hull, rather than for one design or its pair moments?

## Result

Let \`G=S_21 x S_21\` permute even and odd vertices independently. This group acts transitively on all bipartite perfect matchings and preserves the balanced-slice target. Symmetrizing any matching mixture gives the uniform mixture over all \`21!\` bipartite matchings. Convexity of TV and chi-square implies that this symmetrized law minimizes both divergences; strict convexity makes it the unique chi-square-minimizing output law.

For a balanced label \`S\` with \`k=|S intersect E|\`, exactly \`k!(21-k)!\` bipartite matchings have \`S\` as a transversal. Therefore the symmetrized law is

\`q_*(S)=1/(2^21 * binom(21,k))\`.

Grouping the balanced slice into the 22 even-count orbits gives the exact universal bounds

- \`chi^2(q||u) >= 22*binom(42,21)/2^42 - 1 = 465226670411/274877906944 ~= 1.6924847674490593\`;
- \`TV(q,u) >= 452040940614809/2713482158407680 ~= 0.1665907178398677\`.

The TV positive orbits are \`k=0,...,8,13,...,21\`; negative orbits are \`k=9,10,11,12\`. These improve Run 72's pair-only \`13/28\` chi-square floor and are stronger than the old \`1/5330\` finite-pool TV floor, but their scope is only mixtures of bipartite matching atoms.

The existing cycle-matching reachability theorem proves every cycle-reachable matching atom is bipartite. Hence the bounds apply to the physical matching-only subfamily. The uniform mixture over all \`21!\` bipartite matchings is not claimed to be cycle-reachable; the constants need not be sharp within the smaller physical subset. No conclusion is extended to non-permutation cycle exponentials, Choi distance, or diamond distance.

## Verification

The new dependency-free verifier:
- explicitly enumerates all bipartite matchings and all transversals for \`n=1,...,5\`;
- checks every balanced-label probability against the closed formula;
- independently computes exact rational chi-square and TV for those small cases;
- recomputes the N=42 constants and the exact TV sign partition.

The local run completed successfully. Exact N=42 outputs:
- chi-square: \`465226670411/274877906944\`;
- TV: \`452040940614809/2713482158407680\`.

## Artifacts

- \`THEORY_N42_BIPARTITE_MATCHING_CONVEX_HULL_MINIMAX.md\`
- \`verify_n42_bipartite_matching_minimax.py\`
- \`evidence/n42_bipartite_matching_minimax.json\`
- \`.github/workflows/eui-n42-bipartite-matching-minimax.yml\`

## Next highest-value action

Close the matching-only branch formally in Issue #7, then return to non-permutation \`e^{A(c)}D\` atoms. Enforce all 861 pair constraints while searching new physical columns and price the Run 70/71 harmonic coordinates. The exact matching convex-hull theorem is a clean boundary result, not a solution to the full continuous physical convex-hull question.
