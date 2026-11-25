# EUI manuscript/research audit — Run 31 (2026-11-26)

## Repository state inspected

- Repository: `tengxianglin/EfficientUnitaryInversion`
- Default branch: `main`
- HEAD at start of this run: `ac55b84fa89d86875640a7f896bb049497b7438d`
- Current HEAD after this run's commits: `d7068b7e758825354396a91c98b26171f74e04cd`
- Recursive tree at final check: 1,126 paths, `truncated=false`.
- No `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplementary source was present in the inspected tree.
- Open research tracks inspected: #7 (physical cycle-family convex hull), #5 (finite-pool/full-family gap), #6 (Appendix B noise normalization), and #3 (type-1.2 classifier correctness).

## Selected scientific issue

Issue #7 had just gained two exact small-size physical single-exponential constructions at N=4 and N=6. The highest-leverage follow-up was to determine whether the *same construction mechanism* can scale to N=42, rather than extrapolating from two small cases.

## New theorem: fixed-parity rank-one spectral-collapse obstruction

For alternating couplings, suppose the parity-block singular spectrum has one uniform mode at signed frequency `lambda=2(a-b)` and every nonuniform singular frequency is an odd multiple of `pi`. Then
`C=-I+gamma uu^T`, `S=sin(lambda) uu^T`, with `gamma=1+cos(lambda) in [0,2]`.

For a principal subset with p even and q odd vertices, p+q=2r, the matrix determinant lemma gives
`det(Q_I)=(-1)^p(1-2 gamma r/n+2 gamma p q/n^2)`.

Matching only a same-parity two-site target minor, `-1/(2n-1)`, forces
`gamma=n^2/(2n-1)` and `cos(lambda)=(n-1)^2/(2n-1)`.
For every integer n>=4 this exceeds 1. At N=8 it is 9/7; at N=42 it is 400/41. Thus the N=4/N=6 rank-one spectral-collapse mechanism cannot be extended to N>=8, even at second order. The same obstruction applies to any probability mixture supported entirely in this fixed-parity rank-one-collapse class because the relevant minor is affine in gamma.

This is **not** a no-go for arbitrary alternating couplings without spectral collapse, nonalternating cycle couplings, or mixtures over the full physical cycle-exponential family.

## Reproducibility artifacts

- `THEORY_ALTERNATING_SPECTRAL_COLLAPSE_NO_GO.md`
- `verify_alternating_spectral_collapse_no_go.py`
- `evidence/alternating_spectral_collapse_no_go.json`
- `.github/workflows/eui-alternating-spectral-collapse-no-go.yml`

The exact-rational verifier checks all 7 nonempty even subsets at N=4 and all 31 at N=6 using the closed formula, and verifies the required cosine is >1 for n=4,...,21.

CI:
- Initial run [45678333308](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45678333308) failed only because the verifier's printed summary used the wrong JSON key; compilation passed and the mathematical checks had not been reached.
- Fixed in commit `d7068b7e758825354396a91c98b26171f74e04cd`.
- Rerun [45678440640](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45678440640) succeeded, with output: N4=7 subsets, N6=31 subsets, N8 required cosine=9/7, N42 required cosine=400/41.

Issue #7 received a new progress comment (comment ID 7171375194) containing the derivation, scope limitation, evidence links, and next step.

## Evidence classes and remaining blockers

- **Analytically proved:** the rank-one spectral-collapse no-go for n>=4 and for mixtures confined to that ansatz.
- **Exact rational checks:** all even principal minors for the N=4/N=6 formula and the cosine obstruction through n=21.
- **Previously established:** the exact N=4/N=6 physical constructions; the matching-atom reachability theorem and its scope limitation.
- **Not proved:** feasibility or infeasibility of the complete N=42 target in the convex hull of all real cycle exponentials; no global physical-family separator; no Choi/diamond operational bridge.
- **Manuscript blocker:** no editable manuscript/supplement source in the repository, so no paper text was changed.

## Next highest-value action

Derive necessary conditions for a *general* period-two cycle exponential without assuming nonuniform modes are odd multiples of pi. In Fourier variables, use the complete second-order target to constrain every entry magnitude of the parity blocks (C=cossqrt{BB^T}) and (S=B,mathrm{sinc}sqrt{B^TB}). Determine whether those constraints are already inconsistent at n=4 or n=21. Keep this separate from the still broader full-cycle convex-hull problem.
