# Manuscript and supplementary-material audit (source review 2026-11-22; research update 2026-11-24)

## Source inspected

The README identifies the project as accompanying **“Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians.”** The current repository tree contains no manuscript .tex, .bib, .pdf, or separately versioned supplementary source. The accessible manuscript and appendices are the arXiv HTML version:

- https://arxiv.org/html/2506.20570v1
- *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*
- Yin Mo, Tengxiang Lin, Xin Wang
- Version date shown in the HTML: 25 June 2025

This audit is limited to that version and the repository state inspected on 2026-11-22; it does not assert that no later manuscript exists elsewhere.

## Claims and assumptions relevant to EUI

### Appendix A: exact structured inversion

- Theorem A1 gives a one-query, ancilla-free inverse criterion: a Pauli operator V must anticommute with every Pauli term in the known support S, yielding VUV†=U†.
- Corollary A2 restates the criterion as the absence of an odd-cardinality subset of support terms whose product is proportional to identity.
- Theorem A3 gives a (2^L-1)-query recurrence for pairwise-commuting support terms covered by an anticommuting set W.
- Theorem A4 extends the recurrence to a commuting decomposition (S-hat_0,S-hat_1).

These are exact protocol statements under known Pauli support and their stated commutation/anticommutation assumptions. The finite moment-dual computations below neither prove nor refute those algebraic theorems.

### Appendix B: robustness evidence

