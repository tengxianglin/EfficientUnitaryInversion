# Exact N=8 physical cycle ensemble for the complete balanced-slice even-minor target

Date: 2026-11-27. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), the [N=4/N=6 single-exponential constructions](THEORY_PHYSICAL_CYCLE_ENSEMBLE_N4_N6.md), and the [N=8 period-two mixture no-go](THEORY_N8_PERIOD_TWO_MIXTURE_FOURTH_ORDER_NO_GO.md).

## Theorem

Let \(N=8\), \(n=4\), and define the real skew-symmetric nearest-neighbour cycle generator by
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with indices modulo eight. Set
\[
R(c)=e^{A(c)},\qquad D=\operatorname{diag}(1,-1,1,-1,1,-1,1,-1),
\qquad Q(c)=R(c)D.
\]
The complete balanced-slice target is
\[
\tau_I=(-1)^r\frac{\binom4r}{\binom8{2r}},
\qquad |I|=2r,\quad r=0,1,2,3,4.
\]
Thus its nontrivial values at orders \(2,4,6,8\) are
\[
-\frac17,\qquad \frac3{35},\qquad -\frac17,\qquad 1.
\]

There is an exact positive probability measure supported on **37 distinct physical cycle exponentials** such that
\[
\boxed{\mathbb E_\mu\det Q(c)_{I,I}=\tau_I
\quad\text{for every even subset }I\subseteq[8].}
\]
The measure is obtained by taking four base physical atoms, symmetrizing each over the 16-element dihedral group \(D_8\), and assigning base weights
\[
\boxed{\lambda=\frac1{105}(1,16,80,8).}
\]
The 64 labelled group images merge into 37 distinct matrices. Their aggregated weights are strictly positive: 17 atoms have weight \(1/105\), 16 have weight \(1/21\), and 4 have weight \(2/105\).

This is an exact construction for the full \(N=8\) cycle-exponential convex hull, not just a finite numerical fit.

## 1. Four explicit physical atoms

