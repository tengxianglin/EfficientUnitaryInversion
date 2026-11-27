#!/usr/bin/env python3
"""Deterministic floating discovery and full quartic-orbit screen for N=42.

This is a discovery/reproducibility script only.  The mathematical claim is
certified separately by verify_n42_period_two_nine_quartic_ensemble_arb.py.
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_nine_quartic_atoms.json"
OUTPUT = ROOT / "evidence/n42_period_two_nine_quartic_discovery.json"
N, n = 42, 21
PAIR_TARGET = -1.0 / 41.0
QUARTIC_TARGET = 1.0 / 533.0
SEED = 351
CANDIDATE_COUNT = 100_000
WITNESS_10 = [0, 3, 18, 21]


def fourier_tables():
    theta = 2.0 * np.pi * np.arange(n) / n
    cos_table = np.cos(np.outer(np.arange(n), theta))
    sin_table = np.sin(np.outer(np.arange(n), theta))
    return theta, cos_table, sin_table


THETA, COS_TABLE, SIN_TABLE = fourier_tables()


def build_cs_batch(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    theta = THETA
    mu_sq = 4.0 * (
        a[:, None] ** 2 + b[:, None] ** 2
        - 2.0 * a[:, None] * b[:, None] * np.cos(theta)[None, :]
    )
    mu = np.sqrt(np.maximum(mu_sq, 0.0))
    cosine_mu = np.cos(mu)
    sinc_mu = np.divide(
        np.sin(mu), mu, out=np.ones_like(mu), where=(mu != 0.0)
    )
    C = (cosine_mu @ COS_TABLE) / n
    U = 2.0 * sinc_mu * (
        a[:, None] - b[:, None] * np.cos(theta)[None, :]
    )
    V = 2.0 * sinc_mu * (b[:, None] * np.sin(theta)[None, :])
    S = (U @ COS_TABLE + V @ SIN_TABLE) / n
    return C, S


def pair_features(C, S):
    same = C[:, 0, None] ** 2 - C[:, 1:11] ** 2
    cross = -C[:, 0, None] ** 2 - S[:, :20] ** 2
    return np.column_stack((same, cross))


def quartic_minor_batch(indices, C, S):
    indices = list(indices)
    M = np.empty((len(C), 4, 4), dtype=float)
    for p, i in enumerate(indices):
        for q, j in enumerate(indices):
            if i % 2 == 0 and j % 2 == 0:
                M[:, p, q] = C[:, (j // 2 - i // 2) % n]
            elif i % 2 == 1 and j % 2 == 1:
                M[:, p, q] = -C[:, (j // 2 - i // 2) % n]
            elif i % 2 == 0 and j % 2 == 1:
                M[:, p, q] = -S[:, (j // 2 - i // 2) % n]
            else:
                M[:, p, q] = -S[:, (i // 2 - j // 2) % n]
    return np.linalg.det(M)


def sym_quartic_feature(indices, C, S):
    shifted = [((i + 1) % N) for i in indices]
    return (
        quartic_minor_batch(indices, C, S)
        + quartic_minor_batch(shifted, C, S)
    ) / 2.0


def canonical_orbit(indices):
    return min(
        tuple(sorted((i + shift) % N for i in indices))
        for shift in range(N)
    )


def all_quartic_orbits():
    members = {}
    for I in itertools.combinations(range(N), 4):
        key = canonical_orbit(I)
        members.setdefault(key, set()).add(I)
    return sorted(members), members


def solve_float_weights(atoms, witnesses):
    a = np.asarray([float(x["a"]) for x in atoms])
    b = np.asarray([float(x["b"]) for x in atoms])
    C, S = build_cs_batch(a, b)
    pairs = pair_features(C, S)
    quartics = np.column_stack([
        sym_quartic_feature(I, C, S) for I in witnesses
    ])
    A = np.vstack((pairs.T, quartics.T, np.ones((1, len(atoms)))))
    rhs = np.r_[
        np.full(30, PAIR_TARGET),
        np.full(len(witnesses), QUARTIC_TARGET),
        1.0,
    ]
    weights = np.linalg.solve(A, rhs)
    return C, S, A, rhs, weights


def scan_all_quartics(atoms, witnesses):
    C, S, A, rhs, weights = solve_float_weights(atoms, witnesses)
    reps, members = all_quartic_orbits()
    values = np.empty(len(reps), dtype=float)
    for r, I in enumerate(reps):
        values[r] = float(weights @ sym_quartic_feature(I, C, S))
    residuals = values - QUARTIC_TARGET
    order = np.argsort(np.abs(residuals))[::-1]
    top = [
        {
            "representative": list(reps[i]),
            "orbit_size": len(members[reps[i]]),
            "moment": float(values[i]),
            "signed_residual": float(residuals[i]),
            "absolute_residual": float(abs(residuals[i])),
        }
        for i in order[:10]
    ]
    return {
        "orbit_count": len(reps),
        "subset_count_from_orbit_sizes": sum(len(x) for x in members.values()),
        "maximum_absolute_residual": float(abs(residuals[order[0]])),
        "maximum_absolute_residual_representative": list(reps[order[0]]),
        "maximum_positive_residual": float(residuals.max()),
        "minimum_signed_residual": float(residuals.min()),
        "top_ten": top,
        "selected_system_condition_number": float(np.linalg.cond(A)),
        "minimum_reconstructed_weight": float(weights.min()),
        "maximum_reconstructed_weight": float(weights.max()),
    }


def main():
    frozen = json.loads(INPUT.read_text())
    witnesses = frozen["matched_quartic_witnesses"]
    expected_atoms = frozen["atoms"]
    rng = np.random.default_rng(SEED)
    a = rng.uniform(0.0, 100.0, CANDIDATE_COUNT)
    b = rng.uniform(0.0, 100.0, CANDIDATE_COUNT)
    C, S = build_cs_batch(a, b)
    pair = pair_features(C, S)
    qcols = np.column_stack([
        sym_quartic_feature(I, C, S) for I in witnesses
    ])
    candidate_features = np.column_stack((pair, qcols))
    Aeq = np.vstack((candidate_features.T, np.ones((1, CANDIDATE_COUNT))))
    beq = np.r_[
        np.full(30, PAIR_TARGET),
        np.full(len(witnesses), QUARTIC_TARGET),
        1.0,
    ]
    lp = linprog(
        np.zeros(CANDIDATE_COUNT),
        A_eq=Aeq,
        b_eq=beq,
        bounds=(0.0, None),
        method="highs",
    )
    if not lp.success:
        raise RuntimeError(f"nine-orbit discovery LP failed: {lp.message}")
    support = np.flatnonzero(lp.x > 1e-10)
    discovered_atoms = [
        {"a": repr(float(a[i])), "b": repr(float(b[i]))}
        for i in support
    ]
    if discovered_atoms != expected_atoms:
        raise AssertionError(
            "pinned NumPy/SciPy discovery no longer reproduces the frozen support"
        )
    selected_residual = float(np.max(np.abs(Aeq @ lp.x - beq)))

    scan = scan_all_quartics(expected_atoms, witnesses)
    if scan["orbit_count"] != 2670 or scan["subset_count_from_orbit_sizes"] != 111930:
        raise AssertionError("full quartic translation-orbit enumeration mismatch")
    if scan["maximum_absolute_residual_representative"] != WITNESS_10:
        raise AssertionError("the expected next unmatched orbit changed")

    # Discovery-only finite-pool test: append the next unmatched quartic orbit.
    q10 = sym_quartic_feature(WITNESS_10, C, S)
    Aeq10 = np.vstack((
        np.column_stack((candidate_features, q10)).T,
        np.ones((1, CANDIDATE_COUNT)),
    ))
    beq10 = np.r_[
        np.full(30, PAIR_TARGET),
        np.full(len(witnesses) + 1, QUARTIC_TARGET),
        1.0,
    ]
    lp10 = linprog(
        np.zeros(CANDIDATE_COUNT),
        A_eq=Aeq10,
        b_eq=beq10,
        bounds=(0.0, None),
        method="highs",
    )
    result = {
        "status": "reproduced_N42_period_two_nine_quartic_discovery",
        "discovery_only": True,
        "numpy_version": np.__version__,
        "scipy_version": __import__("scipy").__version__,
        "seed": SEED,
        "candidate_count": CANDIDATE_COUNT,
        "search_box": "[0,100]^2",
        "support_size": len(support),
        "selected_equation_max_residual": selected_residual,
        "frozen_input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "full_fourth_order_scan": scan,
        "tenth_orbit_finite_pool_test": {
            "representative": WITNESS_10,
            "status": "feasible" if lp10.success else "infeasible",
            "message": lp10.message,
            "scope": "Only this fixed 100000-candidate pool; not a continuum no-go."
        },
        "scope": (
            "Floating LP and NumPy scan are discovery evidence only. "
            "The independent Arb certificate is the proof for the frozen support."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "support_size": result["support_size"],
        "selected_equation_max_residual": selected_residual,
        "quartic_orbits_scanned": scan["orbit_count"],
        "quartic_subsets_covered": scan["subset_count_from_orbit_sizes"],
        "largest_unmatched_orbit": scan["maximum_absolute_residual_representative"],
        "largest_absolute_residual": scan["maximum_absolute_residual"],
        "tenth_orbit_finite_pool_status": result["tenth_orbit_finite_pool_test"]["status"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
