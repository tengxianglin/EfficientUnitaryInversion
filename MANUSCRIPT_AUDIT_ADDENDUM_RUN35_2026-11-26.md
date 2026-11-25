# EUI manuscript/research audit — Run 35 (2026-11-26)

## Repository state and issue selection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- Starting HEAD inspected: 03320e3d4e7f4339280301c00f185ad55cb3fac9.
- Rechecked recent commits, all four open issues (#7, #5, #6, #3), Issue #7 comments, the perfect-matching SO(42) construction and reachability theorem, the N=4/N=6 physical constructions, the N=8 and N=42 period-two single-atom no-go results, and the current manuscript audit notes.
- Issue #7 remains the highest-leverage theory track: the full unrestricted-SO(42) moment target is known exactly, but physical cycle-family convex-hull membership remains unresolved.

## New scientific result

A numerical feasibility search over 5,000 period-two candidates with \(a,b\in[0,50]\) found a 31-atom positive solution to the complete N=42 second-order pair-moment system. The 31 parameter pairs were frozen as exact decimal rationals. An independent 256-bit Arb verifier then reconstructs the unique exact-real weights from a square 31-by-31 system.

The proof uses the period-two Fourier symbols, ten same-parity displacement classes, twenty of twenty-one cross-parity classes, and one normalization equation. The omitted cross-parity equation follows from the exact row-norm identity
\[
2\sum_{d=1}^{10}(x^2-C_d^2)+\sum_{d=0}^{20}(-x^2-S_d^2)=-1.
\]
The certificate checks all 861 unordered pairs in the original site indexing. Every atom has \(a,b>0\), so all 42 cycle couplings are strictly positive.

The same exact weights fail the quartic coordinate \(I=\{0,1,2,3\}\) by more than \(1/200\), certified by Arb. This is a limitation of the frozen ensemble, not an impossibility theorem for other mixtures.

## Interpretation

- The N=42 period-two single-atom no-go remains intact.
- The period-two convex hull does contain the full second-order target.
- Consequently, second-order moments alone cannot provide a global separator against period-two mixtures.
- The complete even-principal-minor target remains unresolved; no fourth-or-higher-order ensemble is claimed.
- No Choi or diamond-distance statement follows from this pair-moment certificate.

## Reproducibility artifacts

- evidence/n42_period_two_pair_moment_atoms.json
- verify_n42_period_two_pair_moment_ensemble_arb.py
- evidence/n42_period_two_pair_moment_ensemble_arb.json
- .github/workflows/eui-n42-period-two-pair-moment-ensemble.yml
- THEORY_N42_PERIOD_TWO_PAIR_MOMENT_ENSEMBLE.md

The Arb workflow is the authoritative check. The frozen HiGHS candidate pool is discovery only; the proof uses the exact rational coupling strings and interval-certified linear solve.

## Next highest-value action

Augment the pair-feasible period-two mixture with fourth-order orbit constraints. First solve a small candidate LP over additional positive \((a,b)\) atoms, then freeze any candidate support and certify the exact-real weights and all selected quartic orbit moments with Arb. A finite-pool solution is not a global physical-family theorem; the complete all-even-moment target remains the final criterion.


## Final hosted verification

Workflow [45699551876](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45699551876) completed successfully. The exact-real interval solve certifies:
- determinant interval excludes zero;
- minimum weight is greater than \(1/2000\);
- weight sum is one;
- all 861 second-order principal-minor coordinates equal the target;
- the quartic witness \(\{0,1,2,3\}\) misses the target by more than \(1/200\).

The first workflow attempt failed only because the verifier iterated over 42 indices for a 31-coordinate feature vector. This was corrected in commit 6df78435804f19425338cdeebb9d21e739d3e537; the rerun passed. The certificate was committed in 1cd42e69dfaee79da4243fa043e6d0636ec4698e.
