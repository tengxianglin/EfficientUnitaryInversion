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


---

## 6. Continuous pricing of the certified 6,137-column dual — completed

This section supersedes the earlier sentence in Section 4 saying that continuous pricing of the 6,137 dual was still open.

The 94-term rational dual certified above has now been strictly escaped by two exact-rational general-gapped open paths. The search was deterministic multistart discovery; the mathematical signs below come from the independent 256-bit Arb certificate, not from the floating optimizer.

The certificate pins:
- finite-pool diagnostic SHA-256: `68c7c989198e8276d3b4c954cf26413039b26352f5d14e82c8daf9c1c18924ac`;
- finite-pool Arb certificate SHA-256: `59953f81d03223000d58051df9c70bddda8c582ac1cbfa4149cbcc1fae0b6d99`;
- search transcript SHA-256: `9ea13ee742834d7fa5189974c684fa74f6015bdb152e64e114cb1d1daf6f9747`.

### Connected positive-coupling escape

The 42-site open path has (c_{41}=0) and all 41 internal couplings strictly positive. Its minimum positive coupling is
[
rac{19999999999999999}{20000000000000000000000}
=9.9999999999999995	imes10^{-7}.
]
The exact-rational coupling vector is stored in `evidence/ising_full_fourth_plus_fourteen_gapped_escape_arb_n21.json`.

Arb certifies
[
y^{mathsf T}(b-F(R(c)))
in[-19.964971496200965374176154802738282774770390451849943331558707138535637886
pm2.82	imes10^{-73}]<0.
]

### Multi-segment escape

The second exact-rational path has internal zero edges ({4,5}), minimum positive coupling (10^{-8}), and three connected segments. Its exact coupling vector is in the same certificate file.

Arb certifies
[
y^{mathsf T}(b-F(R(c)))
in[-24.358461528831097759646486125750408844060050182748224150215770577931946518
pm8.41	imes10^{-73}]<0.
]

Both candidates pass 1,764 interval orthogonality-entry checks and determinant-one interval checks. The search evaluated 910 initial candidates; its analytic Frechet-gradient self-test had maximum absolute error (3.01	imes10^{-10}). These search statistics explain discovery only; the frozen rational candidates and strict Arb signs establish the escapes.

Evidence:
- [256-bit Arb escape certificate](evidence/ising_full_fourth_plus_fourteen_gapped_escape_arb_n21.json)
- [Deterministic search transcript](evidence/ising_full_fourth_plus_fourteen_gapped_search_n21.json)
- [Successful continuous-pricing workflow 45541488163](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45541488163)
- [Evidence commit 649cc8f](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/649cc8f9f70688f21aa74c2054a59f430246028f)

**Logical scope.** These are strict escapes from this particular 6,137-column dual. They do not invalidate the finite-pool theorem in Sections 1–3, prove that the full physical-family moment target is feasible or infeasible, or imply a Choi/diamond-distance bound. In particular, the connected escape has every internal edge positive, so the failure is not an artifact of allowing internal cuts.

## 7. Next finite-pool test: 6,139 columns

The two newly certified paths have been appended to the 6,137 pool, preserving its fourteen exact-rational gapped paths. The new candidate design therefore has 22 base atoms, 6,101 fractional-grid atoms, and 16 gapped paths, for 6,139 columns, with the same 1,461 complete second-/fourth-order coordinates.

The new discovery script, independent verifier, and workflow are:
- `discover_ising_full_fourth_plus_sixteen_gapped_n21.py`;
- `verify_ising_full_fourth_plus_sixteen_gapped_arb_n21.py`;
- `.github/workflows/eui-reoptimize-6139-full-fourth.yml`.

The corrected run [45545125000](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45545125000) is pending at the time of this note. No 6,139-column LP or Arb theorem is claimed until that run finishes. The parent and path-count pins were corrected in commits [0234e78](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/0234e78beefa237b5807acc8e0217676d5b0968b) and [85414be](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/85414be96052c2496166307b620b941628c29f57).

The paper-central blockers remain the exact positive ensemble satisfying all even-principal-minor constraints at (n=21), or a global physical-family obstruction, and a rigorously quantified operational Choi/diamond bridge.