Appendix B models support mismatch as
\[
H=\sum_{P\in S}\alpha_P P
+\delta\sum_{P\in S'}\beta_P P,
\]
where S' is the complement of the ideal support and delta is defined through an L1-coefficient ratio. It reports 10,000 random instances and average Choi-state fidelities for several comb protocols and noise levels.

This is finite Monte Carlo evidence for average Choi fidelity. The inspected appendix does not provide a uniform worst-case channel-distance theorem, nor a theorem connecting the moment residuals in the current Ising/path analysis to the operational Choi fidelity of an implemented inverse circuit.

## Current finite-pool moment evidence (2026-11-22)

### Earlier 103-column result and its escape

A 128-bit Arb dual certificate for a frozen 103-column / 1,762-row pool proved a lower bound 0.3368495129681047... > 1/3. That theorem was restricted to those 103 columns and rows. Dual pricing then found ten additional canonical physical columns with strictly positive Arb reduced-cost intervals, so the 103-column dual did not separate the expanded pool. This history is recorded in THEORY_103COL_38PROBE_DUAL_OBSTRUCTION.md and its evidence files.

### Current 113-column / 55-separator result

The latest finite LP uses 113 pinned legal 42-site path generators and 1,779 normalized rows:

- 1,461 second-/fourth-order rows;
- 311 sixth-order rows (256 screened, 38 parent probes, eight separators from the rejected 38-probe candidate, one prefix separator from the rejected 46-probe candidate, and eight separators from the rejected 47-probe candidate);
- seven selected eighth-order rows.

Its binary64 HiGHS objective is 0.36575443678254027... > 1/3. A separate exact-rational dual certificate, independently checked with 128-bit Arb against all 113 physical columns, proves
\[
\min_{p\in\Delta_{113}}\|Ap-y\|_\infty
\ge
\frac{4118028861881514868548001}
{11258999068426240000000000}
=0.3657544366825429...
>\frac13.
\]
The exact dual has ||z||_1=1152921504606844607/1152921504606846976<1, slack delta=10^-10, and a strictly negative Arb upper endpoint for every pinned column inequality (maximum upper endpoint approximately -8.24778e-11). See THEORY_55PROBE_113COL_DUAL_OBSTRUCTION.md and evidence/55probe_113col_dual_certificate_n21.json.

This rejects every convex mixture of the pinned 113 columns for this exact 1,779-row constraint set. It does not reject the remaining 1,528 canonical columns or all physical generators. The 311 sixth-order rows are not the complete set of 63,133 sixth-order dihedral orbits. The LP did not produce an admissible 1/3-candidate.

The 128-bit Arb pricing workflow has now screened all 1,528 unused canonical columns in the frozen 1,641-column pool. The binary64 screen found 66 positive reduced-cost candidates; the ten highest were independently checked with 128-bit Arb and all ten had strictly positive interval lower endpoints (columns 1191, 916, 700, 974, 127, 889, 910, 107, 902, 355). This invalidates the 113-column separator for any expanded pool containing one of those columns, but does not prove an improved ensemble. See evidence/55probe_113col_dual_pricing_screen_n21.json and evidence/55probe_113col_dual_pricing_arb_n21.json. The 123-column reoptimization over the same 1,779 rows has now been completed. Its binary64 HiGHS objective is 0.3511700099912447, above 1/3, so it produces no admissible candidate. A 128-bit Arb rational dual certificate verifies all 123 column inequalities and proves
\[
\min_{p\in\Delta_{123}}\|Ap-y\|_\infty
\ge
\frac{202435727565723844694298279}
{576460752305701721000000000}
=0.35117000898331857\ldots
>\frac13.
\]
The exact dual has \(\|z\|_1=1\), uses slack \(10^{-9}\), and the maximum Arb upper endpoint of \(A^Tz+\lambda-\delta\) over the 123 columns is below \(-2.60568\times10^{-10}\). This is a theorem for the pinned 123-column pool and 1,779 rows only. See THEORY_55PROBE_123COL_DUAL_OBSTRUCTION.md and evidence/55probe_123col_dual_certificate_n21.json.

Workflow 45018694807 has now screened all 1,518 unused columns in the frozen 1,641-column canonical pool. The binary64 screen found 34 positive reduced-cost candidates; the ten highest were independently recomputed with 128-bit Arb, and all ten intervals are strictly positive: columns 1610, 1640, 367, 433, 388, 253, 368, 87, 743, and 69. The largest Arb pricing score is 10.7288893003344779... (column 1610), and the second is 2.5544859328709926... (column 1640). These are certified escapes of the 123-column dual, not yet an improved ensemble. Any nonpositive binary64 score is only a screen result; it is not a rigorous all-column exclusion.

### 133-column reoptimization

The ten Arb-positive columns were added to the pinned 123-column pool. The 1,779-row HiGHS LP returned objective
\[
0.3498255930807595>\frac13,
\]
with 42 positive weights and a primal-dual discovery gap of approximately \(7.22\times10^{-16}\). Thus this expanded finite LP also has no sub-\(1/3\) candidate. The objective is numerical discovery evidence until its rationalized dual is interval-certified. The 128-bit Arb dual verification of all 133 physical columns is running in workflow 45019181024. The next pricing scripts are prepared to screen the remaining 1,508 canonical columns after certification.

## Consequence for manuscript claims

The finite-pool dual certificate is a minimax theorem for a pinned finite set of physical generators and moment rows, not an operational inversion-error bound. It does not imply a Choi-fidelity statement. The manuscript-level bridge remains open:

1. Specify the exact random/physical ensemble and the map from its moment constraints to the implemented inverse channel.
2. Derive an explicit inequality from the relevant moment residuals to a Choi-state trace distance, diamond norm, or fidelity loss, with all dimension and normalization factors.
3. Separate average-over-ensemble guarantees from worst-case-over-Hamiltonian guarantees.
4. If no such bridge is available, present the moment-dual result as a distinct auxiliary theorem rather than using it to support Appendix B's robustness claim.

The 113-column lower bound is restricted to its pinned rows and columns. It must not be presented as a lower bound over the full canonical pool or over all physical generators.


## 133-column dual certification completed (2026-11-22 correction)

The status above saying that the 133-column Arb dual audit was running is superseded. Workflow [45019181024](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45019181024) completed successfully. Commit [e40cf6b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e40cf6b4d12b2178c4433e21c47f927d2856d42c) records the complete 128-bit Arb certificate in `evidence/55probe_133col_dual_certificate_n21.json`.

For the exact 133 pinned columns and the same 1,779 rows, the certificate proves
\[
\min_{p\in\Delta_{133}}\|Ap-y\|_\infty
\ge
\frac{3938686025482020591204251}
{11258999068426240000000000}
=0.3498255929807588\ldots
>\frac13.
\]
The exact dual has
\[
\|z\|_1=\frac{1152921504606846859}{1152921504606846976}<1,
\qquad \delta=10^{-10},
\]
and all 133 column inequalities have strictly negative 128-bit Arb upper endpoints; the largest is below `-8.2976879635052549e-11`. The exact gap above (1/3) is `557059008019821773612753/33776997205278720000000000`.

This is a finite-pool minimax theorem only. The 1,779 rows still contain 311 selected sixth-order rows and seven selected eighth-order rows, not the complete moment domains. It gives no all-physical-family no-go and no operational Choi/diamond-norm guarantee. The formal statement and proof are in `THEORY_55PROBE_133COL_DUAL_OBSTRUCTION.md`.

A new pricing workflow was added in commit `038cec576a6c7dbea991f2a9bdd99da5445b511f`; run [45023408185](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45023408185) screens the remaining 1,508 canonical columns and Arb-checks the top ten positive candidates.


## 143-column reoptimization (2026-11-22)

The 133-column dual was used to price the full remaining canonical pool. The binary64 screen found 23 positive discovery scores among 1,508 unused columns; the ten highest were independently recomputed with 128-bit Arb and all ten had strictly positive lower endpoints (columns 323, 374, 120, 206, 278, 438, 178, 896, 229, 320). The 133-column separator is therefore escaped by adding any one of these columns. This is a pricing statement, not a feasible-mixture result.

A 143-column LP was then reoptimized on the same 1,779 rows. Its binary64 HiGHS objective is 0.34406530610030656, with 47 positive weights and a primal-dual discovery gap of approximately 2.50e-15. No sub-1/3 candidate was produced. Transcript SHA256: `5642e2b04e50cf1954f621464691e2a83736f06e5fb120f0b5c370b001c0ebc8`; evidence: `evidence/joint_low_six_eighth_lp_143col_55probe_n21.json`. This objective remains numerical discovery evidence until the 143-column rationalized dual is certified. The 128-bit Arb certification is running in workflow [45023774747](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45023774747).

The 143-column theorem, if certified, will still concern only the exact 1,779 selected rows and the pinned 143 physical columns. It cannot be promoted to a full-canonical-pool or all-physical-family lower bound.


## Rigorous limitation of average Choi-fidelity evidence (2026-11-22)

A separate closed-form counterexample now makes the operational-claim gap explicit; see `THEORY_CHOI_FIDELITY_VS_DIAMOND_COUNTEREXAMPLE.md`.

For (W_d=\operatorname{diag}(1,\ldots,1,-1)), the normalized Choi fidelity relative to the identity channel is ((d-2)^2/d^2\to1), while a two-level superposition of the first and last basis states makes the output states orthogonal, giving the exact diamond distance (2). Thus there is no dimension-independent function tending to zero with Choi infidelity that bounds the diamond distance.

Even at fixed (d=2), an ensemble that is ideal with probability (1-\varepsilon) and applies (Z) with probability (\varepsilon) has mean Choi fidelity (1-\varepsilon\to1), while its worst-case diamond distance remains (2). This is a mathematical counterexample to inferring a uniform guarantee from an average alone; it is not a claim that this bad channel is realized by the current EUI physical family.

Accordingly, Appendix B's finite-sample mean Choi fidelities may support empirical average-performance statements for the sampled distribution, but not worst-case-over-input or worst-case-over-Hamiltonian guarantees without additional uniform or tail assumptions. A dimension-aware operational theorem remains open.


## 143-column Arb certificate completed (2026-11-22 correction)

The preceding sentence saying the 143-column dual certificate was running is superseded. Workflow [45023774747](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45023774747) completed successfully and commit `325c092eb409f6c3dc8b10569ac76e89268a5aaf` records the complete 128-bit Arb certificate. It proves
\[
\min_{p\in\Delta_{143}}\|Ap-y\|_\infty
\ge
\frac{968457739933803314304969}
{2814749767106560000000000}
=0.3440653060003041\ldots>\frac13.
\]
The exact dual has (\|z\|_1=576460752303423461/576460752303423488<1), slack (10^{-10}), and maximum Arb upper endpoint below `-8.2883631651865609e-11). The exact gap above (1/3) is `90623452694849942914907/8444249301319680000000000`. Formal proof: `THEORY_55PROBE_143COL_DUAL_OBSTRUCTION.md`.

The new 143-column pricing workflow [45024159768](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45024159768) is screening all 1,498 unused canonical columns and checking the top ten positive candidates with Arb. No claim about the remaining canonical pool is made until that evidence completes.

The Choi/diamond note now also records the standard dimension-dependent bridge from Kliesch and Roth, *PRX Quantum* **2**, 010201 (2021), Propositions 51 and 53, together with explicit counterexamples to removing dimension or replacing worst-case by average quantifiers.


## 143-column dual pricing completed (2026-11-22)

Workflow [45024159768](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45024159768) screened all 1,498 unused columns in the frozen 1,641-column canonical pool in binary64. Eight candidates had positive discovery scores; all eight were independently checked with 128-bit Arb and all eight pricing intervals have strictly positive lower endpoints: columns 168, 454, 129, 257, 432, 823, 249, and 532. This invalidates the 143-column separator after adding any of these columns. It does not prove an improved mixture or exclude additional escapes hidden by binary64 rounding.

The 151-column reoptimization using those eight Arb-positive columns is running in workflow [45024329244](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45024329244). Its outcome will be treated as binary64 discovery until any resulting dual is independently Arb-certified.


## 151-column reoptimization (2026-11-22)

The eight Arb-positive escapes of the 143-column dual were added to form a 151-column pool. The 1,779-row HiGHS LP completed with objective 0.3437890063736484, 52 positive weights, recomputed maximum residual 0.3437890063766349, and primal-dual discovery gap (4.43\times10^{-14}). It produced no sub-1/3 candidate. Transcript SHA256: `341247c5ceddd5d07b1758b56ff6a7ed1f01f4c05e3e5dd83ead0319046fbaa0`; evidence: `evidence/joint_low_six_eighth_lp_151col_55probe_n21.json`. The raw binary64 dual L1 norm is slightly above one (1.0000000000001859); the 151-column verifier rationalizes and rescales it before interval certification. Workflow [45024474393](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45024474393) is performing the 128-bit Arb checks of all 151 column inequalities.


## 151-column Arb certificate completed (2026-11-22)

The pending 151-column dual audit has completed successfully. Workflow [45024474393](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45024474393) rationalized/rescaled the HiGHS dual and used 128-bit Arb to verify all 151 column inequalities. It proves
\[
\min_{p\in\Delta_{151}}\|Ap-y\|_\infty
\ge
\frac{3963617383802565315392938733}
{11529215046070612670000000000}
=0.3437890062735403\ldots>\frac13.
\]
The exact dual has \(\|z\|_1=1\), slack \(10^{-10}\), and maximum Arb upper endpoint below \(-8.3697181614344422\times10^{-11}\). The exact gap above \(1/3\) is
\[
\frac{361637105337083276178816199}
{34587645138211838010000000000}.
\]
Proof: `THEORY_55PROBE_151COL_DUAL_OBSTRUCTION.md`; certificate: `evidence/55probe_151col_dual_certificate_n21.json`; certificate commit: [4c76f28](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4c76f2843ac9e5e94820a89a2b4aeb611186ef0b).

This is a finite-pool theorem on the exact 1,779 selected rows only. It is not a no-go over the remaining 1,490 canonical columns, all physical generators, the complete sixth/eighth moment domains, or operational channel distance. The next action is to price the remaining canonical columns against this certified 151-column dual and Arb-check every positive candidate.


## 151-column dual pricing and full-pool Arb audit (2026-11-22)

The certified 151-column dual was screened in binary64 against all 1,490 unused columns in the frozen 1,641-column canonical pool. The screen found zero positive scores; its largest unused score is \(-0.00635987569965061\) at column 1632. The active-pool maximum is \(-9.845096786420537\times10^{-11}\). This is only a floating-point screen, not a strict extension of the theorem.

A dedicated verifier now evaluates every unused column with 128-bit Arb: `verify_55probe_151col_full_canonical_pool_arb.py`, run by `.github/workflows/eui-151col-full-canonical-pool-arb.yml`. It emits `evidence/55probe_151col_full_canonical_pool_arb_n21.json` and exits nonzero unless all 1,490 interval upper endpoints are strictly negative. The ordinary top-positive-candidate verifier correctly checked zero candidates because the binary64 screen had no positive candidates; it must not be mistaken for the all-pool proof.

If the exhaustive Arb job passes, the 151-column dual lower bound extends to all 1,641 columns in the frozen canonical path pool, but only for the pinned 1,779 selected rows. No all-Hamiltonian, all-moment, or operational channel theorem follows.


## Full 1,641-column canonical-pool obstruction certified (2026-11-22)

The 151-column dual was extended to the entire frozen canonical pool. The new 128-bit Arb audit evaluated every one of the 1,490 unused columns; all 1,490 interval upper endpoints are strictly negative. Workflow [45034448993](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45034448993) completed successfully, including frozen-seed verification and exact orbit-enumeration tests. The worst unused-column upper endpoint is \(-0.0063598756997121345\ldots\), at canonical column 1632; the active 151-column certificate's maximum upper endpoint remains the overall limiting margin, below \(-8.3697181614344422\times10^{-11}\).

Combining the original 151-column Arb certificate with the exhaustive 1,490-column audit proves
\[
\min_{p\in\Delta_{1641}}\|Ap-y\|_\infty
\ge
\frac{3963617383802565315392938733}
{11529215046070612670000000000}
=0.3437890062735403\ldots>\frac13.
\]
The exact dual has \(\|z\|_1=1\) and slack \(10^{-10}\). This is now a strict no-go for every convex mixture over the complete frozen 1,641-column canonical 42-site path pool on the pinned 1,779 rows. Any larger all-moment maximum containing these same normalized rows inherits the lower bound. Formal proof: `THEORY_55PROBE_1641COL_CANONICAL_POOL_OBSTRUCTION.md`; evidence: `evidence/55probe_151col_full_canonical_pool_arb_n21.json`; run [45034448993](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45034448993); commit [1cd365d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1cd365d7254643132d784926904e315a23096e21).

This does not extend to physical generators outside the frozen canonical pool and does not imply an operational Choi/diamond-norm bound. The selected sixth/eighth rows are sufficient for this lower bound but are not a complete audit of those moment domains.


## Exact path sign-gauge reduction (2026-11-22)

The path generator has 41 signed edge couplings and no closing edge. A diagonal sign matrix gauges every coupling vector to its componentwise absolute value: \(DK(c)D=K(|c|)\). Hence \(e^{K(|c|)}=De^{K(c)}D\), and every principal minor is invariant under this conjugation. All moment features in the present LP therefore depend only on the 41 coupling magnitudes. This exact reduction removes sign patterns from the full-family search, but leaves an unbounded continuous nonnegative orthant; it does not extend the 1,641-column certificate by itself. Proof: `THEORY_PATH_SIGN_GAUGE_REDUCTION.md`.


## Continuous-family counterexample to the 151-column dual (2026-11-23)

The finite 1,641-column obstruction does not extend to the full continuous positive-coupling path family using the same dual. An explicit rational path generator was constructed with
\[
m=(6,0,14,0,0,26,0,10,0,32,0,18,0,34,0,30,2,6,0,7,23,0,28,0,10,0,32,0,20,2,4,1,32,0,68,0,2,0,26,0,30),
\]
and \(c_j=1/1000\) when \(m_j=0\), otherwise \(c_j=3927m_j/5000\), with \(c_{41}=0\). Every one of the 41 path-edge magnitudes is strictly positive.

Workflow [45045453133](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45045453133) used 128-bit Arb on the exact rational input and the exact 151-column dual. It certified
\[
S(c)=\lambda-\delta+z^\mathsf T a(c)
\in[500.2406414402261032179394993312647\pm3.03\times10^{-32}]>0.
\]
The candidate is verified outside the frozen 1,641-column pool. Exact input SHA256: 0221d6eb7570d87ef52bd17eff30e83ff1fcc2ae765dc86f582b2f3c30082e08; evidence: evidence/continuous_path_dual_escape_arb_n21.json; proof and scope: THEORY_CONTINUOUS_PATH_DUAL_ESCAPE.md; verifier: verify_continuous_path_dual_escape_arb.py; evidence commit: [d8a4df8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d8a4df8530d2084629af5575fa2f2d6af7848df6).

This is a counterexample to **global validity of this particular dual**, not to the finite-pool theorem and not a proof that a full continuous-family ensemble meets the \(1/3\) cap. It shows that the previous next step—extending this same separator over the entire positive orthant—is false. A separate 152-column binary64 minimax reoptimization, adding this Arb-certified generator to the 151-column active pool, is running; any sub-\(1/3\) candidate would still require exact rationalization and a fresh Arb audit.


## 152-column exact candidate: all 1,779 pinned rows Arb-certified (2026-11-23)

The Arb-certified continuous-path escape was added to the 151-column active pool. The 152-column binary64 HiGHS LP gave objective \(0.329769894504226\), recomputed maximum \(0.329769894504254\), support 51, escape weight \(4.7680963914\times10^{-5}\), and primal-dual gap \(2.55\times10^{-15}\). The 51 positive weights were converted to exact rational probabilities summing to one.

Workflow [45046016471](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45046016471) then used 128-bit Arb to certify all 1,779 rows. The complete second/fourth block (1,461 rows), 311 selected sixth-order rows, and seven selected eighth-order rows all satisfy the strict \(1/3\) cap. The maximum absolute-error upper endpoint is enclosed by
\[
[0.32976989450473041482078054778650805091\pm3.67\times10^{-40}],
\]
giving a certified margin to \(1/3\) of
\[
[0.00356343882860291851255278554682528242\pm3.46\times10^{-39}].
\]
Evidence: evidence/candidate_152col_selected_rows_arb_n21.json; exact input: evidence/candidate_joint_input_152col_continuous_escape_n21.json; LP: evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json; verifier: verify_152col_continuous_escape_candidate_arb.py; commit [55ec898](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/55ec8985979af1563022d4f6e5ce1404d4b3148b).

This is a strict exact-probability result on the pinned 1,779 rows, not a complete sixth/eighth-order orbit certificate: only 311 of 63,133 sixth orbits and seven selected eighth orbits were checked. It also does not imply full continuous-family optimality or an operational Choi/diamond-norm bound. The next task is a complete sixth-order audit of this exact mixture.


## 152-column candidate fails the complete sixth-order domain (2026-11-23)

The exact 51-support rational candidate that passes the pinned 1,779-row Arb audit is **not** a complete sixth-order witness. The complete binary64 screen covers all 63,133 dihedral orbits / 5,245,786 six-subsets and finds 334 orbits with normalized absolute residual at least 1/3. The largest screen residual is 0.8390979517059564 at orbit representative (0,1,8,18,25,35), orbit index 30,283 (orbit size 42).

This worst row has been independently recomputed using 128-bit Arb, the exact rational candidate probabilities, and exact rational path couplings. The normalized absolute residual is enclosed by

\[
[0.839097951705338056452886319837567\pm2.78\times10^{-34}]>\frac13.
\]

Therefore the candidate's rigorous scope remains exactly the pinned 1,779 rows (1,461 complete second/fourth, 311 selected sixth, and seven selected eighth rows); it must not be described as satisfying all sixth-order constraints.

Evidence:
- Full binary64 scan: `evidence/candidate_152col_complete_sixth_binary64_n21.json`
- Strict one-row counterexample: `evidence/candidate_152col_sixth_counterexample_arb_n21.json`
- Verifier: `verify_152col_sixth_counterexample_arb.py`
- Arb workflow: [45056852005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45056852005)
- Strict counterexample verifier commit: [5f2ca63](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5f2ca63d07ab12ff48659b4491c0dc8015fc4ace)

A cutting-plane workflow now persists all 334 violating orbit representatives, deduplicates them against the original 311 sixth rows, and reoptimizes the same 152 physical generators. This is a finite discovery LP; any resulting candidate needs exact-probability Arb verification and another complete-sixth scan. Workflow: [45057108860](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45057108860); implementation commit: [074ac3b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/074ac3bdd4c45044ed86482f658338738c0f4a25).

The counterexample is candidate-specific. It does not prove infeasibility for other mixtures or for the full continuous physical family.


## Cutting-plane discovery: the same 152-column pool cannot repair the observed sixth failures (2026-11-23)

All 334 sixth-order orbits that violated the previous exact candidate were added as distinct rows; none overlapped the original 311 selected sixth rows. Reoptimization over the same 152 physical generators therefore has 2,113 rows:
- 1,461 complete second-/fourth-order rows;
- 645 sixth-order rows (311 original + 334 new cuts);
- seven selected eighth-order rows.

The binary64 HiGHS LP returns objective 0.5078909209101226 and independently recomputed maximum 0.5078909209177525, with primal-dual discovery gap 1.99e-14. Thus this fixed 152-column pool does not repair the complete-sixth failures by reweighting alone. This is still a numerical discovery result until the rationalized dual is Arb-certified.

Evidence: `evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json`; complete scan with all 334 rows: `evidence/candidate_152col_complete_sixth_binary64_n21.json`; cutting-plane run: [45057108860](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45057108860); implementation commit: [074ac3b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/074ac3bdd4c45044ed86482f658338738c0f4a25).

The follow-up has now stored the full HiGHS dual and independently certified its rationalization with 128-bit Arb on all 152 columns. The exact finite-pool lower bound and its scope are recorded in THEORY_152COL_2113ROW_MINIMAX_OBSTRUCTION.md.


## Strict 152-column / 2,113-row minimax obstruction (2026-11-23)

The cutting-plane LP's rationalized dual is now a complete 128-bit Arb certificate. The exact dual has \(\|z\|_1=36893488147393554485/36893488147419103232<1\), uses only 40 nonzero coordinates (one low-order, 37 sixth-order, two eighth-order), and passes all 152 physical-column inequalities. With slack \(\delta=10^{-9}\), the strict lower bound is
\[
\eta_{152,2113}\ge
\frac{36597397722434817858556439}{72057594037927936000000000}
=0.5078909199101425\ldots>\frac13.
\]
The exact gap above \(1/3\) is \(0.17455758657680914\ldots\); the maximum Arb upper endpoint of the column inequalities after slack is \(-7.9784600657124487\times10^{-10}\).

This proves that **no probability reweighting of these fixed 152 generators** can satisfy even the 2,113-row subset, and therefore cannot satisfy the complete sixth-order objective on that same fixed pool. It does not rule out adding further physical generators or the unrestricted continuous family.

Evidence:
- Strict certificate: evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json
- LP transcript with dual multipliers: evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json
- Arb verifier: verify_152col_full_sixth_cut_dual.py
- Successful conflict-safe workflow: [45058397922](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45058397922)
- Certificate commit: [d27ff52](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d27ff52bd8c21315e4534fd56bf5942630cc3c73)


## 152-column full-sixth dual pricing: canonical escapes and next reoptimization (2026-11-23)

The complete-sixth cutting-plane design adds all 334 sixth-order orbits found violating the earlier 152-column candidate, giving 2,113 rows (1,461 complete second/fourth, 645 sixth, seven selected eighth). A rationalized 128-bit Arb dual proves the fixed 152-generator pool has minimax error at least
\[
\eta_{152,2113}\ge
\frac{36597397722434817858556439}{72057594037927936000000000}
=0.5078909199101425\ldots>\frac13.
\]
This is a finite-pool theorem only; it does not rule out additional physical generators.

A pricing pass screened all 1,490 canonical generators unused by the 151 canonical members of that pool. The binary64 screen found 37 positive reduced-cost candidates. The ten highest were independently recomputed with 128-bit Arb, and all ten pricing intervals have strictly positive lower endpoints. Their canonical indices are 1603, 886, 565, 682, 472, 525, 434, 487, 80, and 145. The largest is column 1603, with pricing score
\[
[27.859490176389019929457002890028332\pm8.38\times10^{-34}]>0.
\]
Thus the 152-column dual is not a separator for the full frozen 1,641-column canonical pool. This does not imply that the larger pool is feasible.

Evidence:
- Strict 152-column / 2,113-row theorem: THEORY_152COL_2113ROW_MINIMAX_OBSTRUCTION.md.
- Exact dual certificate: evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json.
- Full binary64 pricing screen: evidence/55probe_152col_full_sixth_cut_dual_pricing_screen_n21.json.
- Ten strict Arb pricing checks: evidence/55probe_152col_full_sixth_cut_dual_pricing_arb_n21.json.
- Pricing implementation/workflow: price_unused_columns_against_152col_full_sixth_cut_dual.py, verify_152col_full_sixth_cut_dual_pricing_arb.py, .github/workflows/eui-152col-full-sixth-cut-pricing.yml.
- Evidence commit: [0507386](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/05073862b9763aaf8a70292845ee1717cbc6cff0).

A new 162-column discovery LP has been added. It augments the 152-column cut pool with those ten Arb-positive canonical columns while preserving the same 2,113-row design. The script checks the hashes linking the candidate, parent cut LP, strict dual, pricing screen, Arb pricing transcript, and frozen canonical pool before constructing the matrix. The push-triggered workflow is .github/workflows/eui-162col-full-sixth-cut-pool.yml; it writes evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json and, only if the numerical objective is below 1/3, a rationalized candidate file. The LP result is pending at this audit revision and will be treated as discovery only. Any candidate requires a fresh exact-probability Arb audit and a complete 63,133-orbit sixth-order separation scan.

Implementation:
- reoptimize_162col_full_sixth_cut_pool.py
- .github/workflows/eui-162col-full-sixth-cut-pool.yml
- commits [7a3e35c](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/7a3e35c9dbc397b850f1de3fe2a0e7eca023ce49), [53eb0f1](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/53eb0f1679e77054b6f9804678e5705882a7e750), and [01b3c51](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/01b3c5170801d3e611081e07a6e1e162946cfc4e).


## Strict 162-column full-sixth cut obstruction (2026-11-23)

The 162-column discovery LP adds ten canonical generators whose reduced-cost scores against the preceding 152-column dual were independently Arb-certified positive. On the same 2,113-row design, the binary64 HiGHS objective is 0.4931412761911509 and the independently recomputed maximum is 0.49314127619252646. The raw floating dual has L1 norm slightly above one, so it was rationalized and scaled before certification.

The resulting exact rational dual has \(\|z\|_1=1\), slack \(\delta=10^{-10}\), and all 162 column inequalities pass 128-bit Arb. It proves
\[
\eta_{162,2113}\ge
\frac{1421382955036825653848272131}
{2882303761517278690000000000}
=0.493141276091106\ldots>\frac13.
\]
The exact gap above \(1/3\) is
\[
\frac{1381845103593198271544816393}
{8646911284551836070000000000}
=0.15980794275777266\ldots.
\]
The maximum Arb upper endpoint of the column inequalities after slack is \(-7.5752412530783022251271948310938060\times10^{-11}\).

This is a strict finite-pool theorem for the 162 fixed generators and the 2,113 pinned rows (1,461 complete second/fourth, 645 sixth, seven selected eighth). It excludes a complete-sixth cap for that same fixed pool because the full sixth-order maximum contains the 645 certified rows. It does not exclude adding further generators or the unrestricted continuous family.

Evidence:
- LP transcript: evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json.
- Exact Arb certificate: evidence/55probe_162col_full_sixth_cut_dual_certificate_n21.json.
- Verifier: verify_162col_full_sixth_cut_dual_arb.py.
- Workflow: [45059945749](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45059945749).
- Certificate commit: [4d382ab](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4d382ab33e52d4785e314a088402cccffc9a0ed6).

The next column-generation pass prices the 1,480 canonical generators unused by the 161 canonical members of the 162-column pool. Its binary64 screen and ten-candidate Arb verification are defined in price_unused_canonical_paths_against_162col_dual.py and verify_162col_full_sixth_cut_dual_pricing_arb.py, with workflow .github/workflows/eui-162col-full-sixth-cut-pricing.yml. Workflow [45060141610](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45060141610) is queued at this audit revision; no pricing outcome is claimed yet.


## Important scope correction and sixth-only separation (2026-11-23)

An audit of the nonzero dual coordinates found that the 2,113-row LPs contain seven selected eighth-order rows and both the 152-column and 162-column duals have two nonzero eighth-order coordinates. Therefore their Arb lower bounds are valid for the pinned **mixed-order** row sets only. They do not, by themselves, prove a sixth-only lower bound after deleting the eighth-order rows. Any earlier wording that inferred a sixth-only no-go directly from those mixed-order certificates is withdrawn.

The 152-column certificate was rerun after the verifier scope correction. Its current exact lower bound is
\[
\frac{31229779445108377178763165603}
{61489146912368343970000000000}
=0.5078909208094186\ldots,
\]
with exact dual L1 norm 1, slack \(10^{-10}\), and maximum Arb upper endpoint \(-4.2492156984681046212238277835698169369\times10^{-11}\). Its dual support is one low-order, 37 sixth-order, and two eighth-order coordinates. The corrected theorem is THEORY_152COL_2113ROW_MINIMAX_OBSTRUCTION.md.

The 162-column mixed-order certificate is separately documented in THEORY_162COL_2113ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md. It proves the 2,113-row mixed-order lower bound 0.493141276091106..., with 38 sixth-order and two eighth-order active coordinates. It is not a sixth-only certificate.

To answer the sixth-only question, a new LP was solved with no eighth-order rows: 1,461 complete second/fourth rows plus 645 sixth-order rows, total 2,106. The 162-column binary64 objective is 0.47605818509327597, independently recomputed maximum 0.47605818509336406, support 45, and primal-dual discovery gap \(6.11\times10^{-16}\). This is still discovery only because the floating dual L1 norm is slightly above one; exact rationalization and 128-bit Arb checks against all 162 columns are underway. If that certificate passes, its lower bound extends to the complete sixth-order objective for the fixed 162-column pool, because all 645 sixth rows are members of the full 63,133-orbit domain.

Evidence:
- Sixth-only LP: evidence/joint_low_six_lp_162col_sixth_only_n21.json.
- Sixth-only Arb verifier: verify_162col_sixth_only_dual_arb.py.
- Workflow: [45061253393](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45061253393).
- Scope correction comment: [Issue #5 comment](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/5#issuecomment-7084339758).

A first pricing pass against the 162-column mixed-order dual found 12 binary64-positive unused canonical columns and 10/10 top candidates passed Arb with strictly positive lower endpoints (indices 1580, 195, 364, 424, 448, 221, 324, 517, 420, 447). The dual certificate was subsequently regenerated with refreshed parent-row provenance, so a hash-consistent pricing rerun is in progress before these candidates are used for further reoptimization.


## Strict sixth-only 162-column theorem (2026-11-23)

The 2,106-row sixth-only LP has now passed an independent 128-bit Arb dual audit. Unlike the mixed-order 2,113-row certificate, this design contains no eighth-order rows. The rational dual has exact L1 norm 1 and support on exactly 45 sixth-order rows; all 1,461 low-order coordinates are zero. All 162 physical-column inequalities have strictly negative Arb upper endpoints after slack \(10^{-10}\).

The resulting exact bound is
\[
\eta^{(6)}_{162}\ge
\frac{10977154378457033940786269263}
{23058430092137307370000000000}
=0.47605818499326774\ldots>\frac13,
\]
with exact gap
\[
\frac{9873033043233794452358807789}
{69175290276411922110000000000}
=0.1427248516599344\ldots.
\]
The largest Arb upper endpoint after slack is \(-9.4121757377289108485479722255741978272\times10^{-11}\).

This does imply a complete-sixth-order lower bound for this fixed 162-generator pool: the dual is supported only on 45 sixth-order rows, and each is one of the 63,133 \(D_{42}\) sixth-order orbits. Thus the full sixth-order maximum is at least the certified restricted maximum. It remains a finite-pool theorem and does not exclude additional physical generators.

Evidence:
- Formal theorem: THEORY_162COL_2106ROW_SIXTH_ONLY_MINIMAX_OBSTRUCTION.md.
- LP: evidence/joint_low_six_lp_162col_sixth_only_n21.json.
- Exact certificate: evidence/55probe_162col_sixth_only_dual_certificate_n21.json.
- Verifier: verify_162col_sixth_only_dual_arb.py.
- Workflow: [45061253393](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45061253393).
- Certificate commit: [e23dc0b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e23dc0bb776e6a1304258bd39eba664f35afe8ab).

The next column-generation task is to price the remaining canonical generators against this sixth-only dual itself. The earlier 10/10 Arb-positive candidates were priced against the mixed-order 162-column dual and cannot be assumed to escape the sixth-only separator.

## 2026-11-23: sixth-only theorem and pricing status

The current strongest finite-pool result is the 162-generator sixth-only minimax obstruction. Its 2,106-row design has 1,461 complete second/fourth rows and 645 sixth-order rows, with no eighth-order rows. The exact rational dual has L1 norm one and support on 45 sixth-order coordinates only. All 162 physical-column inequalities passed 128-bit Arb. It proves
\[
\eta^{(6)}_{162}\ge
\frac{10977154378457033940786269263}
{23058430092137307370000000000}
=0.47605818499326774\ldots>\frac13.
\]
Because its dual support lies inside the complete 63,133-orbit sixth-order domain, the bound applies to the complete sixth-order worst-row objective for mixtures over this fixed 162-generator pool. It does not exclude additional generators or the unrestricted continuous family.

Evidence: `THEORY_162COL_2106ROW_SIXTH_ONLY_MINIMAX_OBSTRUCTION.md`, `evidence/55probe_162col_sixth_only_dual_certificate_n21.json`, verifier `verify_162col_sixth_only_dual_arb.py`, successful workflow [45061253393](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45061253393), certificate commit [e23dc0b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e23dc0bb776e6a1304258bd39eba664f35afe8ab).

The 152-column exact candidate previously passed only the pinned 1,779 rows; a complete binary64 sixth scan found 334 violations, one independently Arb-certified. The 2,113-row mixed-order dual was not used as a sixth-only proof: a separate LP removed all eighth-order rows before the 162-column sixth-only certificate was built.

The next finite-family task prices the 1,480 unused canonical paths against this sixth-only dual. The new workflow runs the binary64 screen and then independently Arb-checks up to ten highest positive candidates. Positive Arb pricing disproves this separator after adding that candidate. A negative screen or ten nonpositive Arb checks is not a certificate for all unused columns; that would require strict interval checks for every remaining column.

No TeX/Bib/PDF or standalone supplementary-source files are tracked in the repository, so this audit updates the claim/evidence record rather than the original manuscript. Average Choi-fidelity numerics still do not establish a uniform worst-case channel guarantee; the per-instance moment-to-Choi/diamond bridge remains open.


## 2026-11-23: sixth-only 162-column pricing against the frozen canonical pool

The exact 162-column sixth-only dual has now been priced against every one of the 1,480 canonical path generators not already in its physical support. The full binary64 screen found 25 positive reduced-cost scores. The ten highest were independently recomputed from the frozen binary64 couplings interpreted exactly as dyadic rationals, using 128-bit Arb matrix exponentials and principal-minor orbit averages. All ten Arb lower endpoints are strictly positive:

| Canonical column | Arb pricing score midpoint |
|---:|---:|
| 1613 | 6.800109240178720982... |
| 1412 | 4.900651392507548628... |
| 1383 | 4.147358130490488789... |
| 1580 | 0.294471056024061802... |
| 195 | 0.160156078539728071... |
| 221 | 0.123619341765576163... |
| 424 | 0.114060272590299884... |
| 655 | 0.106036955038113731... |
| 614 | 0.098512182916499572... |
| 635 | 0.091871580178178877... |

This rigorously establishes that the particular 162-column sixth-only dual is not a separator for any expanded pool containing one of these ten canonical columns. It does not prove that the expanded pool is feasible or that a new mixture meets the (1/3) cap.

Evidence:
- Successful full pricing + Arb workflow: [45067579358](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45067579358).
- Binary64 screen: `evidence/55probe_162col_sixth_only_dual_pricing_screen_n21.json`.
- Strict Arb transcript: `evidence/55probe_162col_sixth_only_dual_pricing_arb_n21.json`.
- Evidence commit: [80f140e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/80f140e4f9a4a50702a39fd0cd0f3bb595931661).
- The pricing verifier first re-runs the exact 162-column sixth-only dual certificate, then checks the top ten candidates from the frozen pool.

A new 172-column sixth-only reoptimization was implemented in `reoptimize_172col_sixth_only_pool.py` with workflow `.github/workflows/eui-172col-sixth-only-pool.yml`. It combines the 162-column physical pool with these ten strictly Arb-positive canonical columns and keeps the same 2,106-row design (1,461 complete second/fourth rows plus 645 sixth-order rows). Its provenance guards now bind the continuous path through the exact Arb escape certificate and bind the sixth-row inventory through the parent LP's canonical row hash. Workflow [45067985228](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45067985228) is executing the reoptimization; no 172-column objective or candidate is claimed until that run completes.

The exact 162-column lower bound remains a fixed-pool theorem:
```
eta_162^(6) >= 0.47605818499326774... > 1/3.
```
It does not exclude the ten new columns, any larger pool, or the unrestricted continuous path family.


## 172-column complete-sixth-order minimax obstruction (2026-11-23)

The ten Arb-positive canonical columns found against the 162-column sixth-only dual were added to the 162-column physical pool. The resulting 172-column, 2,106-row binary64 HiGHS LP has objective `0.4705549863247866`, independently recomputed maximum `0.4705549863248868`, 50 positive weights, and primal-dual discovery gap `1.23e-14`. It does not produce a sub-`1/3` candidate. Transcript: `evidence/joint_low_six_lp_172col_sixth_only_n21.json`; reoptimization workflow: [45067985228](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45067985228).

The rationalized dual was then independently certified with 128-bit Arb against all 172 physical columns in [workflow 45068269670](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45068269670). The exact certificate proves
[
min_{pinDelta(mathcal P_{172})}
max_{Iininom{[42]}6/D_{42}} |e_I(p)|
ge
rac{1324494537887082708836219}
{2814749767106560000000000}
=0.4705549862247987ldots>rac13.
]
The exact dual has
[
|z|_1=rac{288230376151706861}{288230376151711744}<1,
quad
lambda=rac{413924430527507}{281474976710656},
quad
delta=10^{-10}.
]
Its support contains exactly 50 sixth-order rows and no low-order rows. All 172 column inequalities have strictly negative Arb upper endpoints; the largest is below `-7.6774063738680112e-11`. This is a rigorous complete-sixth-order lower bound for the fixed 172-generator pool, not a bound over all physical generators. Formal statement and proof: `THEORY_172COL_2106ROW_SIXTH_ONLY_MINIMAX_OBSTRUCTION.md`; certificate: `evidence/55probe_172col_sixth_only_dual_certificate_n21.json`; commit [288a253](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/288a2534356453e5c05e5b64a9ba4aaaabe9eb26).

The next pricing stage now screens the remaining 1,470 canonical generators against this new 172-column dual and independently Arb-checks the ten highest positive candidates. Workflow [45068411039](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45068411039) is in progress; no result is claimed yet.


## Pricing the 172-column dual against the remaining canonical pool (2026-11-23)

The exact 172-column sixth-only dual was used to screen all 1,470 canonical generators not already in its physical pool. The binary64 screen found 14 positive scores; the ten highest were independently checked with 128-bit Arb and all ten had strictly positive interval lower endpoints: columns 544, 420, 398, 352, 629, 668, 347, 425, 296, and 844. The largest Arb score is `0.1347370117915883944...` (column 544). This invalidates the 172-column separator for an expanded pool containing any of these columns, but does not imply feasibility. Workflow [45068411039](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45068411039) completed successfully; evidence is in `evidence/55probe_172col_sixth_only_dual_pricing_screen_n21.json` and `evidence/55probe_172col_sixth_only_dual_pricing_arb_n21.json`; commit [517df1b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/517df1bd3c95da7ba81a3529d2edeae3576f2977).

The next step is a 182-column reoptimization on the same 2,106 rows. Until that LP and any new Arb certificate complete, no 182-column minimax value is claimed.


## 182-column sixth-only reoptimization (2026-11-23)

The 172-column sixth-only dual pricing found ten additional canonical path generators with strictly positive 128-bit Arb reduced-cost intervals. Adding them gives a 182-column physical pool and the same pinned 2,106-row discovery design (all 1,461 second-/fourth-order rows plus 645 selected sixth-order rows).

The binary64 HiGHS run completed successfully in workflow [45068718407](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45068718407) and returned:
- objective: 0.4681273410033708;
- independently recomputed maximum: 0.4681273410033828;
- complete low-order block maximum: 0.46812734100337106;
- selected-sixth block maximum: 0.4681273410033828;
- positive primal support: 52;
- binary64 primal-dual discovery gap: 2.83e-15.

The objective is well above 1/3, so this finite LP produced no admissible candidate. The raw binary64 dual L1 norm is 1.0000000000000018; it is therefore not itself a certificate. A new exact-rational/128-bit Arb verifier and workflow have been added:
- `verify_182col_sixth_only_dual_arb.py`;
- `.github/workflows/eui-182col-sixth-only-dual.yml`.

The verifier reconstructs the exact target vector and pinned row/column inventory, rationalizes and scales the dual to enforce the exact L1 constraint, classifies the actual dual support as sixth-only or mixed-order, and independently evaluates all 182 column inequalities with Arb. The current binary64 dual has two nonzero low-order coordinates (row indices 233 and 1265) and 50 sixth-order coordinates, so the expected certificate scope is mixed-order unless exact reconstruction changes that support. The script emits a sixth-only status only when all low-order coordinates vanish. The strict certificate is not claimed until the workflow writes `evidence/55probe_182col_sixth_only_dual_certificate_n21.json`.

The finite-pool scope remains explicit: even a successful 182-column certificate excludes only mixtures over those 182 generators. It does not cover the remaining canonical columns or the full continuous path family.

## 182-column mixed-order Arb certificate completed (2026-11-23)

The corrected 182-column verifier completed and the workflow committed the exact certificate in commit [be82f21777e8ae1714fc4c488528a5374e50d942](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/be82f21777e8ae1714fc4c488528a5374e50d942).

The certificate has:
- 182 physical columns and 2,106 normalized rows;
- exact dual (\|z\|_1=1);
- 52 active dual coordinates: two low-order rows (zero-based indices 233 and 1265) and fifty sixth-order rows;
- exact slack (\delta=10^{-10});
- 128-bit Arb verification of all 182 column inequalities, with maximum upper endpoint (-7.9382193303777883\times10^{-11}).

It proves the finite-pool mixed-order lower bound
\[
\min_{p\in\Delta(\mathcal P_{182})}\|Ap-y\|_\infty
\ge
\frac{1727085050310122398125808297}
{3689348814741917030000000000}
=0.468127340903367\ldots>\frac13.
\]

The exact theorem is recorded in `THEORY_182COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md`; the certificate is `evidence/55probe_182col_sixth_only_dual_certificate_n21.json`. Despite the historical filename containing “sixth_only”, the actual dual is **mixed-order**, not sixth-only. The separate 172-column sixth-only theorem remains the complete-sixth-order result. This 182-column theorem is restricted to the pinned 182-generator pool and 2,106-row design; it does not exclude further physical generators or the unrestricted continuous path family, and it is not an operational channel-distance theorem.

A follow-up column-generation pipeline has been committed for the certified 182-column mixed-order dual. It computes binary64 pricing scores for all 1,460 unused canonical generators using both active low-order coordinates and the fifty active sixth-order coordinates, then recomputes up to ten leading positive candidates with 128-bit Arb. The workflow first reruns the strict 182-column certificate. This is only a screening pipeline until its evidence files are committed; no result from the new pricing run is claimed here.

## 182-column mixed-order pricing completed (2026-11-23)

Workflow [45079216515](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45079216515) completed successfully. The binary64 screen evaluated all 1,460 canonical generators unused by the 182-column pool and found three positive scores. All three were independently recomputed with 128-bit Arb and have strictly positive lower endpoints:

- column 364: 0.07617160777215499539475007470184446;
- column 517: 0.01524906166078186493793878441349329;
- column 430: 0.01482828386245658833675467450664665.

Evidence is in `evidence/55probe_182col_mixed_order_dual_pricing_screen_n21.json` and `evidence/55probe_182col_mixed_order_dual_pricing_arb_n21.json`. These are strict escapes of the 182-column dual, not a feasible mixture. The remaining 1,457 nonpositive binary64 scores are not individual Arb exclusion certificates.

A 185-column mixed-order reoptimization script and workflow have been committed; run [45079471124](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45079471124) was queued at the time of this audit update. Its objective and any resulting certificate remain pending.

The first 185-column workflow attempt [45079471124](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45079471124) completed the 182-column certificate recheck, full 1,460-column binary64 screen, and all three Arb-positive candidate checks, but failed before LP construction because the reoptimizer omitted the parent 172-column dual file from its SHA256 manifest. The manifest and both hash references were corrected in commit [0e33549](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/0e3354906354c79063c410d8972689cb7c92e41d). The corrected rerun is [45079631845](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45079631845); its LP result is pending.

The corrected run [45079631845](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45079631845) has passed the seed/orbit checks, exact 182-column Arb re-verification, fresh full canonical pricing screen, and all three Arb-positive candidate checks. At the time of this update it is executing the 185-column HiGHS reoptimization; no 185-column objective is asserted yet.


## 185-column mixed-order LP discovery and certificate status (2026-11-23)

The corrected 185-column reoptimization completed in workflow [45079631845](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45079631845). Its frozen binary64 transcript is `evidence/joint_low_six_lp_185col_mixed_order_n21.json` (blob SHA `3bc008cfbccee709a8b36e16421a5459d7470c7c`). The 2,106-row HiGHS discovery returned objective 0.4671511510648626, independently recomputed maximum 0.4671511510651767, dual discovery objective 0.46715115106485405, and binary64 primal-dual gap 8.55e-15. The raw dual has 56 nonzero row coordinates (two low-order and 54 sixth-order); its raw L1 norm is 1.0000000000000444.

These values are discovery only. The raw binary64 dual is not a proof. A new independent verifier rationalizes the 2,106 dual coordinates exactly, enforces exact L1 norm at most one, reconstructs the physical inventory and target vector from hash-pinned inputs, and uses 128-bit Arb to check every one of the 185 physical-column inequalities. The new workflow re-runs the parent 182-column Arb certificate and all three strict Arb-positive pricing escapes before the 185-column check.

- Verifier: `verify_185col_mixed_order_dual_arb.py`.
- Workflow: `.github/workflows/eui-185col-mixed-order-dual.yml`.
- Workflow definition commit: [0eed12f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/0eed12f1fd867cd5c590742359debed2ce39373f).
- Verifier commit: [f42bcb7](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f42bcb7a1e946cfc5a99f98c01f67dfd5b3d2991).

**No 185-column strict lower bound is claimed yet.** The claim becomes a theorem only if the new exact rational dual has objective above 1/3 and all 185 Arb interval inequalities pass after the chosen rational slack. If the verifier fails, its exact failure and interval diagnostics must be retained and the dual reconstruction repaired before making any claim.

The 185-column result remains restricted to the pinned 2,106-row design and fixed physical pool. It does not cover additional canonical or continuous generators, the complete sixth-order orbit maximum, or an operational Choi/diamond-norm guarantee.



## 185-column mixed-order Arb certificate completed (2026-11-23)

The corrected verifier completed successfully in [workflow 45090564147](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45090564147), and GitHub Actions committed the theorem and certificate in [ae4ee17](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/ae4ee17bebc6781a5cc2896af2f0e0e48eeb8206).

The exact certificate establishes
\[
\min_{p\in\Delta(\mathcal P_{185})}\|Ap-y\|_\infty
\ge
\frac{86174177255875174056289633093}
{184467440737103669070000000000}
=0.4671511509648334\ldots>\frac13.
\]
The exact dual objective before slack is
\[
\lambda+z^\mathsf Ty=
\frac{8617417727432191813}{18446744073710366907},
\]
with exact \(\|z\|_1=1\), rational slack \(\delta=10^{-10}\), and certified excess over 1/3 equal to
\[
\frac{24685030343507284366289633093}
{184467440737103669070000000000}
=0.1338178176315001\ldots.
\]

The support has 56 coordinates: two low-order coordinates (zero-based row indices 233 and 1265) and 54 sixth-order coordinates. Independent 128-bit Arb evaluation passed all 185 physical-column inequalities; the maximum upper endpoint after slack is
\[
-7.6726289625084981342508868442503571950\times10^{-11}<0.
\]
This is a **mixed-order finite-pool theorem**, not a sixth-only theorem. It applies to the specified 185 generators and the pinned 2,106-row design. It does not exclude additional physical generators, the unrestricted continuous path family, or establish a Choi/diamond-norm guarantee.

The verifier and workflow are `verify_185col_mixed_order_dual_arb.py` and `.github/workflows/eui-185col-mixed-order-dual.yml`; the exact certificate is `evidence/55probe_185col_mixed_order_dual_certificate_n21.json`; the theorem is `THEORY_185COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md`.

The first workflow attempt (45090111228) was a file-ordering race: the workflow commit preceded the verifier file. The second (45090256555) exposed an invalid redundant 172-dual hash assertion. The assertion was removed in [58b6def](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/58b6def296681c5d3baf7e81418ff62c3101f6ab); the corrected run passed. Both failures and their causes are recorded in Issue #5.

A new combined pricing script and workflow now screen all 1,457 unused canonical generators and Arb-check up to ten leading positive candidates against the exact 185-column dual:
- `price_unused_canonical_paths_against_185col_mixed_order_dual.py`;
- `.github/workflows/eui-185col-mixed-order-pricing.yml`;
- current run [45090786248](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45090786248).

At this audit update the 185-column pricing run is in progress; no 185-dual escape or global finite-canonical-pool conclusion is claimed yet.



## 185-column dual pricing and 186-column reoptimization (2026-11-23)

Workflow [45090786248](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45090786248) completed the binary64 screen over all 1,457 canonical generators unused by the 185-column pool. Exactly one candidate had a positive binary64 score: canonical column 447, with score 0.01298752982693295. Its independent 128-bit Arb interval is
\[
[0.01298752982275180001179405643483\pm4.09\times10^{-33}],
\]
with strict lower endpoint
\[
[0.012987529822751800011794056434832732053\pm1.67\times10^{-40}]>0.
\]
This strictly escapes the 185-column dual after adding column 447. It does not prove feasibility or exclude any continuous-path generator. The screen and Arb files were committed in [1e0930d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1e0930d9283e437421e779af0a18543f1f2482a3).

The combined pricing script now explicitly records the SHA256 of its binary64 screen in the Arb transcript (commit [7f47871](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/7f47871a605939ab75d6ae0211d2b95f9872fb88)); corrected provenance rerun [45091164802](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45091164802) is running.

The 186-column reoptimizer and workflow are committed in [1a3cb42](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1a3cb42d259ba060175d1b03955bcbc67491e361), [b1cc491](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b1cc491343e2e866a7b6adf2cdba1943b9cb6840), and [a3f4147](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/a3f4147c3b6c91fe3a20737ba62e5f197e8b1f55). Run [45091230819](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45091230819) has passed seed/orbit checks and the exact 185-column Arb certificate, and is currently repeating full pricing before the 186-column LP. No 186-column objective is asserted yet.



## Pricing provenance correction and 186-column LP status (2026-11-23)

The corrected 185-column pricing provenance rerun [45091164802](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45091164802) completed successfully. The Arb transcript now records `pricing_screen_sha256`, and the 185-column Arb verifier's stored certificate hash and LP hash agree with the exact committed inputs. The only strict-positive canonical escape remains column 447; the other 1,456 nonpositive binary64 scores are not strict Arb exclusion certificates.

The first 186-column workflow [45091230819](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45091230819) reverified the 185-column theorem and repeated all pricing checks, but failed at the 186 reoptimizer's provenance guard because it expected the old pricing JSON keys. The current 185 pricing schema uses `certificate_sha256` and `lp_sha256`. The guard was corrected in [52f7b2b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/52f7b2b531dce1633128c7a30590e5e6573b2098).

Corrected run [45091326325](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45091326325) has passed frozen seed/orbit checks, exact 185-column Arb re-verification, full 1,457-column pricing, the strict Arb-positive check for column 447, and the complete provenance chain. It is currently executing the 186-column HiGHS matrix construction/LP. Its objective and transcript are not yet available, so no 186-column minimax value is claimed.


## 172-column full-sixth-cut mixed-order theorem (2026-11-23)

The 152-column candidate that passed its 1,779 selected-row Arb audit was rejected by the exhaustive binary64 sixth-order screen: 334 of the 63,133 D42 orbits crossed the 1/3 threshold, and a separate 128-bit Arb calculation certified a strict candidate-specific violation at representative (0,1,8,18,25,35). Adding all 334 newly identified representatives to the 152-column LP produced a 2,113-row design (1,461 low-order + 645 sixth + 7 selected eighth rows). The 152-column pool then received a strict finite-pool Arb dual obstruction. Its top ten positive canonical pricing candidates were all independently Arb-positive.

The 162-column reoptimization added those ten paths and produced a binary64 objective 0.4931412761911509. Its mixed-order dual was strictly certified, and pricing against the remaining 1,480 canonical paths produced ten further strictly Arb-positive escapes: 1580, 195, 364, 424, 448, 221, 324, 517, 420, 447.

The resulting 172-column LP has 2,113 rows and binary64 objective 0.4895870821848577 (recomputed maximum 0.4895870821886379; primal-dual discovery gap 2.85e-13). Its rationalized dual passed the independent 128-bit Arb check against all 172 physical columns in [workflow 45102666550](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45102666550). The exact theorem is

\[
\min_{p\in\Delta(\mathcal P_{172})}\|Ap-y\|_\infty
\ge
\frac{4409808392781637575337133}{9007199254740992000000000}
=0.489587081185143\ldots>\frac13.
\]

The exact dual L1 norm is 4611686018424741463 / 4611686018427387904 < 1, the pre-slack dual objective is 2257821901715884457 / 4611686018427387904, and the rational slack is 10^-9. All 172 slack-shifted column inequalities have Arb upper endpoints below zero; the maximum is -7.0535517948488008e-10. The dual support contains 48 coordinates: one fourth-order, 45 sixth-order, and two eighth-order rows. It is therefore a **mixed-order** obstruction, not a sixth-only theorem. It applies only to the specified 172-generator pool and pinned 2,113-row objective.

Formal statement: [THEORY_172COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_172COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md). Exact certificate: [55probe_172col_full_sixth_cut_dual_certificate_n21.json](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/55probe_172col_full_sixth_cut_dual_certificate_n21.json). LP transcript: [joint_low_six_eighth_lp_172col_full_sixth_cuts_n21.json](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/evidence/joint_low_six_eighth_lp_172col_full_sixth_cuts_n21.json). Certificate commit: [ae797e9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/ae797e92557df52f4f419e9215f9029ccbd1a450).

A new full-canonical pricing workflow against this exact 172-column dual is now running: [45103189029](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45103189029). It will screen all 1,470 unused canonical columns and apply 128-bit Arb to up to ten leading positive candidates. No 172-dual escape or finite-canonical-pool exclusion is claimed until that run completes.

### Separate 186-column mixed-order discovery

The 185-dual pricing escape (canonical column 447) was added in a separate 186-column, 2,106-row mixed-order branch. HiGHS returned objective 0.46714365173379313, recomputed maximum 0.4671436517368315, support size 57, and primal-dual discovery gap about 3.36e-14. This is **binary64 discovery only**; no 186-column Arb dual certificate was produced. Workflow [45091326325](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45091326325) failed only at the commit step because the workflow unconditionally staged a candidate file that correctly was not written (the LP was above 1/3). Its log/artifact records the discovery, but the transcript was not committed. This branch must not be conflated with the 172-column full-sixth-cut result above.


## 172-column full-canonical pricing and 182-column reoptimization (2026-11-23)

The previously pending pricing workflow [45103189029](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45103189029) completed successfully. It screened all 1,470 canonical columns unused by the 172-column pool. The binary64 screen's ten leading positive candidates were all independently certified strictly positive by 128-bit Arb:

| Canonical column | Arb interval lower endpoint (decimal prefix) |
|---:|---:|
| 61 | 0.094971255371117435851053050912804100161 |
| 352 | 0.082162433143692804154932815863527787006 |
| 629 | 0.060558969832182688689389546027074325733 |
| 93 | 0.048369660902845630571829819889328884328 |
| 728 | 0.048012261079486591388003765856988382992 |
| 620 | 0.033244789847951735773015296453756896077 |
| 78 | 0.024524006644280791019203829227312601884 |
| 398 | 0.013261356418032375891780988474268490026 |
| 233 | 0.0071350626704812797345796766306698389239 |
| 169 | 0.0011911701981955691906785174017499743409 |

The full Arb radii, exact couplings, screen hash, certificate hash, and LP hash are retained in:
- `evidence/55probe_172col_full_sixth_cut_dual_pricing_screen_n21.json`;
- `evidence/55probe_172col_full_sixth_cut_dual_pricing_arb_n21.json`.

These ten strictly positive reduced-cost values invalidate the 172-column dual after adding any listed column. The other 1,460 nonpositive binary64 scores are not strict Arb exclusion certificates; no all-canonical-pool separation is claimed.

The next 182-column pool is now defined by the 151 base canonical columns, one exact-rational continuous-path escape, the 20 canonical additions already present in the 172-column pool, and these ten newly priced columns. The reoptimizer and independent Arb dual verifier were added in commits [49ef1d0](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/49ef1d084d71f04016cd2b222e1bbf76ff532d2d) and [534e9d9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/534e9d9091ff955a17fc4a3c6e9d177aa39199cd); workflow configuration is [8a65a4e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8a65a4e6c034d080abfa4b357ddc65b2fee1e588). Workflow [45104071580](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104071580) has passed seed/orbit checks and re-certified the 172-column parent dual; at this audit update it is repeating the 1,470-column pricing and Arb checks before building the 182-column, 2,113-row LP. No 182-column objective is yet asserted.

This remains finite-pool, mixed-order evidence. It does not complete the 63,133-orbit sixth-order or 1,408,185-orbit eighth-order audit, does not establish an unrestricted continuous-family minimax theorem, and does not provide a Choi/diamond-norm operational guarantee.


**Inventory distinction.** The repository also contains a separate, already certified 182-column / 2,106-row mixed-order result in `THEORY_182COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md`. Its 182 physical columns are not the inventory being constructed here. The present branch is a distinct 182-column / 2,113-row full-sixth-cut reoptimization descended from the 172-column full-sixth-cut pool. The two 182-column labels must not be conflated or compared as if they shared the same matrix, row set, or physical generators.


## 182-column / 2,113-row full-sixth-cut mixed-order theorem completed (2026-11-23)

The 182-column reoptimization workflow [45104071580](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104071580) completed successfully. It re-certified the 172-column parent dual, repeated the complete 1,470-column binary64 pricing screen and ten Arb-positive checks, compiled the new programs, solved the expanded LP, and independently certified its rationalized dual against all 182 physical columns.

The 182-column HiGHS discovery has objective 0.48770695192985997, independently recomputed maximum 0.48770695192988267, support size 49, and primal-dual discovery gap 3.61e-15. The LP has 2,113 rows: 1,461 complete second/fourth rows, 645 pinned sixth rows, and seven selected eighth rows. No sub-1/3 candidate was produced; accordingly no candidate-input witness file was written.

The exact 128-bit Arb certificate proves
\[
\min_{p\in\Delta(\mathcal P_{182}^{\mathrm{cut}})}\|Ap-y\|_\infty
\ge
\frac{686386514539679318285297}{1407374883553280000000000}
=0.4877069518298635\ldots>\frac13.
\]
The exact dual has
\[
\|z\|_1=\frac{144115188075855847}{144115188075855872}<1,
\qquad
\lambda+z^\mathsf Ty=\frac{70285979103274681}{144115188075855872},
\qquad \delta=10^{-10}.
\]
Its 49 nonzero coordinates are two fourth-order rows (indices 233 and 868), 45 sixth-order rows, and two eighth-order rows; no second-order coordinate is active. All 182 slack-shifted physical-column inequalities have strictly negative Arb upper endpoints; the maximum is -7.6906378333341585e-11.

Formal proof: [THEORY_182COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_182COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md). Exact LP transcript: `evidence/joint_low_six_eighth_lp_182col_full_sixth_cuts_n21.json`. Exact certificate: `evidence/55probe_182col_full_sixth_cut_dual_certificate_n21.json`. Reoptimizer and verifier: `reoptimize_182col_full_sixth_cut_pool.py`, `verify_182col_full_sixth_cut_dual_arb.py`. Evidence commit: [fd37e03](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fd37e03eb67b8ca1a30512c5b5807120edf4862b); formal theorem commit: [caafed8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/caafed8bf44af34207a1b413cd179b89a16bc53e).

**Scope:** this is a mixed-order theorem for the specified 182 physical generators and pinned 2,113 rows. It is not sixth-only, not a complete sixth/eighth orbit audit, not a continuous-family no-go, and not an operational Choi/diamond-norm guarantee. The term “full-sixth-cut” denotes inclusion of all 334 cuts discovered in the earlier full binary64 scan; it does not denote Arb verification of all 63,133 sixth-order orbits.

**Inventory distinction:** this 182-column / 2,113-row branch is distinct from the already certified 182-column / 2,106-row mixed-order result in `THEORY_182COL_2106ROW_MIXED_ORDER_MINIMAX_OBSTRUCTION.md`. Their column inventories and row sets differ and their objectives must not be conflated.

The next action is to price the remaining 1,460 canonical columns against this exact 182-column dual, strictly verify positive candidates with Arb, and reoptimize the expanded pool.


The next pricing stage is now configured and queued in [workflow 45104568684](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104568684). It first reruns the exact 182-column Arb dual verifier, screens all 1,460 remaining canonical generators, then applies independent 128-bit Arb verification to up to ten leading positive candidates. The pricing evidence will be pinned to the exact 182-column certificate, LP transcript, 152-column cut-row inventory, and binary64 screen hash.


The first 182-column pricing attempt [45104568684](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104568684) re-certified the parent 182-column dual and compiled the pricing programs, but the binary64 pricing script stopped at a stale set-cardinality guard (it expected 171 distinct active canonical labels after separately checking 181 labels). The exact dual and its certificate were unaffected. The guard was corrected to 181 in [9501f17](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/9501f17b14fb19b24cce395486b06ef3394244fe); corrected workflow [45104635426](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104635426) is queued. No pricing conclusion is drawn from the failed attempt.


## 182-column full-sixth-cut dual pricing completed (2026-11-23)

Corrected pricing workflow [45104635426](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45104635426) completed successfully after fixing the stale distinct-count guard in [9501f17](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/9501f17b14fb19b24cce395486b06ef3394244fe). The workflow re-certified the 182-column / 2,113-row dual, screened all 1,460 unused canonical columns, and found exactly one binary64-positive candidate: canonical column 544, score 0.023498411984316764.

Independent 128-bit Arb evaluation gives
\[
[0.023498411983883277473391166582309888329\pm4.39\times10^{-40}],
\]
whose lower endpoint is strictly positive. Therefore column 544 escapes the 182-column dual after addition. The full screen and Arb transcript were committed in [5e799a3](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5e799a373bc11e82b87bf5d09680de6f7d67d122), in `evidence/55probe_182col_full_sixth_cut_dual_pricing_screen_n21.json` and `evidence/55probe_182col_full_sixth_cut_dual_pricing_arb_n21.json`.

The positive escape does not prove feasibility or exclude the other 1,459 nonpositive binary64 columns. Note that canonical column 544 is active in the separate 182-column / 2,106-row branch, but is unused in this 182-column / 2,113-row full-sixth-cut pool; the inventories differ.

The next pool expansion is the 183-column / 2,113-row full-sixth-cut reoptimization, with column 544 added.


The 183-column reoptimization has now been launched as [workflow 45105045420](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105045420). Its pool is exactly the 182-column / 2,113-row full-sixth-cut inventory plus canonical column 544, whose reduced-cost score was strictly positive by Arb. The workflow revalidates the 182-column parent certificate and pricing provenance before solving; no 183-column objective is asserted until it completes.


## 183-column / 2,113-row full-sixth-cut theorem completed (2026-11-23)

Workflow [45105045420](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105045420) completed successfully: the 182-column parent certificate was rechecked, the full canonical pool was repriced and column 544 was Arb-verified, the 183-column LP was solved, and the new dual was independently certified against all 183 physical columns.

The 183-column HiGHS objective is 0.48761965408631913; the recomputed maximum is 0.48761965409086705; the primal-dual discovery gap is 3.40e-13. The LP has 2,113 rows (1,461 complete low-order, 645 pinned sixth-order, seven selected eighth-order) and a 50-coordinate dual support.

The exact 128-bit Arb certificate proves
\[
\min_{p\in\Delta(\mathcal P_{183}^{\mathrm{cut}})}\|Ap-y\|_\infty
\ge
\frac{22487487405975385031571661473}
{46116860184283385270000000000}
=0.48761965398587814\ldots>\frac13.
\]
The exact dual has \(\|z\|_1=1\), \(\lambda+z^\mathsf Ty=2248748741058707105/4611686018428338527\), and \(\delta=10^{-10}\). Its support comprises two fourth-order rows (233, 868), 46 sixth-order rows, and two eighth-order rows (2106, 2107), with no second-order support. All 183 slack-shifted column inequalities have strictly negative Arb upper endpoints; the maximum is -2.7990374260551989e-11.

Formal proof: [THEORY_183COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_183COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md). LP transcript and exact certificate are `evidence/joint_low_six_eighth_lp_183col_full_sixth_cuts_n21.json` and `evidence/55probe_183col_full_sixth_cut_dual_certificate_n21.json`. Evidence commit [b551f64](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b551f64603bb071aed303f5a2f879e53c61d4de9); theorem commit [1cfefa5](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1cfefa55672c796a000e0a8a9308beabb085c773).

This remains a finite-pool mixed-order theorem. It is not a complete sixth/eighth orbit audit, a continuous-family no-go, or an operational Choi/diamond-norm guarantee. The next action is to price the remaining 1,459 canonical columns against this exact 183-column dual.


The next separation step is queued in [workflow 45105506797](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105506797). It will reverify the exact 183-column dual, screen all 1,459 unused canonical generators, and apply independent 128-bit Arb verification to up to ten leading positive candidates.


## 183-column full-sixth-cut dual pricing completed (2026-11-23)

Workflow [45105506797](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105506797) completed successfully. It re-certified the 183-column dual, screened all 1,459 unused canonical columns, and found exactly one binary64-positive candidate: canonical column 332, score 0.003290534078972167.

Independent 128-bit Arb evaluation gives
\[
[0.0032905340797223044027532381066990752100\pm2.34\times10^{-41}],
\]
whose lower endpoint is strictly positive. Thus column 332 escapes the 183-column dual after addition. The full screen and Arb transcript are committed in [8e6d733](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8e6d73355a640e28957bc3625581a91a979d365c), in `evidence/55probe_183col_full_sixth_cut_dual_pricing_screen_n21.json` and `evidence/55probe_183col_full_sixth_cut_dual_pricing_arb_n21.json`.

The positive escape does not prove feasibility and does not exclude the other 1,458 nonpositive binary64 columns. The next pool is the 184-column / 2,113-row full-sixth-cut reoptimization, adding column 332.


The 184-column reoptimization has been launched as [workflow 45105751599](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105751599). Its pool is the certified 183-column / 2,113-row full-sixth-cut inventory plus canonical column 332, whose reduced-cost score is strictly positive by Arb. The workflow revalidates the 183-column parent certificate and pricing provenance before solving; no 184-column objective is asserted until it completes.

## 2026-11-23: 184-column / 2,113-row full-sixth-cut obstruction certified

The 184-column reoptimization completed successfully in [workflow 45105751599](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45105751599). It added canonical column 332 to the 183-column parent pool and retained the pinned 2,113-row design: 1,461 complete second-/fourth-order rows, 645 sixth-order rows (311 original plus 334 candidate-specific cuts), and seven selected eighth-order rows.

The binary64 HiGHS discovery returned objective 0.487611737529284, independently recomputed maximum 0.48761173752942266, support size 50, and primal-dual gap 5.885292253537955e-13. These are discovery diagnostics only.

The exact rationalized dual has ||z||_1=1, 50 nonzero entries (two fourth-order, 46 sixth-order, two eighth-order), and slack 10^-10. Independent 128-bit Arb verification covers all 184 physical-column inequalities; the largest slack-shifted interval upper endpoint is -7.6565440382899942e-11. Therefore
\[
\min_{p\in\Delta(P184)}\|r(p)\|_\infty
\ge
\frac{22487122319210016751569973413}
{46116860184300265870000000000}
=0.48761173742841650\ldots>\frac13.
\]

Formal proof: THEORY_184COL_2113ROW_FULL_SIXTH_CUT_MINIMAX_OBSTRUCTION.md. LP transcript and certificate: evidence/joint_low_six_eighth_lp_184col_full_sixth_cuts_n21.json and evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json. Evidence commit: 0c0c745c534fb161835e03e63776d6fe7f7178eb.

**Scope:** this is a mixed-order finite-pool theorem for the pinned 184 physical generators and 2,113 rows. It is not a complete sixth/eighth orbit audit, a continuous-family no-go, or a Choi/diamond-norm guarantee. The next finite-pool action is to price all 1,458 unused canonical columns against the new exact dual; the central paper-level gap remains an operational per-instance moment-to-channel theorem.

## 2026-11-23: 184-column pricing against the frozen canonical inventory

The 184-column exact dual was screened against all 1,458 unused columns in the frozen 1,641-column canonical inventory. The binary64 screen found zero positive candidates; the maximum unused score is -0.008535526293085835. This is discovery evidence only: no nonpositive binary64 score is a rigorous interval exclusion.

A separate complete Arb verifier and workflow have been added to check all 1,458 unused columns at 128-bit precision:
- verifier: verify_184col_full_sixth_cut_dual_all_canonical_arb.py;
- workflow: eui-184col-full-sixth-cut-full-pool-arb.yml;
- workflow run is triggered by commit f58912d1ccf2287b0da81b9bbea3df5ef77ac1ce.

If all 1,458 interval upper endpoints are strictly negative, combining the full-pool audit with the 184 active-column certificate proves the same 2,113-row mixed-order lower bound for the entire 1,641-column canonical inventory plus the one pinned continuous-path escape generator. This remains a finite union, not the unrestricted continuous path family.

## 2026-11-23: complete Arb separation of the canonical inventory

The 184-column dual was extended from its 184 active physical columns (183 canonical plus one exact continuous-path escape) to the entire frozen 1,641-column canonical inventory. The full 128-bit Arb run [45107567728](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45107567728) checked all 1,458 unused canonical columns:

- 1,458 strictly negative interval upper endpoints;
- zero positive intervals;
- zero intervals overlapping zero;
- maximum unused-column upper endpoint at canonical column 430:
  \[
  [-0.0085355262917551396968965552281556190618\pm2.78\times10^{-41}].
  \]

Combining these with the existing Arb certificate for the 183 active canonical columns and the one continuous escape proves the same exact lower bound for every mixture over all 1,641 canonical paths plus that one escape:
\[
\min_{p\in\Delta(\mathcal C_{1641}\cup\{c_\star\})}\|Ap-y\|_\infty
\ge
\frac{22487122319210016751569973413}
{46116860184300265870000000000}
=0.48761173742841650\ldots>\frac13.
\]

Formal extension: [THEORY_FULL_CANONICAL_POOL_PLUS_ESCAPE_2113ROW_MINIMAX_OBSTRUCTION.md](THEORY_FULL_CANONICAL_POOL_PLUS_ESCAPE_2113ROW_MINIMAX_OBSTRUCTION.md). Compact machine-readable summary: evidence/55probe_184col_full_canonical_pool_arb_summary_n21.json. Full interval transcript: evidence/55probe_184col_full_canonical_pool_arb_n21.json, GitHub blob SHA1 146b04f500b519e971b88d325d0cbccd1ee2fd87, committed at [dcab0b7](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/dcab0b7fd7c7e81c36c7164441189c7e89d26a29).

**Boundary:** this is a complete separation result for the finite canonical inventory plus one additional continuous path. It is still not a theorem for the unrestricted continuous coupling family, and the 2,113-row mixed-order residual still has no EUI-specific Choi/diamond-norm guarantee. The next mathematical target is global separation over the admissible continuous path family; the operational moment-to-channel bridge remains independent and essential.


## 184-column dual: strict continuous-path escape (2026-11-23)

The unrestricted positive 41-edge open-path family contains a second exact-rational escape from the 184-column mixed-order dual. The corrected 10-start Frechet/cofactor search passed its active-column regression check (the prior pinned escape is reproduced to within \\(10^{-8}\\)); the analytic gradient agrees with complex-step differentiation with maximum relative defect \(7.97\times10^{-13}\). The candidate is outside the frozen 1,641-column canonical pool and differs from the earlier continuous escape.

An independent 128-bit Arb verifier rebuilt the matrix exponential and all 50 active dual features from the exact 12-decimal rational couplings and certified
\[
S_{184}(c)\in[558.5197275383090425573204756469618\pm6.20\times10^{-32}]>0.
\]
This strictly disproves extending the **particular 184-column dual** to the full continuous path family. It does not invalidate the finite 184-column theorem, prove a full-family feasible ensemble, or establish an operational Choi/diamond guarantee.

- Formal proof and exact couplings: `THEORY_184COL_CONTINUOUS_PATH_DUAL_ESCAPE.md`.
- Discovery: `evidence/184col_continuous_dual_search_n21.json`.
- Arb certificate: `evidence/184col_continuous_dual_escape_arb_n21.json`.
- Workflow: [45115018787](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45115018787).
- Evidence commit: [026ae00](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/026ae00d44e8d3826c881a648293469bb3c81135).

The first two search runs exposed a scalar-value bug (the feature was added without its dual coefficient) and are explicitly discarded in Issue #5. The corrected implementation weights the scalar and gradient consistently and checks the old certified column before optimization.

**Next:** add this exact path as a 185th column, re-solve the same 2,113-row minimax LP, then certify any new dual and test it again against the continuous family. Do not promote the finite-pool obstruction to a continuous-family theorem.


## 185-column follow-up after the second continuous-path escape (2026-11-23)

A second exact-rational 41-edge open path strictly escapes the 184-column mixed-order dual. Its independent 128-bit Arb pricing interval is
\[
S_{184}(c)\in[558.5197275383090425573204756469618\pm6.20\times10^{-32}]>0.
\]
This refutes the global extension of that particular finite-pool dual; it does not affect the 184-column theorem or prove full-family feasibility.

The exact input and proof are recorded in `THEORY_184COL_CONTINUOUS_PATH_DUAL_ESCAPE.md`, with Arb transcript `evidence/184col_continuous_dual_escape_arb_n21.json` and successful workflow [45115018787](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45115018787).

The 185-column reoptimization has been implemented as the 184-column pool plus this second continuous path, retaining exactly the same 2,113-row mixed-order design. The new workflow [45126903168](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45126903168) rechecks the parent dual and both escape certificates, solves the LP, and independently verifies either an exact-probability sub-\(1/3\) candidate on all pinned rows or a new above-cap dual against all 185 columns. At the time of this audit update, the LP step is still running; no 185-column objective or theorem is claimed.

Protocol and scope: `THEORY_185COL_SECOND_CONTINUOUS_ESCAPE_REOPTIMIZATION.md`. The experiment remains finite-pool and selected-row only. A complete 63,133-orbit sixth-order audit, complete eighth-order control, unrestricted continuous-family minimax theorem, and EUI-specific moment-to-Choi/diamond bridge remain unresolved.


## 185-column result after adding the second continuous escape (2026-11-23)

The second Arb-certified continuous path was added to the 184-column pool and the same 2,113-row mixed-order LP was re-solved. Workflow [45126903168](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45126903168) passed all prechecks and its independent 185-column dual verifier.

HiGHS discovery diagnostics: objective 0.47182017897606104; recomputed maximum 0.4718201789763452; support size 54; primal-dual gap \(1.10\times10^{-14}\). The exact rational dual has \(\|z\|_1<1\), 54 nonzero rows (six fourth-order, 46 sixth-order, two eighth-order), and \(\delta=10^{-10}\). The 128-bit Arb verifier checked all 185 physical-column inequalities; the largest slack-shifted upper endpoint is
\[
-7.5382718420716027175678793242632891258\times10^{-11}<0.
\]
It proves
\[
\min_{p\in\Delta(\mathcal P_{185})}\|A_{185}p-y\|_\infty
\ge
\frac{5439716305336726789426356149}
{11529215046068469760000000000}
=0.4718201788760721\ldots>\frac13.
\]
The exact margin above \(1/3\) is \(0.13848684554273874\ldots\).

- LP transcript: `evidence/joint_low_six_eighth_lp_185col_second_continuous_escape_n21.json`
- Arb dual: `evidence/55probe_185col_second_continuous_escape_dual_certificate_n21.json`
- Formal scope and proof record: `THEORY_185COL_SECOND_CONTINUOUS_ESCAPE_REOPTIMIZATION.md`
- Reoptimizer and independent verifiers: `reoptimize_185col_second_continuous_escape.py`, `verify_185col_second_continuous_escape_dual_arb.py`, `verify_185col_second_continuous_escape_candidate_arb.py`
- Evidence commit: [80a913f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/80a913f3186018c1768e03fc0a9edcb0eab1c90a)
- Formal-note update: [7d39631](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/7d39631fc2ed5bf7961bd2087a08f85678cb3fb5)

**Boundary:** this is a fixed 185-generator / 2,113-row mixed-order theorem. It is not a complete sixth/eighth orbit certificate, a no-go for the unrestricted continuous path family, or a Choi/diamond operational guarantee. The second continuous escape invalidates the 184-column dual's attempted global extension; the newly certified 185-column dual must itself be tested against the continuous family before any such extension is considered.


## 185-column dual: third strict continuous-path escape (2026-11-23)

The newly certified 185-column dual also fails to separate the unrestricted positive 41-edge open-path family. A deterministic 10-start Frechet/cofactor search produced an exact-decimal-rational path, distinct from the two prior escapes and from the canonical inventory. The analytic gradient agrees with complex-step differentiation with maximum relative defect \(9.18\times10^{-13}\).

An independent 128-bit Arb verifier certifies
\[
S_{185}(c)\in[293.82920368783706755711439295738586\pm5.02\times10^{-33}]>0.
\]
This refutes the global extension of the particular 185-column dual. It does not invalidate the finite 185-column theorem, prove a full-family feasible mixture, or imply an operational channel guarantee.

- Exact path and proof: `THEORY_185COL_CONTINUOUS_PATH_DUAL_ESCAPE.md`
- Search and Arb evidence: `evidence/185col_continuous_dual_search_n21.json`, `evidence/185col_continuous_dual_escape_arb_n21.json`
- Successful workflow: [45127900561](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45127900561)
- Evidence commit: [4293fc0](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4293fc0e567d0ed0c45c295a9687fb273dc4ea54)

The next finite experiment is the 186-column reoptimization, adding this exact path to the 185-column pool. The continuous-family minimax theorem and the EUI-specific moment-to-Choi/diamond bridge remain open.


## 2026-11-23: 186-column mixed-order minimax obstruction after a third continuous escape

A third exact-rational positive 41-edge path was found against the 185-column dual. Its independent 128-bit Arb pricing interval is
\[
S_{185}(c)\in[293.82920368783706755711439295738586\pm5.02\times10^{-33}]>0.
\]
This invalidates only the attempted global extension of the 185-column dual; it does not affect that finite-pool theorem.

The path was added as column 1643 and the same 2,113-row mixed-order LP was re-solved over 186 physical generators. Workflow [45128712241](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45128712241) completed successfully. HiGHS discovery returned objective 0.4682823606610356, recomputed maximum 0.4682823606621971, support size 54, and primal-dual gap \(8.73\times10^{-14}\). These floating-point values are diagnostics only.

The rationalized dual was independently certified with 128-bit Arb against all 186 physical columns. Its exact \(L_1\) norm is 1; its support comprises five fourth-order, 47 sixth-order, and two eighth-order rows. All 186 slack-shifted column intervals are strictly negative; the largest upper endpoint is
\[
[-5.8049776314970689775168775729908666748\times10^{-11}\pm1.91\times10^{-49}]<0.
\]
Therefore
\[
\min_{p\in\Delta_{186}}\|A p-y\|_\infty
\ge
\frac{2699464018593872397696556823}
{5764607523034431770000000000}
=0.4682823605609322602\ldots>\frac13.
\]
The exact margin above \(1/3\) is
\[
\frac{2333784532747185423089670469}
{17293822569103295310000000000}
=0.1349490272275989268\ldots.
\]

Formal statement: [THEORY_186COL_2113ROW_THIRD_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_186COL_2113ROW_THIRD_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md).

Evidence:
- LP transcript SHA256: 8fdaf824fa742ae34a5a156c251feadd59b0047b
- Dual certificate SHA256: 365dc82f4540cb6821038da3059efeb8cb8205b3
- Independent verifier: verify_186col_third_continuous_escape_dual_arb.py
- All 186 interval checks: evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json

Scope remains finite-pool and mixed-order: 645 selected/cut sixth-order rows and seven selected eighth-order rows, not complete sixth/eighth orbit audits. This is not a global continuous-family no-go or an operational Choi/diamond theorem.

**Next decisive action:** test the new 186-column dual over the unrestricted positive 41-edge path family. The 185-column dual already had a certified continuous escape, so no finite-pool certificate is to be promoted to a continuous-family separator without a separate global proof.


## 2026-11-23: fourth continuous-path escape from the 186-column dual

The 186-column / 2,113-row mixed-order finite-pool theorem remains valid for its pinned 186 physical generators, but its exact dual is not a global separator over the positive 41-edge path family. A 10-start differentiable search found a fourth exact-rational path. The analytic cofactor/Frechet gradient passed complex-step checks with maximum relative defect \(1.10\times10^{-14}\); this is an implementation diagnostic, not the proof.

Independent 128-bit Arb verification certified
\[
S_{186}(c)\in[281.0783501949911583545100045096690\pm1.26\times10^{-32}]>0.
\]
The candidate is outside the frozen canonical inventory and distinct from the three previous continuous escapes. Exact couplings, candidate SHA256, search transcript, and Arb certificate are recorded in [THEORY_186COL_CONTINUOUS_PATH_DUAL_ESCAPE.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_186COL_CONTINUOUS_PATH_DUAL_ESCAPE.md).

Workflow [45130632601](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45130632601) passed all steps: previous escape re-certification, 186-column dual re-certification, py_compile, 10-start search, and independent Arb. Search transcript SHA256: 5f92901fe1191394191c1750f7f4de2d35c6d39c; Arb certificate SHA256: 5d7b25dfc15e9183bf1a06672479bdd8a4cd515b; candidate SHA256: f9c28135608deb0c687407a8cc71e58bf7f3bb5763ab8f997fd3b1141625c24d.

This is a strict counterexample to extending this particular 186-column dual over the continuous path family. It does not invalidate the finite-pool theorem, provide a feasible mixture, or establish a full-family minimax result.

The exact path has been added as column 1644. A new 187-column reoptimizer, dual verifier, exact-mixture Arb verifier, and workflow are committed. Workflow [45132177104](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45132177104) is executing the 187-column, 2,113-row branch. Its result is pending.


## 2026-11-23: 187-column mixed-order minimax obstruction certified

The fourth exact-rational continuous path escaped the 186-column dual and was added as column 1644. Re-solving the same 2,113-row mixed-order LP over 187 pinned physical generators gave binary64 HiGHS objective 0.46338166315236223, recomputed maximum 0.4633816631525127, and primal-dual discovery gap \(5.83\times10^{-14}\). These are discovery diagnostics only.

The rationalized dual has exact \(\ell_1\) norm 1 and support on three fourth-order, 54 sixth-order, and two eighth-order rows. The independent 128-bit Arb verifier checked all 187 physical-column inequalities. Every slack-shifted interval upper endpoint is negative; the maximum is
\[
[-6.1052543564944087761512888156950312261\times10^{-13}
\pm2.23\times10^{-51}]<0.
\]
Therefore
\[
\min_{p\in\Delta_{187}}\|A_{2113\times187}p-y\|_\infty
\ge
\frac{21369707366939402851572579191}
{46116860184274208090000000000}
=0.4633816630523005\ldots>\frac13.
\]
The exact margin above \(1/3\) is 0.13004832971896715....

Formal statement: [THEORY_187COL_2113ROW_FOURTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_187COL_2113ROW_FOURTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md).

Evidence:
- Successful reoptimization and Arb certification: [workflow 45133203733](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45133203733)
- LP transcript SHA256: `8a63fdbec151593e1c52cf3e55585d6c8760d6b3536564812758526ccdbbe245`
- Dual certificate SHA256: `475346510c8d0e7d52031cb21d694f91230beb60`
- Fourth continuous escape certificate SHA256: `320d6048e63ee0e9c71481d25e99b91ab730c0cd570192128782b34c9fa812bd`
- Verifier fix commit: [c7e556b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/c7e556b85c9efec84daf61898f4c1c8cf3c81811)
- Evidence commit: [d8148b9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/d8148b9ccf5e06e934227e418f2e7d313969c3a7)

**Provenance correction:** the initial 187-column verification failed because the verifier compared the third escape against the 186-column parent. The third escape actually belongs to the 185-column parent; the fourth escape belongs to the 186-column parent. The corrected verifier checks both parent links and records the fourth escape certificate hash. The corrected workflow passed.

Scope remains finite-pool and mixed-order. The 645 sixth rows are selected/cut, not all 63,133 sixth-order orbits; seven eighth-order rows are selected, not complete. This is not a full positive-coupling-family no-go or an operational Choi/diamond theorem. The newly certified 187-column dual still requires a separate continuous-path pricing test; a failed local search is not a global proof.


## 2026-11-23: fifth continuous-path escape from the 187-column dual

A deterministic 10-start differentiable search against the newly Arb-certified 187-column dual found a fifth distinct exact-rational positive 41-edge path (augmented column 1645). The best search point came from start 2 and reached the 100-iteration limit; this is discovery evidence, not a convergence claim. The cofactor/Frechet analytic gradient passed complex-step checks with maximum relative defect \(4.4931\times10^{-13}\).

The independent 128-bit Arb verifier proves
\[
S_{187}(c)\in[216.2699462606013389218645814697156
\pm6.50\times10^{-32}]>0.
\]
Thus the 187-column dual also fails to separate the full positive 41-edge path family. This does not invalidate the finite 187-column theorem and does not prove that a continuous-family mixture reaches \(1/3\).

Formal counterexample: [THEORY_187COL_CONTINUOUS_PATH_DUAL_ESCAPE.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_187COL_CONTINUOUS_PATH_DUAL_ESCAPE.md).

Evidence:
- Search transcript SHA256: `b37ba7c81ae78f32e41741e68038eac6dd726b64`
- Arb certificate SHA256: `d84f7b32f0748a3e7433c990b3f82469a178dd4c`
- Candidate SHA256: `7565cc9aa5240c5c42b8692e97381c4415061403e2bddf4563c03fc779e9a9e8`
- Successful search/Arb workflow: [45134044907](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45134044907)

The new path is now the next column-generation input (label 1645). The next action is an 188-column reoptimization on the unchanged 2,113-row mixed-order design, followed by exact rational/Arb certification. A new 188-column dual, if obtained, must again be tested against the continuous path family; failure of a local search will not be treated as global separation.


## 188-column fifth-continuous-escape reoptimization (2026-11-23)

The fifth exact-rational positive 41-edge path escaped the 187-column dual and was appended as column 1645. Re-solving the unchanged 2,113-row mixed-order LP over 188 pinned columns returned the binary64 HiGHS objective 0.4585955253523888, independently recomputed maximum 0.4585955253531613, support size 52, and primal-dual discovery gap 3.98e-13. These are discovery diagnostics only.

The new exact-rational dual was independently checked with 128-bit Arb against all 188 physical columns. Its exact \\(\\ell_1\\) norm is
\\[
\\frac{73786976294791983323}{73786976294838206464}<1,
\\]
and its 52 nonzero rows comprise three fourth-order, 47 sixth-order, and two eighth-order rows. Every slack-shifted column inequality has a strictly negative Arb upper endpoint; the maximum is
\\[
[-8.8068030053955477431256232530676661255\\times10^{-10}
\\pm1.19\\times10^{-48}]<0.
\\]
Consequently the fixed-pool theorem is
\\[
\\min_{p\\in\\Delta_{188}}\\|A p-y\\|_\\infty
\\ge
\\frac{66090580242847531496409753}
{144115188075855872000000000}
=0.4585955243527862\\ldots>\\frac13.
\\]

Formal proof: [THEORY_188COL_2113ROW_FIFTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_188COL_2113ROW_FIFTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md).

Evidence:
- Successful 188-column reoptimization and Arb branch: [workflow 45135692203](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45135692203)
- LP transcript SHA256: `f512d8fa40887d84a3274c7dd5f4716b841573e90adcd2ff7f12d191c2bf8297`
- Dual certificate: `evidence/55probe_188col_fifth_continuous_escape_dual_certificate_n21.json`
- Reoptimizer: `reoptimize_188col_fifth_continuous_escape.py`
- Independent verifier: `verify_188col_fifth_continuous_escape_dual_arb.py`

This remains a fixed-pool mixed-order result. The 645 sixth-order rows are selected/cut rather than all 63,133 sixth-order dihedral orbits, and the seven eighth-order rows are selected representatives. It is not a global continuous-family no-go and does not imply a Choi-fidelity or diamond-norm guarantee.

The 188-column dual is now being tested directly against the positive 41-edge path family. The differentiable search is discovery-only; a candidate will count as an escape only if the independent exact-rational Arb verifier returns a strictly positive interval lower endpoint. Failure to find a candidate will not prove global separation.


## Sixth continuous escape from the 188-column dual (2026-11-23)

A deterministic 10-start differentiable search against the exact 188-column dual found a sixth positive 41-edge path in the bounded discovery box \\(10^{-4}\\le c_j\\le100\\). The analytic cofactor/Frechet gradient passed complex-step checks with maximum relative defect \\(1.8853041827096364\\times10^{-14}\\). The best binary64 score was 229.86008474837345; the optimizer reached its 100-iteration limit, so this is discovery evidence only.

The exact 12-decimal rational path was independently recomputed with 128-bit Arb. Its pricing interval is
\\[
[229.8600847483890088894499687466130
\\pm3.31\\times10^{-32}]>0.
\\]
This strictly disproves global separation by the particular 188-column dual; it does not prove feasibility of the continuous-family minimax problem. The candidate SHA256 is `68baf2aa6667b3b0eb597ef576e114b37f3c6dc790f28068dfd1c74059724680`.

Formal counterexample: [THEORY_188COL_CONTINUOUS_PATH_DUAL_ESCAPE.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_188COL_CONTINUOUS_PATH_DUAL_ESCAPE.md).

Evidence:
- [Search and 128-bit Arb workflow 45142329253](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45142329253)
- Search transcript SHA256: `772d3df9da55e83431e2652cc2bf46b17ee24b195abc751074edc1673a6f30e2`
- Arb certificate SHA256: `d3bb1345d95d305cc48ca1cb491257e6c868bef9`
- Parent 188-column LP SHA256: `f512d8fa40887d84a3274c7dd5f4716b841573e90adcd2ff7f12d191c2bf8297`
- Parent 188-column dual SHA256: `eed80945f8ae5875c7fbad6f4d760c934654eaf44ce22a4bf373f4358ccedef5`

The new path is appended as column 1646. The next experiment is the 189-column reoptimization on the same 2,113 rows, followed by exact-rational dual or primal Arb certification.

## 189-column sixth-continuous-escape minimax obstruction certified (2026-11-23)

The sixth exact-rational positive 41-edge path escaped the 188-column dual and
was appended as column 1646. The unchanged 2,113-row mixed-order LP was
re-solved over 189 physical generators. HiGHS returned objective
0.454195317365923, independently recomputed maximum 0.4541953174059339,
support size 57, and primal-dual discovery gap 2.443489854897507e-12. These
are binary64 discovery diagnostics only.

The rationalized dual was independently certified with 128-bit Arb against
all 189 physical columns. Its exact l1 norm is 1; its support comprises one
fourth-order row, 54 sixth-order rows, and two eighth-order rows. Every
slack-shifted column interval is strictly negative; the largest upper endpoint
is enclosed by
\[
[-8.9418568666754042859549486269839336820\times10^{-9}
\pm3.14\times10^{-47}]<0.
\]
The resulting finite-pool theorem is
\[
\min_{p\in\Delta_{189}}\|A p-y\|_\infty
\ge
\frac{209460614862602549049621931}
{461168601845037806900000000}
=0.4541953073661022\ldots>\frac13.
\]
The exact margin above 1/3 is
\[
\frac{167213242742769840248865793}
{1383505805535113420700000000}
=0.12086197403276885\ldots.
\]

Formal proof: [THEORY_189COL_2113ROW_SIXTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_189COL_2113ROW_SIXTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md).

Evidence:
- Successful reoptimization and strict Arb certification: [workflow 45145380760](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45145380760)
- LP transcript SHA256: `e73311bdf1a683620417dcc2cd7c18f25197d8451f1be76e7ed76c4de31424de`
- Exact dual certificate: `evidence/55probe_189col_sixth_continuous_escape_dual_certificate_n21.json`
- Independent verifier: `verify_189col_sixth_continuous_escape_dual_arb.py`
- Evidence commit: [09fc105](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/09fc1050a3721ef6f00ff51cec73c690a6a9b458)
- Verifier/workflow definition commits: [6710729](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/67107297a570d1006486f61ee9744de7e862f36c), [8aee1b4](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8aee1b46fe56f022680f323e6f2f2b270412dae3)

Scope remains finite-pool and mixed-order: 645 selected/cut sixth rows, not all
63,133 sixth-order dihedral orbits; seven selected eighth rows, not all
1,408,185 eighth-order orbits. This is not a sixth-only theorem, a global
positive-coupling-family no-go, or an operational Choi/diamond theorem. The
new 189-column dual must itself be tested against the unrestricted positive
41-edge path family; failure of a local search will not prove global
separation.

## Seventh continuous-path escape from the 189-column dual (2026-11-23)

A deterministic 10-start differentiable search against the newly Arb-certified
189-column dual found a seventh exact-decimal-rational positive 41-edge path
(label 1647). The candidate is distinct from all six prior paths and outside
the frozen canonical inventory. The cofactor/Frechet analytic gradient passed
complex-step checks with maximum relative defect
1.0714305862054578e-13. The best discovery came from start 8 after 100
iterations; the optimizer hit its iteration limit, so no convergence claim is
made.

The independent 128-bit Arb verifier proves
\[
S_{189}(c)\in
[207.4357421969902709413811580245091
\pm2.10\times10^{-32}]>0.
\]
This strictly refutes global separation by the particular 189-column dual.
It does not invalidate the finite 189-column theorem, prove a feasible
continuous-family mixture, or imply an operational channel guarantee.

Formal counterexample: [THEORY_189COL_CONTINUOUS_PATH_DUAL_ESCAPE.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_189COL_CONTINUOUS_PATH_DUAL_ESCAPE.md).

Evidence:
- [Successful search and Arb workflow 45147006543](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45147006543)
- Search transcript SHA256: `2862b1fc35e1739bed710f9b2059b1b5c855e57a975a091247e8aab7417a9900`
- Arb certificate: `evidence/189col_continuous_dual_escape_arb_n21.json`
- Candidate SHA256: `2dcdd30f2a0c9fbb901c9f63748ca2ca5151e770b92b93255a0cb36324d734c8`
- Search, verifier, workflow commits: [1fd531a](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1fd531a121e88332c685e9558967a6e829dd76ff), [64b7b52](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/64b7b5283a7be21d4417e4935e0593fbb6d994c6), [5198789](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5198789cdcb6dd41c08756257304454aaf3c1e43).

The next finite experiment is a 190-column reoptimization, appending the
seventh path to the unchanged 2,113-row mixed-order design. The continuous
family minimax theorem and the EUI-specific moment-to-Choi/diamond bridge
remain open.

## Seventh continuous-path escape from the 189-column dual; 190-column branch launched

The exact 189-column mixed-order dual is a valid finite-pool certificate, but it is not a separator for the unrestricted positive 41-edge path family. A deterministic 10-start differentiable search found a seventh exact-decimal-rational path (label 1647), distinct from the six earlier escapes and outside the frozen canonical inventory. The analytic cofactor/Frechet gradient passed complex-step checks with maximum relative defect
\[
1.0714305862054578\times10^{-13}.
\]
The optimizer reached its 100-iteration limit, so convergence is not claimed.

The independent 128-bit Arb verifier certifies the exact path's pricing score:
\[
S_{189}(c)\in
[207.4357421969902709413811580245091\pm2.10\times10^{-32}]>0.
\]
This strictly refutes global separation by this particular 189-column dual. It does not invalidate the finite 189-column theorem, establish continuous-family feasibility, or imply an operational channel guarantee.

Formal counterexample: [THEORY_189COL_CONTINUOUS_PATH_DUAL_ESCAPE.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_189COL_CONTINUOUS_PATH_DUAL_ESCAPE.md).

Evidence:
- [Successful search and Arb workflow 45147006543](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45147006543)
- Search transcript SHA256: `2862b1fc35e1739bed710f9b2059b1b5c855e57a975a091247e8aab7417a9900`
- Arb certificate: `evidence/189col_continuous_dual_escape_arb_n21.json`
- Candidate SHA256: `2dcdd30f2a0c9fbb901c9f63748ca2ca5151e770b92b93255a0cb36324d734c8`
- Search/verifier/workflow commits: [1fd531a](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/1fd531a121e88332c685e9558967a6e829dd76ff), [64b7b52](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/64b7b5283a7be21d4417e4935e0593fbb6d994c6), [5198789](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5198789cdcb6dd41c08756257304454aaf3c1e43).

The seventh path is appended as column 1647 in the new 190-column reoptimizer. The unchanged 2,113-row design and all parent/escape provenance are checked. New files:
- `reoptimize_190col_seventh_continuous_escape.py`
- `verify_190col_seventh_continuous_escape_dual_arb.py`
- `.github/workflows/eui-190col-seventh-continuous-escape.yml`

Commits: [c35fa87](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/c35fa87bbb76450f6e42d5bf89cabf1a2c551b26), [51b7e9f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/51b7e9f439e043e838f9d7ba4a79c79334038d78), [5c81d80](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5c81d8083acca12af3e1e23315a450bdfbb2a418). Workflow [45151174105](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45151174105) completed successfully. It passed the frozen seed/orbit checks, re-certified the 189-column parent and all seven escape inputs, compiled both new Python programs, solved the 190-column LP, and completed the independent 128-bit Arb verifier against all 190 physical columns.

HiGHS discovery returned objective 0.45056485307304617, independently recomputed maximum 0.45056485307319294, support size 58, and primal-dual discovery gap 3.375077994860476e-14. These are diagnostics only.

The exact rational dual has \\(\\|z\\|_1=1\\), slack \\(10^{-10}\\), and support on two fourth-order rows, 54 sixth-order rows, and two eighth-order rows (no second-order support). All 190 slack-shifted Arb interval upper endpoints are strictly negative; the maximum is enclosed by
\\[
[-5.0646182194565139235048775368095553314\\times10^{-11}
\\pm3.59\\times10^{-49}]<0.
\\]
The resulting finite-pool theorem is
\\[
\\min_{p\\in\\Delta_{190}}\\|A_{190}p-y\\|_\\infty
\\ge
\\frac{12786853125233436543275375237}
{28379606267246247630000000000}
=0.4505648529730001\\ldots>\\frac13.
\\]
The exact margin above one third is 0.11723151963966673....

Formal proof: [THEORY_190COL_2113ROW_SEVENTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md](https://github.com/tengxianglin/EfficientUnitaryInversion/blob/main/THEORY_190COL_2113ROW_SEVENTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md).

Evidence:
- LP transcript: `evidence/joint_low_six_eighth_lp_190col_seventh_continuous_escape_n21.json`
- Exact dual and all 190 Arb intervals: `evidence/55probe_190col_seventh_continuous_escape_dual_certificate_n21.json`
- LP transcript SHA256 pinned by the dual: `2a4ca0caab7c7ed5dab24f07e51c121e03e49236da98cbc59809d96868e94307`
- Matrix/target SHA256: `324900df03f4a09c8f04f5c30eee048d4b3e7daae214a9dadbffc9885e90c4cc`
- Evidence commit: [6236ce2](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6236ce24a02ab7cb55c53cba3681430d048de5de)
- Formal theory commit: [32875d8](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/32875d80496a9d049c06f2a1af4275f11bcc6e07)

This is a strict mixed-order lower bound for the fixed 190-generator pool on the pinned 2,113-row design only. It is not a complete sixth/eighth orbit certificate, a global positive-coupling-family minimax theorem, or an operational Choi/diamond guarantee.

If the 190-column objective is above 1/3, the workflow proceeds to exact-rational dual reconstruction and independent Arb checks of all 190 physical columns. If below 1/3, it freezes an exact rational candidate as discovery only; a separate exact-primal Arb audit and complete sixth-order separation are still required.

The 2,113-row design remains mixed-order and selected/cut: 1,461 complete second/fourth rows, 645 selected/cut sixth rows, and seven selected eighth rows. This is not a complete sixth/eighth orbit certificate, a global positive-coupling-family minimax theorem, or an operational Choi/diamond guarantee.



## Continuous-family pricing against the certified 190-column dual (2026-11-23)

The 190-column / 2,113-row mixed-order dual is strictly certified on its 190 pinned generators, but no global separation over the positive 41-edge path family has been established. I added a deterministic differentiable pricing search and an independent exact-rational 128-bit Arb verifier for the next decisive test:

- Discovery: `discover_190col_continuous_dual_escape.py`.
- Independent verifier: `verify_190col_continuous_dual_escape_arb.py`.
- Workflow: `.github/workflows/eui-190col-continuous-dual-search.yml`.
- Search uses the cofactor determinant derivative and adjoint Frechet derivative of the matrix exponential, with a complex-step gradient regression check. The search is discovery only; a positive continuous-family escape is recorded only if the independent Arb verifier proves a strictly positive interval lower endpoint.
- The new search is seeded by the seventh certified path (column 1647), checks its computed score against the 190-column certificate's Arb interval, and pins the 190-column dual/LP, the 2,113-row cut design, the frozen seed pool, and all seven prior escape certificates.

Commits:
- [0b2b609](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/0b2b609fa0cc081ff081e414a33f63dcae337035) discovery search;
- [794ff1c](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/794ff1c3d8ac0164e1ec305f6576faff8d668b25) independent Arb verifier;
- [703f299](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/703f299039700627c7adb3e9b127e0ca61b634f7) workflow;
- [c8295e1](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/c8295e129fdf8ac1700183f3d4182eca528ed15e) and [b7d77b9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b7d77b92ee658e77e5c87cf1f92dab5862a89f05) provenance-label corrections.

The workflow has started in runs [45159106797](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45159106797), [45159219699](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45159219699), and [45159224149](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45159224149). At the last inspection, the latest run had passed seed-pool and orbit-enumeration checks and was re-certifying the 190-column dual and seven prior escapes. The optimization and Arb result are not yet available.

A failed local search will not prove global separation. A successful positive Arb interval will refute global separation by this particular 190-column dual only; it will not establish feasibility of the continuous-family minimax problem. The finite 190-column theorem remains limited to its pinned mixed-order 2,113-row design (645 selected/cut sixth rows and seven selected eighth rows), not complete sixth/eighth orbit control and not a Choi/diamond-norm guarantee.


## Eighth continuous-path escape and 191-column follow-up (2026-11-23)

The newly added deterministic search against the 190-column dual found an eighth distinct positive 41-edge open path. The optimizer ran 10 starts with 100 iterations per start and did not converge; this is only a discovery diagnostic. The independent exact-decimal 128-bit Arb verifier certified the path's pricing score:
\[
S_{190}(c)\in[345.1964392867855698654219114260899\pm2.12\times10^{-32}]>0.
\]
Thus the particular 190-column dual is not a global separator for the positive 41-edge path family. This does not invalidate the finite 190-column minimax theorem and does not prove continuous-family feasibility.

The exact candidate is column 1648, distinct from the seven previous Arb-certified escapes and outside the frozen canonical inventory. Evidence:
- Search transcript: evidence/190col_continuous_dual_search_n21.json
- 128-bit Arb certificate: evidence/190col_continuous_dual_escape_arb_n21.json
- Theory note: THEORY_190COL_CONTINUOUS_PATH_DUAL_ESCAPE.md
- Successful search/Arb workflow 45159106797: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45159106797

The 191-column next experiment is now prepared:
- reoptimize_191col_eighth_continuous_escape.py appends column 1648 to the exact 190-column pool and re-solves the same 2,113-row mixed-order LP;
- verify_191col_eighth_continuous_escape_dual_arb.py reconstructs the new dual exactly and checks all 191 physical-column inequalities with 128-bit Arb;
- .github/workflows/eui-191col-eighth-continuous-escape.yml re-certifies the 190-column parent and all eight escape inputs before the LP.

Commits:
- f9fcb4f continuous escape theorem note;
- f11e91b initial 191-column reoptimizer;
- ab92135 corrected parent provenance and eighth-path handling;
- e948211 191-column Arb verifier;
- efdea98 191-column workflow.

Workflow 45160995243 was queued at the time of this audit update. No 191-column objective or certificate is claimed yet. The same logical boundary applies: a positive escape refutes only the particular finite dual's global extension; an unsuccessful local search cannot establish global separation.


## 191-column eighth-continuous-escape result (2026-11-23)

The eighth exact-decimal positive 41-edge path was added as physical column 1648.
The 191-column LP on the pinned 2,113-row mixed-order design returned the
binary64 HiGHS discovery objective 0.44291781834803107 and independently
recomputed maximum 0.4429178183485498. These values are solver diagnostics,
not the theorem.

The exact rationalized dual was independently checked with 128-bit Arb against
all 191 physical columns. The certificate proves
\[
\min_{p\in\Delta_{191}}\|A_{191}p-y\|_\infty
\ge
\frac{2493405651522255993844313}
{5629499534213120000000000}
=0.4429178182480797\ldots>\frac13.
\]
Its exact dual has \(\|z\|_1=576460752303381559/576460752303423488<1\),
59 nonzero coordinates (two fourth-order, 55 sixth-order, two eighth-order),
and slack \(10^{-10}\). All 191 Arb interval upper endpoints are strictly
negative; the maximum interval is
\[
[-2.0472330488499601835976889763931526041\times10^{-11}
\pm3.45\times10^{-49}].
\]
The certified gap above one third is 0.10958448491474636....

Evidence:
- Theory: `THEORY_191COL_2113ROW_EIGHTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md`
- LP transcript: `evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json`
- Strict certificate: `evidence/55probe_191col_eighth_continuous_escape_dual_certificate_n21.json`
- Independent verifier: `verify_191col_eighth_continuous_escape_dual_arb.py`
- Successful workflow: [45177433399](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45177433399)
- Certificate commit: [8faeb967](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8faeb967d44b438030d584f18cfd0a860815538b)

The first workflow attempt failed before evaluating any 191-column interval
because of two stale parent-provenance field names in the verifier. Commit
[80747a71](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/80747a71e5fb245b13f20cf989235a2c21229a50)
corrected the checks, and the clean rerun passed all steps including the Arb
audit. This is a theorem only for the fixed 191-generator pool and pinned
2,113-row mixed-order design. It is not a full continuous-family obstruction,
a complete sixth/eighth orbit audit, or an operational Choi/diamond-norm
inversion guarantee.


## 2026-11-23: ninth Arb-certified continuous-path escape from the 191-column dual

The 191-column pricing workflow completed successfully. A deterministic 10-start search (box \(10^{-4}\le c_j\le100\), at most 100 L-BFGS-B iterations) found a ninth positive 41-edge open path. The best candidate's optimizer run reached the iteration cap, so optimizer convergence is not claimed; the analytic gradient's maximum relative defect against complex-step checks at coordinates 0, 20, and 40 was \(2.765565554341265\times10^{-13}\).

The independent exact-decimal 128-bit Arb verifier certified
\[
S_{191}(c)\in[240.12916173240860667511831935153365\pm7.55\times10^{-33}]>0.
\]
All 41 edge magnitudes are strictly positive (two lie exactly at the search-box lower boundary \(10^{-4}\)); the path differs from the eight previous escapes and is outside the frozen 1,641-column canonical inventory. The 191-column dual has exact \(\|z\|_1=576460752303381559/576460752303423488<1\) and 59 active rows (2 low, 55 selected/cut sixth, 2 selected eighth).

Evidence:
- Theory: THEORY_191COL_NINTH_CONTINUOUS_PATH_DUAL_ESCAPE.md
- Search: evidence/191col_continuous_dual_search_n21.json
- Arb certificate: evidence/191col_continuous_dual_escape_arb_n21.json
- Verifier: verify_191col_continuous_dual_escape_arb.py
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45178729623
- Evidence commit: https://github.com/tengxianglin/EfficientUnitaryInversion/commit/cf142f3b96476a3385aa6bb296e37e811948ee53
- Theory-note commit: a8bfe6f5448efad63bb3a8c2526e9b217cc4a1cf

This refutes global separation by the particular 191-column dual only. It does not invalidate the finite 191-column minimax theorem, establish feasibility/infeasibility of the full continuous-family minimax problem, certify complete sixth/eighth orbit control, or give a Choi/diamond operational guarantee. The next finite experiment is the 192-column LP with this path appended as column 1649.


## Exact dense-torus reduction on the uniform 42-site path

A separate analytic result now gives an exact compactification of one continuous physical subfamily. For the uniform 41-edge path generator \(K_*\) with upper/lower entries \(+2/-2\), its positive frequencies are
\[
\omega_k=4\cos(k\pi/43),\qquad k=1,\ldots,21.
\]
The 21 frequencies are linearly independent over \(\mathbb Q\): writing \(\zeta=e^{2\pi i/43}\) and \(e^{\pi i/43}=-\zeta^{22}\), they are, up to nonzero rational factors and a permutation, the 21 elements \(\zeta^m+\zeta^{-m}\). Their independence follows by multiplying a putative relation by \(\zeta^{21}\) and using the minimal polynomial \(\Phi_{43}(x)=1+\cdots+x^{42}\); the resulting polynomial has zero \(x^{21}\) coefficient and therefore cannot be a nonzero multiple of \(\Phi_{43}\).

Kronecker's theorem then proves that \(e^{tK_*}\), \(t\ge0\), is dense in the conjugate maximal torus of \(SO(42)\), with 21 independent rotation phases. For every continuous pricing functional \(F\),
\[
\sup_{t\ge0}F(e^{tK_*})=\max_{\theta\in\mathbb T^{21}}F(Q(\oplus_k R(\theta_k))Q^\mathsf T).
\]
This is an exact closure theorem and a compactification of the uniform-coupling ray, not a claim that the current 191-column dual has positive maximum on that torus. It suggests the next decisive analytic/numerical test: optimize the certified 191-column pricing functional over these 21 phases, then use density and an Arb-verified strict positive margin to obtain a finite uniform-ray escape if one exists.

Theory: THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md


## Ninth escape appended: 192-column LP discovery

The ninth Arb-certified path (physical label 1649) was appended to the 191-column pool and the same 2,113-row design was reoptimized. The 192-column HiGHS discovery returned
\[
\eta_{\rm LP}=0.43927461827369735,
\qquad
\max_i |(Ap-y)_i|=0.4392746182957874,
\]
with primal/dual discovery gap \(9.893752483947083\times10^{-13}\), 61 positive-support columns, and new-column weight \(2.4935939849649987\times10^{-5}\). The objective remains above \(1/3\).

This is still a binary64 LP discovery, not a theorem. The independent 128-bit Arb verification of the rationalized 192-column dual is the required next step; only if every one of the 192 column inequalities is strictly certified may the corresponding finite-pool minimax lower bound be stated as proved.

- LP transcript: evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json
- Reoptimizer: reoptimize_192col_ninth_continuous_escape.py
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45198909460
- LP evidence commit: ad42fb8e (see repository commit history)


## 2026-11-23: ninth-escape 192-column minimax obstruction is now Arb-certified

The ninth positive 41-edge path (physical label 1649) escaped the 191-column dual with a strict 128-bit Arb pricing interval, and was appended to the fixed 2,113-row pool. The resulting 192-column HiGHS objective was a discovery diagnostic (0.4392746182778578; independently recomputed maximum 0.4392746183411498), not the proof.

The exact rationalized 192-column dual is now stored in
`evidence/55probe_192col_ninth_continuous_escape_dual_certificate_n21.json`.
The verifier output is complete, has 192/192 strictly negative Arb interval upper endpoints, and reports the exact lower bound
\[
\min_{p\in\Delta_{192}}\|A p-y\|_\infty
\ge
\frac{49457924053915886516751}
{112589990684262400000000}
=0.43927460827855824\ldots>\frac13.
\]
The exact dual data are \(\|z\|_1=144115188075273773/144115188075855872<1\), \(\lambda=6145476815434803/4503599627370496\), objective \(\beta=\lambda+z^\mathsf Ty=126612288460328431/288230376151711744\), and slack \(\delta=10^{-8}\). There are 61 active rows (2 low, 56 selected/cut sixth, 3 selected eighth); the maximum Arb upper endpoint after the slack shift is below \(-6.5812383148672463\times10^{-9}\).

Formal proof: `THEORY_192COL_2113ROW_NINTH_CONTINUOUS_ESCAPE_MINIMAX_OBSTRUCTION.md`.
Evidence:
- LP: `evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json`
- Arb certificate: `evidence/55probe_192col_ninth_continuous_escape_dual_certificate_n21.json`
- Independent verifier: `verify_192col_ninth_continuous_escape_dual_arb.py`
- Certificate-output commit: [4ad5c547](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4ad5c5472c391a8ca07bb316ab2f7028ec7d5234)

The exact scope is the 192 pinned generators (183 selected canonical plus nine distinct positive open-path escapes) and the fixed 2,113-row mixed-order design (1,461 complete low-order, 645 selected/cut sixth, seven selected eighth). It is not a full 1,641-column canonical-pool theorem, a complete sixth/eighth orbit theorem, a continuous-family no-go, or an operational Choi/diamond theorem.

**Workflow provenance note.** The earlier run [45198909460](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45198909460) predates the verifier-step addition and its job record contains the LP-discovery steps only; it must not be cited as the Arb-certification run. The verifier step was added in commit `dd0426b` and its path trigger in `7552fb7`. This audit records the committed verifier output and does not attribute the Arb step to run 45198909460.

A reproducibility hardening change now removes the LP, candidate, and dual-certificate outputs both before a fresh run and after the race-safe `git reset --hard origin/main`, before copying only artifacts generated by that run. This prevents a stale candidate/certificate from being re-committed if a later LP takes the opposite branch or verification fails.

The next decisive scientific action is to optimize the *192-column* pricing functional over the 21-torus from `THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md`. A strictly positive Arb-certified torus value would imply a finite-time escape along the uniform positive-coupling ray by Kronecker density and continuity; a failed local search is not a global separation proof.


## Explicit uniform-path torus basis and regression (2026-11-23)

The dense-torus note now gives an explicit real orthogonal matrix \(Q\) from the path-sine eigenvectors and the diagonal phase matrix \(D=\operatorname{diag}(1,i,\ldots,i^{41})\), with
\[
Q^\mathsf TK_*Q=\bigoplus_{k=1}^{21}4\cos(k\pi/43)J.
\]
The orthogonality argument is now stated through the simple spectrum and normality of the real skew generator, together with \(v_k^\mathsf Tv_k=0\). The note also gives \(\partial_{\theta_k}R(\theta)\) and the cofactor derivative for a minor, so the 21-torus pricing search has a reproducible parametrization and analytic gradient.

A numerical sanity check in this run gave
\[
\|Q^\mathsf TQ-I\|_{\max}=2.63\times10^{-15},\qquad
\|Q^\mathsf TK_*Q-\bigoplus_k\omega_kJ\|_{\max}=5.33\times10^{-15},
\]
with \(\det Q\approx1\). These are floating-point regression diagnostics, not the proof. The new dependency-light test file is tests/test_uniform_path_torus_basis.py; the 192-column workflow now runs it alongside the frozen orbit-enumeration test. The 192-column torus pricing search is now complete: a generic-gradient-checked 12-start search found a torus point whose exact-decimal 128-bit Arb pricing interval is strictly positive. By the proved dense-torus result, this refutes global separation by this particular 192-column dual on the continuous uniform positive-coupling ray; see the 2026-11-24 audit section below.


## 2026-11-24: exact uniform-ray torus escape of the 192-column dual

The highest-leverage unresolved Issue #5 task was completed. The 192-column rational dual was tested on the explicit 21-dimensional torus that is the closure of the uniform positive-coupling ray.

A deterministic 12-start L-BFGS-B search (120 iterations/start) found a 21-phase candidate with binary64 score 2.9300228095145076. The analytic cofactor gradient was checked at a generic nonstationary point, not at the identity: across coordinates 0, 10, and 20, the maximum relative discrepancy against complex-step and central differences was 6.7481e-10. The maximum complex-step absolute discrepancy was 1.78e-15. Basis and direct-uniform-ray regressions were also checked: orthogonality 2.63e-15, canonical form 5.33e-15, direct exponential versus torus rotation 3.39e-15, and pricing agreement 5.55e-13. These are implementation diagnostics, not the proof.

The independent exact-decimal Arb verifier reconstructs the phase vector, Q basis, 21 rotation blocks, and all 61 active dual rows from exact inputs at 128-bit precision. It certifies

\[
S_{192}(R(\theta_*))
\in [2.930022809514503777074927378122496
\pm 3.46\times10^{-34}]>0.
\]

The exact phase-vector SHA256 is e1569f8952cf6fbc65d490eb6d8179069f3da47ea77dd3444184a47549ed4546. The verifier pins the 192-column dual SHA256 2b3891b88f40627458764821142f6a83e039fd051795d4146895de68f5c5a308, LP transcript SHA256 ed966f1c3f755b1910f7f34be978af88ee290821ea643cb7690d83c7aeab686a, and cut-design SHA256 d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f.

Because the positive uniform ray is dense in the 21-torus and the pricing functional is continuous, a strict positive torus point implies existence of a finite t>0 with S_192(exp(t K_*))>0, i.e. all 41 path couplings equal to t. The tail of the positive ray is also dense, so t can be taken strictly positive. This refutes extension of this particular 192-column dual to a separator of the continuous positive-coupling family. It does not invalidate the finite 192-column minimax theorem, prove full-family feasibility/infeasibility, or give an operational Choi/diamond guarantee. A direct three-range one-dimensional search has now found the explicit rational time t=14425.249926691145447=14425249926691145447/10^15. The independent 128-bit Arb verifier certifies S_192(exp(t K_*)) in [0.468498256538894200560432299886 +/- 2.83e-31] > 0; all 41 couplings equal this t.

Formal statement and proof: THEORY_192COL_UNIFORM_RAY_DUAL_ESCAPE.md.

Evidence:
- Search: evidence/192col_uniform_torus_search_n21.json (SHA256 90c47cfabf5576014f99705e5bf407cf190e394bcba0a7c00f3a51f42dcebfa9)
- Arb certificate: evidence/192col_uniform_torus_arb_n21.json
- Discovery script: discover_192col_uniform_torus_pricing.py
- Independent verifier: verify_192col_uniform_torus_pricing_arb.py
- Workflow [45220627970](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45220627970): success, including parent-dual re-certification, generic gradient regression, torus search, Arb verification, and artifact commit.
- Evidence commit: 2a7515f7491527af76b5e6010aafdf81c7b62bb5
- Theory commit: e9e1b9c6e8c8df5e20cad01f817dc0c5072b07c7

### Manuscript/supplementary audit

The currently accessible source remains arXiv v1, dated 25 June 2025: https://arxiv.org/html/2506.20570v1. Appendix B states that it generates 10,000 random unitaries with independent standard-normal coefficients and reports average Choi-state fidelity for the tested inverse protocols. This is finite Monte Carlo average-fidelity evidence; it is not a per-instance worst-case guarantee, a uniform Hamiltonian guarantee, or a diamond-norm bound. The repository still does not contain tracked TeX/Bib/PDF source for the manuscript or a separate supplementary source, so no such files are claimed to have been revised.

### Next highest-value action

Find an explicit finite rational decimal t>0 on the uniform ray and independently certify S_192(exp(t K_*))>0 with Arb. This would turn the nonconstructive dense-orbit existence corollary into a directly replayable physical path witness. Afterward, the main theoretical problem remains the full continuous-family minimax question, followed by a rigorous bridge from moment residuals to Choi infidelity and diamond distance.


### Explicit finite uniform-path escape (2026-11-24)

The nonconstructive dense-torus corollary has now been strengthened to an explicit physical witness. A deterministic differential-evolution search over t in [0.001, 10^3], [10^3, 10^4], and [10^4, 10^5] selected

\[
t=14425.249926691145447
=\frac{14425249926691145447}{10^{15}}>0.
\]

The independent 128-bit Arb verifier reconstructs the exact uniform-path torus rotation from the algebraic frequencies \(\omega_k=4\cos(k\pi/43)\) and the exact real orthogonal basis, then checks the same 61 active rows of the rationalized 192-column dual. It certifies

\[
S_{192}(e^{tK_*})
\in[0.468498256538894200560432299886
\pm2.83\times10^{-31}]>0.
\]

This is a directly certified finite physical path with all 41 couplings equal to t. It is outside the 192-column pool because all 192 listed columns have strictly negative Arb-certified pricing. The result refutes this particular 192-column dual as a separator of the continuous positive-coupling family; it does not invalidate the finite 192-column minimax theorem or settle full-family feasibility.

Evidence:
- Search: evidence/192col_uniform_ray_time_search_n21.json
- Arb: evidence/192col_uniform_ray_time_arb_n21.json
- Search script: discover_192col_uniform_ray_time_escape.py
- Arb verifier: verify_192col_uniform_ray_time_arb.py
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45221238345
- Evidence commit: c61fca25cfe6dcc6d13b76429e10c533c907f71f

The finite-time workflow completed the search and Arb-verification steps successfully; artifact upload was still finishing when this audit entry was written. The next action is to append this path as column 193 and reoptimize the same 2,113-row minimax LP.


### 193-column LP after adding the explicit uniform-ray path (2026-11-24)

The exact finite uniform-ray witness at t=14425.249926691145447 was appended as physical column 1650. The 193-column reoptimizer uses the explicit 21-torus spectral representation for the new path and uses that same rotation consistently for low-, sixth-, and eighth-order features. Its binary64 orthogonality defect is 5.21e-15.

The 193-column / 2,113-row HiGHS discovery reports objective 0.4348371573809519, independently recomputed maximum residual 0.4348371573809968, support size 63, and floating primal-dual gap 8.60e-15. Block maxima are 0.43483715738095197 (low), 0.4348371573809968 (sixth), and 0.4348371573809675 (eighth). These remain numerical LP diagnostics, not a theorem.

The exact rationalization and independent 128-bit Arb verifier completed successfully in workflow 45223141522. All 193 column inequalities were strictly certified, with maximum shifted upper endpoint -5.7674808073103104e-11. The exact lower bound is 78333298379892089605752391/180143985094819840000000000 = 0.43483715728094335... > 1/3. The formal theorem is in THEORY_193COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md.

Evidence:
- Reoptimizer workflow 45222472885: success.
- LP transcript: evidence/joint_low_six_eighth_lp_193col_uniform_ray_escape_n21.json.
- Reoptimizer commit: 498908b93d0f35b7c74005e4dfff913dd9dadea1.
- Stable spectral-consistency fix: d005b6ce6264f848793203aa1a379a6ef2906b5b.
- Exact dual verifier: verify_193col_uniform_ray_dual_arb.py.
- Arb workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45223141522 (pending at audit time).

The next action is to finish exact 193-column dual certification; no continuous-family conclusion follows from this finite 193-column LP alone.


### 193-column exact minimax theorem (2026-11-24)

The 193-column rational dual is now fully certified. Its exact values are:

- dual L1 norm: 18446744073709358785/18446744073709551616 < 1;
- dual objective: 8021329755945624383/18446744073709551616;
- strict slack: 1/10^10;
- certified lower bound: 78333298379892089605752391/180143985094819840000000000 = 0.43483715728094335... > 1/3;
- active support: 63 entries (2 low-order, 59 sixth-order, 2 eighth-order);
- Arb checks: 193/193 column intervals, all strictly negative after slack;
- maximum shifted upper endpoint: -5.7674808073103104e-11.

This is a theorem for exactly 193 physical columns and the fixed 2,113-row mixed-order design. It is not a theorem for the full 1,641 canonical inventory or the continuous path family. The uniform path at t=14425.249926691145447 is included as column 1650 and evaluated from the same spectral torus rotation for all moment orders.

Evidence:
- Theory: THEORY_193COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md
- LP: evidence/joint_low_six_eighth_lp_193col_uniform_ray_escape_n21.json
- Arb certificate: evidence/55probe_193col_uniform_ray_escape_dual_certificate_n21.json
- LP SHA256: 92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981
- Arb workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45223141522 (success)
- Certificate commit: 0bf2b18708f278968163700a718a90fdb413ec0e
- Theory commit: aca202be86de571204591e99f32261ff5c8c64e9

The next decisive action is to search the new 193-column dual over the exact uniform-path 21-torus and then the 41-dimensional positive path family. A positive Arb pricing witness would yield another physical escape; failure of finite searches is not a global separation proof.


## 2026-11-24: strict uniform-torus escape of the 193-column dual

The newly certified 193-column rational dual was evaluated over the exact 21-dimensional torus that is the closure of the uniform positive-coupling path. A deterministic 12-start L-BFGS-B search (120 iterations/start) found an exact-decimal phase vector. The independent 128-bit Arb verifier certifies

\[
S_{193}(R(\theta_*))
\in[3.042070453078681243432558976616809
\pm4.22\times10^{-34}]>0.
\]

The phase-vector SHA256 is
\[
\texttt{115a8091de0d2d8b18136c8e74823adb2e5771d70e9270120c39248158962c25}.
\]
The verifier pins the 193-column dual SHA256
\[
\texttt{70c0ab689e7112c70a10eb75d051b43c686d3b6656d4aed37238f10ee5516799},
\]
LP transcript SHA256
\[
\texttt{92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981},
\]
and cut-design SHA256
\[
\texttt{d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f}.
\]

The exact positive interval is the proof. The recorded analytic-gradient regression has maximum relative defect \(4.1551\times10^{-10}\); this is only an implementation check. By the proved rational independence of the 21 frequencies and Kronecker density, continuity implies existence of a finite t>0 such that \(S_{193}(e^{tK_*})>0\). This refutes global separation by this particular 193-column dual only. It does not invalidate the finite 193-column theorem, establish full-family feasibility/infeasibility, complete sixth/eighth orbit control, or provide a Choi/diamond guarantee.

Formal proof: THEORY_193COL_UNIFORM_RAY_DUAL_ESCAPE.md.

Evidence:
- Search: evidence/193col_uniform_torus_search_n21.json
- 128-bit Arb certificate: evidence/193col_uniform_torus_arb_n21.json
- Search script: discover_193col_uniform_torus_pricing.py
- Independent verifier: verify_193col_uniform_torus_pricing_arb.py
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45223892005
- Evidence commit: 6b8cabddaad3648323343fd8fbc1b671afc2d18f

A separate deterministic one-dimensional search over four bounded ranges \(t\in[10^{-3},10^3]\), \([10^3,10^4]\), \([10^4,10^5]\), and \([10^5,10^6]\), followed by an independent 128-bit Arb verifier, is now running in workflow 45224963117. No explicit finite decimal t is claimed until its Arb interval is strictly positive.


### Explicit finite uniform-ray escape of the 193-column dual (2026-11-24)

The nonconstructive dense-torus existence result has now been converted into an explicit physical witness. A deterministic differential-evolution search over four ranges \(t\in[10^{-3},10^3]\), \([10^3,10^4]\), \([10^4,10^5]\), and \([10^5,10^6]\) selected
\[
t_*=588.216987832015661
=\frac{588216987832015661}{10^{15}}>0.
\]
All 41 edge couplings are exactly this same positive rational decimal.

The best binary64 discovery score is 0.44956324068536085. This is not the proof. The independent 128-bit Arb verifier reconstructs the exact uniform-ray matrix from the algebraic frequencies and exact Q basis, then evaluates the 63 active rows of the rationalized 193-column dual. It certifies
\[
S_{193}(e^{t_*K_*})
\in[0.44956324068539347204794614417071
\pm8.33\times10^{-33}]>0.
\]
The exact rational time is \(588216987832015661/10^{15}\). The certificate pins dual SHA256 70c0ab689e7112c70a10eb75d051b43c686d3b6656d4aed37238f10ee5516799, LP SHA256 92931c1a8bad949d03cc11376c98c4d0166a8aae96060e6d76c991415af76981, torus certificate SHA256 178157fed1779e80fb89091662ac79e9c7a99e9331ebb4c176e96434fd3b05f5, and phase-vector SHA256 115a8091de0d2d8b18136c8e74823adb2e5771d70e9270120c39248158962c25.

This is a directly Arb-certified finite physical path with all 41 couplings equal. Since the 193-column certificate proves strictly negative pricing for all 193 listed columns, the new path lies outside the pool and refutes this particular dual as a separator of the continuous positive-coupling family. It does not invalidate the finite 193-column theorem or settle continuous-family feasibility/infeasibility.

Evidence:
- Search: evidence/193col_uniform_ray_time_search_n21.json
- Arb: evidence/193col_uniform_ray_time_arb_n21.json
- Search script: discover_193col_uniform_ray_time_escape.py
- Independent verifier: verify_193col_uniform_ray_time_arb.py
- Workflow [45224963117](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45224963117): success, including parent-dual and torus re-certification, finite-time search, independent Arb verification, artifact commit, and upload.
- Evidence commit: 5d9bc186a82d4b331930069764344e14367ea55c

The next action is to append this path as physical column 1651 and reoptimize the same 2,113-row LP.


## 2026-11-24: 194-column finite-pool minimax obstruction

The explicit uniform path at \(t=588.216987832015661\), with all 41 edge couplings equal, was appended as physical column 1651. Reoptimization of the same 2,113-row mixed-order design gave binary64 objective 0.4317007129307349 and independently recomputed maximum residual 0.4317007129309698. These are discovery diagnostics only.

An exact rational dual was reconstructed and independently checked by 128-bit Arb against all 194 physical columns. It has
\[
\|z\|_1=\frac{1152921504606836423}{1152921504606846976}<1,
\qquad
\delta=10^{-10},
\]
and proves
\[
\eta_{194}\ge
\frac{4860517923600091274798001}
{11258999068426240000000000}
=0.4317007128307263\ldots>\frac13.
\]
The maximum shifted column-LHS Arb upper endpoint is \(-7.63322083947767\times10^{-11}<0\). The 65 nonzero dual coordinates comprise 2 low-order, 61 sixth-order, and 2 eighth-order rows.

The new column 1651 is nearly active but still strictly certified: its raw dual-LHS interval is approximately \(-3.46880890753216023\times10^{-14}\pm1.96\times10^{-32}\). This is a strict negative interval, not a numerical zero.

The 194-column theorem covers exactly the 194 listed physical columns and the fixed 2,113-row design. It does not prove separation of the full canonical inventory or continuous positive-coupling family, complete sixth/eighth orbit control, or a Choi/diamond operational guarantee.

Formal proof: THEORY_194COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md.

Evidence:
- LP: evidence/joint_low_six_eighth_lp_194col_uniform_ray_escape_n21.json
- 128-bit Arb: evidence/55probe_194col_uniform_ray_escape_dual_certificate_n21.json
- Reoptimizer: reoptimize_194col_uniform_ray_escape.py
- Verifier: verify_194col_uniform_ray_dual_arb.py
- Workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45226334693
- Evidence commit: 1c10c6c7a796999448430d6ef9a8141e52b1112c

The next test is to price the 194-column dual over the exact 21-dimensional uniform-path torus. A positive Arb point would refute global separation by this particular dual only; absence of a point in a finite search would not prove global separation.


## 2026-11-24: strict uniform-torus escape of the 194-column dual

A deterministic 12-start L-BFGS-B search over the exact 21-dimensional uniform-path torus found an exact-decimal phase vector for the rationalized 194-column dual. The independent 128-bit Arb verifier certifies
\[
S_{194}(R(\theta_*))
\in[4.165518912347934438721938898592883
\pm7.17\times10^{-34}]>0.
\]
The exact phase-vector SHA256 is
\[
\texttt{f45e6dc6d84e196e9989351d5901dd2a694b7dda8cedb0ca98da69acfaddbdce}.
\]
The verifier pins 194-column dual SHA256
\[
\texttt{7864da033a71d7d2666cde32cf7f900c9a9a30893cbc7b90942fa09517cab474},
\]
194-column LP SHA256
\[
\texttt{c6dec42436d0181a9ff5012153d1896f4fcb0ca8a28cf39c6cdb321440dd7a66},
\]
and both preceding uniform-ray time certificates. The gradient regression defect is \(5.0922\times10^{-10}\), an implementation check only; the proof is the strictly positive Arb interval.

By rational independence of the 21 frequencies and continuity, this proves existence of a finite \(t>0\) with \(S_{194}(e^{tK_*})>0\). This refutes global separation by this particular 194-column dual only. It does not invalidate the finite 194-column minimax theorem or establish full-family feasibility/infeasibility.

Formal proof: THEORY_194COL_UNIFORM_RAY_DUAL_ESCAPE.md.

Evidence:
- Search: evidence/194col_uniform_torus_search_n21.json
- 128-bit Arb: evidence/194col_uniform_torus_arb_n21.json
- Search script: discover_194col_uniform_torus_pricing.py
- Verifier: verify_194col_uniform_torus_pricing_arb.py
- Successful workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45227944554
- Evidence commit: 2972334d665c4882060cd887277cc4a0ec1e364c

Superseded by the 2026-11-24 update below: the explicit finite-time uniform-ray witness is now Arb-certified; the next finite-pool test is the 195-column reoptimization.


## 2026-11-24 update: explicit finite 194-column uniform-ray escape certified

The exact 194-column dual has an explicit finite equal-coupling path that escapes its separator. The bounded search found
\[
t_*=5918.073474550670653
=\frac{5918073474550670653}{10^{15}}>0,
\]
with all 41 edge couplings equal to \(t_*\). The independent python-flint 0.8.0 / Arb verifier at 128-bit precision certifies
\[
S_{194}(e^{t_*K_*})
\in[0.533171018619275430607761736493\pm5.01\times10^{-31}]>0.
\]
The exact certificate pins the 194-column dual SHA256 `7864da033a71d7d2666cde32cf7f900c9a9a30893cbc7b90942fa09517cab474`, LP SHA256 `c6dec42436d0181a9ff5012153d1896f4fcb0ca8a28cf39c6cdb321440dd7a66`, and torus certificate SHA256 `aa5c6abb839f7cdb91175db6fef519dc66246e970dfd2de122440a9cc3a3a292`. Evidence is committed in [30b7145](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/30b7145063d63f664a2dc7b24ac599b826f2429c); the complete corrected workflow [45230548697](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45230548697) passed all steps.

The first workflow attempt [45228501706](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45228501706) had a verifier-only NameError before evaluating the candidate. Six references were corrected in [60dd9a5](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/60dd9a523de4a774c93e1272cc1309c2614f506e), after which the full independent Arb run succeeded.

This result refutes only global separation by this particular 194-column dual. It does not invalidate the finite 194-column / 2,113-row minimax theorem, prove feasibility or infeasibility of mixtures over the full continuous family, complete the selected sixth/eighth orbit audit, or establish a Choi-infidelity/diamond-distance operational guarantee. The next decisive finite-pool test is to append this path as physical column 1652 and reoptimize the same 2,113-row design.

## 195-column minimax theorem and uniform-torus escape (2026-11-24)

The 195-column / 2,113-row mixed-order LP has an exact rational dual independently checked by 128-bit Arb against all 195 listed physical columns. It proves
\[
\min_{p\in\Delta_{195}}\|A_{195}p-y\|_\infty
\ge
\frac{2803294808039097361653228789}
{6588122883467712110000000000}
=0.42550736493906444\ldots>\frac13.
\]
The dual has exact \(\|z\|_1=1\), slack \(10^{-10}\), and maximum shifted column-LHS upper endpoint \(-7.804834406606967\times10^{-11}<0\). Its 64 active coordinates comprise two low-order, 61 sixth-order, and one eighth-order row. The finite-pool theorem applies only to these 195 columns and the pinned 2,113-row design. The successful reoptimization/Arb workflow is [45242902521](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45242902521).

The exact 195-column dual was then priced on the 21-dimensional uniform-path torus. The independent 128-bit Arb certificate proves
\[
S_{195}(R(\theta_*))
\in[4.483867316010550697286473341089799
\pm8.75\times10^{-34}]>0.
\]
The exact-decimal phase vector SHA256 is `dfa636c9dfe1d1d7ddf64667383ec343f65103bf32f2f30f07711b73438b33c7`; the dual and LP SHA256 values are respectively `8371f7f2d4d866839b223dbe1b0c3e872a220092bc22b7cbc69384f08acb456c` and `0d5b2d821b95e3229b3ffbcbfd3dafacd80cb76ba1aba55e2858183d53792908`. By the previously proved rational independence of the uniform-path frequencies and continuity, some finite positive equal coupling exists that escapes this particular 195-column dual. The finite 195-column theorem is unchanged.

Formal write-up: `THEORY_195COL_UNIFORM_TORUS_DUAL_ESCAPE.md`. Evidence: `evidence/195col_uniform_torus_search_n21.json` and `evidence/195col_uniform_torus_arb_n21.json`; evidence commit [f456ab0](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f456ab02a4b49ade64b7a04a06bd4b33a2b78bcf).

A separate explicit finite-time search and Arb verifier have now been added:
- `discover_195col_uniform_ray_time_escape.py`;
- `verify_195col_uniform_ray_time_arb.py`;
- `.github/workflows/eui-195col-uniform-ray-time-escape.yml`.

The workflow is responsible for re-certifying the 194-column parent dual/time, the 195-column dual, and the 195-column torus witness before searching and checking any exact-decimal time. No explicit finite decimal time is claimed until its own Arb interval is strictly positive.

**Scope remains limited:** the 2,113-row design uses 1,461 complete low-order rows, 645 selected/cut sixth-order rows, and seven selected eighth-order rows. This is not a complete sixth/eighth orbit certificate, not a full continuous-family minimax theorem, and not a Choi/diamond operational guarantee.


## Current EUI status addendum (2026-11-24)

### Explicit finite-time escape of the 195-column dual

The fourth equal-coupling ray point in this sequence is now explicit and independently certified. For all 41 path edges,
\[
c_j=t_*=\frac{2901925271922439151}{500000000000000}
=5803.850543844878302>0.
\]
The 128-bit Arb interval for the exact 195-column dual pricing functional is
\[
S_{195}(e^{t_*K_*})
\in[0.5056904994276359992460690567385\pm9.35\times10^{-32}]>0.
\]
The evidence files are evidence/195col_uniform_ray_time_search_n21.json and evidence/195col_uniform_ray_time_arb_n21.json, committed at 133d9c937d465bdd457a3ac8257c9b7a203caed7. The certificate pins the 195-column dual and LP hashes, and the prior 195-column torus certificate. The formal finite-pool theorem is unchanged: this positive point is outside the 195-column pool and only refutes global separation by that particular dual.

### 196-column decisive follow-up

The exact path above is appended as physical column 1653. A deterministic 196-column / 2,113-row reoptimizer, independent rational-dual Arb verifier, and GitHub Actions workflow have been added:
- reoptimize_196col_uniform_ray_escape.py;
- verify_196col_uniform_ray_dual_arb.py;
- .github/workflows/eui-reoptimize-196col-uniform-ray.yml.

The workflow re-certifies the 193-, 194-, and 195-column parent/time chain, reconstructs all four uniform paths using the explicit 21-torus spectral representation, and checks the 196-column dual if the new HiGHS discovery remains above \(1/3\). The workflow result has not yet been independently observed in this audit; no 196-column numerical or theorem claim is made here.

### Manuscript-level limitation remains

The original Appendix B's finite 10,000-Hamiltonian mean Choi-fidelity experiment is empirical average evidence for its sampling distribution. It is not a worst-case-over-Hamiltonian or worst-case-over-input guarantee. The present 2,113-row design still contains selected/cut sixth-order rows and seven selected eighth-order rows, not the complete higher-order orbit inventory. No theorem currently connects its moment residual to a per-instance Choi infidelity or diamond distance. These are separate open tasks and must not be inferred from the finite-pool dual sequence.


## Core theorem map and long-ring publication blocker (2026-11-24)

The highest-value route to a full minimax result is not another finite-pool residual alone. The repository contains three complementary results:

1. The exact physical program-span theorem holds for every odd cycle length. It identifies the balanced Majorana labels as the full physical span for the fixed encoder and gives a physical fixed-recovery error floor.
2. The radial-recovery theorem gives an exact physical-family supremum and a radial minimax-optimal decoder.
3. The joint-parity diamond converse upgrades the radial value to a full diamond minimax theorem against arbitrary orientation-dependent non-radial stochastic Pauli corrections, conditional on one legal physical ensemble having exactly uniform diagonal program masses in both parity sectors. Its positive physical ensembles are interval-certified at n=5 and n=7.

For admissible long rings n>=21, the third theorem remains conditional. The all-moment physical ensemble is the missing hypothesis. The exact principal-minor criterion is
\[
\mathbb E\det R_{I,I}
=(-1)^{v(I)+k}\frac{\binom nk}{\binom{2n}{2k}},
\qquad |I|=2k,
\]
for every even subset modulo complement. A zero edge in every seed makes the two parity-sector program masses identical by the gap/gauge lemma. The complement-folded projection-DPP representation supplies a positive determinant formula and a sampler, but not an exact long-ring construction.

Known exclusions are deliberately limited: mixtures of single perfect-mirror segments are excluded for every odd n>=5; at n=21, mixtures of at most two disjoint perfect-mirror segments are excluded by an exact fourth-order separator. Fractional-transfer seeds escape the latter functional numerically. Arbitrary gapped couplings, three-plus segments, and all-moment positive ensembles remain open.

The n=21 low-moment repair certificates and later LP candidates are not full joint ensembles: the 83-orbit repair is only approximate in low moments and has a sixth relative error above one; the 29-column candidate has a strict seventh eighth-order violation; later 32-/34-/35-column reweights have candidate-specific sixth-order separators. These are finite candidate results, not global no-go statements.

**Manuscript decision:** the conditional joint-parity theorem, all-odd program-span theorem, and radial-recovery theorem form a coherent core result. The n>=21 exact positive ensemble or a global physical obstruction is the principal missing theorem. The 195/196-column mixed-order LP sequence is supporting finite-pool evidence and must not be presented as a substitute for the all-moment hypothesis or as an operational channel-error theorem. The original Appendix B's 10,000-sample mean Choi-fidelity experiment remains average empirical evidence, not a worst-case channel guarantee. No manuscript TeX/PDF source is present in the repository.


## 196-column finite-pool theorem (2026-11-24)

The exact fourth equal-coupling path from the 195-column dual escape was appended as column 1653. The resulting 196-column / 2,113-row LP remains above the \(1/3\) cap. Its binary64 discovery objective is \(0.41973861363658294\), and the recomputed maximum residual is \(0.4197386136366168\).

An independent 128-bit Arb dual certificate is complete for all 196 columns. It gives
\[
\eta_{196}\ge
\frac{18903346635163739503488879}{45035996273704960000000000}
=0.41973861353658526\ldots>\frac13.
\]
The exact dual has \(L_1\) norm
\[
\frac{4611686018427369049}{4611686018427387904}<1,
\]
slack \(10^{-10}\), and 63 active rows (5 low, 57 sixth, 1 eighth). The verifier reports a maximum shifted column-LHS upper bound of \(-4.4216806140854604\times10^{-11}\); the certificate stores all 196 column intervals. Evidence commit: 3ef1287d4dcecc7bdf21cc5cbf4efaf09f33cecf.

Formal note: THEORY_196COL_2113ROW_FOURTH_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md. Evidence: evidence/joint_low_six_eighth_lp_196col_uniform_ray_escape_n21.json and evidence/55probe_196col_uniform_ray_escape_dual_certificate_n21.json.

This remains a finite-pool theorem for exactly 196 listed columns and the selected 2,113 rows. It does not separate the full continuous physical family, and it is not a complete sixth/eighth-order or operational Choi/diamond certificate.

A new deterministic 21-dimensional torus pricing search and independent Arb verifier for the 196-column dual have been added:
- discover_196col_uniform_torus_pricing.py;
- verify_196col_uniform_torus_pricing_arb.py;
- .github/workflows/eui-196col-uniform-torus-pricing.yml.

The search result is not yet observed in this audit. A positive exact Arb phase interval would imply a finite equal-coupling escape for this 196-column dual by continuity and the already-proved Kronecker density; a finite multistart failure would not prove global separation.



## 196-column uniform-torus escape (2026-11-24)

The 196-column finite-pool theorem remains valid for its exact 196 listed columns and 2,113 selected rows, with certified lower bound
\[
\eta_{196}\ge0.41973861353658526\ldots>1/3.
\]
A separate exact pricing test now shows that this same dual is not a separator of the full continuous physical family. The 21-dimensional torus search found a rational-decimal phase vector; an independent 128-bit Arb verifier certifies
\[
S_{196}(R(\theta_*))
\in[1.5804582969205441019413585480859926
\pm4.77\times10^{-35}]>0.
\]
The phase-vector SHA256 is \texttt{07ef5b4a57de7be1ac1ec0d7aded62b86fadecf2dc4cf4caa6c0a9b4ebfee6b8}. The verifier pins dual SHA256 \texttt{45edad15fc5978381108c9ade57006da941c476e05cb447c044fbe4ed986cd86} and LP SHA256 \texttt{d203f3cddd74b896f565d44509168f11a39b814b5f5de8fe1f99a89d26c2e179}. It re-certified the 193-, 194-, and 195-column parent/time chain and the 196-column finite-pool dual before evaluating the candidate. Successful workflow: [45282545933](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45282545933).

By the proved rational independence of \(\omega_k=4\cos(k\pi/43)\), the positive uniform-coupling ray is dense in the torus. Continuity therefore implies that some finite \(t>0\), with all 41 couplings equal to \(t\), has positive 196-column pricing. This is a rigorous **existence** result, not yet an explicit decimal time. It refutes global separation by this particular dual only. It does not invalidate the finite-pool theorem, establish full-family mixture feasibility/infeasibility, or imply a Choi/diamond operational guarantee.

Formal note: [THEORY_196COL_UNIFORM_TORUS_DUAL_ESCAPE.md](THEORY_196COL_UNIFORM_TORUS_DUAL_ESCAPE.md). Evidence: [search transcript](evidence/196col_uniform_torus_search_n21.json), [128-bit Arb certificate](evidence/196col_uniform_torus_arb_n21.json). The first verifier run exposed a provenance-check bug: it expected a nonexistent \texttt{parent_194col_uniform_ray_time_exact_rational} field in the 195-column time certificate. The verifier was corrected to load the 194-column certificate itself and check its raw-file hash, LP/dual ancestry, and exact rational time. The corrected workflow passed all parent checks and the Arb evaluation. Workflow hygiene was also tightened so stale outputs are removed immediately after checkout, before any potentially failing verification step.

**Next:** search the one-dimensional uniform ray for an explicit finite \(t\), then certify that exact rational-decimal time with Arb. A failed bounded search would not negate the density-based existence theorem. In parallel, the publication-critical long-ring joint-parity ensemble and the moment-to-operational-error bridge remain open; the 196-column sequence is supporting finite-pool/dual-pricing evidence, not a replacement for either theorem.


## 196-column explicit uniform-ray escape (2026-11-24)

The previous 196-column status is superseded by a completed deterministic search and independent 128-bit Arb verification. For the exact rational 196-column dual pinned by SHA256 45edad15fc5978381108c9ade57006da941c476e05cb447c044fbe4ed986cd86 and LP SHA256 d203f3cddd74b896f565d44509168f11a39b814b5f5de8fe1f99a89d26c2e179, the explicit uniform positive-coupling path is
\[
t_*=3070.785790481181266=\frac{1535392895240590633}{500000000000000},\qquad c_0=\cdots=c_{40}=t_*.
\]
The 128-bit Arb pricing interval is
\[
S_{196}(e^{t_*K_*})\in[0.3637338868622431662555343998069\pm6.07\times10^{-32}]>0.
\]
This is a directly specified physical path, not merely the dense-torus existence argument. It proves that this particular 196-column dual is not a global separator of the continuous physical family. It does not invalidate the 196-column/2,113-row finite-pool minimax theorem and does not prove feasibility or infeasibility of mixtures over the full continuous family.

Reproduction: evidence/196col_uniform_ray_time_search_n21.json, evidence/196col_uniform_ray_time_arb_n21.json, and verify_196col_uniform_ray_time_arb.py; [workflow 45283332130](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45283332130), [evidence commit 6e6a670](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6e6a6705fd44b85b1274132d7530796145c7b3a1).

The higher-level long-ring blocker remains the exact positive joint-parity ensemble at n=21 (or a global physical obstruction). The existing 22-atom ensemble is certified only for all 21 distance-averaged second moments plus one fourth-order orbit; a distant fourth-order probe fails by more than 1/100. The conditional joint-parity diamond theorem therefore remains conditional at n=21.


## n=21 single-fractional-atom extension test (2026-11-24)

The 22-atom low-moment ensemble has a certified distant fourth-probe residual
\[
\Delta_0=0.0129392316409538071962346592130359334639942998783638688669442\ldots>0.
\]
I tested the 27 previously absent seeds in the grid \(L\in\{10,21,30,41,42\}\), \(\alpha\in\{1/8,1/4,1/2,3/4,5/4,3/2\}\). For each candidate, the exact affine reweighting formula preserves the 21 distance-averaged second moments, the consecutive fourth probe, and normalization while solving for the one new weight that would repair the distant probe. At the 384-bit Arb stage, 25 candidates require a strictly negative new weight; two slope intervals contain zero and were left unresolved pending the higher-precision/analytic check below. No positive single-atom extension was certified on this finite grid.

The particularly relevant length-41, \(\alpha=5/4\) fractional seed, which numerically escapes the perfect-two-mirror separator, has certified positive affine slope about \(0.0974547302469660\), hence a negative required weight about \(-0.1327717147044962\). It cannot repair this distant probe alone while preserving the base constraints.

Evidence and exact affine derivation: [THEORY_LOW_MOMENT_FRACTIONAL_SINGLE_ATOM_SCREEN_N21.md](THEORY_LOW_MOMENT_FRACTIONAL_SINGLE_ATOM_SCREEN_N21.md), [384-bit Arb JSON](evidence/ising_low_moment_fractional_extension_n21.json), [successful workflow 45299958866](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45299958866).

This intermediate paragraph records the initial single-atom screen. The subsequent analytic resolution and multi-atom corollary below strengthen the result to every nonnegative mixture of any subset of the same 27 grid atoms. Continuous fractional parameters outside the grid and general gapped couplings remain open; the n=21 joint-parity diamond theorem remains conditional.


### Analytic resolution of the two zero-slope candidates

The two cases whose 768-bit Arb intervals still contain zero are exact redundancies, not unresolved directions. A length-\(L\) fractional open path is the spin-\(j=(L-1)/2\) rotation \(R_{L,\alpha}=\exp(\alpha\pi J_y^{(j)})\). For \(L=41\), integer spin \(j=20\) gives \(R_{41,3/2}=R_{41,1/2}^{\mathsf T}\). For \(L=42\), half-integer spin \(j=41/2\) gives \(R_{42,5/4}=-R_{42,3/4}^{\mathsf T}\); the global minus sign disappears in every even-order principal minor. Thus both candidates have exactly the same all-even-minor feature columns as seeds already present in the 22-atom ensemble.

Consequently the full 27-seed grid is accounted for: 25 candidates require strictly negative new weights, and two are exact duplicate feature columns. No positive single-atom extension exists on this finite grid. The next paragraph strengthens this to a finite-grid multi-atom convex-cone obstruction, but not to a general obstruction for arbitrary gapped ensembles. See the [spin-identity proof](THEORY_LOW_MOMENT_FRACTIONAL_SINGLE_ATOM_SCREEN_N21.md) and [768-bit Arb consistency certificate](evidence/ising_low_moment_zero_slope_refinement_n21.json).


The sign pattern also gives a multi-atom corollary. For any nonnegative weights \(\tau\) on any subset of the 27 grid atoms, preserving the base 22 constraints forces old weights \(p-M^{-1}V\tau\), and the distant residual becomes \(\Delta_0+\sum_j\sigma_j\tau_j\). Since all 25 nonduplicate slopes are strictly positive and the two duplicate slopes are exactly zero, this residual is at least \(\Delta_0>0\). Thus no nonnegative mixture of any subset of this finite fractional grid repairs the distant probe while preserving the base constraints. This remains a finite-grid obstruction only.


## 2026-11-24: positive 41-atom n=21 two-fourth-probe ensemble

A deterministic 8,241-column fractional-path discovery (all lengths L=2,...,42 and alpha=k/100, k=0,...,200) found a multi-atom repair of the 22-atom design's distant fourth-order residual. The independent 384-bit Arb verifier certifies a 41-atom physical ensemble (the 22 base atoms plus 19 fractional open paths) with every weight strictly positive. It preserves all 21 distance-averaged second moments and matches both q_{0123}=1/533 and q_{0,2,21,23}=1/533 exactly.

The exact interpolation factor is
\[
\gamma=0.86839903706115658184287441518140630184539297518602\ldots,
\]
and the minimum final weight is
\[
0.000110852097544644610007668601156342369587115893874\ldots>0.
\]
The 384-bit certificate reports all 21 second-moment residual intervals and both fourth-probe residual intervals containing zero. It also certifies strict failures for q_{0,1,2,4} and q_{0,10,20,30}; this is not a complete fourth-order design.

A separate 384-bit Arb Farkas certificate covers the 861-seed coarse grid L=2,...,42, alpha=k/10 and proves no nonnegative mixture from any subset of that finite grid can repair the distant probe while preserving the base constraints. Its dual cost is 0.01199999912229604678... versus base residual 0.01293923164095380719..., with minimum candidate dual slack 0.00147717709277052838... . The positive construction uses the finer 0.01 grid and therefore does not contradict the coarse-grid theorem. Both finite-grid results are strictly scoped; neither is a continuum no-go.

Evidence:
- [theory and exact affine proof](THEORY_LOW_MOMENT_TWO_FOURTH_PROBE_ENSEMBLE_N21.md)
- [discovery transcript](evidence/ising_low_moment_two_fourth_discovery_n21.json)
- [384-bit positive-ensemble certificate](evidence/ising_low_moment_two_fourth_ensemble_n21.json)
- [861-seed Farkas certificate](evidence/ising_fractional_grid_cone_n21.json)
- [successful exact workflow 45315065442](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45315065442)
- [evidence commit 69dfb15](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/69dfb15)

**Revised paper priority:** use the 41-atom ensemble as a warm start for column generation against all 1,440 fourth-order dihedral orbits. It does not yet satisfy all fourth-order moments, all sixth/eighth-order moments, or the all-even-principal-minor joint-parity condition. The conditional n=21 diamond theorem remains conditional.


## 2026-11-24: full fourth-order orbit screen of the 41-atom candidate

A deterministic floating audit evaluated all 111,930 four-subsets and all 1,440 dihedral fourth-order orbits of the Arb-certified 41-atom ensemble. It found 1,438/1,440 absolute residuals above 1e-8 and 720/1,440 relative absolute errors above 1/3. The largest midpoint residual is 0.0057556283852348965 at {0,10,20,30}. The 384-bit Arb ensemble certificate independently proves this probe's residual is strictly positive and the {0,1,2,4} residual strictly negative. The full-orbit counts and ranking are floating diagnostics, not interval proofs for every orbit.

- [full-orbit audit JSON](evidence/ising_low_moment_two_fourth_fourth_audit_n21.json)
- [audit script](audit_ising_low_moment_two_fourth_ensemble_fourth_orbits.py)
- [successful workflow 45315655489](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45315655489)
- [evidence commit 42d32b9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/42d32b9)

The 41-atom ensemble is a useful low-moment warm start, but it is far from a fourth-order uniform design. The next step remains full 1,440-orbit column generation, not a claim of near-complete joint parity.


## 2026-11-24 addendum: complete fourth-order finite-grid obstruction and one continuous cell

The full 1,440-orbit fourth-order target was tested against 6,123 physical columns (22 pinned base atoms plus 6,101 corrected fractional single-open-path seeds). A frozen 80-term rational separator has a 128-bit Arb certificate checking every column. For each column, the exact score gap y^T b - y^T a_j is strictly positive; hence no probability mixture on this exact finite pool satisfies the complete second-/fourth-order target. See [the certificate](evidence/ising_full_fourth_fractional_grid_dual_arb_n21.json), [the independent verifier](verify_ising_full_fourth_fractional_grid_dual_arb.py), and [the theory note](THEORY_FULL_FOURTH_FRACTIONAL_GRID_N21.md).

A stronger continuous-parameter step now certifies one full interval cell, not merely its sampled midpoint: for the length-40 fractional open path, every alpha in [1.835, 1.845] has separator gap strictly greater than 1/4. The 512-bit Arb certificate uses a degree-40 scalar Taylor model and an exterior-power operator-norm remainder; its certified lower gap endpoint is 0.2643780467418314563... . Evidence is [here](evidence/ising_full_fourth_continuous_alpha_cell_probe_n21.json), with reproducible code in [probe_ising_full_fourth_continuous_alpha_cell_n21.py](probe_ising_full_fourth_continuous_alpha_cell_n21.py).

These results remain sharply scoped. The finite-grid theorem excludes only the pinned 6,123-column pool. The continuous Taylor certificate covers only one L=40 alpha cell; the other cells and path lengths are not yet covered. Neither result is a global obstruction for arbitrary gapped couplings or multi-segment paths, and neither supplies the missing operational moment-to-Choi/diamond bridge. The repository still has no tracked manuscript TeX/Bib/PDF source; the public arXiv v1 remains the inspected manuscript reference.


## 2026-11-24 addendum: global continuous single-open-path obstruction

The latest result supersedes the earlier audit's description of continuous coverage as only a single \(L=40\) alpha cell. At commit [5979d33](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5979d33a58fe8fb247a23253a8b4fb1dcd6ead10), workflow [45350942797](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45350942797) completed a 512-bit Arb Fourier--Bernstein proof for all 41 path lengths \(L=2,\ldots,42\) and every real \(\alpha\in\mathbb R\). The certificate contains 4,389 exact-size Fourier samples, positive Bernstein leaves for every length, no unresolved leaves, and no negative witness. The 22 pinned base atoms were separately rechecked at 512 bits.

For the frozen 80-term rational separator, the global certified gap lower endpoint is \(0.02800447635786912086\ldots>0.028\). Its exact coefficient \(\ell_1\)-norm is \(1161904514761212958261/2305843009213693952<504\), yielding a uniform lower bound \(1/18000\) on the reduced second-/fourth-order moment residual infinity norm for every probability measure supported on the 22 pinned base atoms plus the full continuous single-open-path family.

This is a genuine continuum obstruction for that restricted family, not a finite-grid extrapolation. It does **not** cover arbitrary nonuniform gapped couplings, multi-segment paths, all even principal minors, or worst-case Choi/diamond error. The original manuscript's Appendix B remains average finite-sample Choi-fidelity evidence, not an operational worst-case theorem. The manuscript TeX/Bib/PDF source is still not tracked in this repository, so this addendum updates the research audit rather than a manuscript source.


The exterior-power Fourier representation also extends the single-path obstruction to every real scale \(\alpha\), not only \([0,2]\): for each \(L\), the score is \(P_L(\cos\theta_L(\alpha))\), and the Bernstein proof is uniform on the full domain \(\cos\theta\in[-1,1]\). The verifier is being strengthened with negative and out-of-period direct-evaluation checks before this all-real statement is promoted in the machine-readable certificate.
