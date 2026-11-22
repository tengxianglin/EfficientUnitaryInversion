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
