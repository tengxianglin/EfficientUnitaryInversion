#!/usr/bin/env python3
"""256-bit Arb lower bound from the complete N=42 sixth-harmonic orbit audit.

For the frozen 37-base / 74-labelled period-two ensemble, compute every
D_42 orbit representative of six-subsets, evaluate its corrected degree-six
harmonic residual, and sum every square whose Arb interval excludes zero.
Intervals containing zero are safely dropped, so the result is a rigorous
lower bound on the complete sixth-harmonic projection norm.
"""
import hashlib
import json
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, fmpq, ctx

import verify_n42_period_two_six_quartic_ensemble_arb as base_audit

ROOT = Path(__file__).resolve().parent
ATOM_PATH = ROOT / "evidence/n42_period_two_six_quartic_atoms.json"
WEIGHT_PATH = ROOT / "evidence/n42_period_two_six_quartic_ensemble_arb.json"
QUARTIC_ORBIT_PATH = ROOT / "evidence/n42_period_two_six_quartic_all_orbits_arb.json"
QUARTIC_CERT_PATH = ROOT / "evidence/n42_optimal_quartic_chi_square_arb.json"
RUN69_PATH = ROOT / "evidence/n42_degree_six_harmonic_witness_arb.json"
OUTPUT_PATH = ROOT / "evidence/n42_degree_six_harmonic_projection_arb.json"

N = 42
n = 21
M = (1 << N) - 1
EXPECTED_SIX_ORBITS = 63133
EXPECTED_SIX_SUBSETS = comb(N, 6)
QUARTIC_FLOOR_DECIMAL = "0.0823554383888206439539508334768407205230"


def rotate_left_one(mask):
    return ((mask << 1) & M) | (mask >> (N - 1))


def reflect_mask(mask):
    """Reflection i -> N-1-i; together with rotations this generates D_42."""
    reflected = 0
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        index = bit.bit_length() - 1
        reflected |= 1 << (N - 1 - index)
        remaining ^= bit
    return reflected


def is_canonical_mask(mask):
    """Return true iff mask is the numeric minimum in its D_42 orbit."""
    for start in (mask, reflect_mask(mask)):
        current = start
        for _ in range(N):
            if current < mask:
                return False
            current = rotate_left_one(current)
    return True


def orbit_size_mask(mask):
    images = set()
    for start in (mask, reflect_mask(mask)):
        current = start
        for _ in range(N):
            images.add(current)
            current = rotate_left_one(current)
    return len(images)


def mask_to_tuple(mask):
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return tuple(result)


def all_six_orbit_representatives():
    """Enumerate D_42 bracelets of weight six using an early-exit canonical test."""
    records = []
    orbit_size_sum = 0
    for subset in combinations(range(N), 6):
        mask = sum(1 << i for i in subset)
        if is_canonical_mask(mask):
            size = orbit_size_mask(mask)
            records.append((mask, size))
            orbit_size_sum += size
    if len(records) != EXPECTED_SIX_ORBITS:
        raise AssertionError(
            f"wrong D42 six-orbit count: {len(records)} != {EXPECTED_SIX_ORBITS}"
        )
    if orbit_size_sum != EXPECTED_SIX_SUBSETS:
        raise AssertionError(
            f"six-orbit sizes sum to {orbit_size_sum}, expected {EXPECTED_SIX_SUBSETS}"
        )
    return records, orbit_size_sum


def build_quartic_residual_lookup(quartic_data):
    """Expand all 1,440 certified D42 orbit residuals to all 111,930 quartets."""
    records = quartic_data["all_orbit_records"]
    if len(records) != 1440:
        raise AssertionError("the frozen quartic certificate must contain 1,440 orbits")
    residual_by_rep = {}
    subset_to_rep = {}
    orbit_size_sum = 0
    for record in records:
        representative = tuple(record["representative"])
        residual = arb(record["residual_interval"])
        residual_by_rep[representative] = residual
        images = set()
        for sign in (1, -1):
            for shift in range(N):
                image = tuple(sorted((sign * x + shift) % N for x in representative))
                images.add(image)
                old = subset_to_rep.setdefault(image, representative)
                if old != representative:
                    raise AssertionError("quartic D42 orbit records overlap")
        if len(images) != record["orbit_size"]:
            raise AssertionError("quartic orbit size disagrees with its D42 images")
        orbit_size_sum += record["orbit_size"]
    if len(subset_to_rep) != comb(N, 4):
        raise AssertionError("quartic D42 map does not cover all four-subsets")
    if orbit_size_sum != comb(N, 4):
        raise AssertionError("quartic orbit sizes do not sum to C(42,4)")
    return residual_by_rep, subset_to_rep


