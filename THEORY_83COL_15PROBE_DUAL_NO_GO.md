# Rigorous finite-pool separation from the 15-probe LP

Date: 2026-11-22

## Result

The finite minimax LP over the frozen 83-column physical path pool has
1,739 normalized constraints:

- 1,461 complete second/fourth-order rows;
- 256 frozen sixth-order screen rows;
- fifteen sixth-order rows with strict 128-bit Arb counterexamples from four
  successive candidate audits;
- seven selected eighth-order rows.

HiGHS finds the binary64 minimax objective
`0.33621835337230044`, above the target cap (1/3). This floating result is
only the dual-vector discovery step. The rigorous result is the independently
reconstructed Arb dual certificate in
`evidence/fifteen_probe_dual_certificate_n21.json`.

The exact rational witness, pinned to LP transcript SHA256 `9ea11822609963403194bdf7b507e02debb8e77836d9964bb7549721bd249911`, has

[
\|z\|_1=1,
\qquad
L=\lambda+z^T b
=\frac{3876333697222609805389947281}
{11529215046100527190000000000}
\approx0.33621835326366684,
]

and therefore

[
L-\frac13
=\frac{399144183259618584698661563}
{138350580553013384370000000000}
\approx0.002885019937496207>0.
]

At 128-bit Arb precision, every one of the 83 exact physical columns satisfies
the dual inequality (a_j^Tz+\lambda-\delta<0); the largest certified upper
endpoint is approximately (-9.24722548\times10^{-11}). The rational slack
`delta` and all 83 intervals are frozen in the certificate JSON.

## Theorem: obstruction for the frozen pool

Let (A\in\mathbb R^{1739\times83}) be the normalized moment-feature matrix
of the 83 pinned legal path columns, and let (b\in\mathbb Q^{1739}) be the
normalized target vector. For a probability vector (p\in\Delta_{83}), define

[
G_{\mathrm{finite}}(p)=\|Ap-b\|_\infty.
]

The certificate supplies (z\in\mathbb Q^{1739}) and
(\lambda\in\mathbb Q) such that

[
\|z\|_1\le1,\qquad A^Tz+\lambda\mathbf1\le0,
\qquad \lambda+z^Tb=L>\frac13.
]

For any (p\in\Delta_{83}),

[
z^T(Ap-b)=p^TA^Tz-z^Tb
\le-\lambda-z^Tb=-L.
]

By Hölder's inequality,

[
G_{\mathrm{finite}}(p)
\ge |z^T(Ap-b)|
\ge L>\frac13.
]

Thus **no reweighting of the frozen 83 columns can satisfy all 1,739
selected normalized constraints with worst error below (1/3)**. The
inequalities (A^Tz+\lambda\mathbf1\le0) are checked column-by-column with
128-bit Arb; the lower bound (L) is exact rational arithmetic.

## The 15th separator

The fourteenth-probe candidate was rejected by the first 1,024-orbit Arb
prefix at

[
I=(0,1,2,3,19,26),\qquad t_I=+5/19721,
]

with relative error interval centered at (0.4410096800482815489), strictly
above (1/3). This is a strict counterexample for that candidate, not a
global no-go statement.

Adding this row to the finite LP raises the best objective over the fixed
83-column pool to (0.33621835337). The dual theorem above upgrades that
observation to a rigorous finite-pool lower bound.

## Scope and next step

This theorem is deliberately limited to the exact 83 pinned physical columns
and the 1,739 listed rows. It does **not** rule out:

- new legal physical columns or other Hamiltonian families;
- a different physical ensemble with a larger support;
- satisfying the complete sixth/eighth-order orbit families;
- exact program uniformity, higher moments, or an operational inversion or
  channel-error guarantee.

The next step is therefore not another reweighting of the same pool. Use the
dual functional as a pricing oracle: search for a new legal physical column
(c) with (a(c)^Tz+\lambda>0), certify it with Arb, append it to the
pool, and resolve the expanded minimax problem. Such a column invalidates
this fixed-pool separator and is the required mechanism for escaping the
finite-pool obstruction.

## Reproduction

```bash
python freeze_seed_pool.py
python joint_low_six_eighth_lp_with_fifteen_sixth_probes.py
python verify_fifteen_probe_dual_certificate.py
```

The GitHub Actions workflow pins Python 3.11, NumPy 2.3.5, SciPy 1.15.3,
and python-flint 0.8.0. The certificate records the LP transcript SHA256,
frozen seed-pool SHA256, exact rational dual vector, exact lower bound, and
all 83 Arb-verified column inequalities.
