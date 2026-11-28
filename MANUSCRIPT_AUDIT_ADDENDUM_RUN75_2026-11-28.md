# Manuscript audit addendum — Run 75

Date: 2026-11-28. Repository: tengxianglin/EfficientUnitaryInversion.

## Selection and repository state

Inspected the current mainline through `4451f313a933dedb10c44e12f56de060c1225660`, the recent Run 74 commits, open Issues #7/#5/#6/#3, the Issue #7 discussion through Run 73, the Run 74 theory note, frozen 30-seed input, independent Arb verifier/certificate, and workflow 46128674321.

Run 74 is a genuine constructive advance: a positive mixture of 220 distinct strictly-positive cycle atoms matches all 861 pair moments and 357 quartic coordinates in nine translation orbits, with 6.9816047% mass on four primitive-period-42 seed orbits. It also certifies two quartic misses, so it is not a complete quartic design.

The next full quartic-orbit search benefits from eliminating constraints that are algebraically redundant for every physical atom. This run formalizes that reduction.

## Proved structural reduction

For (Q=R(c)D), the block-bipartite skew generator gives (operatorname{tr}Q=0); together with symmetry and (Q^2=I), this gives 21 eigenvalues of each sign and (det Q=-1).

The characteristic-polynomial identity
[
det(I+tQ)=(1-t^2)^{21}
]
implies
[
sum_{|I|=2r}det Q_{I,I}=(-1)^rinom{21}{r}.
]
The balanced-slice target has exactly the same aggregate at every even order. Hence one weighted aggregate direction per degree is automatic for every normalized ensemble.

Jacobi's complementary-minor identity gives
[
det Q_{I,I}=-det Q_{I^c,I^c}.
]
Therefore only orders 0,2,...,20 need to be imposed; orders 22,...,42 follow exactly.

For cyclic quartets, exact bit-mask enumeration gives 2,670 translation orbits covering 111,930 four-subsets: ten orbits have size 21 and 2,660 have size 42. The global sum rule leaves 2,669 independent quartic orbit coordinates. This is a constraint-count reduction, not a feasibility result.

Normalization caveat: Run 74's 21 pair-distance equations infer weight normalization via the pair sum identity. If a future LP drops a pair equation, it must add an explicit sum-of-weights row. Once normalized, one quartic orbit equation is redundant.

## Reproducibility

- Theory: `THEORY_N42_INVOLUTION_MOMENT_SUM_RULES.md`
- Standard-library verifier: `verify_n42_involution_moment_sum_rules.py`
- Machine certificate: `evidence/n42_involution_moment_sum_rules.json`
- Workflow: `eui-n42-involution-moment-sum-rules.yml`
- Workflow [46129841167](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46129841167): SUCCESS; compilation, exact rational hierarchy, pair/quartet orbit enumeration, deterministic certificate commit, and artifact upload passed.
- Certificate commit: `013fe8afff81f558bac42573389660228d9a02cd`.
- Final theory correction commit: `4451f313a933dedb10c44e12f56de060c1225660`.

## Next highest-value action

Resume the Run 74 quartic cutting-plane search using the exact reduced system:
1. retain all 861 pair coordinates (or 20 pair-orbit rows plus an explicit weight-sum row);
2. retain the nine already matched quartic orbit rows;
3. add the largest unresolved quartic orbit ((0,1,6,7)) as a tenth row;
4. generate new strictly-positive primitive-period-42 seeds and solve the positive LP;
5. freeze any candidate and independently reconstruct its exact-real weights/minors with Arb.

Finite-pool infeasibility remains discovery only. The full continuous cycle-family convex-hull question and the operational channel-distance bridge remain open.

## Manuscript status

The repository still has no editable manuscript TeX/BibTeX or standalone supplementary source. No formal manuscript text was changed in this run. The characteristic-polynomial and Jacobi identities are standard linear algebra; the contribution here is their explicit use to reduce the EUI cyclic moment hierarchy and its exact orbit count.
