# Three-query Pauli obstruction for fully fielded odd Ising cycles

Consider an odd cycle of length $L\geq 3$ with independent real coefficients in
$$
H(x,h)=\sum_{j=0}^{L-1}x_j Z_j Z_{j+1\bmod L}+\sum_{j=0}^{L-1}h_j X_j,\qquad U=e^{-iH(x,h)}.
$$
A query is an unconditional forward call to the same $U$. We first analyze circuits on the system alone with fixed tensor-product Pauli gates between and around calls. Channel equality allows a global phase.

**Result.** No three-query Pauli circuit inverts this full family exactly. Every Pauli circuit for this family requires at least five queries. The obstruction works for every odd $L$, with no assumption of translation symmetry. The earlier three-query lower bound for general fixed-order combs still applies. The argument here leaves the three-query question open for combs with arbitrary intervening operations.

## The three sign classes

Moving the fixed Pauli gates to the right writes any three-query word as a product of three evolutions from Pauli conjugations of $H$, followed by a fixed Pauli. At $H=0$ this final Pauli must be scalar. Discard it. The remaining evolutions have determinant one because each toggled Hamiltonian is traceless. Exact equality of channels implies equality of these matrices with $U^\dagger$ in a neighborhood of zero, since their relative scalar is a continuous $2^L$-th root of unity equal to one at zero.

The first derivatives in the independent coefficients require the three signs of every generator to sum to $-1$. Therefore each generator is plus in exactly one slot. Assign it the color 1, 2 or 3 of that slot. For each slot the product of its signs on the $L$ edges is plus. This follows by conjugating the operator identity $\prod_j Z_jZ_{j+1}=I$. Since $L$ is odd, each color occurs an odd number of times among the edges. In particular colors 1 and 3 both occur.

## A coefficient on the shortest anticommutation path

The anticommutation graph on the $2L$ generators is a cycle. A field anticommutes with exactly its two incident edges, and the fields commute with one another, as do the edges. Take a shortest path between the color-1 set and the color-3 set, oriented from 1 to 3. It has $k$ vertices with $2\leq k\leq L+1$. Every interior vertex has color 2, and the path is induced. Set all coefficients off the path to zero, and denote the remaining generators by $P_1,\dots,P_k$ with coefficients $u_1,\dots,u_k$.

These path Paulis are projectively independent. Their field factors are distinct binary $X$ directions, while their edge factors form a proper subset of the cycle edges and hence are independent binary $Z$ directions. Only the full cycle has a nonempty edge subset with zero binary sum. The $2^k$ ordered monomials are therefore pairwise distinct up to phase and linearly independent in the Pauli basis. The relations $P_j^2=I$, anticommutation for adjacent indices and commutation otherwise allow every word to be reordered into these monomials. Consequently the substitution $P_j\mapsto i\gamma_{j-1}\gamma_j$ extends to a unital algebra homomorphism for Majoranas $\gamma_0,\ldots,\gamma_k$ with $\{\gamma_p,\gamma_q\}=2\delta_{pq}I$. The substituted generators satisfy the same relations.

Apply the substitution to the claimed matrix identity. On the span of the Majoranas, conjugation by one substituted evolution acts as the exponential of a tridiagonal generator. In the ordered Majorana basis, generator $j$ gives entry $2$ at row $j-1$, column $j$, and entry $-2$ in the reverse direction, before multiplication by the corresponding signed $u_j$. For example $[\gamma_{j-1}\gamma_j,\gamma_j]=2\gamma_{j-1}$.

Extract the coefficient of $u_1\cdots u_k$ in row 0, column $k$ of the resulting product of adjoint matrices. A term of degree $k$ can connect these indices only by traversing the whole path monotonically. The first, second and third exponentials thus contribute consecutive chunks of sizes $a,b,c$ with $a+b+c=k$. Relative to the factor $(-2)^k/k!$, the proposed circuit has coefficient
$$
\sum_{a+b+c=k}\binom{k}{a,b,c}(-1)^{M(a,b,c)},
$$
where $M$ counts the positions whose path color equals the slot of their chunk. The target inverse, a single exponential with every sign negative, has normalized coefficient $1$.

When $b>0$, the parity of $M$ equals that of $b$. For the left endpoint, assigning it to the first chunk adds one match, while including it in the middle chunk removes one from the initial count $b$. The right endpoint gives the same parity adjustment, so the two changes cancel modulo two. When $b=0$, the sign is plus unless the entire path lies in slot 1 or entirely in slot 3. The sum is therefore $(1-1+1)^k-2-2=-3$. The unequal coefficients rule out the identity.

The commuting restriction in [the heralded converse](THEORY_HERALDED_COMMUTING.md) rules out zero, one and two queries even for general fixed-order combs. For any Pauli circuit with an even number of calls, the same first-derivative argument gives a sum of an even number of signs and hence cannot give $-1$. These facts give the five-query Pauli lower bound.

A five-site example shows why pairwise checks alone can miss the obstruction. Give the edges cyclic colors $(1,2,3,2,2)$ and all fields color 2. Each slot's edge signs have even parity and are realizable by Pauli conjugation, since an even-parity sign pattern on the cycle is a cut. The field signs can be set independently using local $Z$ factors. The linear equations hold, and no anticommuting pair has colors 1 and 3. The second-order product residual is $-2[A,C]$ when the three sign classes are written with generators $-iH$ and class sums $A,B,C$, so it vanishes for this example. The shortest color-1 to color-3 path has five vertices, and the coefficient argument above gives a fifth-degree witness.

## Reproduction and manuscript scope

The following integer calculation checks the coefficient formula for path sizes 2 through 20. The analytic argument above covers every size.

~~~python
from math import comb

for length in range(2, 21):
    colors = (1,) + (2,) * (length - 2) + (3,)
    coefficient = 0
    for a in range(length + 1):
        for b in range(length - a + 1):
            c = length - a - b
            slots = (1,) * a + (2,) * b + (3,) * c
            matches = sum(slot == color for slot, color in zip(slots, colors))
            coefficient += (-1) ** matches * comb(length, a) * comb(length - a, b)
    assert coefficient == -3, (length, coefficient)
print("Path sizes 2 through 20: normalized coefficient -3")
~~~

The construction in [Mo, Lin and Wang, Section IV and Appendix A](https://arxiv.org/html/2506.20570v1) achieves three calls after two neighboring transverse fields are removed from the seven-site example. The full-field obstruction uses the continuous anticommutation cycle, which depends on including all field terms as independently tunable generators. The restricted and full-field query counts can therefore differ within the Pauli ansatz. A next step is to apply the ray spectrum converse to a fully fielded Hamiltonian and check whether it rules out three calls without assuming Pauli controls.
