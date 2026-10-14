# EUI grid independent Codex audit, round2 (2026-10-14)

Start with `codex_verdict.md`, then the four `proofs/` documents. `NEXT_PRO_PROMPT.md` is the ready-to-paste next Pro instruction; the received Pro task is unchanged under `inputs/NEXT_CODEX_TASK_PROMPT.md`. Original R1 ZIP and its receipt are preserved under inputs. No Pro submission is claimed.

Authoritative fresh outputs:
- T1: `results/T1_final/`, source provenance `results/T1_source_provenance/`.
- T2: `results/T2_final/`.
- T3: `results/T3_transport_verified/`, `results/T3_circuits_streamed/`, `results/T3_saved_artifact_audit.json`.
- T4: `results/T4_final/`, `results/T4_final_independent_verification.json`, `results/T4_final_fixed_maps.json`.
- R1 fresh reproduction: `results/r1_fresh/`;77 original tests passed.

All main tasks reached completed terminal states. The failed initial T4 verification and corrected rerun are retained, with the exact-zero diagnostic. Preliminary source versions and outputs are provenance, not additional independent evidence.

`runs/` records serialized CPU-only commands, environment, terminal state, timing and budgets. CPU process accounting covers science commands and compilation/tests, not editing, packaging or network delivery. `BUILD_MANIFEST.json` hashes every delivered file except itself. Original raw text files that contain machine-local paths are preserved byte-for-byte inside `raw_execution_evidence.zip`; corresponding readable files are explicitly portable path projections, with original/projected hashes in `PORTABLE_PROJECTION.json`. Input ZIP bytes and mathematical data are not silently rewritten.

Reproduction needs installed Python, NumPy, SciPy, SymPy, pytest and C++17. No installation, GPU, solver or network is required for the science. Run the provided commands from this cycle directory, using fresh output directories. The source R1 directory is the sibling `../grid_discovery_20261014_r1`; the original frozen handoff is `../pro_handoff_20261014` in the Git branch. If using only this standalone ZIP, recover those same bytes from the preserved received ZIP or use its frozen_input ZIP. Never overwrite historical outputs.

T1: `c++ -O2 -std=c++17 code/rref_census.cpp -o <fresh_backend>` then `python code/audit_rref.py --n 3 --all-ordered-bases --backend <fresh_backend> --source ../grid_discovery_20261014_r1/results --output <fresh>`. T2: `python code/audit_comb_indices.py --dims 2 4 --targets transpose adjugate2 --certificates ../grid_discovery_20261014_r1/results/comb_certificates.json --output <fresh>`.
T3: `python code/audit_transport.py --representatives quadratic37 --input ../grid_discovery_20261014_r1/results --output <fresh>` and `python code/compile_all_anti.py --input ../grid_discovery_20261014_r1/results/validation/all_anti_grids.json --seed 20261015 --samples-per-grid 3 --output <fresh>`.
T4: `python code/tied_coeff_span.py --input ../grid_discovery_20261014_r1/results --grids matched_q4 B4q0 B55q0 --constraints independent row column uniform --span-max-degree 7 --graded-max-degree 15 --rays ternary --output <fresh>`; independent checks `code/verify_t4.py` and `code/t4_fixed_map.py` take --input <that fresh output> --output <fresh JSON>.

No novelty, hardware/QPU execution, gate/ancilla minimum, general coefficient-subspace theorem, or finite-ray feasibility is claimed. Known logical universal-transpose bounds remain attributed to prior work in received R1; the current audit supplies self-contained independent certificates and narrower stated conclusions.
