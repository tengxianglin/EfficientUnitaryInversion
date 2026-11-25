# 200-column mixed-order rational-dual audit at n=21

**Status (updated 2026-11-25):** the 200-column / 2,113-row finite-pool obstruction is now certified by an exact rational dual and a complete 128-bit Arb check. This is a theorem for the exact 200 listed physical columns and the fixed mixed-order row design only; it is not a continuous-family, complete-sixth/eighth-order, or Choi/diamond theorem.

## Certified finite-pool theorem

The independent verifier output is committed as `evidence/55probe_200col_uniform_ray_escape_dual_certificate_n21.json` (certificate blob SHA `11a65b9b12dcaafa22cc1c40d923c8e47bc92d45`; evidence commit `29f7a3b3eb2f08b92650a40c5d37027aeed510e9`). It records:

- `status = strict_200col_2113row_uniform_ray_escape_minimax_obstruction`, `complete = true`;
- 128-bit Arb, 200 columns, 2,113 rows;
- exact scaled dual normalization \\(\\|z\\|_1=1\\);
- maximum shifted-column upper endpoint \\(-6.28103085754082\\times10^{-10}<0\\);
- 62 active dual rows (3 low-order, 57 selected sixth-order, 2 selected eighth-order);
- exact certified minimax lower bound
\\[
\\boxed{\\eta_{200}\\ge
\\frac{604278563840813954190133571}
{1537228672809866429000000000}
=0.39309607902139015\\ldots>\\frac13.}
\\]

The row design consists of 1,461 complete second-/fourth-order coordinates, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. The latter two inventories are not complete. The result is therefore strictly a finite-pool minimax obstruction for this fixed design. It does not certify the full 1,641-column canonical inventory, every continuous physical path, all sixth/eighth orbit constraints, or an operational Choi-state/channel diamond-distance bound.

The certificate pins the exact 200-column LP transcript and the 199/198-column ancestry, including the finite-time uniform-ray witness. The finite-time path at column 1657 is
\\[
t=\\frac{6964814605006808961}{10^{15}}
=6964.814605006808961>0,
\\qquad c_0=\\cdots=c_{40}=t,\\quad c_{41}=0.
\\]
The path is included as a physical column; the finite-pool theorem remains valid for the resulting exact 200-column list.

### Reproducibility

- LP diagnostic: `evidence/joint_low_six_eighth_lp_200col_uniform_ray_escape_n21.json`
- Exact dual certificate: `evidence/55probe_200col_uniform_ray_escape_dual_certificate_n21.json`
- Verifier: `verify_200col_uniform_ray_dual_arb.py`
- Workflow definition: `.github/workflows/eui-certify-200col-uniform-ray-dual.yml`
- Evidence commit: [29f7a3b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/29f7a3b3eb2f08b92650a40c5d37027aeed510e9)

The certificate's `complete` flag and all 200 Arb column intervals are stored in the JSON. The binary64 LP objective is discovery; the rational dual plus Arb interval inequalities are the proof.

## Frozen 200-column discovery

The completed HiGHS run reports:
- 200 physical columns and 2,113 scaled rows;
- expanded minimax objective (0.39309608002188723);
- independently recomputed maximum residual (0.39309608002298124);
- dual discovery objective (0.3930960800215787), L1 norm midpoint (1.0000000000004796), and primal/dual gap (3.09\times10^{-13}).

The row inventory is 1,461 complete second-/fourth-order coordinates, 645 selected/cut sixth-order rows, and 7 selected eighth-order rows. The sixth/eighth inventory is not complete.

The added physical column is the eighth explicit uniform-ray path, with
\[
t=\frac{6964814605006808961}{10^{15}}
=6964.814605006808961>0,
\qquad c_0=\cdots=c_{40}=t,\quad c_{41}=0,
\]
at column label 1657. Its finite-time escape certificate is the 199-dual certificate; the new 200 verifier rechecks that ancestry before pricing the 200 columns.

## Exact verification

- LP diagnostic: `evidence/joint_low_six_eighth_lp_200col_uniform_ray_escape_n21.json`
- Parent 199-column dual: `evidence/55probe_199col_uniform_ray_escape_dual_certificate_n21.json`
- Parent 199 finite-time certificate: `evidence/199col_uniform_ray_time_arb_n21.json`
- Verifier: `verify_200col_uniform_ray_dual_arb.py`
- Workflow: `.github/workflows/eui-certify-200col-uniform-ray-dual.yml`
- Output: `evidence/55probe_200col_uniform_ray_escape_dual_certificate_n21.json`

The verifier rationalizes the HiGHS dual, checks the exact scaled-L1 normalization and objective, reconstructs the exact 2,113-row design and all 200 physical columns, then evaluates every dual inequality with Arb. A successful result proves only the finite 200-column / fixed-row-design statement. It does not cover the full canonical inventory, all continuous paths, complete sixth/eighth orbit constraints, or a Choi/diamond operational bound.


## Exact program-mass total-variation corollary

