#!/usr/bin/env python3
"""256-bit Arb certificate for an explicit degree-six harmonic witness at N=42.

The witness is h(x)=prod_{r=0}^5 (x_{2r}-x_{2r+1}).  Its coefficient vector
lies in ker(D_6), so it is orthogonal on the balanced slice to all lower-degree
components, including the nonzero quartic discrepancy of the frozen candidate.
Only 64 six-subset minors per physical atom are needed.
"""
import hashlib
import json
from itertools import combinations, product
from math import comb
from pathlib import Path

from flint import arb, fmpq, ctx

import verify_n42_period_two_six_quartic_ensemble_arb as base_audit

ROOT = Path(__file__).resolve().parent
ATOM_PATH = ROOT / "evidence/n42_period_two_six_quartic_atoms.json"
WEIGHT_PATH = ROOT / "evidence/n42_period_two_six_quartic_ensemble_arb.json"
QUARTIC_PATH = ROOT / "evidence/n42_optimal_quartic_chi_square_arb.json"
OUTPUT_PATH = ROOT / "evidence/n42_degree_six_harmonic_witness_arb.json"

N = 42
N_HALF = 21
PAIRS = tuple((2 * r, 2 * r + 1) for r in range(6))
PAIR_CHOICES = tuple(product(*PAIRS))
COEFFICIENTS = tuple((-1) ** sum(choice[r] == PAIRS[r][1] for r in range(6))
                     for choice in PAIR_CHOICES)
SUBSETS = tuple(tuple(sorted(choice)) for choice in PAIR_CHOICES)


