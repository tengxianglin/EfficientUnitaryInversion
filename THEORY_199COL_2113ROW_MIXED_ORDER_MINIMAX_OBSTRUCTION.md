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
- A finite-pool dual is not automatically a separator of the continuous physical family. The 199-column dual is currently undergoing its own 21-dimensional uniform-path torus pricing; only a strictly positive independent Arb interval would establish an escape from this particular dual.
- The program-mass TV statement is classical/dephased. It is **not** a Choi-state trace-distance or channel diamond-distance bound.
- The full (n=21) all-even-principal-minor positive ensemble (or a global physical-family obstruction), the operational Choi/diamond bridge, and tracked manuscript/supplement sources remain open.

## Reproducibility

- [199-column LP transcript](evidence/joint_low_six_eighth_lp_199col_uniform_ray_escape_n21.json)
- [Exact rational dual and 128-bit Arb column intervals](evidence/55probe_199col_uniform_ray_escape_dual_certificate_n21.json)
- [Independent finite-pool verifier](verify_199col_uniform_ray_dual_arb.py)
- [Exact program-mass TV verifier](verify_199col_program_mass_tv_bound.py)
- [199-column reoptimization](reoptimize_199col_uniform_ray_escape.py)
- [199-column torus pricing discovery](discover_199col_uniform_torus_pricing.py)
- [Dense-torus theorem](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)
- [Successful reoptimization workflow](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45442617400)
- [Successful 128-bit Arb dual-certification workflow](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45443651012)
- [199-column torus pricing workflow](.github/workflows/eui-199col-uniform-torus-pricing.yml)
