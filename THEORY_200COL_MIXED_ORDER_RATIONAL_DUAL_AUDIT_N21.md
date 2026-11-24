# 200-column mixed-order rational-dual audit at n=21

**Status:** the 200-column LP is a binary64 discovery only. A new exact-rational/128-bit Arb verifier is being added; no 200-column theorem is claimed until it passes.

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
