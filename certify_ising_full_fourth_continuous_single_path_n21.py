"""Global continuous-alpha certificate for the n=21 full-fourth separator.

For each active open-path length L, every score term is a principal minor of
R_L(alpha) on an active subset of size r<=4.  Exterior powers show that the
score is an even trigonometric polynomial of a rigorously bounded degree.
An exact-size DFT (with Arb-enclosed samples) reconstructs its cosine
coefficients, and adaptive Bernstein subdivision certifies target-score
positivity on the whole x=cos(theta) interval [-1,1].

This is a continuum theorem for the one-parameter single-open-path family
for every real scale alpha.  The 22 pinned base atoms are checked separately
at 512-bit Arb.  It does not cover arbitrary nonuniform gapped couplings or
multi-segment paths.
"""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from ising_fourth_moments import FourthMoments
from verify_ising_full_fourth_fractional_grid_dual_arb import (
    block_score,
    build_mask_weights,
    fractional_block,
    full_score,
)
from verify_ising_low_moment_design import build_rotation, rational

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
FINITE_CERT = ROOT / "evidence/ising_full_fourth_fractional_grid_dual_arb_n21.json"
WARM_CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_continuous_single_path_n21.json"
PRECISION_BITS = 512
MAX_BERNSTEIN_DEPTH = 18
MAX_BERNSTEIN_NODES_PER_LENGTH = 100000


def degree_and_parameterization(length):
    """Return (degree, period, theta_scale, active_orders, mode).

    theta = pi*alpha for odd L and for the full L=42 block, whose even
    minors have period 2 in alpha.  For even L<42, idle identity sites allow
    odd active-subset orders, hence half-integer spin frequencies; use
    theta = pi*alpha/2 and period 4 in alpha instead.
    """
    j = Fraction(length - 1, 2)
    if length == 42:
        orders = (2, 4)
        max_frequency = max(
            Fraction(r) * j - Fraction(r * (r - 1), 2) for r in orders
        )
        if max_frequency.denominator != 1:
            raise RuntimeError("full even-order block has a nonintegral frequency")
        return int(max_frequency), Fraction(2), Fraction(1), orders, "period-2"
    orders = tuple(range(min(4, length) + 1))
    max_frequency = max(
        Fraction(r) * j - Fraction(r * (r - 1), 2) for r in orders
    )
    if length % 2:
        if max_frequency.denominator != 1:
            raise RuntimeError("integer-spin path produced a half-integer frequency")
        return int(max_frequency), Fraction(2), Fraction(1), orders, "period-2"
    doubled = 2 * max_frequency
    if doubled.denominator != 1:
        raise RuntimeError("twice the half-integer-spin frequency is not integral")
    return int(doubled), Fraction(4), Fraction(1, 2), orders, "period-4"


def cosine_coefficients(scores):
    """Exact-size DFT for an even real trigonometric polynomial."""
    count = len(scores)
    degree = (count - 1) // 2
    result = []
    for k in range(degree + 1):
        total = arb(0)
        for j, score in enumerate(scores):
            angle = rational(Fraction(2 * k * j, count)) * arb.pi()
            total += score * angle.cos()
        result.append(total / count)
    return result


def chebyshev_power_coefficients(degree):
    """Coefficients of T_k(2u-1), in ascending powers of u."""
    if degree == 0:
        return [[arb(1)]]
    polynomials = [[arb(1)], [arb(-1), arb(2)]]
    for k in range(1, degree):
        current = polynomials[k]
        previous = polynomials[k - 1]
        nxt = [arb(0) for _ in range(k + 2)]
        for i, value in enumerate(current):
            nxt[i] -= 2 * value
            nxt[i + 1] += 4 * value
        for i, value in enumerate(previous):
            nxt[i] -= value
        polynomials.append(nxt)
    return polynomials


def gap_power_polynomial(target, coefficients):
    """Return g(u)=target-S(alpha), where x=2u-1=cos(theta)."""
    degree = len(coefficients) - 1
    chebyshev = chebyshev_power_coefficients(degree)
    power = [arb(0) for _ in range(degree + 1)]
    power[0] = target - coefficients[0]
    for k in range(1, degree + 1):
        factor = 2 * coefficients[k]
        for j, value in enumerate(chebyshev[k]):
            power[j] -= factor * value
    return power


def power_to_bernstein(power):
    """Convert ascending power coefficients on [0,1] to degree-n Bernstein."""
    degree = len(power) - 1
    result = []
    for i in range(degree + 1):
        value = arb(0)
        for j in range(i + 1):
            ratio = rational(Fraction(math.comb(i, j), math.comb(degree, j)))
            value += power[j] * ratio
        result.append(value)
    return result


