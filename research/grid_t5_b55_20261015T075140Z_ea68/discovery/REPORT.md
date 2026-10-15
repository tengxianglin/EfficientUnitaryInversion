# Public Skill Discovery Record

Date: 2026-10-15  
Search close time: 07:51:46 UTC  
Per-call timestamps: not exposed by the web tool; only the session close time is retained here.  
Scope: generic public skill repositories and catalog entries for symbolic exact computation, linear algebra verification, quantum circuit / Pauli / unitary verification, and scientific evidence or reproducibility packaging. No private project material was used in search queries.

## Search and inspection log

1. web.run search round 1, four queries:
   - site:skills.sh quantum computing skill agent SKILL.md
   - GitHub "SKILL.md" "symbolic" linear algebra
   - GitHub "SKILL.md" scientific reproducibility evidence packaging experiment
   - agent skills quantum circuit Pauli verification SKILL.md
   Search result refs included turn0search0 through turn0search11. This surfaced reproducibility and mathematical-computation candidates, including verify-results, ReproRun, SageMath, Math.Skill, and SymPy.

2. web.run search round 2, four queries:
   - site:github.com "SKILL.md" "quantum circuit" "Pauli" agent skill verification
   - site:github.com "SKILL.md" "quantum" "unitary" agent skill
   - site:skills.sh "symbolic" "math"
   - site:github.com/VeryMath/AI4Math-Sagemath-skill "SKILL.md"
   Search result refs included turn1search0 through turn1search11. No focused quantum unitary-inversion certificate skill surfaced.

3. web.run source inspection:
   - Opened the original SageMath source at https://raw.githubusercontent.com/VeryMath/AI4Math-Sagemath-skill/main/sagemath-skill/SKILL.md (turn2view0, 102 total lines). The full body appeared in the returned result and is transcribed in sagemath-skill.source.md.
   - Opened the original Math.Skill source at https://raw.githubusercontent.com/Wholiver/Math.Skill/main/SKILL.md (turn2view1, 606 total lines). The returned body was partial in the conversation output. Verbatim excerpts visible there are preserved in math-skill-returned-excerpts.txt; the unseen remainder is not reconstructed.
   - Opened the original ReproProof source at https://raw.githubusercontent.com/YimingLi0923/reproproof-skill/main/reproproof/SKILL.md (turn2view2, line count only), then opened that same source from line 0 (turn3view0, 108 total lines). Its full returned body is transcribed in reproproof.source.md.

4. web.run catalog inspection:
   - Opened https://skills.sh/, redirected to https://www.skills.sh/ (turn4view0). The general leaderboard and topic links were visible; no focused exact-math or quantum certificate skill surfaced there.

## Source disposition

- Adapt selectively — SageMath Skill: reference-first API lookup, explicit parent rings/fields, and reporting actual runtime output may help when a task explicitly uses SageMath. Its setup and execution procedures are conditional and do not supply a unitary-inversion certificate method.
- Reject wholesale — Math.Skill: useful local checks include dimension compatibility, rank analysis, reconstruction, and orthogonality. Its broad routing and mandatory two-method policy are not a good fit for exact certificates; numerical sampling can be weak evidence for exact claims.
- Adapt only if useful — ReproProof: its claim-to-artifact ledger and separation of unavailable, incomplete, and sufficient evidence are reusable ideas, with substantial overlap against existing evidence-packaging skills.
- No inspected public source provides a clear exact quantum unitary-inversion certificate workflow. Existing local skills remain the closer task fit.

## Search-result leads not fetched as original bodies

These appeared in search output only; their original SKILL.md bodies were not fetched under the three-source cap:

- https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/sympy/SKILL.md
- https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/verify-results/SKILL.md
- https://github.com/zihaoye5/icra-skills/blob/main/skills/icra-reproducibility/SKILL.md
- https://github.com/WUBING2023/ReproRun/blob/main/paper-reproduction/SKILL.md

## Limits and failures

- No further searches or source fetches were performed after the source results above.
- The web output included the literal text: You can’t perform that action at this time. This appeared twice after GitHub search-result content and not on the three inspected raw source opens.
- No raw downloaded byte files were returned, so source SHA-256 hashes are unavailable. The saved source documents are text transcriptions of the web output, not byte-preserving downloads.
- The Math.Skill result reported 606 total lines, but the conversation output did not contain the complete body. Only verbatim excerpts visible in that output are saved. Do not infer or reconstruct the unseen remainder.
- No install, local code execution, or experiment was performed. No project-code source files were edited; only the discovery documents in this directory were written.
