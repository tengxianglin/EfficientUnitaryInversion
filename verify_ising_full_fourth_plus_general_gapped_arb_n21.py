"""Independent Arb certificate for the 6,124-column full-fourth expanded pool.

The 6,123-column single-path pool is enlarged by one exact-decimal,
256-bit-Arb-certified connected nonuniform gapped open path. The floating LP
dual is rationalized from its JSON decimal tokens, normalized exactly in the
scaled coordinates, and independently checked against every physical column.

A successful certificate proves only a finite-pool obstruction. It does not
exclude the full continuous gapped family.
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
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_general_gapped_n21.json"
OLD_DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
OLD_CERTIFICATE = ROOT / "evidence/ising_full_fourth_fractional_grid_dual_arb_n21.json"
WARM_CERTIFICATE = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
GAPPED_SEARCH = ROOT / "evidence/ising_full_fourth_general_gapped_search_n21.json"
GAPPED_CERTIFICATE = ROOT / "evidence/ising_full_fourth_general_gapped_escape_arb_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_plus_general_gapped_arb_n21.json"

N = 42
GRID_PRECISION_BITS = 128
BASE_PRECISION_BITS = 512
SEPARATION_FLOOR = Fraction(1, 5)


def read_json(path, *, decimal_floats=False):
    raw = path.read_bytes()
    if decimal_floats:
        value = json.loads(raw, parse_float=Decimal)
    else:
        value = json.loads(raw)
    return raw, value


def target_score(system, coefficients):
    return sum(
        (
            rational(coefficients[index]) * rational(system.rational_target[index])
            for index in coefficients
        ),
        arb(0),
    )


def main():
    ctx.prec = BASE_PRECISION_BITS

    diagnostic_raw, diagnostic = read_json(DIAGNOSTIC, decimal_floats=True)
    old_diagnostic_raw, old_diagnostic = read_json(OLD_DIAGNOSTIC)
    old_certificate_raw, old_certificate = read_json(OLD_CERTIFICATE)
    warm_raw, warm = read_json(WARM_CERTIFICATE)
    search_raw, search = read_json(GAPPED_SEARCH)
    gapped_certificate_raw, gapped_certificate = read_json(GAPPED_CERTIFICATE)

    diagnostic_sha = hashlib.sha256(diagnostic_raw).hexdigest()
    old_diagnostic_sha = hashlib.sha256(old_diagnostic_raw).hexdigest()
    old_certificate_sha = hashlib.sha256(old_certificate_raw).hexdigest()
    warm_sha = hashlib.sha256(warm_raw).hexdigest()
    search_sha = hashlib.sha256(search_raw).hexdigest()
    gapped_certificate_sha = hashlib.sha256(gapped_certificate_raw).hexdigest()

    if diagnostic.get("status") != (
        "floating_plus_gapped_finite_pool_separator_candidate_not_arb_certified"
    ):
        raise RuntimeError("unexpected expanded-pool diagnostic status")
    floating_dual = diagnostic.get("dual", {})
    if not floating_dual.get("success"):
        raise RuntimeError("the expanded-pool LP did not return a successful dual candidate")
    reported_gap = (
        Fraction(floating_dual["target_score"])
        - Fraction(floating_dual["maximum_candidate_score"])
    )
    if reported_gap <= Fraction(1, 5):
        raise RuntimeError("the floating dual summary does not retain the intended one-fifth margin")
    if Fraction(floating_dual["normalized_l1_upper_bound"]) > Fraction(1000001, 1000000):
        raise RuntimeError("the floating dual summary violates its unit scaled-l1 normalization")
    if diagnostic.get("old_candidate_count") != 6123:
        raise RuntimeError("expanded diagnostic does not pin 6,123 old columns")
    if diagnostic.get("new_candidate_count") != 6124:
        raise RuntimeError("expanded diagnostic does not contain exactly 6,124 columns")
    if diagnostic.get("appended_column_index") != 6123:
        raise RuntimeError("unexpected appended-column index")
    if diagnostic.get("independent_moment_rows") != 1313:
        raise RuntimeError("unexpected independent moment-row count")
    if diagnostic.get("equalities_including_normalization") != 1314:
        raise RuntimeError("unexpected equality-system size")
    if diagnostic.get("fourth_orbit_count") != 1440:
        raise RuntimeError("unexpected fourth-order orbit count")
    if diagnostic.get("full_feature_count") != 1461:
        raise RuntimeError("unexpected full feature count")
    if old_certificate.get("status") != (
        "arb_certified_finite_6123_column_full_fourth_separator"
    ):
        raise RuntimeError("the pinned 6,123-column parent certificate is invalid")
    if old_certificate.get("diagnostic_sha256") != old_diagnostic_sha:
        raise RuntimeError("the parent Arb certificate does not pin its diagnostic")
    if diagnostic.get("old_diagnostic_sha256") != old_diagnostic_sha:
        raise RuntimeError("expanded diagnostic has a stale parent diagnostic hash")
    if diagnostic.get("old_finite_certificate_sha256") != old_certificate_sha:
        raise RuntimeError("expanded diagnostic has a stale parent certificate hash")
    if diagnostic.get("warm_certificate_sha256") != warm_sha:
        raise RuntimeError("expanded diagnostic has a stale warm-start hash")
    if diagnostic.get("gapped_search_sha256") != search_sha:
        raise RuntimeError("expanded diagnostic has a stale gapped-search hash")
    if diagnostic.get("gapped_arb_certificate_sha256") != gapped_certificate_sha:
        raise RuntimeError("expanded diagnostic has a stale gapped Arb-certificate hash")
    if warm.get("status") != "arb_certified_positive_41_atom_two_fourth_probe_ensemble":
        raise RuntimeError("the pinned 41-atom warm certificate is invalid")
    if len(warm.get("atoms", [])) != 41:
        raise RuntimeError("the pinned warm certificate does not contain 41 atoms")
    if gapped_certificate.get("status") != "arb_certified_general_gapped_separator_escape":
        raise RuntimeError("the connected gapped-path certificate is invalid")
    if gapped_certificate.get("search_sha256") != search_sha:
        raise RuntimeError("the gapped Arb certificate does not pin the search output")
    if "connected" not in gapped_certificate.get("escape_kinds", []):
        raise RuntimeError("the pinned gapped certificate has no connected escape")

    system = FourthMoments(21)
    reduced = set(system.reduced_indices())

    raw_coefficients = {}
    for item in diagnostic["dual"]["nonzero_coefficients"]:
        index = int(item["feature_index"])
        if index in raw_coefficients:
            raise RuntimeError(f"duplicate dual feature index {index}")
        if index not in reduced:
            raise RuntimeError(f"dual uses non-independent feature coordinate {index}")
        if index < 0 or index >= 1461:
            raise RuntimeError(f"dual feature index {index} is out of range")
        raw_coefficients[index] = Fraction(item["coefficient"])
    if len(raw_coefficients) != 75:
        raise RuntimeError(f"expected 75 nonzero dual coefficients, got {len(raw_coefficients)}")

    # The discovery LP uses D_i=41 for second moments and D_i=533 for
    # fourth-order orbit moments. Its normalized dual is y_scaled=D^{-1}y.
    # Rationalize the frozen decimal coefficients, then normalize exactly so
    # ||y_scaled||_1=1. This preserves every strict column inequality.
    scale = {index: (41 if index < 21 else 533) for index in raw_coefficients}
    scaled_norm = sum(
        (abs(value) / scale[index] for index, value in raw_coefficients.items()),
        Fraction(0),
    )
    if scaled_norm <= 0:
        raise RuntimeError("the rationalized dual has zero scaled l1 norm")
    coefficients = {
        index: value / scaled_norm for index, value in raw_coefficients.items()
    }
    exact_scaled_l1 = sum(
        (abs(value) / scale[index] for index, value in coefficients.items()),
        Fraction(0),
    )
    if exact_scaled_l1 != 1:
        raise RuntimeError("exact scaled dual normalization failed")
    full_l1 = sum((abs(value) for value in coefficients.values()), Fraction(0))
    if full_l1 > 533:
        raise RuntimeError("the full-coordinate dual l1 norm exceeds the scale bound")

    second_coefficients = [
        rational(coefficients.get(index, Fraction(0))) for index in range(21)
    ]
    mask_weights = base.build_mask_weights(system, coefficients)
    block_test = base.self_test(
        system, coefficients, second_coefficients, mask_weights
    )
    if block_test.get("passed") != 5:
        raise RuntimeError("active-block pricing self-test did not pass all five cases")

    target = target_score(system, coefficients)
    floor = rational(SEPARATION_FLOOR)
    minimum_lower = None
    minimum_lower_label = None
    minimum_interval = None
    minimum_midpoint = None
    minimum_midpoint_label = None
    checked_base = 0
    checked_grid = 0

    # Recheck all 22 pinned base atoms at 512 bits.
    ctx.prec = BASE_PRECISION_BITS
    for base_index, atom in enumerate(warm["atoms"][:22]):
        if atom["kind"] == "fractional":
            length = int(atom["length"])
            block = base.fractional_block(length, rational(Fraction(atom["alpha"])))
            score = base.block_score(
                block, length, second_coefficients, mask_weights[length]
            )
        else:
            rotation = build_rotation(atom)
            score = base.full_score(rotation, system, coefficients)
        gap = target - score
        if not gap > floor:
            raise RuntimeError(
                f"base atom {base_index} does not have a certified gap > 1/5: {gap}"
            )
        lower = gap.lower()
        if minimum_lower is None or lower < minimum_lower:
            minimum_lower = lower
            minimum_lower_label = {"kind": "base", "base_index": base_index}
        if minimum_interval is None or float(gap) < minimum_midpoint:
            minimum_interval = str(gap)
            minimum_midpoint = float(gap)
            minimum_midpoint_label = {"kind": "base", "base_index": base_index}
        checked_base += 1

    # The old pool contains 6,101 fractional single-open-path grid columns.
    # Use the independently self-tested active-block minor aggregation.
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
            score = base.block_score(
                block, length, second_coefficients, entries
            )
            gap = grid_target - score
            if not gap > grid_floor:
                raise RuntimeError(
                    f"fractional column L={length}, alpha={alpha_fraction} "
                    f"does not have a certified gap > 1/5: {gap}"
                )
            lower = gap.lower()
            label = {
                "kind": "fractional",
                "length": length,
                "alpha": str(alpha_fraction),
            }
            if minimum_lower is None or lower < minimum_lower:
                minimum_lower = lower
                minimum_lower_label = label
            if minimum_interval is None or float(gap) < minimum_midpoint:
                minimum_interval = str(gap)
                minimum_midpoint = float(gap)
                minimum_midpoint_label = label
            checked_grid += 1

    if checked_base != 22 or checked_grid != 6101:
        raise RuntimeError(
            f"wrong parent-pool counts: base={checked_base}, grid={checked_grid}"
        )

    # Independently rebuild the appended connected path from its exact decimal
    # rational couplings and evaluate the new dual on the full 42x42 rotation.
    appended = diagnostic["appended_column_label"]
    if appended.get("kind") != "general_gapped":
        raise RuntimeError("the appended column is not labelled general_gapped")
    decimal_couplings = [Fraction(value) for value in appended["couplings_exact_decimal"]]
    certified_couplings = [
        Fraction(value)
        for value in gapped_certificate["candidate_results"]["connected"][
            "couplings_exact_rational"
        ]
    ]
    if decimal_couplings != certified_couplings:
        raise RuntimeError("appended couplings disagree with the independent Arb witness")
    if len(decimal_couplings) != 42 or decimal_couplings[-1] != 0:
        raise RuntimeError("appended connected path has the wrong edge layout")
    if any(value <= 0 for value in decimal_couplings[:-1]):
        raise RuntimeError("appended connected path is not strictly positive internally")
    if gapped_certificate["candidate_results"]["connected"]["internal_zero_edges"] != []:
        raise RuntimeError("the pinned connected witness unexpectedly has an internal cut")

    gapped_atom = {
        "kind": "gapped",
        "couplings": [str(value) for value in decimal_couplings],
    }
    ctx.prec = BASE_PRECISION_BITS
    gapped_rotation = build_rotation(gapped_atom)
    gapped_score = base.full_score(gapped_rotation, system, coefficients)
    gapped_gap = target - gapped_score
    if not gapped_gap > rational(SEPARATION_FLOOR):
        raise RuntimeError(f"appended general-gapped column gap is not > 1/5: {gapped_gap}")
    lower = gapped_gap.lower()
    if minimum_lower is None or lower < minimum_lower:
        minimum_lower = lower
        minimum_lower_label = {"kind": "general_gapped", "column_index": 6123}
    if minimum_interval is None or float(gapped_gap) < minimum_midpoint:
        minimum_interval = str(gapped_gap)
        minimum_midpoint = float(gapped_gap)
        minimum_midpoint_label = {"kind": "general_gapped", "column_index": 6123}

    checked = checked_base + checked_grid + 1
    if checked != 6124:
        raise RuntimeError(f"checked {checked} columns instead of 6,124")
    if minimum_lower is None or not minimum_lower > rational(SEPARATION_FLOOR):
        raise RuntimeError("the common strict 1/5 column-gap margin was not certified")

    result = {
        "status": "arb_certified_finite_6124_column_full_fourth_plus_general_gapped_separator",
        "complete": True,
        "precision_bits_base_and_gapped": BASE_PRECISION_BITS,
        "precision_bits_fractional_grid": GRID_PRECISION_BITS,
        "interval_backend": "python-flint / Arb",
        "diagnostic_sha256": diagnostic_sha,
        "old_diagnostic_sha256": old_diagnostic_sha,
        "old_finite_certificate_sha256": old_certificate_sha,
        "warm_certificate_sha256": warm_sha,
        "gapped_search_sha256": search_sha,
        "gapped_arb_certificate_sha256": gapped_certificate_sha,
        "candidate_count": checked,
        "base_atom_count": checked_base,
        "fractional_grid_count": checked_grid,
        "general_gapped_count": 1,
        "fourth_orbit_count": len(system.keys),
        "quartet_count": len(system.indices),
        "independent_moment_rows": 1313,
        "equalities_including_normalization": 1314,
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
        "minimum_column_gap_lower_endpoint": str(minimum_lower),
        "minimum_gap_lower_endpoint_candidate": minimum_lower_label,
        "minimum_gap_interval_by_midpoint_selection": minimum_interval,
        "minimum_gap_candidate_by_midpoint": minimum_midpoint_label,
        "appended_general_gapped_gap_interval": str(gapped_gap),
        "block_pricing_self_test": block_test,
        "proof": (
            "Let D be diagonal with entries 41 on the 21 second-moment "
            "coordinates and 533 on the 1,440 fourth-order orbit coordinates. "
            "The exact rationalized dual y is normalized so ||D^{-1}y||_1=1. "
            "Arb certifies y^T(b-a_j)>1/5 for every one of the 6,124 listed "
            "physical columns. Hence for every probability vector p on this "
            "finite pool, y^T(b-Ap)>1/5. Since ||y||_1<=533, Holder's inequality "
            "gives ||b-Ap||_infinity>1/2665."
        ),
        "scope": (
            "This is a rigorous finite-pool obstruction for exactly 22 pinned "
            "base atoms, 6,101 fractional single-open-path grid atoms, and one "
            "specified connected nonuniform gapped open path. It does not cover "
            "other nonuniform gapped couplings, the continuous gapped family, "
            "multi-segment paths outside the listed atoms, all even principal "
            "minors, or an operational Choi/diamond-distance guarantee."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_count": checked,
        "base_atom_count": checked_base,
        "fractional_grid_count": checked_grid,
        "general_gapped_count": 1,
        "target_score_interval": result["target_score_interval"],
        "certified_common_column_gap_lower_bound": "1/5",
        "minimum_column_gap_lower_endpoint": str(minimum_lower),
        "appended_general_gapped_gap_interval": str(gapped_gap),
        "dual_full_coordinate_l1_exact": str(full_l1),
        "moment_residual_infinity_lower_bound": "1/2665",
        "diagnostic_sha256": diagnostic_sha,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
