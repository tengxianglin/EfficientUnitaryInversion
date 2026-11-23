# 184-column, 2,113-row mixed-order minimax obstruction

**Status:** proved for the fixed 184-generator pool and the pinned 2,113-row design.  
**Discovery:** SciPy/HiGHS, binary64.  
**Certificate:** exact rational dual, independently verified with 128-bit Arb on all 184 physical columns.

## Theorem

Let P184 be the frozen set of 184 legal path generators specified, in exact order, by the LP transcript at evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json. For any probability vector p on P184, let r(p) be the normalized residual vector on these 2,113 pinned rows:

- 21 complete second-order rows;
- 1,440 complete fourth-order dihedral-orbit rows;
- 645 sixth-order dihedral-orbit rows (311 original rows plus 334 candidate-specific cuts);
- seven selected eighth-order dihedral-orbit rows.

Then
\[
\boxed{
\min_{p\in\Delta(P184)} \|r(p)\|_\infty
\ge
\frac{22487122319210016751569973413}
{46116860184300265870000000000}
=0.48761173742841646\ldots>\frac13.
}
\]
The exact margin above one third is
\[
\frac{21344506773329784384709920239}
{138350580552900797610000000000}
=0.15427840409508313\ldots.
\]

This is a mixed-order finite-pool theorem. It is not a sixth-only theorem, a complete sixth/eighth-orbit theorem, or a lower bound for the unrestricted continuous physical family.

The HiGHS discovery objective was 0.487611737529284, the independently recomputed maximum was 0.48761173752942266, support size was 50, and the primal-dual discovery gap was 5.885292253537955e-13. These are diagnostics, not the proof.

## Physical pool and row design

For c=(c0,...,c40,0), define the real skew-symmetric path generator by
\[
K(c)_{j,j+1}=2c_j,\quad K(c)_{j+1,j}=-2c_j,\quad j=0,\ldots,40,
\]
with all other entries zero, and R(c)=exp(K(c)).

The pool contains 151 base canonical paths, one exact-rational continuous-path escape generator at augmented column index 1641, and 32 additional canonical paths:
\[
(1603,886,565,682,472,525,434,487,80,145,
1580,195,364,424,448,221,324,517,420,447,
61,352,629,93,728,620,78,398,233,169,544,332).
\]
Thus 151+1+32=184. The exact base-column labels, column order, and coupling data are pinned in the LP transcript.

The row definitions and normalizations are the same as in THEORY_183COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md:
- second order: 21 cyclic distances, scale s2=1/41;
- fourth order: all 1,440 D42 orbit representatives, scale s4=C(21,2)/C(42,4);
- sixth order: the pinned 645 representatives, scale s6=5/19721;
- eighth order: seven pinned representatives, scale s8=1/19721.

For a k-subset I, each higher-order feature is the average of the principal minors det R[J,J] over the D42 orbit of I. The target signs and rational values are pinned row-by-row in the LP transcript and are checked by the independent Arb verifier. The 645 sixth rows are exactly the original 311 plus the 334 cuts; they are not all 63,133 sixth-order orbits.

Frozen hashes:
- 1,600-by-42 seed pool: 93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315;
- 1,641-column canonical inventory, little-endian binary64: f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98;
- sixth-row inventory: 5ea65e5c906046cf82253202563b01e86a3aeddbdc1ff2ac4d01127147132abb;
- eighth-row inventory: c96eb71f87e5396658d73c5589be00b3f82cfcda46f8b2b71fc168b2391a93d0;
- matrix/target, little-endian binary64: 4a365613ce03ecb5a683affb3fc291ce277978b9763c4120fbc858b1bf2344d3.

## Exact dual certificate

The certificate at evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json stores the full 2,113-entry rational vector z, lambda, and 184 interval evaluations. Its exact values are
\[
\|z\|_1=1,\qquad
\lambda=\frac{6860398250812196864}{4611686018430026587},
\]
\[
\lambda+z^T y=\frac{2248712232382170277}{4611686018430026587},
\qquad \delta=10^{-10}.
\]
Hence lambda+z^T y-delta is exactly the lower bound in the theorem.

