"""768-bit Arb refinement of the two zero-containing fractional slopes."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx
from verify_ising_low_moment_design import build_rotation, features, probe, rational

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/ising_low_moment_design_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_zero_slope_refinement_n21.json"
CANDIDATES = (
    {"kind": "fractional", "length": 41, "alpha": "3/2"},
    {"kind": "fractional", "length": 42, "alpha": "5/4"},
)
DISTANT = [0, 2, 21, 23]


def dot(weights, values):
    return sum((weights[j, 0] * values[j] for j in range(len(values))), arb(0))


def main():
    ctx.prec = 768
    raw = INPUT.read_bytes()
    data = json.loads(raw)
    assert len(data["atoms"]) == 22
    rotations = [build_rotation(atom) for atom in data["atoms"]]
    columns = [features(rotation) for rotation in rotations]
    rows = list(range(20)) + [21]
    matrix = arb_mat(
        [[columns[j][i] for j in range(22)] for i in rows]
        + [[arb(1) for _ in range(22)]]
    )
    rhs = arb_mat(
        [[rational(Fraction((-1) ** (d + 1), 41))] for d in range(1, 21)]
        + [[rational(Fraction(1, 533))], [arb(1)]]
    )
    determinant = matrix.det()
    if determinant.contains(0):
        raise RuntimeError("base 22-atom matrix is not certified nonsingular")
    weights = matrix.solve(rhs)
    distant_old = [probe(rotation, DISTANT) for rotation in rotations]
    target = rational(Fraction(1, 533))
    base_residual = dot(weights, distant_old) - target

    records = []
    for atom in CANDIDATES:
        rotation = build_rotation(atom)
        column = features(rotation)
        vector = arb_mat([[column[i]] for i in rows] + [[arb(1)]])
        response = matrix.solve(vector)
        distant_new = probe(rotation, DISTANT)
        slope = distant_new - dot(response, distant_old)
        record = {
            "atom": atom,
            "slope_interval": str(slope),
            "strictly_positive": bool(slope > 0),
            "strictly_negative": bool(slope < 0),
            "contains_zero": bool(slope.contains(0)),
        }
        if atom["length"] == 41 and atom["alpha"] == "3/2":
            record.update({
                "exact_even_minor_equivalent_base_atom": {"kind": "fractional", "length": 41, "alpha": "1/2"},
                "strictly_zero_by_analytic_identity": True,
                "identity": (
                    "For spin j=20, exp((3*pi/2) J_y)=exp((-pi/2) J_y) because "
                    "exp(2*pi*J_y)=I; exp((-pi/2) J_y) is the transpose of "
                    "exp((pi/2) J_y), and transposition preserves every principal minor."
                ),
            })
        elif atom["length"] == 42 and atom["alpha"] == "5/4":
            record.update({
                "exact_even_minor_equivalent_base_atom": {"kind": "fractional", "length": 42, "alpha": "3/4"},
                "strictly_zero_by_analytic_identity": True,
                "identity": (
                    "For spin j=41/2, exp(2*pi*J_y)=-I; hence exp((5*pi/4)J_y) "
                    "=-exp((-3*pi/4)J_y). Every even-order principal minor is "
                    "invariant under global sign, and transposition maps the "
                    "negative-angle rotation to the positive-angle rotation."
                ),
            })
        if not slope.contains(0):
            raise RuntimeError("analytic duplicate identity disagrees with Arb slope interval")
        if not slope.contains(0):
            tau = -base_residual / slope
            old_weights = [weights[j, 0] - tau * response[j, 0] for j in range(22)]
            record.update({
                "required_new_weight_interval": str(tau),
                "required_weight_strictly_positive": bool(tau > 0),
                "all_reweighted_old_weights_strictly_positive": all(w > 0 for w in old_weights),
                "minimum_reweighted_old_weight": str(min(old_weights, key=float)),
            })
        records.append(record)

    result = {
        "status": "two_zero_slopes_exactly_redundant_by_spin_periodicity",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint / Arb",
        "base_input_sha256": hashlib.sha256(raw).hexdigest(),
        "base_atoms": 22,
        "base_matrix_determinant": str(determinant),
        "base_distant_probe": DISTANT,
        "base_distant_residual": str(base_residual),
        "candidates": records,
        "scope": (
            "Both 768-bit intervals contain zero, and separate exact spin-representation "
            "identities prove that these candidates have the same every-even-principal-minor "
            "feature columns as fractional seeds already present in the base 22-atom ensemble. "
            "The zero slopes are therefore exact redundancies, not unresolved numerical cases."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "precision_bits": ctx.prec,
        "candidates": records,
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
