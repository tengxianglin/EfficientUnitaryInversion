# Rigorous dual audit of the 93-column, 20-probe design

Date: 2026-11-22

## Finite LP finding

The 20-probe active-set LP uses 93 legal physical path columns and 1,744 normalized rows:
- 1,461 complete second/fourth-order rows;
- 256 frozen sixth-order screen rows;
- 20 Arb-certified sixth-order separators;
- seven selected eighth-order rows.

HiGHS returned finite binary64 minimax objective
`0.33420131882640136 > 1/3`
(the maximum recomputed residual is `0.3342013188266635`). Therefore the finite LP did not produce a candidate below the strict cap. This is a numerical discovery, not yet a theorem.

The stored HiGHS dual has rationalizable `z` with exact `||z||_1 <= 1` after normalization and rationalized objective near `0.3342013188262`. The decisive question is whether the exact dual inequalities can be certified for every one of the 93 physical columns with a positive slack `delta` while keeping the lower bound above 1/3.

## Dual theorem to certify

Let `a_j` be the exact normalized 1,744-row moment vector of physical column `j`, and let `y` be the exact target vector. If rational `z, lambda, delta` satisfy
[
|z|_1le 1,qquad
a_j^T z+lambda-deltale 0quad	ext{for all 93 columns }j,
]
and
[
lambda+z^T y-delta>rac13,
]
then every convex mixture (p) of these 93 columns obeys
[
|Ap-y|_infty
ge -z^T(Ap-y)
ge lambda+z^Ty-delta
>rac13.
]
The proof is finite-dimensional weak duality plus the certified column inequalities. The certificate is restricted to this exact 93-column pool and these 1,744 rows.

## Reproducibility

`verify_twenty_probe_93col_dual_certificate.py` reconstructs all exact row scales and physical column moments, rationalizes the HiGHS dual, and checks all 93 inequalities with 128-bit Arb. The CI workflow pins the LP transcript and frozen seed-pool hash and stores the resulting certificate only if every strict interval check passes.

A successful certificate would prove a fixed-pool obstruction, not a no-go for other physical generators. The next step after certification is to price the remaining legal canonical columns against this new dual, then Arb-certify any positive reduced-cost candidates.
