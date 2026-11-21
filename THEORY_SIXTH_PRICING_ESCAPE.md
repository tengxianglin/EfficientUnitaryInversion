# Certified physical escape and a low/sixth-moment repair ensemble

2026-11-21; base `2c458d8d9cb27f1e1c904970f1417606e1949dd8`; Issue #3.
Continues the [fixed-pool tradeoff certificate](THEORY_FIXED_POOL_SIXTH_TRADEOFF.md).

## Results and logical scope

**Certified physical columns.** Two connected zero-edge physical seeds
have exact decimal-rational couplings and frozen-functional values
L>3700. The old 1639-seed family satisfies L<-158.4465. Both seeds also
cross the necessary repair threshold -157.515507748 and the uniform
functional target -112.175924. This proves that the old pointwise
functional ceiling does not hold over all legal continuous couplings.
It does not by itself prove ensemble feasibility.

**Certified repaired ensemble.** An explicit exact positive mixture of
83 seed orbits, using only the first new seed orbit outside the old
family, has

\[
 G_{24}<109/500=0.218,\qquad
 G_{6,\mathcal P}<31/20=1.55,
\]

where G_24 covers all 21 second and all 1440 fourth orbit rows, while
P is the fixed set of 256 sixth orbits. The old-family theorem forces
the contiguous sixth error >482748063/250000000=1.930992252 at the same
low-order budget. Thus the new construction beats the old-family
conditional lower bound by more than

\[
 \frac{482748063}{250000000}-\frac{31}{20}
 =\frac{95248063}{250000000}>0.38.
\]

This is a finite-family approximation separation realized by legal
physical Hamiltonians. It also disproves extending that particular
conditional tradeoff to *all* legal physical ensembles. It neither
rules out other global obstructions nor proves full uniformity.

The low-order budget is .218, slightly looser than the previous witness's
certified .217405. We do **not** claim simultaneous improvement of both
objectives relative to that specific witness. The comparison is against
what the old family can achieve under the same .218 budget.

## 1. Physical discovery and derivative check

The frozen functional is L=y.V-Z_6 from the preceding note: 65 low-order
coefficients and the contiguous sixth coefficient -1. The new
[ising_sixth_pricing.py](ising_sixth_pricing.py) evaluates this same exact
coefficient selection numerically for discovery. Its six-minor term is
-(19721/5) times the average over the contiguous six-set's 42-element
orbit. Low-order terms use the existing scalar pricing implementation.

For R=exp(A), a determinant derivative is the cofactor contraction with
dR. Assemble the R-gradient G of the sixth term and use the adjoint
Frechet derivative B=Dexp(A^T)[G]. Free-edge derivatives are
2(B_{j,j+1}-B_{j+1,j}), added to the low-order gradients. Cofactors need
no inverse principal block, so singular principal submatrices are
allowed. This standard differentiation method is not an originality
claim. Central differences at coordinates 0/20/40 on a seeded test point
have max defect 2.7823e-7, below the stated 1e-4 discovery check threshold.

Two L-BFGS-B starts use old column 1614 and its fixed normal perturbation,
RNG 202611212242. Both stop at the 100-iteration limit, not a certified
maximum. Couplings are rounded to nine decimal places. All 41 internal
edges remain nonzero and the closing edge is exactly zero. The frozen
initial/final vectors and stopping messages are in
[evidence/sixth_pricing_escape_n21.json](evidence/sixth_pricing_escape_n21.json).

Independent 192-bit Arb calculations prove

\[
 L(c_0)\in[3788.4252101494142251608303580880483416403449890585088
                 \ \pm7.19\times10^{-50}],
\]
\[
 L(c_1)\in[3728.7163586105760378974254942033049004646045068931127
                 \ \pm6.50\times10^{-50}].
\]

Here every candidate decimal string is interpreted directly as an exact
rational, rather than substituting its binary64 counterpart. The proof
rebuilds its exponentials/minors without the optimizer, and recomputes
the exact functional target/coefficient norm against the preceding
certificate. See [the scalar proof](evidence/sixth_pricing_escape_verification_n21.json).

The connected-path pure-Pauli classification would force any pure-Pauli
rotation to be +/-I, where L=-28745015663/500000. Both witness intervals
are disjoint from this value, proving non-Pauli programs. This does not
prove that non-Pauli resources are necessary: some other pure-Pauli
seed family might also be useful, and no non-Clifford advantage follows.

## 2. Numerical reweighting and exact normalization

