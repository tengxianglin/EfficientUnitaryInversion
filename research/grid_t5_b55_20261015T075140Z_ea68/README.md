# EUI T5 B55 exact certificate

Start with codex_verdict.md and results/T5_summary.json. Proofs distinguish exact finite checks from analytic physical claims. Raw inputs and historical failures are preserved in inputs/EUI_Pro_R3_Handoff_20261015.zip. The portable package omits its extracted duplicate; extracting that ZIP into inputs/ restores the original input paths used by every command.

Run `python verify_delivery.py` before extraction to verify this immutable package. For reproduction, work in a new copy, extract the input ZIP into inputs/, and use the recorded commands with fresh output names and a fresh explicitly authorized budget. Existing budget ledgers are terminal and may not be reset. No dependencies were installed; Python/SymPy (see runtime_versions.json for the exact versions); runtime details are authoritative in runs/preflight-01/stdout.txt.

Dense entries are exact strings parsed by a whitelist AST (integers, rational arithmetic, I and sqrt); sparse entries map Hermitian IXYZ words to exact coefficients. Qubit order is left-to-right Kronecker; J order is logical qubit then three-dimensional multiplicity. Dagger, transpose and star are separate targets.
