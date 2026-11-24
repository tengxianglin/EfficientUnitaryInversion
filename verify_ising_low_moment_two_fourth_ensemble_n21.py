"""384-bit Arb certificate for a positive n=21 two-fourth-probe ensemble.

The deterministic floating LP supplies only a finite list of candidate atoms
and nonnegative decimal weights. This verifier reconstructs all exact
physical rotations, solves the 22 base equations with Arb, rescales the
candidate weights so the distant fourth probe is exact, and certifies every
old and new ensemble weight strictly positive.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from verify_ising_low_moment_design import build_rotation, features, probe, rational

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
DISCOVERY = ROOT / "evidence/ising_low_moment_two_fourth_discovery_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
N = 42
DISTANT = [0, 2, 21, 23]
ROWS = list(range(20)) + [21]


def dot(weights, values):
    return sum((weights[j] * values[j] for j in range(len(values))), arb(0))


def main():
    ctx.prec = 384
    raw = INPUT.read_bytes()
    base_sha = hashlib.sha256(raw).hexdigest()
    if base_sha != "d8c5a0ed699f7757d171c4e05913704fc280f9e35d0bba04ad5af768df2a7807":
        raise RuntimeError("frozen 22-atom base input SHA256 changed")
    data = json.loads(raw)
    discovery_raw = DISCOVERY.read_bytes()
    discovery_sha = hashlib.sha256(discovery_raw).hexdigest()
    discovery = json.loads(discovery_raw)
    if discovery.get("status") != "floating_discovery_only_positive_two_probe_candidate":
        raise RuntimeError("unexpected fractional discovery status")
    if discovery.get("base_input_sha256") != base_sha:
        raise RuntimeError("discovery does not pin the current base input")
    selected = discovery.get("selected_new_atoms", [])
    if len(selected) != 19:
        raise RuntimeError(f"expected 19 new fractional atoms, found {len(selected)}")

    base_atoms = list(data["atoms"])
    base_rotations = [build_rotation(atom) for atom in base_atoms]
    base_columns = [features(rotation) for rotation in base_rotations]
    matrix = arb_mat(
        [[base_columns[j][i] for j in range(22)] for i in ROWS]
        + [[arb(1) for _ in range(22)]]
    )
    rhs = arb_mat(
        [[rational(Fraction((-1) ** (d + 1), 41))] for d in range(1, 21)]
        + [[rational(Fraction(1, 533))], [arb(1)]]
    )
    determinant = matrix.det()
    if determinant.contains(0):
        raise RuntimeError("base 22x22 feature matrix is not certified invertible")
    base_weights_matrix = matrix.solve(rhs)
    base_weights = [base_weights_matrix[j, 0] for j in range(22)]
    if not all(weight > 0 for weight in base_weights):
        raise RuntimeError("the original 22-atom ensemble is not strictly positive")
    if not sum(base_weights, arb(0)).contains(1):
        raise RuntimeError("base weights do not certify normalization")

    distant_old = [probe(rotation, DISTANT) for rotation in base_rotations]
    target = rational(Fraction(1, 533))
    base_distant = dot(base_weights, distant_old)
    delta = base_distant - target
    if not delta > 0:
        raise RuntimeError("the pinned base distant-probe residual is not positive")

    new_atoms = []
    new_rotations = []
    new_columns = []
    new_tau = []
    responses = []
    slopes = []
    for item in selected:
        atom = item["atom"]
        if atom.get("kind") != "fractional":
            raise RuntimeError("new discovery atom is not a fractional path")
        tau = rational(Fraction(item["weight_fraction"]))
        if not tau > 0:
            raise RuntimeError("discovery supplied a nonpositive candidate weight")
        rotation = build_rotation(atom)
        column = features(rotation)
        vector = arb_mat([[column[i]] for i in ROWS] + [[arb(1)]])
        response = matrix.solve(vector)
        distant_new = probe(rotation, DISTANT)
        slope = distant_new - dot(
            [response[j, 0] for j in range(22)], distant_old
        )
        new_atoms.append(atom)
        new_rotations.append(rotation)
        new_columns.append(column)
        new_tau.append(tau)
        responses.append(response)
        slopes.append(slope)

    repair = -sum((slopes[j] * new_tau[j] for j in range(len(new_tau))), arb(0))
    if not repair > delta:
        raise RuntimeError(
            f"candidate mixture does not repair the base residual: repair={repair}, delta={delta}"
        )
    scale = delta / repair
    if not scale > 0 or not scale < 1:
        raise RuntimeError("the exact interpolation scale is not strictly between zero and one")

    old_weights = []
    for i in range(22):
        correction = sum(
            (responses[j][i, 0] * new_tau[j] for j in range(len(new_tau))),
            arb(0),
        )
        old_weights.append(base_weights[i] - scale * correction)
    new_weights = [scale * tau for tau in new_tau]
    weights = old_weights + new_weights
    atoms = base_atoms + new_atoms
    rotations = base_rotations + new_rotations
    columns = base_columns + new_columns
    if not all(weight > 0 for weight in weights):
        raise RuntimeError("the rescaled 41-atom ensemble has a nonpositive weight")
    weight_sum = sum(weights, arb(0))
    if not weight_sum.contains(1):
        raise RuntimeError("the rescaled ensemble does not certify normalization")

    second_residuals = []
    for d in range(1, 22):
        value = dot(weights, [column[d - 1] for column in columns])
        required = rational(Fraction((-1) ** (d + 1), 41))
        residual = value - required
        if not residual.contains(0):
            raise RuntimeError(f"distance moment d={d} is not certified exact")
        second_residuals.append(str(residual))

    local_value = dot(weights, [column[21] for column in columns])
    local_residual = local_value - target
    if not local_residual.contains(0):
        raise RuntimeError("consecutive fourth-order probe is not certified exact")

    distant_values = [probe(rotation, DISTANT) for rotation in rotations]
    distant_value = dot(weights, distant_values)
    distant_residual = distant_value - target
    if not distant_residual.contains(0):
        raise RuntimeError(
            f"distant fourth-order probe is not certified exact: {distant_residual}"
        )

    additional_probes = {}
    for indices, required in (
        ((0, 1, 2, 4), Fraction(-1, 533)),
        ((0, 10, 20, 30), Fraction(1, 533)),
    ):
        values = [probe(rotation, list(indices)) for rotation in rotations]
        residual = dot(weights, values) - rational(required)
        additional_probes[str(list(indices))] = {
            "target": str(required),
            "residual_interval": str(residual),
            "strictly_nonzero": not residual.contains(0),
        }

    result = {
        "status": "arb_certified_positive_41_atom_two_fourth_probe_ensemble",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "base_input_sha256": base_sha,
        "discovery_sha256": discovery_sha,
        "base_atom_count": len(base_atoms),
        "new_fractional_atom_count": len(new_atoms),
        "atom_count": len(atoms),
        "base_matrix_determinant_interval": str(determinant),
        "base_distant_residual_interval": str(delta),
        "candidate_repair_before_scaling_interval": str(repair),
        "interpolation_scale_interval": str(scale),
        "minimum_weight_interval": str(min(weights, key=float)),
        "maximum_weight_interval": str(max(weights, key=float)),
        "weight_sum_interval": str(weight_sum),
        "atoms": atoms,
        "weights": [str(weight) for weight in weights],
        "distance_moment_residuals": second_residuals,
        "consecutive_fourth_probe": [0, 1, 2, 3],
        "consecutive_fourth_target": "1/533",
        "consecutive_fourth_residual": str(local_residual),
        "distant_fourth_probe": DISTANT,
        "distant_fourth_target": "1/533",
        "distant_fourth_residual": str(distant_residual),
        "additional_fourth_probes": additional_probes,
        "scope": (
            "A rigorously certified positive 41-atom physical ensemble satisfying "
            "all 21 distance-averaged second moments, the consecutive fourth-order "
            "dihedral probe, and the distant fourth-order dihedral probe. This is "
            "not an all-fourth-order or all-even-principal-minor uniform-program "
            "certificate and does not activate the conditional n=21 joint-parity "
            "diamond theorem."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        key: result[key] for key in (
            "status", "atom_count", "base_matrix_determinant_interval",
            "base_distant_residual_interval", "candidate_repair_before_scaling_interval",
            "interpolation_scale_interval", "minimum_weight_interval",
            "maximum_weight_interval", "weight_sum_interval",
            "consecutive_fourth_residual", "distant_fourth_residual",
            "additional_fourth_probes", "base_input_sha256", "discovery_sha256"
        )
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
