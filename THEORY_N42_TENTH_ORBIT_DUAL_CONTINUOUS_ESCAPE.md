# A rationalized tenth-orbit dual has a certified continuous period-two escape

Date: 2026-11-27.

## Setup

Let \Phi(a,b) be the 41-component period-two feature column used by the
10-quartic-orbit candidate-pool feasibility LP:
- 30 independent pair features (10 same-parity and 20 cross-parity);
- ten one-site-symmetrized quartic principal-minor coordinates;
- a normalization coordinate equal to one.

The target vector is
```
tau = ((-1/41) repeated 30 times,
       ( 1/533) repeated 10 times,
       1).
```
The ten quartic representatives are listed in
[evidence/n42_period_two_tenth_orbit_dual_escape.json](evidence/n42_period_two_tenth_orbit_dual_escape.json).

## Exact rational functional and physical witness

A floating HiGHS Farkas candidate from the 100,000-column, ten-orbit
discovery LP was rounded coefficientwise to six decimal places; its
normalization coefficient was then increased by 1/1,000,000. The resulting
41 coefficients are frozen as exact rational numbers in the JSON evidence.

At the exact-rational period-two point
```
a = 8.94088796,   b = 97.09897923,
```
all 42 cycle couplings are strictly positive. The independent 256-bit Arb
workflow [45933314487](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45933314487)
certifies
```
y^T tau       = [-0.999999264540337711... +/- 7.40e-75] < 0,
y^T Phi(a,b)  = [-0.483006473660593274... +/- 8.31e-72] < 0.
```

Thus this exact rational functional is not a global separator for the
continuous period-two physical family: it is negative on an allowed physical
atom (and on the target).

## What this does and does not establish

The original ten-orbit floating LP was infeasible on one fixed 100,000-point
candidate pool. After rationalization and the 1e-6 normalization shift, a
binary64 screen found no negative score among those 100,000 columns, with a
minimum score about 6.18e-7. That screen is not an independent interval
certificate.

Accordingly:
- **Proved:** the frozen exact rational functional has negative target score
  and negative score on the exact-rational, strictly-positive period-two
  physical witness above.
- **Not proved:** that the rationalized functional is nonnegative on every
  column of the finite 100,000-point pool.
- **Not proved:** a finite-pool Farkas theorem, a continuum no-go, or
  infeasibility of the complete physical period-two moment problem.

This is a rigorous rejection of this proposed global dual, not a theorem
about the convex hull itself.

## Reproducibility

- Rational input: [evidence/n42_period_two_tenth_orbit_dual_escape.json](evidence/n42_period_two_tenth_orbit_dual_escape.json)
- Independent verifier:
  [verify_n42_period_two_tenth_orbit_dual_escape_arb.py](verify_n42_period_two_tenth_orbit_dual_escape_arb.py)
- Machine certificate:
  [evidence/n42_period_two_tenth_orbit_dual_escape_arb.json](evidence/n42_period_two_tenth_orbit_dual_escape_arb.json)
- Workflow:
  [eui-n42-period-two-tenth-orbit-dual-escape.yml](.github/workflows/eui-n42-period-two-tenth-orbit-dual-escape.yml)
- Successful CI: [45933314487](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45933314487)

The next useful step is not to reuse this functional as a separator. Instead,
derive a different dual with a verified finite-pool Farkas margin, then run
continuous pricing before making any global claim.
