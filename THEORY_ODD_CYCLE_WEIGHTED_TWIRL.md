# Optimal support-only CP certificate for a weighted complementary twirl

The [uniform program twirl](THEORY_ODD_CYCLE_PROGRAM_TWIRL.md) extracts a target-unitary component of weight \(M/(D^4s)\) from the complementary branch. Conditioning its Pauli distribution on the program syndrome gives a strictly stronger full-physical-family certificate. We solve the resulting **support-only synthesis-certificate optimization**, not the unrestricted recovery or diamond-norm optimization.

## Recovery and certified improvement

Use the same six-query encoder, ideal-flag selective architecture and fair parity orientation, on an odd ring \(n\ge21\). Each oracle call is \(W_\epsilon=e^{-i(H+\epsilon P)}\), with \(P=\prod_jX_j\); the target is the channel of \(e^{+iH}\). Errors use the diamond norm without a factor of one half. Retain the notation
\[
 D=2^{n-1},\quad s=\tfrac12\binom{2n}{n},\quad r=D^2-s=fD^2,
 \quad \beta=M/D^4,\quad p=3/(4f),\quad
 g=(e^{-6i\epsilon}+3e^{2i\epsilon})/4.
\]
Pauli labels are even Majorana subsets modulo full complementation. The set \(\mathcal S\) contains the balanced labels. For a label \(P\) of degree \(2k\), write \(h(P)=|a_k|\), with the integer coefficients from the [uniform-twirl verifier](verify_ising_program_twirl.py). These magnitudes are well defined under full complementation and positive at odd \(n\).

On an ideal-flag complementary program label \(R\), apply \(R^\dagger\), then draw a balanced Pauli \(T\) with probability
\[
 q_R(T)=\frac{h(RT)}{Z_R},\qquad
 Z_R=\sum_{T\in\mathcal S}h(RT).
\]
Apply \(T\) to the selected data. Preserve the protected program coherently and leave the orthogonal split flag unchanged. This is a fixed CPTP decoder, independent of the Hamiltonian and drift. It preserves exact ideal inversion, first-order common parity-drift cancellation and six unconditional queries.

Define
\[
 L=\frac1s\sum_{R\notin\mathcal S} Z_R^2.
\]
**Theorem.** For every physical Hamiltonian and drift, the new decoder obeys
\[
 \mathcal E_H^{\rm weighted}(\epsilon)
 \le |1-g|+\frac32(1-f)\sin^2(4\epsilon)
       -\frac{9M^2}{8r^2L}\sin^2(4\epsilon).
\]
This synthesis argument gives an upper bound and does not establish attainment. The subsequent [radial recovery theorem](THEORY_ODD_CYCLE_RADIAL_RECOVERY.md) determines this decoder's exact physical supremum and supplies a better ML decoder with an inverse-cube gain guarantee; the bounds here remain valid. The guaranteed quadratic-coefficient reduction from this argument is
\[
 \Delta C_{\rm cert}=\frac{18M^2}{r^2L}.
\]
For every odd \(n\ge5\), \(L<sM\), so this guarantee strictly exceeds the uniform-twirl gain \(18M/(r^2s)\). Thus it certifiably improves the full-family supremum of that particular decoder whenever \(\sin(4\epsilon)\ne0\).

Exact integer/Fraction evaluations give:

| n | certified quadratic gain | gain / uniform-twirl gain |
|---|---:|---:|
| 21 | 4.00537895313e-11 | 2.75901457432 |
| 23 | 2.65439524926e-12 | 2.92444925378 |
| 83 | 4.46951879614e-48 | 6.41714882349 |

The absolute gains remain very small. No useful asymptotic performance improvement or globally optimal recovery is asserted.

## 1. A synthesis certificate for arbitrary positive distributions

