# 6,133-column full-second/fourth finite-pool obstruction at n=21

**Status:** rigorous finite-pool theorem, independently certified with python-flint / Arb in workflow [45484523550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45484523550) on 2026-11-25. **Not claimed:** a continuum-family obstruction, an all-even-principal-minor obstruction, or a Choi/diamond-distance lower bound.

## 1. Exact finite physical pool

Let N=42 (n=21) and
\[
R(c)=e^{A(c)}\in SO(42),\qquad
A(c)_{j,j+1}=2c_j,\quad A(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,\quad c_{41}=0.
\]

The exact pool has 6,133 columns: 22 pinned base atoms, 6,101 corrected fractional single-open-path grid atoms, and ten exact-rational gapped paths (eight inherited from the certified 6,131-column pool, plus two new 256-bit-Arb-certified escapes from the 6,131-column dual).

## 2. Complete second-/fourth-order feature system

The feature vector F(R) contains all 21 distance-averaged second moments and all 1,440 dihedral orbits of fourth-order principal minors. There are
\[
\binom{42}{4}=111{,}930
\]
raw quartets and 1,461 full feature coordinates. Exact incidence reduction gives 1,313 independent moment coordinates; with normalization there are 1,314 equality constraints.

Let b be the exact balanced target and A_6133 the matrix of these 1,461 features for the 6,133 listed columns.

## 3. Exact rational dual and interval certificate

The floating LP is discovery only. The independent verifier freezes all 85 nonzero dual coefficients as exact rational numbers and imposes
\[
D=\operatorname{diag}(41I_{21},533I_{1440}),\qquad
\|D^{-1}y\|_1=1.
\]
For this certificate the exact full-coordinate norm is
\[
\boxed{\|y\|_1=533.}
\]

Arb independently verifies
\[
\boxed{y^{\mathsf T}(b-F(R_j))>\frac15,\qquad j=1,\ldots,6133.}
\]
The minimum certified column-gap lower endpoint is
\[
0.22948739235422886048519109417616827\ldots>\frac15.
\]
The verifier uses 512-bit Arb for all 22 base atoms and ten gapped paths, and 128-bit Arb for all 6,101 fractional-grid paths. Five independent active-block/full-feature pricing self-tests pass.

### Theorem — finite-pool moment obstruction

For every probability vector p in the 6,133-column simplex,
\[
y^{\mathsf T}(b-A_{6133}p)>\frac15.
\]
By Holder and the **exact equality** \(\|y\|_1=533\),
\[
\boxed{\|b-A_{6133}p\|_\infty>\frac1{2665}.}
\]
The strict inequality follows from the strict Arb-certified column gap; the norm equality is sufficient and must not be misstated as \(\|y\|_1<533\).

### Corollary — program-mass TV

Each retained moment coordinate is the expectation of a bounded even-parity program-label character averaged over its dihedral orbit, with pointwise norm at most one. The moment residual therefore supplies a bounded test with expectation gap greater than 1/2665 between the ensemble-averaged balanced-label mass w_p and the uniform balanced-label law u_bal. Hence
\[
\boxed{\operatorname{TV}(w_p,u_{\rm bal})>\frac1{5330}.}
\]
This is a classical program-mass / dephased-register result only, not a Choi-state trace-distance or channel diamond-distance bound.

## 4. Reproducibility

- Floating LP diagnostic: [ising_full_fourth_plus_ten_gapped_n21.json](evidence/ising_full_fourth_plus_ten_gapped_n21.json)
- Exact Arb certificate: [ising_full_fourth_plus_ten_gapped_arb_n21.json](evidence/ising_full_fourth_plus_ten_gapped_arb_n21.json)
- Independent verifier: [verify_ising_full_fourth_plus_ten_gapped_arb_n21.py](verify_ising_full_fourth_plus_ten_gapped_arb_n21.py)
- Reoptimizer: [discover_ising_full_fourth_plus_ten_gapped_n21.py](discover_ising_full_fourth_plus_ten_gapped_n21.py)
- Successful workflow: [45484523550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45484523550)
- Diagnostic commit: [65fe242](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/65fe24253ede8010ea2a8a0dcf43f14c7297d34e)
- Workflow/reoptimizer commit: [d904ac8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d904ac89242f9e7568b951c91bdf41a944e65eb9)

## 5. Scope and next step

This theorem excludes only mixtures over the exact 6,133 listed columns under the complete second-/fourth-order feature design. It does not cover all nonuniform positive couplings, arbitrary multi-segment paths, all even principal minors, or an operational Choi/diamond metric. The highest-value next step is continuous pricing of this newly certified 85-term dual; any found escape must be frozen as exact rationals and independently checked with Arb before a new finite-pool LP is constructed.
