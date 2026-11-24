# 6,135-column full-second/fourth reoptimization after certified 6,133-dual escapes

**Status:** reproducible LP experiment launched after two exact 256-bit Arb escapes from the 6,133-column dual. No 6,135-column theorem is claimed until the new LP dual is independently certified.

## Parent certificate

The parent is the 6,133-column exact finite-pool theorem in [THEORY_6133COL_FULL_FOURTH_PLUS_TEN_GAPPED_FINITE_POOL_N21.md](THEORY_6133COL_FULL_FOURTH_PLUS_TEN_GAPPED_FINITE_POOL_N21.md). Its 85-term rational dual has exact scaled norm 1, full-coordinate norm 533, and a common Arb-certified column gap greater than 1/5. It applies only to the exact 6,133-column pool.

## New pricing result

The deterministic pricing search [45503337509](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45503337509) evaluated 906 initial candidates, used 12 L-BFGS-B starts per class with up to 160 iterations, and passed the analytic Frechet-gradient finite-difference test (maximum absolute defect 1.3736090043181548e-10).

Two exact-decimal candidates were reconstructed as rational couplings and independently verified at 256-bit Arb:

- Connected path: all 41 internal couplings are strictly positive, with minimum 1e-6. The certified target-minus-score interval is
  \[
  [-27.0885582355989401299362582312374963\pm4.80\times10^{-71}]<0.
  \]
- Multi-segment path: internal cuts are {8,13,32,35}, with minimum positive coupling 1e-8. The certified target-minus-score interval is
  \[
  [-36.8524360048385916942304027666603097\pm3.25\times10^{-69}]<0.
  \]

Both pass 1,764 Arb orthogonality-entry checks and determinant-one certification. These are strict escapes from this particular 6,133-column dual, not a failure of the 6,133-column finite-pool theorem and not a global feasibility/infeasibility result.

Evidence:
- [Search transcript](evidence/ising_full_fourth_plus_ten_gapped_search_n21.json)
- [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_ten_gapped_escape_arb_n21.json)
- [Search source](search_ising_full_fourth_plus_ten_gapped_n21.py)
- [Independent verifier](verify_ising_full_fourth_plus_ten_gapped_escape_arb_n21.py)
- [Workflow 45503337509](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45503337509)

## 6,135-column reoptimization

The two new exact-rational paths are appended to the ten gapped paths of the certified parent, giving
\[
22+6101+12=6135
\]
columns. The new workflow reconstructs every gapped feature independently and solves the same full 1,461-coordinate second-/fourth-order LP. A floating dual is discovery only until the independent 512-/128-bit Arb verifier checks every column. A floating primal is discovery only until exact rational weights and all 1,461 coordinates are independently interval-verified.

This experiment still does not cover all nonuniform positive couplings, arbitrary multi-segment paths, all even principal minors, or a Choi/diamond operational metric.
