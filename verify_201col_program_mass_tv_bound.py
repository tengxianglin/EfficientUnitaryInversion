"""Exact-rational program-mass TV corollary from the certified 201-column dual.

This script does not re-run the Arb column pricing. It verifies the exact
post-processing from the already Arb-certified rational dual to a bounded
orbit-character witness and its total-variation lower bound.
"""
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERT = ROOT / "evidence/55probe_201col_uniform_ray_escape_dual_certificate_n21.json"
OUTPUT = ROOT / "evidence/201col_program_mass_tv_bound_n21.json"
EXPECTED_CERT_GIT_BLOB_SHA = "976fa3a07a0677a7753de329f9928f6ace5f4aff"


def git_blob_sha(raw):
    header = b"blob " + str(len(raw)).encode() + b"\0"
    return hashlib.sha1(header + raw).hexdigest()


def main():
    raw = CERT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    blob_digest = git_blob_sha(raw)
    if blob_digest != EXPECTED_CERT_GIT_BLOB_SHA:
        raise RuntimeError(f"the pinned 201-column Arb certificate changed: {blob_digest}")
    cert = json.loads(raw)

    if cert.get("status") != "strict_201col_2113row_uniform_ray_escape_minimax_obstruction":
        raise RuntimeError("the source is not the expected certified 201-column dual")
    if cert.get("complete") is not True or cert.get("precision_bits") != 128:
        raise RuntimeError("the source 201-column Arb certificate is incomplete")
    if (cert.get("column_count"), cert.get("row_count")) != (201, 2113):
        raise RuntimeError("unexpected source certificate dimensions")
    if Fraction(cert["dual_l1_norm_exact"]) <= 0 or Fraction(cert["dual_l1_norm_exact"]) > 1:
        raise RuntimeError("the exact dual scaled-L1 norm is outside the admissible unit ball")
    if not cert.get("strict_lower_bound_above_one_third"):
        raise RuntimeError("the source certificate does not prove the required strict bound")
    if cert.get("maximum_shifted_column_lhs_upper", 0) >= 0:
        raise RuntimeError("the source certificate has no strict Arb column separation")
    if len(cert.get("column_dual_lhs_intervals", [])) != 201:
        raise RuntimeError("the source certificate does not record all 201 column intervals")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(1, 533)] * 1440
        + [Fraction(5, 19721)] * 645
        + [Fraction(1, 19721)] * 7
    )
    if len(z) != 2113 or len(scales) != 2113:
        raise RuntimeError("the dual/scale vector does not match the 2,113-row design")

    # Every row feature is an average of parity characters over a dihedral
    # orbit, so its pointwise absolute value is at most one. The LP evaluates
    # that feature divided by its exact row scale.
    coefficient_norm = sum(
        (abs(value) / scale for value, scale in zip(z, scales)),
        Fraction(0),
    )
    objective = Fraction(cert["dual_objective_exact"])
    slack = Fraction(cert["dual_slack_delta"])
    residual_gap = objective - slack
    if residual_gap != Fraction(cert["certified_minimax_lower_bound"]):
        raise RuntimeError("the exact objective-minus-slack does not match the certified lower bound")
    if coefficient_norm <= 0:
        raise RuntimeError("the bounded-character coefficient norm is not positive")

    tv_bound = residual_gap / (2 * coefficient_norm)
    with localcontext() as ctx:
        ctx.prec = 60
        tv_decimal = str(Decimal(tv_bound.numerator) / Decimal(tv_bound.denominator))
        norm_decimal = str(Decimal(coefficient_norm.numerator) / Decimal(coefficient_norm.denominator))

    result = {
        "status": "exact_rational_program_mass_tv_corollary_from_201col_arb_dual",
        "complete": True,
        "source_certificate_sha256": digest,
        "source_certificate_git_blob_sha": blob_digest,
        "source_certificate_status": cert["status"],
        "source_precision_bits": cert["precision_bits"],
        "column_count": cert["column_count"],
        "row_count": cert["row_count"],
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
            "For each retained row i, let phi_i be its dihedral-orbit average "
            "of the even-parity character (-1)^|I intersect T|. Then "
            "||phi_i||_infinity <= 1 and E_{w_R} phi_i is the corresponding "
            "principal-minor moment. With exact row scale s_i, define "
            "G(T)=sum_i z_i phi_i(T)/s_i. Its sup norm is at most "
            "M=sum_i |z_i|/s_i. The Arb-certified dual gives "
            "E_u G - E_{w_p} G > objective-slack for every mixture p on "
            "the exact 201-column pool. By the TV dual inequality, "
            "TV(w_p,u) > (objective-slack)/(2M)."
        ),
        "scope": (
            "One selected parity sector and arbitrary probability mixtures "
            "over exactly the 200 certified physical columns. The conclusion "
            "is for the balanced program-label mass distribution (equivalently "
            "the dephased label-register trace distance), not a Choi-state or "
            "channel diamond-distance lower bound. The 645 sixth-order rows "
            "and seven eighth-order rows are selected/cut inventories, not "
            "complete orbit systems."
        )
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
