# EUI manuscript/repository audit — Run 29 (2026-11-26)

## Repository and issue state inspected

Repository: `tengxianglin/EfficientUnitaryInversion`

- Mainline at this audit: `fca6b51fdd7aee2874bc7a2c5a695dd985ccc74a`.
- Recent commits were inspected through the 204-column finite-pool certificate, 204-column torus search/verifier, and finite-time search/verifier setup.
- Open research issues inspected:
  - #5 — finite-pool minimax obstruction / full-family EUI gap (selected highest-leverage theory track);
  - #6 — Appendix B per-instance L1 noise normalization (implementation fixed; manuscript source correction and full QuAIRKit table regeneration remain);
  - #3 — type-1.2 classifier correctness (dependency-light regressions passed; full QuAIRKit-backed smoke test remains).

## Manuscript and supplement audit

The public manuscript remains [arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1). Its main text describes the structured-Hamiltonian inverse protocols and claims numerical robustness under support perturbations. Appendix B (HTML lines 294–304) writes the noisy Hamiltonian as a supported part plus \(\delta\) times an out-of-support coefficient vector, defines \(\delta\) using the L1 ratio of the coefficient vectors, and says both coefficient vectors are sampled independently from standard normal distributions. The table reports 10,000-sample average Choi fidelities. This is a distribution-dependent numerical experiment, not a worst-case Hamiltonian theorem or a diamond-norm guarantee.

Issue #6 records the implementation distinction: the five checked routines normalize each raw out-of-support Gaussian row to match the in-support L1 norm before multiplying by \(\delta\). Thus the code realizes the intended per-instance relative L1 strength; the mismatch is in the manuscript's description of raw versus normalized Gaussian coefficients. No editable TeX/Bib/PDF manuscript or supplement source is tracked in the repository, so no formal manuscript edit is claimed.

## Selected scientific issue and completed work

Issue #5's 203-column finite-time escape was appended as physical column 1661. The fixed 2,113-row design was reoptimized at 204 columns.

### 1. 204-column finite-pool theorem

The design contains 21 complete second-order, 1,440 complete fourth-order, 645 selected/cut sixth-order, and 7 selected eighth-order rows.

Binary64 HiGHS discovery:
- objective: 0.3855817390106711;
- recomputed maximum residual: 0.38558173901226533;
- primal/dual discovery gap: 2.586264535864302e-13;
- support size: 71.

The rationalized dual has exact L1 norm
\[
\|z\|_1=\frac{4611686018426502061}{4611686018427387904}<1,
\]
and objective
\[
\lambda+z^Ty=\frac{1778181914757622867}{4611686018427387904}.
\]
With exact slack \(10^{-8}\), independent 128-bit Arb verifies all 204 columns; the maximum shifted-column upper endpoint is \(-8.980803464660286\times10^{-9}\). Therefore
\[
\eta_{204}\ge
\frac{694602292437797922939891}{1801439850948198400000000}
=0.38558172901092974\ldots>\frac13.
\]

The exact program-mass TV corollary is
\[
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{17810315190712767254869}{387656137538470562495468750}
=4.5943591410171576\ldots\times10^{-5}.
\]
It is for mixtures over exactly the 204-column pool in one selected parity sector / dephased program-label register, not a Choi or diamond bound.

Evidence:
- LP: `evidence/joint_low_six_eighth_lp_204col_uniform_ray_escape_n21.json`
- Arb dual: `evidence/55probe_204col_uniform_ray_escape_dual_certificate_n21.json`
- TV: `evidence/204col_program_mass_tv_bound_n21.json`
- certification workflow [45657144300](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45657144300), success.

### 2. 204-column continuous torus escape

An eight-start deterministic 21-torus search (seed `202611260040`, NumPy 2.3.5, SciPy 1.15.3, L-BFGS-B, at most 120 iterations/start) found binary64 score 1.4230491133899206. The analytic cofactor-gradient check defect was 1.2278706314693422e-8.

Independent 128-bit Arb certifies the exact rational-decimal phase vector:
\[
S_{204}(R(\theta_*))
\in[1.423049113389920506173001037795141\pm6.68\times10^{-34}]>0.
\]
The lower endpoint is itself strictly positive. By the exact dense-ray theorem and continuity, this proves existence of some finite positive equal-coupling time on the 42-site open path that escapes this particular 204-column dual.

Evidence:
- `evidence/204col_uniform_torus_search_n21.json`
- `evidence/204col_uniform_torus_arb_n21.json`
- workflow [45657547014](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45657547014), success.

The finite-time search is now separately running in workflow [45658174449](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45658174449). No explicit rational time is claimed until the search transcript and independent Arb certificate are committed.

## Scientific scope and blockers

**Proved in this run:** the fixed 204-column / 2,113-row minimax lower bound, its exact program-label TV corollary, and a positive point of the continuous uniform-path torus for the particular 204-column dual.

**Not proved:** the complete all-even-principal-minor positive-ensemble problem at \(n=21\); complete sixth/eighth-order orbit control; a global physical-family converse; or a quantitative operational bridge to Choi trace distance / channel diamond distance.

The finite-pool dual is a certificate only for its 204 listed columns and fixed mixed-order row design. The torus escape shows this particular dual is not a global separator on the continuous equal-coupling ray; it does not invalidate the finite-pool theorem or settle full-family feasibility/infeasibility.

## Next highest-value action

Finish workflow 45658174449. If its 12-start finite-time search yields a candidate, require the exact rational time and 128-bit Arb pricing interval to be strictly positive before calling it an explicit physical escape. Then use the new dual's escape as column 205 for one more fixed-design cutting-plane diagnostic, but do not let column-count growth displace the central structural task: construct the complete positive ensemble or prove a global physical-family converse, and establish the operational Choi/diamond bridge.

## Runtime/model note

Repository changes and GitHub Actions runs are real. The requested GPT-6.1-sol Max model tier cannot be selected from this execution environment, so no model-switch claim is made.
