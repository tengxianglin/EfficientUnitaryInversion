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
- A certified connected gapped escape from the 6,124-column separator, showing its scope is finite-pool only.

**Finite numerical discovery, not a theorem**
- The deterministic 514-start / 12-local-optimization pricing search that found the second gapped escape.
- The 6,125-column LP reoptimization launched from the new escape. Until its diagnostic is committed and any primal/dual candidate is independently certified, no feasibility or infeasibility claim is allowed.

**Still unresolved**
- A positive ensemble satisfying every even principal-minor constraint at (n=21), or a global obstruction for the full allowed physical family.
- A rigorous bridge from the relevant program-mass/moment residual to Choi-state trace distance or channel diamond distance with correct per-instance versus average quantifiers.
- A tracked manuscript and supplementary TeX/Bib/PDF source suitable for direct paper revision.

## Reproducibility pointers

- [Expanded-dual gapped escape theory](THEORY_EXPANDED_DUAL_GENERAL_GAPPED_ESCAPE_N21.md)
- [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_general_gapped_escape_arb_n21.json)
- [6,125-column reoptimizer](discover_ising_full_fourth_plus_two_gapped_n21.py)
- [6,125-column workflow](.github/workflows/eui-full-fourth-plus-two-gapped-n21.yml)
- [Issue #5](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5)

The next decisive step is to inspect the 6,125-column LP output, then certify either an exact positive primal or a new rational dual with independent Arb checks. Any new dual must again be priced on fresh nonuniform positive-coupling paths before a broader no-go statement is considered.
