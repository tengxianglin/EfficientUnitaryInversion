"""Exact finite-pool program-mass TV corollary for the 199-column EUI dual.

This script independently reconstructs the fixed mixed-order row inventory,
checks all rational normalizations, and derives the TV bound using only exact
Fraction arithmetic. The columnwise dual inequalities are certified separately
by verify_199col_uniform_ray_dual_arb.py.
"""
import hashlib
import json
from fractions import Fraction

from audit_complete_sixth_moments import ROOT
from screen_ising_sixth_moments import orbit
from verify_184col_full_sixth_cut_dual_arb import load_exact_design

CERT_PATH = ROOT / "evidence/55probe_199col_uniform_ray_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_199col_uniform_ray_escape_n21.json"
CUT_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
OUTPUT_PATH = ROOT / "evidence/199col_program_mass_tv_bound_n21.json"

EXPECTED_BLOCKS = {
    "low_complete": 1461,
    "sixth_selected_plus_all_cuts": 645,
    "eighth_selected": 7,
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    cert_raw = CERT_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    cut_raw = CUT_PATH.read_bytes()
    cert, lp, cut = (json.loads(raw) for raw in (cert_raw, lp_raw, cut_raw))
    cert_sha, lp_sha, cut_sha = map(sha, (cert_raw, lp_raw, cut_raw))

    if cert.get("status") != "strict_199col_2113row_uniform_ray_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("199-column rational dual is not marked complete and Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (199, 2113):
        raise RuntimeError("unexpected 199-column / 2,113-row dimensions")
    if cert.get("lp_transcript_sha256") != lp_sha or lp.get("lp_transcript_sha256") not in (None, lp_sha):
        raise RuntimeError("199-column LP transcript hash mismatch")
    if cert.get("cut_lp_transcript_sha256") != cut_sha or lp.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("mixed-order cut-design hash mismatch")
    if lp.get("status") != "199col_uniform_ray_escape_lp_above_one_third":
        raise RuntimeError("unexpected 199-column LP status")
    if (lp.get("columns"), lp.get("rows")) != (199, 2113):
        raise RuntimeError("199-column LP dimensions mismatch")

    system, low_scales, sixth_rows, eighth_rows, target, row_blocks = load_exact_design(cut)
    if row_blocks != EXPECTED_BLOCKS or row_blocks != cert.get("row_blocks"):
        raise RuntimeError(f"mixed-order row inventory mismatch: {row_blocks}")
    if len(low_scales) != 1461 or len(system.keys) != 1440:
        raise RuntimeError("complete second-/fourth-order inventory mismatch")
    if len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("selected sixth/eighth-order inventory mismatch")
    if any(len(row) != 6 or not orbit(row, 42) for row in sixth_rows):
        raise RuntimeError("a selected sixth-order row is not a nonempty dihedral orbit")
    if any(len(row) != 8 or not orbit(row, 42) for row in eighth_rows):
        raise RuntimeError("a selected eighth-order row is not a nonempty dihedral orbit")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(z) != 2113:
        raise RuntimeError("exact dual vector has the wrong dimension")
    z_norm = sum((abs(value) for value in z), Fraction(0))
    if z_norm != Fraction(1) or z_norm != Fraction(cert["dual_l1_norm_exact"]):
        raise RuntimeError("exact dual L1 normalization mismatch")

    beta = Fraction(cert["dual_objective_exact"])
    delta = Fraction(cert["dual_slack_delta"])
    lower_bound = beta - delta
    if lower_bound != Fraction(cert["certified_minimax_lower_bound"]):
        raise RuntimeError("exact minimax lower bound mismatch")
    if lower_bound <= Fraction(1, 3):
        raise RuntimeError("finite-pool lower bound does not exceed one third")

    # Row scales in A,b: 1/41 for second moments; 210/111930=1/533
    # for fourth moments; 5/19721 for selected sixth moments; 1/19721
    # for selected eighth moments.
    scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(210, 111930)] * 1440
        + [Fraction(5, 19721)] * 645
        + [Fraction(1, 19721)] * 7
    )
    if len(scales) != len(z):
        raise RuntimeError("row-scale inventory does not match the dual")
    coefficient_bound = sum(
        (abs(value) / scale for value, scale in zip(z, scales)),
        Fraction(0),
    )
    tv_lower_bound = lower_bound / (2 * coefficient_bound)

    expected_M = Fraction(181246491308462426915523, 46116860184274002815)
    expected_tv = Fraction(37088783410838194813145199437, 724985965233849707662092000000000)
    if coefficient_bound != expected_M or tv_lower_bound != expected_tv:
        raise RuntimeError("exact program-character coefficient or TV fraction changed")

    result = {
        "status": "certified_199col_program_mass_tv_lower_bound",
        "complete": True,
        "arithmetic": "exact Python fractions",
        "column_count": 199,
        "row_count": 2113,
        "row_blocks": row_blocks,
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_sha,
        "dual_l1_norm_exact": str(z_norm),
        "dual_objective_exact": str(beta),
        "dual_slack_delta": str(delta),
        "moment_residual_lower_bound_exact": str(lower_bound),
        "program_character_sup_norm_bound_exact": str(coefficient_bound),
        "program_character_sup_norm_bound_decimal": float(coefficient_bound),
        "program_mass_tv_lower_bound_exact": str(tv_lower_bound),
        "program_mass_tv_lower_bound_decimal": float(tv_lower_bound),
        "interpretation": (
            "For every probability mixture supported on the exact 199-column pool, "
            "the ensemble-averaged balanced program-label mass distribution has TV "
            "distance strictly greater than the stated rational bound from the "
            "uniform balanced-label distribution. Equivalently this bounds the "
            "trace distance of the corresponding dephased program registers."
        ),
        "scope": (
            "Finite 199-column pool and fixed 2,113-row mixed-order design only. "
            "The sixth/eighth inventories are selected/cut, not complete. This is "
            "not a Choi-state trace-distance or channel diamond-distance bound, "
            "and it does not extend to arbitrary continuous physical couplings."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "moment_residual_lower_bound_exact": result["moment_residual_lower_bound_exact"],
        "program_character_sup_norm_bound_exact": result["program_character_sup_norm_bound_exact"],
        "program_mass_tv_lower_bound_exact": result["program_mass_tv_lower_bound_exact"],
        "program_mass_tv_lower_bound_decimal": result["program_mass_tv_lower_bound_decimal"],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
