# Optimal quartic-harmonic chi-square certificate for the frozen N=42 candidate

Date: 2026-11-28. Run 68. Base: `main` after Run 67.

## Scope

This note sharpens the Run 67 all-orbit Gram certificate. The Run 67 inequality was valid, but its chosen orbit coefficient vector was not the optimal fourth-order Cauchy--Schwarz witness. The balanced-slice Gram kernel has an exact scalar action on the fourth harmonic subspace, so the optimal degree-four bound can be computed without constructing or pseudoinverting a 1,440 by 1,440 matrix.

The result remains candidate-specific: it rejects the frozen 37-base / 74-labelled period-two ensemble more quantitatively. It is not a global separator for all period-two measures or for the continuous 42-cycle exponential family.

## 1. Balanced-slice characters and residual vector

Let
[
Omega_{42}={xin{-1,1}^{42}:sum_i x_i=0}
]
with uniform law (u). For each four-subset (I), put
[
f_I(x)=prod_{iin I}x_i,
qquad
delta_I=mathbb E_q f_I-mathbb E_u f_I,
]
where (q) is the frozen candidate's complement-folded program-label distribution.

The projection-DPP/minor identity gives
[
mathbb E_q f_I=ar m_I,
qquad
mathbb E_u f_I=rac1{533}
quad (|I|=4).
]
The candidate is (D_{42})-invariant, so (delta_I) is constant on each of the 1,440 dihedral orbits (mathcal O); write this value as (delta_{mathcal O}).

The existing 256-bit Arb reconstruction certifies all 861 pair coordinates:
[
mathbb E_q x_i x_j=mathbb E_u x_i x_j=-rac1{41}
quad	ext{for every }i
e j.
]
Hence every second-order residual is exactly zero.

## 2. The fourth-to-third down relation

On coefficient vectors indexed by four-subsets, define
[
(D_4 a)_J=sum_{i
otin J}a_{Jcup{i}},
qquad |J|=3.
]
For every balanced sign vector,
[
egin{aligned}
sum_{i
otin J}f_{Jcup{i}}(x)
&=f_J(x)sum_{i
otin J}x_i\
&=-f_J(x)sum_{jin J}x_j\
&=-sum_{jin J}f_{Jsetminus{j}}(x).
end{aligned}
]
Taking the difference of expectations under (q) and (u), and using the exact pair match, gives
[
oxed{D_4delta=0.} 	ag{1}
]
This is the key structural fact missed by the arbitrary coefficient choice in Run 67.

## 3. Exact action of the quartic Gram kernel on (ker D_4)

Define the full quartet Gram matrix
[
K_{I,J}=mathbb E_u[f_I f_J]
=mu_{8-2|Icap J|},
]
where (mu_{2r}=mathbb E_uprod_{iin A}x_i) for any (2r)-set (A). The balanced-slice recurrence gives
[
(mu_0,mu_2,mu_4,mu_6,mu_8)
=left(
1,-rac1{41},rac1{533},
-rac{15}{41cdot39cdot37},
rac{105}{41cdot39cdot37cdot35}
ight).
]

**Lemma.** For every coefficient vector (ainker D_4),
[
oxed{Ka=lambda_4 a,qquad
lambda_4=sum_{r=0}^4(-1)^rinom4rmu_{2r}
=rac{21888}{19721}.} 	ag{2}
]

**Proof.** Write (F(s)=mu_{8-2s}) for (s=0,ldots,4), and expand it in the binomial basis:
[
F(s)=sum_{t=0}^4 c_tinom{s}{t}.
]
For fixed (I),
[
(Ka)_I
=sum_{t=0}^4c_t
sum_{substack{Tsubseteq I\|T|=t}}
sum_{substack{Jsupseteq T\|J|=4}}a_J.
]
If (|T|=3), the inner sum is ((D_4a)_T=0). If (|T|<3), sum these zero relations over all triples containing (T); each four-set containing (T) is counted the same positive number of times, so the inner sum again vanishes. Only (t=4), (T=I), survives. Its coefficient is the fourth finite difference
[
c_4=sum_{s=0}^4(-1)^{4-s}inom4smu_{8-2s}
=sum_{r=0}^4(-1)^rinom4rmu_{2r}.
]
Substitution of the five exact moments gives (21888/19721). (square)

