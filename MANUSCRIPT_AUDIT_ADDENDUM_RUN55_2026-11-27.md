# EUI manuscript/evidence audit — Run 55 (2026-11-27)

## Repository state and issue selection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- HEAD at the start of this run: 994a04396048e2af94477d76731066c5ea83690e.
- The latest completed EUI workflow at the start was the 6,153-dual open-positive-cycle-box certificate, workflow 45907210706 (SUCCESS). The 6,153 finite-pool Arb theorem and its continuous-dual escape/open-box analysis remain correctly scoped in the Run 54 note.
- Open issues rechecked: #5 (full cycle-family convex hull), #7 (physical reachability / positive ensembles), #6 (Appendix B normalization), and #3 (Hamiltonian classifier correctness). Issue #7 was selected for this run because the current N=42 period-two constructions match all pairs and selected quartic orbits but explicitly fail at another quartic coordinate. The next useful question is whether adding more period-two atoms could ever produce a complete small-size design.

## New theorem: N=8 period-two mixtures cannot match the full target

A new exact analytic inequality proves that no probability measure over the full real two-parameter N=8 period-two cycle family can match the balanced-slice even-principal-minor target.

For Q=exp(A(c))D, with c_(2j)=a and c_(2j+1)=b, define the pair and quartic coordinates
\[
P(a,b)=\det Q_{\{0,4\},\{0,4\}},\qquad
K(a,b)=\det Q_{\{0,1,4,5\},\{0,1,4,5\}}.
\]
Fourier reduction gives
\[
P(a,b)=\cos(2a)\cos(2b)\cos(2\sqrt{a^2+b^2}),
\]
\[
K(a,b)=\cos^2(2b)\left[
\cos^2\omega+\frac{a^2}{a^2+b^2}\sin^2\omega
\right],\quad \omega=2\sqrt{a^2+b^2}.
\]
After averaging each atom over its eight cyclic shifts, the pair feature remains P and the quartic feature becomes Kbar=(K(a,b)+K(b,a))/2. With alpha=a^2/(a^2+b^2), beta=b^2/(a^2+b^2), x=cos(omega), z=sin^2(omega), X=cos^2(2a), and Y=cos^2(2b),
\[
\bar K=\tfrac12[Y(x^2+\alpha z)+X(x^2+\beta z)],\quad P^2=XYx^2,
\]
and
\[
(x^2+\alpha z)(x^2+\beta z)=x^2+\alpha\beta z^2\ge x^2.
\]
AM-GM therefore proves Kbar >= |P| for every real a,b, including the zero limit.

The N=8 target has P*=-1/7 and K*=3/35, violating K>=|P|. More quantitatively, the full moment-vector infinity discrepancy is at least 1/35. The two-coordinate dual has exact L1 norm one and margin 1/35. This excludes every positive mixture in the N=8 period-two family, not merely one atom.

The result is restricted to N=8 and period-two couplings. It does not exclude general non-period-two N=8 cycles, and it does not prove a no-go for the unrestricted N=42 cycle family.

## Reproducibility work added

- THEORY_N8_PERIOD_TWO_MIXTURE_FOURTH_ORDER_NO_GO.md: analytic derivation and exact scope.
- verify_n8_period_two_mixture_fourth_order_no_go.py: direct Arb matrix-exponential regression against the Fourier formulas at frozen exact-rational couplings, including positive, negative, and zero-edge parameters.
- .github/workflows/eui-n8-period-two-mixture-fourth-order-no-go.yml: pinned python-flint 0.9.0 CI and committed machine-readable output at evidence/n8_period_two_mixture_fourth_order_no_go.json.

The analytic AM-GM argument is the continuum proof. The finite Arb sample checks are implementation/regression evidence, not a substitute for that proof. Hosted CI was triggered by the workflow addition and is pending at the time of this note.

## Manuscript and supplementary-source audit

The repository tree was rechecked (1,246 entries at the start of this run). No editable tracked TeX/Bib manuscript or separate supplementary source was found. The public manuscript remains Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians, arXiv:2506.20570v1. No formal manuscript or Appendix B numerical table was changed. Issue #6 still records that the normalization helper is verified but the full QuAIRKit-backed Choi-fidelity table has not been regenerated.

## Changes, verified claims, blockers, and next action

**Changed:** added the N=8 period-two mixture theorem, its independent Arb regression, and a dedicated CI workflow.

**Proved analytically:** for every real N=8 period-two parameter pair, the cyclically symmetrized selected quartic minor is at least the absolute value of the selected antipodal pair minor; hence every period-two mixture has full-feature infinity discrepancy at least 1/35 from the balanced target.

**Finite verification pending:** hosted 256-bit Arb checks of the exact Fourier-to-minor formulas and frozen rational regression points. These do not establish the continuum theorem; the AM-GM proof does.

**Still blocked:** full N=42 physical-cycle convex-hull membership/nonmembership; a complete N=42 positive physical ensemble; a global separator for arbitrary 42-edge couplings; and the operational moment-to-Choi/diamond bridge. The N=42 period-two partial ensemble remains valid within its stated 861 pair plus 84 selected quartic coordinates.

**Next highest-value action:** test whether the N=8 AM-GM structure has a useful analogue for the N=42 odd sublattice, or otherwise identify a non-period-two physical family capable of correcting the remaining quartic orbits. Do not infer an N=42 no-go from the N=8 theorem.
