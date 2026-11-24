# 6,131-column full-second/fourth finite-pool obstruction at n=21

**Status (2026-11-25): rigorous finite-pool theorem; independently certified with python-flint / Arb.** The certificate is committed at [053032e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/053032e2fbe094448076e29883fa8f7285f40920), produced by successful [workflow 45469881533](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45469881533). A new deterministic continuous-gapped pricing search against this frozen dual has been added and is launched by [workflow file](.github/workflows/eui-search-6131-full-fourth-gapped.yml); its outcome is not yet known.

**Not claimed:** a continuum obstruction, an all-even-principal-minor obstruction, a positive ensemble, or a Choi/diamond-distance lower bound.

## 1. Exact finite physical pool

Let (N=42) ((n=21)) and
[
R(c)=e^{A(c)}in SO(42),qquad
A(c)_{j,j+1}=2c_j,quad A(c)_{j+1,j}=-2c_j,
quad j=0,ldots,40,quad c_{41}=0.
]

The certified pool has exactly
[
22+6101+8=6131
]
columns:

1. **22 pinned base atoms**, inherited from the 41-atom low-moment Arb certificate;
2. **6,101 corrected fractional single-open-path grid atoms**, with (alpha=k/100):
   - (L=2): (k=0,ldots,200);
   - odd (L=3,5,ldots,41), and (L=42): (k=1,ldots,100);
   - even (L=4,6,ldots,40): (k=1,ldots,200);
3. **Eight exact-rational gapped paths**: six inherited paths and two new paths that escaped the preceding 6,129-column dual. The eight comprise five connected paths and three segmented paths. Every path has the closing edge (c_{41}=0); all internal couplings are nonnegative, with the zero-edge pattern frozen in the diagnostic.

The 6,101 grid count is (201+20(100)+100+19(200)=6101). The diagnostic and its complete gapped coupling list are frozen in [the LP record](evidence/ising_full_fourth_plus_eight_gapped_n21.json).

## 2. Complete second-/fourth-order feature system

For (Rin SO(42)), let (F(R)inmathbb R^{1461}) contain:

- all 21 distance-averaged second moments;
- all 1,440 dihedral orbits of fourth-order principal minors, covering all
  [
  inom{42}{4}=111930
  ]
  quartets.

The exact incidence hierarchy has 1,313 independent moment coordinates; adding normalization gives 1,314 equalities. The pinned exact hierarchy pivot-minor determinant is
[
824633720832
e0.
]
Let (binmathbb Q^{1461}) be the exact balanced target and (A_{6131}) the matrix whose columns are the 6,131 listed feature vectors.

This is the **complete second-/fourth-order** feature system. It does not include sixth- or eighth-order constraints.

## 3. Exact rational dual and Arb certificate

The floating HiGHS solve is discovery only. The independent verifier freezes the 82 nonzero printed dual decimals as exact rational numbers and normalizes them using
[
D=operatorname{diag}(41I_{21},533I_{1440}),qquad
oxed{|D^{-1}y|_1=1}.
]
The exact full-coordinate norm is
[
|y|_1=
rac{93744873970464755319593}
{177666666666666580821}
<533.
]

The verifier independently prices:

- 22 base atoms at 512-bit Arb;
- all 6,101 fractional-grid atoms at 128-bit Arb;
- all eight exact-rational gapped paths at 512-bit Arb.

The minimum certified column-gap lower endpoint is
[
0.2396341325267923622380270022592260250ldots>rac15,
]
attained at the (L=41,alpha=1/2) fractional-grid column. Thus every one of the 6,131 listed columns obeys
[
oxed{y^{mathsf T}(b-F(R_j))>rac15.}
]

The certificate pins the LP diagnostic by SHA-256
`c2d86c213d2f0fe4c3784251dc3922a6e517d8debdf5d0b3b6dcaf4fd5cab9ea`,
the 6,129-column parent diagnostic/certificate, both 6,129-dual escape artifacts, and the warm positive 41-atom certificate. The independent verifier also runs five active-block-vs-full-matrix pricing self-tests; all five pass.

