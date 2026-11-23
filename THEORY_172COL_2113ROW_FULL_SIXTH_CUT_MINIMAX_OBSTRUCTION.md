# 172-column, 2,113-row mixed-order minimax obstruction

**Status:** proved for the fixed physical pool and fixed row design stated below.  
**Numerical discovery:** HiGHS, binary64.  
**Certificate:** exact rational dual plus 128-bit Arb interval verification of all 172 physical-column inequalities.

## Theorem

Let \(\mathcal P_{172}\) be the frozen set of 172 legal physical path generators recorded in **evidence/joint_low_six_eighth_lp_172col_full_sixth_cuts_n21.json**. For a probability vector \(p\in\Delta(\mathcal P_{172})\), let \(r(p)\) be the vector of normalized moment residuals on the pinned row set:

- 21 complete second-order rows;
- 1,440 complete fourth-order rows;
- 645 sixth-order dihedral-orbit rows (the original 311 rows plus 334 candidate-specific cuts);
- 7 selected eighth-order dihedral-orbit rows.

There are 2,113 rows in total. Then every probability mixture over this fixed physical pool satisfies

\[
\boxed{
\min_{p\in\Delta(\mathcal P_{172})}
\|r(p)\|_\infty
\ge
\frac{4409808392781637575337133}
{9007199254740992000000000}
=0.489587081185143\ldots
>\frac13.
}
\]

The exact certified margin above \(1/3\) is

\[
\frac{4222225923603920726011399}
{27021597764222976000000000}
=0.15625374785180968\ldots.
\]

This is a **mixed-order finite-pool theorem**. It is not a sixth-only theorem and does not establish a lower bound for the unrestricted continuous physical family.

## Physical pool

The frozen physical pool consists of:

- 151 canonical base paths;
- one exact-rational continuous-path escape generator, with index 1641 in the augmented column convention;
- ten canonical paths added after pricing the 152-column cut dual:
  \(1603,886,565,682,472,525,434,487,80,145\);
- ten further canonical paths whose reduced-cost scores against the 162-column cut dual were independently certified strictly positive by Arb:
  \(1580,195,364,424,448,221,324,517,420,447\).

Thus the pool contains 171 canonical paths and one continuous-path generator. The frozen canonical inventory contains 1,641 columns and has little-endian binary64 SHA256

\[
\texttt{f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98}.
\]

The frozen 1,600-by-42 seed pool SHA256 is

\[
\texttt{93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315}.
\]

## Dual certificate and proof

The 128-bit Arb certificate reconstructs an exact rational dual vector \(z\) and scalar \(\lambda\). Its exact norm and objective are

\[
\|z\|_1=
\frac{4611686018424741463}{4611686018427387904}<1,
\qquad
\lambda+z^Ty=
\frac{2257821901715884457}{4611686018427387904}.
\]

With rational slack \(\delta=10^{-9}\), every one of the 172 physical columns satisfies the strict interval-certified inequality

\[
z^T a_j+\lambda-\delta\le0.
\]

The largest Arb upper endpoint among these 172 slack-shifted column expressions is

\[
-7.0535517948488008\times10^{-10}<0.
\]

For any probability vector \(p\), convexity gives
\[
z^T A p+\lambda-\delta\le0.
\]
Consequently
\[
z^T(y-Ap)\ge\lambda+z^Ty-\delta.
\]
By Hölder's inequality and \(\|z\|_1<1\),
\[
\|Ap-y\|_\infty
\ge
\frac{|z^T(y-Ap)|}{\|z\|_1}
\ge
\lambda+z^Ty-\delta,
\]
which is exactly the rational lower bound in the theorem.

The rationalized dual has 48 nonzero coordinates: one fourth-order coordinate (row index 233), 45 sixth-order coordinates, and two eighth-order coordinates. It has no second-order support. The presence of the fourth- and eighth-order coordinates is why the result must be labelled mixed-order.

## What the 334 cuts mean

The 334 added sixth-order representatives were discovered by an exhaustive **binary64 screen** of all 63,133 \(D_{42}\) sixth-order orbits for the earlier exact 152-column candidate. A separate 128-bit Arb computation then certified a strict violation for that candidate at orbit representative \((0,1,8,18,25,35)\).

The 334-row list is a finite cut set, not the complete sixth-order orbit set. The theorem above is nevertheless rigorous for its stated 2,113-row objective: the row representatives and rational targets are frozen, and the dual inequalities are independently certified against all 172 physical columns. The binary64 scan is only the provenance of the cut selection; it is not used as a numerical premise in the dual proof.

## Reproducibility record

- Binary64 LP transcript: **evidence/joint_low_six_eighth_lp_172col_full_sixth_cuts_n21.json**
- Exact rational dual and Arb intervals: **evidence/55probe_172col_full_sixth_cut_dual_certificate_n21.json**
- Reoptimizer: **reoptimize_172col_full_sixth_cut_pool.py**
- Independent verifier: **verify_172col_full_sixth_cut_dual_arb.py**
- Workflow: [45102666550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45102666550)
- LP transcript SHA256: **9ad6881a32409e091c0354e4d5bd4f013d2343ca456e0a3bef81a911e171dc44**
- Sixth-row inventory SHA256: **5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb**
- Eighth-row inventory SHA256: **c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0**
- Matrix/target binary64 SHA256: **cafa34b92ec68b504772c4e52724d9ac9d9adccb15d72e99d25543625fff4a6b**
- Certificate commit: [ae797e9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/ae797e92557df52f4f419e9215f9029ccbd1a450)

The workflow reruns the 162-column parent Arb certificate, screens the complete frozen canonical pool, verifies the ten strictly positive parent escapes, reconstructs the 172-column LP, rationalizes its dual, and interval-checks every one of the 172 column inequalities.

## Scope and unresolved questions

This theorem excludes only convex mixtures over the specified 172-generator pool for the pinned 2,113-row mixed-order objective. It does **not** prove:

1. a complete sixth-only lower bound (the dual has fourth- and eighth-order support);
2. a complete eighth-order lower bound (only seven eighth-order rows are included);
3. a lower bound for all 1,641 canonical paths or for the unrestricted continuous physical family;
4. a Choi-infidelity or diamond-distance guarantee for the inversion channel.

The next mathematical target is either a genuinely complete continuous-family separation argument or a constructive ensemble that survives a complete sixth-order audit. Any sub-\(1/3\) candidate must pass exact-probability Arb checks and the complete 63,133-orbit sixth-order scan before being described as a witness.
