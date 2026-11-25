# EUI manuscript and evidence audit — run 21 (2026-11-25)

## Repository and issue state

- Default branch: main.
- Audited tree: 1,021 tracked paths; recursive Git tree was complete (not truncated).
- Current head before this audit note: 591769a5d3e0126de738e071855436726e311219.
- Open issues inspected: #5 (finite-pool/global-family gap), #6 (Appendix B noise normalization), and #3 (type-1.2 Hamiltonian classification).
- Issue #5 received three evidence updates this run: 200-column finite-pool dual/TV result, positive torus escape, and explicit finite-time Arb escape.

No tracked .tex, .bib, .pdf, .doc, or .docx manuscript/supplement source is present. No manuscript-body edit is claimed.

## Public manuscript inspected

The available manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, arXiv:2506.20570v1 (2025-06-25), including Appendices A–E:
https://arxiv.org/html/2506.20570v1

Appendix B reports 10,000 random Hamiltonian samples and average Choi-state fidelity under its support-perturbation model. This is finite-sample, distribution-dependent average evidence; it is not a worst-case Hamiltonian guarantee, a worst-case-input guarantee, or a channel diamond-norm theorem. The separate fixed six-query joint-parity converse remains conditional on a positive ensemble uniform in every even-principal-minor moment in both parity sectors.

## Highest-leverage issue advanced: price the 200-column mixed-order dual on the continuous physical family

The exact 200-column / 2,113-row finite-pool dual is independently certified at 128-bit Arb. Its exact lower bound is
\[
\eta_{200}\ge
\frac{604278563840813954190133571}
{1537228672809866429000000000}
=0.39309607902139015\ldots>\frac13.
\]
The row inventory is 1,461 complete second/fourth coordinates, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. The latter two inventories are not complete. Exact rational post-processing gives a balanced program-label TV lower bound of approximately \(4.92847\times10^{-5}\) for mixtures on the exact 200-column pool; this is a classical/dephased-register statement, not a Choi or diamond bound.

The same 200-column dual has now been disproved as a global separator for the continuous physical family:

1. A 21-torus phase point has a 128-bit Arb pricing interval
\[
[1.4530576032069032574827532865451450\pm5.50\times10^{-35}]>0.
\]
Together with the exact dense-orbit theorem for the equal-coupling 42-site open path, this proves existence of some finite positive time with positive pricing.

2. A bounded deterministic search found the explicit time
\[
t_* = 666454.439114346168935
=\frac{133290887822869233787}{200000000000000}>0.
\]
For \(c_0=\cdots=c_{40}=t_*\), \(c_{41}=0\), all 41 internal couplings are strictly positive. The independent 128-bit Arb score is
\[
[0.1462687155056939188352076552\pm1.54\times10^{-29}]>0.
\]

The finite-pool theorem remains valid for its exact 200 columns. The escape only refutes extending that particular dual unchanged to the full continuous physical family; it does not prove full-family feasibility or infeasibility.

## Reproducibility added

- discover_200col_uniform_torus_pricing.py
- verify_200col_uniform_torus_pricing_arb.py
- .github/workflows/eui-200col-uniform-torus-pricing.yml
- evidence/200col_uniform_torus_search_n21.json
- evidence/200col_uniform_torus_arb_n21.json
- discover_200col_uniform_ray_time_escape.py
- verify_200col_uniform_ray_time_arb.py
- .github/workflows/eui-200col-uniform-ray-time.yml
- evidence/200col_uniform_ray_time_search_n21.json
- evidence/200col_uniform_ray_time_arb_n21.json

Successful workflows:
- Torus pricing: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45584351764
- Explicit finite time: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45585112087

The 200-column theory note now records both escapes. Issue #5 records the finite-pool theorem, exact TV scope, torus witness, and explicit finite-time witness.

## Claim ledger and blockers

**Proved / interval-certified**
- Exact conditional joint-parity diamond-minimax theorem under its all-even-principal-minor ensemble hypothesis.
- Exact positive joint ensembles at n=5 and n=7.
- n=21 200-column / 2,113-row finite-pool rational-dual obstruction and its program-label TV corollary.
- Strict 128-bit Arb torus and explicit finite-time escapes of that particular 200-column dual.
- Existing 6,141-column complete second/fourth finite-pool theorem and its scope-limited continuous dual escapes.
- Exact 3–7 perfect-mirror-block obstruction for its declared family.

**Discovery only**
- Binary64 optimizer phases/times before interval certification.
- The 200-column local search itself; the strict escape conclusions rest on the exact-decimal Arb certificates.

**Still unresolved**
1. Construct an exact positive physical ensemble satisfying every even-principal-minor target at n=21, or prove a global obstruction for the full allowed physical family.
2. Complete all sixth/eighth/higher even-moment constraints; selected/cut rows are not complete.
3. Establish a correctly quantified per-instance operational bridge to Choi trace distance or channel diamond error.
4. Obtain editable manuscript and supplement sources before claiming formal manuscript-body revisions.

## Next highest-value action

Append the exact 200-column finite-time escape as the next physical column and rerun the fixed 2,113-row LP with complete provenance pins. If its dual is above the cap, rationalize and Arb-certify every column inequality, then price that new dual independently on the continuous family. In parallel, the paper-level priority remains a structural all-even-minor construction or global converse—not an unqualified extrapolation from finite candidate pools.
