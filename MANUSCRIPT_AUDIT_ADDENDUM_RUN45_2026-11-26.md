# EUI research audit — Run 45 (2026-11-26)

## Selection and repository inspection

Issue #5 remains the highest-leverage active scientific track: after the 6,143-column dual was shown by two independently Arb-certified continuous escapes not to extend to the full gapped family, the next useful step was to append those paths, reoptimize the same complete second-/fourth-order design, certify the new finite-pool dual, and immediately price it continuously.

Repository inspection at this run:
- Default branch: `main`.
- Recursive Git tree: 1,188 entries; tree response was not truncated.
- No tracked `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplement source was found. README describes the code repository and the paper but does not supply an editable manuscript.
- Open scientific/correctness tracks inspected: Issues #5, #7, #6, and #3. Issue #5 is selected; #7 remains the separate physical reachability track, while #6 and #3 are distinct manuscript/protocol and taxonomy correctness tasks.

## 6,145-column finite-pool certificate — completed

The 6,145 pool is the pinned 6,143 pool plus two new exact-rational, 256-bit-Arb-certified escapes from the 6,143 dual:
- 22 base atoms;
- 6,101 fractional-grid atoms;
- 22 exact-rational general-gapped paths;
- 6,145 columns total.

The feature design remains complete at second and fourth order:
- 21 second-moment coordinates;
- 1,440 fourth-order dihedral orbits;
- 111,930 raw quartets before orbit reduction;
- 1,461 feature coordinates;
- 1,313 independent moment rows and 1,314 equalities including normalization.

Workflow [45787634578](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45787634578) completed successfully. Its steps included compilation, deterministic block-minor/restricted-spin/serialization regressions, the full HiGHS reoptimization, independent Arb pricing, and evidence publication.

The resulting certificate is:
- [6,145-column Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_two_gapped_arb_n21.json)
- [6,145-column diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_two_gapped_n21.json)
- Evidence commit [52fa465](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/52fa465cf6b99c2f0de38a521fd0c2c38a641364), produced by workflow run [45787634578](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45787634578).

Certified facts:
- 107 nonzero exact-rational dual coefficients;
- exact scaled dual norm \(\|D^{-1}y\|_1=1\), with \(D=\operatorname{diag}(41I_{21},533I_{1440})\);
- exact full-coordinate dual norm \(\|y\|_1=533\);
- common rational column gap \(1/5\);
- minimum Arb lower endpoint approximately \(0.2206104558375831>1/5\);
- 22 base/gapped columns checked at 512-bit Arb and 6,101 fractional-grid columns at 128-bit Arb.

Consequently, for every probability mixture over **this exact 6,145-column pool**,
\[
\|b-Ap\|_\infty>\frac{1}{2665},
\qquad
\operatorname{TV}(w_p,u_{\rm bal})>\frac{1}{5330}.
\]
The TV statement concerns the balanced program-label distribution / dephased classical label register. It is not a Choi trace-distance or channel diamond-distance bound.

The LP diagnostic reports HiGHS dual optimality and primal infeasibility, but those floating solver statuses are discovery metadata only. The finite-pool theorem is certified by the independently reconstructed exact-rational dual and Arb column pricing.

## Continuous pricing of the new 6,145 dual — added, first run diagnosed, retry pending

Added:
- `search_ising_full_fourth_plus_twenty_two_gapped_n21.py`;
- `verify_ising_full_fourth_plus_twenty_two_gapped_escape_arb_n21.py`;
- `.github/workflows/eui-full-fourth-plus-twenty-two-gapped-search-n21.yml`.

The deterministic search inherits the established connected/multi-segment protocol (frozen seed-pool starts, lognormal connected starts, fractional-profile perturbations, piecewise multi-segment starts, analytic Fréchet gradients, and exact-decimal freezing before Arb verification). Seed: `202611261842`. A finite multistart search can find a counterexample to this dual, but failure to find one cannot prove a continuum inequality.

First workflow [45804242553](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45804242553) compiled both scripts, then stopped at the discovery script's stale dimension guard: the copied 6,143 template still expected 20 gapped paths and 103 dual terms. The current certificate correctly has 22 gapped paths and 107 terms. No continuous pricing was performed in that failed run; this was a bookkeeping guard failure, not a mathematical result.

The guard was corrected in commit [63007ea](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/63007eafca2b607c3ba81ed8b71146e856fb9d48). The corrected workflow [45804379602](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45804379602) was queued at the latest status check. Its final result is pending and must be inspected before making any continuous-family claim.

## Proof boundary and next action

- **Proved:** a strict second-/fourth-order separation for the exact pinned 6,145-column finite pool.
- **Not proved:** separation of all continuous physical couplings; feasibility/infeasibility of the complete all-even-principal-minor positive ensemble at \(n=21\); full sixth/eighth and higher-order control; or a program-label-to-Choi/diamond operational bridge.
- **Next:** finish continuous pricing of the 6,145 dual. If an Arb-certified escape is found, append that exact-rational path and reoptimize; if none is found, report only the finite search result and do not call it a global bound. In parallel, the paper-level target remains an exact positive physical ensemble satisfying every even-principal-minor moment, or a global proof covering all allowed couplings.
