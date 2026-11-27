"""256-bit Arb regression for the universal pair-quartic incidence identity.

The continuum proof is in THEORY_N42_PRINCIPAL_MINOR_INCIDENCE_IDENTITY.md.
For frozen rational period-two couplings, this script reconstructs Q, checks
Q^T=Q, Q^2=I and tr(Q)=0, then directly sums all 780 quartic principal
minors containing I={0,1} and checks sum = 1 - 19 det(Q_I).
"""
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/n42_principal_minor_incidence_identity_arb.json"
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

        for i in range(N):
            for j in range(N):
                check_zero(Q[i, j] - Q[j, i], "Q symmetry")
        Q2 = Q * Q
        for i in range(N):
            for j in range(N):
                check_zero(Q2[i, j] - (1 if i == j else 0), "Q involution")
        trace_q = sum((Q[i, i] for i in range(N)), arb(0))
        check_zero(trace_q, "tr(Q)=0")

        pair = principal_minor(Q, [0, 1])
        total = arb(0)
        for J in quartets:
            total += principal_minor(Q, [0, 1, J[0], J[1]])
        expected = 1 - (n - 2) * pair
        residual = total - expected
        check_zero(residual, "universal pair-quartic incidence identity")

        records.append({
            "a": a_text,
            "b": b_text,
            "trace_Q": str(trace_q),
            "pair_minor": str(pair),
            "sum_780_quartic_minors": str(total),
            "identity_rhs": str(expected),
            "identity_residual": str(residual),
            "quartic_count": len(quartets),
        })

    pair_target = Fraction(-1, 41)
    quartic_target = Fraction(1, 533)
    assert Fraction(comb(n, 2), comb(N, 4)) == quartic_target
    target_sum = comb(40, 2) * quartic_target
    target_identity_rhs = 1 - (n - 2) * pair_target
    assert target_sum == Fraction(60, 41)
    assert target_identity_rhs == Fraction(60, 41)
    assert target_sum == target_identity_rhs

    return {
        "status": "arb_regression_passed_universal_pair_quartic_incidence_identity",
        "N": N,
        "n": n,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "sample_count": len(records),
        "quartic_minors_summed_per_sample": len(quartets),
        "samples": records,
        "target_pair_Q": str(pair_target),
        "target_quartic_Q": str(quartic_target),
        "target_sum_of_780_quartics": str(target_sum),
        "identity_prediction_from_pair_target": str(target_identity_rhs),
        "target_identity_exactly_satisfied": True,
        "scope": (
            "The identity is universal for every real symmetric involution of "
            "balanced signature, not a period-two separator. The finite Arb "
            "samples check the Fourier reconstruction and direct 780-minor sums; "
            "the continuum identity is proved analytically in the theory note."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        key: result[key] for key in (
            "status", "precision_bits", "sample_count",
            "quartic_minors_summed_per_sample", "target_sum_of_780_quartics",
            "identity_prediction_from_pair_target", "target_identity_exactly_satisfied",
            "scope"
        )
    }, indent=2), flush=True)
