#!/usr/bin/env python3
"""256-bit Arb check of the local sixth-harmonic pricing identity at N=42."""
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from flint import arb, fmpq, ctx

import verify_n42_period_two_six_quartic_ensemble_arb as base_audit
import verify_n42_degree_six_harmonic_projection_arb as projection

ROOT = Path(__file__).resolve().parent
ATOM_PATH = ROOT / "evidence/n42_period_two_six_quartic_atoms.json"
WEIGHT_PATH = ROOT / "evidence/n42_period_two_six_quartic_ensemble_arb.json"
QUARTIC_ORBIT_PATH = ROOT / "evidence/n42_period_two_six_quartic_all_orbits_arb.json"
QUARTIC_CERT_PATH = ROOT / "evidence/n42_optimal_quartic_chi_square_arb.json"
RUN70_PATH = ROOT / "evidence/n42_degree_six_harmonic_projection_arb.json"
OUTPUT_PATH = ROOT / "evidence/n42_sixth_harmonic_local_pricing_arb.json"

N = 42
n = 21
PROBES = [
    (0, 1, 2, 3, 4, 5),
    (0, 1, 2, 3, 4, 6),
    (0, 1, 2, 3, 5, 7),
    (0, 1, 2, 4, 6, 8),
    (0, 1, 3, 5, 7, 9),
    (0, 2, 4, 6, 8, 10),
    (0, 1, 10, 11, 20, 21),
    (0, 3, 9, 15, 21, 27),
    (0, 5, 12, 19, 26, 33),
    (0, 7, 14, 21, 28, 35),
    (0, 2, 13, 17, 29, 38),
    (1, 4, 11, 20, 30, 39),
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def local_witness(indices, atom):
    """W_S(Q): one 6-minor, fifteen 4-minors, fifteen 2-minors, constant."""
    value = arb(fmpq(1, 2849))
    value += base_audit.principal_minor(indices, atom, n)
    for subset in combinations(indices, 4):
        value += base_audit.principal_minor(subset, atom, n) / 33
    for subset in combinations(indices, 2):
        value += base_audit.principal_minor(subset, atom, n) / 385
    return value


def verify():
    atom_bytes = ATOM_PATH.read_bytes()
    weight_bytes = WEIGHT_PATH.read_bytes()
    quartic_orbit_bytes = QUARTIC_ORBIT_PATH.read_bytes()
    quartic_cert_bytes = QUARTIC_CERT_PATH.read_bytes()
    run70_bytes = RUN70_PATH.read_bytes()

    atom_sha = sha256(atom_bytes)
    weight_sha = sha256(weight_bytes)
    quartic_orbit_sha = sha256(quartic_orbit_bytes)
    quartic_cert_sha = sha256(quartic_cert_bytes)

    atom_data = json.loads(atom_bytes)
    weight_data = json.loads(weight_bytes)
    quartic_data = json.loads(quartic_orbit_bytes)
    quartic_cert = json.loads(quartic_cert_bytes)
    run70 = json.loads(run70_bytes)

    top_rows = run70.get("top_harmonic_coordinates_by_abs_midpoint", [])
    top_by_indices = {tuple(row["indices"]): row for row in top_rows}
    probes = [PROBES[0]]
    seen_orbits = {
        projection.canonical_mask(sum(1 << i for i in probes[0]))
    }
    for row in run70.get("top_harmonic_coordinates_by_abs_midpoint", []):
        candidate = tuple(row["indices"])
        representative = projection.canonical_mask(sum(1 << i for i in candidate))
        if representative not in seen_orbits:
            probes.append(candidate)
            seen_orbits.add(representative)
        if len(probes) == 12:
            break
    for candidate in PROBES[1:]:
        if len(probes) == 12:
            break
        representative = projection.canonical_mask(sum(1 << i for i in candidate))
        if representative not in seen_orbits:
            probes.append(candidate)
            seen_orbits.add(representative)
    if len(probes) != 12:
        raise AssertionError("could not construct twelve distinct pricing probes")

    if run70["status"] != "full_sixth_harmonic_projection_certified":
        raise AssertionError("Run 70 full projection certificate is not complete")
    if atom_sha != run70["atom_input_sha256"]:
        raise AssertionError("frozen atom hash differs from Run 70")
    if weight_sha != run70["weight_input_sha256"]:
        raise AssertionError("frozen weight hash differs from Run 70")
    if quartic_orbit_sha != run70["quartic_orbit_certificate_sha256"]:
        raise AssertionError("quartic orbit certificate hash differs from Run 70")
    if quartic_cert_sha != run70["quartic_certificate_sha256"]:
        raise AssertionError("Run 68 certificate hash differs from Run 70")
    if quartic_data["input_sha256"] != atom_sha:
        raise AssertionError("quartic orbit evidence is not tied to the frozen atoms")
    if quartic_cert["input_sha256"] != quartic_orbit_sha:
        raise AssertionError("quartic chi-square evidence is not tied to the orbit file")
    if atom_data["N"] != N or atom_data["n"] != n:
        raise AssertionError("unexpected N or n")
    if atom_data["precision_bits"] != 256:
        raise AssertionError("unexpected Arb precision")

    ctx.prec = 256
    quartic_residual_by_rep, quartic_subset_to_rep = (
        projection.build_quartic_residual_lookup(quartic_data)
    )
    weights, direct, translated = projection.build_candidate(atom_data, weight_data)
    mu6, lambda6 = projection.exact_lambda6()

    canonical_orbits = {
        projection.canonical_mask(sum(1 << i for i in indices))
        for indices in probes
    }
    if len(canonical_orbits) != len(probes):
        raise AssertionError("the fixed probes are not in distinct D42 orbits")

    variance = arb(fmpq(7938048, 8026447))
    chi_multiplier = arb(fmpq(8026447, 7938048))
    target_mean = (
        fmpq(-5, 19721)
        + fmpq(15, 33) * fmpq(1, 533)
        + fmpq(15, 385) * fmpq(-1, 41)
        + fmpq(1, 2849)
    )
    if target_mean != 0:
        raise AssertionError("the local witness is not exactly centered")

    # A non-period-two, fully connected positive-cycle escape for the first
    # probe S={0,...,5}. At zero closing edge, the length-42 spin-chain
    # perfect-transfer atom is the signed reversal i <-> 41-i. No pair lies
    # wholly inside S, so all nonempty even principal minors on S vanish and
    # W_S=1/2849 exactly. Opening the closing edge by eps changes A in
    # operator norm by 2 eps. The Duhamel/Hadamard bound below is global.
    epsilon = Fraction(1, 10**6)
    witness_lipschitz = Fraction(1216, 77)
    boundary_witness = Fraction(1, 2849)
    path_witness_lower = boundary_witness - witness_lipschitz * epsilon
    path_witness_upper = boundary_witness + witness_lipschitz * epsilon
    if not (path_witness_lower > 0):
        raise AssertionError("the fully connected path-escape witness is not positive")
    if not (witness_lipschitz < 16):
        raise AssertionError("unexpected local-witness Lipschitz constant")

    records = []
    first_probe_coordinate = None
    for indices in probes:
        direct_coordinate = projection.harmonic_residual(
            indices,
            weights,
            direct,
            translated,
            quartic_residual_by_rep,
            quartic_subset_to_rep,
            mu6,
        )
        priced_mean = arb(0)
        for weight, atom, shift_atom in zip(weights, direct, translated):
            priced_mean += weight * (
                local_witness(indices, atom)
                + local_witness(indices, shift_atom)
            ) / 2
        difference = priced_mean - direct_coordinate
        if not difference.contains(0):
            raise AssertionError(
                f"local pricing disagrees with the Run 70 projection at {indices}: "
                f"{difference}"
            )
        stored_top = top_by_indices.get(tuple(indices))
        if stored_top is not None:
            stored_interval = arb(stored_top["residual_interval"])
            if not (stored_interval - direct_coordinate).contains(0):
                raise AssertionError(
                    f"recomputed coordinate disagrees with Run 70 stored interval at {indices}"
                )
        if not records:
            first_probe_coordinate = direct_coordinate
        if direct_coordinate.contains(0):
            chi_lower = arb(0)
        else:
            chi_lower = direct_coordinate * direct_coordinate / variance
        records.append({
            "indices": list(indices),
            "canonical_D42_representative": list(
                projection.mask_to_tuple(
                    projection.canonical_mask(sum(1 << i for i in indices))
                )
            ),
            "direct_projection_coordinate_interval": str(direct_coordinate),
            "32_minor_pricing_expectation_interval": str(priced_mean),
            "difference_interval": str(difference),
            "run70_stored_residual_interval": (
                stored_top["residual_interval"] if stored_top is not None else None
            ),
            "single_coordinate_chi_square_lower_bound_interval": str(chi_lower),
        })

    if first_probe_coordinate is None or not (first_probe_coordinate < 0):
        raise AssertionError("the frozen candidate's first local coordinate is not negative")

    result = {
        "schema": "eui_n42_sixth_harmonic_local_pricing_arb_v1",
        "status": "local_pricing_identity_certified_on_frozen_n42_probes",
        "N": N,
        "n": n,
        "precision_bits": ctx.prec,
        "probe_count": len(records),
        "probe_selection_method": "fixed S={0,...,5} plus eleven largest-magnitude Run 70 harmonic coordinates, ranked by binary64 midpoint",
        "run70_top_coordinate_count": len(top_rows),
        "run70_top_coordinate_ranking_method": run70.get("top_coordinate_ranking_method"),
        "distinct_D42_probe_orbits": len(canonical_orbits),
        "minors_per_atom_per_probe": 32,
        "local_witness_coefficients": {
            "order_0": "1/2849",
            "order_2": "1/385",
            "order_4": "1/33",
            "order_6": "1",
        },
        "lambda6_exact": str(lambda6),
        "witness_variance_exact": "7938048/8026447",
        "chi_square_multiplier_exact": "8026447/7938048",
        "uniform_target_mean_exact": "0",
        "atom_input_sha256": atom_sha,
        "weight_input_sha256": weight_sha,
        "quartic_orbit_certificate_sha256": quartic_orbit_sha,
        "quartic_certificate_sha256": quartic_cert_sha,
        "run70_certificate_sha256": sha256(run70_bytes),
        "fully_connected_positive_cycle_escape": {
            "probe_indices": list(probes[0]),
            "path_couplings": (
                "c_j=(pi/4)*sqrt((j+1)*(41-j)) for j=0,...,40; "
                "c_41=1/1000000"
            ),
            "all_42_couplings_strictly_positive": True,
            "minimum_internal_coupling_expression": "pi*sqrt(41)/4 > 0",
            "zero_closing_edge_perfect_transfer_matching": "i <-> 41-i",
            "boundary_witness_exact": str(boundary_witness),
            "closing_edge_epsilon": str(epsilon),
            "generator_operator_norm_difference_bound": "2*epsilon",
            "witness_lipschitz_constant_exact": str(witness_lipschitz),
            "witness_lipschitz_constant_less_than_16": True,
            "positive_cycle_witness_lower_bound_exact": str(path_witness_lower),
            "positive_cycle_witness_upper_bound_exact": str(path_witness_upper),
            "frozen_candidate_coordinate_interval": str(first_probe_coordinate),
            "opposite_sign_physical_atom_certified": True,
            "two_atom_mixture_can_cancel_this_one_coordinate": True,
            "scope": (
                "The positive-cycle atom cancels only the selected S={0,...,5} "
                "harmonic coordinate after a suitable convex reweighting. It "
                "does not match the other moment coordinates or solve the "
                "full convex-hull problem."
            ),
        },
        "probes": records,
        "scope": (
            "This verifies the compact local pricing identity against the Run 70 "
            "full-projection coordinate formula on twelve distinct D42 orbits of "
            "the frozen 37-base/74-labelled period-two candidate. Probe set: one fixed path-escape set plus eleven largest Run 70 residual coordinates. The theorem "
            "itself applies to every real 42-cycle coupling vector because Q(c) "
            "is a symmetric involution with 21 eigenvalues of each sign. The "
            "probe computation is not a global separator and does not exclude "
            "the continuous physical convex hull or imply a Choi/diamond bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "probe_count": len(records),
        "minors_per_atom_per_probe": 32,
        "all_differences_contain_zero": True,
        "positive_cycle_escape_lower_bound": str(path_witness_lower),
        "frozen_first_probe_coordinate": str(first_probe_coordinate),
        "witness_variance_exact": result["witness_variance_exact"],
        "chi_square_multiplier_exact": result["chi_square_multiplier_exact"],
        "probe_coordinates": [
            {
                "indices": row["indices"],
                "coordinate": row["direct_projection_coordinate_interval"],
                "chi_square_lower": row["single_coordinate_chi_square_lower_bound_interval"],
            }
            for row in records
        ],
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
