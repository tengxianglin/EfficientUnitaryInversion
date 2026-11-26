# EUI manuscript/research audit — Run 40 (2026-11-26)

## Repository and manuscript audit

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Current HEAD: `915227d7b5dbd28479ec7829e64cb44ec0495335`.
- Recursive Git tree: 1,167 entries, `truncated=false`.
- Open issues rechecked: #5 (finite-pool/full-family gap), #7 (physical reachability), #6 (Appendix B noise normalization), and #3 (type-1.2 classifier correctness). Issue #5 remains the highest-leverage open scientific track.
- No editable manuscript or supplementary source (`.tex`, `.bib`, `.pdf`, `.doc`, `.docx`) is present in the repository. The public manuscript inspected is Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, arXiv:2506.20570v1, submitted 25 June 2025: https://arxiv.org/abs/2506.20570. No formal manuscript text was modified.

## Scientific state selected

The paper-level long-ring question remains whether a positive measure over legal gapped physical cycle Hamiltonians can satisfy every even-principal-minor target, or whether a global physical-family converse exists. The DPP identity in `THEORY_PROGRAM_DPP.md` expresses each selected-parity program mass as a complement-folded projection-DPP probability; the conditional diamond theorem in `THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md` becomes unconditional for long rings only if the same legal ensemble is uniform in both parity sectors. The n=21 all-moment ensemble is not established.

## Parent 6,141-column evidence rechecked

The current parent finite pool contains 22 pinned base atoms, 6,101 fractional single-open-path grid atoms, and 18 exact-rational gapped paths. Its feature system includes all 21 distance-averaged second moments and all 1,440 fourth-order dihedral orbits (111,930 four-subsets before orbit reduction), with 1,313 independent moment rows / 1,314 equalities including normalization.

The independent Arb certificate `evidence/ising_full_fourth_plus_eighteen_gapped_arb_n21.json` has status `arb_certified_finite_6141_column_full_fourth_plus_eighteen_gapped_separator`, uses 512-bit Arb for base/gapped atoms and 128-bit Arb for the fractional grid, and certifies common dual gap (1/5). Its finite-pool consequences are (|b-Ap|_\infty>1/2665) and program-mass TV (>1/5330), for exactly this finite pool.

The separately certified 6141-dual pricing escape is pinned to diagnostic SHA-256 `6edd34feb2a5ce1e3257ba65abcb3fe760643c03afa084c29cb3620f7eaf5a4e`, finite-certificate SHA-256 `d9fda798752cac4398dd002cc27db7e01c6dc9e8df2b056d4480f81e88ac107a`, and search SHA-256 `4f3f3a3faa566c997fb6748df90feb1b8b7c49ce3dd596544cdd0ee67ec19470`. At 256-bit Arb it certifies strict negative target-minus-score intervals for both a connected positive path and a multi-segment path:
- connected: ([-48.72288490827776094638895982381562433556478549657956204206291814479735310 \pm 5.94\times10^{-72}]);
- multi-segment: ([-49.76549033526441878726991857388691787660087949705930335736051873139170391 \pm 5.95\times10^{-72}]).

These are escapes from this particular 6141-column dual. They do not invalidate the 6141 finite-pool theorem and do not establish global feasibility or infeasibility.

## Run 40 changes

Added a 6,143-column full-second-/fourth-order reoptimization pipeline by appending those two exact-rational Arb-certified escapes to the 6,141-column pool:

- `discover_ising_full_fourth_plus_twenty_gapped_n21.py` — floating LP discovery on 6,143 columns;
- `verify_ising_full_fourth_plus_twenty_gapped_arb_n21.py` — independent interval verifier, pinned to the 6,141 parent diagnostic/certificate and the two escape search/certificate artifacts;
- `.github/workflows/eui-reoptimize-6143-full-fourth.yml` — reproducible hosted run with pinned Python/numerical dependencies, self-tests, reoptimization, Arb verification, and hash-checked evidence publication.

Commit sequence:
- discovery: `ced424c5a938f0c7b3c0b5c855599c155d34ca27`;
- verifier: `e13400308efd7ad9f215489ecd457162830498db`;
- workflow: `1001b1235ae84b42c39dde2a9a8281aa112c36f3`;
- workflow staging-path correction: `635e7c5ef8fe9450009398a4828ee9c2583bd765`;
- verifier parent-certificate-status correction: `915227d7b5dbd28479ec7829e64cb44ec0495335`.

Hosted run [45745598002](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45745598002) is in progress at the time of this audit. Dependency installation, Python compilation, and block-minor/spin-symmetry/JSON-serialization self-tests passed; the 6,143-column LP is still running. Two earlier attempts were cancelled while correcting the staging paths and parent-status pin; neither produced a mathematical result used here.

No 6,143-column theorem is claimed yet. The current verifier certifies a frozen dual if the LP returns one. If the LP returns a primal feasible candidate, it must be treated as floating discovery until a separate positive-weight interval verification is added.

Issue #5 received Run 40 progress comment 7181290225.

## Evidence classification and next action

- **Previously proved / interval-certified:** finite 6,141-column full second-/fourth-order separation; exact 256-bit escapes from that particular dual.
- **Verified this run:** 6,143 pipeline compiles; deterministic block-minor, spin-symmetry and serialization self-tests pass; parent/escape hashes are pinned.
- **Still running:** 6,143-column LP reoptimization and (if applicable) independent Arb pricing.
- **Not proved:** any 6,143-column theorem; a positive n=21 all-even-principal-minor ensemble; a global converse for all legal gapped couplings; an operational Choi/diamond-distance lower bound from the finite-pool program-mass TV separation.
- **Next highest-value action:** inspect run 45745598002. If it returns a dual, complete independent Arb certification, then continuously price that new dual and append only independently certified escapes. If it returns a primal, build a separate interval verifier for strict positivity of all weights and the full 1,461-coordinate residual before making any construction claim.