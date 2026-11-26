"""Independent Arb certificate for the 6,153-column n=21 full-fourth pool.

The floating HiGHS result is only a discovery candidate. This verifier freezes
all decimal dual coefficients as exact rationals, imposes exact scaled-l1
normalization, and independently prices 22 base atoms, 6,101 fractional-grid
atoms, and thirty exact-rational gapped paths.

A successful result proves separation only for this exact finite pool. It is
not a continuum obstruction and is not a Choi/diamond-distance lower bound.
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
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_thirty_gapped_n21.json"
PARENT_DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_twenty_eight_gapped_n21.json"
PARENT_CERTIFICATE = ROOT / "evidence/ising_full_fourth_plus_twenty_eight_gapped_arb_n21.json"
NEW_ESCAPE_CERTIFICATE = ROOT / "evidence/ising_full_fourth_plus_twenty_eight_gapped_escape_arb_n21.json"
NEW_ESCAPE_SEARCH = ROOT / "evidence/ising_full_fourth_plus_twenty_eight_gapped_search_n21.json"
WARM_CERTIFICATE = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_plus_thirty_gapped_arb_n21.json"

N = 42
GRID_PRECISION_BITS = 128
BASE_PRECISION_BITS = 512
SEPARATION_FLOOR = Fraction(0)


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
    search_raw, escape_search = read_json(NEW_ESCAPE_SEARCH)
    warm_raw, warm = read_json(WARM_CERTIFICATE)

    hashes = {
        "diagnostic_sha256": hashlib.sha256(diagnostic_raw).hexdigest(),
        "parent_diagnostic_sha256": hashlib.sha256(parent_raw).hexdigest(),
        "parent_certificate_sha256": hashlib.sha256(parent_cert_raw).hexdigest(),
        "new_escape_certificate_sha256": hashlib.sha256(escape_raw).hexdigest(),
        "new_escape_search_sha256": hashlib.sha256(search_raw).hexdigest(),
        "warm_certificate_sha256": hashlib.sha256(warm_raw).hexdigest(),
    }

    if diagnostic.get("status") != "floating_full_fourth_6153_column_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected 6,153-column diagnostic status")
    if diagnostic.get("candidate_count") != 6153:
        raise RuntimeError("diagnostic does not contain exactly 6,153 columns")
    if diagnostic.get("base_atom_count") != 22 or diagnostic.get("fractional_grid_count") != 6101:
        raise RuntimeError("unexpected base/fractional-grid pool counts")
    if diagnostic.get("general_gapped_count") != 30 or len(diagnostic.get("appended_gapped_columns", [])) != 30:
        raise RuntimeError("diagnostic does not contain exactly thirty appended gapped paths")
    if diagnostic.get("full_feature_count") != 1461:
        raise RuntimeError("unexpected full feature count")
    if diagnostic.get("fourth_orbit_count") != 1440 or diagnostic.get("quartet_count") != 111930:
        raise RuntimeError("unexpected fourth-order orbit counts")
    if diagnostic.get("reduced_equations_including_normalization") != 1314:
        raise RuntimeError("unexpected reduced equality-system size")
    if diagnostic.get("exact_hierarchy_pivot_minor_determinant") != "824633720832":
        raise RuntimeError("the exact hierarchy pivot-minor certificate changed")
    for field, key in (
        ("parent_diagnostic_sha256", "parent_diagnostic_sha256"),
        ("parent_certificate_sha256", "parent_certificate_sha256"),
        ("new_escape_certificate_sha256", "new_escape_certificate_sha256"),
        ("new_escape_search_sha256", "new_escape_search_sha256"),
        ("warm_certificate_sha256", "warm_certificate_sha256"),
    ):
        if diagnostic.get(field) != hashes[key]:
            raise RuntimeError(f"the 6,153-column diagnostic does not pin {field}")

    if parent_cert.get("status") != "arb_certified_finite_6151_column_full_fourth_plus_twenty_eight_gapped_separator":
        raise RuntimeError("the 6,151-column parent certificate is invalid")
    if not parent_cert.get("complete") or parent_cert.get("candidate_count") != 6151:
        raise RuntimeError("the 6,151-column parent certificate is incomplete")
    if parent_cert.get("diagnostic_sha256") != hashes["parent_diagnostic_sha256"]:
        raise RuntimeError("the parent certificate does not pin the current parent diagnostic")
    if parent.get("status") != "floating_full_fourth_6151_column_separator_candidate_not_arb_certified" or parent.get("candidate_count") != 6151:
        raise RuntimeError("unexpected 6,151-column parent diagnostic")

    if escape_cert.get("status") != "arb_certified_6151_dual_general_gapped_escape":
        raise RuntimeError("the 6,151-dual escape certificate is invalid")
    if not escape_cert.get("complete") or not {"connected", "multisegment"}.issubset(set(escape_cert.get("escape_kinds", []))):
        raise RuntimeError("the 6,151-dual escape certificate is incomplete")
    if escape_cert.get("diagnostic_sha256") != hashes["parent_diagnostic_sha256"]:
        raise RuntimeError("the escape certificate does not pin the 6,151-column parent diagnostic")
    if escape_cert.get("finite_certificate_sha256") != hashes["parent_certificate_sha256"]:
        raise RuntimeError("the escape certificate does not pin the 6,151-column parent finite-pool certificate")
    if escape_cert.get("search_sha256") != hashes["new_escape_search_sha256"]:
        raise RuntimeError("the escape certificate does not pin its search transcript")
    if escape_search.get("status") != "floating_general_gapped_separator_escape_candidate" or not escape_search.get("complete"):
        raise RuntimeError("the pinned escape search transcript is incomplete")
    if escape_search.get("pins", {}).get("diagnostic_sha256") != hashes["parent_diagnostic_sha256"]:
        raise RuntimeError("the escape search used a different parent diagnostic")
    if escape_search.get("pins", {}).get("finite_certificate_sha256") != hashes["parent_certificate_sha256"]:
        raise RuntimeError("the escape search used a different parent certificate")

    if warm.get("status") != "arb_certified_positive_41_atom_two_fourth_probe_ensemble" or len(warm.get("atoms", [])) != 41:
        raise RuntimeError("the pinned 41-atom warm certificate is invalid")

    # The first twenty-eight gapped columns are inherited exactly from the certified
    # 6,151-column parent. The final two are the connected and multi-segment escapes
    # from that parent's dual, independently certified at 256-bit Arb.
    appended = diagnostic["appended_gapped_columns"]
    parent_appended = parent["appended_gapped_columns"]
    if len(parent_appended) != 28:
        raise RuntimeError("the 6,151-column parent does not contain twenty-eight gapped paths")
    expected_kinds = [
        item["kind"] for item in parent_appended
    ] + [
        "new_connected_escape_from_6151_dual",
        "new_multisegment_escape_from_6151_dual",
    ]
    if [x.get("kind") for x in appended] != expected_kinds:
        raise RuntimeError("unexpected ordering or labels for thirty appended gapped paths")

    for index in range(26):
        expected = [Fraction(x) for x in parent_appended[index]["couplings_exact_rational"]]
        actual = [Fraction(x) for x in appended[index]["couplings_exact_rational"]]
        if expected != actual:
            raise RuntimeError(f"appended path {index} differs from the certified 6,151-column parent pool")

    expected_escape = {
        "new_connected_escape_from_6151_dual": "connected",
        "new_multisegment_escape_from_6151_dual": "multisegment",
    }
    for label, kind in expected_escape.items():
        result = escape_cert["candidate_results"][kind]
        if not result.get("strict_separator_escape_certified"):
            raise RuntimeError(f"the {kind} candidate is not an Arb-certified escape from the 6,151 dual")
        search_values = [
            Fraction(x) for x in escape_search[f"best_{kind}"]["couplings_exact_decimal"]
        ]
        cert_values = [Fraction(x) for x in result["couplings_exact_rational"]]
        if search_values != cert_values:
            raise RuntimeError(f"the {kind} search and Arb certificate couplings disagree")
        column = next(x for x in appended if x.get("kind") == label)
        actual = [Fraction(x) for x in column["couplings_exact_rational"]]
        if actual != cert_values:
            raise RuntimeError(f"the appended {label} differs from its Arb escape certificate")

    for index, column in enumerate(appended):
        couplings = [Fraction(x) for x in column["couplings_exact_rational"]]
        if len(couplings) != N or couplings[-1] != 0:
            raise RuntimeError(f"gapped path {index} has the wrong open-chain edge layout")
        if any(value < 0 for value in couplings[:-1]):
            raise RuntimeError(f"gapped path {index} has a negative internal coupling")
        zero_edges = [j for j, value in enumerate(couplings[:-1]) if value == 0]
        if zero_edges != column.get("internal_zero_edges", []):
            raise RuntimeError(f"gapped path {index} has inconsistent internal-zero metadata")
        if index < 28 and zero_edges != parent_appended[index].get("internal_zero_edges", []):
            raise RuntimeError(f"inherited gapped path {index} differs from the certified 6,151 parent cut pattern")
        if index == 28 and zero_edges:
            raise RuntimeError("the new connected escape unexpectedly has internal zero edges")
        if index == 29:
            expected_new_cuts = escape_cert["candidate_results"]["multisegment"]["internal_zero_edges"]
            if zero_edges != expected_new_cuts or not zero_edges:
                raise RuntimeError("the new 6,151-dual multi-segment escape has inconsistent cuts")

    floating_dual = diagnostic.get("dual", {})
    if not floating_dual.get("success"):
        raise RuntimeError("the floating LP did not return a dual candidate")
    if Fraction(floating_dual["recomputed_gap"]) <= Fraction(1, 10**8):
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
    if not raw_coefficients:
        raise RuntimeError("the 6,153-column diagnostic contains no nonzero dual coefficients")

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
            raise RuntimeError(f"base atom {base_index} does not have a strictly positive Arb gap: {gap}")
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
                    f"does not have a strictly positive Arb gap: {gap}"
                )
            record_minimum(
                gap,
                {"kind": "fractional", "length": length, "alpha": str(alpha_fraction)},
                minimum,
            )
            checked_grid += 1

    if checked_base != 22 or checked_grid != 6101:
        raise RuntimeError(f"wrong base/grid counts: base={checked_base}, grid={checked_grid}")

    # Evaluate all thirty exact-rational gapped paths independently at 512 bits.
    ctx.prec = BASE_PRECISION_BITS
    for index, column in enumerate(appended):
        couplings = [Fraction(x) for x in column["couplings_exact_rational"]]
        atom = {"kind": "gapped", "couplings": [str(x) for x in couplings]}
        score = base.full_score(build_rotation(atom), system, coefficients)
        gap = target - score
        if not gap > floor:
            raise RuntimeError(f"gapped column {index} does not have a strictly positive Arb gap: {gap}")
        record_minimum(gap, {"kind": column["kind"], "column_index": 6123 + index}, minimum)
        gapped_intervals.append({
            "kind": column["kind"],
            "gap_interval": str(gap),
            "minimum_lower_endpoint": str(gap.lower()),
        })
        checked_gapped += 1

    checked = checked_base + checked_grid + checked_gapped
    if checked != 6153 or checked_gapped != 30:
        raise RuntimeError(f"verified {checked} columns instead of exactly 6,153")
    if minimum["minimum_lower"] is None or not minimum["minimum_lower"] > floor:
        raise RuntimeError("the common strictly positive Arb lower bound was not established")
    # Use the strongest simple rational floor justified by the certified Arb minimum.
    # Choose the strongest predeclared rational floor strictly below the
    # independently Arb-certified minimum lower endpoint.
    floor_candidates = (
        Fraction(1, 4),
        Fraction(23879, 100000),
        Fraction(231161, 1000000),
        Fraction(1, 5),
        Fraction(1, 10),
        Fraction(1, 100),
        Fraction(1, 1000),
        Fraction(1, 10**6),
        Fraction(1, 10**12),
        Fraction(1, 10**24),
        Fraction(1, 10**48),
    )
    chosen_floor = next(
        (candidate for candidate in floor_candidates if minimum["minimum_lower"] > rational(candidate)),
        None,
    )
    if chosen_floor is None:
        raise RuntimeError("no predeclared rational separation floor is certified")
    residual_bound = chosen_floor / Fraction(533)
    tv_bound = residual_bound / 2

    result = {
        "status": "arb_certified_finite_6153_column_full_fourth_plus_thirty_gapped_separator",
        "complete": True,
        "interval_backend": "python-flint / Arb",
        "precision_bits_base_and_gapped": BASE_PRECISION_BITS,
        "precision_bits_fractional_grid": GRID_PRECISION_BITS,
        **hashes,
        "parent_certificate_status": parent_cert["status"],
        "new_escape_certificate_status": escape_cert["status"],
        "new_escape_search_status": escape_search["status"],
        "candidate_count": checked,
        "base_atom_count": checked_base,
        "fractional_grid_count": checked_grid,
        "general_gapped_count": checked_gapped,
        "diagnostic_status_label_legacy": False,
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
        "certified_common_column_gap_lower_bound": str(chosen_floor),
        "moment_residual_infinity_lower_bound": str(residual_bound),
        "program_mass_tv_lower_bound": str(tv_bound),
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
            f"y^T(b-a_j)>{chosen_floor} for every one of the 6,153 listed physical columns. "
            "Hence every probability mixture p on this exact finite pool obeys "
            f"y^T(b-Ap)>{chosen_floor}. Since ||y||_1<=533, Holder gives "
            f"||b-Ap||_infinity>{residual_bound}. Each retained moment coordinate is "
            "a bounded orbit-character expectation, so the program-mass TV distance "
            f"is >{tv_bound}."
        ),
        "scope": (
            "This is a rigorous finite-pool obstruction for exactly 22 pinned "
            "base atoms, 6,101 corrected fractional single-open-path grid atoms, "
            "thirty exact-rational gapped paths (twenty-eight inherited from the certified "
            "6,151-column pool and two newly Arb-certified escapes from the 6,151-column dual). "
            "It does not cover "
            "other nonuniform gapped couplings, the continuous gapped family, "
            "other arbitrary multi-segment paths, all even principal minors, or an "
            "operational Choi/diamond-distance guarantee."
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
        "certified_common_column_gap_lower_bound": str(chosen_floor),
        "moment_residual_infinity_lower_bound": str(residual_bound),
        "program_mass_tv_lower_bound": str(tv_bound),
        "minimum_column_gap_lower_endpoint": str(minimum["minimum_lower"]),
        "minimum_gap_candidate": minimum["minimum_lower_label"],
        "gapped_gap_intervals": gapped_intervals,
        "dual_full_coordinate_l1_exact": str(full_l1),
        "moment_residual_infinity_lower_bound": str(residual_bound),
        "program_mass_tv_lower_bound": str(tv_bound),
        "diagnostic_sha256": hashes["diagnostic_sha256"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
