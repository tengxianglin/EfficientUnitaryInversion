# Manuscript and evidence audit — EUI run 14 (2026-11-25)

## Verified parent result

The 6,133-column complete second-/fourth-order finite-pool obstruction is independently certified in [workflow 45484523550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45484523550). Its 85-term exact rational dual has \(\|D^{-1}y\|_1=1\), exact \(\|y\|_1=533\), and Arb-certified column gaps strictly greater than 1/5 on all 6,133 listed columns. This implies a finite-pool moment residual greater than 1/2665 and a balanced program-mass TV lower bound greater than 1/5330. The exact-norm proof wording was corrected in commit [706487f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/706487ff00380d4f4cfc6fd82e4ac5817ee7ad29).

## New result: two 256-bit-Arb escapes from the 6,133 dual

The deterministic pricing search [45503337509](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45503337509) evaluated 906 initial candidates, ran 12 L-BFGS-B starts per class (maximum 160 iterations), and passed the analytic Frechet-gradient finite-difference test with maximum absolute defect \(1.3736090043181548\times10^{-10}\).

The frozen exact-rational connected candidate has all 41 internal couplings strictly positive (minimum approximately \(10^{-6}\)). Its Arb target-minus-score interval is
\[
[-27.0885582355989401299362582312374963\pm4.80\times10^{-71}]<0.
\]
The frozen exact-rational multi-segment candidate has cuts \(\{8,13,32,35\}\), minimum positive coupling \(10^{-8}\), and Arb target-minus-score interval
\[
[-36.8524360048385916942304027666603097\pm3.25\times10^{-69}]<0.
\]
Both candidates pass 1,764 orthogonality-entry interval checks and determinant-one certification at 256-bit Arb.

These counterexamples refute extension of this specific 6,133-column dual unchanged to the continuous connected/general-gapped family. They do not refute the finite-pool theorem and do not prove global feasibility/infeasibility.

Evidence:
- Search transcript: `evidence/ising_full_fourth_plus_ten_gapped_search_n21.json`
- Escape certificate: `evidence/ising_full_fourth_plus_ten_gapped_escape_arb_n21.json`
- Search source: `search_ising_full_fourth_plus_ten_gapped_n21.py`
- Arb verifier: `verify_ising_full_fourth_plus_ten_gapped_escape_arb_n21.py`

## 6,135-column reoptimization

The two new exact-rational paths have been appended to the ten inherited gapped paths, producing a 6,135-column candidate pool. The full 1,461-coordinate LP and independent Arb verifier are in workflow [45504430215](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45504430215). This is pending; no 6,135-column theorem is claimed. The scripts were corrected so the parent is pinned to the 6,133-column diagnostic/certificate, the new pool has 12 gapped paths, and the verifier expects exactly 6,135 columns.

## Manuscript-source audit

The recursive main tree previously contained 946 tracked paths and no TeX/Bib/PDF or word-processor manuscript/supplement sources. The new tracked manuscript-level artifacts are theory notes and audit addenda only; no formal manuscript body modification is claimed.

## Remaining blockers

- Complete all-even-principal-minor moment constraints for the n=21 physical family.
- A genuinely global obstruction or exact positive ensemble over the full continuous physical family.
- A rigorous bridge from program-mass TV / moment discrepancy to Choi-state trace distance or channel diamond error.
