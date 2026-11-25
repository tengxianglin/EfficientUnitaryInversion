# EUI research audit — Run 38 (2026-11-26)

## Repository and issue selection

Inspected the current default-branch head, recent commits, open issues, Issue #7 discussion, the N=42 perfect-matching construction, the cycle-parity theorem, the N=8 alternating single-atom theorem, the period-two pair/quartic partial design, and the manuscript audit.

- Main HEAD before this run: f12b4ec865fd136d928c0c36b73f0d522cc62409.
- The 35-atom period-two partial design is hosted-verified in workflows 45700330683 and 45700425742.
- The N=42 cycle-matching parity theorem is hosted-verified in workflow 45685188470.
- Open scientific track selected: Issue #7, physical reachability of the balanced-slice target.

The repository tree had 1,154 entries and was not truncated. No .tex, .bib, .pdf, .doc, or .docx manuscript/supplementary source was present. The manuscript audit therefore remains anchored to the public arXiv HTML source; this run does not claim a manuscript-text edit.

## New theorem

For every N=4m+2 >= 6, if a signed perfect-matching atom R_M=P_M D is a physical cycle exponential exp(A(c)), then the matching contains at least two edges that are also edges of the physical cycle.

The proof has three parts:
1. Invariance of the nonzero-edge support graph under the matching permutation, with componentwise preservation because exp(A) is block diagonal over support components.
2. Reversal of every even path component, or an edge-axis reflection in the full-cycle case, supplies two adjacent matched pairs.
3. The only remaining full-cycle involution, the half-turn, is excluded by a complex-trace congruence: tr_C(A)=0 from nearest-neighbour support, but e^A=iI forces the sum of n odd quarter-turn phases to be nonzero when n is odd.

## Exact separating functional

For Q=R D, define Lambda(Q)=-sum_j det Q_{j,j+1;j,j+1}. On a matching atom Q=P_M, this is exactly the number of cycle-adjacent matching edges. It is at least 2 on every physically reachable matching atom and every positive mixture thereof.

The balanced target has Lambda=N/(N-1), so the strict gap is (N-2)/(N-1). At N=42 this is exactly 40/41.

This closes the matching-atom route: no reweighting or pruning of physically reachable perfect-matching atoms can match even the adjacent-pair moments. It does not provide a separator for general non-matching physical exponentials.

## Verification

- Exact verifier: verify_physical_matching_ensemble_adjacent_pair_obstruction.py.
- Machine-readable evidence: evidence/physical_matching_ensemble_adjacent_pair_obstruction_n42.json.
- Checks: 21 edge-axis reflections; half-turn adjacency count and odd trace congruence; all 2^20 even-path compositions via exact binomial component counts; exact N=42 target and gap; exact N=4 matrix counterexample.
- The N=4 counterexample confirms the N=4m+2 hypothesis is essential.
- The proof is analytic; the script checks finite arithmetic and combinatorial bookkeeping rather than numerically approximating matrix exponentials.

## Next highest-value action

Move beyond signed matching atoms. The exact SO(42) matching ensemble is a useful unrestricted benchmark, but its physically reachable subset is separated from the target already by adjacent-pair moments. The next decisive task is to derive a functional valid on the full continuous family Q(c)=exp(A(c))D, or to construct a non-matching positive physical ensemble satisfying all even principal-minor moments. The existing 35-atom period-two construction only covers all pairs and four quartic translation orbits; it is not a complete fourth-order or all-order design.
