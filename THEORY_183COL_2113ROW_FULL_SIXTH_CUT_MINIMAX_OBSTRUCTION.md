# 183-column, 2,113-row mixed-order minimax obstruction (full-sixth-cut LP)

**Status:** proved for the fixed 183-generator pool and the fixed 2,113-row design stated below.  
**Numerical discovery:** HiGHS, binary64.  
**Certificate:** exact rational dual plus independent 128-bit Arb interval verification of all 183 physical-column inequalities.

> **Naming warning.** This theorem belongs to the full-sixth-cut, 2,113-row column-generation branch descended from the 172- and 182-column cut pools. It is distinct from the pre-existing 182-column / 2,106-row mixed-order theorem; column count alone does not identify a pool or an objective.

## Theorem

Let \(\mathcal P_{183}^{\mathrm{cut}}\) be the frozen set of 183 legal physical path generators recorded in **evidence/joint_low_six_eighth_lp_183col_full_sixth_cuts_n21.json**. For a probability vector \(p\in\Delta(\mathcal P_{183}^{\mathrm{cut}})\), let \(r(p)\) be the vector of normalized moment residuals on the pinned row set:

- 21 complete second-order rows;
- 1,440 complete fourth-order dihedral-orbit rows;
- 645 sixth-order dihedral-orbit rows (the original 311 rows plus 334 candidate-specific cuts);
- 7 selected eighth-order dihedral-orbit rows.

There are 2,113 rows in total. Then every probability mixture over this fixed physical pool satisfies

\[
\boxed{
\min_{p\in\Delta(\mathcal P_{183}^{\mathrm{cut}})}
\|r(p)\|_\infty
\ge
\frac{22487487405975385031571661473}
{46116860184283385270000000000}
=0.48761965398587814\ldots
>\frac13.
}
\]

The exact certified margin above \(1/3\) is

\[
\frac{21345602033642769824714984419}
{138350580552850155810000000000}
=0.1542863206525448\ldots.
\]

This is a **mixed-order finite-pool theorem**. It is not a sixth-only theorem and does not establish a lower bound for the unrestricted continuous physical family.

## Physical pool

For a coupling vector \(c=(c_0,\ldots,c_{40},0)\), define the real skew-symmetric path generator
\[
K(c)_{j,j+1}=2c_j,\qquad
K(c)_{j+1,j}=-2c_j,\quad j=0,\ldots,40,
\]
with all other entries zero, and set \(R(c)=e^{K(c)}\).

The frozen physical pool consists of:

