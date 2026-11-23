# Strict 192-column mixed-order minimax obstruction after the ninth continuous escape

## Theorem

Let \(A\in\mathbb R^{2113\times192}\) be the frozen EUI moment-feature matrix and \(y\in\mathbb R^{2113}\) its target vector for the pinned design. The 192 columns are the ordered physical pool recorded in
`evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json`: 183 selected canonical generators and nine pairwise-distinct, strictly positive 41-edge open-path generators, including the ninth escape from the 191-column dual.

Then every probability vector \(p\in\Delta_{192}\) obeys
\[
\boxed{
\|Ap-y\|_\infty\ge
\frac{49457924053915886516751}
{112589990684262400000000}
=0.43927460827855824\ldots>\frac13.
}
\]

This is a theorem for this fixed 192-generator pool and this fixed 2,113-row mixed-order design. It is not a minimax theorem for the full continuous physical family.

## Exact dual data

The independent verifier reconstructs a rational vector \(z\in\mathbb Q^{2113}\) and \(\lambda\in\mathbb Q\) from the stored HiGHS marginals, with
\[
\|z\|_1=
\frac{144115188075273773}{144115188075855872}<1,
\]
\[
\lambda=
\frac{6145476815434803}{4503599627370496},
\qquad
\beta:=\lambda+z^{\mathsf T}y
=
\frac{126612288460328431}{288230376151711744}.
\]
The verifier selects the exact slack
\[
\delta=\frac1{10^8}.
\]

For every one of the 192 physical columns \(a_j\), a 128-bit Arb evaluation certifies
\[
z^{\mathsf T}a_j+\lambda-\delta<0.
\]
All 192 outward-rounded interval upper endpoints are strictly negative. The largest upper endpoint is enclosed by
\[
[-6.5812383148672463128658647839462803268\times10^{-9}
\ \pm 3.53\times10^{-47}]<0.
\]
The exact rational lower bound is
\[
\beta-\delta=
\frac{49457924053915886516751}
{112589990684262400000000},
\]
and its margin above \(1/3\) is
\[
\frac{35783781477485259550253}
{337769972052787200000000}.
\]

The dual has 61 nonzero coordinates: two complete low-order rows, 56 selected/cut sixth-order rows, and three selected eighth-order rows.

## Proof

The Arb column audit gives \(z^{\mathsf T}a_j+\lambda\le\delta\) for every \(j\). Hence, for any \(p\in\Delta_{192}\),
\[
z^{\mathsf T}Ap+\lambda
=\sum_{j=1}^{192}p_j(z^{\mathsf T}a_j+\lambda)
\le\delta.
\]
Subtracting \(z^{\mathsf T}y\) yields
\[
-z^{\mathsf T}(Ap-y)\ge\beta-\delta>0.
\]
By Hölder duality,
\[
\beta-\delta
\le |z^{\mathsf T}(Ap-y)|
\le \|z\|_1\|Ap-y\|_\infty
\le \|Ap-y\|_\infty,
\]
because the exact rational certificate has \(\|z\|_1<1\). This proves the claim.

## Frozen design and scope

The 2,113 rows are exactly:
- 1,461 complete second-/fourth-order rows;
- 645 selected/cut sixth-order rows (311 selected rows plus the frozen complete-scan cuts);
- seven selected eighth-order rows.

The verifier pins the 1,600-by-42 seed pool, the full 1,641-column canonical inventory, the row inventories, the 152-column cut LP and dual, the 191-column parent LP and dual, and all nine continuous-escape Arb certificates by SHA256. It checks that the nine escape inputs are pairwise distinct and that each has 41 strictly positive physical edge magnitudes.

Consequently, this result:
1. proves a strict mixed-order minimax obstruction for every convex mixture over these 192 fixed generators;
2. does not prove a lower bound for every generator in the 1,641-element canonical inventory (only 183 canonical columns are in this 192-column pool);
3. does not prove a no-go or feasibility theorem for the unrestricted positive 41-edge path family;
4. does not certify the complete sixth- or eighth-order orbit objectives;
5. does not by itself imply a Choi-infidelity or diamond-distance guarantee.

## Reproduction

Use Python 3.11 with the workflow-pinned versions:
`numpy==2.3.5`, `scipy==1.15.3`, and `python-flint==0.8.0`.

```bash
python freeze_seed_pool.py
python -m unittest tests/test_eighth_orbit_enumeration.py
python verify_192col_ninth_continuous_escape_dual_arb.py
```

The verifier independently reconstructs the exact rational dual, checks the complete ancestry and frozen row/column hashes, evaluates all 192 physical columns with 128-bit Arb, and writes the machine-readable certificate.

Evidence:
- LP transcript: `evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json`
- 128-bit Arb certificate: `evidence/55probe_192col_ninth_continuous_escape_dual_certificate_n21.json`
- Independent verifier: `verify_192col_ninth_continuous_escape_dual_arb.py`
- Workflow: `.github/workflows/eui-192col-ninth-continuous-escape.yml`
- Certificate-output commit: [4ad5c5472c391a8ca07bb316ab2f7028ec7d5234](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/4ad5c5472c391a8ca07bb316ab2f7028ec7d5234)
- LP transcript SHA256: `ed966f1c3f755b1910f7f34be978af88ee290821ea643cb7690d83c7aeab686a`
- Certificate JSON blob SHA: `df4855cc985ae34507039e83ef3e43c446c2c66d`

## Next continuous-family test

The exact dense-torus theorem in `THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md` applies to every continuous pricing functional, including the new 192-column dual pricing functional. The next decisive test is therefore to optimize this *192-column* functional over the 21-torus of the uniform positive-coupling ray. A strictly positive Arb-certified torus value would, by continuity and orbit density, prove that this particular 192-column dual also fails to separate the full positive path family. A nonpositive numerical maximum or an unsuccessful local search would not prove global separation; that would require a certified global upper bound over the torus.
