"""Arb-certified finite-grid Farkas obstruction for n=21 fractional paths.

The certificate covers every segment length L=2,...,42 and alpha=k/10,
k=0,...,20. It proves that no nonnegative mixture of any subset of these
861 atoms can repair the distant fourth probe while preserving the 22 base
constraints and keeping all 22 old weights nonnegative.

Discovery LP dual multipliers are frozen as exact rationals below. This
verifier reconstructs the base design and every candidate independently.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from verify_ising_low_moment_design import (
    features,
    probe,
    rational,
)

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
OUTPUT = ROOT / "evidence/ising_fractional_grid_cone_n21.json"
N = 42
DISTANT = [0, 2, 21, 23]
ROWS = list(range(20)) + [21]

# Rounded to 12 decimal places from a separate HiGHS max-margin dual LP,
# then converted to exact rationals. The strict Arb verifier, not the LP,
# establishes all inequalities used in the theorem.
LAMBDA = tuple(Fraction(x) for x in (
    "0",
    "20353183241/500000000000",
    "65211683959/1000000000000",
    "52663826399/500000000000",
    "0", "0",
    "4578322563/200000000000",
    "0",
    "196539673471/1000000000000",
    "0",
    "3625435111/100000000000",
    "150056261451/1000000000000",
    "2771270079/250000000000",
    "0",
    "1477212049/1000000000000",
    "0",
    "3704297139/500000000000",
    "0", "0", "0",
    "137910995831/500000000000",
    "37702853907/100000000000",
))


def dot_vector(a, b):
    return sum((a[j] * b[j] for j in range(len(b))), arb(0))


def fractional_rotation(length, alpha):
    """Exact Arb spin-path exponential, embedded in a 42x42 identity."""
    block_generator = arb_mat(length, length)
    for j in range(length - 1):
        c = alpha * arb.pi() / 4 * arb((j + 1) * (length - j - 1)).sqrt()
        block_generator[j, j + 1] = 2 * c
        block_generator[j + 1, j] = -2 * c
    block = block_generator.exp()
    rotation = arb_mat(N, N)
    for i in range(N):
        rotation[i, i] = 1
    for i in range(length):
        for j in range(length):
            rotation[i, j] = block[i, j]
    return rotation


def main():
    ctx.prec = 384
    raw = INPUT.read_bytes()
    data = json.loads(raw)
    if len(data["atoms"]) != 22:
        raise RuntimeError("frozen base design no longer has 22 atoms")

    base_rotations = []
    base_columns = []
    # Import the canonical builder only for the 22 frozen base atoms.
    from verify_ising_low_moment_design import build_rotation
    for atom in data["atoms"]:
        rotation = build_rotation(atom)
        base_rotations.append(rotation)
        base_columns.append(features(rotation))

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
    base_weights = matrix.solve(rhs)
    if not all(base_weights[j, 0] > 0 for j in range(22)):
        raise RuntimeError("base physical weights are not all strictly positive")
    if not sum((base_weights[j, 0] for j in range(22)), arb(0)).contains(1):
        raise RuntimeError("base weights do not certify normalization")

    distant_old = [probe(rotation, DISTANT) for rotation in base_rotations]
    target = rational(Fraction(1, 533))
    base_distant = dot_vector(
        [base_weights[j, 0] for j in range(22)], distant_old
    )
    delta = base_distant - target
    if not delta > 0:
        raise RuntimeError("the pinned base distant-probe residual is not positive")

    lambda_balls = [rational(x) for x in LAMBDA]
    if len(lambda_balls) != 22 or not all(x >= 0 for x in lambda_balls):
        raise RuntimeError("Farkas multipliers must be 22 nonnegative rationals")
    dual_cost = dot_vector(
        lambda_balls, [base_weights[j, 0] for j in range(22)]
    )
    if not dual_cost < delta:
        raise RuntimeError("Farkas cost does not lie strictly below the base residual")

    records = []
    minimum_slack = None
    minimum_candidate = None
    for length in range(2, N + 1):
        for numerator in range(21):
            alpha = Fraction(numerator, 10)
            rotation = fractional_rotation(length, rational(alpha))
            column = features(rotation)
            vector = arb_mat([[column[i]] for i in ROWS] + [[arb(1)]])
            response = matrix.solve(vector)
            distant_new = probe(rotation, DISTANT)
            slope = distant_new - dot_vector(
                [response[j, 0] for j in range(22)], distant_old
            )
            dual_slack = slope + dot_vector(
                lambda_balls, [response[j, 0] for j in range(22)]
            )
            if not dual_slack > 0:
                raise RuntimeError(
                    f"dual pricing is not strictly positive at L={length}, alpha={alpha}: {dual_slack}"
                )
            if minimum_slack is None or dual_slack < minimum_slack:
                minimum_slack = dual_slack
                minimum_candidate = {"length": length, "alpha": str(alpha)}
            records.append({
                "length": length,
                "alpha": str(alpha),
                "slope_interval": str(slope),
                "dual_slack_interval": str(dual_slack),
            })

    result = {
        "status": "arb_certified_finite_fractional_grid_convex_cone_obstruction",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "base_input_sha256": hashlib.sha256(raw).hexdigest(),
        "base_atoms": 22,
        "candidate_count": len(records),
        "lengths": [2, 42],
        "alpha_grid": "k/10, k=0,...,20 (inclusive)",
        "distant_probe": DISTANT,
        "distant_target": "1/533",
        "base_distant_residual_interval": str(delta),
        "farkas_lambda_exact": [str(x) for x in LAMBDA],
        "farkas_cost_interval": str(dual_cost),
        "strict_residual_gap_interval": str(delta - dual_cost),
        "minimum_dual_slack_interval": str(minimum_slack),
        "minimum_dual_slack_candidate": minimum_candidate,
        "records": records,
        "proof": (
            "For each candidate feature column v_j, let u_j=M^{-1}v_j and "
            "sigma_j=d_j-d^T u_j. The verifier certifies lambda>=0, "
            "sigma_j+lambda^T u_j>0 for all 861 candidates, and "
            "lambda^T p<Delta_0. Any nonnegative added weights tau that keep "
            "the old weights p-U tau nonnegative satisfy U tau<=p. Hence "
            "-sigma^T tau < = lambda^T U tau <= lambda^T p < Delta_0, "
            "so Delta_0+sigma^T tau>0. Thus no nonnegative mixture of any "
            "subset of this exact finite grid can repair the distant probe "
            "while preserving the 22 base constraints."
        ),
        "output": str(OUTPUT.relative_to(ROOT)),
        "scope": (
            "This is a rigorous finite-grid convex-cone obstruction for "
            "L=2,...,42 and alpha in {0,0.1,...,2}. It does not cover "
            "continuous alpha between grid points, arbitrary gapped couplings, "
            "or the full all-even-moment ensemble."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "candidate_count", "base_distant_residual_interval",
        "farkas_cost_interval", "strict_residual_gap_interval",
        "minimum_dual_slack_interval", "minimum_dual_slack_candidate",
        "base_input_sha256", "output"
    )}, indent=2), flush=True)


if __name__ == "__main__":
    main()
