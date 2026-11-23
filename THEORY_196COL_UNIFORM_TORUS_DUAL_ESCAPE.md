# 196-column dual escape on the uniform-path 21-torus

## Theorem

Let \(A\in\mathbb R^{2113\times196}\), \(y\in\mathbb R^{2113}\), and the exact rational dual data \((z,\lambda,\delta)\) be the frozen 196-column mixed-order design and certificate identified below. Define its pricing functional on a path rotation \(R\in SO(42)\) by
\[
S_{196}(R)=z^{\mathsf T}a(R)+\lambda-\delta,
\]
where \(a(R)\) is the same normalized 2,113-component moment-feature vector used to form the LP columns.

There exists a phase vector \(\theta_*\in\mathbb Q^{21}\) such that
\[
S_{196}\!\left(
Q\left(\bigoplus_{k=1}^{21}
\begin{pmatrix}
\cos\theta_{*,k}&\sin\theta_{*,k}\\
-\sin\theta_{*,k}&\cos\theta_{*,k}
\end{pmatrix}
\right)Q^{\mathsf T}
\right)>0.
\]
The inequality is certified by 128-bit Arb interval arithmetic. Consequently, there exists a finite \(t>0\) for which the **physical uniform positive-coupling path**
\[
c_1=\cdots=c_{41}=t>0
\]
has \(S_{196}(e^{tK_*})>0\).

Thus the particular exact 196-column dual is **not** a global separator of the continuous positive-coupling physical family, even when restricted to the one-dimensional equal-coupling ray.

This theorem does not invalidate the 196-column finite-pool minimax obstruction, and it does not prove feasibility or infeasibility of a convex mixture over the full continuous physical family.

## 1. Exact torus witness

The exact phase vector is the list of decimal strings below, each interpreted as an exact rational number (not as a binary64 approximation):
\[
\begin{aligned}
\theta_* = (&-0.115122920280,\ 0.333003677241,\ -3.116925006593,\\
&3.141592653590,\ -3.141592653590,\ 3.141592653590,\\
&-0.451016709334,\ -0.184552518666,\ -0.161514824032,\\
&-0.147141913049,\ -0.110710352898,\ -0.168466960386,\\
&-0.014722467749,\ -3.137711458388,\ 3.141592653590,\\
&3.141592653590,\ -3.141592653590,\ -3.131702851062,\\
&-0.284411194108,\ 3.141592653590,\ 0.103020282781).
\end{aligned}
\]

The independent verifier reports
\[
\boxed{
S_{196}(R(\theta_*))
\in
[1.5804582969205441019413585480859926
\pm 4.77\times10^{-35}]>0.
}
\]
The lower endpoint is strictly positive. The phase-vector SHA256 is
\texttt{07ef5b4a57de7be1ac1ec0d7aded62b86fadecf2dc4cf4caa6c0a9b4ebfee6b8}.

The phase optimizer is only a discovery mechanism. Its 12-start binary64 search and gradient checks are not used as proof. The proof is the independent Arb evaluation of the exact decimal phase strings against the exact rational dual.

## 2. Why the torus point implies a finite physical path

For the 42-site open path generator
\[
(K_*)_{j,j+1}=2,\qquad (K_*)_{j+1,j}=-2,
\qquad j=0,\ldots,40,
\]
the positive frequencies are
\[
\omega_k=4\cos(k\pi/43),\qquad k=1,\ldots,21.
\]
The exact dense-torus theorem in
[\texttt{THEORY\_UNIFORM\_42SITE\_PATH\_DENSE\_TORUS.md}](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md)
proves that these frequencies are linearly independent over \(\mathbb Q\). Hence
\[
\{e^{tK_*}:t\ge0\}
\]
is dense in
\[
\mathcal T_*=
\left\{
Q\left(\bigoplus_{k=1}^{21}R(\theta_k)\right)Q^{\mathsf T}:
\theta\in\mathbb T^{21}
\right\}.
\]

The pricing functional \(S_{196}\) is a finite linear combination of normalized matrix-entry products and principal minors, so it is continuous on \(SO(42)\). Since \(S_{196}(R(\theta_*))>0\), continuity gives a nonempty open neighborhood \(U\subset\mathcal T_*\) on which \(S_{196}>0\). Density gives some finite \(t>0\) with \(e^{tK_*}\in U\). This proves the asserted finite-time existence.

The argument is existential: it does **not** provide an explicit decimal value or an upper bound for \(t\). A separate one-dimensional search plus Arb verification would be needed for an explicit finite-time witness.

## 3. Frozen evidence and reproduction

The witness is tied to the following exact inputs:

- 196-column dual certificate SHA256: \
  \texttt{45edad15fc5978381108c9ade57006da941c476e05cb447c044fbe4ed986cd86};
- 196-column LP transcript SHA256: \
  \texttt{d203f3cddd74b896f565d44509168f11a39b814b5f5de8fe1f99a89d26c2e179};
- selected-row cut-design SHA256: \
  \texttt{d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f};
- parent 195-column LP SHA256: \
  \texttt{0d5b2d821b95e3229b3ffbcbfd3dafacd80cb76ba1aba55e2858183d53792908};
- parent 195-column dual SHA256: \
  \texttt{8371f7f2d4d866839b223dbe1b0c3e872a220092bc22b7cbc69384f08acb456c}.

Evidence and verifier:

- [196-column search transcript](evidence/196col_uniform_torus_search_n21.json)
- [128-bit Arb torus certificate](evidence/196col_uniform_torus_arb_n21.json)
- [Independent verifier](verify_196col_uniform_torus_pricing_arb.py)
- [Search implementation](discover_196col_uniform_torus_pricing.py)
- [Successful GitHub Actions run 45282545933](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45282545933)
- [Verifier ancestry fix commit 5f2dbba](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/5f2dbba35fc6a1c81d9dfae58d9c2b3c647ce669)

The verifier re-certified the 193-, 194-, and 195-column parent/time chain and the 196-column finite-pool dual before evaluating the exact phase point. It uses python-flint 0.8.0 / Arb at 128 bits.

## 4. Scope

**Proved:**
1. The finite 196-column / 2,113-row minimax residual is greater than \(1/3\), by the separate exact rational dual certificate.
2. The same 196-column dual has strictly positive pricing at one exact rational point of the uniform-path torus.
3. By the dense-ray theorem and continuity, some finite equal-positive-coupling physical path has positive pricing. Therefore this dual cannot separate the full continuous physical family.

**Not proved:**
1. An explicit decimal value of the finite escape time \(t\).
2. Feasibility or infeasibility of a convex mixture over all legal continuous physical generators.
3. A global minimax value for the continuous physical family.
4. Complete sixth-/eighth-order orbit control or an operational Choi/diamond-distance guarantee.

The finite-pool lower bound and the continuous dual escape are logically compatible: the escaping physical path is outside the 196 listed columns.
