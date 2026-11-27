# N=42 period-two no-go from a complete fourth-order incidence sum

## Result

This note gives a continuum theorem for the period-two subfamily of the 42-cycle physical model. It is stronger than a support-specific missing-orbit check: it excludes **every probability measure**, with arbitrary support size, over all real period-two couplings from matching the complete second- and fourth-order balanced-slice principal-minor targets simultaneously.

Use the repository convention
\[
A(c)_{j,j+1}=2c_j,\qquad A(c)_{j+1,j}=-2c_j,
\qquad R=e^{A(c)},\qquad D=\operatorname{diag}(1,-1,\ldots),\qquad Q=RD.
\]
For N=42, the target in Q coordinates is
\[
\tau_I^{(2)}=-\frac1{41},\qquad
\tau_K^{(4)}=\frac1{533}
\]
for every two-subset I and four-subset K.

## Theorem 1 — incidence identity for symmetric involutions

Let Q be a real symmetric involution of size 2n with trace zero. Fix a two-subset I and put T=Q_{I,I}. Then
\[
\boxed{
\sum_{J\in\binom{I^c}{2}}\det Q_{I\cup J,I\cup J}
=(\operatorname{tr}T)^2-n\det T-1.
}
\tag{1}
\]

### Proof

Order coordinates as I followed by I^c and write
\[
Q=\begin{pmatrix}T&C^T\\ C&B\end{pmatrix}.
\]
The equations Q^2=I and tr Q=0 imply
\[
T^2+C^TC=I_2,\quad B^2+CC^T=I_{2n-2},\quad
\operatorname{tr}B=-\operatorname{tr}T.
\]
Writing p=det T and t=tr T, we obtain
\[
\sum_{J\in\binom{I^c}{2}}\det B_{J,J}
=\frac{(\operatorname{tr}B)^2-\operatorname{tr}(B^2)}2
=p-(n-2).
\]
For each J, the Desnanot–Jacobi identity gives
\[
\det Q_{I\cup J,I\cup J}
=p\det B_{J,J}-\det(Q_{I,J})^2,
\]
where symmetry of Q makes the two cross determinants equal. Cauchy–Binet and T^2+C^TC=I give
\[
\sum_J\det(Q_{I,J})^2
=\det(CC^T)=\det(I_2-T^2)
=1-t^2+2p+p^2.
\]
Summing the Desnanot–Jacobi identity therefore yields
\[
p[p-(n-2)]-[1-t^2+2p+p^2]
=t^2-np-1,
\]
which is (1). No invertibility assumption on T or B is used. \(\square\)

## Theorem 2 — every period-two 42-cycle mixture is excluded

Let N=42=2n with n=21 and take period-two couplings
\[
c_{2j}=a,\qquad c_{2j+1}=b,\qquad a,b\in\mathbb R.
\]
For I={0,1}, every resulting Q satisfies
\[
\operatorname{tr}Q_{I,I}=Q_{00}+Q_{11}=0.
\tag{2}
\]

To see this, reorder the one-particle basis into even and odd sites. The generator has block form
\[
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},
\]
where B is circulant (a linear combination of the identity and a cyclic shift), hence normal: BB^T=B^TB. The two diagonal blocks of e^A are consequently the same matrix \(\cos\sqrt{BB^T}\), which is circulant and has a constant diagonal \(\gamma\). Thus R_{2j,2j}=R_{2j+1,2j+1}=\gamma; multiplication by D gives Q_{00}=\gamma and Q_{11}=-\gamma. This proves (2) for all real a,b, including zero or negative couplings.

Since Q is a symmetric involution with trace zero, Theorem 1 and (2) imply, for every period-two atom,
\[
\sum_{J\in\binom{\{2,\ldots,41\}}2}
\det Q_{\{0,1\}\cup J,\{0,1\}\cup J}
=-21\det Q_{\{0,1\},\{0,1\}}-1.
\tag{3}
\]
The identity is affine in the moment coordinates, so it also holds for every probability mixture over the continuous (a,b) family, with no restriction on support size.

There are \(\binom{40}{2}=780\) four-subsets containing I={0,1}. The balanced target evaluates the left side of (3) to
\[
\frac{780}{533}=\frac{60}{41},
\]
while the right side, after inserting the target pair moment -1/41, equals
\[
-21\left(-\frac1{41}\right)-1=-\frac{20}{41}.
\]
The mismatch is exactly 80/41. Hence:

**No-go.** No positive probability measure over period-two 42-cycle Hamiltonians can match all 861 second-order and all 111,930 fourth-order principal-minor coordinates of the balanced-slice target simultaneously.

## Quantitative separation

Define the linear functional on the complete pair/fourth-moment vector
\[
L(m)=21m_{\{0,1\}}^{(2)}
+\sum_{J\in\binom{\{2,\ldots,41\}}2}
m_{\{0,1\}\cup J}^{(4)}.
\]
Every period-two mixture has L(m)=-1, whereas L(\tau)=39/41. Its coefficient \(\ell_1\)-norm is 21+780=801. Therefore
\[
\boxed{
\|m-\tau\|_\infty\ge
\frac{80}{41\cdot801}=\frac{80}{32841}.
}
\tag{4}
\]
If all pair coordinates are matched exactly, (3) further implies that at least one of the 780 quartic coordinates containing {0,1} undershoots its target by at least
\[
\boxed{\frac{80/41}{780}=\frac4{1599}.}
\tag{5}
\]

## Necessary condition for leaving period two

For a general physical atom, (1) still holds, but t=Q_{00}+Q_{11}=R_{00}-R_{11} need not vanish. Any ensemble matching the complete pair and fourth-order target must satisfy
\[
\boxed{
\mathbb E[(R_{00}-R_{11})^2]=\frac{80}{41}.
}
\tag{6}
\]
Thus a successful full physical ensemble must have substantial atom-to-atom diagonal imbalance on this adjacent even/odd pair. Equation (6) is a useful constraint for non-period-two searches; it is not yet a construction or a no-go for the unrestricted cycle family.

## Relation to the ten-orbit partial ensemble

The 82-atom Run-58 ensemble remains valid: it matches all 861 pair coordinates and 399 quartic coordinates in ten specified translation orbits. The theorem explains why that period-two construction cannot be extended to all quartic coordinates merely by adding more period-two atoms. It does **not** invalidate any of the 399 certified coordinates and does not rule out non-period-two cycle couplings.

## Reproducibility and scope

- `verify_n42_period_two_all_quartic_no_go_arb.py` checks the Fourier reconstruction against Q symmetry/involution/trace identities and directly sums all 780 quartic minors for frozen exact-rational (a,b) samples at 256-bit Arb precision.
- The finite Arb samples are regression checks. The continuum no-go is the exact block-circulant argument plus Theorem 1.
- No Choi trace-distance or channel diamond-distance claim follows from this moment-space separator.
