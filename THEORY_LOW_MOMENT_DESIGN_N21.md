# Certified feasibility of the n=21 low-moment screen, and its fourth-order failure

Date: 2026-11-20. Base commit: `6852042a6e1e93509e767f9ecc99b469abbbcc4d`.
Related: Issue #3; [minor criterion](THEORY_PROGRAM_MINOR_OBSTRUCTION.md);
[two-mirror obstruction](THEORY_TWO_MIRROR_OBSTRUCTION.md);
[conditional joint-parity converse](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md).

## Result and limitation

**Computer-assisted existence theorem.** There is a single ensemble of
legal gapped n=21 Ising Hamiltonians, averaged over physical dihedral
images, satisfying all 21 distance-averaged degree-two program moments
and the fourth-order moment on {0,1,2,3}, simultaneously in both physical
parity sectors. It has 22 seed orbits with strictly positive weights,
each exceeding 1/2000. Exact weights are defined by a nonsingular analytic
linear system; 192-bit ball arithmetic certifies nonsingularity and
positivity. They are not rounded floating weights asserted to be exact.

This proves that a universal obstruction using only these 22 invariant
features cannot exclude all legal gapped physical seeds. The previous
perfect-two-mirror obstruction remains valid for its restricted family.

**Certified counterexample to full uniformity of this ensemble.** Its
fourth-order moment on {0,2,21,23} differs from the required value by more
than 1/100. Thus this is a low-order feasibility result, not a full
uniform-program certificate and not a long-ring minimax corollary. It
neither proves nor disproves existence of another fully uniform ensemble.

## Frozen physical atoms

[evidence/ising_low_moment_design_n21.json](evidence/ising_low_moment_design_n21.json)
defines all atoms and the exact interpretation of their parameters:

- Thirteen perfect two-segment seeds, with both idle gaps allowed, using
  the signed mirrors and physical couplings from the previous note.
- Three fractional-transfer seeds: open segment length 41 at time factors
  1/4 and 1/2, and length 42 at factor 3/4. Their internal couplings are
  c_j=alpha*pi/4*sqrt((j+1)(L-j-1)); all outside edges vanish.
- Six general gapped seeds. Every stored decimal coupling is interpreted
  as the exact rational represented by that finite decimal, and the last
  coupling is exactly zero. Five came from a finite random search and
  one from optimizing a current separating functional.

All nonzero edges lie in an open path or a forest. In particular the
wrap edge is zero, even for the length-42 seed. The previous gap/gauge
lemma identifies the program masses in the two physical parity blocks;
we do not infer this for an ungapped periodic seed. Physical dihedral
images preserve this property.

The discovery metadata records RNG seeds and an approximate basic LP
solution for orientation only. The verified construction is defined by
the frozen atoms and the exact linear system below; reproducing the
optimizer is not needed to reproduce the scientific certificate.

## Exact linear system and why the omitted equation holds

Let N=42, R=exp(A), A_(j,j+1)=2c_j, A_(j+1,j)=-2c_j. Define

\[
 m_d(R)=\frac1{42}\sum_i\det R_{\{i,i+d\},\{i,i+d\}},
 \quad d=1,\ldots,21,
\]
\[
 q_I(R)=\frac1{84}\sum_{s=0}^{41}\sum_{\eta=\pm1}
 \det R_{s+\eta I,s+\eta I}.
\]

Indices are cyclic. Required values are t_d=(-1)^(d+1)/41 and
q_{0123}=1/533. For any even I of size 2k, the full target is
(-1)^(v+k)*binom(21,k)/binom(42,2k), v=#odd Majorana indices.

For each atom form its column with rows m_1,...,m_20,q_{0123},1.
This defines the 22-by-22 analytic matrix B. Define exact weights as
p=B^(-1)b, where b contains the corresponding exact rational targets and
normalization one. This square system proves exact equality, not merely
containment of zero by numerical residual balls.

The one omitted distance equation follows from an exact structural
identity. Since A is bipartite and Z=diag(1,-1,...), Z exp(A) is a symmetric
involution with trace zero. Its second elementary symmetric polynomial
gives, with the antipodal pair multiplicity included,

\[
 \sum_{d=1}^{20}(-1)^{d+1}m_d+\tfrac12m_{21}=\tfrac12.
\]

Each atom obeys it. Normalization of p and the first twenty equations
therefore force E m_21=1/41. The determinant and strict positivity checks
certify a physical positive mixture satisfying every asserted equation.
Dihedral averaging turns these invariant features into the corresponding
individual second-order moments and the complete orbit of the selected
fourth-order moment. No other fourth-order equation follows from this
argument.

## Certified bounds and independent higher-order checks

At 192 bits the verifier certifies

\[
 \det B=[3.088169808307897296756219211560721795481972378453
 \times10^{-24}\ \pm\ 3.14\times10^{-73}],
\]
\[
 \min_j p_j=[0.0007116950239929113846941430708519016421251830114558
 \ \pm\ 4.77\times10^{-53}]>1/2000.
\]

