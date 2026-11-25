# Manuscript/repository audit addendum — Run 23 (2026-11-25)

## Repository and issue state inspected

Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.

The current head at the start of this run was `84984edc9b3de3ebb9baa230683db15cb6564a6e`. The recent 201-column work was inspected, including the exact rational dual, the 2,113-row LP transcript, the 201-column finite-pool verifier, program-mass TV verifier, torus discovery, Arb torus verifier, dense-ray theorem, and the public manuscript.

Open issues returned by the repository query:
- #5: finite-pool minimax obstruction / full-family EUI gap;
- #6: Appendix B per-instance L1 noise normalization;
- #3: type-1.2 Hamiltonian classification runtime audit.

Issue #3's dependency-light classifier regression is already recorded as passing; the remaining QuAIRKit-backed end-to-end smoke test is separate. Issue #6's helper and five-protocol L1 normalization regression are already implemented; full QuAIRKit Choi-fidelity table regeneration remains outstanding.

## Highest-leverage scientific issue advanced: price the 201-column dual on the continuous physical ray

The exact 201-column / 2,113-row finite-pool theorem remains valid for its frozen pool. Its exact dual has
[
\|z\|_1=\frac{4611686018393898135}{4611686018427387904}<1,
\]
and the certified finite-pool lower bound is
[
\eta_{201}\ge
\frac{707660612964980394033641}
{1801439850948198400000000}
=0.3928305530670364\ldots>\frac13.
]
The associated exact program-mass TV lower bound is
[
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{707660612964980394033641}
{14457838324154432986977656250}
=4.8946502035695432\times10^{-5}.
]
This TV statement is for the balanced program-label distribution / dephased label register in one parity sector, not a Choi or diamond-distance bound.

The 2,113 rows are 21 complete second-order + 1,440 complete fourth-order + 645 selected/cut sixth-order + 7 selected eighth-order rows. The latter two inventories are not complete.

## New continuous escape: exact torus Arb certificate

The 201-column continuous torus workflow [45600250848](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45600250848) completed successfully. Its independent 128-bit Arb certificate `evidence/201col_uniform_torus_arb_n21.json` encloses the shifted pricing functional at an exact-decimal phase vector by
[
[1.3570081357546039609626799191784434\pm6.27\times10^{-35}]>0.
]

The certificate pins the 201-column rational dual, LP transcript, cut design, and discovery transcript by SHA-256. The exact dense-torus theorem in `THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md` proves rational independence of the 21 positive frequencies
[
\omega_k=4\cos(k\pi/43),\quad k=1,\ldots,21,
]
and density of the positive-time equal-coupling open-path orbit in the 21-torus. Since the pricing functional is continuous, the strictly positive interval gives an open set of positive pricing; density therefore proves that **some finite positive physical time exists** at which this particular 201-column dual is violated.

This refutes global separation by the particular 201-column dual on the continuous equal-coupling physical ray. It does not invalidate the finite-pool theorem, prove full-family feasibility/infeasibility, complete sixth/eighth moments, or yield a channel operational bound.

## Reproducibility correction and explicit-time verification

The first finite-time discovery script had a metadata bug: it initialized NumPy's generator with seed `202611251837` but wrote `202611251720` into the output JSON. This was fixed in commit [b975b24](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b975b24cf0b3fa9f7c7105e7d60538a76d4b4523) by centralizing the seed constant and using it both for the RNG and metadata.

Added:
- `discover_201col_uniform_ray_time_escape.py`;
- `verify_201col_uniform_ray_time_arb.py`, which recomputes the exact physical path from the rationalized decimal time and independently encloses the 201-dual score with Arb;
- `.github/workflows/eui-201col-uniform-ray-time.yml`, which rechecks the pinned 201-/200-column parent evidence, runs 12 deterministic starts, and invokes the exact-time verifier.

Commits:
- [84984ed](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/84984edc9b3de3ebb9baa230683db15cb6564a6e): finite-time discovery;
- [b975b24](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b975b24cf0b3fa9f7c7105e7d60538a76d4b4523): seed provenance correction;
- [6915acb](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6915acbd977d887814376d4cb1d434f023fefa49): independent Arb verifier;
- [19101a3](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/19101a30f03e120be53e1857e10089bff9556110): workflow;
- [e7d02c2](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e7d02c2b46dba08bf5071a4e5d858b683679a9b4): update 201-column theory note.

At audit time, the finite-time search/Arb JSON outputs were not yet visible on `main`; therefore no explicit decimal time is claimed. The existence of some finite time follows already from the certified torus point plus the dense-ray theorem.

## Public manuscript and supplement audit

The public manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, arXiv:2506.20570v1 (2025-06-25): https://arxiv.org/html/2506.20570v1

Appendix B (HTML lines 294–313) defines the perturbation using raw-looking Gaussian coefficients while defining delta as a relative L1 ratio; the code normalizes each out-of-support Gaussian direction per sample before applying delta. This notation/protocol mismatch is tracked in Issue #6. The code-level normalization regression is not a rerun of the published Choi-fidelity table.

No editable `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplement source was found in the repository. No formal manuscript-body edit is claimed.

## Claim ledger and blockers

**Proved / independently interval-certified**
- 201-column / 2,113-row finite-pool rational-dual obstruction and exact program-mass TV corollary, with the declared selected-row scope.
- Strict 128-bit Arb positive pricing of the 201-column dual at an exact torus point.
- By the exact dense-ray theorem and continuity, existence of some finite positive equal-coupling physical time escaping the 201-column dual.
- The predecessor 200-column finite-time escape and 200-/201-column ancestry checks recorded in the committed certificates.

**Discovery only / pending explicit witness**
- A particular finite decimal time from the new 201-column one-dimensional optimizer. It must pass the new exact-time Arb verifier before being called a physical escape certificate.

**Unresolved**
1. Construct an exact positive physical ensemble matching every even-principal-minor target at n=21, or prove a global converse for the intended continuous physical family.
2. Complete all sixth/eighth/higher even-moment orbit constraints; selected/cut rows are not complete.
3. Establish a correctly quantified operational bridge to Choi trace distance or channel diamond error.
4. Regenerate the Appendix B Choi-fidelity tables in a pinned QuAIRKit runtime and correct the editable manuscript source when supplied.
5. Run the full QuAIRKit-backed type-1.2 classifier/comb-search smoke test.

## Next highest-value action

Finish the finite-time 201-dual search and Arb verification. If an explicit positive time is certified, append that exact physical path as column 202 and rerun the fixed 2,113-row LP with complete provenance pins. If the bounded optimizer fails to find a decimal witness, retain the already-proved dense-ray existence result and do not interpret the failed bounded search as a global separation proof.
