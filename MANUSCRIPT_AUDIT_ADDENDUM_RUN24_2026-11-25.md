# Manuscript audit addendum — Run 24 (2026-11-25)

## New finite-pool result

The 201-column finite-time escape was appended as physical column 1659. Reoptimization on 202 physical columns and the fixed 2,113-row mixed-order design returned a binary64 objective of 0.3883774420090974. The exact rational dual was independently certified with 128-bit Arb across all 202 columns.

The strict finite-pool lower bound is
[
\eta_{202}\ge
\frac{895537407287253699785572869}
{2305843009214427131000000000}
=0.3883774410090271\ldots>1/3.
]

The exact dual has (\|z\|_1=1), rational objective
(895537409593096709/2305843009214427131), and slack (10^{-9}). The maximum shifted-column upper endpoint is (-8.472548623521715\times10^{-10}).

The corresponding exact program-mass TV lower bound for the balanced program-label distribution is
[
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{298512469095751233261857623}
{6522695149182325846205200000000}
=4.5765203227866974\times10^{-5}\ldots.
]
It is not a Choi or diamond bound.

## Evidence and code

- Reoptimizer: `reoptimize_202col_uniform_ray_escape.py`.
- Independent dual verifier: `verify_202col_uniform_ray_dual_arb.py`.
- Exact TV postprocessor: `verify_202col_program_mass_tv_bound.py`.
- LP: `evidence/joint_low_six_eighth_lp_202col_uniform_ray_escape_n21.json`.
- Dual certificate: `evidence/55probe_202col_uniform_ray_escape_dual_certificate_n21.json`.
- TV output: `evidence/202col_program_mass_tv_bound_n21.json`.
- LP workflow 45617194808 and certification workflow 45617814843 both succeeded.

The pool is 183 canonical columns + 9 nonuniform positive open paths + 10 uniform positive open paths. The row design remains mixed-order: complete second/fourth moments, 645 selected/cut sixth rows, and seven selected eighth rows.

## Interpretation and blocker

This result is strictly for the 202-column finite pool and fixed 2,113-row design. It does not extend to all canonical columns, all continuous physical paths, complete sixth/eighth moments, or channel diamond distance.

A separate 202-dual torus pricing workflow is now running. If a positive torus interval is certified, the next step is an exact finite-time search and Arb check. The current 202-column finite-pool theorem must not be conflated with a global physical-family theorem.


## Continuous-family follow-up

The 202-column dual also has a strictly positive continuous-torus pricing witness. An eight-start, 120-iteration search found a binary64 score of 0.9971550877716457; the exact decimal phase vector was independently certified by 128-bit Arb:
[
S_{202}(R(\theta_*))\in
[0.997155087771645424273385402820507\pm5.10\times10^{-34}]>0.
]
The verifier pins the exact 202-column dual and LP hashes. By the dense-orbit theorem for the uniform positive-coupling ray, this proves existence of some finite positive physical time escaping this particular dual. An explicit finite-time rational witness is still pending; the separate search/Arb workflow is in progress.
