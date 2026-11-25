# 6,135-column complete second-/fourth-order finite-pool obstruction

**Status (2026-11-25): certified finite-pool theorem.** The independent Arb certificate is committed at [f38a7933b954abc454315c5b25a21141cdb3c97c](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f38a7933b954abc454315c5b25a21141cdb3c97c). The theorem below applies only to the exact 6,135-column pool and the complete second-/fourth-order feature system defined here.

## 1. Feature system and frozen physical pool

Set \(n=21\), \(N=42\). Let \(F(R)\in\mathbb R^{1461}\) contain the 21 distance-averaged second-order principal-minor coordinates and all 1,440 fourth-order dihedral-orbit averages (111,930 four-subsets before orbit reduction). The target \(b\) is the exact uniform balanced-label moment vector. The reduced equality system has 1,313 independent moment rows, or 1,314 equalities after normalization.

The frozen pool has
\[
6135=22+6101+12
\]
columns:
- 22 pinned base atoms;
- 6,101 corrected fractional single-open-path grid atoms;
- 12 exact-rational gapped paths: ten inherited from the certified 6,133-column parent and two newly appended 256-bit-Arb-certified escapes from that parent's dual.

Every gapped path is stored as 42 exact rational couplings with the open-chain closing edge exactly zero. The last two paths are respectively connected (all 41 internal couplings positive) and multi-segment.

## 2. Exact dual and independent interval evidence

The 101-term rationalized dual \(y\) has support only on fourth-order feature indices 77–1452. With
\[
D=\operatorname{diag}(41 I_{21},533 I_{1440}),
\]
the verifier establishes exactly
\[
\|D^{-1}y\|_1=1,\qquad \|y\|_1=533.
\]

