"""Independent Arb certificate for the 6,125-column n=21 full-fourth pool.

The discovery LP is floating-point only.  This verifier freezes each decimal
dual coefficient as an exact rational, normalizes it exactly in the scaled
coordinates, and checks all 22 base atoms, 6,101 fractional-grid atoms, and
both connected nonuniform gapped paths with Arb intervals.

A successful result proves a finite-pool separation only.  It is not a
continuous-family obstruction and does not imply a Choi/diamond lower bound.
"""
import hashlib
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from ising_fourth_moments import FourthMoments
from verify_ising_low_moment_design import build_rotation, rational
import verify_ising_full_fourth_fractional_grid_dual_arb as base

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_two_gapped_n21.json"
PARENT_DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_general_gapped_n21.json"
PARENT_CERTIFICATE = ROOT / "evidence/ising_full_fourth_plus_general_gapped_arb_n21.json"
NEW_ESCAPE_CERTIFICATE = ROOT / "evidence/ising_full_fourth_plus_general_gapped_escape_arb_n21.json"
WARM_CERTIFICATE = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_plus_two_gapped_arb_n21.json"

N = 42
GRID_PRECISION_BITS = 128
BASE_PRECISION_BITS = 512
SEPARATION_FLOOR = Fraction(1, 5)


def read_json(path, *, decimal_floats=False):
    raw = path.read_bytes()
    value = json.loads(raw, parse_float=Decimal) if decimal_floats else json.loads(raw)
    return raw, value


def target_score(system, coefficients):
    return sum(
        (
            rational(coefficients[index]) * rational(system.rational_target[index])
            for index in coefficients
        ),
        arb(0),
    )


def record_minimum(gap, label, state):
    lower = gap.lower()
    if state["minimum_lower"] is None or lower < state["minimum_lower"]:
        state["minimum_lower"] = lower
        state["minimum_lower_label"] = label
    if state["minimum_midpoint"] is None or float(gap) < state["minimum_midpoint"]:
        state["minimum_interval"] = str(gap)
        state["minimum_midpoint"] = float(gap)
        state["minimum_midpoint_label"] = label


