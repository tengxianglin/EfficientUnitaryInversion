# EUI manuscript and evidence audit — run 16 (2026-11-25)

## Current manuscript and supplement status

The project’s public manuscript remains [arXiv:2506.20570v1, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*](https://arxiv.org/html/2506.20570v1). The previously completed manuscript audit of Appendix B remains relevant: the reported 10,000-instance robustness experiment is distribution-dependent average Choi fidelity, not a worst-case Hamiltonian guarantee or a diamond-norm theorem.

The latest repository state was inspected through commit [da9fe176](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/da9fe176a429992f7ce9d06f161390dfad6cb6a9). The default branch still has no tracked editable TeX/Bib manuscript or separate supplementary source. This run therefore adds a theorem/evidence note, not a claimed revision of the formal paper body.

## New verified result

The 6,137-column / 1,461-coordinate full-second-/fourth-order finite-pool obstruction is independently Arb-certified by [workflow 45539976654](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45539976654), with evidence commit [da9fe176](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/da9fe176a429992f7ce9d06f161390dfad6cb6a9).

For exactly 22 base atoms, 6,101 fractional single-open-path grid atoms, and 14 exact-rational gapped paths, the 94-term rational dual has
\[
\|D^{-1}y\|_1=1,\qquad \|y\|_1=533,
\]
and Arb certifies every column gap above (1/5). Thus every mixture on this exact pool obeys
\[
\|b-Ap\|_\infty>1/2665,\qquad
\operatorname{TV}(w_p,u_{\rm bal})>1/5330.
\]
The TV conclusion is for the balanced program-label distribution / dephased classical register, not Choi trace distance or channel diamond distance. The diagnostic’s legacy status label still says “not Arb-certified”; the separate certificate, which pins the diagnostic hash, is authoritative.

## Current continuous-pricing frontier

The 6,135-column parent dual has now been re-priced against its refreshed parent hashes. [Workflow 45539362903](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45539362903) succeeded and the refreshed 256-bit Arb escape certificate is recorded in [commit f68544e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f68544ea5266424878f42a79f2209c6e34c9f58b). The two exact-rational paths in that certificate are what raise the pool from 6,135 to 6,137.

The 6,137 finite-pool theorem does not settle the continuous physical family. The next experiment is a fresh deterministic connected/multi-segment pricing search against the **94-term 6,137 dual**, followed by independent 256-bit Arb verification of any frozen exact-rational escape.

## Remaining paper-level blockers

1. Construct an exact positive physical ensemble satisfying every even-principal-minor constraint at (n=21), or prove a global obstruction for the full allowed physical family.
2. Establish a rigorously quantified bridge from program-mass/moment discrepancy to Choi-state trace distance or channel diamond error.
3. Obtain the editable manuscript and supplementary source files before claiming formal paper-body revisions.
