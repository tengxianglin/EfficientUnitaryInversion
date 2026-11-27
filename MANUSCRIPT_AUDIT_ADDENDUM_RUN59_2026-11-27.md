# EUI research audit — Run 59 (2026-11-27)

## Repository and issue selection

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Starting HEAD: `617202485ee4720df565160fc96cfad678876460` (Run-58 audit).
- Rechecked recent commits, all four open issues (#7, #5, #6, #3), recent #7/#5 comments, current Actions runs, the Run-58 audit, the N=42 ten-orbit discovery/verifier/evidence, the current fourth-moment hierarchy note, and the public arXiv HTML manuscript with Appendices A–E.
- Issue #7 remains the highest-leverage positive-ensemble track. The 82-atom ten-orbit ensemble is a verified partial construction; its 11-orbit finite-pool infeasibility is not a continuum theorem.

## Run-59 attempted separator: rejected by its first Arb regression

I explored the sum of all fourth-order principal minors containing a fixed pair and initially wrote an incorrect 2x2-block determinant shortcut. The first hosted regression, [workflow 45942068441](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45942068441), failed at the direct 780-minor sum. For the first rational sample, the proposed identity residual was approximately 0.9625068757963673, far outside its Arb enclosure.

This was a mathematical derivation error, not an environment or dependency failure. The proposed period-two no-go claim is withdrawn. The invalid draft theory, verifier, and workflow were deleted before this audit was completed.

## Correct result: universal pair–quartic incidence identity

For every real symmetric involution Q of size 2n with trace zero, and every fixed two-subset I,

```
sum_{J subset I^c, |J|=2} det Q_{I union J,I union J}
    = 1 - (n-2) det(Q_{I,I}).
```

The proof uses a block decomposition Q=[[T,X],[X^T,B]], the block equations from Q^2=I, the Schur complement of T in diag(0_I,I)+zQ, and the eigenvalue decomposition of B into range(X^T) and its orthogonal complement. The generic invertibility argument extends to all symmetric involutions by polynomial continuity.

For N=42 (n=21), this becomes

```
sum of 780 quartic minors containing I + 19 * pair_minor(I) = 1.
```

The balanced target satisfies it exactly:
- pair target: -1/41;
- each quartic target: 1/533;
- 780 quartets containing a fixed pair: 780/533 = 60/41;
- 1 - 19*(-1/41) = 60/41.

Therefore this incidence sum is **not** a physical separator. It is a universal affine dependency shared by every symmetric balanced-signature atom, including all physical cycle exponentials.

### Novelty/duplication audit

A subsequent repository search found that this pair-incidence identity is already a corollary of the stronger, earlier `THEORY_FOURTH_MOMENT_HIERARCHY.md`, which proves the triple-set relation
```
sum_{I superset K, |I|=4} det Q_I = - sum_{J subset K, |J|=2} det Q_J,   |K|=3.
```
Summing that relation over triples containing a fixed pair and using the row-sum identity `sum_{k != i} det Q_{ik} = -1` yields the pair-incidence identity. Thus Run 59 does **not** claim a new hierarchy theorem or priority. The companion note records an independent Schur-complement derivation and an independent direct Arb regression. The existing hierarchy already supplies the stronger LP reduction: its 147-by-1440 orbit-incidence matrix has certified rank 147, reducing the design to 1,314 equations including normalization.

## Corrected reproducibility artifacts and hosted verification

- `THEORY_N42_PRINCIPAL_MINOR_INCIDENCE_IDENTITY.md`: alternative proof, explicit corollary relation to the pre-existing hierarchy, and direct regression target.
- `verify_n42_principal_minor_incidence_identity_arb.py`: 256-bit Arb regression that reconstructs Q for five exact-rational period-two samples, checks Q symmetry/involution/trace, and directly sums all 780 incident quartic minors.
- `.github/workflows/eui-n42-principal-minor-incidence-identity.yml`: pinned python-flint CI and machine-certificate upload.
- Machine output: `evidence/n42_principal_minor_incidence_identity_arb.json`.

Workflow [45942386352](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45942386352) completed **SUCCESS**. It checked five rational samples and 780 quartic minors per sample at 256-bit Arb precision. All five identity residual intervals contain zero; the largest reported radius is below 5e-73. The target identity is exactly checked as 60/41=60/41. Evidence commit: `b403b178524d64a71acaba330d90b775af5d2276`; artifact ID `15173551526` (SHA256 `d8bfa68e0ea40a06de5a30c4ab5511db5f6ec7c06b15a2b98f05ba8487a13924`).

The finite Arb samples are regression checks only. The continuum identity is proved analytically; the stronger triple-set hierarchy and its exact orbit-rank certificate were already present in the repository before this run.

## Manuscript audit

The public manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, [arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1). The current HTML manuscript exposes Sections I–VIII and Appendices A–E. No editable tracked TeX/Bib source or separate supplementary source was found in the repository. Appendix B's per-instance L1 normalization wording/implementation mismatch remains tracked in Issue #6; the full QuAIRKit table has not been regenerated. No Choi trace-distance or channel diamond-distance statement was added.

## Changes, verification status, blockers, next action

- Added the alternative pair-incidence derivation, independent Arb verifier, CI workflow, and machine evidence; explicitly linked it to the stronger pre-existing fourth-moment hierarchy.
- Corrected theory commits: `5a5dc1c40fb09cc7fd36e149a9fd64dc44345667`, `d5da45a5ca0e2f874e66897c506b27d57c2373aa`, `dd5d24ae23e648b618f5563ca2207dd9ed1a9c37`, and `cb37eae4a02ebd0d46ec81b3d2fd5542c7415490`.
- Corrected verifier: `a4ae5f1352510a094b5db94f69043877b737b049`; workflow: `8a8f4b62830dcc2d284713720567f568098258fd`; machine evidence: `b403b178524d64a71acaba330d90b775af5d2276`.
- Removed invalid draft workflow/verifier/theory in commits `e3533fea5824dd2937a269fbf1899e502f28d368`, `5dd805bd5f96d7166c833d65845e66759e5869ad`, and `9d94dbdfce5b6696bc50311bb0f3853346e81251`.
- Still blocked: complete non-period-two physical ensemble or global separator; remaining higher even moments; operational bridge from moment discrepancy to Choi/diamond error.
- Next highest-value action: build on the existing triple-incidence hierarchy and its exact 147-row orbit reduction, then search for a symmetry-broken physical ensemble. Any proposed dual must be priced over the full allowed cycle family before being called global.
