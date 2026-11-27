"""256-bit Arb regression for the N=8 period-two mixture no-go.

The continuum theorem is analytic in THEORY_N8_PERIOD_TWO_MIXTURE_FOURTH_ORDER_NO_GO.md.
This script independently checks the Fourier-to-principal-minor identities on
frozen exact-rational couplings using direct Arb matrix exponentials.
"""
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/n8_period_two_mixture_fourth_order_no_go.json"
SAMPLES = [
    ("1/3", "2/5"),
    ("3/2", "7/4"),
    ("-2/3", "5/7"),
    ("-3/2", "-5/4"),
    ("7/5", "-9/8"),
    ("2/7", "11/9"),
    ("5/3", "1/4"),
    ("0", "2/3"),
    ("2/3", "0"),
]


def ball(value):
    q = Fraction(value)
    return arb(fmpq(q.numerator, q.denominator))


def build_q(a, b):
    couplings = [a, b] * 4
    A = arb_mat(8, 8)
    for j in range(8):
        k = (j + 1) % 8
        A[j, k] = 2 * couplings[j]
        A[k, j] = -2 * couplings[j]
    R = A.exp()
    Q = arb_mat(8, 8)
    for i in range(8):
        for j in range(8):
            Q[i, j] = R[i, j] if j % 2 == 0 else -R[i, j]
    return Q


def principal_minor(Q, indices):
    return arb_mat([[Q[i, j] for j in indices] for i in indices]).det()


def formulas(a, b):
    total = a * a + b * b
    omega = 2 * total.sqrt()
    x, s = omega.cos(), omega.sin()
    P = (2 * a).cos() * (2 * b).cos() * x
    if total == 0:
        K = arb(1)
    else:
        K = (2 * b).cos() ** 2 * (
            x * x + (a * a / total) * s * s
        )
    return P, K, omega


def check_contains_zero(value, message):
    if not value.contains(0):
        raise AssertionError(f"{message}: {value}")


def verify():
    ctx.prec = 256
    records = []
    strict_amgm_checks = 0

    for a_text, b_text in SAMPLES:
        a_q, b_q = Fraction(a_text), Fraction(b_text)
        a, b = ball(a_q), ball(b_q)
        Q = build_q(a, b)
        Qswap = build_q(b, a)

        for i in range(8):
            for j in range(8):
                check_contains_zero(Q[i, j] - Q[j, i], "Q symmetry")
        Q2 = Q * Q
        for i in range(8):
            for j in range(8):
                check_contains_zero(Q2[i, j] - (1 if i == j else 0), "Q involution")
        check_contains_zero(Q.det() - 1, "det(Q)=1")

        P_direct = principal_minor(Q, [0, 4])
        K_direct = principal_minor(Q, [0, 1, 4, 5])
        P_swap_direct = principal_minor(Qswap, [0, 4])
        K_swap_direct = principal_minor(Qswap, [0, 1, 4, 5])

        P_formula, K_formula, omega = formulas(a, b)
        P_swap_formula, K_swap_formula, _ = formulas(b, a)
        check_contains_zero(P_direct - P_formula, "pair Fourier formula")
        check_contains_zero(K_direct - K_formula, "quartic Fourier formula")
        check_contains_zero(P_swap_direct - P_swap_formula, "swapped pair formula")
        check_contains_zero(K_swap_direct - K_swap_formula, "swapped quartic formula")
        check_contains_zero(P_formula - P_swap_formula, "pair swap invariance")

        K_bar = (K_formula + K_swap_formula) / 2
        total = a * a + b * b
        if total != 0:
            alpha, beta = a * a / total, b * b / total
            x, s = omega.cos(), omega.sin()
            z = s * s
            X, Y = (2 * a).cos() ** 2, (2 * b).cos() ** 2
            A = x * x + alpha * z
            B = x * x + beta * z
            check_contains_zero(alpha + beta - 1, "alpha+beta")
            check_contains_zero(A * B - x * x - alpha * beta * z * z,
                                "key scalar identity")
            K_bar_formula = (Y * A + X * B) / 2
            check_contains_zero(K_bar - K_bar_formula, "symmetrized quartic formula")
            amgm_first = K_bar - (X * Y * A * B).sqrt()
            amgm_second = (X * Y * A * B).sqrt() - abs(P_formula)
            check_contains_zero(
                K_bar - abs(P_formula) - amgm_first - amgm_second,
                "AM-GM decomposition",
            )
            if a_q != 0 and b_q != 0 and not (amgm_first > 0 and amgm_second > 0):
                raise AssertionError(
                    f"strict sample AM-GM gaps not certified for {(a_text, b_text)}: "
                    f"{amgm_first}, {amgm_second}"
                )
            if a_q != 0 and b_q != 0:
                strict_amgm_checks += 1
        else:
            check_contains_zero(K_bar - abs(P_formula), "origin limit")

        gap = K_bar - abs(P_formula)
        if not (gap >= 0):
            raise AssertionError(f"period-two feature inequality failed: {gap}")
        records.append({
            "a": a_text,
            "b": b_text,
            "pair_formula_residual": str(P_direct - P_formula),
            "quartic_formula_residual": str(K_direct - K_formula),
            "swapped_quartic_formula_residual": str(K_swap_direct - K_swap_formula),
            "symmetrized_quartic_minus_abs_pair": str(gap),
        })

    pair_target = Fraction(-1, 7)
    quartic_target = Fraction(3, 35)
    target_sum = pair_target + quartic_target
    dual_l1 = Fraction(1, 2) + Fraction(1, 2)
    margin = -target_sum / 2
    assert target_sum == Fraction(-2, 35)
    assert dual_l1 == 1 and margin == Fraction(1, 35)

    return {
        "status": "arb_verified_N8_period_two_mixture_fourth_order_no_go",
        "complete": True,
        "N": 8,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "sample_count": len(records),
        "strict_amgm_sample_count": strict_amgm_checks,
        "samples": records,
        "pair_target_Q": str(pair_target),
        "quartic_target_Q": str(quartic_target),
        "target_pair_plus_quartic": str(target_sum),
        "dual_l1_norm": str(dual_l1),
        "certified_analytic_margin": str(margin),
        "analytic_inequality": "cyclic-average K(a,b) >= |P(a,b)| for every real a,b",
        "scope": (
            "The analytic theorem excludes every probability measure over the "
            "N=8 period-two cycle family from the complete balanced-slice even-minor "
            "target, with full-feature l_infinity discrepancy at least 1/35. "
            "It does not exclude non-period-two N=8 couplings or the unrestricted "
            "N=42 cycle family. Arb samples verify the exact Fourier/minor formulas; "
            "the continuum inequality is proved analytically."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        key: result[key] for key in (
            "status", "precision_bits", "sample_count",
            "strict_amgm_sample_count", "pair_target_Q", "quartic_target_Q",
            "target_pair_plus_quartic", "dual_l1_norm",
            "certified_analytic_margin", "scope"
        )
    }, indent=2), flush=True)
