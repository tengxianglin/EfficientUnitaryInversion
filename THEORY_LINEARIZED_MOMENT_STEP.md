# All-row bounded linearization and an analytic remainder bound

Certified follow-up: [complete n=21 low-moment ensemble and strict improvement](THEORY_CERTIFIED_LOW_MOMENT_ENSEMBLE.md).

2026-11-21; base `5a0dc205791de699a6f6374656ded6c3fc51a67a`; Issue #3.
This follows the [scalar-versus-minimax descent audit](THEORY_LOCAL_MOMENT_STEP.md).
The unresolved question remains physical joint uniformity at n=21.

## Result and evidence levels

**Finite numerical result.** A local LP now constrains all 1461 moment
rows simultaneously. For four selected support points, all three tested
radii give actual fixed-weight descent after recomputing the nonlinear
moments. Appending all twelve candidates and correcting every weight
lowers the all-row scaled objective from approximately 0.2262303074 to
0.2174042699 (3.90%). The final saved weights evaluate to
0.21740426994709916, with 0.25848165458888894 probability on the four
radius-.1 candidates. The pool has 1639 columns. These are floating
approximate designs, not interval-certified improvements or exact uniformity.

**Proved analytic result.** For the physical path generator, a k-by-k
principal determinant has first-order remainder at most 8 k^2 h^2 when
all changed edge couplings have magnitude at most h. This gives a
uniform scaled second/fourth-moment remainder bound
68224 sum_j p_j h_j^2 for nonnegative mixture weights. The proof below
has no small-coupling or spectral-gap assumption. It is a standard
matrix-exponential norm argument specialized to this moment system;
no literature-wide mathematical novelty is claimed.

**Important limitation.** That general bound is very conservative here.
For all three tested radii it exceeds the predicted improvement. It
therefore does NOT certify these particular numerical descent steps.
Exact rational arithmetic in the verifier supplies the ideal-moment
bound only; it does not bound floating errors in expm or the Jacobian.
The core exact-design claim remains unresolved.

## 1. All-row local minimax model

Use the preceding physical convention: N=42, A_{j,j+1}=2c_j,
A_{j+1,j}=-2c_j, closing edge c_41=0, R=exp(A). The feature map phi
contains all 21 second moments and all 1440 fourth dihedral orbit
averages, with target m_d*=(-1)^(d+1)/41 and q_o*=(-1)^v/533.
Let S have row scalings 41 and 533 respectively. At the preceding
1627-column mixture, freeze weights p and form r=S(sum p_j phi(c_j)-t).
The four largest-weight parents are:

| Column | Weight | All-feature random-JVP finite-difference defect |
| --- | --- | --- |
| 1623 | 0.07641341192937545 | 1.82e-12 |
| 1626 | 0.06796390898343187 | 5.96e-12 |
| 1624 | 0.052804251508615715 | 7.21e-11 |
| 1625 | 0.05032207868267556 | 9.55e-12 |

Compute B=[p_j S Dphi(c_j)] for those parents, of shape 1461 by 164.
For each h=.001,.01,.1 solve

\[
 \min_{\delta,\epsilon}\epsilon,
 \qquad -\epsilon\mathbf1\le r+B\delta\le\epsilon\mathbf1,
 \qquad -h\le\delta_l\le h.
\]

Here only epsilon is constrained nonnegative; delta is free within its
box. All rows are included, so an inactive constraint cannot silently
cross the linearized maximum. No exact active-set identification or
choice of a single dual optimizer is required. Nonlinear curvature can
still invalidate a predicted decrease, which must be evaluated separately.

Each parent's changed internal couplings are rounded to nine decimal
places; the closing edge is kept exactly zero, and every internal edge
is checked nonzero. Thus each candidate remains a legal connected
zero-edge physical path, retaining the prior parity compatibility lemma.
The following are floating results at fixed old weights:

| Radius | LP prediction | Rounded-step prediction | Actual maximum residual |
| --- | --- | --- | --- |
| .001 | 0.22615459349981956 | 0.22615459355400222 | 0.2261552372449922 |
| .01 | 0.2254732945953219 | 0.22547329465526314 | 0.22553928615522226 |
| .1 | 0.21890825387040125 | 0.21890825393463376 | 0.22473246653062287 |

The old directly evaluated residual is 0.22623030742241432. Maximum
coordinate-wise defects between the rounded linear model and actual
nonlinear mixture are 6.7680e-7, 6.9342e-5, and 0.00671164. This is
consistent with a quadratic local error but does not establish an
asymptotic law from three tests. The large-radius prediction substantially
overstated the actual fixed-weight gain.

All old columns are retained, all twelve candidates are appended, and a
separate all-row epigraph LP corrects the full probability vector. Its
objective is 0.21740426994708814. Only the four radius-.1 candidates
receive positive weights among the new columns in the returned solution;
no uniqueness or necessity theorem is inferred. This is a nonlinear
support proposal plus convex weight correction, not a proof of global
convergence or a matched-budget advantage over another search method.

## 2. Derivative implementation without inverse-block assumptions

