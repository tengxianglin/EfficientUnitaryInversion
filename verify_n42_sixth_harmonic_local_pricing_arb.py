#!/usr/bin/env python3
"""256-bit Arb check of the local sixth-harmonic pricing identity at N=42."""
import hashlib
import json
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
        for indices in PROBES
    }
    if len(canonical_orbits) != len(PROBES):
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

    records = []
    for indices in PROBES:
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
            "single_coordinate_chi_square_lower_bound_interval": str(chi_lower),
        })

    result = {
        "schema": "eui_n42_sixth_harmonic_local_pricing_arb_v1",
        "status": "local_pricing_identity_certified_on_frozen_n42_probes",
        "N": N,
        "n": n,
        "precision_bits": ctx.prec,
        "probe_count": len(records),
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
        "probes": records,
        "scope": (
            "This verifies the compact local pricing identity against the Run 70 "
            "full-projection coordinate formula on twelve distinct D42 orbits of "
            "the frozen 37-base/74-labelled period-two candidate. The theorem "
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
