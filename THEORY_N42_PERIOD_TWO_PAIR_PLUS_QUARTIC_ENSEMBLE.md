# N=42 period-two positive ensemble: all pairs plus four quartic orbits

Date: 2026-11-26.

## Theorem (computer-assisted exact existence)

For the 42-cycle family with period-two couplings
\[
c_{2j}=a,\qquad c_{2j+1}=b,\qquad a,b>0,
\]
there exists a positive probability measure supported on **35 exact rational coupling pairs** such that:
1. every one of the 861 second-order principal-minor coordinates of \(Q=e^{A(c)}D\) equals \(-1/41\);
2. the fourth-order principal-minor target
\[
\tau_4=\frac{\binom{21}{2}}{\binom{42}{4}}
\]
is matched on each of the following four distinct translation-by-two orbits:
\[
\begin{aligned}
I_1&=\{0,1,2,3\},\\
I_2&=\{0,3,10,15\},\\
I_3&=\{0,2,4,6\},\\
I_4&=\{0,10,20,30\}.
\end{aligned}
\]
Each orbit has 21 translates, so 84 specified quartic subset moments are certified.

All 42 couplings in every atom are strictly positive. The 35 weights are defined as the unique exact-real solution of a frozen \(35\times35\) linear system; they are not asserted to be rational. The 256-bit Arb certificate proves invertibility, normalization, and a strict weight floor \(w_\ell>1/1000\).

This is a **partial moment design**, not a complete fourth-order design and not a full even-principal-minor solution.

## Fourier formulas and pair constraints

With \(n=21\), the parity-block generator is
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},\qquad B=2(aI-bT).
\]
For \(\phi_k=2\pi k/n\),
\[
\widehat B_k=2(a-be^{i\phi_k}),\qquad
\mu_k=2\sqrt{a^2+b^2-2ab\cos\phi_k}.
\]
The Fourier symbols of \(R=e^A\) are \(\widehat C_k=\cos\mu_k\) and
\(\widehat S_k=\widehat B_k\sin(\mu_k)/\mu_k\). Inverse Fourier transformation gives real circulant coefficients \(C_d,S_d\), and
\[
Q=RD=\begin{pmatrix}C&-S\\-S^T&-C\end{pmatrix}.
\]
Writing \(x=C_0\), the 31 pair classes are
\[
m_d=x^2-C_d^2\quad(d=1,\ldots,10),\qquad
n_d=-x^2-S_d^2\quad(d=0,\ldots,20).
\]
The exact row-norm identity
\[
2\sum_{d=1}^{10}m_d+\sum_{d=0}^{20}n_d=-1
\]
makes one cross displacement redundant. The verifier imposes ten \(m_d\) and twenty \(n_d\) coordinates.

## Exact 35-by-35 system

The 35 columns are frozen in
evidence/n42_period_two_pair_plus_quartic_atoms.json, each decimal coupling interpreted as an exact rational. The 35 rows are:
- 10 same-parity pair coordinates;
- 20 cross-parity pair coordinates;
- the four quartic determinants for \(I_1,\ldots,I_4\);
- normalization.

The right-hand side is 30 copies of \(-1/41\), four copies of \(\tau_4\), and one. The Arb verifier independently rebuilds every Fourier coefficient, constructs the matrix, proves its determinant interval excludes zero, and solves for the unique exact-real weight vector. It then checks all 861 pairs, all 84 even translates of the four quartic witnesses, and a separate quartic failure witness.

## Certified limitation of this ensemble

For \(J=\{0,2,21,23\}\), the same exact weights give a quartic residual
\[
\mathbb E\det Q_{J,J}-\tau_4>1/400.
\]
This does not show that another period-two mixture cannot match this orbit. It only proves that the frozen 35-atom support/weights are not a complete fourth-order design.

## Scientific consequence and next step

The N=42 period-two single-atom no-go is strictly a single-atom statement. Positive mixtures already match all pair moments and several nontrivial quartic orbits, using only strictly positive period-two couplings. Any continuous-family obstruction must therefore use additional quartic or higher-order information, not pair moments alone.

Next, enlarge the quartic orbit set and run a positive-mixture search over new period-two atoms. Every proposed finite support must be frozen and interval-certified as above. The final objective remains all even-principal-minor moments; this certificate does not imply full EUI feasibility or any Choi/diamond-distance bound.

## Reproducibility

- Frozen atoms: evidence/n42_period_two_pair_plus_quartic_atoms.json
- Independent verifier: verify_n42_period_two_pair_plus_quartic_ensemble_arb.py
- Arb certificate: evidence/n42_period_two_pair_plus_quartic_ensemble_arb.json
- Workflow: .github/workflows/eui-n42-period-two-pair-plus-quartic.yml
