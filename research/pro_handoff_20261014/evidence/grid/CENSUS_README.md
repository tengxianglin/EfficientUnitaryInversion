# Independent exact grid census

This result was produced by scripts/independent_exact_grid_verifier.py.
The verifier does not import verify_grid_examples.py or any repository
analysis helper.

## 中文结论

字面上的“穷尽所有 alternating form”分类**被反驳**：零 form（rank 0）
的 16 个 q-refinement 都让六条线 commuting 且 `T_L=W`（16 个标签），
不是 `|T_L|=10`。不过 rank 0 不能嵌入 proper 的三量子比特 Pauli 空间。
限制到可实现的 rank 2/4 后，1024 个 case 中的 1008 个全部满足该分类：
全 commuting 当且仅当 `|T_L|=10` 且有 restricted-character one-Pauli
witness；其余均为 `T_L=W`，并且饱和时精确 `lambda=2^(rank/2)`。

## Model

The nine fixed coefficient vectors are the rank-one tensors

    r_i tensor c_j, with r_i,c_j in {(1,0),(0,1),(1,1)},

flattened in the basis
(e0 tensor f0, e0 tensor f1, e1 tensor f0, e1 tensor f1) of
W = F_2^4. They are

~~~text
0001 0010 0011
0100 1000 1100
0101 1010 1111
~~~

The six lines are ordered as row0, row1, row2, col0, col1, col2.

For a proper grid, the four corner vectors must be independent: a subspace of
dimension at most 3 contains at most 7 nonzero vectors, so it cannot contain
nine distinct nonzero grid entries.  On a 4-dimensional subspace of the
6-dimensional physical Pauli symplectic space, an alternating restriction can
therefore have rank only 2 or 4; rank 0 is retained here solely to test the
literal abstract statement.

For every one of the 64 alternating 4x4 forms, all 16 compatible quadratic
refinements are enumerated. Thus the raw population is exactly 1024 cases.
The phase lift is the explicit Z4 cocycle

~~~text
phi(u,v) = q(u) + q(v) - q(u+v) + 2 u^T C v  (mod 4),
~~~

where C_ii=q(e_i), C_ij=omega(e_i,e_j) for i>j, and C_ij=0 for
i<j. Associativity, involution, commutator, and transpose
anti-automorphism identities are checked exactly.

## Results

- 64 alternating forms × 16 refinements = **1024 raw cases**.
- The grid automorphism group (GL(2,2) x GL(2,2)) semidirect C2 has order
  **72**, giving **44 equivalence classes**.
- Alternating-form ranks: rank 0: 1 form, rank 2: 35 forms, rank 4: 28 forms.
- The all-six-lines-commuting condition selects exactly two alternating forms:
  mask 0 (rank 0) and mask 12 (rank 4); each has 16 refinements.
- |T_L|=10 for **16 cases** and |T_L|=16 for **1008 cases**.
- Exact LCU lambda histogram: 1: 32 cases, 2: 560 cases, 4: 432 cases.
- The proposed classification fails for **16 abstract rank-0 cases**, in
  three grid-automorphism orbits.
- After excluding rank 0, the classification passes all **1008 rank-2/rank-4
  cases**, which are the forms realizable as restrictions of a nondegenerate
  three-qubit Pauli symplectic form on a proper four-dimensional span.

## Classification decision

The literal all-forms statement is false. A representative counterexample is

~~~text
omega = 0_(4x4), q = 0
~~~

All six grid lines commute, but symbolic powers give T_L=W (16 labels), not
10. The restricted-character equations have the one-character solution
ell=0 and exact lambda 1; this does not repair the failed |T_L|=10
claim. Rank 0 is not a physical proper three-qubit embedding because a
four-dimensional totally isotropic subspace cannot fit inside the
six-dimensional nondegenerate symplectic space.

The refined physical statement supported by this census is:

~~~text
For every proper three-qubit-realizable rank-2 or rank-4 form/refinement,
all six lines commute iff |T_L|=10 and a restricted-character
one-Pauli witness exists; otherwise T_L=W. In the saturated cases,
the exact normalized Pauli-conjugation LCU optimum is
lambda_T = 2^(rank(omega)/2).
~~~

Here “one-Pauli witness” means a character ℓ in the restricted character
dictionary. For rank 2 or rank 4 physical embeddings, every such restricted
character has an ambient Pauli extension; rank 0 is retained only as an
abstract algebraic counterexample.

The lambda statement is scoped to the normalized Pauli-conjugation LCU
dictionary. It is not a lower bound for arbitrary quantum combs, and the
census does not prove a new protocol mechanism.

## Files

- independent_grid_certificates.json: all 44 class certificates plus all
  1024 raw-case summaries and counterexample records.
- scripts/independent_exact_grid_verifier.py: standalone verifier.
- docs/research/eui_grid_examples_20260905/CHATGPT_PRO_EXACT_CENSUS_PROMPT.md:
  direct handoff prompt for an independent Pro audit.

Reproduce:

~~~bash
/opt/anaconda3/bin/python scripts/independent_exact_grid_verifier.py \
  --output results/eui_grid_exact_20260905/independent_grid_certificates.json
~~~

Certificate SHA-256:

    fd7d62aeeed96f72bdf740c9f9aeed45bf00f5f9c78fc4417bdada5e44c9cf74

No random tests and no floating-point optimization are used.

An additional self-contained cross-check (written independently at runtime and
not importing this verifier) reproduced the exact counts
`|T_L|: 10 -> 16, 16 -> 1008`, `lambda: 1 -> 32, 2 -> 560, 4 -> 432`, and
the same 16 rank-0 counterexamples.
