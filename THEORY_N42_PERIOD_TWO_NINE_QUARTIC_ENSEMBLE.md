# N=42 period-two positive ensemble with nine quartic translation orbits

Date: 2026-11-27. This is a certified extension of the six-orbit partial design in
[THEORY_N42_PERIOD_TWO_SIX_QUARTIC_ENSEMBLE.md](THEORY_N42_PERIOD_TWO_SIX_QUARTIC_ENSEMBLE.md).

## Statement and physical family

Let N=42 and n=21. For each base atom \ell, take a period-two cycle coupling
```
c_(2j)   = a_l,
c_(2j+1) = b_l,       j=0,...,20,
```
with a_l,b_l>0. Let R_l=exp(A(c_l)), D=diag(1,-1,...,1,-1), and Q_l=R_l D.
Include the one-site translate (b_l,a_l) with equal half of the base-atom
weight. This produces a one-site translation-invariant physical ensemble.

The balanced-slice target in Q coordinates is
```
E det Q_{I,I} = -1/41,  |I|=2,
E det Q_{I,I} =  1/533, |I|=4.
```

## Frozen support and exact-real weights

The frozen support contains 40 base atoms, each stored as a finite decimal and
therefore interpreted as an exact rational input. All 80 expanded atoms have
strictly positive cycle couplings. The minimum coupling is exactly
```
5804273538392679 / 1000000000000000 > 0.
```

The exact-real base weights are defined as the unique solution of a 40x40
linear system consisting of:
- 30 independent period-two pair-feature equations;
- nine symmetrized quartic principal-minor equations;
- normalization.

The omitted 31st independent cross-parity pair equation follows from the
period-two row-norm identity already used in the six-orbit construction.
The weights are not asserted to be rational: the matrix entries contain
trigonometric functions of the rational couplings. The proof is a
computer-assisted interval certificate: the determinant interval excludes
zero and every exact-real weight is enclosed in a strictly positive Arb
interval.

The nine quartic representatives are
```
[0,1,2,3]       [0,3,10,15]      [0,2,4,6]
[0,10,20,30]    [0,2,21,23]      [6,13,14,30]
[0,3,19,26]     [0,8,20,28]      [0,4,8,12].
```
Their full cyclic-translation orbit sizes are
```
42, 42, 42, 42, 21, 42, 42, 42, 42,
```
so the matched fourth-order set contains 357 distinct four-subsets.

## Certified result

The independent 256-bit Arb verifier certifies:
- the 40x40 moment matrix is invertible (determinant interval excludes zero);
- the minimum exact-real weight is enclosed by
  `[0.0007816680367558847538021943219787... +/- 4.04e-72]`,
  hence exceeds the prescribed floor 1/10000;
- the weights sum to one;
- all 861 unordered pair principal-minor coordinates equal -1/41;
- all 357 distinct translated quartic coordinates in the nine listed orbits
  equal 1/533.

The hosted run [45932791312](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45932791312)
passed all steps. The determinant enclosure was
`[6.9410873420103589179538316236902944e-50 +/- 9.65e-117]`.

This is an exact positive physical ensemble for the stated partial moment
system. "Exact" refers to exact-rational coupling inputs and rigorous interval
enclosures of the uniquely defined real weights and moments.

## A certified tenth-orbit miss for this frozen support

The next quartic representative found by the full-orbit screen is
```
I_10 = [0,3,18,21].
```
Its orbit has 42 distinct translates and is disjoint from the nine matched
orbits. The Arb verifier checks every translate and proves
```
E det Q_{I,I} - 1/533 > 1/250
```
for all 42 translates in this particular 80-atom ensemble. A representative
moment is enclosed near 0.0064165635096204070, whereas the target is
0.00187617260787992495....

This is a candidate-specific failure of the frozen support, not a no-go
theorem for other period-two mixtures.

## Discovery and finite-pool boundary

The deterministic discovery used NumPy 2.3.5 / SciPy 1.17.0, seed 351, and
100,000 candidate pairs sampled uniformly from [0,100]^2. A binary64 HiGHS
LP found the 40-atom support with selected-equation residual
8.881784197001252e-16. A deterministic screen enumerated all 2,670 cyclic
translation orbits of four-subsets, whose orbit sizes sum to all 111,930
four-subsets. Its largest absolute residual for this support is the tenth
orbit above, about 0.004540390901740525.

Adding that tenth orbit makes the LP infeasible on this fixed 100,000-column
candidate pool. Both the scan and this infeasibility status are discovery
evidence only; neither is a theorem about the continuous period-two family.
A rational Farkas certificate and continuous pricing have not yet been
completed.

## Scope and limitations

Proved by the hosted Arb certificate:
- a strictly-positive 80-atom period-two physical ensemble matches all 861
  pair coordinates and 357 specified quartic coordinates;
- the same frozen ensemble misses the tenth orbit by more than 1/250.

Not proved:
- a complete fourth-order design (the full quartic system has 111,930
  coordinates);
- any sixth- or higher-order moment constraints;
- feasibility or infeasibility of the complete all-even-principal-minor
  target over all real cycle couplings;
- a program-label TV to Choi trace-distance or channel diamond-distance
  implication.

No global physical-family converse or operational channel bound is claimed.

## Reproducibility

- Frozen support:
  [evidence/n42_period_two_nine_quartic_atoms.json](evidence/n42_period_two_nine_quartic_atoms.json)
- Floating discovery and full-orbit scan:
  [discover_n42_period_two_nine_quartic_ensemble.py](discover_n42_period_two_nine_quartic_ensemble.py)
- Independent verifier:
  [verify_n42_period_two_nine_quartic_ensemble_arb.py](verify_n42_period_two_nine_quartic_ensemble_arb.py)
- Workflow:
  [.github/workflows/eui-n42-period-two-nine-quartic.yml](.github/workflows/eui-n42-period-two-nine-quartic.yml)
- Discovery transcript:
  [evidence/n42_period_two_nine_quartic_discovery.json](evidence/n42_period_two_nine_quartic_discovery.json)
- Arb certificate:
  [evidence/n42_period_two_nine_quartic_ensemble_arb.json](evidence/n42_period_two_nine_quartic_ensemble_arb.json)
- Workflow:
  [45932791312](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45932791312)
- Evidence commit: `dfcf43d`.
