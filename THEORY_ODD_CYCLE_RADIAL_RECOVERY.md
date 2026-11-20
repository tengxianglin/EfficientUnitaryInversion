# Exact radial recovery and a polynomial maximum-likelihood gain

The [weighted twirl](THEORY_ODD_CYCLE_WEIGHTED_TWIRL.md) had only a conservative synthesis bound. Direct physical Choi checks suggest a stronger eigenvector identity. A weighted cross-effect lemma proves it for a whole class of radial syndrome rules and yields a maximum-likelihood (ML) decoder whose gain has an inverse-cube lower bound.

## Setting and main result

Fix an odd fully fielded Ising ring of length \(n\ge21\), the coherent six-query encoder and fair parity orientation. Each unconditional forward query is \(W_\epsilon=e^{-i(H+\epsilon P)}\), \(P=\prod_jX_j\), and the target is the channel of \(e^{+iH}\). Diamond errors below have no factor of one half. Use
\[
 D=2^{n-1},\quad s=\tfrac12\binom{2n}{n},\quad r=D^2-s=fD^2,
 \quad p=\frac3{4f},\quad g=(e^{-6i\epsilon}+3e^{2i\epsilon})/4.
\]
Balanced even Majorana labels, modulo full complementation, form the physical program space \(\mathcal S\). On ideal-flag complementary Bell label \(R\), apply \(R^\dagger\), then a balanced Pauli \(T\) drawn from \(q_R\). Leave the protected program coherent and the orthogonal split flag unchanged.

A **radial rule** has \(q_R(T)\) depending only on the absolute imbalance \(d_R=|n_a(R)-n_b(R)|\) and the Majorana degree of \(RT\), with complementary degrees identified. Require normalization over balanced labels. It can include zero probabilities. Both the previous uniform and absolute-coefficient rules are radial.

Let \(h(P)=|a_{|P|/2}|\), with the integer coefficients in [the verifier](verify_ising_program_twirl.py). Translate labels by the subset of all \(b\)-Majoranas; balanced labels then form the middle Hamming layer. A complementary label has translated odd weight \(\ell\ne n\), and \(d_R=|\ell-n|\).

**Theorem (exact radial error).** For every radial rule, define
\[
 G(q)=\sum_{R\notin\mathcal S}h(R)^2q_R(I).
\]
The exact physical-family supremum is
\[
 \sup_H\mathcal E_H^q(\epsilon)
 =|1-g|+\frac32(1-f)\sin^2(4\epsilon)
       -\frac{9G(q)}{8r^2}\sin^2(4\epsilon).
\]
The identity oracle attains it. Ideal exactness and first-order common parity-drift cancellation are retained.

**Theorem (restricted minimax optimum).** Within all radial rules, choose uniformly among the balanced labels maximizing \(h(RT)^2\). Equivalently choose a nearest balanced label in the antipodally identified Hamming cube. This maximizes \(G\), with
\[
 G_{\rm ML}=\frac1{2s}
   \sum_{\substack{\ell\ {\rm odd}\\\ell\ne n}}
      \binom{2n}{\ell}a_{|\ell-n|/2}^{\,2}.
\]
Its quadratic improvement over the old balanced decoder is exactly
\(\Delta C_{\rm ML}=18G_{\rm ML}/r^2\).
This is optimality within the stated radial recovery architecture, not among arbitrary syndrome channels, coherent program recovery, or all encoders.

| n | prior absolute-weight rule: exact gain | ML: exact gain |
|---|---:|---:|
| 21 | 4.83523374944e-8 | 0.00187357262152 |
| 23 | 1.01499277287e-8 | 0.00140333517815 |
| 83 | 9.21842068712e-28 | 2.51098267671e-5 |

The earlier absolute-weight synthesis bounds remain valid but are not tight. ML gives an algebraic guarantee rather than those exponentially small example gains. The resulting absolute reduction is still modest; journal readiness and unrestricted optimality are not implied.

## 1. A constant weighted cross-effect lemma

