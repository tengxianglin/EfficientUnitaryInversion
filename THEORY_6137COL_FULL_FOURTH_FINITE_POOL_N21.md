# 6,137-column complete second-/fourth-order finite-pool obstruction (n=21)

**Status (2026-11-25): independently Arb-certified finite-pool theorem.** The authoritative GitHub Actions run [45539976654](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45539976654) completed the 6,137-column LP and independent Arb verification successfully. Its evidence was committed by [da9fe176a429992f7ce9d06f161390dfad6cb6a9](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/da9fe176a429992f7ce9d06f161390dfad6cb6a9).

## 1. Feature system and exact candidate pool

Set (n=21), (N=42). Let (F(R)inmathbb R^{1461}) contain:

- all 21 distance-averaged second-order principal-minor coordinates;
- all 1,440 fourth-order dihedral-orbit averages, covering all 111,930 four-subsets before orbit reduction.

The reduced moment system has 1,313 independent moment rows, or 1,314 equalities including normalization. The target (b) is the exact uniform balanced-label moment vector.

The frozen candidate pool is
[
6137=22+6101+14:
]
- 22 pinned base atoms;
- 6,101 corrected fractional single-open-path grid atoms;
- 14 exact-rational general-gapped paths. These include the twelve paths in the certified 6,135-column parent pool and two new paths that were independently Arb-certified as strict escapes from that parent's dual.

Each gapped path is encoded by 42 rational couplings, with the closing/wrap edge exactly zero. The newly appended two paths are pinned by the parent escape certificate and search transcript; one is connected with all 41 internal couplings positive, and one is multi-segment.

## 2. Exact dual and interval certificate

The rationalized dual has 94 nonzero coefficients, all supported on fourth-order feature coordinates. With
[
D=operatorname{diag}(41I_{21},533I_{1440}),
]
the independent verifier establishes exactly
[
|D^{-1}y|_1=1,qquad |y|_1=533.
]

The verifier checks every one of the 6,137 columns using python-flint/Arb: 512-bit precision for the 22 base atoms and 14 gapped paths, and 128-bit precision for all 6,101 fractional-grid atoms. The minimum certified lower endpoint is
[
0.2326666409579100988019484538581578176903987019669ldots
>rac15.
]

The diagnostic JSON retains its historical discovery status string `floating_full_fourth_6137_column_separator_candidate_not_arb_certified`. This is a legacy label, not the final status: the separate certificate is authoritative, has status `arb_certified_finite_6137_column_full_fourth_plus_fourteen_gapped_separator`, and pins the diagnostic SHA-256 exactly. Do not edit the diagnostic in place without regenerating the certificate.

Evidence:
- [6,137-column LP diagnostic](evidence/ising_full_fourth_plus_fourteen_gapped_n21.json)
- [Independent Arb certificate](evidence/ising_full_fourth_plus_fourteen_gapped_arb_n21.json)
- [Independent verifier](verify_ising_full_fourth_plus_fourteen_gapped_arb_n21.py)
- [Workflow 45539976654](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45539976654)
- [Evidence commit da9fe176](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/da9fe176a429992f7ce9d06f161390dfad6cb6a9)

## 3. Finite-pool theorem

**Theorem.** For every probability vector (pinDelta_{6137}), where the columns of (A_{6137}) are exactly the 6,137 physical feature vectors above,
[
oxed{|b-A_{6137}p|_infty>rac1{2665}.}
]

**Proof.** The Arb certificate proves, for every listed column (a_j=F(R_j)),
[
y^{mathsf T}(b-a_j)>rac15.
]
By convexity, for every (pinDelta_{6137}),
[
y^{mathsf T}(b-A_{6137}p)>rac15.
]
Since (|y|_1=533), Hölder's inequality gives
[
|b-A_{6137}p|_infty
ge rac{y^{mathsf T}(b-A_{6137}p)}{|y|_1}
>rac{1}{5cdot533}=rac1{2665}.
]

Every retained second-/fourth-order coordinate is the expectation of a bounded balanced-program-label character or a dihedral-orbit average of such characters. The same dual therefore gives a bounded test function with sup norm at most 533. Using
[
|mathbb E_P g-mathbb E_Q g|
le 2|g|_infty,operatorname{TV}(P,Q),
]
we obtain the exact program-mass consequence
[
oxed{operatorname{TV}(w_p,u_{m bal})>rac1{5330}.}
]
This concerns the balanced program-label distribution in the selected parity sector, equivalently its dephased classical register. It is not a Choi-state trace-distance or channel diamond-distance bound.

## 4. Scope and non-implications

This is a rigorous finite-pool theorem for exactly the 6,137 listed columns and the complete 1,461-coordinate second-/fourth-order design. It is **not**:
- a separation theorem for every nonuniform positive coupling or every multi-segment path;
- a complete sixth-/eighth-order orbit theorem;
- a construction or obstruction for the full all-even-principal-minor system;
- a Choi- or diamond-distance lower bound.

The two new paths are escapes from the **6,135-column parent dual**, not from the new 6,137-column dual. They do not invalidate the 6,135-column theorem. Continuous pricing of the current 6,137-column dual is a separate, still-open task.

## 5. Reproduction and next decisive action

The authoritative workflow [45539976654](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45539976654) completed successfully. It passed Python compilation, block-minor/spin-symmetry/serialization regressions, the 6,137-column LP, the independent Arb verifier, evidence commit, and artifact upload. The resulting certificate records:
- 6,137 columns and 1,461 full second-/fourth-order coordinates;
- 94 exact rational dual coefficients;
- (|D^{-1}y|_1=1) and (|y|_1=533);
- common certified column gap (1/5);
- residual lower bound (1/2665);
- program-mass TV lower bound (1/5330).

The next decisive experiment is to price this **new 94-term 6,137-column dual** on connected positive-coupling and general multi-segment open paths. Search is only a deterministic discovery step. Any candidate must be frozen as exact rational couplings and independently Arb-checked for all orthogonality entries, determinant one, and strict dual escape. Failure to find an escape is not a continuum upper bound.

In parallel, the paper-central question remains construction of an exact positive ensemble satisfying every even-principal-minor constraint at (n=21), or a genuinely global physical-family obstruction, together with a rigorous bridge to an operational Choi/diamond metric.
