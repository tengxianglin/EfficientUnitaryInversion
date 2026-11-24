"""128-bit Arb verification of the 6,123-column full-fourth finite-grid separator.

# The corresponding workflow is path-triggered by this verifier and its frozen inputs.

The floating LP only discovers a rational candidate separator. This verifier
reconstructs its coefficients as exact decimal rationals and checks, with Arb,
that its score on every listed physical column is strictly below its exact
score on the target moment vector. The result is a finite-grid obstruction
only; it does not cover continuous alpha or arbitrary gapped couplings.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from ising_fourth_moments import FourthMoments
from verify_ising_low_moment_design import build_rotation, probe, rational

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
WARM_CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_fractional_grid_dual_arb_n21.json"
N = 42
PRECISION_BITS = 128
SEPARATION_FLOOR = Fraction(1, 4)


def fractional_block(length, alpha):
    """Exact Arb exponential on the active open path."""
    generator = arb_mat(length, length)
    for j in range(length - 1):
        coupling = alpha * arb.pi() / 4 * arb((j + 1) * (length - j - 1)).sqrt()
        generator[j, j + 1] = 2 * coupling
        generator[j + 1, j] = -2 * coupling
    return generator.exp()


def block_second_moments(block, length):
    diagonal = [block[i, i] if i < length else arb(1) for i in range(N)]
    moments = []
    for distance in range(1, 22):
        total = arb(0)
        for i in range(N):
            j = (i + distance) % N
            if i < length and j < length:
                off_diagonal_product = block[i, j] * block[j, i]
            else:
                off_diagonal_product = arb(0)
            total += diagonal[i] * diagonal[j] - off_diagonal_product
        moments.append(total / N)
    return moments


def full_second_moments(rotation):
    diagonal = [rotation[i, i] for i in range(N)]
    moments = []
    for distance in range(1, 22):
        total = arb(0)
        for i in range(N):
            j = (i + distance) % N
            total += (
                diagonal[i] * diagonal[j]
                - rotation[i, j] * rotation[j, i]
            )
        moments.append(total / N)
    return moments


def block_minor(block, indices):
    if not indices:
        return arb(1)
    if len(indices) == 1:
        return block[indices[0], indices[0]]
    return arb_mat(
        [[block[i, j] for j in indices] for i in indices]
    ).det()


def build_mask_weights(system, coefficient_by_feature):
    """Collapse selected orbit averages to weighted active-block minors."""
    coefficient_by_orbit = {
        feature_index - 21: coefficient
        for feature_index, coefficient in coefficient_by_feature.items()
        if feature_index >= 21
    }
    result = {}
    for length in range(2, N + 1):
        weights = {}
        for quartet, raw_orbit_id in zip(system.indices, system.ids):
            orbit_id = int(raw_orbit_id)
            coefficient = coefficient_by_orbit.get(orbit_id)
            if coefficient is None:
                continue
            mask = 0
            for raw_index in quartet:
                index = int(raw_index)
                if index < length:
                    mask |= 1 << index
            contribution = coefficient / int(system.counts[orbit_id])
            weights[mask] = weights.get(mask, Fraction(0)) + contribution
        entries = []
        for mask, weight in sorted(weights.items()):
            if not weight:
                continue
            indices = tuple(i for i in range(length) if (mask >> i) & 1)
            entries.append((rational(weight), indices))
        result[length] = entries
    return result


def block_score(block, length, second_coefficients, fourth_entries):
    second = block_second_moments(block, length)
    score = sum(
        (second_coefficients[d] * second[d] for d in range(21)),
        arb(0),
    )
    for weight, indices in fourth_entries:
        score += weight * block_minor(block, indices)
    return score


def full_score(rotation, system, coefficient_by_feature):
    second = full_second_moments(rotation)
    score = sum(
        (rational(coefficient_by_feature.get(d, Fraction(0))) * second[d]
         for d in range(21)),
        arb(0),
    )
    for feature_index, coefficient in coefficient_by_feature.items():
        if feature_index >= 21:
            orbit_id = feature_index - 21
            score += rational(coefficient) * probe(
                rotation, list(system.representatives[orbit_id])
            )
    return score


def self_test(system, coefficient_by_feature, second_coefficients, mask_weights):
    cases = []
    for length, alpha_fraction in (
        (2, Fraction(17, 100)),
        (7, Fraction(43, 100)),
        (21, Fraction(89, 100)),
        (41, Fraction(117, 100)),
        (42, Fraction(83, 100)),
    ):
        alpha = rational(alpha_fraction)
        block = fractional_block(length, alpha)
        score_fast = block_score(
            block, length, second_coefficients, mask_weights[length]
        )
        rotation = arb_mat(N, N)
        for i in range(N):
            rotation[i, i] = 1
        for i in range(length):
            for j in range(length):
                rotation[i, j] = block[i, j]
        score_direct = full_score(rotation, system, coefficient_by_feature)
        defect = score_fast - score_direct
        if not defect.contains(0):
            raise RuntimeError(
                f"block pricing self-test failed at L={length}, alpha={alpha_fraction}: {defect}"
            )
        cases.append({
            "length": length,
            "alpha": str(alpha_fraction),
            "score_difference_interval": str(defect),
        })
    return {"cases": cases, "passed": len(cases)}


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    diagnostic_sha = hashlib.sha256(diagnostic_raw).hexdigest()
    diagnostic = json.loads(diagnostic_raw)
    warm_raw = WARM_CERT.read_bytes()
    warm_sha = hashlib.sha256(warm_raw).hexdigest()
    warm = json.loads(warm_raw)

    if diagnostic.get("status") != "floating_finite_grid_separator_candidate_not_arb_certified":
        raise RuntimeError("unexpected floating separator diagnostic status")
    if diagnostic.get("candidate_count") != 6123:
        raise RuntimeError("unexpected finite-grid candidate count")
    if diagnostic.get("fourth_orbit_count") != 1440:
        raise RuntimeError("unexpected fourth-order orbit count")
    if diagnostic.get("reduced_equations_including_normalization") != 1314:
        raise RuntimeError("unexpected reduced equality-system size")
    if diagnostic.get("warm_certificate_sha256") != warm_sha:
        raise RuntimeError("diagnostic does not pin the 41-atom warm certificate")
    if len(warm.get("atoms", [])) != 41:
        raise RuntimeError("the pinned warm certificate is not the 41-atom witness")

    system = FourthMoments(21)
    coefficient_by_feature = {}
    for item in diagnostic["dual"]["nonzero_coefficients"]:
        index = int(item["feature_index"])
        if index in coefficient_by_feature:
            raise RuntimeError(f"duplicate dual feature index {index}")
        coefficient_by_feature[index] = Fraction(item["coefficient"])
    if len(coefficient_by_feature) != 80:
        raise RuntimeError("expected the frozen 80-term rational separator")
    reduced_feature_indices = set(system.reduced_indices())
    if not set(coefficient_by_feature).issubset(reduced_feature_indices):
        raise RuntimeError("separator uses a feature outside the pinned reduced equality system")
    if any(index < 0 or index >= 1461 for index in coefficient_by_feature):
        raise RuntimeError("dual coefficient feature index is out of range")

    second_coefficients = [
        rational(coefficient_by_feature.get(d, Fraction(0)))
        for d in range(21)
    ]
    mask_weights = build_mask_weights(system, coefficient_by_feature)
    test = self_test(
        system, coefficient_by_feature, second_coefficients, mask_weights
    )

    target_score = sum(
        (
            rational(coefficient_by_feature[index])
            * rational(system.rational_target[index])
            for index in coefficient_by_feature
        ),
        arb(0),
    )

    minimum_gap = None
    minimum_label = None
    checked = 0
    base_atoms = warm["atoms"][:22]
    for base_index, atom in enumerate(base_atoms):
        rotation = build_rotation(atom)
        score = full_score(rotation, system, coefficient_by_feature)
        gap = target_score - score
        if not gap > rational(SEPARATION_FLOOR):
            raise RuntimeError(
                f"separator margin is not above 1/4 on base atom {base_index}: gap={gap}"
            )
        if minimum_gap is None or float(gap) < float(minimum_gap):
            minimum_gap = gap
            minimum_label = {"kind": "base", "base_index": base_index}
        checked += 1

    for length in range(2, N + 1):
        max_k = 100 if (length % 2 == 1 or length == N) else 200
        entries = mask_weights[length]
        for k in range(max_k + 1):
            if k == 0 and length != 2:
                continue
            alpha_fraction = Fraction(k, 100)
            block = fractional_block(length, rational(alpha_fraction))
            score = block_score(
                block, length, second_coefficients, entries
            )
            gap = target_score - score
            if not gap > rational(SEPARATION_FLOOR):
                raise RuntimeError(
                    f"separator margin is not above 1/4 at L={length}, alpha={alpha_fraction}: gap={gap}"
                )
            if minimum_gap is None or float(gap) < float(minimum_gap):
                minimum_gap = gap
                minimum_label = {
                    "kind": "fractional",
                    "length": length,
                    "alpha": str(alpha_fraction),
                }
            checked += 1

    if checked != 6123:
        raise RuntimeError(f"checked {checked} columns instead of 6123")
    if not minimum_gap > rational(SEPARATION_FLOOR):
        raise RuntimeError("the selected smallest candidate gap is not above 1/4")

    result = {
        "status": "arb_certified_finite_6123_column_full_fourth_separator",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "diagnostic_sha256": diagnostic_sha,
        "warm_certificate_sha256": warm_sha,
        "candidate_count": checked,
        "base_atom_count": len(base_atoms),
        "fractional_candidate_count": checked - len(base_atoms),
        "fourth_orbit_count": len(system.keys),
        "quartet_count": len(system.indices),
        "independent_moment_rows": 1313,
        "equalities_including_normalization": 1314,
        "dual_nonzero_coefficients": len(coefficient_by_feature),
        "dual_coefficients_exact_decimal_rationals": [
            {"feature_index": index, "coefficient": str(value)}
            for index, value in sorted(coefficient_by_feature.items())
        ],
        "target_score_interval": str(target_score),
        "certified_common_gap_lower_bound": "1/4",
        "smallest_gap_candidate_interval_by_midpoint_selection": str(minimum_gap),
        "smallest_gap_candidate_by_midpoint": minimum_label,
        "block_pricing_self_test": test,
        "proof": (
            "Let a_j be each of the 6,123 candidate feature columns restricted "
            "to the 1,313 independent moment rows, and let b be the corresponding "
            "exact target. The frozen rational vector y satisfies y^T b > "
            "y^T a_j for every candidate j, as independently enclosed by Arb. "
            "For any probability vector p on this finite pool, "
            "y^T b - y^T a_j > 1/4 for every candidate j. For any "
            "probability vector p on this finite pool, "
            "y^T b - y^T(sum_j p_j a_j) > 1/4, contradicting the required "
            "moment equations. Hence the exact finite pool is infeasible "
            "with a certified common separation margin greater than 1/4."
        ),
        "scope": (
            "This is a rigorous obstruction for exactly the 22 pinned base "
            "atoms plus the corrected 6,101-column fractional single-open-path "
            "grid. It does not cover continuous alpha between grid points, "
            "arbitrary gapped couplings, multi-segment paths outside the grid, "
            "or the full continuous physical family. It is not an operational "
            "Choi/diamond-distance bound."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        key: result[key] for key in (
            "status", "candidate_count", "dual_nonzero_coefficients",
            "target_score_interval", "minimum_candidate_gap_interval",
            "minimum_gap_candidate_by_midpoint", "block_pricing_self_test",
            "diagnostic_sha256", "warm_certificate_sha256",
        )
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
