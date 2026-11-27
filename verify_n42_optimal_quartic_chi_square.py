#!/usr/bin/env python3
"""Optimal degree-four character chi-square certificate for the frozen N=42 candidate.

The proof uses the exact Johnson-scheme action of the balanced-slice Gram
kernel on the fourth harmonic subspace.  No 1,440x1,440 pseudoinverse is used.
"""
import hashlib
import json
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, fmpq, ctx

import verify_n42_period_two_six_quartic_ensemble_arb as pair_audit
import verify_n42_period_two_six_quartic_all_orbits_arb as quartic_audit

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_six_quartic_all_orbits_arb.json"
OUTPUT = ROOT / "evidence/n42_optimal_quartic_chi_square_arb.json"
N = 42
PAIR_TARGET = fmpq(-1, 41)
QUARTIC_TARGET = fmpq(1, 533)
LAMBDA4 = fmpq(21888, 19721)


def orbit_lookup(records):
    """Map every quartet to its D42 representative using the frozen orbit list."""
    lookup = {}
    for record in records:
        representative = tuple(record["representative"])
        for sign in (1, -1):
            for shift in range(N):
                image = tuple(sorted((sign * x + shift) % N for x in representative))
                old = lookup.setdefault(image, representative)
                if old != representative:
                    raise AssertionError("quartic D42 orbits overlap")
    if len(lookup) != comb(N, 4):
        raise AssertionError("D42 orbit map does not cover all quartets")
    return lookup


def verify_down_relations(records):
    """Certify D_4 delta=0 from the 861 pair equations and quartet intervals."""
    residual_by_rep = {
        tuple(record["representative"]): arb(record["residual_interval"])
        for record in records
    }
    lookup = orbit_lookup(records)
    checked = 0
    for triple in combinations(range(N), 3):
        total = arb(0)
        triple_set = set(triple)
        for i in range(N):
            if i in triple_set:
                continue
            quartet = tuple(sorted((*triple, i)))
            representative = lookup[quartet]
            total += residual_by_rep[representative]
        if not total.contains(0):
            raise AssertionError(
                f"fourth-to-third down relation is not certified at {triple}: {total}"
            )
        checked += 1
    if checked != comb(N, 3):
        raise AssertionError("incorrect number of down relations")
    return checked


def exact_lambda4():
    """Fourth-harmonic eigenvalue of the balanced-slice quartic Gram kernel."""
    moments = [
        fmpq(1),
        fmpq(-1, 41),
        fmpq(1, 533),
        fmpq(-15, 41 * 39 * 37),
        fmpq(105, 41 * 39 * 37 * 35),
    ]
    value = sum(
        (fmpq((-1) ** j * comb(4, j)) * moments[j] for j in range(5)),
        fmpq(0),
    )
    if value != LAMBDA4:
        raise AssertionError(f"unexpected lambda_4: {value}")
    return moments, value


def verify():
    # Independently regenerate the exact-real weights and all pair coordinates.
    pair_audit.verify()
    # Independently regenerate all 1,440 quartic orbit residual intervals.
    quartic_audit.verify()

    data = json.loads(INPUT.read_text())
    ctx.prec = data["precision_bits"]
    assert data["N"] == N and data["n"] == 21
    assert data["quartic_subset_count"] == comb(N, 4) == 111930
    assert data["quartic_orbit_count"] == 1440
    assert data["quartic_orbit_size_sum"] == comb(N, 4)
    assert data["orbits_with_strict_certified_mismatch"] == 1434
    assert data["orbits_whose_residual_interval_contains_zero"] == 6

    moments, eigenvalue = exact_lambda4()
    down_relations = verify_down_relations(data["all_orbit_records"])

    residual_norm2 = arb(0)
    for record in data["all_orbit_records"]:
        residual = arb(record["residual_interval"])
        residual_norm2 += record["orbit_size"] * residual * residual

    if not (residual_norm2 > arb("0.0913")):
        raise AssertionError(f"quartic residual norm is too small: {residual_norm2}")

    chi_square_lower_bound = residual_norm2 / arb(eigenvalue)
    threshold = arb("0.0823")
    if not (chi_square_lower_bound > threshold):
        raise AssertionError(
            f"optimal quartic chi-square bound did not exceed {threshold}: "
            f"{chi_square_lower_bound}"
        )

    previous_bound = arb("0.0733075379017796406817054805625287")
    improvement = chi_square_lower_bound / previous_bound
    if not (improvement > arb("1.12")):
        raise AssertionError(f"improvement over Run 67 is not >1.12: {improvement}")

    d = comb(N, 21)
    frame_potential_target = arb(fmpq(4, d))
    frame_potential_lower_bound = (
        frame_potential_target * (1 + chi_square_lower_bound)
    )

    result = {
        "schema": "eui_n42_optimal_quartic_chi_square_arb_v1",
        "status": "optimal_degree_four_character_chi_square_bound_certified",
        "N": N,
        "n": 21,
        "group": "D_42",
        "pair_target": str(PAIR_TARGET),
        "quartic_target": str(QUARTIC_TARGET),
        "pair_coordinates_recomputed": comb(N, 2),
        "quartic_subset_count": comb(N, 4),
        "quartic_orbit_count": len(data["all_orbit_records"]),
        "quartic_orbit_size_sum": data["quartic_orbit_size_sum"],
        "down_operator": "D_4[a]_J = sum_{i notin J} a_{J union {i}}",
        "all_triple_down_relations_interval_contain_zero": True,
        "triple_down_relations_checked": down_relations,
        "balanced_slice_moments_order_0_to_8": [str(x) for x in moments],
        "quartic_gram_harmonic_eigenvalue_exact": str(eigenvalue),
        "quartic_residual_l2_squared_interval": str(residual_norm2),
        "optimal_quartic_chi_square_lower_bound_interval": str(chi_square_lower_bound),
        "optimal_quartic_chi_square_lower_bound_gt_0.0823": True,
        "improvement_over_run67_interval": str(improvement),
        "improvement_over_run67_gt_1.12": True,
        "frame_potential_target_interval": str(frame_potential_target),
        "frame_potential_lower_bound_interval": str(frame_potential_lower_bound),
        "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "optimality_scope": (
            "This is the exact maximum Cauchy-Schwarz chi-square lower bound "
            "obtainable from all fourth-order character moments, because the "
            "residual vector lies in ker(D_4) and the balanced-slice Gram kernel "
            "acts there as the scalar lambda_4. It is not the full chi-square "
            "unless all higher harmonic discrepancies vanish."
        ),
        "scope": (
            "Candidate-specific for the frozen 37-base/74-labelled period-two "
            "ensemble. It does not exclude another period-two measure or the "
            "general continuous cycle-exponential family. The existing direct "
            "program-label TV lower bound remains >0.00275; this chi-square "
            "improvement is not a stronger TV, Choi, or diamond-distance bound."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "quartic_residual_l2_squared_interval": result["quartic_residual_l2_squared_interval"],
        "lambda4_exact": result["quartic_gram_harmonic_eigenvalue_exact"],
        "optimal_quartic_chi_square_lower_bound_interval": result[
            "optimal_quartic_chi_square_lower_bound_interval"
        ],
        "improvement_over_run67_interval": result["improvement_over_run67_interval"],
        "frame_potential_lower_bound_interval": result["frame_potential_lower_bound_interval"],
        "down_relations_checked": down_relations,
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
