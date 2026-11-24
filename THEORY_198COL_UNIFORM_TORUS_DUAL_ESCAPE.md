# Continuous uniform-torus escape from the 198-column mixed-order dual

**Status:** exact-decimal 21-torus point independently certified with 128-bit Arb; dense-ray theorem implies existence of a finite equal-positive-coupling open-path escape. **Not claimed:** an explicit finite time, full-family feasibility/infeasibility, or a Choi/diamond bound.

## 1. Exact pricing problem

Use the uniform 42-site open-path spectral basis from [THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md](THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md):
\[
R(\theta)=Q\left(\bigoplus_{k=1}^{21}
\begin{bmatrix}\cos\theta_k&\sin\theta_k\\-\sin\theta_k&\cos\theta_k\end{bmatrix}\right)Q^{\mathsf T},
\qquad \theta\in\mathbb T^{21}.
\]
The exact 198-column dual, fixed 2,113-row mixed-order design, exact target, row scales, and rational slack are loaded from the pinned LP and Arb dual certificate. The verifier evaluates the same shifted dual pricing function used in the finite-pool certificate, not a separately fitted surrogate.

## 2. Strict Arb witness

The search used 16 deterministic L-BFGS-B starts (including the previously certified 197-column torus point), 160 maximum iterations per start, and the analytic cofactor gradient. The maximum relative gradient-check defect was
\[
6.972813787968378\times10^{-10}.
\]
The best binary64 score was 1.3026969054283108; this is discovery evidence only. The exact decimal phase vector was then independently evaluated with python-flint 0.8.0 / Arb at 128-bit precision. The certificate encloses
\[
\boxed{
S_{198}(\theta_*)\in
[1.3026969054283107647764243746907199\pm8.46\times10^{-35}]>0.
}
\]
The exact 21-entry decimal vector, phase hash, and interval endpoints are stored in [evidence/198col_uniform_torus_arb_n21.json](evidence/198col_uniform_torus_arb_n21.json).

## 3. Physical consequence from dense recurrence

The pinned dense-torus theorem establishes rational independence of the 21 uniform-path frequencies and density of the one-parameter ray \(t\mapsto t\omega\pmod{2\pi}\) in \(\mathbb T^{21}\). The shifted dual score is continuous in \(\theta\). Strict positivity at \(\theta_*\) therefore persists on an open neighborhood; density guarantees that some finite \(t>0\) enters this neighborhood. Along the corresponding physical path,
\[
c_0=\cdots=c_{40}=t>0,\qquad c_{41}=0,
\]
the 198-column dual has positive pricing. Hence this particular dual cannot separate the entire connected positive-coupling physical family.

This is an existence proof for a finite physical time, not yet an explicit numerical value of that time. A separate bounded search can isolate a rational time and independently certify it, but is not needed for the density-based existence implication.

## 4. Scope

- **Proved:** a strict positive Arb interval at one exact rational point of the 21-torus; by the pinned dense-ray theorem and continuity, existence of a finite positive equal-coupling physical time escaping this specific dual.
- **Still true:** the exact 198-column / 2,113-row finite-pool minimax theorem, because the escape lies outside its 198 listed columns.
- **Not proved:** feasibility or infeasibility of the full physical family; a complete sixth/eighth-order orbit result; an all-even-principal-minor positive ensemble; a Choi-state or channel diamond-distance lower bound.

## 5. Reproduction and hashes

- Discovery script: [discover_198col_uniform_torus_pricing.py](discover_198col_uniform_torus_pricing.py)
- Independent verifier: [verify_198col_uniform_torus_pricing_arb.py](verify_198col_uniform_torus_pricing_arb.py)
- Search transcript: [evidence/198col_uniform_torus_search_n21.json](evidence/198col_uniform_torus_search_n21.json)
- Arb certificate: [evidence/198col_uniform_torus_arb_n21.json](evidence/198col_uniform_torus_arb_n21.json)
- Workflow: [45428424440](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45428424440), success
- Certificate commit: [7d8ebf3](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/7d8ebf3fb454b0342cb8138ccb6a7006263c51c4)
- Dual SHA256: d5bc214a70bdb610c034ef673252be8d7109d31b18a33d4bc5ac25e9c993e06f
- LP SHA256: b2bf21c4656b0e46e544a3fe1f72ffea651ea7f138e2c518b17609c6633ddf00
- Dense-torus theory SHA256: 123c137df1a4bff8c017d8c7e1aa49fc8f39b1a54f5535651327bd18bd65aa71
