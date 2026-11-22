# Full sixth-order Arb audit of the 32-column seven-row candidate

Status: verification workflow added; no complete sixth-order result is claimed until the frozen transcript says `complete: true`.

## Frozen inputs

- Candidate: `evidence/candidate_joint_input_7row_n21.json`
- Candidate SHA256: `403614d80d8c5eeb15d56960fc7503103f8d376a7ab990fcb8988b1850d1a54d`
- Finite LP transcript SHA256: `64170b6e433e4e32240a46efcbdc47ba97eb1ce2f6c97126393f6ae45037767e`
- Frozen 1,600 x 42 seed-pool SHA256: `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`
- Exact support: 32 positive rational probabilities summing to one
- Interval backend: python-flint 0.8.0 / Arb, 128-bit precision

The candidate consists of legal 42-site real-skew nearest-neighbour path generators with the closing edge exactly zero. The candidate file pins the seven-row LP transcript and the earlier 29-column input from which the newly certified eighth-order separator was obtained.

## Quantity audited

For every six-subset (I\subset\mathbb Z_{42}), let (O(I)) be its dihedral orbit and let (R_j=\exp(A_j)) be the orthogonal matrix associated with physical column (j). The exact candidate moment is

\[
q_I=\sum_{j=1}^{32}p_j\frac{1}{|O(I)|}
\sum_{J\in O(I)}\det R_j[J,J],
\qquad
t_I=(-1)^{v(I)+3}\frac{\binom{21}{3}}{\binom{42}{6}}.
\]

The verifier checks the strict Arb inequality

\[
\left|\frac{q_I-t_I}{|t_I|}\right|<\frac13
\]

for every dihedral orbit. The canonical enumeration has 63,133 orbits and their orbit sizes sum to \(\binom{42}{6}=5,245,786\). A complete pass therefore evaluates 32 x 5,245,786 = 167,865,152 candidate-by-principal-minor determinants.

## Reproduction

A short prefix is a separator check only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_32_sixth_bound.py --workers 8 --limit 1024 \
  --output evidence/candidate_sixth_prefix_7row_n21.json
```

The complete audit is:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_32_sixth_bound.py --workers 8 \
  --output evidence/candidate_complete_sixth_bound_7row_n21.json
```

Only `complete: true`, `passed: true`, 63,133 certified orbits, and 5,245,786 covered six-sets establish the stated sixth-order bound. A prefix pass is not promoted to a global statement. A failed interval is classified as either a strict candidate-specific violation or an interval-unresolved row.

## Scope limits

Even a complete sixth-order pass would not certify the other 1,408,185 eighth-order orbits, higher moments, exact program uniformity, global optimality, or operational inversion/channel error. If a strict sixth-order violation is found, its exact orbit and Arb interval are the next row to add to the finite minimax design; any reweighted candidate must be rechecked from its own exact input.
