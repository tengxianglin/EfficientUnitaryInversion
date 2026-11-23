# Strict 186-column mixed-order minimax obstruction after the third continuous escape

Date: 2026-11-23

## Theorem

Let P_186 be the ordered set of 186 physical path generators pinned by the LP transcript at evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json. It consists of the 151-column canonical base, 32 additional canonical generators, and three exact-rational continuous open-path generators (augmented column labels 1641, 1642, and 1643). The frozen 1,641-column canonical inventory has little-endian binary64 SHA256
\[
\texttt{f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98}.
\]
The ordered column-index inventory is pinned by SHA256
\[
\texttt{8bc8760e5d81cade91e459148cb49c33ac844cdae59e5ed474093ee2e7bab07e}.
\]
The 1,600-by-42 frozen seed pool is pinned by SHA256
\[
\texttt{93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315}.
\]

For a coupling vector c=(c_0,...,c_40,0), define
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,\qquad j=0,\ldots,40,
\]
with all other entries zero, and R(c)=exp K(c). Each of the three added continuous generators has 41 strictly positive open-path couplings and terminal padding c_41=0. Their exact rational inputs are pinned by the first, second, and third continuous-path Arb certificate files listed in Reproducibility.

Let O_k(I)={gI:g in D_42}. The pinned 2,113 normalized residual coordinates are ordered as follows.

1. 21 complete cyclic second-order rows, with I_{i,d}={i,(i+d) mod 42}, d=1,...,21,
\[
b_d^{(2)}(c)=\frac1{42}\sum_{i=0}^{41}\det R(c)_{I_{i,d},I_{i,d}},
\qquad \tau_d^{(2)}=\frac{(-1)^{d+1}}{41}.
\]
2. All 1,440 fourth-order dihedral-orbit rows,
\[
b_I^{(4)}(c)=\frac1{|O_4(I)|}\sum_{J\in O_4(I)}\det R(c)_{J,J},
\quad
\tau_I^{(4)}=(-1)^{\sum_{i\in I}(i\bmod2)}
\frac{\binom{21}{2}}{\binom{42}{4}}.
\]
3. 645 pinned sixth-order dihedral-orbit rows (311 original selected rows plus 334 cuts),
\[
b_I^{(6)}(c)=\frac1{|O_6(I)|}\sum_{J\in O_6(I)}\det R(c)_{J,J},
\quad
\tau_I^{(6)}=(-1)^{\sum_{i\in I}(i\bmod2)+3}
\frac{\binom{21}{3}}{\binom{42}{6}}.
\]
4. Seven selected eighth-order dihedral-orbit rows,
\[
b_I^{(8)}(c)=\frac1{|O_8(I)|}\sum_{J\in O_8(I)}\det R(c)_{J,J},
\quad
\tau_I^{(8)}=(-1)^{\sum_{i\in I}(i\bmod2)+4}
\frac{\binom{21}{4}}{\binom{42}{8}}.
\]

The row scales are
\[
s_2=\frac1{41},\quad
s_4=\frac{\binom{21}{2}}{\binom{42}{4}},\quad
s_6=\frac5{19721},\quad
s_8=\frac1{19721}.
\]
For each physical generator c_j, its column a_j in R^2113 consists of the corresponding b^(k)(c_j)/s_k, and y consists of the corresponding tau^(k)/s_k. For p in the probability simplex Delta_186, the normalized residual is r(p)=Ap-y.

The sixth-row inventory SHA256 is
\[
\texttt{5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb},
\]
the eighth-row inventory SHA256 is
\[
\texttt{c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0},
\]
and the binary64 matrix/target reconstruction SHA256 is
\[
\texttt{4fb01a980f91e3cacfbf39a792e07933fa47d8c7ba3ba4fbe6842a20fbe0b191}.
\]

Then every probability vector on this fixed physical pool satisfies
\[
\boxed{
\min_{p\in\Delta_{186}}\|Ap-y\|_\infty
\ge
\frac{2699464018593872397696556823}
{5764607523034431770000000000}
=0.4682823605609322602\ldots>\frac13.
}
\]
The exact certified margin above 1/3 is
\[
\frac{2333784532747185423089670469}
{17293822569103295310000000000}
=0.1349490272275989268\ldots.
\]

This is a mixed-order finite-pool theorem.

## Exact dual certificate and proof