def balanced_slice_moments_through_six():
    moments = [fmpq(1)]
    value = fmpq(1)
    for j in range(1, 7):
        value *= fmpq(-(2 * j - 1), N - (2 * j - 1))
        moments.append(value)
    return moments


def exact_lambda6():
    moments = balanced_slice_moments_through_six()
    value = sum(
        (fmpq((-1) ** j * comb(6, j)) * moments[j] for j in range(7)),
        fmpq(0),
    )
    closed = fmpq(4 ** 6 * comb(N - 12, n - 6), comb(N, n))
    if value != closed or value != fmpq(7938048, 6724861):
        raise AssertionError(f"unexpected sixth harmonic eigenvalue: {value}")
    return moments[3], value


def build_candidate(atom_data, weight_data):
    ctx.prec = atom_data["precision_bits"]
    atoms = atom_data["atoms"]
    weights = [arb(value) for value in weight_data["weights"]]
    if len(atoms) != 37 or len(weights) != 37:
        raise AssertionError("unexpected frozen candidate support size")
    if not all(weight > 0 for weight in weights):
        raise AssertionError("a frozen candidate weight is not strictly positive")
    if not sum(weights, arb(0)).contains(1):
        raise AssertionError("frozen candidate weights do not sum to one")
    cosine, sine = base_audit.build_tables(n)
    direct = [base_audit.build_atom(atom, n, cosine, sine) for atom in atoms]
    translated_atoms = [{"a": atom["b"], "b": atom["a"]} for atom in atoms]
    translated = [
        base_audit.build_atom(atom, n, cosine, sine)
        for atom in translated_atoms
    ]
    return weights, direct, translated


def harmonic_residual(indices, weights, direct, translated,
                      quartic_residual_by_rep, quartic_subset_to_rep,
                      mu6):
    """delta_6^harm(I) = delta_6(I) + (1/33) sum_{K subset I, |K|=4} delta_4(K)."""
    moment = arb(0)
    for weight, atom, shift_atom in zip(weights, direct, translated):
        base_minor = base_audit.principal_minor(indices, atom, n)
        shift_minor = base_audit.principal_minor(indices, shift_atom, n)
        moment += weight * (base_minor + shift_minor) / 2
    delta6 = moment - arb(mu6)

    correction_sum = arb(0)
    for quartet in combinations(indices, 4):
        representative = quartic_subset_to_rep[tuple(quartet)]
        correction_sum += quartic_residual_by_rep[representative]
    return delta6 + correction_sum / 33


