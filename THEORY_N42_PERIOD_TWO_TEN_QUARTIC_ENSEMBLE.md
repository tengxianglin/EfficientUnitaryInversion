# N=42 period-two positive ensemble matching ten quartic translation orbits

Date: 2026-11-27. This is a rigorously certified extension of the nine-orbit partial ensemble in [THEORY_N42_PERIOD_TWO_NINE_QUARTIC_ENSEMBLE.md](THEORY_N42_PERIOD_TWO_NINE_QUARTIC_ENSEMBLE.md).

## Statement and physical family

Let \(N=42\) and \(n=21\). For each base atom \(\ell\), use the period-two nearest-neighbour cycle couplings
\[
c_{2j}=a_\ell,\qquad c_{2j+1}=b_\ell,\qquad j=0,\ldots,20,
\]
with \(a_\ell,b_\ell>0\). Write \(R_\ell=e^{A(c_\ell)}\) and
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\qquad Q_\ell=R_\ell D.
\]
For every base atom \((a_\ell,b_\ell)\), include its one-site translate \((b_\ell,a_\ell)\) with equal half of the base-atom probability. The resulting ensemble has 82 physical atoms.

The balanced-slice target in these \(Q\)-coordinates is
\[
\mathbb E\det Q_{I,I}=-\frac1{41}\quad(|I|=2),\qquad
\mathbb E\det Q_{I,I}=\frac1{533}\quad(|I|=4).
\]
The quartic target is \(\binom{21}{2}/\binom{42}{4}=1/533\).

## Frozen support and exact-real weights

The 41 base couplings are frozen in [evidence/n42_period_two_ten_quartic_atoms.json](evidence/n42_period_two_ten_quartic_atoms.json). Every finite decimal in that file is interpreted as an exact rational number. The minimum of all base coupling coordinates is exactly
\[
\frac{9135346810271617}{10^{15}}>0.
\]
Thus every one of the 42 couplings in every expanded physical atom is strictly positive.

The 41 exact-real base weights are defined as the unique solution of a \(41\times41\) moment system containing:
- 30 independent period-two pair equations (10 same-parity and 20 cross-parity coordinates);
- 10 symmetrized quartic principal-minor equations, one for each listed translation-orbit representative;
- normalization.

The omitted independent cross-parity pair equation follows from the period-two row-norm identity. The verifier nevertheless checks all unordered pairs directly after the one-site symmetrization.

The matrix entries involve trigonometric functions of the exact-rational couplings, so the weights are not claimed to be rational. The independent proof is a 256-bit Arb interval certificate: the determinant interval excludes zero and every exact-real weight is enclosed in a strictly positive interval.

## Ten matched quartic translation orbits

The ten representatives are
\[
\begin{gathered}
[0,1,2,3],\ [0,3,10,15],\ [0,2,4,6],\ [0,10,20,30],\\
[0,2,21,23],\ [6,13,14,30],\ [0,3,19,26],\\
[0,8,20,28],\ [0,4,8,12],\ [0,3,18,21].
\end{gathered}
\]
Their distinct full-translation orbit sizes are
\[
42,42,42,42,21,42,42,42,42,42,
\]
for 399 distinct four-subsets.

## Certified result

The independent verifier [verify_n42_period_two_ten_quartic_ensemble_arb.py](verify_n42_period_two_ten_quartic_ensemble_arb.py) and hosted workflow [45935129650](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45935129650) certify:

- the \(41\times41\) moment matrix is invertible, with determinant enclosure
  \[
  [-4.1090678188375528048\ldots\times10^{-52}\ \pm 7.53\times10^{-118}],
  \]
  which excludes zero;
- the minimum exact-real base weight is enclosed by
  \[
  [0.00121547137116687654968\ldots\ \pm 7.34\times10^{-71}]
  >\frac1{10000};
  \]
- the weights sum to one;
- all 861 unordered pair principal-minor coordinates equal \(-1/41\);
- all 399 distinct translated quartic coordinates in the ten listed orbits equal \(1/533\).

The machine certificate is [evidence/n42_period_two_ten_quartic_ensemble_arb.json](evidence/n42_period_two_ten_quartic_ensemble_arb.json). The frozen support and exact-real weights define a positive physical ensemble for the stated partial moment system.

## The next unmatched orbit is a support-specific miss

The next witness is
\[
I_{11}=[0,6,15,21].
\]
Its translation orbit has 42 distinct members and is disjoint from the ten matched orbits. The Arb verifier checks every translate and certifies
\[
\mathbb E\det Q_{I,I}-\frac1{533}>\frac1{250}
\]
for all 42 translates in this particular 82-atom ensemble. A representative moment is enclosed near \(0.006559917286531836\), while the target is approximately \(0.001876172607879925\).

This is only a failure of the frozen support. It does not exclude a different 11-orbit ensemble or any other physical ensemble.

## Discovery scope and reproducibility

The floating discovery used NumPy 2.3.5 / SciPy 1.17.0, seed 352, and 300,000 positive candidate pairs sampled uniformly from \([0,1000]^2\). The selected-equation binary64 residual was \(7.59\times10^{-14}\). The discovery script scanned all 2,670 cyclic translation orbits, covering all 111,930 four-subsets, and identified \([0,6,15,21]\) as the largest-residual orbit for this frozen support.

The 11-orbit feasibility LP was infeasible only on that fixed 300,000-candidate pool. This is a floating finite-pool observation, not an exact Farkas certificate and not a continuum no-go theorem.

HiGHS returned the same ordered 41-atom support with a maximum coordinate difference \(4.55\times10^{-13}\) from the frozen decimal support. The discovery check therefore uses an explicit \(10^{-9}\) coordinate tolerance. The frozen decimal inputs remain authoritative for the independent exact-rational Arb certificate; the tolerance does not weaken the certified moment statement.

## Scope limitations

This is a partial fourth-order design:
- it matches all 861 pair coordinates;
- it matches 399 of the 111,930 quartic coordinates, in ten specified translation orbits;
- it does not match all 2,670 quartic orbits;
- it does not establish sixth-, eighth-, or higher-even-order moment matching;
- it does not settle the full continuous physical-family convex-hull question;
- it implies no Choi trace-distance or channel diamond-distance bound.

In particular, the finite-pool infeasibility for the eleventh orbit must not be promoted to a global physical obstruction.
