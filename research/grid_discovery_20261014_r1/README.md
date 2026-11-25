# Efficient Unitary Inversion — grid discovery r1

Read `THEORY.md` first, then `NEXT_CODEX_TASK_PROMPT.md`. Primary-source access and attribution are in `RELATED_WORK.md`; exact commands and a bounded fresh-run wrapper are in `REPRODUCE.md`.

This round derives the missing cross-line phase bit, corrects three-qubit quadratic realizability to 973 abstract types/37 grid orbits, proves a cubic exponential-envelope law, and supplies a phase-aware one-query target classification for **nine independent real coefficients**. Explicit multi-Kraus and comb arguments are separated from finite-sample matrix checks. Three failed candidate claims and their counterexamples are retained.

`results/exact/` contains calibration, all64 forms and all1024 refinements. `results/validation/` contains the actual973 dense-matrix inputs, all30 all-anti grids/circuits, phase gauges and counterexamples. `results/comb_certificates.json` contains exact integer optimality certificates. `results/reproductions/` preserves both actual clean reruns; the portable rerun uses a frozen input directory with no adjacent archive. Logs include the failed test-reader attempt and the repaired run; final release tests: **77 passed**.

Six hypotheses are recorded in `hypothesis_ledger.json`; every scientific batch and meaningful failure/preflight is in `experiment_ledger.json`. The recorded timed processes and clean reruns total about82 CPU-seconds, excluding unmeasured reading/editing/probes; no GPU, paid VM or user remote device was used. Scientific numerical tests are `finite-support`, not a substitute for proofs.

Frozen input remains unchanged. The GitHub branch was readable, but no write action or authenticated local network workflow was available. **No new GitHub commit or push exists for this round.** The add-only patch targets `research/grid_discovery_20261014_r1/` on top of baseline `62fa763aff42e4bedf82b5de19bc9f05c5ed83b2`; existing draft PR2 was not changed. See `github_delivery.json` and the outer delivery validation record.

The original executed checker before a metadata-only portability repair is preserved at `logs/source_versions/grid_check_initial.py`, so its hash in first-run outputs remains auditable. Current executable checker is `code/grid_check.py`; its portable rerun records the new source hash. Frozen historical outputs were never rewritten to remove contradictions.
