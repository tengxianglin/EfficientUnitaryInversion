# 6,153-column finite-pool theorem and continuous-pricing handoff (N=21)

Date: 2026-11-27

## 1. Independently certified finite-pool theorem

The corrected full-second-/fourth-order workflow [45880800772](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880800772) completed successfully. Its job ran the full 1,461-coordinate LP and the independent Arb verifier, then committed both outputs at [e705c3de4eb65f43009d382caed904cf8b62fa3f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e705c3de4eb65f43009d382caed904cf8b62fa3f).

The exact pinned pool is
\[
6153=22+6101+30,
\]
consisting of 22 base atoms, 6,101 corrected fractional single-open-path grid atoms, and 30 exact-rational gapped paths (28 inherited from the certified 6,151-column pool and two new 256-bit Arb-certified escapes from its dual).

The complete feature system has 1,461 coordinates: 21 second-order coordinates and 1,440 fourth-order dihedral orbits (111,930 four-subsets). The reduced system has 1,313 independent moment equations and 1,314 equalities including normalization.

The exact rational dual has 116 nonzero coefficients and satisfies
\[
\|D^{-1}y\|_1=1,\qquad \|y\|_1=533,
\qquad D=\operatorname{diag}(41I_{21},533I_{1440}).
\]
Independent python-flint/Arb pricing at 128 bits for all 6,101 fractional-grid columns and 512 bits for all 22 base plus 30 gapped columns certifies
\[
y^{\mathsf T}(b-a_j)\ge \frac15
\quad\text{for every one of the 6,153 pinned columns}.
\]
The minimum certified column-gap lower endpoint is
\[
0.2171118517172996872064128775649697\ldots>\frac15.
\]

Consequently every probability vector supported on this exact finite pool obeys
\[
\boxed{\|b-Ap\|_\infty>\frac1{2665}},
\qquad
\boxed{\operatorname{TV}(w_p,u_{\rm bal})>\frac1{5330}}.
\]
The TV statement concerns the balanced program-label distribution / dephased classical label register. It is not a Choi trace-distance or channel diamond-distance bound.

Evidence:
- [6,153 floating diagnostic](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_n21.json)
- [Independent 128/512-bit Arb certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_arb_n21.json)
- [Workflow 45880800772](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45880800772)
- [Certificate commit e705c3d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e705c3de4eb65f43009d382caed904cf8b62fa3f)

## 2. What the theorem does not prove

This is a rigorous obstruction for exactly the 6,153 listed columns. It does not cover all nonuniform gapped couplings, the continuous gapped family, arbitrary multi-segment paths, all even principal-minor coordinates, or an operational Choi/diamond guarantee. In particular, the repeated Arb-certified escapes of previous duals show that a finite-pool dual must not be called a global physical separator.

The 6,153 floating LP diagnostic reported a primal-infeasible / dual-optimal HiGHS status, target score 0.23817163642834843, maximum candidate score 0.012641010269954268, recomputed gap 0.22553062615849276, and maximum pricing-constraint violation 9.86e-14. These are discovery diagnostics; the finite-pool theorem rests on the exact rational dual and independent Arb column pricing, not on the floating LP status.

## 3. Completed continuous pricing of this specific 6,153 dual

Workflow [45892294782](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45892294782) completed SUCCESS. All nine job steps completed, including deterministic search, the independent 256-bit Arb verifier, evidence pin checks, and evidence commit [a25e50b8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a25e50b8a31fb750e60f8802aa641e44a580764d).

The finite multistart search used seed `202611270434`, evaluated 1,822 initial candidates (512 connected random starts, 526 multi-segment random starts, 256 fractional perturbations plus the frozen seed-pool starts), and optimized 16 starts per class with L-BFGS-B and the analytic Fréchet gradient. Its finite-difference gradient self-test had maximum absolute defect (1.816526928877238\times10^{-10}). These are discovery diagnostics, not a continuum proof.

The independent verifier reconstructed the 116-term rational dual from the exact finite certificate, froze candidate couplings as exact rationals, and used 256-bit Arb. It certified two escapes:

- **Connected open-path witness.** All 41 internal couplings are strictly positive, with exact minimum
  [
  c_{min}=\frac{19999999999999999}{20000000000000000000000}
  \approx 10^{-6},
  ]
  and wrap coupling (c_{41}=0). The target-minus-score interval is
  [
  [-20.3240037122535534424538099596397106465\ldots
  \pm 3.92\times10^{-72}]<0.
  ]
- **Four-segment witness.** Internal cuts are at edges ({12,30,33}), and the minimum positive coupling is (10^{-8}). Its target-minus-score interval is
  [
  [-27.8847046473750978838078064544366446125\ldots
  \pm 6.17\times10^{-73}]<0.
  ]

