# Eighth-order counterexample for the 29-column witness

## Result

The fixed 29-column candidate does **not** satisfy the proposed complete eighth-order bound
\[
G_8 := \max_{|I|=8}\frac{|q_I-t_I|}{|t_I|}<\frac13.
\]

A previously unselected dihedral orbit gives a decisive violation. The canonical representative is
\[
I=(0,1,3,14,19,24,29,40),
\]
with cyclic gaps
\[
(1,2,11,5,5,5,11,2)
\]
and orbit size 42. Since \(I\) has four odd indices, its target is \(t_I=+1/19721\).

For the exact 29 probabilities and exact reconstructed physical columns pinned by
evidence/candidate_joint_input_n21.json (SHA256
5ae3afde386225dc1a398643303684ac1589fc2abfcf3cf2ff177ace4b640059),
the 128-bit Arb replay gives
\[
q_I\in[9.82971346527856824420185373628913\times10^{-5}
\;\pm\;6.62\times10^{-38}],
\]
and
\[
\frac{q_I-t_I}{t_I}
\in[0.938517792487586443439047575333579
\;\pm\;9.77\times10^{-34}].
\]
In particular, the certified rational lower bound is
\[
\boxed{\frac{q_I-t_I}{t_I}>\frac{1877}{2000}=0.9385>\frac13.}
\]
The targeted Arb calculation covers all 29 exact weights and all 42 subsets in the orbit: 1,218 principal-minor determinants.

## Evidence and reproducibility

- **Publication-grade targeted confirmation:** frozen 128-bit Arb transcript at evidence/candidate_eighth_probe_arb_n21.json, generated with python-flint 0.8.0 / Arb.
- **Independent interval cross-check:** 22-dps mpmath.iv transcript at evidence/candidate_eighth_probe_mpmath_iv_n21.json, whose interval overlaps the Arb result.
- **Reproducer:** verify_candidate_eighth_probe_arb.py.
- **CI:** targeted Arb workflow at .github/workflows/eui-targeted-arb.yml.
- **Orbit-enumeration fingerprint:** d395d745428d5b7b35319aa368d701716e7323d0f599e6314fc8ec59c6af83db.

The exact full-orbit enumerator remains useful for finding the global maximum, but the complete 1,408,185-orbit determinant scan is **not needed to reject this candidate**: one strictly certified orbit already disproves its proposed G8 < 1/3 bound.

## Consequence and next step

Do not describe the current 29-column witness as eighth-order 1/3-uniform. Add this orbit as a seventh eighth-order row to the finite low/sixth/eighth minimax LP over the frozen 83-column physical pool. Any replacement candidate must then be rechecked against all low-order constraints and the complete sixth-order certificate before an improvement claim.

This is candidate-specific. It is not a no-go theorem for other physical distributions, nor does it settle the complete eighth-order maximum, moments of orders 10 through 20, exact all-moment program uniformity, or an operational inversion/channel-error bound.
