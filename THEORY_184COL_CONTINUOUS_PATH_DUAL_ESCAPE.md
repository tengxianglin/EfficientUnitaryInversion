# Strict continuous-path escape from the 184-column mixed-order dual

Date: 2026-11-23

## Result

The exact rational dual certificate for the fixed 184-column / 2,113-row mixed-order LP is **not** a global separator for the unrestricted positive 41-edge open-path family.

The dual score is
\[
S_{184}(c)=\lambda_{184}-\delta_{184}
+\sum_{r=0}^{2112}z_r a_r(c),
\]
where the exact rational vector \(z\), scalar \(\lambda_{184}\), slack
\(\delta_{184}\), row inventory, and normalization scales are frozen in
\texttt{evidence/55probe_184col_full_sixth_cut_dual_certificate_n21.json}.
The 50 nonzero dual coordinates comprise two complete low-order rows, 46
selected/cut sixth-order rows, and two selected eighth-order rows.

For a 42-site open path, let
\[
K(c)_{j,j+1}=2c_j,\qquad K(c)_{j+1,j}=-2c_j,
\quad j=0,\ldots,40,
\]
with all other entries zero and \(c_{41}=0\), and put \(R(c)=e^{K(c)}\).

The following exact-decimal-rational coupling vector is a physical escape:
\[
\begin{aligned}
c=(&1.557209608315,\ 0.000672972016,\ 14.183148223252,\
&0.000432314830,\ 0.000653424974,\ 37.676061575771,\
&0.000648907230,\ 6.279008390849,\ 0.001352870027,\
&33.074601335144,\ 0.001648995477,\ 1.537814014376,\
&0.001801459321,\ 25.137251163187,\ 0.001291570530,\
&26.668821401122,\ 1.245143988236,\ 0.182707156520,\
&0.001702636465,\ 17.127005052415,\ 2.605194390503,\
&0.000836857224,\ 18.838700828271,\ 0.000512607335,\
&2.000016627127,\ 0.000863681145,\ 42.406284123354,\
&0.000716524273,\ 32.682133380522,\ 4.419040918995,\
&0.432998773341,\ 0.396792287987,\ 18.872987550827,\
&0.001243553964,\ 73.762430476692,\ 0.000672463529,\
&0.180190571989,\ 0.000699183542,\ 1.524912694397,\
&0.001730038960,\ 22.026102321790,\ 0).
\end{aligned}
\]
Every one of the 41 open-path edge magnitudes is strictly positive. The
candidate is distinct from the previously certified continuous escape and
is outside the frozen 1,641-column canonical inventory.

At 128-bit Arb precision, rebuilding the matrix exponential and all 50
active principal-minor features from these exact rational inputs gives
\[
\boxed{
S_{184}(c)\in
[558.5197275383090425573204756469618
\;\pm\;6.20\times10^{-32}]>0.
}
\]
In particular, the certified lower endpoint is
\[
[558.51972753830904255732047564696182650
\;\pm\;3.37\times10^{-36}]>0.
\]
Thus the universal inequality \(S_{184}(c)\le0\) fails strictly on the
continuous physical family.

## Reproducibility and provenance

- Corrected differentiable discovery: \texttt{discover_184col_continuous_dual_escape.py}.
- Independent exact-input verifier: \texttt{verify_184col_continuous_dual_escape_arb.py}.
- Workflow: [45115018787](https://github.com/tengxianglin/EfficientUnitaryInversion/actions/runs/45115018787).
- Evidence commit: [026ae00](https://github.com/tengxianglin/EfficientUnitaryInversion/commit/026ae00d44e8d3826c881a648293469bb3c81135).
- Search evidence: \texttt{evidence/184col_continuous_dual_search_n21.json}.
- Arb evidence: \texttt{evidence/184col_continuous_dual_escape_arb_n21.json}.
- Exact candidate SHA256: \texttt{a9d1aac1680d59d907a83733fbd5262f7bb09b8ab664e2bd0a83560fb04ef2d0}.
- Parent 184-column dual SHA256: \texttt{143adc0d0c3eac2732ae45f4e441be8ab9f53c304bf52e1c8fd7ec744d58295e}.
- Parent LP SHA256: \texttt{894405a7e879c05d69d71d5e2c67c82e47736842781221ce8c2c42011704687e}.
- Frozen 2,113-row cut-design SHA256: \texttt{d1ad14762d00aa7e9dcdc197898273ac3b91bf8244f2c65c31072f761e22694f}.

The discovery routine uses cofactor derivatives of principal minors and the
adjoint Frechet derivative of the matrix exponential. Its analytic gradient
was checked against complex-step differentiation at coordinates 0, 20, and
40, with maximum relative defect \(7.97\times10^{-13}\). As a regression
invariant, the same routine reproduces the Arb-certified score of the
already-included continuous column 1641 to within \(10^{-8}\). The final
candidate is then independently recomputed with exact rational inputs and
Arb; no optimizer output is used in the proof.

## Scope

This result disproves **only** the attempted global extension of this
particular 184-column dual. It does not invalidate the 184-column finite-pool
theorem: that theorem still applies to its pinned 184 generators, and its
full-canonical-pool extension still applies to the frozen 1,641 canonical
paths plus the one previously pinned continuous escape.

The new path is a second continuous-family escape. Its positive pricing
score is not a feasible ensemble and does not establish that any probability
mixture over the full continuous family reaches the \(1/3\) moment cap.
It also says nothing by itself about Choi infidelity or diamond distance.

## Next decisive step

Append this exact path as a new column to the 184-column discovery pool,
re-solve the same 2,113-row minimax LP, rationalize any new dual, and
independently Arb-certify it. A subsequent search must test the new dual
against the unrestricted continuous path family again; the present escape
must not be silently reused as a proof of global feasibility or infeasibility.


## Differentiable discovery formula (not part of the proof)

For a row feature built from principal minors, the derivative with respect to
the rotation matrix is a sum of cofactor matrices. If
\(G=\nabla_R S_{184}\), the adjoint Frechet derivative gives
\[
\nabla_K S_{184}=L_{\exp}(K^\mathsf T,G),
\]
where \(L_{\exp}(A,E)=D\exp(A)[E]\). Since
\[
\frac{\partial K}{\partial c_j}
=2(E_{j,j+1}-E_{j+1,j}),
\]
the edge derivative is
\[
\frac{\partial S_{184}}{\partial c_j}
=2\big[(\nabla_K S_{184})_{j,j+1}
-(\nabla_K S_{184})_{j+1,j}\big].
\]
The discovery code uses this cofactor/Frechet formula. Its complex-step check
is an implementation diagnostic only; the mathematical counterexample is
certified independently by the exact-rational Arb evaluation above. The
Frechet derivative identity is standard matrix calculus and is not claimed
as a new EUI mechanism.
