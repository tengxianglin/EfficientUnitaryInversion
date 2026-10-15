# Reproduce the round

No network, GPU or paid resource is required for the science checks. The input is the unchanged extracted `EUI_Pro_Grid_Theory_20261014.zip`, or the repository directory `research/pro_handoff_20261014/` at the recorded baseline. The delivery ZIP contains a byte-identical copy of the original input ZIP as a convenience, outside the Git patch.

Required: Python 3.13.5 (the version actually tested; other compatible versions not audited here), a C++17 compiler, NumPy, SciPy, SymPy; pytest for tests. Exact versions actually used are in `environment.json`. There is no automatic package installation and no CVXPY dependency. On a compatible installed environment, from this round's directory:

```bash
python code/run_round.py \
  --input /absolute/path/to/frozen_handoff \
  --output /absolute/path/to/a_new_empty_run_name
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest tests -q
```

The output path must **not already exist** and must not be within frozen input. Each subprocess has a 40-second wall deadline; stop on failure instead of silently skipping. A slower machine can trigger a diagnostic timeout; raise a bound only after measuring and recording the change. Core work was far below the 30 CPU-minute initial budget. Compile artifacts go into the fresh run, not into the scientific input or source tree. The incremental run ledger is the only file intentionally updated inside a newly created run.

First-run granular commands are recorded in `experiment_ledger.json` and `/usr/bin/time` logs. Source `grid_check.py` reads frozen results only for calibration and comparison; its multiplication engine uses a literal standard single-qubit table, not a copied frozen cocycle. `physical_census.cpp` directly enumerates physical labels without calling the abstract embedding predicate. `validate_predictions.py` uses Kronecker matrices, exact integer spectral checks and independent phase gauges. `comb_certificate.py` uses integer identities and a stated PSD argument, not a solver.

Exact reproducibility fields are supports, counts, witnesses, rational primal/dual values, phases and status. Floating-point error norms, CPU time, memory use, absolute paths and platform/version strings are expected to vary. `results/reproduction_comparison.json` records the in-container clean rerun and its semantic comparisons.

The returned delivery manifest lists payload hashes. The manifest excludes itself, as explicitly stated in its schema. The external `.sha256` file hashes the whole ZIP. `verify_delivery.py` validates an extracted delivery without executing scientific code. Do not confuse a package hash, an uncommitted patch or a synthetic patch-check repository with a remote Git commit.
