# Universal pair–quartic principal-minor incidence identity

## Motivation and correction

An attempted Run-59 separator based on the sum of all fourth-order principal minors containing a fixed pair was rejected by its first Arb regression. The proposed 2x2-block Desnanot–Jacobi shortcut was invalid: for disjoint 2-subsets I,J, the determinant of the 4x4 block matrix is not simply the product of the two diagonal-block determinants minus the product of the cross-block determinants.

The correct identity below is universal for every real symmetric involution of balanced signature. It is therefore **not** a period-two obstruction. Its value is structural: it gives exact linear dependencies between the pair and quartic moment coordinates and provides a strong implementation consistency check.

## Theorem

Let Q be a real symmetric involution of size 2n with trace zero. Fix a two-subset I and write T=Q_{I,I}. Then
\[
\boxed{
\sum_{J\in\binom{I^c}{2}}\det Q_{I\cup J,I\cup J}
=1-(n-2)\det T.
}
\tag{1}
\]

No invertibility assumption is needed in the statement.

### Proof on a dense open set

Order the coordinates as I followed by I^c and write
\[
Q=\begin{pmatrix}T&X\\X^T&B\end{pmatrix},
\qquad m=2n-2.
\]
Assume temporarily that T and I_2-T^2 are invertible. The block equations from Q^2=I give
\[
T^2+XX^T=I_2,\qquad
TX+XB=0,\qquad
X^TX+B^2=I_m.
\]
Thus X has rank two. The subspace range(X^T) is B-invariant, and
\[
BX^T=-X^TT,
\]
so B restricted to range(X^T) is similar to -T. On ker(X), the last block equation gives B^2=I. Since Q and T have trace zero only in the special case tr(T)=0, we keep t=tr(T) general: tr(B)=-t, while the trace of B on range(X^T) is -t. Hence the restriction of B to ker(X) has trace zero. Its eigenvalues are therefore equally many +1 and -1.

Consequently
\[
\operatorname{tr}(B^{-1})=-\operatorname{tr}(T^{-1})=-\frac{t}{p},
\]
\[
\operatorname{tr}(B^{-2})
=\operatorname{tr}(T^{-2})+(2n-4)
=\frac{t^2}{p^2}-\frac2p+2n-4,
\]
where p=det(T). Therefore
\[
e_2(B^{-1})
=\frac{(\operatorname{tr}B^{-1})^2-\operatorname{tr}(B^{-2})}{2}
=\frac1p-(n-2).
\tag{2}
\]

Now consider
\[
M(z)=\begin{pmatrix}zT&zX\\zX^T&I_m+zB\end{pmatrix}.
\]
By the principal-minor expansion of a determinant, the coefficient of z^4 in det M(z) is exactly the left side of (1): setting the two diagonal entries indexed by I to zero forces every selected principal-minor index set to contain I.

The Schur complement of zT gives
\[
\det M(z)
=z^2p\det\bigl(I_m+z(B-X^TT^{-1}X)\bigr).
\]
Because Q^{-1}=Q, the lower-right block of the block inverse formula implies
\[
(B-X^TT^{-1}X)^{-1}=B,
\]
so B-X^TT^{-1}X=B^{-1}. The coefficient of z^4 is therefore p e_2(B^{-1}). Using (2), it equals
\[
p\left(\frac1p-(n-2)\right)=1-(n-2)p.
\]
This proves (1) on the dense open set. Both sides are polynomial in the entries of Q, so continuity extends the identity to every symmetric involution, including singular T or B. \(\square\)

## Consequence for the N=42 balanced target

In the repository convention Q=RD, the complete balanced-slice target has
\[
\tau_I^{(2)}=-\frac1{41},\qquad
\tau_K^{(4)}=\frac1{533}.
\]
For any fixed pair I, there are \(\binom{40}{2}=780\) four-subsets containing it. Their target sum is
\[
780\cdot\frac1{533}=\frac{60}{41}
=1-19\left(-\frac1{41}\right).
\]
Thus the balanced target satisfies (1) exactly. The incidence sum cannot separate the physical family; it is already forced by the symmetric-involution geometry shared by every physical atom.

Equivalently, for every pair I,
\[
\boxed{
\sum_{J\in\binom{I^c}{2}}m_{I\cup J}^{(4)}
+19m_I^{(2)}=1.
}
\tag{3}
\]
These are universal affine dependencies between the pair and quartic feature coordinates, not additional physical constraints.

## Scope and research value

- The identity applies to every Q with Q^T=Q, Q^2=I, tr(Q)=0; it is independent of period-two symmetry, coupling signs, and the nearest-neighbour graph.
- It does not prove or disprove existence of a positive physical ensemble.
- It does not imply a Choi trace-distance or channel diamond-distance bound.
- For future LPs, the 861 pair-indexed incidence relations can be used to detect redundant quartic equations and to check target-vector construction.
- The Run-59 attempted no-go based on the incorrect coefficient 21 is withdrawn. The correct coefficient is n-2=19 for N=42.
- The accompanying Arb script directly sums all 780 incident quartic minors for frozen rational period-two samples and checks (1). These finite checks are regression evidence; the proof is the block-matrix argument above.