def verify():
    atom_bytes = ATOM_PATH.read_bytes()
    weight_bytes = WEIGHT_PATH.read_bytes()
    quartic_orbit_bytes = QUARTIC_ORBIT_PATH.read_bytes()
    quartic_cert_bytes = QUARTIC_CERT_PATH.read_bytes()
    run69_bytes = RUN69_PATH.read_bytes()

    atom_sha = hashlib.sha256(atom_bytes).hexdigest()
    weight_sha = hashlib.sha256(weight_bytes).hexdigest()
    quartic_orbit_sha = hashlib.sha256(quartic_orbit_bytes).hexdigest()
    quartic_cert_sha = hashlib.sha256(quartic_cert_bytes).hexdigest()

    atom_data = json.loads(atom_bytes)
    weight_data = json.loads(weight_bytes)
    quartic_data = json.loads(quartic_orbit_bytes)
    quartic_cert = json.loads(quartic_cert_bytes)
    run69 = json.loads(run69_bytes)

    if run69["status"] != "candidate_specific_degree_six_harmonic_witness_certified":
        raise AssertionError("Run 69 explicit witness certificate is missing")
    if atom_sha != run69["atom_input_sha256"]:
        raise AssertionError("frozen atom input hash differs from Run 69")
    if weight_sha != run69["weight_input_sha256"]:
        raise AssertionError("frozen weight input hash differs from Run 69")
    if quartic_cert_sha != run69["quartic_certificate_sha256"]:
        raise AssertionError("Run 68 quartic certificate hash differs from Run 69")
    if quartic_data["input_sha256"] != atom_sha:
        raise AssertionError("quartic orbit certificate is not tied to the frozen atoms")
    if quartic_cert["input_sha256"] != quartic_orbit_sha:
        raise AssertionError("Run 68 certificate is not tied to the full quartic orbit file")
    if quartic_data["status"] != "strict_counterexample_to_full_quartic_design_for_frozen_support":
        raise AssertionError("unexpected full-quartic audit status")
    if quartic_cert["status"] != "optimal_degree_four_character_chi_square_bound_certified":
        raise AssertionError("unexpected Run 68 quartic certificate status")

    ctx.prec = atom_data["precision_bits"]
    quartic_floor = arb(QUARTIC_FLOOR_DECIMAL)
    if ctx.prec != 256 or atom_data["N"] != N or atom_data["n"] != n:
        raise AssertionError("unexpected N, n, or Arb precision")
    if not (arb(quartic_cert["optimal_quartic_chi_square_lower_bound_interval"])
            > quartic_floor):
        raise AssertionError("Run 68 does not certify the conservative quartic floor")

    quartic_residual_by_rep, quartic_subset_to_rep = (
        build_quartic_residual_lookup(quartic_data)
    )
    weights, direct, translated = build_candidate(atom_data, weight_data)
    mu6, lambda6 = exact_lambda6()
    run69_witness = arb(run69["degree_six_chi_square_lower_bound_interval"])

    # Small symmetry regression: both generators of D_42 preserve the corrected
    # harmonic residual for several representatives of the frozen ensemble.
    symmetry_checks = 0
    def check_symmetry(indices):
        nonlocal symmetry_checks
        original = harmonic_residual(
            indices, weights, direct, translated,
            quartic_residual_by_rep, quartic_subset_to_rep, mu6
        )
        for image in (
            tuple(sorted((x + 1) % N for x in indices)),
            tuple(sorted((N - 1 - x) for x in indices)),
        ):
            transformed = harmonic_residual(
                image, weights, direct, translated,
                quartic_residual_by_rep, quartic_subset_to_rep, mu6
            )
            if not (transformed - original).contains(0):
                raise AssertionError("corrected sixth residual is not D42 invariant")
            symmetry_checks += 1
    symmetry_probe_count = 12

    orbit_records, orbit_size_sum = all_six_orbit_representatives()
    for mask, _ in orbit_records[:symmetry_probe_count]:
        check_symmetry(mask_to_tuple(mask))

    norm2_lower = arb(0)
    sign_definite_orbits = 0
    zero_crossing_orbits = 0
    digest = hashlib.sha256()

    for index, (mask, orbit_size) in enumerate(orbit_records):
        indices = mask_to_tuple(mask)
        residual = harmonic_residual(
            indices, weights, direct, translated,
            quartic_residual_by_rep, quartic_subset_to_rep, mu6
        )
        digest.update(f"{mask}:{orbit_size}:{residual}\n".encode())
        if residual.contains(0):
            zero_crossing_orbits += 1
        else:
            square = residual * residual
            if not (square > 0):
                raise AssertionError("a sign-definite harmonic residual did not square positive")
            norm2_lower += orbit_size * square
            sign_definite_orbits += 1
        if (index + 1) % 5000 == 0:
            print(
                f"priced {index + 1}/{len(orbit_records)} sixth orbits; "
                f"sign-definite={sign_definite_orbits}; "
                f"norm2-lower={norm2_lower}",
                flush=True,
            )

    if sign_definite_orbits + zero_crossing_orbits != EXPECTED_SIX_ORBITS:
        raise AssertionError("not every sixth-order orbit was priced")
    if not (norm2_lower > 0):
        raise AssertionError("no positive full-projection lower bound was certified")

    degree6_partial = norm2_lower / arb(lambda6)
    partial_beats_run69 = degree6_partial > run69_witness
    best_degree6 = degree6_partial if partial_beats_run69 else run69_witness
    combined = quartic_floor + best_degree6
    if not (combined > arb("0.0823555")):
        raise AssertionError("combined degree-four/sixth lower bound regressed")

    result = {
        "schema": "eui_n42_full_sixth_harmonic_projection_lower_bound_v1",
        "status": "all_63133_sixth_orbits_priced_with_certified_harmonic_projection_lower_bound",
        "N": N,
        "n": n,
        "precision_bits": ctx.prec,
        "quartic_orbit_count": 1440,
        "quartic_subset_count": comb(N, 4),
        "quartic_orbit_size_sum": comb(N, 4),
        "sixth_orbit_count": len(orbit_records),
        "sixth_subset_count": EXPECTED_SIX_SUBSETS,
        "sixth_orbit_size_sum": orbit_size_sum,
        "sixth_orbits_with_harmonic_interval_excluding_zero": sign_definite_orbits,
        "sixth_orbits_with_harmonic_interval_containing_zero": zero_crossing_orbits,
        "sixth_principal_minors_evaluated": EXPECTED_SIX_ORBITS * 74,
        "D42_symmetry_regression_checks": symmetry_checks,
        "harmonic_projection_coordinate_formula": (
            "delta6_harm(I)=delta6(I)+(1/33)*sum_{K subset I, |K|=4} delta4(K)"
        ),
        "harmonic_projection_norm2_partial_lower_bound_interval": str(norm2_lower),
        "lambda6_exact": str(lambda6),
        "degree_six_partial_projection_chi_square_lower_bound_interval": str(degree6_partial),
        "run69_explicit_witness_chi_square_contribution_interval": str(run69_witness),
        "partial_projection_beats_run69_explicit_witness": bool(partial_beats_run69),
        "best_degree_six_contribution_interval": str(best_degree6),
        "quartic_chi_square_lower_bound_floor": str(quartic_floor),
        "combined_degree_four_plus_degree_six_chi_square_lower_bound_interval": str(combined),
        "combined_lower_bound_gt_0.0823555": True,
        "orbit_residual_digest_sha256": digest.hexdigest(),
        "atom_input_sha256": atom_sha,
        "weight_input_sha256": weight_sha,
        "quartic_orbit_certificate_sha256": quartic_orbit_sha,
        "quartic_certificate_sha256": quartic_cert_sha,
        "run69_certificate_sha256": hashlib.sha256(run69_bytes).hexdigest(),
        "scope": (
            "Candidate-specific for the frozen 37-base/74-labelled period-two ensemble. "
            "All 63,133 D42 sixth-subset orbits were evaluated. The reported norm is a "
            "rigorous lower bound obtained by summing every orbit whose corrected Arb "
            "residual interval excludes zero; intervals containing zero were safely "
            "dropped. This does not exclude another physical measure or the full "
            "continuous cycle-exponential family and implies no program-TV, Choi, or "
            "diamond-distance bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "sixth_orbits": result["sixth_orbit_count"],
        "sixth_subsets": result["sixth_subset_count"],
        "sign_definite_orbits": sign_definite_orbits,
        "zero_crossing_orbits": zero_crossing_orbits,
        "harmonic_projection_norm2_partial_lower_bound_interval": result[
            "harmonic_projection_norm2_partial_lower_bound_interval"
        ],
        "degree_six_partial_projection_chi_square_lower_bound_interval": result[
            "degree_six_partial_projection_chi_square_lower_bound_interval"
        ],
        "run69_explicit_witness_chi_square_contribution_interval": result[
            "run69_explicit_witness_chi_square_contribution_interval"
        ],
        "partial_projection_beats_run69_explicit_witness": partial_beats_run69,
        "combined_degree_four_plus_degree_six_chi_square_lower_bound_interval": result[
            "combined_degree_four_plus_degree_six_chi_square_lower_bound_interval"
        ],
        "orbit_residual_digest_sha256": result["orbit_residual_digest_sha256"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