- 151 canonical base paths, with zero-based indices in the frozen 1,641-column canonical inventory;
- one exact-rational continuous-path escape generator, with augmented column index 1641, specified by \`evidence/candidate_joint_input_152col_continuous_escape_n21.json\` and independently certified in \`evidence/continuous_path_dual_escape_arb_n21.json\`;
- twenty canonical paths already present in the 172-column parent pool:
  \[
  (1603,886,565,682,472,525,434,487,80,145,
  1580,195,364,424,448,221,324,517,420,447);
  \]
- ten further canonical paths strictly priced against the 172-column full-sixth-cut dual:
  \[
  (61,352,629,93,728,620,78,398,233,169);
  \]
- one further canonical path, column \(544\), whose reduced-cost score against the 182-column full-sixth-cut dual was independently certified strictly positive by Arb.

Thus the pool contains 182 canonical paths and one continuous-path generator. The frozen canonical inventory has little-endian binary64 SHA256

\[
\texttt{f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98}.
\]

The frozen \(1,600\times42\) seed-pool SHA256 is

\[
\texttt{93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315}.
\]

## Moment rows and normalization

Let \(\mathcal O_k(I)=\{gI:g\in D_{42}\}\) denote the dihedral orbit of a \(k\)-subset.

For the 21 cyclic second-order rows, define
\[
I_{i,d}=\{i,(i+d)\bmod42\},\qquad d=1,\ldots,21,
\]
\[
b_d^{(2)}(c)=\frac1{42}\sum_{i=0}^{41}
\det R(c)_{I_{i,d},I_{i,d}},
\qquad
\tau_d^{(2)}=\frac{(-1)^{d+1}}{41}.
\]

For each of the 1,440 fourth-order dihedral orbits, with representative \(I\), define
\[
b_I^{(4)}(c)=\frac1{|\mathcal O_4(I)|}
\sum_{J\in\mathcal O_4(I)}\det R(c)_{J,J},
\]
\[
\tau_I^{(4)}
=(-1)^{\sum_{i\in I}(i\bmod2)}
\frac{\binom{21}{2}}{\binom{42}{4}}.
\]

For each of the 645 pinned sixth-order orbit representatives \(I\), define
\[
b_I^{(6)}(c)=\frac1{|\mathcal O_6(I)|}
\sum_{J\in\mathcal O_6(I)}\det R(c)_{J,J},
\]
\[
\tau_I^{(6)}
=(-1)^{\sum_{i\in I}(i\bmod2)+3}
\frac{\binom{21}{3}}{\binom{42}{6}}.
\]

For the seven selected eighth-order representatives \(I\), define
\[
b_I^{(8)}(c)=\frac1{|\mathcal O_8(I)|}
\sum_{J\in\mathcal O_8(I)}\det R(c)_{J,J},
\]
\[
\tau_I^{(8)}
=(-1)^{\sum_{i\in I}(i\bmod2)+4}
\frac{\binom{21}{4}}{\binom{42}{8}}.
\]

The row scales are
\[
s_2=\frac1{41},\qquad
s_4=\frac{\binom{21}{2}}{\binom{42}{4}},\qquad
s_6=\frac5{19721},\qquad
s_8=\frac1{19721}.
\]
The normalized feature column \(a(c)\) contains \(b^{(k)}(c)/s_k\) in the row order above, and the target vector \(y\) contains the corresponding \(\tau^{(k)}/s_k\). For a probability distribution \(p\) on the fixed pool,
\[
r(p)=\sum_{c\in\mathcal P_{183}^{\mathrm{cut}}}p_c a(c)-y.
\]

The sixth-row inventory is frozen by SHA256
\[
\texttt{5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb},
\]
and the seven-row eighth inventory by SHA256
\[
\texttt{c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0}.
\]

## Dual certificate and proof

The 128-bit Arb certificate reconstructs an exact rational dual vector \(z\) and scalar \(\lambda\). Its exact norm and objective are
\[
\|z\|_1=1,
\qquad
\lambda=
\frac{6860434759487045632}{4611686018428338527},
\qquad
\lambda+z^\mathsf Ty=
\frac{2248748741058707105}{4611686018428338527}.
\]
With rational slack
\[
\delta=\frac1{10^{10}},
\]
every one of the 183 physical columns satisfies the strict interval-certified inequality
\[
z^\mathsf T a_j+\lambda-\delta<0.
\]
The largest Arb upper endpoint among these 183 slack-shifted column expressions is
\[
-2.7990374260551989388860683521287060874\times10^{-11}<0.
\]

The rationalized dual has 50 nonzero coordinates:
- two fourth-order coordinates, zero-based row indices 233 and 868;
- 46 sixth-order coordinates, zero-based row indices
  \[
  (1675,1712,1716,1765,1767,1779,1782,1790,1794,1805,
  1821,1827,1830,1847,1865,1876,1879,1883,1884,1913,
  1922,1929,1963,1971,1985,1987,1989,1990,2001,2002,
  2006,2011,2018,2032,2033,2038,2051,2071,2079,2085,
  2088,2090,2098,2099,2101,2105);
  \]
- two eighth-order coordinates, zero-based row indices 2106 and 2107;
- no second-order coordinates.

In particular, this is a **mixed-order** certificate. The presence of fourth- and eighth-order coordinates precludes describing it as a sixth-only theorem.

For any probability vector \(p\), the certified column inequalities and \(\sum_jp_j=1\) give
\[
z^\mathsf T A p+\lambda-\delta\le0,
\]
hence
\[
z^\mathsf T(y-Ap)\ge\lambda+z^\mathsf Ty-\delta.
\]
The right-hand side is the positive exact rational lower bound displayed in the theorem. By Hölder's inequality,
\[
\|Ap-y\|_\infty
\ge
\frac{|z^\mathsf T(y-Ap)|}{\|z\|_1}
=
\lambda+z^\mathsf Ty-\delta,
\]
where the equality uses the exact norm \(\|z\|_1=1\). This proves the theorem.

## What the 334 cuts mean

The 334 added sixth-order representatives were discovered by an exhaustive **binary64 screen** of all 63,133 \(D_{42}\) sixth-order orbits for the earlier exact 152-column candidate. A separate 128-bit Arb computation certified a strict violation for that candidate at orbit representative \((0,1,8,18,25,35)\).

The 334-row list is a finite cut set, not the complete sixth-order orbit set. The theorem above is rigorous for its stated 2,113-row objective: the row representatives and rational targets are frozen, and the dual inequalities are independently certified against all 183 physical columns. The binary64 scan is only the provenance of the cut selection; it is not used as a numerical premise in the dual proof.

The phrase **full-sixth-cut** refers to including all 334 cuts discovered in that complete binary64 screen. It does not mean that the final 183-column theorem has an Arb audit of all 63,133 sixth-order orbits.

## Reproducibility record

- Binary64 LP transcript: \`evidence/joint_low_six_eighth_lp_183col_full_sixth_cuts_n21.json\`.
- Exact rational dual and Arb intervals: \`evidence/55probe_183col_full_sixth_cut_dual_certificate_n21.json\`.
- Reoptimizer: \`reoptimize_183col_full_sixth_cut_pool.py\`.
- Independent verifier: \`verify_183col_full_sixth_cut_dual_arb.py\`.
- Workflow: [45105045420](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105045420).
- LP transcript SHA256: \`6ee01897aca66e60cb082f5553ee545e694e58a6de2fd9585eb92d8f9a2b8fe0\`.
- Parent 182-column LP SHA256: \`5326cbf9ae8a81765b12cbd63458f72521bc1606f0041910c5cf48cd84aaa224\`.
- Parent 182-column dual certificate SHA256: \`ec35a7c1f9bf5b164e3363767ae3543a7511321519ced190cb305e9cebcdfa3e\`.
- Pricing screen SHA256: \`7a61a7217ccf65865ab80fb49910c5ed3f7124c444b2065bde63e9815acb53d5\`.
- Arb pricing SHA256: \`3e7884f8ac8f104328231168fa7221f06cdf9f61f1c8f2e72eec78a569ef59e8\`.
- Sixth-row inventory SHA256: \`5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb\`.
- Eighth-row inventory SHA256: \`c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0\`.
- Matrix/target binary64 SHA256: \`19da73b11f2e124c8dd745e1a80812a55afced2e3cab453dd57977e35da0c5a8\`.
- Evidence commit: [b551f64](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b551f64603bb071aed303f5a2f879e53c61d4de9).

The workflow re-certifies the 182-column parent dual, repeats the full canonical pricing and strict Arb verification of column 544, reconstructs the 183-column LP, rationalizes its dual, and interval-checks every one of the 183 column inequalities.

## Scope and unresolved questions

This theorem excludes only convex mixtures over the specified 183-generator pool for the pinned 2,113-row mixed-order objective. It does **not** prove:

1. a complete sixth-only lower bound;
2. a complete eighth-order lower bound (only seven eighth-order rows are included);
3. a lower bound for all 1,641 canonical paths or for the unrestricted continuous physical family;
4. a Choi-infidelity or diamond-distance guarantee for the inversion channel.

The next mathematical target is to price the remaining 1,459 canonical generators against this exact dual, then either extend the finite pool with strictly Arb-certified escapes or pursue a global continuous-family argument. Any constructive sub-\(1/3\) candidate must pass exact-probability Arb checks and the complete 63,133-orbit sixth-order scan before being described as a witness.
