# Strict 187-column mixed-order minimax obstruction after the fourth continuous escape

Date: 2026-11-23

## Theorem

Let \(\mathcal P_{187}\) be the ordered set of 187 physical generators pinned by the LP transcript
\[
\texttt{evidence/joint\_low\_six\_eighth\_lp\_187col\_fourth\_continuous\_escape\_n21.json}.
\]
The ordered pool consists of the 151-column canonical base, the first exact-rational continuous path (label 1641), 32 additional canonical generators, and the second, third, and fourth exact-rational continuous paths (labels 1642, 1643, and 1644). The 1,641-column canonical inventory is frozen with little-endian binary64 SHA256
\[
\texttt{f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98}.
\]
The 1,600-by-42 seed pool SHA256 is
\[
\texttt{93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315}.
\]
The ordered 187-column index SHA256 is
\[
\texttt{1387cf3864d50ed35ccca5a0073b4a7c0fd5dba4a9350606f62437954d1d1e72}.
\]

For \(c=(c_0,\ldots,c_{40},0)\), define the skew-symmetric path generator
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,
\qquad j=0,\ldots,40,
\]
with all other entries zero, and \(R(c)=\exp K(c)\). Each of the four added continuous paths has 41 strictly positive open-edge couplings and terminal padding \(c_{41}=0\). Their exact inputs are pinned by the four Arb escape certificates listed below.

The 2,113 normalized residual rows are ordered as:
- 21 complete second-order cyclic rows and all 1,440 fourth-order dihedral-orbit rows (1,461 complete low-order rows);
- 645 pinned sixth-order orbit rows (311 selected rows plus 334 cuts);
- seven selected eighth-order orbit rows.

For a physical column \(a_j\), each entry is the corresponding principal-minor orbit average divided by its order-specific target scale. The target vector \(y\) uses the exact ideal moments. The row scales are
\[
s_2=\frac1{41},\qquad
s_4=\frac{\binom{21}{2}}{\binom{42}{4}},\qquad
s_6=\frac5{19721},\qquad
s_8=\frac1{19721}.
\]
For \(p\in\Delta_{187}\), write \(r(p)=Ap-y\).

**Claim.** Every probability vector on this fixed physical pool obeys
\[
\boxed{
\min_{p\in\Delta_{187}}\|Ap-y\|_\infty
\ge
\frac{21369707366939402851572579191}
{46116860184274208090000000000}
=0.4633816630523005\ldots>\frac13.
}
\]
The exact certified margin above \(1/3\) is
\[
\frac{17992261916544000464717737573}
{138350580552822624270000000000}
=0.13004832971896715\ldots.
\]

This is a mixed-order finite-pool theorem.

## Exact rational dual and proof

The machine-readable certificate is
\[
\texttt{evidence/55probe\_187col\_fourth\_continuous\_escape\_dual\_certificate\_n21.json}.
\]
It contains \(z\in\mathbb Q^{2113}\) and \(\lambda\in\mathbb Q\) with
\[
\|z\|_1=1,\qquad
\delta=\frac1{10^{10}},
\]
\[
\lambda=\frac{6557460267099352064}{4611686018427420809},
\qquad
\lambda+z^\mathsf Ty
=\frac{2136970737155108887}{4611686018427420809}.
\]
The dual support has 59 coordinates:
- three fourth-order rows, zero-based indices \(233,868,1413\);
- 54 sixth-order rows, zero-based indices
\[
\begin{aligned}
&1675,1716,1738,1765,1766,1767,1779,1781,1782,1790,1796,1797,\\
&1805,1807,1816,1821,1827,1845,1847,1857,1876,1883,1884,1899,\\
&1902,1909,1913,1929,1937,1971,1985,1987,1989,2001,2002,2004,\\
&2007,2018,2021,2030,2032,2036,2038,2046,2071,2074,2079,2085,\\
&2088,2090,2098,2099,2101,2105;
\end{aligned}
\]
- two eighth-order rows, indices \(2106,2107\).

There is no second-order support. The row blocks are 1,461 low-order, 645 sixth-order, and seven eighth-order rows.

