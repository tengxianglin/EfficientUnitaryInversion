# Independent one-query audit (T2)

Scope: finite-dimensional, exact, one forward query to the original physical
unitary, parameter-independent preprocessing/postprocessing, arbitrary finite
memory, and finitely many successful Kraus operators. Parameters are all of
R^9 independently, including zero and every complete ray. Success means equality
of CP maps on every input and reference system. The matrix representative of each
target is fixed as U^T, U*, or U†, so its value at I is I. Probability may initially
depend on parameters and may be zero. These hypotheses are essential.

Verdicts: the amplitude rigidity, derivative/span identity, coherent logical
simulation, SU(2) restriction, and comb bounds below are **analytic-checked**.
The three independently indexed integer certificates and the specified spectral
controls are **exact-finite**. The physical saturation premise for a non-special
proper grid is supplied by the independent T1 cubic-law audit, not inferred from
these comb computations. T2 finds no failed quantifier or counterexample. There
is no claim of a new universal-transpose bound, minimum ancilla count, minimum
known-gate count, or extension to coefficient-tied families.

## 1. Rank-one Choi condition and phase-aware amplitude rigidity

Purify preprocessing into an isometry E from external input i to oracle input b
and memory e. Write the postprocessing/instrument Kraus operators K_mu from a,e
to output o. A successful branch is

    L_mu(U)_{oi} = sum_{a,b,e} (K_mu)_{oae} U_{ab} E_{bei}.

Consequently L_mu is a fixed complex-linear function of the matrix U; equivalently
it is a finite sum A U B. Include all unobserved environments in mu. Every exact
successful CP map has Choi matrix

    sum_mu |L_mu(U)><L_mu(U)| = p(U) |F(U)><F(U)|.

Positivity of each summand implies that every vector on the left lies in the
one-dimensional range on the right. This is also true at p=0, where all vectors
are zero. Thus L_mu(U(alpha))=a_mu(alpha) F(U(alpha)) for each mu separately.
No common branch phase, positive probability, or constant coefficient has been
assumed. The amplitude is uniquely defined because F(U) is a nonzero matrix.

Fix any beta in R^9. Let H=H(beta)=sum_{lambda in S} lambda P_lambda, where S is
the finite nonempty set of distinct eigenvalues and each P_lambda has positive
rank m_lambda. Along alpha=t beta,

    L_mu(e^{-itH}) = sum_{nu in S} e^{-it nu} L_mu(P_nu).

