# Degree-six harmonic projection and an explicit N=42 witness

Date: 2026-11-28. Run 69. This note extends the degree-four balanced-slice
certificate without incorrectly treating raw sixth-order residuals as
harmonic.

## Scope and relation to prior work

The frozen candidate is the 37-base / 74-labelled period-two ensemble in
evidence/n42_period_two_six_quartic_atoms.json. It exactly matches all
861 pair moments but fails many quartic moments. Run 68 established the
optimal degree-four contribution
\[
\chi^2(q\Vert u)\ge
\frac{\|\delta_4\|_2^2}{\lambda_4}
>0.0823554383888206439539508334768407,
\qquad
\lambda_4=\frac{21888}{19721}.
\]

The harmonic decomposition on a fixed Hamming slice / Johnson scheme is
standard; see Yuval Filmus, *An Orthogonal Basis for Functions over a Slice
of the Boolean Hypercube*, Electronic Journal of Combinatorics 23(1), 2016,
P1.23, DOI [10.37236/4567](https://doi.org/10.37236/4567), and
[arXiv:1406.0142](https://arxiv.org/abs/1406.0142). The contribution here is
the explicit lower-order correction for the EUI sixth-principal-minor
residual and its use in a certified physical-ensemble witness, not a claim
to have introduced slice harmonic analysis.

## 1. Down/up operators

Let \(\Omega_{N,n}=\{x\in\{-1,1\}^N:\sum_i x_i=0\}\), with uniform law
\(u\), where \(N=2n\). For an \(m\)-subset \(I\), write
\[
f_I(x)=\prod_{i\in I}x_i,\qquad
\delta_I^{(m)}=\mathbb E_q f_I-\mathbb E_u f_I.
\]
Let \(C_m\) be the real vector space indexed by the \(m\)-subsets, with
the standard counting inner product. Define
\[
(D_m a)_J=\sum_{i\notin J}a_{J\cup\{i\}},
\quad |J|=m-1,
\qquad
(D_m^T b)_I=\sum_{j\in I}b_{I\setminus\{j\}},
\quad |I|=m.
\]
On \(C_k\), direct counting gives the up/down commutator
\[
\boxed{D_{k+1}D_{k+1}^T
=D_k^TD_k+(N-2k)I.} \tag{1}
\]
This is the standard Boolean-lattice / Johnson-scheme relation.

For balanced signs,
\[
\sum_{i\notin J}f_{J\cup\{i\}}(x)
=-\sum_{j\in J}f_{J\setminus\{j\}}(x).
\]
Consequently, exact pair matching implies \(D_4\delta_4=0\), while the
sixth-order residual obeys
\[
\boxed{D_6\delta_6=-D_5^T\delta_4.} \tag{2}
\]
Thus \(\delta_6\) is generally not in \(\ker D_6\).

## 2. Exact sixth-harmonic projection

Set \(b=D_5^T\delta_4\). Since \(D_4\delta_4=0\), equation (1) gives
\[
D_5D_5^T\delta_4=(N-8)\delta_4,
\qquad
D_6D_6^Tb=(2N-18)b.
\]
Equation (2) then shows that the orthogonal projection of \(\delta_6\)
onto \((\ker D_6)^\perp=\operatorname{im}D_6^T\) is
\[
\operatorname{Proj}_{\operatorname{im}D_6^T}\delta_6
=-\frac{1}{2N-18}D_6^Tb.
\]
Therefore its degree-six harmonic component is
\[
\boxed{
\delta_6^{\mathrm{harm}}
=\delta_6+\frac{1}{2N-18}D_6^TD_5^T\delta_4.
} \tag{3}
\]
Using the orthogonality of the projection and its complement,
\[
\boxed{
\|\delta_6^{\mathrm{harm}}\|_2^2
=\|\delta_6\|_2^2
-\frac{N-8}{2N-18}\|\delta_4\|_2^2.
} \tag{4}
\]
For \(N=42\), the correction coefficient is
\[
\frac{N-8}{2N-18}=\frac{34}{66}=\frac{17}{33}.
\]
Equation (4) is the exact correction needed before using sixth-order
residuals as degree-six harmonic data. It avoids a dense pseudoinverse.

The balanced-slice Gram kernel on \(\ker D_m\) has scalar eigenvalue
\[
\lambda_m=4^m\frac{\binom{N-2m}{n-m}}{\binom Nn}.
\]
For \(N=42,m=6\),
\[
\lambda_6=\frac{7938048}{6724861}.
\]
Consequently, if all sixth-order coordinates were available, the optimal
combined degree-four and degree-six character bound would be
\[
\boxed{
\chi^2(q\Vert u)\ge
\frac{\|\delta_4\|_2^2}{\lambda_4}
+\frac{\|\delta_6\|_2^2-
\frac{17}{33}\|\delta_4\|_2^2}{\lambda_6}.
} \tag{5}
\]
This is an orthogonal sum of the degree-four and degree-six harmonic
contributions. The second numerator is nonnegative by construction.

## 3. A cheap explicit harmonic witness

A full \(\binom{42}{6}=5,245,786\)-coordinate sixth-moment audit is not
needed to obtain a rigorous additional contribution. Choose six disjoint
pairs
\[
(0,1),(2,3),(4,5),(6,7),(8,9),(10,11)
\]
and define
\[
h(x)=\prod_{r=0}^{5}(x_{2r}-x_{2r+1})
=\sum_{\epsilon\in\{0,1\}^6}
(-1)^{|\epsilon|}f_{I_\epsilon}(x),
\quad
I_\epsilon=\{2r+\epsilon_r:0\le r<6\}.
\]
Its coefficient vector has 64 entries \(\pm1\) and lies in
\(\ker D_6\): for any five-set that chooses one endpoint from five
different pairs, the two completions from the remaining pair cancel; all
other five-sets have no supported completion. Hence \(h\) is a pure
degree-six harmonic on the balanced slice and is orthogonal to every
degree-four harmonic witness.

The uniform mean is zero. Its exact variance is
\[
\mathbb E_u h^2
=64\lambda_6
=64\frac{7938048}{6724861}.
\]
For the EUI projection-DPP distribution, the even-minor identity gives
\[
\mathbb E_q f_I=\mathbb E_q\det Q_{I,I}.
\]
Thus \(\mathbb E_q h\) is a signed sum of only 64 sixth-order principal
minors per physical atom.

Let \(L_4=\|\delta_4\|_2^2/\lambda_4\) denote the already certified Run 68
quartic lower bound. Orthogonality and Bessel's inequality imply
\[
\boxed{
\chi^2(q\Vert u)\ge
L_4+\frac{(\mathbb E_q h)^2}{64\lambda_6}.
} \tag{6}
\]
No lower-order correction is needed for this selected witness because its
coefficient vector is exactly in \(\ker D_6\).

## 4. Candidate-specific certified result

The verifier uses the frozen exact-decimal couplings, the 256-bit Arb
positive weights reconstructed in the Run 57 evidence, and the existing
Fourier-block formula for \(Q=RD\). It evaluates the 64 minors for each of
the 37 base atoms and their one-site translates (4,736 principal minors in
total), with outward-rounded Arb arithmetic.

The certificate records:
- the exact 64-term witness and its 792 local down-relation checks;
- exact \(\lambda_6\) and \(\mathbb E_u h^2\);
- the Arb interval for \(\mathbb E_q h\);
- the additional degree-six chi-square contribution;
- the conservative sum with the Run 68 degree-four lower-bound floor;
- hashes of all frozen atom, weight, and quartic-certificate inputs.

The result is candidate-specific. It is not a full sixth-harmonic projection,
does not exclude any other period-two or general cycle-exponential measure,
and does not imply a program-label TV, Choi, or diamond-distance bound.

## 5. Reproduction

```bash
python -m pip install "python-flint==0.9.0"
python -m py_compile verify_n42_degree_six_harmonic_witness_arb.py
python verify_n42_degree_six_harmonic_witness_arb.py
```

The workflow .github/workflows/eui-n42-degree-six-harmonic-witness.yml
runs the existing Run 68 quartic certificate first, then this witness
certificate. The exact lower-order projection identity (4) is recorded for
the subsequent full sixth-order orbit audit.