For the distant probe I={0,2,21,23}, whose target is 1/533,

\[
 \mathbb E q_I-1/533=
 [0.0129392316409538071962346592130359334639942998783639
 \ \pm\ 6.47\times10^{-53}]>1/100.
\]

A second checked probe, {0,1,2,4}, also fails: its target is -1/533 and its
residual lies in [-0.00557596461544756 +/- 6.25e-18]. Neither selected
higher-order witness is an LP constraint used to determine p.

A separate finite floating audit enumerates all binom(42,4)=111,930
quartets and groups them into 1,440 cyclic/reflection orbits. Of these,
1,439 have residual magnitude above 1e-8 for this ensemble. The largest
absolute residual is at {0,2,21,23}, consistent with the independently
certified interval above. The all-orbit counts and ranking are numerical
diagnostics, not interval proofs for every orbit. Their practical message
is that satisfying one fourth-order orbit leaves substantial structure
uncontrolled.

## Reproduction and evidence status

Dependencies: Python, NumPy/SciPy, python-flint. This run used Python
3.12.14, NumPy 2.3.5, SciPy 1.17.0 and python-flint 0.9.0.

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_low_moment_design.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_low_moment_design.py --audit-fourth
```

The first rebuilds exact perfect rotations or interval matrix exponentials
from the frozen parameters, verifies B is invertible, solves for p,
certifies positivity, checks all asserted moment equations and two failing
higher probes. The analytic redundancy argument above supplies the
omitted exact equation. The second additionally performs the floating
all-quartet audit using midpoints of the certified rotations and weights.
Frozen outputs are
[evidence/ising_low_moment_verification_n21.json](evidence/ising_low_moment_verification_n21.json)
and [evidence/ising_low_moment_fourth_audit_n21.json](evidence/ising_low_moment_fourth_audit_n21.json).
The input file's approximate weights are not read by either certificate
solve or audit.

## Scientific implication and next highest-value action

The previous 30 fractional seeds can escape one separator but did not
make the finite 22-feature pool feasible. A directed coupling search
supplied a new physical column and made the reduced target attainable;
the ball certificate upgrades that discovery to a low-order existence
proof. Failure of the earlier finite pools was therefore not evidence
of a universal 22-feature physical obstruction.

The next search should enforce the distant probe {0,2,21,23} immediately
and use column generation against the **full set of fourth-order orbit
constraints**, rather than repeatedly certifying one extra local probe.
A successful fourth-order solution would still require higher even
moments or an analytic implication before extending the conditional
long-ring minimax theorem. General joint uniformity remains open.

The inspected manuscript and Appendix B at
[arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1) study a broader
robustness promise. No manuscript sources are present in this repository;
this update is a research-note and reproducibility result, without a
literature-wide novelty or journal-readiness claim.


## Follow-up: single fractional-segment extension screen (2026-11-24)

A 384-bit Arb affine-reweighting test added each of 27 previously absent fractional-segment seeds from the predeclared \((L,\alpha)\) grid and asked whether one new positive weight could repair the distant fourth-order probe \(\{0,2,21,23\}\) while preserving the 21 second moments, the consecutive fourth probe, and normalization. Twenty-five candidates have strictly positive affine slopes (hence negative required new weights), and two are exact duplicate even-minor columns by spin periodicity. Thus every one of the 27 candidate slopes is nonnegative. The affine formula then proves a stronger finite-family result: no nonnegative mixture of any subset of these 27 seeds can repair the distant fourth probe while preserving the 22 base constraints. This does not rule out fractional parameters outside the grid or general gapped couplings. See [the exact affine reduction and convex-cone obstruction](THEORY_LOW_MOMENT_FRACTIONAL_SINGLE_ATOM_SCREEN_N21.md).


## Follow-up: positive 41-atom two-fourth-probe ensemble (2026-11-24)

A deterministic 8,241-column fractional-path LP found 19 new fractional open paths that, together with the original 22 atoms, repair the distant fourth probe. The exact Arb verifier uses the frozen decimal LP weights only as a seed, rescales them by the exact interval factor gamma, and independently certifies all 41 final weights strictly positive. It verifies all 21 distance moments and both q_{0,1,2,3}=1/533 and q_{0,2,21,23}=1/533 with 384-bit Arb.

The minimum final weight is 0.0001108520975446446100... and the maximum is 0.3065707132581335893.... Two other fourth-order probes are still strict failures, so this is not a complete fourth-order design. See [the full derivation](THEORY_LOW_MOMENT_TWO_FOURTH_PROBE_ENSEMBLE_N21.md) and [the exact certificate](evidence/ising_low_moment_two_fourth_ensemble_n21.json).

The earlier 27-seed and 861-seed results remain valid finite-family obstructions for their exact candidate sets. The 861-seed coarse grid is bypassed by the finer 0.01 grid; neither finite-grid obstruction is a global no-go for fractional paths or general gapped couplings.
