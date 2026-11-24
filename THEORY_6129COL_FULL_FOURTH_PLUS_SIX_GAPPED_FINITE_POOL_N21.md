# 6,129-column full-second/fourth finite-pool obstruction at n=21

**Status:** rigorous finite-pool theorem; independently certified with python-flint / Arb on 2026-11-24. **Not claimed:** a continuous-family obstruction, an all-even-principal-minor obstruction, or a Choi/diamond-distance lower bound.

## 1. Exact finite physical pool

Let \(N=42\) (\(n=21\)) and
\[
R(c)=e^{A(c)}\in SO(42),\qquad
A(c)_{j,j+1}=2c_j,\quad A(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,\quad c_{41}=0.
\]
The exact pool contains 6,129 columns:

1. 22 pinned base atoms from the 41-atom low-moment Arb certificate;
2. 6,101 corrected fractional single-open-path grid atoms with step 0.01:
   - \(L=2\): \(k=0,\ldots,200\);
   - odd \(L=3,5,\ldots,41\), and \(L=42\): \(k=1,\ldots,100\);
   - even \(L=4,6,\ldots,40\): \(k=1,\ldots,200\).
   The identity at \(\alpha=0\) is included once;
3. six exact-rational gapped paths: four inherited from the certified 6,127-column pool, plus a new connected escape and a new one-cut escape from the 6,127-column dual. The inherited multi-segment path has cuts \([16,26]\); the new two-segment path has cut \([35]\). Four of the six gapped paths are connected with all 41 internal couplings strictly positive. Every path has closing edge \(c_{41}=0\).

The 6,129-column diagnostic retains a legacy status string containing “6125”; its explicit candidate count is 6,129, and the independent verifier checks that exact count and every column. This is a metadata-label defect, not a mathematical ambiguity.

## 2. Full second-/fourth-order feature system

For each rotation, retain all 21 distance-averaged second moments and all 1,440 dihedral orbits of fourth-order principal minors. The raw fourth-order set contains
\[
\binom{42}{4}=111{,}930
\]
quartets. The full feature vector has dimension 1,461. Exact incidence identities reduce this to 1,313 independent moment coordinates; adding normalization gives 1,314 equalities. The exact hierarchy pivot-minor determinant is
\[
824{,}633{,}720{,}832\ne0.
\]

Let \(F(R)\in\mathbb R^{1461}\) be the full feature vector and \(b\in\mathbb Q^{1461}\) the exact balanced target. Let \(A_{6129}\) contain precisely the 6,129 listed physical columns.

## 3. Exact rational dual and Arb certificate

The floating HiGHS discovery has 80 nonzero dual coefficients. The independent verifier freezes each printed decimal exactly as a rational and normalizes it so
\[
D=\operatorname{diag}(41I_{21},533I_{1440}),
\qquad
\boxed{\|D^{-1}y\|_1=1}.
\]
The exact full-coordinate norm is
\[
\|y\|_1=
\frac{18276314286132367993801}
{35533333333333310677}
=514.3428035496918\ldots<533.
\]

The verifier uses 512-bit Arb for all 22 base atoms and six gapped paths, and 128-bit Arb for all 6,101 fractional-grid atoms. It independently certifies
\[
\boxed{y^{\mathsf T}(b-F(R_j))>\frac15,\qquad j=1,\ldots,6129.}
\]
The minimum Arb lower endpoint is
\[
0.2374306538960380051374786212565\ldots>\frac15,
\]
attained at pinned base atom 14. All six gapped-path gaps are approximately \(0.2525282113487\ldots\).

### Theorem 1 — finite-pool moment obstruction

For every probability vector \(p\in\Delta_{6129}\),
\[
y^{\mathsf T}(b-A_{6129}p)>\frac15.
\]
Since \(\|y\|_1<533\), Hölder gives
\[
\boxed{\|b-A_{6129}p\|_\infty>\frac1{2665}.}
\]
No nonnegative mixture of the exact 6,129 listed physical columns can match all retained second-/fourth-order target moments within this residual.

### Corollary 1 — finite-pool program-label TV obstruction

For each retained moment coordinate, the DPP / Pauli-character identity expresses it as the expectation of a bounded program-label test: a distance-averaged second-order character or a dihedral-orbit average of fourth-order characters. Each test has sup norm at most one. Therefore the infinity-norm residual bound implies that at least one bounded test has expectation gap greater than \(1/2665\) between the ensemble-averaged program-label mass \(w_p\) and the uniform balanced-label law \(u_{\rm bal}\). By
\[
|\mathbb E_P f-\mathbb E_Q f|\le2\,\operatorname{TV}(P,Q),
\qquad \|f\|_\infty\le1,
\]
\[
\boxed{\operatorname{TV}(w_p,u_{\rm bal})>\frac1{5330}.}
\]
Equivalently, the associated dephased program-label registers have trace distance greater than \(1/5330\).

This is a finite-pool classical program-mass statement. It is not a Choi-state trace-distance or channel diamond-distance bound.

## 4. Reproducibility and provenance

- Floating diagnostic: [ising_full_fourth_plus_six_gapped_n21.json](evidence/ising_full_fourth_plus_six_gapped_n21.json)
- Exact rational Arb certificate: [ising_full_fourth_plus_six_gapped_arb_n21.json](evidence/ising_full_fourth_plus_six_gapped_arb_n21.json)
- Independent verifier: [verify_ising_full_fourth_plus_six_gapped_arb_n21.py](verify_ising_full_fourth_plus_six_gapped_arb_n21.py)
- Workflow: [45429779133](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45429779133), success
- Certificate commit: [741760a](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/741760af23d1fcfa66af4b1c2876b71ed3cf1f24)
- Diagnostic SHA256: 9cb255dfe0d96155f69ee9d9b9870cf1d442879e3afa3258ff599c0f7e834ccd
- Parent 6,127-column Arb certificate SHA256: e7d4a8e79c6b7346ee9b2dd9629f756d3eb868cf3a2c2d32ad14fb5b92c499e7
- New 6,127-dual escape certificate SHA256: 2ec37629fb392023a977bf062a93f292126075ebd00e256ff81ae86a369c4dc6
- Warm 41-atom ensemble certificate SHA256: 33cc0432fe8639ef22f0153fcc31e060a48cba5cb638fa500edaddc43b9560d5

## 5. Scope and next step

Theorem 1 is a **finite-pool** statement. The six gapped paths are exact and certified, but they do not exhaust all positive nonuniform couplings or all multi-segment paths. The continuous pricing task has now found two independently Arb-certified escapes from this particular 80-term dual, including a path with all 41 internal couplings strictly positive. The finite 6,129-column theorem remains valid. See [the escape note](THEORY_6129COL_DUAL_GAPPED_ESCAPE.md). The next step is an 6,131-column reoptimization after appending both escapes. The all-even-principal-minor positive-ensemble condition remains unresolved, as does a per-instance bridge from moment residuals to Choi/diamond error.