For a Hermitian Majorana Pauli \(P_0\) of degree \(2k\), write the actual shared-projector expansion as
\[
 Q=D^{-2}\sum_{P_0}\alpha_{P_0}P_0\otimes\bar P_0.
\]
With the charge-conjugation convention used in the existing verifier,
\(\alpha_{P_0}=(-1)^{n_b(P_0)}a_k\), while
\(\bar P_0=(-1)^{k+n_b(P_0)}P_0\). Thus each full degree sum is proportional to \((-1)^ka_k\sum P_0\otimes P_0\). Summing all even subsets with a factor one half accounts for complementary representatives. These degree sums are invariant under the two-copy Gaussian action: conjugation rotates the Hermitian grade basis by a real orthogonal exterior-power matrix.

Consequently, for any real kernel \(u_k=u_{n-k}\),
\[
 Q_u=D^{-2}\sum_{P_0}\alpha_{P_0}u_{|P_0|/2}
                        P_0\otimes\bar P_0
\]
commutes with \(V\otimes V\) for physical Gaussian \(V\), just as \(Q\) does. Positivity or idempotence of \(Q_u\) is not needed. Let \(L_R^u\) be its shared-projector Bell amplitude, and let \(\Pi_d\) project onto program labels of absolute imbalance \(d>0\).

**Cross-effect lemma.** For every such kernel and every physical Hamiltonian,
\[
 \sum_{R:d_R=d}(L_R^u)^\dagger L_R
 =D^{-4}\sum_{R:d_R=d}h(R)^2u_{|R|/2}\ I.
\]

