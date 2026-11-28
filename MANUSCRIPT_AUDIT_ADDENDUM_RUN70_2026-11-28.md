# Manuscript audit addendum — Run 70 (2026-11-28)

## Selected issue

Issue #7 remains the highest-leverage unresolved scientific issue: whether the
uniform balanced-slice target lies in the closed convex hull of the full
42-cycle exponential physical family. This run did not claim a global
separation theorem. It closed the next exact mathematical subproblem left by
Run 69: compute the entire sixth-order harmonic projection for the frozen
37-base / 74-labelled period-two candidate, rather than using one explicit
sixth-order witness.

## New theorem and derivation

For the balanced-slice character residuals
\[
\delta_I^{(m)}=\mathbb E_q\prod_{i\in I}x_i-
\mathbb E_u\prod_{i\in I}x_i,
\]
define
\[
(D_ma)_J=\sum_{i\notin J}a_{J\cup\{i\}}.
\]
The candidate exactly matches all 861 pair coordinates. Its exact-real
weights are the unique solution of the 37-by-37 moment system: the Arb
determinant excludes zero, all 37 weights are strictly positive, 30
independent pair-feature equations are imposed, and the remaining
cross-parity feature follows from the row-norm identity. Period-two
translation and the equal one-site symmetrization extend this to all pair
coordinates. Hence
\[
D_4\delta_4=0,\qquad D_6\delta_6=-D_5^T\delta_4.
\]

The Boolean-lattice commutator
\[
D_{k+1}D_{k+1}^T=D_k^TD_k+(42-2k)I
\]
gives
\[
\delta_6^{\rm harm}
=\delta_6+\frac1{66}D_6^TD_5^T\delta_4.
\]
Each four-subset of a six-set is counted twice in the double up-operator, so
the coordinate formula is
\[
\boxed{
h_I=\delta_{6,I}^{\rm harm}
=\delta_{6,I}+\frac1{33}
\sum_{\substack{K\subset I\\|K|=4}}\delta_{4,K}.
}
\]
The degree-six Gram eigenvalue is exact:
\[
\lambda_6=\frac{7938048}{6724861}.
\]
The complete degree-four and degree-six orthogonal projections therefore
give
\[
\chi^2(q\Vert u)\ge
\frac{\|\delta_4\|_2^2}{\lambda_4}
+\frac{\|h\|_2^2}{\lambda_6}.
\]

## Full N=42 verification

The verifier enumerated all 63,133 D42 orbits of six-subsets. Their orbit
sizes sum to all 5,245,786 six-subsets. It evaluated 4,671,842 six-by-six
principal minors (37 base atoms and 37 one-site translates for each orbit
representative), used the full 1,440-orbit quartic Arb certificate for the
15 quartic submoments in each correction, and formed every corrected
sixth-harmonic residual at 256-bit Arb precision.

All 63,133 corrected residual intervals excluded zero; no orbit contribution
was dropped. It additionally enumerated all 10,222 D42 orbits of five-subsets
and checked that the interval for \(D_6h\) contains zero on every orbit
representative. By D42 invariance this covers all 850,668 five-subsets.
Twenty-four independent rotation/reflection symmetry regression checks also
passed.

### Certified numerical result

Complete sixth-harmonic projection norm:
\[
\|h\|_2^2\in
[0.0459250490456842704146973544669054902195855549007702836745852313698437
\pm 7.09\times10^{-71}].
\]

Degree-six chi-square contribution:
\[
\frac{\|h\|_2^2}{\lambda_6}
\in
[0.0389062363002099972720311172038350639683171901096527698802218018352923
\pm 7.31\times10^{-71}].
\]

The degree-six contribution is at least 276,954.188 times the Run 69
single-witness lower bound \(1.4047895985994776\times10^{-7}\). This is a
comparison of certified lower-bound contributions; it does not mean the
Run 69 witness was optimal.

