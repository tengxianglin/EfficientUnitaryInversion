# An exact fourth-order obstruction for all two-mirror placements at n=21

Date: 2026-11-20. Base: `7468a5fbb07c6c00bdd2b16fce226409312248af`.
This advances Issue #3's long-ring joint uniform ensemble problem.

## Result and scope

**Computer-assisted theorem (exact finite-family proof).** At n=21, no
convex mixture of at most two disjoint contiguous perfect-mirror segments,
idle spectators, their cyclic/reflection images, and vertex-sign gauges
has uniform balanced program masses. Arbitrary segment lengths and both
idle-gap lengths are allowed. The obstruction already uses the 21
second-order conditions and one fourth-order condition. It applies jointly
to the physical parity sectors since all these seeds have a zero edge.

This strengthens the previous rejection of one particular two-segment
mixture. It is not an all-n theorem and does not rule out fractional
transfer times, three or more active segments, or general physical
couplings. It does not establish or refute the general long-ring ensemble
hypothesis or unrestricted inversion optimality.

## Family and completeness of enumeration

Use N=42 Majorana vertices. A segment of length L has couplings
c_j=(pi/4)sqrt((j+1)(L-j-1)), and its exact rotation is the signed mirror
(R_L)_(i,L-1-i)=(-1)^i. All edges outside segments, including edges between
them and the closing edge, are zero. The construction and conventions are
in [the principal-minor note](THEORY_PROGRAM_MINOR_OBSTRUCTION.md).
The perfect-transfer primitive is established literature, not a novelty
claim; that note cites Christandl et al. and Bravyi for the standard tools.

After a cyclic rotation every two-segment placement can be specified by
(a,b,g): segment A starts at vertex 0, has length a>=1; an idle gap has
length g>=0; segment B has length b>=1; the remaining idle gap has length
42-a-b-g>=0. Thus a+b<=42 and 0<=g<=42-a-b. There are
binom(43,3)=12,341 ordered configurations. Duplicates under symmetry are
retained. Every single segment of length <=41 is included by taking the
second segment to have length one (an identity spectator). Add the full
open 42-vertex mirror separately, giving 12,342 columns. The identity is
included. No continuous coupling search is being claimed complete.

For a signed permutation with row permutation p and signs s, a principal
minor on I vanishes unless p(I)=I. When it is nonzero, it is exactly the
permutation sign of p restricted to I times the product of its row signs.
This supplies all needed minors by integer operations.

## Exact separating inequality

Let m_d=(1/42) sum_i det R[{i,i+d},{i,i+d}], d=1,...,21, with cyclic
indices. Let q=(1/42) sum_i det R[I_i,I_i], where
I_i={i,i+1,i+2,i+3}. Reflection gives the same consecutive-set average,
so q is already the complete dihedral average of this probe.
The uniform target, by the Fourier/minor criterion, is

\[
 t_d=(-1)^{d+1}/41,\qquad q_* = 1/533.
\]

Define L(R)=sum_d y_d m_d -209 q, with integer coefficients in distance order

```
y = [-209, 198, -201, 209, -3, 0, 6, 11, 181, -12, 15,
     -36, 42, -52, 44, -23, 206, -209, 54, -19, 4].
```

Exact enumeration proves

\[
 \max_{\text{12,342 configurations}} L(R)=-3,
 \qquad L(t,q_*)=727/533,
 \qquad L(t,q_*)-(-3)=2326/533>0.                 \tag{1}
\]

To check this without floating arithmetic, multiply all features by 42.
Their numerator row has 22 integer entries. The dot product with (y,-209)
is at most -126 for every row; 120 rows attain it. The full 42-vertex
mirror has score -140. The frozen certificate records the coefficients,
maximum and target exactly, and a hash of all generated integer rows.
All dot products are far below the signed 64-bit integer limit (the
absolute-value bound 22*42*209 suffices).

