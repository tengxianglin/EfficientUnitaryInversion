# Physical dihedral reduction and a certified seven-site Pauli CP converse

The [five-site physical ensemble](THEORY_PHYSICAL_PROGRAM_DESIGN_CONVERSE.md) establishes a target-component converse without assuming every balanced program-basis Pauli is a legal oracle. We now prove a symmetry reduction valid for every odd ring, and use it to certify the analogous converse at seven sites.

## 1. Scope and result

Keep the existing encoder, ideal-flag protected-program treatment and unchanged orthogonal split flag. On complementary program label \(R\), apply \(R^\dagger\) followed by a logical Pauli drawn from arbitrary probabilities \(q_R(T)\). They may be non-radial, but cannot depend on the unknown Hamiltonian. Define, in a selected parity sector,
\[
 \kappa_H(q)=\sup\{\kappa\ge0:
  J_{H,q}-\kappa|V_H\rangle\!\rangle\langle\!\langle V_H|\succeq0\},
 \qquad K_n=\sup_q\inf_{H\ {\rm physical}}\kappa_H(q),
\]
where \(J\) is the recovered complementary Choi matrix before its drift factor, \(V_H\) the intended inverse, and \(\|\operatorname{vec}V_H\|^2=D=2^{n-1}\).

**Computer-assisted theorem.** At seven sites,
\[
 \boxed{K_7=\frac{G_{\rm ML}}{D^4}
 =\frac{552503}{449839104},\qquad
 D=64,\quad G_{\rm ML}=\frac{8840048}{429}.}
\]
Radial ML attains the lower bound by the [cross-effect identity](THEORY_ODD_CYCLE_RADIAL_RECOVERY.md). The upper bound covers all stochastic Pauli correction tables, not just radial ones. Extra hypotheses outside the balanced program span have zero Bell overlap and do not invalidate the upper bound.

This is a **seven-site complementary-map theorem**, not a seven-site first-order-canceling six-query protocol. The admissible long-ring construction requires \(n\ge21\). We do not optimize the full diamond norm, arbitrary non-Pauli CPTP corrections, or coherent data-program recovery.

## 2. An exact physical symmetry reduction for all odd rings

In the selected sector, write the physical Majorana-cycle Hamiltonian as
\[
 H_+=\sum_{j=0}^{2n-1}c_j\,i\gamma_j\gamma_{j+1},
 \qquad j+1\pmod {2n}.
\]
The alternating bilinears are local fields and Ising edges. The wrap edge has a fixed parity-dependent sign absorbed into its coupling. Thus every real vector \(c\) has a legal original-Hamiltonian extension. The code checks each basis bilinear is exactly a signed allowed field or edge.

