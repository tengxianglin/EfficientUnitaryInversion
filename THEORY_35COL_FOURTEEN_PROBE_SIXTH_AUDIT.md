# Complete sixth-order audit of the 35-column fourteen-probe candidate

## Exact input

- Candidate SHA256: `ac789d6fa678a4759c13d3d5588253e57d63e5a448946bdd9bb915369d401d80`
- LP transcript SHA256: `7ddda3942e1e2212bb9af38c3b6bc9b97f25e186298bdc93653258b1a1536eb3`
- Parent 35-column candidate SHA256: `ced62e0ef71f384056cd535d2294f3af52875c75497df7a1815bf8d3c0ca135e`
- Three pinned Arb prefix Git blob SHA1s: `6604c6727b075b79ceca438b01faadbbb0ebbd19`, `4827a61b30abdfdab2675eac6df557e71081294e`, `6b655f83d87b9ea24f9394355ef1aa8c4633136e`
- Frozen seed-pool content SHA256: `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`
- Exact support: 35 positive rational probabilities summing to one
- Interval backend: python-flint 0.8.0 / Arb, 128-bit precision

The candidate has passed Arb checks on all 1,461 low-order rows, 270 selected sixth-order rows, and seven selected eighth-order rows. These are selected-row statements only.

## Complete sixth-order question

For every six-subset (I\subset\mathbb Z_{42}), the verifier computes

\[
q_I=\sum_{j=1}^{35}p_j\frac{1}{|O(I)|}
\sum_{J\in O(I)}\det R_j[J,J],
\qquad
t_I=(-1)^{v(I)+3}\frac{\binom{21}{3}}{\binom{42}{6}}.
\]

It checks the strict Arb inequality

\[
\left|\frac{q_I-t_I}{|t_I|}\right|<\frac13.
\]

The full scan must cover 63,133 canonical dihedral orbits and 5,245,786 six-subsets. A complete pass evaluates 35 x 5,245,786 = 183,602,510 candidate-by-principal-minor determinants.

## Reproduction

A 1,024-orbit prefix is run first. If it passes, the workflow proceeds to the full scan:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_35_fourteen_probe_sixth_bound.py --workers 8 --limit 1024 \
  --output evidence/candidate_sixth_prefix_14probe_n21.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_35_fourteen_probe_sixth_bound.py --workers 8 \
  --output evidence/candidate_complete_sixth_bound_14probe_n21.json
```

Only `complete: true`, `passed: true`, 63,133 certified orbits, and 5,245,786 covered six-sets establish the complete sixth-order upper bound. A prefix pass is not promoted to a global statement.

## Scope limits

Even a complete sixth-order pass would not certify the other 1,408,185 eighth-order orbits, higher moments, exact program uniformity, global optimality, or operational inversion/channel error. Any new strict sixth-order separator must be added to the LP and the replacement candidate must be rechecked from its own exact rational input.
