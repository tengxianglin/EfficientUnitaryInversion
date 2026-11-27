# Manuscript / repository audit — Run 62 (2026-11-27)

## Repository snapshot

- Repository: tengxianglin/EfficientUnitaryInversion
- Default branch: main
- Pre-run HEAD: e3245c804637e78ce75eb6394af0e5b31d219022
- Exact N=10 ensemble support, verifier, and theory were added in commits 293ffb2, 2e632c0, and 8013050.
- CI workflow was added in 307435e; the certificate serialization was corrected in 9f6e80b.
- Final 512-bit Arb certificate was committed by CI in 84d5e3c9570460dc7049f469a58d856a4e19f0a6.
- Frozen atom-input SHA256: 6fbb07814e51e44ae8068b38c5c2bfd89247d5432e62636f6f13217e9dc8433c.

## Issues inspected

- Issue #7 remains the canonical physical reachability question for N=42. The N=10 small-size subproblem is now solved constructively; the main N=42 question remains open.
- Issue #5 remains a distinct finite-pool minimax / full-family gap. Its finite-pool certificates are not promoted to a global physical theorem.
- Issue #6 still tracks the Appendix B per-instance L1 normalization wording and the pending QuAIRKit regeneration of the 10,000-sample fidelity table.
- Issue #3 classifier regression is passing; the full QuAIRKit runtime smoke test remains pending.
- Issue #4 remains closed and was not duplicated.

## Run-62 scientific result: exact N=10 full-cycle feasibility

A deterministic numerical discovery searched 2,500 cycle-coupling candidates, 1,500 with all ten couplings strictly positive. A 13-atom support matched the 44 D10-orbit all-even feature vector to a binary64 maximum residual of 2.67841304690819e-15. This is discovery only.

The frozen decimal coupling strings are exact rationals. The 13 base weights are then defined as the exact-real solution of a 13x13 system: four pair-orbit equations, eight independent quartic-orbit equations, and normalization.

The final 512-bit Arb workflow 45985463935 passed. It certifies:
- the 13x13 moment-matrix determinant interval excludes zero:
  \[
  [-4.0577797582873793057671609755\ldots\times10^{-10}
  \pm 5.75\times10^{-157}];
  \]
- all 13 exact-real weights are strictly positive; the smallest interval is centered at approximately 0.00247897639976289846;
- all thirteen base coupling vectors have strictly positive exact-rational decimal entries; the minimum is exactly 3827933674451301/10^18;
- every base rotation has R^T R=I and det R=1, and Q=RD is certified symmetric, involutory, trace zero, and det -1;
- all five pair-orbit and all sixteen quartic-orbit residual intervals contain zero, with radii below 7.1e-147.

The exact proof is not based only on interval residuals. D10 symmetrization makes each coordinate equal its orbit average. The e2 identity fixes the fifth pair orbit. The universal triple-to-quartic identity gives an 8x16 incidence system whose first 8x8 pivot minor has exact determinant 64, fixing all remaining quartic orbits from the selected twelve coordinates. Jacobi's complementary-minor identity then fixes sixth/eighth order, and the full determinant fixes order ten. Thus all 512 even subsets are matched exactly.

The symmetrized measure has 13 base atoms and 260 labelled D10 images (at most 260 distinct support points). Reflection images can be vertex-sign gauged to strictly positive couplings without changing principal minors.

## Files and verification

- THEORY_PHYSICAL_CYCLE_ENSEMBLE_N10.md
- evidence/n10_positive_cycle_ensemble_atoms.json
- evidence/n10_positive_cycle_ensemble_arb.json
- verify_n10_positive_cycle_ensemble.py
- .github/workflows/eui-n10-positive-cycle-ensemble.yml

Final CI: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45985463935

Key commits:
- 293ffb21a0e47476ee310dfa298b9836a47e010f — frozen strictly positive support
- 2e632c022dd65b796f7f980abee411dee90da2ca — Arb verifier
- 8013050bef7b4878d74f438f95fc99ebfffcb9ad — theory
- 307435eb541f44435039c86bdc5e46bcde681fdd — CI workflow
- 9f6e80b1c1d6fe04af7014d2f327a29c0062e409 — JSON newline serialization fix
- 84d5e3c9570460dc7049f469a58d856a4e19f0a6 — final Arb certificate

## Manuscript audit

The public manuscript remains arXiv:2506.20570v1, dated 25 June 2025. The current HTML contains Sections I–VIII and Appendices A–E. Appendix B lines 294–304 still use the raw-Gaussian / relative-L1 notation tracked by Issue #6; this run did not alter or reinterpret the manuscript's reported table. No editable TeX/Bib or separate supplementary source was found in the repository, so no manuscript-source change is claimed.

## Scope and next action

The N=10 complete balanced-slice even-principal-minor convex-hull problem is now solved for the real nearest-neighbour cycle-exponential family, with a witness representable using strictly positive couplings. This is a small-size exact existence theorem. It does not solve N=42 and does not imply a Choi trace-distance or diamond-distance bound.

Next highest-value action: transfer the full-cycle positive-candidate discovery strategy to the N=42 reduced moment system, while retaining higher even-order constraints beyond the 2nd/4th hierarchy. The N=10 result shows that the N=10 block-mirror no-go and connected-cycle escape are compatible with full-cycle feasibility; it does not justify extrapolating feasibility to N=42.
