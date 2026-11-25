# Exact obstruction for 3–7 consecutive perfect-mirror segments at n=21

Date: 2026-11-25.

This note strengthens the exact three-segment result to every ordered
composition of 42 into 3, 4, 5, 6, or 7 consecutive perfect-mirror blocks.
The proof is a finite exhaustive enumeration, but every arithmetic operation
in the enumeration is integer/rational exact. It is **not** a theorem for
arbitrary couplings or for an unbounded number of segments.

## 1. Physical family

Set (N=42), (n=21). Let
[
(L_1,ldots,L_k)inmathbb N^k,qquad
sum_{a=1}^k L_a=42,qquad kin{3,4,5,6,7}.
]
These lengths partition the open path into (k) consecutive blocks. On a
block of length (L), beginning at site (s), use
[
A_{s+r,s+r+1}
=rac{pi}{2}sqrt{(r+1)(L-r-1)},qquad
A_{s+r+1,s+r}=-A_{s+r,s+r+1}
]
for (r=0,ldots,L-2), with all inter-block and wrap couplings zero.
Equivalently, the physical Ising/Majorana couplings are
[
c_{s+r}=rac{pi}{4}sqrt{(r+1)(L-r-1)}.
]
The spin-((L-1)/2) pi rotation gives the signed reversal
[
R^{(L)}_{r,L-1-r}=(-1)^r,
qquad R^{(L)}_{ij}=0quad	ext{otherwise}.
]
For (L=1), this is the identity on a singleton. The full (R) is the direct
sum of the block reversals. Each signed reversal has determinant (+1), so
(Rin SO(42)) exactly.

The number of ordered compositions for fixed (k) is
(inom{41}{k-1}). The five families contain
[
820+10,660+101,270+749,398+4,496,388
=5,358,536
]
distinct ordered compositions in total.

## 2. One exact dual for all five segment counts

For (d=1,ldots,21), define the complete distance-averaged second moments
[
m_d(R)=rac1{42}sum_{i=0}^{41}
det R_{{i,i+d},{i,i+d}},
qquad
t_d=rac{(-1)^{d+1}}{41},
]
with cyclic indices. These are all 21 second-order distance orbits of the
balanced-program target.

Use the fixed rational dual
[
y=rac1{47}(
-10,8,-6,6,-4,2,-2,2,0,2,0,0,0,0,0,0,2,-2,0,0,1).
]
Its exact norm is (|y|_1=1).

### Exact pair-count formula

Let (S_d=42m_d(R)). Each block of length (L) contributes one
transposition pair for each (r=0,ldots,lfloor L/2floor-1). The
corresponding (2	imes2) principal minor is exactly ((-1)^L), and its
cyclic distance is
[
d=min(L-1-2r,;42-(L-1-2r)).
]
If (L) is odd, the block also has one fixed centre
[
p=s+(L-1)/2,qquad sigma=(-1)^{(L-1)/2}.
]
Every pair of fixed centres from distinct blocks contributes
(sigma_asigma_b) at their cyclic separation. No other pair has a
nonzero (2	imes2) principal minor. In the sum over (i), an unordered
pair at distance (d<21) occurs once, while an antipodal pair at (d=21)
occurs twice. This gives an integer formula for every (S_d), hence for
[
Delta(L_1,ldots,L_k)
=y^{mathsf T}(t-m(R))
=rac{sum_{d=1}^{21} q_d
igl(42(-1)^{d+1}-41S_digr)}{47cdot41cdot42},
]
where (q=47y) is the displayed integer vector.

### Exhaustive exact census

The verifier enumerates every cut set (equivalently every positive
composition), evaluates the pair-count formula using integers only, and
checks the resulting exact rational extrema. It also compares the formula
against a direct signed-permutation construction on 700 deterministic
random compositions, checking all 21 moment sums and (det R=1).

| Number of blocks (k) | Compositions | Exact minimum slack | Attainers | Exact maximum slack | Distinct slacks |
|---:|---:|---:|---:|---:|---:|
| 3 | 820 | (2/40467) | 117 | (192/13489) | 15 |
| 4 | 10,660 | (2/40467) | 38 | (1027/40467) | 26 |
| 5 | 101,270 | (4/1927) | 30 | (1478/40467) | 35 |
| 6 | 749,398 | (4/1927) | 6 | (86/1927) | 43 |
| 7 | 4,496,388 | (166/40467) | 7 | (299/5781) | 48 |

There are no nonpositive slacks in any of the 5,358,536 cases. The common
minimum over the union is therefore
[
oxed{min_{3le kle7};min_{L_1+cdots+L_k=42}
Delta(L_1,ldots,L_k)=rac{2}{40467}>0.}
]

**Theorem.** Every probability measure supported on the union of all
three-, four-, five-, six-, and seven-block perfect-mirror seeds obeys
[
oxed{
left|t-mathbb E_mu m(R)ight|_infty
ge rac{2}{40467}.
}
]
Indeed, the exact dual gap is at least (2/40467) on every atom and hence
on every convex mixture. Since (|y|_1=1), Holder's inequality gives the
stated infinity-norm residual. The bound is non-strict because the exact
minimum is attained.

The same moment gap is invariant under dihedral images (the moments are
cyclic distance averages) and under vertex-sign gauges (Rmapsto SRS),
because every principal minor is unchanged by diagonal sign conjugation.

## 3. Program-mass total-variation corollary

For each distance (d), define the bounded balanced-label character
[
phi_d([T])=rac1{42}sum_{i=0}^{41}
(-1)^{|{i,i+d}cap T|},
qquad |phi_d|le1.
]
The exact program/principal-minor identity gives
[
mathbb E_{w_R}phi_d=m_d(R),qquad
mathbb E_{u_{m bal}}phi_d=t_d.
]
Thus (G=sum_d y_dphi_d) has (|G|_inftyle|y|_1=1), and
[
mathbb E_{u_{m bal}}G-mathbb E_{w_mu}G
gerac{2}{40467}.
]
The total-variation dual inequality therefore yields
[
oxed{operatorname{TV}(w_mu,u_{m bal})gerac1{40467}.}
]
Equivalently, this is a trace-distance lower bound (one-half trace-norm
convention) for the associated dephased classical program-label registers.
It is **not** a Choi-state trace-distance or channel diamond-norm bound.

## 4. Explicit scope boundary

This particular dual does not cover two blocks: for the composition
((1,41)), its exact slack is (-80/40467). The separate two-mirror
obstruction uses a different certificate. The present theorem also does
not cover (kge8), arbitrary nonuniform couplings within a block, general
gapped paths, or the full all-even-principal-minor system. In particular,
it is not a global obstruction for the continuous physical family.

## 5. Reproduction

Run:
```bash
python verify_ising_three_to_seven_mirror_segment_obstruction.py \
  --output /tmp/three_to_seven_mirror.json
```
Then compare the generated JSON with
`evidence/ising_three_to_seven_mirror_segment_obstruction_n21.json`.
The dependency-free GitHub Actions workflow performs this full exhaustive
check and compares the parsed JSON objects exactly.

Primary artifacts:
- [Exact verifier](verify_ising_three_to_seven_mirror_segment_obstruction.py)
- [Machine-readable evidence](evidence/ising_three_to_seven_mirror_segment_obstruction_n21.json)
- [CI workflow](.github/workflows/eui-three-to-seven-mirror-segment-obstruction.yml)
