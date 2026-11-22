# Eighth-order counterexample for the 29-column witness

## Result

The fixed 29-column candidate does **not** satisfy the proposed complete eighth-order bound
\[
G_8 := \max_{|I|=8}\frac{|q_I-t_I|}{|t_I|}<\frac13.
\]

A previously unselected dihedral orbit gives a large violation. The canonical representative is
\[
I=(0,1,3,14,19,24,29,40),
\]
with cyclic gaps
\[
(1,2,11,5,5,5,11,2)
\]
and orbit size 42. Since \(I\) has four odd indices, its target is \(t_I=+1/19721\).

For the exact 29 probabilities and exact reconstructed physical columns pinned by
\`evidence/candidate_joint_input_n21.json\`, an independent 22-decimal-digit \`mpmath.iv\` interval calculation gives
\[
q_I\in[9.82971346527856056808239434,\,9.82971346527857421879427353]\times10^{-5},
\]
and
\[
\frac{q_I-t_I}{t_I}
\in[0.938517792487584929631528970,\,
0.938517792487587621688423774].
\]
The lower endpoint exceeds \(1/3\) by more than \(0.60518\). The interval computation covers all 29 support columns and all 42 subsets in this orbit (1,218 principal-minor determinants).

## Evidence status

- **Established by the current interval run:** this orbit is a decisive counterexample to the \(G_8<1/3\) claim for this fixed candidate, with a very large separation.
- **Independent implementation check:** the binary64 SciPy screen gives the same relative error to approximately \(10^{-13}\).
- **Still required for the repository's publication-grade standard:** run \`verify_candidate_eighth_probe_arb.py\` at 128 bits. It uses the repository's existing Arb reconstruction path and only evaluates this one orbit.
- The complete 1,408,185-orbit scan is no longer needed to reject this candidate. It would only be needed to determine the candidate's actual global maximum or to produce a full diagnostic transcript.

## Consequence and next step

Do not describe the current 29-column witness as eighth-order \(1/3\)-uniform. First reproduce the named violation with Arb, then add this orbit as a seventh eighth-order LP row, re-solve over the frozen physical pool, and re-certify all low- and sixth-order constraints for any replacement candidate.

This is candidate-specific. It is not a no-go theorem for other physical distributions, nor does it settle moments of orders 10 through 20 or an operational inversion-error bound.
