# A finite fractional-segment grid obstruction for the n=21 low-moment ensemble

Date: 2026-11-24. Related: [the certified 22-atom low-moment design](THEORY_LOW_MOMENT_DESIGN_N21.md), [the exact two-mirror obstruction](THEORY_TWO_MIRROR_OBSTRUCTION.md), and Issue #5.

## Question

The existing 22-atom gapped ensemble matches all 21 distance-averaged second-order moments and the consecutive fourth-order orbit \(\{0,1,2,3\}\), but its distant fourth-order probe \(\{0,2,21,23\}\) exceeds the target \(1/533\) by more than \(1/100\).

Can one add a single fractional-transfer path seed, reweighting the original 22 atoms, while preserving the 21 second-order constraints, the consecutive fourth-order constraint, and normalization, and use the one new degree of freedom to repair that distant fourth-order probe?

## Exact affine reduction

Let \(M\in\mathbb R^{22\times22}\) be the feature matrix whose columns are the 22 frozen physical atoms and whose rows are
\[
m_1,\ldots,m_{20},\quad q_{0123},\quad 1.
\]
The existing certificate proves \(M\) nonsingular and the base solution \(p=M^{-1}b\) strictly positive. Here \(b\) contains the exact targets \(t_d=(-1)^{d+1}/41\), \(q_{0123}=1/533\), and normalization one. The omitted \(m_{21}\) equation follows from the symmetric-involution identity in the base theorem.

For a new physical seed with feature column \(v\), define
\[
u=M^{-1}v.
\]
Every reweighting that preserves the 22 old constraints and gives the new atom weight \(\tau\) must have
\[
p_{\rm old}(\tau)=p-\tau u.
\]
Let \(d\in\mathbb R^{22}\) be the distant-probe values of the old atoms, \(d_{\rm new}\) the new atom's value, and \(d_*=1/533\) the target. Then the distant residual is exactly affine:
\[
\Delta(\tau)=d^{\mathsf T}p-d_*+
\tau\bigl(d_{\rm new}-d^{\mathsf T}u\bigr)
=\Delta_0+\tau\sigma.
\]
The base residual is
\[
\Delta_0=
[0.0129392316409538071962346592130359334639942998783638688669442274633158182283219506115420611837007481148
\pm 6.25\times10^{-104}]>0.
\]
If \(\sigma>0\), the unique weight that would repair the probe is \(\tau_*=-\Delta_0/\sigma<0\), so the new atom cannot be added with positive probability. If \(\sigma=0\), that atom cannot change the distant probe while preserving the old constraints. Only \(\sigma<0\) can potentially help, and it must additionally leave every component of \(p-\tau_*u\) positive.

## Finite 27-seed Arb result

The reproducible screen tested every not-already-present seed in the predeclared grid
\[
L\in\{10,21,30,41,42\},\qquad
\alpha\in\left\{\tfrac18,\tfrac14,\tfrac12,\tfrac34,\tfrac54,\tfrac32\right\},
\]
with
\[
c_j=\alpha\frac{\pi}{4}\sqrt{(j+1)(L-j-1)}
\quad (j=0,\ldots,L-2),
\]
and all remaining/wrap couplings zero. The three fractional seeds already in the base ensemble were skipped, leaving 27 candidates. Each candidate's matrix exponential, feature column, affine slope, and required weight was evaluated with 384-bit Arb.

- 25 candidates have a strictly positive slope interval and hence a strictly negative required new weight.
- Two candidates, \((L,\alpha)=(41,3/2)\) and \((42,5/4)\), have slope intervals containing zero at 384 and 768 bits. Exact spin-periodicity and transpose identities prove that they are redundant: their every-even-principal-minor columns equal the already-present \((41,1/2)\) and \((42,3/4)\) seeds, respectively.
- Thus all 27 candidates are accounted for: 25 require negative new weight, and two are exact duplicate feature columns. No positive single-atom extension exists on this finite grid.

For the especially relevant length-41, \(\alpha=5/4\) seed—which numerically escapes the perfect-two-mirror separator—the certified slope is approximately
\[
\sigma=0.09745473024696600573516666781615925315243834707351366\ldots>0,
\]
so the required new weight is approximately
\[
\tau_*=-0.13277171470449620188836537349650093968565370825617\ldots<0.
\]
Thus this particular fractional seed cannot repair the distant fourth probe by itself while preserving the base 22 constraints.

## Exact resolution of the two zero slopes

