#!/usr/bin/env python3
"""Exact N=4 verification of the complement-folded Plucker frame identities.

Dependency-free: all matrix and exterior-power calculations use Fraction.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/complement_folded_plucker_frame_n4.json"
N = 4
N_PARTICLES = 2
SUBSETS = list(combinations(range(N), N_PARTICLES))
DIM = len(SUBSETS)
MATCHINGS = [
    ((0, 1), (2, 3)),
    ((0, 3), (1, 2)),
    ((0, 2), (1, 3)),
]


def determinant(matrix):
    size = len(matrix)
    if size == 0:
        return F(1)
    result = F(0)
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = F(-1 if inversions % 2 else 1)
        for row in range(size):
            term *= matrix[row][permutation[row]]
        result += term
    return result


def identity(size):
    return [[F(int(i == j)) for j in range(size)] for i in range(size)]


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(matrix, scalar):
    return [[scalar * value for value in row] for row in matrix]


def multiply(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def matrix_equal(left, right):
    return left == right


def matching_involution(matching):
    matrix = [[F(0) for _ in range(N)] for _ in range(N)]
    for i, j in matching:
        matrix[i][j] = F(1)
        matrix[j][i] = F(1)
    return matrix


def minor(matrix, rows, columns):
    return determinant(
        [[matrix[i][j] for j in columns] for i in rows]
    )


def plucker_projector(projection):
    return [
        [minor(projection, rows, columns) for columns in SUBSETS]
        for rows in SUBSETS
    ]


def gauge_projection(projection, signs):
    return [
        [
            signs[i] * projection[i][j] * signs[j]
            for j in range(N)
        ]
        for i in range(N)
    ]


def trace_product(left, right):
    return sum(
        left[i][j] * right[j][i]
        for i in range(DIM)
        for j in range(DIM)
    )


def unnormalized_matching_frames(matching):
    """Return integer-scaled plus/minus frames; normalized columns divide by sqrt(2)."""
    plus = [[F(0) for _ in range(N_PARTICLES)] for _ in range(N)]
    minus = [[F(0) for _ in range(N_PARTICLES)] for _ in range(N)]
    for column, (i, j) in enumerate(matching):
        plus[i][column] = F(1)
        plus[j][column] = F(1)
        minus[i][column] = F(1)
        minus[j][column] = F(-1)
    return plus, minus


def determinant_overlap_square(left, signs, right):
    """Squared Slater overlap from integer-scaled frames, exactly over Fractions."""
    overlap = [
        [
            sum(left[k][i] * signs[k] * right[k][j] for k in range(N))
            for j in range(N_PARTICLES)
        ]
        for i in range(N_PARTICLES)
    ]
    return determinant(overlap) ** 2 / F(2 ** (2 * N_PARTICLES))


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def matrix_text(matrix):
    return [[fraction_text(value) for value in row] for row in matrix]


def check_physical_matching_exponentials():
    D = [[F(int(i == j)) * ((-1) ** j) for j in range(N)] for i in range(N)]

    K0 = [[0 for _ in range(N)] for _ in range(N)]
    for i, j in ((0, 1), (2, 3)):
        K0[i][j] = -1
        K0[j][i] = 1

    K1 = [[0 for _ in range(N)] for _ in range(N)]
    for i, j in ((1, 2), (3, 0)):
        K1[i][j] = 1
        K1[j][i] = -1

    K2 = [
        [0, 1, 0, 1],
        [-1, 0, 1, 0],
        [0, -1, 0, -1],
        [-1, 0, 1, 0],
    ]

    K0_squared = multiply(K0, K0)
    K1_squared = multiply(K1, K1)
    K2_squared = multiply(K2, K2)
    K2_cubed = multiply(K2_squared, K2)

    minus_identity = scale(identity(N), F(-1))
    assert matrix_equal(K0_squared, minus_identity)
    assert matrix_equal(K1_squared, minus_identity)
    assert matrix_equal(K2_cubed, scale(K2, F(-4)))

    records = []
    generators = (K0, K1, K2)
    coupling_strings = [
        ["-pi/4", "0", "-pi/4", "0"],
        ["0", "pi/4", "0", "pi/4"],
        ["pi/4", "pi/4", "-pi/4", "-pi/4"],
    ]

    for index, matching in enumerate(MATCHINGS):
        Q = matching_involution(matching)
        R = multiply(Q, D)
        if index < 2:
            exponential_polynomial = generators[index]
            identity_text = "K^2=-I, hence exp((pi/2)K)=K"
            assert matrix_equal(R, exponential_polynomial)
        else:
            exponential_polynomial = add(
                identity(N), scale(K2_squared, F(1, 2))
            )
            identity_text = "K^3=-4K and K is skew, hence exp((pi/2)K)=I+K^2/2"
            assert matrix_equal(R, exponential_polynomial)

        assert matrix_equal(multiply(transpose(R), R), identity(N))
        assert determinant(R) == 1
        records.append({
            "matching": [list(pair) for pair in matching],
            "cycle_couplings": coupling_strings[index],
            "generator_polynomial_identity": identity_text,
            "R_equals_matching_times_D": True,
            "det_R": "1",
        })
    return D, records


def compute_certificate():
    D, physical_records = check_physical_matching_exponentials()
    seed_q = []
    gauge_states = []
    state_metadata = []
    per_seed_twirl_checks = []

    for matching_index, matching in enumerate(MATCHINGS):
        Q = matching_involution(matching)
        assert matrix_equal(Q, transpose(Q))
        assert matrix_equal(multiply(Q, Q), identity(N))
        assert trace(Q) == 0

        P = scale(add(identity(N), Q), F(1, 2))
        P_complement = add(identity(N), scale(P, F(-1)))
        assert matrix_equal(multiply(P, P), P)
        assert matrix_equal(multiply(P_complement, P_complement), P_complement)
        assert trace(P) == N_PARTICLES
        assert trace(P_complement) == N_PARTICLES

        q = [
            (
                minor(P, subset, subset)
                + minor(P_complement, subset, subset)
            ) / 2
            for subset in SUBSETS
        ]
        assert all(value >= 0 for value in q)
        assert sum(q) == 1
        seed_q.append(q)

        twirl_sum = [[F(0) for _ in range(DIM)] for _ in range(DIM)]
        seed_states = []
        for signs in product((F(-1), F(1)), repeat=N):
            P_g = gauge_projection(P, signs)
            P_complement_g = gauge_projection(P_complement, signs)
            rho_plus = plucker_projector(P_g)
            rho_minus = plucker_projector(P_complement_g)
            Pi = add(rho_plus, rho_minus)

            zero = [[F(0) for _ in range(DIM)] for _ in range(DIM)]
            assert matrix_equal(rho_plus, transpose(rho_plus))
            assert matrix_equal(rho_minus, transpose(rho_minus))
            assert matrix_equal(multiply(rho_plus, rho_plus), rho_plus)
            assert matrix_equal(multiply(rho_minus, rho_minus), rho_minus)
            assert trace(rho_plus) == 1
            assert trace(rho_minus) == 1
            assert matrix_equal(multiply(rho_plus, rho_minus), zero)
            assert matrix_equal(multiply(Pi, Pi), Pi)
            assert trace(Pi) == 2

            seed_states.append(Pi)
            state_metadata.append((matching_index, signs))
            for i in range(DIM):
                for j in range(DIM):
                    twirl_sum[i][j] += Pi[i][j]

        gauge_average = scale(twirl_sum, F(1, 2 ** N))
        expected_gauge_average = [
            [
                2 * q[i] if i == j else F(0)
                for j in range(DIM)
            ]
            for i in range(DIM)
        ]
        assert matrix_equal(gauge_average, expected_gauge_average)
        per_seed_twirl_checks.append(True)
        gauge_states.extend(seed_states)

    q_average = [
        sum(seed_q[seed][i] for seed in range(len(seed_q))) / len(seed_q)
        for i in range(DIM)
    ]
    assert q_average == [F(1, DIM)] * DIM

    pi_average_sum = [[F(0) for _ in range(DIM)] for _ in range(DIM)]
    for Pi in gauge_states:
        for i in range(DIM):
            for j in range(DIM):
                pi_average_sum[i][j] += Pi[i][j]
    pi_average = scale(pi_average_sum, F(1, len(gauge_states)))
    expected_pi_average = [
        [F(2, DIM) if i == j else F(0) for j in range(DIM)]
        for i in range(DIM)
    ]
    assert matrix_equal(pi_average, expected_pi_average)

    frame_potential = sum(
        trace_product(left, right)
        for left in gauge_states
        for right in gauge_states
    ) / (len(gauge_states) ** 2)
    frame_potential_from_q = 4 * sum(value * value for value in q_average)
    target_frame_potential = F(4, DIM)
    assert frame_potential == frame_potential_from_q == target_frame_potential

    matching_frames = [unnormalized_matching_frames(matching) for matching in MATCHINGS]
    for left_index, (left_seed, left_signs) in enumerate(state_metadata):
        U_left, V_left = matching_frames[left_seed]
        for right_index, (right_seed, right_signs) in enumerate(state_metadata):
            U_right, V_right = matching_frames[right_seed]
            relative_signs = tuple(
                left_signs[k] * right_signs[k] for k in range(N)
            )
            overlap_formula = sum((
                determinant_overlap_square(U_left, relative_signs, U_right),
                determinant_overlap_square(U_left, relative_signs, V_right),
                determinant_overlap_square(V_left, relative_signs, U_right),
                determinant_overlap_square(V_left, relative_signs, V_right),
            ))
            direct_overlap = trace_product(
                gauge_states[left_index], gauge_states[right_index]
            )
            assert overlap_formula == direct_overlap

    first_seed_states = gauge_states[: 2 ** N]
    single_seed_frame_potential = sum(
        trace_product(left, right)
        for left in first_seed_states
        for right in first_seed_states
    ) / (len(first_seed_states) ** 2)
    single_seed_chi_square = DIM * single_seed_frame_potential / 4 - 1
    single_seed_tv = sum(
        abs(value - F(1, DIM)) for value in seed_q[0]
    ) / 2
    assert single_seed_frame_potential == 1
    assert single_seed_chi_square == F(1, 2)
    assert single_seed_tv == F(1, 3)

    return {
        "schema": "eui_complement_folded_plucker_frame_n4_v1",
        "status": "exact_fraction_verification_passed",
        "N": N,
        "n": N_PARTICLES,
        "plucker_dimension": DIM,
        "physical_matching_seed_count": len(MATCHINGS),
        "sign_gauges_per_seed_with_global_duplicate": 2 ** N,
        "gauge_expanded_rank_two_projectors": len(gauge_states),
        "physical_exponential_certificates": physical_records,
        "plucker_basis_subsets": [list(subset) for subset in SUBSETS],
        "per_seed_q": [
            [fraction_text(value) for value in q]
            for q in seed_q
        ],
        "mean_q": [fraction_text(value) for value in q_average],
        "mean_rank_two_projector": matrix_text(pi_average),
        "expected_mean_rank_two_projector": matrix_text(expected_pi_average),
        "frame_potential_direct": fraction_text(frame_potential),
        "frame_potential_from_q": fraction_text(frame_potential_from_q),
        "uniform_target_frame_potential": fraction_text(target_frame_potential),
        "single_matching_frame_potential": fraction_text(single_seed_frame_potential),
        "single_matching_chi_square": fraction_text(single_seed_chi_square),
        "single_matching_program_label_tv": fraction_text(single_seed_tv),
        "checks": {
            "all_three_matching_atoms_are_exact_cycle_exponentials": True,
            "all_projection_and_complement_identities": True,
            "all_plucker_projectors_rank_two_after_complement_sum": True,
            "each_seed_gauge_twirl_equals_diagonal_2q": all(per_seed_twirl_checks),
            "three_seed_mean_q_is_uniform": True,
            "mean_rank_two_projector_is_2_over_d_identity": True,
            "direct_frame_potential_matches_4_over_d": True,
            "four_determinant_overlap_formula_all_2304_pairs": True,
            "single_seed_frame_potential_and_tv_diagnostic": True,
        },
        "scope": (
            "Exact N=4 verification of the Plucker/fusion-frame reformulation. "
            "It is not an N=42 ensemble or an operational Choi/diamond certificate."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = compute_certificate()
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        frozen = json.loads(OUTPUT.read_text())
        if frozen != result:
            raise AssertionError("frozen Plucker-frame evidence differs from exact recomputation")
    print(json.dumps({
        "status": result["status"],
        "N": result["N"],
        "dimension": result["plucker_dimension"],
        "mean_q": result["mean_q"],
        "frame_potential": result["frame_potential_direct"],
        "target_frame_potential": result["uniform_target_frame_potential"],
        "single_seed_frame_potential": result["single_matching_frame_potential"],
        "single_seed_TV": result["single_matching_program_label_tv"],
    }, indent=2))


if __name__ == "__main__":
    main()
