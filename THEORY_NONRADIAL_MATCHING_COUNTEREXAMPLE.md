# A certified obstruction to a non-radial finite-oracle improvement

The [radial recovery optimum](THEORY_ODD_CYCLE_RADIAL_RECOVERY.md) leaves open non-radial recovery. A five-site diagnostic gives both a positive finite-ensemble optimization and a certified obstruction to promoting it to a full-physical-family target-component guarantee.

This is a **small-system complementary-map diagnostic**. Five sites do not satisfy the long-ring six-query cancellation threshold. No five-site cancellation protocol, long-ring counterexample, or unrestricted recovery no-go theorem is claimed.

## 1. Exactly optimized legal Pauli test ensemble

Use the occupation basis in the selected plus-parity block, of dimension \(D=16\). The physical Majorana graph is a ten-cycle: its alternating edges represent the local fields and Ising couplings, with known convention-dependent signs. Every matching of that graph generates a legal unitary block: set its disjoint bilinear coefficients to \(\pi/2\) and all other coefficients to zero. The bilinears commute, and their exponential is their Majorana monomial up to phase.

Identify full Majorana complements in the selected parity block. The matchings generate **91 distinct balanced Pauli labels**, denoted \(\mathcal B\), among the 126 balanced program labels. This is an explicitly realizable subset; it is not asserted to enumerate every possible physical Pauli oracle. There are 130 complementary program labels \(R\).

For a rule applying \(R^\dagger\) followed by \(T\in\mathcal B\), let \(q_R(T)\) be its conditional distribution. The target component at a Pauli oracle \(B\in\mathcal B\) is proportional to
\[
 G_B(q)=\sum_{R\notin\mathcal S}a_{|RB|/2}^2q_R(B).
\]
The finite LP maximizes \(\min_{B\in\mathcal B}G_B\), subject to nonnegative probabilities with row sums one. Its **exact optimum** is
\[
 G_{\mathcal B}^*=\frac{23880}{91}
 =\frac{18}{13}G_{\rm radial},\qquad G_{\rm radial}=\frac{3980}{21}.
\]
The averaging upper bound is
\[
 \min_BG_B\le\frac1{91}\sum_RG_{\rm row,max}
 =\frac1{91}\sum_R\max_{B\in\mathcal B}a_{|RB|/2}^2
 =\frac{23880}{91}.
\]
A frozen rational primal rule with 220 nonzero probabilities attains it, with exactly equal gain on all 91 labels. The largest denominator is 4459. Both this rule and the averaging upper bound are checked with exact fractions; the optimum is not inferred from solver tolerances. The initial solution was found with SciPy/HiGHS. Verification requires no LP/SDP solver.

## 2. Training Choi checks improve, but do not certify the full family

Freeze the mixture
\[
 q_\eta=(1-\eta)q_{\rm radial}+\eta q_{\mathcal B},\qquad \eta=2/25,
\]
where the baseline is radial ML. On the seven pinned physical instances used in the earlier verifier (identity, fields, edge Pauli and four seeded noncommuting Hamiltonians), the measured maximal target-unitary Choi subtraction weight improves by factors
\[
 1.03076923,\ 1.02416016,\ 1.03076923,\ 1.01500724,\
 1.01127727,\ 1.02153178,\ 1.01036789.
\]
These are finite floating-point checks. The inverse/range formula for rank-one PSD subtraction is checked against the extracted residual matrix. They do not establish a uniform improvement. A grid and scalar mixture search preceded freezing the rational weight; the displayed seven instances are training instances, not independent evidence.

A random scan of 128 additional instances (32 each at coefficient standard deviations 1/4, 1, 3 and 10; seed 202611201043) did not cross the Bell-overlap failure threshold. A subsequent local search did; its coefficients were simplified to the rational witness below. Optimizer convergence is not used as evidence: the fixed witness is independently verified by complex ball arithmetic.

## 3. A necessary Bell-overlap inequality

