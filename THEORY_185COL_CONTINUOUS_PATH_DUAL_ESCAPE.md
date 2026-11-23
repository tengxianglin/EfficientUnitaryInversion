# Strict continuous-path escape from the 185-column mixed-order dual

Date: 2026-11-23

## Result

The exact rational dual of the fixed 185-column / 2,113-row mixed-order minimax LP is not a global separator over the positive 41-edge open-path family.

The parent 185-column theorem remains valid for its pinned 185 physical generators. Its exact dual vector, lambda, slack, row inventory, and 185 Arb column inequalities are frozen in
`evidence/55probe_185col_second_continuous_escape_dual_certificate_n21.json`.

A deterministic 10-start differentiable search over \(10^{-4}\le c_j\le100\) found a second new path. The exact-decimal-rational couplings are

\[
\begin{aligned}
c=(&0.021717233185,\ 0.016610875963,\ 1.567928100304,\ 0.000182302949,\\
&0.001766079570,\ 0.010550378835,\ 12.568411916342,\ 0.109198959642,\\
&0.090128218273,\ 4.711305605693,\ 0.006142167309,\ 0.072144941225,\\
&9.428300639089,\ 0.133730286022,\ 4.713219007760,\ 0.014896968245,\\
&0.000100000000,\ 0.011309488368,\ 0.001027403950,\ 0.042782615036,\\
&0.010985869657,\ 0.002872731889,\ 0.000100000000,\ 0.033986365669,\\
&0.355648542050,\ 9.418722195716,\ 0.010067453471,\ 0.001484420138,\\
&1.561424303401,\ 0.000100000000,\ 3.063668089955,\ 0.693270233700,\\
&0.000100000000,\ 4.711470243490,\ 0.006671069180,\ 1.571104250964,\\
&0.021334196681,\ 4.712811702449,\ 0.004211589643,\ 0.005643549486,\\
&9.425364564992,\ 0).
\end{aligned}
\]

All 41 open-path edge magnitudes are strictly positive. The path is distinct from both previously Arb-certified continuous escapes and from the frozen canonical inventory.

At 128-bit Arb precision, the independent verifier rebuilds \(e^{K(c)}\) from these exact rational inputs and evaluates all 54 active dual features. It certifies

\[
\boxed{
S_{185}(c)\in
[293.82920368783706755711439295738586
\pm5.02\times10^{-33}]>0.
}
\]

The lower endpoint is strictly positive. Thus the universal inequality \(S_{185}(c)\le0\) fails on the continuous physical family.

## Search diagnostics

- 10 deterministic starts;
- 100 L-BFGS-B iterations per start;
- analytic cofactor/Frechet gradient;
- complex-step checks at coordinates 0, 20, and 40;
- maximum relative gradient defect \(9.175993298526919\times10^{-13}\);
- best rounded binary64 discovery score \(293.8292036878351\);
- exact candidate SHA256 `ccf04bb70d08014f949c2c48554fdec0d93bc7308dbbbc89d9c033e60e5922ca`.

The search is a discovery procedure. The proof is the independent Arb interval evaluation, not the optimizer status or binary64 score.

## Reproducibility

- Search: `discover_185col_continuous_dual_escape.py`
- Independent verifier: `verify_185col_continuous_dual_escape_arb.py`
- Search transcript: `evidence/185col_continuous_dual_search_n21.json`
- Arb certificate: `evidence/185col_continuous_dual_escape_arb_n21.json`
- Workflow: [45127900561](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45127900561)
- Evidence commit: [4293fc0](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4293fc0e567d0ed0c45c295a9687fb273dc4ea54)
- Parent 185 dual SHA256: `3d66af653cef76f0e8bca5c9672730fa08bb390da067b37df7f12450668f71b7`
- Parent 185 LP SHA256: `53b3e6b6369b05be741ac9f716be798051059fb646002df33bfc67e06bc68e0b`

## Scope

This result disproves only the attempted global extension of this particular 185-column dual. It does not invalidate the finite 185-column minimax theorem, construct a feasible ensemble for the unrestricted family, or establish an operational Choi/diamond-norm bound.

The next decisive step is to add this exact path as a 186th physical column, re-solve the same 2,113-row minimax LP, certify the resulting branch, and then test the new dual against the continuous path family again. Do not promote a failed local search to a global separator.
