"""Exact all-orbit fourth-moment audit of the frozen N=42 partial ensemble.

The 37 period-two seeds are paired with their one-site translates.  This
makes every even-principal-minor moment D_42-invariant (reflection adds only
an alternating diagonal gauge, and a one-site shift contributes a global
minus sign to Q, invisible at even order).  Therefore one representative
per D_42 orbit is sufficient.

The exact-real weights are reconstructed from the already frozen 37x37
system.  Every one of the 1,440 quartic orbit representatives is then
priced with 256-bit Arb.  A strict residual interval excluding zero is an
exact counterexample to full fourth-order feasibility for this support.
"""
import hashlib
import json
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, arb_mat, ctx

import verify_n42_period_two_six_quartic_ensemble_arb as base

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_six_quartic_atoms.json"
OUTPUT = ROOT / "evidence/n42_period_two_six_quartic_all_orbits_arb.json"
N = 42
n = 21


def canonical_orbit(I):
    images = {
        tuple(sorted((sign * x + shift) % N for x in I))
        for sign in (1, -1)
        for shift in range(N)
    }
    return min(images), len(images)


def all_quartic_orbits():
    records = {}
    for I in combinations(range(N), 4):
        key, size = canonical_orbit(I)
        records[key] = size
    assert len(records) == 1440, len(records)
    assert sum(records.values()) == comb(N, 4), sum(records.values())
    return records


def reconstruct():
    data = json.loads(INPUT.read_text())
    ctx.prec = data["precision_bits"]
    atoms = data["atoms"]
    assert len(atoms) == 37
    cosine, sine = base.build_tables(n)
    direct = [base.build_atom(atom, n, cosine, sine) for atom in atoms]
    shifted_input = [{"a": atom["b"], "b": atom["a"]} for atom in atoms]
    shifted = [base.build_atom(atom, n, cosine, sine) for atom in shifted_input]

    rows = [
        [direct[j]["features"][i] for j in range(len(atoms))]
        for i in range(30)
    ]
    witnesses = [list(map(int, I)) for I in data["matched_quartic_witnesses"]]
    assert len(witnesses) == 6
    for I in witnesses:
        rows.append([
            (
                base.principal_minor(I, direct[j], n)
                + base.principal_minor(I, shifted[j], n)
            ) / 2
            for j in range(len(atoms))
        ])
    rows.append([arb(1) for _ in atoms])
    matrix = arb_mat(rows)
    rhs = arb_mat(
        [[base.rational("-1/41")] for _ in range(30)]
        + [[base.rational("1/533")] for _ in witnesses]
        + [[arb(1)]]
    )
    determinant = matrix.det()
    if determinant.contains(0):
        raise AssertionError("frozen 37x37 moment matrix is not certified invertible")
    weights = matrix.solve(rhs)
    floor = base.rational(data["weight_floor"])
    if not all(weights[j, 0] > floor for j in range(len(atoms))):
        raise AssertionError("strict positive exact-real weights were not certified")
    if not sum((weights[j, 0] for j in range(len(atoms))), arb(0)).contains(1):
        raise AssertionError("exact-real weights do not sum to one")
    return data, direct, shifted, weights, determinant


