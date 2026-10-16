# EUI R4 — pinned GitHub-first archival intake, NOT an experiment

Use `$pro-codex-research-loop` from the user-pinned Codex Skills commit:
`tengxianglin/codex-config@635db3e2952491963d78c5bbe8d2079c371f132a`.
Protocol: `pro-codex-research/4.1`.

## What is and is not authorized
The user requested GitHub-first handoff migration. This entry prepares a **manual**
Pro-to-Codex launch; it does not automatically start Codex, execute a scientific
task or send a message. Preserve the R4 `FREEZE_WRITE` decision.
Scientific CPU/GPU/replicates: **zero**. No grid census, SDP, T1–T5 reruns, new
promise searches, hardware jobs, random tests, gate minima or remote publication.
No article edit, no new code edit, no paper repository enable/import, no Overleaf
action. Do not use a moving branch HEAD to replace the pinned source.

## Bounded, independent read-only preflight (only if the human launches it)
1. Fetch the **exact handoff commit and entry SHA-256 provided by Pro**, not HEAD.
   Check `BUILD_MANIFEST.json`, `cycle_manifest.json`, `CLAIMS.json` and the
   `inputs/R4_ARCHIVE_IDENTITY.json` digest. Reject hash/path mismatches.
2. Confirm the original source commit `28c7e0ffb833a88f6980011ffecf48c7fbe2f1b1` is available. Inspect the
   actual local checkout state without overwriting, rebasing, resetting, fetching
   unapproved external hosts, or modifying tracked/untracked research files.
3. If the original R4 ZIP is **already accessible under an approved local path**,
   optionally compare its SHA-256 with `d9f81ff1273ade8e422472d9ade6c355bd264f848ad35eef7ea275b79685ec95` and original theory note with
   `7dc922216e4008bc137d79e4c2abb5fd41b622bdd7c885794808e2adbfb4d631`. If missing, say `not_accessible`, not `verified`.
   Never fetch those protected bytes through the public experiment repository.
4. Report the actual metadata/check results, blockers, and `not_run` status. End
   this administrative check. Do not create a new scientific task or claim paper
   integration. Any future manuscript action needs actual source and separate scope.

## Limits / stop rules
One local CPU process; read-only wall time at most 30 s; <=1 GiB RAM, <=20 MiB
new temporary disk, no GPU, no formal science runs. Stop immediately on a checksum,
authorization or source mismatch; preserve evidence as failed/blocked rather than
retrying to obtain a favorable result. A correctly resolved pointer and manifest
support only **transport readiness**, not theorem correctness, novelty, paper
readiness or receipt by Codex.

## Expected outcomes
**Supporting:** exact source/entry hashes match and approved local archive, if
present, has its expected digest; report transport VERIFIED, science NOT_RUN.
**Falsifying/blocking:** hash mismatch, incorrect source revision or inaccessible
protected input; report the precise failure and stop. Missing private paper
binding specifically blocks full manuscript integration, not read-only transport.
