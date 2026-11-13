# Theory audit: exact one-slot Pauli inversion

Let $\mathcal S$ be a finite set of non-identity Pauli operators and
\[
H(\theta)=\sum_{P\in\mathcal S}\theta_P P,
\qquad
U_\theta(t)=e^{-itH(\theta)}.
\]
Let $V$ be a Hermitian Pauli operator, so $V^2=I$. Partition the support into
\[
\mathcal S_+(V)=\{P\in\mathcal S: VP=PV\},
\qquad
\mathcal S_-(V)=\{P\in\mathcal S: VP=-PV\}.
\]

## Lemma

For arbitrary real coefficients $\theta_P$ and all real $t$,
\[
V U_\theta(t)V=U_\theta(t)^\dagger
\]
if and only if every support element anticommutes with $V$, that is
$\mathcal S_+(V)=\varnothing$.

## Proof

Conjugation by $V$ acts termwise,
\[
V H(\theta)V
 =\sum_{P\in\mathcal S_+(V)}\theta_P P
  -\sum_{P\in\mathcal S_-(V)}\theta_P P.
\]
Therefore
\[
V U_\theta(t)V=e^{-itV H(\theta)V},
\qquad
U_\theta(t)^\dagger=e^{+itH(\theta)}.
\]
If every term anticommutes, then $V H(\theta)V=-H(\theta)$ and the two expressions agree.

Conversely, assume equality for all coefficients and all $t$. Differentiating at $t=0$ gives
$V H(\theta)V=-H(\theta)$. The Pauli operators are linearly independent, and the coefficients are independent, so each supported term must have commutation sign $-1$.

## Scope

This lemma proves the exact condition implemented by the mode='dagger' branch of the Pauli mapping search. It applies to a one-slot protocol whose only free operation is Pauli conjugation by V.

For the other one-slot targets, let y(P) be the parity of Y factors in P. Transpose requires the commutation character chi_V(P)=(-1)^y(P), while complex conjugation requires chi_V(P)=-(-1)^y(P). The corresponding exact checks are implemented by certify_one_slot_pauli_transpose and certify_one_slot_pauli_conj.

These one-slot certificates do not establish optimality among multi-slot combs or ancilla-assisted protocols.

The repaired type-1.2 classifier is recorded in commit b270a30ec9099613c6f4ddba4f99cc215b05e68b.

## Certification boundary

`pauli_gate_solutions` samples a finite random set of Hamiltonian parameters and accepts candidates using a floating-point `torch.isclose` test. That procedure is a finite numerical check, not an exact certificate for all coefficients and times. A candidate found this way must be reported as a conjectured protocol until it is covered by an algebraic proof or a certified symbolic identity check.

For all three one-slot targets, the repository now supplies algebraic certificates. Multi-slot searches still need an explicit symbolic or representation-theoretic certification step before claiming exactness or optimality.
