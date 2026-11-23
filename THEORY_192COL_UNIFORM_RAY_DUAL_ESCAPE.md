# 192-column dual escape on the uniform positive-coupling ray

**Status:** proved existence of a finite uniform-ray escape for the particular rationalized 192-column dual. The proof uses an exact-decimal torus point certified by 128-bit Arb and the dense-torus theorem in THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md.

This result does **not** invalidate the finite 192-column minimax theorem. It shows that its particular dual vector cannot be extended to a separator of the full continuous positive-coupling path family.

## 1. Fixed finite-pool result remains valid

The 192-column / 2,113-row mixed-order LP has an independently Arb-certified rational dual. Its finite-pool lower bound is

\[
\min_{p\in\Delta_{192}}\|A_{2113\times192}p-y\|_\infty
\ge
\frac{49457924053915886516751}{112589990684262400000000}
=0.4392746082785582\ldots > \frac13.
\]

The dual certificate pins the LP transcript by SHA256

ed966f1c3f755b1910f7f34be978af88ee290821ea643cb7690d83c7aeab686a

and the exact 2,113-row cut design by SHA256

d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f.

The finite-pool theorem concerns exactly the 192 listed physical columns and the fixed mixed-order row design.

## 2. Uniform-path torus

Let \(K_*\in\mathbb R^{42\times42}\) be the real skew-symmetric path generator with

\[
(K_*)_{j,j+1}=2,\qquad (K_*)_{j+1,j}=-2,
\quad j=0,\ldots,40.
\]

For \(k=1,\ldots,21\), define

\[
\omega_k=4\cos\left(\frac{k\pi}{43}\right).
\]

The explicit real orthogonal basis \(Q\) in THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md satisfies

