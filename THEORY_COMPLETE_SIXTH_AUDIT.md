# Exhaustive sixth-order audit: coverage, numerical maximum, and certified rows

2026-11-22; base `301e20b14aed72f362764624447482e29e1ccaa4`; Issue #3.
Follow-up to the [certified low/selected-sixth repair](THEORY_SIXTH_PRICING_ESCAPE.md).

## Decision and evidence levels

The complete floating audit of the exact repair ensemble finds **no
sixth-order orbit outside the original 256 with relative error >1.55**.
Across all 63133 sixth orbits, its numerical maximum remains the known
contiguous probe, approximately 1.5486211350. This supports, rather than
refutes, extending the previous screen's bound, but it is not an interval
certificate of a complete sixth upper bound.

The 70-orbit reference ensemble's complete floating maximum is about
2.1996664252, also at the contiguous probe. This reference is the prior
low-order witness, not an optimum over the 1639-column pool. No global
optimization or certified full-max comparison is asserted.

Two previously untested rows are independently interval-certified:

- I=(0,4,12,20,28,32), target -5/19721: the repair moment is positive,
  opposite to its target, and 28/25<|E_6(I)|<9/8 (1.12 to 1.125).
  The reference moment also has the wrong sign; this is a persisting,
  not newly created, sign defect.
- I=(0,5,14,19,28,33), target +5/19721: the reference relative error is
  <23/200, while the repair relative error is >37/50. The increase is
  >5/8=.625. This does not contradict improvement of the maximum norm.

Thus no new sampled-bound violation was found, but a large individual
tradeoff exists outside the optimized screen. This is not evidence that
the repair failed or that every higher-order direction worsened. It is
also not a counterexample with exact low-order matching, a full uniform
program construction, or a general physical no-go result.

## 1. Exact enumeration and independent completeness count

Every six-subset of the 42-cycle can be rotated to contain zero. Enumerate
all binom(41,5) such anchored sets, convert each to its six positive
cyclic gaps, and select the lexicographically minimal cyclic/reversed
rotation of that gap tuple. Equal canonical gap tuples are exactly the
same dihedral orbit. This generates every orbit without assuming generic
orbit size 84.

An independent Burnside count gives the same answer. For rotations,
only cycle lengths 1,2,3,6 divide both 42 and 6, so the fixed-set sum is

\[
 \binom{42}{6}+\binom{21}{3}
       +2\binom{14}{2}+2\binom71=5247312.
\]

Of the 42 reflections, 21 have two fixed vertices and 20 swapped pairs,
with binom(20,3)+binom(20,2)=1330 invariant six-sets; the other 21 have
21 swapped pairs and binom(21,3)=1330 invariant sets. Therefore

\[
 |\mathcal O_6|=(5247312+55860)/84=63133.
\]

The explicitly generated orbit sizes sum to binom(42,6)=5245786.
Stabilizers are handled exactly, including shorter special orbits.
Independent small-size counts at N=10 and 14 give 16 and 126 sixth
orbits. These are exact combinatorial coverage checks, distinct from the
floating moment calculations. Burnside counting itself is standard,
not a new mathematical mechanism.

## 2. Exact ensemble definitions and floating computation

The canonical 83-orbit repair distribution is rebuilt from the exact
normalization/blending rule of the preceding certificate, then checked
against its recorded exact probabilities. All source hashes and the
positive, exact probability sum are checked. It includes the complete
70-orbit reference support, so a single bank of 83 rotations suffices
for both ensembles. The reference couplings use exact binary64 rationals;
the new physical seed uses exact decimal rationals, as before.

The audit converts those exact inputs/probabilities to binary64 solely
for this numerical calculation. For each batch of 256 orbits it evaluates
all distinct six-principal determinants, averages using the actual orbit
sizes, and accumulates both distributions. It evaluates 435400238
six-by-six determinants in total. Batches avoid storing all 5245786
principal blocks at once. No random probe selection enters this pass.

