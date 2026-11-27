# EUI manuscript/research audit — Run 65 (2026-11-28)

## Repository and issue inspection

- Starting main HEAD: ba4fb90d2faf14d8933fb01cf65273b3bb855de2 (Run 64 all-quartic audit).
- Confirmed the repository is writable and main is the default branch.
- Inspected the latest 12 commits, all open Issues, recent Issue updates, the complete Issue #7 discussion, the Run 64 all-1,440-quartic audit, the all-order incidence note, the perfect-matching construction, the physical-matching reachability theorem and verifier, and the current manuscript/source tree.
- Open scientific tracks include #7 (physical reachability/full-cycle convex hull), #5 (finite-pool versus full-family gap), #6 (Appendix B noise normalization and QuAIRKit reproduction), and #3 (classifier/runtime audit). Issue #7 remains the highest-leverage mathematical blocker.
- The tracked tree contains 1,317 entries and no .tex, .bib, .bbl, .sty, .cls, or .pdf manuscript source. No formal manuscript-body edit is claimed.

## New exact combinatorial result

The existing physical-matching theorem proves that, for N=4m+2 >= 6, every signed perfect-matching atom R_M=P_M D that is reachable as exp(A(c)) on the physical cycle must contain at least two edges of that cycle.

I derived and verified the complete distribution of
X_N(M) = |M intersect E(C_N)|
under a uniformly random perfect matching of K_N.

For 0 <= k <= N/2, the number of k-edge matchings in the cycle is
m_k(C_N) = N/(N-k) * binom(N-k,k) (with m_0=1).
The binomial moments of X_N, summed over all perfect matchings, are
B_k = m_k(C_N) * (N-2k-1)!!.
Binomial inversion gives the exact count
C_j = sum_{k=j}^{N/2} (-1)^(k-j) binom(k,j) B_k.

At N=42:
- total perfect matchings: 41!! = 13113070457687988603440625;
- exactly zero cycle edges: 4649413893260078385217444;
- exactly one cycle edge: 4878759342216072267293262;
- zero or one cycle edge: 9528173235476150652510706;
- exact uniform mass with X_42 <= 1:
  9528173235476150652510706/13113070457687988603440625
  = 0.7266164904871636....

Because every physically reachable matching atom has X_42 >= 2, at least 72.66% of the unrestricted uniform matching representation is individually unreachable. Any probability measure supported on physically reachable matching atoms has TV distance at least this fraction from the uniform matching measure on the discrete matching space. This is a measure-support statement, not a channel or program-label bound.

For every fixed k, the factorial moments satisfy
E[(X_N)_k] = k! m_k(C_N) (N-2k-1)!!/(N-1)!! -> 1
as even N tends to infinity. Hence X_N converges in distribution to Poisson(1), and the excluded mass P(X_N <= 1) tends to 2/e.

## Verification

Added:
- THEORY_PERFECT_MATCHING_CYCLE_EDGE_DISTRIBUTION_N42.md
- verify_perfect_matching_cycle_edge_distribution.py
- evidence/perfect_matching_cycle_edge_distribution_n42.json
- .github/workflows/eui-perfect-matching-cycle-edge-distribution.yml

The dependency-free exact verifier:
- recomputes the N=42 distribution by integer binomial inversion;
- checks all binomial-moment reconstruction identities and the total 41!!;
- independently enumerates every perfect matching for N=4,6,8,10,12,14 and exactly matches the formula's full distribution;
- freezes the complete 22-entry N=42 count distribution and first six factorial moments.

Hosted workflow 46036070939 was triggered on the final workflow commit; its terminal status is recorded in the run discussion.

Commits:
- e330f55cc764754d517af9a6b13fcfebc8279bca — exact distribution theorem;
- 18462010d94670773f171f531670c75aaf2e5473 — exact verifier;
- 59b52bb64cdb8a53f53d8fc6049995f668418924 — frozen machine evidence;
- 31a363bcf0379a765562e749732a22f7f3be8992 — CI workflow.

## Scope and remaining blockers

This sharpens the incompatibility of the unrestricted perfect-matching representation with the fixed-cycle physical atom family. It does not exclude a different positive measure supported on non-permutation cycle exponentials exp(A(c)); the N=8 and N=10 constructions already show why such a distinction matters at smaller sizes.

The Run 64 37-base/74-labelled N=42 period-two candidate remains rejected as a complete quartic design: 1,434 of 1,440 D42 quartic-orbit residual intervals strictly exclude zero. No general period-two or full-cycle no-go follows from that candidate-specific failure.

No Choi/diamond-distance conclusion follows from this run. The full N=42 positive physical ensemble, a global separator for all real cycle couplings, higher-even-moment closure, and the operational moment-to-channel bridge remain open.

## Next highest-value action

Stop trying to repair the frozen 74-atom support. Build a symmetry-broken N=42 discovery pool of general 42-coupling cycle exponentials and impose all 1,440 quartic orbit constraints (after the exact pair/quartic incidence reduction). Use finite-pool LP only for discovery; freeze any candidate support and certify exact-real positive weights plus every quartic orbit independently. If no candidate survives, use the resulting dual only as a lead for a continuum inequality, not as a global theorem.
