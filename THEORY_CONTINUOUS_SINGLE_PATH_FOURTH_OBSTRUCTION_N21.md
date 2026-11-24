# Global continuous-alpha separator for the single-open-path family (n=21)

Date: 2026-11-24. Related: Issue #5; the exact 6,123-column finite-grid full-fourth separator.

## Objective

The finite-grid certificate proves strict separation only at 6,101 sampled fractional-path parameters, plus 22 pinned base atoms. One Taylor/Arb cell had separately been certified for \(L=40\), \(\alpha\in[1.835,1.845]\). The next question is whether the same frozen 80-term separator separates the target from **every** single-open-path seed with \(L=2,\ldots,42\) and continuous \(\alpha\in[0,2]\).

The new verifier reconstructs each path score as a finite cosine polynomial and proves its positivity globally by adaptive Bernstein subdivision. It is not a grid interpolation argument: the Fourier degree is derived exactly from the exterior-power spectrum, and the DFT sample count is chosen to prevent aliasing.

## Exterior-power frequency theorem

Let \(A_L=\pi J_y^{((L-1)/2)}\), so \(R_{L,\alpha}=e^{\alpha A_L}\). Its complex eigenvalues are
\[
i\pi m,\qquad m=-j,-j+1,\ldots,j,\qquad j=(L-1)/2.
\]
For an active subset \(J\subseteq\{0,\ldots,L-1\}\) of size \(r\), the principal minor is the diagonal matrix coefficient
\[
\det R_{L,\alpha}[J,J]
=\langle e_J,\exp(\alpha A_L^{[r]})e_J\rangle
\]
in the \(r\)-th exterior power. The eigenfrequencies are sums of \(r\) distinct spin weights. Their absolute values are bounded by
\[
\Omega_{L,r}=\sum_{s=0}^{r-1}(j-s)
=rj-\frac{r(r-1)}2.
\]

The frozen separator score is a rational linear combination of second- and fourth-order principal minors. Because the full matrix is \(R_{L,\alpha}\oplus I_{42-L}\), its active minor order can be any \(r=0,\ldots,\min(4,L)\) when \(L<42\). For \(L=42\), the active order is only \(r=2\) or \(4\).

Every principal minor is even in \(\alpha\), since \(R_{L,-\alpha}=R_{L,\alpha}^{\mathsf T}\) and principal determinants are invariant under transpose.

### Integer-spin lengths and the full \(L=42\) block

For odd \(L\), all spin weights are integers. Hence every frequency is an integer and the score is a cosine polynomial in \(\theta=\pi\alpha\), of degree
\[
D_L=\max_{0\le r\le\min(4,L)}\Omega_{L,r}.
\]
For \(L=42\), only \(r=2,4\) occur and their sums are integers; use
\[
D_{42}=\max_{r\in\{2,4\}}\Omega_{42,r}=76.
\]
These scores have period 2 in \(\alpha\).

### Half-integer-spin lengths with an idle complement

For even \(L<42\), active orders \(r\) can be odd because a second- or fourth-order full minor may also include idle identity sites. Odd \(r\) gives half-integer frequencies. The full score is therefore represented as a cosine polynomial in
\[
\theta=\frac{\pi\alpha}{2},
\]
whose integer degree is
\[
D_L=2\max_{0\le r\le\min(4,L)}\Omega_{L,r}.
\]
The score has period 4 in \(\alpha\). This distinction is essential: applying the full-block even-minor period-2 symmetry to an even \(L<42\) active block would be incorrect.

In both cases \(\alpha\in[0,2]\) maps onto \(x=\cos\theta\in[-1,1]\).

## Exact-size Fourier reconstruction

For a degree-\(D_L\) cosine polynomial, take \(N_L=2D_L+1\) equally spaced samples over its exact period:
\[
\alpha_q=
\begin{cases}
2q/N_L,&L\text{ odd or }L=42,\\
4q/N_L,&L<42\text{ even},
\end{cases}
\qquad q=0,\ldots,N_L-1.
\]
At these points \(\theta_q=2\pi q/N_L\). The exact DFT orthogonality relation recovers each cosine coefficient without aliasing:
\[
c_k=\frac1{N_L}\sum_{q=0}^{N_L-1}
S_L(\alpha_q)\cos(2\pi kq/N_L),
\qquad k=0,\ldots,D_L.
\]
The verifier encloses every sample and coefficient with Arb. It checks reflection symmetry at every sample, exact-size DFT reconstruction at every sample, and an independent off-grid point evaluation for each length.

