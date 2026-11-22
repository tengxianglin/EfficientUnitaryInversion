# Complete sixth-order audit of the 34-column reweighted candidate

## Exact input

- Candidate SHA256: `00ba81adfcbebb02137e02b75a7f180d0bf528f71a4bdaa8afe9b9e2b19b7e99`
- LP transcript SHA256: `92e366abd639d80418b60a4831efd39c5c4ffeeb05a134fedc2ff1331f41963d`
- Parent 32-column candidate SHA256: `403614d80d8c5eeb15d56960fc7503103f8d376a7ab990fcb8988b1850d1a54d`
- Five-row Arb prefix transcript Git blob SHA1: `6604c6727b075b79ceca438b01faadbbb0ebbd19`
- Frozen seed-pool content SHA256: `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`
- Exact support: 34 positive rational probabilities summing to one
- Interval backend: python-flint 0.8.0 / Arb, 128-bit precision

The exact candidate has already passed Arb checks on all 1,461 low-order rows, the 261 selected sixth-order rows, and seven selected eighth-order rows. These are selected-row statements only.

## Complete sixth-order question

For every six-subset (I\subset\mathbb Z_{42}), the verifier computes

\[
q_I=\sum_{j=1}^{34}p_j\frac{1}{|O(I)|}
\sum_{J\in O(I)}\det R_j[J,J],
\qquad
t_I=(-1)^{v(I)+3}\frac{\binom{21}{3}}{\binom{42}{6}}.
\]

It checks the strict Arb inequality

\[
\left|\frac{q_I-t_I}{|t_I|}\right|<\frac13.
\]

The full scan must cover 63,133 canonical dihedral orbits and 5,245,786 six-subsets. A complete pass evaluates 34 x 5,245,786 = 178,356,724 candidate-by-principal-minor determinants.

## Reproduction

A 1,024-orbit prefix is run first. If it passes, the workflow proceeds to the full scan:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_34_sixth_bound.py --workers 8 --limit 1024 \
  --output evidence/candidate_sixth_prefix_12row_n21.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_34_sixth_bound.py --workers 8 \
  --output evidence/candidate_complete_sixth_bound_12row_n21.json
```

Only `complete: true`, `passed: true`, 63,133 certified orbits, and 5,245,786 covered six-sets establish the complete sixth-order upper bound. A prefix pass is not promoted to a global statement.

## Scope limits

Even a complete sixth-order pass would not certify the other 1,408,185 eighth-order orbits, higher moments, exact program uniformity, global optimality, or operational inversion/channel error. Any new strict sixth-order separator must be added to the finite LP and the replacement candidate must be rechecked from its own exact rational input.
