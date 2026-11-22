# 113-column / 55-separator finite-pool dual obstruction

Date: 2026-11-22  
LP transcript: evidence/joint_low_six_eighth_lp_113col_55probe_n21.json  
128-bit Arb certificate: evidence/55probe_113col_dual_certificate_n21.json  
Certificate commit: 3a8741afec6d0f049daf132b8716779ff83a2a7f

## Statement

Let C_113 be the 113 pinned legal 42-site path generators in the LP transcript. Let A in R^(1779 x 113) contain their normalized moment features, and let y in Q^1779 be the corresponding normalized target vector. Define
\[
\eta_{113,55}:=\min_{p\in\Delta_{113}}\|Ap-y\|_\infty.
\]

The 1,779 rows are exactly:

- 1,461 second-/fourth-order rows;
- 311 sixth-order rows: 256 frozen screening rows, 38 parent probes, eight strict Arb separators from the rejected 38-probe candidate, one strict Arb prefix separator from the rejected 46-probe candidate, and eight strict Arb separators from the rejected 47-probe candidate;
- seven selected eighth-order rows.

The finite binary64 HiGHS discovery objective is
\[
0.36575443678254027\ldots
\]
and its dual was rationalized and independently checked using 128-bit Arb. The certificate proves
\[
\boxed{
\eta_{113,55}\ge
\frac{4118028861881514868548001}
{11258999068426240000000000}
=0.3657544366825429\ldots
>\frac13.
}
\]
The exact certified gap above 1/3 is
\[
\frac{1095087517218304605644003}
{33776997205278720000000000}
=0.032421103349209585\ldots.
\]

## Certificate data

The rational dual vector z in Q^1779, multiplier lambda, and slack delta satisfy
\[
\|z\|_1=
\frac{1152921504606844607}{1152921504606846976}<1,
\qquad
\lambda=\frac{1308000615381053}{1125899906842624},
\qquad
\delta=10^{-10}.
\]
Its exact objective before slack is
\[
\lambda+z^Ty=
\frac{421686155571959273}{1152921504606846976}.
\]
For every one of the 113 pinned columns, 128-bit Arb certifies
\[
a_j^Tz+\lambda-\delta<0.
\]
The maximum Arb upper endpoint over all column inequalities is
\[
-8.2477822270927892308\times10^{-11}
\]
(up to the reported Arb radius \(2.19\times10^{-49}\)). The certificate records all 113 intervals and the complete rational dual vector.

## Proof

For any p in Delta_113, Holder's inequality and the simplex constraint give
\[
\|Ap-y\|_\infty
\ge z^T(y-Ap)
=z^Ty-\sum_{j=1}^{113}p_j a_j^Tz.
\]
The Arb-certified column inequalities imply \(a_j^Tz\le-\lambda+\delta\) for every j. Hence
\[
-\sum_jp_ja_j^Tz\ge\lambda-\delta,
\]
and therefore
\[
\|Ap-y\|_\infty\ge z^Ty+\lambda-\delta.
\]
The exact rational value of the right-hand side is the boxed lower bound. This proves the stated finite-pool minimax obstruction.

## What this does and does not establish

**Proved:** no convex mixture of these exact 113 physical columns can meet the 1/3 normalized-error cap on this exact 1,779-row constraint set.

**Not proved:** infeasibility over the remaining 1,528 columns in the frozen 1,641-column canonical pool; infeasibility over all legal physical Hamiltonians; a complete sixth- or eighth-order maximum; any all-moment uniformity theorem; or an operational Choi/diamond-norm inversion guarantee.

The 311 sixth-order rows are a finite selected/separator set, not all 63,133 sixth-order dihedral orbits. The 55-separator LP has objective above the cap, so it produces no admissible 1/3-candidate; its nonzero LP weights must not be described as a passing ensemble.

## Reproduction

~~~bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python verify_55probe_113col_dual_certificate.py
~~~

The workflow 45016441616 completed successfully. The certificate pins the LP transcript SHA256
b81c2a157600964d5e53b30f80e1d442d9038a4b7821b3a544dc07314995620b
and uses python-flint 0.8.0 / Arb at 128-bit precision.

## Next decisive action

Price the remaining 1,528 canonical columns against this new dual. Binary64 scores are only a discovery screen; any candidate escape must be recomputed with Arb before adding it to the physical pool. If no positive column is found, a full-pool obstruction requires rigorous verification of every remaining column, not merely the top few float scores.