The two interval slopes that still contain zero at 768 bits are exact duplicate even-minor columns, by the spin representation of the fractional open path. Let \(G_L\) be the real skew-symmetric tridiagonal matrix with \((G_L)_{r,r+1}=\sqrt{(r+1)(L-r-1)}\) and \((G_L)_{r+1,r}=-\sqrt{(r+1)(L-r-1)}\), for \(r=0,\ldots,L-2\). Put \(J_y^{(j)}=G_L/2\), where \(j=(L-1)/2\); this is the real skew form of the spin-\(j\) generator and has eigenvalues \(im\), \(m=-j,\ldots,j\). Since the physical path generator has entries \(2c_r=\alpha\pi\sqrt{(r+1)(L-r-1)}/2\), the length-\(L\) block is
\[
R_{L,\alpha}=\exp(\alpha\pi J_y^{(j)}).
]
Transposition sends \(\alpha\) to \(-\alpha\).

For \(L=41\), \(j=20\) is integer, so \(\exp(2\pi J_y^{(20)})=I\). Therefore
\[
R_{41,3/2}=R_{41,-1/2}=R_{41,1/2}^{\mathsf T}.
\]
Every principal minor is invariant under transposition. Hence the \((41,3/2)\) candidate has exactly the same all-even-minor feature column as the \((41,1/2)\) atom already in the base ensemble.

For \(L=42\), \(j=41/2\) is half-integer, so \(\exp(2\pi J_y^{(41/2)})=-I\). Therefore
\[
R_{42,5/4}=-R_{42,-3/4}=-R_{42,3/4}^{\mathsf T}.
\]
For every even-size index set \(I\), \(\det((-R)_{I,I})=\det(R_{I,I})\); transposition also preserves the principal minor. Thus the \((42,5/4)\) candidate has exactly the same all-even-minor feature column as the \((42,3/4)\) base atom.

The 768-bit Arb intervals are consistent with these exact identities. The identities resolve the two zero-slope cases analytically, so the entire predeclared 27-seed grid is now accounted for: 25 strictly negative required weights and two exact redundancies.

## Multi-atom corollary for the same finite grid

The sign information is stronger than a one-atom test. Let \(V\) contain any subset of the 27 new feature columns, and let \(\tau\ge0\) be arbitrary added weights. Preserving the 22 base equations forces the old weights to be
\[
x=p-M^{-1}V\tau.
\]
The distant-probe residual is therefore
\[
\Delta(\tau)=\Delta_0+
\bigl(d_{\rm new}^{\mathsf T}-d^{\mathsf T}M^{-1}V\bigr)\tau
=\Delta_0+\sum_j\sigma_j\tau_j.
\]
For all 25 nonduplicate candidates, Arb proves \(\sigma_j>0\); for the two duplicate candidates, the spin identities prove \(\sigma_j=0\). Hence every \(\tau_j\ge0\) obeys
\[
\Delta(\tau)\ge\Delta_0>0.
\]
No nonnegative mixture of any subset of these 27 fractional seeds can repair the distant fourth probe while preserving the 21 second-moment equations, the consecutive fourth probe, and normalization. This is an exact finite-family convex-cone obstruction, not merely a failure of a particular LP or optimizer.

The result still leaves open fractional parameters outside the grid, mixtures involving other gapped couplings, and designs that change the base support or enforce the complete fourth-order orbit system directly.

## Evidence and reproduction

- Exact input: [evidence/ising_low_moment_design_n21.json](evidence/ising_low_moment_design_n21.json)
- 384-bit result: [evidence/ising_low_moment_fractional_extension_n21.json](evidence/ising_low_moment_fractional_extension_n21.json)
- Verifier: [verify_ising_low_moment_fractional_extension.py](verify_ising_low_moment_fractional_extension.py)
- Workflow: [eui-23atom-low-moment-fractional-extension.yml](.github/workflows/eui-23atom-low-moment-fractional-extension.yml)
- Successful workflow: [45299958866](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45299958866)

The verifier reconstructs the base \(22\times22\) system and every candidate rotation from the frozen exact seed definitions, computes \(M^{-1}v\), and interval-certifies the sign of \(\sigma\) and \(\tau_*\). The two zero-containing intervals are resolved by the exact spin-periodicity identities above. The workflow pins Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and python-flint 0.9.0.

## Scope and next step

This is a finite-grid, single-new-atom result. It is not a no-go theorem for two or more new atoms, continuous fractional-transfer parameters, arbitrary gapped couplings, or the full all-even-moment ensemble. It does not activate the conditional n=21 joint-parity diamond theorem.

The next decisive step is to move beyond this finite fractional grid and use multi-atom column generation over general gapped couplings, enforcing the complete fourth-order orbit family rather than one distant probe at a time. Any resulting ensemble must still pass all higher even moments before the long-ring diamond theorem becomes unconditional.
