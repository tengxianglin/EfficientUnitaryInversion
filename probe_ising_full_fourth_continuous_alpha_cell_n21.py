"""Arb interval probe for extending the n=21 finite-grid separator to a continuum cell.

This first decisive probe encloses the full separator score over the Voronoi
cell around the currently worst grid point (L=40, alpha=46/25). It is a
continuum statement for this one cell only if the interval lower gap exceeds
1/4. An inconclusive enclosure is not evidence of a counterexample.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from ising_fourth_moments import FourthMoments
from verify_ising_full_fourth_fractional_grid_dual_arb import (
    block_score,
    build_mask_weights,
    fractional_block,
)
from verify_ising_low_moment_design import rational

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
WARM_CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_continuous_alpha_cell_probe_n21.json"
PRECISION_BITS = 128  # pinned interval precision for reproducibility


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    diagnostic = json.loads(diagnostic_raw)
    warm_raw = WARM_CERT.read_bytes()
    warm = json.loads(warm_raw)

    if hashlib.sha256(warm_raw).hexdigest() != diagnostic["warm_certificate_sha256"]:
        raise RuntimeError("warm certificate hash does not match frozen diagnostic")
    if diagnostic["status"] != "floating_finite_grid_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected diagnostic status")

    coefficient_by_feature = {
        int(item["feature_index"]): Fraction(item["coefficient"])
        for item in diagnostic["dual"]["nonzero_coefficients"]
    }
    if len(coefficient_by_feature) != 80:
        raise RuntimeError("expected the frozen 80-term separator")

    system = FourthMoments(21)
    if not set(coefficient_by_feature).issubset(set(system.reduced_indices())):
        raise RuntimeError("separator support is outside the pinned reduced system")

    second_coefficients = [
        rational(coefficient_by_feature.get(d, Fraction(0)))
        for d in range(21)
    ]
    mask_weights = build_mask_weights(system, coefficient_by_feature)
    target_score = sum(
        (
            rational(coefficient_by_feature[index])
            * rational(system.rational_target[index])
            for index in coefficient_by_feature
        ),
        arb(0),
    )

    # Exact decimal interval [1.835, 1.845], centered at alpha=46/25.
    alpha_interval = arb("1.84 +/- 0.005")
    length = 40
    interval_block = fractional_block(length, alpha_interval)
    interval_score = block_score(
        interval_block,
        length,
        second_coefficients,
        mask_weights[length],
    )
    interval_gap = target_score - interval_score

    point_block = fractional_block(length, rational(Fraction(46, 25)))
    point_score = block_score(
        point_block,
        length,
        second_coefficients,
        mask_weights[length],
    )
    point_gap = target_score - point_score
    floor = rational(Fraction(1, 4))
    certified = interval_gap.lower() > floor

    result = {
        "status": (
            "arb_certified_continuous_alpha_cell_gap_gt_1_over_4"
            if certified
            else "continuous_alpha_cell_interval_inconclusive"
        ),
        "complete_for_declared_cell": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb interval matrix exponential",
        "diagnostic_sha256": hashlib.sha256(diagnostic_raw).hexdigest(),
        "warm_certificate_sha256": hashlib.sha256(warm_raw).hexdigest(),
        "length": length,
        "alpha_interval": str(alpha_interval),
        "alpha_interval_lower": str(alpha_interval.lower()),
        "alpha_interval_upper": str(alpha_interval.upper()),
        "target_score_interval": str(target_score),
        "score_interval_over_entire_alpha_cell": str(interval_score),
        "gap_interval_over_entire_alpha_cell": str(interval_gap),
        "gap_lower_endpoint": str(interval_gap.lower()),
        "gap_upper_endpoint": str(interval_gap.upper()),
        "required_strict_floor": "1/4",
        "midpoint_alpha": "46/25",
        "midpoint_gap_interval": str(point_gap),
        "strictly_above_floor_over_entire_cell": bool(certified),
        "scope": (
            "If certified, every alpha in [1.835,1.845] for the L=40 "
            "single-open-path family has separator gap strictly greater "
            "than 1/4. This is only one continuum cell; it does not cover "
            "other path lengths, other alpha cells, multi-segment paths, "
            "arbitrary gapped couplings, or the full physical family."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
