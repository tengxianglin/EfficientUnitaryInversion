# Program-supported Pauli twirling beats complementary data replacement

The [replacement-class theorem](THEORY_ODD_CYCLE_COMPLEMENT_DEPOLARIZATION.md#3-optimality-among-complementary-data-replacement-recoveries) fixes the best error of a decoder that discards complementary data and prepares a state. A Pauli channel acting on that data escapes the premise. Its Choi support can be matched to the physical ideal-program span, giving a stronger full-family certificate.

## Result and scope

Fix an odd ring of length \(n\ge21\), the coherent six-query encoder, and the fair parity orientation. Let
\[
 D=2^{n-1},\quad s=\tfrac12\binom{2n}{n},\quad r=D^2-s=fD^2,
 \quad p=\frac3{4f},\quad
 g=\tfrac14e^{-6i\epsilon}+\tfrac34e^{2i\epsilon}.
\]
Let \(\mathcal S\) be the physical program space of dimension \(s\), spanned by balanced Majorana Pauli labels, and let \(M\) and \(\beta=M/D^4\) be as defined in the [constant-effect theorem](THEORY_ODD_CYCLE_COMPLEMENT_DEPOLARIZATION.md). In particular \(M>0\) and the complementary data effect is \(\beta I\) for every physical Hamiltonian.

**Recovery.** On an ideal-flag complementary Bell label \(R\), apply \(R^\dagger\) to the selected-parity data, then apply
\[
 \mathcal R_{\mathcal S}(\rho)=\frac1s\sum_{T\in\mathcal S}T\rho T^\dagger.
\]
Here the sum is over the balanced Pauli basis labels, not all vectors in the subspace. Preserve the protected program space coherently and leave the orthogonal split flag unchanged. The recovery is independent of the Hamiltonian and drift.

**Theorem.** This recovery retains exact ideal inversion and first-order common parity-drift cancellation with six unconditional forward queries. Its exact physical-family supremum, in the diamond convention without a factor of one half, is
\[
 \sup_H\mathcal E_H^{\rm twirl}(\epsilon)
 = |1-g|+\frac32(1-f)\sin^2(4\epsilon)
       -\frac{9M}{8r^2s}\sin^2(4\epsilon).
\]
The identity oracle attains the bound. The quadratic improvement over the old balanced decoder is
\[
 \Delta C_{\rm twirl}=\frac{18M}{r^2s}
 =\frac{D^2}{s}\Delta C_{\rm reset}
 =\frac{\Delta C_{\rm reset}}{1-f}.
\]
At \(n=21\), this is \(1.45174258607\times10^{-11}\), about \(4.08545\) times the best replacement-class gain. It remains very small. Indeed \(M\le rs\) gives \(\Delta C_{\rm twirl}\le18/r=O(4^{-(n-1)})\). This is a strict certified improvement, not a practically large one or an optimal-recovery result.

## A Choi support certificate

Work in either selected parity space, in the occupation basis. Write \(V\) for the intended inverse. The physical Hamiltonian is real symmetric, so \(V^T=V\). The [program-span theorem](THEORY_ODD_CYCLE_PROGRAM_SPAN_THEOREM.md) gives \(V,V^\dagger\in\mathcal S\). The shared Bell projector has the Pauli expansion
\[
 Q=D^{-2}\sum_P a_P P\otimes\bar P,
 \qquad [Q,V\otimes V]=0.
\]
These are the shared-projector identities used in the existing encoder construction.

Define the linear map
\[
 \mathcal T(X)=D^{-1}\operatorname{Tr}_E[(I\otimes X)Q].
\]
Its Pauli expansion is diagonal in Pauli labels: it multiplies the coefficient of each \(P\) by a scalar (which can include its transpose sign). It therefore preserves every span of a specified set of Pauli labels. The ideal shared-projector amplitude on Bell label \(R\) is
\[
 L_R=D^{-1}\operatorname{Tr}_E[(I\otimes R^\dagger)(V\otimes V)Q]
     =\mathcal T(VR^\dagger)V.
\]
The last equality uses commutation with \(V\otimes V\) and cyclicity of the partial trace for factors acting only on the traced register.

Choose Hermitian Pauli representatives and put \(A_R=R^\dagger L_R\). Then
\[
 VA_R^\dagger=\mathcal T(RV^\dagger)R\ \in\mathcal S.
\]
For clarity, multiplication of \(V^\dagger\) by \(R\) shifts its Pauli support from \(\mathcal S\) to \(R\mathcal S\). The Pauli-diagonal map \(\mathcal T\) does not change that support. Right multiplication by \(R\) shifts every label back to \(\mathcal S\), up to phases. No positivity property of \(\mathcal T\) is assumed.

Let \(J_H\) be the unnormalized Choi matrix of the complementary CP map
\[
 \rho\longmapsto\sum_{R\notin\mathcal S}
                  \mathcal R_{\mathcal S}(A_R\rho A_R^\dagger),
\]
with the factor \(pb\) omitted, where \(b=e^{2i\epsilon}-e^{-6i\epsilon}\). The twirl itself has Choi matrix \((D/s)\Pi_{\mathcal S}\). In row-vectorization notation its action on the target vector is consequently
\[
 J_H|V\rangle\!\rangle
 =\frac Ds\left|\sum_{R\notin\mathcal S}
           \Pi_{\mathcal S}(VA_R^\dagger)A_R\right\rangle\!\rangle
 =\frac{D\beta}{s}|V\rangle\!\rangle.
\]
The final equality uses the support inclusion and
\(\sum_R A_R^\dagger A_R=\sum_RL_R^\dagger L_R=\beta I\).
Since \(J_H\) is positive and \(\langle\!\langle V|V\rangle\!\rangle=D\),
\[
 J_H-\frac\beta s|V\rangle\!\rangle\langle\!\langle V|\succeq0.
\]
Thus the complementary recovery contains a target-unitary CP component of weight \(\beta/s\), uniformly for every physical Hamiltonian. The replacement decoder extracted only \(\beta/D^2\).

## From the CP certificate to the exact supremum

The [selective residual decomposition](THEORY_ODD_CYCLE_SELECTIVE_SYNDROME.md) has selected-sector noise weight
\(\gamma=3(1-f)\sin^2(4\epsilon)\). Removing its original complementary outcomes leaves a CP residual. Inserting the recovered map and extracting the target component gives a new CP residual with uniform trace weight
\[
 \gamma_{\rm twirl}
 =\gamma-p^2|b|^2\frac\beta s
 =\left[3(1-f)-\frac{9M}{4r^2s}\right]\sin^2(4\epsilon).
\]
The coefficient is nonnegative because it is the trace weight of this CP residual. The cross-parity multiplier stays \(g\): the modified outcomes have zero ideal program amplitude and no opposite-parity data component. With equal orientations, the [balanced norm argument](THEORY_ODD_CYCLE_BALANCED_SIX_QUERY.md) gives the full-family upper bound \(|1-g|+\gamma_{\rm twirl}/2\), using \(\gamma_{\rm twirl}\le\gamma\le2|1-g|\).

At \(H=0\) all unmodified residual errors are nonidentity Paulis. In addition, the recovered Choi residual above is orthogonal to the target vector, since that vector was an eigenvector and its full eigenvalue was subtracted. The equal two-sector Bell input therefore makes the positive residual orthogonal to the two target components and attains the upper bound. This proves the stated supremum.

Ideal exactness and the vanishing first derivative are unchanged: all modified ideal-flag complementary amplitudes vanish at zero drift and are proportional to \(b=O(\epsilon)\).

## Implementation, literature and next question

The twirl need not enumerate \(s\) Paulis. Sample \(k\in\{0,\ldots,n\}\) with probability \(\binom nk^2/\binom{2n}{n}\), then choose independently a uniform \(k\)-subset of the \(a\)-Majoranas and a uniform \(k\)-subset of the \(b\)-Majoranas. Apply their monomial as a known Pauli string. Full complementation pairs the two representatives of each sector Pauli, so this samples the \(s\) labels uniformly. Classical sampling and forming the Pauli string require polynomial work in \(n\). The program measurement is the existing selective measurement; this does not claim an efficient new compilation of that measurement or the full encoder.

The intermediate idea of using the symmetric matrix subspace connects to the known physical approximate-transpose channel \((\operatorname{Tr}(\rho)I+\rho^T)/(D+1)\). Its Choi matrix is proportional to the symmetric projector; see Buscemi, D'Ariano, Perinotti and Sacchi, *Optimal realization of the transposition maps*, Physics Letters A **314**, 374–379 (2003), [DOI](https://doi.org/10.1016/S0375-9601(03)00954-X), [primary paper](https://wordpress.qubit.it/wp-content/uploads/publications-dariano/transp.pdf), Eq. (15). That channel is established literature. Here the stronger certificate uses the smaller physical program subspace and the identity \(VA_R^\dagger\in\mathcal S\). No literature-wide originality claim is made.

The next focused optimization is to replace the uniform balanced-Pauli distribution by a syndrome-dependent distribution, starting with weights by balanced Majorana degree. Any claimed improvement must retain a uniform CP or diamond certificate and be checked on identity, field and edge oracles. The unrestricted six-query quadratic optimum and the physical pentagon six-versus-seven query problem remain unresolved.

## Reproducibility and evidence status

Run `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_program_twirl.py` (NumPy/SciPy). The verifier reconstructs the actual physical \(Q\), protected program projector and complementary amplitudes at \(n=3,5\). For seven Hamiltonians per size (identity, diagonal fields, an edge Pauli, four seeded noncommuting cases) it checks the constant effect, support inclusion, the Choi target eigenvector, positivity after extraction and the residual trace effect, with absolute tolerance \(2\times10^{-12}\). It also checks Kraus completeness for the twirl and exact Fraction formulas at \(n=21,23,83\). Seed: \(20261120+n\), inherited from the constant-effect verifier.

These small physical sizes verify dimension-independent identities. They do not implement the long-ring first-order-canceling protocol, which requires \(n\ge21\). The all-length recovery theorem follows from the analytic support and constant-effect proofs, rather than extrapolation of the finite checks.
