# 6,131-column full-second/fourth reoptimization protocol at n=21

**Status:** experiment specification and reproducibility record only. No 6,131-column LP outcome is claimed until the workflow produces a diagnostic and, for a dual result, the independent Arb certificate.

## Frozen parent and new physical columns

The parent is the exact 6,129-column pool documented in [THEORY_6129COL_FULL_FOURTH_PLUS_SIX_GAPPED_FINITE_POOL_N21.md](THEORY_6129COL_FULL_FOURTH_PLUS_SIX_GAPPED_FINITE_POOL_N21.md). Its 80-term rational dual was independently Arb-certified on all 6,129 columns, with common gap greater than 1/5 and program-mass TV lower bound greater than 1/5330.

That particular dual was then escaped by two additional paths, both independently certified at 256-bit Arb:
- a connected 42-site open path with all 41 internal couplings strictly positive;
- a multi-segment open path with cuts [17, 29].

The exact search and certificate are pinned in:
- [6,129-dual search](evidence/ising_full_fourth_plus_six_gapped_search_n21.json)
- [6,129-dual escape certificate](evidence/ising_full_fourth_plus_six_gapped_escape_arb_n21.json)
- [escape theory note](THEORY_6129COL_DUAL_GAPPED_ESCAPE.md)

The next finite pool is therefore exactly
\[
22+6101+6+2=6131
\]
columns: 22 pinned base atoms, 6,101 corrected fractional single-open-path grid atoms, six inherited gapped paths, and the two new escapes from the 6,129-column dual. The feature design remains the complete 1,461-coordinate second-/fourth-order system (21 second moments and all 1,440 fourth-order dihedral orbits), with 1,313 independent moment coordinates plus normalization.

## Reproducible implementation

- Discovery LP: `discover_ising_full_fourth_plus_eight_gapped_n21.py`
- Independent rational-dual/Arb verifier: `verify_ising_full_fourth_plus_eight_gapped_arb_n21.py`
- Workflow: `.github/workflows/eui-reoptimize-6131-full-fourth.yml`
- Diagnostic output: `evidence/ising_full_fourth_plus_eight_gapped_n21.json`
- Arb output, if the LP returns a dual candidate: `evidence/ising_full_fourth_plus_eight_gapped_arb_n21.json`

The reoptimizer first reconstructs each exact-rational gapped path and checks its block-minor features against the independent full-matrix feature implementation. It then solves the same scaled full-second/fourth LP. The HiGHS output is discovery only.

## Decision rules

1. If the LP returns a separating dual, the verifier rationalizes the printed coefficients and independently checks all 6,131 columns with Arb. Only a successful certificate supports a finite-pool theorem.
2. If the LP returns a feasible primal, the output is only a floating candidate. A separate exact-rational weight freeze and interval verification of all 1,461 coordinates is required before claiming a positive ensemble.
3. Solver failure, insufficient dual margin, or an ambiguous interval is not a theorem and must be reported as unresolved.

This experiment does not cover all positive nonuniform couplings or all multi-segment paths, does not impose every even principal minor, and does not imply a Choi-state or channel diamond-distance bound.
