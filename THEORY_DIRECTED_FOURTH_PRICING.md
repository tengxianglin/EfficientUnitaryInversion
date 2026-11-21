# A certified finite-pool separator and a physical column beyond it

Continuation: [eight further pricing steps and a certified reflection-averaging
counterexample](THEORY_ITERATED_FOURTH_PRICING.md). The enlarged pool remains
numerically infeasible; the original finite-pool certificate below retains
its original scope.

Date: 2026-11-21. Base: `9a95c61a289ecd49bfeab4bd4473a1a70ac95c60`.
Related: Issue #3, [complete fourth-order system](THEORY_FOURTH_MOMENT_HIERARCHY.md),
[pure-Pauli classification](THEORY_PURE_PAULI_CLASSIFICATION.md), and
[conditional joint-parity converse](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md).

## Results and logical boundaries

**Certified finite-pool theorem.** A fixed rational linear functional L
of 49 dihedrally averaged fourth-order Majorana minors satisfies
L(H)<-6/5 for all 1600 seeds in the previous pool. Its value at the uniform
moment target is exactly -505837519/533000000, strictly greater than
-6/5. No positive mixture of that pool, including its dihedral images or
vertex-sign gauges, can match these 49 fourth-order moments. This
upgrades the prior numerical finite-pool failure to an interval-verified
separation for the precisely encoded inputs.

**Certified physical pricing witness.** A new legal gapped connected-path
Hamiltonian, with exact decimal-rational couplings, satisfies

\[
 L(H_*)=[0.064634182899040801543102197020054618125681679581782
             \ \pm\ 5.99\times10^{-52}]>1/20,
\]
\[
 L(H_*)-L(\text{uniform target})=
 [1.013672680084781889723214767376527413622867420669962
             \ \pm\ 4.87\times10^{-52}]>1.
\]

The finite-pool bound therefore cannot be promoted to a global bound on
legal physical couplings. This is an explicit new column from directed
optimization, not a proof that the full uniform target is feasible.

**Numerical continuation.** Adding that column gives 1601 candidates.
The complete reduced second/fourth-order feasibility LP still reports
infeasible. Its next normalized finite-pool dual gap is approximately
0.2471042713022, and the next suggested direction has 55 fourth-order
terms. These are separately frozen floating diagnostics, not an exact
certificate for the enlarged pool or a general no-go theorem.

## 1. A fixed rational functional, independent of solver tolerances

For a fourth-order orbit o of the 42-cycle, let

\[
 q_o(R)=\frac1{|o|}\sum_{I\in o}\det R_{I,I},
 \qquad L(R)=\sum_{o\in\mathcal O_{49}} a_o q_o(R).
\]

All 49 orbit representatives and rational a_o are frozen in
[evidence/directed_fourth_pricing_n21.json](evidence/directed_fourth_pricing_n21.json).
The coefficient list was found by an L1-normalized finite-pool LP on the
previous reduced/scaled moment coordinates, then rounded to six decimal
places and interpreted exactly. Optimality of that LP is **not** used in
the proof. Any frozen rational functional can supply a valid separator
if its inequalities are independently verified.

The 49 orbits contain 2058 distinct four-sets. Averaging distinct four-sets
is identical to averaging all 84 dihedral images, including the proper
multiplicity for orbits with stabilizers. The implementation uses
coefficient a_o/|o| for each four-set.

For the required target, q_o=(-1)^v(I)/533, v(I)=number of odd indices.
Exact rational evaluation gives

\[
 L_*=-505837519/533000000,
 \quad L_*-(-6/5)=133762481/533000000>0.               \tag{1}
\]

At 128-bit ball precision the verifier rebuilds each 42-by-42 rotation
exp(A), evaluates the weighted principal determinants, and checks
L(H_j)<-6/5 for **every** j=0,...,1599. The largest midpoint occurs at
index 303, with enclosure

\[
 [-1.21335767072456497192781268331801942
        \ \pm\ 5.64\times10^{-36}].
\]

The common bound -6/5, rather than identification of the exact maximizer,
is the certificate. Convexity and (1) give the finite-pool exclusion.
Principal minors are invariant under vertex-sign conjugation; L is also
dihedrally invariant, so the exclusion includes those transformed seeds.

The exact interpretation of the old numerical inputs is explicit:
`seed_pool()` generates the frozen binary64 values, whose little-endian
SHA256 is checked against the prior experiment, and **each binary64 value
is interpreted exactly as a rational**, using `Fraction.from_float`.
No rounded decimal approximation is substituted for the pool. The new
witness instead has explicitly frozen six-decimal rational parameters.
These two input conventions are intentional and distinct.

## 2. Directed discovery with an exponential Frechet derivative

The local optimizer starts from the old maximizing seed, index 303: an
open uniform path of internal coupling approximately 20.69130573548436.
It varies all 41 internal couplings, keeping the closing edge exactly zero.
A 61-iteration L-BFGS-B run found the recorded candidate; rounding to six
decimal places preserves the independently certified strict inequality.
The discovery command reproduces the same rounded parameters in this
environment. Convergence does not certify a global maximum.