def balanced_slice_moment(order):
    """Exact E[product of 'order' distinct balanced signs] for N=2n."""
    if order % 2:
        return fmpq(0)
    value = fmpq(1)
    for j in range(1, order // 2 + 1):
        value *= fmpq(-(2 * j - 1), N - (2 * j - 1))
    return value


def verify_harmonic_coefficients():
    """Check D_6 a=0 exactly; all nonzero coefficients lie on [0,12)."""
    if len(set(SUBSETS)) != 64 or len(COEFFICIENTS) != 64:
        raise AssertionError("the degree-six character expansion is not 64-term")
    if sum(COEFFICIENTS) != 0:
        raise AssertionError("the uniform balanced-slice mean must vanish")

    # A five-set outside [0,12) is contained in no support six-set.  It is
    # therefore enough to check all C(12,5)=792 five-sets inside [0,12).
    coefficient = dict(zip(SUBSETS, COEFFICIENTS))
    checked = 0
    for J in combinations(range(12), 5):
        total = 0
        Jset = set(J)
        for i in range(12):
            if i not in Jset:
                total += coefficient.get(tuple(sorted((*J, i))), 0)
        if total != 0:
            raise AssertionError(f"D_6 coefficient relation failed at {J}: {total}")
        checked += 1
    if checked != comb(12, 5):
        raise AssertionError("incorrect number of local harmonic checks")
    return checked


def exact_degree_six_variance():
    """Return E_u[h^2] = 64 lambda_6 as an exact rational."""
    moments = [balanced_slice_moment(2 * j) for j in range(7)]
    lambda_from_moments = sum(
        (fmpq((-1) ** j * comb(6, j)) * moments[j] for j in range(7)),
        fmpq(0),
    )
    lambda_closed = fmpq(
        4 ** 6 * comb(N - 12, N_HALF - 6),
        comb(N, N_HALF),
    )
    if lambda_from_moments != lambda_closed:
        raise AssertionError(
            f"degree-six eigenvalue mismatch: {lambda_from_moments} != {lambda_closed}"
        )
    variance = 64 * lambda_closed
    return moments, lambda_closed, variance


def compute_witness_moment(atom_data, weight_data):
    """Evaluate E_q h from 64 principal minors per base/translated atom."""
    ctx.prec = atom_data["precision_bits"]
    atoms = atom_data["atoms"]
    weights = [arb(value) for value in weight_data["weights"]]
    if len(atoms) != 37 or len(weights) != len(atoms):
        raise AssertionError("unexpected frozen candidate support size")
    if not all(weight > 0 for weight in weights):
        raise AssertionError("a certified ensemble weight is not strictly positive")
    if not sum(weights, arb(0)).contains(1):
        raise AssertionError("frozen exact-real weights do not sum to one")

    cosine, sine = base_audit.build_tables(N_HALF)
    base = [base_audit.build_atom(atom, N_HALF, cosine, sine) for atom in atoms]
    shifted_atoms = [{"a": atom["b"], "b": atom["a"]} for atom in atoms]
    shifted = [
        base_audit.build_atom(atom, N_HALF, cosine, sine)
        for atom in shifted_atoms
    ]

    total = arb(0)
    per_atom = []
    for index, (weight, item, translated) in enumerate(zip(weights, base, shifted)):
        moment_ab = sum(
            (
                COEFFICIENTS[k]
                * base_audit.principal_minor(SUBSETS[k], item, N_HALF)
                for k in range(64)
            ),
            arb(0),
        )
        moment_ba = sum(
            (
                COEFFICIENTS[k]
                * base_audit.principal_minor(SUBSETS[k], translated, N_HALF)
                for k in range(64)
            ),
            arb(0),
        )
        atom_average = (moment_ab + moment_ba) / 2
        total += weight * atom_average
        per_atom.append({
            "atom_index": index,
            "base_witness_interval": str(moment_ab),
            "translated_witness_interval": str(moment_ba),
            "symmetrized_witness_interval": str(atom_average),
        })
    return total, per_atom


def verify():
    atom_data = json.loads(ATOM_PATH.read_text())
    weight_data = json.loads(WEIGHT_PATH.read_text())
    quartic_data = json.loads(QUARTIC_PATH.read_text())
    assert atom_data["N"] == N and atom_data["n"] == N_HALF
    assert weight_data["status"] == "certified_N42_period_two_six_quartic_orbit_ensemble"
    assert quartic_data["status"] == "optimal_degree_four_character_chi_square_bound_certified"

    harmonic_checks = verify_harmonic_coefficients()
    moments, lambda6, variance = exact_degree_six_variance()
    witness_moment, per_atom = compute_witness_moment(atom_data, weight_data)

    if not (witness_moment > arb("0.0032")):
        raise AssertionError(f"sixth harmonic witness is not separated: {witness_moment}")

    variance_arb = arb(variance)
    degree_six_bound = witness_moment * witness_moment / variance_arb
    if not (degree_six_bound > arb("1.3e-7")):
        raise AssertionError(f"degree-six chi-square bound too small: {degree_six_bound}")

    # Use a conservative decimal floor strictly below the frozen Run 68
    # interval.  This avoids treating the midpoint of an Arb interval as a
    # certified lower bound when adding orthogonal harmonic contributions.
    quartic_floor = arb("0.0823554383888206439539508334768407205230")
    quartic_interval = arb(quartic_data["optimal_quartic_chi_square_lower_bound_interval"])
    if not (quartic_interval > quartic_floor):
        raise AssertionError("the Run 68 quartic certificate no longer supports its floor")
    combined_bound = quartic_floor + degree_six_bound
    if not (combined_bound > arb("0.0823555")):
        raise AssertionError(f"combined orthogonal bound too small: {combined_bound}")

    result = {
        "schema": "eui_n42_degree_six_harmonic_witness_arb_v1",
        "status": "candidate_specific_degree_six_harmonic_witness_certified",
        "N": N,
        "n": N_HALF,
        "pairing": [list(pair) for pair in PAIRS],
        "witness": "h(x)=product_{r=0}^5 (x_{2r}-x_{2r+1})",
        "coefficient_support_size": 64,
        "coefficient_vector_squared_norm": 64,
        "D6_harmonic": True,
        "local_D6_relations_checked": harmonic_checks,
        "uniform_mean_exact": "0",
        "balanced_slice_moments_order_0_to_12": [str(x) for x in moments],
        "lambda6_exact": str(lambda6),
        "uniform_witness_variance_exact": str(variance),
        "uniform_witness_variance_interval": str(variance_arb),
        "candidate_witness_expectation_interval": str(witness_moment),
        "candidate_witness_expectation_gt_0.0032": True,
        "degree_six_chi_square_lower_bound_interval": str(degree_six_bound),
        "degree_six_chi_square_lower_bound_gt_1.3e-7": True,
        "quartic_chi_square_lower_bound_floor": str(quartic_floor),
        "combined_degree_four_plus_degree_six_chi_square_lower_bound_interval": str(combined_bound),
        "combined_lower_bound_gt_0.0823555": True,
        "quartic_certificate_status": quartic_data["status"],
        "atom_input_sha256": hashlib.sha256(ATOM_PATH.read_bytes()).hexdigest(),
        "weight_input_sha256": hashlib.sha256(WEIGHT_PATH.read_bytes()).hexdigest(),
        "quartic_certificate_sha256": hashlib.sha256(QUARTIC_PATH.read_bytes()).hexdigest(),
        "per_atom_witness_intervals": per_atom,
        "scope": (
            "This certifies one explicit degree-six harmonic witness for the frozen "
            "37-base/74-labelled period-two candidate. Its chi-square contribution "
            "adds to the degree-four harmonic contribution because the two test "
            "functions are orthogonal under the uniform balanced-slice law. It does "
            "not compute the full sixth-harmonic projection, exclude other physical "
            "measures, or imply a program-label TV, Choi, or diamond-distance bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "witness_expectation_interval": result["candidate_witness_expectation_interval"],
        "lambda6_exact": result["lambda6_exact"],
        "variance_exact": result["uniform_witness_variance_exact"],
        "degree_six_chi_square_lower_bound_interval": result[
            "degree_six_chi_square_lower_bound_interval"
        ],
        "combined_degree_four_plus_degree_six_chi_square_lower_bound_interval": result[
            "combined_degree_four_plus_degree_six_chi_square_lower_bound_interval"
        ],
        "local_D6_relations_checked": harmonic_checks,
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