\[
Q^\mathsf T K_*Q=\bigoplus_{k=1}^{21}\omega_k J,
\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Consequently,

\[
e^{tK_*}=Q\left(\bigoplus_{k=1}^{21}
\begin{pmatrix}
\cos(t\omega_k)&\sin(t\omega_k)\\
-\sin(t\omega_k)&\cos(t\omega_k)
\end{pmatrix}\right)Q^\mathsf T.
\]

The 21 frequencies are linearly independent over \(\mathbb Q\). To see this, put \(\zeta=e^{2\pi i/43}\) and \(\eta=e^{\pi i/43}=-\zeta^{22}\). Up to nonzero rational factors, the \(\omega_k\) are \(\eta^k+\eta^{-k}\). Since multiplication by 22 permutes the 21 nonzero residue pairs \(\{m,-m\}\pmod{43}\), a rational relation would give

\[
\sum_{m=1}^{21}b_m(\zeta^m+\zeta^{-m})=0.
\]

Multiplying by \(\zeta^{21}\) produces a polynomial of degree at most 42 with zero coefficient at \(x^{21}\). It vanishes at \(\zeta\), so it must be a rational multiple of \(\Phi_{43}(x)=1+x+\cdots+x^{42}\); the missing \(x^{21}\) coefficient forces that multiple, and hence every \(b_m\), to vanish.

Kronecker's theorem therefore gives density of \(\{e^{tK_*}:t\ge0\}\) in the 21-torus

\[
\mathbb T_*=
\left\{
Q\left(\bigoplus_{k=1}^{21}R(\theta_k)\right)Q^\mathsf T:
\theta\in\mathbb T^{21}
\right\}.
\]

## 3. Exact positive torus point

Let \(S_{192}(R)\) be the pricing functional of the exact rationalized 192-column dual, including its certified slack shift. It is a finite linear combination of principal minors and is therefore continuous in the matrix entries.

A deterministic 12-start L-BFGS-B search on \([-\pi,\pi]^{21}\) found the following exact-decimal phase vector:

\[
\begin{aligned}
\theta_* = (&3.115144923682,\;0.012782675023,\;0.002801179562,\\
&0.005221189140,\;3.141592653590,\;-2.961380908559,\\
&3.098936035689,\;-3.141592653590,\;-0.021806339419,\\
&0.003042765378,\;0.005467769476,\;-0.015694296862,\\
&3.141592653590,\;-3.117698947068,\;3.141592653590,\\
&2.969232121438,\;0.015147063365,\;-0.003822981075,\\
&0.032516371679,\;3.135156410377,\;-3.063699868854).
\end{aligned}
\]

The phase-vector SHA256 is

e1569f8952cf6fbc65d490eb6d8179069f3da47ea77dd3444184a47549ed4546.

The discovery optimizer is not used as proof. The independent verifier reconstructs \(Q\), all 21 rotation blocks, the 42-by-42 torus matrix, and every active row contribution from exact rational/decimal inputs using 128-bit Arb. It reports

\[
\boxed{
S_{192}(R(\theta_*))
\in
[2.930022809514503777074927378122496
\pm 3.46\times10^{-34}]
>0.
}
\]

In particular, the lower endpoint is strictly greater than 2.93. The exact dual has 61 active rows: two low-order, 56 selected/cut sixth-order, and three selected eighth-order rows. The verifier independently pins the 192-column dual, LP transcript, and cut-row inventory.

## 4. Corollary: the 192-column dual does not separate the continuous uniform ray

**Theorem.** There exists a finite \(t>0\) such that

\[
S_{192}(e^{tK_*})>0.
\]

**Proof.** By the Arb certificate, \(S_{192}(R(\theta_*))>0\). Continuity gives a nonempty open neighborhood \(U\subset\mathbb T_*\) of \(R(\theta_*)\) on which \(S_{192}>0\). For every \(T>0\), the tail \(\{e^{tK_*}:t\ge T\}\) is dense in \(\mathbb T_*\): it is the translate by \(e^{TK_*}\) of the dense positive semiorbit, and translation by a torus element is a homeomorphism. Hence the tail intersects \(U\), giving a finite \(t\ge T>0\) with the strict inequality. \(\square\)

Equivalently, for the physical path with all 41 edge couplings equal to this same positive \(t\), the 192-column dual pricing is strictly positive. Thus this dual cannot certify a global separator for the continuous positive-coupling path family.

### Explicit finite-time witness

A direct one-dimensional search along the uniform ray selected
\[
t_* = 14425.249926691145447
=\frac{14425249926691145447}{10^{15}}>0.
\]
All 41 edge couplings are exactly this same positive rational number. This witness uses the unbounded positive-coupling domain \((0,\infty)^{41}\) established by the sign-gauge reduction; a separately imposed coupling-norm or upper-bound constraint would define a different family and must be checked independently. An independent 128-bit Arb verifier evaluates the exact uniform-ray matrix from the algebraic frequencies and exact phase basis, then recomputes all 61 active dual-row contributions. It certifies
\[
\boxed{
S_{192}(e^{t_*K_*})
\in
[0.468498256538894200560432299886
\pm 2.83\times10^{-31}]>0.
}
\]
The lower endpoint is strictly greater than 0.4684982565388942. The binary64 discovery score at the rounded decimal time was 0.46849825653705707; it is only a search diagnostic. The Arb interval is the physical-path proof.

This is an explicit finite, strictly positive uniform-coupling escape, not merely a nonconstructive consequence of density. Since all 192 pinned columns have strictly negative Arb-certified pricing values, this path is necessarily outside that finite pool.

## 5. What this does and does not establish

**Established:**
- The finite 192-column / 2,113-row minimax obstruction remains rigorously certified.
- The exact 192-column dual has a strictly positive point on the closure torus of the uniform positive-coupling ray.
- An explicit rational uniform coupling t=14425.249926691145447 has a 128-bit Arb-certified positive pricing interval, so a finite physical path escapes this particular dual.

**Not established:**
- Feasibility or infeasibility of a probability mixture over the full continuous physical family.
- A continuous-family minimax lower bound or upper bound.
- Complete sixth/eighth orbit control.
- A Choi-infidelity or diamond-distance guarantee.

The next useful experiment is to append this exact uniform path as the 193rd column and reoptimize the same 2,113-row LP. Even if the new finite pool remains obstructed, a different dual may still separate the full continuous family; the present result only refutes this particular 192-column dual.

## 6. Reproducibility

- Dense-torus derivation: THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md
- Search: discover_192col_uniform_torus_pricing.py
- Independent verifier: verify_192col_uniform_torus_pricing_arb.py
- Search transcript: evidence/192col_uniform_torus_search_n21.json
- Search transcript SHA256: 90c47cfabf5576014f99705e5bf407cf190e394bcba0a7c00f3a51f42dcebfa9
- Arb certificate: evidence/192col_uniform_torus_arb_n21.json
- Torus workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45220627970 (success).
- Explicit-time search: discover_192col_uniform_ray_time_escape.py
- Explicit-time Arb verifier: verify_192col_uniform_ray_time_arb.py
- Explicit-time search transcript: evidence/192col_uniform_ray_time_search_n21.json
- Explicit-time Arb certificate: evidence/192col_uniform_ray_time_arb_n21.json
- Explicit-time workflow: https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45221238345 (success; finite-time search, Arb verification, artifact commit, and upload passed).
- Evidence commit: c61fca25cfe6dcc6d13b76429e10c533c907f71f
- Torus/theory commit: e9e1b9c6e8c8df5e20cad01f817dc0c5072b07c7

The final discovery transcript checks the analytic cofactor gradient at the generic nonstationary phase vector
\[
\theta^{\rm check}_k=1.35\sin(0.37k)+0.82\cos(0.23k),\qquad k=0,\ldots,20.
\]
For coordinates 0, 10, and 20, the maximum relative defect across complex-step and central-difference checks is \(6.7481\times10^{-10}\); the maximum complex-step absolute defect is \(1.78\times10^{-15}\). The basis regressions report orthogonality defect \(2.63\times10^{-15}\), canonical-form defect \(5.33\times10^{-15}\), uniform-ray rotation defect \(3.39\times10^{-15}\), and pricing agreement defect \(5.55\times10^{-13}\). These are numerical implementation checks; the positive pricing conclusion itself is the independent Arb interval proof.
