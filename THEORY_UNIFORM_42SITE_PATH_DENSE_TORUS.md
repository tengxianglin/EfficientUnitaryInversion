# Exact dense-torus theorem for the uniform 42-site open path

## Theorem

Let \(K_*\in\mathbb R^{42\times42}\) be the skew-symmetric nearest-neighbour path generator with
\[
(K_*)_{j,j+1}=2,\qquad (K_*)_{j+1,j}=-2,\qquad j=0,\ldots,40,
\]
and all other entries zero. Then the positive-frequency vector of \(K_*\),
\[
\omega_k=4\cos(k\pi/43),\qquad k=1,\ldots,21,
\]
is linearly independent over \(\mathbb Q\). Consequently, for any real orthogonal canonical-form matrix \(Q\) satisfying
\[
Q^\mathsf T K_*Q=\bigoplus_{k=1}^{21}\omega_k J,\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\]
the positive-time orbit
\[
\left\{e^{tK_*}:t\ge0\right\}
\]
is dense in the conjugate maximal torus
\[
\left\{
Q\left(\bigoplus_{k=1}^{21}R(\theta_k)\right)Q^\mathsf T:
(\theta_1,\ldots,\theta_{21})\in\mathbb T^{21}
\right\},
\quad
R(\theta)=e^{\theta J}.
\]

In particular, for every continuous function \(F:SO(42)\to\mathbb R\),
\[
\sup_{t\ge0}F(e^{tK_*})
=
\max_{\theta\in\mathbb T^{21}}
F\!\left(Q\left(\bigoplus_{k=1}^{21}R(\theta_k)\right)Q^\mathsf T\right).
\]
The equality is a closure statement; it does not assert that every torus point is reached at a finite time.

## Proof

Let \(A_{42}\) be the ordinary adjacency matrix of the 42-vertex path and let \(D=\operatorname{diag}(1,i,i^2,\ldots,i^{41})\). Directly on each super- and subdiagonal entry,
\[
D^{-1}K_*D=2iA_{42}.
\]
The path adjacency eigenvalues are \(2\cos(k\pi/43)\), \(k=1,\ldots,42\). Hence the eigenvalues of \(K_*\) are
\[
4i\cos(k\pi/43),\qquad k=1,\ldots,42,
\]
giving the 21 positive frequencies stated above.

It remains to prove their rational linear independence. Put
\[
\zeta=e^{2\pi i/43},\qquad \eta=e^{\pi i/43}=-\zeta^{22}.
\]
Then
\[
2\cos(k\pi/43)
=\eta^k+\eta^{-k}
=(-1)^k(\zeta^{22k}+\zeta^{-22k}).
\]
Because 22 is invertible modulo 43, the residue pairs \(\{\pm22k\}\), \(k=1,\ldots,21\), run through all 21 nonzero pairs \(\{\pm m\}\) modulo 43. It is therefore enough to show that
\[
\zeta^m+\zeta^{-m},\qquad m=1,\ldots,21,
\]
are linearly independent over \(\mathbb Q\).

Suppose
\[
\sum_{m=1}^{21}b_m(\zeta^m+\zeta^{-m})=0,
\qquad b_m\in\mathbb Q.
\]
Multiplying by \(\zeta^{21}\) gives \(P(\zeta)=0\), where
\[
P(x)=\sum_{m=1}^{21}b_m(x^{m+21}+x^{21-m}).
\]
The degree of \(P\) is at most 42, and its coefficient of \(x^{21}\) is zero. The minimal polynomial of \(\zeta\) is
\[
\Phi_{43}(x)=1+x+\cdots+x^{42}.
\]
Thus \(P\) must be a rational multiple of \(\Phi_{43}\); comparison of the \(x^{21}\) coefficient forces that multiple to be zero. Hence \(P\equiv0\), and the distinct exponents \(0,\ldots,20,22,\ldots,42\) imply \(b_m=0\) for every \(m\). This proves rational independence of the frequencies.

By Kronecker's theorem, rational independence of \(\omega_1,\ldots,\omega_{21}\) makes
\[
t(\omega_1,\ldots,\omega_{21})\pmod{2\pi},\qquad t\ge0,
\]
dense in \(\mathbb T^{21}\). The real skew-symmetric canonical form then identifies the closure of \(e^{tK_*}\) with the stated conjugate maximal torus. Finally, continuity of \(F\) and compactness of the torus give the supremum/max equality.

## EUI consequence and exact limitation

The uniform positive coupling ray \(c(t)=(t,\ldots,t)\), \(t>0\), is an admissible one-dimensional subfamily of the 41-edge positive open-path family. Every normalized path-moment pricing functional used in the finite EUI design is continuous in \(R=e^K\), because its entries are finite sums/products of matrix entries or minors. Therefore its supremum along this single physical ray equals its maximum over the associated 21-torus.

This gives an exact reduction for testing a dual pricing functional on the uniform-coupling ray: optimize over 21 independent torus phases rather than over the unbounded scalar time parameter. It does **not** prove that a given EUI dual has positive maximum on that torus, does not control nonuniform coupling directions, and does not establish a full continuous-family minimax theorem or an operational Choi/diamond bound. A positive torus maximum would imply a finite positive-time escape by density and continuity; the present theorem alone does not assert that such a maximum is positive.
