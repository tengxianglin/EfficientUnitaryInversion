# Complete eighth-order audit: exact orbit geometry and interval protocol

2026-11-22; candidate base commit 0f1a4f2c7a2828ff1d6ca06f69ee1542b1e14f34.

This note closes the *combinatorial enumeration* gap for the next independent
moment order. It does not claim that the 29-column candidate passes all
eighth-order inequalities; the determinant scan remains to be run.

## 1. Target and finite certificate to be tested

For N=42 and k=8, the Haar/program-uniform target for an eight-set I is

\[
t_I=(-1)^{v(I)+4}\frac{\binom{21}{4}}{\binom{42}{8}}
=(-1)^{v(I)+4}\frac{1}{19721},
\]

where v(I) is the number of odd indices in I. For the exact positive
29-column distribution pinned by
[evidence/candidate_joint_input_n21.json](evidence/candidate_joint_input_n21.json),
define

\[
q_I=\sum_{j=1}^{29}p_j\frac{1}{|\mathcal O(I)|}
\sum_{J\in\mathcal O(I)}\det R^{(j)}_{J,J},
\qquad
e_I=\frac{q_I-t_I}{|t_I|}.
\]

The proposed complete finite certificate is

\[
\boxed{\max_{|I|=8}|e_I|<\frac13.}
\]

The six previously selected eighth-order rows pass this threshold by
128-bit Arb arithmetic, but that fact alone is not an all-row statement.

## 2. Exact dihedral orbit count by Burnside

The dihedral group D_42 has 84 elements. For a rotation by s positions,
let g=gcd(42,s) and L=42/g. A fixed eight-subset must be a union of
L-cycles, so its count is C(g,8/L) when L divides 8 and zero otherwise.
Summing over all rotations gives

\[
R_8=\sum_{\substack{s=0,\ldots,41\\42/\gcd(42,s)\mid 8}}
\binom{\gcd(42,s)}{8/(42/\gcd(42,s))}
=118036170.
\]

There are 21 vertex-axis reflections. Each fixes two vertices and swaps
the remaining 40 vertices into 20 pairs, giving

\[
V_8=\sum_{\substack{a=0,1,2\\8-a\ {\rm even}}}
\binom2a\binom{20}{(8-a)/2}=5985.
\]

There are 21 edge-axis reflections, each consisting of 21 swapped pairs:

\[
E_8=\binom{21}{4}=5985.
\]

Burnside therefore gives

\[
|\tbinom{[42]}8/D_{42}|=
\frac{R_8+21(V_8+E_8)}{84}
=\frac{118036170+251370}{84}
=1408185.
\]

The orbit sizes are 21, 42 or 84. Their exact histogram is 45, 6060
and 1402080 respectively, and the weighted sum is

\[
45(21)+6060(42)+1402080(84)=118030185=\binom{42}{8}.
\]

## 3. Memory-bounded canonical gap enumeration

An eight-subset is represented by its eight positive cyclic gaps
\(g=(g_0,\ldots,g_7)\), with sum 42. Translation rotates the gap tuple;
reflection reverses it. Thus every dihedral orbit has exactly one
lexicographically minimal representative among the rotations of g and
the rotations of its reversal.

Let m=min(g). The canonical representative starts with m. Write

\[
g_0=m,\qquad g_i=m+h_i\quad (i=1,\ldots,7),
\qquad h_i\ge0,\quad \sum_{i=1}^7h_i=42-8m.
\]

Consequently m is one of 1,...,5. Enumerating weak compositions of
42-8m into seven parts and retaining only dihedral-canonical tuples
produces every orbit once. This examines 4,887,204 raw weak-composition
candidates, rather than materializing all 22,481,940 anchored descriptions
in one global Python set.

For bounded worker memory, the enumeration is partitioned by
(m,h_1,h_2). There are 1,270 deterministic tasks, 409 nonempty. Each
task has a separate canonical-key SHA256. The global canonical-key hash
is frozen in
[evidence/candidate_eighth_orbit_enumeration_n21.json](evidence/candidate_eighth_orbit_enumeration_n21.json).

The independent Burnside count and the orbit-size sum are both required
before the enumeration is marked complete. Small N=10,k=4 and N=14,k=6
enumerations are also checked against Burnside and explicit orbit sizes.

## 4. Interval scan protocol

[verify_candidate_eighth_bound.py](verify_candidate_eighth_bound.py)
reconstructs the exact 29 probabilities and 29 physical 42-by-42
rotations in each spawned worker. At 128 Arb midpoint bits, every orbit
is tested using outward-rounded matrix exponentials, 8-by-8 determinants,
exact rational weights and exact target fractions. The only acceptance
condition is a definite strict comparison |e_I|<1/3.

A worker independently regenerates its assigned canonical keys and checks
the task hash before evaluating determinants. The parent checks all 1,270
task IDs, task hashes, Burnside orbit count, and the sum of explicit orbit
sizes. A prefix run or a run with an interval overlap cannot return
complete=true. A definite interval violation is a counterexample to the
proposed 1/3 bound for this candidate, not a no-go theorem for other
physical ensembles.

The complete scan would require

\[
29\binom{42}{8}=3422875365
\]

candidate-by-principal-minor evaluations. This is a substantial compute
job. The canonical-gap enumeration was independently executed in Python and
its counts/hash are frozen above; the repository exposes a dependency-light
enumeration-only replay. The full Arb determinant scan has **not** been
executed in this run.

## 5. Reproducibility

Enumeration only:

~~~
python verify_candidate_eighth_bound.py --enumeration-only \
  --output evidence/candidate_eighth_orbit_enumeration_n21.json
~~~

Small regression tests:

~~~
python -m unittest tests/test_eighth_orbit_enumeration.py
~~~

Full interval scan:

~~~
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python verify_candidate_eighth_bound.py --workers 8 \
  --output evidence/candidate_complete_eighth_bound_n21.json
~~~

A full pass would certify only this candidate's degree-eight maximum.
It would not establish orders 10,12,...,20, exact all-moment program
uniformity, an operational inversion/channel-error theorem, or global
optimality. If a row violates the threshold, add that row to the joint
minimax LP and rerun the complete sixth-order interval verifier after
reweighting. If all rows pass, proceed to degree ten without promoting
the finite degree-eight statement to full uniformity.