The independent verifier uses python-flint/Arb at 512-bit precision for the 22 base atoms and 12 gapped paths, and 128-bit precision for all 6,101 fractional-grid atoms. It also passes five block-pricing versus full-pricing self-tests. The stored certificate reports
\[
\min_j \operatorname{lower}\!\left(y^{\mathsf T}(b-F(R_j))\right)
=0.23879583857497366478523939563642828758\ldots
>\frac{23879}{100000}.
\]
The exact diagnostic SHA-256 is \`647bdce0b83bfa6f86dcb2e1e211ff8a310c657c79dfbc22f4af9229802f8ba7\`; the Arb certificate pins this hash and the parent/escape/warm-start evidence hashes.

Evidence:
- [6,135-column floating LP diagnostic](evidence/ising_full_fourth_plus_twelve_gapped_n21.json)
- [6,135-column Arb certificate](evidence/ising_full_fourth_plus_twelve_gapped_arb_n21.json)
- [Independent verifier](verify_ising_full_fourth_plus_twelve_gapped_arb_n21.py)
- [Authoritative workflow 45519860433](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45519860433)
- [Certificate commit f38a793](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/f38a7933b954abc454315c5b25a21141cdb3c97c)

## 3. Finite-pool theorem

**Theorem.** For every probability vector \(p\in\Delta_{6135}\),
\[
\boxed{\|b-Ap\|_\infty>\frac{23879}{53300000}
=0.0004480112570356473\ldots .}
\]
Here the columns of \(A\) are exactly the 6,135 vectors \(F(R_j)\) above.

**Proof.** Arb certifies \(y^{\mathsf T}(b-F(R_j))>23879/100000\) for every listed column. Convexity therefore gives
\[
y^{\mathsf T}(b-Ap)>\frac{23879}{100000}.
\]
Since \(\|y\|_1=533\), Hölder's inequality yields the stated infinity-norm bound.

Every retained coordinate is the expectation of a dihedral-orbit average of even program-label characters, each pointwise bounded in absolute value by one. Thus the same dual induces a bounded character witness with sup norm at most 533. By the total-variation dual inequality,
\[
\boxed{\operatorname{TV}(w_p,u_{\rm bal})>
\frac{23879}{106600000}
=0.00022400562851782364\ldots .}
\]
This is a statement about the balanced program-label distribution in one selected parity sector, equivalently its dephased classical register. It is not a Choi-state trace-distance or channel diamond-distance bound.

The previously committed certificate records the conservative rational floor \(1/5\), giving \(1/2665\) and \(1/5330\). The stronger floor \(23879/100000\) follows directly from its stored Arb lower endpoint. The verifier has now been updated to select this stronger predeclared rational floor automatically; the reproducibility rerun is pending.

## 4. Scope and non-implications

This is a rigorous finite-pool obstruction for exactly the 6,135 columns and the complete 1,461-coordinate second-/fourth-order design. It is **not**:
- a separation theorem for all nonuniform positive couplings or all multi-segment paths;
- a complete sixth-/eighth-order orbit theorem;
- an obstruction or construction for the full all-even-principal-minor system;
- a Choi- or diamond-distance lower bound.

The 6,133-column parent dual had two continuous gapped escapes, and those exact paths are included here. That fact does not invalidate either finite-pool theorem. No continuous escape of the new 6,135-column dual has yet been certified.

## 5. Reproduction and next decisive action

The authoritative run [45519860433](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45519860433) completed successfully: LP solve, independent Arb verification, certificate commit, and artifact upload. The latest verifier refinement is commit [fbfa21c63b0adba7e3f08de0b03f9d9574029e1b](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/fbfa21c63b0adba7e3f08de0b03f9d9574029e1b); its workflow rerun must confirm the sharper rational floor is reproduced from scratch.

The next scientific action is continuous pricing of this **new 101-term dual** over the general gapped family. Any candidate escape must be frozen as exact rational couplings and independently Arb-certified before it is added to a new pool. In parallel, the paper-central target remains an exact positive ensemble satisfying every even-principal-minor constraint at \(n=21\), or a genuinely global physical-family obstruction.

## 6. Continuous pricing of the new 6,135-column dual

A deterministic multistart search and independent 256-bit Arb verifier have now been added for the new 101-term dual:

- [Search source](search_ising_full_fourth_plus_twelve_gapped_n21.py)
- [Independent escape verifier](verify_ising_full_fourth_plus_twelve_gapped_escape_arb_n21.py)
- [GitHub Actions workflow](.github/workflows/eui-full-fourth-plus-twelve-gapped-search-n21.yml)

The search uses the frozen seed pool, all 12 inherited/appended gapped paths, connected lognormal starts, fractional-profile perturbations, and multi-segment starts. It is discovery only: a found candidate is reconstructed from its frozen decimal as an exact rational and must pass Arb orthogonality, determinant-one, and exact-dual pricing checks. Failure to find an escape is not a global pricing bound.


## 7. Continuous escape of the 6,135-column dual (256-bit Arb)

The new 101-term dual was priced on connected and multi-segment open paths. The deterministic search evaluated 908 initial candidates (random seed 20261127), used L-BFGS-B with analytic Frechet gradients (12 starts per class, at most 160 iterations), and passed gradient self-tests with maximum absolute error \(1.4598736802762247\times10^{-10}\). Search time was 89.96 s. These are discovery statistics only.

The independent 256-bit Arb certificate is [evidence/ising_full_fourth_plus_twelve_gapped_escape_arb_n21.json](evidence/ising_full_fourth_plus_twelve_gapped_escape_arb_n21.json), pinned to the exact search transcript [evidence/ising_full_fourth_plus_twelve_gapped_search_n21.json](evidence/ising_full_fourth_plus_twelve_gapped_search_n21.json) and the 6,135-column parent diagnostic/certificate.

The target score interval is
\[
[0.321167169883441891720217398682819719066979250535922876218093482325363297972
\pm4.08\times10^{-76}].
\]
Two exact-rational candidates are strict escapes:

1. **Connected:** all 41 internal couplings are positive, with minimum \(19999999999999999/20000000000000000000000\). Arb certifies
\[
y^{\mathsf T}(b-F(R(c)))\in
[-26.157407375828305275291539049492401738948470292029244527892433256798474110
\pm2.58\times10^{-73}]<0.
\]
2. **Multi-segment:** internal zero edges are exactly \(\{2,8,14,34\}\), and the minimum positive coupling is \(10^{-8}\). Arb certifies
\[
y^{\mathsf T}(b-F(R(c)))\in
[-29.0202659222329264370830935075472903097715424919454197347578133979724768
\pm4.07\times10^{-71}]<0.
\]

Both candidates pass 1,764 Arb orthogonality-entry checks and determinant-one interval checks. Thus the 6,135-column dual is **not** a global separator for either the connected positive-coupling family or the general multi-segment family. This does not invalidate the finite-pool theorem and does not settle whether another global obstruction exists.

Evidence commit: [2ad5b3d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/2ad5b3dfef9cf3a3fc945c4e25f52376362c3b87).

## 8. Next finite-pool reoptimization

The two newly certified exact-rational paths are being appended to the 6,135 pool, giving a 6,137-column, 1,461-coordinate full-second-/fourth-order LP. The discovery and independent verifier are committed as:
- [6,137-column LP source](discover_ising_full_fourth_plus_fourteen_gapped_n21.py)
- [6,137-column Arb verifier](verify_ising_full_fourth_plus_fourteen_gapped_arb_n21.py)

The 6,137 workflow is intentionally not launched until the 6,135 parent certificate and its escape certificate have matching current SHA-256 pins. The sharper 6,135 rational-floor verifier rerun is still pending; if it rewrites the parent certificate, the 6,135 escape verifier must be rerun before the 6,137 pool is certified. This preserves the evidence chain rather than silently accepting a stale parent hash.


## 9. Parent-hash refresh after the sharper-floor rerun

The 256-bit escape evidence in commit 2ad5b3d was generated against the previous 6,135 diagnostic SHA-256 647bdce0b83bfa6f86dcb2e1e211ff8a310c657c79dfbc22f4af9229802f8ba7 and previous finite-certificate SHA-256 8618589ab8a195f3980408d9722e861f6f899caa7086c6f2d2118347a76f7d90.

The sharper-floor rerun subsequently rewrote the 6,135 diagnostic and certificate. The current hashes are:
- diagnostic:  eb0493da0cadf4408c43fe7ff371ce52d20dbc21fbd329f2669f90465e6adc43;
- finite certificate: 1b7a8f17e6332d66cd4508d0179ebb13919bc7db4873b2d6810e7558435a19dd.

The current diagnostic target-score midpoint is 0.32116716988338767, whereas the old search transcript pinned 0.3211671698834419. Therefore the old escape certificate must **not** be treated as a certificate for the current rationalized dual, even though the numerical values are close. The 6,135 finite-pool theorem and sharpened bounds remain certified; only the continuous-escape provenance must be refreshed.

The continuous-pricing workflow was retriggered in commit [8e6a1af](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/8e6a1af70a4b67cfe00f4f581573648919adfd91). Until a new search transcript and 256-bit Arb certificate pin the current hashes, there is no current-dual continuous-escape claim. The 6,137 discovery/verifier scripts are staged, but their workflow is withheld until this parent/escape chain is current.
