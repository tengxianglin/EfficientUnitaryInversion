# Complete fourth-order tests: exact dependencies and a certified seed-pool rejection

Date: 2026-11-21. Base: `13a15652b9c752207869aeedbf95b6e0a85151e2`.
Related: Issue #3, [minor criterion](THEORY_PROGRAM_MINOR_OBSTRUCTION.md),
[low-moment certificate](THEORY_LOW_MOMENT_DESIGN_N21.md), and
[program sampling](THEORY_PROGRAM_DPP.md).

## Results and evidence classes

**Proved analytically:** for each odd n>=3, every physical Majorana
rotation supplies exact linear relations linking fourth-order and
second-order principal minors. After dihedral averaging, these relations
can remove known redundant moment equations without weakening the design
test.

**Exact finite rank certificate at n=21:** the 147-by-1440 fourth-order
incidence matrix has rank 147. An explicitly generated 147-by-147 minor
has integer determinant 824633720832 = 3*2^38. Removing its 147 pivot
fourth-order coordinates, and the one redundant second-order equation,
gives a system of 1314 equations including normalization, equivalent to
the original 1462 equations for mixtures of legal physical seeds. No
claim is made that every remaining row is independent or that degree
four suffices for full program uniformity.

**Certified finite-family rejection:** none of the six gapped seeds
screened by Monte Carlo in the previous run, nor any positive mixture of
their dihedral images or vertex-sign gauges, can have uniform program
masses. All have a distance-two moment strictly above -17/1000, while
the target is -1/41. This is a 192-bit interval certificate, independent
of sampling. It excludes these six specified seeds, not a continuous
uniform-chain family or general physical couplings.

**Finite numerical study:** 1600 gapped seeds near long uniform paths
were evaluated against all 21 distance moments and all 1440 fourth-order
orbits. A scaled, reduced HiGHS-IPM feasibility test reports infeasible.
This is a solver diagnostic for one finite pool, without an exact dual
certificate. It is not a general physical no-go theorem.

## 1. All-odd-length fourth/second hierarchy

Use N=2n, R=exp(A), Z=diag(1,-1,...), and Q=ZR. The physical nearest-neighbor
generator is bipartite, ZAZ=-A, so Q is a symmetric involution with n
positive and n negative eigenvalues. For any fixed index set K, |K|=r,
let

\[
 G_K(t)=\sum_{I\supseteq K}t^{|I|}\det Q_I.
\]

The principal-minor expansion of det(I+t diag(x)Q), differentiated once
in each x_k for k in K and evaluated at x=1, gives

\[
 G_K(t)=\det(I+tQ)
        \det\bigl[tQ(I+tQ)^{-1}\bigr]_K
 =t^r(1-t^2)^{n-r}\det(Q_K-tI_r).                    \tag{1}
\]

This is a polynomial/formal-series identity around t=0; values at t=+/-1
are not used. For the needed case r=3, n>=3 and no negative exponent
occurs. The coefficient of t^4 is

\[
 \boxed{\sum_{\substack{I\supseteq K\\|I|=4}}\det Q_I
       =-\sum_{\substack{J\subseteq K\\|J|=2}}\det Q_J,\quad |K|=3.} \tag{2}
\]

The odd three-set K is an auxiliary matrix index set, not an odd logical
Pauli observable. Only even-order physical program moments occur in (2).
The determinant differentiation is standard linear algebra; its explicit
application here is a correctness and reduction tool, not a claim of
first discovery of principal-minor identities or DPP methods.

Write v(I)=number of odd-index vertices. Since det Q_I=(-1)^v(I) det R_I,
(2) is a relation entirely among the second/fourth program probes.
For a dihedrally averaged seed define m_d as the distance-d two-by-two
minor average and q_o as the four-by-four minor average on orbit o.
For one representative K of each triple orbit define integer matrices

\[
 C_{K,o}=\sum_{\substack{I\supset K,\ |I|=4\\I\in o}}(-1)^{v(I)},
 \qquad
 D_{K,d}=\sum_{\substack{\{i,j\}\subset K\\\operatorname{dist}(i,j)=d}}
               (-1)^d.
\]

Then every physical seed and every normalized mixture obeys

\[
 Cq+Dm=0.                                             \tag{3}
\]

No assumption of a uniform ensemble is used. The target values
m_d=(-1)^(d+1)/(2n-1) and
q_o=(-1)^v(I) binom(n,2)/binom(2n,4) satisfy (3) exactly. At n=21,
q_o is +/-1/533. For each K the signed fourth-order target sum is
39/533=3/41, canceling the three target Q-pair minors.

## 2. Exact reduction and checks of equivalence

On the 42-cycle, all 111930 four-sets partition into 1440 dihedral orbits;
the three-sets partition into 147 orbits. The module constructs C,D by
explicit integer incidence counting. Modular elimination selects 147
pivot columns. The independent FLINT integer determinant of that pivot
minor is 824633720832, confirming full row rank over the rationals.
The evidence freezes the complete pivot list and the modular check.

There is also the existing exact second-order identity

\[
 \sum_{d=1}^{20}(-1)^{d+1}m_d+\tfrac12m_{21}=\tfrac12. \tag{4}
\]

It follows from e_2(Q)=-21. The half coefficient accounts for antipodal
unordered pairs, which occur twice in the distance average.

