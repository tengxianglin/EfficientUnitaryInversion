# Strict 189-column mixed-order minimax obstruction after the sixth continuous-path escape

Date: 2026-11-23

## Theorem

Let \\(\\mathcal P_{189}\\) be the ordered physical-generator pool pinned by
\`evidence/joint_low_six_eighth_lp_189col_sixth_continuous_escape_n21.json\`.
It contains 183 selected columns from the frozen 1,641-column canonical inventory
(151 base columns and 32 additional canonical columns), together with six
pairwise-distinct rational open-path generators, labelled 1641 through 1646.
The six paths have 41 strictly positive edge couplings and a final zero padding
coordinate. Their exact rational inputs are pinned by the six continuous-path
Arb certificates in the LP transcript.

For an open-path coupling vector
\\[
c=(c_0,\\ldots,c_{40},0),\qquad c_j>0\quad(0\\le j\\le40),
\\]
define the real skew-symmetric matrix
\\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,
\qquad j=0,\\ldots,40,
\\]
with all other entries zero, and set \\(R(c)=e^{K(c)}\\).

The fixed normalized moment design has 2,113 rows, ordered as:
- 1,461 complete second-/fourth-order rows (21 second-order cyclic rows and all 1,440 fourth-order dihedral-orbit rows);
- 645 pinned sixth-order rows (311 initial selected rows plus 334 cutting rows);
- seven selected eighth-order rows.

For second order, with
\\[
I_{i,d}=\\{i,(i+d)\\bmod42\\},\qquad d=1,\\ldots,21,
\\]
the feature and target are
\\[
b_d^{(2)}(c)=\\frac1{42}\\sum_{i=0}^{41}
\\det R(c)_{I_{i,d},I_{i,d}},
\qquad
\\tau_d^{(2)}=\\frac{(-1)^{d+1}}{41}.
\\]
For \\(k\\in\\{4,6,8\\}\\), a pinned representative \\(I\\) contributes
\\[
b_I^{(k)}(c)=
\\frac1{|\\mathcal O_k(I)|}
\\sum_{J\\in\\mathcal O_k(I)}
\\det R(c)_{J,J},
\\qquad
\\mathcal O_k(I)=D_{42}\\cdot I,
\\]
with target
\\[
\\tau_I^{(k)}
=(-1)^{\\sum_{i\\in I}(i\\bmod2)+k/2}
\\frac{\\binom{21}{k/2}}{\\binom{42}{k}}.
\\]
The row scales are
\\[
s_2=\\frac1{41},\qquad
s_4=\\frac{\\binom{21}{2}}{\\binom{42}{4}},\qquad
s_6=\\frac5{19721},\qquad
s_8=\\frac1{19721}.
\\]
Let \\(A\\in\\mathbb R^{2113\\times189}\\) and \\(y\\in\\mathbb R^{2113}\\)
be the feature and target arrays after division by their corresponding row
scales.

**Claim.** Every probability mixture supported on this fixed 189-generator pool
obeys
\\[
\\boxed{
\\min_{p\\in\\Delta_{189}}\\|Ap-y\\|_\\infty
\\ge
\\frac{209460614862602549049621931}
{461168601845037806900000000}
=0.4541953073661022\\ldots
>\\frac13.
}
\\]
The exact certified gap above \\(1/3\\) is
\\[
\\frac{167213242742769840248865793}
{1383505805535113420700000000}
=0.12086197403276885\\ldots.
\\]

This is a finite-pool, mixed-order minimax theorem.

## Exact rational dual and proof

The machine-readable exact certificate is
\`evidence/55probe_189col_sixth_continuous_escape_dual_certificate_n21.json\`.
It contains an exact rational vector \\(z\\in\\mathbb Q^{2113}\\) and scalar
\\(\\lambda\\), with
\\[
\\|z\\|_1=1,
\\qquad
\\lambda=\\frac{6348338075111778304}{4611686018450378069},
\\]
and
\\[
\\lambda+z^\\mathsf T y
=\\frac{2094606194742885675}{4611686018450378069}.
\\]
The certified slack is
\\[
\\delta=\\frac1{10^8}.
\\]
The dual has 57 nonzero coordinates:
- one low-order row, zero-based index 1413;
- 54 sixth-order rows, zero-based indices
\\[
\\begin{aligned}
&1675,1716,1738,1765,1766,1767,1777,1779,1781,1784,1790,1795,1796,1805,\\
&1807,1816,1827,1845,1847,1876,1883,1899,1902,1927,1929,1937,1942,1949,\\
&1963,1971,1975,1983,1985,1988,1989,1991,2001,2002,2004,2007,2018,2021,\\
&2032,2038,2051,2069,2071,2079,2085,2088,2090,2098,2099,2101;
\\end{aligned}
\\]
- two eighth-order rows, indices 2106 and 2107.

There is no second-order support. In particular, this is not a sixth-only
certificate: the nonzero low-order coordinate is a fourth-order row, and the
two eighth-order coordinates are part of the separating functional.

An independent 128-bit Arb calculation reconstructs the exact rational dual
and evaluates every one of the 189 physical columns. For each column
\\(a_j\\), it certifies
\\[
a_j^\\mathsf Tz+\\lambda-\\delta<0.
\\]
All 189 slack-shifted interval upper endpoints are strictly negative. The
largest upper endpoint is enclosed by
\\[
[-8.9418568666754042859549486269839336820\\times10^{-9}
\\;\\pm3.14\\times10^{-47}]<0.
\\]

For any \\(p\\in\\Delta_{189}\\), averaging the 189 column inequalities gives
\\[
z^\\mathsf TAp+\\lambda-\\delta<0.
\\]
Consequently,
\\[
\\|Ap-y\\|_\\infty
\\ge z^\\mathsf T(y-Ap)
\\ge \\lambda+z^\\mathsf Ty-\\delta,
\\]
where the first inequality follows from \\(\\|z\\|_1=1\\) and Hölder's
inequality. The right-hand side is exactly the rational lower bound displayed
in the theorem.

The binary64 HiGHS solve is discovery evidence only: objective
0.454195317365923, independently recomputed maximum 0.4541953174059339,
support size 57, and primal-dual discovery gap
2.443489854897507\\times10^{-12}. The theorem rests on the exact rational dual
and the 128-bit Arb interval checks, not on the floating-point solver status.

## Reproducibility and provenance

- LP transcript: \`evidence/joint_low_six_eighth_lp_189col_sixth_continuous_escape_n21.json\`
- Exact dual and all 189 Arb intervals: \`evidence/55probe_189col_sixth_continuous_escape_dual_certificate_n21.json\`
- Independent verifier: \`verify_189col_sixth_continuous_escape_dual_arb.py\`
- Reoptimizer: \`reoptimize_189col_sixth_continuous_escape.py\`
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45145380760
- Evidence commit: [09fc105](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/09fc1050a3721ef6f00ff51cec73c690a6a9b458)
- LP transcript SHA256: \`e73311bdf1a683620417dcc2cd7c18f25197d8451f1be76e7ed76c4de31424de\`
- Parent 188-column LP SHA256: \`f512d8fa40887d84a3274c7dd5f4716b841573e90adcd2ff7f12d191c2bf8297\`
- Parent 188-column dual certificate SHA256: \`eed80945f8ae5875c7fbad6f4d760c934654eaf44ce22a4bf373f4358ccedef5\`
- Sixth continuous-path Arb certificate SHA256: \`31749b9038749e77371b47fc5a45a87c5d7e9b7580bfedace9894ab36f6b8ca7\`
- Frozen seed-pool SHA256: \`93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315\`
- Canonical inventory SHA256: \`f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98\`
- Sixth-row inventory SHA256: \`5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb\`
- Eighth-row inventory SHA256: \`c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0\`
- Matrix/target binary64 SHA256: \`51ad203ee55f677f44cc3031eed411d370003278e1c10fc2c81880bb0aa30ccb\`

Reproduce in the pinned workflow environment with:
\`\`\`bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python verify_continuous_path_dual_escape_arb.py
python verify_184col_continuous_dual_escape_arb.py
python verify_185col_continuous_dual_escape_arb.py
python verify_186col_continuous_dual_escape_arb.py
python verify_187col_continuous_dual_escape_arb.py
python verify_188col_fifth_continuous_escape_dual_arb.py
python verify_188col_continuous_dual_escape_arb.py
python reoptimize_189col_sixth_continuous_escape.py
python verify_189col_sixth_continuous_escape_dual_arb.py
\`\`\`

## Scope and limitations

The result concerns every convex mixture over these exact 189 pinned physical
generators and the fixed 2,113-row mixed-order objective. The 645 sixth-order
rows are selected/cut rows, not all 63,133 sixth-order dihedral orbits; the
seven eighth-order rows are selected representatives, not all 1,408,185
eighth-order orbits. The theorem is not a sixth-only result, a complete
sixth/eighth orbit audit, a no-go theorem for all positive 41-edge couplings,
or an operational Choi-fidelity/diamond-norm guarantee.

The six continuous paths are certified escapes from the 151-, 184-, 185-,
186-, 187-, and 188-column duals, respectively. The new 189-column dual
has not yet been tested against the unrestricted positive 41-edge path family.
A positive continuous-path pricing value would refute global separation by
this particular 189-column dual; failure of a local search would not prove
global separation.