def main():
    ctx.prec = BASE_PRECISION_BITS

    diagnostic_raw, diagnostic = read_json(DIAGNOSTIC, decimal_floats=True)
    parent_raw, parent = read_json(PARENT_DIAGNOSTIC)
    parent_cert_raw, parent_cert = read_json(PARENT_CERTIFICATE)
    escape_raw, escape_cert = read_json(NEW_ESCAPE_CERTIFICATE)
    warm_raw, warm = read_json(WARM_CERTIFICATE)

    hashes = {
        "diagnostic_sha256": hashlib.sha256(diagnostic_raw).hexdigest(),
        "parent_diagnostic_sha256": hashlib.sha256(parent_raw).hexdigest(),
        "parent_certificate_sha256": hashlib.sha256(parent_cert_raw).hexdigest(),
        "new_escape_certificate_sha256": hashlib.sha256(escape_raw).hexdigest(),
        "warm_certificate_sha256": hashlib.sha256(warm_raw).hexdigest(),
    }

    if diagnostic.get("status") != "floating_full_fourth_6125_column_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected 6,125-column diagnostic status")
    if diagnostic.get("candidate_count") != 6125:
        raise RuntimeError("diagnostic does not contain exactly 6,125 columns")
    if diagnostic.get("base_atom_count") != 22 or diagnostic.get("fractional_grid_count") != 6101:
        raise RuntimeError("unexpected base/fractional-grid pool counts")
    if diagnostic.get("general_gapped_count") != 2 or len(diagnostic.get("appended_gapped_columns", [])) != 2:
        raise RuntimeError("diagnostic does not contain exactly two appended gapped paths")
    if diagnostic.get("full_feature_count") != 1461:
        raise RuntimeError("unexpected full feature count")
    if diagnostic.get("fourth_orbit_count") != 1440 or diagnostic.get("quartet_count") != 111930:
        raise RuntimeError("unexpected fourth-order orbit counts")
    if diagnostic.get("reduced_equations_including_normalization") != 1314:
        raise RuntimeError("unexpected reduced equality-system size")
    if diagnostic.get("exact_hierarchy_pivot_minor_determinant") != "824633720832":
        raise RuntimeError("the exact hierarchy pivot-minor certificate changed")
    if diagnostic.get("parent_diagnostic_sha256") != hashes["parent_diagnostic_sha256"]:
        raise RuntimeError("the 6,125-column diagnostic does not pin the current parent diagnostic")
    if diagnostic.get("parent_certificate_sha256") != hashes["parent_certificate_sha256"]:
        raise RuntimeError("the 6,125-column diagnostic does not pin the current parent Arb certificate")
    if diagnostic.get("new_escape_certificate_sha256") != hashes["new_escape_certificate_sha256"]:
        raise RuntimeError("the 6,125-column diagnostic does not pin the new escape certificate")
    if diagnostic.get("warm_certificate_sha256") != hashes["warm_certificate_sha256"]:
        raise RuntimeError("the 6,125-column diagnostic does not pin the warm certificate")

    if parent_cert.get("status") != "arb_certified_finite_6124_column_full_fourth_plus_general_gapped_separator":
        raise RuntimeError("the 6,124-column parent certificate is invalid")
    if not parent_cert.get("complete") or parent_cert.get("candidate_count") != 6124:
        raise RuntimeError("the 6,124-column parent certificate is incomplete")
    if parent_cert.get("diagnostic_sha256") != hashes["parent_diagnostic_sha256"]:
        raise RuntimeError("the parent certificate does not pin the current parent diagnostic")
    if parent.get("status") != "floating_plus_gapped_finite_pool_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected parent diagnostic status")
    if parent.get("new_candidate_count") != 6124:
        raise RuntimeError("the parent diagnostic does not describe 6,124 columns")

    if escape_cert.get("status") != "arb_certified_expanded_dual_general_gapped_escape":
        raise RuntimeError("the new connected-path escape certificate is invalid")
    if not escape_cert.get("complete") or "connected" not in escape_cert.get("escape_kinds", []):
        raise RuntimeError("the new connected-path escape certificate is incomplete")
    if escape_cert.get("expanded_finite_certificate_sha256") != hashes["parent_certificate_sha256"]:
        raise RuntimeError("the new escape certificate does not pin the 6,124-column parent certificate")
    if not escape_cert.get("candidate_results", {}).get("connected", {}).get("strict_separator_escape_certified"):
        raise RuntimeError("the new connected path is not a certified escape from the parent dual")

    if warm.get("status") != "arb_certified_positive_41_atom_two_fourth_probe_ensemble" or len(warm.get("atoms", [])) != 41:
        raise RuntimeError("the pinned 41-atom warm certificate is invalid")

    # Verify that the two appended exact-rational paths are exactly the parent
    # witness and the independently certified escape, not relabelled columns.
    appended = diagnostic["appended_gapped_columns"]
    if [x.get("kind") for x in appended] != ["parent_general_gapped", "new_general_gapped_escape"]:
        raise RuntimeError("unexpected ordering or labels for appended gapped columns")
    parent_decimal = parent["appended_column_label"]["couplings_exact_decimal"]
    parent_exact = [Fraction(x) for x in parent_decimal]
    parent_column = [Fraction(x) for x in appended[0]["couplings_exact_rational"]]
    if parent_exact != parent_column:
        raise RuntimeError("first appended path differs from the certified parent path")
    escape_exact = [
        Fraction(x)
        for x in escape_cert["candidate_results"]["connected"]["couplings_exact_rational"]
    ]
    escape_column = [Fraction(x) for x in appended[1]["couplings_exact_rational"]]
    if escape_exact != escape_column:
        raise RuntimeError("second appended path differs from the Arb-certified parent-dual escape")
    for label, couplings in (("parent", parent_column), ("new_escape", escape_column)):
        if len(couplings) != N or couplings[-1] != 0:
            raise RuntimeError(f"{label} path has the wrong open-chain edge layout")
        if any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError(f"{label} path is not connected with strictly positive interior couplings")

    floating_dual = diagnostic.get("dual", {})
    if not floating_dual.get("success"):
        raise RuntimeError("the floating LP did not return a dual candidate")
    if Fraction(floating_dual["recomputed_gap"]) <= Fraction(1, 5):
        raise RuntimeError("the floating dual summary has insufficient discovery margin")
    if Fraction(floating_dual["normalized_l1_upper_bound"]) > Fraction(1000001, 1000000):
        raise RuntimeError("the floating dual violates its reported scaled-l1 normalization")

    system = FourthMoments(21)
    reduced = set(system.reduced_indices())
    raw_coefficients = {}
    for item in floating_dual["nonzero_coefficients"]:
        index = int(item["feature_index"])
        if index in raw_coefficients:
            raise RuntimeError(f"duplicate dual feature index {index}")
        if index not in reduced or not 0 <= index < 1461:
            raise RuntimeError(f"dual uses invalid/non-independent feature index {index}")
        raw_coefficients[index] = Fraction(item["coefficient"])
    if len(raw_coefficients) != 78:
        raise RuntimeError(f"expected 78 nonzero dual coefficients, got {len(raw_coefficients)}")

    # The LP scales second moments by 41 and fourth-order orbit moments by
    # 533. Rationalize the decimal dual exactly, then impose ||D^{-1} y||_1=1.
    scale = {index: (41 if index < 21 else 533) for index in raw_coefficients}
    scaled_norm = sum(
        (abs(value) / scale[index] for index, value in raw_coefficients.items()),
        Fraction(0),
    )
    if scaled_norm <= 0:
        raise RuntimeError("the rationalized dual has zero scaled l1 norm")
    coefficients = {index: value / scaled_norm for index, value in raw_coefficients.items()}
    exact_scaled_l1 = sum(
        (abs(value) / scale[index] for index, value in coefficients.items()),
        Fraction(0),
    )
    if exact_scaled_l1 != 1:
        raise RuntimeError("exact scaled dual normalization failed")
    full_l1 = sum((abs(value) for value in coefficients.values()), Fraction(0))
    if full_l1 > 533:
        raise RuntimeError("the full-coordinate dual l1 norm exceeds 533")

    second_coefficients = [
        rational(coefficients.get(index, Fraction(0))) for index in range(21)
    ]
    mask_weights = base.build_mask_weights(system, coefficients)
    block_test = base.self_test(system, coefficients, second_coefficients, mask_weights)
    if block_test.get("passed") != 5:
        raise RuntimeError("active-block pricing self-test did not pass all five cases")

    target = target_score(system, coefficients)
    floor = rational(SEPARATION_FLOOR)
    minimum = {
        "minimum_lower": None,
        "minimum_lower_label": None,
        "minimum_interval": None,
        "minimum_midpoint": None,
        "minimum_midpoint_label": None,
    }
    checked_base = 0
    checked_grid = 0
    checked_gapped = 0
    gapped_intervals = []

    # Recheck the 22 pinned base atoms at 512 bits.
    ctx.prec = BASE_PRECISION_BITS
    for base_index, atom in enumerate(warm["atoms"][:22]):
        if atom["kind"] == "fractional":
            length = int(atom["length"])
            block = base.fractional_block(length, rational(Fraction(atom["alpha"])))
            score = base.block_score(block, length, second_coefficients, mask_weights[length])
        else:
            score = base.full_score(build_rotation(atom), system, coefficients)
        gap = target - score
        if not gap > floor:
            raise RuntimeError(f"base atom {base_index} lacks a certified gap > 1/5: {gap}")
        record_minimum(gap, {"kind": "base", "base_index": base_index}, minimum)
        checked_base += 1

    # Independently price every corrected fractional single-path grid column.
    ctx.prec = GRID_PRECISION_BITS
    grid_target = target_score(system, coefficients)
    grid_floor = rational(SEPARATION_FLOOR)
    for length in range(2, N + 1):
        max_k = 100 if (length % 2 == 1 or length == N) else 200
        entries = mask_weights[length]
        for k in range(max_k + 1):
            if k == 0 and length != 2:
                continue
            alpha_fraction = Fraction(k, 100)
            block = base.fractional_block(length, rational(alpha_fraction))
            score = base.block_score(block, length, second_coefficients, entries)
            gap = grid_target - score
            if not gap > grid_floor:
                raise RuntimeError(
                    f"fractional column L={length}, alpha={alpha_fraction} "
                    f"lacks a certified gap > 1/5: {gap}"
                )
            record_minimum(
                gap,
                {"kind": "fractional", "length": length, "alpha": str(alpha_fraction)},
                minimum,
            )
            checked_grid += 1

    if checked_base != 22 or checked_grid != 6101:
        raise RuntimeError(f"wrong base/grid counts: base={checked_base}, grid={checked_grid}")

    # Evaluate both exact-rational connected paths independently at 512 bits.
    ctx.prec = BASE_PRECISION_BITS
    for index, column in enumerate(appended):
        couplings = [Fraction(x) for x in column["couplings_exact_rational"]]
        atom = {"kind": "gapped", "couplings": [str(x) for x in couplings]}
        score = base.full_score(build_rotation(atom), system, coefficients)
        gap = target - score
        if not gap > floor:
            raise RuntimeError(f"gapped column {index} lacks a certified gap > 1/5: {gap}")
        record_minimum(gap, {"kind": column["kind"], "column_index": 6123 + index}, minimum)
        gapped_intervals.append({
            "kind": column["kind"],
            "gap_interval": str(gap),
            "minimum_lower_endpoint": str(gap.lower()),
        })
        checked_gapped += 1

    checked = checked_base + checked_grid + checked_gapped
    if checked != 6125 or checked_gapped != 2:
        raise RuntimeError(f"verified {checked} columns instead of exactly 6,125")
    if minimum["minimum_lower"] is None or not minimum["minimum_lower"] > floor:
        raise RuntimeError("the common strict 1/5 Arb lower bound was not established")

    result = {
        "status": "arb_certified_finite_6125_column_full_fourth_plus_two_gapped_separator",
        "complete": True,
        "interval_backend": "python-flint / Arb",
        "precision_bits_base_and_gapped": BASE_PRECISION_BITS,
        "precision_bits_fractional_grid": GRID_PRECISION_BITS,
        **hashes,
        "parent_certificate_status": parent_cert["status"],
        "new_escape_certificate_status": escape_cert["status"],
        "candidate_count": checked,
        "base_atom_count": checked_base,
        "fractional_grid_count": checked_grid,
        "general_gapped_count": checked_gapped,
        "full_feature_count": 1461,
        "independent_moment_rows": 1313,
        "equalities_including_normalization": 1314,
        "fourth_orbit_count": len(system.keys),
        "quartet_count": len(system.indices),
        "dual_nonzero_coefficients": len(coefficients),
        "dual_scaled_l1_exact": str(exact_scaled_l1),
        "dual_full_coordinate_l1_exact": str(full_l1),
        "dual_full_coordinate_l1_upper_bound": 533,
        "dual_coefficients_exact_rational": [
            {"feature_index": index, "coefficient": str(value)}
            for index, value in sorted(coefficients.items())
        ],
        "target_score_interval": str(target),
        "certified_common_column_gap_lower_bound": "1/5",
        "minimum_column_gap_lower_endpoint": str(minimum["minimum_lower"]),
        "minimum_gap_lower_endpoint_candidate": minimum["minimum_lower_label"],
        "minimum_gap_interval_by_midpoint_selection": minimum["minimum_interval"],
        "minimum_gap_candidate_by_midpoint": minimum["minimum_midpoint_label"],
        "appended_gapped_gap_intervals": gapped_intervals,
        "block_pricing_self_test": block_test,
        "proof": (
            "Let D be diagonal with entries 41 on the 21 second-moment coordinates "
            "and 533 on the 1,440 fourth-order orbit coordinates. The exact "
            "rationalized dual y is normalized so ||D^{-1}y||_1=1. Arb certifies "
            "y^T(b-a_j)>1/5 for every one of the 6,125 listed physical columns. "
            "Hence every probability mixture p on this exact finite pool obeys "
            "y^T(b-Ap)>1/5. Since ||y||_1<=533, Holder gives "
            "||b-Ap||_infinity>1/2665."
        ),
        "scope": (
            "This is a rigorous finite-pool obstruction for exactly 22 pinned "
            "base atoms, 6,101 corrected fractional single-open-path grid atoms, "
            "and two specified connected nonuniform gapped open paths. It does "
            "not cover other nonuniform gapped couplings, the continuous gapped "
            "family, arbitrary multi-segment paths, all even principal minors, "
            "or an operational Choi/diamond-distance guarantee."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_count": checked,
        "base_atom_count": checked_base,
        "fractional_grid_count": checked_grid,
        "general_gapped_count": checked_gapped,
        "dual_nonzero_coefficients": len(coefficients),
        "target_score_interval": result["target_score_interval"],
        "certified_common_column_gap_lower_bound": "1/5",
        "minimum_column_gap_lower_endpoint": str(minimum["minimum_lower"]),
        "minimum_gap_candidate": minimum["minimum_lower_label"],
        "gapped_gap_intervals": gapped_intervals,
        "dual_full_coordinate_l1_exact": str(full_l1),
        "moment_residual_infinity_lower_bound": "1/2665",
        "diagnostic_sha256": hashes["diagnostic_sha256"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
