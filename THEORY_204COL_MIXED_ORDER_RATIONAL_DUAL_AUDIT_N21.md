# 204-column mixed-order rational dual audit (n=21)

Date: 2026-11-26. This note records the 204-column extension of the fixed 2,113-row finite-pool obstruction. It is a finite-pool theorem, not a global physical-family converse.

## 1. Frozen design and parentage

The 204-column LP appends the exact Arb-certified finite-time escape of the 203-column dual as physical column 1661. The 42-site open path is
\[
t_{203}=\frac{5594112299050130881369}{500000000000000}>0,
\qquad c_0=\cdots=c_{40}=t_{203},\quad c_{41}=0.
\]
All 41 internal couplings are strictly positive. Its 128-bit Arb pricing certificate is `evidence/203col_uniform_ray_time_arb_n21.json`.

The LP retains the fixed 2,113-row design:
- 21 complete second-order rows;
- 1,440 complete fourth-order rows;
- 645 selected/cut sixth-order rows;
- 7 selected eighth-order rows.

The 204-column HiGHS discovery objective is 0.3855817390106711, with recomputed maximum residual 0.38558173901226533, primal/dual discovery gap 2.586264535864302e-13, and 71 positive-support entries. These are binary64 discovery diagnostics only.

## 2. Exact rational dual and independent Arb certificate

The rationalized dual has
\[
\|z\|_1=
\frac{4611686018426502061}{4611686018427387904}<1,
\]
and
\[
\lambda+\langle z,y\rangle=
\frac{1778181914757622867}{4611686018427387904}.
\]
The rational slack is exactly \(10^{-8}\). Independent 128-bit Arb arithmetic certifies all 204 column inequalities, with maximum shifted-column upper endpoint
\[
-8.980803464660286\times10^{-9}<0.
\]
Therefore
\[
\boxed{
\eta_{204}\ge
\frac{694602292437797922939891}{1801439850948198400000000}
=0.38558172901092974\ldots>\frac13.
}
\]

The machine-readable certificate is `evidence/55probe_204col_uniform_ray_escape_dual_certificate_n21.json`. It records 204 interval evaluations, 71 active rows (4 low-order, 64 sixth-order, 3 eighth-order), precision 128 bits, and parent LP/dual hashes. The independent certification workflow [45657144300](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45657144300) completed successfully.

## 3. Program-mass TV corollary

The exact-rational bounded-character calculation gives
\[
\boxed{
\operatorname{TV}(w_p,u_{\rm bal})\ge
\frac{17810315190712767254869}{387656137538470562495468750}
=4.5943591410171576\ldots\times10^{-5}.
}
\]
This is a statement for arbitrary probability mixtures over exactly these 204 certified physical columns, in one selected parity sector. Equivalently it bounds trace distance of the corresponding dephased classical program-label registers. It is **not** a Choi trace-distance or channel diamond-distance lower bound.

The exact-rational postprocessor output is `evidence/204col_program_mass_tv_bound_n21.json`.

## 4. Scope and next decisive check

**Proved:** the stated minimax lower bound for the fixed 204-column pool and fixed 2,113-row mixed-order design.

**Not proved:** a global converse over all physical couplings, full all-even-principal-minor feasibility/infeasibility, complete sixth/eighth orbit control, or an operational Choi/diamond bound.

The new 204-column dual must be priced separately over the 21-dimensional uniform-path torus. A positive exact-decimal point with a strictly positive Arb interval would refute global separation by this particular 204-column dual on the continuous equal-coupling physical ray, without affecting the finite-pool theorem. Failure of a finite multistart search is not a global separation proof.

## 5. Reproducibility

- Reoptimization script: `reoptimize_204col_uniform_ray_escape.py`
- Reoptimization workflow: `.github/workflows/eui-reoptimize-204col-uniform-ray.yml`
- Reoptimization run: [45638510647](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45638510647)
- Rational dual verifier: `verify_204col_uniform_ray_dual_arb.py`
- TV verifier: `verify_204col_program_mass_tv_bound.py`
- Certification workflow: `.github/workflows/eui-certify-204col-uniform-ray-dual.yml`
- Certification run: [45657144300](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45657144300)
- 204-column torus discovery/verifier: `discover_204col_uniform_torus_pricing.py`, `verify_204col_uniform_torus_pricing_arb.py`
- Torus workflow: `.github/workflows/eui-204col-uniform-torus-pricing.yml`
