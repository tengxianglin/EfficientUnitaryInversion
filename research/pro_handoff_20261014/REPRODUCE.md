# Reproduction entrypoints

Package verification (standard library):

```bash
python verify_bundle.py
```

Create a new output directory first. These are reference replay commands, not a statement that this preparation reran them:

```bash
mkdir exploratory_replay_001
python source/grid/verify_grid_examples.py --output exploratory_replay_001/grid_examples.json
python source/grid/independent_exact_grid_verifier.py --output exploratory_replay_001/abstract_census.json
python source/theory/verify_new_theory.py --output exploratory_replay_001/theory.json
python source/heisenberg/verify_heisenberg_tied_inversion.py --boundary open --n-min 2 --n-max 6 --output exploratory_replay_001/open.json
python source/heisenberg/verify_heisenberg_tied_inversion.py --boundary periodic --n-min 3 --n-max 6 --output exploratory_replay_001/periodic.json
python source/heisenberg/verify_triangle_intertwiner.py --output exploratory_replay_001/triangle.json
python source/heisenberg/run_heisenberg_followup_extensions.py --output exploratory_replay_001/extensions.json
python source/heisenberg/verify_phase_covariant_inversion.py --output exploratory_replay_001/phase.json
python source/heisenberg/verify_affine_spectrum_controls.py --output exploratory_replay_001/affine.json
python source/heisenberg/validate_triangle_gate_compilation.py --output exploratory_replay_001/compiled.json
```

The full abstract census may exceed a single cloud tool timeout. Estimate first or analyze the supplied complete records and run smaller independent checks. Some original grid/theory scripts permit output overwrites; the caller must enforce fresh paths. Heisenberg sources reject existing outputs. Exact algebraic fields and numerical diagnostics must be compared separately.

Dependencies: grid checkers use Python standard library only; theory checker uses NumPy; Heisenberg sources use NumPy/SymPy/SciPy, with Qiskit also needed for compilation. The original September 9 environment was Python 3.12.7, NumPy 1.26.4, SciPy 1.13.1, SymPy 1.13.2; Qiskit 2.2.3 for compilation. Version differences can change floating residuals and gate synthesis; record actual versions and retain original thresholds. requirements-reference.txt records this historical package set, not an instruction to replace an existing environment.

Background S1/S2 certificate regeneration is outside this supplied dependency closure. Read their explicit proof/resource records as historical evidence, and request targeted source supplementation if it becomes decisive.
