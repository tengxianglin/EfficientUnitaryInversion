# 191-column mixed-order minimax obstruction after the eighth continuous-path escape

## Theorem

Let \(\mathcal P_{191}\) be the ordered finite pool pinned by
`evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json`.
It consists of 183 selected canonical generators and eight distinct exact-decimal
open-path generators. Each open path has 41 strictly positive edge magnitudes
and a zero closing-edge coordinate. The eight path inputs are independently
certified as distinct and strictly positive.

Let \(A_{191}\) denote the exact normalized moment-feature matrix and
\(y\) its exact target vector for the pinned 2,113-row design:

- 1,461 complete second-/fourth-order rows (21 second-order and 1,440 fourth-order);
- 645 sixth-order rows (311 previously selected rows and 334 additional orbit cuts);
- seven selected eighth-order rows.

Then every probability vector \(p\in\Delta_{191}\) obeys
\[
\boxed{
\|A_{191}p-y\|_\infty
\ge
\frac{2493405651522255993844313}
{5629499534213120000000000}
=0.4429178182480797\ldots
>\frac13.
}
\]
The exact certified margin above one third is
\[
\frac{1850717420353647981532939}
{16888498602639360000000000}
=0.10958448491474636\ldots.
\]

This is a finite-pool mixed-order minimax theorem. It rules out every
probability reweighting of these 191 fixed physical generators for the pinned
row design. It is not a no-go theorem for the unrestricted continuous path
family.

## Exact dual certificate

The machine-readable certificate is
`evidence/55probe_191col_eighth_continuous_escape_dual_certificate_n21.json`.
It records a rational vector \(z\in\mathbb Q^{2113}\), a rational
\(\lambda\), and slack \(\delta=10^{-10}\), with
\[
\|z\|_1=
\frac{576460752303381559}{576460752303423488}<1,
\qquad
\lambda=
\frac{3003779145842305}{2251799813685248},
\]
and
\[
\lambda+z^\mathsf Ty
=
\frac{255324738773525089}{576460752303423488}.
\]
Thus
\[
\lambda+z^\mathsf Ty-\delta
=
\frac{2493405651522255993844313}
{5629499534213120000000000}.
\]

The 128-bit Arb verifier independently evaluates all 191 physical-column
inequalities
\[
z^\mathsf Ta_j+\lambda-\delta<0,
\qquad j=1,\ldots,191.
\]
All 191 interval upper endpoints are strictly negative. The largest recorded
interval is
\[
[-2.0472330488499601835976889763931526041\times10^{-11}
\;\pm\;3.45\times10^{-49}],
\]
which is strictly below zero.

The exact dual has 59 nonzero coordinates: two fourth-order rows (zero-based
row indices 233 and 1413), 55 sixth-order rows, and two eighth-order rows
(indices 2106 and 2107). It has no nonzero second-order coordinate. The
certificate records the complete rational dual vector, all 191 Arb intervals,
the exact row/column ordering, and hashes for the LP transcript, cut design,
canonical inventory, seed pool, and all eight escape certificates.

## Proof

For each column, the certified inequality gives
\[
z^\mathsf Ta_j< -\lambda+\delta.
\]
For any \(p\in\Delta_{191}\), convexity therefore yields
\[
z^\mathsf T A_{191}p
=\sum_{j=1}^{191}p_j z^\mathsf Ta_j
< -\lambda+\delta.
\]
Consequently,
\[
z^\mathsf T(y-A_{191}p)
>z^\mathsf Ty+\lambda-\delta.
\]
The right-hand side is the positive rational number displayed in the theorem.
By Hölder's inequality and \(\|z\|_1<1\),
\[
\|A_{191}p-y\|_\infty
\ge
\frac{|z^\mathsf T(y-A_{191}p)|}{\|z\|_1}
\ge z^\mathsf T(y-A_{191}p)
>z^\mathsf Ty+\lambda-\delta.
\]
This proves the stated non-strict lower bound for every probability mixture.

## Reproduction and evidence

- LP discovery transcript:
  `evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json`
- Exact 128-bit Arb certificate:
  `evidence/55probe_191col_eighth_continuous_escape_dual_certificate_n21.json`
- Independent verifier:
  `verify_191col_eighth_continuous_escape_dual_arb.py`
- Reoptimization and certification workflow:
  [GitHub Actions run 45177433399](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45177433399)
- Certificate commit:
  [8faeb967d44b438030d584f18cfd0a860815538b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8faeb967d44b438030d584f18cfd0a860815538b)
- Verifier provenance-key repair:
  [80747a71e5fb245b13f20cf989235a2c21229a50](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/80747a71e5fb245b13f20cf989235a2c21229a50)

Reproduce from a clean checkout with the pinned workflow, or run:
```bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python verify_190col_seventh_continuous_escape_dual_arb.py
python verify_191col_eighth_continuous_escape_dual_arb.py
```

The first 191-column workflow attempt failed before any column interval was
evaluated because the verifier mistakenly looked for `parent_189col_*`
fields on the 191-column transcript; the transcript correctly stores
`parent_190col_*`. Commit `80747a7` corrected those provenance keys and the
dimension/error labels. The clean rerun 45177433399 passed all steps,
including the exact rational reconstruction and the 128-bit Arb audit.

## Scope and limitations

1. The pool contains 191 fixed generators, not the full 1,641-column
   canonical inventory and not every positive 41-edge path.
2. The sixth-order block contains 645 rows, a strict subset of the 63,133
   dihedral sixth-order orbits. The seven eighth-order rows are selected, not
   a complete eighth-order orbit audit. The 334 added sixth-order cuts are
   valid exact orbit rows; their discovery by a binary64 scan is not itself
   claimed as an interval-certified violation of the earlier candidate.
3. Because the full moment maximum contains the same normalized pinned rows,
   the lower bound also applies to any larger row objective that includes
   them, for mixtures over this same 191-generator pool. It does not extend
   the physical generator pool.
4. The theorem does not establish feasibility or infeasibility over the
   unrestricted continuous family, nor does it give a per-instance bridge
   from these moment residuals to Choi infidelity, diamond distance, or an
   operational inversion-error guarantee.