Writing \(x=2u-1\), \(u\in[0,1]\), the gap polynomial is
\[
g_L(u)=y^{\mathsf T}b-S_L(\alpha(u)).
\]
It is converted to degree-\(D_L\) Bernstein form. Adaptive de Casteljau subdivision certifies positivity whenever all interval Bernstein coefficients on each leaf have strictly positive lower endpoints. Since the Bernstein basis is nonnegative and sums to one, the smallest such coefficient lower endpoint is a rigorous lower bound on the entire leaf. The finite collection of certified leaves covers \([0,1]\).

A negative Bernstein hull or negative midpoint evaluation instead yields a certified continuous-path escape. Depth/node exhaustion is reported as inconclusive, never as a proof.

## Reproduction

Pinned environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0.

~~~bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python certify_ising_full_fourth_continuous_single_path_n21.py
~~~

The script pins the finite-grid diagnostic, its 128-bit Arb certificate, and the 41-atom warm certificate by SHA256. It independently rechecks all 22 pinned base atoms at 512-bit Arb precision. For each \(L=2,\ldots,42\), it uses the exact exterior-power degree, \(2D_L+1\) Arb samples, and adaptive Bernstein subdivision.

## Scope

The 2026-11-24 run certifies all 41 lengths. The same separator therefore proves that no probability measure supported on the 22 pinned base atoms together with the entire continuous single-open-path family \(R_{L,\alpha}\), \(L=2,\ldots,42\), \(\alpha\in[0,2]\), can satisfy the complete second-/fourth-order target.

This is still not a global obstruction for arbitrary nonuniform gapped couplings, multi-segment paths, or the full physical family. It also does not construct the all-even-principal-minor positive ensemble and is not an operational Choi/diamond-distance theorem.


## Completed global certificate and quantitative consequence (2026-11-24)

The conditional statement above is now proved by the committed 512-bit Arb certificate \`evidence/ising_full_fourth_continuous_single_path_n21.json\` (blob SHA \`db7f259b055fe29bec300acc207af02135120762\`), produced by workflow [45350942797](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45350942797) and recorded in commit [5979d33](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5979d33a58fe8fb247a23253a8b4fb1dcd6ead10).

The verifier certifies every \(L=2,\ldots,42\) over the full continuous interval \(\alpha\in[0,2]\): 41 lengths, 4,389 exact-size Fourier samples, exact exterior-power frequency bounds, Arb-enclosed DFT coefficients, and adaptive de Casteljau/Bernstein subdivisions. Every path has status \`positive\`; there are no unresolved leaves and no negative witness. The 22 pinned base atoms are independently re-evaluated at 512-bit Arb precision. The smallest certified Bernstein lower endpoint over all path leaves and base atoms is

\[
\delta_{\rm cert}=0.02800447635786912086169875814833305913\ldots>0.028.
\]

For the frozen 80-term rational separator \(y\), the exact coefficient norm is

\[
\|y\|_1=\frac{1161904514761212958261}{2305843009213693952}<504.
\]

Consequently, for every atom feature vector \(a\) in the union of the 22 pinned base atoms and all \(R_{L,\alpha}\),

\[
y^{\mathsf T}(b-a)\ge\delta_{\rm cert}>0.028.
\]

By linearity, the same bound holds for every probability measure \(\mu\) supported on that union. Hölder's inequality then gives the explicit reduced-moment residual obstruction

\[
\left\|b-\mathbb E_{\mu}a\right\|_\infty
\ge \frac{0.028}{504}=\frac1{18000}.
\]

The infinity norm here is on the 1,313 independent second-/fourth-order moment coordinates; because these are selected coordinates of the full moment vector, the same lower bound also applies to the full second-/fourth-order residual infinity norm.

**Scope remains restricted.** This is a continuum theorem for the single-open-path family plus the 22 pinned base atoms. It does not cover arbitrary nonuniform gapped couplings, multi-segment paths, the all-even-principal-minor system, or the operational Choi/diamond bridge. In particular it is not a global no-go for the full physical family.
