# THEORETICAL DERIVATION — coefficient promises after T4

Date: 2026-10-15. Status: Pro analytic derivation with additional local exact checks; the new T5 representation/reduction certificate has not yet been independently executed by Codex. This document is not a novelty claim.

## 1. Evidence and input integrity

The supplied outer ZIP is truncated at 5,898,240 bytes and lacks its central directory. Its SHA-256 is `b36a77297af0a4df5ce8b92a71c81f38817f6179254032ee006f5959350e283f`. Recovery validated CRC32 for 748 complete local members, including the delivery manifest. All 747 recovered members listed in that manifest matched their SHA-256 and byte counts. The complete inner raw-evidence ZIP passes its own CRC test; it supplies another 47 missing members with hashes identical to the outer manifest. Eighteen other inner historical members differ from the outer portable projection and were NOT substituted; two members have no inner counterpart. Thus 794 of 814 declared outer files are recovered/hash-matched, not the entire outer archive. All mathematical premises and files required below are present and hash-matched. The reports preserve this distinction.

Read: `codex_verdict.md`, `claim_ledger.json`, `proofs/T1.md`, `proofs/one_query_audit.md`, `proofs/T3.md`, `proofs/T4.md`, the requested T3 summaries/saved-artifact audit, T4 full per-family coefficient JSON, final independent verification and fixed-map diagnostics. The packet includes their verified bytes and the received R1 ZIP and raw-evidence ZIP, preserving historical counterexamples and nonzero-phase controls.

The package records revision `28c7e0ffb833a88f6980011ffecf48c7fbe2f1b1`, branch `codex/eui-grid-pro-20261014`, repository `https://github.com/tengxianglin/EfficientUnitaryInversion`, R2 path `research/grid_discovery_20261014_r2_20261014T091523Z`. This is the received historical receipt, not a new live Git readback or a Pro push.

Retained facts: independent T1 gives 973 types/37 orbits; T2 establishes the phase-aware/shared-origin and comb machinery; T3 supplies coherent physical constructions. None requires recensus. T4 computes actual whole-matrix coefficient spans, not their Pauli support unions:

| Grid | Independent span | Row full/even/odd | Column full/even/odd | Uniform full/even/odd |
|---|---:|---:|---:|---:|
| matched q4 partial | 10 | 7/7/7 | 4/4/4 | 3/3/3 |
| matched q4 saturated | 16 | 7/7/7 | 5/5/5 | 3/3/3 |
| B4q0 | 16 | 12/12/12 | 12/12/12 | 6/5/5 |
| B55q0 | 16 | 6/2/4 | 6/2/4 | 4/2/2 |

All twelve tied support unions exceed the actual spans. T4's 82 asymmetric rays among 216 establish global dagger/star impossibility for the first nine families; the 54 symmetric B55 rays alone are not an existence theorem. B55 star probability one and dagger probability one quarter were already inherited, not unresolved.

## 2. Focused primary-literature check and route decision

Search performed live on 2026-10-15. Scope: promise-dependent inversion, physical one-query supermaps, parameter-dependent phases, matrix/operator-space extension, and spectral sign reversal. The six load-bearing sources below were accessed as full text, not merely abstracts. For the two PDF sources, decisive pages were also inspected as screenshots. Metadata pages were used for dates/DOIs. This focused search is neither exhaustive nor a novelty certificate.

