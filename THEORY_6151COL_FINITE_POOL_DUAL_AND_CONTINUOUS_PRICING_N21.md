# 6,151-column finite-pool dual and continuous-pricing handoff (N=21)

Date: 2026-11-27

## 1. Verified finite-pool theorem

The corrected 6,151-column full-second-/fourth-order workflow completed successfully:

- Workflow: [45861230625](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45861230625)
- Diagnostic: [`evidence/ising_full_fourth_plus_twenty_eight_gapped_n21.json`](evidence/ising_full_fourth_plus_twenty_eight_gapped_n21.json)
- Independent certificate: [`evidence/ising_full_fourth_plus_twenty_eight_gapped_arb_n21.json`](evidence/ising_full_fourth_plus_twenty_eight_gapped_arb_n21.json)
- Certificate commit: [`f163790724dd4bd132591a7413b3809adb02088d`](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f163790724dd4bd132591a7413b3809adb02088d)

The exact pinned pool is

[
6151=22+6101+28,
]

with 22 base atoms, 6,101 corrected fractional single-open-path grid atoms, and 28 exact-rational gapped paths (26 inherited from the 6,149-column pool and two newly certified escapes from its dual).

The feature system contains 21 second-order coordinates and 1,440 fourth-order dihedral orbits (111,930 four-subsets), for 1,461 coordinates total. The reduced system has 1,313 independent moment equations and 1,314 equalities including normalization.

The independently reconstructed rational dual has 118 nonzero coefficients and satisfies exactly

[
|D^{-1}y|_1=1,qquad |y|_1=533,
qquad D=operatorname{diag}(41I_{21},533I_{1440}).
]

The 128-bit Arb pricing of all 6,101 fractional-grid columns and 512-bit Arb pricing of the 22 base plus 28 gapped columns certify the common rational column gap

[
y^{mathsf T}(b-a_j)ge rac15
quad	ext{for every one of the 6,151 pinned columns.}
]

Consequently every probability vector supported on this exact finite pool obeys

[
|b-Ap|_infty>rac1{2665},
qquad
operatorname{TV}(w_p,u_{m bal})>rac1{5330}.
]

The TV statement concerns the balanced program-label distribution / dephased classical label register only. It is not a Choi trace-distance or channel diamond-distance bound.

## 2. What this does not prove

The theorem is finite-pool only. It does not cover other nonuniform gapped couplings, the continuous gapped family, arbitrary multi-segment paths, all even principal-minor coordinates, or an operational Choi/diamond guarantee. In particular, the repeated escape of earlier finite-pool duals means no unchanged finite-pool dual should be described as a global physical separator.

## 3. Continuous pricing of this specific 6,151 dual

A deterministic discovery/verification pipeline has now been added:

- Search: [`search_ising_full_fourth_plus_twenty_eight_gapped_n21.py`](search_ising_full_fourth_plus_twenty_eight_gapped_n21.py)
- Independent 256-bit Arb verifier: [`verify_ising_full_fourth_plus_twenty_eight_gapped_escape_arb_n21.py`](verify_ising_full_fourth_plus_twenty_eight_gapped_escape_arb_n21.py)
- Workflow: [`eui-full-fourth-plus-twenty-eight-gapped-search-n21.yml`](.github/workflows/eui-full-fourth-plus-twenty-eight-gapped-search-n21.yml)
- Current run: [45879531992](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45879531992)

The search reconstructs the exact 118-term rational dual from the certified finite-pool certificate, then tests connected and multi-segment open-path couplings. It uses seed `202611270247`, a frozen seed-pool sample, random connected and fractional-profile starts, all 28 pinned gapped paths as starts, random multi-segment starts, L-BFGS-B, and the analytic Fréchet gradient. This is finite multistart discovery only.

The hosted run has passed dependency installation and Python compilation; the pricing search is running and the independent Arb step is pending. A candidate counts as a continuous physical escape only if its decimal couplings are frozen as exact rationals and the independent 256-bit verifier certifies all 1,764 orthogonality entries, determinant one, and a strictly negative target-minus-score interval. Failure to find an escape in this finite search is not a global upper bound.

