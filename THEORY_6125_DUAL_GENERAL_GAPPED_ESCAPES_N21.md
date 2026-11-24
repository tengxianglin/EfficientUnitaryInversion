# Certified general-gapped escapes from the 6,125-column dual (n=21)

Date: 2026-11-24. Related: Issue #5.

## Main result

The exact rational dual certified on the 6,125-column pool is **not** positive on the full connected nonuniform gapped open-path family. A deterministic finite multistart/L-BFGS-B search found a connected candidate and a multi-segment candidate. Both are frozen as exact decimal rationals and independently reconstructed with 256-bit Arb.

The finite-pool theorem remains valid: these candidates are outside its exact 6,125-column list. The result refutes only extension of this particular new dual unchanged to the broader gapped family.

## Exact target and Arb scores

The 78-term dual has target score
\[
y^{\mathsf T}b\in[0.3730980596968074923019997412068832567693162667\ldots].
\]

### Connected positive-coupling escape

The 42-site open path has \(c_{41}=0\) and all 41 interior couplings strictly positive. The minimum interior coupling is
\[
\frac{19999999999999999}{20000000000000000000000}
=9.9999999999999995\times10^{-7}.
\]
At 256-bit Arb,
\[
y^{\mathsf T}F(R(c))
\in[13.39534571134364063663490148997725698945\ldots],
\]
so
\[
\boxed{
y^{\mathsf T}(b-F(R(c)))
\in[-13.02224765164683314433290174877037373268\ldots]<0.
}
\]

### Multi-segment escape

A second path has internal cuts at edges \(16\) and \(26\), hence three open segments. At 256-bit Arb,
\[
y^{\mathsf T}F(R(c))
\in[27.03109850670501738179435107722054517357\ldots],
\]
and
\[
\boxed{
y^{\mathsf T}(b-F(R(c)))
\in[-26.65800044700820988949235133601366191680\ldots]<0.
}
\]

For each candidate the verifier checks all 1,764 entries of \(R^{\mathsf T}R-I\) with Arb intervals containing zero and certifies \(\det R\) contains 1. The Arb/floating score discrepancies are below \(3.0\times10^{-13}\).

## Reproducibility

- Search transcript: evidence/ising_full_fourth_plus_two_gapped_search_n21.json.
- Search script: search_ising_full_fourth_plus_two_gapped_n21.py.
- Search workflow: [45378179718](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45378179718).
- Independent 256-bit verifier: verify_ising_full_fourth_plus_two_gapped_escape_arb_n21.py.
- Arb escape certificate: evidence/ising_full_fourth_plus_two_gapped_escape_arb_n21.json.
- Arb workflow: [45378513134](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45378513134).
- Certificate commit: [aed0e00](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/aed0e007753d93990791d93c3ec0e13a1668f2cd).

The escape certificate pins the 6,125-column diagnostic, its Arb certificate, the parent 6,124-column certificate, the previous-dual escape certificate, and the deterministic search transcript by SHA-256.

## Scope

This is a certified counterexample to global extension of the **specific 6,125-column rational dual** to the connected general-gapped family. It does not invalidate the finite-pool 6,125-column theorem. It does not prove that the full physical moment problem is feasible or infeasible, does not construct an all-even-principal-minor positive ensemble, and does not imply a Choi trace-distance or channel diamond-distance bound.

## Next decisive action

Append both exact-rational candidates to the 6,125-column pool and rerun the full 1,440-orbit second-/fourth-order LP. If the new LP is infeasible, independently Arb-certify its new rational dual before pricing it on fresh gapped paths. If feasible, freeze the positive primal and certify every second-/fourth-order moment. Do not reuse either escape as evidence against the next dual without checking it against that dual.
