# 203-column mixed-order rational dual audit (n=21)

Date: 2026-11-25. This note records the 203-column extension of the fixed 2,113-row finite-pool obstruction. It is a finite-pool theorem, not a global physical-family converse.

## 1. Frozen design and parentage

The 203-column LP appends the exact Arb-certified finite-time escape of the 202-column dual as physical column 1660. The path is the 42-site open chain
\[
t_{202}=\frac{2906260875695546623319}{1000000000000000}>0,
\qquad c_0=\cdots=c_{40}=t_{202},\quad c_{41}=0.
\]
All 41 internal couplings are strictly positive. Its 128-bit Arb pricing certificate is
`evidence/202col_uniform_ray_time_arb_n21.json`.

The LP retains the fixed 2,113-row design:
- 21 complete second-order rows;
- 1,440 complete fourth-order rows;
- 645 selected/cut sixth-order rows;
- 7 selected eighth-order rows.

The 203-column HiGHS discovery objective is 0.38670687143193666, with recomputed maximum residual 0.38670687143626825, primal/dual discovery gap 1.4449552665496412e-13, and 68 positive-support entries. This is a binary64 discovery diagnostic only.

## 2. Exact rational dual and independent Arb certificate

The rationalized dual has
\[
\|z\|_1=1,
\qquad
\langle z,y\rangle=
\frac{19815229691242147}{51240955760304989}
=0.3867068714317870026003763735\ldots.
\]
The rational slack is exactly \(10^{-9}\). Independent 128-bit Arb arithmetic certifies all 203 column inequalities, with maximum shifted-column upper endpoint
\[
-8.650750565965185\times10^{-10}<0.
\]
Therefore
\[
\boxed{
\eta_{203}\ge
\frac{19815229640001191239695011}{51240955760304989000000000}
=0.3867068704317870026003763735\ldots>\frac13.
}
\]

The machine-readable certificate is `evidence/55probe_203col_uniform_ray_escape_dual_certificate_n21.json`. It records 203 interval evaluations, 68 active rows (4 low-order, 61 sixth-order, 3 eighth-order), precision 128 bits, and the parent LP/dual hashes. The independent certification workflow [45624017940](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45624017940) completed successfully.

## 3. Program-mass TV corollary

The exact-rational bounded-character calculation gives
\[
\boxed{
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{19815229640001191239695011}{422945788402254629538000000000}
=4.6850518868757130472901251919\ldots\times10^{-5}.
}
\]
This is a statement for arbitrary probability mixtures over exactly these 203 certified physical columns, in one selected parity sector. Equivalently it bounds trace distance of the corresponding dephased classical program-label registers. It is **not** a Choi trace-distance or channel diamond-distance lower bound.

The exact-rational postprocessor output is `evidence/203col_program_mass_tv_bound_n21.json`.

## 4. Scope and next decisive check

**Proved:** the stated minimax lower bound for the fixed 203-column pool and fixed 2,113-row mixed-order design.

**Not proved:** a global converse over all physical couplings, full all-even-principal-minor feasibility/infeasibility, complete sixth/eighth orbit control, or an operational Choi/diamond bound.

The 203-column dual has not yet been priced over the full 21-dimensional uniform-path torus. The next decisive step is a continuous torus search for a positive pricing point, followed by independent Arb verification and, if positive, a finite-time positive-coupling witness. A torus escape would refute global separation by this particular dual without affecting the finite-pool theorem.

## 5. Reproducibility

- Reoptimization script: `reoptimize_203col_uniform_ray_escape.py`
- Reoptimization workflow: `.github/workflows/eui-reoptimize-203col-uniform-ray.yml`
- Reoptimization run: [45622431946](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45622431946)
- Rational dual verifier: `verify_203col_uniform_ray_dual_arb.py`
- TV verifier: `verify_203col_program_mass_tv_bound.py`
- Certification workflow: `.github/workflows/eui-certify-203col-uniform-ray-dual.yml`
- Certification run: [45624017940](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45624017940)


## 6. Continuous uniform-path torus pricing of the 203-column dual (Run 27)

The exact 203-column dual has now been priced at a point of the full 21-dimensional uniform-path torus. The deterministic discovery used eight starts, at most 120 L-BFGS-B iterations per start, seed `202611252115`, NumPy 2.3.5 and SciPy 1.15.3. The analytic cofactor gradient was checked against complex-step and central differences; the maximum recorded relative defect was
`2.590572462859631e-9`. The explicit spectral-basis regressions had maximum absolute defects below `5.4e-15`.

The exact rational-decimal phase vector is stored in
`evidence/203col_uniform_torus_search_n21.json` and pinned by SHA-256
`7477552fc810d4438138130a5fee7baebbe3fc33490bd50ad17544478e3cb5d3`.
Independent 128-bit Arb evaluation gives
[
S_{203}(R(\theta_*))
\in
[1.0825780781000278157417170733698968
\pm 7.99\times10^{-35}]>0.
]
The lower endpoint itself is enclosed by
`[1.0825780781000278157417170733698967202 +/- 3.69e-38]`,
strictly above zero. The certificate pins the exact 203-column rational dual, LP transcript, mixed-order cut design, discovery transcript, 202-column warm-start transcript, and dense-torus theorem source.

Evidence:
- [203-column torus search](evidence/203col_uniform_torus_search_n21.json)
- [independent 128-bit Arb certificate](evidence/203col_uniform_torus_arb_n21.json)
- [discovery and verifier scripts](discover_203col_uniform_torus_pricing.py), [Arb verifier](verify_203col_uniform_torus_pricing_arb.py)
- [successful CI workflow 45627659423](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45627659423)
- evidence commit [e3e8b5c](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e3e8b5cec6892f190dcc434140e27710c890c7e7)

**Theorem-level consequence.** The exact dense-ray theorem in `THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md`, together with continuity and the strictly positive Arb interval, proves that there exists at least one finite (t>0) on the equal-positive-coupling 42-site open path for which the 203-column dual pricing is positive.

**Scope.** This refutes global separation by this particular 203-column dual on the continuous equal-coupling physical ray. It does not invalidate the exact 203-column finite-pool theorem, prove feasibility or infeasibility of the complete physical-family moment problem, complete the selected sixth/eighth-order orbit system, or imply a Choi/diamond-distance bound. The torus certificate proves existence of a finite physical time by density; an explicit exact-rational time is being searched and must still receive its own Arb certificate.
