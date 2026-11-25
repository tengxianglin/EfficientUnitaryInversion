# EUI manuscript/research audit — Run 33 (2026-11-26)

## Repository state and selection

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- HEAD at start: `9c135fc572e25c2f9701c17c96894cd04064df16` (Run 32 N=8 period-two obstruction audit).
- Recursive tree at start: 1,132 paths, not truncated. After this run's artifacts: 1,136 paths, not truncated.
- Open issues rechecked: #7 physical cycle-family convex hull; #5 finite-pool/full-family gap; #6 Appendix B noise normalization; #3 type-1.2 classification.
- The highest-leverage active question was Issue #7: the new unrestricted-SO(42) perfect-matching ensemble exactly matches all even principal-minor moments, but its support was not physically characterized.
- Rechecked manuscript/source inventory: no editable `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` files are present. Research/theory notes are the current editable record.

## Scientific result completed

### General parity obstruction for matching atoms

Proved the following theorem:

For (N=4m+2), if a signed perfect-matching matrix (R_M=P_MD) equals (e^{A(c)}) for any real skew-symmetric generator supported on the cycle (C_N), then every matched pair must join opposite parity classes.

The proof is support-graph based:
1. (A) commutes with (e^A=R_M), so the matching permutation preserves the nonzero-edge support graph of (A).
2. (e^A) is block diagonal over support components, so the matching involution preserves each component.
3. Proper components are paths; a fixed-point-free path automorphism is reversal of an even path and pairs opposite parity.
4. If the support is the full cycle, fixed-point-free involutive dihedral symmetries are edge-axis reflections or the half-turn. Both swap parity when (N=4m+2).
5. Isolated vertices are impossible because a matching has no fixed points.

This is valid for arbitrary real couplings, including zero entries; it is not a numerical or finite-search statement.

### Exact N=42 counting consequence

- Total matching atoms: (41!!=13,113,070,457,687,988,603,440,625).
- Bipartite (even-odd) matchings: (21!=51,090,942,171,709,440,000).
- Therefore at most
  [
  rac{21!}{41!!}=rac{262144}{67282234305}
  =3.896184523416147ldots	imes10^{-6}
  ]
  of the uniform matching support can be physically reachable.
- At least
  [
  rac{67281972161}{67282234305}
  =0.9999961038154765ldots
  ]
  of that particular uniform SO(42) matching measure lies on atoms proved unreachable.

This quantifies the nonphysicality of the *specific matching representation*. It does not prove that the balanced-slice target is outside the convex hull of all physical cycle exponentials, and it does not classify the remaining cross-parity atoms.

### Modulus scope check

An exact N=4 counterexample shows why (Nequiv2pmod4) is essential. For matching (M={(0,2),(1,3)}), an explicit cycle generator with couplings ((pi/4,pi/4,-pi/4,-pi/4)) exponentiates to (P_MD). The verifier checks the integer identities (K^T=-K), (K^3=-4K), and (e^{(pi/2)K}=I+K^2/2=P_MD).

## Artifacts and verification

Created:
- `THEORY_CYCLE_MATCHING_ATOM_PARITY_OBSTRUCTION_N42.md`
- `verify_cycle_matching_atom_parity_obstruction.py`
- `evidence/cycle_matching_atom_parity_obstruction_n42.json`
- `.github/workflows/eui-cycle-matching-parity-obstruction.yml`

Updated:
- `THEORY_PERFECT_MATCHING_BALANCED_SLICE_ENSEMBLE_N42.md` with a link and summary of the new obstruction.

The verifier exhaustively enumerates matchings for N=4,6,8,10, recomputes exact double-factorial/factorial counts and the N=42 reduced fractions, and checks the N=4 counterexample by exact integer matrix arithmetic. Local execution and compilation passed.

GitHub Actions [45685188470](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45685188470) completed successfully; compile and exact verifier steps both passed.

Issue [#7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7) received progress comment 7172308290 with the theorem, exact counts, evidence, and limitations.

## Commit record

- `d1e58050c54c5ee3901ead52d3229b1ac33d463b` — exact verifier.
- `5ea8f9dc893b975dfc26e0032cd5e9e4a7139264` — machine-readable evidence.
- `4d8d6b48b05ae983fa0328c5a7d81d1cf81d6df6` — theorem note.
- `69d9aa2252b390444e9b9e85d307b1e3d22784e7` — CI workflow.
- `06838b8bc3e0cffb6ee5d5683686df76be101ddb` — link from the SO(42) matching-ensemble note.

HEAD before this audit note: `06838b8bc3e0cffb6ee5d5683686df76be101ddb`.

## Related theory and remaining scope

The repository also contains `THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md`, a separate conditional full-diamond minimax theorem with certified joint ensembles at n=5 and n=7; its all-long-ring ensemble existence remains conditional. `THEORY_ODD_CYCLE_PARITY_ROBUSTNESS.md` treats a separate parity-breaking noise model. Neither result converts the new matching-atom mass bound into a Choi/diamond lower bound for the N=42 convex-hull problem.

## Next highest-value action

Strengthen the support-graph characterization for the remaining cross-parity matching atoms. For a candidate matching involution (p), exact reachability requires a nonempty p-invariant subset of cycle edges whose connected components are each preserved by p; path components must be reversed, while a full-cycle component must carry a fixed-point-free dihedral involution. Derive a direct combinatorial characterization/count for N=42 and then test whether any surviving matching atoms admit exact cycle logarithms. Keep this atom-level problem separate from the still-open question of whether a different positive physical measure matches the complete target.