1. **Mo, Lin, Wang (2025), _Efficient Inversion of Unknown Unitary Operations with Structured Hamiltonians_.** arXiv v1, 25 June 2025. [Full text](https://arxiv.org/html/2506.20570v1), [DOI](https://doi.org/10.48550/arXiv.2506.20570). Inspected setup §§II–III, Theorem 1/Corollary 2 and the one-query statement on printed p.2. Independent Pauli coefficients permit generatorwise anticommutation tests. **Adapt**, not blindly reuse: tying coefficients requires flipping the actual sums; a Pauli-support obstruction need not survive. The uniform sign-reversal principle is known.

2. **Chiribella, D'Ariano, Perinotti (2008), _Transforming quantum operations: quantum supermaps_.** EPL 83, 30004. [Full text](https://arxiv.org/html/0804.0180v2), [DOI](https://doi.org/10.1209/0295-5075/83/30004). Inspected Theorems 1–2 and Eqs. (23)–(24): pre/post isometries, memory, and heralded projection. **Retain** the physical-comb model. A linear map on oracle amplitudes is not automatically a normalized physical supermap.

3. **Quintino et al. (2019), _Probabilistic exact universal quantum circuits for transforming unitary operations_.** PRA 100, 062339. [Full text](https://arxiv.org/html/1909.01366v2), [DOI](https://doi.org/10.1103/PhysRevA.100.062339). Inspected §III's Choi-span formulation, Eq. (39) and Eqs. (41)–(44)'s parameter-phase/Fourier argument, §VI.1 and Theorem 2. One-query universal transpose has optimum 1/d². **Retain the known bound only after a valid reduction**; neither universal U(8) statements nor parent-promise bounds apply automatically here. Its Choi span is not to be confused with our amplitude matrix span.

4. **Odake, Yoshida, Murao (2025), _Analytical Lower Bound on Query Complexity for Transformations of Unknown Unitary Operations_.** PRL 135, 230603; inspected arXiv v4, 25 November 2025. [Full text](https://arxiv.org/html/2405.07625v4), [DOI](https://doi.org/10.1103/drp2-rzzw). Appendix C, Eqs. (74)–(75), addresses Lie-subgroup promises; Appendix D, Theorem S6, Eqs. (112), (113), (115), allows success probability and phase dependence. Its probabilistic test is a local first-derivative necessary condition. **Retain as a comparison**, not a replacement for the all-parameter span proof; the tied exponential promise is not automatically a Lie subgroup.

5. **Heinosaari, Jivulescu, Reeb, Wolf (2012), _Extending quantum operations_.** JMP 53, 102208. [Full text](https://arxiv.org/html/1205.0641), [DOI](https://doi.org/10.1063/1.4755845). Inspected Theorem 4, §6.1/Example 5 and §6.2. CP extension and simultaneous normalization are distinct constraints. **Retain this warning**, but do not identify an oracle-amplitude map with a CP state map. Below an explicit scaled query circuit, rather than a bare linear extension, establishes positive success.

6. **Schulte-Herbrüggen, Spörl (2006), _Which Quantum Evolutions Can Be Reversed by Local Unitary Operations? Algebraic Classification and Gradient-Flow-Based Numerical Checks_.** arXiv quant-ph/0610061, 9 October 2006. [Full PDF](https://arxiv.org/pdf/quant-ph/0610061), [DOI](https://doi.org/10.48550/arXiv.quant-ph/0610061). Inspected printed pp.3–4, Eqs. (15)–(17), and “Algebra I: Eigenoperators.” For unrestricted unitary conjugation, reflected eigenvalues with matched multiplicities give sign reversal; additional locality constraints are separate. **Adapt the known spectral-pair construction**. No optimizer is warranted for B55 uniform.

Decision: retain phase-aware amplitude rigidity and physical comb normalization; replace support cropping and proposed optimization with a phase-centred graded-span criterion and a heralded matrix-corner reduction. The one-quarter bound and spectral-reflection mechanism are known ingredients. The particular tied-family representation, its reduction interface and its certified application are the proposed increment. Priority/novelty of this combination remains literature-dependent and is not established by the search.

## 3. Model and all-parameter amplitude theorem

Let H(α)=Σ α_j H_j on C^N, with known Hermitian H_j and α ranging over all R^m, including zero. U(α)=exp[-iH(α)]. A protocol uses one unconditional forward U, parameter-independent processing, arbitrary finite memory and a finite exact heralded instrument. Equality is equality of CP maps on every input and reference. Targets are fixed computational-basis representatives U†, U*, U^T, separately. There is no controlled-U assumption.

After purification, each successful Kraus branch is a complex-linear oracle-amplitude map

    L_mu(X)=K_mu (X⊗I_M) E,
    E†E=I,  Σ_success K_mu†K_mu≤I.

Rank-one target Choi output forces L_mu(U(α))=a_mu(α)F(U(α)), including zero-probability points. Initially neither a common phase nor constant success is assumed.

For a fixed ray H(β) with distinct spectral set S_β, normalized traces against its spectral projectors extract finite exponential polynomials. Their frequency intersections are

    Γ_T = ⋂_{λ∈S}(S−λ)={0},
    Γ_- = ⋂_{λ∈S}(S+λ).

The second is empty or {γ_β}, where γ_β=min S+max S and S=γ_β−S. Degeneracy is removed only for this frequency test, not for physical encodings. Linear independence of finite exponentials gives

    T:   a_mu(tβ)=c_mu;
    †,*: a_mu(tβ)=c_mu exp(−itγ_β), or identically zero.

All rays share U(0)=F(I)=I, hence c_mu=a_mu(0) is branch-dependent but ray-independent. A branch zero at the origin is identically zero. Any asymmetric ray kills every successful branch globally. Consequently any nonzero exact protocol has constant positive probability Σ|c_mu|².

There is a further global restriction. Pick a nonzero dagger branch and differentiate at t=0:

    L_mu(H(β))/c_mu = γ_β I − H(β).                 (1)

For star replace H on the right by H^T. Taking trace proves γ_β is a single real linear functional ℓ(β), since the left side and H are linear in β. Thus all surviving branches have

    a_mu(α)=c_mu exp[−iℓ(α)],                     (2)

with the same ℓ, although their constant phases c_mu can differ. Raywise reflection by itself does not establish this global compatibility or a physical circuit.

## 4. Phase-centred graded coefficient criterion, with a physical completion

Set G(α)=H(α)−ℓ(α)I/2 and V(α)=exp[−iG(α)]. Let E_+(G) and E_-(G) be the complex spans of all whole coefficient matrices of the even and odd powers of G, respectively, with I included in E_+. Mixed derivatives at the origin show span{V(α)}=E_++E_-. These are matrix spans, not coordinate support unions. For N=8, Cayley–Hamilton on G closes the full span through degree7, while Cayley–Hamilton on G² separately closes even through14 and odd through15.

**Theorem (positive success, not optimum).** Under §3, a nonzero exact one-query dagger protocol exists if and only if there is a real linear ℓ such that

    E_+(H−ℓI/2) ∩ E_-(H−ℓI/2) = {0}.           (3)

The same equivalence holds for star. This does not identify their optimal probabilities, nor impose ancilla restrictions.

Necessity: (2) and scalar linearity give L_mu(V)=c_mu V†. Comparing Taylor coefficients forces L_mu/c_mu to be +identity on E_+ and −identity on E_-. Any intersection must therefore be zero. Star has the same conclusion after composing with transpose.

Sufficiency at the amplitude level: define J(X_++X_-)=X_+−X_-. It is well-defined exactly when (3) holds, and its exponential series gives J(V)=V†. Consequently J(U)=exp[−iℓ(α)]U†. For star use T∘J. Extend the resulting complex-linear amplitude map F from the actual span to M_N in any fixed way.

**The physical step cannot be skipped.** Write

    F(X)_{oi}=Σ_{ab} f_{oi;ab} X_{ab},
    B_{o;a,r,s}=f_{os;ar},
    E_0|ψ> = |Φ_N>_{b r}⊗|ψ>_s,
    |Φ_N>=N^(−1/2)Σ_b|b b>.

Here B is an N×N³ matrix, query wire b becomes a, and r,s are memory. Let κ=||B||_op (or the conservative ||B||_F) and K=B/κ. Then E_0†E_0=I, K†K≤I, and

    K (U⊗I) E_0 = F(U)/(√N κ).                 (4)

Completing the postmeasurement by failure Kraus operators is a valid CP instrument. It succeeds with constant p=1/(Nκ²)>0 on the promised family. The query is the original physical oracle, acting once on half of a known entangled state; the external input is stored coherently. No CP property of F as a density-matrix map is assumed. Thus a fixed linear extension alone is diagnostic, while (4) supplies the missing scaled physical certificate. There is no implication that the scale is optimal or memory-efficient.

**Phase control.** H=diag(−3,1,1,1) has ℓ(t)=−2t and G=H+I with eigenvalues ±2. Its shifted graded spaces are disjoint, whereas the unshifted even/odd spaces both span {I,H}. With P_- rank1 and P_+ rank3,

    F(X)=Tr(P_-X)P_+ + Tr(P_+X)P_-/3

satisfies F(U(t))=exp(2it)U(t)†. The Frobenius choice in (4) gives κ²=10/3 and p=3/40. This explicit construction shows why an unshifted constant-amplitude test is not a general impossibility test. It does not claim ancilla-free spectral pairing with mismatched multiplicities.

For transpose, amplitudes are constant without centring and a scaled physical construction is always available. Non-invariance T(E)⊄E is not an impossibility criterion: the output map may take values in all M_N.

## 5. Apply the evidence: the nine negative families and B55 structure

For the first nine tied families, the retained asymmetric-ray/shared-I certificates already force p_dagger=p_star=0 for the entire real parameter domain. There is no experiment to repeat. Their unshifted graded intersections alone would not have proved the phase-aware statement; the asymmetric rays do.

For B55 the actual row-major physical grid is

    XII   ZII   YII
    ZXI   YIY   XXY
    YXI   XIY   ZXY.

Let R=IXI, S=IIY, Π_rs=(I+rR)(I+sS)/4, Π_0=Π_++, and Π_c=I−Π_0. All four Π_rs have rank2. The centre is coherent; S is complex, and transpose interchanges s and −s. No original physical implementation may measure these labels and replace their superpositions by classical cases.

For either row or column tying, write H(β)=Σ_j β_j H_j. In sector (r,s), its first-qubit Bloch vector is A_rs β. The ++ sector has A_++ equal to the all-ones 3×3 matrix. In the other sectors choose

    A0=A_(+,-)=[[1,-1,-1],[1,-1,1],[1,1,-1]],
    A0^(-1)=[[0,1/2,1/2],[-1/2,0,1/2],[-1/2,1/2,0]].

Each nontrivial-sector A has A^T A=4I−11^T and det A=−4; hence A A0^(-1) is in SO(3), not an orientation-reversing equivalence. The exact rotations are:

    row:    I, [[0,1,0],[0,0,1],[1,0,0]], [[0,0,1],[1,0,0],[0,1,0]];
    column: I, [[0,0,1],[-1,0,0],[0,-1,0]], [[0,1,0],[0,0,-1],[-1,0,0]],

in sector order (+,−),(−,+),(−,−). Known qubit unitaries implement these rotations. Thus a fixed coherent encoding yields

    H(β) ≅ (β1+β2+β3)(X+Y+Z)
             ⊕ [(A0β)·σ ⊗ I3].              (5)

The enclosing represented algebra has dimension 1+1+4=6. The saved actual span also has dimension6, so

    E_row ≅ E_column ≅ C ⊕ C ⊕ (M2⊗I3),     (6)

as represented algebras, not merely as vector spaces with equal dimension.

An explicit matrix-corner certificate avoids relying on an abstract encoding. Put

    B_a=Σ_j (A0^(-1))_{j a} Π_c H_j.

They obey B_a†=B_a and B_a B_b=δ_ab Π_c+i ε_abc B_c. The four matrix units are

    M00=(Π_c+B_z)/2, M11=(Π_c−B_z)/2,
    M01=(B_x+iB_y)/2, M10=(B_x−iB_y)/2.

They belong to the saved six-dimensional span, obey Mij Mkl=δ_jk Mil and have rank-three diagonal units. Choose a deterministic orthonormal basis v1,v2,v3 of ran M00 and set J|0,k>=vk, J|1,k>=B_x vk. Then J†J=I6, JJ†=Π_c and J(X⊗I3)J† is this M2 corner.

The even space is span{Π_0,Π_c}; the odd space is spanned by Π_0(XII+YII+ZII) and B_x,B_y,B_z. The recorded ranks 2/4/6 certify that these are whole graded spaces. Every spectrum is symmetric about zero by (5), so ℓ=0 and all successful dagger branches have constant amplitudes. Their linear restriction to the corner must be

    L_mu(J(X⊗I3)J†)=c_mu J(A2(X)⊗I3)J†,
    A2(X)=Tr(X)I2−X.                         (7)

## 6. A physical upper-bound reduction, not parent-bound inheritance

Let E,K_mu be any putative one-query physical B55 row/column inverse protocol. Define contractions

    E'=(J†⊗I_M) E J,
    K'_mu=J† K_mu (J⊗I_M).

They obey E'†E'≤I and Σ K'_mu†K'_mu≤I. Inserting a single arbitrary forward V∈SU(2) on the logical qubit gives, by (7),

    K'_mu (V⊗I3⊗I_M) E'=c_mu (V†⊗I3).      (8)

Complete E' by a heralded reject outcome. Reject outcomes still pass a dummy wire through the same unconditional V call and never count as successful. Complete the postinstrument similarly. Do not renormalize the accepted branch. Equation (8) has exactly the original c_mu, hence the same total p. The qutrit multiplicity remains coherent and can be retained; preparing any known spectator gives a legitimate universal qubit inverse protocol.

This is a loss-heralded upper-bound simulator, not a claim that the full correlated 8×8 oracle can be freely synthesized from V. The original constructions below remain valid on all four centres, including superpositions across Π_0 and Π_c. The controlled projection in the bound is justified by the contraction completion and unchanged unnormalized success operator, not by silently dropping a centre.

For V∈SU(2), V†=A2(V)=Y V^T Y, and SU(2) spans M2. The received T2 (i,b,a,o) adjugate certificate gives the known p≤1/4. Explicitly, for the adjugate coefficient vector t, Q=Tr_o|t><t| satisfies Q²=dQ, Tr_a Q=I_ib, Tr Q²=d³. A deterministic completion satisfies Cdet≥p|t><t| and Tr_o Cdet=C1⊗I_a with Tr_b C1=I_i. Therefore

    d=Tr[(C1⊗I_a)Q] ≥ p Tr Q²=p d³,

so p≤1/d²=1/4 at d=2. This is the established bound, newly licensed here by (7)–(8), not a new universal bound.

## 7. Matching physical constructions and the uniform improvement

Let X1=XII, Y1=YII, Z1=ZII. Every B55 sector has a traceless qubit Hamiltonian. The coherent LCU identity on the original eight-dimensional oracle is

    (−U+X1 U X1+Y1 U Y1+Z1 U Z1)/4=U†/2.   (9)

Prepare a four-state/two-qubit ancilla uniformly; apply a known controlled Pauli before and after the single unconditional U; put the minus sign on the identity branch; unprepare and herald the uniform outcome. This realizes p=1/4 on every physical input and reference, including all centre coherences. It is an inherited construction written directly for this grid, not a minimum-ancilla claim.

For all nine physical generators P,

    Q0=YIX,        Q0 P Q0=−P*,
    Q0 U Q0=U*,    Q0 U† Q0=U^T.              (10)

Hence star has probability one, and dagger/transpose have equal optima via known pre/post sandwiches. Equations (8)–(10) give

    B55 row and column: p_dagger^opt=p_T^opt=1/4,
                         p_star^opt=1.        (11)

For uniform tying H(t)=t H0, H0=sum of the nine displayed Paulis. Exact factorization gives

    χ_H0(x)=(x²−27)(x²−3)^3.

Thus ±3√3 have multiplicity1 and ±√3 multiplicity3. The known paired-eigenspace mechanism applies, with multiplicities checked, not inferred from a square-free polynomial. More directly,

    W=(XII−YIY)/√2,
    W†=W, W²=I, {W,H0}=0.

Therefore on the original physical oracle

    W U(t) W=U(t)†,
    Q0 W U(t) W Q0=U(t)^T,
    Q0 U(t) Q0=U(t)*.                        (12)

All three transformations are deterministic, use one query, and need no ancilla in this construction. Probability one is the matching universal probability upper bound. The tied promise really improves dagger and transpose from 1/4 to1; no gate-minimum or hardware-routing claim follows. W does NOT anticommute with the row/column generators separately: that is a required negative control.

For any fixed known Hermitian H0, irrespective of reflection, one-parameter transpose is deterministic: if H0=C D C† with D real diagonal, V0=C* C† obeys V0 U(t)V0†=U(t)^T. Thus the other three uniform families have p_T^opt=1, while their dagger/star optima remain zero by T4. The matched-q4 partial row/column families also inherit deterministic transpose from their special ten-dimensional parent. The saturated-q4 and B4 row/column transpose optima are not settled here; no new scan is authorized.

## 8. What was actually checked in Pro, and what should happen next

The added Pro calculation used literal SymPy 2×2 Pauli matrices and the saved B55 coefficient files. It checked exactly: W²=I and {W,H0}=0; all nine Q0 generator identities; the characteristic polynomial; projector ranks2 and6; all nine B_a B_b identities for each of row/column; membership of all four corner units in each saved span; all16 matrix-unit multiplication identities per family; and failure of the overgeneralized W at the first row/column generator. A separate exploratory script checked all36 products of each six-dimensional basis and the sector matrices/Gram matrices/orientations. These are Pro local checks, not a second independent Codex certificate or physical hardware tests. A further literal 4×4 phase-control check confirms BB†=diag(1/3,1,1,1), κ²=10/3, the pre-isometry, and all16 matrix-unit compositions for the p=3/40 construction; its JSON is also retained.

One Pro helper initially used structural SymPy equality for matrix-unit products and reported false negatives. The coefficient/Pauli identities remained exact. Changing only the comparison to expanded-entry zero tests made all32 corner products pass. The initial output/source and corrected output/source are both retained. This is not a rerun of, or defect in, the decided T4 calculation.

The appropriate next increment is a small exact independent certificate of the new representation and heralded-corner interface, plus the explicit phase control for theorem (3). No optimizer, new grid family, random census, or new ray scan is scientifically needed. Claim status after a successful independent run should be analytic-checked for the all-parameter theorems, exact-finite for the finite representation identities, and explicitly known-work attribution for the universal bound and spectral-pair mechanism. Failure must identify a concrete algebraic or physical-normalization premise rather than trigger an unregistered search.