The gradient has no inverse-principal-block assumption. If R=exp(A) and
G=gradient_R L is assembled from determinant cofactors, then

\[
 dL=\langle G,\mathcal L_{\exp}(A,dA)\rangle_F
    =\langle\mathcal L_{\exp}(A^T,G),dA\rangle_F.
\]

Consequently, setting \(B=\mathcal L_{\exp}(A^T,G)\), the free-edge derivative is

\[
 \frac{\partial L}{\partial c_j}=2(B_{j,j+1}-B_{j+1,j}).
\]

Cofactors remain valid when a principal block is singular. The adjoint
identity follows directly by transposing the power-series derivative of
the matrix exponential. The implementation uses
[SciPy's `expm_frechet`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm_frechet.html),
which documents the standard Al-Mohy--Higham method. A finite central-
difference check at coordinates 0,20,40 has maximum defect about
4.43e-10. That is a discovery-code check, not a global optimization or
existence proof. The frozen interval witness is the existence evidence.
Neither Frechet differentiation nor generic LP column generation is
claimed as a new EUI primitive.

## 3. The physical witness is not a pure-Pauli shortcut

The input JSON lists all 42 c_j. The last is exactly zero; all 41 internal
couplings are positive rationals, between 15.584677 and 23.304666, and
exactly reflection symmetric. It is therefore a connected open path,
and the existing gap/gauge lemma ensures matching program masses in the
two physical parity sectors.

The complete pure-Pauli classification gives a useful independent check.
If a connected-path exponential is a pure Pauli program in one sector,
its Majorana rotation is +/-D_T. Commutation with the generator forces
D_T to be constant along every nonzero edge; connectivity then forces
R=+/-I. All fourth-order principal minors would be one, and the functional
would equal the exact identity value

\[
 L(I)=\sum_o a_o=-100315369/200000.
\]

The certified witness enclosure is disjoint from that value. Thus this
new physical column has a genuinely non-Pauli program; it is not merely
an overlooked matching-Pauli label. This does not imply a non-Clifford
resource lower bound or any unrestricted query advantage.

## 4. One complete finite-pool continuation step

The new seed's complete 1461-dimensional second/fourth feature vector is
appended to the old 1600 columns. The previous exact hierarchy selects
1314 equivalent equations including normalization. The augmented
HiGHS-IPM solve reports status 2, infeasible. A fresh L1-normalized dual
solve reports status 0 and gap approximately 0.24710427130220025.

The next direction's 55 floating coefficients are frozen in
[evidence/directed_fourth_augmentation_n21.json](evidence/directed_fourth_augmentation_n21.json).
It is a proposal for the next pricing step; it has not been promoted to
a rational interval-verified separator here. In particular, the old
functional no longer bounds the enlarged pool, and its old certificate
must not be used as a proof about all 1601 columns.

The scientific conclusion is specific: the old finite pool really is
separated from the target, but a local search already finds legal physical
points beyond that separation. Full fourth-order feasibility is still
unresolved, and even a positive fourth-order design would require higher
even moments before extending the long-ring conditional minimax theorem.

## 5. Reproduction and exact objects

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_moment_pricing.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_moment_pricing.py --pool
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python discover_ising_moment_pricing.py
```

The first verifies the fixed witness and target inequality at 192 bits,
checks positive/reflection-symmetric connected couplings, and checks the
discovery gradient. The second additionally certifies all 1600 old inputs
at 128 bits; no LP or optimizer is required for either proof.
The third repeats the local discovery, whose exact candidate identity is
not needed for the validity of the fixed certificate.

To reproduce the numerical continuation, first obtain the full feature
cache using `verify_ising_fourth_moments.py --search --cache /path/pool.npz`,
then run

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python discover_ising_moment_pricing.py --study --cache /path/pool.npz
```

The study checks the old feature fingerprint and records the appended
column fingerprint, solver statuses and next direction. Its result is
numerical evidence only. Environment: Python 3.12.14, NumPy 2.3.5,
SciPy 1.17.0, python-flint 0.9.0. Frozen certificate outputs are
[evidence/directed_fourth_pricing_verification_n21.json](evidence/directed_fourth_pricing_verification_n21.json)
and [evidence/directed_fourth_pool_certificate_n21.json](evidence/directed_fourth_pool_certificate_n21.json).

The next highest-value action is to price the saved 55-term direction,
add independently verified new gapped columns, and repeat the complete
fourth-order solve. A useful stopping distinction remains: a positive
finite design needs exact weights and higher-moment closure; a claimed
physical no-go needs a global bound on all allowed couplings, not just
optimizer failure or a finite-pool separator.

The repository state, recent Issue comments, relevant theory/code/evidence
and [manuscript/Appendix B](https://arxiv.org/html/2506.20570v1) were
inspected. No manuscript TeX/PDF sources are present. This research update
keeps the fixed static-oracle promise distinct from the manuscript's
broader robustness study, and does not claim journal readiness.
