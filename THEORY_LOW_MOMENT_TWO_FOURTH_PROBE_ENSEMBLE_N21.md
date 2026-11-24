# A positive 41-atom n=21 ensemble matching two fourth-order probes

Date: 2026-11-24. Related: [the 22-atom low-moment design](THEORY_LOW_MOMENT_DESIGN_N21.md), [the 27-seed fractional-grid obstruction](THEORY_LOW_MOMENT_FRACTIONAL_SINGLE_ATOM_SCREEN_N21.md), and Issue #5.

## Result

A deterministic search over 8,241 fractional open-path seeds found a positive physical ensemble that preserves all 21 distance-averaged second moments and matches two distinct fourth-order dihedral probes exactly. The final ensemble has 41 atoms: the original 22 physical atoms plus 19 fractional open paths.

This is a constructive low-moment result. It is **not** a complete fourth-order, all-even-minor, or joint-parity uniform-program design.

## Base affine system

Let the 22 original physical atoms have feature matrix
\[
M\in\mathbb R^{22\times22},
\]
whose rows are
\[
m_1,\ldots,m_{20},\quad q_{\{0,1,2,3\}},\quad 1.
\]
The exact target vector is
\[
b=\left(\frac1{41},-\frac1{41},\ldots,\frac{(-1)^{21+1}}{41},
\frac1{533},1\right)^{\mathsf T},
\]
with the first 20 distance rows included. The base weights are \(p=M^{-1}b\). The existing 192-bit Arb certificate proves \(\det M\ne0\) and \(p_i>0\) for all 22 atoms.

For a new fractional seed \(j\), let \(v_j\) be its 22-entry feature column and define
\[
u_j=M^{-1}v_j.
\]
Let \(d\) be the vector of distant-probe values on the base atoms and \(d_j\) the value on new atom \(j\), for
\[
I_{\rm far}=\{0,2,21,23\},\qquad t_{\rm far}=\frac1{533}.
\]
Then
\[
\Delta_0=d^{\mathsf T}p-t_{\rm far}>0,\qquad
\sigma_j=d_j-d^{\mathsf T}u_j.
\]
For any nonnegative new-weight vector \(\tau\), preserving the 22 base equations forces old weights \(p-U\tau\), where \(U=(u_j)_j\), and the distant residual is
\[
\Delta(\tau)=\Delta_0+\sigma^{\mathsf T}\tau.
\]

## Deterministic 8,241-column discovery

The discovery pool contains every
\[
L=2,\ldots,42,\qquad
\alpha=\frac{k}{100},\quad k=0,\ldots,200,
\]
for 8,241 fractional open paths. Their nonzero couplings are
\[
c_r=\frac{\alpha\pi}{4}\sqrt{(r+1)(L-r-1)},
\qquad r=0,\ldots,L-2,
\]
and all remaining and wrap couplings vanish.

The floating LP minimizes \(\sigma^{\mathsf T}\tau\) subject to \(U\tau\le p\) and \(\tau\ge0\). It is a support-discovery computation only. It returns 19 new fractional seeds with positive decimal weights. The maximum residual reduction is approximately
\[
0.01490009901984,
\]
larger than the base residual
\[
\Delta_0\approx0.01293923164095.
\]

The exact verifier freezes the 19 seed labels and rationalizes the printed decimal LP weights. It does not use the floating LP as a proof.

## Exact positive rescaling

Let \(\tau\) denote the frozen nonnegative rational vector and define the exact Arb quantity
\[
R=-\sigma^{\mathsf T}\tau.
\]
The independent 384-bit verifier proves \(R>\Delta_0>0\). Set
\[
\gamma=\frac{\Delta_0}{R}\in(0,1).
\]
The final ensemble weights are
\[
w_{\rm old}=p-\gamma U\tau,\qquad
w_{\rm new}=\gamma\tau.
\]
The verifier independently proves every component of both vectors is strictly positive.

The 22 base equations are preserved exactly:
\[
M w_{\rm old}+V w_{\rm new}
=M(p-\gamma U\tau)+\gamma V\tau
=Mp=b,
\]
because \(MU=V\).

The distant probe is repaired exactly:
\[
d^{\mathsf T}w_{\rm old}+d_{\rm new}^{\mathsf T}w_{\rm new}
-t_{\rm far}
=\Delta_0+\gamma\sigma^{\mathsf T}\tau
=\Delta_0-\gamma R=0.
\]
Normalization follows from the last row of the base system and the unit normalization of each new feature column.

## 384-bit Arb certificate

The independent verifier certifies:

- 41 physical atoms (22 base + 19 new fractional paths);
- base input SHA256 d8c5a0ed699f7757d171c4e05913704fc280f9e35d0bba04ad5af768df2a7807;
- discovery JSON SHA256 8c92bcf3896e960a04c7ab8d4b1d4cb9b2c568cc0c91e73385e0ea1f5f831641;
- base matrix determinant
  \[
  [3.08816980830789729675621921156072179548197237845\ldots\times10^{-24}
  \ \pm 7.62\times10^{-130}];
  \]
