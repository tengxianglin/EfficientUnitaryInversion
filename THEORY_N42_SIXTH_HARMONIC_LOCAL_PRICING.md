# Local pricing oracle for the N=42 sixth-harmonic coordinate

Date: 2026-11-28. Run 71.

## Result and scope

Run 70 computed the complete sixth-harmonic projection of one frozen
37-base/74-labelled period-two candidate. This note derives a different,
candidate-independent tool: **any one coordinate of the sixth-harmonic
projection can be priced on an arbitrary physical cycle atom using only 32
principal minors on a fixed six-site set**. No period-two assumption is used
in the theorem.

Let
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j
\]
on the 42-cycle, let
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\quad
R(c)=e^{A(c)},\quad Q(c)=R(c)D.
\]
Because the cycle is bipartite, \(DAD=-A\). Hence
\[
Q(c)^T=Q(c),\qquad Q(c)^2=I,
\]
and \(Q(c)\) is conjugate to \(D\). It has 21 eigenvalues \(+1\) and 21
eigenvalues \(-1\), for every real coupling vector \(c\). In particular,
\[
\det(I+zQ(c))=(1-z^2)^{21}.
\]

For a six-set \(J\), write \(v_J(Q)=\det Q_{J,J}\). Under the uniform
balanced-slice target \(u\), the degree-\(2r\) character moment is
\[
\mu_{2r}=\mathbb E_u f_I
=(-1)^r\frac{\binom{21}{r}}{\binom{42}{2r}},
\qquad |I|=2r.
\]
Thus
\[
\mu_0=1,\quad \mu_2=-\frac1{41},\quad
\mu_4=\frac1{533},\quad \mu_6=-\frac5{19721}.
\]

## Theorem: one-coordinate sixth-harmonic witness

Let \(D_6:C_6\to C_5\) be the down operator
\[
(D_6a)_K=\sum_{i\notin K}a_{K\cup\{i\}},
\]
and let \(\mathcal H_6=\ker D_6\). Let \(P_6\) be the orthogonal projector
onto \(\mathcal H_6\). For a fixed six-set \(S\), define
\[
a^{(S)}=P_6e_S.
\]
Then \(a^{(S)}_J\) depends only on \(t=|J\cap S|\), with
\[
a^{(S)}_J=p_t,\qquad
p_t=\frac{31}{37}\frac{(-1)^{6-t}}{\binom{36}{6-t}},
\quad t=0,\ldots,6.
\]
In particular,
\[
\|a^{(S)}\|_2^2=a^{(S)}_S=\frac{31}{37}.
\]

For every real 42-cycle coupling vector \(c\), define
\[
\boxed{
W_S(Q(c))=
\det Q(c)_{S,S}
+\frac1{33}\sum_{\substack{K\subset S\\|K|=4}}\det Q(c)_{K,K}
+\frac1{385}\sum_{\substack{K\subset S\\|K|=2}}\det Q(c)_{K,K}
+\frac1{2849}.
}
\]
Then
\[
\boxed{
W_S(Q)=\sum_{|J|=6}a^{(S)}_J\det Q_{J,J}.
}
\]
Consequently \(W_S\) is a pure degree-six harmonic witness: its expectation
under the balanced-slice target is exactly zero. For any program-label law
\(q\) induced by a probability measure over physical cycle atoms,
\[
\mathbb E_q W_S
=\bigl(P_6\delta_6\bigr)_S,
\]
where \(\delta_6\) is the degree-six principal-minor residual.

The balanced-slice Gram operator acts on \(\mathcal H_6\) as
\[
\lambda_6=\frac{7938048}{6724861}.
\]
Therefore the one-coordinate chi-square bound is
\[
\boxed{
\chi^2(q\Vert u)\ge
\frac{8026447}{7938048}
\left(\mathbb E_q W_S\right)^2.
}
\]
This is a valid candidate-specific lower bound for every chosen \(S\), and a
continuous pricing objective on the entire physical cycle family.

## Proof

### 1. Exact harmonic projection coefficients

The stabilizer of \(S\) in the symmetric group acts transitively on six-sets
with a fixed value of \(|J\cap S|\). Thus \(a^{(S)}_J=p_t\). For a five-set
\(K\) with \(|K\cap S|=t\), the equation \(D_6a^{(S)}=0\) is
\[
(6-t)p_{t+1}+(31+t)p_t=0.
\]
The diagonal entry of the orthogonal projector is constant by permutation
symmetry and equals
\[
(P_6)_{S,S}
=\frac{\dim\mathcal H_6}{\binom{42}{6}}
=1-\frac{\binom{42}{5}}{\binom{42}{6}}
=\frac{31}{37}.
\]
Solving the recurrence backwards from \(p_6=31/37\) gives the displayed
formula for \(p_t\). Since \(P_6\) is an orthogonal projector,
\(\|P_6e_S\|^2=e_S^TP_6e_S=p_6=31/37\).

Its Newton expansion is
\[
p_t=\sum_{k=0}^{t}\binom tk\alpha_k,\qquad
\alpha_k=\frac{(-1)^k}{\binom{37-k}{6-k}}.
\]

### 2. Price the incidence sums using only minors inside S

