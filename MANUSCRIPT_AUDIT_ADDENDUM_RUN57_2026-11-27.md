# EUI research audit — Run 57 (2026-11-27)

## Repository and issue selection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- Starting main HEAD: `4f9f851d63513facb1060bdeca294ae660017fad` (Run 56 finalization).
- Recent commits and the merged PR #9 were inspected. The latest prior scientific result was the 74-atom N=42 period-two ensemble matching all 861 pair coordinates and six quartic translation orbits (231 quartets).
- Open issues rechecked: #7 (physical reachability / positive ensembles), #5 (full physical-family convex hull), #6 (Appendix B noise normalization), and #3 (classifier correctness). Issue #7 was selected because the certified six-orbit support supplied a concrete next quartic residual to test. Issue #4 remains closed.

## New N=42 nine-orbit positive ensemble

A deterministic NumPy 2.3.5 / SciPy 1.17.0 search used seed 351 and 100,000 positive period-two candidate pairs in [0,100]^2. The resulting 40-base-atom support was frozen with exact-decimal couplings. Each atom was symmetrized with its one-site translate, giving 80 physical atoms.

The independent 256-bit Arb workflow [45932791312](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45932791312) passed. The exact-real weights are reconstructed from a 40x40 interval system. The determinant interval is
`[6.9410873420103589179538316236902944e-50 +/- 9.65e-117]`,
and the minimum weight is
`[0.0007816680367558847538021943219787... +/- 4.04e-72] > 1/10000`.
All 861 pair coordinates and 357 quartic coordinates in nine full translation orbits are certified. All cycle couplings are strictly positive; the minimum is the exact rational
`5804273538392679/1000000000000000`.

The verifier also checks all 42 translates of the next unmatched quartic
representative [0,3,18,21] and certifies a residual strictly greater than
1/250 for this frozen ensemble.

## Exhaustive floating quartic screen and next blocker

The discovery script enumerates all 2,670 cyclic translation orbits of
four-subsets; the orbit-size sum is exactly 111,930. For the frozen nine-orbit
support, the largest absolute binary64 residual is 0.004540390901740525 at
[0,3,18,21]. Adding that tenth orbit makes the LP infeasible on the same fixed
100,000-candidate pool. This is only a finite-pool floating result: no exact
Farkas certificate or continuous-period-two pricing theorem is claimed.

The highest-value next action is to rationalize and independently certify a
Farkas vector for that fixed candidate pool, then price it over the continuous
period-two parameter domain. If a continuous escape is found, append it and
reoptimize; if not, the result remains a finite-pool obstruction until an
analytic inequality or certified global minimization closes the continuum.

## Manuscript and supplementary-source audit

Default-branch searches for `documentclass`, `bibliography`, and
supplementary-material terms returned audit notes but no editable tracked
TeX/Bib manuscript or separate supplementary source. The public manuscript
remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown
Unitary Operations with Structured Hamiltonians*, arXiv:2506.20570v1.
No formal manuscript text or Appendix B table was changed. Issue #6 still
records the notation/protocol mismatch and the unregenerated QuAIRKit-backed
robustness table.

## Changes and evidence

Created:
- `evidence/n42_period_two_nine_quartic_atoms.json`
- `verify_n42_period_two_nine_quartic_ensemble_arb.py`
- `discover_n42_period_two_nine_quartic_ensemble.py`
- `.github/workflows/eui-n42-period-two-nine-quartic.yml`
- `THEORY_N42_PERIOD_TWO_NINE_QUARTIC_ENSEMBLE.md`

The workflow generated and committed:
- `evidence/n42_period_two_nine_quartic_discovery.json`
- `evidence/n42_period_two_nine_quartic_ensemble_arb.json`

Commit chain before this audit:
- `a03e0b0`: freeze nine-quartic support;
- `7c9c15d`: independent Arb verifier;
- `b32276b`: deterministic discovery/full-orbit scan;
- `637d528`: CI workflow;
- `dfcf43d`: discovery and Arb certificates committed by CI.

Workflow [45932791312](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45932791312) passed dependency checks, compilation, deterministic LP reproduction, all 2,670-orbit floating scan, 256-bit Arb certification, and artifact upload.

## Scope

This is a positive physical partial design, not a complete fourth-order or
all-even-moment ensemble. The tenth-orbit miss is specific to the frozen
support. The 10-orbit candidate-pool infeasibility is not a global
period-two-family theorem. No Choi trace-distance or diamond-distance bound
is inferred from these program moments.


## Follow-up: rationalized tenth-orbit dual rejected by a continuous Arb witness

After the nine-orbit certificate, the ten-orbit floating candidate-pool LP
was infeasible on its fixed 100,000 columns. A rationalized version of its
floating Farkas vector was frozen with exact rational coefficients. The
independent 256-bit Arb workflow
[45933314487](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45933314487)
certified a strictly-positive period-two physical point
(a,b)=(8.94088796,97.09897923) at which the functional score is
[-0.483006473660593274... +/- 8.31e-72], while its target score is
[-0.999999264540337711... +/- 7.40e-75]. Thus this exact rational functional
cannot be a global separator.

Important limitation: the rationalized functional's nonnegativity on all
100,000 finite-pool columns was only screened in binary64 (minimum about
6.18e-7); those inequalities were not independently Arb-certified. No exact
finite-pool Farkas theorem is claimed. The result only proves that this
rationalized candidate has a continuous physical escape.

New files:
- `evidence/n42_period_two_tenth_orbit_dual_escape.json`
- `verify_n42_period_two_tenth_orbit_dual_escape_arb.py`
- `evidence/n42_period_two_tenth_orbit_dual_escape_arb.json`
- `.github/workflows/eui-n42-period-two-tenth-orbit-dual-escape.yml`
- `THEORY_N42_TENTH_ORBIT_DUAL_CONTINUOUS_ESCAPE.md`

The CI committed the Arb evidence as `8baa9f1`. The next action is to derive
a different finite-pool dual with a certified margin and subject it to
continuous pricing before attempting a global claim.


## Final repository state for this run

- Final main HEAD: `98adb341787868b6b4e5b37189069a1edd0464e5`.
- Tenth-orbit escape input: `e01a1ff`.
- Independent Arb verifier: `1d16bf4`.
- Escape CI workflow: `b4972c5`.
- Arb certificate committed by CI: `8baa9f1`.
- Dual-escape theory note: `9b94465`.
- Initial audit append: `b9c7ed6`; final audit correction: `98adb34`.
- Both new workflows, [45932791312](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45932791312) and [45933314487](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45933314487), are confirmed completed with SUCCESS.
- Issue #7 comments 7208820125 and 7208881702 record the nine-orbit ensemble and the separate rationalized-dual continuous escape. Issue #5 comment 7208820469 records the cross-track scope distinction.
