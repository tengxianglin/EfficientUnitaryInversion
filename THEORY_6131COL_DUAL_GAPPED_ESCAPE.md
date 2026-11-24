# Two 256-bit Arb-certified escapes from the 6,131-column full-fourth dual

**Status (2026-11-25): both a connected strictly-positive path and a multi-segment path are certified escapes from the particular 82-term rational dual of the 6,131-column finite-pool theorem.** This does not invalidate the finite-pool theorem.

## 1. Frozen separator

The parent certificate is [the 6,131-column Arb certificate](evidence/ising_full_fourth_plus_eight_gapped_arb_n21.json), with exact target
[
\beta=\frac{125831795006523867023}{532999999999999742463}
=0.2360821669916021159904\ldots
]
and
[
y^{\mathsf T}(b-F(R_j))>\frac15
]
for every one of its 6,131 listed columns. The exact rational dual has 82 nonzero coefficients and is normalized by
[
\|D^{-1}y\|_1=1,\qquad D=\operatorname{diag}(41I_{21},533I_{1440}).
]

The pricing functional used below is reconstructed from the exact rational coefficients in the Arb certificate, not from a floating surrogate.

## 2. Deterministic pricing search

The search used:

- random seed: 20261125;
- 520 initial connected/multi-segment candidates;
- 8 optimized starts per class;
- at most 120 L-BFGS-B iterations per start;
- analytic Frechet gradient;
- maximum central finite-difference gradient self-test error (1.1420807355388973\times10^{-10}).

The optimizer is discovery only. The exact-decimal couplings from the best connected and multi-segment candidates were independently reconstructed as rational numbers and evaluated with 256-bit Arb.

## 3. Connected strictly-positive escape

All 41 internal couplings are strictly positive; the closing edge is zero. The exact minimum internal coupling is
[
c_{\min}=\frac{19999999999999999}{20000000000000000000000}
\approx10^{-6},
]
and the maximum is
[
c_{\max}=\frac{25132469788959689}{1000000000000000}
\approx25.132469788959689.
]
The independent 256-bit Arb score and target-minus-score intervals are
[
y^{\mathsf T}F(R(c_*))
\in[26.6793590432269705692367061214979470\pm5.08\times10^{-72}],
]
[
\boxed{
y^{\mathsf T}(b-F(R(c_*)))
\in[-26.4432768762353684532462876589909411\pm6.42\times10^{-72}]<0.
}
]
All 1,764 entries of (R^{\mathsf T}R-I) have Arb intervals containing zero, and the determinant interval contains one.

This single candidate is enough to refute extension of this particular dual to the full connected strictly-positive open-path family.

## 4. Multi-segment escape

The second exact path has internal cuts
[
\{12,17,29,37\},
]
with every other internal coupling positive and minimum positive coupling (10^{-8}). Its maximum coupling is approximately (499.9443699621192). At 256-bit Arb,
[
y^{\mathsf T}F(R(c_*))
\in[30.6133439975955950004560926046616281\pm3.78\times10^{-69}],
]
[
\boxed{
y^{\mathsf T}(b-F(R(c_*)))
\in[-30.3772618306039928844656741421546222\pm1.73\times10^{-69}]<0.
}
]
It also passes all 1,764 interval orthogonality checks and the determinant check.

## 5. Exact scope

These are strict counterexamples to **global extension of this particular 6,131-column rational dual** to the connected and multi-segment general-gapped families. They do not invalidate the finite-pool theorem: both paths are outside the exact 6,131-column pool, while all 6,131 listed columns retain their certified gap.

They do not prove that the full physical moment problem is feasible or infeasible, do not construct an ensemble satisfying every even principal minor, and do not imply a Choi-state or channel diamond-distance lower bound. A finite multistart search with no escape would not be a continuum upper bound; here, however, the two found candidates are independently certified exact escapes.

## 6. Reproduction and next action

- [Deterministic search](search_ising_full_fourth_plus_eight_gapped_n21.py)
- [Independent 256-bit Arb verifier](verify_ising_full_fourth_plus_eight_gapped_escape_arb_n21.py)
- [Search transcript](evidence/ising_full_fourth_plus_eight_gapped_search_n21.json)
- [Escape certificate](evidence/ising_full_fourth_plus_eight_gapped_escape_arb_n21.json)
- [Successful workflow 45483583523](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45483583523)
- [Evidence commit 4991341](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4991341eb3e95325cd8817c1de3c402094c95fd3)

The next decisive experiment is to append both exact rational paths to the 6,131-column pool and reoptimize the complete 1,461-coordinate second-/fourth-order LP, producing a 6,133-column candidate. Any resulting dual must again be independently rationalized and Arb-verified; any resulting primal is discovery only until exact weights and all 1,461 coordinates are interval-verified.
