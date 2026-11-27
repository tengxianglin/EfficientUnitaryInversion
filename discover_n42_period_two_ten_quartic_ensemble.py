#!/usr/bin/env python3
"""Deterministic floating discovery and full quartic-orbit screen for N=42.

Discovery only: exact-real weights and the stated moment equations are
certified by verify_n42_period_two_ten_quartic_ensemble_arb.py.
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_ten_quartic_atoms.json"
OUTPUT = ROOT / "evidence/n42_period_two_ten_quartic_discovery.json"
N, n = 42, 21
PAIR_TARGET, QUARTIC_TARGET = -1.0 / 41.0, 1.0 / 533.0
SEED, CANDIDATE_COUNT, SEARCH_MAX = 352, 300_000, 1000.0
NEXT_WITNESS = [0, 6, 15, 21]


def tables():
    theta = 2.0 * np.pi * np.arange(n) / n
    return theta, np.cos(np.outer(np.arange(n), theta)), np.sin(np.outer(np.arange(n), theta))


THETA, COS_TABLE, SIN_TABLE = tables()


def build_cs_batch(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    mu_sq = 4.0 * (
        a[:, None] ** 2 + b[:, None] ** 2
        - 2.0 * a[:, None] * b[:, None] * np.cos(THETA)[None, :]
    )
    mu = np.sqrt(np.maximum(mu_sq, 0.0))
    cosine_mu = np.cos(mu)
    sinc_mu = np.divide(np.sin(mu), mu, out=np.ones_like(mu), where=(mu != 0.0))
    C = (cosine_mu @ COS_TABLE) / n
    U = 2.0 * sinc_mu * (a[:, None] - b[:, None] * np.cos(THETA)[None, :])
    V = 2.0 * sinc_mu * (b[:, None] * np.sin(THETA)[None, :])
    S = (U @ COS_TABLE + V @ SIN_TABLE) / n
    return C, S


def pair_features(C, S):
    same = C[:, 0, None] ** 2 - C[:, 1:11] ** 2
    cross = -C[:, 0, None] ** 2 - S[:, :20] ** 2
    return np.column_stack((same, cross))


def quartic_minor_batch(I, C, S):
    I = list(I)
    M = np.empty((len(C), 4, 4), dtype=float)
    for p, i in enumerate(I):
        for q, j in enumerate(I):
            if i % 2 == 0 and j % 2 == 0:
                M[:, p, q] = C[:, (j // 2 - i // 2) % n]
            elif i % 2 == 1 and j % 2 == 1:
                M[:, p, q] = -C[:, (j // 2 - i // 2) % n]
            elif i % 2 == 0 and j % 2 == 1:
                M[:, p, q] = -S[:, (j // 2 - i // 2) % n]
            else:
                M[:, p, q] = -S[:, (i // 2 - j // 2) % n]
    return np.linalg.det(M)


def sym_quartic(I, C, S):
    shifted = [(i + 1) % N for i in I]
    return (quartic_minor_batch(I, C, S) + quartic_minor_batch(shifted, C, S)) / 2.0


def canonical_orbit(I):
    return min(tuple(sorted((i + s) % N for i in I)) for s in range(N))


def all_orbits():
    members = {}
    for I in itertools.combinations(range(N), 4):
        members.setdefault(canonical_orbit(I), set()).add(I)
    return sorted(members), members


def scan(atoms, witnesses):
    a = np.array([float(x["a"]) for x in atoms])
    b = np.array([float(x["b"]) for x in atoms])
    C, S = build_cs_batch(a, b)
    P = pair_features(C, S)
    Q = np.column_stack([sym_quartic(I, C, S) for I in witnesses])
    A = np.vstack((P.T, Q.T, np.ones((1, len(atoms)))))
    rhs = np.r_[np.full(30, PAIR_TARGET), np.full(len(witnesses), QUARTIC_TARGET), 1.0]
    w = np.linalg.solve(A, rhs)
    reps, members = all_orbits()
    moments = np.array([w @ sym_quartic(I, C, S) for I in reps])
    residuals = moments - QUARTIC_TARGET
    order = np.argsort(np.abs(residuals))[::-1]
    top = [{
        "representative": list(reps[i]),
        "orbit_size": len(members[reps[i]]),
        "moment": float(moments[i]),
        "signed_residual": float(residuals[i]),
        "absolute_residual": float(abs(residuals[i])),
    } for i in order[:10]]
    return A, rhs, w, {
        "orbit_count": len(reps),
        "subset_count_from_orbit_sizes": sum(len(x) for x in members.values()),
        "maximum_absolute_residual": float(abs(residuals[order[0]])),
        "maximum_absolute_residual_representative": list(reps[order[0]]),
        "minimum_signed_residual": float(residuals.min()),
        "maximum_positive_residual": float(residuals.max()),
        "top_ten": top,
        "selected_system_condition_number": float(np.linalg.cond(A)),
        "minimum_reconstructed_weight": float(w.min()),
        "maximum_reconstructed_weight": float(w.max()),
    }


def main():
    frozen = json.loads(INPUT.read_text())
    witnesses = frozen["matched_quartic_witnesses"]
    expected_atoms = frozen["atoms"]
    rng = np.random.default_rng(SEED)
    a = rng.uniform(0.0, SEARCH_MAX, CANDIDATE_COUNT)
    b = rng.uniform(0.0, SEARCH_MAX, CANDIDATE_COUNT)
    C, S = build_cs_batch(a, b)
    P = pair_features(C, S)
    Q = np.column_stack([sym_quartic(I, C, S) for I in witnesses])
    F = np.column_stack((P, Q))
    Aeq = np.vstack((F.T, np.ones((1, CANDIDATE_COUNT))))
    beq = np.r_[np.full(30, PAIR_TARGET), np.full(len(witnesses), QUARTIC_TARGET), 1.0]
    lp = linprog(np.zeros(CANDIDATE_COUNT), A_eq=Aeq, b_eq=beq,
                 bounds=(0.0, None), method="highs")
    if not lp.success:
        raise RuntimeError(f"ten-orbit discovery LP failed: {lp.message}")
    support = np.flatnonzero(lp.x > 1e-10)
    discovered = [{"a": repr(float(a[i])), "b": repr(float(b[i]))} for i in support]
    if discovered != expected_atoms:
        print(json.dumps({
            "discovered_support_size": len(discovered),
            "frozen_support_size": len(expected_atoms),
            "first_discovered_atoms": discovered[:8],
            "first_frozen_atoms": expected_atoms[:8],
            "first_mismatch_indices": [
                i for i, (x, y) in enumerate(zip(discovered, expected_atoms)) if x != y
            ][:12],
        }, indent=2), flush=True)
        raise AssertionError("pinned NumPy/SciPy LP no longer reproduces frozen support")
    selected_residual = float(np.max(np.abs(Aeq @ lp.x - beq)))
    _, _, weights, full_scan = scan(expected_atoms, witnesses)
    if full_scan["orbit_count"] != 2670 or full_scan["subset_count_from_orbit_sizes"] != 111930:
        raise AssertionError("quartic translation-orbit enumeration mismatch")
    if full_scan["maximum_absolute_residual_representative"] != NEXT_WITNESS:
        raise AssertionError("expected next unmatched quartic orbit changed")

    q11 = sym_quartic(NEXT_WITNESS, C, S)
    Aeq11 = np.vstack((
        np.column_stack((F, q11)).T,
        np.ones((1, CANDIDATE_COUNT)),
    ))
    beq11 = np.r_[
        np.full(30, PAIR_TARGET),
        np.full(len(witnesses) + 1, QUARTIC_TARGET),
        1.0,
    ]
    lp11 = linprog(np.zeros(CANDIDATE_COUNT), A_eq=Aeq11, b_eq=beq11,
                   bounds=(0.0, None), method="highs")
    result = {
        "status": "reproduced_N42_period_two_ten_quartic_discovery",
        "discovery_only": True,
        "numpy_version": np.__version__,
        "scipy_version": __import__("scipy").__version__,
        "seed": SEED,
        "candidate_count": CANDIDATE_COUNT,
        "search_box": "[0,1000]^2",
        "support_size": len(support),
        "selected_equation_max_residual": selected_residual,
        "frozen_input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "full_fourth_order_scan": full_scan,
        "eleventh_orbit_finite_pool_test": {
            "representative": NEXT_WITNESS,
            "status": "feasible" if lp11.success else "infeasible",
            "message": lp11.message,
            "scope": "Only this fixed 300000-candidate pool; not a continuum no-go."
        },
        "scope": "Floating LP and full-orbit scan are discovery only; see the independent Arb certificate.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "support_size": len(support),
        "selected_equation_max_residual": selected_residual,
        "quartic_orbits_scanned": full_scan["orbit_count"],
        "quartic_subsets_covered": full_scan["subset_count_from_orbit_sizes"],
        "next_unmatched_orbit": full_scan["maximum_absolute_residual_representative"],
        "next_unmatched_absolute_residual": full_scan["maximum_absolute_residual"],
        "eleventh_orbit_finite_pool_status": result["eleventh_orbit_finite_pool_test"]["status"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