Appending both candidates gives 1641 numerical columns. The all-row
low/256-sixth LP at G_24<=.218 returns objective 1.5486146245091734,
versus the old-pool numerical 1.931381887620645. Direct low residual is
.21800000000000863. The tiny overshoot is retained honestly as a floating
diagnostic; raw LP weights are not treated as an exact feasible design.
Only candidate zero receives positive new weight, approximately
0.00017720834829388412. Candidate one is not needed by this returned
solution; no uniqueness/necessity theorem is inferred.

To define the certified witness, convert every nonzero LP weight exactly
from binary64 and normalize by its exact rational sum. Then mix that
normalized distribution with probability 1/100000 of the previous exact
70-orbit low-order witness. This creates a small interior margin. All
83 resulting probabilities are strictly positive and sum to one exactly.
The old 1639 couplings retain the preceding exact binary64-rational
convention; the new candidate couplings are exact decimal rationals.
These conventions are intentionally distinct and checked explicitly.

The [ensemble input](evidence/sixth_escape_ensemble_certificate_input_n21.json)
pins the source hashes, exact mixing probability and proof bounds.
[The complete proof transcript](evidence/sixth_escape_ensemble_certificate_n21.json)
records all exact probabilities. Physical signed-dihedral averaging gives
at most 83*84=6972 atoms counting multiplicity. The zero edge survives
these images, so the existing gap/gauge lemma applies to both parity
sectors. This is a witness ensemble, not a new inversion circuit.

## 3. Complete interval checks within the declared orders

At 128-bit Arb precision, the ensemble verifier rebuilds each selected
exact-input rotation and computes all 21 second rows and all 111930
four-principal minors, averaged into all 1440 fourth orbits. It also
computes every six-minor in the fixed 256 orbits (21091 distinct six-sets
per seed). Exact probabilities/averaging factors are used throughout.
Each low row is checked strictly inside +/-109/500, and each tested
sixth relative residual strictly inside +/-31/20.

The transcript's largest-midpoint diagnostics are

\[
 r_{24,882}\in[-0.2179999940430907677052477964037307
                         \ \pm6.08\times10^{-35}],
\]
\[
 r_{6,0}\in[1.548621135027835614323148142986884
                         \ \pm5.61\times10^{-34}].
\]

The common inequalities, not identification of exact maximizers, are the
proof. There are 9,290,190 fourth and 1,750,553 selected sixth determinants
in this calculation. The earlier old-family certificate is reused as a
proved bound; it need not be recomputed to evaluate the new witness.

These are relative Fourier-moment errors. Bounds on individual program
probabilities, off-diagonal program data, diamond/channel error, all
sixth orbits or higher orders do not follow. The tested sixth bound
still exceeds one; it is far from full target matching. No unrestricted
query advantage or original Nature Physics-level core theorem is claimed.

## 4. Reproduction and next action

Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0;
OPENBLAS_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1. Fixed proofs need
no numerical feature cache or optimizer:

```
python verify_ising_sixth_escape.py
python verify_ising_sixth_escape_ensemble.py
python -m unittest discover -s tests -v
```

Discovery and optional floating weight replay use the prior checked
low/sixth caches as documented in the preceding note:

```
python discover_ising_sixth_escape.py --output /tmp/eui-sixth-escape.json
python reweight_ising_sixth_escape.py --cache /tmp/eui-pool.npz --six-cache /tmp/eui-six-pool.npz
python reweight_ising_sixth_escape.py --cache /tmp/eui-pool.npz --six-cache /tmp/eui-six-pool.npz --replay
```

The proof/reweight tools read frozen evidence, not an arbitrary new
discovery output. Floating LP/optimizer rediscovery can depend on solver
versions; the exact fixed-input certificates do not rely on its success.
The [floating reweight study](evidence/sixth_pricing_escape_reweight_n21.json)
and [weight replay](evidence/sixth_pricing_escape_replay_n21.json) are
separate from both interval proofs.

**Next highest-value action:** recompute the expanded family's low/sixth
dual and price its new active higher-order directions, while auditing
additional sixth orbits outside the fixed screen before accepting claims
about higher-order quality. Do not infer full sixth closure from the
256 constraints. **Remaining blockers:** exact low-order feasibility,
complete higher-even-moment closure and full joint uniformity/minimax.
A failed local pricing run would not establish global nonexistence.

Latest main/recent Issues, relevant proof/code/evidence and the manuscript
with Appendix B were inspected. No manuscript sources are present. The
static-oracle design scope remains distinct from the broader robustness
and unrestricted-query claims; generic Gaussian derivatives and LP
column generation are not asserted as new EUI mechanisms.
