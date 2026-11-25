# Manuscript audit addendum — Run 25 (2026-11-25)

## Explicit finite-time escape for the 202-column dual

The 202-column dual's positive torus pricing witness has been strengthened to a directly certified finite physical path. A deterministic 12-start, 400-iteration-per-start search (seed `202611251840`) selected

\[
t_{202}=2906260.875695546623319
=\frac{2906260875695546623319}{1000000000000000}>0.
\]

For the 42-site uniform open path,
\[
c_0=\cdots=c_{40}=t_{202},\qquad c_{41}=0,
\]
all 41 internal couplings are strictly positive. Independent 128-bit Arb verification certifies
\[
S_{202}(e^{t_{202}K_*})
\in[0.1751293387639196832622918436\pm5.42\times10^{-29}]>0.
\]
The certified lower-endpoint enclosure is
\[
[0.17512933876391968326229184354589133476\pm1.71\times10^{-39}].
\]

The machine-readable certificate is `evidence/202col_uniform_ray_time_arb_n21.json`; the search transcript is `evidence/202col_uniform_ray_time_search_n21.json`. The certificate pins the 202-column dual SHA-256 `e76b964f36192069070647964c415c0f87308c26552ca718aa119acf62586187`, LP SHA-256 `98b07b734dcb86c4bff1a28d550d1b1a3dda64857d05d2c38c8136c10de280ba`, torus certificate, and search transcript. End-to-end CI [45618890398](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45618890398) succeeded. The preceding attempt [45618516687](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45618516687) failed on a verifier-dimension bug, fixed in [dd279775](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/dd2797752e177b4a339279ee27c3a254e9168bc1).

## Scope and interpretation

This positive score strictly violates one column inequality required for the particular 202-column dual to separate the full continuous equal-coupling physical ray. It does **not** invalidate the 202-column finite-pool theorem, establish full-family feasibility/infeasibility, complete all sixth/eighth principal-minor constraints, or imply a Choi trace-distance or channel diamond-distance bound.

The fixed finite-pool result remains:
- 202 physical columns and 2,113 rows;
- complete 21 second-order and 1,440 fourth-order rows;
- 645 selected/cut sixth-order and 7 selected eighth-order rows;
- exact rational dual with \(\|z\|_1=1\);
- certified lower bound
\[
\eta_{202}\ge
\frac{895537407287253699785572869}
{2305843009214427131000000000}
=0.3883774410090271\ldots>\frac13.
\]
The program-mass TV corollary applies to the balanced program-label distribution/dephased register in one selected parity sector, not the Choi state or channel diamond norm.

## Executable next step

The new `reoptimize_203col_uniform_ray_escape.py` appends the exact 202-dual escape as physical column 1660 and reruns the same fixed 2,113-row LP. The workflow `.github/workflows/eui-reoptimize-203col-uniform-ray.yml` pins Python 3.11, NumPy 2.3.5, SciPy 1.15.3 and python-flint 0.8.0, rechecks the 202-column dual/time certificate, and archives only the generated 203-column LP/candidate output. The HiGHS result is discovery only: above-cap requires a new rational dual and independent Arb verification on all 203 columns; below-cap requires an exact primal audit and complete sixth-order separation.

## Remaining paper-central blockers

1. Exact positive physical ensemble satisfying the complete all-even-principal-minor system at \(n=21\), or a global physical-family converse.
2. Complete sixth/eighth and higher even-order moment control.
3. A quantitative bridge from the moment/program-mass discrepancy to the relevant operational Choi/diamond error with correct quantifiers.
4. The editable manuscript source is still absent from the repository; this addendum is an audit record, not a claim that the public arXiv manuscript has been edited.
