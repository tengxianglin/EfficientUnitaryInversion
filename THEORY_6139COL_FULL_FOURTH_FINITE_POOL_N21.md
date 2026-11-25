# 6,139-column complete second-/fourth-order finite-pool obstruction (n=21)

Run date: 2026-11-25. Reproducible source revision: `71d1b1d1b027371df933f687082bd31b5ad03ff1`; evidence commit: `c6ae70171d68e4a56cf598bf4679f21279ba1d6f`.

## Certified statement

The exact candidate pool contains 6,139 physical columns:

- 22 pinned base atoms;
- 6,101 corrected fractional single-open-path grid atoms;
- 16 exact-rational gapped paths (14 inherited from the 6,137 pool and two previously Arb-certified escapes of the 6,137-column dual).

The feature system contains all 21 distance-averaged second moments and all 1,440 fourth-order dihedral orbits (all 111,930 four-subsets are included before orbit reduction). The exact rank reduction leaves 1,313 independent moment equations, or 1,314 equalities including normalization, equivalent to the full second-/fourth-order system for normalized physical mixtures.

The frozen rational dual has 104 nonzero coefficients: one second-order coordinate and 103 fourth-order coordinates. With
\[
D=\operatorname{diag}(41 I_{21},533 I_{1440}),
\]
the verifier checks exactly
\[
\|D^{-1}y\|_1=1,
\qquad
\|y\|_1=
\frac{14164662956157091950169}{26649999999999965711}<533.
\]
The positive rational slack is certified for every one of the 6,139 columns. The smallest Arb lower endpoint is
\[
0.23116168351538610661485619036098658\ldots
\]
(the fractional-grid column \(L=35,\alpha=1/2\)). The verifier therefore freezes the simpler exact rational common gap
\[
\delta=\frac{231161}{100000}.
\]

**Theorem (finite-pool obstruction).** For every probability vector \(p\in\Delta_{6139}\),
\[
\boxed{\|b-Ap\|_\infty>
\frac{231161}{533000000}.}
\]
Using the exact program-character/DPP identity, each retained coordinate is the expectation of a bounded orbit character. Hence the associated balanced program-label distribution obeys
\[
\boxed{\operatorname{TV}(w_p,u_{\rm bal})>
\frac{231161}{1066000000}.}
\]
The latter is also the trace distance between the corresponding dephased classical program-label registers.

The LP diagnostic is a discovery artifact; the proof is the exact rational dual plus independent Arb interval pricing of every column. The Arb run uses 512-bit precision for the base and gapped columns and 128-bit precision for the 6,101 fractional-grid columns. The exact certificate status is `arb_certified_finite_6139_column_full_fourth_plus_sixteen_gapped_separator`.

## Reproduction and provenance

- Diagnostic: [evidence/ising_full_fourth_plus_sixteen_gapped_n21.json](evidence/ising_full_fourth_plus_sixteen_gapped_n21.json)
- Arb certificate: [evidence/ising_full_fourth_plus_sixteen_gapped_arb_n21.json](evidence/ising_full_fourth_plus_sixteen_gapped_arb_n21.json)
- Discovery: [discover_ising_full_fourth_plus_sixteen_gapped_n21.py](discover_ising_full_fourth_plus_sixteen_gapped_n21.py)
- Independent verifier: [verify_ising_full_fourth_plus_sixteen_gapped_arb_n21.py](verify_ising_full_fourth_plus_sixteen_gapped_arb_n21.py)
- Successful workflow: [45548273987](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45548273987)
- Diagnostic SHA-256 pinned by the certificate: `b456515c60930c0e253f9239615acc59d2bd816d540bdad9e35840f5d58ad7f3`.

The verifier now writes the correct 6,139-column scope and uses the certified rational floor \(231161/1000000\); earlier generated prose that said 6,137 columns or retained the weaker \(1/5\) floor has been corrected at source and regenerated.

## Scope and limits