For \(K\subseteq[42]\), \(|K|=k\), put
\[
F_K(Q)=\sum_{\substack{J\supseteq K\\|J|=6}}\det Q_{J,J}.
\]
The principal-minor generating identity is
\[
\sum_{J\supseteq K}z^{|J|}\det Q_{J,J}
=\det(I+zQ)\,
\det\!\left[zQ(I+zQ)^{-1}\right]_{K,K}.
\]
For a symmetric involution with 21 eigenvalues of each sign,
\[
zQ(I+zQ)^{-1}=\frac{z(Q-zI)}{1-z^2},
\]
so
\[
F_K(Q)=[z^6]\,
z^k(1-z^2)^{21-k}\det(Q_{K,K}-zI_k).
\]
Now
\[
\sum_{|J|=6}p_{|J\cap S|}\det Q_{J,J}
=\sum_{k=0}^6\alpha_k
\sum_{\substack{K\subseteq S\\|K|=k}}F_K(Q).
\]
Expanding the coefficient above and collecting the terms indexed by
\(L\subseteq S\) gives the following exact coefficients:

| \(|L|\) | coefficient of \(\det Q_{L,L}\) |
|---:|---:|
| 0 | \(1/2849\) |
| 2 | \(1/385\) |
| 4 | \(1/33\) |
| 6 | \(1\) |

This is precisely the boxed 32-minor formula for \(W_S\). It requires one
six-minor, fifteen four-minors, fifteen two-minors, and the constant term.

### 3. Target mean and chi-square variance

The target mean vanishes exactly:
\[
\mu_6+\frac{15}{33}\mu_4
+\frac{15}{385}\mu_2+\frac1{2849}=0.
\]
Thus \(W_S\) is centered under \(u\). Since its coefficient vector is
\(a^{(S)}\in\mathcal H_6\), the balanced-slice Gram eigenvalue gives
\[
\mathbb E_u W_S^2
=\lambda_6\|a^{(S)}\|^2
=\frac{7938048}{6724861}\frac{31}{37}
=\frac{7938048}{8026447}.
\]
Cauchy--Schwarz applied to
\(\mathbb E_qW_S-\mathbb E_uW_S\) proves the chi-square inequality.

## Why this is useful for the next physical search

The full Run 70 projection has 5,245,786 coordinates. A single coordinate
\(S\) of that projection can now be evaluated on **any** physical cycle atom
from only 32 minors contained in \(S\). This gives a cheap, exact-form
pricing function for non-period-two coupling searches. One can select a
large-residual orbit from the Run 70 certificate, optimize \(W_S(Q(c))\)
over all 42 real couplings, and independently interval-certify any proposed
escape.

The formula is not a global separator. A positive or negative value at one
atom can be cancelled by a mixture, and this note does not exclude the
continuous physical convex hull. It also does not imply a Choi or diamond
distance bound. The general slice-harmonic decomposition is established
prior
work; the EUI-specific result is the compact local pricing identity for the
cycle involution.


## A fully connected positive-cycle escape for one local coordinate

The local oracle also exposes why it must not be promoted to a global
separator. For the first probe \(S=\{0,1,2,3,4,5\}\), the frozen Run 70
candidate has the 256-bit Arb-certified coordinate
\[
(P_6\delta_6)_S
\in[-0.000604644388181486443843770485452175730900398725814867757300154235939399
\pm4.37\times10^{-73}]<0.
\]

There is a physical atom with the opposite sign and with **all 42 cycle
couplings strictly positive**. Start from the standard length-42
perfect-transfer path couplings
\[
c_j^*=\frac{\pi}{4}\sqrt{(j+1)(41-j)},\quad j=0,\ldots,40,
\qquad c_{41}^*=0.
\]
The path spin-chain identity gives
\(R^*|j\rangle=(-1)^j|41-j\rangle\), so \(Q^*=R^*D\) is minus the reversal
permutation. No pair \(\{j,41-j\}\) lies wholly inside \(S\). Hence every
nonempty even principal minor of \(Q^*\) on a subset of \(S\) vanishes and
\[
W_S(Q^*)=\frac1{2849}>0.
\]

Now open the closing edge by \(\varepsilon=10^{-6}\), keeping all other
couplings fixed. The new atom has all 42 couplings strictly positive. The
generator perturbation has operator norm \(2\varepsilon\). Duhamel's identity
for skew-symmetric generators gives
\(\|Q-Q^*\|_2\le2\varepsilon\). For a \(k\)-minor of orthogonal matrices,
determinant multilinearity and Hadamard's inequality give a change at most
\(k\|Q-Q^*\|_2\). Therefore
\[
|W_S(Q)-W_S(Q^*)|
\le2\varepsilon\left(6+\frac{60}{33}+\frac{30}{385}\right)
=\frac{1216}{77}\varepsilon<16\varepsilon.
\]
Consequently
\[
\boxed{
W_S(Q)>
\frac1{2849}-\frac{1216}{77\cdot10^6}
=\frac{14922}{44515625}>0.
}
\]

Thus a strictly positive, non-period-two physical cycle atom has the
opposite sign to the frozen candidate on this one harmonic coordinate. A
unique convex reweighting of these two laws can cancel this coordinate.
It does **not** match the remaining coordinates and is not a solution of the
full moment problem. The perfect-transfer primitive is standard (Christandl
et al., Phys. Rev. Lett. 92, 187902 (2004)); the EUI-specific point is the
local-witness pricing and the explicit positive-cycle escape bound.

## Exact checks

The dependency-free exact verifier checks the projection, variance, target
centering, and local-minor identity using rational arithmetic for small
balanced involutions. The N=42 Arb verifier compares the 32-minor pricing
formula against the Run 70 full-projection coordinate formula on frozen
candidate probes.
