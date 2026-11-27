"""256-bit Arb regression for the N=42 period-two all-quartic no-go.

The continuum theorem is analytic in THEORY_N42_PERIOD_TWO_ALL_QUARTIC_NO_GO.md.
For each frozen rational period-two coupling pair, this script reconstructs
Q in Fourier form, checks Q^T=Q, Q^2=I, tr(Q)=0 and tr(Q[{0,1},{0,1}])=0,
then directly sums all C(40,2)=780 quartic principal minors containing {0,1}.
"""
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/n42_period_two_all_quartic_no_go_arb.json"
N, n = 42, 21
SAMPLES = [
    ("1/3", "2/5"),
    ("3/2", "7/4"),
    ("-2/3", "5/7"),
    ("-3/2", "-5/4"),
    ("7/5", "-9/8"),
]


def rational(value):
    q = Fraction(value)
    return arb(fmpq(q.numerator, q.denominator))


def build_tables(size):
    two_pi = 2 * arb.pi()
    cosine, sine = [], []
    for k in range(size):
        rc, rs = [], []
        for d in range(size):
            angle = two_pi * (k * d) / size
            rc.append(angle.cos())
            rs.append(angle.sin())
        cosine.append(rc)
        sine.append(rs)
    return cosine, sine


def build_q(a, b, cosine, sine):
    c_symbol, sinc_symbol = [], []
    for k in range(n):
        ck = cosine[k][1]
        sk = sine[k][1]
        mu_sq = 4 * (a * a + b * b - 2 * a * b * ck)
        if not (mu_sq > 0):
            raise AssertionError(f"sample has a nonpositive Fourier mode: k={k}, {mu_sq}")
        mu = mu_sq.sqrt()
        cm, sm = mu.cos(), mu.sin()
        if not (cm * cm + sm * sm).contains(1):
            raise AssertionError("Fourier trigonometric identity failed")
        c_symbol.append(cm)
        sinc_symbol.append(sm / mu)

    C, S = [], []
    for d in range(n):
        cd, sd = arb(0), arb(0)
        for k in range(n):
            co, si = cosine[k][d], sine[k][d]
            cd += c_symbol[k] * co
            sd += 2 * sinc_symbol[k] * (
                (a - b * cosine[k][1]) * co + b * sine[k][1] * si
            )
        C.append(cd / n)
        S.append(sd / n)

    def entry(i, j):
        if i % 2 == 0 and j % 2 == 0:
            return C[(j // 2 - i // 2) % n]
        if i % 2 == 1 and j % 2 == 1:
            return -C[(j // 2 - i // 2) % n]
        if i % 2 == 0 and j % 2 == 1:
            return -S[(j // 2 - i // 2) % n]
        return -S[(i // 2 - j // 2) % n]

    return arb_mat([[entry(i, j) for j in range(N)] for i in range(N)])


def principal_minor(Q, indices):
    return arb_mat([
        [Q[i, j] for j in indices]
        for i in indices
    ]).det()


def check_zero(value, label):
    if not value.contains(0):
        raise AssertionError(f"{label} does not contain zero: {value}")


def verify():
    ctx.prec = 256
    cosine, sine = build_tables(n)
    records = []
    quartets = list(combinations(range(2, N), 2))
    assert len(quartets) == comb(40, 2) == 780

    for a_text, b_text in SAMPLES:
        a, b = rational(a_text), rational(b_text)
        Q = build_q(a, b, cosine, sine)

        # Structural regression for Q=exp(A)D.
        for i in range(N):
            for j in range(N):
                check_zero(Q[i, j] - Q[j, i], "Q symmetry")
        Q2 = Q * Q
        for i in range(N):
            for j in range(N):
                check_zero(Q2[i, j] - (1 if i == j else 0), "Q involution")
        trace_q = sum((Q[i, i] for i in range(N)), arb(0))
        check_zero(trace_q, "tr(Q)=0")

        # Period-two gives equal R diagonal entries on even/odd sites,
        # hence Q_00 + Q_11 = 0.
        t = Q[0, 0] + Q[1, 1]
        check_zero(t, "tr(Q_{I,I})=0 for I={0,1}")
        p = principal_minor(Q, [0, 1])

        total = arb(0)
        for J in quartets:
            total += principal_minor(Q, [0, 1, J[0], J[1]])
        identity_residual = total + n * p + 1
        check_zero(identity_residual, "sum of 780 quartics + 21 pair + 1")

        records.append({
            "a": a_text,
            "b": b_text,
            "trace_Q": str(trace_q),
            "trace_fixed_pair_block": str(t),
            "pair_minor": str(p),
            "sum_780_quartic_minors": str(total),
            "incidence_identity_residual": str(identity_residual),
            "quartic_count": len(quartets),
        })

    pair_target = Fraction(-1, 41)
    quartic_target = Fraction(1, 533)
    assert Fraction(comb(n, 2), comb(N, 4)) == quartic_target
    target_quartic_sum = comb(40, 2) * quartic_target
    target_functional = target_quartic_sum + n * pair_target
    physical_functional = Fraction(-1, 1)
    gap = target_functional - physical_functional
    coefficient_l1 = comb(40, 2) + n
    margin = gap / coefficient_l1
    pair_exact_quartic_residual = gap / comb(40, 2)
    required_diagonal_imbalance = gap

    assert target_quartic_sum == Fraction(60, 41)
    assert target_functional == Fraction(39, 41)
    assert gap == Fraction(80, 41)
    assert coefficient_l1 == 801
    assert margin == Fraction(80, 32841)
    assert pair_exact_quartic_residual == Fraction(4, 1599)

    return {
        "status": "arb_regression_passed_N42_period_two_all_quartic_incidence_identity",
        "N": N,
        "n": n,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "sample_count": len(records),
        "quartic_minors_summed_per_sample": len(quartets),
        "samples": records,
        "target_pair_Q": str(pair_target),
        "target_quartic_Q": str(quartic_target),
        "target_sum_of_780_quartics": str(target_quartic_sum),
        "target_linear_functional": str(target_functional),
        "period_two_linear_functional": str(physical_functional),
        "exact_gap": str(gap),
        "coefficient_l1_norm": coefficient_l1,
        "certified_analytic_linf_margin": str(margin),
        "quartic_only_margin_if_pair_moments_are_exact": str(pair_exact_quartic_residual),
        "necessary_mean_square_diagonal_imbalance_for_general_physical_ensemble": str(required_diagonal_imbalance),
        "scope": (
            "The analytic theorem excludes every probability measure over all real "
            "N=42 period-two cycle couplings from matching all pair and all quartic "
            "balanced-slice principal-minor moments. The Arb samples are regression "
            "checks of the Fourier reconstruction and the 780-minor incidence identity; "
            "they are not the continuum proof. Non-period-two physical ensembles remain open."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        key: result[key] for key in (
            "status", "precision_bits", "sample_count",
            "quartic_minors_summed_per_sample", "target_linear_functional",
            "period_two_linear_functional", "exact_gap",
            "coefficient_l1_norm", "certified_analytic_linf_margin",
            "quartic_only_margin_if_pair_moments_are_exact",
            "necessary_mean_square_diagonal_imbalance_for_general_physical_ensemble",
            "scope"
        )
    }, indent=2), flush=True)
