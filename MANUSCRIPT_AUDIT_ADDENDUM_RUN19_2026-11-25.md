# EUI manuscript/reproducibility audit — Run 19 (2026-11-25)

## Repository state inspected

- Default branch: `main`.
- Pre-run head: `d9a37c240b41b8787ae3a2a26c3a3eac26ad3b85`.
- Latest finite-pool certificate: 6,141 columns, from workflow [45550680525](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45550680525).
- Latest continuous-pricing workflow: [45552403077](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45552403077), completed successfully.
- Open scientific trackers inspected: Issues #5 (finite-pool/full-family gap), #4 (complete eighth-order audit), and #3 (classifier/runtime correctness). Issue #5 is the relevant theory frontier.

## 1. 6,141-column finite-pool theorem — verified

The frozen pool is 22 base atoms + 6,101 fractional-grid atoms + 18 exact-rational gapped paths = 6,141 columns. It retains all 1,461 second-/fourth-order coordinates (21 second-order distances and 1,440 fourth-order dihedral orbits).

The exact rational dual has 103 nonzero coefficients,
[
|D^{-1}y|_1=1,qquad
|y|_1=
rac{13830126800815374421723}{26650000000000003271}<533.
]
The independent Arb verifier checks every column and certifies a common gap greater than (1/5). Hence, for every mixture on this exact pool,
[
|b-Ap|_infty>rac1{2665},qquad
operatorname{TV}(w_p,u_{m bal})>rac1{5330}.
]
The TV statement is for the balanced program-label distribution / dephased register, not Choi or diamond distance.

Evidence:
- [6,141-column Arb certificate](evidence/ising_full_fourth_plus_eighteen_gapped_arb_n21.json)
- [6,141-column diagnostic](evidence/ising_full_fourth_plus_eighteen_gapped_n21.json)
- [finite-pool workflow 45550680525](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45550680525)

## 2. The 6,141 dual has certified continuous escapes

The deterministic general-gapped pricing run [45552403077](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45552403077) completed successfully. It priced the exact 103-term rational dual, froze two candidates as rational couplings, and independently checked them at 256-bit Arb.

- Connected open path: all 41 internal couplings are strictly positive; the minimum is (19999999999999999/20000000000000000000000). The certified target-minus-score interval is centered at (-48.7228849082777609463889598238ldots) with radius (5.94	imes10^{-72}).
- Multi-segment path: internal zero edge ({33}), minimum positive coupling (10^{-8}). The certified target-minus-score interval is centered at (-49.7654903352644187872699185739ldots) with radius (5.95	imes10^{-72}).

Both certificates check all 1,764 orthogonality-matrix entries and enclose determinant one. These strict escapes disprove extension of this particular 6,141-column dual to the continuous connected/general-gapped family. They do not invalidate the finite-pool theorem and do not prove full-family feasibility or infeasibility.

Evidence:
- [search transcript](evidence/ising_full_fourth_plus_eighteen_gapped_search_n21.json)
- [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_eighteen_gapped_escape_arb_n21.json)
- [workflow 45552403077](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45552403077)
- [evidence commit d9a37c2](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d9a37c240b41b8787ae3a2a26c3a3eac26ad3b85)

## 3. New exact theorem: 3–7 perfect-mirror segments

A single rational second-moment dual now separates every ordered composition of 42 into 3, 4, 5, 6, or 7 consecutive perfect-mirror blocks. The exact integer census covers 5,358,536 compositions, with no nonpositive slack. The common minimum is (2/40467), attained in the 3- and 4-block families. The resulting bounds are
[
left|t-mathbb E_mu m(R)ight|_inftygerac{2}{40467},
qquad
operatorname{TV}(w_mu,u_{m bal})gerac1{40467}.
]
The second bound is again only for the program-label/dephased register.

The same dual does not cover two blocks: composition ((1,41)) has slack (-80/40467). The separate two-mirror result uses another certificate. This new result does not cover (kge8), arbitrary nonuniform within-block couplings, or the full physical family.

Artifacts:
- [theory note](THEORY_THREE_TO_SEVEN_MIRROR_SEGMENT_OBSTRUCTION_N21.md)
- [exact verifier](verify_ising_three_to_seven_mirror_segment_obstruction.py)
- [machine-readable evidence](evidence/ising_three_to_seven_mirror_segment_obstruction_n21.json)
- [reproducibility workflow](.github/workflows/eui-three-to-seven-mirror-segment-obstruction.yml)

## 4. Manuscript scope and blockers

The current repository contains theory notes and evidence, but the editable source of the cited manuscript/supplement (TeX/Bib/PDF or equivalent) has not yet been located in the tracked project tree. The public manuscript remains [arXiv:2506.20570v1](https://arxiv.org/abs/2506.20570). Its Appendix B's 10,000 random instances are distribution-dependent average-Choi-fidelity evidence, not a worst-case-over-Hamiltonian or channel diamond guarantee.

Still unresolved:
1. A positive ensemble satisfying the complete all-even-principal-minor system at (n=21), or a global physical-family obstruction.
2. A rigorous bridge from the moment/program-mass discrepancy to per-instance Choi or channel diamond error.
3. A complete eighth-order audit of the 29-column witness (Issue #4).
4. QuAIRKit/Torch-backed end-to-end runtime smoke test (Issue #3).

## 5. What changed in this run

- Added a closed-form integer pair-count formula for the second moments of consecutive signed-mirror blocks.
- Exhaustively checked all 5,358,536 compositions for 3–7 blocks, with 700 independent direct-matrix cross-checks.
- Added the exact theorem, evidence JSON, and GitHub Actions reproduction workflow.
- Updated Issue #5 with the new 6,141 escape result and the 3–7 segment theorem.

## 6. Next highest-value action

Append the two 256-bit-Arb-certified 6,141-dual escapes to the finite pool, reoptimize the complete 1,461-coordinate LP on 6,143 columns, and independently certify the resulting rational dual (or exact primal). In parallel, extend the perfect-mirror combinatorial census beyond seven blocks only if a structural reduction avoids another brute-force scale-up. The main paper-level target remains the full all-even-principal-minor positive ensemble/global converse and its operational channel-metric bridge.