The 50 nonzero dual coordinates (zero-based row indices) are:
- fourth order: 233, 868;
- sixth order: 1675, 1712, 1716, 1765, 1767, 1779, 1782, 1790, 1794, 1805, 1821, 1827, 1830, 1847, 1865, 1876, 1879, 1883, 1884, 1913, 1922, 1929, 1963, 1971, 1985, 1987, 1989, 1990, 2001, 2002, 2006, 2011, 2018, 2032, 2033, 2038, 2051, 2071, 2079, 2085, 2088, 2090, 2098, 2099, 2101, 2105;
- eighth order: 2106, 2107;
- no second-order coordinates.

For each physical column a_j, 128-bit Arb certifies
\[
z^T a_j+\lambda-\delta<0.
\]
The largest slack-shifted interval upper endpoint over all 184 columns is
\[
-7.6565440382899941721222335508948670479\times10^{-11}<0.
\]
The certificate is marked complete and contains 184 column intervals.

For any probability vector p, multiply each certified column inequality by p_j and sum:
\[
z^T A p+\lambda-\delta\le0,
\quad
z^T(y-Ap)\ge\lambda+z^T y-\delta.
\]
Hölder's inequality and ||z||_1=1 give
\[
\|Ap-y\|_\infty\ge |z^T(y-Ap)|
\ge\lambda+z^T y-\delta,
\]
which proves the theorem for every mixture over the frozen 184-column pool.

## What “full-sixth-cut” means

The 334 extra sixth-order representatives were discovered by a complete binary64 scan of all 63,133 D42 sixth-order orbits for the earlier exact 152-column candidate. That scan supplies the provenance of the cuts; it is not a numerical premise in the dual proof. One candidate-specific violation, at representative (0,1,8,18,25,35), was separately certified with 128-bit Arb. The other 333 are binary64 screening findings unless separately interval-certified.

“Full-sixth-cut” means all 334 rows from that complete scan were inserted into the 645-row sixth block. It does not mean that this 184-column theorem verifies all 63,133 sixth-order inequalities.

## Reproducibility

- LP transcript: evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json;
- exact dual and Arb intervals: evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json;
- discovery: reoptimize_184col_full_sixth_cut_pool.py;
- independent verifier: verify_184col_full_sixth_cut_dual_arb.py;
- successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105751599;
- evidence commit: 0c0c745c534fb161835e03e63776d6fe7f7178eb;
- parent 183-column LP SHA256: 6ee01897aca66e60cb082f5553ee545e694e58a6de2fd9585eb92d8f9a2b8fe0;
- parent 183-column dual SHA256: dade1e61180f22be13d9b253734c6e1e932d0b31b6e3987018c33f2fa74bec48;
- 183-column pricing screen SHA256: 15081ac62dff2b53db1a39c76bb1739d15a4e8934df71d41b8dc7629159ebc9b;
- 183-column Arb pricing SHA256: 2fbd27ecfec9a18bd5990c36c6dccef1f1ead5bf31595158da6679707e018c0c;
- LP transcript SHA256 pinned by the certificate: 894405a7e879c05d69d71d5e2c67c82e47736842781221ce8c2c42011704687e.

## Scope and next action

This theorem excludes only convex mixtures over the specified 184 generators for the pinned 2,113-row mixed-order objective. It does not establish a complete sixth-only lower bound, a complete eighth-order lower bound, a no-go theorem for all canonical paths or the continuous physical family, or an operational Choi/diamond-norm guarantee.

Next: price all 1,458 unused canonical columns against this exact dual, strictly Arb-check positive candidates, and reoptimize. The central paper-level gap remains a per-instance bridge from the path-moment residual to Choi infidelity and an operational channel metric.