Let \(V\) be the intended selected-sector inverse and \(A_R=R^\dagger L_R\). The [uniform support proof](THEORY_ODD_CYCLE_PROGRAM_TWIRL.md#a-choi-support-certificate) gives
\[
 \sum_R A_R^\dagger A_R=\beta I,\qquad
 B_R:=VA_R^\dagger=\mathcal T(RV^\dagger)R\in\mathcal S.
\]
Write \(V=\sum_T v_T T\), with \(\sum_T|v_T|^2=1\). The Pauli-diagonal form of \(\mathcal T\) implies that the coefficient \(b_{RT}\) of \(T\) in \(B_R\) satisfies
\[
 |b_{RT}|^2=D^{-4}h(RT)^2|v_T|^2.
\]
Transpose signs and Pauli phases disappear in this identity.

For any positive distribution \(q_R(T)\), the complementary recovered map has Kraus operators \(C_{RT}=\sqrt{q_R(T)}\,T A_R\). The identity
\[
 V=\beta^{-1}\sum_R B_R A_R
   =\sum_{R,T}\frac{b_{RT}}{\beta\sqrt{q_R(T)}}C_{RT}
\]
produces a rank-one CP certificate by Cauchy--Schwarz in the Kraus coefficient space. Specifically, set
\[
 L_T(q)=\sum_{R\notin\mathcal S}\frac{h(RT)^2}{q_R(T)},
 \qquad L_{\max}(q)=\max_{T\in\mathcal S}L_T(q).
\]
The squared coefficient norm is at most \(L_{\max}(q)/(\beta^2D^4)\). Therefore the unnormalized Choi matrix satisfies
\[
 J_{H,q}\succeq
 \frac{M^2}{D^4L_{\max}(q)}
 |V\rangle\!\rangle\langle\!\langle V|.
\]
This estimate uses only unit norm and membership of \(V\) in the program span. It need not exploit all constraints on physically realizable \(V\).

Extracting this target component from the selective residual channel reduces its noise trace weight by
\(p^2|b|^2M^2/(D^4L_{\max})\), where \(|b|^2=4\sin^2(4\epsilon)\). The cross-parity factor stays \(g\). The balanced norm upper bound gives the stated error bound once \(L_{\max}=L\) is established below. Unlike the uniform-twirl eigenvector certificate, this synthesis certificate need not saturate the Choi or diamond bound.

## 2. Middle-layer symmetry and exact certificate optimality

Represent labels temporarily by their full even subsets of the \(2n\) Majoranas. Let \(C\) be the subset of all \(b\)-Majoranas. Translating a label by symmetric difference with \(C\) turns the balanced condition into
\[
 |T\mathbin\triangle C|=n.
\]
Since \(n\) is odd, all translated labels have odd weight. Full complementation identifies antipodal labels. Thus \(\mathcal S\) is the central Hamming layer in this translated, antipodally identified cube.

Coordinate permutations preserve this layer, its complement, and pairwise Hamming distances. They act transitively on \(\mathcal S\). Since \(h(RT)\) depends only on the distance between the labels, these permutations preserve \(Z_R\) and show that
\[
 L_T(q^{\rm weighted})=\sum_R h(RT)Z_R
\]
is the same for every balanced \(T\). Its common value is its average, namely \(s^{-1}\sum_R Z_R^2=L\).

For any other distributions,
\[
 L_{\max}(q)\ge\frac1s\sum_TL_T(q)
 \ge\frac1s\sum_R\left(\sum_T h(RT)\right)^2=L,
\]
where the second inequality is Cauchy--Schwarz with \(\sum_Tq_R(T)=1\). The weighted rule attains both inequalities. It therefore maximizes this support-only synthesis certificate among **all** syndrome-dependent Pauli distributions supported on \(\mathcal S\), at every odd size.

This averaging argument concerns label combinatorics. It is not a prior over legal physical oracles: a program-span basis label need not itself be reachable by the nearest-neighbour physical Hamiltonian. The argument proves optimality of the stated certificate, not physical minimax optimality of the decoder.

The same transitivity shows that \(\sum_Rh(RT)^2=M\) for every balanced \(T\), using \(T=I\) and the constant-effect calculation to identify the value. Hence
\[
 L=\frac1s\sum_R Z_R^2
 \le\sum_R\sum_T h(RT)^2=sM.
\]
The inequality is strict if a row has two distinct magnitudes. Choose \(R\) containing two \(a\)-Majoranas, and compare \(T=I\) with a balanced bilinear using a third \(a\)-Majorana and any \(b\)-Majorana. The two distances give \(|a_1|\) and \(|a_2|\), with ratio \(3/(2n-3)<1\) for odd \(n\ge5\). This proves the strict improvement without numerical extrapolation.

## 3. Polynomial exact evaluation and sampling

If the translated syndrome has weight \(\ell\), define
\[
 Z_\ell=\frac12\sum_u
 \binom\ell u\binom{2n-\ell}{n-u}
 \left|a_{(\ell+n-2u)/2}\right|.
\]
Only valid binomial indices are included. The factor \(1/2\) identifies antipodal middle-layer labels. Then
\[
 L=\frac1{2s}\sum_{\substack{\ell\ {\rm odd}\\\ell\ne n}}
                   \binom{2n}{\ell}Z_\ell^2.
\]
This requires only polynomially many integer operations. It also gives an efficient exact sampling recipe: choose intersection size \(u\) with weight
\(\binom\ell u\binom{2n-\ell}{n-u}|a_{(\ell+n-2u)/2}|\), then choose a uniform \(u\)-subset inside the translated syndrome and an \((n-u)\)-subset outside it. Translate back and identify antipodes. The resulting distribution on \(T\) is exactly \(q_R(T)\). This does not supply a new efficient compilation of the protected-program measurement or the complete encoder.

## Evidence, reproducibility and next action

Run `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_weighted_twirl.py` with NumPy/SciPy. The standalone verifier:

- agrees exactly between full enumeration, independent two-frame intersection counting, and the middle-layer formula at \(n=3,5,7\);
- reconstructs actual physical complementary maps for identity, fields, edge Pauli and four seeded noncommuting Hamiltonians each at \(n=3,5\), and checks the extracted Choi residual is positive with the certified uniform trace effect (tolerance \(2\times10^{-12}\));
- evaluates the long-ring gains using exact integers/Fractions at \(n=21,23,83\).

The physical checks reuse the uniform verifier through an optional callback; its existing checks still run. The small physical sizes test the certificate algebra, not the \(n\ge21\) cancellation protocol. The all-size statement follows from the analytic synthesis and Hamming-layer proofs.

The [EUI manuscript and robustness appendix](https://arxiv.org/html/2506.20570v1) supply the physical setting. The prior uniform-twirl note distinguishes the established approximate-transpose channel from its EUI support application. Neither that channel nor Cauchy--Schwarz is claimed as new; this note records the EUI certificate and its combinatorial optimization without claiming literature-wide originality.

The [radial cross-effect proof](THEORY_ODD_CYCLE_RADIAL_RECOVERY.md) now resolves the Choi gap for this rule and optimizes the larger radial class, giving a polynomial rather than exponentially small gain guarantee. The next high-value question is whether non-radial or coherent recovery can improve that identity-attained optimum. Improving this same relaxed certificate by merely retuning its Pauli probabilities is now ruled out. The exact worst-case error of this absolute-weight decoder is now resolved by the linked radial theorem. Unrestricted six-query optimality and the pentagon six-versus-seven query question remain open.
