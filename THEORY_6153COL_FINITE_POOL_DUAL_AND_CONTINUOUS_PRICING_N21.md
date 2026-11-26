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

## 3. Continuous pricing of this specific 6,153 dual

A deterministic finite-multistart search and independent 256-bit Arb verifier are being added:

- Search: `search_ising_full_fourth_plus_thirty_gapped_n21.py`
- Independent verifier: `verify_ising_full_fourth_plus_thirty_gapped_escape_arb_n21.py`
- Workflow: `.github/workflows/eui-full-fourth-plus-thirty-gapped-search-n21.yml`

The search reconstructs the exact 116-term rational dual from the 6,153 Arb certificate and prices connected and multi-segment open-path couplings. The search is finite numerical discovery only. A candidate counts as a physical escape only after its decimal couplings are frozen as exact rationals and the independent Arb verifier certifies all 1,764 orthogonality entries, determinant one, and a strictly negative target-minus-score interval.

A successful connected escape would refute only this particular 6,153-column dual as a global separator, including on the strictly positive interior-edge family. Failure to find an escape is not a global bound.

## 4. Reproducibility and next decision

The search and verifier pin the 6,153 diagnostic and Arb certificate by SHA256, reconstruct the rational dual from the exact certificate coefficients, and reject stale parent evidence.

Decision rule:
1. If Arb certifies a connected escape, record the precise failure of this dual and only then consider another finite-pool reoptimization.
2. If only a multi-segment escape is certified, report that narrower scope.
3. If no escape is found, report only the finite search scope.
4. If a positive primal ensemble is ever produced, independently certify every required moment rather than treating selected low-order rows as the complete all-even-minor problem.

The paper-level target remains an exact positive physical measure matching every even principal minor, or a global separator valid for every allowed cycle coupling, together with a separate operational bridge to Choi/diamond error.
