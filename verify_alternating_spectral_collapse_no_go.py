"""Exact rational checks for the fixed-parity rank-one spectral-collapse no-go."""
from __future__ import annotations
import json
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence/alternating_spectral_collapse_no_go.json"


def target(n: int, r: int) -> Fraction:
    return Fraction((-1) ** r * comb(n, r), comb(2 * n, 2 * r))


def collapsed_minor(n: int, p: int, q: int) -> Fraction:
    """Minor from det Q_I=(-1)^p(1-2 gamma r/n+2 gamma p q/n^2)."""
    if p < 0 or q < 0 or p > n or q > n or (p + q) % 2:
        raise ValueError("invalid even subset parity counts")
    r = (p + q) // 2
    gamma = Fraction(n * n, 2 * n - 1)
    return Fraction((-1) ** p) * (
        1 - Fraction(2 * gamma * r, n)
        + Fraction(2 * gamma * p * q, n * n)
    )


def verify_small_sizes():
    records = []
    for n in (2, 3):
        checked_subsets = 0
        parity_cases = 0
        by_order = {}
        for r in range(1, n + 1):
            expected = target(n, r)
            order_count = 0
            for p in range(max(0, 2 * r - n), min(n, 2 * r) + 1):
                q = 2 * r - p
                observed = collapsed_minor(n, p, q)
                if observed != expected:
                    raise AssertionError(
                        f"n={n}, r={r}, p={p}, q={q}: {observed} != {expected}"
                    )
                multiplicity = comb(n, p) * comb(n, q)
                checked_subsets += multiplicity
                order_count += multiplicity
                parity_cases += 1
            by_order[str(2 * r)] = {
                "target": str(expected),
                "subsets_checked": order_count,
            }
        if checked_subsets != 2 ** (2 * n - 1) - 1:
            raise AssertionError("not all nonempty even subsets were counted")
        records.append({
            "N": 2 * n,
            "gamma_required": str(Fraction(n * n, 2 * n - 1)),
            "cos_lambda_required": str(Fraction((n - 1) ** 2, 2 * n - 1)),
            "parity_count_cases_checked": parity_cases,
            "nonempty_even_subsets_checked": checked_subsets,
            "orders": by_order,
        })
    return records


def verify_no_go_range():
    records = []
    for n in range(4, 22):
        required_cos = Fraction((n - 1) ** 2, 2 * n - 1)
        if required_cos <= 1:
            raise AssertionError(f"unexpected feasible cosine at n={n}")
        if n > 4:
            previous = Fraction((n - 2) ** 2, 2 * n - 3)
            difference = required_cos - previous
            exact_difference = Fraction(2 * (n - 1) ** 2 - 1, (2 * n - 1) * (2 * n - 3))
            if difference != exact_difference or difference <= 0:
                raise AssertionError("monotonicity certificate failed")
        if n in (4, 5, 21):
            records.append({
                "n": n,
                "N": 2 * n,
                "required_cos_lambda": str(required_cos),
                "strictly_above_one": True,
            })
    return records


def build_evidence():
    return {
        "status": "exact_no_go_for_fixed_parity_rank_one_spectral_collapse",
        "complete": True,
        "assumptions": [
            "N=2n even cycle with fixed even/odd bipartition",
            "alternating couplings c_(2k)=a and c_(2k+1)=b",
            "uniform parity-block singular mode has signed frequency lambda=2(a-b)",
            "every nonuniform singular frequency is an odd integer multiple of pi",
        ],
        "exact_identity": "det(Q_I)=(-1)^p*(1-2*gamma*r/n+2*gamma*p*q/n^2), gamma=1+cos(lambda), |I|=p+q=2r",
        "second_order_requirement": {
            "gamma": "n^2/(2n-1)",
            "cos_lambda": "(n-1)^2/(2n-1)",
            "necessary_condition": "(n-1)^2 <= 2n-1",
            "integer_solutions_n_ge_2": [2, 3],
        },
        "small_size_exact_checks": verify_small_sizes(),
        "excluded_sizes": verify_no_go_range(),
        "N42_required_cos_lambda": str(Fraction(400, 41)),
        "mixture_scope": "The same obstruction applies to every probability mixture supported within this fixed-parity rank-one spectral-collapse class, because the second-order same-parity minor is affine in gamma and E[gamma] must equal n^2/(2n-1)>2 for n>=4.",
        "limitation": "This does not exclude arbitrary alternating couplings, nonalternating cycle couplings, or mixtures of general physical cycle exponentials.",
    }


def main():
    result = build_evidence()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not EVIDENCE.exists():
        EVIDENCE.write_text(encoded)
    elif json.loads(EVIDENCE.read_text()) != result:
        raise AssertionError("committed evidence differs from exact rational recomputation")
    print(json.dumps({
        "status": result["status"],
        "N4_even_subsets": result["small_size_exact_checks"][0]["nonempty_even_subsets_checked"],
        "N6_even_subsets": result["small_size_exact_checks"][1]["nonempty_even_subsets_checked"],
        "N8_required_cos": result["excluded_sizes"][0]["required_cos_lambda"],
        "N42_required_cos": result["N42_required_cos"],
        "evidence": str(EVIDENCE.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
