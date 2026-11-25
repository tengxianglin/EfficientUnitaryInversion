# EUI manuscript/research audit — Run 32 (2026-11-26)

## Repository and issue state

- Repository: `tengxianglin/EfficientUnitaryInversion`, default branch `main`.
- HEAD at start of this run: `ac55b84fa89d86875640a7f896bb049497b7438d`.
- HEAD before this audit note: `dd9e86e3ed32c760c24c5fd311283c640003040d`.
- Recursive tree: 1,131 paths, not truncated.
- No editable `.tex`, `.bib`, `.pdf`, `.doc`, or `.docx` manuscript/supplement source found.
- Open issues rechecked: #7 physical cycle-family convex hull; #5 finite-pool/full-family gap; #6 Appendix B noise normalization; #3 classifier correctness.
- Issue #7 received two new comments this run: the rank-one spectral-collapse no-go (comment 7171375194) and the stronger N=8 period-two single-atom no-go (comment 7171507132).

## Scientific work completed

### A. General rank-one spectral-collapse limitation

The exact N=4/N=6 alternating construction uses one uniform parity-block mode and puts every nonuniform singular frequency at an odd multiple of pi. In that class,
`det(Q_I)=(-1)^p(1-2 gamma r/n+2 gamma p q/n^2)`.
The order-two target forces `cos(lambda)=(n-1)^2/(2n-1)`, which is >1 for every n>=4 (N>=8), and equals 400/41 at N=42. The same argument excludes probability mixtures confined to this fixed-parity rank-one-collapse class.

Artifacts:
- `THEORY_ALTERNATING_SPECTRAL_COLLAPSE_NO_GO.md`
- `verify_alternating_spectral_collapse_no_go.py`
- `evidence/alternating_spectral_collapse_no_go.json`
- `.github/workflows/eui-alternating-spectral-collapse-no-go.yml`

The first CI attempt failed on a summary-print JSON key after compilation. This was corrected in commit `d7068b7e758825354396a91c98b26171f74e04cd`; rerun [45678440640](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45678440640) succeeded. Exact checks covered all 7 nonempty even subsets at N=4, all 31 at N=6, and the rational cosine obstruction for n=4,...,21.

### B. Stronger N=8 no-go for all period-two couplings, not just spectral collapse

A separate exact argument now rules out **any single N=8 physical cycle exponential with arbitrary real alternating couplings** as a realization of the complete second-order target. It uses only:
- normal-circulant parity block (B=2(aI-bT));
- pair-minor constraints forcing a constant magnitude for all off-diagonal entries of (C) and all entries of (S);
- the orthogonality identity (C^2+SS^T=I);
- exhaustive exact enumeration of the 16 possible circulant sign rows for (S/s).

The sign-correlation pairs are exactly {(2,2),(-2,2),(0,0),(0,-2)}. The orthogonality equations leave only (R_2=0) or 2. The first forces (1/7=0); the second forces (z=9/49>1/7), contradicting (z\le1/7). Therefore no such single atom exists.

Artifacts:
- `THEORY_N8_ALTERNATING_CYCLE_SECOND_ORDER_NO_GO.md`
- `verify_n8_alternating_cycle_second_order_no_go.py`
- `evidence/n8_alternating_cycle_second_order_no_go.json`
- `.github/workflows/eui-n8-alternating-cycle-second-order-no-go.yml`

Workflow [45679384306](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45679384306) succeeded. It compiled the verifier, exhausted all 16 sign rows, and reproduced the exact correlation-pair set and (9/49>1/7) contradiction.

## Evidence classification and scope

- **Analytically proved:** no N=8 single-atom realization with period-two couplings, for arbitrary real coupling values, already at order two.
- **Analytically proved:** no N>=8 single atom or positive mixture within the narrower fixed-parity rank-one spectral-collapse ansatz.
- **Exact finite enumeration:** all 16 circulant sign rows at N=8; all even-minor checks for N=4/N=6 from the earlier construction.
- **Not proved:** no mixture of general period-two atoms at N=8; no impossibility for arbitrary non-period-two couplings; no N=42 full physical convex-hull result; no Choi/diamond operational bridge.
- **Manuscript blocker:** no editable manuscript source found; only repository theory/audit notes were changed.

## Next highest-value action

Generalize the N=8 sign-correlation method to odd parity-block size (n=21). For a period-two N=42 atom, pair-minor matching again forces all off-diagonal entries of (C) and all entries of (S) to have fixed magnitudes. Derive the resulting autocorrelation constraints for length-21 circulant sign sequences and determine whether they are inconsistent. In parallel, keep the convex-mixture problem distinct: a single-atom no-go is not a no-go for the physical convex hull.
