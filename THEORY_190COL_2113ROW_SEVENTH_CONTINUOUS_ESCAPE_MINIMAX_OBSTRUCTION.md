# 190-column, 2,113-row seventh-continuous-escape minimax obstruction

## Statement and scope

Let \(\mathcal P_{190}\) be the frozen physical pool consisting of 183 canonical paths (151 base columns and 32 canonical additions) and seven distinct exact-rational positive 41-edge open paths. The seven noncanonical paths are assigned labels 1641 through 1647. For each physical path, let \(a_j\in\mathbb R^{2113}\) be its normalized moment-feature column, and let \(y\in\mathbb R^{2113}\) be the fixed target vector.

The row inventory is unchanged from the preceding 189-column branch:

- 1,461 complete low-order rows: 21 second-order and 1,440 fourth-order rows;
- 645 selected/cut sixth-order rows;
- 7 selected eighth-order rows.

Thus \(A_{190}=[a_1\ \cdots\ a_{190}]\in\mathbb R^{2113\times190}\). The 645 sixth-order rows are a selected/cut inventory, not the complete set of 63,133 sixth-order dihedral orbits. The seven eighth-order rows are selected representatives, not the complete eighth-order orbit inventory.

**Theorem.** The exact rational dual certificate in `evidence/55probe_190col_seventh_continuous_escape_dual_certificate_n21.json`, independently verified with 128-bit Arb, proves
\[
\boxed{
\min_{p\in\Delta_{190}}\|A_{190}p-y\|_\infty
\ge
\frac{12786853125233436543275375237}
{28379606267246247630000000000}
=0.4505648529730001\ldots
>\frac13.
}
\]
The exact margin above one third is
\[
\frac{3326984369484687333275375237}
{28379606267246247630000000000}
=0.11723151963966673\ldots.
\]

This is a rigorous mixed-order minimax obstruction for every probability mixture over these **190 pinned physical generators** on this **fixed 2,113-row design**. It is not a theorem for the unrestricted continuous positive-coupling family.

## Physical-path convention

For a 42-site open path with couplings \(c=(c_0,\ldots,c_{40})\), define the real skew-symmetric generator
\[
K(c)_{j,j+1}=2c_j,\qquad
K(c)_{j+1,j}=-2c_j,\qquad j=0,\ldots,40,
\]
with all other entries zero, and \(R(c)=\exp K(c)\). Each of the seven appended paths has exact rational couplings \(c_j>0\) for all 41 edges; its 42nd stored terminal component is zero. The seven exact coupling vectors and their parent-certificate provenance are stored in the seven Arb escape transcripts referenced by the LP JSON.

The 190-column ordering is pinned in the LP transcript: the 151 base canonical columns, first continuous escape (1641), 32 canonical additions, then continuous escapes 2 through 7 (1642–1647). The frozen seed-pool SHA256 is `93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315`; the canonical inventory SHA256 is `f94a0ba43bcc7566705ff0bec3b6ab6b48b49a5ce29592173664e15a01c08d98`.

## Dual certificate

Write the exact rational dual vector as \(z\in\mathbb Q^{2113}\), and its equality multiplier as \(\lambda\in\mathbb Q\). The certificate records
\[
\|z\|_1=1,\qquad
\lambda=\frac{51573359187061440512}{36893488147420121919},
\]
and
\[
\lambda+z^Ty
=\frac{1278685312807139717}{2837960626724624763}.
\]
The exact slack is
\[
\delta=10^{-10}.
\]

The nonzero dual support has 58 coordinates: two fourth-order rows (zero-based row indices 233 and 1413), 54 sixth-order rows, and two eighth-order rows (indices 2106 and 2107). There is no second-order support. The full exact rational vector is included in the machine-readable certificate.

For each of the 190 physical columns, the independent verifier evaluates the exact path matrix and the active normalized moment features with Arb at 128-bit precision. Every interval for
\[
z^Ta_j+\lambda-\delta
\]
has a strictly negative upper endpoint. The largest (least negative) upper enclosure is reported as
\[
[-5.0646182194565139235048775368095553314\times10^{-11}
\ \pm\ 3.59\times10^{-49}]<0.
\]
The certificate contains exactly 190 column intervals and marks the audit complete.

## Proof

The Arb certificate establishes, for every \(j=1,\ldots,190\),
\[
z^Ta_j+\lambda\le\delta,
\qquad \|z\|_1=1.
\]
For any probability vector \(p\in\Delta_{190}\), convexity gives
\[
z^TA_{190}p+\lambda
=\sum_{j=1}^{190}p_j(z^Ta_j+\lambda)
\le\delta.
\]
Therefore
\[
z^T(y-A_{190}p)
\ge \lambda+z^Ty-\delta.
\]
By Hölder's inequality,
\[
\|y-A_{190}p\|_\infty
\ge \frac{|z^T(y-A_{190}p)|}{\|z\|_1}
\ge \lambda+z^Ty-\delta.
\]
Substitution of the exact rational values yields the theorem's lower bound. Since that rational number is strictly greater than \(1/3\), no probability mixture over the pinned 190-column pool can meet the one-third cap on the pinned design.

## Numerical discovery diagnostics (not the proof)

The binary64 HiGHS solve returned objective 0.45056485307304617, independently recomputed maximum 0.45056485307319294, support size 58, and primal-dual discovery gap \(3.375077994860476\times10^{-14}\). These are numerical diagnostics only; the theorem follows from the exact rational dual and Arb interval checks.

The LP matrix-plus-target SHA256 is `324900df03f4a09c8f04f5c30eee048d4b3e7daae214a9dadbffc9885e90c4cc`. The raw LP transcript SHA256 pinned by the dual is `2a4ca0caab7c7ed5dab24f07e51c121e03e49236da98cbc59809d96868e94307`.

## Reproducibility

- [190-column LP transcript](evidence/joint_low_six_eighth_lp_190col_seventh_continuous_escape_n21.json)
- [Exact dual and all 190 Arb column intervals](evidence/55probe_190col_seventh_continuous_escape_dual_certificate_n21.json)
- [Independent verifier](verify_190col_seventh_continuous_escape_dual_arb.py)
- [Reoptimizer](reoptimize_190col_seventh_continuous_escape.py)
- [Successful workflow 45151174105](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45151174105)
- Evidence commit [6236ce2](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/6236ce24a02ab7cb55c53cba3681430d048de5de)

The workflow re-certified the 189-column parent dual, all seven exact-rational continuous-path escape inputs, the frozen seed pool, and orbit-enumeration tests before solving. It compiled both new Python programs, solved the 190-column LP, and completed the independent Arb verifier.

## Explicit limitations

1. The theorem is for a fixed 190-generator pool. The seventh path itself strictly escapes the preceding 189-column dual; this does not establish feasibility or infeasibility for the entire continuous path family.
2. The objective contains 645 selected/cut sixth-order rows and seven selected eighth-order rows, not every sixth/eighth orbit. It is therefore a mixed-order finite-design theorem, not a complete sixth/eighth moment theorem.
3. No implication to Choi infidelity, entanglement fidelity, diamond distance, or a worst-case operational inversion guarantee is established here. A separate quantitative bridge is required.
