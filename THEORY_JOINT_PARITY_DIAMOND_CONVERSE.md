# Joint parity ensembles lift the Pauli converse to the full diamond error

The existing [physical design](THEORY_ODD_CYCLE_ORBIT_DESIGN.md) bounds a selected-sector CP target component. That statement alone is not a full diamond-norm converse. A joint ensemble uniform in **both physical parity sectors**, together with a reference-assisted pinching bound, supplies the missing argument.

We prove a general conditional theorem and certify its ensemble hypothesis at five and seven sites. The encoder and recovery architecture stay fixed. Unrestricted inversion optimality is not claimed.

## 1. Encoder, class and result

Let \(n\ge3\) be odd, \(D=2^{n-1}\),
\[
 f=1-2\binom{2n}{n}/4^n,\qquad
 a=e^{-6i\epsilon},\quad b=e^{2i\epsilon}-a.
\]
Use the coherent six-query encoder with any valid fixed split probability \(0\le p\le1\), and a fair choice of plus/minus program orientation. The target is the full channel of \(e^{iH}\), while every unconditional forward query uses \(e^{-i(H+\epsilon P)}\), \(P=\prod_jX_j\). Define
\[
 g_p=a+pfb,\qquad \gamma_p=p|b|^2f(1-f),\qquad c_p=|1-g_p|.
\]
Preserve the ideal-flag protected program coherently and leave the orthogonal split flag unchanged. On a complementary Bell label, allow an arbitrary stochastic logical Pauli correction. Its probabilities may depend on the label and orientation, but not on \(H\) or \(\epsilon\). Write these two arbitrary tables as \(q_+,q_-\).

**Conditional minimax theorem.** Suppose a single ensemble of legal physical Hamiltonians has diagonal program moments \(1/s\) for every balanced label in **each** parity sector, with \(s=\binom{2n}{n}/2\). Then
\[
 \boxed{\inf_{q_+,q_-}\sup_{H\ {\rm physical}}
 \|\mathcal C^{q_+,q_-}_{p,H,\epsilon}-\mathcal U_H^{-1}\|_\diamond
 =c_p+\frac{\gamma_p}{2}
       -\frac{p^2|b|^2G_{\rm ML}}{2D^4}.}
\]
The diamond convention has no factor one half. Radial ML in both orientations attains the right side for every drift, and the identity oracle is a maximizer of that decoder. The minimax statement permits arbitrary non-radial, orientation-dependent Pauli tables.

**Certified corollary.** The joint ensemble hypothesis holds at \(n=5\) and \(n=7\), using the gapped certificates below. Consequently the displayed formula is the exact full physical-family minimax diamond error in this fixed architecture for any valid \(p\) at those sizes.

This does not make five or seven sites first-order-canceling: cancellation requires \(pf=3/4\), which is inadmissible there. For the known admissible odd rings \(n\ge21\), setting \(p=3/(4f)\) would give the corresponding long-ring Pauli minimax converse **if** the joint ensemble hypothesis is established. That all-length existence question remains open.

## 2. General split probability and the radial upper bound

The same encoder's reduced selected-sector residual has total weight \(\gamma_p\); balancing divides that weight by two in each data sector. The plus-to-minus multiplier is \(g_p\) in either orientation: the mirrored selected-minus amplitude is conjugated when acting on plus-to-minus coherence. These formulas follow directly from the two coherent flag amplitudes \(aI+pbQ\) and \(\sqrt{p(1-p)}bQ\).

They obey
\[
 1-|g_p|^2-\gamma_p=p(1-p)f^2|b|^2\ge0,
 \qquad c_p\ge\gamma_p/2.
\]
The latter follows from \(1-|g_p|^2\le2(1-\operatorname{Re}g_p)\le2c_p\). Thus the balanced norm argument is valid for every admissible \(p\), not just the drift-canceling value.

