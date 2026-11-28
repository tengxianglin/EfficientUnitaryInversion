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

The hypothesis needed below is exact pair matching, not merely a small
numerical pair residual. It is supplied by the frozen construction: the
37 exact-real weights are the unique solution of the 37-by-37 moment system
(the Arb determinant excludes zero); 30 independent pair-feature equations
are imposed exactly, the remaining cross-parity feature follows from the
row-norm identity, and period-two translation plus the equal one-site
symmetrization extends these equations to all 861 unordered pairs. The
256-bit verifier independently checks every pair coordinate and certifies
strict positivity of all 37 weights. Thus delta_2=0 exactly, and the
balanced-sign identity implies D_4 delta_4=0.

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
otherwise its interval square is included. In the final certificate, all
63,133 corrected intervals exclude zero, so no term is dropped and the
complete sixth-harmonic projection norm is enclosed.

The verifier also enumerates all 10,222 D42 orbits of five-subsets and checks
that the Arb interval for D_6 h contains zero on every orbit representative.
By D42 invariance this covers all 850,668 five-subsets. This is a direct
machine check of harmonicity, in addition to the operator derivation.

## 3. Certified N=42 result (Run 70)

At 256-bit Arb precision, the complete orbit computation gives
\[
\|h\|_2^2\in
[0.0459250490456842704146973544669054902195855549007702836745852313698437
\pm 7.09\times10^{-71}].
\]
All 63,133 six-subset orbit intervals are sign-definite; the orbit sizes sum
to all 5,245,786 six-subsets. The verifier evaluates 4,671,842 six-by-six
principal minors and checks all 10,222 five-subset orbit down relations.

With
\[
\lambda_6=\frac{7938048}{6724861},
\]
the complete degree-six contribution is
\[
\frac{\|h\|_2^2}{\lambda_6}
\in
[0.0389062363002099972720311172038350639683171901096527698802218018352923
\pm 7.31\times10^{-71}].
\]
This is at least 276,954.188 times the single-witness degree-six lower bound
from Run 69; the comparison is between certified contributions, not a claim
that the earlier witness was optimal.

Combining the independently certified degree-four floor with the complete
degree-six projection gives
\[
\boxed{
\chi^2(q\Vert u)>
0.1212616746890306412259819506806757844913171901096527698802218018352923.
}
\]
Using the complement-folded Plücker frame-potential identity from
[THEORY_COMPLEMENT_FOLDED_PLUCKER_FRAME_N42.md](THEORY_COMPLEMENT_FOLDED_PLUCKER_FRAME_N42.md),
\[
\boxed{
\operatorname{FP}>
8.332524077650208180211101200592596643935999786427223122225814449603037
\times10^{-12}.
}
\]
The ideal value is
\(7.431382223923010964580659670172348923453308318310907496251881494350739665140
\times10^{-12}\).

The machine certificate is
[evidence/n42_degree_six_harmonic_projection_arb.json](evidence/n42_degree_six_harmonic_projection_arb.json);
its orbit-residual digest is
7ce511ee2d4517fe3e3d80e15a73cc0df0b8a53c5ce42037179d7ba3111daa6f.
The full workflow passed:
[GitHub Actions run 46100133850](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46100133850).

These are degree-four plus degree-six lower bounds, not the full chi-square
divergence. They remain specific to the frozen 37-base / 74-labelled candidate.

## 4. Reproducibility and evidence

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

## 5. Interpretation boundary

The all-orbit calculation is for the frozen 37-base / 74-labelled candidate
only. A strict positive sixth-harmonic contribution quantitatively rejects
that candidate more strongly; it does not rule out another period-two measure,
a non-period-two physical measure, or the full continuous 42-cycle
exponential family.

The resulting chi-square lower bound is a program-label distribution
statement. It is not a Choi trace-distance or channel diamond-distance bound.
The global physical convex-hull question in Issue #7 and the operational
bridge tracked in Issue #5 remain open.