The output [evidence/complete_sixth_audit_n21.json](evidence/complete_sixth_audit_n21.json)
freezes orbit/set counts, independent Burnside data, selected rows and
SHA256 hashes of both complete binary64 moment vectors. The full vectors
are reproducible intermediate data, optionally saved with --vector-cache.
They are not needed for the selected-row interval proof.

Numerical findings:

| Quantity | Reference 70-orbit ensemble | Repair 83-orbit ensemble |
| --- | --- | --- |
| Maximum over all sixth orbits | 2.1996664252416105 | 1.5486211350271804 |
| Error at the repair's largest untested row | 1.1581116539387888 | 1.123927854276574 |
| Error at the untested largest-increase row | 0.11409473413306981 | 0.7422365638888914 |

Both complete numerical maxima occur at (0,1,2,3,4,5), already in the
original screen. The repair's largest untested row is (0,4,12,20,28,32).
There are 62877 additional orbits outside the original 256.
"Maximum" in this table means the exhaustive **floating** calculation
for the specified distribution, not a rigorous exact maximum or an
optimum over physical Hamiltonian ensembles.

As a physics consistency check, Q=Z exp(A) is a symmetric involution,
so det(I+tQ)=(1-t^2)^21 gives

\[
 \sum_{|I|=6}(-1)^{v(I)}\det R_I=-\binom{21}{3}=-1330.
\]

The full vectors, with exact orbit multiplicities, give approximately
-1329.9999999998295 and -1329.9999999998286. Both pass the declared 1e-7
floating tolerance. This is a useful completeness/sign/weight checksum,
not an interval error bound on every determinant.

## 3. Independent selected-row certificates

The frozen [input](evidence/complete_sixth_outlier_input_n21.json) pins
source hashes and the two rows. At 128-bit Arb precision,
[verify_complete_sixth_outliers.py](verify_complete_sixth_outliers.py)
rebuilds exact-input rotations and all principal six-minors in their
42- and 14-element orbits, using the exact positive probabilities.
It verifies membership outside the original 256, target signs and the
strict rational inequalities stated above. No numerical vector cache,
optimizer, or assumption that the floating argmax is exact enters this
proof. See [the interval transcript](evidence/complete_sixth_outlier_certificate_n21.json).

In particular the increase certificate is
|E_6^repair|>37/50 and |E_6^reference|<23/200, hence a strict increase
>5/8. It does not prove that the repair's *complete* maximum is larger;
the exhaustive floating evidence actually indicates the opposite.

## 4. Reproduction and remaining decision

Python 3.12.14 / NumPy 2.3.5 / SciPy 1.17.0 / python-flint 0.9.0;
OPENBLAS_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1. Full numerical pass:

```
python audit_complete_sixth_moments.py --output /tmp/eui-sixth-all.json --vector-cache /tmp/eui-sixth-vectors.npz
```

Recompute exact coverage, checksums and summary from that saved vector
cache (this does not repeat determinant calculations):

```
python audit_complete_sixth_moments.py --output /tmp/eui-sixth-replay.json --replay-vector-cache /tmp/eui-sixth-vectors.npz
python verify_complete_sixth_outliers.py
python -m unittest discover -s tests -v
```

The interval verifier reads the frozen selections, not an arbitrary new
audit output. Full floating vectors may depend on the numerical library
version; this limitation does not affect the exact selected-row proof.
The prior low/256-sixth certificate remains valid and is reused, not
silently promoted to an all-sixth certificate.

**Next highest-value action:** obtain a complete sixth-order interval
upper certificate for this exact ensemble before asserting G_6<1.55.
Use the exhaustive orbit audit as a separation oracle after subsequent
updates, adding genuinely violated orbits rather than arbitrary probes.
**Still blocked:** that all-sixth interval upper bound, exact low-order
feasibility, higher-even-moment closure and full joint uniformity/minimax.
No original Nature Physics-level core claim or unrestricted-query result
follows from this audit. Current main/recent Issues, research notes,
code/evidence and the manuscript/Appendix B were rechecked; no manuscript
sources are present.