The radial ML Choi eigenvector identity extracts a target component \(G_{\rm ML}/D^4\) from the complementary map. Its residual trace weight becomes
\(\gamma_p-p^2|b|^2G_{\rm ML}/D^4\). The balanced diamond bound is the displayed expression. At identity all unmodified errors are nonidentity Paulis, and the extracted Choi residual is orthogonal to the target, so the equal two-sector Bell input attains the bound.

## 3. A lower bound using Bell overlap, not CP subtraction

For a general table in orientation \(s=\pm\), denote the complementary map's normalized target Bell overlap by
\[
 F_s(H)=\frac{\langle\!\langle V_s|J_{H,q_s}|V_s\rangle\!\rangle}{D^2},
 \qquad \lambda_s=p^2|b|^2F_s(H),\quad
 \sigma_s=\gamma_p-\lambda_s\ge0.
\]
This is an overlap; it is not assumed equal to the maximal subtractable CP weight. That distinction is essential for a norm converse.

Take the fixed maximally entangled input on the full data/reference space. After the ideal inverse, let \(u_+,u_-\) be its normalized sector Bell components, with orthogonal reference supports. Pinch the output error onto their two-dimensional span and its orthogonal complement. On the span, the exact compressed matrix is
\[
 A_H=\begin{pmatrix}
 -\sigma_+/4&(g_p-1)/2\\
 (\bar g_p-1)/2&-\sigma_-/4
 \end{pmatrix}.
\]
The other compression is positive, with trace \((\sigma_++\sigma_-)/4\). Since \(c_p\ge\gamma_p/2\), the two eigenvalues of \(A_H\) have opposite signs, possibly with a zero eigenvalue, and
\[
 \|A_H\|_1=\sqrt{c_p^2+(\sigma_+-\sigma_-)^2/16}\ge c_p.
\]
For completeness, the two-block pinching is the average of identity conjugation and conjugation by the Hermitian unitary \(2\Pi-I\), so trace-norm convexity and unitary invariance prove contraction directly. It therefore gives
\[
 \mathcal E_H(q_+,q_-)
 \ge c_p+\frac{\gamma_p}{2}
       -\frac{p^2|b|^2}{4}(F_+(H)+F_-(H)).
\]
The input is independent of \(H\); the target-dependent pinching is only a mathematical lower-bound operation.

Under the joint uniform-moment ensemble, the general Pauli Bell-overlap identity gives
\(\mathbb E F_s\le G_{\rm ML}/D^4\) separately for either arbitrary table. Averaging the lower bound over the **same physical ensemble** proves the minimax lower bound, matched by radial ML above. A selected-sector CP bound alone does not justify this step.

## 4. Why gapped seeds work simultaneously in both sectors

For odd \(n\), a genuine Gaussian unitary has a raw even-Clifford expansion
\[
 U=\sum_{I\ {\rm even}}u_I\Gamma_I,\qquad u_I\in\mathbb R,
\]
because its exponential generator has real coefficients in the raw Majorana algebra. Since the full Majorana product has square \(-I\), complementary monomials restrict in the two chiral sectors as \(\Gamma_{I^c}=\pm i\Gamma_I\), with opposite signs in the sectors. The paired coefficient masses are consequently \(u_I^2+u_{I^c}^2\) in either sector. Their equality is special to odd \(n\).

A physical periodic Ising Hamiltonian must still be treated carefully: its two sectors correspond to quadratic cycles whose wrap-edge coupling has opposite sign. They are not generally the same quadratic generator. An arbitrary closed-cycle seed cannot simply be declared joint-uniform from one sector's certificate.

A Majorana sign gauge \(\gamma_j\mapsto\varepsilon_j\gamma_j\) changes raw Clifford coefficients only by signs, so it leaves these paired masses invariant. If any cycle edge has zero coupling, the nonzero graph is a path or forest. The wrap sign change can then be removed by a vertex-sign gauge; there is no nonzero cycle flux. Combining gauge invariance with the preceding chiral equality proves that **each gapped physical seed has identical program masses in the two physical parity sectors**.

