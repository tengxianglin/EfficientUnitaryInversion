"""Exact-rational program-mass TV corollary from the certified 202-column dual."""
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERT = ROOT / "evidence/55probe_202col_uniform_ray_escape_dual_certificate_n21.json"
OUTPUT = ROOT / "evidence/202col_program_mass_tv_bound_n21.json"


def main():
    raw = CERT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    cert = json.loads(raw)
    if cert.get("status") != "strict_202col_2113row_uniform_ray_escape_minimax_obstruction":
        raise RuntimeError("source is not the strict 202-column Arb dual certificate")
    if cert.get("complete") is not True or cert.get("precision_bits") != 128:
        raise RuntimeError("source 202-column Arb certificate is incomplete")
    if (cert.get("column_count"), cert.get("row_count")) != (202, 2113):
        raise RuntimeError("unexpected source certificate dimensions")
    if not cert.get("strict_lower_bound_above_one_third") or cert.get("maximum_shifted_column_lhs_upper", 0) >= 0:
        raise RuntimeError("source certificate lacks strict finite-pool separation")
    if len(cert.get("column_dual_lhs_intervals", [])) != 202:
        raise RuntimeError("source certificate does not record all 202 Arb column intervals")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(1, 533)] * 1440
        + [Fraction(5, 19721)] * 645
        + [Fraction(1, 19721)] * 7
    )
    if len(z) != 2113 or len(scales) != 2113:
        raise RuntimeError("dual/scale vector does not match the 2,113-row design")

    coefficient_norm = sum((abs(value) / scale for value, scale in zip(z, scales)), Fraction(0))
    objective = Fraction(cert["dual_objective_exact"])
    slack = Fraction(cert["dual_slack_delta"])
    residual_gap = objective - slack
    if residual_gap != Fraction(cert["certified_minimax_lower_bound"]):
        raise RuntimeError("objective-minus-slack does not match the certified lower bound")
    if coefficient_norm <= 0:
        raise RuntimeError("bounded-character coefficient norm is not positive")

    tv_bound = residual_gap / (2 * coefficient_norm)
    with localcontext() as ctx:
        ctx.prec = 60
        tv_decimal = str(Decimal(tv_bound.numerator) / Decimal(tv_bound.denominator))
        norm_decimal = str(Decimal(coefficient_norm.numerator) / Decimal(coefficient_norm.denominator))

    result = {
        "status": "exact_rational_program_mass_tv_corollary_from_202col_arb_dual",
        "complete": True,
        "source_certificate_sha256": digest,
        "source_certificate_status": cert["status"],
        "source_precision_bits": cert["precision_bits"],
        "column_count": 202,
        "row_count": 2113,
        "row_blocks": {
            "second_order_complete": 21,
            "fourth_order_complete": 1440,
            "sixth_order_selected_and_cuts": 645,
            "eighth_order_selected": 7
        },
        "row_scales_exact": {
            "second_order": "1/41",
            "fourth_order": "1/533",
            "sixth_order": "5/19721",
            "eighth_order": "1/19721"
        },
        "dual_l1_norm_exact": cert["dual_l1_norm_exact"],
        "dual_objective_exact": str(objective),
        "dual_slack_exact": str(slack),
        "moment_residual_lower_bound_exact": str(residual_gap),
        "bounded_character_coefficient_norm_exact": str(coefficient_norm),
        "bounded_character_coefficient_norm_decimal": norm_decimal,
        "program_mass_tv_lower_bound_exact": str(tv_bound),
        "program_mass_tv_lower_bound_decimal": tv_decimal,
        "strict": True,
        "proof": (
            "For each retained row i, let phi_i be its dihedral-orbit average of the even-parity "
            "character (-1)^|I intersect T|. Then ||phi_i||_infinity <= 1 and E_{w_R} phi_i is "
            "the corresponding principal-minor moment. With exact row scale s_i, define "
            "G(T)=sum_i z_i phi_i(T)/s_i. Its sup norm is at most M=sum_i |z_i|/s_i. "
            "The Arb-certified dual gives E_u G - E_{w_p} G > objective-slack for every mixture "
            "p on the exact 202-column pool. By the TV dual inequality, "
            "TV(w_p,u) > (objective-slack)/(2M)."
        ),
        "scope": (
            "One selected parity sector and arbitrary probability mixtures over exactly the 202 "
            "certified physical columns. This is a balanced program-label mass / dephased "
            "label-register trace-distance statement, not a Choi trace-distance or channel "
            "diamond-distance lower bound. The 645 sixth-order and seven eighth-order rows are "
            "selected/cut inventories, not complete orbit systems."
        )
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
