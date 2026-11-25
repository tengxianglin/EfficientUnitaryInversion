# 201-column mixed-order rational-dual obstruction (n=21)

**Status:** proved for the exact finite pool and fixed 2,113-row design below. This note does not claim a continuous-family obstruction.

## 1. Frozen physical pool

The ordered pool has 201 columns:

- 183 columns from the frozen canonical physical inventory;
- nine exact-rational positive open-path escape columns, labels 1641--1649;
- nine uniform positive-coupling open-path columns, labels 1650--1658.

The newest column is label 1658. It is the exact finite-time escape of the 200-column dual:
[
c_0=cdots=c_{40}=t_*,qquad c_{41}=0,qquad
t_* = \frac{133290887822869233787}{200000000000000}>0.
]
Thus all 41 internal couplings are strictly positive. The path certificate is independently verified with 128-bit Arb in `evidence/200col_uniform_ray_time_arb_n21.json`.

The canonical inventory and the 1,600-row seed pool are pinned by the SHA-256 fields in the LP transcript. The LP diagnostic is
`evidence/joint_low_six_eighth_lp_201col_uniform_ray_escape_n21.json`.

## 2. Fixed moment design

The 2,113 rows comprise:

| Block | Rows | Coverage |
|---|---:|---|
| Second-order | 21 | Complete |
| Fourth-order | 1,440 | Complete dihedral-orbit system |
| Sixth-order | 645 | Selected rows and cuts |
| Eighth-order | 7 | Selected rows |
| **Total** | **2,113** | |

The exact row scales are
[
s_2=\frac1{41},\qquad
s_4=\frac1{533},\qquad
s_6=\frac5{19721},\qquad
s_8=\frac1{19721}.
]
Let (a_jin\mathbb R^{2113}) be the scaled feature column for physical candidate (j), and (b) the correspondingly scaled target. The finite-pool minimax quantity is
[
\eta_{201}=\min_{p\in\Delta_{201}}\|b-Ap\|_\infty.
]

## 3. Exact rational dual and Arb certificate

The binary64 HiGHS discovery (not itself a proof) returned objective
[
0.39283056306574515,
]
recomputed maximum (0.39283056309822917), primal-dual gap (1.291189377639057\times10^{-12}), and 62 positive-support columns.

The independent verifier rationalizes the 2,113-entry dual vector (z) and scalar (lambda), checks the exact scaled-(L_1) constraint
[
\|z\|_1=
\frac{4611686018393898135}{4611686018427387904}<1,
]
and the exact objective
[
\lambda+z^{\mathsf T}b
=\frac{1811611215307209993}{4611686018427387904}.
]
With the rational slack (delta=10^{-8}), 128-bit Arb verifies all 201 inequalities
[
\lambda+z^{\mathsf T}a_j\le\delta
\qquad(j=1,\ldots,201).
]
The maximum Arb shifted-column upper endpoint is
[
-8.902968402615641\times10^{-9}<0.
]

Therefore, by weak duality,
[
\boxed{
\eta_{201}\ge
\frac{707660612964980394033641}
{1801439850948198400000000}
=0.3928305530670364\ldots>\frac13.
}
]
This is a strict finite-pool theorem for exactly the 201 listed columns and the fixed 2,113 rows.

The active dual support has 62 entries: 2 low-order, 58 sixth-order, and 2 eighth-order coordinates.

## 4. Exact program-mass TV corollary

For every retained row (i), the unscaled feature is an orbit average of an even-parity character (phi_i(T)), hence
[
\|\phi_i\|_\infty\le1.
]
For the exact dual define
[
G(T)=\sum_i\frac{z_i}{s_i}\phi_i(T),\qquad
M=\|G\|_\infty\le\sum_i\frac{|z_i|}{s_i}.
]
The independently checked exact value is
[
M=\frac{92530165274588371116657}{23058430092136939520}
=4012.8562484460597\ldots.
]
The moment discrepancy lower bound is the exact (eta)-bound above, so the TV dual inequality gives, for every probability mixture over the same 201 physical columns,
[
\boxed{
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{707660612964980394033641}
{14457838324154432986977656250}
=4.8946502035695432\times10^{-5}.
}
]
Here (w_p) is the balanced program-label mass distribution and (u_{\rm bal}) is the balanced reference distribution in the selected parity sector. This is equivalently a trace-distance statement for the dephased label register.

## 5. Evidence and reproducibility

