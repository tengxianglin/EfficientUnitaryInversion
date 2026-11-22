# Certified 29-column low/sixth candidate

2026-11-22; Issue #3.

The finite joint LP from the previous step produced a 29-column candidate.
This note records the stronger result obtained by converting its binary64 LP
weights into exact `Fraction.from_float` probabilities, renormalizing them
exactly, and rerunning interval checks.

## Certified facts

For the same physical model (42-site real skew ring with one exactly zero
closing edge), the candidate has at most `29*84=2436` signed-dihedral atoms.
Every candidate coupling is one of the previously hash-pinned physical
columns. The exact normalized probabilities sum to one.

With 128-bit Arb balls, `verify_candidate_low_bound.py` certifies all 21
second-order and all 1,440 fourth-order rows:

\[
 G_{\le4}<1/3.
\]

With 64-bit Arb balls, `verify_candidate_sixth_bound.py` certifies every
sixth-order index set: all 63,133 dihedral orbits, all 5,245,786 six-sets,
and all 435,400,238 candidate-by-principal-minor evaluations pass the
strict interval inequality

\[
 G_6<31/20=1.55.
\]

A separate 128-bit Arb calculation of six selected eighth-order rows gives
`|e_I|<1/3` for all six rows, including the contiguous and mixed sparse rows
that had errors above 6 and 2 for the previous witness. This is not a
complete degree-eight certificate.

The complete sixth transcript is frozen in
`evidence/candidate_complete_sixth_bound_n21.json`; the low and selected
8-row certificates are frozen in
`evidence/candidate_low_bound_n21.json` and
`evidence/candidate_selected_eighth_n21.json`. All source hashes and exact
probabilities are pinned in
`evidence/candidate_joint_input_n21.json`.

## Interpretation

This is a genuine finite physical witness improving the previous fixed
repair ensemble on the certified low-order block while retaining the full
sixth-order upper bound. The old `G_{\le4}<0.218` certificate does not apply
to these new weights; the candidate's independently certified low bound is
`1/3`. The selected eighth rows are controlled, but the other eighth-order
orbits and all orders 10,12,...,20 remain uncontrolled.

No claim of exact joint uniformity, global optimum, query optimality,
operational inversion/channel error, or Nature Physics-level novelty follows.
The candidate is a separation-oracle starting point: a complete eighth-order
scan may still find large violations.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python verify_candidate_low_bound.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python verify_candidate_selected_eighth.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python verify_candidate_sixth_bound.py --workers 8
```

The last command is the complete six-order run; its `complete:true` flag,
range hashes and exact set count are required. Prefix runs must not be
reported as complete certificates.

**Next highest-value action:** perform a complete eighth-order orbit scan for
this candidate. Add any violated eighth rows to the joint LP, then repeat
the complete sixth certificate after each reweighting. Only after the
higher-order scan stabilizes should the support be promoted to an exact
closed-form distribution for a paper theorem.
