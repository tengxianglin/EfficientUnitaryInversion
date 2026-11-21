# Selected eighth-order audit for the fixed n=21 ensemble

2026-11-22; base `334d1ef5e1819bc1ab72a1f770b362d687436e5d`; Issue #3.

The complete sixth-order certificate does not imply control of the next
independent moment order. This note supplies a small, rigorous separation
audit for the *same* exact 83-seed-orbit physical ensemble. It is intended
to prevent an unsupported extrapolation from degree six to all moments.

## Certified calculation

For an 8-set `I`, the target magnitude is

\[
 |t_I|=\binom{21}{4}/\binom{42}{8}=1/19721,
 \qquad t_I=(-1)^{v(I)+4}/19721.
\]

`audit_selected_eighth_moments.py` reconstructs the canonical exact
probabilities and all 83 matrix exponentials from the hash-pinned input,
then evaluates each selected dihedral orbit with 128-bit Arb balls. Every
acceptance test is a definite strict inequality, with no floating tolerance:

| representative `I` | orbit size | certified fact |
|---|---:|---|
| `(0,1,2,3,4,5,6,7)` | 42 | `|e_I| > 6` |
| `(0,5,10,15,20,25,30,35)` | 42 | `|e_I| > 1` |
| `(0,1,8,9,16,17,24,25)` | 42 | `|e_I| > 9/10` |
| `(0,4,12,16,20,28,32,36)` | 84 | `|e_I| > 2` |
| `(0,2,6,14,22,30,34,40)` | 84 | `|e_I| > 6/5` |
| `(0,3,9,14,21,27,33,39)` | 84 | `|e_I| > 3/10` |

Here `e_I=(E det(R_{I,I})-t_I)/(1/19721)`. The first row has a
128-bit enclosure centered at approximately `6.20204152419733649`; the
fourth is centered at approximately `-2.01784656824718808`. The full
intervals and exact input hash are frozen in
`evidence/selected_eighth_moment_audit_n21.json`.

## Interpretation and boundary

This is a **finite countercheck against degree-eight extrapolation**, not a
complete degree-eight maximum or a no-go theorem. It proves that the fixed
repair distribution which achieves `G_6<1.55` has severe errors on several
independent eighth-order rows; it does not show that another physical
ensemble cannot improve those rows. Orders 8, 10, ..., 20 therefore remain
scientifically active constraints for the joint moment-design problem.

The result also rules out describing the current witness as approximately
uniform through degree eight under any claim requiring small relative error.
It does not imply an operational inversion/channel error bound, query
optimality, or impossibility of a different ensemble.

## Reproduction

From this commit:

```bash
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  PYTHONDONTWRITEBYTECODE=1 python audit_selected_eighth_moments.py
```

The script uses only the exact source reconstruction and Arb interval
arithmetic. The six rows are intentionally selected diagnostics, not a
replacement for an eventual all-8-set separation oracle.

**Next action:** include the near-active sixth directions and at least the
first two high-error eighth directions in a coupled low/sixth/eighth dual
pricing problem. Any proposed reweighting must then be re-audited at all
sixth orbits before claiming improvement.
