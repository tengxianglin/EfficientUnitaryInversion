# Strict 188-column mixed-order minimax obstruction after the fifth continuous escape

Date: 2026-11-23

## Theorem

Let \\(\\mathcal P_{188}\\) be the ordered set of 188 physical generators pinned by the LP transcript
``evidence/joint_low_six_eighth_lp_188col_fifth_continuous_escape_n21.json``.
It consists of the 151-column canonical base, the first exact-rational continuous path (column 1641), 32 additional canonical generators, and four further exact-rational continuous paths (columns 1642--1645). Equivalently, it contains 183 selected members of the frozen 1,641-column canonical inventory and five continuous open-path generators. The full ordered column list and its hash are recorded in the LP transcript and dual certificate.

The frozen 1,600-by-42 seed pool has little-endian binary64 SHA256
``93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315``,
and the full canonical inventory has little-endian binary64 SHA256
``f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98``.

For an open path coupling vector \\(c=(c_0,\\ldots,c_{40},0)\\), define
\\[
K(c)_{j,j+1}=2c_j,\\qquad K(c)_{j+1,j}=-2c_j,
\\qquad j=0,\\ldots,40,
\\]
with all other entries zero, and \\(R(c)=\\exp K(c)\\). Each of the five continuous paths in \\(\\mathcal P_{188}\\) has 41 strictly positive open-edge couplings; their exact rational inputs are pinned by the five Arb escape certificates listed below.

The 2,113 normalized residual rows are ordered as:
- 21 complete second-order cyclic rows and all 1,440 fourth-order dihedral-orbit rows (1,461 complete low-order rows);
- 645 pinned sixth-order orbit rows (311 selected rows plus 334 cuts);
- seven selected eighth-order orbit rows.

Let \\(D_{42}\\) be the order-84 dihedral group and \\(\\mathcal O_k(I)=\\{gI:g\\in D_{42}\\}\\). For each physical path \\(c_j\\), write \\(R_j=\\exp K(c_j)\\). The second-order rows use
\\[
I_{i,d}=\\{i,(i+d)\\bmod 42\\},\\quad d=1,\\ldots,21,
\\]
\\[
b_d^{(2)}(c_j)=\\frac1{42}\\sum_{i=0}^{41}\\det (R_j)_{I_{i,d},I_{i,d}},
\\qquad
\\tau_d^{(2)}=\\frac{(-1)^{d+1}}{41}.
\\]
For \\(k\\in\\{4,6,8\\}\\), each pinned representative \\(I\\) contributes
\\[
b_I^{(k)}(c_j)=\\frac1{|\\mathcal O_k(I)|}
\\sum_{J\\in\\mathcal O_k(I)}\\det (R_j)_{J,J},
\\]
with exact ideal target
\\[
\\tau_I^{(k)}
=(-1)^{\\sum_{i\\in I}(i\\bmod 2)+k/2}
\\frac{\\binom{21}{k/2}}{\\binom{42}{k}}.
\\]
The feature and target vectors are divided by the row scales
\\[
s_2=\\frac1{41},\\qquad
s_4=\\frac{\\binom{21}{2}}{\\binom{42}{4}},\\qquad
s_6=\\frac5{19721},\\qquad
s_8=\\frac1{19721}.
\\]
For a probability vector \\(p\\in\\Delta_{188}\\), let \\(r(p)=A p-y\\).

**Claim.** Every probability mixture supported on this fixed 188-generator pool obeys
\\[
\\boxed{
\\min_{p\\in\\Delta_{188}}\\|A p-y\\|_\\infty
\\ge
\\frac{66090580242847531496409753}
{144115188075855872000000000}
=0.4585955243527862\\ldots>\\frac13.
}
\\]
The exact certified margin above \\(1/3\\) is
\\[
\\frac{54156552652686722489229259}
{432345564227567616000000000}
=0.1252621910194529\\ldots.
\\]

This is a mixed-order finite-pool theorem.

## Exact rational dual and proof

The machine-readable certificate is
``evidence/55probe_188col_fifth_continuous_escape_dual_certificate_n21.json``.
It supplies an exact rational vector \\(z\\in\\mathbb Q^{2113}\\), an exact rational \\(\\lambda\\), and slack
\\[
\\delta=10^{-9}.
\\]
The exact normalization is
\\[
\\|z\\|_1=
\\frac{73786976294791983323}{73786976294838206464}<1,
\\]
and
\\[
\\lambda=\\frac{6287284550233029}{4503599627370496}.
\\]
The certificate's exact dual objective is
\\[
\\lambda+z^\\mathsf T y
=\\frac{33838377158124912421}{73786976294838206464},
\\]
so subtracting \\(\\delta\\) gives the displayed lower bound.

