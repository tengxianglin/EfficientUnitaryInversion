# No-go for the fixed-parity rank-one spectral-collapse ansatz

## Scope

Let (N=2n) and let the cycle generator be
[
A(c)_{j,j+1}=2c_j,qquad A(c)_{j+1,j}=-2c_j
]
with cyclic indices. Write (R=e^{A(c)}), (D=operatorname{diag}(1,-1,ldots,1,-1)), and (Q=RD). The balanced-slice target is
[
	au_I=(-1)^rrac{inom nr}{inom{2n}{2r}},qquad |I|=2r.
]

The exact (N=4,6) constructions in `THEORY_PHYSICAL_CYCLE_ENSEMBLE_N4_N6.md` use alternating couplings and a particularly strong spectral collapse: the uniform parity-block mode has frequency (lambda=2(a-b)), while every nonuniform singular mode has an odd-integer multiple of (pi) as its frequency. This note proves that this *same rank-one spectral-collapse ansatz*, with the fixed even/odd cycle bipartition, cannot reproduce even the second-order target once (N\ge 8).

This is an ansatz-specific obstruction. It is **not** a no-go theorem for arbitrary alternating couplings, arbitrary cycle couplings, or mixtures of general physical cycle exponentials.

## Parity-block form

For alternating couplings (c_{2k}=a), (c_{2k+1}=b), order the even vertices before the odd vertices. Then
[
A=egin{pmatrix}0&B\\-B^T&0end{pmatrix},
qquad B=2(aI-bT),
]
where (T) is the cyclic shift on (n) sites. The matrix (B) is normal and the uniform vector (u=mathbf 1/sqrt n) is a singular mode with signed frequency
[
lambda=2(a-b).
]

Assume every nonuniform singular frequency is an odd multiple of (pi). On those modes, cosine is (-1) and sine is zero. On the uniform mode, set
[
gamma=1+coslambdain[0,2],qquad s=sinlambda.
]
The exponential blocks therefore collapse to
[
C=-I+gamma uu^T,qquad S=s,uu^T,
]
and
[
Q=RD=
egin{pmatrix}
-I+gamma uu^T&-suu^T\\
-suu^T&I-gamma uu^T
end{pmatrix}.
]

## All even principal minors in the ansatz

Take an even-cardinality subset (I) containing (p) even sites and (q) odd sites, with (p+q=2r). Let (U) be the (2n)-by-2 matrix whose columns are the indicators of the selected even and odd sites. Then
[
Q_{I,I}=
operatorname{diag}(-I_p,I_q)+rac1n U
egin{pmatrix}gamma&-s\\-s&-gammaend{pmatrix}U^T.
]
The matrix determinant lemma, together with (gamma^2+s^2=2gamma), gives the exact formula
[
oxed{
det Q_{I,I}
=(-1)^pleft(1-rac{2gamma r}{n}
+rac{2gamma pq}{n^2}ight).
}
]
Thus the minor depends only on the parity counts (p,q), not on the locations within each parity class.

For a two-site subset with both sites even (or both odd), (p=2,q=0,r=1), so
[
det Q_{I,I}=1-rac{2gamma}{n}.
]
The target at order two is (-1/(2n-1)). Matching it forces
[
gamma=rac{n^2}{2n-1},
qquad
coslambda=gamma-1=rac{(n-1)^2}{2n-1}.
]
Since a real (lambda) requires (coslambdale1), a necessary condition is
[
(n-1)^2le 2n-1
quadLongleftrightarrowquad
n^2-4n+2le0.
]
For integer (n\ge2), this is possible only for (n=2,3). At (n=4) the required value is (9/7>1), and it increases thereafter. In particular, at (N=42) ((n=21)) the ansatz would require
[
coslambda=rac{400}{41}>1,
]
which is impossible.

The same conclusion holds for any probability mixture supported entirely on this fixed-parity rank-one spectral-collapse class: every atom has (gammain[0,2]), while the order-two same-parity minor is affine in (gamma). Matching the target would require the mean (mathbb E[gamma]=n^2/(2n-1)>2) for (n\ge4).

## Relation to the exact (N=4,6) constructions

For (n=2), the required values are (gamma=4/3) and (coslambda=1/3). For (n=3), they are (gamma=9/5) and (coslambda=4/5). These are exactly the values used by the existing (N=4) and (N=6) constructions. Substituting them into the boxed formula verifies every even principal-minor order for those two sizes.

## What this does and does not establish

**Proved:** the fixed-parity, rank-one spectral-collapse construction used at (N=4,6), and every positive mixture confined to that class, cannot match the (N=2n\ge8) balanced-slice target even at second order.

**Not proved:** impossibility for general period-two couplings whose nonuniform modes do not all sit at odd multiples of (pi); impossibility for nonalternating cycle couplings; or impossibility for a positive measure over the full physical cycle-exponential family. Those remain the actual (N=42) convex-hull question in Issue #7.

The result is useful as a precise stopping rule: the (N=4,6) spectral-collapse trick cannot simply be extrapolated to (N=42). Any continuation must use non-collapsed Fourier modes, a genuinely nonuniform coupling pattern, or a broader multi-atom construction.
