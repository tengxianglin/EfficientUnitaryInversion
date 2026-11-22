# Choi fidelity does not certify a uniform diamond-norm guarantee

Date: 2026-11-22

## Purpose

The robustness discussion in the inspected arXiv v1 Appendix B reports finite-sample averages of Choi-state fidelity. This note records a precise limitation: high average Choi fidelity, by itself, cannot imply a uniform worst-case diamond-norm guarantee. The counterexamples below are mathematical statements about channels; they do not claim that the bad channels have already been realized by the particular EUI Hamiltonian family.

## Definitions

For a unitary (U\in U(d)), let
\[
\mathcal U(\rho)=U\rho U^\dagger,
\qquad
|U\rangle=(I\otimes U)|\Phi_d\rangle,
\qquad
|\Phi_d\rangle=\frac1{\sqrt d}\sum_{j=1}^d|j\rangle|j\rangle.
\]
The normalized Choi state is (J(\mathcal U)=|U\rangle\langle U|). For two unitary channels,
\[
F_{\rm Choi}(\mathcal U,\mathcal V)
=|\langle U|V\rangle|^2
=\frac{|\operatorname{Tr}(U^\dagger V)|^2}{d^2}.
\]
Use the unhalved diamond norm, so the distance between two perfectly distinguishable channels is (2).

## Counterexample 1: Choi fidelity tends to one while diamond distance is maximal

For every (d\ge2), set
\[
W_d=I_d-2|d\rangle\langle d|
=\operatorname{diag}(1,\ldots,1,-1).
\]
Then
\[
F_{\rm Choi}(\mathcal I,\mathcal W_d)
=\frac{|\operatorname{Tr}W_d|^2}{d^2}
=\frac{(d-2)^2}{d^2}
\longrightarrow1
\quad(d\to\infty).
\]
Nevertheless, for
\[
|\psi\rangle=\frac{|1\rangle+|d\rangle}{\sqrt2},
\]
the outputs under (I_d) and (W_d) are the orthogonal states
\[
\frac{|1\rangle+|d\rangle}{\sqrt2},
\qquad
\frac{|1\rangle-|d\rangle}{\sqrt2}.
\]
Their trace-norm distance is (2), so
\[
\boxed{\|\mathcal I-\mathcal W_d\|_\diamond=2}
\]
(the upper bound (2) holds for the difference of any two channels). Thus no dimension-independent function (g(F)\to0) as (F\to1) can upper-bound the diamond distance using normalized Choi fidelity alone.

## Counterexample 2: mean Choi fidelity tends to one while worst-case error stays maximal at fixed dimension

Fix (d=2). Consider an ensemble of implemented channels that equals (\mathcal I) with probability (1-\varepsilon) and (\mathcal Z), where (Z=\operatorname{diag}(1,-1)), with probability (\varepsilon). Relative to the ideal inverse (\mathcal I),
\[
\mathbb E[F_{\rm Choi}]
=(1-\varepsilon)\cdot1+\varepsilon\cdot0
=1-\varepsilon\longrightarrow1.
\]
But the worst-case channel error over the ensemble is
\[
\max\{\|\mathcal I-\mathcal I\|_\diamond,
\|\mathcal I-\mathcal Z\|_\diamond\}=2
\]
for every (\varepsilon>0). Hence even at fixed dimension, an average over random instances cannot imply a uniform-over-instances guarantee without additional tail or support assumptions.

## Consequence for EUI claims

The inspected Appendix B Monte Carlo averages can support an empirical statement about the sampled distribution and sample size. They do not, without an additional theorem, support any of the following:

1. a worst-case-over-Hamiltonians bound;
2. a worst-case-over-input-states bound;
3. a dimension-independent conversion from Choi fidelity to diamond distance;
4. a tail guarantee for rare but severe failures.

A rigorous operational claim needs an explicit additional hypothesis or certificate: for example, a uniform bound on the relevant channel difference, a dimension-aware Choi-to-diamond estimate with all normalization factors, or a distributional tail bound that matches the stated quantifiers. The two counterexamples show why an average-fidelity number alone is insufficient.

## Reproducibility

The derivations are closed-form and require no numerical experiment. The first example is valid for every integer (d\ge2); the second is a two-channel distribution at (d=2).
