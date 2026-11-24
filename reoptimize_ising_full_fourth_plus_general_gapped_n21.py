"""Reoptimize the complete n=21 second-/fourth-order LP after adding an Arb-certified gapped path.

The existing 6,123-column fractional pool is retained unchanged.  One exact
decimal-rational connected open-path witness is appended as column 6,124.
HiGHS output is discovery only; any new dual or primal requires a separate
independent Arb certificate.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog

from ising_fourth_moments import FourthMoments
from verify_ising_low_moment_design import build_rotation
from discover_ising_full_fourth_fractional_grid_n21 import (
    features_from_rotation,
    fractional_features,
    full_couplings,
    json_safe,
    self_test,
    subset_layout,
)

ROOT = Path(__file__).resolve().parent
WARM_CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
SEARCH = ROOT / "evidence/ising_full_fourth_general_gapped_search_n21.json"
GAPPED_ARB = ROOT / "evidence/ising_full_fourth_general_gapped_escape_arb_n21.json"
OLD_DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
OLD_CERT = ROOT / "evidence/ising_full_fourth_fractional_grid_dual_arb_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_plus_general_gapped_n21.json"
N = 42


def float_rotation(couplings):
    c = np.asarray(couplings, dtype=float)
    if c.shape != (N,) or c[-1] != 0 or np.any(c[:-1] <= 0):
        raise RuntimeError("the appended connected witness must have 41 positive edges and one wrap cut")
    A = np.zeros((N, N), dtype=float)
    j = np.arange(N - 1)
    A[j, j + 1] = 2 * c[:-1]
    A[j + 1, j] = -2 * c[:-1]
    return expm(A)


def main():
    for path in (WARM_CERT, SEARCH, GAPPED_ARB, OLD_DIAGNOSTIC, OLD_CERT):
        if not path.exists():
            raise RuntimeError(f"missing pinned input: {path.name}")
    warm_raw = WARM_CERT.read_bytes()
    search_raw = SEARCH.read_bytes()
    gapped_arb_raw = GAPPED_ARB.read_bytes()
    old_diag_raw = OLD_DIAGNOSTIC.read_bytes()
    old_cert_raw = OLD_CERT.read_bytes()
    warm = json.loads(warm_raw)
    search = json.loads(search_raw)
    gapped_arb = json.loads(gapped_arb_raw)
    old_diag = json.loads(old_diag_raw)
    old_cert = json.loads(old_cert_raw)

    if warm.get("status") != "arb_certified_positive_41_atom_two_fourth_probe_ensemble":
        raise RuntimeError("the 41-atom warm certificate is not valid")
    if old_cert.get("status") != "arb_certified_finite_6123_column_full_fourth_separator":
        raise RuntimeError("the original 6,123-column Arb certificate is not valid")
    if gapped_arb.get("status") != "arb_certified_general_gapped_separator_escape":
        raise RuntimeError("the appended gapped path is not Arb-certified")
    if old_cert.get("diagnostic_sha256") != hashlib.sha256(old_diag_raw).hexdigest():
        raise RuntimeError("old finite certificate does not pin its diagnostic")
    if search.get("pins", {}).get("finite_certificate_sha256") != hashlib.sha256(old_cert_raw).hexdigest():
        raise RuntimeError("gapped search does not pin the old finite certificate")
    if gapped_arb.get("search_sha256") != hashlib.sha256(search_raw).hexdigest():
        raise RuntimeError("gapped Arb certificate does not pin the search output")

    system = FourthMoments(21)
    test = self_test(system)
    base_atoms = warm["atoms"][:22]
    rows = [
        features_from_rotation(build_rotation(atom), system)
        for atom in base_atoms
    ]
    labels = [
        {"kind": "base", "base_index": i, "source_kind": atom["kind"]}
        for i, atom in enumerate(base_atoms)
    ]

    layouts = {}
    for length in range(2, N + 1):
        layouts[length] = subset_layout(system, length)
        max_k = 100 if (length % 2 == 1 or length == N) else 200
        for k in range(max_k + 1):
            if k == 0 and length != 2:
                continue
            feature = fractional_features(
                length,
                k / 100.0,
                system,
                layouts[length],
            )
            rows.append(feature)
            labels.append({
                "kind": "fractional",
                "length": length,
                "alpha": f"{k}/100",
            })

    if len(rows) != 6123:
        raise RuntimeError(f"expected 6,123 old columns, got {len(rows)}")

    candidate_record = search["best_connected"]
    candidate_couplings = np.asarray(
        [float(value) for value in candidate_record["couplings_exact_decimal"]],
        dtype=float,
    )
    if candidate_couplings.shape != (N,) or candidate_couplings[-1] != 0:
        raise RuntimeError("malformed connected gapped witness")
    if np.any(candidate_couplings[:-1] <= 0):
        raise RuntimeError("connected gapped witness has an internal zero or negative edge")

    candidate_rotation = float_rotation(candidate_couplings)
    candidate_feature = features_from_rotation(candidate_rotation, system)
    coefficient_by_feature = {
        int(item["feature_index"]): float(item["coefficient"])
        for item in old_diag["dual"]["nonzero_coefficients"]
    }
    old_dual = np.zeros(1461, dtype=float)
    for index, coefficient in coefficient_by_feature.items():
        old_dual[index] = coefficient
    old_score = float(old_dual @ candidate_feature)
    search_score = float(candidate_record["score_float"])
    if abs(old_score - search_score) > 2e-7:
        raise RuntimeError(
            f"full feature reconstruction disagrees with certified pricing candidate: "
            f"{old_score} vs {search_score}"
        )

    rows.append(candidate_feature)
    labels.append({
        "kind": "general_gapped",
        "source": "256-bit Arb-certified connected open path",
        "search_sha256": hashlib.sha256(search_raw).hexdigest(),
        "couplings_exact_decimal": candidate_record["couplings_exact_decimal"],
    })
    W = np.asarray(rows, dtype=float)
    if W.shape != (6124, 1461):
        raise RuntimeError(f"unexpected expanded feature matrix shape {W.shape}")

    columns = system.reduced_indices()
    scale = np.asarray(
        [41.0 if index < 21 else 533.0 for index in columns],
        dtype=float,
    )
    V = W[:, columns] * scale
    target = system.target[columns] * scale
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
        "status": "floating_full_fourth_plus_gapped_numerical_diagnostic",
        "complete": True,
        "n": 21,
        "old_candidate_count": 6123,
        "new_candidate_count": len(W),
        "appended_column_index": len(W) - 1,
        "appended_column_label": labels[-1],
        "appended_column_old_separator_score": old_score,
        "appended_column_old_separator_target_gap": (
            float(old_cert["target_score_interval"].split(" +/- ")[0].strip("[]"))
            - old_score
        ),
        "appended_column_feature_sha256_le_f64": hashlib.sha256(
            candidate_feature.astype("<f8", copy=False).tobytes()
        ).hexdigest(),
        "feature_matrix_sha256_le_f64": hashlib.sha256(
            W.astype("<f8", copy=False).tobytes()
        ).hexdigest(),
        "full_feature_count": W.shape[1],
        "fourth_orbit_count": len(system.keys),
        "quartet_count": len(system.indices),
        "independent_moment_rows": len(columns),
        "equalities_including_normalization": len(columns) + 1,
        "old_diagnostic_sha256": hashlib.sha256(old_diag_raw).hexdigest(),
        "old_finite_certificate_sha256": hashlib.sha256(old_cert_raw).hexdigest(),
        "gapped_search_sha256": hashlib.sha256(search_raw).hexdigest(),
        "gapped_arb_certificate_sha256": hashlib.sha256(gapped_arb_raw).hexdigest(),
        "warm_certificate_sha256": hashlib.sha256(warm_raw).hexdigest(),
        "block_self_test": test,
        "primal": {
            "status_code": int(primal.status),
            "message": primal.message,
            "success": bool(primal.success),
        },
        "scope": (
            "Floating discovery LP on the 6,123 old columns plus one exact-decimal "
            "general-gapped physical column. A feasible primal is only a candidate; "
            "an infeasible status and floating dual are only candidates until "
            "independently certified with Arb."
        ),
    }

    if primal.success:
        full_residual = W.T @ primal.x - system.target
        support = np.flatnonzero(primal.x > 1e-9)
        output["status"] = "floating_full_fourth_plus_gapped_feasible_candidate_only"
        output["primal"].update({
            "support_size": int(len(support)),
            "minimum_positive_weight": float(np.min(primal.x[support])),
            "maximum_full_feature_residual": float(np.max(np.abs(full_residual))),
            "maximum_reduced_equation_residual": float(
                np.max(np.abs(A_eq @ primal.x - b_eq))
            ),
            "support": [
                {
                    "candidate": labels[int(index)],
                    "weight": format(float(primal.x[index]), ".17g"),
                }
                for index in support
            ],
        })
    elif primal.status == 2:
        p = len(columns)
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
            y_scaled = dual.x[:p] - dual.x[p:2 * p]
            y_full = np.zeros(W.shape[1], dtype=float)
            y_full[columns] = y_scaled * scale
            pricing = V @ y_scaled
            target_score = float(target @ y_scaled)
            max_column_score = float(np.max(pricing))
            threshold = float(dual.x[-1])
            gap = target_score - threshold
            output["dual"].update({
                "normalized_l1_upper_bound": float(np.sum(dual.x[:2 * p])),
                "target_score": target_score,
                "maximum_candidate_score": max_column_score,
                "threshold": threshold,
                "recomputed_gap": gap,
                "maximum_pricing_constraint_violation": float(np.max(pricing - threshold)),
                "nonzero_coefficients": [
                    {
                        "feature_index": int(index),
                        "kind": "second" if index < 21 else "fourth",
                        "distance": int(index + 1) if index < 21 else None,
                        "representative": (
                            None if index < 21
                            else system.representatives[int(index - 21)]
                        ),
                        "coefficient": float(y_full[index]),
                    }
                    for index in np.argsort(np.abs(y_full))[::-1]
                    if abs(y_full[index]) > 1e-10
                ],
            })
            if gap > 1e-8 and output["dual"]["normalized_l1_upper_bound"] <= 1 + 1e-7:
                output["status"] = (
                    "floating_plus_gapped_finite_pool_separator_candidate_not_arb_certified"
                )

    serialized = json.dumps(json_safe(output), indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(serialized)
    print(json.dumps({
        "status": output["status"],
        "candidate_count": output["new_candidate_count"],
        "primal": output["primal"],
        "dual": output.get("dual"),
        "appended_column_old_separator_score": output["appended_column_old_separator_score"],
        "appended_column_old_separator_target_gap": output["appended_column_old_separator_target_gap"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