- base distant residual
  \[
  [0.01293923164095380719623465921303593346399429987836\ldots
  \ \pm6.25\times10^{-104}];
  \]
- candidate repair before rescaling
  \[
  [0.01490009901985021209904941069324555847589819015710\ldots
  \ \pm2.42\times10^{-103}];
  \]
- interpolation factor
  \[
  \gamma=
  [0.86839903706115658184287441518140630184539297518602\ldots
  \ \pm7.22\times10^{-102}];
  \]
- minimum final weight
  \[
  [0.000110852097544644610007668601156342369587115893874\ldots
  \ \pm3.88\times10^{-104}]>0;
  \]
- maximum final weight
  \[
  [0.306570713258133589263585088232991389845162512240\ldots
  \ \pm4.00\times10^{-102}];
  \]
- total weight
  \[
  [1\pm1.46\times10^{-101}].
  \]

All 21 distance-moment residual intervals contain zero. Both fourth-order probes
\[
q_{\{0,1,2,3\}}=\frac1{533},\qquad
q_{\{0,2,21,23\}}=\frac1{533}
\]
are independently checked with Arb; their residual intervals contain zero.

Two other fourth-order probes remain strict failures:
\[
q_{\{0,1,2,4\}}+\frac1{533}
\in[-0.004912977759388897\pm8.18\times10^{-19}],
\]
and
\[
q_{\{0,10,20,30\}}-\frac1{533}
\in[0.00576\pm7.86\times10^{-6}].
\]
Thus the new ensemble is not fourth-order uniform.

## A separate coarse-grid Farkas certificate

A second independent 384-bit Arb certificate covers the 861-seed coarse grid
\[
L=2,\ldots,42,\qquad \alpha=k/10,\quad k=0,\ldots,20.
\]
It freezes a nonnegative rational vector \(\lambda\) and certifies
\[
\lambda^{\mathsf T}p
=0.01199999912229604678\ldots
<\Delta_0,
\]
and, for every one of the 861 seeds,
\[
\sigma_j+\lambda^{\mathsf T}u_j
\ge0.00147717709277052838\ldots>0.
\]
For any nonnegative mixture on any subset of this *coarse* grid with \(U\tau\le p\),
\[
\begin{aligned}
\Delta(\tau)
&=\Delta_0-\lambda^{\mathsf T}U\tau
+\sum_j(\sigma_j+\lambda^{\mathsf T}u_j)\tau_j\\
&\ge\Delta_0-\lambda^{\mathsf T}p>0.
\end{aligned}
\]
This is a rigorous finite-grid convex-cone obstruction. It does not cover continuous \(\alpha\), and it is consistent with the positive construction above, which uses a finer 0.01 grid and includes directions absent from the coarse grid.

The juxtaposition is scientifically important: the 861-seed coarse-grid obstruction is bypassed by the 8,241-seed 0.01 grid. The separate 27-seed result also remains finite-grid only; neither certificate is a global no-go for fractional physical paths.

## Reproduction

Pinned environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0.

~~~bash
OPENBLAS_NUM_THREADS=1 python discover_ising_low_moment_two_fourth_ensemble_n21.py
OPENBLAS_NUM_THREADS=1 python verify_ising_low_moment_two_fourth_ensemble_n21.py
OPENBLAS_NUM_THREADS=1 python verify_ising_fractional_grid_cone_n21.py
~~~

Evidence and workflow:

- [floating discovery](evidence/ising_low_moment_two_fourth_discovery_n21.json)
- [384-bit positive-ensemble certificate](evidence/ising_low_moment_two_fourth_ensemble_n21.json)
- [861-seed Farkas certificate](evidence/ising_fractional_grid_cone_n21.json)
- [discovery script](discover_ising_low_moment_two_fourth_ensemble_n21.py)
- [independent Arb verifier](verify_ising_low_moment_two_fourth_ensemble_n21.py)
- [coarse-grid Farkas verifier](verify_ising_fractional_grid_cone_n21.py)
- [workflow](.github/workflows/eui-two-fourth-ensemble-n21.yml)
- successful exact run: [45315065442](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45315065442)
- evidence commit: [69dfb15](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/69dfb15)

## Scope and next action

This result is a positive physical ensemble for 21 second moments and two specified fourth-order dihedral probes only. It does not satisfy the full set of 1,440 fourth-order orbits, all sixth/eighth-order minors, or the all-even-principal-minor target. It therefore does not activate the conditional n=21 joint-parity diamond theorem.

The next decisive task is column generation with the complete 1,440 fourth-order orbit constraints. The current 41-atom ensemble is a warm start, not a final program-uniform design. Any subsequent claim must retain exact positive weights and independently certify the full orbit system before moving to higher even orders.
