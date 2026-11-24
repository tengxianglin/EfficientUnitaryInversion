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
