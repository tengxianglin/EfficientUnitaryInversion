# Iterated physical pricing and a reflection-averaging counterexample

Follow-up: [six-column batch and explicit approximate mixture](THEORY_BATCH_FOURTH_PRICING.md).

Date: 2026-11-21. Base commit: `a1207766abb8c3470016d7addbb6bc31305ae5ed`.
Issue #3. This continues the [certified first pricing step](THEORY_DIRECTED_FOURTH_PRICING.md)
for the [complete second/fourth system](THEORY_FOURTH_MOMENT_HIERARCHY.md).

## What is established

**Interval-certified existence:** eight additional legal, gapped, connected
physical seeds cross their respective frozen rational pricing targets by
more than one. Each seed is non-Pauli, by the existing connected-path
classification. No global optimizer claim is needed for these inequalities.

**Interval-certified counterexample:** averaging a seed with its reflected
coupling vector can destroy the useful program moments. For the explicit
positive-coupling example below, the probability mixture has functional
value greater than 8, while the averaged Hamiltonian has value less than
-3. Their difference exceeds 11, and they lie on opposite sides of the
same target. Symmetry can be imposed on the probability ensemble; imposing
reflection symmetry on each individual coupling vector requires a separate
argument and is not justified by parameter averaging.

**Finite numerical progress:** the pool grew from 1601 to 1609 seeds. Its
reduced/scaled minimax moment residual decreased from approximately
0.2471042713 to 0.2244753240 (9.16%). The final feasibility LP still reports
infeasible. Neither the residual nor that solver status is an interval
certificate, a channel error, or an obstruction for all physical couplings.
Full fourth-order feasibility and higher-moment closure remain open.

## 1. Physical model and frozen objects

Use the previous static-oracle convention: n=21, N=42, closing coupling
c_41=0, A_{j,j+1}=2c_j, A_{j+1,j}=-2c_j, and R(c)=exp(A(c)). All 41
internal couplings of each new seed are nonzero, although some signed
representatives have negative entries. The zero closing edge gives a
connected open path. The existing gap/gauge lemma makes the two physical
parity sectors have the same program masses. Thus these are legitimate
columns for the joint-parity search, rather than arbitrary orthogonal
matrices or unphysical convex combinations of generators.

Let m_d be the cyclic average of second-order principal minors at distance
d=1,...,21, and q_o the average of fourth-order principal minors over a
dihedral orbit o. The target is

\[
 m_d^*=(-1)^{d+1}/41,\qquad q_o^*=(-1)^{v(I)}/533,
\]

where v(I) counts odd indices in a representative four-set. These signs
are constant on each orbit. A frozen pricing direction specifies

\[
 L(c)=\sum_d b_d m_d(c)+\sum_o a_o q_o(c),\qquad
 L_*=\sum_d b_d m_d^*+\sum_o a_o q_o^*.
\]

The exact rational coefficients, targets and six-decimal rational
couplings for all eight rounds are in
[the experiment input](evidence/iterated_fourth_pricing_n21.json).
For every round r=0,...,7 the 192-bit Arb calculation proves

\[
 L_r(c_r)-L_r^*>1.                                      \tag{1}
\]

The smallest margin is about 9.53068548, so the deliberately conservative
threshold 1 has ample separation. All coefficients and parameters are
interpreted exactly as the rational numbers encoded in the JSON, not as
the nearby binary64 values used during discovery. The interval evaluation
rebuilds exp(A) and the relevant determinants; it does not use the saved
floating feature vector or optimizer status. The outputs are frozen in
[the proof transcript](evidence/iterated_fourth_pricing_verification_n21.json).

The [pure-Pauli classification](THEORY_PURE_PAULI_CLASSIFICATION.md) provides
another check. For a connected-path generator a pure Pauli program would
force R=+/-I, hence all principal minors equal one. Each certified value in
(1) is disjoint from the corresponding exact value
sum_d b_d + sum_o a_o. Thus all eight columns are non-Pauli. This does not
establish a non-Clifford resource requirement.

## 2. Why symmetrizing the generator is not without loss

Let J reverse the N vertices, and let c^rev_j=c_{40-j} for j=0,...,40,
with c^rev_41=0. Directly from the oriented path matrix,

\[
 A(c^{\rm rev})=-J A(c)J,\qquad
 R(c^{\rm rev})=J R(c)^T J.                            \tag{2}
\]

A principal determinant is unchanged by transposition. Reversal permutes
the four-sets within a dihedral orbit and the pairs at a fixed cyclic
distance. Consequently every feature satisfies

\[
 m_d(c^{\rm rev})=m_d(c),\quad q_o(c^{\rm rev})=q_o(c).  \tag{3}
\]

Also, signs of internal path couplings can be removed by a diagonal
vertex-sign matrix S: choose S_0=1 recursively so that
S_j S_{j+1} c_j=|c_j|. Then A(|c|)=S A(c) S and every principal minor is
unchanged. This works because the closing edge is zero.

Take the absolute values of the first new seed. Its internal couplings
are strictly positive, between 0.341978 and 32.988564. Define

\[
 \mu=\tfrac12\delta_{|c_0|}+\tfrac12\delta_{|c_0|^{\rm rev}},
 \qquad \bar c=\tfrac12(|c_0|+|c_0|^{\rm rev}).
\]

The averaged vector is also a valid positive, gapped path and is exactly
reflection symmetric. The functional is the first frozen direction,
with exact target L_*=-437812631/533000000. Equations (2)-(3) prove that
the probability mixture preserves the first seed's features. Independent
interval evaluation of the three rotations certifies

