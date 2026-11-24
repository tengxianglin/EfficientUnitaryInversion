# Continuous gapped escapes from the 6,129-column full-fourth dual

**Status:** deterministic multistart discovery followed by independent 256-bit Arb certification of both a connected positive-coupling path and a multi-segment path. These are escapes from one particular exact rational dual, not counterexamples to the 6,129-column finite-pool theorem.

## 1. Frozen dual and pricing functional

The parent finite-pool certificate is
[evidence/ising_full_fourth_plus_six_gapped_arb_n21.json](evidence/ising_full_fourth_plus_six_gapped_arb_n21.json), with 80 exact rational coefficients, target score
\[
\beta=
\frac{12364611528457646871}{35533333333333310677}
=0.34797218185152874544\ldots,
\]
and the strict finite-pool inequality
\[
y^{\mathsf T}(b-F(R_j))>\frac15
\]
for all 6,129 listed columns. The pricing search reconstructs this same rational functional from the pinned diagnostic and Arb certificate; it does not refit a floating surrogate.

## 2. Search and independent verification

The deterministic search evaluated 518 initial candidates and optimized eight starts in each of the connected and multi-segment classes, with 120 L-BFGS-B iterations per start. The Frechet-gradient finite-difference self-test had maximum absolute defect
\[
3.422795102903109\times10^{-10}.
\]
The optimizer is discovery only. Both best candidates were frozen as exact rationals and independently checked with python-flint / Arb at 256-bit precision.

### Connected positive-coupling escape

All 41 internal couplings are strictly positive; the closing edge is zero. The minimum internal coupling is
\[
c_{\min}=\frac{19999999999999999}{20000000000000000000000}
=9.9999999999999995\times10^{-7}.
\]
The maximum internal coupling is \(11.05338495863263\). The certified score and residual are
\[
y^{\mathsf T}F(R(c_*))
\in[40.37256643487302543212445920\pm4.43\times10^{-72}],
\]
\[
\boxed{
y^{\mathsf T}(b-F(R(c_*)))
\in[-40.02459425302149668668054524\pm2.09\times10^{-72}]<0.
}
\]
Arb checks all 1,764 entries of \(R^{\mathsf T}R-I\) with intervals containing zero and certifies \(\det R\) in an interval containing one.

### Multi-segment escape

A second candidate has internal cuts \([17,29]\), with all other internal couplings positive (minimum \(10^{-8}\)). Its certified residual is
\[
y^{\mathsf T}(b-F(R(c)))
\in[-36.94266442196780728292023791\pm7.36\times10^{-73}]<0.
\]
It passes the same 1,764-entry orthogonality and determinant checks.

## 3. Consequence and scope

The connected candidate alone proves that the particular 6,129-column dual does **not** separate the full connected positive-coupling 42-site open-path family. The multi-segment candidate independently shows escape in the larger segmented family.

This does **not** invalidate the 6,129-column finite-pool theorem: the new rational path is outside that exact finite pool, while all 6,129 listed columns retain their Arb-certified positive gap. It does not prove full-family feasibility or infeasibility, construct an all-even-principal-minor positive ensemble, or imply a Choi/diamond-distance bound.

## 4. Reproduction

- [Search script](search_ising_full_fourth_plus_six_gapped_n21.py)
- [Independent 256-bit Arb verifier](verify_ising_full_fourth_plus_six_gapped_escape_arb_n21.py)
- [Search transcript](evidence/ising_full_fourth_plus_six_gapped_search_n21.json)
- [Escape certificate](evidence/ising_full_fourth_plus_six_gapped_escape_arb_n21.json)
- [Workflow 45431346012](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45431346012), success
- [Certificate commit cc2d6e4](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/cc2d6e495ca5ba53a3a0d3531fb1a810a60f47b8)
- Parent 6,129 finite certificate SHA256: c7efb8caa40d1f5472dd93263f1fcea2f2bebc86ca60b0ffc7417f6b5f94a5db
- Parent diagnostic SHA256: 9cb255dfe0d96155f69ee9d9b9870cf1d442879e3afa3258ff599c0f7e834ccd

## 5. Next step

Append both exact-rational escapes to the full 1,461-coordinate candidate matrix and reoptimize. The next pool has 6,131 columns (22 base + 6,101 fractional-grid + 8 gapped). Any new dual must again be rationalized and independently Arb-checked; any new continuous escape must be frozen and checked in the same way.
