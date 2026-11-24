"""Full fourth-order finite-grid test with an exact spin-symmetry reduction.

This is a floating discovery experiment. It does not certify feasibility or
infeasibility of the continuous physical family.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog

from ising_fourth_moments import FourthMoments, orbit_key
from verify_ising_low_moment_design import build_rotation

ROOT = Path(__file__).resolve().parent
WARM_CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
N = 42


def interval_midpoint(value):
    return float(value.split(" +/- ")[0].strip("[]"))


def features_from_rotation(rotation, system):
    R = np.array(
        [[float(rotation[i, j]) for j in range(N)] for i in range(N)],
        dtype=float,
    )
    i = np.arange(N)
    diagonal = np.diag(R)
    second = [
        np.mean(
            diagonal * diagonal[(i + d) % N]
            - R[i, (i + d) % N] * R[(i + d) % N, i]
        )
        for d in range(1, 22)
    ]
    I = system.indices
    values = np.linalg.det(R[I[:, :, None], I[:, None, :]])
    fourth = (
        np.bincount(system.ids, weights=values, minlength=len(system.keys))
        / system.counts
    )
    return np.r_[second, fourth]


def subset_layout(system, length):
    subsets = [()]
    for order in range(1, min(4, length) + 1):
        subsets.extend(combinations(range(length), order))
    lookup = {
        sum(1 << int(i) for i in subset): index
        for index, subset in enumerate(subsets)
    }
    masks = np.zeros(len(system.indices), dtype=np.int64)
    for column in range(4):
        indices = system.indices[:, column]
        masks |= np.where(
            indices < length,
            np.left_shift(np.int64(1), indices),
            np.int64(0),
        )
    quartet_to_minor = np.fromiter(
        (lookup[int(mask)] for mask in masks),
        dtype=np.int32,
        count=len(masks),
    )
    return subsets, quartet_to_minor


def fractional_small_rotation(length, alpha):
    c = (
        float(alpha)
        * np.pi
        / 4
        * np.sqrt(
            np.arange(1, length, dtype=float)
            * np.arange(length - 1, 0, -1, dtype=float)
        )
    )
    A = np.zeros((length, length), dtype=float)
    j = np.arange(length - 1)
    A[j, j + 1] = 2 * c
    A[j + 1, j] = -2 * c
    return expm(A)


def fractional_features(length, alpha, system, layout=None):
    if layout is None:
        layout = subset_layout(system, length)
    subsets, quartet_to_minor = layout
    small = fractional_small_rotation(length, alpha)

    minor_values = np.empty(len(subsets), dtype=float)
    minor_values[0] = 1.0
    offset = 1
    for order in range(1, min(4, length) + 1):
        selected = np.asarray(
            list(combinations(range(length), order)), dtype=np.int64
        )
        if order == 1:
            values = np.diag(small)[selected[:, 0]]
        else:
            blocks = small[
                selected[:, :, None],
                selected[:, None, :],
            ]
            values = np.linalg.det(blocks)
        minor_values[offset : offset + len(selected)] = values
        offset += len(selected)

    quartet_values = minor_values[quartet_to_minor]
    fourth = (
        np.bincount(
            system.ids,
            weights=quartet_values,
            minlength=len(system.keys),
        )
        / system.counts
    )

    R = np.eye(N)
    R[:length, :length] = small
    i = np.arange(N)
    diagonal = np.diag(R)
    second = [
        np.mean(
            diagonal * diagonal[(i + d) % N]
            - R[i, (i + d) % N] * R[(i + d) % N, i]
        )
        for d in range(1, 22)
    ]
    return np.r_[second, fourth]


def full_couplings(length, alpha):
    c = np.zeros(N, dtype=float)
    c[: length - 1] = (
        float(alpha)
        * np.pi
        / 4
        * np.sqrt(
            np.arange(1, length, dtype=float)
            * np.arange(length - 1, 0, -1, dtype=float)
        )
    )
    return c


def self_test(system):
    cases = 0
    max_block_defect = 0.0
    max_spin_defect = 0.0
    for length in (2, 7, 21, 41, 42):
        layout = subset_layout(system, length)
        for alpha in (0.17, 0.43, 0.89, 1.17, 1.83):
            block = fractional_features(length, alpha, system, layout)
            direct = system.features(full_couplings(length, alpha))
            block_defect = float(np.max(np.abs(block - direct)))
            max_block_defect = max(max_block_defect, block_defect)
            reflected = fractional_features(
                length, 2.0 - alpha, system, layout
            )
            spin_defect = float(np.max(np.abs(block - reflected)))
            max_spin_defect = max(max_spin_defect, spin_defect)
            if block_defect > 2e-10 or spin_defect > 2e-10:
                raise RuntimeError(
                    f"block/spin symmetry regression failed at L={length}, "
                    f"alpha={alpha}: block={block_defect}, spin={spin_defect}"
                )
            cases += 1
    return {
        "cases": cases,
        "max_block_feature_defect": max_block_defect,
        "max_alpha_to_two_minus_alpha_feature_defect": max_spin_defect,
        "status": "finite floating regression passed",
    }


def solve_full_grid(system, warm, warm_sha):
    base_atoms = warm["atoms"][:22]
    base_features = [
        features_from_rotation(build_rotation(atom), system)
        for atom in base_atoms
    ]

    rows = list(base_features)
    labels = [
        {"kind": "base", "base_index": i, "source_kind": atom["kind"]}
        for i, atom in enumerate(base_atoms)
    ]
    grid_index = {}
    layouts = {}
    for length in range(2, N + 1):
        layouts[length] = subset_layout(system, length)
        for k in range(101):
            if k == 0 and length != 2:
                continue
            alpha = Fraction(k, 100)
            feature = fractional_features(
                length, alpha, system, layouts[length]
            )
            grid_index[(length, k)] = len(rows)
            rows.append(feature)
            labels.append({
                "kind": "fractional",
                "length": length,
                "alpha": str(alpha),
            })

    W = np.asarray(rows, dtype=float)
    if W.shape != (4123, 1461):
        raise RuntimeError(f"unexpected candidate feature shape {W.shape}")

    warm_atoms = warm["atoms"]
    warm_weights = np.asarray(
        [interval_midpoint(value) for value in warm["weights"]],
        dtype=float,
    )
    warm_features = [
        features_from_rotation(build_rotation(atom), system)
        for atom in warm_atoms
    ]
    max_symmetry_defect = 0.0
    for atom_index, atom in enumerate(warm_atoms[22:], start=22):
        alpha = Fraction(atom["alpha"])
        reduced = min(alpha, Fraction(2) - alpha)
        scaled = reduced * 100
        if scaled.denominator != 1:
            raise RuntimeError("warm fractional atom is outside the 0.01 grid")
        key = (int(atom["length"]), int(scaled))
        if key not in grid_index:
            raise RuntimeError(f"missing reduced warm atom {key}")
        defect = float(np.max(np.abs(
            warm_features[atom_index] - W[grid_index[key]]
        )))
        max_symmetry_defect = max(max_symmetry_defect, defect)
        if defect > 2e-9:
            raise RuntimeError(
                f"spin-symmetry warm-start mismatch for {key}: {defect}"
            )

    warm_moment = warm_weights @ np.asarray(warm_features)
    warm_residual = warm_moment - system.target
    fourth_residual = warm_residual[21:]
    order = np.argsort(np.abs(fourth_residual))[::-1]
    warm_top = []
    for j in order[:20]:
        warm_top.append({
            "representative": system.representatives[int(j)],
            "canonical_gap_key": list(system.keys[int(j)]),
            "residual_midpoint": float(fourth_residual[j]),
            "target": float(system.target[21 + j]),
        })

    local_id = system.keys.index(orbit_key([0, 1, 2, 3], N))
    distant_id = system.keys.index(orbit_key([0, 2, 21, 23], N))

    cols = system.reduced_indices()
    scale = np.asarray(
        [41.0 if j < 21 else 533.0 for j in cols],
        dtype=float,
    )
    V = W[:, cols] * scale
    target = system.target[cols] * scale
    A_eq = np.vstack((V.T, np.ones((1, len(W)))))
    b_eq = np.r_[target, 1.0]

    primal = linprog(
        np.zeros(len(W)),
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=(0, None),
        method="highs-ipm",
        options={"time_limit": 1800, "presolve": True},
    )

    output = {
        "status": "finite_full_fourth_fractional_grid_numerical_diagnostic",
        "complete": True,
        "n": 21,
        "candidate_count": len(W),
        "base_atom_count": len(base_atoms),
        "fractional_grid_count": len(W) - len(base_atoms),
        "fractional_grid": (
            "L=2,...,42; alpha=k/100, k=0,...,100; "
            "one shared alpha=0 identity column"
        ),
        "symmetry_reduction": (
            "For spin j=(L-1)/2, R_(L,2-alpha)=+R_(L,alpha)^T "
            "for integer j and -R_(L,alpha)^T for half-integer j. "
            "Every even principal minor is invariant under transpose and "
            "global sign, so [0,1] covers the original [0,2] grid exactly."
        ),
        "warm_certificate_sha256": warm_sha,
        "candidate_feature_sha256_le_f64": hashlib.sha256(
            W.astype("<f8", copy=False).tobytes()
        ).hexdigest(),
        "full_feature_count": W.shape[1],
        "fourth_orbit_count": len(system.keys),
        "quartet_count": len(system.indices),
        "reduced_equations_including_normalization": len(cols) + 1,
        "exact_hierarchy_pivot_minor_determinant": "824633720832",
        "max_warm_spin_reduction_defect": max_symmetry_defect,
        "warm_start": {
            "atom_count": len(warm_atoms),
            "minimum_weight_midpoint": float(np.min(warm_weights)),
            "weight_sum_midpoint": float(np.sum(warm_weights)),
            "max_second_residual_midpoint": float(
                np.max(np.abs(warm_residual[:21]))
            ),
            "max_fourth_residual_midpoint": float(
                np.max(np.abs(fourth_residual))
            ),
            "local_probe_residual_midpoint": float(fourth_residual[local_id]),
            "distant_probe_residual_midpoint": float(fourth_residual[distant_id]),
            "top_20_fourth_residuals": warm_top,
        },
        "primal": {
            "status_code": int(primal.status),
            "message": primal.message,
            "success": bool(primal.success),
        },
        "scope": (
            "Floating finite-pool feasibility test over the exact symmetry-"
            "reduced fractional grid plus the 22 base atoms. It is not an "
            "interval certificate, a continuous-parameter theorem, or a "
            "global physical obstruction."
        ),
    }

    if primal.success:
        full_residual = W.T @ primal.x - system.target
        support = np.flatnonzero(primal.x > 1e-9)
        output["primal"].update({
            "support_size": int(len(support)),
            "minimum_positive_weight": float(np.min(primal.x[support])),
            "maximum_full_feature_residual": float(np.max(np.abs(full_residual))),
            "maximum_reduced_equation_residual": float(
                np.max(np.abs(A_eq @ primal.x - b_eq))
            ),
            "support": [
                {"candidate": labels[int(i)], "weight": float(primal.x[i])}
                for i in support
            ],
        })
        output["status"] = "floating_full_fourth_feasible_candidate_only"
    elif primal.status == 2:
        p = len(cols)
        dual = linprog(
            np.r_[-target, target, 1.0],
            A_ub=np.vstack((
                np.column_stack((V, -V, -np.ones(len(V)))),
                np.r_[np.ones(2 * p), 0.0][None, :],
            )),
            b_ub=np.r_[np.zeros(len(V)), 1.0],
            bounds=[(0, None)] * (2 * p) + [(None, None)],
            method="highs-ipm",
            options={"time_limit": 1800, "presolve": True},
        )
        output["dual"] = {
            "status_code": int(dual.status),
            "message": dual.message,
            "success": bool(dual.success),
        }
        if dual.success:
            y_scaled = dual.x[:p] - dual.x[p : 2 * p]
            y_full = np.zeros(W.shape[1], dtype=float)
            y_full[cols] = y_scaled * scale
            pricing = V @ y_scaled
            target_score = float(target @ y_scaled)
            max_column_score = float(np.max(pricing))
            gap = target_score - float(dual.x[-1])
            output["dual"].update({
                "normalized_l1_upper_bound": float(np.sum(dual.x[: 2 * p])),
                "target_score": target_score,
                "maximum_candidate_score": max_column_score,
                "threshold": float(dual.x[-1]),
                "recomputed_gap": gap,
                "maximum_pricing_constraint_violation": float(
                    np.max(pricing - dual.x[-1])
                ),
                "nonzero_coefficients": [
                    {
                        "feature_index": int(j),
                        "kind": "second" if j < 21 else "fourth",
                        "distance": int(j + 1) if j < 21 else None,
                        "representative": (
                            None if j < 21
                            else system.representatives[int(j - 21)]
                        ),
                        "coefficient": float(y_full[j]),
                    }
                    for j in np.argsort(np.abs(y_full))[::-1]
                    if abs(y_full[j]) > 1e-10
                ],
            })
            if gap > 1e-8 and output["dual"]["normalized_l1_upper_bound"] <= 1 + 1e-7:
                output["status"] = (
                    "floating_finite_grid_separator_candidate_not_arb_certified"
                )

    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test-only", action="store_true")
    args = parser.parse_args()
    system = FourthMoments(21)
    test = self_test(system)
    if args.self_test_only:
        print(json.dumps(test, indent=2))
        return
    raw = WARM_CERT.read_bytes()
    warm = json.loads(raw)
    if warm.get("status") != "arb_certified_positive_41_atom_two_fourth_probe_ensemble":
        raise RuntimeError("the pinned 41-atom Arb certificate is missing")
    if len(warm.get("atoms", [])) != 41 or len(warm.get("weights", [])) != 41:
        raise RuntimeError("unexpected 41-atom warm certificate shape")
    result = solve_full_grid(system, warm, hashlib.sha256(raw).hexdigest())
    result["self_test"] = test
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