An independent 128-bit Arb computation reconstructs the exact rational path inputs, the matrix exponentials, the active normalized moment features, and the rational dual. For every one of the 187 physical columns it certifies
\[
a_j^\mathsf Tz+\lambda-\delta<0.
\]
All 187 interval upper endpoints are strictly negative. The largest is enclosed by
\[
[-6.1052543564944087761512888156950312261\times10^{-13}
\ \pm 2.23\times10^{-51}]<0.
\]

For any \(p\in\Delta_{187}\), averaging the column inequalities gives
\[
z^\mathsf TAp+\lambda-\delta<0.
\]
Since \(\|z\|_1=1\), Hölder's inequality yields
\[
\|Ap-y\|_\infty
\ge z^\mathsf T(y-Ap)
\ge \lambda+z^\mathsf Ty-\delta,
\]
which is the stated exact rational lower bound.

The binary64 HiGHS solve is discovery evidence only: objective \(0.46338166315236223\), independently recomputed maximum \(0.4633816631525127\), and primal-dual discovery gap \(5.83\times10^{-14}\). The theorem rests on the exact rational dual and the Arb interval checks, not on the floating-point optimizer status.

## Reproducibility and provenance

- LP transcript: \(\texttt{evidence/joint\_low\_six\_eighth\_lp\_187col\_fourth\_continuous\_escape\_n21.json}\)
- Exact dual and all 187 Arb intervals: \(\texttt{evidence/55probe\_187col\_fourth\_continuous\_escape\_dual\_certificate\_n21.json}\)
- Independent verifier: \(\texttt{verify\_187col\_fourth\_continuous\_escape\_dual\_arb.py}\)
- Reoptimizer: \(\texttt{reoptimize\_187col\_fourth\_continuous\_escape.py}\)
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45133203733
- LP transcript SHA256: \(\texttt{8a63fdbec151593e1c52cf3e55585d6c8760d6b3536564812758526ccdbbe245}\)
- Dual certificate SHA256: \(\texttt{475346510c8d0e7d52031cb21d694f91230beb60}\)
- Parent 186-column LP SHA256: \(\texttt{46b4076a61deee11c5f690caede4a9a36be763745e3747d45886a49857af9287}\)
- Parent 186-column dual SHA256: \(\texttt{555e9a9e9cb7050af595337dd16e0326d25c159e90f2893913171dfd9da99545}\)
- Fourth continuous escape certificate SHA256: \(\texttt{320d6048e63ee0e9c71481d25e99b91ab730c0cd570192128782b34c9fa812bd}\)
- Sixth-row inventory SHA256: \(\texttt{5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb}\)
- Eighth-row inventory SHA256: \(\texttt{c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0}\)
- Matrix/target SHA256: \(\texttt{3372113ef7002560e45fc64797b9c1b5abfd097d282205b30cfa3369efeb4ea9}\)

The successful workflow rechecked the frozen seed pool, orbit-enumeration regression, all four continuous-path Arb certificates, the 186-column parent dual, the 187-column LP, and the independent 187-column Arb dual verifier. The verifier provenance bug found in the preceding run was that the third escape was incorrectly compared with the 186-column parent; the corrected verifier checks the third escape against its 185-column parent and the fourth escape against the 186-column parent, and pins the fourth certificate hash in the new output.

## Scope and limitations

The result concerns only mixtures over these 187 fixed physical generators and the pinned 2,113-row mixed-order objective. The 645 sixth-order rows are selected/cut rows, not all 63,133 sixth-order dihedral orbits; the seven eighth-order rows are selected representatives, not the complete eighth-order orbit set. This is not a complete sixth/eighth orbit certificate, a sixth-only theorem, a global minimax theorem over all positive couplings, or an operational Choi-fidelity/diamond-norm guarantee.

The fourth continuous path is a strict escape from the 186-column dual, so that particular dual cannot be promoted to a full-family separator. The new 187-column dual has **not yet** been tested against the unrestricted continuous path family. A failed local search against it would not prove global separation.
