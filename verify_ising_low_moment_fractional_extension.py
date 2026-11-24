"""192-bit Arb screen of single fractional-segment extensions at n=21.

The frozen 22-atom low-moment ensemble is kept fixed in its 21 distance
moments, consecutive fourth probe and normalization. Each candidate
fractional segment supplies one new atom and one free weight. The old
weights are solved affinely so that the distant fourth probe {0,2,21,23}
is exactly repaired. Every candidate's weight signs are certified with Arb.

A positive result gives an exact 23-atom gapped ensemble satisfying two
fourth-order probes. A negative finite-grid result only rejects this
predeclared single-segment grid; it is not a global physical no-go.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from verify_ising_low_moment_design import build_rotation, features, probe, rational

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_fractional_extension_n21.json"
DISTANT = [0, 2, 21, 23]
OTHER = [0, 1, 2, 4]
LENGTHS = (10, 21, 30, 41, 42)
ALPHAS = ("1/8", "1/4", "1/2", "3/4", "5/4", "3/2")


def dot(weights, values):
    return sum((weights[j, 0] * values[j] for j in range(len(values))), arb(0))


def main():
    ctx.prec = 192
    raw = INPUT.read_bytes()
    data = json.loads(raw)
    assert len(data["atoms"]) == 22

    atoms = list(data["atoms"])
    rotations = [build_rotation(atom) for atom in atoms]
    columns = [features(rotation) for rotation in rotations]

    # Original square system: m_1,...,m_20, q_{0123}, normalization.
    selected_rows = list(range(20)) + [21]
    matrix = arb_mat(
        [[columns[j][i] for j in range(22)] for i in selected_rows]
        + [[arb(1) for _ in range(22)]]
    )
    rhs = arb_mat(
        [[rational(Fraction((-1) ** (d + 1), 41))] for d in range(1, 21)]
        + [[rational(Fraction(1, 533))], [arb(1)]]
    )
    determinant = matrix.det()
    if determinant.contains(0):
        raise RuntimeError("base low-moment system is not certified nonsingular")
    base_weights = matrix.solve(rhs)

    distant_old = [probe(rotation, DISTANT) for rotation in rotations]
    distant_target = rational(Fraction(1, 533))
    base_distant = dot(base_weights, distant_old)
    existing = {
        (int(atom["length"]), str(Fraction(atom["alpha"])))
        for atom in atoms if atom["kind"] == "fractional"
    }

    records = []
    feasible = []
    for length in LENGTHS:
        for alpha in ALPHAS:
            key = (length, str(Fraction(alpha)))
            if key in existing:
                continue
            atom = {"kind": "fractional", "length": length, "alpha": alpha}
            rotation = build_rotation(atom)
            column = features(rotation)
            vector = arb_mat(
                [[column[i]] for i in selected_rows] + [[arb(1)]]
            )
            response = matrix.solve(vector)
            distant_new = probe(rotation, DISTANT)
            slope = distant_new - dot(response, distant_old)

            if slope.contains(0):
                records.append({
                    "atom": atom,
                    "status": "unresolved_zero_slope",
                    "slope_interval": str(slope),
                })
                continue

            tau = (distant_target - base_distant) / slope
            old_weights = [
                base_weights[j, 0] - tau * response[j, 0]
                for j in range(22)
            ]
            tau_positive = bool(tau > 0)
            old_positive = all(weight > 0 for weight in old_weights)
            record = {
                "atom": atom,
                "status": (
                    "positive_extension"
                    if tau_positive and old_positive
                    else "negative_new_weight"
                    if not tau_positive
                    else "nonpositive_reweighted_old_weight"
                ),
                "slope_interval": str(slope),
                "new_atom_weight_interval": str(tau),
                "minimum_reweighted_old_weight_interval": str(
                    min(old_weights, key=float)
                ),
                "new_atom_distant_probe_interval": str(distant_new),
            }
            records.append(record)
            if tau_positive and old_positive:
                min_weight = min(old_weights + [tau], key=float)
                feasible.append({
                    "atom": atom,
                    "rotation": rotation,
                    "column": column,
                    "tau": tau,
                    "old_weights": old_weights,
                    "weights": old_weights + [tau],
                    "min_weight": min_weight,
                    "response": response,
                    "distant_new": distant_new,
                })

    if not feasible:
        result = {
            "status": "no_single_fractional_grid_atom_extension_found",
            "complete": True,
            "precision_bits": ctx.prec,
            "interval_backend": "python-flint / Arb",
            "base_input_sha256": hashlib.sha256(raw).hexdigest(),
            "base_atoms": 22,
            "tested_candidates": len(records),
            "records": records,
            "base_distant_probe": DISTANT,
            "base_distant_residual": str(base_distant - distant_target),
            "scope": (
                "Every listed single-segment fractional candidate was checked "
                "with 192-bit Arb. None can be added alone with a strictly "
                "positive new weight while preserving the 21 second moments, "
                "the consecutive fourth probe, normalization, and the distant "
                "fourth target. This is only a finite-grid rejection, not a "
                "no-go for multiple new atoms or general gapped couplings."
            ),
        }
        OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({
            "status": result["status"],
            "tested_candidates": len(records),
            "base_distant_residual": result["base_distant_residual"],
            "output": str(OUTPUT.relative_to(ROOT)),
        }, indent=2), flush=True)
        return

    # Deterministic selection among already interval-certified positive
    # extensions: maximize the minimum weight by midpoint, then exact key.
    feasible.sort(
        key=lambda item: (
            float(item["min_weight"]),
            item["atom"]["length"],
            Fraction(item["atom"]["alpha"]),
        ),
        reverse=True,
    )
    chosen = feasible[0]
    atom = chosen["atom"]
    rotation = chosen["rotation"]
    column = chosen["column"]
    weights = chosen["weights"]
    all_columns = columns + [column]

    if not sum(weights, arb(0)).contains(1):
        raise RuntimeError("23 exact weights do not certify normalization")

    second_residuals = []
    for i in range(21):
        target = rational(Fraction((-1) ** (i + 2), 41))
        value = sum(
            (weights[j] * all_columns[j][i] for j in range(23)), arb(0)
        )
        residual = value - target
        if not residual.contains(0):
            raise RuntimeError(f"second-moment row {i + 1} failed")
        second_residuals.append(str(residual))

    local_target = rational(Fraction(1, 533))
    local_value = sum(
        (weights[j] * all_columns[j][21] for j in range(23)), arb(0)
    )
    local_residual = local_value - local_target
    if not local_residual.contains(0):
        raise RuntimeError("consecutive fourth-order probe failed")

    distant_values = distant_old + [chosen["distant_new"]]
    distant_value = sum(
        (weights[j] * distant_values[j] for j in range(23)), arb(0)
    )
    distant_residual = distant_value - distant_target
    if not distant_residual.contains(0):
        raise RuntimeError("distant fourth-order probe failed")

    other_values = [probe(r, OTHER) for r in rotations] + [probe(rotation, OTHER)]
    other_value = sum(
        (weights[j] * other_values[j] for j in range(23)), arb(0)
    )
    other_residual = other_value - rational(Fraction(-1, 533))

    result = {
        "status": "certified_positive_23_atom_two_fourth_probe_ensemble",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "base_input_sha256": hashlib.sha256(raw).hexdigest(),
        "base_atoms": 22,
        "tested_candidates": len(records),
        "added_atom": atom,
        "added_atom_couplings": (
            "c_j=alpha*pi/4*sqrt((j+1)*(length-j-1)) for j=0,...,length-2; "
            "all remaining and wrap couplings are zero"
        ),
        "atom_count": 23,
        "new_atom_weight": str(chosen["tau"]),
        "minimum_all_weight": str(chosen["min_weight"]),
        "maximum_all_weight": str(max(weights, key=float)),
        "weight_sum_interval": str(sum(weights, arb(0))),
        "base_system_determinant": str(determinant),
        "preserved_second_moment_residuals": second_residuals,
        "consecutive_fourth_probe": [0, 1, 2, 3],
        "consecutive_fourth_residual": str(local_residual),
        "distant_fourth_probe": DISTANT,
        "distant_fourth_target": "1/533",
        "distant_fourth_residual": str(distant_residual),
        "additional_fourth_probe": OTHER,
        "additional_fourth_target": "-1/533",
        "additional_fourth_residual": str(other_residual),
        "weights": [str(weight) for weight in weights],
        "grid_records": records,
        "scope": (
            "This is an exact positive gapped physical ensemble satisfying all "
            "21 distance-averaged second moments and two specified fourth-order "
            "dihedral probes. It is not an all-fourth-order or all-even-moment "
            "uniform-program certificate and does not yet activate the long-ring "
            "joint-parity diamond theorem."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "added_atom": atom,
        "new_atom_weight": result["new_atom_weight"],
        "minimum_all_weight": result["minimum_all_weight"],
        "distant_fourth_residual": result["distant_fourth_residual"],
        "additional_fourth_residual": result["additional_fourth_residual"],
        "tested_candidates": len(records),
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
