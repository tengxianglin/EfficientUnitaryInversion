"""384-bit Arb certificate for a positive n=21 two-fourth-probe ensemble."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from verify_ising_low_moment_design import build_rotation, features, probe, rational

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
N = 42
DISTANT = [0, 2, 21, 23]
ROWS = list(range(20)) + [21]
OLD_INDICES = (13, 16, 19)
NEW_SPECS = (
    (38, "48/25"),
    (39, "1"),
    (40, "159/100"),
    (40, "43/25"),
    (41, "23/100"),
    (41, "13/50"),
    (41, "14/25"),
    (41, "33/50"),
    (41, "67/100"),
    (41, "18/25"),
    (41, "79/100"),
    (41, "4/5"),
    (41, "22/25"),
    (41, "24/25"),
    (42, "19/50"),
    (42, "27/50"),
    (42, "22/25"),
    (42, "89/100"),
    (42, "91/100"),
)


def dot(weights, values):
    return sum((weights[j] * values[j] for j in range(len(values))), arb(0))


def main():
    ctx.prec = 384
    raw = INPUT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != "d8c5a0ed699f7757d171c4e05913704fc280f9e35d0bba04ad5af768df2a7807":
        raise RuntimeError("frozen 22-atom base input SHA256 changed")
    data = json.loads(raw)

    atoms = [data["atoms"][i] for i in OLD_INDICES]
    atoms += [
        {"kind": "fractional", "length": length, "alpha": alpha}
        for length, alpha in NEW_SPECS
    ]
    if len(atoms) != 22:
        raise RuntimeError("the selected support must contain exactly 22 atoms")

    rotations = [build_rotation(atom) for atom in atoms]
    columns = [features(rotation) for rotation in rotations]
    matrix = arb_mat(
        [[columns[j][i] for j in range(22)] for i in ROWS]
        + [[arb(1) for _ in range(22)]]
    )
    rhs = arb_mat(
        [[rational(Fraction((-1) ** (d + 1), 41))] for d in range(1, 21)]
        + [[rational(Fraction(1, 533))], [arb(1)]]
    )
    determinant = matrix.det()
    if determinant.contains(0):
        raise RuntimeError("selected 22x22 feature matrix is not certified invertible")
    weights_matrix = matrix.solve(rhs)
    weights = [weights_matrix[j, 0] for j in range(22)]
    if not all(weight > 0 for weight in weights):
        raise RuntimeError("at least one selected ensemble weight is not strictly positive")
    if not sum(weights, arb(0)).contains(1):
        raise RuntimeError("the selected weights do not certify normalization")

    second_residuals = []
    for d in range(1, 22):
        value = dot(weights, [column[d - 1] for column in columns])
        target = rational(Fraction((-1) ** (d + 1), 41))
        residual = value - target
        if not residual.contains(0):
            raise RuntimeError(f"distance moment d={d} is not certified exact")
        second_residuals.append(str(residual))

    local_value = dot(weights, [column[21] for column in columns])
    local_residual = local_value - rational(Fraction(1, 533))
    if not local_residual.contains(0):
        raise RuntimeError("consecutive fourth-order probe is not certified exact")

    distant_values = [probe(rotation, DISTANT) for rotation in rotations]
    distant_value = dot(weights, distant_values)
    distant_residual = distant_value - rational(Fraction(1, 533))
    if not distant_residual.contains(0):
        raise RuntimeError("distant fourth-order probe is not certified exact")

    other_probe = [0, 1, 2, 4]
    other_values = [probe(rotation, other_probe) for rotation in rotations]
    other_value = dot(weights, other_values)
    other_residual = other_value - rational(Fraction(-1, 533))

    result = {
        "status": "arb_certified_positive_22_atom_two_fourth_probe_ensemble",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "base_input_sha256": digest,
        "atom_count": len(atoms),
        "base_atom_indices_zero_based": list(OLD_INDICES),
        "atoms": atoms,
        "matrix_determinant_interval": str(determinant),
        "minimum_weight_interval": str(min(weights, key=float)),
        "maximum_weight_interval": str(max(weights, key=float)),
        "weight_sum_interval": str(sum(weights, arb(0))),
        "weights": [str(weight) for weight in weights],
        "distance_moment_residuals": second_residuals,
        "consecutive_fourth_probe": [0, 1, 2, 3],
        "consecutive_fourth_target": "1/533",
        "consecutive_fourth_residual": str(local_residual),
        "distant_fourth_probe": DISTANT,
        "distant_fourth_target": "1/533",
        "distant_fourth_residual": str(distant_residual),
        "additional_fourth_probe": other_probe,
        "additional_fourth_target": "-1/533",
        "additional_fourth_residual": str(other_residual),
        "scope": (
            "A rigorously certified positive physical ensemble satisfying all 21 "
            "distance-averaged second moments and two specified fourth-order "
            "dihedral probes. This is not an all-fourth-order or all-even-minor "
            "uniform-program certificate and does not activate the conditional "
            "n=21 joint-parity diamond theorem."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        key: result[key] for key in (
            "status", "atom_count", "matrix_determinant_interval",
            "minimum_weight_interval", "maximum_weight_interval",
            "weight_sum_interval", "consecutive_fourth_residual",
            "distant_fourth_residual", "additional_fourth_residual",
            "base_input_sha256"
        )
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
