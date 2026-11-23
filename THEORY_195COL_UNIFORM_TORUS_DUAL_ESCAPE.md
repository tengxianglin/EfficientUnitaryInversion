# 195-column dual escape on the uniform-path 21-torus

## Status

The exact rational 195-column dual is strictly certified on its pinned finite pool, but it is **not** a separator of the full continuous positive-coupling path family. A deterministic search found an exact-decimal phase point on the uniform-path 21-torus, and an independent 128-bit Arb verifier certifies a strictly positive pricing interval:

\[
S_{195}(R(\theta_*))
\in
[4.483867316010550697286473341089799
\pm 8.75\times10^{-34}]>0.
\]

The phase vector is exact decimal input (hence rational), with SHA256
\[
\texttt{dfa636c9dfe1d1d7ddf64667383ec343f65103bf32f2f30f07711b73438b33c7}.
\]
The positive interval is the proof; the floating-point search score and gradient checks are discovery/implementation diagnostics only.

## 1. The finite 195-column theorem remains valid

The pinned 195-column, 2,113-row mixed-order design has an exact rational dual with
\[
\|z\|_1=1,\qquad
\delta=10^{-10},
\]
and proves
\[
\min_{p\in\Delta_{195}}\|A_{195}p-y\|_\infty
\ge
\frac{2803294808039097361653228789}
{6588122883467712110000000000}
=0.42550736493906444\ldots>\frac13.
\]
All 195 finite-column inequalities were independently checked by 128-bit Arb. The theorem is stated in
[THEORY_195COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md](THEORY_195COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md).

This finite-pool theorem is not changed by the continuous escape below.

## 2. Uniform-path torus

Let \(K_*\in\mathbb R^{42\times42}\) be the skew-symmetric nearest-neighbor path generator
\[
(K_*)_{j,j+1}=2,\qquad (K_*)_{j+1,j}=-2,
\qquad j=0,\ldots,40.
\]
The explicit real orthogonal matrix \(Q\) in
[THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)
satisfies
\[
Q^{\mathsf T}K_*Q
=\bigoplus_{k=1}^{21}\omega_k J,
\qquad
\omega_k=4\cos(k\pi/43),\quad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]
The 21 frequencies are linearly independent over \(\mathbb Q\), so Kronecker's theorem implies that the positive-time uniform ray
\[
e^{tK_*},\qquad t\ge0,
\]
is dense in
\[
\mathbb T_*=
\left\{
Q\left(\bigoplus_{k=1}^{21}
\begin{pmatrix}
\cos\theta_k&\sin\theta_k\\
-\sin\theta_k&\cos\theta_k
\end{pmatrix}\right)Q^{\mathsf T}
:\theta\in\mathbb T^{21}
\right\}.
\]

For the exact rationalized 195-column dual, define the continuous pricing functional
\[
S_{195}(R)=\lambda-\delta+z^{\mathsf T}a(R),
\]
where \(a(R)\in\mathbb R^{2113}\) is the pinned normalized mixed-order feature vector.

## 3. Exact positive torus point

The 21 exact-decimal phases are
\[
\begin{aligned}
\theta_*=(&-0.237174330367,\;-0.581129084226,\;-0.631199185419,\\
&-0.162921096430,\;0.030911107456,\;0.321973998812,\\
&0.484773690946,\;0.788165599622,\;1.093079528693,\\
&2.583780776120,\;2.651623134437,\;2.521196888821,\\
&1.837204249747,\;1.074691145021,\;0.327566525064,\\
&0.137813104031,\;0.078470257286,\;0.073975915144,\\
&3.141592653590,\;3.141592653590,\;3.141592653590).
\end{aligned}
\]

The search used 12 deterministic starts and L-BFGS-B on \([-\pi,\pi]^{21}\), with at most 120 iterations per start. Its best binary64 score was approximately 4.483867316010547. The maximum relative gradient regression defect was approximately \(1.80\times10^{-9}\). Neither number is used as proof.

The independent verifier reconstructs the exact-decimal rational phases, the algebraic entries of \(Q\), the rotation blocks, the exact rational dual, and all 64 nonzero dual-row contributions with python-flint 0.8.0 / Arb at 128-bit precision. It certifies
\[
\boxed{
S_{195}(R(\theta_*))
\in
[4.483867316010550697286473341089799
\pm8.75\times10^{-34}]>0.
}
\]
The certificate records the lower endpoint as
\[
[4.4838673160105506972864733410897981250
\pm2.46\times10^{-38}],
\]
which is strictly positive.

Pinned provenance:
- 195-column dual SHA256: `8371f7f2d4d866839b223dbe1b0c3e872a220092bc22b7cbc69384f08acb456c`;
- 195-column LP SHA256: `0d5b2d821b95e3229b3ffbcbfd3dafacd80cb76ba1aba55e2858183d53792908`;
- 2,113-row cut-design SHA256: `d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f`.

## 4. Theorem: the 195-column dual does not separate the uniform positive-coupling ray

**Theorem.** There exists a finite \(t>0\) such that
\[
S_{195}(e^{tK_*})>0.
\]

**Proof.** The Arb interval above proves \(S_{195}(R(\theta_*))>0\). The pricing functional is a finite linear combination of matrix minors and is therefore continuous on \(\mathbb T_*\). Hence it is positive on a nonempty open neighborhood of \(R(\theta_*)\). The positive-time uniform orbit is dense in \(\mathbb T_*\), so it intersects that neighborhood at some finite \(t>0\). \(\square\)

This establishes existence of a finite physical equal-coupling escape, although the explicit finite decimal time is not yet supplied in this note. A separate bounded one-dimensional search and direct Arb verification have now been added (workflow `.github/workflows/eui-195col-uniform-ray-time-escape.yml`); until the finite-time Arb certificate is committed, no explicit value of \(t\) is claimed.

## 5. Scope

**Proved:**
- the finite 195-column / 2,113-row minimax lower bound above \(1/3\);
- a strictly positive Arb interval at an exact rational point of the uniform-path torus;
- by continuity and the proved Kronecker density, existence of some finite positive equal coupling that escapes this particular 195-column dual.

**Not proved:**
- feasibility or infeasibility of probability mixtures over the full continuous physical family;
- a continuous-family minimax optimum or lower bound;
- complete sixth/eighth orbit control beyond the pinned design;
- an operational Choi-infidelity or diamond-distance guarantee.

The result refutes only global separation by this particular 195-column dual. It does not invalidate the finite 195-column theorem.

## 6. Reproduction

- Finite-pool theorem: [THEORY_195COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md](THEORY_195COL_2113ROW_UNIFORM_RAY_ESCAPE_MINIMAX_OBSTRUCTION.md)
- Search: [discover_195col_uniform_torus_pricing.py](discover_195col_uniform_torus_pricing.py)
- Independent Arb verifier: [verify_195col_uniform_torus_pricing_arb.py](verify_195col_uniform_torus_pricing_arb.py)
- Search transcript: [evidence/195col_uniform_torus_search_n21.json](evidence/195col_uniform_torus_search_n21.json)
- 128-bit Arb certificate: [evidence/195col_uniform_torus_arb_n21.json](evidence/195col_uniform_torus_arb_n21.json)
- Evidence commit: [f456ab0](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f456ab02a4b49ade64b7a04a06bd4b33a2b78bcf)
- 195-column LP/dual workflow: [45242902521](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45242902521), success.

The 195-column torus pricing certificate is independent of the optimizer: a positive exact Arb interval, not a local-optimality assertion, is the mathematical witness.
