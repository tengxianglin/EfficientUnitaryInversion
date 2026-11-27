# EUI manuscript/evidence audit — Run 60 (2026-11-27)

## Repository state and issue selection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- Starting HEAD inspected: 6dffc495c59d712a6cb25b6a2e232945a00234d8 (Run 59 incidence-identity correction).
- Worktree state was inspected through recent commits, current tree entries, evidence, and the latest workflows. The most recent prior mathematical items were the N=42 principal-minor incidence identity (workflow 45942386352, SUCCESS), the N=8 period-two mixture no-go, and the N=42 ten-quartic-orbit partial ensemble (workflow 45935129650, SUCCESS).
- Open issues rechecked: #7 (physical cycle-family convex hull / positive ensembles), #5 (finite-pool versus full physical family), #6 (Appendix B normalization), and #3 (Hamiltonian classifier correctness). Issue #7 was selected: the N=8 period-two family had just been excluded analytically, but the corresponding unrestricted non-period-two N=8 cycle convex-hull question was still open. The small-size N=4/N=6 physical constructions made N=8 the smallest decisive next test.

## New exact result: full N=8 physical cycle convex-hull feasibility

Let \(R=e^{A(c)}\), \(D=\mathrm{diag}(1,-1,\ldots,1,-1)\), and \(Q=RD\). The balanced-slice target at \(N=8,n=4\) is
\[
\tau_I=(-1)^r\binom4r/\binom8{2r},\qquad |I|=2r.
\]
Its order-2, 4, 6, and 8 values are \(-1/7,3/35,-1/7,1\).

Four gapped perfect-mirror block compositions give an exact construction:

| Composition | Weight |
|---|---:|
| (1,1,1,1,1,1,1,1) | 1/105 |
| (1,1,6) | 16/105 |
| (1,2,5) | 80/105 |
| (1,3,1,3) | 8/105 |

A block of length \(L\) uses \(c_{s+r}=(\pi/4)\sqrt{(r+1)(L-r-1)}\) for its internal edges, with all cuts and the wrap edge zero. The standard spin-\((L-1)/2\) rotation at angle \(\pi\) gives the signed reversal \(R_{r,L-1-r}=(-1)^r\). The block primitive is established perfect-transfer/spin-rotation technology; see Christandl et al., *Phys. Rev. Lett.* 92, 187902 (2004), DOI 10.1103/PhysRevLett.92.187902. No novelty is claimed for that primitive.

Symmetrize each base atom over the 16-element dihedral group. Because a dihedral map either preserves or swaps the two sublattices, \(P_gDP_g^T=\pm D\); the global sign drops out of every even-order principal minor. The 64 labelled group images merge into 37 distinct signed-permutation matrices. The aggregate weights are exactly:
- 17 atoms of weight 1/105;
- 16 atoms of weight 1/21;
- 4 atoms of weight 2/105.

The exact orbit table has 4 pair orbits, 8 quartic orbits, 4 sixth-order orbits, and 1 full-set orbit. The dependency-free verifier checks every one of the 128 even subsets (including the empty subset) using integer and Fraction arithmetic. All 127 nonempty even-subset moments match exactly; there are zero failed checks. No floating-point matrix exponential or numerical optimizer enters the certificate.

This proves that the full N=8 real nearest-neighbour cycle-exponential convex hull contains the complete balanced-slice even-principal-minor target. It does not contradict the N=8 period-two mixture no-go: the present measure is not supported entirely on \(c_{2j}=a,c_{2j+1}=b\); three of the four base patterns break that symmetry.

## Reproducibility

Added:
- THEORY_PHYSICAL_CYCLE_ENSEMBLE_N8.md — exact construction and orbit proof;
- verify_n8_physical_cycle_balanced_slice_ensemble.py — independent signed-permutation verifier;
- evidence/n8_physical_cycle_balanced_slice_ensemble.json — exact machine certificate;
- .github/workflows/eui-physical-cycle-ensemble-n8.yml — dependency-free CI.

The first workflow attempt, 45955796719, compiled and recomputed the certificate but failed only because the committed JSON used a different valid whitespace layout from json.dumps output. The workflow was corrected to compare parsed JSON objects rather than bytes. The corrected workflow 45955932031 completed SUCCESS: Python compilation, all 128 exact subset checks, semantic certificate comparison, and artifact upload all passed.

Key commits:
- f9f3be5c4a7df98c54e496eb6e23663d06bf6d09 — theory;
- 8c58047fbaacd2ea7b31669d5cf46b878e97b148 — verifier;
- bf45da816dc788fd999391dafeeeda20cc04b91a — evidence;
- a8a4318865bdd91fa9ba1756d1fa7232ba58e081 — initial workflow;
- 6ef125391fa84f645cd16dfa22b19ddac729d723 — semantic JSON comparison fix.

## Manuscript and literature audit

The public manuscript [arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1) was reopened. It contains Sections I–VIII and Appendices A–E; no separate supplementary source was linked from the inspected HTML. The repository tree still has no editable manuscript TeX/Bib or standalone supplementary source. No formal manuscript text or Appendix B noise table was modified. Issue #6 remains the owner of the unresolved full QuAIRKit-backed normalization/table regeneration.

The literature check confirms that engineered spin-chain perfect transfer is an established primitive (Christandl et al., PRL 92, 187902 (2004)). The present contribution is the exact four-base-atom, dihedrally symmetrized balanced-slice moment design, not the perfect-transfer Hamiltonian.

## Changes, verified claims, blockers, next action

**Changed:** added the N=8 physical-cycle ensemble theorem, exact verifier, machine evidence, CI workflow, and this audit; Issue #7 was updated with the exact construction.

**Proved:** a positive mixture of 37 distinct physical cycle exponentials realizes every even principal-minor balanced-slice target at N=8. The weights are strictly positive and all equalities are exact rational identities after the standard spin-rotation block exponentials are reduced to signed reversals.

**Verified:** all 128 even subsets, 17 dihedral orbit averages, determinant-one membership, symmetric-involution structure, exact weight normalization, and the 37-atom aggregate-weight histogram. Hosted workflow 45955932031 passed.

**Not proved:** N=42 physical-cycle convex-hull membership or nonmembership; an N=42 full positive physical ensemble; an all-size extension of the N=8 block-partition construction; and the operational moment-to-Choi/diamond bridge. Because \(n=4\) is even, this result does not extend the repository's odd-\(n\) program-span or joint-parity diamond theorem.

**Next highest-value action:** use the N=8 block-partition construction as a structural ansatz for N=42. Search for a probability law on contiguous mirror-block compositions and dihedral images whose complete even-principal-minor moments equal the balanced-slice target. First derive closed formulas for subset-closure moments of a random block partition; only then attempt a finite support or an exact obstruction. Do not extrapolate the N=8 weights to N=42 without proof.
