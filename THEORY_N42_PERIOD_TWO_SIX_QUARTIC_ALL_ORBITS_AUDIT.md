# Complete fourth-order orbit audit of the N=42 period-two partial ensemble

Date: 2026-11-27. Frozen support:
[evidence/n42_period_two_six_quartic_atoms.json](evidence/n42_period_two_six_quartic_atoms.json).
This audit is candidate-specific; it is not a no-go theorem for the period-two family.

## 1. Question

The 37 positive period-two base atoms (a_l,b_l) from the six-quartic construction are paired with their one-site translates (b_l,a_l) at equal conditional weight. Their exact-real weights are the unique solution of the frozen 37-by-37 Arb system matching all pair coordinates and six chosen quartic translation orbits.

The remaining question is whether this same 74-labelled-atom ensemble accidentally matches the complete fourth-order target
\[
\tau_I=\frac{\binom{21}{2}}{\binom{42}{4}}=\frac1{533},
\qquad |I|=4.
\]

## 2. Why one D_42 representative per orbit suffices

Let A(a,b) be the cyclic skew generator with even edges a and odd edges b, R=exp(A), D=diag(1,-1,...,1,-1), and Q=RD.

Let T be a one-site cyclic shift and F a reflection. The bipartite sign matrix obeys T D T^T=-D and F D F^T=D. With the edge-orientation convention in the code,
\[
T A(a,b)T^T=A(b,a),\qquad
F A(a,b)F^T=-A(b,a),\qquad
D A(b,a)D=-A(b,a).
\]
Consequently,
\[
TQ(a,b)T^T=-Q(b,a),\qquad
FQ(a,b)F^T=DQ(b,a)D.
\]
A principal minor of order four is unchanged by a global sign and by diagonal sign conjugation. Since (a,b) and (b,a) have equal ensemble weight, the averaged fourth-order feature is invariant under both generators T and F, hence under D_42.

Thus the full fourth-order ensemble is determined by one representative from each D_42 orbit of four-subsets.

## 3. Exact interval result

The verifier enumerates all C(42,4)=111,930 four-subsets, canonicalizes under the 84-element dihedral action, and obtains exactly 1,440 orbits. The orbit-size sum is exactly 111,930.

For every canonical representative I, it reconstructs the exact-real weights from the frozen rational-decimal couplings and evaluates
\[
\bar m_I=
\sum_{\ell=1}^{37}w_\ell\,
\frac{\det Q(a_\ell,b_\ell)_{I,I}+\det Q(b_\ell,a_\ell)_{I,I}}2
\]
with 256-bit Arb. The six defining witness orbits are rechecked; all other orbit values are independently priced.

Results:
- 1,440 / 1,440 D_42 quartic orbits covered;
- exactly 6 residual intervals contain zero, corresponding to the six defining witness orbits;
- 1,434 residual intervals strictly exclude zero.

A concrete strict counterexample is
\[
I_*=\{0,3,19,26\},\qquad |D_{42}I_*|=42.
\]
Its certified moment and residual are
\[
\bar m_{I_*}\in
[0.007385676363809209868663416983790243579563528021136093775955478737633122
\ \pm 2.36\times10^{-73}],
\]
\[
\bar m_{I_*}-\frac1{533}\in
[0.005509503755929284915567732180788367406955648096182998091152476861460514
\ \pm 3.56\times10^{-73}].
\]
The residual interval is strictly positive. Therefore this frozen 37-base / 74-labelled-atom ensemble is not a complete fourth-order design.

The reported strict_counterexample is selected by the largest absolute interval midpoint among strict mismatches. That ranking is a diagnostic, not a separately certified global maximum. The strict sign of the displayed counterexample is certified.

## 4. Reproduction

Run:
    python -m py_compile verify_n42_period_two_six_quartic_ensemble_arb.py verify_n42_period_two_six_quartic_all_orbits_arb.py
    python verify_n42_period_two_six_quartic_all_orbits_arb.py

Dependency: python-flint==0.9.0; precision: 256 bits.

Artifacts:
- Frozen support: evidence/n42_period_two_six_quartic_atoms.json
- All-orbit verifier: verify_n42_period_two_six_quartic_all_orbits_arb.py
- Machine certificate: evidence/n42_period_two_six_quartic_all_orbits_arb.json
- Workflow: .github/workflows/eui-n42-period-two-six-quartic-all-orbits.yml
- Workflow run: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46022836608

## 5. Scope and next step

This proves a strict failure of the frozen support and its uniquely reconstructed weights. It does not prove that no other period-two positive ensemble can match all quartic orbits, and it does not exclude general non-period-two cycle couplings. It also says nothing by itself about sixth or higher moments, or about Choi/diamond distance.

The next decisive search should use all 1,440 quartic orbit rows in a column-generation loop: retain the 30 independent pair constraints, add the most violated quartic orbit, price new positive (a,b) atoms against the current dual, and re-solve. Any resulting finite-pool dual remains pool-specific unless a global bound over all (a,b)>0 is proved.