## 4. Next decision rule

1. If Arb certifies a connected escape, record that this particular 6,151 dual is not a separator even on the strictly positive interior-edge family; append the exact path and reoptimize only if that finite-pool continuation remains useful.
2. If Arb certifies only a multi-segment escape, record the narrower failure of this dual on the gapped family.
3. If no escape is found, report only the finite search scope; do not infer global separation.
4. In parallel, prioritize the exact positive-measure problem for the complete even-principal-minor target and the independent moment-to-Choi/diamond bridge.

## 5. Reproducibility

The search and verifier pin both the 6,151 diagnostic and the 6,151 Arb certificate by SHA256. The verifier uses the exact rational dual coefficients in the finite certificate and reconstructs each candidate coupling from its frozen decimal string as a rational before Arb evaluation.


## 4. Continuous pricing result for the 6,151 dual — two certified escapes

Workflow [45879531992](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45879531992) completed successfully. The deterministic search used seed `202611270247`, evaluated 1,820 initial candidates, and ran 16 L-BFGS-B starts per class. Its analytic Fréchet-gradient finite-difference self-test had maximum absolute defect (1.947994265893982\times10^{-10}). These optimizer results are discovery only.

The independent 256-bit Arb verifier certified both frozen candidates:

1. **Connected path:** all 41 internal couplings are strictly positive; the minimum is
   [
   \frac{19999999999999999}{20000000000000000000000}\approx10^{-6}.
   ]
   The exact-rational path has Arb score
   [
   [33.4302001490294726321390\ldots\pm7.12\times10^{-73}],
   ]
   so target minus score is
   [
   [-33.1812592736687668483584\ldots\pm6.65\times10^{-73}]<0.
   ]

2. **Two-segment path:** the internal cut is edge 32 and the minimum positive coupling is (1/10^8). Its target-minus-score interval is
   [
   [-24.3211293146278319656689\ldots\pm4.64\times10^{-71}]<0.
   ]

For each path the verifier checked all 1,764 entries of the (42\times42) orthogonality matrix and certified determinant one. The result status is `arb_certified_6151_dual_general_gapped_escape`.

This proves that the particular 6,151-column dual is not a global separator for the continuous connected/general-gapped physical family. The 6,151-column finite-pool theorem is unchanged and remains valid for its exact pinned columns. No full-family feasibility or infeasibility result follows.

Evidence:
- [Search transcript](evidence/ising_full_fourth_plus_twenty_eight_gapped_search_n21.json)
- [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_twenty_eight_gapped_escape_arb_n21.json)
- [Workflow 45879531992](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45879531992)
- [Evidence commit 170efc7](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/170efc7332ef5a4d9e6395f407ec38b03a4a9cce)

## 5. 6,153-column continuation

Both certified paths have been appended to the 6,151-column pool, giving 22 base + 6,101 fractional-grid + 30 exact-rational gapped paths = 6,153 columns. The new discovery and Arb-verification scripts are:

- `discover_ising_full_fourth_plus_thirty_gapped_n21.py`;
- `verify_ising_full_fourth_plus_thirty_gapped_arb_n21.py`;
- workflow `eui-reoptimize-6153-full-fourth.yml`.

The first hosted attempt [45880306574](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880306574) stopped before the LP because a copied parent-status guard expected the 6,153 child label on the 6,151 parent diagnostic. This was a metadata guard error, not a numerical or mathematical failure; it was corrected in [commit 2733809](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/273380954425bedc055bd61d02098443c40f9304). A subsequent static audit caught two more copied parent pins in the independent verifier (the parent diagnostic path and its status label); both were corrected in [commit f844913](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f844913492aaaa65a95b0b69223d1bc2cc538890). The intermediate run [45880550567](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880550567) was superseded during its LP step by that verifier repair. Corrected run [45880800772](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880800772) has passed setup, dependency installation, compilation, and structural regressions; the full 1,461-coordinate LP is running and independent Arb certification is pending. No 6,153-column result is claimed until the corrected verifier completes.
