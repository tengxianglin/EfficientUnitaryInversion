# Parity obstruction for perfect-matching atoms of an even-cycle exponential

Date: 2026-11-26.

## Theorem

Let (N=4m+2), with vertices (0,1,ldots,N-1) on the cycle (C_N). Let
[
A(c)_{j,j+1}=2c_j,qquad A(c)_{j+1,j}=-2c_j
]
(cyclic indices), with all other entries zero and arbitrary real couplings (c_j). Let (M) be a perfect matching, (P_M) its endpoint-swap permutation matrix, and
[
D=operatorname{diag}(1,-1,1,-1,ldots,1,-1),qquad R_M=P_MD.
]

**Theorem.** If
[
R_M=e^{A(c)}
]
for some real coupling vector (c), then every matching edge joins opposite cycle bipartition classes: one endpoint is even and the other is odd.

Equivalently, for (N=4m+2), every perfect-matching atom containing even-even or odd-odd pairs is unreachable by the fixed-cycle exponential family, for every real coupling vector, including vectors with zero entries.

## Proof

Write (p) for the fixed-point-free involution underlying (P_M). Suppose (R_M=e^A), where (A=A(c)) is skew-symmetric and supported on cycle edges. Since a matrix commutes with its exponential,
[
AR_M=R_MA,
qquad R_M A R_M^{-1}=A.
]
Conjugation by the signed permutation (R_M=P_MD) permutes matrix-entry locations according to (p), changing only their signs. Hence the support graph
[
G_A=igl(V,{{j,j+1}:c_j
e0}igr)
]
is invariant under (p).

Also, (A) is block diagonal across the connected components of (G_A), so (e^A=R_M) is block diagonal across those same components. Because (R_M) maps each basis vector (e_j) to a signed copy of (e_{p(j)}), the permutation (p) must preserve each connected component individually. An isolated vertex would therefore be fixed by (p), which is impossible for a perfect matching.

There are two cases.

1. **The support graph is a proper subgraph of the cycle.** Every nontrivial connected component is a path. The restriction of (p) to such a component is a graph automorphism of a path. The only path automorphisms are the identity and reversal. The identity has fixed vertices, and reversal of an odd number of vertices has a fixed middle vertex. Thus each component has an even number (L) of vertices and (p) acts by reversal. In path coordinates (0,ldots,L-1), reversal pairs (j) with (L-1-j). Since (L-1) is odd, each pair has opposite parity.

2. **The support graph is the full cycle.** Then (p) is a fixed-point-free involutive automorphism of (C_N), hence a dihedral symmetry. A fixed-point-free reflection has the form (p(j)=a-jpmod N) with (a) odd; it swaps parity. The only nontrivial involutive rotation is the half-turn (p(j)=j+N/2pmod N). Because (N=4m+2), the shift (N/2=2m+1) is odd, so the half-turn also swaps parity. Reflections with even (a) have fixed vertices and are excluded.

In either case every matched pair joins opposite parity classes. This proves the theorem. (square)

## Exact consequence for the N=42 SO(42) matching ensemble

For (N=42=4cdot10+2), there are
[
41!!=13{,}113{,}070{,}457{,}687{,}988{,}603{,}440{,}625
]
perfect matchings in total. The number of bipartite perfect matchings between the 21 even and 21 odd vertices is exactly
[
21!=51{,}090{,}942{,}171{,}709{,}440{,}000.
]
Therefore at most
[
rac{21!}{41!!}
=rac{262144}{67282234305}
=3.896184523416147ldots	imes10^{-6}
]
of the uniform perfect-matching support can be physically reachable. Equivalently, the uniform matching measure assigns at least
[
oxed{
1-rac{21!}{41!!}
=rac{67281972161}{67282234305}
=0.9999961038154765ldots
}
]
of its mass to atoms proved unreachable by the fixed 42-cycle exponential family. The exact number of such same-parity matchings is
[
41!!-21!=13{,}113{,}019{,}366{,}745{,}816{,}894{,}000{,}625.
]

This is a quantitative statement about the **particular uniform perfect-matching representation** of the unrestricted (SO(42)) moment ensemble. It is not a lower bound on the distance between moment vectors, and it does not exclude another positive measure supported on physical cycle exponentials that reproduces the same complete moments.

## Why the congruence condition matters

The conclusion is specific to (Nequiv2pmod4). At (N=4), the same-parity antipodal matching (M={(0,2),(1,3)}) is reachable. Define
[
K=egin{pmatrix}
0&1&0&1\-1&0&1&0\0&-1&0&-1\-1&0&1&0
end{pmatrix},
qquad A=racpi2K.
]
Then (K^T=-K), (K^3=-4K), and
[
e^A=I+rac12K^2=P_MD,
]
which corresponds to cycle couplings
[
(c_0,c_1,c_2,c_3)=left(racpi4,racpi4,-racpi4,-racpi4ight).
]
Thus the modulo-four hypothesis cannot be dropped.

## Reproducibility and scope

- Exact verifier: `verify_cycle_matching_atom_parity_obstruction.py`.
- Machine-readable evidence: `evidence/cycle_matching_atom_parity_obstruction_n42.json`.
- Workflow: `.github/workflows/eui-cycle-matching-parity-obstruction.yml`.
- The verifier exhaustively enumerates perfect matchings for (N=4,6,8,10), checks the exact total and bipartite counts, recomputes the (N=42) integer/fractional bounds, and verifies the (N=4) counterexample by exact integer matrix identities.

**Not proved:** whether the balanced-slice target lies in the closed convex hull of the full 42-cycle exponential family; whether any or all cross-parity matching atoms are reachable; or any Choi/diamond operational bound. The result only removes a very large portion of the unrestricted matching ensemble from physical reachability.
