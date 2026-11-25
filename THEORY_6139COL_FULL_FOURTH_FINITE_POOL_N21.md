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
[
\|D^{-1}y\|_1=1,
\qquad
\|y\|_1=
\frac{14164662956157091950169}{26649999999999965711}<533.
\]
The positive rational slack is certified for every one of the 6,139 columns. The smallest Arb lower endpoint is
[
0.23116168351538610661485619036098658\ldots
\]
(the fractional-grid column \(L=35,\alpha=1/2\)). The verifier therefore freezes the simpler exact rational common gap
[
\delta=\frac{231161}{100000}.
\]

**Theorem (finite-pool obstruction).** For every probability vector \(p\in\Delta_{6139}\),
[
\boxed{\|b-Ap\|_\infty>
\frac{231161}{533000000}.}
\]
Using the exact program-character/DPP identity, each retained coordinate is the expectation of a bounded orbit character. Hence the associated balanced program-label distribution obeys
[
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

The next decisive task is continuous pricing of this specific 104-term 6,139-column dual. A finite multistart search can discover a candidate escape, but only an exact-rational frozen path and independent Arb interval with strictly negative slack establish one. If no escape is found, that is only a finite search result, not a global certificate. The all-even-principal-minor positive-ensemble problem remains the paper-level bottleneck.
