# A coefficient-projection test on 21 physical pentagon tori

The open question is whether the fully fielded Ising pentagon admits deterministic exact inversion with six forward queries and zero linear response to common parity drift. The [independent Gaussian-group converse](THEORY_ODD_CYCLE_GAUSSIAN_GROUP_DRIFT.md) uses an alternate-lift projection with squared norm at most \(65/128\). Can a finite ensemble of [physically reachable tori](THEORY_ODD_CYCLE_PHYSICAL_ROOT_TORI.md) give a coefficient-projection bound below the required \(3/4\)?

**Exact result for the specified ensemble.** For the inverse-spinor Bell spectator, the two-query alternate coefficient space retains at least \(19/25=0.76\) of the ideal squared norm under the equal-weight average of the 21 tori defined below. The certified polynomial gives \(0.763899784673\ldots\). A finite floating-point evaluation estimates the full projected fraction as \(0.912244764890\) on this same ensemble. The exact witness rules out a proof of a bound below \(3/4\) using this average and the alternate coefficient space alone. The physical six-query feasibility question remains open. The witness is an approximation by matrix-coefficient functions and does not impose pointwise Stinespring normalization or the causal realization constraints.

## Physical tori and the projection

Fix the plus sector of dimension \(D=16\). Its field-basis weights \(w\) are the length-five sign rows with even parity, i.e. all \(w\in\{\pm1\}^5\) with \(\prod_i w_i=+1\). Take the field basis and one rotated basis for each of the ten unordered site pairs and each of the two occupation types, equal and opposite. The spinor rotation in each affected two-dimensional block has cosine \(3/5\) and sine \(4/5\). In field-basis coordinates its hopping sign is \(\prod_{i<k<j}w_k\), from the Majorana string between sites \(i,j\). The particle–hole rotation follows by flipping one endpoint, leaving this sign unchanged up to an overall angle sign. The minus basis is fixed. Choose each of the 21 bases uniformly and use normalized torus measure in each.

The spectator is \(v(U)=\operatorname{vec}(\bar U_+)/\sqrt{D}\), as in the [six-query split construction](THEORY_ODD_CYCLE_SIX_QUERY_RECOVERY.md). On plus data the ideal amplitude has the matrix entries of \(\bar U_+^{\otimes2}\) divided by \(\sqrt D\). The preferred lift has six plus calls and the alternate has two plus and four minus calls. The alternate coefficient space consists of the span of entries of \(U_+^{\otimes2}\) times coefficients from the four minus queries. In the chosen ensemble the minus phase torus is independent and its four-query coefficients include the constant function. Equivalently, four minus weights can sum to zero. Since the target amplitude is constant in the minus variables, only that constant component enters its orthogonal projection. There is no alternate lift on minus data for this spectator character. After averaging the \(D\) plus inputs, the projected fraction is therefore the squared Hilbert–Schmidt norm of the projection of \(\bar U_+^{\otimes2}\) onto the span of entries of \(U_+^{\otimes2}\), normalized by \(D^2\).

The alternate coefficient space in this calculation uses a single set of polynomial coefficients across all 21 tori. Thus it already enforces the common-oracle equalities on their intersections. Parseval across the phase tori reduces the calculation to a real matrix projection. For a chosen basis \(R_i\), let
\[
 P_{i,\nu}
 =(R_i\otimes R_i)
  \left(\sum_{w+w'=\nu}|w,w'\rangle\langle w,w'|\right)
  (R_i\otimes R_i)^{\mathsf T}.
\]
These are the Fourier coefficient matrices of \(U_+^{\otimes2}\), with the negative-frequency matrices \(P_{i,-\nu}\) for the inverse square. Include rows for \(\nu\) in the union of query and target frequencies, taking absent projectors as zero. Let \(A\) and \(B\) be the matrix arrays with rows \(\operatorname{vec}(P_{i,\nu})^{\mathsf T}\) and \(\operatorname{vec}(P_{i,-\nu})^{\mathsf T}\). Up to the common weighting, the projected fraction is
\[
 \mathcal F=\frac{\|\operatorname{Proj}_{\operatorname{col}(A)}B\|_F^2}{\|B\|_F^2}.
\]
The Gram matrices \(G=5^8AA^{\mathsf T}\) and \(H=5^8BB^{\mathsf T}\) are integer matrices of size 2,562. The entries of \(G\) are computed by aggregating squared two-copy overlaps of the rotated occupation states. The target Gram \(H\) is \(G\) with the character labels in each basis negated. In particular \(\operatorname{Tr}H=21D^2\,5^8\).

## Exact polynomial witness

Put \(L=\max_i\sum_j G_{ij}\), \(Z=G/L\), and \(p(z)=34z-244z^2+506z^3-316z^4\). The columns of \(p(Z)B\) are in \(\operatorname{col}(A)\) because \(p(0)=0\) and \(G\) has that column space. The least-squares variational identity gives
\[
 \mathcal F\ \ge\ 
 \frac{2\operatorname{Tr}[p(Z)H]-\operatorname{Tr}[p(Z)^2H]}{\operatorname{Tr}H}.
\]
The right-hand side is rational. The [verifier](verify_ising_pentagon_root_projection.py) computes the eight integer moments \(\operatorname{Tr}(G^kH)\) using modular products and Chinese remaindering. It uses \(0\le\operatorname{Tr}(G^kH)\le L^k\operatorname{Tr}H\), from positivity and the maximum row-sum bound. Every binary64 product used for modular matrix multiplication is an integer dot product of nonnegative residues whose total is strictly below \(2^{53}\). The verifier checks that bound at every modulus. The returned bound is certified by exact rational comparison with \(19/25\), independent of any eigensolver or singular-value cutoff.

Run from the repository root with NumPy and SymPy:
~~~bash
OPENBLAS_NUM_THREADS=4 python verify_ising_pentagon_root_projection.py
~~~
For the separate floating estimate, use SciPy to diagonalize \(G/5^8\), retain eigenvalues above \(10^{-9}\), and evaluate \(\operatorname{Tr}(Q^{\mathsf T} H Q)/\operatorname{Tr}H\) with the retained eigenvectors \(Q\). This yielded numerical rank 1,026 with smallest retained eigenvalue \(0.88803157\ldots\).

The measured projection is only one condition. The next test is to retain the coefficient-wise isometry identities from \(V_\epsilon(z)^\dagger V_\epsilon(z)=I\), alongside the common-face equations, rather than averaging away all nonzero characters. On the central phase face, charge and input labels can be fixed first, and orthogonality can be checked for the degree-six coefficient blocks before imposing full causality. An alternative ensemble with additional physically reachable bases may also reduce the projection. The \(31/16\) linear-coefficient lower bound for independent Gaussian sectors and its fixed-parallel-encoder corollary remain as previously proved.

The [EUI manuscript and robustness appendix](https://arxiv.org/html/2506.20570v1) give the inversion and systematic-error setting. [Odake, Yoshida and Murao](https://doi.org/10.1103/drp2-rzzw) study differentiated query bounds for group promises. The calculation here tests a specific step in transferring a bound from the Gaussian-group promise to physical cyclic Ising exponentials.
