# EUI manuscript/repository audit — Run 28 (2026-11-25)

## Repository state inspected

Repository: `tengxianglin/EfficientUnitaryInversion`

- Mainline at the time of this audit: `bc7dfc4f1a62c1412041444971688794e8bdd3c3`.
- Recursive Git tree: 1,087 paths, not truncated.
- No tracked `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplement source is present.
- Open research issues inspected: #5 (finite-pool/full-family EUI gap), #6 (Appendix B normalization), and #3 (type-1.2 classifier/QuAIRKit smoke test). Issue #5 remains the highest-leverage active theory track.

## Manuscript and supplement check

The public manuscript remains [arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1). Appendix B, lines 294–313, defines the noisy Hamiltonian and relative (L_1) scale and reports 10,000-sample average Choi fidelities. This is a distribution-dependent numerical robustness experiment, not a worst-case Hamiltonian theorem or a diamond-norm bound. The raw-Gaussian versus per-instance-normalized coefficient mismatch remains tracked in Issue #6; the code normalization helper is already tested, but the full QuAIRKit fidelity table has not been regenerated.

## Selected issue and work performed

Issue #5's Run 27 frontier certified a 203-column / 2,113-row finite-pool dual and then found an explicit finite-time escape of that particular dual. The exact 203-dual escape is

[
t_{203}=\frac{5594112299050130881369}{500000000000000}>0,
]

with 41 equal positive internal couplings on the 42-site open path.

Added:
- `reoptimize_204col_uniform_ray_escape.py`
- `.github/workflows/eui-reoptimize-204col-uniform-ray.yml`

The reoptimizer reconstructs the already-present 202-column path at physical label 1660 from its own Arb certificate and appends the 203-dual escape as label 1661. It keeps the fixed 2,113-row design (21 complete second-order, 1,440 complete fourth-order, 645 selected/cut sixth-order, 7 selected eighth-order rows). It pins the 203 LP, rational dual, cut design, and finite-time certificate hashes and re-certifies the parent before running HiGHS.

## Verification status

- Pinned environment installation: passed.
- Regression tests and Python compilation of the 204-column reoptimizer: passed in workflow [45638510647](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45638510647).
- Independent 203-column dual, program-mass TV, torus, and finite-time Arb parent re-certification: passed in the same workflow.
- The first 204 run, [45638216359](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45638216359), reached the LP setup but failed because the 201-column ancestor time variable was checked before being assigned. The ordering was corrected in commit `bc7dfc4f1a62c1412041444971688794e8bdd3c3`.
- Current run [45638510647](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45638510647) has passed compile/regression and all parent re-certification; the 204-column HiGHS step is still in progress at the time of this note. No 204-column LP objective or theorem is claimed yet.

## Scientific scope and next action

This experiment is only a fixed 2,113-row cutting-plane diagnostic. If HiGHS returns an above-(1/3) objective, the next proof obligation is a new exact rational dual plus independent Arb pricing of all 204 columns and then continuous physical pricing. If it returns below (1/3), freeze an exact rational primal and independently verify all pinned rows plus the complete sixth-order orbit condition. Neither outcome alone resolves the complete all-even-principal-minor positive-ensemble problem at (n=21).

Still unresolved:
1. Complete all-even-principal-minor positive ensemble or a global physical-family converse.
2. Complete sixth/eighth-order orbit control.
3. A valid quantitative bridge from program-mass/moment discrepancy to Choi trace distance or channel diamond distance.

Next action: retrieve the final status and generated evidence from workflow 45638510647, update Issue #5 with the actual LP result, and proceed to the appropriate exact rational dual/primal verification branch.

## Model/runtime note

The repository changes and GitHub Actions execution are real. The requested GPT-6.1-sol Max model tier cannot be selected from this execution environment, so no model-switch claim is made.
