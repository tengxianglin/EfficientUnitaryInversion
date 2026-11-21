# A certified sixth-order boundary of the low-moment construction

2026-11-21; base `9477d4f5d7938e63bc2d242b1417f430f01795dd`;
Issue #3. Follows the [complete low-order certificate](THEORY_CERTIFIED_LOW_MOMENT_ENSEMBLE.md).

## Scientific decision

The previous exact physical ensemble has a certified complete
second/fourth scaled residual G_24<0.217405, improving the specified old
ensemble's G_24>0.226230. That improvement does not control the next
moment order. Two new interval certificates establish:

1. For the contiguous six-set I=(0,1,2,3,4,5), the new ensemble's
   relative sixth-moment error is strictly greater than 219/100=2.19.
   This exceeds ten times the certified low-order upper bound.
2. For I=(0,2,6,9,14,22), the old relative sixth error is below 1/200,
   while the new error exceeds 7/100. That individual higher-order
   error therefore increases by more than 13/200=0.065, even though
   the complete G_24 objective strictly improves.

This is a concrete tradeoff for two specified physical ensembles. It
refutes extending the numerical/certified low-order bound to these
sixth-order probes, or assuming this update improves every individual
higher moment. It is **not** a counterexample with exact second/fourth
matching, a claim that exact low-order matching is generally insufficient
within every physical subclass, or a global physical no-go theorem.
Nonuniformity of these witnesses was already visible at lower orders;
the new result identifies a significant missing-order obstruction to
using low-order progress as a proxy for full uniformity.

## 1. Exact model and sixth-order target

Keep the canonical exact inputs of the preceding certificate: all source
couplings become exact binary64 rationals, and positive source binary64
weights are converted exactly and normalized by their exact rational
sum. The same old 67 and new 70 seed orbits are used, with the same
physical 84-image dihedral average and zero-edge parity compatibility.
The verifier hash-checks the prior input definition and its five source
JSONs. No probability or parameter convention changes in this audit.

For a six-set I let v(I) count odd indices and define

\[
 q_I=\mathbb E\det R_{I,I},\qquad
 t_I=(-1)^{v(I)+3}\frac{\binom{21}{3}}{\binom{42}{6}},
 \qquad a_6=|t_I|=\frac5{19721}.
\]

The expectation includes seed probabilities and the dihedral average;
all index sets in an orbit have the same ensemble moment. Write
E_6(I)=(q_I-t_I)/a_6 and report |E_6|. This is relative error against a
small nonzero Fourier target, not a probability error or a channel norm.
The [full principal-minor criterion](THEORY_PROGRAM_MINOR_OBSTRUCTION.md)
requires matching these and all other even-order moments for complete
program-mass uniformity.

Both certified probes have positive target 5/19721:

| Probe | Old moment, approximately | New moment, approximately | Old / new relative error, approximately |
| --- | --- | --- | --- |
| (0,1,2,3,4,5) | 0.000838049180334473 | 0.000811233310998990 | 2.30543 / 2.19967 |
| (0,2,6,9,14,22) | 0.000254668079825131 | 0.000271320325285650 | 0.00446184 / 0.07014163 |

Thus one sixth-order probe improves while the other worsens. No
comparison of the *complete* sixth-order maximum is claimed.

At 128-bit Arb precision the certificate rebuilds exact rational-input
42-by-42 rotations for the union of both supports and evaluates all
principal six-minors in the two probe orbits (42 and 84 distinct sets).
It averages with exact factors and exact normalized probabilities.
The rational inequalities above are checked independently of floating
screening, LP objectives and the previous Taylor bound. The transcript
[evidence/sixth_moment_certificate_n21.json](evidence/sixth_moment_certificate_n21.json)
contains interval enclosures and exact thresholds. It does not claim an
interval upper bound for every sixth orbit.

## 2. What fourth-order closure actually implies at sixth order

There is an exact hierarchy, extending the previous fourth/second
identity. Let Q=Z exp(A), with Z=diag(1,-1,...), so Q is a symmetric
involution with n eigenvalues of each sign. For any five-set K and n>=5,

