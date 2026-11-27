# N=42 period-two ensemble with six quartic translation orbits

Date: 2026-11-27. This strengthens
[the five-orbit partial design](THEORY_N42_PERIOD_TWO_FIVE_QUARTIC_ENSEMBLE.md)
by adding the sixth representative \(\{6,13,14,30\}\).

## Discovery

A deterministic HiGHS feasibility search over 100,000 strictly positive
period-two atoms in \([0,100]^2\), seed 351, found a 37-base-atom support
matching all 30 independent pair equations and six quartic targets. The
binary64 selected-equation residual is \(4.44\times10^{-16}\).

The six representatives are
\[
\begin{aligned}
I_1&=\{0,1,2,3\},&
I_2&=\{0,3,10,15\},\\
I_3&=\{0,2,4,6\},&
I_4&=\{0,10,20,30\},\\
I_5&=\{0,2,21,23\},&
I_6&=\{6,13,14,30\}.
\end{aligned}
\]
Their distinct full-translation orbit sizes are \(42,42,42,42,21,42\).
The orbits are pairwise disjoint, giving 231 distinct quartic coordinates.

The frozen exact-decimal support is
[evidence/n42_period_two_six_quartic_atoms.json](evidence/n42_period_two_six_quartic_atoms.json).
Every base coupling is strictly positive. The one-site symmetrization
\((a,b)\leftrightarrow(b,a)\) gives a 74-atom physical ensemble.

## Exact-real certificate construction

For each base atom \((a_\ell,b_\ell)\), define the period-two pair features
\[
m_d=C_0^2-C_d^2,\quad d=1,\ldots,10,\qquad
n_d=-C_0^2-S_d^2,\quad d=0,\ldots,20.
\]
For a quartic representative \(I\), let
\(k_I(a,b)=\det Q(a,b)_{I,I}\).

The exact-real weights \(w_\ell\) are defined by the unique solution of the
frozen \(37\times37\) system:
\[
\begin{aligned}
\sum_\ell w_\ell m_d(a_\ell,b_\ell)&=-1/41,
&&d=1,\ldots,10,\\
\sum_\ell w_\ell n_d(a_\ell,b_\ell)&=-1/41,
&&d=0,\ldots,19,\\
\frac12\sum_\ell w_\ell\bigl(k_{I_r}(a_\ell,b_\ell)
+k_{I_r}(b_\ell,a_\ell)\bigr)&=1/533,
&&r=1,\ldots,6,\\
\sum_\ell w_\ell&=1.
\end{aligned}
\]
The omitted \(n_{20}\) equation follows from
\[
2\sum_{d=1}^{10}m_d+\sum_{d=0}^{20}n_d=-1.
\]
The 50/50 \((a,b)\), \((b,a)\) symmetrization is exactly the one-site
translation average.

The independent verifier uses 256-bit Arb with exact-rational decimal
couplings. It certifies the \(37\times37\) matrix determinant excludes zero,
all weights exceed \(1/10000\), all 861 pair coordinates equal \(-1/41\),
and all 231 distinct translated quartic coordinates equal \(1/533\).
The independent 256-bit Arb certificate passed in GitHub Actions run 45931260609 (PR verification path). The workflow checked JSON validity, dependency consistency, Python compilation, exact-real matrix invertibility, strict weight positivity, all 861 pair coordinates, and all 231 quartic coordinates. The machine certificate is committed at evidence/n42_period_two_six_quartic_ensemble_arb.json.

## Scope

The computer-assisted exact existence result is now certified: a positive
physical period-two ensemble of 74 atoms matches all 861 pair principal-minor
coordinates and six full fourth-order translation orbits (231 distinct
subsets). It remains a partial design, not a complete fourth-order design or
an all-even-principal-minor ensemble. It implies no Choi trace-distance or
channel diamond-distance bound.

## Reproducibility

- Frozen support: evidence/n42_period_two_six_quartic_atoms.json
- Independent verifier: verify_n42_period_two_six_quartic_ensemble_arb.py
- Workflow: .github/workflows/eui-n42-period-two-six-quartic.yml
- Certified machine evidence: evidence/n42_period_two_six_quartic_ensemble_arb.json
- Workflow run: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45931260609
- Evidence commit: https://github.com/tengxianglin/EfficientUnitaryInversion/commit/c57dba80805be1a1d127ae7a3521e2ce61452913