This is a theorem for this exact finite candidate pool and these complete second-/fourth-order coordinates. It does **not** prove a global obstruction for all nonuniform gapped couplings or the continuous physical family. It does not impose all even-principal-minor constraints, and the program-mass TV bound is not a Choi-state trace-distance or channel diamond-distance bound. The 6,137-column dual's continuous escapes are part of the 16-path pool; they are not escapes of the new 6,139-column dual.

## Continuous pricing of the 104-term 6,139-column dual

The deterministic pricing search evaluated 912 initial candidates (256 frozen-pool samples, 256 connected random starts, 263 multi-segment starts, and 128 fractional perturbations). The analytic gradient self-test's maximum absolute error was (2.2600188387400522\times10^{-10}).

It found two strict floating-point escape candidates. Both were frozen as exact rational couplings and independently certified with 256-bit Arb:

1. **Connected positive-coupling path.** All 41 internal couplings are strictly positive; the open-chain wrap edge is zero. The minimum positive internal coupling is
   \\[
   \frac{19999999999999999}{20000000000000000000000}\approx10^{-6}.
   \\]
   The certified target-minus-candidate interval is
   \\[
   [-26.2094024867797243425\ldots\ \pm 5.80\times10^{-72}]<0.
   \\]

2. **Five-segment path.** Internal zero edges are ({11,16,18,21}); the minimum positive coupling is \\(10^{-8}\\). Its certified target-minus-candidate interval is
   \\[
   [-30.229130393353341\ldots\ \pm 7.88\times10^{-72}]<0.
   \\]

Both certificates verify all 1,764 entries of the 42-by-42 rotation's orthogonality defect and enclose determinant one. These are strict escapes of the **6,139-column dual**, not failures of the finite-pool theorem above.

Reproduction:

- Search transcript: [evidence/ising_full_fourth_plus_sixteen_gapped_search_n21.json](evidence/ising_full_fourth_plus_sixteen_gapped_search_n21.json)
- 256-bit Arb escape certificate: [evidence/ising_full_fourth_plus_sixteen_gapped_escape_arb_n21.json](evidence/ising_full_fourth_plus_sixteen_gapped_escape_arb_n21.json)
- Search: [search_ising_full_fourth_plus_sixteen_gapped_n21.py](search_ising_full_fourth_plus_sixteen_gapped_n21.py)
- Independent verifier: [verify_ising_full_fourth_plus_sixteen_gapped_escape_arb_n21.py](verify_ising_full_fourth_plus_sixteen_gapped_escape_arb_n21.py)
- Successful workflow: [45549396031](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45549396031)
- Evidence commit: `66cf75f52a48a219f94b0b52cb55cf6869d74682`.

The two new exact-rational paths have been appended to the 6,139 pool. The next candidate set has 6,141 columns: 22 pinned base atoms, 6,101 fractional-grid atoms, and 18 exact-rational gapped paths (16 inherited from the certified 6,139 pool plus these two new escapes). The reoptimizer, independent Arb verifier, and workflow are:

- [discover_ising_full_fourth_plus_eighteen_gapped_n21.py](discover_ising_full_fourth_plus_eighteen_gapped_n21.py)
- [verify_ising_full_fourth_plus_eighteen_gapped_arb_n21.py](verify_ising_full_fourth_plus_eighteen_gapped_arb_n21.py)
- [6,141-column workflow](.github/workflows/eui-reoptimize-6141-full-fourth.yml)

The 6,141-column LP and Arb certification are now running. If a new dual is certified, the next step is continuous pricing of that dual; if a primal appears, freeze its support and weights and independently certify the full 1,461-coordinate residual. Neither branch licenses a global claim without the corresponding certificate.

The next decisive task is to resolve the 6,141-column LP and then price its new dual or certify any primal support. A finite multistart search can discover a candidate escape, but only an exact-rational frozen path and independent Arb interval with strictly negative slack establish one. If no escape is found, that is only a finite search result, not a global certificate. The all-even-principal-minor positive-ensemble problem remains the paper-level bottleneck.