For every principal four-set I, precompute the determinant cofactors of
R[I,I]. For each of the 41 free edges, form its skew generator E and
compute Dexp(A)[E] with the Frechet derivative. Contract its principal
blocks with the precomputed cofactors, then average by dihedral orbit.
Second-moment derivatives follow the 2-by-2 product rule. This yields
all 1461 feature derivatives for each edge; no invertibility of the
principal blocks is assumed. The four assembled Jacobians are checked
against complete-feature central differences in independently seeded
random directions, as recorded in the table. This validates discovery
code numerically, not a global or interval derivative certificate.

## 3. Uniform second-order bound (analytic proof)

Let f_I(c)=det exp(A(c))[I,I], with |I|=k. On the exterior-power space,

\[
 f_I(c)=\langle e_I,\exp(A(c)^{[k]})e_I\rangle,
\]

where A^[k] is the additive exterior generator, the sum of A acting on
each tensor slot restricted to the antisymmetric subspace. For a skew
perturbation E=A(delta c), the induced perturbation satisfies
||E^[k]|| <= k ||E||. Every exponential factor of the real skew generator
A^[k]+t E^[k] is orthogonal for real t. The second derivative is twice
the time-ordered double integral of three such exponential factors
with two inserted E^[k] factors. Its integration simplex has area 1/2,
so its operator norm is at most ||E^[k]||^2. Taylor's integral remainder
therefore gives

\[
 |f_I(c+\delta c)-f_I(c)-Df_I(c)[\delta c]|
 \le\tfrac12 k^2\|E\|^2.
\]

Each row and column of the path perturbation E has absolute sum at
most 4h, where h=||delta c||_infinity. Thus ||E||_2 <=4h, giving

\[
 |\mathrm{remainder}|\le 8k^2 h^2.
\]

Orbit averaging preserves this bound. For second moments (k=2) after
scaling by 41 it is 1312 h^2; for fourth moments (k=4) after scaling by
533 it is 68224 h^2. Nonnegative weighted summation over changed seeds
proves the uniform all-row bound

\[
 \|r_{\mathrm{actual}}-(r+B\delta)\|_\infty
 \le 68224\sum_{j\,\mathrm{changed}}p_j h_j^2.       \tag{1}
\]

This holds for any nonnegative weights, even without normalization.
For exact features and derivatives it implies the sufficient condition
||r+B delta||_infinity + RHS(1) < ||r||_infinity for strict descent.
It also handles rounding by using the actual coupling changes in h_j.
It does not certify descent if this sufficient condition fails.

At the tested steps, the general bound is approximately .0168857,
1.68857 and 168.857, much larger than the measured defects and gains.
The verifier recomputes exact rational versions from the exact binary64
parent points/weights and exact decimal-rational candidates. This
arithmetic verifies the bound's input calculation, not the exactness of
numerically evaluated moments or derivatives. Tighter local curvature
bounds or interval moment evaluation are needed for a numerical descent
certificate. Equation (1) alone supplies neither.

## 4. Reproduction and next scientific decision

Inputs, all twelve candidate couplings/full-feature hashes, all-row
Jacobian hash, model predictions and final numerical weights are frozen
in [evidence/linearized_moment_step_n21.json](evidence/linearized_moment_step_n21.json).
The [verification transcript](evidence/linearized_moment_step_verification_n21.json)
reconstructs all candidate features, the full Jacobian, fixed-weight
models, and final weights, and records exact rational remainder bounds.
No exact optimum or general impossibility is inferred from these files.

Environment: Python 3.12.14 / NumPy 2.3.5 / SciPy 1.17.0 /
python-flint 0.9.0; OPENBLAS_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1.
Regenerate the fingerprint-checked original feature cache as documented
in the preceding notes, then:

```
python linearized_ising_moment_step.py --cache /tmp/eui-pool.npz --output /tmp/eui-linear.json
python verify_linearized_moment_step.py --cache /tmp/eui-pool.npz
python -m unittest discover -s tests -v
```

Verification reads the frozen evidence, not an arbitrary rediscovery
output. The optional --jac-cache writes a reproducible intermediate
matrix; it is not required for verification. Identical rediscovery
trajectories across solver/BLAS versions are not claimed.

**Remaining blocker:** exact second/fourth feasibility, and all higher
moments needed for full joint uniformity and the conditional long-ring
minimax extension. **Next highest-value action:** repeat the all-row
bounded step with an acceptance rule comparing nonlinear and predicted
gain, and seek a useful local curvature/interval bound for one accepted
step. Judge success against all moment rows; do not infer impossibility
from a positive finite-pool residual or numerical stagnation. No original
Nature Physics-level core theorem is established by this optimization step.

Latest main/recent Issues, relevant notes/code/evidence, and the
[manuscript and appendices](https://arxiv.org/html/2506.20570v1) were
inspected. No manuscript source files are present. This remains a
static-oracle moment-design study, distinct from the manuscript's broader
robustness and unrestricted query claims. The generic LP and exterior-power
arguments above are not asserted as literature-wide novelties.