def verify():
    data, direct, shifted, weights, determinant = reconstruct()
    target = base.rational("1/533")
    orbit_map = all_quartic_orbits()
    rows = []
    strict = []
    strict_residuals = {}
    contains = []
    for I, orbit_size in sorted(orbit_map.items()):
        value = base.symmetrized_quartic_moment(
            list(I), direct, shifted, weights, n
        )
        residual = value - target
        record = {
            "representative": list(I),
            "orbit_size": orbit_size,
            "moment_interval": str(value),
            "residual_interval": str(residual),
            "residual_contains_zero": bool(residual.contains(0)),
        }
        rows.append(record)
        if residual.contains(0):
            contains.append(record)
        else:
            strict.append(record)
            strict_residuals[tuple(I)] = residual

    if not strict:
        raise AssertionError(
            "No strict quartic counterexample found: all 1,440 orbit intervals "
            "contain the target. This would upgrade the candidate and requires "
            "a separate full interpretation."
        )

    # Rank violations by interval midpoint only.  The chosen record is already
    # a rigorous counterexample because its Arb residual interval excludes 0;
    # this ranking is not claimed to certify the global maximum residual.
    worst = max(strict, key=lambda row: abs(float(row["residual_interval"].split(" +/- ")[0].strip("[]"))))
    assert not worst["residual_contains_zero"]

    worst_residual = strict_residuals[tuple(worst["representative"])]
    absolute_residual = worst_residual if worst_residual > 0 else -worst_residual
    program_tv_lower_bound = absolute_residual / 2
    chi_square_lower_bound = absolute_residual ** 2
    plucker_dimension = comb(N, n)
    frame_potential_target = base.rational(f"4/{plucker_dimension}")
    frame_potential_lower_bound = frame_potential_target * (1 + chi_square_lower_bound)
    if not (program_tv_lower_bound > base.rational("0.00275")):
        raise AssertionError("moment witness did not certify the stated program-TV lower bound")
    if not (chi_square_lower_bound > base.rational("3/100000")):
        raise AssertionError("moment witness did not certify the stated chi-square lower bound")

    witness_keys = {
        canonical_orbit(tuple(map(int, I)))[0]
        for I in data["matched_quartic_witnesses"]
    }
    for key in witness_keys:
        matching = next(row for row in rows if tuple(row["representative"]) == key)
        if not matching["residual_contains_zero"]:
            raise AssertionError(
                f"one of the six frozen witness orbits failed its own equation: {key}"
            )

    import hashlib
    input_sha256 = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    result = {
        "schema": "eui_n42_period_two_six_quartic_all_orbits_arb_v2",
        "status": "strict_counterexample_to_full_quartic_design_for_frozen_support",
        "N": N,
        "n": n,
        "group": "D_42",
        "precision_bits": ctx.prec,
        "input_sha256": input_sha256,
        "base_atom_count": len(direct),
        "expanded_atom_count_after_one_site_symmetrization": 2 * len(direct),
        "moment_matrix_determinant": str(determinant),
        "weight_floor": data["weight_floor"],
        "quartic_target": str(target),
        "quartic_subset_count": comb(N, 4),
        "quartic_orbit_count": len(rows),
        "quartic_orbit_size_sum": sum(row["orbit_size"] for row in rows),
        "orbits_whose_residual_interval_contains_zero": len(contains),
        "orbits_with_strict_certified_mismatch": len(strict),
        "strict_counterexample": worst,
        "program_label_tv_lower_bound_interval": str(program_tv_lower_bound),
        "program_label_tv_lower_bound_gt_0.00275": True,
        "chi_square_lower_bound_interval": str(chi_square_lower_bound),
        "chi_square_lower_bound_gt_0.00003": True,
        "plucker_dimension": plucker_dimension,
        "frame_potential_target_interval": str(frame_potential_target),
        "frame_potential_lower_bound_interval": str(frame_potential_lower_bound),
        "fourier_test_function": "f_I(S)=product_{i in I}(2*1[i in S]-1), |f_I|=1",
        "counterexample_ranking": "largest absolute Arb midpoint among strict mismatches; not a certified global maximum",
        "matched_witness_orbits": len(witness_keys),
        "all_six_frozen_witness_orbits_rechecked": True,
        "all_orbit_records": rows,
        "scope": (
            "The frozen 37-base-atom / 74-labelled-atom period-two ensemble "
            "matches all pair moments and six quartic translation orbits, but "
            "at least one of the 1,440 D_42 quartic orbit moments differs "
            "strictly from 1/533. This rejects this support, not the period-two "
            "family as a whole and not the full physical cycle family."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "quartic_orbits": result["quartic_orbit_count"],
        "quartic_subsets": result["quartic_subset_count"],
        "strict_mismatches": result["orbits_with_strict_certified_mismatch"],
        "target_contains_zero_count": result["orbits_whose_residual_interval_contains_zero"],
        "counterexample": worst,
        "program_label_tv_lower_bound": str(program_tv_lower_bound),
        "chi_square_lower_bound": str(chi_square_lower_bound),
        "frame_potential_lower_bound": str(frame_potential_lower_bound),
        "moment_matrix_determinant": str(determinant),
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
