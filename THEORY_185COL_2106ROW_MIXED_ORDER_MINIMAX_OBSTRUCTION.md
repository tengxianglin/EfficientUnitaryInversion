# Strict 185-column mixed-order minimax obstruction

Date: 2026-11-23

## Theorem

Let P_185 be the fixed set of 185 physical path generators pinned by
evidence/joint_low_six_lp_185col_mixed_order_n21.json. Its inventory is:

- the 151-column canonical base (zero-based indices in the frozen 1,641-column pool): [3, 6, 16, 23, 46, 69, 74, 87, 99, 107, 116, 120, 125, 127, 129, 138, 155, 160, 168, 172, 178, 181, 193, 199, 206, 211, 223, 229, 230, 239, 249, 253, 257, 267, 268, 274, 278, 282, 283, 289, 303, 317, 320, 323, 338, 340, 341, 342, 343, 344, 349, 355, 367, 368, 374, 384, 388, 397, 404, 405, 415, 417, 422, 427, 432, 433, 438, 439, 445, 446, 454, 474, 475, 480, 484, 488, 493, 494, 502, 510, 511, 521, 532, 563, 569, 571, 579, 583, 590, 596, 599, 600, 615, 617, 625, 634, 636, 666, 679, 683, 695, 698, 700, 723, 727, 743, 755, 770, 779, 780, 796, 813, 817, 822, 823, 832, 882, 889, 890, 896, 902, 904, 906, 910, 915, 916, 933, 969, 974, 1087, 1191, 1282, 1600, 1601, 1602, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1614, 1635, 1636, 1637, 1638, 1639, 1640];
- the exact rational continuous-path generator certified in evidence/continuous_path_dual_escape_arb_n21.json;
- thirty earlier canonical additions: [1603, 886, 565, 682, 472, 525, 434, 487, 80, 145, 1613, 1412, 1383, 1580, 195, 221, 424, 655, 614, 635, 544, 420, 398, 352, 629, 668, 347, 425, 296, 844];
- three further canonical additions: [364, 517, 430].

For a coupling vector c=(c_0,...,c_40,0), define the real skew-symmetric path generator by
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,\quad j=0,\ldots,40,
\]
with all other entries zero, and set R(c)=exp(K(c)).

The normalized feature vector contains the 21 cyclic second-order rows, all 1,440 dihedral fourth-order orbit rows, and the 645 pinned sixth-order orbit rows. The row scales are
\[
s_2=\frac1{41},\qquad s_4=\frac{\binom{21}{2}}{\binom{42}{4}},\qquad s_6=\frac5{19721}.
\]
For completeness, the feature and target definitions are as follows. Let
\[
\mathcal O_k(I)=\{gI:g\in D_{42}\}.
\]
For the 21 cyclic second-order rows, with
\[
I_{i,d}=\{i,(i+d)\bmod 42\},\qquad d=1,\ldots,21,
\]
set
\[
b_d^{(2)}(c)=\frac1{42}\sum_{i=0}^{41}\det R(c)_{I_{i,d},I_{i,d}},
\qquad
\tau_d^{(2)}=\frac{(-1)^{d+1}}{41}.
\]
For each of the 1,440 dihedral fourth-order orbits, with representative (I), set
\[
b_I^{(4)}(c)=\frac1{|\mathcal O_4(I)|}
\sum_{J\in\mathcal O_4(I)}\det R(c)_{J,J},
\qquad
\tau_I^{(4)}=(-1)^{\sum_{i\in I}(i\bmod2)}
\frac{\binom{21}{2}}{\binom{42}{4}}.
\]
For each of the 645 pinned sixth-order orbit representatives (I), set
\[
b_I^{(6)}(c)=\frac1{|\mathcal O_6(I)|}
\sum_{J\in\mathcal O_6(I)}\det R(c)_{J,J},
\qquad
\tau_I^{(6)}=(-1)^{\sum_{i\in I}(i\bmod2)+3}
\frac{\binom{21}{3}}{\binom{42}{6}}.
\]
The normalized column (a(c)) consists of (b^{(2)}/s_2), (b^{(4)}/s_4), and (b^{(6)}/s_6), and the target vector (y) consists of the corresponding (	au/s) entries in the same row order. Thus the residual is exactly (e(p)=\sum_c p_c a(c)-y).

The 2,106-row inventory and exact targets are the same frozen design defined in
THEORY_182COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md; the sixth-row inventory hash is
5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb.

For a probability distribution p on this fixed pool, let e(p) be its normalized moment vector minus the exact target vector. Then

\[
\boxed{\min_{p\in\Delta(\mathcal P_{185})}\|e(p)\|_\infty
\ge \frac{86174177255875174056289633093}{184467440737103669070000000000}
= 0.4671511509648334 > \frac13.}
\]

The certified excess over 1/3 is
\[
\frac{24685030343507284366289633093}{184467440737103669070000000000}
= 0.1338178176315001.
\]

## Proof

The certificate supplies an exact rational vector z and scalar lambda with
\[\|z\|_1=1,\qquad \delta=1/10000000000,\]
and exact dual objective
\[\lambda+z^\mathsf T y=8617417727432191813/18446744073710366907.\]
The dual support contains 2 low-order rows and 54 sixth-order rows.
Independent 128-bit Arb evaluation verifies, for every one of the 185 physical columns a(c),
\[a(c)^\mathsf Tz+\lambda-\delta<0.\]
The largest certified interval upper endpoint after subtracting the slack is
[-7.6726289625084981342508868442503571950e-11 +/- 2.73e-49].

For every probability vector p, Holder's inequality gives
\[\|e(p)\|_\infty\ge z^\mathsf T\!\left(y-\sum_c p_c a(c)\right).
\]
Averaging the 185 strict column inequalities and using sum_c p_c=1 yields
\[\|e(p)\|_\infty\ge \lambda+z^\mathsf T y-\delta,\]
which is the exact rational lower bound above.

## Reproducibility

- Binary64 discovery: evidence/joint_low_six_lp_185col_mixed_order_n21.json.
- Exact rational dual and all 185 Arb intervals: evidence/55probe_185col_mixed_order_dual_certificate_n21.json.
- Independent verifier: verify_185col_mixed_order_dual_arb.py.
- Workflow: .github/workflows/eui-185col-mixed-order-dual.yml.
- LP transcript SHA256: 98d0cea6344d4e987436e347fa4c58df7f7cb844b6df7ab413c62750680837a2.
- Exact dual objective: 8617417727432191813/18446744073710366907.

## Scope

This is a rigorous mixed-order lower bound for mixtures over the specified 185-generator pool and the pinned 2,106-row design only. It does not exclude additional canonical or continuous physical generators, does not establish a global minimax result over the unrestricted path family, and is not a Choi-fidelity or diamond-norm theorem.
