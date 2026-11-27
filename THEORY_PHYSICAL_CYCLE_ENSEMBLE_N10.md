# Exact positive physical cycle ensemble for the complete N=10 balanced-slice moment target

Date: 2026-11-27. Related: [Issue #7](https://github.com/tengxianglin/EfficientUnitaryInversion/issues/7), the [N=8 full-cycle construction](THEORY_PHYSICAL_CYCLE_ENSEMBLE_N8.md), and the [N=10 block-mirror no-go](THEORY_N10_BLOCK_MIRROR_SUBFAMILY_NO_GO.md).

## Theorem

Let \(N=10\), \(n=5\), and let
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
with indices modulo ten. Define
\[
R(c)=e^{A(c)},\qquad D=\operatorname{diag}(1,-1,\ldots,1,-1),
\qquad Q(c)=R(c)D.
\]
For every even subset \(I\subseteq\mathbb Z_{10}\), \(|I|=2r\), set
\[
\tau_I=(-1)^r\frac{\binom5r}{\binom{10}{2r}}.
\]
Then there exists a probability measure supported on at most 260 physical cycle exponentials, each with **all ten couplings strictly positive**, such that
\[
\boxed{\mathbb E_\mu\det Q(c)_{I,I}=\tau_I
\quad\text{for every even }I\subseteq\mathbb Z_{10}.}
\]
The non-rational weights are defined as the unique exact-real solution of a pinned \(13\times13\) moment system. The independent 512-bit Arb certificate proves that this system is nonsingular and that every weight is strictly positive. Exact principal-minor identities then imply all omitted moment equations. This is an existence theorem, not a floating-point fit.

The target values are
\[
\tau_{|I|=2}=-\frac19,\quad
\tau_{|I|=4}=\frac1{21},\quad
\tau_{|I|=6}=-\frac1{21},\quad
\tau_{|I|=8}=\frac19,\quad
\tau_{|I|=10}=-1.
\]

## 1. Frozen strictly positive physical support

The 13 base coupling vectors are stored as exact decimal rationals in [evidence/n10_positive_cycle_ensemble_atoms.json](evidence/n10_positive_cycle_ensemble_atoms.json). Every decimal string is interpreted as an exact rational, not a binary floating-point number.

| Atom | \(c_0,\ldots,c_9\) |
|---:|---|
| 1 | (1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896, 1.0788341596387896) |
| 2 | (0.4032567733506249, 0.15170492244876216, 0.3087593264925357, 0.2539318514222358, 1.104851296324943, 0.8153809363035497, 0.2292475249011958, 0.4478156335829401, 1.1373474266233217, 0.24971538231024118) |
| 3 | (0.02177169589239904, 2.900338152054269, 0.5271596392953278, 1.3743031751504102, 1.1213834055396639, 1.6140425138842218, 2.0418916421914037, 1.6110749623111231, 0.6726749106662882, 1.4893503849786016) |
| 4 | (7.530539183374695, 1.7156702647290736, 7.530539183374695, 1.7156702647290736, 7.530539183374695, 1.7156702647290736, 7.530539183374695, 1.7156702647290736, 7.530539183374695, 1.7156702647290736) |
| 5 | (1.7465285335359806, 4.616363112330272, 0.6960026393312752, 1.566407199174237, 1.5577010640202382, 1.9442953232425009, 0.2941127177054075, 1.3791744154006709, 0.6296342796875415, 1.1497262261281131) |
| 6 | (0.30029157140367063, 1.055916812536728, 0.1414413891248127, 1.4658111765277915, 0.3872072282028176, 0.17022520636014307, 0.003827933674451301, 0.8878051210501476, 1.3257105023987816, 0.08882573822097177) |
| 7 | (0.06368657086380293, 0.8233505320970474, 0.8729283377951499, 0.11928852111554324, 1.1004085713817406, 1.6186041404825076, 1.7744493468176161, 1.5466207558604266, 0.6835292026946928, 2.10480617999538) |
| 8 | (1.1746969160957557, 1.8771541853657465, 0.6765044420812184, 0.09148364996939533, 0.8005619858801748, 0.25134185437408857, 0.3224344427341958, 0.42817029295471726, 0.3813784527519739, 2.737665897752713) |
| 9 | (5.431195090010676, 1.509617732156352, 5.431195090010676, 1.509617732156352, 5.431195090010676, 1.509617732156352, 5.431195090010676, 1.509617732156352, 5.431195090010676, 1.509617732156352) |
| 10 | (1.71937386531825, 3.301581293086543, 1.71937386531825, 3.301581293086543, 1.71937386531825, 3.301581293086543, 1.71937386531825, 3.301581293086543, 1.71937386531825, 3.301581293086543) |
| 11 | (0.7555574308824503, 0.04075824227511716, 1.3955403155264843, 0.30540084871605505, 1.3693902846520905, 1.0531277108870867, 0.26475587546829976, 1.9343193757912622, 0.3354230259461561, 0.8456648338680351) |
| 12 | (2.1884619326164203, 2.787596473843775, 4.381775859406539, 3.156337710726171, 0.748489213437188, 1.176265054810419, 1.3921129242937688, 1.0244363090958788, 0.23450059573688503, 4.7570270436508) |
| 13 | (0.7377611725650661, 0.05587750337103081, 0.7377611725650661, 0.05587750337103081, 0.7377611725650661, 0.05587750337103081, 0.7377611725650661, 0.05587750337103081, 0.7377611725650661, 0.05587750337103081) |

The smallest base coupling is exactly \(0.003827933674451301>0\).

## 2. D10 symmetrization remains inside the positive physical family

Let \(P_g\) be the site permutation for \(g\in D_{10}\). Rotations permute the positive edge couplings. A reflection reverses the cycle orientation and produces the negative of a permuted coupling vector. Since the cycle is even, conjugation by the alternating vertex-sign matrix \(D\) flips every edge sign:
\[
D A(c')D=-A(c').
\]
It therefore turns each reflected generator back into one with all couplings positive. Diagonal sign conjugation leaves every principal minor unchanged:
\[
\det (D R D)_{I,I}=\det R_{I,I}.
\]
Thus all twenty dihedral images can be represented by legal strictly positive cycle couplings without changing any even principal-minor feature.

For base weights \(w_1,\ldots,w_{13}\), define
\[
\mu=\frac1{20}\sum_{j=1}^{13}w_j\sum_{g\in D_{10}}
\delta_{P_gR(c^{(j)})P_g^{\mathsf T}},
\]
with the reflection images replaced by their positive-coupling vertex-sign gauges. The measure is \(D_{10}\)-invariant, so each principal-minor coordinate is equal to its orbit average.

## 3. Exact reduction to twelve moment coordinates

The even-subset dihedral orbit counts are:
- order 0: 1;
- order 2: 5;
- order 4: 16;
- order 6: 16;
- order 8: 5;
- order 10: 1.

There are 44 orbits covering all 512 even subsets. We only need four pair-orbit averages and eight quartic-orbit averages.

### Pair identity

Since \(Q\) is a symmetric involution with five \(+1\) and five \(-1\) eigenvalues,
\[
\sum_{|I|=2}\det Q_{I,I}=e_2(Q)
=\frac{(\operatorname{tr}Q)^2-\operatorname{tr}(Q^2)}2=-5.
\]
The five pair-orbit sizes are \((10,10,10,10,5)\). Matching the first four pair averages to \(-1/9\) therefore forces the fifth to equal \(-1/9\) as well.

### Triple-to-quartic identity

For every three-set \(K\), the principal-minor generating identity
\[
\sum_{I\supseteq K}t^{|I|}\det Q_{I,I}
=\det(I+tQ)\det\!\left[tQ(I+tQ)^{-1}\right]_K
=t^3(1-t^2)^2\det(Q_{K,K}-tI_3)
\]
gives, by taking the coefficient of \(t^4\),
\[
\boxed{
\sum_{\substack{I\supset K\\|I|=4}}\det Q_{I,I}
=-\sum_{\substack{J\subset K\\|J|=2}}\det Q_{J,J}.
}
\]
After averaging over the eight \(D_{10}\)-orbits of triples, this becomes
\[
Cq+Dp=0,
\]
where \(C\) is the exact \(8\times16\) integer triple/quartet incidence matrix and \(D\) is the exact \(8\times5\) triple/pair incidence matrix.

The first eight quartic columns are pivots:
\[
\boxed{\det C_{[:,0:8]}=64.}
\]
Hence the four pair coordinates and the last eight quartic coordinates determine all sixteen quartic coordinates. The balanced target \(p_d=-1/9\), \(q_o=1/21\) satisfies these eight equations exactly.

The eight free quartic representatives are
\[
\begin{split}
&(0,1,3,8),\ (0,1,4,5),\ (0,1,4,6),\ (0,1,4,7),\\
&(0,1,5,6),\ (0,2,4,6),\ (0,2,4,7),\ (0,2,5,7).
\end{split}
\]
The four selected pair representatives are \((0,1),(0,2),(0,3),(0,4)\).

### Complementary minors

Jacobi's complementary-minor identity, \(Q^{-1}=Q\), and \(\det Q=-1\) imply
\[
\boxed{\det Q_{I,I}=-\det Q_{I^c,I^c}.}
\]
Thus matching all pair and quartic coordinates forces all sixth- and eighth-order coordinates. The full-set moment is \(\det Q=-1\), and the empty-set moment is one.

## 4. The exact-real weight system and its certificate

For the thirteen frozen atoms, let \(M\) be the \(13\times13\) matrix whose first four rows are their orbit-averaged pair features at the selected representatives, whose next eight rows are their orbit-averaged quartic features at the representatives above, and whose last row consists of ones. Define
\[
b=(-1/9,-1/9,-1/9,-1/9,
\underbrace{1/21,\ldots,1/21}_{8},1)^{\mathsf T}.
\]
The weights are the exact-real vector
\[
\boxed{w=M^{-1}b.}
\]
They are not asserted to be rational. The 512-bit Arb verifier encloses the exact exponential entries, proves \(\det M\ne0\), solves the interval linear system, and proves every component of \(w\) strictly positive. The final hosted certificate also audits all five pair and all sixteen quartic orbit residuals independently.

The proof uses only:
1. the certified invertibility and positivity of this finite exact-real system;
2. the exact pair identity;
3. the exact triple/quartic incidence identity with pivot determinant 64;
4. Jacobi complementary minors.

The interval residual checks are independent numerical consistency checks; exact equality of the omitted coordinates follows from the algebraic identities, not merely from an interval containing zero.

## 5. Reproduction

Install python-flint 0.9.0, then run:

    python -m py_compile verify_n10_positive_cycle_ensemble.py
    python verify_n10_positive_cycle_ensemble.py

The frozen input is evidence/n10_positive_cycle_ensemble_atoms.json; the verifier writes evidence/n10_positive_cycle_ensemble_arb.json. The workflow pins Python 3.11 and python-flint 0.9.0.

## 6. Scope and implications

This resolves the complete balanced-slice principal-minor convex-hull problem for the \(N=10\) real nearest-neighbour cycle-exponential family, with all base and symmetrized couplings representable as strictly positive couplings.

It does **not** solve the \(N=42\) physical convex-hull problem. It does show that the N=10 seven-coordinate block-mirror separator cannot be a full-family obstruction, consistent with the previously certified connected-cycle escape. The result is a small-size existence theorem and a test case for the N=42 search, not an operational Choi/diamond-distance theorem.