def split_bernstein(coefficients):
    """de Casteljau split at t=1/2."""
    degree = len(coefficients) - 1
    work = list(coefficients)
    left = [work[0]]
    right = [None] * (degree + 1)
    right[degree] = work[-1]
    half = rational(Fraction(1, 2))
    for level in range(1, degree + 1):
        work = [(work[i] + work[i + 1]) * half
                for i in range(len(work) - 1)]
        left.append(work[0])
        right[degree - level] = work[-1]
    return left, right


def certify_bernstein(coefficients):
    """Certify positivity, find a negative point, or return an honest timeout."""
    minimum_lower = None
    stats = {
        "nodes": 0,
        "positive_leaves": 0,
        "unresolved_leaves": 0,
        "max_depth_reached": 0,
        "minimum_bernstein_lower_endpoint": None,
        "negative_point": None,
        "negative_interval": None,
        "unresolved_examples": [],
    }

    def recurse(values, left, right, depth):
        nonlocal minimum_lower
        stats["nodes"] += 1
        stats["max_depth_reached"] = max(stats["max_depth_reached"], depth)
        lower_positive = all(value.lower() > 0 for value in values)
        if lower_positive:
            stats["positive_leaves"] += 1
            leaf_lower = min(value.lower() for value in values)
            if minimum_lower is None or leaf_lower < minimum_lower:
                minimum_lower = leaf_lower
            return "positive"

        upper_negative = all(value.upper() < 0 for value in values)
        if upper_negative:
            stats["negative_interval"] = {
                "u_lower": str(left),
                "u_upper": str(right),
                "gap_bernstein_hull": [str(min(v.lower() for v in values)),
                                       str(max(v.upper() for v in values))],
            }
            return "negative"

        degree = len(values) - 1
        midpoint_value = arb(0)
        denominator = 1 << degree
        for i, value in enumerate(values):
            midpoint_value += value * rational(
                Fraction(math.comb(degree, i), denominator)
            )
        midpoint = (left + right) / 2
        if midpoint_value.upper() < 0:
            stats["negative_point"] = {
                "u": str(midpoint),
                "x=2u-1": str(2 * midpoint - 1),
                "gap_interval": str(midpoint_value),
                "alpha_expression": (
                    "acos(2u-1)/pi" if MODE_THETA_SCALE == 1
                    else "2*acos(2u-1)/pi"
                ),
            }
            return "negative"

        if depth >= MAX_BERNSTEIN_DEPTH or stats["nodes"] >= MAX_BERNSTEIN_NODES_PER_LENGTH:
            stats["unresolved_leaves"] += 1
            if len(stats["unresolved_examples"]) < 8:
                stats["unresolved_examples"].append({
                    "u_lower": str(left),
                    "u_upper": str(right),
                    "depth": depth,
                    "coefficient_lower_min": str(min(v.lower() for v in values)),
                })
            return "inconclusive"

        first, second = split_bernstein(values)
        first_status = recurse(first, left, midpoint, depth + 1)
        if first_status == "negative":
            return "negative"
        second_status = recurse(second, midpoint, right, depth + 1)
        if second_status == "negative":
            return "negative"
        if first_status == "positive" and second_status == "positive":
            return "positive"
        return "inconclusive"

    # The alpha-expression map depends only on the current length's parameterization.
    global MODE_THETA_SCALE
    status = recurse(coefficients, Fraction(0), Fraction(1), 0)
    stats["minimum_bernstein_lower_endpoint"] = (
        str(minimum_lower) if minimum_lower is not None else None
    )
    stats["status"] = status
    return stats