The proof is a direct finite-difference calculation; no numerical eigensolver, representation-theory black box, matrix inverse, or pseudoinverse is used.

## 4. Optimality among all fourth-order character witnesses

For any coefficient vector (a), the chi-square Cauchy--Schwarz inequality gives
[
chi^2(qVert u)ge
rac{(a^mathsf Tdelta)^2}{a^mathsf TKa}
]
whenever the denominator is positive.

Let (H=ker D_4). By (1), (deltain H). By (2), (K) acts as (lambda_4 I) on (H). Since (K) is symmetric positive semidefinite, (H^perp) is invariant and contributes a nonnegative denominator. For (a=a_H+a_perp),
[
a^mathsf Tdelta=a_H^mathsf Tdelta,
qquad
a^mathsf TKagelambda_4|a_H|_2^2.
]
Cauchy--Schwarz in coefficient space therefore gives
[
rac{(a^mathsf Tdelta)^2}{a^mathsf TKa}
lerac{|delta|_2^2}{lambda_4}.
]
Equality is attained by (a=delta). Thus
[
oxed{
sup_{a:,a^mathsf TKa>0}
rac{(a^mathsf Tdelta)^2}{a^mathsf TKa}
=
rac{|delta|_2^2}{lambda_4}.
} 	ag{3}
]
This is the exact optimal Cauchy--Schwarz lower bound obtainable from the complete fourth-order character vector. It is not the full chi-square unless all higher harmonic discrepancies vanish.

Because the residual is constant on each (D_{42})-orbit,
[
|delta|_2^2
=sum_{|I|=4}delta_I^2
=sum_{mathcal O}|mathcal O|,delta_{mathcal O}^2.
]
Consequently the optimal quartic-only certificate is
[
oxed{
chi^2(qVert u)ge
rac{19721}{21888}
sum_{mathcal O}|mathcal O|,delta_{mathcal O}^2.
} 	ag{4}
]

## 5. Certified N=42 value

The verifier independently reruns the 861-pair Arb audit and all 1,440 quartic-orbit Arb residuals. It also checks all (inom{42}{3}=11,480) down relations in interval arithmetic.

The frozen residual intervals give
[
sum_{mathcal O}|mathcal O|,delta_{mathcal O}^2
approx 0.09140488998805886,
]
and therefore
[
oxed{
chi^2(qVert u)>0.0823
}
]
(the full 256-bit interval is recorded in the machine certificate).

The Run 67 arbitrary-coefficient Gram witness gave
[
chi^2(qVert u)>0.07330753790177964068.
]
The new result is the **optimal fourth-order character bound** and improves that certified bound by more than 12%.

By the exact complement-folded Plucker frame-potential identity,
[
operatorname{FP}=rac4{inom{42}{21}}
left(1+chi^2(qVert u)ight),
]
so the new machine certificate also gives the corresponding stronger candidate-specific frame-potential lower bound.

The direct bounded-character TV certificate remains
[
operatorname{TV}(q,u)>0.00275.
]
The improved chi-square bound is not claimed to improve that TV bound and does not imply a Choi trace-distance or channel diamond-distance bound.

## 6. Reproduction

From the repository root:
```bash
python -m pip install python-flint==0.9.0
python verify_n42_optimal_quartic_chi_square.py
```

The verifier:
1. reruns the exact-real positive-weight reconstruction and all 861 pair-minor checks;
2. reruns the complete 1,440-orbit / 111,930-quartet 256-bit Arb audit;
3. checks all 11,480 fourth-to-third down relations;
4. computes (lambda_4=21888/19721) exactly;
5. sums the orbit-weighted residual squares with Arb;
6. certifies the optimal quartic chi-square and Plucker frame-potential lower bounds.

The workflow pins `python-flint==0.9.0` and freezes the resulting JSON certificate.

## 7. Interpretation and next step

The Run 67 all-orbit Gram bound was mathematically valid but not optimal because its orbit coefficients did not account for orbit multiplicities and the exact lower-degree null constraints. Equation (4) removes that inefficiency analytically.

This still rejects only the frozen 37-base / 74-labelled candidate. It does not exclude a different period-two measure, a general non-period-two cycle-exponential ensemble, or the full continuous physical family. The next decisive target remains a general-cycle positive ensemble or a global separator valid for every real coupling vector.
