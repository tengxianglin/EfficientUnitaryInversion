"""Deterministic floating discovery of a two-fourth-probe n=21 ensemble.

This is only a support-discovery LP. The exact physical claim is made by
verify_ising_low_moment_two_fourth_ensemble_n21.py using Arb.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog

from verify_ising_low_moment_design import build_rotation

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_two_fourth_discovery_n21.json"
N = 42
DISTANT = [0, 2, 21, 23]
ROWS = list(range(20)) + [21]


def probe(rotation, indices):
    values = []
    for shift in range(N):
        for sign in (-1, 1):
            I = [(shift + sign * j) % N for j in indices]
            values.append(np.linalg.det(rotation[np.ix_(I, I)]))
    return float(np.mean(values))


def features(rotation):
    diagonal = np.diag(rotation)
    moments = [
        np.mean(
            diagonal * np.roll(diagonal, -d)
            - rotation[np.arange(N), (np.arange(N) + d) % N]
            * rotation[(np.arange(N) + d) % N, np.arange(N)]
        )
        for d in range(1, 22)
    ]
    return np.r_[moments, probe(rotation, [0, 1, 2, 3])]


def fractional_rotation(length, alpha):
    c = alpha * np.pi / 4 * np.sqrt(
        np.arange(1, length) * np.arange(length - 1, 0, -1)
    )
    A = np.zeros((length, length))
    j = np.arange(length - 1)
    A[j, j + 1] = 2 * c
    A[j + 1, j] = -2 * c
    R = np.eye(N)
    R[:length, :length] = expm(A)
    return R


def main():
    raw = INPUT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != "d8c5a0ed699f7757d171c4e05913704fc280f9e35d0bba04ad5af768df2a7807":
        raise RuntimeError("frozen 22-atom input SHA256 changed")

    data = json.loads(raw)
    base_rotations = []
    for atom in data["atoms"]:
        Rarb = build_rotation(atom)
        base_rotations.append(np.array(
            [[float(Rarb[i, j]) for j in range(N)] for i in range(N)]
        ))
    base_columns = np.column_stack([features(R) for R in base_rotations])
    M = np.vstack([base_columns[ROWS, :], np.ones(22)])
    b = np.r_[
        [(-1) ** (d + 1) / 41 for d in range(1, 21)],
        1 / 533,
        1.0,
    ]
    p = np.linalg.solve(M, b)
    distant_old = np.array([probe(R, DISTANT) for R in base_rotations])
    delta = float(distant_old @ p - 1 / 533)

    candidates = []
    responses = []
    slopes = []
    for length in range(2, N + 1):
        for k in range(201):
            alpha = k / 100
            R = fractional_rotation(length, alpha)
            column = features(R)
            u = np.linalg.solve(M, np.r_[column[ROWS], 1.0])
            slope = probe(R, DISTANT) - distant_old @ u
            candidates.append({"kind": "fractional", "length": length, "alpha": f"{k}/100"})
            responses.append(u)
            slopes.append(slope)

    U = np.column_stack(responses)
    sigma = np.asarray(slopes)
    result = linprog(
        sigma,
        A_ub=U,
        b_ub=p,
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"fractional column-generation LP failed: {result.message}")
    old_weights = p - U @ result.x
    if np.min(old_weights) < -1e-7:
        raise RuntimeError("discovery LP returned materially negative old weights")
    if -result.fun <= delta:
        raise RuntimeError("fractional grid cannot repair the distant probe")

    selected_new = [
        {"atom": candidates[i], "weight": float(result.x[i]), "weight_fraction": str(Fraction(str(float(result.x[i])))), "slope": float(sigma[i])}
        for i in np.flatnonzero(result.x > 1e-8)
    ]
    selected_old = [
        {"base_index": int(i), "atom": data["atoms"][int(i)], "weight": float(old_weights[i])}
        for i in np.flatnonzero(old_weights > 1e-8)
    ]
    output = {
        "status": "floating_discovery_only_positive_two_probe_candidate",
        "complete": True,
        "base_input_sha256": digest,
        "candidate_count": len(candidates),
        "grid": "L=2,...,42; alpha=k/100, k=0,...,200",
        "base_distant_residual": delta,
        "maximum_distant_residual_reduction": float(-result.fun),
        "remaining_distant_residual": float(delta + result.fun),
        "selected_new_atoms": selected_new,
        "selected_old_atoms": selected_old,
        "support_size": len(selected_new) + len(selected_old),
        "minimum_old_weight": float(np.min(old_weights)),
        "minimum_new_weight": float(np.min(result.x[result.x > 1e-8])),
        "scope": (
            "Floating-point support discovery only. No physical ensemble claim "
            "is made until the frozen support is independently solved and "
            "strictly positive with Arb."
        ),
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2), flush=True)


if __name__ == "__main__":
    main()
