# 199-column / 2,113-row mixed-order finite-pool obstruction at n=21

## Exact finite-pool theorem

Let (A_{199}inmathbb R^{2113	imes199}) be the fixed mixed-order moment matrix whose columns are the 199 pinned physical program candidates and whose rows consist of:

- 1,461 complete second-/fourth-order coordinates (21 second moments and all 1,440 fourth-order dihedral-orbit moments);
- 645 selected sixth-order coordinates, including the frozen cut rows;
- 7 selected eighth-order coordinates.

Let (b) be the corresponding exact target vector. The 128-bit Arb certificate records an exact rational dual vector (z), scalar (lambda), and slack (delta=10^{-10}), with

[
|z|_1=1,qquad
eta=lambda+z^{mathsf T}b
=rac{3708878342006156685}{9223372036854800563}.
]

Every one of the 199 column inequalities is strictly certified; the maximum Arb upper endpoint of the shifted column left-hand sides is

[
-2.635079172408285	imes10^{-11}<0.
]

Consequently, for every probability vector (pinDelta_{199}),

[
oxed{
|A_{199}p-b|_infty
ge eta-delta
=
rac{37088783410838194813145199437}
{92233720368548005630000000000}
=0.40211739548875ldots>rac13.
}
]

This is an exact rational-dual/interval-arithmetic theorem for the **pinned finite 199-column pool and fixed 2,113-row design**. The sixth- and eighth-order row inventories are selected/cut, not complete.

## Program-mass total-variation corollary

Every retained row is an orbit average of even-principal-minor program characters. For a dihedral orbit (O_i) of even Majorana index sets, define

[
phi_i([T])=rac1{|O_i|}sum_{Iin O_i}(-1)^{|Icap T|}.
]

Then (|phi_i|_inftyle1). By the exact program/DPP identity, the expectation of (phi_i) under the ensemble-averaged balanced program-label mass (w_p) is the corresponding raw principal-minor moment; its expectation under the uniform balanced-label distribution (u_{m bal}) is the raw target moment.

If (s_i) denotes the row scale in (A_{199},b), then (A_i p=mathbb E_{w_p}phi_i/s_i) and (b_i=mathbb E_{u_{m bal}}phi_i/s_i). Define

[
G([T])=sum_{i=1}^{2113}rac{z_i}{s_i}phi_i([T]).
]

The triangle inequality gives (|G|_inftyle M), where exact rational arithmetic yields

[
M=sum_irac{|z_i|}{s_i}
=rac{181246491308462426915523}{46116860184274002815}
=3930.156792640191ldots.
]

The dual theorem implies

[
mathbb E_{u_{m bal}}G-mathbb E_{w_p}G
=z^{mathsf T}(b-A_{199}p)>eta-delta.
]

Using the total-variation dual inequality
(|mathbb E_PG-mathbb E_QG|le2|G|_inftyoperatorname{TV}(P,Q)), we obtain

[
oxed{
operatorname{TV}(w_p,u_{m bal})
>
rac{37088783410838194813145199437}
{724985965233849707662092000000000}
=5.1157932966157385	imes10^{-5}.
}
]

Equivalently, the trace distance of the corresponding **dephased program-label registers** exceeds this bound. The derivation is recomputed from the pinned rational dual by `verify_199col_program_mass_tv_bound.py` using exact `Fraction` arithmetic.

## Scope and unresolved questions

- The finite-pool theorem and TV corollary apply only to the exact 199 columns and this fixed 2,113-row design.
- The 645 sixth-order and 7 eighth-order rows are selected/cut inventories, not complete higher-order orbit systems.
- A finite-pool dual is not automatically a separator of the continuous physical family. For the 199-column dual, a deterministic 16-start search found a positive 21-torus point with binary64 score 1.3039304930013147. The independent 128-bit Arb certificate encloses the exact-decimal phase point at \([1.3039304930013150180208493982584973\pm6.62\times10^{-35}]>0\). By the exact rational-independence/dense-ray theorem for the 42-site uniform open path, continuity implies that some finite equal-positive-coupling time \\(t>0\\) escapes this particular dual. This does not invalidate the finite 199-column theorem.
- The program-mass TV statement is classical/dephased. It is **not** a Choi-state trace-distance or channel diamond-distance bound.
- The full \\(n=21\\) all-even-principal-minor positive ensemble (or a global physical-family obstruction), the operational Choi/diamond bridge, and tracked manuscript/supplement sources remain open.

