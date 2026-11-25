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
