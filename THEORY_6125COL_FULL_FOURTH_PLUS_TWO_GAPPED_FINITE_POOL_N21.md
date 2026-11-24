# Certified 6,125-column full-second-/fourth-moment obstruction (n=21)

Date: 2026-11-24. Related: Issue #5.

## Theorem (finite-pool separation)

Let (N=42), (n=21). Let (F(R)inmathbb R^{1461}) consist of the 21 distance-averaged second principal-minor moments and the 1,440 dihedral-orbit-averaged fourth principal minors. The exact uniform balanced-label target is
[
b_d=rac{(-1)^{d+1}}{41},qquad d=1,ldots,21,
]
and, for a four-set (I),
[
b_I=(-1)^{v(I)+2}rac{inom{21}{2}}{inom{42}{4}}
=(-1)^{v(I)+2}rac1{533}.
]

Let (mathcal P_{6125}) be exactly:
1. the 22 pinned base atoms from the 41-atom low-moment certificate;
2. all 6,101 columns in the symmetry-corrected fractional single-open-path grid;
3. the parent connected nonuniform open path from the certified 6,124-column pool;
4. the second connected nonuniform open path, independently certified as an escape from the *parent* 6,124-column dual.

Both gapped paths have 41 strictly positive interior couplings and exactly zero wrap coupling. Their exact rational coupling vectors are frozen in `evidence/ising_full_fourth_plus_two_gapped_n21.json` and independently reconstructed by the Arb verifier.

There is an exact rational vector (y), supported on the 1,313 independent moment coordinates, such that, with
[
D=operatorname{diag}(41 I_{21},533 I_{1440}),
qquad |D^{-1}y|_1=1,
]
Arb certifies
[
oxed{y^{mathsf T}(b-F(R_j))>rac15
quad	ext{for every }R_jinmathcal P_{6125}.}
]

The exact full-coordinate norm is
[
|y|_1=
rac{1160260291609871892947}{2220833333333332779}
<533.
]
Therefore, for every probability vector (p) on this exact finite pool,
[
y^{mathsf T}left(b-sum_jp_jF(R_j)ight)>rac15.
]
By Hölder,
[
oxed{
left|b-sum_jp_jF(R_j)ight|_infty>rac1{2665}.
}
]
No probability mixture on these 6,125 columns can satisfy all listed second- and fourth-order target moments exactly, or approach them within (1/2665) in the full-coordinate sup norm.

## Certified numerical margins

The independent verifier uses 512-bit Arb for the 22 base atoms and both gapped paths, and 128-bit Arb for the 6,101 fractional-grid columns.

- All 6,125 column gaps are strictly greater than (1/5).
- The minimum recorded Arb lower endpoint is
  [
  0.2556395192282210077992726129448631454393ldots,
  ]
  at the fractional column (L=41,alpha=19/20).
- The two appended connected-path gaps are approximately
  [
  0.26137281773705033936ldots,qquad
  0.26137281773708948535ldots.
  ]
- The active-block pricing implementation passed five independent full-matrix comparisons.
- The exact dual has 78 nonzero rational coefficients and (|D^{-1}y|_1=1).

The 6,125-column floating LP itself reported primal infeasibility. That status is discovery only; the theorem above rests on the independent rational/Arb certificate, not on the floating solver status.

## Reproducibility

- Floating discovery: `evidence/ising_full_fourth_plus_two_gapped_n21.json`.
- Independent certificate: `evidence/ising_full_fourth_plus_two_gapped_arb_n21.json`.
- Verifier: `verify_ising_full_fourth_plus_two_gapped_arb_n21.py`.
- Workflow: [45377450829](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45377450829).
- Certificate commit: [2640a0e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/2640a0efcb84b889b95a29581e64e5ae85b2dfb8).
- Discovery diagnostic commit: [bead29d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/bead29dbad301d9008b100185f6bd46576e06767).
- Verifier commit: [c73af75](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/c73af75607272b4aad85f89aeb948a313ab2ca48).

Replay:
```bash
python verify_ising_full_fourth_plus_two_gapped_arb_n21.py
```

## Scope and limitations

This is a rigorous obstruction for exactly the 6,125 listed physical columns. It is not a separation theorem for all nonuniform gapped couplings, the continuous gapped open-path family, arbitrary multi-segment paths, all even principal minors, or the full physical family. The prior dual has a certified escape in a connected gapped path; the new dual has only been checked on this enlarged finite pool so far.

It does not establish an all-even-principal-minor obstruction or a positive joint-parity ensemble. It also does not imply a Choi-state trace-distance or channel diamond-distance lower bound. The moment-to-operational-error bridge remains a separate theorem obligation.

## Next decisive step

Price this *new* exact rational dual over the full 41-coupling nonuniform gapped open-path family. Search for a certified negative-slack seed. If one exists, freeze its rational couplings and independently Arb-certify the escape before appending it and reoptimizing. If the search finds no escape, that is only finite numerical evidence; a continuum no-go still requires a rigorous global pricing argument.

## Corollary: finite-pool program-mass total-variation lower bound

The exact program/DPP identity in `THEORY_PROGRAM_DPP.md` states that, for every even Majorana index set (I),
[
mathbb E_{[T]sim w_R}(-1)^{|I\cap T|}=det R_{I,I}.
]
For each second-order distance orbit or fourth-order dihedral orbit (O), define
[
phi_O([T])=\frac1{|O|}\sum_{I\in O}(-1)^{|I\cap T|}.
]
Each summand is (pm1), hence (|phi_O|_inftyle1). The 1,461 coordinates of (F(R)) are precisely expectations of these bounded orbit characters (with the same orbit averaging, including the antipodal second-order orbit). The target vector (b) is the corresponding expectation under the uniform balanced-label distribution (u_{\rm bal}).

For a mixture (p) on (mathcal P_{6125}), the certified moment theorem gives
[
\max_O|\mathbb E_{w_p}\phi_O-\mathbb E_{u_{\rm bal}}\phi_O|
=\|b-Ap\|_\infty>\frac1{2665}.
]
The variational inequality for total variation, (|\mathbb E_P f-\mathbb E_Q f|\le2\operatorname{TV}(P,Q)) when (|f|_infty\le1), therefore yields
[
oxed{\operatorname{TV}(w_p,u_{\rm bal})>\frac1{5330}.}
]
Equivalently, the trace distance between the corresponding dephased program-label registers exceeds (1/5330).

**Scope:** this is a lower bound on the classical program-label mass distribution (or its dephased register) for mixtures supported on this exact 6,125-column pool. It is not a Choi-state trace-distance or channel diamond-distance bound, and it does not cover arbitrary gapped couplings outside the pool.