The same rational dual yields an operational statement about the **classical balanced program-label distribution** in one selected parity sector. For every retained row i, let phi_i([T]) be the dihedral-orbit average of the character (-1)^{|I intersect T|}. Since each character is ±1,
\\[
\\|\\phi_i\\|_\\infty\\le1,
\\qquad
\\mathbb E_{[T]\\sim w_R}\\phi_i([T])
=\\text{the corresponding principal-minor orbit moment}.
\\]
The exact row scales are 1/41 (21 second-order rows), 1/533 (1,440 fourth-order rows), 5/19721 (645 selected/cut sixth-order rows), and 1/19721 (seven selected eighth-order rows).

Let z be the 2,113-entry rational dual vector and define
\\[
G([T])=\\sum_i\\frac{z_i}{s_i}\\phi_i([T]).
\\]
Then
\\[
\\|G\\|_\\infty\\le
M:=\\sum_i\\frac{|z_i|}{s_i}
=\\frac{91957325757615679956959}{23058430092147996435}
\\approx3988.013294492653884645.
\\]
Writing beta for the exact dual objective and delta for its certified slack,
\\[
\\beta-\\delta
=\\frac{604278563840813954190133571}
{1537228672809866429000000000}.
\\]
The Arb-certified column inequalities imply the same strict inequality for every probability mixture p over the exact 200-column pool:
\\[
\\mathbb E_{u_{\\rm bal}}G-\\mathbb E_{w_p}G>\\beta-\\delta.
\\]
Using |E_P G-E_Q G| <= 2||G||_infty TV(P,Q), we obtain
\\[
\\boxed{
\\operatorname{TV}(w_p,u_{\\rm bal})>
\\frac{1812835691522441862570400713}
{36782930303046271982783600000000}
\\approx4.9284700174425941841\\times10^{-5}.
}
\\]

This is equivalently a trace-distance lower bound for the corresponding dephased balanced-label registers. It is **not** a Choi-state trace-distance or channel diamond-distance converse. The statement is for one selected parity sector and the exact 200-column pool; it does not repair the incomplete sixth/eighth orbit inventories.

Reproduce the exact rational post-processing with:
- `verify_200col_program_mass_tv_bound.py`
- `evidence/200col_program_mass_tv_bound_n21.json`

The verifier pins the source Arb certificate SHA256 and recomputes M and the TV fraction using only Python's `fractions.Fraction`; it does not rerun the interval pricing itself.


## Continuous uniform-path escape of the 200-column dual (certified 2026-11-25)

The finite 200-column theorem above is unchanged, but its particular dual is **not** a separator of the continuous physical family. This has now been established in two independent stages.

### Positive torus witness

On the exact 21-torus parameterization of the 42-site uniform open path, a deterministic four-start cofactor-gradient search found the exact-decimal phase vector stored in evidence/200col_uniform_torus_search_n21.json. The maximum relative defect in the analytic-gradient checks was \(7.26\times10^{-9}\). The optimizer is discovery only.

The independent 128-bit Arb verifier certifies
\[
S_{200}(R(\theta_*))
\in
[1.4530576032069032574827532865451450
\pm5.50\times10^{-35}]>0.
\]
The certificate pins the exact 200-column rational dual, its LP transcript, and the 2,113-row cut design. Combined with the exact dense-orbit theorem for the uniform 42-site open-path generator, this already proves existence of some finite positive time with positive pricing.

### Explicit finite-time physical witness

A deterministic six-start one-dimensional search then found
\[
t_* = 666454.439114346168935
=\frac{133290887822869233787}{200000000000000}>0.
\]
For the physical open path
\[
c_0=\cdots=c_{40}=t_*,\qquad c_{41}=0,
\]
all 41 internal couplings are strictly positive. The independent 128-bit Arb verifier certifies
\[
S_{200}(e^{t_*K_*})
\in
[0.1462687155056939188352076552
\pm1.54\times10^{-29}]>0.
\]
Thus this is an explicit connected physical path escaping the **particular 200-column dual**, not merely a torus-closure argument.

### Exact scope

- The 200-column / 2,113-row finite-pool lower bound and its program-label TV corollary remain valid for the exact pinned 200 columns.
- The explicit path proves that the same dual cannot be extended unchanged to the full continuous physical family.
- It does **not** invalidate the finite-pool theorem, prove feasibility or infeasibility of the full continuous-family moment problem, complete the sixth/eighth orbit inventories, or imply a Choi/diamond operational bound.
- The 645 sixth-order rows and seven eighth-order rows remain selected/cut, not complete.

### Reproduction

- Torus search and evidence: discover_200col_uniform_torus_pricing.py, evidence/200col_uniform_torus_search_n21.json.
- Independent torus Arb certificate: verify_200col_uniform_torus_pricing_arb.py, evidence/200col_uniform_torus_arb_n21.json.
- Finite-time search and evidence: discover_200col_uniform_ray_time_escape.py, evidence/200col_uniform_ray_time_search_n21.json.
- Independent finite-time Arb certificate: verify_200col_uniform_ray_time_arb.py, evidence/200col_uniform_ray_time_arb_n21.json.
- Successful torus workflow: [45584351764](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45584351764).
- Successful finite-time workflow: [45585112087](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45585112087).
- Evidence commits: [435c7cd](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/435c7cd2c354e5e4530ba65185a51b294ed36d89), [1c19fe2](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1c19fe23500a74205531d1220e8029f02ada67ec).