The dual has 52 nonzero coordinates:
- three fourth-order rows, zero-based indices \\(233,1265,1413\\);
- 47 sixth-order rows, zero-based indices
\\[
\\begin{aligned}
&1675,1716,1738,1756,1766,1767,1779,1781,1782,1784,1790,1794,\\
&1805,1814,1816,1827,1830,1845,1847,1883,1899,1902,1929,1937,\\
&1963,1971,1983,1985,1988,1989,2004,2006,2018,2021,2032,2038,\\
&2046,2051,2071,2074,2079,2085,2088,2090,2098,2099,2101;
\\end{aligned}
\\]
- two eighth-order rows, indices \\(2106,2107\\).

There is no second-order support. The row blocks contain 1,461 low-order, 645 sixth-order, and seven eighth-order rows.

An independent 128-bit Arb calculation reconstructs the exact rational dual and every normalized feature for all 188 physical columns. For every column \\(a_j\\), it certifies
\\[
a_j^\\mathsf T z+\\lambda-\\delta<0.
\\]
All 188 interval upper endpoints are strictly negative. The largest is enclosed by
\\[
[-8.8068030053955477431256232530676661255\\times10^{-10}
\\;\\pm 1.19\\times10^{-48}]<0.
\\]

For any \\(p\\in\\Delta_{188}\\), averaging the column inequalities gives
\\[
z^\\mathsf T A p+\\lambda-\\delta<0.
\\]
Since \\(\\|z\\|_1<1\\), Hölder's inequality implies
\\[
\\|A p-y\\|_\\infty
\\ge z^\\mathsf T(y-Ap)
\\ge \\lambda+z^\\mathsf T y-\\delta,
\\]
which is the stated exact rational lower bound.

The binary64 HiGHS solve is discovery evidence only: objective \\(0.4585955253523888\\), independently recomputed maximum \\(0.4585955253531613\\), support size 52, and primal-dual discovery gap \\(3.98\\times10^{-13}\\). The theorem rests on the exact rational dual and Arb interval checks, not on the floating-point optimizer status.

## Reproducibility and provenance

- LP transcript: ``evidence/joint_low_six_eighth_lp_188col_fifth_continuous_escape_n21.json``
- Exact dual and all 188 Arb intervals: ``evidence/55probe_188col_fifth_continuous_escape_dual_certificate_n21.json``
- Independent verifier: ``verify_188col_fifth_continuous_escape_dual_arb.py``
- Reoptimizer: ``reoptimize_188col_fifth_continuous_escape.py``
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45135692203
- LP transcript SHA256: ``f512d8fa40887d84a3274c7dd5f4716b841573e90adcd2ff7f12d191c2bf8297``
- Parent 187-column LP SHA256: ``8a63fdbec151593e1c52cf3e55585d6c8760d6b3536564812758526ccdbbe245``
- Parent 187-column dual certificate SHA256: ``b762ad6b9eee7fb0e632143558339ecc0d602210da2ab94ad41bed9d69ef7a87``
- First through fifth continuous escape Arb certificate SHA256 values, in order:
  - ``9e85d7f617baaa5bee371297e9f94716c21c7404f8349def2ef376dafb20d59e``
  - ``d40aeaa3c5c5a814a47f046ff96f892e4bf98069fa59330ffa4c7e343674543c``
  - ``71e7581990b50f1dd8ad22a11190ac66e016318d925022f250a51253166e7a4e``
  - ``320d6048e63ee0e9c71481d25e99b91ab730c0cd570192128782b34c9fa812bd``
  - ``723709c44c518c44a86a8b06d78065276bca4e3582de92e1603f78ba6b3da38e``
- Sixth-row inventory SHA256: ``5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb``
- Eighth-row inventory SHA256: ``c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0``
- Matrix/target SHA256: ``ba1f39e80731603c7eb08f227dda3919eea779b6e0506dff1f427b2770468863``
- Successful workflow run: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45135692203

The workflow rechecked the frozen seed pool, orbit-enumeration regression, all five prior continuous-path Arb certificates, the 187-column parent dual, the 188-column LP, and the independent 188-column Arb dual verifier before committing the evidence.

## Scope and limitations

The result concerns only mixtures over these 188 fixed physical generators and the pinned 2,113-row mixed-order objective. The 645 sixth-order rows are selected/cut rows, not all 63,133 sixth-order dihedral orbits; the seven eighth-order rows are selected representatives, not the complete eighth-order orbit set. This is not a complete sixth/eighth orbit certificate, a sixth-only theorem, a global minimax theorem over all positive couplings, or an operational Choi-fidelity/diamond-norm guarantee.

The fifth continuous path is a strict escape from the 187-column dual, so that particular dual cannot be promoted to a full-family separator. The new 188-column dual has **not yet** been tested against the unrestricted positive 41-edge path family. The next decisive action is a differentiable search against this 188-column dual, followed by exact-rational 128-bit Arb verification of any positive candidate. Failure of a local search will not prove global separation.