\[
 \boxed{\sum_{I\supset K,\ |I|=6}\det Q_I
       =-\sum_{J\subset K,\ |J|=4}\det Q_J.}          \tag{1}
\]

Proof: differentiating det(I+t diag(x)Q) once in each x_k, k in K,
at x=1 gives the principal-minor generating identity

\[
 \sum_{I\supset K}t^{|I|}\det Q_I
   =t^5(1-t^2)^{n-5}\det(Q_K-tI_5).
\]

The coefficient of t^6 on the right is minus the fourth elementary
symmetric polynomial of Q_K: the prefactor has no linear t term.
That polynomial is the sum of its four-principal minors, proving (1).
This specializes the same standard determinant-generating argument as
the preceding hierarchy; it is not claimed as a new general identity.

Because det Q_I=(-1)^v(I) det R_I, subtracting the exact targets and
averaging any normalized physical ensemble gives a useful normalized form.
Let a_4=binom(n,2)/binom(2n,4), a_6=binom(n,3)/binom(2n,6), and use
signed errors E_r(I)=(q_I-t_I)/a_r. The exact ratio

\[
 (2n-5)a_6=5a_4
\]

implies

\[
 \frac1{2n-5}\sum_{I\supset K,|I|=6}(-1)^{v(I)}E_6(I)
 =-\frac15\sum_{J\subset K,|J|=4}(-1)^{v(J)}E_4(J). \tag{2}
\]

The verifier checks the target identities exactly at n=5,7,21. Equation
(2) holds analytically for every K and legal ensemble, not merely those
finite checks. If all fourth-order relative errors are bounded by epsilon,
then the absolute value of this *signed average* over 2n-5 sixth probes
is bounded by epsilon. It does not isolate or bound each sixth error.
At n=21 that is an average over 37 terms, explaining the limitation of
trying to close the next order solely with the previous hierarchy. The
certified outlier above coexists with these exact averaged constraints.
No opposite-sign cancellation of specific uncomputed terms is asserted.

In particular, this hierarchy does not prove or disprove physical exact
sixth-order closure once every fourth moment is matched exactly. That
stronger question requires additional structural evidence.

## 3. Discovery, reproducibility and next step

The deterministic floating screen examined 256 sixth orbits, containing
21091 distinct six-sets. It includes seven arithmetic-progression probes
and fills the remaining canonical orbit keys using RNG 202611211836.
The contiguous probe is the largest new relative error *among this screen*;
the tradeoff probe has the largest increase *among this screen*. Neither
is asserted to be a global sixth-order maximizer. The complete screen
and selections are frozen in
[evidence/sixth_moment_screen_n21.json](evidence/sixth_moment_screen_n21.json)
and [the certificate input](evidence/sixth_moment_certificate_input_n21.json).

Commands (Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0;
OPENBLAS_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1):

```
python screen_ising_sixth_moments.py > /tmp/eui-sixth-screen.json
python verify_ising_sixth_moments.py
python verify_full_low_moment_certificate.py
python -m unittest discover -s tests -v
```

The second command proves the two frozen sixth-order statements without
repeating the screen or using a feature cache/optimizer. The third
reproduces the prior complete G_24 certificate needed for the combined
tradeoff statement. Proof inputs are frozen independently of which new
screening run happens to find a larger outlier. The screen output is
floating evidence; the two selected inequalities are interval-certified.

**Next highest-value action:** add these and a modest adversarial set of
sixth-order probes to the full-row local model, then measure both G_24
and the tested G_6 errors before accepting an update. Use (2) for exact
consistency checks, not to delete independent sixth constraints without
a rank/closure proof. A useful result would improve both measured orders
or establish a structural barrier. Optimizing only G_24 indefinitely
cannot by itself demonstrate full program uniformity.

**Still blocked:** exact low-order feasibility, higher-order closure,
and the original full joint-uniformity/minimax claim. The two finite
witness obstructions do not exclude other legal Hamiltonian ensembles.
No original Nature Physics-level core result or journal readiness is
asserted. Current main/recent Issues, relevant proof/code/evidence,
physical minor/parity lemmas and the
[manuscript/appendices](https://arxiv.org/html/2506.20570v1) were rechecked;
no manuscript source files are present.
