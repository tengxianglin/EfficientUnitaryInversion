# EUI manuscript/research audit — Run 64 (2026-11-27)

## Repository and issue inspection

- Starting main HEAD: 7d5eec0e72e88350bc1494d4f46d77a804e2f9eb (Run 63 all-order hierarchy audit).
- Inspected recent commits, current open Issues, the full Issue #7 body and latest comments, the N=42 period-two six-quartic support, its 256-bit Arb verifier/certificate, the all-order hierarchy note/evidence, the projection-DPP note, the conditional joint-parity diamond theorem, and the public-paper/source audit.
- Active scientific tracks remain #7 (physical full-moment reachability), #5 (finite-pool/full-family gap), #6 (Appendix B normalization and QuAIRKit rerun), and #3 (classifier/runtime smoke test). Issue #7 was selected because its latest six-quartic N=42 candidate had never been priced against every quartic orbit.
- The public manuscript remains arXiv:2506.20570v1. The repository audit still finds no editable TeX/Bib or separate supplementary source; no manuscript-body edit is claimed.

## New decisive verification

Added an independent 256-bit Arb audit of the frozen N=42 period-two six-quartic candidate.

The 37 positive base atoms and their one-site translates form a 74-labelled-atom ensemble. Translation and reflection act on Q=R D by a global sign or an alternating diagonal sign gauge, with the paired (a,b)/(b,a) support carrying equal weights. Hence every even-principal-minor moment is D_42-invariant and one representative per dihedral orbit suffices.

The verifier:
- enumerates all 111,930 four-subsets;
- canonicalizes them into exactly 1,440 D_42 orbits and checks the orbit-size sum;
- reconstructs the exact-real weights from the frozen 37-by-37 system;
- prices all 1,440 quartic orbit representatives at 256-bit Arb precision.

Result:
- six residual intervals contain zero, exactly the six defining witness orbits;
- 1,434 residual intervals strictly exclude zero;
- a concrete strict counterexample is I={0,3,19,26}, orbit size 42:
  \[
  \bar m_I-\frac1{533}
  \in[0.005509503755929284915567732180788367406955648096182998091152476861460514
  \pm3.56\times10^{-73}]>0.
  \]

This is a rigorous rejection of the frozen 37-base/74-labelled support with its uniquely reconstructed weights. It is not a no-go for all period-two mixtures or the full cycle family.

## Reproducibility and commits

Added:
- verify_n42_period_two_six_quartic_all_orbits_arb.py
- .github/workflows/eui-n42-period-two-six-quartic-all-orbits.yml
- evidence/n42_period_two_six_quartic_all_orbits_arb.json
- THEORY_N42_PERIOD_TWO_SIX_QUARTIC_ALL_ORBITS_AUDIT.md

Workflow 46022836608 completed SUCCESS on the code/workflow head. It compiled both verifiers, installed python-flint==0.9.0, recomputed all 1,440 orbit intervals, committed the deterministic 17,317-line certificate, and uploaded the artifact.

Commits:
- 69665621cac84e04303bca2147837b269c6d7fb4 — all-orbit verifier
- b6d1763b6392008280db971190c6e3bf1b862fc6 — CI workflow
- 9d1b8693d23a7f6b4a50eb3ed349db42fd49977f — Arb all-orbit certificate
- b8c5ebacdef2efc7711edac803322bb20cb6049c — theory note

## Manuscript boundary

The new result concerns the static physical cycle-exponential moment design, not the broader manuscript's average Choi-fidelity robustness experiment. No program-moment residual is relabelled as a Choi or diamond bound. The conditional joint-parity diamond theorem still requires one legal ensemble uniform in both parity sectors at n=21; this run does not supply that hypothesis.

## Remaining blockers and next highest-value action

1. N=42 complete positive physical ensemble remains open.
2. No global physical-family separator has been proved.
3. The 1,314-row pair/quartic system is still a low-order relaxation; all-order hierarchy leaves many higher-order coordinates.
4. The exact moment-to-operational-error bridge for the manuscript's intended claim remains separate.
5. Issue #6 still lacks the pinned QuAIRKit full Appendix B table regeneration and editable manuscript source.

Next action: directed column generation against all 1,440 quartic orbit rows, starting from the exact pair constraints and pricing new strictly positive period-two atoms. A finite-pool result must remain explicitly pool-specific; any global conclusion needs a uniform bound over all positive (a,b).
