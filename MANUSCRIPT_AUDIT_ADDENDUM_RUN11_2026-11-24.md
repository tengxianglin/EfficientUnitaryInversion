# Manuscript and claim-scope audit addendum — 2026-11-24 (run 11)

## Source rechecked

The repository still has no tracked manuscript `.tex`, `.bib`, compiled `.pdf`, or separate supplement source. The source inspected for this audit is the public arXiv HTML version:

- [Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians](https://arxiv.org/html/2506.20570v1), version dated 25 June 2025.
- Authors: Yin Mo, Tengxiang Lin, Xin Wang.
- Appendix B (HTML lines 292–313) defines a support-mismatch perturbation and reports 10,000 independently sampled random Hamiltonians, with **average Choi-state fidelity** at selected noise strengths.

The manuscript's Appendix B is finite Monte Carlo average-fidelity evidence. It does not establish a worst-case-over-Hamiltonian channel bound, a worst-case-over-input diamond bound, or a bridge from the current moment LP residuals to per-instance Choi/diamond error.

## Paper-central theorem map

The tracked note [THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md) states an exact conditional full diamond-minimax formula for the fixed six-query architecture, allowing arbitrary non-radial and orientation-dependent stochastic logical-Pauli correction tables. Its hypothesis is one legal physical ensemble with exactly uniform diagonal program masses in both parity sectors. The repository records computer-assisted exact positive ensemble certificates at n=5 and n=7. At admissible long rings n>=21, the required joint uniform ensemble is not yet constructed or ruled out.

The all-even-principal-minor target remains
\[
\mathbb E\det R_{I,I}
=(-1)^{v(I)+k}\frac{\binom nk}{\binom{2n}{2k}},
\qquad |I|=2k.
\]
A selected-row LP, finite-pool dual, low-order approximation, or escape from a particular dual is not a substitute for an exact positive solution of this full system or a global physical-family obstruction.

## Latest mixed-order finite-pool result and its escape

The 196-column / 2,113-row design is a finite-pool mixed-order diagnostic: 1,461 complete second-/fourth-order rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. Its exact rational 128-bit Arb dual proves
\[
\min_{p\in\Delta_{196}}\|A p-y\|_\infty
\ge 0.41973861353658526\ldots>\frac13.
\]
This is a theorem only for the exact 196 listed columns and 2,113 listed rows; sixth/eighth-order rows are not exhaustive.

The same 196-column dual has now been escaped by an explicitly certified **strictly positive equal-coupling path**:
\[
c_1=\cdots=c_{41}=t_*,
\qquad
t_* = \frac{1535392895240590633}{500000000000000}
=3070.785790481181266>0.
\]
At 128-bit Arb precision,
\[
S_{196}(e^{t_*K_*})
\in[0.3637338868622431662555343998069\pm6.07\times10^{-32}]>0.
\]
This refutes global separation by that particular 196-column dual. It does not invalidate the finite-pool theorem and does not prove full continuous-family feasibility or infeasibility.

Evidence:
- [196-column finite-pool theorem](THEORY_196COL_2113ROW_FOURTH_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md)
- [Uniform-path escape theorem](THEORY_196COL_UNIFORM_TORUS_DUAL_ESCAPE.md)
- [128-bit finite-time Arb certificate](evidence/196col_uniform_ray_time_arb_n21.json)
- [128-bit torus Arb certificate](evidence/196col_uniform_torus_arb_n21.json)
- [Exact dense-torus theorem](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)

## Current executable follow-up

The explicit finite-time path above is appended as column 1654. A reproducible 197-column / 2,113-row reoptimization has been committed and launched:

- [Reoptimizer](reoptimize_197col_uniform_ray_escape.py)
- [Workflow](.github/workflows/eui-reoptimize-197col-uniform-ray.yml)
- [Run 45418660688](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45418660688)

At the time of this addendum, the workflow has passed Python compilation, the eighth-order enumeration regression, the uniform-path torus regression, and the 193-column ancestor re-certification; the 194-/195-/196-column re-certification and 197-column LP are still running. No 197-column result is claimed.

If the LP is above 1/3, its floating dual is only a discovery candidate and requires a new exact-rational dual plus independent Arb pricing of all 197 columns. If it is below 1/3, the rationalized primal requires interval verification on every pinned row and a complete 63,133-orbit sixth-order audit.

## Separate 6,129-column low-order track

The 6,129-column full-second/fourth workflow has produced a diagnostic JSON with 6,129 candidates, but its status remains explicitly `floating_full_fourth_6125_column_separator_candidate_not_arb_certified`. It is not a theorem and is not used to support any manuscript claim in this addendum. The metadata-consistent rerun 45398176444 completed the LP step but failed its artifact commit with a Git add/add conflict because the earlier 45397929610 run had already committed the same evidence path. The 6,129-column JSON is present from 45397929610; 45398176444 is not a second independent LP result. A new exact-rational/Arb certificate is required before any finite-pool claim is made for this expanded pool.

## Manuscript claim discipline

1. Keep the 196-column theorem attached to its exact 196-column pool and 2,113-row design.
2. Keep the uniform-path result attached to the particular 196-column dual it escapes.
3. Do not call the 2,113-row design a complete sixth/eighth-order certificate.
4. Do not infer Choi-state trace distance or channel diamond distance from the program-label TV/moment bounds without a separate operational theorem.
5. Do not describe Appendix B's average over 10,000 random Hamiltonians as a worst-case guarantee.
6. No manuscript-source edit is claimed because manuscript and supplement source files are not tracked in this repository.


## 197-column mixed-order discovery (2026-11-24)

The first completed 197-column HiGHS run (workflow [45418660688](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45418660688)) successfully appended the fifth explicit uniform positive-coupling path at column 1654. On the same fixed 2,113-row design it returned
\[
\epsilon_{197}^{\rm HiGHS}=0.41510755390323995>\frac13,
\]
with independently recomputed maximum residual 0.41510755390327847 and binary64 primal/dual gap below \(4\times10^{-16}\). The floating dual has \(\ell_1\)-norm 1 and discovery objective 0.4151075539032396.

This is **not yet a theorem**: the floating dual has not been rationalized and Arb-verified on all 197 columns. The independent verifier is now tracked at [verify_197col_uniform_ray_dual_arb.py](verify_197col_uniform_ray_dual_arb.py). The verifier's Python compilation passed in the first workflow run. The follow-up workflow [45420486905](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45420486905) is queued to re-run all pinned ancestor certificates, recompute the 197-column LP, rationalize the new dual, and certify all 197 column inequalities at 128-bit Arb precision. No 197-column finite-pool lower bound is claimed until that verification completes.


## Final run-11 correction: 197-column mixed-order dual is now Arb-certified

The pending statement in the preceding section is superseded by the completed authoritative workflow [45420486905](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45420486905), which successfully re-ran the pinned 197-column LP and independently certified its rational dual.

For the exact 197-column pool and 2,113-row design (1,461 complete second-/fourth-order rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows), the 128-bit Arb verifier certifies all 197 rational-dual inequalities. The exact dual has
\[
\|z\|_1=\frac{2305843009213687359}{2305843009213693952}<1,
\]
\[
\beta=\lambda+z^{\mathsf T}b
=\frac{957172851239594049}{2305843009213693952},
\qquad \delta=10^{-10},
\]
and hence the finite-pool minimax lower bound
\[
\min_{p\in\Delta_{197}}\|Ap-b\|_\infty
\ge
\beta-\delta
=\frac{9347391123134860821080377}{22517998136852480000000000}
=0.415107553803245\ldots>\frac13.
\]
The largest Arb upper endpoint among the 197 shifted column inequalities is
\[
-6.236499982702207\times10^{-11}<0.
\]
The exact dual support is 63 rows (2 low-order, 59 sixth-order, 2 eighth-order). This is a finite-pool theorem only; the 645 sixth and seven eighth rows are selected/cut inventories, not complete higher-order orbit systems.

Evidence: [certificate JSON](evidence/55probe_197col_uniform_ray_escape_dual_certificate_n21.json), [independent verifier](verify_197col_uniform_ray_dual_arb.py), [theory note](THEORY_197COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md), [workflow 45420486905](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45420486905), and [certificate commit 3ba48b8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/3ba48b8ee85f69906613c817e20e69e1c05bea10).

A new 21-dimensional uniform-path torus-pricing search against this 197-column rational dual is now running in [workflow 45422332355](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422332355). A positive candidate will count as a continuous-ray escape only after the exact-decimal phase vector is independently certified by Arb. Failure of this finite multi-start search is not a global separation proof.

The 197-column result does not resolve the full all-even-principal-minor ensemble problem, the global continuous physical-family problem, or the separate Choi/diamond operational bridge. No manuscript-source edit is claimed: the repository still lacks tracked manuscript/supplement TeX, Bib, and PDF files.


## Final continuum correction: the 197-column dual has a certified uniform-ray escape

The new 197-column finite-pool theorem remains valid, but its particular rational dual is **not** a global separator of the continuous physical family. The 21-dimensional uniform-path torus search [workflow 45422332355](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422332355) found an exact-decimal phase vector; the independent 128-bit Arb verifier certifies
\[
S_{197}(R(\theta_*))
\in
[1.7152449127664802147236733367025386
\pm5.20\times10^{-35}]>0.
\]
The exact phase vector and all input hashes are stored in [the torus Arb certificate](evidence/197col_uniform_torus_arb_n21.json). The pricing gradient's maximum relative self-test defect was \(2.4667717161121613\times10^{-9}\); this is only a discovery diagnostic, while the Arb interval is the proof.

By the already proved rational independence of the 21 frequencies \(4\cos(k\pi/43)\), the equal-positive-coupling open-path orbit is dense in the 21-torus. Continuity therefore implies existence of some finite \(t>0\) with positive pricing against the 197-column dual. This refutes extension of that *particular dual* to the continuous equal-coupling ray. It does not invalidate the exact finite 197-column theorem or prove feasibility/infeasibility of the full physical-family moment problem.

A separate search for an explicit finite decimal time is running in [workflow 45422810828](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422810828); only a positive Arb interval will be accepted as an explicit-time certificate.

Evidence and theory: [197-column theorem and escape note](THEORY_197COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md), [search transcript](evidence/197col_uniform_torus_search_n21.json), [128-bit Arb torus certificate](evidence/197col_uniform_torus_arb_n21.json), [independent verifier](verify_197col_uniform_torus_pricing_arb.py), and [workflow 45422332355](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422332355).

The remaining paper-central blockers are unchanged: a positive ensemble satisfying every even principal-minor constraint at n=21 (or a global obstruction), a separate per-instance operational bridge to Choi/diamond distance, and tracked manuscript/supplement source files.


## Additional 197-pool program-mass TV corollary

The exact 197-column mixed-order dual also yields a finite-pool program-label distribution bound. Each of the 2,113 raw rows is an orbit average of a balanced-label character \(\phi_i\) with \(\|\phi_i\|_\infty\le1\), by the exact program/DPP identity. Undoing the row scales \(s_i\), the dual test function has sup-norm at most
\[
M=\sum_i |z_i|/s_i
=\frac{48834410514256017587079}{11529215046068469760}.
\]
Combining the dual gap \(\beta-\delta\) with the total-variation dual inequality gives, for every mixture on the exact 197-column pool,
\[
\operatorname{TV}(w_p,u_{\rm bal})
>
\frac{9347391123134860821080377}
{190759416071312568699527343750}
=4.900094221110678\times10^{-5}.
\]
This is a classical balanced program-label mass (equivalently dephased-register trace-distance) result, finite-pool only. It is not a Choi-state trace-distance or channel diamond-distance guarantee. The derivation is recorded in [the 197-column theory note](THEORY_197COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md).


## Explicit finite-time escape of the 197-column dual is now certified

The bounded positive-ray search found the exact rational time
\[
t=\frac{14386899302852951223}{250000000000000}
=57547.597211411804892>0,
\]
with all 41 internal open-path couplings equal to \(t\). The independent 128-bit Arb verifier certifies
\[
S_{197}(e^{tK_*})
\in[0.55379539820858412380775878883\pm2.37\times10^{-30}]>0.
\]
This is an explicit finite physical path outside the pinned 197-column pool. It directly refutes global separation by the 197-column dual, without relying only on the dense-torus existence argument. The finite 197-column minimax theorem is unaffected.

Evidence: [search transcript](evidence/197col_uniform_ray_time_search_n21.json), [128-bit Arb certificate](evidence/197col_uniform_ray_time_arb_n21.json), [independent verifier](verify_197col_uniform_ray_time_arb.py), [successful workflow 45422810828](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45422810828), [commit b3d85e7](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b3d85e763465a62c7015ded2c803de27746753a6).

Next: append this sixth explicit equal-coupling path as column 1655 and reoptimize the fixed 2,113-row mixed-order design. The 198-column result must receive its own rational dual/Arb certificate; no extension of the 197-column theorem is assumed.


## New 198-column mixed-order finite-pool theorem (128-bit Arb)

The 198-column reoptimization completed and its exact rational dual passed independent 128-bit Arb verification for all 198 columns. The fixed 2,113-row design still comprises 1,461 complete second-/fourth-order coordinates, 645 selected/cut sixth-order coordinates, and seven selected eighth-order coordinates.

The exact dual has \(\|z\|_1<1\), objective
\[
\beta=\frac{942233106657499055}{2305843009213693952},
\qquad \delta=10^{-8},
\]
and every shifted column inequality is strictly negative; the largest certified upper endpoint is \(-1.978441155579956\times10^{-9}\). Therefore
\[
\min_{p\in\Delta_{198}}\|Ap-b\|_\infty
\ge
\frac{368059798280886313618383}
{900719925474099200000000}
=0.4086284624903306\ldots>\frac13.
\]
The dual support has 66 nonzero rows (5 low-order, 58 sixth-order, 3 eighth-order). This is an exact finite-pool theorem only; no full continuous-family or channel diamond conclusion is claimed.

Evidence: [198-column theorem note](THEORY_198COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md), [LP transcript](evidence/joint_low_six_eighth_lp_198col_uniform_ray_escape_n21.json), [exact rational dual + 198 Arb intervals](evidence/55probe_198col_uniform_ray_escape_dual_certificate_n21.json), [independent verifier](verify_198col_uniform_ray_dual_arb.py), [reoptimization workflow 45424946690](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45424946690), and [dual-certification workflow 45425975195](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45425975195).

Next: run continuous uniform-torus pricing on the new 198-column dual. The new dual must receive its own search and Arb witness; the 197-column torus/finite-time escape does not automatically transfer to it.


## 2026-11-24: 6,129-column full-fourth certificate and 198-dual torus escape

A new exact-rational 80-term dual has now been independently Arb-certified on the 6,129-column full second-/fourth-order pool. The common column gap is strictly greater than \(1/5\); the minimum Arb lower endpoint is \(0.2374306538960380051\ldots\), at pinned base atom 14. The resulting finite-pool bounds are
\[
\|b-Ap\|_\infty>1/2665,\qquad
\operatorname{TV}(w_p,u_{\rm bal})>1/5330.
\]
This remains a finite-pool theorem only.

Separately, the 198-column mixed-order dual has a strict 128-bit Arb-positive point on the 21-torus. By the dense-ray theorem and continuity, this proves existence of a finite equal-positive-coupling open-path escape from that particular dual. An explicit time remains to be isolated.

The 6,129 verifier and 198-torus verifier are separate reproducible workflows; neither result implies a Choi/diamond bound or solves the all-even-minor ensemble problem.



## Run 11 continuation: 199-column mixed-order theorem and exact program-mass TV bound

The current mainline advances beyond the 198-column state described above. The exact 199-column / 2,113-row LP has been rationalized and its dual independently certified at 128-bit Arb precision. The certificate is pinned by SHA256 and verifies all 199 physical columns. It has
\[
\|z\|_1=1,\qquad
\beta=\frac{3708878342006156685}{9223372036854800563},
\qquad \delta=10^{-10},
\]
with maximum shifted column-LHS Arb upper endpoint
\[
-2.635079172408285\times10^{-11}<0.
\]
Hence
\[
\min_{p\in\Delta_{199}}\|A_{199}p-b\|_\infty
\ge
\frac{37088783410838194813145199437}
{92233720368548005630000000000}
=0.40211739548875\ldots>\frac13.
\]
The row inventory remains 1,461 complete second-/fourth-order rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. The latter two inventories are not complete.

An exact rational program-mass corollary has now been added. Undoing the row scales gives the bounded-character test norm
\[
M=\sum_i |z_i|/s_i
=\frac{181246491308462426915523}{46116860184274002815}.
\]
The exact DPP/program-character identity and TV duality imply, for every mixture on this finite pool,
\[
\operatorname{TV}(w_p,u_{\rm bal})
>
\frac{37088783410838194813145199437}
{724985965233849707662092000000000}
=5.1157932966157385\times10^{-5}.
\]
This is a finite-pool balanced program-label mass (equivalently dephased-register trace-distance) bound, not a Choi-state or channel diamond-distance bound.

Reproducibility additions:
- [199-column theory note](THEORY_199COL_2113ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md)
- [Exact TV verifier](verify_199col_program_mass_tv_bound.py)
- [199-column torus pricing discovery](discover_199col_uniform_torus_pricing.py)
- [Independent 128-bit Arb torus verifier](verify_199col_uniform_torus_pricing_arb.py)
- [Pricing workflow](.github/workflows/eui-199col-uniform-torus-pricing.yml)
- [199-column reoptimization workflow 45442617400](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45442617400)
- [199-column dual Arb workflow 45443651012](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45443651012)

The 21-dimensional uniform-path torus search for this *new* 199-column dual is now being run independently. Its finite-pool certificate does not automatically extend to the continuous physical family. A positive torus candidate will count as an escape only if the exact-decimal phase vector has a strictly positive independent Arb interval; a failed finite multi-start search will not be treated as a global separation proof.


## Final run-11 continuum correction: the 199-column dual also has a certified uniform-ray escape

The 199-column finite-pool theorem remains valid, but its particular dual is not a global separator of the continuous physical family. The 16-start 21-dimensional torus search found a candidate with binary64 score \\(1.3039304930013147\\). The independent 128-bit Arb verifier certifies the exact-decimal phase vector:
\[
S_{199}(R(\theta_*))
\in[1.3039304930013150180208493982584973\pm6.62\times10^{-35}]>0.
\]
The gradient self-test maximum relative defect was (3.851324106723261\times10^{-9}); this is discovery diagnostics only, while the Arb interval is the proof.

The exact dense-torus theorem for the 42-site uniform open path proves rational independence of its 21 frequencies. By density and continuity, the positive torus point implies that **some finite \\(t>0\\)** on the admissible equal-positive-coupling physical path has positive pricing against the 199-column dual. This refutes global separation by this particular dual, but it does not invalidate the exact 199-column / 2,113-row finite-pool theorem and does not prove full-family feasibility or infeasibility.

Evidence:
- [Search transcript](evidence/199col_uniform_torus_search_n21.json)
- [Independent 128-bit Arb certificate](evidence/199col_uniform_torus_arb_n21.json)
- [Independent Arb verifier](verify_199col_uniform_torus_pricing_arb.py)
- [Successful workflow 45445503907](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45445503907)
- [Exact dense-torus theorem](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)

A bounded six-window search for an explicit finite decimal time and its independent Arb verifier have been added. Workflow [45446134912](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45446134912) is in progress. A positive binary64 candidate will not be reported as a finite-time theorem unless its exact-decimal rational value has a strictly positive Arb interval.


## Repository manuscript inventory check

A fresh recursive Git tree inspection of `main` returned 912 tracked paths and found no `.tex`, `.bib`, `.pdf`, `.docx`, `.odt`, or `.rtf` manuscript/supplement source. The only manuscript-named tracked files are audit Markdown notes. Accordingly, no formal manuscript-body edit is claimed in this run; the new theorem and reproducibility material are research notes/evidence only.

The other open tracker inspected was Issue #3 (type-1.2 classifier correctness). Its four dependency-light regression tests and compile checks are already green; only a QuAIRKit/Torch-backed end-to-end comb-search smoke test remains. It is separate from the moment/ensemble work tracked here and was not duplicated on Issue #5.
