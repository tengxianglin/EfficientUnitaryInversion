# Exact sixth-order counterexample for the 152-column candidate

## Statement

The exact-rational 51-support mixture stored in
`evidence/candidate_joint_input_152col_continuous_escape_n21.json` is **not**
a complete sixth-order (1/3)-witness. This is a candidate-specific
counterexample, not an infeasibility result for other mixtures.

For the (D_{42})-orbit represented by
[
I=(0,1,8,18,25,35),
]
whose orbit has size 42, define the orbit-averaged sixth principal minor
[
ar m_I(R)=rac1{42}sum_{Jin D_{42}cdot I}det R[J,J].
]
The target and normalization scale are both (5/19721).

Using the exact rational probabilities (p_k) and exact rational couplings
for all 51 support columns, a 128-bit Arb computation certifies
[
M_I=sum_k p_kar m_I(R_k)
in
[0.0004662790811077881589302992545605108
pm 5.56	imes10^{-38}],
]
and hence
[
rac{|M_I-5/19721|}{5/19721}
in
[0.839097951705338056452886319837567
pm2.78	imes10^{-34}]
>rac13.
]
The interval lower endpoint is strictly above (1/3); this is a rigorous
failure of the full-sixth cap for this exact mixture.

## Exhaustive floating-point context

A separate complete binary64 scan evaluated all 63,133 (D_{42}) sixth-order
orbits, covering all 5,245,786 six-subsets. It found 334 rows with normalized
absolute error at least (1/3), with maximum 0.8390979517059564 at the same
representative. The scan also checked the sixth elementary-symmetric signed
sum, obtaining -1329.9999999999989 versus the exact -1330.

Only the representative above has been promoted here to a strict Arb
counterexample. The other 333 violations remain binary64 screening findings
until individually or collectively interval-certified.

## Scope and logical boundary

The exact candidate remains rigorously certified on its original 1,779 pinned
rows: 1,461 complete second/fourth rows, 311 selected sixth rows, and seven
selected eighth rows. That statement does not imply a complete sixth-order
certificate. The new counterexample disproves only the complete-sixth claim
for this candidate; it does not prove that the 152-column pool, a larger pool,
or the continuous physical family is infeasible.

The next cutting-plane LP adds all 334 binary64-identified sixth rows to the
original design. Its HiGHS objective is a discovery result until its
rationalized dual is independently certified with Arb.

## Reproducibility

- Exact candidate input SHA256:
  `78f396b6efba5b6d230322c253294a0b0c834319d42b8e796e732088938d5d65`
- Complete sixth binary64 screen SHA256:
  `75813b18eaba426c818f25a67b8d8a608a05a5d421e8a2013d9ae252a6716bdc`
- Verifier: `verify_152col_sixth_counterexample_arb.py`
- Frozen Arb output: `evidence/candidate_152col_sixth_counterexample_arb_n21.json`
- Workflow: [45056852005](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45056852005)
- Verifier commit: [5f2ca63](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5f2ca63d07ab12ff48659b4491c0dc8015fc4ace)