## Reproducibility

- [199-column LP transcript](evidence/joint_low_six_eighth_lp_199col_uniform_ray_escape_n21.json)
- [Exact rational dual and 128-bit Arb column intervals](evidence/55probe_199col_uniform_ray_escape_dual_certificate_n21.json)
- [Independent finite-pool verifier](verify_199col_uniform_ray_dual_arb.py)
- [Exact program-mass TV verifier](verify_199col_program_mass_tv_bound.py)
- [199-column reoptimization](reoptimize_199col_uniform_ray_escape.py)
- [199-column torus pricing discovery](discover_199col_uniform_torus_pricing.py)
- [199-column torus search transcript](evidence/199col_uniform_torus_search_n21.json)
- [Independent 128-bit Arb torus certificate](evidence/199col_uniform_torus_arb_n21.json)
- [Dense-torus theorem](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)
- [Successful reoptimization workflow](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45442617400)
- [Successful 128-bit Arb dual-certification workflow](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45443651012)
- [199-column torus pricing workflow 45445503907](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45445503907)
- [199-column finite-time pricing workflow](.github/workflows/eui-199col-uniform-ray-time.yml)


## Explicit finite-time refinement (certified 2026-11-25)

The bounded deterministic search over six windows from (10^{-3}) through (10^8) found the exact-decimal candidate
[
t_* = 6964.814603259045725
= rac{278592584130361829}{40000000000000}>0.
]
For the 42-site uniform open path with (c_0=cdots=c_{40}=t_*) and closing edge (c_{41}=0), the independent 128-bit Arb verifier certifies
[
S_{199}(e^{t_*K_*})
in [0.503110853024683924836078551677pm5.03	imes10^{-31}]>0.
]
The lower endpoint is itself enclosed by
[
[0.50311085302468392483607855167729431699pm4.03	imes10^{-39}]>0.
]
Thus this is an explicit connected, strictly positive internal-coupling physical path escaping the **particular 199-column dual**. It does not invalidate the finite 199-column theorem, and it does not prove feasibility or infeasibility of the full continuous-family moment problem.

The proof artifact pins the exact 199-column rational dual, LP transcript, sixth/eighth cut design, torus certificate, search transcript, and dense-torus theorem hashes. The search and verifier are `discover_199col_uniform_ray_time_escape.py` and `verify_199col_uniform_ray_time_arb.py`; successful workflow [45446134912](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45446134912), evidence commit [e76e8c0](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e76e8c025ba06033e9f36c2a20fb52401f914d8f).

## Next finite-pool diagnostic: 200 columns

The certified path above is appended as physical column 1657. The new `reoptimize_200col_uniform_ray_escape.py` rebuilds all 2,113 fixed rows on the 199-column parent plus this exact rational path, while independently checking the complete ancestry of the 192--199 uniform-time certificates. Its workflow re-runs the 199-column dual and torus verifiers, refreshes the finite-time discovery against the exact current torus certificate, then Arb-verifies the exact time before solving the binary64 HiGHS diagnostic. The first run exposed a stale cross-workflow torus-certificate hash; the corrected workflow [45463435443](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45463435443) is the authoritative rerun. No 200-column LP conclusion is claimed until that run finishes.

The 200-column LP remains a finite selected-row diagnostic: 1,461 complete second-/fourth-order rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. A sub-(1/3) discovery still requires an exact rational primal, Arb checks on every pinned row, and complete sixth-order separation; an above-(1/3) result requires a new exact rational dual and independent Arb certification against all 200 columns.
