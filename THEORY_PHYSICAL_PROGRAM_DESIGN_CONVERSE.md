# A physical ensemble closes the five-site non-radial Pauli CP gap

The [matching-ensemble obstruction](THEORY_NONRADIAL_MATCHING_COUNTEREXAMPLE.md) ruled out one candidate recovery, but left the whole non-radial Pauli class open. A computer-assisted physical ensemble now gives a matching converse for that class's **uniform target-unitary CP component** at five sites.

This does not optimize the full diamond norm, arbitrary CPTP correction, or coherent data-program recovery. Five sites are a complementary-map diagnostic; they do not meet the long-ring six-query first-order-cancellation threshold.

## 1. Exact quantity and result

Fix the existing encoder and selective architecture. Preserve the ideal-flag protected program coherently, leave the orthogonal split flag unchanged, and on a complementary Bell label \(R\) apply \(R^\dagger\) followed by a logical Pauli \(T\), selected with arbitrary conditional probabilities \(q_R(T)\). The probabilities may be fully non-radial, but cannot depend on the unknown Hamiltonian. Initially allow all 126 balanced Pauli hypotheses. Allowing additional Pauli hypotheses outside the balanced span does not improve the converse below.

At \(n=5\), let \(D=16\), \(s=126\), and let \(V\) be the selected-sector inverse. Denote by \(J_{H,q}\) the unnormalized Choi matrix of the recovered complementary map, with the drift-dependent factor \(pb\) omitted. Thus \(\|\operatorname{vec}V\|^2=D\). Define
\[
 \kappa_H(q)=\sup\{\kappa\ge0:
 J_{H,q}-\kappa|V\rangle\!\rangle\langle\!\langle V|\succeq0\},
 \qquad K_5=\sup_q\inf_{H\ {m physical}}\kappa_H(q).
\]

**Computer-assisted theorem.** In this stochastic Pauli correction class,
\[
 \boxed{K_5=\frac{G_{\rm ML}}{D^4}
              =\frac{995}{344064},\qquad G_{\rm ML}=\frac{3980}{21}.}
\]
Radial ML attains the lower bound. The upper bound holds for every non-radial probability table, rather than only for a frozen candidate or tested table.

The radial cross-effect proof gives the lower bound directly at the complementary-map level. Its Choi identities are independent of the split probability. The restriction \(n\ge21\) in the drift-canceling protocol is needed for the chosen split probability to be admissible, not for these five-site Choi identities.

## 2. A general ensemble converse

Expand \(V=\sum_{T\in\mathcal S}v_TT\), with \(\sum_T|v_T|^2=1\), and put
\[
 G_T(q)=\sum_{R\notin\mathcal S}a_{|RT|/2}^2q_R(T).
\]
The previous support calculation supplies the Bell expectation identity
\[
 \frac{\langle\!\langle V|J_{H,q}|V\rangle\!\rangle}{D^2}
 =D^{-4}\sum_T|v_T|^2G_T(q).
\]
Any target component satisfies \(\kappa_H(q)\) no larger than this Bell expectation. Suppose a physical oracle ensemble has probabilities \(p_j\) and exact diagonal program moments
\[
 \sum_jp_j|v_T(H_j)|^2=\frac1s
       \quad\text{for every }T\in\mathcal S.
\]
Averaging the Bell upper bound gives, for every probability table,
\[
 \inf_H\kappa_H(q)
 \le\frac1{D^4s}\sum_R\sum_Ta_{|RT|/2}^2q_R(T)
 \le\frac1{D^4s}\sum_R\max_Ta_{|RT|/2}^2
 =\frac{G_{\rm ML}}{D^4}.
\]
For five sites, the integer row-max sum is 23880, and \(23880/126=3980/21\). Extra correction hypotheses outside \(\mathcal S\) have zero Bell overlap by the program-support identity, so they cannot increase this upper bound.

Crucially, this is an ensemble of **legal physical Hamiltonians**, not a uniform prior over program-basis labels whose physical realizability is unknown. Only diagonal coefficient moments are uniform. No unitary design or off-diagonal program-moment property is claimed.

## 3. A certified physical ensemble

The frozen certificate contains 126 atoms:

- 43 matching-generated Pauli blocks, each realized by a matching of the physical ten-Majorana cycle with disjoint coefficients \(\pi/2\);
- 83 Hamiltonians with explicit rational local fields and nearest-neighbour Ising couplings.