def evaluate_power(power, value):
    result = arb(0)
    for coefficient in reversed(power):
        result = result * value + coefficient
    return result


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    diagnostic = json.loads(diagnostic_raw)
    finite_raw = FINITE_CERT.read_bytes()
    finite_certificate = json.loads(finite_raw)
    warm_raw = WARM_CERT.read_bytes()
    warm = json.loads(warm_raw)

    diagnostic_sha = hashlib.sha256(diagnostic_raw).hexdigest()
    warm_sha = hashlib.sha256(warm_raw).hexdigest()
    if diagnostic.get("status") != "floating_finite_grid_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected frozen discovery diagnostic status")
    if diagnostic.get("candidate_count") != 6123 or diagnostic.get("fourth_orbit_count") != 1440:
        raise RuntimeError("unexpected finite-grid dimensions")
    if finite_certificate.get("status") != "arb_certified_finite_6123_column_full_fourth_separator":
        raise RuntimeError("the finite-grid Arb certificate is missing or stale")
    if not finite_certificate.get("complete"):
        raise RuntimeError("finite-grid Arb certificate is incomplete")
    if finite_certificate.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("finite-grid certificate does not pin the current diagnostic")
    if diagnostic.get("warm_certificate_sha256") != warm_sha:
        raise RuntimeError("discovery diagnostic does not pin the 41-atom warm certificate")
    if len(warm.get("atoms", [])) != 41:
        raise RuntimeError("expected the frozen 41-atom warm certificate")

    coefficient_by_feature = {
        int(item["feature_index"]): Fraction(item["coefficient"])
        for item in diagnostic["dual"]["nonzero_coefficients"]
    }
    if len(coefficient_by_feature) != 80:
        raise RuntimeError("expected the frozen 80-term separator")

    system = FourthMoments(21)
    if not set(coefficient_by_feature).issubset(set(system.reduced_indices())):
        raise RuntimeError("dual support is outside the exact reduced moment system")

    second_coefficients = [
        rational(coefficient_by_feature.get(d, Fraction(0)))
        for d in range(21)
    ]
    mask_weights = build_mask_weights(system, coefficient_by_feature)
    target_score = sum(
        (rational(coefficient_by_feature[index])
         * rational(system.rational_target[index])
         for index in coefficient_by_feature),
        arb(0),
    )

    # Recheck the 22 pinned non-path atoms at 512 bits. This makes the final
    # continuous-family margin independent of the finite-grid verifier's
    # lower-precision fractional-grid pass.
    base_gaps = []
    base_labels = []
    for base_index, atom in enumerate(warm["atoms"][:22]):
        if atom["kind"] == "fractional":
            length = int(atom["length"])
            block = fractional_block(length, rational(Fraction(atom["alpha"])))
            score = block_score(
                block, length, second_coefficients, mask_weights[length]
            )
        else:
            rotation = build_rotation(atom)
            score = full_score(rotation, system, coefficient_by_feature)
        gap = target_score - score
        if not gap.lower() > 0:
            raise RuntimeError(
                f"pinned base atom {base_index} is not strictly separated: {gap}"
            )
        base_gaps.append(gap.lower())
        base_labels.append({"base_index": base_index, "gap_interval": str(gap)})

    path_results = []
    global_lower = min(base_gaps)
    global_negative = None
    all_paths_certified = True

    for length in range(2, 43):
        degree, period, theta_scale, orders, mode = degree_and_parameterization(length)
        sample_count = 2 * degree + 1
        if sample_count < 1:
            raise RuntimeError("invalid Fourier sample count")
        scores = []
        for sample_index in range(sample_count):
            alpha = period * Fraction(sample_index, sample_count)
            block = fractional_block(length, rational(alpha))
            scores.append(block_score(
                block, length, second_coefficients, mask_weights[length]
            ))

        # Exact DFT recovery: the exterior-power frequency bound is <= degree,
        # and sample_count=2*degree+1 prevents aliasing.
        coefficients = cosine_coefficients(scores)

        # Independent checks of evenness and the exact DFT reconstruction.
        symmetry_defects = []
        reconstruction_defects = []
        for sample_index, score in enumerate(scores):
            reflected = scores[(-sample_index) % sample_count]
            symmetry_defects.append(score - reflected)
            theta = rational(Fraction(2 * sample_index, sample_count)) * arb.pi()
            reconstructed = coefficients[0]
            for k in range(1, degree + 1):
                reconstructed += 2 * coefficients[k] * (k * theta).cos()
            reconstruction_defects.append(reconstructed - score)
        if any(not defect.contains(0) for defect in symmetry_defects):
            raise RuntimeError(f"evenness check failed at L={length}")
        if any(not defect.contains(0) for defect in reconstruction_defects):
            raise RuntimeError(f"DFT reconstruction check failed at L={length}")

        power = gap_power_polynomial(target_score, coefficients)
        bernstein = power_to_bernstein(power)

        global MODE_THETA_SCALE
        MODE_THETA_SCALE = theta_scale
        proof = certify_bernstein(bernstein)

        # The Bernstein polynomial is a global identity in x=cos(theta), so
        # test both negative and out-of-fundamental-interval alpha values.
        test_alphas = (
            Fraction(-7, 13),
            Fraction(7, 13),
            Fraction(13, 5),
            Fraction(23, 5),
        )
        off_grid_checks = []
        for test_alpha in test_alphas:
            test_theta = rational(test_alpha) * arb.pi() * rational(theta_scale)
            x = test_theta.cos()
            u = (x + 1) / 2
            polynomial_score_gap = evaluate_power(power, u)
            test_block = fractional_block(length, rational(test_alpha))
            direct_score = block_score(
                test_block, length, second_coefficients, mask_weights[length]
            )
            direct_gap = target_score - direct_score
            point_defect = polynomial_score_gap - direct_gap
            if not point_defect.contains(0):
                raise RuntimeError(
                    f"off-grid Fourier polynomial check failed at L={length}, "
                    f"alpha={test_alpha}: {point_defect}"
                )
            off_grid_checks.append({
                "alpha": str(test_alpha),
                "direct_gap_interval": str(direct_gap),
                "polynomial_defect": str(point_defect),
            })
        reference_check = next(
            item for item in off_grid_checks if item["alpha"] == "7/13"
        )

        certified = proof["status"] == "positive"
        if certified:
            lower = proof["minimum_bernstein_lower_endpoint"]
            lower_value = arb(lower)
            if not lower_value > 0:
                raise RuntimeError(f"nonpositive certified lower bound at L={length}")
            if lower_value < global_lower:
                global_lower = lower_value
        else:
            all_paths_certified = False
            if proof["status"] == "negative" and global_negative is None:
                global_negative = {
                    "length": length,
                    "mode": mode,
                    "degree": degree,
                    "negative_point": proof["negative_point"],
                    "negative_interval": proof["negative_interval"],
                }

        path_results.append({
            "length": length,
            "mode": mode,
            "period_in_alpha": str(period),
            "theta_scale": str(theta_scale),
            "active_orders_in_degree_bound": list(orders),
            "degree_bound": degree,
            "fourier_sample_count": sample_count,
            "symmetry_checks": len(symmetry_defects),
            "dft_reconstruction_checks": len(reconstruction_defects),
            "off_grid_test_alphas": [item["alpha"] for item in off_grid_checks],
            "off_grid_checks": off_grid_checks,
            "off_grid_test_alpha": "7/13",
            "off_grid_gap_interval": reference_check["direct_gap_interval"],
            "off_grid_polynomial_defect": reference_check["polynomial_defect"],
            "bernstein": proof,
            "certified_for_all_real_alpha": certified,
            "certified_for_all_alpha_0_to_2": certified,
        })
        print(json.dumps({
            "length": length,
            "degree": degree,
            "samples": sample_count,
            "status": proof["status"],
            "nodes": proof["nodes"],
            "minimum_lower": proof["minimum_bernstein_lower_endpoint"],
        }), flush=True)
        if global_negative is not None:
            break

    complete = all_paths_certified and len(path_results) == 41
    result = {
        "status": (
            "arb_certified_continuous_single_open_path_separator"
            if complete
            else "certified_continuous_single_path_escape"
            if global_negative is not None
            else "continuous_single_path_fourier_bernstein_inconclusive"
        ),
        "complete": complete,
        "precision_bits": PRECISION_BITS,
        "interval_backend": "python-flint / Arb; exact-size DFT plus adaptive Bernstein subdivision",
        "diagnostic_sha256": diagnostic_sha,
        "finite_grid_certificate_sha256": hashlib.sha256(finite_raw).hexdigest(),
        "warm_certificate_sha256": warm_sha,
        "target_score_interval": str(target_score),
        "base_atom_count": len(base_gaps),
        "base_atom_minimum_gap_lower_endpoint": str(min(base_gaps)),
        "continuous_path_length_count": len(path_results),
        "total_fourier_samples": sum(item["fourier_sample_count"] for item in path_results),
        "global_certified_gap_lower_endpoint": str(global_lower) if complete else None,
        "global_negative_witness": global_negative,
        "path_results": path_results,
        "proof_scope": (
            "If complete, the same frozen separator strictly separates the exact "
            "second-/fourth-order target from every probability mixture supported "
            "on the 22 pinned base atoms together with every single-open-path seed "
            "R_{L,alpha} for L=2,...,42 and all real alpha. It does not cover "
            "arbitrary nonuniform gapped couplings, multi-segment paths, or the "
            "full continuous physical family."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "complete": result["complete"],
        "continuous_path_length_count": result["continuous_path_length_count"],
        "total_fourier_samples": result["total_fourier_samples"],
        "base_atom_minimum_gap_lower_endpoint": result["base_atom_minimum_gap_lower_endpoint"],
        "global_certified_gap_lower_endpoint": result["global_certified_gap_lower_endpoint"],
        "global_negative_witness": result["global_negative_witness"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
