# Codex execution plan

Received R1 input is preserved byte-for-byte under inputs; receipt.json records hashes. Worktree starts at 62fa763aff42e4bedf82b5de19bc9f05c5ed83b2; unrelated main-worktree changes remain untouched. Additive R1 patch paths and every delivered hash passed before application. Existing draft PR2 and remote branch were read live and match the baseline.

## Online skill discovery and decision (2026-10-14)
Registered luna_worker performed bounded read-only public discovery in two web calls, no private disclosure or installation. Root then inspected original SKILL.md sources:
- https://raw.githubusercontent.com/VeryMath/AI4Math-Sagemath-skill/main/sagemath-skill/SKILL.md : exact Sage Python computation, documented API lookup, runtime evidence. Retain its exact-computation discipline; reject adoption of Sage dependency for the specified independent C++/Python integer task. No installation.
- https://raw.githubusercontent.com/Wholiver/Math.Skill/main/SKILL.md : explicit assumptions, stepwise derivation and multiple verification methods. Reject as redundant with installed verifying-pauli-identities and research-loop verification contract.
- https://github.com/BoltzmannEntropy/QuantumNovelty : Luna inspected README only, raw JSON claim audit and negative evidence discipline; domain mismatched and no original skill inspection, not adopted.
- https://github.com/OriginQ/pyqpanda3-skill/blob/main/SKILL.md : unavailable substantive body to Luna, simulator/API focus, not adopted.
No dedicated comb certificate skill found; this is discovery scope, not novelty evidence. Root retains installed pro-codex-research-loop, verifying-pauli-identities and implementation-consistency-checker.

## Gates and resource allocation
All scientific command execution uses code/run_bounded.py with a shared exclusive lock, explicit single CPU affinity and BLAS/OpenMP threads=1. GPU=0. Group CPU caps: R1 verifier/tests/fresh reproduction120s, T1 480s RAM1GiB, T2 300s RAM1GiB, T3 420s RAM2GiB, T4 480s RAM2GiB, total1800s. Disk cap300MiB, per T1/T2/T3/T4 caps80/30/80/100MiB. Compilation and diagnostic reruns consume the same group budget. No paid resources, no a6k/a6k2, no d8 SDP.
T1/T2 are independent priority audits; T3/T4 implementations may be prepared in parallel but all computations remain serialized. Every run gets fresh ID, stdout/stderr, command/environment/status/result and timing. Gate failures stop dependent rows; independent tasks may continue. T3 uses complex128 tol1e-10, seed20261015 and3 samples/grid. T1/T2/T4 exact checks have no random seed. T4 fixed rays {-1,0,1}^m excluding0, full degree7 and graded even14/odd15; independent9-parameter control through degree3 only.

## Acceptance and prohibited claims
Compare independent calculations with R1 only after own calculation. Preserve B1q3 forbidden embedding, all35 rank-only counterexamples, B4q0 cubic counterexample, S-gate wrong encoding and nonzero phase controls. Separate analytic-checked, exact-finite, finite-support, falsified and incomplete/not_run. No finite-ray feasibility, novelty, physical instrument existence, minimum ancilla/gates, hardware routing/noise or general coefficient-subspace theorem is implied.
Git delivery after successful R1 tests and fresh reproduction: commit only research additions on isolated branch and fast-forward intended target without force, verify remote ref and key blob hashes, retain PR2. Outgoing cycle version3 includes NEXT_PRO_PROMPT.md, not a new Codex-authored next task.