\[
 \mathbb E_\mu L=L(|c_0|)=L(|c_0|^{\rm rev})
   \in[8.70927341907144808688414830326033860947968019231411
          \ \pm 1.63\times10^{-51}],
\]
\[
 L(\bar c)\in[-3.749477674314347721469425240168156566847073621573792
          \ \pm 9.12\times10^{-52}].
\]

In particular, E_mu L > 8 > L_* > -3 > L(c_bar) and
E_mu L-L(c_bar)>11. Exact inputs are in
[the reflection counterexample](evidence/reflection_averaging_counterexample_n21.json).
The verifier checks positivity, exact reversal and exact rational averaging,
and checks that this input is the absolute-value gauge of round zero.
Interval overlap of the reflected scores is a consistency check; the
equality itself follows from (2)-(3).

This refutes the parameter-averaging argument for restricting the search
to palindromic seeds. It does **not** prove that all ensembles made of
palindromic seeds fail, nor that asymmetry alone caused the optimizer's
improvement: the two restarts also differ in initialization. Nonlinearity
of exponentiation and generic symmetry averaging are standard facts; the
contribution here is an explicit certified counterexample for this EUI
moment search, not a new general symmetry principle.

## 3. Meaning of the finite-pool residual

The exact hierarchy leaves 1313 retained feature coordinates. Set V_j to
the retained feature vector of seed j after scaling each second-order row
by 41 and each fourth-order row by 533, and set t to the equally scaled
target. The optimization solved in each round is

\[
 g=\max_{\|y\|_1\le1}
       \bigl(y\cdot t-\max_j y\cdot V_j\bigr)
   =\min_{p\ge0,\,\sum_jp_j=1}
       \left\|t-\sum_jp_jV_j\right\|_\infty.            \tag{4}
\]

The equality follows from finite-dimensional minimax on the compact
simplex and unit l1 ball, followed by l1/linfinity duality. It is an exact
identity for the specified real feature vectors. The recorded values are
floating LP evaluations of (4), not exact evaluations of g. Dropping
dependent rows preserves exact feasibility; it need not preserve an
approximate residual norm. Thus g is specific to these retained/scaled
coordinates, and is not asserted to be an operational EUI error.

| Pool size | Numerical g |
| --- | --- |
| 1601 | 0.24710427130220025 |
| 1602 | 0.2395164240096308 |
| 1603 | 0.23413539724179766 |
| 1604 | 0.23150416094266613 |
| 1605 | 0.23088033786187723 |
| 1606 | 0.22948093507132328 |
| 1607 | 0.22842236100086954 |
| 1608 | 0.22697626867013365 |
| 1609 | 0.22447532395677383 |

At each round a numerical dual is rounded to six-decimal rational
coefficients. Two L-BFGS-B runs, each limited to 120 iterations, price
that direction: one starts at a current pool maximizer; the other starts
at the latest seed with a fixed, generally asymmetric perturbation.
Rounding the better candidate to six decimals gives the new physical
input. A local optimizer stopping at its iteration limit does not affect
the validity of (1). It also does not certify a maximum.

The numerical replay checks every prefix's positive separating gap,
all eight complete 1461-feature SHA256 fingerprints, the final LP gap,
and the final feasibility status 2. Results are in
[the replay transcript](evidence/iterated_fourth_pricing_replay_n21.json).
The prefix inequalities have not been interval-certified. In particular,
the proof of individual columns in (1) is not a theorem excluding their
augmented prefixes, and the old 1600-column certificate is not reused
as a bound for larger pools.

## 4. Reproduction and next decisive action

Dependencies used: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0,
python-flint 0.9.0. No optimizer or cache is needed to verify the fixed
inequalities:

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_iterated_moment_pricing.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

For the numerical study, generate the previous complete feature cache
and either replay the frozen columns or repeat discovery:

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_fourth_moments.py --search --cache /tmp/eui-pool.npz
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_iterated_moment_pricing.py --cache /tmp/eui-pool.npz --replay-final
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python continue_ising_moment_pricing.py --cache /tmp/eui-pool.npz --output /tmp/eui-iteration.json --rounds 8
```

Use `--resume` with the same output to extend a saved checkpoint. The
old cache's little-endian binary64 feature fingerprint must be
`3825a5cce52e221f96c10319b8c5e57eb9c11c793ebb21b6c4a5c8f085badad5`;
every new column has a separate fingerprint in the input JSON. Identical
optimizer trajectories across BLAS/solver versions are not required for
the fixed rational proof. The final direction is saved as `next_direction`.

**Remaining blocker:** no positive finite ensemble solves the complete
second/fourth equations here; the final status is only numerical. A full
uniform program requires all higher even moments as well. The
[joint-parity minimax theorem](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md)
therefore remains conditional at n=21.

**Next highest-value action:** price the saved next direction with several
distinct asymmetric starts and add a batch of independently verified
violating columns before resolving (4). Do not restrict all seeds to
reflection-symmetric couplings on the basis of parameter averaging. A
positive design would require certified positive weights and closure of
the remaining moments; a negative theorem would require a global physical
bound, not this finite pool or local optimization failure.

This run inspected the current main commit, recent Issue #3 progress,
research notes, code and evidence, and the
[manuscript and Appendix B](https://arxiv.org/html/2506.20570v1).
No manuscript TeX/PDF sources are present. The current results concern
the fixed static-oracle design promise, distinct from the manuscript's
broader robustness study. They do not establish journal readiness or an
unrestricted query advantage.