Combining with the conservative Run 68 quartic floor gives
\[
\boxed{
\chi^2(q\Vert u)>
0.1212616746890306412259819506806757844913171901096527698802218018352923.
}
\]

The complement-folded Plücker frame-potential identity then yields
\[
\boxed{
\operatorname{FP}>
8.332524077650208180211101200592596643935999786427223122225814449603037
\times10^{-12}.
}
\]
The ideal frame-potential value is
\(7.431382223923010964580659670172348923453308318310907496251881494350739665140
\times10^{-12}\).

## Evidence and reproducibility

- Verifier: verify_n42_degree_six_harmonic_projection_arb.py
- Theory: THEORY_N42_DEGREE_SIX_HARMONIC_PROJECTION.md
- Machine certificate: evidence/n42_degree_six_harmonic_projection_arb.json
- Workflow: [46100133850 — SUCCESS](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46100133850)
- Verifier commit: cdcd4b7817d23d3fc206fac1c48f632a08b6d834
- Machine-certificate commit: 6d0c86ff35102721e535a1441c5e63d98d664bc4
- Theory-note commit: 6daf87f8dc9a164878292284cea0191b1bf2e862
- Orbit residual digest: 7ce511ee2d4517fe3e3d80e15a73cc0df0b8a53c5ce42037179d7ba3111daa6f
- Frozen atom SHA-256: 948ee6542ae8f358bae27614d7124acfd7d1c5db9bcbaf2db787449253a8cb0d
- Frozen weight SHA-256: 53144e15c92afa65a60e568499608ba30e2c25f645a4804414afde9de088fffd
- Full quartic orbit certificate SHA-256: b9f4aaf33af2419174e0f48c111d786fbc3a159e7e1da8f3bb259629c05492ac
- Run 68 quartic certificate SHA-256: c5acc1e15996700282fe9e4e27ecf412db18e2a3707a5240518bdf4e1c1bbdbe
- Run 69 witness certificate SHA-256: 965069acff1bd06e6016337c4ca3d5753fee24931808fb4fb101f8a5f946fab6

## Literature and manuscript boundary

The general slice-harmonic/Johnson-scheme decomposition is established prior
work, notably Yuval Filmus, *An Orthogonal Basis for Functions over a Slice
of the Boolean Hypercube*, Electronic Journal of Combinatorics 23(1), 2016,
P1.23, DOI 10.37236/4567, [arXiv:1406.0142](https://arxiv.org/abs/1406.0142).
The EUI-specific result here is the exact sixth-residual correction from the
nonzero quartic residual, together with the complete D42-orbit Arb evaluation.

The public manuscript remains arXiv:2506.20570v1 with appendices A–E. The
repository contains no editable TeX, BibTeX, PDF, or standalone supplementary
source; this run therefore updated research theory/evidence, not the formal
manuscript text. Issue #6's Appendix B noise-normalization audit remains
separate.

## What is and is not established

**Established:** exact pair matching for this frozen ensemble; the sixth
harmonic projection formula; all 63,133 sixth-order orbit residuals and all
10,222 harmonic down relations; the stated 256-bit candidate-specific
chi-square and frame-potential lower bounds.

**Not established:** a full N=42 physical positive ensemble; a global
separator for every real 42-cycle coupling vector; infeasibility of the
continuous cycle-exponential convex hull; a stronger program-label TV bound;
or any Choi trace-distance / channel diamond-distance consequence. The direct
program-label TV certificate remains the previous \(>0.00275\).

## Next highest-value action

Stop spending the next cycle on still higher moments of this already rejected
74-labelled candidate. The highest-value next step is to leave the frozen
period-two support: either (i) search a genuinely non-period-two physical
ensemble with an explicit, reproducible pricing oracle, or (ii) derive a
global continuous-coupling separator. In parallel, Issue #5's operational
bridge must remain explicit: a program-mass discrepancy is not automatically
a channel diamond-distance lower bound.