For an arbitrary physical target \(V=\sum_{T\in\mathcal S}v_TT\), with \(\sum_T|v_T|^2=1\), the program-support identity from the previous notes gives
\[
 \frac{\langle\!\langle V|J_q|V\rangle\!\rangle}{D^2}
 =D^{-4}\sum_{T\in\mathcal S}|v_T|^2G_T(q).
\]
Any target-unitary CP component \(\kappa\) in \(J_q\) must satisfy
\(\kappa\le\langle\!\langle V|J_q|V\rangle\!\rangle/D^2\).
Define the matching-span program mass
\[
 p_{\mathcal B}(V)=\sum_{B\in\mathcal B}
               |\operatorname{Tr}(B^\dagger V)/D|^2.
\]
The optimized matching rule has zero probability outside \(\mathcal B\) and equal \(G_B=G_{\mathcal B}^*\) inside it. Therefore
\[
 \frac{\kappa(q_\eta,H)}{\kappa_{\rm radial}}
 \le (1-\eta)+\eta\frac{18}{13}p_{\mathcal B}(V),\qquad
 \kappa_{\rm radial}=G_{\rm radial}/D^4.
\]
In particular, \(p_{\mathcal B}<13/18\) rules out a uniform target-component improvement for **every positive mixture weight**. The same argument applies to any finite-ensemble optimal rule supported on \(\mathcal B\), since equality in the averaging bound forces equal gain on all its 91 oracle labels.

## 4. Rational physical witness and certified bounds

In the original physical coordinates, take
\[
 H=\sum_{j=0}^4 h_jX_j+\sum_{j=0}^4J_jZ_jZ_{j+1},
 \qquad j+1\text{ modulo }5,
\]
with
\[
 (h_0,\ldots,h_4)=(-12/5,-5/3,0,37/20,-49/20),
\]
\[
 (J_0,\ldots,J_4)=(49/20,-37/20,0,-5/3,12/5).
\]
The selected plus-parity block is represented after sitewise Hadamards by even occupation rows, local \(Z\) fields and \(XX\) edges, exactly as in the existing verifiers.

Using a rational matrix for \(H\), the verifier encloses \(V=e^{iH}\) with `acb_mat.exp()` at 192-bit precision and computes the sum of coefficient squared magnitudes using ball arithmetic. It certifies
\[
 0.5414777<p_{\mathcal B}(V)<0.5414778<13/18.
\]
The more precise enclosure in the recorded run is
\[
 p_{\mathcal B}(V)=
 0.541477719069843137479535001289827706079977631529726454
 \ \pm\ 4.97\times10^{-55}.
\]
For \(\eta=2/25\), the Bell upper bound on the CP target-weight ratio is
\[
 0.9799790704200441629208100309121039920580898299540620072
 \ \pm\ 4.31\times10^{-56}<0.98.
\]
Thus the mixed candidate cannot match the radial **uniform CP target-component guarantee**, despite improving all seven training checks. The implication follows from an exact inequality and a certified enclosure, rather than a sampled small negative eigenvalue.

This does **not** by itself prove a larger full balanced diamond error at this witness: an insufficient target-component certificate and a worse channel norm are different assertions. It also does not preclude a different non-radial decoder.

## Reproducibility and next action

Frozen data: [evidence/nonradial_matching_n5.json](evidence/nonradial_matching_n5.json). Verifier: [verify_ising_nonradial_matching.py](verify_ising_nonradial_matching.py).

Run `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_nonradial_matching.py`. Use `--ball-only` for the exact finite-ensemble certificate and certified witness without the floating training checks. Dependencies in this run: NumPy 2.3.5, SciPy 1.17.0 and python-flint 0.9.0. The matrix-exponential interface and ball semantics are documented by [python-flint](https://python-flint.readthedocs.io/en/latest/acb_mat.html); the implementation reads exact rationals and does not truncate the matrix exponential to an uncertified numerical polynomial.

The pinned input rule, rational Hamiltonian, exact LP certificate and ball enclosures are reproducible without rediscovering the candidate or rerunning the local search. The manuscript [robustness appendix](https://arxiv.org/html/2506.20570v1) supplies the physical support context; this diagnostic retains the narrower common parity-drift recovery framework of the theory notes.

The next finite optimization should include this witness and allow all 126 balanced correction hypotheses. Maximize a shared \(\kappa\) with nonnegative row-normalized \(q_R(T)\), requiring \(J_H(q)-\kappa|V_H\rangle\!\rangle\langle\!\langle V_H|\succeq0\) for the pinned instances and the witness. A finite SDP result still requires a uniform analytic certificate or a verified converse before any full-family claim. The long-ring non-radial optimum and the unrestricted query questions remain open.