The rational Hamiltonians use the original convention
\(H=\sum_jh_jX_j+\sum_jJ_jZ_jZ_{j+1}\), with indices modulo five. The verifier applies sitewise Hadamards and restricts to even occupation parity, giving local \(Z\) fields and \(XX\) edges, as in the existing verification code.

Let \(A\) be the exact real \(126\times126\) matrix
\[
 A_{Tj}=|\operatorname{Tr}(T^\dagger e^{iH_j})/D|^2,
\]
with matching atoms represented by their exact unit coordinate columns. Define the ensemble weights **implicitly and exactly** by
\[
 p=A^{-1}(\mathbf1/126).
\]
The weights need not be rational. Their definition uses the exact matrix exponentials of rational-input Hamiltonians; stored floating-point optimization weights are not used in the proof.

The verifier encloses all matrix exponentials and entries of \(A\) with complex/real ball arithmetic at 192-bit precision, and then certifies:

1. the determinant enclosure excludes zero;
2. the ball solution of \(Ap=\mathbf1/126\) has every component strictly greater than \(7/100000\).

The determinant enclosure obtained is
\[
 \det A=2.63008012122552322656597778645996988889622760384\times10^{-64}
          \ \pm\ 9.28\times10^{-112}.
\]
The smallest weight is enclosed by
\[
 p_{\min}=7.0609945672286086594427106219259411073916165959797\times10^{-5}
          \ \pm\ 8.59\times10^{-55}.
\]
Therefore the true exact system has a unique strictly positive solution. Every column sums to one exactly, because its physical unitary lies in the balanced program span and has unit Hilbert--Schmidt norm under the Pauli normalization. Summing the exact linear equations yields \(\sum_jp_j=1\). Thus these exact weights define a probability ensemble with the required **exact**, not approximately uniform, diagonal moments.

This establishes the hypothesis of the ensemble converse and closes the target-component gap. The proof relies on interval-certified invertibility and positivity, not on an LP feasibility tolerance. Interval residual checks are included as sanity checks; they are not used in place of the invertibility/solution enclosure argument.

## 4. Discovery, reproducibility and boundaries

The discovery search used the matching family, seeded physical Hamiltonians, the earlier rational witness and its spatial symmetry images, and two rounds of adversarial Hamiltonian search. Initial Bell-game upper bounds were about 1.0206152 and then 1.0009451 times the radial value. An enriched pool admitted a positive square uniform-moment representation. Atom coefficients were rounded to fixed rationals and the exact linear system was re-certified from those rational inputs. No optimizer convergence or floating feasibility flag is needed for verification.

Frozen atoms: [evidence/physical_uniform_program_design_n5.json](evidence/physical_uniform_program_design_n5.json). Verifier: [verify_ising_uniform_program_design.py](verify_ising_uniform_program_design.py).

Run `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_uniform_program_design.py`. Dependencies in this run: NumPy 2.3.5, SciPy 1.17.0 (shared helpers) and python-flint 0.9.0. The verifier rebuilds the physical basis, checks all matching atoms are realizable, constructs rational Hamiltonians, certifies the full matrix and positive solution, and checks the integer row-max converse. It does not require an LP or SDP optimizer. See the primary [python-flint matrix documentation](https://python-flint.readthedocs.io/en/latest/arb_mat.html) for the ball linear-system interface.

The [manuscript robustness appendix](https://arxiv.org/html/2506.20570v1) motivates structured noise comparisons, while this calculation concerns the explicitly narrower complementary-map target-component figure. No literature-wide originality or publication-readiness conclusion follows solely from this certificate.

The theorem rules out improving this five-site **uniform CP target component** by stochastic Pauli reweighting alone. It does not rule out a better full diamond error with a different decomposition, non-Pauli CPTP corrections, coherent program processing, or a different encoder. It also does not prove the same converse for the admissible long rings \(n\ge21\).

The next high-value theoretical question is whether a physical ensemble with uniform diagonal program moments exists for general odd rings, preferably by an analytic construction. The ensemble lemma would then upgrade radial ML to an all-Pauli CP converse there without enumerating exponentially many labels. If that construction fails, the alternative is to exploit the obstruction or leave the Pauli correction class.