Equation (1) is a convex-hull separation, so it excludes every positive
mixture, including arbitrary real probabilities. Vertex-sign gauges
preserve principal minors; cyclic/reflection maps preserve m and q.
If an unsymmetrized ensemble in this family were uniform, symmetrizing
it would remain uniform and have these averaged features. Therefore the
same separation excludes unsymmetrized ensembles as well. This completes
the finite-family theorem; an LP infeasibility status alone is not used
as proof.

## Verification and evidence

Run:

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_two_mirror_obstruction.py
```

The default verifier enumerates every configuration and verifies (1)
with integer arithmetic and exact `Fraction` targets. It also compares
six boundary/interior configurations with the earlier independent
unordered-pair enumerator and all 84 dihedral images of the exact
four-by-four minor calculation. The antipodal second-order moment has
its required factor of two. Output is frozen in
[evidence/two_mirror_obstruction_n21.json](evidence/two_mirror_obstruction_n21.json).
The canonical row checksum is SHA256 over row-major little-endian signed
64-bit integers, in the generator's displayed lexicographic order.

Optional `--discover` additionally runs the 22-condition floating HiGHS
feasibility LP, which reports infeasible. Solver output is corroboration;
the integer certificate is the evidence for the theorem. Discovery used
NumPy 2.3.5 and SciPy 1.17.0 with Python 3.12.14. No interval extrapolation
or numerical diamond-norm optimization is involved.

The previous exact 21-atom degree-two solution remains valid. Its failure
at fourth order now reflects an obstruction to the entire two-mirror
family, rather than just an unfortunate choice of weights.

## Relation to the paper and next action

The inspected [manuscript and Appendix B](https://arxiv.org/html/2506.20570v1)
use a broader robustness perturbation model; this note concerns the
separate fixed six-query encoder and the joint ensemble hypothesis of
[the Pauli-architecture converse](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md).
No manuscript theorem is silently extended by this result. There are no
manuscript TeX/PDF sources in the inspected repository; this update is a
research-note and reproducibility result.

The next highest-value step is to test fractional-transfer versions of
these gapped seeds against this explicit 22-feature separator. A family
must cross its bound before a full positive-mixture search is useful.
Then add the remaining fourth-order orbit conditions before treating
any low-order feasibility as evidence for full uniformity. Three-segment
seeds are another route, but all higher even moments ultimately remain
required. General joint uniformity at admissible long rings remains open.

## Completed fractional-time pre-screen (finite numerical evidence)

The 30-case grid with lengths 10,21,30,41,42 and time multipliers
1/8,1/4,1/2,3/4,5/4,3/2 has also been run. Its best case is one open
segment of length 41 at multiplier 5/4: L(R)=13.331690721787323 in
NumPy/SciPy floating arithmetic, exceeding both -3 and the target
727/533=1.3639774859287055. These gapped fractional seeds can therefore
escape this particular obstruction numerically; their moment vector is
not asserted to equal the target. No positivity of an ensemble or full
uniformity follows from this one functional.

Reproduce with `python verify_ising_two_mirror_obstruction.py --fractional`;
output is frozen in
[evidence/fractional_mirror_screen_n21.json](evidence/fractional_mirror_screen_n21.json).
This is a finite floating diagnostic, separate from the exact theorem.
The next concrete search should include the length-41, 5/4 seed and its
dihedral images when solving all 22 constraints. This avoids repeatedly
searching a perfect-transfer family now known to be impossible.

## Follow-up: reduced physical feasibility is certified

The [n=21 low-moment certificate](THEORY_LOW_MOMENT_DESIGN_N21.md) constructs a positive gapped physical ensemble satisfying all 21 degree-two conditions and the consecutive fourth-order probe. It uses fractional and general gapped seeds beyond the perfect-mirror theorem. A distant fourth-order probe is certified to fail by more than 1/100, so full joint uniformity remains unresolved.