Here is a proof of the required extension of the [constant-effect argument](THEORY_ODD_CYCLE_COMPLEMENT_DEPOLARIZATION.md#1-constant-complementary-probability). First diagonalize a physical Hamiltonian by its real \(\mathrm{SO}(n)\times\mathrm{SO}(n)\) frame. Both shared kernels are invariant under the two-copy action, and \(\Pi_d\) is invariant under the frame because conjugation preserves the separate \(a,b\) counts. It therefore suffices to consider arbitrary independent diagonal mode phases.

For these phases, both kernels conserve the sum of the two occupation-weight rows. At fixed data input \(x\) and output \(y\), let \(F=x\triangle y\). The forced program row on \(F\) is \(x\), with the opposite purifier row; outside \(F\) the program and purifier rows agree. The projector \(\Pi_d\) preserves the program bit-flip support \(F\). Since empty/double labels have zero imbalance, their unrestricted sum makes its matrix elements vanish between different rows off \(F\). On the forced support, its quadratic form is the constant
\[
 \omega_{m,d}=2^{-m}\sum_{j=0}^m\binom mj
                      {\bf1}_{|2j-m|=d},\qquad m=|F|,
\]
times the ordinary inner product. The same statement applies to the bilinear form between amplitudes from \(Q_u\) and \(Q\). Diagonal phases multiply the corresponding forced coefficients equally, so they cancel in that form. Different data inputs have different program bit-flip supports at a common output, hence their effects vanish off diagonal. Thus the cross-effect is independent of the diagonal phases. At \(V=I\), its Pauli expansion is exactly the scalar on the right of the lemma. Conjugating back by the real frame proves the claim for all physical \(H\).

This proof uses invariance and the bilinear matrix-element argument; it does not infer a long-ring identity from a few numerical samples.

## 2. Exact target eigenvalue and diamond supremum

For each imbalance \(d\), write the radial probabilities as \(q_R(T)=u_{d,|RT|/2}\). Normalization is possible with a function of \(d\) alone, by the middle-layer distance counts. Put \(A_R=R^\dagger L_R\), and let \(A_R^{u_d}=R^\dagger L_R^{u_d}\). As in the previous program-support proof,
\(VA_R^\dagger=\mathcal T(RV^\dagger)R\in\mathcal S\).
Multiplying its Pauli coefficients by \(u_{d,|RT|/2}\) yields \(V(A_R^{u_d})^\dagger\). Thus the recovered unnormalized complementary Choi matrix obeys
\[
 J_{H,q}|V\rangle\!\rangle
 =D\left|V\sum_{d>0}\sum_{R:d_R=d}
                       (L_R^{u_d})^\dagger L_R\right\rangle\!\rangle
 =\frac{G(q)}{D^3}|V\rangle\!\rangle.
\]
Since \(\|\operatorname{vec}V\|^2=D\), positivity gives the exact maximal target-component subtraction
\[
 J_{H,q}\succeq\frac{G(q)}{D^4}
                 |V\rangle\!\rangle\langle\!\langle V|.
\]
The residual is orthogonal to the target vector. Inserting the drift amplitude \(pb\), \(|b|^2=4\sin^2(4\epsilon)\), reduces the selected-sector residual trace weight to
\[
 \gamma_q=\left[3(1-f)-\frac{9G(q)}{4r^2}\right]\sin^2(4\epsilon).
\]
Its nonnegativity follows from the CP decomposition. The cross-parity multiplier remains \(g\). The balanced norm argument gives an upper bound \(|1-g|+\gamma_q/2\), since \(\gamma_q\le\gamma\le2|1-g|\). At the identity, unmodified residual errors are nonidentity Paulis and the modified Choi residual is orthogonal to the target. The equal two-sector Bell input attains the bound, proving the supremum.

## 3. ML optimality and a polynomial lower bound

For a radial rule, affine coordinate permutations of the translated cube show that
\(G_T(q)=\sum_Rh(RT)^2q_R(T)\)
is constant on balanced \(T\). Its value equals \(G_I(q)=G(q)\). Averaging these equal numbers gives
\[
 G(q)=\frac1s\sum_R\sum_T h(RT)^2q_R(T)
 \le\frac1s\sum_R\max_T h(RT)^2.
\]
The ML rule attains this bound. The coefficient ratio
\( |a_{k+1}/a_k|=(2k+1)/(2n-2k-1)\)
shows that the maximizers have the smallest degree \(|\ell-n|\), or its full complement. This proves the displayed formula for \(G_{\rm ML}\) and radial minimax optimality. The algebraic average over labels is not presented as a prior over legal physical oracles; the physical supremum was already fixed by the identity witness and the cross-effect lemma.

The two terms \(\ell=n\pm2\) alone imply
\[
 \Delta C_{\rm ML}\ge
 \frac{36n(n-1)}{(n+1)(n+2)}
 \left[\frac{\binom{2n-2}{n-1}}{nr}\right]^2
 \sim\frac{36}{\pi n^3}.
\]
The asymptotic is for this lower bound, not a claimed full expansion of the ML gain. Its value at \(n=21\) is \(0.00186722983634\), close to the complete gain \(0.00187357262152\).

Sampling ML is simple: translate \(R\) by the all-\(b\) subset. If its weight exceeds \(n\), remove a uniform subset of the excess occupied coordinates; if it is below \(n\), add a uniform subset of the missing coordinates. Translate back and identify antipodes. This is uniform over the nearest balanced labels and costs polynomial classical work plus a known Pauli operation. No new efficient implementation of the full protected-program measurement is claimed.

For the previous absolute-weight rule, define
\[
 Z_\ell^{(m)}=\tfrac12\sum_u\binom\ell u\binom{2n-\ell}{n-u}
             |a_{(\ell+n-2u)/2}|^m.
\]
Its **exact** gain parameter is
\(G_{\rm abs}=(2s)^{-1}\sum_{\ell\ {\rm odd},\ell\ne n}
\binom{2n}{\ell}Z_\ell^{(3)}/Z_\ell^{(1)}\), resolving the earlier gap between its certificate and its actual physical supremum.

## Verification, limitations and next step

Run `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_radial_twirl.py` (NumPy/SciPy). At \(n=3,5,7\), exact label enumeration checks all ML maximizing sets, equal gain on every balanced label and the closed formula. At physical \(n=3,5\), seven Hamiltonians each (identity, fields, edge Pauli, four seeded noncommuting cases) test both absolute-weight and ML recovery: 28 Choi eigenvector, residual-positivity, uniform-trace-effect and maximal-rank-one-subtraction checks. The verifier also reconstructs the signed Pauli expansion and checks that every radial shared-kernel component commutes with one noncommuting physical two-copy evolution at each size. Exact Fraction evaluations cover \(n=21,23,83\).

The small physical rings check dimension-independent identities, not first-order cancellation at those sizes. The long-ring statements rely on the cross-effect proof. The manuscript [Appendix B](https://arxiv.org/html/2506.20570v1) uses a broader random support-perturbation noise study; the common static parity-drift promise here is explicit and narrower. ML and channel-norm methods are not claimed as new primitives, and no literature-wide originality claim is made.

The next question is whether a non-radial or coherent data-program recovery can improve the identity-attained radial optimum. A useful first test is a finite optimization allowing degree/frame-dependent corrections while retaining the identity, field and edge constraints. Unrestricted six-query optimality and the physical pentagon six-versus-seven problem remain open.