For both candidates, Arb checked all 1,764 entries of the (42\times42) orthogonality defect matrix and certified determinant one. The verifier pins the diagnostic, finite certificate, and search transcript by SHA256. Thus the **particular 6,153-column rational dual is not a global separator**. This does not invalidate the finite-pool theorem or establish full-family convex-hull membership/nonmembership.

Evidence:
- [Search transcript](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_search_n21.json)
- [Independent 256-bit Arb escape certificate](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/ising_full_fourth_plus_thirty_gapped_escape_arb_n21.json)
- [Workflow 45892294782](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45892294782)
- [Evidence commit a25e50b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a25e50b8a31fb750e60f8802aa641e44a580764d)

## 4. Decision after the continuous escape

The 6,153 finite-pool theorem remains valid for its exact 6,153 pinned columns. Its dual, however, is now explicitly refuted on the continuous family. Repeating the same cutting-plane cycle without a structural change would only produce another finite-pool theorem whose dual must be priced again.

The next high-value work is therefore not an automatic 6,155-column expansion. It is to exploit the exact all-even-minor / complement-folded DPP formulation to seek either (i) a positive measure supported on the full cyclic physical family, or (ii) a global inequality with a proof valid for every allowed cycle coupling. The unrestricted (SO(42)) perfect-matching ensemble is a useful target identity but is not itself a physical cycle ensemble.

## 5. A full-dimensional strictly-positive-cycle escape region

The connected Arb witness above has (c_{41}^*=0), but this boundary feature can be removed analytically. Let (c^*\in\mathbb Q^{42}) be its exact rational coupling vector, and keep the 6,153-dual score
[
s(R)=y^{\mathsf T}F(R),\qquad g(c)=y^{\mathsf T}b-s(e^{A(c)}).
]
The finite certificate gives the exact coefficient bound (\|y\|_1=533). Set
[
\delta=\frac1{2,000,000},\qquad
\mathcal B=\left\{c:\ |c_j-c_j^*|<\delta\ (0\le j\le40),\quad 0<c_{41}<\delta\right\}.
]
Every point of \(\mathcal B\) has all 42 cycle couplings strictly positive: the exact minimum of the first 41 base couplings exceeds \(\delta\), and the wrap coupling is positive by definition.

For (c\in\mathcal B), each row and column of (A(c)-A(c^*)) has absolute sum at most (4\delta). Hence
[
\|A(c)-A(c^*)\|_2
\le\sqrt{\|A(c)-A(c^*)\|_1\,\|A(c)-A(c^*)\|_\infty}
\le4\delta.
]
Both generators are real skew-symmetric. Duhamel's identity and orthogonality of their exponentials therefore give
[
\|e^{A(c)}-e^{A(c^*)}\|_2
\le\|A(c)-A(c^*)\|_2
\le4\delta.
]
For any principal (m\times m) minor with (m\in\{2,4\}), multilinearity of the determinant and Hadamard's inequality imply
[
|\det R_{I,I}-\det S_{I,I}|\le m\|R-S\|_2.
]
The 21 second-order coordinates and 1,440 fourth-order coordinates are averages of such minors over cyclic or signed-dihedral orbits, so every feature coordinate changes by at most (4\|R-S\|_2). Consequently
[
|s(R)-s(S)|\le4\|y\|_1\|R-S\|_2
\le 4\cdot533\cdot4\delta
=8528\delta
=\frac{533}{125000}
=0.004264.
]
At the Arb-certified base point,
[
g(c^*)\in[-20.3240037122535534\ldots\pm3.92\times10^{-72}]< -20.324.
]
Thus throughout the entire open set \(\mathcal B\),
[
g(c)<-20.324+0.004264=-20.319736<0.
]
This is a rigorous analytic extension of the Arb base-point escape to a **full-dimensional open region of strictly positive 42-cycle couplings**. It rules out the 6,153 dual as a separator even if the physical domain is restricted to all couplings strictly positive; it still says nothing by itself about whether the target belongs to the convex hull of the full physical family.

The exact rational checks and Arb interval addition are reproduced by `verify_6153_connected_escape_neighborhood.py`; its machine-readable output is `evidence/ising_full_fourth_plus_thirty_gapped_open_box_arb_n21.json`.


The open-box certificate was independently rerun in GitHub Actions workflow [45907210706](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45907210706), with all steps successful. The exact-rational/Arb output is committed at [a56d3d8135ce305c18e3cca8c02b070b66948549](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a56d3d8135ce305c18e3cca8c02b070b66948549).