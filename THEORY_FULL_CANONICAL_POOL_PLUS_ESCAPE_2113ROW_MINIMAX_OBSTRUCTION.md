# Full 1,641-column canonical inventory plus one continuous escape: 2,113-row minimax obstruction

**Status:** computer-assisted proof completed with exact rational dual data and outward-rounded 128-bit Arb intervals.  
**Scope:** all 1,641 frozen canonical generators plus one separately certified continuous-path generator; not the unrestricted continuous family.

## Theorem

Let \(\mathcal C_{1641}\) be the complete frozen canonical path inventory, with little-endian binary64 SHA256
\[
\texttt{f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98}.
\]
Let \(c_\star\) be the exact-rational continuous-path escape generator pinned by the 152-column candidate input and its Arb certificate. For the 2,113 normalized moment rows defined in [the 184-column theorem](THEORY_184COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md), every probability mixture over
\[
\mathcal Q=\mathcal C_{1641}\cup\{c_\star\},
\qquad |\mathcal Q|=1642,
\]
satisfies
\[
\boxed{
\min_{p\in\Delta(\mathcal Q)}\|Ap-y\|_\infty
\ge
\frac{22487122319210016751569973413}
{46116860184300265870000000000}
=0.48761173742841650\ldots>\frac13.
}
\]
The exact rational dual, lambda, slack, and lower-bound derivation are unchanged from the 184-column certificate.

## Why the finite-pool extension is rigorous

The 184-column active certificate consists of 183 canonical columns plus the one continuous-path generator \(c_\star\). Its exact rational dual vector \(z\) and scalar \(\lambda\) satisfy \(\|z\|_1=1\), with slack \(\delta=10^{-10}\). The independent 128-bit Arb certificate checks
\[
z^T a(c)+\lambda-\delta<0
\]
for every one of those 184 active physical columns. The largest active-column interval upper endpoint is
\[
-7.6565440382899941721222335508948670479\times10^{-11}<0.
\]

The remaining 1,458 canonical columns were then checked individually by a separate complete 128-bit Arb audit. The audit result is:
- complete = true;
- 1,458 columns checked;
- 1,458 strictly negative interval upper endpoints;
- zero strictly positive intervals;
- zero intervals overlapping zero;
- maximum upper endpoint among the unused canonical columns:
\[
[-0.0085355262917551396968965552281556190618
\ \pm 2.78\times10^{-41}],
\]
attained at canonical column 430.

Thus every canonical column, and the separately included continuous escape column, satisfies the same exact dual inequality. Multiplying by arbitrary nonnegative probabilities summing to one gives
\[
z^T A p+\lambda-\delta\le0.
\]
Since \(\|z\|_1=1\),
\[
\|Ap-y\|_\infty
\ge |z^T(y-Ap)|
\ge \lambda+z^Ty-\delta,
\]
which is the displayed bound. This proves the result for every convex mixture over the stated 1,642-generator finite union, not merely for a numerically optimized distribution.

## Reproducibility and evidence

- 184-column exact rational dual and active-column Arb certificate: evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json;
- complete unused-canonical Arb transcript: evidence/55probe_184col_full_canonical_pool_arb_n21.json;
- complete-audit verifier: verify_184col_full_sixth_cut_dual_all_canonical_arb.py;
- binary64 discovery screen (not used as a proof premise): evidence/55probe_184col_full_sixth_cut_dual_pricing_screen_n21.json;
- successful full-pool audit workflow: [45107567728](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45107567728);
- full-audit evidence commit: [dcab0b7](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/dcab0b7fd7c7e81c36c7164441189c7e89d26a29);
- GitHub blob SHA1 of the full interval transcript: 146b04f500b519e971b88d325d0cbccd1ee2fd87;
- artifact: [eui-184col-full-canonical-pool-arb](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45107567728/artifacts/14788590851);
- frozen canonical inventory SHA256: f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98.

The full verifier reconstructs the exact rational dual from the committed certificate, regenerates the frozen canonical inventory, excludes only the 183 canonical columns already checked in the active certificate, and recomputes the dual pricing functional for all remaining 1,458 columns with Arb. The acceptance condition is a strict interval upper endpoint below zero for every column; no binary64 nonpositive score is treated as a proof.

## Boundary of the theorem

This closes the complete canonical finite-pool separation problem for the pinned 2,113-row mixed-order objective. It does not cover every point in the unrestricted 41-dimensional continuous coupling family. In particular, a finite list of 1,641 canonical paths plus one continuous escape is not a discretization theorem for that family.

It also does not turn the 2,113-row residual into a Choi-infidelity or diamond-distance guarantee. The paper-level next step is a global continuous-family separation theorem (or a rigorously certified continuous escape) and, independently, an operational per-instance bridge from moment residuals to channel error.
