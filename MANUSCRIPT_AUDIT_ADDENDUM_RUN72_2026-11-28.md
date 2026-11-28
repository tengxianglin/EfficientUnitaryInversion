# Manuscript audit addendum — Run 72

Date: 2026-11-28. Base repository HEAD: 6d135894020d3b02d58709d6ba8f825b7624f438.

## Selection

Inspected the current main head and recent commits through Run 71, open Issues #7, #5 and #6, all Issue #7 comments through the Run 71 follow-up, the full sixth-harmonic local-pricing note/verifier/certificate, the perfect-matching reachability and adjacent-pair obstruction notes, recent Actions runs, and the repository tree. The repository still contains research/audit Markdown but no editable .tex, .bib, manuscript PDF, or independent supplementary source.

The highest-leverage unresolved subtask was the Run 71 proposal to find a pair-balanced mixture of non-periodic path/block perfect-transfer matching atoms. This is an exact, finite question and can be settled before spending more compute on a matching-design search.

## Result

Added an exact 21-atom 1-factorization of K21,21, obtained by even cyclic translates of the 42-site engineered path-perfect-transfer matching. It partitions all 441 even--odd edges exactly once; each atom has exactly two physical cycle edges and is realized by the cycle generator with one zero closing-edge coupling.

Proved the pair-level minimax over all bipartite perfect-matching mixtures:
- any such mixture has a doubly stochastic cross-parity edge marginal matrix p;
- its squared degree-two residual is at least 20/41, uniquely minimized by p_ab=1/21;
- the balanced-slice degree-two Gram eigenvalue is 560/533, giving chi-square(q||u) >= 13/28 for every mixture supported on physically reachable matching atoms.

For the explicit cyclic 1-factorization, the union of atoms M_t,M_s has gcd(21,t-s) alternating components. Exact overlap counting gives:
- sum_S q(S)^2 = 99880/2^42;
- full program-label chi-square = 839949975821189/68719476736 ~= 12222.88084421873;
- support-size TV lower bound = 22425576427/22427411435 ~= 0.9999181801250082;
- complement-folded frame potential = 12485/137438953472.

This is a sharp negative result for the matching-only branch, not for the full cycle-exponential family. The path atoms use zero couplings; if the intended physical domain is strictly positive on every edge, they are boundary atoms and positive-edge perturbations do not preserve exact matching identities. No Choi/diamond bound is inferred.

## Reproducibility

- Theory: THEORY_N42_PATH_MATCHING_1_FACTORIZATION_PAIR_MINIMAX.md
- Dependency-free exact verifier: verify_n42_path_matching_1_factorization_pair_minimax.py
- Machine evidence: evidence/n42_path_matching_1_factorization_pair_minimax.json
- CI: .github/workflows/eui-n42-path-matching-pair-minimax.yml

The verifier checks all 21 matchings, all 441 cross edges, all 441 ordered atom-pair component counts, and every rational divergence formula.

## Next highest-value action

Do not continue searching for a pair-balanced mixture of signed matching atoms: the 1-factorization is already pair-optimal, and the universal matching-subfamily lower bound is 13/28. Move to non-permutation cycle exponentials. Enforce all 861 pair constraints in the candidate mixture, then use the Run 71 32-minor local pricing oracle on the largest Run 70 sixth-harmonic coordinates to generate/certify new non-periodic columns. The first goal is a reproducible finite-pool primal/dual diagnostic; a global conclusion still requires a separator priced over every real coupling vector or an exact positive physical ensemble matching all even orders.

## Final CI closure

The first two workflow attempts reached the exact verifier and produced the expected rational outputs, but failed the final byte-for-byte evidence comparison because of JSON formatting only (float exponent and array pretty-printing). The committed certificate was normalized to the verifier's deterministic Python output. Final [workflow 46113888051](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/46113888051) passed compilation, the exact verifier, evidence diff, and artifact upload. Final main HEAD: 6873c1ebb8c5d7bb8705822b52a341dde1c45710.
