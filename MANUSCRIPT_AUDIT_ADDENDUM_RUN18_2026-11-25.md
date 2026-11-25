# Manuscript / evidence audit — Run 18 (2026-11-25)

## Repository snapshot

- Main revision at audit time: `989fcfaacf9d5bbcea39a0347a938bda473b88d5`.
- Recursive tree: 984 tracked paths; tree not truncated.
- No tracked `.tex`, `.bib`, `.bbl`, `.bst`, `.pdf`, `.docx`, `.odt`, or `.rtf` manuscript/supplement source was found.
- The open research frontier remains Issue #5; no open pull request was returned by the repository query.
- Issue #5 body and a new top-level progress comment were updated in this run.

## Verified scientific progress

### 6,139-column finite-pool theorem

The refreshed independent Arb run [45548273987](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45548273987) succeeded. The certificate generator was corrected to state the actual 6,139-column scope and to use the strongest predeclared rational floor below the certified minimum interval endpoint.

- Pool: 22 base + 6,101 fractional-grid + 16 exact-rational gapped paths = 6,139.
- Features: all 21 second-order coordinates and all 1,440 fourth-order dihedral orbits (111,930 four-subsets before orbit reduction).
- Dual: 104 nonzero terms (one second-order and 103 fourth-order); exact scaled norm (\|D^{-1}y\|_1=1).
- Exact full-coordinate norm:
  (\|y\|_1=14164662956157091950169/26649999999999965711<533).
- Certified common rational gap: (231161/100000).
- Finite-pool moment residual lower bound: (231161/533000000).
- Program-label TV lower bound: (231161/1066000000).

The exact theory record is [THEORY_6139COL_FULL_FOURTH_FINITE_POOL_N21.md](../blob/main/THEORY_6139COL_FULL_FOURTH_FINITE_POOL_N21.md). The evidence files are the corresponding `ising_full_fourth_plus_sixteen_gapped_n21.json` diagnostic and `..._arb_n21.json` certificate. The evidence commit is `c6ae70171d68e4a56cf598bf4679f21279ba1d6f`.

### Continuous escape of the 6,139 dual

The deterministic search and independent 256-bit Arb verification succeeded in [workflow 45549396031](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45549396031), evidence commit `66cf75f52a48a219f94b0b52cb55cf6869d74682`.

- Connected path: all 41 internal couplings strictly positive, minimum about (10^{-6}); target-minus-candidate interval is strictly negative, centered at (-26.2094024867797243\ldots).
- Five-segment path: internal cuts ({11,16,18,21}), minimum positive coupling (10^{-8}); target-minus-candidate interval is strictly negative, centered at (-30.229130393353341\ldots).
- Both certificates check all 1,764 orthogonality entries by Arb intervals and enclose determinant one.

This disproves the global extension of this particular 6,139-column dual, not the finite-pool theorem and not the existence of a positive ensemble for the full physical family.

### 6,141-column next pool

The two new paths have been appended, producing 22 + 6,101 + 18 = 6,141 columns. Discovery, verifier, and workflow files are present:

- `discover_ising_full_fourth_plus_eighteen_gapped_n21.py`
- `verify_ising_full_fourth_plus_eighteen_gapped_arb_n21.py`
- `.github/workflows/eui-reoptimize-6141-full-fourth.yml`

The corrected workflow run is [45549928060](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45549928060). It was pending at audit time. An earlier run, 45549909617, was launched before the commit-step output-path correction; it is not the authoritative run. No 6,141 LP or Arb result is claimed yet.

## Manuscript scope and limitations

The public source remains [arXiv:2506.20570v1](https://arxiv.org/abs/2506.20570). Its Appendix B reports finite random-instance average Choi-fidelity experiments; that is not a worst-case diamond-norm theorem. The repository still lacks editable manuscript/supplement source, so this run updated theory notes, evidence, workflows, and Issue #5 rather than claiming a main-text edit.

The program-mass TV bounds concern the balanced program-label distribution/dephased classical register. They do not by themselves imply Choi-state trace distance or channel diamond distance. The all-even-principal-minor positive-ensemble problem and the operational diamond converse remain unresolved.

## Next highest-value action

Read the corrected 6,141 workflow's actual result. If it yields a dual, independently price that exact dual over continuous positive/general-gapped paths and Arb-certify any frozen escape before adding it. If it yields a primal, freeze the support/weights and independently verify the complete 1,461-coordinate residual. Do not extrapolate any finite-pool theorem to the continuous family.

The current execution environment cannot change its model selection to GPT-6.1-sol Max; no model switch is claimed.

## Post-audit refresh (2026-11-25, 04:59 UTC)

The deterministic 6,139-dual pricing workflow was rerun against the refreshed finite certificate and succeeded again: [workflow 45550004161](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45550004161), evidence commit `3f1d5fae696a3e3a428304e98d8cf32569c80d6a). The current frozen Arb intervals are:

- Connected path: ([-26.20940248677975330532500069462903387096527750760617930150028583597970395\ldots\pm4.39\times10^{-72}]<0).
- Five-segment path: ([-30.22913039335334084872133552629950046305661562639125881662670819414718008\ldots\pm7.96\times10^{-72}]<0).

The 6,141 workflow was refreshed to pin this latest parent evidence and set `cancel-in-progress: true`, so stale runs are cancelled rather than allowed to publish against an obsolete parent chain. The prior runs 45549909617 and 45549928060 were cancelled. The current authoritative run is [45550376910](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45550376910), on head `65e4853a3c3c5c2742d2e33c32a5aa9aaf81b739). Python compilation and the block-minor/spin-symmetry/serialization regressions passed; the 6,141-column LP is still running, with Arb certification pending. No 6,141 theorem is claimed yet.

Issue #5's current-frontier section and progress comment were refreshed to link the current 6,139 escape evidence and the new authoritative 6,141 run.
