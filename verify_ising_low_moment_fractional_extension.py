"""192-bit Arb test: add one fractional-transfer seed to the n=21 low-moment ensemble.

The new atom is the length-41 open segment at alpha=5/4. We preserve the
21 distance-averaged second moments, the consecutive fourth probe, and
normalization, then use the single new degree of freedom to set the
distant fourth probe {0,2,21,23} exactly to its uniform target.

A success is an exact positive-ensemble existence certificate for these
24 constraints only; it is not full program uniformity.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from verify_ising_low_moment_design import (
    build_rotation,
    features,
    probe,
    rational,
)

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_fractional_extension_n21.json"
NEW_ATOM = {"kind": "fractional", "length": 41, "alpha": "5/4"}
DISTANT = [0, 2, 21, 23]
OTHER = [0, 1, 2, 4]


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

    # The original 22-by-22 square system: m_1,...,m_20, q_{0123}, 1.
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

    # Add one exact physical fractional-transfer atom and preserve all
    # selected equations by solving old_weights = base_weights - tau*u.
    new_rotation = build_rotation(NEW_ATOM)
    new_column = features(new_rotation)
    new_vector = arb_mat(
        [[new_column[i]] for i in selected_rows] + [[arb(1)]]
    )
    response = matrix.solve(new_vector)

    distant_old = [probe(rotation, DISTANT) for rotation in rotations]
    distant_new = probe(new_rotation, DISTANT)
    distant_target = rational(Fraction(1, 533))
    base_distant = dot(base_weights, distant_old)
    slope = distant_new - dot(response, distant_old)
    if slope.contains(0):
        raise RuntimeError("new atom has unresolved zero response on distant probe")

    tau = (distant_target - base_distant) / slope
    new_old_weights = [
        base_weights[j, 0] - tau * response[j, 0] for j in range(22)
    ]
    if not tau > 0:
        raise RuntimeError("the required new-atom weight is not strictly positive")
    if not all(weight > 0 for weight in new_old_weights):
        raise RuntimeError("the reweighted original atoms are not all strictly positive")

    weights = new_old_weights + [tau]
    all_columns = columns + [new_column]
    if not sum(weights, arb(0)).contains(1):
        raise RuntimeError("23 exact weights do not certify normalization")

    # Verify all 21 second moments and the original local fourth probe.
    moment_residuals = []
    for i in range(21):
        target = rational(Fraction((-1) ** (i + 2), 41))
        value = sum((weights[j] * all_columns[j][i] for j in range(23)), arb(0))
        residual = value - target
        if not residual.contains(0):
            raise RuntimeError(f"second-moment row {i + 1} failed")
        moment_residuals.append(str(residual))

    local_target = rational(Fraction(1, 533))
    local_value = sum(
        (weights[j] * all_columns[j][21] for j in range(23)), arb(0)
    )
    local_residual = local_value - local_target
    if not local_residual.contains(0):
        raise RuntimeError("consecutive fourth-order probe failed")

    # The new free parameter was chosen to make this distant probe exact.
    distant_value = sum(
        (weights[j] * (distant_old + [distant_new])[j] for j in range(23)),
        arb(0),
    )
    distant_residual = distant_value - distant_target
    if not distant_residual.contains(0):
        raise RuntimeError("distant fourth-order probe failed")

    other_values = [probe(rotation, OTHER) for rotation in rotations] + [
        probe(new_rotation, OTHER)
    ]
    other_value = sum(
        (weights[j] * other_values[j] for j in range(23)), arb(0)
    )
    other_target = rational(Fraction(-1, 533))
    other_residual = other_value - other_target

    result = {
        "status": "certified_positive_23_atom_two_fourth_probe_ensemble",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "base_input_sha256": hashlib.sha256(raw).hexdigest(),
        "base_atoms": 22,
        "added_atom": NEW_ATOM,
        "added_atom_couplings": (
            "c_j=(5/4)*(pi/4)*sqrt((j+1)*(40-j)) for j=0,...,39; "
            "c_40=c_41=0"
        ),
        "atom_count": 23,
        "weight_floor_strictly_positive": True,
        "new_atom_weight": str(tau),
        "minimum_old_weight": str(min(new_old_weights, key=float)),
        "minimum_all_weight": str(min(weights, key=float)),
        "maximum_all_weight": str(max(weights, key=float)),
        "weight_sum_interval": str(sum(weights, arb(0))),
        "base_system_determinant": str(determinant),
        "preserved_second_moment_residuals": moment_residuals,
        "consecutive_fourth_probe": [0, 1, 2, 3],
        "consecutive_fourth_residual": str(local_residual),
        "distant_fourth_probe": DISTANT,
        "distant_fourth_target": "1/533",
        "distant_fourth_residual": str(distant_residual),
        "additional_fourth_probe": OTHER,
        "additional_fourth_target": "-1/533",
        "additional_fourth_residual": str(other_residual),
        "weights": [str(weight) for weight in weights],
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
        "new_atom_weight": result["new_atom_weight"],
        "minimum_all_weight": result["minimum_all_weight"],
        "distant_fourth_residual": result["distant_fourth_residual"],
        "additional_fourth_residual": result["additional_fourth_residual"],
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
