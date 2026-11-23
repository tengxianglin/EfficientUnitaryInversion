# Manuscript and supplementary-material audit (2026-11-22)

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
