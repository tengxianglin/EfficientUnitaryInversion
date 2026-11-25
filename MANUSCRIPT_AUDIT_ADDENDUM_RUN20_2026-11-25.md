# EUI manuscript and Appendix B audit — Run 20 (2026-11-25)

## Scope inspected

- Repository head before this update: 2c0e620879a368373667888edae321e612f518a7.
- Open issues: #5 (finite-pool/full-family theory frontier) and #3 (type-1.2 classifier correctness).
- Public manuscript: [arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1), including Appendices A–E. Appendix B is the support-mismatch robustness experiment.
- The repository tree has 1,006 tracked paths and no editable manuscript TeX/Bib/PDF or separately tracked supplement source.

## 1. Appendix B normalization audit

Appendix B, HTML lines 294–304, writes

\[
H=\sum_{P\in\mathcal S}\alpha_P P+
\delta\sum_{P\in\mathcal S'}\beta_P P
\]

and defines \(\delta\) as the ratio of the out-of-support and in-support coefficient \(L_1\) sums. It then says that \(\alpha_P\) and \(\beta_P\) are sampled independently from standard normal distributions.

Taken literally with \(\beta\) denoting the raw Gaussian draw, equations (B.1)–(B.2) are inconsistent: multiplying the raw draw by the separately defined ratio would apply the scale twice. The code resolves the intended convention.

In every one of the five routines in robustness_analysis.py, the raw out-of-support Gaussian batch is normalized independently for each Monte-Carlo instance:

\[
\widetilde\beta^{(r)}
=
\frac{\|\alpha^{(r)}\|_1}{\|g^{(r)}\|_1}g^{(r)},
\qquad
g^{(r)}_P\stackrel{\mathrm{iid}}{\sim}\mathcal N(0,1),
\]

and the actual noisy coefficient vector is \(\delta\widetilde\beta^{(r)}\). Therefore

\[
\frac{\|\delta\widetilde\beta^{(r)}\|_1}
{\|\alpha^{(r)}\|_1}
=\delta
\]

for every sampled instance (up to floating-point roundoff).

**Interpretation:** the code implements the intended per-instance relative \(L_1\) perturbation. This audit does not identify evidence that the reported table used a \(\delta^2\) perturbation. The manuscript's prose/equation is nevertheless underspecified: it must distinguish the raw iid-Gaussian direction \(g\) from the normalized vector \(\widetilde\beta\), and define \(\delta\) as the ratio after scaling. A consistent replacement is

\[
\widetilde\beta_P
=
\frac{\sum_{Q\in\mathcal S}|\alpha_Q|}
{\sum_{Q\in\mathcal S'}|g_Q|}g_P,
\qquad
H_\delta
=
\sum_{P\in\mathcal S}\alpha_P P+
\delta\sum_{P\in\mathcal S'}\widetilde\beta_P P.
\]

This gives \(\|\delta\widetilde\beta\|_1/\|\alpha\|_1=\delta\) by construction.

## 2. Code hardening and verification

The repeated normalization expression was extracted to utils/noise_scaling.py and all five routines now call the same helper. The helper rejects zero-norm rows, mismatched batch shapes/dtypes/devices, and non-finite or negative \(\delta\). The command-line delta grid is now a reusable list rather than a one-shot iterator, so enabling multiple protocol functions does not silently exhaust the grid after the first function.

The regression test covers the support dimensions of all five protocols, 10,000 samples per protocol, and \(\delta\in\{0,0.001,0.01,0.1\}\). With PyTorch 2.10.0 CPU and float64, the maximum observed absolute error in the per-instance ratio was \(5.551115123125783\times10^{-17}\). Three unit tests pass, including zero-row and invalid-input checks.

Evidence: evidence/robustness_noise_normalization.json. Reproduction: python -m unittest tests/test_robustness_noise_normalization.py -v.

The full Choi-fidelity simulation was **not** rerun: PyTorch 2.10.0 is available in the current environment, but QuAIRKit is not installed. The table values therefore remain unverified by this run. The new GitHub Actions workflow installs pinned CPU PyTorch and runs the normalization regression; it does not claim to reproduce the Choi table.

## 3. Required manuscript correction

When the editable manuscript source becomes available, revise Appendix B so that:
1. raw Gaussian draws and per-instance normalized coefficients have different symbols;
2. \(\delta\) is explicitly the realized relative \(L_1\) norm after scaling;
3. the coefficient normalization is stated before the 10,000-instance sampling description;
4. all five protocol rows are regenerated from a pinned environment and fixed random seeds, with the per-protocol sample means and software versions archived.

No formal manuscript source edit is claimed because no TeX/Bib/PDF source is tracked in this repository.

## 4. Evidence boundary and next action

- **Verified from source code:** all five routines normalize each raw out-of-support Gaussian vector so the realized relative coefficient \(L_1\) norm equals \(\delta\).
- **Verified numerically:** the helper preserves that ratio to \(5.56\times10^{-17}\) maximum absolute error over the recorded 20 protocol/delta cases.
- **Not verified:** the published average Choi-fidelity table, because QuAIRKit is unavailable in this environment.
- **Not implied:** a worst-case Hamiltonian guarantee, a worst-case input guarantee, or a channel diamond-norm bound.

Next highest-value action: obtain the editable manuscript source and the pinned QuAIRKit environment, correct (B.1)–(B.2), and regenerate all five Appendix B rows with fixed seeds and archived raw means.


## Commit and CI identifiers

- Production refactor: [2c0e620](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/2c0e620879a368373667888edae321e612f518a7).
- Shared helper, tests, evidence, workflow and this audit: [5a7e045](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5a7e045012e2cf97b7a18c69607b7d50784a9128).
- README verification instructions: [3810fdae](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/3810fdae773e5dac49400c6625d28da095edfebf).
- Production-wiring assertion and py_compile step: [08b68c5](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/08b68c5ade068970ced05bebb419fa0a0ce0c62c).
- Final workflow: [45564164419 — SUCCESS](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45564164419).
- Final main HEAD at audit close: 08b68c5ade068970ced05bebb419fa0a0ce0c62c.