### Theorem 1 — 6,131-column finite-pool moment obstruction

For every probability vector (pinDelta_{6131}),
[
y^{mathsf T}(b-A_{6131}p)
=sum_{j=1}^{6131}p_j,y^{mathsf T}(b-F(R_j))
>rac15.
]
By Hölder and the exact norm bound (|y|_1<533),
[
oxed{
|b-A_{6131}p|_infty>rac1{2665}.
}
]
No nonnegative mixture of the exact 6,131 listed physical columns can match all 1,461 retained second-/fourth-order coordinates within this residual.

### Corollary 1 — finite-pool program-label TV obstruction

For every even Majorana index set (I), the exact DPP / Pauli-character identity gives
[
mathbb E_{[T]sim w_R}(-1)^{|Icap T|}
=det R_{I,I}.
]
For each retained second- or fourth-order dihedral orbit (O), its feature is therefore the expectation of the bounded orbit test
[
phi_O([T])=rac1{|O|}sum_{Iin O}(-1)^{|Icap T|},
qquad |phi_O|_inftyle1.
]
The target coordinate is the same expectation under the uniform balanced-label law (u_{m bal}). The moment residual implies that at least one retained test has expectation gap greater than (1/2665). Since
[
|mathbb E_P f-mathbb E_Q f|
le 2,mathrm{TV}(P,Q)
quad	ext{for }|f|_inftyle1,
]
every mixture on this exact pool satisfies
[
oxed{mathrm{TV}(w_p,u_{m bal})>rac1{5330}.}
]
Equivalently, the corresponding dephased program-label registers have trace distance greater than (1/5330).

This is a **finite-pool classical program-mass** statement. It is not a Choi-state trace-distance or channel diamond-distance lower bound.

## 4. Reproducibility

- LP discovery: [discover_ising_full_fourth_plus_eight_gapped_n21.py](discover_ising_full_fourth_plus_eight_gapped_n21.py)
- Independent 128-/512-bit Arb verifier: [verify_ising_full_fourth_plus_eight_gapped_arb_n21.py](verify_ising_full_fourth_plus_eight_gapped_arb_n21.py)
- Floating diagnostic: [ising_full_fourth_plus_eight_gapped_n21.json](evidence/ising_full_fourth_plus_eight_gapped_n21.json)
- Rational Arb certificate: [ising_full_fourth_plus_eight_gapped_arb_n21.json](evidence/ising_full_fourth_plus_eight_gapped_arb_n21.json)
- Successful CI: [45469881533](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45469881533)
- Certificate commit: [053032e](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/053032e2fbe094448076e29883fa8f7285f40920)

The verifier checks all 6,131 columns, the exact scaled-(ell_1) normalization, the full-coordinate norm, and the strict (1/5) common gap. The workflow pins NumPy 2.3.5, SciPy 1.17.0, python-flint 0.9.0, and Python 3.12.14.

## 5. Scope and next decisive test

Theorem 1 is a finite-pool statement. It does not cover arbitrary nonuniform positive couplings or all multi-segment open paths. The eight gapped paths are witnesses, not an exhaustive parameterization of that continuum. It does not impose every even principal minor and does not imply an operational Choi/diamond converse.

The next test prices this exact 82-term rational dual over the connected and multi-segment general-gapped families:

- [Deterministic discovery search](search_ising_full_fourth_plus_eight_gapped_n21.py)
- [Independent 256-bit Arb escape verifier](verify_ising_full_fourth_plus_eight_gapped_escape_arb_n21.py)
- [Search workflow](.github/workflows/eui-search-6131-full-fourth-gapped.yml)

A certified negative target-minus-score interval will refute extension of this **particular** 6,131-column dual to the tested continuous family, without invalidating Theorem 1. Failure to find an escape is only a finite multistart search result, not a continuum proof. The paper-central problem remains an exact positive ensemble satisfying every even-principal-minor constraint at (n=21), or a genuinely global physical-family obstruction, followed by an operational bridge to Choi/channel diamond error.
