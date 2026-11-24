# 384-bit screen of single fractional-segment extensions of the n=21 low-moment ensemble

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
[0.0129392316409538071962346592130359334639942998783638688669442
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
- Two candidates, \((L,\alpha)=(41,3/2)\) and \((42,5/4)\), have slope intervals containing zero at 384 bits. They remain unresolved; they are not counted as exclusions.
- No positive 23-atom extension was certified on this finite grid.

For the especially relevant length-41, \(\alpha=5/4\) seed—which numerically escapes the perfect-two-mirror separator—the certified slope is approximately
\[
\sigma=0.09745473024696600573516666781615925315243834707351366\ldots>0,
\]
so the required new weight is approximately
\[
\tau_*=-0.13277171470449620188836537349650093968565370825617\ldots<0.
\]
Thus this particular fractional seed cannot repair the distant fourth probe by itself while preserving the base 22 constraints.

## Evidence and reproduction

- Exact input: [evidence/ising_low_moment_design_n21.json](evidence/ising_low_moment_design_n21.json)
- 384-bit result: [evidence/ising_low_moment_fractional_extension_n21.json](evidence/ising_low_moment_fractional_extension_n21.json)
- Verifier: [verify_ising_low_moment_fractional_extension.py](verify_ising_low_moment_fractional_extension.py)
- Workflow: [eui-23atom-low-moment-fractional-extension.yml](.github/workflows/eui-23atom-low-moment-fractional-extension.yml)
- Successful workflow: [45299958866](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45299958866)

The verifier reconstructs the base \(22\times22\) system and every candidate rotation from the frozen exact seed definitions, computes \(M^{-1}v\), and interval-certifies the sign of \(\sigma\) and \(\tau_*\). The two zero-containing intervals are explicitly retained as unresolved. The workflow pins Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and python-flint 0.9.0.

## Scope and next step

This is a finite-grid, single-new-atom result. It is not a no-go theorem for two or more new atoms, continuous fractional-transfer parameters, arbitrary gapped couplings, or the full all-even-moment ensemble. It does not activate the conditional n=21 joint-parity diamond theorem.

The next decisive step is to resolve the two zero-slope cases analytically or at higher precision, then move from one-atom repair to a multi-atom column-generation problem that enforces the complete fourth-order orbit family rather than one distant probe at a time. Any resulting ensemble must still pass all higher even moments before the long-ring diamond theorem becomes unconditional.