- LP discovery: [workflow 45598370006](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45598370006).
- Rational dual + 128-bit Arb verification: [workflow 45599105012](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45599105012).
- TV corollary re-verification: [workflow 45599717698](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45599717698).
- LP transcript: `evidence/joint_low_six_eighth_lp_201col_uniform_ray_escape_n21.json`.
- Exact rational dual and 201 Arb intervals: `evidence/55probe_201col_uniform_ray_escape_dual_certificate_n21.json`.
- Exact TV post-processing: `evidence/201col_program_mass_tv_bound_n21.json`.
- Reoptimizer: `reoptimize_201col_uniform_ray_escape.py`.
- Arb verifier: `verify_201col_uniform_ray_dual_arb.py`.
- TV verifier: `verify_201col_program_mass_tv_bound.py`.

## 6. Explicit limitations

This result does **not** establish:

1. a separator for the full continuous physical family (the 200-column dual already had a certified continuous escape; the 201-column dual still requires its own pricing);
2. a theorem for the full 1,641-column canonical inventory;
3. complete sixth- or eighth-order orbit control (645 and 7 rows are selected/cut);
4. feasibility or infeasibility of the full all-even-principal-minor positive-ensemble problem;
5. a Choi-state or channel diamond-distance lower bound.

The next decisive step is continuous pricing of this new 201-column dual, followed by an exact finite-time physical witness if its torus pricing is positive.


## 7. Continuous uniform-ray pricing of the 201-column dual

The 201-column rational dual has now been priced on the exact 21-torus associated with the equal-coupling 42-site open path. The independent 128-bit Arb certificate is
`evidence/201col_uniform_torus_arb_n21.json`, generated by workflow [45600250848](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45600250848).

At the exact-decimal phase vector stored in that certificate, Arb encloses the shifted pricing functional by
[
S_{201}(R(\theta_*))
\in [1.3570081357546039609626799191784434
\pm 6.27\times10^{-35}]>0.
]
The certificate pins the 201-column rational dual, the 201-column LP transcript, the 2,113-row cut design, and the exact discovery transcript by SHA-256. This is an interval-certified violation of at least one column inequality that the 201-column dual would need to satisfy on the full uniform-path family.

The exact dense-torus theorem in `THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md` says that the positive-time equal-coupling orbit is dense in this torus. Since the pricing functional is continuous and the Arb lower endpoint above is strictly positive, there is an open neighborhood of \(\theta_*\) on which the pricing remains positive. Density therefore proves that **there exists at least one finite (t>0)** for which the physical equal-coupling open path has positive 201-dual pricing. This existence conclusion is rigorous; it does not identify a decimal value of (t).

The explicit finite-time search has been staged and its deterministic discovery transcript is now committed:
- discovery: `discover_201col_uniform_ray_time_escape.py`;
- independent exact-time verifier: `verify_201col_uniform_ray_time_arb.py`;
- workflow: `.github/workflows/eui-201col-uniform-ray-time.yml`;
- search evidence: `evidence/201col_uniform_ray_time_search_n21.json`.

With 12 deterministic starts, 400 iterations per start, and seed `202611251837`, the binary64 optimizer found
[
t_{\rm cand}=3952466.400764009915292,
qquad
S_{201}^{\rm float}=0.3771886165386608>0.
]
This is **discovery only**: it is not yet a physical escape certificate. The exact-time Arb output file is not yet committed, so the decimal candidate must not be promoted to a theorem until the independent verifier encloses its score with a strictly positive lower endpoint.

A provenance defect in the initial search script was found before execution: its RNG used seed `202611251837` while the JSON metadata incorrectly reported `202611251720`. Commit [b975b24](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b975b24cf0b3fa9f7c7105e7d60538a76d4b4523) centralizes the seed as a constant and makes the recorded metadata match the actual RNG. The independent verifier also rejects a transcript whose seed metadata is not the pinned value. A verifier unpacking bug was found in the first run and corrected in [commit f52f73f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f52f73fcdf5c016224b18043cf6207111f098d10); the verifier now preserves machine-readable diagnostics if another check fails.

**Scope:** the positive torus interval and density already refute global separation by this particular 201-column dual on the continuous equal-coupling physical ray. The finite-time candidate is a stronger explicit witness only after Arb passes. None of this invalidates the 201-column finite-pool theorem, proves feasibility or infeasibility of the complete physical-family ensemble problem, completes the selected sixth/eighth-order inventories, or implies a Choi/diamond-distance bound.