For a contiguous block of \(L\) vertices beginning at \(s\), choose
\[
c_{s+r}=\frac{\pi}{4}\sqrt{(r+1)(L-r-1)},
\qquad r=0,\ldots,L-2,
\]
and set every cut edge and the closing edge to zero. The corresponding block generator has upper off-diagonal entries
\[
(A_L)_{r,r+1}=\frac{\pi}{2}\sqrt{(r+1)(L-r-1)}.
\]
This is the real spin-\((L-1)/2\) rotation generator. Its angle-\(\pi\) exponential is the signed reversal
\[
e^{A_L}|r\rangle=(-1)^r|L-1-r\rangle.
\]
This perfect-transfer / spin-rotation primitive is standard; see Christandl, Datta, Ekert and Landahl, *Phys. Rev. Lett.* **92**, 187902 (2004), [DOI: 10.1103/PhysRevLett.92.187902](https://doi.org/10.1103/PhysRevLett.92.187902). No novelty is claimed for the block exponential itself.

Use the following four compositions of eight. Each listed block is a signed reversal; singleton blocks are fixed points.

| Base atom | Block composition | Exact cycle couplings \(c_0,\ldots,c_7\) | Weight |
|---|---|---|---:|
| \(R_0\) | \((1,1,1,1,1,1,1,1)\) | \((0,0,0,0,0,0,0,0)\) | \(1/105\) |
| \(R_1\) | \((1,1,6)\) | \((0,0,\frac{\pi\sqrt5}{4},\frac{\pi\sqrt2}{2},\frac{3\pi}{4},\frac{\pi\sqrt2}{2},\frac{\pi\sqrt5}{4},0)\) | \(16/105\) |
| \(R_2\) | \((1,2,5)\) | \((0,\frac\pi4,0,\frac\pi2,\frac{\pi\sqrt6}{4},\frac{\pi\sqrt6}{4},\frac\pi2,0)\) | \(80/105\) |
| \(R_3\) | \((1,3,1,3)\) | \((0,\frac{\pi\sqrt2}{4},\frac{\pi\sqrt2}{4},0,0,\frac{\pi\sqrt2}{4},\frac{\pi\sqrt2}{4},0)\) | \(8/105\) |

Every base generator is a direct sum of the indicated block generators, with zero couplings between blocks and at the wrap edge. Hence its exponential is exactly the corresponding direct sum of signed reversals. Each block reversal has determinant \(+1\): the reversal permutation sign and the product of row signs are both \((-1)^{L(L-1)/2}\). Thus every \(R_\alpha\in SO(8)\).

All four bases are gapped. Under a reflection, the conjugated skew generator may reverse some coupling signs, but it remains a real nearest-neighbour cycle generator. Since the nonzero graph is a forest, a vertex-sign gauge can make every nonzero coupling nonnegative if desired; this gauge leaves every principal minor unchanged.

## 2. Dihedral symmetrization and exact moment proof

Let \(P_g\) be the site-permutation matrix for \(g\in D_8\). Define
\[
\mu=\sum_{\alpha=0}^3\frac{\lambda_\alpha}{16}
\sum_{g\in D_8}\delta_{P_gR_\alpha P_g^{\mathsf T}}.
\]
Each conjugate is again a legal cycle exponential. Since every dihedral map either preserves or swaps the two sublattices,
\[
P_gDP_g^{\mathsf T}=\varepsilon_gD,\qquad \varepsilon_g\in\{\pm1\}.
\]
Consequently
\[
Q_{\alpha,g}
=P_gR_\alpha P_g^{\mathsf T}D
=\varepsilon_gP_gQ_\alpha P_g^{\mathsf T}.
\]
For even \(|I|\), the global sign disappears from the principal determinant:
\[
\det(Q_{\alpha,g})_{I,I}
=\det(Q_\alpha)_{g^{-1}I,g^{-1}I}.
\]
Thus the expectation under \(\mu\) is constant on every dihedral orbit of subsets. It is enough to check one orbit average for each orbit.

There are 4 pair orbits, 8 quartic orbits, 4 sixth-order orbits, and 1 full-set orbit. The following table gives the exact orbit averages for the four base atoms and their weighted mean. Atom columns are ordered \(R_0,R_1,R_2,R_3\).

| Order | Orbit representative | Size | \(R_0\) | \(R_1\) | \(R_2\) | \(R_3\) | Mixture |
|---:|---|---:|---:|---:|---:|---:|---:|
| 2 | \(\{0,1\}\) | 8 | \(-1\) | \(-1/4\) | \(-1/8\) | \(0\) | \(-1/7\) |
| 2 | \(\{0,2\}\) | 8 | \(1\) | \(0\) | \(-1/8\) | \(-3/4\) | \(-1/7\) |
| 2 | \(\{0,3\}\) | 8 | \(-1\) | \(-1/4\) | \(-1/8\) | \(0\) | \(-1/7\) |
| 2 | \(\{0,4\}\) | 4 | \(1\) | \(0\) | \(-1/4\) | \(1/2\) | \(-1/7\) |
| 4 | \(\{0,1,2,3\}\) | 8 | \(1\) | \(1/4\) | \(0\) | \(1/2\) | \(3/35\) |
| 4 | \(\{0,1,2,4\}\) | 16 | \(-1\) | \(0\) | \(1/8\) | \(0\) | \(3/35\) |
| 4 | \(\{0,1,2,5\}\) | 8 | \(1\) | \(0\) | \(1/8\) | \(-1/4\) | \(3/35\) |
| 4 | \(\{0,1,3,4\}\) | 8 | \(1\) | \(0\) | \(1/8\) | \(-1/4\) | \(3/35\) |
| 4 | \(\{0,1,3,5\}\) | 16 | \(-1\) | \(0\) | \(1/8\) | \(0\) | \(3/35\) |
| 4 | \(\{0,1,3,6\}\) | 8 | \(1\) | \(1/4\) | \(0\) | \(1/2\) | \(3/35\) |
| 4 | \(\{0,1,4,5\}\) | 4 | \(1\) | \(1/2\) | \(0\) | \(0\) | \(3/35\) |
| 4 | \(\{0,2,4,6\}\) | 2 | \(1\) | \(0\) | \(0\) | \(1\) | \(3/35\) |
| 6 | \(\{0,1,2,3,4,5\}\) | 8 | \(-1\) | \(-1/4\) | \(-1/8\) | \(0\) | \(-1/7\) |
| 6 | \(\{0,1,2,3,4,6\}\) | 8 | \(1\) | \(0\) | \(-1/8\) | \(-3/4\) | \(-1/7\) |
| 6 | \(\{0,1,2,3,5,6\}\) | 8 | \(-1\) | \(-1/4\) | \(-1/8\) | \(0\) | \(-1/7\) |
| 6 | \(\{0,1,2,4,5,6\}\) | 4 | \(1\) | \(0\) | \(-1/4\) | \(1/2\) | \(-1/7\) |
| 8 | \(\{0,1,2,3,4,5,6,7\}\) | 1 | \(1\) | \(1\) | \(1\) | \(1\) | \(1\) |

Every entry is rational because each \(Q_\alpha\) is a signed permutation. The weighted column is obtained exactly from \((1,16,80,8)/105\). The table covers all 17 dihedral orbits and therefore all 127 nonempty even subsets; the empty-subset moment is trivially one.

After merging duplicate group images, the 64 labelled atoms give 37 distinct signed-permutation matrices. Their exact aggregate-weight histogram is
\[
17\times\frac1{105},\qquad
16\times\frac1{21},\qquad
4\times\frac2{105}.
\]
In particular, the minimum distinct-atom weight is \(1/105>0\).

## 3. Exact machine verification

The dependency-free verifier [verify_n8_physical_cycle_balanced_slice_ensemble.py](verify_n8_physical_cycle_balanced_slice_ensemble.py) independently:

1. builds the four signed-reversal permutations from their compositions;
2. checks \(R\in SO(8)\), \(Q=RD\) symmetric, \(Q^2=I\), and \(\operatorname{tr}Q=0\);
3. constructs all 64 labelled dihedral images and merges duplicates;
4. computes every even principal minor by the exact signed-permutation determinant rule;
5. checks all 128 even subsets including the empty subset against the exact rational target;
6. reconstructs all 17 orbit averages and the 37-atom positive weight histogram.

The machine-readable output is [evidence/n8_physical_cycle_balanced_slice_ensemble.json](evidence/n8_physical_cycle_balanced_slice_ensemble.json). The verifier uses only integer arithmetic and fractions.Fraction; it uses no floating-point matrix exponential, optimizer, or numerical tolerance.

Hosted reproducibility is provided by [.github/workflows/eui-physical-cycle-ensemble-n8.yml](.github/workflows/eui-physical-cycle-ensemble-n8.yml).

## 4. Relation to the N=8 period-two no-go and N=42

This result does not contradict the exact [N=8 period-two mixture no-go](THEORY_N8_PERIOD_TWO_MIXTURE_FOURTH_ORDER_NO_GO.md). That theorem excludes every probability measure supported entirely on \(c_{2j}=a,c_{2j+1}=b\). The present ensemble is not supported on that two-parameter subfamily: three of its four base patterns break period-two symmetry. The identity atom \(R_0\) alone does not change the support restriction.

Together with the existing N=4 and N=6 single-exponential constructions, this completes the small-size matrix-moment tests requested in Issue #7:
- \(N=4\): one physical exponential;
- \(N=6\): one physical exponential;
- \(N=8\): a positive mixture of 37 distinct physical cycle exponentials.

The construction is a useful warning against extrapolating the N=8 period-two separator to the full cycle family: the full \(N=8\) physical convex hull does contain the target.

**Limitations:** this is a small even-\(n\) matrix-moment result. The odd-\(n\) program-span and joint-parity diamond theorems are not extended to \(n=4\) here. No Choi trace-distance or channel diamond-distance conclusion is claimed. The N=42 physical-cycle convex-hull problem, complete N=42 ensemble, and global N=42 separator remain unresolved.
