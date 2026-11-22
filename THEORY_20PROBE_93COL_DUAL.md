# Rigorous 93-column obstruction at 20 sixth-order probes

Date: 2026-11-22

## Certified result

The 93-column, 1,744-row LP has a rigorous dual certificate. The row blocks are:
- 1,461 complete second/fourth-order rows;
- 256 frozen sixth-order screen rows;
- 20 Arb-certified sixth-order separators;
- seven selected eighth-order rows.

At 128-bit Arb, the rationalized dual vector has exact `||z||_1 = 1`. With
[
\lambda=\frac{4669608075013085184}{4611686018429340679},\qquad
\delta=10^{-10},
]
the certificate verifies for every one of the 93 physical columns (a_j):
[
a_j^Tz+\lambda-\delta<0.
]
The maximum Arb upper endpoint over the 93 shifted column inequalities is
[
-8.5561176627143476\times10^{-11}
]
(up to the printed Arb interval enclosure).

The resulting exact minimax lower bound is
[
\boxed{
\min_{p\in\Delta_{93}}\|Ap-y\|_\infty
\ge
\frac{15412315489096098691570659321}
{46116860184293406790000000000}
\approx0.33420131872605807
>
\frac13.
}
]
The exact gap above (1/3) is
[
\frac{120086282994889284711977963}
{138350580552880220370000000000}
\approx 8.679853927247528\times10^{-4}.
]

This is a proved fixed-pool obstruction: every convex mixture of these exact 93 legal physical path columns violates the strict (1/3) cap on at least one of the 1,744 pinned normalized rows. It does **not** rule out a new physical column, another Hamiltonian family, or a different approximation target.

## Evidence pins

- 20-probe LP transcript SHA256: `046c7b8a1bafb9916cf073ec1931a8dbbb447ce86978779a2289c787d40e1aab`.
- Frozen seed pool SHA256 (little-endian f64): `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`.
- Canonical 1,641-column array SHA256 (little-endian f64): recorded in the certificate.
- Arb backend: python-flint 0.8.0 / Arb, 128-bit precision.
- Exact dual `l1` norm: 1.
- Exact slack: `1/10000000000`.

The complete per-column Arb intervals and rational dual vector are stored in `evidence/twenty_probe_93col_dual_certificate_n21.json`.

## Proof

For any convex weights (p_j\ge0), (sum_jp_j=1), the certified column inequalities imply
[
z^T(Ap)+\lambda-\delta
=\sum_jp_j(a_j^Tz+\lambda-\delta)\le0.
]
Therefore
[
\|Ap-y\|_\infty
\ge -z^T(Ap-y)
\ge \lambda+z^Ty-\delta
>\frac13,
]
where (|z|_1=1) gives the first inequality. Every quantity in the certificate is rational except the reconstructed physical feature evaluations, whose upper endpoints are enclosed by Arb and are strictly negative after the slack shift.

## Next step

Use this new dual to price the remaining 1,548 unused canonical legal path columns. Binary64 scores are discovery only; every positive reduced-cost candidate must be re-evaluated with 128-bit Arb before it is admitted to an expanded pool.