The machine-readable certificate is evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json. It contains an exact rational vector z in Q^2113 and lambda in Q, with
\[
\|z\|_1=1,\qquad \delta=\frac1{10^{10}},
\qquad
\lambda=\frac{824319676466621440}{576460752303443177},
\]
and
\[
\lambda+z^\mathsf Ty
=\frac{269946401917033315}{576460752303443177}.
\]
The support has 54 coordinates: five fourth-order rows (zero-based indices 41, 233, 868, 1413, 1444), 47 sixth-order rows (indices 1675, 1712, 1716, 1737, 1738, 1765, 1767, 1779, 1781, 1782, 1794, 1796, 1797, 1805, 1821, 1845, 1847, 1857, 1865, 1883, 1884, 1902, 1913, 1929, 1933, 1937, 1963, 1971, 1983, 1985, 1987, 1988, 1989, 2002, 2032, 2038, 2046, 2051, 2071, 2074, 2079, 2085, 2088, 2090, 2098, 2099, 2101), and two eighth-order rows (indices 2106, 2107). There is no second-order support.

Independent 128-bit Arb evaluation certifies, for every one of the 186 physical columns,
\[
a_j^\mathsf Tz+\lambda-\delta<0.
\]
All 186 interval upper endpoints are strictly negative; the maximum upper endpoint is
\[
[-5.8049776314970689775168775729908666748\times10^{-11}
\ \pm 1.91\times10^{-49}]<0.
\]
The certificate records all 186 intervals and is marked complete.

For any p in Delta_186, averaging the 186 strict column inequalities gives
\[
z^\mathsf TAp+\lambda-\delta<0.
\]
Since ||z||_1=1, Holder's inequality yields
\[
\|Ap-y\|_\infty
\ge z^\mathsf T(y-Ap)
\ge \lambda+z^\mathsf Ty-\delta,
\]
which is the stated exact rational lower bound.

The binary64 HiGHS calculation is discovery evidence only: objective 0.4682823606610356, independently recomputed maximum 0.4682823606621971, support size 54, and primal-dual discovery gap 8.73e-14. The theorem rests on the exact rational dual and Arb interval checks, not on the optimizer's floating-point status.

## Reproducibility

- LP transcript: evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json
- Exact dual and 186 Arb intervals: evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json
- Independent verifier: verify_186col_third_continuous_escape_dual_arb.py
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45128712241
- LP transcript SHA256: 8fdaf824fa742ae34a5a156c251feadd59b0047b
- Dual certificate SHA256: 365dc82f4540cb6821038da3059efeb8cb8205b3
- Parent 185-column LP SHA256: 53b3e6b6369b05be741ac9f716be798051059fb646002df33bfc67e06bc68e0b
- Parent 185-column dual SHA256: 3d66af653cef76f0e8bca5c9672730fa08bb390da067b37df7f12450668f71b7
- First continuous escape certificate: evidence/continuous_path_dual_escape_arb_n21.json (SHA256 9e85d7f617baaa5bee371297e9f94716c21c7404f8349def2ef376dafb20d59e)
- Second continuous escape certificate: evidence/184col_continuous_dual_escape_arb_n21.json (SHA256 d40aeaa3c5c5a814a47f046ff96f892e4bf98069fa59330ffa4c7e343674543c)
- Third continuous escape certificate: evidence/185col_continuous_dual_escape_arb_n21.json (SHA256 71e7581990b50f1dd8ad22a11190ac66e016318d925022f250a51253166e7a4e)

The third path was a strict escape from the 185-column dual:
\[
S_{185}(c)\in[293.82920368783706755711439295738586\pm5.02\times10^{-33}]>0.
\]
It was then added as column 1643 and the 186-column problem was reoptimized.

## Scope and limitations

The theorem concerns only mixtures over these 186 fixed physical generators and the pinned 2,113-row mixed-order objective. The 645 sixth-order rows are selected/cut rows, not all 63,133 sixth-order dihedral orbits; the seven eighth-order rows are selected representatives, not all 1,408,185 eighth-order orbits. The result is not a sixth-only theorem, a global minimax theorem over all positive couplings, or an operational Choi-fidelity/diamond-norm guarantee.

The third continuous path disproves the global extension of the 185-column dual. The newly certified 186-column dual was subsequently tested by a deterministic 10-start differentiable search; a fourth exact-rational path has a strictly positive 128-bit Arb pricing interval against it. See THEORY_186COL_CONTINUOUS_PATH_DUAL_ESCAPE.md. This refutes global separation by this particular 186-column dual, but does not invalidate the finite 186-column theorem or establish a full-family minimax value.
