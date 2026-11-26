# EUI research audit — Run 43 (2026-11-26)

## Repository state and issue selection

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Latest inspected history before this run: `fcb399eaf5c1f742ef7dc067786b32defcd65a4e` (6,143-column evidence commit), preceded by Run 42 repair `9d56aa79dd62f8a9e32200b756e8de2115295348`.
- Open research tracks rechecked: #5 (finite-pool/full-family gap), #7 (physical reachability of the perfect-matching ensemble), #6 (Appendix B noise normalization), and #3 (type-1.2 Hamiltonian classification). #5 remains the immediate highest-leverage item because the 6,143-column Arb gate has just completed and its new dual can now be priced against continuous physical paths.
- Recursive tree at the inspected revision: 1,172 entries, not truncated. No tracked `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplementary source was present. No formal manuscript text was modified.

## Run 43 result — repaired 6,143-column certificate succeeded

GitHub Actions [45770191253](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45770191253) completed with success. Its job log confirms the LP and independent Arb steps both completed, and the workflow committed the certificate as [fcb399eaf5c1f742ef7dc067786b32defcd65a4e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fcb399eaf5c1f742ef7dc067786b32defcd65a4e).

Machine-readable certificate:
- `evidence/ising_full_fourth_plus_twenty_gapped_arb_n21.json`
- Status: `arb_certified_finite_6143_column_full_fourth_plus_twenty_gapped_separator`
- Candidate count: 6,143 = 22 base + 6,101 fractional-grid + 20 exact-rational gapped paths.
- Feature system: 1,461 coordinates = 21 second-moment distances + 1,440 fourth-order dihedral orbits; 111,930 four-subsets before orbit reduction.
- Exact rank reduction: 1,313 independent moment rows, 1,314 equalities including normalization.
- Dual support: 103 nonzero coefficients.
- Interval pricing: 512-bit Arb for base and gapped atoms; 128-bit Arb for fractional-grid atoms.
- Exact scaled norm: \(\\|D^{-1}y\\|_1=1\), with \(D=\\operatorname{diag}(41I_{21},533I_{1440})\).
- Exact full-coordinate norm: \(18426978530271890734441/35533333333333334517<533\).
- Minimum observed Arb lower endpoint: approximately 0.2242378058366994375; a simpler common rational floor \(1/5\) is frozen.

Thus, for every probability vector on this exact finite pool, the certificate proves
\[
\\|b-Ap\\|_\\infty>1/2665,
\\qquad
\\operatorname{TV}(w_p,u_{\\rm bal})>1/5330.
\]
The TV quantity is the balanced program-label distribution / corresponding dephased classical label register, not Choi trace distance or channel diamond distance.

## Scope warning

This is a finite-pool theorem only. It does not cover arbitrary nonuniform couplings, the continuous gapped family, arbitrary multi-segment paths, all even principal minors, or a channel-level Choi/diamond lower bound.

The discovery JSON's prose `scope` field still contains a stale phrase saying “6,141 columns total”; its machine-readable `candidate_count=6143`, component counts, hash-pinned certificate, and verifier's actual loops all say 6,143. This is a documentation-string defect, not a change to the certified inequalities. It should be corrected at the generator and regenerated in a later cleanup so the diagnostic text agrees with its verified metadata.

## Continuous-pricing follow-up launched

Added:
- `search_ising_full_fourth_plus_twenty_gapped_n21.py` — deterministic multistart pricing search for the exact 103-term 6,143 dual;
- `verify_ising_full_fourth_plus_twenty_gapped_escape_arb_n21.py` — independent 256-bit Arb verification of frozen connected and multi-segment candidates;
- `.github/workflows/eui-full-fourth-plus-twenty-gapped-search-n21.yml` — pinned, reproducible workflow.

Commits:
- search: `edd2897787fbca9b7b18567388e56fff9da4df34`;
- verifier: `354f165b2a64b2200f7fce7a8117bffbbc725922`;
- workflow: `30e2367b89b960e937e3babc0c88758085a272fe`.

Workflow [45785906516](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45785906516) was observed in progress at audit time, during dependency installation. No continuous escape or global bound is claimed yet.

## Next highest-value action

Complete workflow 45785906516. If a best connected or multi-segment candidate has an Arb-certified score above the target, append that exact rational path and reoptimize the finite pool. If no candidate escapes, treat that only as a finite search result and broaden deterministic starts / structured families; do not infer global separation.