# N=42 period-two ensemble with five quartic translation orbits

Date: 2026-11-27. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7) and [the four-orbit partial design](THEORY_N42_PERIOD_TWO_PAIR_PLUS_QUARTIC_ENSEMBLE.md).

## Discovery

A deterministic HiGHS search over 100,000 strictly positive period-two atoms
\[
c_{2j}=a,\qquad c_{2j+1}=b,\qquad (a,b)\in[0,100]^2,
\]
with seed 351 found a 36-atom support for the complete pair target and five fourth-order translation-orbit targets.

The five representatives are
\[
\begin{aligned}
I_1&=\{0,1,2,3\},&
I_2&=\{0,3,10,15\},\\
I_3&=\{0,2,4,6\},&
I_4&=\{0,10,20,30\},\\
I_5&=\{0,2,21,23\}.
\end{aligned}
\]
The first four have 42 distinct translates each; the last has 21. Their translation orbits are pairwise disjoint, giving 189 distinct fourth-order coordinates.

The support is frozen as exact decimal rationals in
[evidence/n42_period_two_five_quartic_atoms.json](evidence/n42_period_two_five_quartic_atoms.json).
The floating LP residual was \(2.93\times10^{-14}\). This is discovery evidence only.

## Exact-real certificate construction

For each frozen base pair \((a_\ell,b_\ell)\), include the one-site translated
Hamiltonian \((b_\ell,a_\ell)\) with equal half weight. Thus the final support
has 72 physical atoms, all with strictly positive couplings.

Let \(m_d(a,b)=C_0^2-C_d^2\), \(d=1,\ldots,10\), and
\(n_d(a,b)=-C_0^2-S_d^2\), \(d=0,\ldots,20\), be the period-two pair features
from
[THEORY_N42_PERIOD_TWO_PAIR_MOMENT_ENSEMBLE.md](THEORY_N42_PERIOD_TWO_PAIR_MOMENT_ENSEMBLE.md).
For a quartic representative \(I\), write
\[
k_I(a,b)=\det Q(a,b)_{I,I}.
\]

The exact-real base weights \(w_\ell\) are defined as the unique solution of
the frozen \(36\times36\) system:
\[
\begin{aligned}
\sum_\ell w_\ell m_d(a_\ell,b_\ell)&=-1/41,
&&d=1,\ldots,10,\\
\sum_\ell w_\ell n_d(a_\ell,b_\ell)&=-1/41,
&&d=0,\ldots,19,\\
\frac12\sum_\ell w_\ell\bigl(k_{I_r}(a_\ell,b_\ell)
+k_{I_r}(b_\ell,a_\ell)\bigr)&=1/533,
&&r=1,\ldots,5,\\
\sum_\ell w_\ell&=1.
\end{aligned}
\]
The omitted \(n_{20}\) equation follows from the exact row-norm identity
\[
2\sum_{d=1}^{10}m_d+\sum_{d=0}^{20}n_d=-1.
\]
The quartic symmetrization is exactly the 50/50 mixture with the one-site
translate; it is not an approximation or an extra assumption.

The independent verifier reconstructs the weights from exact-rational coupling
inputs using 256-bit Arb. It checks invertibility of the \(36\times36\) matrix,
strict positivity of all weights, all 861 unordered pair coordinates, and all
189 distinct translated quartic coordinates. The certificate is pending the
hosted Arb run; no exact existence claim is made until that run succeeds.

## Scope

If the independent certificate succeeds, the result will establish a positive
period-two physical ensemble matching every pair principal-minor target and
five full fourth-order translation orbits (189 distinct coordinates). It will
not be a complete fourth-order design: the remaining quartic orbits and all
sixth-/higher-order moments remain unconstrained. It implies no Choi
trace-distance or channel diamond-distance bound.

## Reproducibility

- Frozen support: evidence/n42_period_two_five_quartic_atoms.json
- Independent verifier: verify_n42_period_two_five_quartic_ensemble_arb.py
- Workflow: .github/workflows/eui-n42-period-two-five-quartic.yml
- Expected machine certificate:
  evidence/n42_period_two_five_quartic_ensemble_arb.json
