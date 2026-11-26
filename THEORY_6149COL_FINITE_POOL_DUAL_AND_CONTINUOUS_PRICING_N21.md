# 6,149-column finite-pool separator and next continuous-pricing test (n = 21)

## 1. Moment system and exact scope

Let (N=42) and (R(c)=e^{A(c)}), where the real skew-symmetric open-path generator is
[
A(c)_{j,j+1}=2c_j,qquad A(c)_{j+1,j}=-2c_j,qquad j=0,ldots,40,
]
with the wrap coupling fixed to zero. Internal zero couplings split the open path into segments.

The pinned finite feature vector contains 21 cyclic second-order distance averages and 1,440 fourth-order dihedral-orbit averages. The latter are formed from 111,930 four-subsets. Thus there are 1,461 full coordinates, 1,313 independent moment equations, and 1,314 equalities after normalization.

The audited pool is exactly:
- 22 base atoms;
- 6,101 fractional single-open-path grid atoms;
- 26 exact-rational gapped paths;
- 6,149 columns in total.

This is a finite candidate pool, not the continuum of all real path couplings.

## 2. Finite-pool theorem (independently Arb-certified)

The HiGHS discovery LP reports an optimal dual and an infeasible primal on this finite design. The floating diagnostic is not itself the proof. The frozen dual has 106 nonzero coefficients, and the independent python-flint/Arb verifier rationalizes those coefficients and certifies:
[
|D^{-1}y|_1=1,qquad |y|_1=533,
qquad D=operatorname{diag}(41I_{21},533I_{1440}).
]
For every one of the 6,149 listed columns (a_j), Arb verifies
[
y^{mathsf T}(b-a_j)ge rac15.
]
The minimum certified column-gap interval is approximately
[
0.21015308557772221504800518ldots > rac15.
]

Therefore every probability vector (p) supported on this exact finite pool satisfies
[
y^{mathsf T}(b-Ap)gerac15,
qquad
oxed{|b-Ap|_inftygerac1{2665}.}
]
The corresponding program-label/dephased-label corollary is
[
oxed{operatorname{TV}(w_p,u_{m bal})gerac1{5330}.}
]
This TV statement is not a Choi trace-distance or channel diamond-distance bound.

The certificate is hash-pinned to the exact diagnostic:
- diagnostic SHA-256: `f5ed3c323420e6b7e11c147d8cc778aab05212b5bb9a52e373f842bc44f9184d`;
- parent 6,147 diagnostic SHA-256: `6e1851ed18b84ea767593fd833477478733f3f7f2de08fe7222ff3679944e2bb`;
- parent 6,147 Arb certificate SHA-256: `bdd324a73c6054d5a0bc47aeed379e6ca88e7b8e7668ca0a0f031296fb83d3e2`;
- newly appended 6,147-dual escape certificate SHA-256: `6444f4bd1360f09f744fd02928d0cf05d88dc426f2511d552eb77d911e57c63e`.

Reproducibility:
- [6,149-column reoptimization workflow 45826172005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45826172005);
- [floating diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_n21.json);
- [independent Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_twenty_six_gapped_arb_n21.json).

## 3. Interpretation and proof boundary

The exact certificate proves separation only for the 6,149 pinned columns. It does not cover other nonuniform gapped couplings, the continuous gapped family, arbitrary multi-segment paths, all even principal minors, or an operational Choi/diamond guarantee.

The preceding 6,147-column dual was escaped by two 256-bit-Arb-certified physical paths. Those paths are now among the 26 gapped columns in this pool. Their existence does not invalidate either finite-pool theorem; it shows why each newly optimized dual must be independently priced against the continuous family.

## 4. Next decisive test: continuous pricing of the 6,149 dual

A deterministic finite multistart pricing pipeline has been added:
- search: `search_ising_full_fourth_plus_twenty_six_gapped_n21.py`;
- independent 256-bit Arb verifier: `verify_ising_full_fourth_plus_twenty_six_gapped_escape_arb_n21.py`;
- workflow: [6,149-dual continuous pricing](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/workflows/eui-full-fourth-plus-twenty-six-gapped-search-n21.yml).

The search uses seed `202611262241`, samples frozen seed-pool and random connected/fractional/multi-segment starts, and locally optimizes the best starts with the analytic Fréchet gradient. This is finite discovery only. A candidate is a physical escape only after the independent verifier freezes its decimal couplings as exact rationals, rebuilds (e^{A(c)}) with Arb, checks all 1,764 orthogonality entries and determinant one, and certifies
[
y^{mathsf T}b-y^{mathsf T}F(R(c))<0
]
with a strictly negative interval upper endpoint. Failure to find an escape is not a continuum upper bound.

## 5. Remaining theorem gaps

1. Construct a positive physical measure matching every even-principal-minor coordinate at (n=21), or prove a global separator for every allowed real coupling vector.
2. Control complete sixth-, eighth-, and higher-order moment orbits.
3. Prove the operational bridge from program-label/moment discrepancy to Choi trace distance or channel diamond distance.
4. Incorporate verified results into an editable manuscript source; the repository currently has research notes and audit addenda but no complete editable TeX/Bib manuscript source.

A finite-pool separator and a continuous escape from a different dual are compatible. Neither settles full physical convex-hull membership.
