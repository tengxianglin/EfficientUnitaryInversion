# EUI research audit — Run 59 (2026-11-27)

## Repository and issue selection

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- Starting HEAD: `617202485ee4720df565160fc96cfad678876460` (Run-58 audit).
- Rechecked the latest 15 commits, all four open issues (#7, #5, #6, #3), the latest #7/#5 discussion, current Actions runs, the Run-58 research note, the N=42 ten-orbit discovery/verifier/evidence, and the public arXiv HTML manuscript with Appendices A–E.
- Issue #7 remains the highest-leverage positive-ensemble track. The ten-orbit ensemble is a verified partial construction, but its 11-orbit finite-pool infeasibility is not a continuum theorem.

## New analytic result: an all-quartic incidence identity

For any real symmetric involution Q of size 2n with trace zero and any fixed two-subset I, let T=Q_{I,I}. The exact identity is

```
sum_{J subset I^c, |J|=2} det Q_{I union J,I union J}
    = (tr T)^2 - n det(T) - 1.
```

The proof uses the block equations from Q^2=I, the Desnanot–Jacobi identity for disjoint 2x2 blocks, and Cauchy–Binet. It does not require T or its complement block to be invertible.

For the N=42 period-two cycle family c_{2j}=a, c_{2j+1}=b, the even/odd bipartition makes the off-diagonal generator block B circulant and normal. Consequently the two diagonal blocks of exp(A) coincide and have constant diagonal gamma. Since Q=exp(A)D, the fixed cross-parity block T=Q_{ {0,1},{0,1} } has trace zero for every real a,b.

Taking n=21 and I={0,1}, every period-two atom therefore obeys

```
sum_{J in C({2,...,41},2)} det Q_{I union J} = -21 det Q_I - 1.
```

This identity is affine in the feature vector and hence holds for every positive probability mixture over the continuous period-two family, regardless of support size.

The balanced target gives:
- pair moment: -1/41;
- each quartic moment: 1/533;
- number of quartets containing I: C(40,2)=780;
- target quartic incidence sum: 780/533=60/41;
- target value of L=21 m_I + sum_J m_{I union J: 39/41;
- physical period-two value: -1;
- exact gap: 80/41;
- coefficient l1 norm: 801.

Thus every period-two mixture has complete pair/fourth feature-vector l-infinity discrepancy at least

```
80/(41*801) = 80/32841.
```

If all pair moments are exact, at least one of the 780 incident quartic coordinates undershoots its target by at least

```
(80/41)/780 = 4/1599.
```

This is a genuine continuum no-go for the entire N=42 period-two subfamily. It explains why the Run-58 82-atom construction can match ten selected quartic orbits but cannot be extended to a complete fourth-order design by adding more period-two atoms.

## New necessary condition for a non-period-two construction

For a general physical atom, the same incidence identity holds, but t=Q_00+Q_11=R_00-R_11 need not vanish. Any ensemble matching all pair and quartic targets must satisfy

```
E[(R_00-R_11)^2] = 80/41.
```

This is a useful exact constraint for future non-period-two candidate generation. It is not a construction and does not exclude the unrestricted cycle family.

## Reproducibility artifacts added

- `THEORY_N42_PERIOD_TWO_ALL_QUARTIC_NO_GO.md`: full analytic statement and proof.
- `verify_n42_period_two_all_quartic_no_go_arb.py`: 256-bit Arb regression; reconstructs Q for frozen rational period-two couplings, checks symmetry/involution/trace and directly sums all 780 incident quartic minors.
- `.github/workflows/eui-n42-period-two-all-quartic-no-go.yml`: pinned python-flint CI and machine-certificate upload.
- Expected machine output: `evidence/n42_period_two_all_quartic_no_go_arb.json`.

The finite Arb samples are regression checks only. The continuum result is proved by the algebraic incidence identity and the period-two block-circulant argument.

## Manuscript audit

The public manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, arXiv:2506.20570v1. The HTML manuscript and its appendices A–E were checked. No editable tracked TeX/Bib source or separate supplementary source was found in the repository. Appendix B's per-instance L1 normalization wording/implementation mismatch remains tracked in Issue #6; the full QuAIRKit table has not been regenerated. No manuscript-body claim about Choi trace distance or diamond distance was changed.

## Changes, verification status, blockers, next action

- Added the exact period-two all-quartic no-go theorem and an independent Arb regression workflow.
- Commits: theory `9e3b30baa53d6e5960e0ceadeb925549939378e4`; verifier `8340746ba0834afeb84c9a37090505620f1db15a`; workflow `634a0cfa1ea3a074fb01e4b18ec66a76f9e6e3c2`.
- Hosted CI status is pending at the time this audit was authored; do not call the machine regression passed until the new run completes.
- Still blocked: complete non-period-two physical ensemble or global separator; higher even moments; operational bridge from moment discrepancy to Choi/diamond error.
- Next highest-value action: use the necessary condition E[(R_00-R_11)^2]=80/41 to guide a symmetry-broken physical search, and price any candidate separator over the full allowed cycle family before interpreting it globally.
