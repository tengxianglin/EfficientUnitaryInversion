# EUI research audit — Run 58 (2026-11-27)

## Repository and issue selection

- Repository: \`tengxianglin/EfficientUnitaryInversion\`, default branch \`main\`.
- Starting HEAD observed: \`f9db95de9c20e09cabf0f27976d099505745edb1\`.
- Issue #7 remains the highest-leverage track for the positive physical-ensemble question. Issue #5 remains a separate finite-pool/global-converse track; Issues #6 and #3 remain independent manuscript-normalization and classifier tracks; Issue #4 is closed.
- Recent main commits, open issues, research notes, current evidence, workflow runs, and the public manuscript/appendices were inspected.

## Scientific result: N=42 ten-quartic partial ensemble

A 300,000-candidate NumPy 2.3.5 / SciPy 1.17.0 HiGHS discovery (seed 352, \([0,1000]^2\)) supplied a frozen support of 41 positive period-two base atoms. Each base atom \((a,b)\) is symmetrized with its one-site translate \((b,a)\), yielding 82 physical atoms.

The independent 256-bit Arb verifier and final workflow [45935129650](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45935129650) passed. The exact-real weights are reconstructed from the \(41\times41\) interval moment system. The determinant interval is
\`[-4.1090678188375528048...e-52 +/- 7.53e-118]\`,
which excludes zero. The minimum exact-real base weight is
\`[0.00121547137116687654968... +/- 7.34e-71] > 1/10000\`.
The minimum coupling is the exact rational
\`9135346810271617/1000000000000000\`.

The verifier certifies:
- weight sum one;
- all 861 unordered pair principal-minor coordinates equal \(-1/41\);
- all 399 distinct quartic coordinates in ten specified full translation orbits equal \(1/533\);
- all 42 translates of the next witness \([0,6,15,21]\) miss the target upward by strictly more than \(1/250\) for this frozen support.

The ten quartic representatives are
\`[0,1,2,3]\`, \`[0,3,10,15]\`, \`[0,2,4,6]\`, \`[0,10,20,30]\`, \`[0,2,21,23]\`, \`[6,13,14,30]\`, \`[0,3,19,26]\`, \`[0,8,20,28]\`, \`[0,4,8,12]\`, and \`[0,3,18,21]\`.
Their orbit sizes are \(42,42,42,42,21,42,42,42,42,42\).

This extends the previous nine-orbit partial ensemble from 357 to 399 quartic coordinates while preserving all 861 pair constraints. It remains a partial fourth-order design, not a complete fourth-order or all-even-moment ensemble.

## Reproducibility-gate repair

The first three ten-orbit workflow attempts failed before Arb because the discovery script compared binary64 support decimals by exact string equality. The mismatch was isolated to the 14th atom: the current HiGHS run returned \(a=663.2480645579019\), while the frozen rational decimal is \(663.2480645579014\); the other coordinate agreed. The difference is \(4.55\times10^{-13}\), not a support change.

The script now requires the same ordered support with maximum coordinate discrepancy at most \(10^{-9}\), records that discrepancy, and keeps the frozen exact decimal inputs authoritative for Arb. The final verifier wording was also corrected from “nine” to “ten” matched quartic orbits and from “tenth” to “eleventh” unmatched orbit.

Final CI [45935129650](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45935129650) passed all steps, including deterministic discovery, independent Arb certification, evidence commit, and artifact upload. The machine certificate scope string now explicitly says ten orbits.

## Finite-pool boundary

The discovery script enumerated all 2,670 quartic translation orbits (111,930 four-subsets) in binary64. The largest absolute residual for this support is approximately \(0.00468374467865546\) at \([0,6,15,21]\). Adding that eleventh orbit made the floating LP infeasible on the fixed 300,000-candidate pool.

This is finite-pool discovery only. There is no exact Farkas certificate for that infeasibility and no global period-two or full-physical-family no-go theorem. The Arb certificate proves only that this particular 82-atom support misses the next orbit.

## Manuscript and supplementary-source audit

The public manuscript remains Yin Mo, Tengxiang Lin, Xin Wang, *Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians*, [arXiv:2506.20570v1](https://arxiv.org/abs/2506.20570). I rechecked the HTML manuscript's main Sections II–VIII and Appendices A–E, including Appendix B lines 294–313 and its five-row average-Choi-fidelity table. Appendix B still defines \(\delta\) as a ratio of coefficient \(L_1\) sums while saying the raw \(\alpha_P,\beta_P\) are independently standard normal; Issue #6 remains the canonical tracker, and the full QuAIRKit table has not been regenerated.

Default-branch searches for \`documentclass\`, bibliography, and supplementary-source terms still find no editable tracked TeX/Bib manuscript or separate supplementary source. This run therefore adds a theory note and audit record, not a formal manuscript-body revision. No new claim about Choi trace distance or channel diamond distance is made.

## Changes, evidence, blockers, next action

- Added the ten-orbit theory statement and this audit record.
- Fixed the discovery support check to tolerate sub-\(10^{-9}\) floating basis variation while preserving exact frozen inputs.
- Corrected the verifier's certificate scope wording and reran the final CI successfully.
- Evidence: \`evidence/n42_period_two_ten_quartic_atoms.json\`, \`evidence/n42_period_two_ten_quartic_discovery.json\`, and \`evidence/n42_period_two_ten_quartic_ensemble_arb.json\`.
- Main code/evidence commits: \`8c458de\`, \`27b02bf\`, and \`32276c3\`.

Remaining blockers: the other 2,271 quartic translation orbits, higher even moments, a global continuous-family converse or full positive ensemble, and the operational moment-to-Choi/diamond bridge.

Next highest-value action: search for an 11-orbit positive support using a genuinely different or enlarged candidate-generation strategy, then independently certify it. Treat any finite-pool infeasibility only as a candidate generator for a dual, and price any proposed dual over the continuous period-two family before claiming an obstruction.
