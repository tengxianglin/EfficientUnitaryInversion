# Run 50 — 6,149-dual continuous escapes and 6,151-column handoff

Date: 2026-11-26

## 1. Current repository and scientific tracks

The repository mainline was inspected through the recursive Git tree and recent commits. The open scientific issues remain #5 (finite-pool versus full physical convex-hull membership), #7 (physical reachability of the exact unrestricted-SO matching ensemble), #6 (Appendix B noise normalization), and #3 (Hamiltonian classifier correctness). Issue #5 remains the highest-leverage active track because the new 6,149-column certificate is now continuously priced.

The recursive tree had 1,214 entries and was not truncated. No `.tex`, `.bib`, `.pdf`, `.docx`, or other editable manuscript source exists in this repository. The public manuscript is the arXiv v1 preprint, submitted 25 June 2025; its appendices A–E are included in the preprint. The new results are recorded in theory/audit notes, not silently inserted into the public manuscript.

## 2. Verified finite-pool result: 6,149 columns

GitHub Actions [45826172005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45826172005) completed SUCCESS, including the full 1,461-coordinate LP and independent Arb verification.

Exact pool:
- 22 base atoms;
- 6,101 fractional single-open-path grid atoms;
- 26 exact-rational gapped paths;
- 6,149 columns.

The moment design has 21 second-order coordinates, 1,440 fourth-order dihedral orbits (111,930 four-subsets), 1,313 independent moment rows, and 1,314 equalities including normalization.

The independently certified dual has 106 exact-rational nonzero coefficients, exact scaled (L_1) norm 1, and exact full-coordinate (L_1) norm 533. Arb checks the 6,101 fractional-grid columns at 128 bits and 22 base + 26 gapped columns at 512 bits. Every column has certified gap at least (1/5); the minimum Arb lower-endpoint interval is centered near 0.2101530855777222, strictly above (1/5).

For mixtures over this exact pool only:
[
\|b-Ap\|_\infty>1/2665,
\qquad
\operatorname{TV}(w_p,u_{\rm bal})>1/5330.
]
The TV statement concerns the balanced program-label/dephased-label register, not Choi trace distance or channel diamond distance.

Evidence:
- [6,149 diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_n21.json);
- [6,149 Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_arb_n21.json);
- reoptimization workflow [45826172005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45826172005);
- certificate commit [9df5080](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/9df5080c0d55e3578f509a9866adee4071d0bfd6).

## 3. Two continuous physical escapes from the 6,149 dual

The deterministic pricing search [45842142632](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45842142632) completed SUCCESS. Search configuration:
- random seed `202611262241`;
- 1,818 initial candidates;
- 512 frozen seed-pool samples;
- 512 independent connected starts;
- 256 fractional-profile perturbations;
- 524 multi-segment starts (including pinned gapped paths);
- 16 optimized starts per class;
- L-BFGS-B with analytic Fréchet gradient, up to 180 iterations;
- elapsed time 74.876 seconds.

The gradient finite-difference self-test maximum absolute defect was (1.0638556702247115\times10^{-10}). This finite multistart search is discovery only.

The independent 256-bit Arb verifier certified two exact-rational escapes from this particular 106-term dual:

**Connected path:** all 41 internal couplings are strictly positive; the minimum is
[
\frac{19999999999999999}{20000000000000000000000}\approx10^{-6}.
]
Target-minus-score:
[
[-28.988535237245591114040969525479118373780243642708482564441772663183324271
\pm8.08\times10^{-73}]<0.
]

**Multi-segment path:** one internal cut at edge 35; minimum positive coupling (10^{-8}). Target-minus-score:
[
[-29.3124498332463992078096047892697695368233657693673495466858610419640643
\pm4.95\times10^{-71}]<0.
]

For each candidate, Arb checked all 1,764 orthogonality entries and certified that the determinant interval contains 1. Both couplings are frozen as exact rational numbers in the certificate.

Evidence:
- [search transcript](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_search_n21.json);
- [256-bit Arb escape certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_escape_arb_n21.json);
- evidence commit [6334f7a](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6334f7a11e604aab9605b977d73ab852ddafb34c).

**Conclusion:** the 6,149-column finite-pool theorem remains valid for its exact pinned columns, but its dual is not a global separator for the continuous connected/general-gapped physical family. This does not prove that the balanced target is or is not in the full physical convex hull.

## 4. Work completed: 6,151-column cutting-plane pool

The two new Arb-certified paths have been appended to the 26 inherited gapped paths. The next pool has:
- 22 base atoms;
- 6,101 fractional-grid atoms;
- 28 exact-rational gapped paths;
- 6,151 columns total.

New files:
- `discover_ising_full_fourth_plus_twenty_eight_gapped_n21.py`;
- `verify_ising_full_fourth_plus_twenty_eight_gapped_arb_n21.py`;
- `.github/workflows/eui-reoptimize-6151-full-fourth.yml`.

The discovery code reconstructs all inherited exact-rational paths and both newly certified escapes before rebuilding the full 1,461-coordinate design. The independent verifier pins the 6,149 parent diagnostic/certificate and 6,149-dual escape search/certificate hashes, then prices all 6,151 columns at the configured Arb precisions.

The first pricing workflow attempt failed at a copied guard that expected 24 instead of 26 gapped paths; no numerical pricing was run. That guard was corrected. The corrected 6,149-dual pricing workflow passed, and the 6,151 reoptimization workflow [45842843414](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45842843414) is currently in progress. No 6,151 LP or Arb result is claimed yet.

Mainline code commits:
- discovery [49adf4f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/49adf4fea7f420d57593b07bd6378f9e054f9a49);
- verifier [184d372](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/184d3720a73b2d517ca480a010db5e576d56a291);
- workflow [9f1d2f9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/9f1d2f9b8d0795d032335dcf04a7b1f832c25f03);
- count/status/provenance fixes [0830378](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/08303786fc98a26e1a7d77789f0dc0278259645d), [df4a8eb](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/df4a8eb0bfaf9f3adb762246ea30ad2dcbf9f427), [42130aa](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/42130aa6b472d4d25469013cd5d99760ad9c90dc).

## 5. Remaining blockers and next action

- Exact positive physical ensemble matching every even-principal-minor coordinate at (n=21): unresolved.
- Global separator valid for every allowed real coupling vector: unresolved.
- Complete sixth-, eighth-, and higher-order moment control: unresolved.
- Operational bridge from program-label TV/moment discrepancy to Choi trace distance or channel diamond distance: unresolved.
- Editable manuscript TeX/Bib source: absent from the repository.

Next highest-value action: inspect workflow [45842843414](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45842843414). If the 6,151 dual certifies, immediately price that particular dual continuously. If the LP finds a primal, independently certify all positive weights and all 1,461 coordinates. A finite multistart failure to find an escape must not be presented as a global proof.
