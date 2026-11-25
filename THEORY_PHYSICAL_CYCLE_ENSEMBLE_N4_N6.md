# Exact physical cycle realizations of the complete balanced-slice target at N=4 and N=6

## Statement

For the even cycle \(N=2n\), define
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j,
\]
with cyclic indices, \(R=e^{A(c)}\), and
\[
D=\operatorname{diag}(1,-1,\ldots,1,-1),\qquad Q=RD.
\]
Because \(DAD=-A\), \(Q\) is a symmetric orthogonal involution. The balanced-slice target in these coordinates is
\[
\tau_I^{(Q)}
=(-1)^r\frac{\binom nr}{\binom{2n}{2r}},
\qquad |I|=2r.
\]

There is an exact **single physical cycle exponential** realizing every even principal-minor coordinate for \(N=4\) and \(N=6\). Thus the complete target is physically feasible at these two small sizes, not merely feasible over unrestricted \(SO(N)\).

## Block reduction

Order vertices by parity, with all even sites first and all odd sites second. Then
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix}.
\]
Writing
\[
C=\cos\sqrt{BB^T},\qquad
S=B\,\frac{\sin\sqrt{B^TB}}{\sqrt{B^TB}},
\]
the exponential and \(Q=RD\) are
\[
R=\begin{pmatrix}C&S\\-S^T&C_o\end{pmatrix},
\qquad
Q=\begin{pmatrix}C&-S\\-S^T&-C_o\end{pmatrix},
\]
where \(C_o=\cos\sqrt{B^TB}\). In both constructions below \(BB^T=B^TB\), so \(C_o=C\), and \(S=S^T\).

## N=4 construction

Let
\[
\theta_2=\arccos(1/3),\qquad
a_2=\frac{\pi+\theta_2}{4},\qquad
b_2=\frac{\pi-\theta_2}{4},
\]
and choose alternating cycle couplings
\[
(c_0,c_1,c_2,c_3)=(a_2,b_2,a_2,b_2).
\]
In parity order,
\[
B_2=2\begin{pmatrix}a_2&-b_2\\-b_2&a_2\end{pmatrix}.
\]
Its orthonormal modes \((1,1)/\sqrt2\) and \((1,-1)/\sqrt2\) have eigenvalues \(\theta_2\) and \(\pi\). Since \(\cos\theta_2=1/3\) and \(\sin\theta_2=2\sqrt2/3\),
\[
C_2=-I_2+\frac23J_2,\qquad
S_2=\frac{\sqrt2}{3}J_2.
\]
After returning to the interleaved site order,
\[
Q_4=\frac13
\begin{pmatrix}
-1&-\sqrt2&2&-\sqrt2\\
-\sqrt2&1&-\sqrt2&-2\\
2&-\sqrt2&-1&-\sqrt2\\
-\sqrt2&-2&-\sqrt2&1
\end{pmatrix}.
\]
Direct exact algebra gives \(Q_4^T=Q_4\), \(Q_4^2=I\), and \(\det Q_4=1\). Every one of the six two-site principal minors equals \(-1/3\), and the full determinant is \(+1\). These are exactly the target values for \(n=2\), at orders 2 and 4.

## N=6 construction

Let
\[
\theta_3=\arccos(4/5),\qquad d=\theta_3/2,
\]
\[
a_3=\frac{3d+\sqrt{3(\pi^2-d^2)}}{6},\qquad
b_3=a_3-d,
\]
and choose
\[
(c_0,\ldots,c_5)=(a_3,b_3,a_3,b_3,a_3,b_3).
\]
In parity order,
\[
B_3=2\begin{pmatrix}
a_3&0&-b_3\\
-b_3&a_3&0\\
0&-b_3&a_3
\end{pmatrix}.
\]
The exact parameter identities are
\[
2(a_3-b_3)=\theta_3,\qquad
a_3^2+a_3b_3+b_3^2=\frac{\pi^2}{4}.
\]
For \(u=(1,1,1)^T/\sqrt3\) and \(P=uu^T=J_3/3\),
\[
B_3B_3^T=B_3^TB_3
=\theta_3^2P+\pi^2(I-P),\qquad B_3u=\theta_3u.
\]
Using \(\cos\theta_3=4/5\), \(\sin\theta_3=3/5\), \(\cos\pi=-1\), and \(\sin\pi=0\), functional calculus gives
\[
C_3=-I_3+\frac35J_3,\qquad S_3=\frac15J_3.
\]
Thus, in the original interleaved site order,
\[
Q_6=\frac15
\begin{pmatrix}
-2&-1&3&-1&3&-1\\
-1&2&-1&-3&-1&-3\\
3&-1&-2&-1&3&-1\\
-1&-3&-1&2&-1&-3\\
3&-1&3&-1&-2&-1\\
-1&-3&-1&-3&-1&2
\end{pmatrix}.
\]
Exact algebra gives \(Q_6^T=Q_6\), \(Q_6^2=I\), and \(\det Q_6=-1\). Exhaustive exact principal-minor evaluation gives:
- all 15 two-site minors equal \(-1/5\);
- all 15 four-site minors equal \(+1/5\);
- the six-site determinant equals \(-1\).

These are exactly the target values for \(n=3\) at every even order 2, 4, and 6. A single physical cycle exponential therefore realizes the complete target.

## Consequence and limitation

The perfect-matching \(SO(42)\) ensemble is not the only possible representation of the balanced-slice moments. The N=4 and N=6 constructions demonstrate explicitly why excluding individual matching atoms cannot settle physical convex-hull membership: a non-permutation physical exponential can realize the same full moment hierarchy at small sizes.

These constructions do **not** establish feasibility at \(N=42\). The two-parameter alternating-coupling spectral degeneracy used above is special to \(n=2,3\); the 21-site parity block at \(N=42\) has many distinct Fourier modes. No N=42 positive physical ensemble or global converse is claimed.

## Exact verification

- Verifier: verify_physical_cycle_ensemble_n4_n6.py
- Evidence: evidence/physical_cycle_ensemble_n4_n6.json
- Workflow: .github/workflows/eui-physical-cycle-ensemble-n4-n6.yml

The verifier uses exact symbolic arithmetic for the spectral identities, all principal minors, orthogonality, determinant, and chiral relation. Decimal coupling values are included only as human-readable diagnostics.
