from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction
from math import comb

N = 42
n = N // 2
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence/n42_period_two_single_atom_no_go.json'


def sign_vector(mask: int, length: int) -> tuple[int, ...]:
    return tuple(1 if (mask >> j) & 1 else -1 for j in range(length))


def cyclic_corr_f2(f: tuple[int, ...]) -> tuple[int, ...]:
    # First row of F^2 for the symmetric circulant matrix F_ij=f[j-i].
    return tuple(sum(f[k] * f[(d-k) % n] for k in range(n)) for d in range(n))


def cyclic_corr_ggt(g: tuple[int, ...]) -> tuple[int, ...]:
    # First row of G G^T for the circulant matrix G_ij=g[j-i].
    return tuple(sum(g[k] * g[(k-d) % n] for k in range(n)) for d in range(n))



def verify_correlation_conventions():
    # Check the cyclic-convolution formulas against direct integer matrix products.
    for mask in (0, 1, 0x155, (1 << (n//2)) - 1):
        f = [0] * n
        for d in range(1, n//2 + 1):
            sign = 1 if (mask >> (d-1)) & 1 else -1
            f[d] = sign
            f[n-d] = sign
        f = tuple(f)
        f2 = cyclic_corr_f2(f)
        F = [[f[(j-i) % n] for j in range(n)] for i in range(n)]
        for d in range(n):
            direct = sum(F[0][k] * F[k][d] for k in range(n))
            assert f2[d] == direct
    for mask in (0, 1, 0x55555, (1 << n) - 1):
        g = sign_vector(mask, n)
        gg = cyclic_corr_ggt(g)
        G = [[g[(j-i) % n] for j in range(n)] for i in range(n)]
        for d in range(n):
            direct = sum(G[0][k] * G[d][k] for k in range(n))
            assert gg[d] == direct


def phase_classification():
    counts = Counter()
    nonconstant_minus = []
    for mask in range(1 << n):
        g = sign_vector(mask, n)
        u = tuple(g[j] - g[(-j) % n] for j in range(n))
        v = tuple(g[(j+1) % n] - g[(1-j) % n] for j in range(n))
        uz = all(x == 0 for x in u)
        vz = all(x == 0 for x in v)
        if uz and vz:
            counts['both_zero'] += 1
        elif uz:
            counts['u_zero_only'] += 1
        elif vz:
            counts['v_zero_only'] += 1
        else:
            # With u_j,v_j in {-2,0,2}, a nonzero proportional pair
            # has ratio exactly +/-1. Check the full vector identity.
            if all(u[j] == -v[j] for j in range(n)):
                counts['ratio_minus_one'] += 1
                if not (all(x == g[0] for x in g)):
                    nonconstant_minus.append((mask, g, cyclic_corr_ggt(g)))
            elif all(u[j] == v[j] for j in range(n)):
                counts['ratio_plus_one'] += 1
            else:
                counts['nonproportional'] += 1
    counts['ratio_plus_one'] += 0
    counts['total'] = 1 << n
    return counts, nonconstant_minus


def solve_sign_system(f, f2, gg):
    # For d=1,...,n//2, exact orthogonality gives
    # A_d X + B_d Y + C_d = 0, where X=x^2/rho, Y=xc/rho.
    ds = range(1, n//2 + 1)
    A = [f2[d] - gg[d] for d in ds]
    B = [2 * f[d] for d in ds]
    C = [f2[d] + gg[d] for d in ds]
    # B[0]=+/-2, so row 0 is nonzero. Find first independent row.
    pivot = None
    for j in range(1, len(A)):
        det = A[0] * B[j] - A[j] * B[0]
        if det:
            pivot = (j, det)
            break
    if pivot is None:
        # Rank one. Check exact consistency of all rows with row 0.
        consistent = all(
            A[0] * B[d] - A[d] * B[0] == 0
            and A[0] * C[d] - A[d] * C[0] == 0
            and B[0] * C[d] - B[d] * C[0] == 0
            for d in range(len(A))
        )
        return ('rank1_consistent' if consistent else 'rank1_inconsistent',
                (A[0], B[0], C[0]))

    j, det = pivot
    num_x = B[0] * C[j] - B[j] * C[0]
    num_y = A[j] * C[0] - A[0] * C[j]
    if det < 0:
        det, num_x, num_y = -det, -num_x, -num_y
    consistent = all(
        A[d] * num_x + B[d] * num_y + C[d] * det == 0
        for d in range(len(A))
    )
    if not consistent:
        return ('rank2_inconsistent', None)
    physical_range = 0 <= num_x <= det
    quadratic = num_y * num_y == num_x * (num_x + det)
    if physical_range and quadratic:
        return ('rank2_solution', (num_x, num_y, det))
    return ('rank2_linear_only', (num_x, num_y, det))


def audit_constant_G():
    # G=+J or -J gives G G^T = n J, so the sign of G is immaterial.
    counts = Counter()
    rank1_lines = []
    for fmask in range(1 << (n//2)):
        f = [0] * n
        for d in range(1, n//2 + 1):
            sign = 1 if (fmask >> (d-1)) & 1 else -1
            f[d] = sign
            f[n-d] = sign
        f = tuple(f)
        f2 = cyclic_corr_f2(f)
        gg = tuple(n for _ in range(n))
        status, data = solve_sign_system(f, f2, gg)
        counts[status] += 1
        if status == 'rank1_consistent':
            rank1_lines.append((fmask, *data))
    return counts, rank1_lines


def audit_nonconstant_G(g_records):
    counts = Counter()
    rank1_lines = []
    quadratic_solutions = []
    for fmask in range(1 << (n//2)):
        f = [0] * n
        for d in range(1, n//2 + 1):
            sign = 1 if (fmask >> (d-1)) & 1 else -1
            f[d] = sign
            f[n-d] = sign
        f = tuple(f)
        f2 = cyclic_corr_f2(f)
        for gmask, g, gg in g_records:
            status, data = solve_sign_system(f, f2, gg)
            counts[status] += 1
            if status == 'rank1_consistent':
                rank1_lines.append((fmask, gmask, *data))
            elif status == 'rank2_solution':
                nx, ny, den = data
                quadratic_solutions.append((fmask, gmask, nx, ny, den))
    return counts, rank1_lines, quadratic_solutions


def main():
    verify_correlation_conventions()
    phase_counts, nonconstant_minus = phase_classification()
    constant_counts, constant_lines = audit_constant_G()
    nonconstant_counts, nonconstant_lines, solutions = audit_nonconstant_G(nonconstant_minus)

    # Independent exact postconditions for the exhaustive classification.
    assert phase_counts == Counter({
        'nonproportional': 2091012,
        'u_zero_only': 2046,
        'v_zero_only': 2046,
        'ratio_minus_one': 2046,
        'both_zero': 2,
        'total': 2097152,
    })
    assert len(nonconstant_minus) == 2046
    assert constant_counts == Counter({'rank2_inconsistent': 1018, 'rank2_linear_only': 4,
                                        'rank1_consistent': 2})
    assert len(constant_lines) == 2
    assert all(line[1:] in [(-2, -2, 40), (-2, 2, 40)] for line in constant_lines)
    assert nonconstant_counts == Counter({
        'rank2_inconsistent': 2086892,
        'rank2_linear_only': 4096,
        'rank2_solution': 24,
        'rank1_inconsistent': 4088,
        'rank1_consistent': 4,
    })
    assert len(nonconstant_lines) == 4
    assert all(line[2:] in [(2, -2, 36), (2, 2, 36)] for line in nonconstant_lines)
    assert len(solutions) == 24
    assert all((x, y) == (0, 0) for _, _, x, y, _ in solutions)

    haar_moments = []
    for r in range(n + 1):
        numerator = (-1) ** r * comb(n, r)
        denominator = comb(2*n, 2*r)
        assert Fraction(numerator, denominator) * denominator == numerator
        reduced = Fraction(numerator, denominator)
        haar_moments.append({'order': 2*r, 'moment': f'{reduced.numerator}/{reduced.denominator}',
                             'subset_sum': numerator})

    mode0_pairs = sorted((u, v) for u in range(-6, 7) for v in range(-6, 7)
                         if u % 2 == 0 and v % 2 == 1 and u*u + v*v == 41)
    assert mode0_pairs == [(-4, -5), (-4, 5), (4, -5), (4, 5)]

    result = {
        'status': 'exact_exhaustive_N42_period_two_single_atom_pair_moment_no_go',
        'complete': True,
        'N': N,
        'n': n,
        'rho': '1/41',
        'geometric_interpretation': {
            'physical_Q': 'Q=exp(A(c))D=exp(A(c)/2) D exp(-A(c)/2), a symmetric orthogonal involution with 21 eigenvalues +1 and 21 eigenvalues -1.',
            'projector': 'P=(I+Q)/2 is a rank-21 real orthogonal projector, hence a point of Gr_R(21,42).',
            'haar_target': 'For Haar Q=O D O^T, det(I+tQ)=(1-t^2)^21. Orthogonal invariance makes each order-2r principal-minor expectation equal (-1)^r*C(21,r)/C(42,2r).',
            'moments': haar_moments,
        },
        'phase_sign_patterns': {k: v for k, v in sorted(phase_counts.items())},
        'constant_G_branch': {
            'F_patterns': 1024,
            'counts': dict(sorted(constant_counts.items())),
            'rank1_consistent_lines': [list(x) for x in constant_lines],
            'line_exclusion': 'For X in [0,1], Y^2=X(X+1), |Y|<=sqrt(2), -2X +/- 2Y + 40 > 0.',
        },
        'nonconstant_G_branch_b_equals_minus_a': {
            'G_patterns': len(nonconstant_minus),
            'F_patterns': 1024,
            'pair_count': len(nonconstant_minus) * 1024,
            'counts': dict(sorted(nonconstant_counts.items())),
            'rank1_consistent_lines': [list(x) for x in nonconstant_lines],
            'quadratic_solutions': [list(x) for x in solutions],
            'rank1_line_exclusion': 'For X in [0,1], Y^2=X(X+1), |Y|<=sqrt(2), 2X +/- 2Y + 36 > 0.',
            'rank2_conclusion': 'All 24 feasible exact sign-pattern systems force X=Y=0, hence x=0 and c=s=1/sqrt(41).',
        },
        'transcendence_step': {
            'fourier_mode_0': 'exp(i*4a)=(f_sum+i*g_sum)/sqrt(41), where f_sum is an even integer, g_sum is an odd integer, and f_sum^2+g_sum^2=41; hence f_sum=+/-4 and g_sum=+/-5.',
            'mode0_integer_pairs': [list(x) for x in mode0_pairs],
            'not_root_of_unity': 'If alpha were a root of unity, alpha+alpha^{-1}=+/-8/sqrt(41) would be an algebraic integer, but its square 64/41 is rational nonintegral.',
            'fourier_mode_1': 'exp(i*4a*cos(pi/21))=C_1+i*exp(-i*pi/21)*S_1 is algebraic because C_1,S_1 are cyclotomic algebraic numbers scaled by 1/sqrt(41).',
            'theorem': 'Gelfond-Schneider: if alpha is algebraic and not 0 or 1, and beta is algebraic irrational, every value of alpha^beta is transcendental. Here beta=cos(pi/21), contradicting algebraicity of exp(i*4a*beta).',
        },
        'transcendence_reference': {
            'Gelfond': 'A. O. Gelfond, Sur le septieme probleme de D. Hilbert, C. R. Acad. Sci. URSS 2 (1934), 1-6.',
            'Schneider': 'T. Schneider, Transzendenzuntersuchungen periodischer Funktionen. I. Transzendenz von Potenzen, J. Reine Angew. Math. 172 (1934), 65-69.',
        },
        'theorem': 'No real alternating couplings c_(2j)=a,c_(2j+1)=b on the 42-cycle produce a single physical Q=exp(A(c))D whose every two-site principal minor equals -1/41.',
        'scope': 'Single period-two atom only. This does not exclude positive mixtures of period-two atoms or arbitrary non-periodic cycle-coupling ensembles.',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': result['status'],
        'phase_sign_patterns': result['phase_sign_patterns'],
        'constant_G_branch': result['constant_G_branch']['counts'],
        'constant_G_lines': result['constant_G_branch']['rank1_consistent_lines'],
        'nonconstant_G_branch': result['nonconstant_G_branch_b_equals_minus_a']['counts'],
        'nonconstant_G_lines': result['nonconstant_G_branch_b_equals_minus_a']['rank1_consistent_lines'],
        'quadratic_solutions': len(solutions),
        'all_X_Y_zero': all((x,y)==(0,0) for _,_,x,y,_ in solutions),
        'output': str(OUT),
    }, indent=2))

if __name__ == '__main__':
    main()
