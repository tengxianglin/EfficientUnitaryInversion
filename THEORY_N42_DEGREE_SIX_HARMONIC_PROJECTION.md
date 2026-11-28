# Full degree-six harmonic projection audit at N=42

Date: 2026-11-28. Run 70.

## Scope

This note upgrades Run 69's one explicit degree-six witness to a complete
D_42-orbit evaluation of the corrected sixth-order harmonic residual for the
same frozen 37-base / 74-labelled period-two candidate. It is still a
candidate-specific certificate, not a statement about every physical
cycle-exponential ensemble.

The balanced-slice harmonic decomposition itself is established prior work;
see Yuval Filmus, *An Orthogonal Basis for Functions over a Slice of the
Boolean Hypercube*, Electronic Journal of Combinatorics 23(1), 2016,
P1.23, DOI [10.37236/4567](https://doi.org/10.37236/4567),
[arXiv:1406.0142](https://arxiv.org/abs/1406.0142). The EUI-specific object
here is the exact lower-order correction for the sixth principal-minor
residual and its all-orbit interval evaluation.

## 1. Coordinate form of the sixth-harmonic projection

For an m-subset I of [42], let
\[
f_I(x)=\prod_{i\in I}x_i,\qquad
\delta_I^{(m)}=\mathbb E_q f_I-\mathbb E_u f_I,
\]
where u is uniform on the balanced slice and q is the frozen candidate's
complement-folded program-label law.

Use the down operator
\[
(D_m a)_J=\sum_{i\notin J}a_{J\cup\{i\}},
\qquad |J|=m-1.
\]
The exact balanced-sign identity gives
\[
D_4\delta_4=0,\qquad
D_6\delta_6=-D_5^T\delta_4.
\]
The Boolean-lattice commutator
\[
D_{k+1}D_{k+1}^T=D_k^TD_k+(42-2k)I
\]
then yields
\[
\delta_6^{\rm harm}
=\delta_6+\frac1{66}D_6^TD_5^T\delta_4.
\]

For a fixed six-set I, each four-set K contained in I occurs twice in
\((D_6^TD_5^T\delta_4)_I\), once for each ordering of the two removed
elements. Therefore the coordinate formula is
\[
\boxed{
h_I:=\delta_{6,I}^{\rm harm}
=\delta_{6,I}+\frac1{33}
\sum_{\substack{K\subset I\\|K|=4}}\delta_{4,K}.
}
\]
This is the exact harmonic projection, not a heuristic correction.

The balanced-slice Gram kernel acts on ker(D_6) as the scalar
\[
\lambda_6
=\sum_{j=0}^{6}(-1)^j\binom6j\mu_{2j}
=4^6\frac{\binom{30}{15}}{\binom{42}{21}}
=\frac{7938048}{6724861},
\]
where
\[
\mu_{2j}
=\mathbb E_u\prod_{r=1}^{2j}x_r
=\prod_{\ell=1}^{j}
-\frac{2\ell-1}{42-(2\ell-1)}.
\]

Since the degree-four and degree-six harmonic subspaces are orthogonal,
\[
\boxed{
\chi^2(q\Vert u)\ge
\frac{\|\delta_4\|_2^2}{\lambda_4}
+\frac{\|h\|_2^2}{\lambda_6}.
}
\]
The first term is the independently certified Run 68 quartic contribution.

## 2. Reduction to D42 orbits

The frozen ensemble averages each period-two atom with its one-site translate.
For every even principal-minor order, the resulting moment is invariant under
the dihedral group D42: translation exchanges the two phases, while reflection
acts by the corresponding site permutation and alternating diagonal gauge.
The correction map in the boxed coordinate formula is D42-equivariant.
Consequently h_I is constant on each D42 orbit of six-subsets.

There are exactly
\[
\binom{42}{6}=5,245,786
\]
six-subsets and 63,133 D42 orbits. The verifier enumerates canonical bit-mask
representatives using early-exit rotation/reflection comparisons, then checks
that the orbit sizes sum to 5,245,786.

For each representative I it:
1. evaluates the candidate sixth moment from 74 six-by-six principal minors
   (37 base atoms and 37 one-site translates);
2. obtains the 15 quartic submoments from the frozen 1,440-orbit Arb
   certificate;
3. forms h_I with the exact 1/33 correction;
4. multiplies h_I^2 by the exact D42 orbit size.

All arithmetic is outward-rounded at 256-bit Arb precision. If an h_I interval
contains zero, its nonnegative square is dropped from the lower-bound sum;
otherwise its interval square is included. Thus the reported sum is a rigorous
lower bound on the complete \|h\|_2^2 even if a few individual intervals are
too wide to certify a nonzero sign.

## 3. Reproducibility and evidence

Run:
python verify_n42_degree_six_harmonic_projection_arb.py

Pinned dependency:
python-flint==0.9.0.

The workflow first reruns the exact pair and all-quartic audits, then prices
all 63,133 sixth-order orbits and writes
evidence/n42_degree_six_harmonic_projection_arb.json. The certificate pins
SHA-256 hashes of the frozen atoms, exact-real weights, full quartic orbit
certificate, Run 68 quartic certificate, and Run 69 explicit-witness
certificate. It also records a digest over every orbit representative, orbit
size, and Arb harmonic-residual interval.

## 4. Interpretation boundary

The all-orbit calculation is for the frozen 37-base / 74-labelled candidate
only. A strict positive sixth-harmonic contribution quantitatively rejects
that candidate more strongly; it does not rule out another period-two measure,
a non-period-two physical measure, or the full continuous 42-cycle
exponential family.

The resulting chi-square lower bound is a program-label distribution
statement. It is not a Choi trace-distance or channel diamond-distance bound.
The global physical convex-hull question in Issue #7 and the operational
bridge tracked in Issue #5 remain open.