In a normalized physical mixture, matching m_1,...,m_20 forces m_21 by
(4). Once m is fixed, matching the 1293 nonpivot fourth-order coordinates
forces all 147 omitted ones by (3) and invertibility of the pivot minor.
Thus 20+1293+1=1314 retained equations are **equivalent** to all 21+1440
moment equations plus normalization for this physical mixture problem.
This is an exact implication; numerical residual tests alone would not
justify deleting rows.

Independent finite construction checks at n=3,5,7 give fourth/triple
orbit counts (3,3), (16,8), (47,16) and reduced equation counts 3,13,38.
Their modular row ranks are full and their exact rational targets pass
all incidence equations. The n=5 count 13 is consistent with the earlier
13-orbit full certificate; this consistency is not substituted for the
present proof. At n=21 all 1600 numerical columns obey (3) to maximum
floating defect 4.54e-12; (4) is checked independently as well.

## 3. A decisive check of the previous six Monte Carlo seeds

The six inputs are frozen as exact decimal coupling strings in
[evidence/program_dpp_screen_n21.json](evidence/program_dpp_screen_n21.json):
five open paths with every internal c equal to 1,3,10,30,100, respectively,
and one specified disordered open path. Every closing edge is exactly
zero. The sampler's matching-label statistics are not used in this proof.

For each exact input, the verifier encloses the 42-by-42 real matrix
exponential at 192 bits and computes

\[
 m_2=\frac1{42}\sum_i(R_{ii}R_{i+2,i+2}-R_{i,i+2}R_{i+2,i}).
\]

All six enclosures are strictly above -17/1000. In particular, the
all-100 seed (whose empirical matching mass was near the uniform target)
has

\[
 m_2=[-0.016935150088194559386100291030660604381970189182589827534
       \ \pm\ 6.66\times10^{-58}],
\]
\[
 m_2-(-1/41)=
 [0.007455093814244465004143611408363785861932249841800416368
       \ \pm\ 7.38\times10^{-58}].
\]

The uniform target requires -1/41=-0.0243902439..., so convexity gives
the exact common separation

\[
 \mathbb E m_2-(-1/41)>1/41-17/1000=303/41000>0.       \tag{5}
\]

Both the distance average and principal minors are invariant under the
specified dihedral averaging and vertex-sign gauges. Therefore arbitrary
positive weights on these six seed orbits cannot repair the defect.
This closes a concrete possible overinterpretation of the previous
sampling screen. Matching-subspace mass is one necessary scalar test;
it does not determine even the full second-order vector.

The complete floating fourth-order audit also checks every quartet orbit
for each of the six seeds. For the all-100 path the maximum absolute
second/fourth residuals are about 0.0476031 and 0.0102265, respectively.
Those all-orbit magnitudes/rankings are numerical diagnostics; (5) is
the separate rigorous rejection certificate.

## 4. Full fourth-order finite-pool experiment

Experiment recipe: seed 202611210435; 320 samples each at relative disorder
0,.02,.1,.3,.7; each internal coupling vector is
c_j=tau*(1+sigma*g_j), g_j independent standard normal, with tau
log-uniform on [3,500]; c_41=0. This creates 1600 actual gapped static
oracles, each subsequently averaged over legal dihedral images.
The exact generation code, environment and floating coupling/feature
SHA256 fingerprints define the reproducible numerical experiment.
These generated doubles are not an interval certificate for the pool.

The test evaluates all 1461 features, retains the 1314-equation system
proved equivalent above, and multiplies second/fourth rows by 41 and 533, respectively. SciPy/HiGHS-IPM reports status 2 (infeasible). No positive mixture
was certified. There is no verified exact separating dual for the entire
1600-column pool, so the conclusion remains a finite numerical failure.
It does not exclude a different finite pool, other couplings, or a
full uniform physical ensemble.

An exploratory raw unscaled formulation with redundant rows returned an
Unknown solver status; that result was not interpreted as infeasibility.
The reported experiment uses the analytically reduced/scaled system and
records the explicit final status. Numerical solver failures and physical
no-go theorems are kept separate.

## 5. Reproduction and next action

```
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_fourth_moments.py
OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_fourth_moments.py --search
```

The default checks the integer incidence/rank certificate, rational
target equations, finite matrix identities, all six seed orbits and the
interval separation. `--search` regenerates the full 1600-column study.
Optional `--cache /path/pool.npz` writes/reuses intermediate feature
arrays; cached couplings must match the deterministic recipe and selected
columns are rebuilt as a consistency check. The cache is an acceleration
for the numerical experiment, not an exact proof object.

Dependencies used: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and
python-flint 0.9.0. Frozen outputs are
[evidence/fourth_moment_hierarchy_verification.json](evidence/fourth_moment_hierarchy_verification.json)
and [evidence/fourth_moment_pool_n21.json](evidence/fourth_moment_pool_n21.json).
The default verifier needs only the previously frozen six coupling
vectors, not any Monte Carlo samples.

The next highest-value action is directed column generation against this
complete reduced fourth-order system, rather than enlarging a generic
near-uniform-path pool or treating matching-mass sampling as a certificate.
A finite-pool dual can guide the search but becomes a physical no-go
only with a global bound over allowed couplings. A positive fourth-order
solution still needs higher even moments before the conditional joint
minimax theorem can be extended. Both blockers remain open.

The manuscript/Appendix B at
[arXiv:2506.20570v1](https://arxiv.org/html/2506.20570v1) were inspected;
there are no manuscript TeX/PDF sources in this repository. Its broader
robustness promise is not silently replaced by this fixed static-oracle
moment problem. Standard determinant identities and generic numerical
methods are not asserted as literature-wide EUI novelties.