Signed dihedral images preserve the existence of a zero edge. Therefore a dihedrally averaged ensemble of gapped seeds that is uniform in one sector is exactly uniform in both. Matching-generated seeds can be chosen gapped as well: use a non-perfect matching, with the identity label realized by the empty matching.

## 5. Certified joint ensembles

Frozen data is in [evidence/joint_parity_program_designs.json](evidence/joint_parity_program_designs.json). All nonmatching seeds have at least one exactly zero Majorana edge; this is checked as an exact rational property.

At five sites the certificate has 13 seed orbits: two matching and eleven gapped rational Hamiltonians. At 192-bit ball precision,
\[
 \det A_5=4.97547880863518538340984099750395644779026939473996\times10^{-10}
                 \ \pm\ 5.58\times10^{-61},
\]
\[
 (p_5)_{\min}=0.00120100052639109056419727617288669746118711344059
                 \ \pm\ 3.82\times10^{-51}>1/1000.
\]
At seven sites we reuse the earlier 85 seed orbits after setting the smallest-magnitude coupling of every nonmatching seed to **exactly** zero, and re-solving the changed exact system. Approximate gaps or old weights are not used as proof. The certificate contains 33 matching and 52 gapped rational seed orbits, with
\[
 \det A_7=9.36091669809291890162503031290609148238311335241\times10^{-33}
                 \ \pm\ 5.29\times10^{-81},
\]
\[
 (p_7)_{\min}=4.9390572008872218157235483735161093365649831785150\times10^{-5}
                 \ \pm\ 7.38\times10^{-55}>1/25000.
\]
As before, exact weights are defined by \(p=A^{-1}b\), where \(b_{\mathcal O}=|\mathcal O|/|\mathcal S|\). Invertibility and strict positivity are certified; exact column normalization proves that the weights sum to one. Dihedral averaging and the gap/gauge lemma supply the joint uniform moments. This is a computer-assisted existence proof, not sampled approximate uniformity.

## 6. Reproducibility, checks and limits

Run with NumPy/SciPy/python-flint:

1. `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_joint_parity_design.py`
2. `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_diamond_pinching.py`

The first rebuilds and certifies both positive exact orbit systems, including the exact gap condition. The second independently constructs both physical parity blocks and checks the gapped parity-mass identity on every dihedral image at three and five sites. It also builds complete balanced Kraus channels on a three-site physical model for five Hamiltonians, three valid split probabilities, three nonzero drifts and radial/random orientation-dependent corrections: 90 cases. It checks completeness, the full compressed error matrix, positivity/trace of the orthogonal compression, the pinching bound, and radial attainment on the Bell input. These finite checks support the analytic identities; they are not treated as a numerical diamond-norm optimization.

The [EUI manuscript robustness appendix](https://arxiv.org/html/2506.20570v1) concerns a broader perturbation study. The noise promise and fixed architecture here are explicitly narrower. Reference-assisted channel norms are standard tools; see [Watrous, The Theory of Quantum Information, Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/). The joint-ensemble and gapped-parity arguments here are stated explicitly rather than attributing new primitives to pinching. No unrestricted-query or literature-wide novelty conclusion is drawn.

The remaining high-value question is an analytic joint uniform ensemble for admissible long rings. Gapped seed families reduce this to a single-sector moment problem while guaranteeing parity compatibility. A general construction would turn the existing long-ring radial formula into a full Pauli minimax diamond theorem; the five/seven-site certificates alone do not establish it.

The [principal-minor criterion and mirror obstruction](THEORY_PROGRAM_MINOR_OBSTRUCTION.md) characterizes the full uniform-mass condition through Majorana rotation minors. It proves that convex mixtures of single perfect-mirror segments cannot satisfy even the degree-two conditions for any odd n >= 5; this excludes that proposed seed family, not general physical ensembles.
