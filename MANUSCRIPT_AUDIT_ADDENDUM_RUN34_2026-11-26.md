# EUI manuscript/research audit — Run 34 (2026-11-26)

## Repository inspection and issue selection

- Repository: tengxianglin/EfficientUnitaryInversion; default branch main.
- Starting HEAD: e6efa87c0c3348424d5395d3a768323d0239a926 (Run 33 cycle-matching parity theorem audit).
- Rechecked recent commits, the open-issue set, Issue #7 and its latest comments, Issue #5's 204-column frontier, Issue #6's Appendix B normalization record, and Issue #3's classifier regression status.
- Issue #7 remains the highest-leverage scientific track: the complete balanced-slice target has an exact unrestricted-SO(42) representation, while the physical fixed-cycle convex-hull question remains open.
- The repository still has no editable manuscript TeX/Bib/PDF/Word source; theory notes and audit addenda are the editable research record.

## Scientific result

Proved an exact no-go for a **single period-two 42-cycle physical atom**. For c_(2j)=a and c_(2j+1)=b, no real a,b can make every pair principal minor of Q=e^{A(c)}D equal -1/41. Since the full target includes these pair coordinates, no such single atom can realize the full even-minor hierarchy.

The proof has three parts:

1. The pair-moment equations force the parity-block matrices to have the forms C=xI+cF and S=sG, with F a symmetric circulant sign matrix and G a circulant sign matrix.
2. Fourier phase compatibility reduces all possible nonconstant G patterns to b=-a. Exact enumeration covers all 2^21 Fourier-phase sign rows, all 1,024 F patterns, and all 2,095,104 nonconstant (F,G) pairs in that branch. The only 24 exact feasible sign systems force x=0 and c=s=1/sqrt(41); all rank-one residual cases are excluded by explicit inequalities.
3. At Fourier modes 0 and 1, the residual equations make exp(i4a) algebraic and also make exp(i4a cos(pi/21)) algebraic. The Gelfond-Schneider theorem makes the latter transcendental, a contradiction.

A useful geometric clarification was added: Q=e^{A/2}D e^{-A/2} is a symmetric orthogonal involution, so P=(I+Q)/2 is a rank-21 real projector. The balanced-slice target is exactly the Haar-Grassmannian average of the principal-minor observables, by O(42)-invariance and det(I+tODO^T)=(1-t^2)^21. The physical question is thus a restricted Grassmannian cubature problem.

## Evidence and reproducibility

Created:
- THEORY_N42_PERIOD_TWO_SINGLE_ATOM_NO_GO.md
- verify_n42_period_two_single_atom_no_go.py
- evidence/n42_period_two_single_atom_no_go.json
- .github/workflows/eui-n42-period-two-single-atom-no-go.yml

Local checks:
- Python compilation passed.
- Exact verifier passed in 22.2 seconds.
- All sign enumeration and rational constraints use integer arithmetic; no floating-point optimization is used.
- The machine-readable evidence records all phase counts, both G branches, all 24 residual mask pairs, and the exact Haar moment sequence.

Commits:
- e474c66aabcf308321361ad0efb20e0a181a14c4 — exact verifier.
- 59ab4f39ea9e4b3f4771117977896729ba11024a — machine-readable evidence.
- 4f3e3049c2c64f6919b09078d41b5017243b903f — theory note.
- ccecf4c26f27585fc38c79476984025289c04197 — CI workflow.

The workflow file is present on main. The commit-status endpoint returned no status checks; the available commit-workflow listing is limited to pull-request-triggered runs, so no hosted push-run result is claimed. Local compile and full exact verification are complete.

## What this does not prove

- It does not exclude a positive mixture of period-two atoms.
- It does not exclude a positive ensemble with non-period-two cycle couplings.
- It is not a global separating functional for the full physical family.
- It gives no Choi trace-distance or channel diamond-distance bound.

The earlier matching-atom parity theorem remains a statement about the particular perfect-matching representation, not the full physical convex hull. The 204-column finite-pool dual remains a separate finite-pool result.

## Next highest-value action

Do not continue single-atom searches in the same ansatz. The next decisive problem is the **convex hull of the period-two family**: derive a linear inequality valid for every real (a,b), or construct a positive measure whose displacement-resolved pair-minor functions average to -1/41. If that subfamily is excluded, move to general non-periodic cycle couplings; if it is feasible, use the construction to identify what extra degrees of freedom are essential at N=42.


## Literature check added after the first audit

- Ehler & Gräf, *Constructive Approximation* 49, 29–58 (2019), DOI 10.1007/s00365-018-9443-5: general Grassmannian cubatures and designs. This supports the geometric framing, not the restricted-cycle result.
- Wan et al., *Communications in Mathematical Physics* 404, 629–700 (2023), DOI 10.1007/s00220-023-04844-0: matchgate 3-design from Haar matchgates and a discrete Clifford-matchgate ensemble. It concerns the full matchgate group, not the fixed-cycle one-exponential support.
- Boccato, Pieroni & Trevisan, arXiv:2504.08971: trace/TV/Wasserstein relations between Slater determinant states and their DPPs. Potentially relevant to a future operational bridge, but not a channel diamond-norm theorem for EUI.

The theory note now records this novelty boundary. The available status endpoint still exposes no hosted check for this push; exact local verification remains the current reproducibility evidence.
