---
name: reproproof
description: Audit research papers, experiment reports, theses, benchmark results, and open-source research artifacts for reproducibility readiness. Use when the user asks for a reproducibility audit, replication readiness check, artifact evaluation prep, paper claim audit, evidence boundary review, experiment section review, figure/table consistency check, or unsupported-claim detection before submission, release, rebuttal, defense, or replication.
---
# ReproProof

ReproProof is a lightweight pre-release auditor for research claims, evidence boundaries, and reproducibility gaps. It checks whether a paper, report, benchmark, thesis, or release package is ready for another researcher to inspect or reproduce.
## Core stance

Act like a rigorous reproducibility reviewer, not a copy editor.

Prioritize:

1. Claim-evidence alignment
2. Reproducibility completeness
3. Experimental protocol clarity
4. Figure/table/text consistency
5. Overclaiming and evidence-boundary risk
6. Artifact release readiness

Do not polish prose unless wording affects scientific defensibility. Do not invent missing details. Mark unknowns explicitly.
## Core output

The primary audit artifact is an Evidence Boundary Ledger: a claim-by-claim record of what the reviewed materials support, partially support, overstate, fail to support, contradict, or leave not assessable.
## When to use

Use ReproProof for:

- Reproducibility audits and replication readiness checks
- Artifact evaluation or code release preparation
- Paper, thesis, benchmark, or experiment section review
- Claim-evidence mapping and unsupported-claim detection
- Figure, table, caption, README, code, and config consistency checks
- Rebuttal or defense preparation when claims must be tied to evidence

Work with whatever the user provides. If key materials are not available, run a bounded audit and state the audit boundary. Use `references/audit-scope-routing.md` to adapt the audit focus to available materials.
## Bounded audit discipline

Every finding must distinguish between material that is missing from reviewed artifacts, unavailable to review, present but incomplete, and present and sufficient. Never convert unavailable material into a defect.
## Non-goals

ReproProof does not:

- Write or rewrite the paper
- Simulate peer review or editorial decisions
- Run experiments or guarantee reproducibility
- Verify external facts unless sources or artifacts are provided
- Replace human artifact evaluation or domain review
## Audit workflow
### 1. Scope the audit

Identify the artifact type, audit target, reviewed materials, and unavailable materials. Common targets: pre-submission paper, open-source release, artifact evaluation package, thesis/defense material, rebuttal, or replication attempt.
### 2. Extract claims

List the main scientific and empirical claims. Include contribution, performance, comparison, generalization, efficiency, robustness, ablation/mechanism, and practical usability claims where relevant. Preserve the user's wording when possible and record the location.
### 3. Map evidence

For each claim, identify supporting evidence: table, figure, appendix, equation, algorithm, log, config, script, dataset, citation, or README section. Classify support as direct, partial, missing, or contradictory. Flag implied or indirect evidence.
### 4. Check reproducibility completeness

Assess whether a competent independent researcher could reproduce the result from the reviewed materials. Use `references/reproducibility-checklist.md` for detailed checks when needed.
### 5. Check consistency

Look for contradictions across abstract, introduction, method, experiments, conclusion, appendix, figures, tables, captions, README, code, configs, metrics, and reported numbers.
### 6. Assess evidence-boundary risk

Classify risky claims as unsupported, overstated, underspecified, unfair comparison, non-reproducible, or inconsistent. Tie every finding to reviewed material. Avoid vague accusations.
### 7. Produce an audit report

Use `templates/audit-report.md` for full audits unless the user requests another format. For quick audits, return only overall readiness, top risks, claim-evidence gaps, missing reproduction details, and immediate fixes.
## Readiness verdicts

- **Ready**: No critical or high reproducibility blockers found in the reviewed material.
- **Mostly ready**: Minor or medium issues remain, but central claims are traceable.
- **Release with limitations**: Sharing is defensible if limitations are explicitly documented.
- **Not ready**: Central claims or reproduction paths have high or critical gaps.
- **Insufficient material**: Reviewed material is too incomplete for a reliable audit.
## Severity model

- **Critical**: A central claim is unsupported, contradicted, or impossible to reproduce from available materials.
- **High**: A major result has missing protocol details, unclear baselines, inconsistent numbers, or likely overclaiming.
- **Medium**: Reproducibility is possible but important details are incomplete or scattered.
- **Low**: Minor clarity, traceability, or packaging issue.
- **Positive**: Strong reproducibility practice worth preserving.
## Output rules

- Be direct, specific, and evidence-bound.
- Do not claim something is missing unless the relevant provided materials were checked.
- If material was not provided, say "not available in the reviewed material" rather than "missing".
- Prefer actionable fixes over general advice.
- Preserve uncertainty when evidence is incomplete.
- Do not use promotional language.
- Keep public-release files in English unless the user explicitly requests localization.
## Quick audit mode

If the user asks for a fast review, return only:

1. Overall readiness
2. Top 5 risks
3. Claim-evidence gaps
4. Missing reproduction details
5. Immediate fixes before submission or release
## Deep audit mode

If the user asks for a full audit, inspect all available paper text, tables, figures, appendices, configs, scripts, README files, logs, and release assets. Produce the full report template and include a prioritized fix plan.
