# Certified 6,124-column full-fourth obstruction with one general gapped path (n=21)

Date: 2026-11-24. Related: Issue #5.

## Theorem (finite-pool separation)

Let (N=42), (n=21). Let (F(R)inmathbb R^{1461}) contain the 21 distance-averaged second principal-minor moments and the 1,440 dihedral-orbit-averaged fourth principal minors. Let (b) be the exact uniform balanced-label target:
[
b_d=rac{(-1)^{d+1}}{41},qquad d=1,ldots,21,
]
and, for a four-set (I),
[
b_I=(-1)^{v(I)+2}rac{inom{21}{2}}{inom{42}{4}}
=(-1)^{v(I)+2}rac1{533}.
]

Let (mathcal P_{6124}) be exactly the following finite physical pool:

1. the 22 pinned base atoms from the 41-atom low-moment certificate;
2. all 6,101 columns in the corrected fractional single-open-path grid;
3. one additional connected nonuniform open path with 41 strictly positive interior couplings and exactly zero wrap coupling, frozen as exact decimal rationals in 'evidence/ising_full_fourth_plus_general_gapped_n21.json'.

There is an exact rational vector (y), supported on the 1,313 independent moment coordinates, such that
[
|D^{-1}y|_1=1,qquad
D=operatorname{diag}(41 I_{21},533 I_{1440}),
]
and, for every (R_jinmathcal P_{6124}),
[
oxed{y^{mathsf T}(b-F(R_j))>rac15.}
]

The exact full-coordinate norm recorded by the certificate is
[
|y|_1=
rac{5632855504966086341009}{10660000000000000909}
<533.
]

Consequently, for every probability vector (p) supported on this exact pool,
[
y^{mathsf T}left(b-sum_jp_jF(R_j)ight)
=sum_jp_j,y^{mathsf T}(b-F(R_j))
>rac15.
]
Hölder's inequality gives the unscaled full-feature residual bound
[
oxed{
left|b-sum_jp_jF(R_j)ight|_infty>rac1{2665}.
}
]
Thus no probability mixture on these 6,124 columns can satisfy all second- and fourth-order target moments exactly, or even approach them within (1/2665) in the full-coordinate sup norm.

## Certified numerical margins

The independent verifier uses 512-bit Arb for the 22 base atoms and the added gapped path, and 128-bit Arb for the 6,101 fractional-grid columns.

- All 6,124 column gaps are strictly greater than (1/5).
- Minimum recorded Arb lower endpoint:
  [
  0.24071664437556099470717930988636007195ldots
  ]
  at pinned base atom 14.
- Added connected gapped-path gap:
  [
  0.26347152267596481483322724961002130074ldots
  ]
- The active-block pricing implementation passed five independent full-matrix comparisons at ((L,alpha)=(2,17/100),(7,43/100),(21,89/100),(41,117/100),(42,83/100)).

The first attempt asked for a common gap (>1/4) and stopped at base atom 14 because its Arb enclosure was ([0.3pm0.0593]). This was insufficient for the stronger (1/4) floor, but its lower endpoint was positive. The accepted verifier uses the conservative strict (1/5) floor.

## Reproduction and frozen evidence

- Floating LP discovery: 'evidence/ising_full_fourth_plus_general_gapped_n21.json'.
- Independent Arb certificate: 'evidence/ising_full_fourth_plus_general_gapped_arb_n21.json'.
- Verifier: 'verify_ising_full_fourth_plus_general_gapped_arb_n21.py'.
- Workflow: '.github/workflows/eui-full-fourth-plus-general-gapped-arb-n21.yml'.
- Successful workflow: [45364156140](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45364156140).
- Certificate commit: [bb3929d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/bb3929db1d30161a2ea7c60f7e2f36c76b1682ee).
- Verifier/workflow commits: [e63b56e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/e63b56e3a5612db868402f80b24fc484035eb04e), [35c8468](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/35c846841bd9e1001872b05f51355902aa72f3ab), [b07841d](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/b07841ddf9a504a2524b299de68a554e28ba7938).

Replay with:
```bash
python verify_ising_full_fourth_plus_general_gapped_arb_n21.py
```

## Scope and limitations

This is a rigorous obstruction for exactly the 6,124 listed physical columns. It is **not** a separation theorem for all nonuniform gapped couplings, the continuous gapped open-path family, arbitrary multi-segment paths, or the full physical family. The previous 80-term separator has a certified escape in a connected nonuniform gapped path; the new dual has only been certified on the enlarged finite pool so far.

It does not establish an all-even-principal-minor obstruction or a positive joint-parity ensemble. It also does not imply a Choi-state trace-distance or channel diamond-distance lower bound. The moment-to-operational-error bridge remains a separate theorem obligation.

## Next decisive step

Price the new exact rational separator over the full 41-coupling nonuniform gapped open-path family. Search for a certified negative-slack seed; if one exists, append it and reoptimize. A positive finite-pool dual must not be promoted to a continuous-family no-go without a continuum pricing proof.
