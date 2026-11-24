# Manuscript audit addendum — 2026-11-24

This addendum records the paper-facing implications of the 2026-11-24 full-fourth pricing results. It supplements, and does not replace, `MANUSCRIPT_AUDIT_2026-11-22.md`.

## Source availability and inspected manuscript

The current repository code search finds no tracked `documentclass` source and no manuscript TeX/Bib/PDF artifact. The accessible manuscript reference remains:

- Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, [arXiv:2506.20570v1 (HTML)](https://arxiv.org/html/2506.20570v1), version dated 25 June 2025.
- Appendix B reports average Choi-state fidelity over 10,000 independently sampled Hamiltonians under its support-perturbation model. This is finite-sample average evidence; it is not a worst-case-over-couplings or worst-case-over-input channel-distance theorem.

No manuscript-source edit is claimed in this run because no tracked TeX/Bib/PDF source is available in the repository.

## New theorem-scope correction

The 6,124-column full-second-/fourth-moment separator remains a valid **finite-pool** theorem for its exact pinned list of 22 base atoms, 6,101 fractional single-open-path grid atoms, and one connected nonuniform gapped path. However, a second connected gapped path with all 41 interior couplings strictly positive has now been independently certified by 256-bit Arb to violate that separator:
[
y^{\mathsf T}(b-F(R(c)))< -41.50254300237819.
]

This is a counterexample to extending that particular dual unchanged to the full connected gapped family. It does not invalidate the finite-pool theorem and does not establish feasibility or infeasibility of the continuous physical-family moment problem.

The strongest currently supported continuum statement remains the separate 512-bit Arb Fourier–Bernstein obstruction for the 22 pinned base atoms plus the entire one-parameter single-open-path family. That result must not be silently generalized to arbitrary nonuniform couplings or multi-segment paths.

## Current paper-facing claim ledger

**Proved / interval-certified**
- Exact conditional joint-parity diamond-minimax theorem, under its positive all-even-principal-minor ensemble hypothesis.
- Exact program-span and radial-recovery statements under their stated architecture assumptions.
- 512-bit Arb all-real single-open-path separator and the associated restricted-family program-mass TV lower bound.
- Finite-pool 6,124-column second-/fourth-order separator.
- Finite-pool 6,125-column second-/fourth-order separator, independently Arb-certified over 22 base atoms, 6,101 fractional single-path columns, and two connected nonuniform gapped paths; the exact rational dual has 78 nonzero coefficients, scaled ℓ1 norm 1, and every Arb column gap exceeds 1/5, yielding a full-feature sup-norm moment residual lower bound >1/2665 for mixtures on this exact pool.
- A certified connected gapped escape from the 6,124-column separator, showing why each new dual must be repriced against fresh nonuniform paths.

**Finite numerical discovery, not a theorem**
- The deterministic 514-start / 12-local-optimization pricing search that found the second gapped escape.
- The 6,125-column LP reoptimization launched from the new escape. Until its diagnostic is committed and any primal/dual candidate is independently certified, no feasibility or infeasibility claim is allowed.

**Still unresolved**
- A positive ensemble satisfying every even principal-minor constraint at (n=21), or a global obstruction for the full allowed physical family.
- A rigorous bridge from the relevant program-mass/moment residual to Choi-state trace distance or channel diamond distance with correct per-instance versus average quantifiers.
- A tracked manuscript and supplementary TeX/Bib/PDF source suitable for direct paper revision.

## 6,125-column follow-up certificate

The 6,125-column LP returned a floating infeasibility/dual candidate in diagnostic commit `bead29dbad301d9008b100185f6bd46576e06767`. This candidate is now independently rationalized and Arb-certified: [workflow 45377450829](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45377450829), certificate commit [2640a0e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/2640a0efcb84b889b95a29581e64e5ae85b2dfb8). The certificate pins all input SHA-256 hashes and checks every one of the 6,125 columns. The exact theorem and scope are stated in `THEORY_6125COL_FULL_FOURTH_PLUS_TWO_GAPPED_FINITE_POOL_N21.md`.

## Finite-pool program-mass TV corollary

Combining the 6,125-column moment residual \(\|b-Ap\|_\infty>1/2665\) with the exact program/DPP character identity gives a bounded orbit-character witness. Each second-/fourth-order orbit average is an expectation of a function \(\phi_O\) with \(\|\phi_O\|_\infty\le1\). Hence every program-label mass distribution from a mixture on this exact pool obeys
\[
\operatorname{TV}(w_p,u_{\rm bal})>\frac1{5330}.
\]
This is a classical program-mass (equivalently dephased-register trace-distance) lower bound only. It is not a Choi-state trace-distance or channel diamond-distance bound, and its finite-pool scope does not extend to arbitrary gapped couplings.

## New 6,125-dual general-gapped escapes

The exact rational dual certified on the 6,125-column finite pool has two independently Arb-certified escapes outside that pool. A connected 42-site open path with all 41 interior couplings strictly positive gives
\[
y^{\mathsf T}(b-F(R(c)))< -13.0222476516468331,
\]
and a three-segment path with cuts at edges 16 and 26 gives a second escape with
\[
y^{\mathsf T}(b-F(R(c)))< -26.6580004470082098.
\]
Both 256-bit verifiers check all 1,764 orthogonality entries and certify determinant one. This does not invalidate the exact 6,125-column finite-pool theorem; it prevents promoting its particular dual to a full-family separator. See [escape certificate commit aed0e00](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/aed0e007753d93990791d93c3ec0e13a1668f2cd) and [workflow 45378513134](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45378513134).

## Reproducibility pointers

- [Expanded-dual gapped escape theory](THEORY_EXPANDED_DUAL_GENERAL_GAPPED_ESCAPE_N21.md)
- [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_general_gapped_escape_arb_n21.json)
- [6,125-column reoptimizer](discover_ising_full_fourth_plus_two_gapped_n21.py)
- [6,125-column workflow](.github/workflows/eui-full-fourth-plus-two-gapped-n21.yml)
- [Issue #5](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5)

The next decisive step is to inspect the 6,125-column LP output, then certify either an exact positive primal or a new rational dual with independent Arb checks. Any new dual must again be priced on fresh nonuniform positive-coupling paths before a broader no-go statement is considered.


## Late-run correction: 6,127-column certificate supersedes the pending 6,125-column state

The earlier sentence above saying that the 6,125-column follow-up LP was still pending is historical and is now superseded. The 6,125-column pool was expanded by the two independently Arb-certified escapes from its dual, producing a 6,127-column full-second/fourth LP. HiGHS returned a floating infeasibility/dual candidate; the new 83-term rationalized dual has now been independently certified.

**Certified finite-pool theorem.** For exactly 6,127 columns (22 pinned base atoms, 6,101 corrected fractional single-open-path grid atoms, and four exact-rational gapped paths: three connected and one three-segment), the exact rational dual satisfies
\[
\|D^{-1}y\|_1=1,\qquad D=\operatorname{diag}(41I_{21},533I_{1440}),
\]
and Arb certifies
\[
y^{\mathsf T}(b-F(R_j))>\frac15
\]
for all 6,127 listed columns. The minimum certified lower endpoint is
\[
0.2413486692674136993452754291\ldots>\frac15
\]
at base atom 14. The exact full-coordinate norm is
\[
\|y\|_1=
\frac{10763356977938966597333}{20499999999999938401}
<533.
\]
Consequently, every probability mixture on this exact finite pool obeys
\[
\|b-Ap\|_\infty>\frac1{2665},
\qquad
\operatorname{TV}(w_p,u_{\rm bal})>\frac1{5330}.
\]
The second inequality is a program-label mass/dephased-register result derived from bounded orbit characters. It is **not** a Choi-state trace-distance or channel diamond-distance bound.

Verification: [successful Arb workflow 45396006111](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45396006111), [certificate commit b4de3ef](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b4de3ef66e000ed4502afbeeb8a5c030c6613a38), [formal finite-pool theorem note](THEORY_6127COL_FULL_FOURTH_PLUS_FOUR_GAPPED_FINITE_POOL_N21.md), [independent verifier](verify_ising_full_fourth_plus_four_gapped_arb_n21.py).

The diagnostic JSON has a stale status label containing “6125”, although its explicit candidate_count is 6127. The verifier records this legacy-label flag and checks the explicit count and input hashes. The label should be corrected when the diagnostic is next regenerated; it does not enter the dual inequalities.

**Scope remains finite.** This certificate does not cover arbitrary continuous nonuniform couplings, arbitrary multi-segment paths, the all-even-principal-minor system, or a Choi/diamond operational error. A deterministic multistart pricing search against this new 83-term dual is now queued in [workflow 45396671388](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45396671388). A found escape must be frozen and Arb-certified; failure to find one is not a continuum proof.

The main paper blockers remain unchanged: construct an exact positive all-even-minor ensemble at n=21 or prove a global physical obstruction, and establish a separate per-instance operational bridge to Choi/diamond distance. No tracked manuscript TeX/Bib/PDF source is present, so no manuscript-source edit is claimed.


## Late-run correction: certified escapes from the 6,127-column dual

The 6,127-column finite-pool theorem above remains valid for its exact 6,127 listed columns. However, its particular 83-term rational dual has now been shown not to separate the full connected/multi-segment gapped family.

A deterministic pricing search evaluated 516 candidates and performed 12 local optimizations. Two candidates were then frozen as exact rationals and independently verified at 256-bit Arb precision:

1. A connected open path with all 41 interior couplings strictly positive (minimum coupling (9.9999999999999995\times10^{-7})) has
\[
y^{\mathsf T}(b-F(R(c)))\in[-38.5781670484723052122\ldots]<0.
\]
2. A two-segment path with one internal cut at edge 35 has
\[
y^{\mathsf T}(b-F(R(c)))\in[-28.4051423560518348783\ldots]<0.
\]

For each candidate, all 1,764 orthogonality entries are interval-checked and the determinant interval contains one. See [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_four_gapped_escape_arb_n21.json), [verifier](verify_ising_full_fourth_plus_four_gapped_escape_arb_n21.py), [workflow 45397267570](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45397267570), and [certificate commit 3bcff7c](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/3bcff7c3697c393bafd7981a076c50609b6ffbcb).

These are escapes from this particular dual, not counterexamples to the exact 6,127-column theorem. They do not prove global feasibility/infeasibility, construct the all-even-minor ensemble, or imply a Choi/diamond bound.

Both new paths have been appended to the full second-/fourth-order pool. The 6,129-column reoptimization is running in [workflow 45397564995](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45397564995). Its LP result remains floating discovery until a new independent Arb certificate checks every column.
