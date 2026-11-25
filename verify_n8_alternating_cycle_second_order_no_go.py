"""Exact finite sign-pattern verifier for the N=8 period-two single-atom no-go."""
from __future__ import annotations
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence/n8_alternating_cycle_second_order_no_go.json"


def main():
    observed_pairs = set()
    admissible_pairs = set()
    rows = []
    for g, h, i, j in itertools.product((-1, 1), repeat=4):
        r1 = (g + i) * (h + j) // 2
        r2 = g * i + h * j
        observed_pairs.add((r1, r2))
        eps_f_solutions = [
            [eps, f]
            for eps, f in itertools.product((-1, 1), repeat=2)
            if eps * r1 == f * r2
        ]
        if eps_f_solutions:
            admissible_pairs.add((r1, r2))
        rows.append({
            "F_first_row": [g, h, i, j],
            "R1": r1,
            "R2": r2,
            "eps_f_solutions": eps_f_solutions,
        })

    expected_pairs = {(2, 2), (-2, 2), (0, 0), (0, -2)}
    expected_admissible = {(2, 2), (-2, 2), (0, 0)}
    if observed_pairs != expected_pairs:
        raise AssertionError(f"correlation pair set mismatch: {observed_pairs}")
    if admissible_pairs != expected_admissible:
        raise AssertionError(f"admissible pair set mismatch: {admissible_pairs}")
    if {r2 for _, r2 in admissible_pairs} != {0, 2}:
        raise AssertionError("the remaining R2 values are not exactly {0,2}")

    rho = Fraction(1, 7)
    z_r2_zero_gap = (Fraction(0), rho)  # z(z+rho)=(z+rho)^2 forces rho=0
    z_r2_two = Fraction(9, 7) * rho
    if not (z_r2_two > rho):
        raise AssertionError("R2=2 did not contradict z<=rho")

    result = {
        "status": "exact_no_alternating_single_atom_N8_second_order",
        "complete": True,
        "N": 8,
        "target_pair_minor": "-1/7",
        "parity_block_assumptions": [
            "B=2(aI-bT) is real normal circulant for arbitrary real a,b",
            "C=cos(sqrt(BB^T)) is symmetric circulant",
            "S=B*sinc(sqrt(B^TB)) is real circulant",
            "Q=[[C,-S],[-S^T,-C]] and C^2+SS^T=I",
        ],
        "pair_minor_consequences": {
            "rho": "1/7",
            "C_first_row": "[x, eps*c, f*c, eps*c]",
            "c_squared": "x^2+rho",
            "S_entries": "s times a circulant +/-1 sign matrix",
            "s_squared": "rho-x^2",
        },
        "all_16_sign_rows_checked": len(rows),
        "correlation_pair_set": [list(pair) for pair in sorted(observed_pairs)],
        "pairs_surviving_eps_R1_equals_f_R2": [
            list(pair) for pair in sorted(admissible_pairs)
        ],
        "remaining_R2_values": [0, 2],
        "s_zero_case": {
            "forced_identity": "x*f=-c",
            "squared_consequence": "z=z+rho",
            "contradiction": "rho=1/7>0",
        },
        "R2_zero_case": {
            "equation": "z(z+rho)=(z+rho)^2",
            "contradiction": "z+rho>0 forces rho=0",
        },
        "R2_two_case": {
            "equation": "z(z+rho)=(3*rho-z)^2",
            "forced_z": str(z_r2_two),
            "upper_bound": str(rho),
            "contradiction": "9/49 > 1/7",
        },
        "scope": "Excludes one N=8 cycle exponential with alternating real couplings. Does not exclude mixtures of such atoms or arbitrary non-period-two physical cycle couplings.",
    }

    if len(rows) != 16 or z_r2_zero_gap[1] <= 0:
        raise AssertionError("incomplete exact checks")
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not EVIDENCE.exists():
        EVIDENCE.write_text(encoded)
    elif json.loads(EVIDENCE.read_text()) != result:
        raise AssertionError("committed evidence differs from exact sign enumeration")
    print(json.dumps({
        "status": result["status"],
        "sign_rows_checked": len(rows),
        "correlation_pairs": result["correlation_pair_set"],
        "admissible_pairs": result["pairs_surviving_eps_R1_equals_f_R2"],
        "R2_two_forced_z": str(z_r2_two),
        "rho": str(rho),
        "evidence": str(EVIDENCE.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