Consider a dihedral permutation \(\pi(j)=s+\sigma j\pmod {2n}\), with \(\sigma=\pm1\). Choose Majorana signs \(\varepsilon_j\) so that the signed permutation has determinant +1; explicitly all signs can be +1 except \(\varepsilon_0=\operatorname{sgn}\pi\). It has a Spin lift preserving the selected parity block. The underlying Gaussian-unitary implementation of arbitrary SO(2n) rotations is standard; see Bravyi, *Lagrangian representation for fermionic linear optics*, Quantum Inf. Comput. 5, 216–238 (2005), [primary paper, Eq. (5)](https://arxiv.org/html/quant-ph/0404180v2). The restriction to signed cycle automorphisms here ensures that the physical nearest-neighbour promise is preserved. Under
\(\gamma_j\mapsto\varepsilon_j\gamma_{\pi(j)}\), each cycle bilinear maps to a signed cycle bilinear. Therefore the transformed Hamiltonian is still physical. The induced coupling map is
\[
 c'_{e(j)}=\sigma\varepsilon_j\varepsilon_{j+1}c_j,
 \quad e(j)=\begin{cases}\pi(j),&\sigma=+1,\\\pi(j+1),&\sigma=-1.\end{cases}
\]
A Pauli label \(T\), represented by an even Majorana subset modulo full complementation, maps to \(\pi(T)\), up to an irrelevant phase. Balanced labels stay balanced: graph automorphisms preserve or exchange the two bipartitions. Consequently the program masses \(|v_T|^2\) are permuted exactly.

Let \(\mathcal O_1,\ldots,\mathcal O_m\) be the dihedral orbits in the balanced label set \(\mathcal S\), and define seed orbit masses
\[
 M_i(H)=\sum_{T\in\mathcal O_i}
           |\operatorname{Tr}(T^\dagger e^{iH_+})/D|^2.
\]
A uniform average over the \(4n\) group elements has per-label mass \(M_i(H)/|\mathcal O_i|\). Hence seed probabilities \(p_j\) yield an exactly uniform physical program-mass ensemble if and only if
\[
 \sum_jp_jM_i(H_j)=\frac{|\mathcal O_i|}{|\mathcal S|}
             \quad\text{for every orbit }i.
\]
This reduction is exact. It uses a known family of legal oracle Hamiltonians for a converse, not additional gates or queries in the recovery protocol. It imposes no uniform off-diagonal program moments.

Exact orbit counts are:

| n | balanced labels | dihedral orbits |
|---|---:|---:|
| 3 | 10 | 3 |
| 5 | 126 | 13 |
| 7 | 1716 | 85 |

The reduction saves a group-size factor; it is not a polynomial-size general construction. The number of labels and orbits still grows exponentially.

## 3. Certified seven-site ensemble

The frozen data specifies 85 seed orbits:

- 33 matching-generated Pauli seed orbits;
- 52 seed Hamiltonians with 14 explicit rational Majorana-cycle couplings.

Each rational coupling vector is interpreted by the displayed selected-sector Hamiltonian and has a legal local-field/Ising-edge extension. A seed is averaged over all 28 dihedral images. The full physical ensemble therefore has at most 2380 atoms, counting multiplicity; distinctness is neither needed nor claimed.

Let the exact real orbit-mass matrix be \(A_{ij}=M_i(H_j)\), and let \(b_i=|\mathcal O_i|/1716\). Define the exact weights by \(p=A^{-1}b\). The weights need not be rational. The numerical discovery weights are not used in verification.

At 192-bit ball precision, the verifier encloses all rational-input matrix exponentials, sparse Pauli coefficient sums, orbit masses, determinant and linear-system solution. It certifies
\[
 \det A=9.360913548825585072193198876728410741604962292148\times10^{-33}
            \ \pm\ 8.88\times10^{-82},
\]
which excludes zero, and
\[
 p_{\min}=4.9390458004836023982587337994771222614559364663615\times10^{-5}
            \ \pm\ 7.06\times10^{-55}>1/25000.
\]
The exact matrix is therefore invertible and its exact solution strictly positive. Every orbit-mass column sums to one by the balanced program-span theorem and unitarity. Summing the exact equations gives \(\sum_jp_j=\sum_ib_i=1\). After the physical group averages, each of the 1716 balanced labels has exact mean mass \(1/1716\). This is an existence proof with certified exact weights, not an approximately flat sampled ensemble.

The [ensemble converse](THEORY_PHYSICAL_PROGRAM_DESIGN_CONVERSE.md#2-a-general-ensemble-converse) now gives, for any table \(q\),
\[
 \inf_H\kappa_H(q)
 \le \frac1{D^4|\mathcal S|}
      \sum_{R\notin\mathcal S}\max_{T\in\mathcal S}a_{|RT|/2}^2
 =\frac{G_{\rm ML}}{D^4}.
\]
The exact row-max sum is 35360192, and \(35360192/1716=8840048/429\). Radial ML supplies equality, proving the theorem.

## 4. Reproducibility and evidence status

**Subsequent result:** the [joint-parity diamond converse](THEORY_JOINT_PARITY_DIAMOND_CONVERSE.md) uses modified, exactly gapped seed designs to make the same ensemble uniform in both physical parity sectors. A Bell-input pinching argument then upgrades the restricted result to full diamond minimax error for valid split probabilities at five and seven sites. The admissible long-ring theorem still requires a joint ensemble construction.

Files:

- [ising_cycle_program_orbits.py](ising_cycle_program_orbits.py): sparse Pauli representation, physical cycle bilinears, signed dihedral coupling maps, floating and ball orbit masses;
- [verify_ising_orbit_program_design.py](verify_ising_orbit_program_design.py): independent verification of the frozen exact certificate;
- [evidence/physical_orbit_program_design_n7.json](evidence/physical_orbit_program_design_n7.json): rational seeds and proof parameters.

Run:

1. `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python ising_cycle_program_orbits.py`
2. `OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 python verify_ising_orbit_program_design.py`

Dependencies: NumPy 2.3.5, SciPy 1.17.0 and python-flint 0.9.0. No optimizer is required. The exact proof uses the analytic symmetry action and certified invertibility/positivity; numerical group-action tests are additional checks.

The sparse Pauli matrices agree exactly with the earlier independent dense Majorana construction at n=3,5. Every physical dihedral image at those sizes is also checked on a seeded noncommuting Hamiltonian, with mass tolerance \(2\times10^{-12}\). Physical bilinears are checked as signed allowed qubit terms. The seven-site verifier reconstructs all 85 ball columns and solves the complete reduced system.

Discovery used 400 seeded random physical Hamiltonians followed by separating-direction searches. Initial sample infeasibility was treated only as failure of the finite pool. Analytic gradients were checked against finite differences. Subsequent floating feasibility selected seeds; all coefficients were then fixed to rationals and the resulting exact system was re-certified. Optimizer status flags and the discovery weights are not proof inputs.

The [EUI manuscript and robustness appendix](https://arxiv.org/html/2506.20570v1) provide the physical setting. This theorem addresses the narrower program-recovery CP figure. No literature-wide originality or publication-readiness conclusion is asserted.

The remaining blocker is an analytic construction for general odd rings, especially the admissible \(n\ge21\) regime. The five- and seven-site certificates provide evidence and a reusable symmetry reduction, not an induction theorem. A useful next step is to identify a parameterized family of physical seed Hamiltonians whose orbit-mass vectors admit a provably positive decomposition, or find a separating obstruction. Further sample growth alone cannot establish the all-length result.