For transpose use R_lambda=P_lambda^T; for conjugation use R_lambda=P_lambda*;
for inverse use R_lambda=P_lambda. All are orthogonal Hermitian projectors of
rank m_lambda. Normalized trace extraction gives

    transpose:  a_mu(t) e^{-it lambda}
                = Tr[R_lambda L_mu(e^{-itH})]/m_lambda;
    inverse/*:  a_mu(t) e^{+it lambda}
                = Tr[R_lambda L_mu(e^{-itH})]/m_lambda.

For every lambda the right side is a finite exponential polynomial with
frequencies contained in S. Therefore a_mu itself is a finite exponential
polynomial, with support contained in

    Gamma_T = intersection_lambda (S-lambda),
    Gamma_- = intersection_lambda (S+lambda),

respectively. Finite exponentials with distinct real frequencies are linearly
independent on the full real axis (differentiate at zero and use the nonsingular
Vandermonde matrix). Taking one trace extraction already supplies a finite
frequency expansion; uniqueness makes its nonzero support obey every other
extraction. This avoids any assumption about regularity of a_mu or cancellation
between branches. Eigenvalue degeneracy is harmless because m_lambda>0 is
explicitly divided out. The singleton spectrum H=0 is included.

For Gamma_T, gamma+min S and gamma+max S must belong to S, so gamma>=0 and
gamma<=0. Since zero always belongs, Gamma_T={0}. For Gamma_-, membership says
gamma-S is a subset of S; equal finite cardinalities make it equality. Necessarily
gamma=min S+max S, so Gamma_- is either empty or one point. Hence

    T:       a_mu(t beta)=c_mu(beta);
    inverse/*: either a_mu(t beta)=0 for all t,
               or a_mu(t beta)=c_mu(beta) exp(-it gamma_beta).

At t=0 every ray represents the same I and the same F(I)=I. Thus every c_mu(beta)
equals the single scalar a_mu(0). In particular a_mu(0)=0 forces that branch to
vanish on **every** ray, even if its value was first shown to vanish on one ray.
Multiple Kraus branches cannot evade this: the rank-one condition and frequency
argument apply to each branch individually, and p=sum_mu |a_mu|^2.

For transpose all amplitudes on all R^9 equal c_mu=a_mu(0), so p=sum_mu|c_mu|^2
is constant. For inverse/*, the existence of one beta with empty Gamma_- forces
all branches to vanish on the entire family. A branch cannot have zero success
at I and regain success elsewhere. If every ray is symmetric, phase functions
may remain; their existence alone does not construct a CP instrument.

Exact controls retained by the code:

| S | Gamma_T | Gamma_- | allowed inverse/* branch phase |
|---|---|---|---|
| {-3,1} | {0} | {-2} | exp(2it) |
| {-15,-3,9} | {0} | {-6} | exp(6it) |
| {-5,-3,1,7} | {0} | empty | identically zero |
| {0} | {0} | {0} | constant |
| {-2,2} | {0} | {0} | constant |
| {-1,3} | {0} | {2} | exp(-2it) |

The first two are necessary-condition positive controls, not reconstructed
encoders. Multiplicities do not enter S. For example three copies of eigenvalue
1 and one copy of -3 have exactly the first row's conclusion.

For a commuting grid line with distinct independent A,D and third member ±AD,
independent coefficients allow H=A+2D+4AD after absorbing the known sign. Joint
eigenspaces of A,D for all (s,t) in {±1}^2 are nonzero: their projector is
(I+sA)(I+tD)/4 and has trace N/4, since A,D,AD are distinct nonidentity Paulis.
The distinct spectrum is {7,-5,-3,1}. Its candidate reflection center sum is 2,
but 2-(-3)=5 is absent. The third control therefore proves the global zero claim
for inverse/* whenever a commuting line belongs to the independent family.

## 2. True span from mixed derivatives

Let V=span_C{exp(-i sum_j alpha_j P_j): alpha in R^9}, and let C_k be the matrix
coefficient of alpha^k in H(alpha)^n, where |k|=n. The C_k here are **coefficient
matrices**, not their individual coordinate supports. Since V is a subspace of
a finite-dimensional matrix space it is closed. Every mixed derivative at zero
is a limit of finite linear combinations of U(alpha), hence belongs to V.
Homogeneity ensures that only the nth exponential term survives that derivative:

    partial^k U(0) = (-i)^n (k!/n!) C_k.

Thus every C_k belongs to V. Conversely, every H(alpha)^n is a linear combination
of these coefficient matrices; the convergent exponential series then places
every U(alpha) in their closed span. Including n=0 gives I, proving exactly

    V = span_C{C_k: n>=0, |k|=n}.

For nine independent Pauli coefficients each ordered word contributing to a
given monomial k has the same binary sum v=sum_j k_j g_j. Its product is a phase
times the same Pauli P_v. Consequently C_k=c_k P_v, possibly with c_k=0 after
cancellation. Distinct v give linearly independent Paulis. Therefore, and only
under this single-coordinate property, V equals the Pauli coordinate envelope
of the **nonzero** monomial coefficients. Bound variables destroy that property;
union support can then exceed actual span.

The proper-grid cubic theorem, audited independently by T1, supplies the finite
stopping result: when B differs from the geometric polar J, coefficients through
degree three contain all 16 labels of W, so V=A=span{P_v:v in W}. There is no
assumption that products of already present labels automatically enter V.
When B=J, define tau(P_v)=(-1)^Delta(v)P_v. The identity
Delta(v+w)=Delta(v)+Delta(w)+B(v,w) makes tau a complex-linear
anti-automorphism. It fixes every grid generator and therefore every H^n, so only
the ten labels {0} union G occur. I and the nine independent first derivatives
already span these ten coordinates. This exceptional V is not the full algebra;
the general logical reduction is not applied to it. Its explicit deterministic
transpose construction and the trivial probability upper bound one settle it.

## 3. Coherent logical simulation and target-aware decoding

Assume saturation V=A and the physical system is N=8. Write r=rank B,
d=2^{r/2}, z=2^{4-r}, m=2^{3-4+r/2}, and k=z m=8/d. A fixed, known unitary
encoding C identifies H_L tensor H_Z tensor H_M with the physical space, such
that

    A = C[(direct sum_{z sectors} M_d) tensor I_m]C†.

Here r=2 means d=2,z=4,m=1; r=4 means d=4,z=1,m=2. C is independent of every
unknown parameter. Standard finite-dimensional *-algebra block decomposition
gives such a C; T3 separately constructs actual encodings. No efficiency or
Clifford-only claim is needed for this upper-bound reduction.

From section 1 each physical success branch has L_mu(U(alpha))=c_mu U(alpha)^T.
Section 2 and complex linearity imply L_mu(X)=c_mu X^T for **every** X in A. The
same underlying physical circuit remains a valid instrument for all physical
unitary inputs, including those not in the original exponential promise.

For any arbitrary logical V in U(d), define

    W(V) = C(V tensor I_Z tensor I_M)C† in A.

Every call to W(V) can be simulated with exactly one forward call to the given
logical V: apply C†, call V on L while leaving Z,M alone, apply C. This is an
ordinary unconditional V call; it needs neither controlled-V nor any target
oracle. All four rank-two centers receive the same V coherently. No sector is
measured, selected as a classical case, or discarded during the oracle use.

In the fixed computational bases,

    W(V)^T = C* (V^T tensor I_Z tensor I_M) C^T.

Use C* as the input encoding and C^T as the output decoding. The successful
operator of the induced instrument on the full logical-plus-label space is

    C^T L_mu(W(V)) C* = c_mu (V^T tensor I_Z tensor I_M),

because C^T C*=I. This identity holds on all entangled states with references,
including sum_s |psi_s>_L |s>_Z with arbitrary inter-sector coherence. It also
automatically accounts for a transpose that permutes physical center projectors:
the input encoding uses the conjugate basis, not the original C basis.

For a pure logical-only interface choose any normalized known |eta> in Z,M,
including a coherent superposition of all four centers. Let J_eta psi=psi tensor
eta. The explicit physical input isometry and success decoder are

    E_in = C* J_eta,       D_out = J_eta† C^T.

Then D_out L_mu(W(V)) E_in=c_mu V^T. D_out is implemented by C^T followed by
postselection onto eta; on every original successful output this extra selection
succeeds with probability one. Thus the probability is exactly p=sum|c_mu|^2.
Equivalently keep Z,M and obtain V^T tensor I, avoiding an extra outcome label.

This reduces any proposed physical p to a legitimate one-query universal logical
transpose p. It does not claim a free compressed oracle for the original task:
the reduction starts with a logical oracle and explicitly simulates the larger
physical oracle. The converse construction still uses the original 8x8 forward U.

## 4. Inverse upper bound from an anticommuting line, not U(8)

Choose an anticommuting Pauli line A,D,±iAD of an all-anticommuting grid. Its three
independent coefficients allow precisely all H=xA+y(iAD)+zD, with a known sign
absorbed into y. There is a fixed unitary C_line with

    A=C_line(X tensor I_4)C_line†,
    D=C_line(Z tensor I_4)C_line†,
    iAD=C_line(Y tensor I_4)C_line†.

For completeness, choose an orthonormal basis e_j of D's +1 eigenspace, and set
the corresponding -1 basis to A e_j. Anticommutation ensures this is a paired
orthonormal basis and A exchanges the two halves. Both eigenspaces have dimension
four because D is a nonidentity Pauli. This constructs C_line and the displayed
sign convention iXZ=Y. The subfamily is

    W_line(V)=C_line(V tensor I_4)C_line†, V in SU(2),

since every SU(2) unitary is exp[-i(xX+yY+zZ)]. Every nonzero ray has distinct
spectrum {-rho,rho}; hence Gamma_-={0}. Including the origin, every successful
inverse branch on this subfamily has the same scalar c_mu, and the probability
there is constant.

Simulate each W_line(V) call by C_line†, one call to V, C_line. Use input
C_line J_eta and output J_eta† C_line†. This yields c_mu V† on every SU(2) V with
exactly one forward V query. The chosen spectator state eta can again be retained
instead of measured. This argument restricts the promise; it never invokes a
universal U(8) inverse impossibility theorem.

For every 2x2 matrix X define A2(X)=Tr(X)I-X. This is complex-linear. Cayley-Hamilton
gives V†=V^{-1}=A2(V) for V in SU(2), whose determinant is one. SU(2) spans M2(C):
the four members I,-iX,-iY,-iZ form a complex basis. Therefore each induced
successful linear map equals c_mu A2 on all M2(C). Its coefficient comb is
exactly p|t_A2><t_A2|, so the d=2 adjugate bound in section 5 applies and gives
p<=1/4. This also bounds worst-case success of the full all-anticommuting family.
For that entire family every block Hamiltonian is traceless and all distinct
spectra are symmetric, so section 1 additionally makes p constant throughout.
The given LCU inverse construction attains 1/4. This audit verifies the upper
bound; full physical circuit execution belongs to T3.

The matrix identity behind the adjugate certificate is, for every complex X,

    Y X^T Y = Tr(X)I-X,
    X=[[a,b],[c,d]]  =>  both sides [[d,-b],[-c,a]].

It is verified on all four matrix units using the real integer J=iY and
Y X^T Y=-J X^T J. No SU(2) assumption is needed for that identity itself.

## 5. One-query comb certificate in a different tensor order

All audit tensors use C-order axes (i,b,a,o): external input, oracle input,
oracle output, external output. Define t by

    L(U)_{oi}=sum_{a,b} t_{ibao} U_{ab},
    T=|t><t|, Q=Tr_o T on (i,b,a), M=d I_{iba}-Q.

For transpose t_{ibao}=delta_{ob}delta_{ai}. For adjugate2,
t_{ibao}=delta_{ab}delta_{oi}-delta_{oa}delta_{bi}. The implementation derives
these tensors independently by generating all matrix-unit images. It imports no
r1 functions. Source tensors in (o,a,b,i) are compared only afterward via axis
permutation (3,2,1,0).

For clarity, the causality normalization follows from the actual query circuit,
not a remembered reshuffle. With a purified preprocessing isometry E and all
postprocessing Kraus operators K_mu as in section 1, sum_mu K_mu†K_mu=I_{ae}.
The total coefficient matrix Cdet=sum_mu |t_mu><t_mu| therefore obeys

    Tr_o Cdet = C1_{ib} tensor I_a,
    (C1)_{ib,i'b'}=sum_e E_{bei} conjugate(E_{b'ei'}),
    Tr_b C1=I_i, C1>=0.

The first equality follows by summing o,mu and using
sum_{o,mu} K_{oae} conjugate(K_{oa'e'})=delta_{aa'}delta_{ee'};
the second trace follows from E†E=I. Include failed outcomes in Cdet, so Cdet is
positive and dominates the successful matrix Csucc. Conversely the standard
two-slot dilation can realize any such finite positive completion; the explicit
teleportation network below independently supplies achievability, so the bound
does not rely on asserting that converse.

After amplitude/span reduction, every success tensor is c_mu t and hence
Csucc=pT exactly. This step is what licenses the rank-one success comb. A
rank-one target on a sparse sample of oracle matrices alone would not license it.

The integer identities checked for each of (d=2,T), (d=4,T), (d=2,A2) are

    Q=Q^T, Q^2=dQ, Tr_a Q=I_{ib}, Tr(Q^2)=d^3,
    M=M^T, M^2=dM, ||t||^2=d^2.

Thus Q and M are positive semidefinite: real symmetric matrices satisfying
X^2=dX have eigenvalues only 0,d. T is an outer product. Partial trace preserves
the positive inequality Cdet>=pT; pairing with Q>=0 gives

    d = Tr(C1)
      = Tr[Q(C1 tensor I_a)]
      = Tr[Q Tr_o Cdet]
      >= p Tr(Q^2) = p d^3,

using Tr_a Q=I_{ib} and Tr_b C1=I_i. Therefore p<=1/d^2 for every finite memory
dimension and any number of successful branches. No SDP approximation is used.

An exact feasible completion is

    p=1/d^2, C1=I_{ib}/d,
    Cdet=(d T + M tensor I_o)/d^3.

Its difference from pT is (M tensor I_o)/d^3>=0. Its output trace is
(d Q+d M)/d^3=I_{iba}/d=C1 tensor I_a, and Tr_b C1=I_i. The audit stores the
integer numerators Q,M,D=dT+M tensor I_o and their rational denominators; there
are no floating eigenvalues. Integer magnitudes and dimensions remain far below
int64 overflow, with a conservative multiplication bound recorded for each case.

Achievability also has an independent network check. Prepare a normalized Bell
pair between query input b and memory r, and store input i in memory s. Its
isometry numerator is E0_{brsi}=delta_{br}delta_{si}, divided by sqrt(d).
Postselect a normalized Bell state on query output a and s; output r as o. Its
success numerator is K0_{oars}=delta_{or}delta_{as}, divided by sqrt(d). Contracting
over r,s gives t/d, the desired transpose success map. This uses one unconditional
forward U query. For d=2, apply J=iY before this network and -J afterwards, both
known unitaries, to obtain A2(U)/2. The scalar-index contraction is checked against
the coefficient tensor in all entries.

## 6. Exact checks and negative controls

`code/audit_comb_indices.py` was run under the shared serial T2 CPU/RAM runner.
Every matrix unit E_ab is generated and checked. All three input certificates
agree after the named-axis conversion. A second, scalar-loop partial trace
independently checks Q, Tr_a Q, and the completion trace without using np.trace.
The explicit Bell-network contraction independently checks t/d. All Q/M/D
integer matrices are retained as sparse JSON, with code/input/source hashes.

The mandatory wrong-order negative swaps oracle b and a but keeps interpreting
the tensor as (i,b,a,o). It fails the off-diagonal matrix-unit images and fails
Tr_a Q=I in every case. The first failing unit and both actual/expected matrices
are saved. An additional asymmetric dense tensor with coefficients
1000o+100a+10b+i checks the conversion itself. This is necessary because both
target tensors happen to be invariant under reversal of all four axes: merely
reinterpreting the old target-vector bytes in reverse order would accidentally
pass, despite not auditing the order conversion. The asymmetric control catches
12/16 such direct-reinterpretation entries.

The initial run and subsequent enhanced independent-check run are both retained
with distinct fresh output directories. The final run's `comb_index_audit.json`
is the complete raw certificate; runner status files supply actual CPU time,
timestamps, host, thread limit, and terminal state. Finite controls are not used
as a replacement for sections 1–5's all-parameter arguments.

## 7. Claim boundaries

* **analytic-checked:** phase-aware rigidity, including degeneracies, distinct
  branch phases, zero-at-I, multi-Kraus instruments, and shared origin.
* **analytic-checked:** mixed derivatives identify the true matrix span; its
  identification with coordinate support uses independent variables and Pauli
  products with a unique label per monomial.
* **analytic-checked conditional on saturation:** target-aware logical transpose
  simulation preserves all center-sector coherence and proves p<=2^{-rank B}.
  T1 supplies the independently checked saturation premise for the grid table.
* **analytic-checked:** the anticommuting SU(2) line yields the inverse p<=1/4
  bound using adjugate2, without a universal U(8) claim.
* **exact-finite:** integer certificates for d=2,4 transpose and d=2 adjugate,
  every matrix unit, scalar trace checks, network contraction, and six distinct
  spectral-set controls. The code rejects both deliberate order defects.
* **not_run:** optional SDP solver, larger-d SDP, and new physical circuit
  compilation. They are unnecessary for these exact upper bounds.

No T2 item needs `PRO_FOLLOWUP_REQUIRED` under the stated independent-parameter
contract. Coefficient-tied families, origin-excluding promises, approximate
targets, controlled-oracle contracts, and multiple forward queries need separate
arguments. The analysis and certificates do not establish minimum workspace or
known-gate complexity.
