# A rational continuous-path escape from the 151-column dual

Date: 2026-11-23

## Finding

The exact rational dual certified against the frozen 1,641-column canonical pool is **not** a global separator for the full continuous positive-coupling path family.

The dual score is
\[
S(c)=\lambda-\delta+z^\mathsf T a(c),
\]
where \(z\), \(\lambda\), \(\delta=10^{-10}\), the 1,779 normalized rows, and their ordering are pinned by
\`evidence/55probe_151col_dual_certificate_n21.json\` and
\`evidence/joint_low_six_eighth_lp_151col_55probe_n21.json\`.

## Explicit physical witness

Let
\[
m=(6,0,14,0,0,26,0,10,0,32,0,18,0,34,0,30,2,6,0,7,23,0,28,0,10,0,32,0,20,2,4,1,32,0,68,0,2,0,26,0,30).
\]
Define the 41 open-path edge magnitudes exactly by
\[
c_j=\begin{cases}
1/1000,&m_j=0,\\
3927m_j/5000,&m_j>0,
\end{cases}
\qquad j=0,\ldots,40,
\]
and set \(c_{41}=0\). Thus every one of the 41 path edges is strictly positive; the witness lies in the positive orthant left after the exact sign-gauge reduction. Its largest edge magnitude is \(53.4072\).

A multi-start differentiable search was used only to discover the near signed-permutation pattern. The final witness above is rational and is checked independently with Arb; no optimizer output enters the proof.

## Certified test

The verifier rebuilds \(R(c)=e^{K(c)}\) from the exact rational couplings using Arb, reconstructs all 52 nonzero entries of the exact dual against the pinned low/sixth/eighth row inventory, and evaluates \(S(c)\) as an interval.

The successful certificate must have a strictly positive lower endpoint:
\[
\underline{S(c)}>0.
\]
This directly violates the column inequality \(a(c)^\mathsf Tz+\lambda-\delta<0\) that would be required for this dual to separate every generator in the continuous path family.

Reproduce with:
\`\`\`bash
python freeze_seed_pool.py
python verify_continuous_path_dual_escape_arb.py
\`\`\`

The expected evidence is \`evidence/continuous_path_dual_escape_arb_n21.json\`, with the exact candidate, all source hashes, 128-bit Arb interval, and per-row contribution transcript.

## Consequences and scope

- **Disproved:** the current 151-column rational dual cannot be promoted to a global separator over all strictly positive 41-edge path couplings.
- **Unaffected:** the previously certified lower bound over the frozen 1,641-column canonical pool remains valid. The witness is checked to be outside that pool.
- **Not proved:** existence of a convex mixture over the full continuous family achieving the \(1/3\) cap; nonexistence of a different global dual; a full-family minimax value; complete moment control; or a Choi/diamond-norm operational guarantee.

The correct next step is therefore not to keep extending this same dual. Either derive a new global certificate with a different separating functional, or use the certified escape as a new column in a larger finite minimax reoptimization and inspect whether the optimum moves toward or below \(1/3\).
