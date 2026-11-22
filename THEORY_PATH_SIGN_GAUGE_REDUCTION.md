# Exact sign-gauge reduction for the 42-site path generator

## Generator

For $c=(c_0,\ldots,c_{40})\in\mathbb R^{41}$, the skew-symmetric path generator used by `rotation_entries_exact` is

$$
K(c)_{j,j+1}=2c_j,\qquad
K(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,
$$

with all other entries zero. Let $R(c)=e^{K(c)}$.

## Lemma

For every real coupling vector $c$, every principal minor of $R(c)$ is unchanged by replacing $c$ with its componentwise absolute value:

$$
\det R(c)_{I,I}=\det R(|c|)_{I,I}
\quad\text{for every }I\subseteq\{0,\ldots,41\}.
$$

Consequently, every feature used in the current moment LP—being a linear combination or orbit average of principal minors—is sign-invariant:

$$
a(c)=a(|c|).
$$

## Proof

Set $d_0=1$ and recursively choose $d_{j+1}=d_j s_j$, where $s_j=1$ if $c_j\ge0$ and $s_j=-1$ if $c_j<0$. Let

$$
D=\operatorname{diag}(d_0,\ldots,d_{41}).
$$

Then $D^2=I$. For every path edge,

$$
(DK(c)D)_{j,j+1}
=d_j(2c_j)d_{j+1}
=2|c_j|,
$$

and the lower-triangular entry is its negative. Hence

$$
DK(c)D=K(|c|).
$$

Conjugation commutes with the matrix exponential, so

$$
R(|c|)=e^{DK(c)D}=D R(c)D.
$$

For any index set $I$, the corresponding principal submatrix satisfies

$$
R(|c|)_{I,I}=D_I R(c)_{I,I}D_I.
$$

Taking determinants and using $D_I^2=I$ gives

$$
\det R(|c|)_{I,I}
=\det(D_I)^2\det R(c)_{I,I}
=\det R(c)_{I,I}.
$$

This proves the lemma.

## Consequence for the full-family extension

The continuous 41-parameter path family can be reduced from signed couplings to the nonnegative orthant without changing any principal-minor moment feature. For strictly nonzero couplings, the reduced domain is $(0,\infty)^{41}$; zero couplings follow by continuity.

This removes sign patterns as a source of new moment vectors, but it does **not** make the remaining magnitude domain finite or compact. The 1,641-column theorem therefore remains a finite-pool theorem. A genuine extension to the full path family still needs a global bound over positive coupling magnitudes (or an additional physically justified compact parameter range).
