# 182-column, 2,113-row mixed-order minimax obstruction (full-sixth-cut LP)

**Status:** proved for the fixed 182-generator pool and the fixed 2,113-row design stated below.  
**Numerical discovery:** HiGHS, binary64.  
**Certificate:** exact rational dual plus independent 128-bit Arb interval verification of all 182 physical-column inequalities.

> **Naming warning.** This is the *full-sixth-cut, 2,113-row* 182-column pool. It is distinct from the pre-existing 182-column / 2,106-row mixed-order theorem in \`THEORY_182COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md\`; the physical inventories and row sets differ.

## Theorem

Let \(\mathcal P_{182}^{\mathrm{cut}}\) be the frozen set of 182 legal physical path generators recorded in **evidence/joint_low_six_eighth_lp_182col_full_sixth_cuts_n21.json**. For a probability vector \(p\in\Delta(\mathcal P_{182}^{\mathrm{cut}})\), let \(r(p)\) be the vector of normalized moment residuals on the pinned row set:

- 21 complete second-order rows;
- 1,440 complete fourth-order dihedral-orbit rows;
- 645 sixth-order dihedral-orbit rows (the original 311 rows plus 334 candidate-specific cuts);
- 7 selected eighth-order dihedral-orbit rows.

There are 2,113 rows in total. Then every probability mixture over this fixed physical pool satisfies

\[
\boxed{
\min_{p\in\Delta(\mathcal P_{182}^{\mathrm{cut}})}
\|r(p)\|_\infty
\ge
\frac{686386514539679318285297}
{1407374883553280000000000}
=0.4877069518298635\ldots
>\frac13.
}
\]

The exact certified margin above \(1/3\) is

\[
\frac{651784660065757954855891}
{4222124650659840000000000}
=0.1543736184965302\ldots.
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
- ten further canonical paths whose reduced-cost scores against the 172-column full-sixth-cut dual were independently certified strictly positive by Arb:
  \[
  (61,352,629,93,728,620,78,398,233,169).
  \]

Thus the pool contains 181 canonical paths and one continuous-path generator. The frozen canonical inventory has little-endian binary64 SHA256

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

For each of the 1,440 dihedral fourth-order orbits, with representative \(I\), define
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
r(p)=\sum_{c\in\mathcal P_{182}^{\mathrm{cut}}}p_c a(c)-y.
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
\|z\|_1=
\frac{144115188075855847}{144115188075855872}<1,
\qquad
\lambda+z^\mathsf Ty=
\frac{70285979103274681}{144115188075855872}.
\]
With rational slack
\[
\delta=\frac1{10^{10}},
\]
every one of the 182 physical columns satisfies the strict interval-certified inequality
\[
z^\mathsf T a_j+\lambda-\delta<0.
\]
The largest Arb upper endpoint among these 182 slack-shifted column expressions is
\[
-7.6906378333341585107836512615530130919\times10^{-11}<0.
\]

The rationalized dual has 49 nonzero coordinates:
- two fourth-order coordinates, zero-based row indices 233 and 868;
- 45 sixth-order coordinates;
- two eighth-order coordinates;
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
\ge
\lambda+z^\mathsf Ty-\delta,
\]
where the final inequality uses \(0<\|z\|_1<1\). This proves the theorem.

## What the 334 cuts mean

The 334 added sixth-order representatives were discovered by an exhaustive **binary64 screen** of all 63,133 \(D_{42}\) sixth-order orbits for the earlier exact 152-column candidate. A separate 128-bit Arb computation certified a strict violation for that candidate at orbit representative \((0,1,8,18,25,35)\).

The 334-row list is a finite cut set, not the complete sixth-order orbit set. The theorem above is rigorous for its stated 2,113-row objective: the row representatives and rational targets are frozen, and the dual inequalities are independently certified against all 182 physical columns. The binary64 scan is only the provenance of the cut selection; it is not used as a numerical premise in the dual proof.

The phrase **full-sixth-cut** refers to including all 334 cuts discovered in that complete binary64 screen. It does not mean that the final 182-column theorem has an Arb audit of all 63,133 sixth-order orbits.

## Reproducibility record

- Binary64 LP transcript: \`evidence/joint_low_six_eighth_lp_182col_full_sixth_cuts_n21.json\`.
- Exact rational dual and Arb intervals: \`evidence/55probe_182col_full_sixth_cut_dual_certificate_n21.json\`.
- Reoptimizer: \`reoptimize_182col_full_sixth_cut_pool.py\`.
- Independent verifier: \`verify_182col_full_sixth_cut_dual_arb.py\`.
- Workflow: [45104071580](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104071580).
- LP transcript SHA256: \`5326cbf9ae8a81765b12cbd63458f72521bc1606f0041910c5cf48cd84aaa224\`.
- Sixth-row inventory SHA256: \`5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb\`.
- Eighth-row inventory SHA256: \`c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0\`.
- Matrix/target binary64 SHA256: \`8e05c6801359f2775d00cbe7f58c271c64d0b3883439d509b8591711f7d88941\`.
- Evidence commit: [fd37e03](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fd37e03eb67b8ca1a30512c5b5807120edf4862b).

The workflow re-certifies the 172-column parent dual, screens all 1,470 unused canonical columns, verifies the ten strictly positive parent escapes with Arb, reconstructs the 182-column LP, rationalizes its dual, and interval-checks every one of the 182 column inequalities.

## Scope and unresolved questions

This theorem excludes only convex mixtures over the specified 182-generator pool for the pinned 2,113-row mixed-order objective. It does **not** prove:

1. a complete sixth-only lower bound;
2. a complete eighth-order lower bound (only seven eighth-order rows are included);
3. a lower bound for all 1,641 canonical paths or for the unrestricted continuous physical family;
4. a Choi-infidelity or diamond-distance guarantee for the inversion channel.

The next mathematical target is to price the remaining 1,460 canonical generators against this exact dual, then either extend the finite pool with strictly Arb-certified escapes or pursue a global continuous-family argument. Any constructive sub-\(1/3\) candidate must pass exact-probability Arb checks and the complete 63,133-orbit sixth-order scan before being described as a witness.
