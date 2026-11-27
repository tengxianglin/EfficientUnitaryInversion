"""256-bit Arb check of a rationalized 10-orbit dual's continuous escape.

This does NOT certify the finite 100000-column Farkas inequalities.  It
certifies an exact rational functional and one exact-rational physical point
where that functional is strictly negative.
"""
import json
from pathlib import Path

from flint import arb, ctx
from verify_n42_period_two_nine_quartic_ensemble_arb import (
    build_atom, build_tables, principal_minor, rational,
)

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_tenth_orbit_dual_escape.json"
OUTPUT = ROOT / "evidence/n42_period_two_tenth_orbit_dual_escape_arb.json"


def verify():
    data = json.loads(INPUT.read_text())
    ctx.prec = data["precision_bits"]
    N, n = 42, 21
    witnesses = data["quartic_witnesses"]
    coeffs = [rational(x) for x in data["dual_coefficients"]]
    if len(coeffs) != 41 or len(witnesses) != 10:
        raise AssertionError("unexpected dual dimension or quartic witness count")

    cosine, sine = build_tables(n)
    atom = data["escape_atom"]
    base = build_atom(atom, n, cosine, sine)
    shifted_atom = {"a": atom["b"], "b": atom["a"]}
    shifted = build_atom(shifted_atom, n, cosine, sine)

    # The first 30 pair features are the 10 same-parity and 20 cross-parity
    # independent coordinates used by the finite candidate-pool LP.
    features = list(base["features"][:30])
    for I in witnesses:
        I = list(map(int, I))
        q0 = principal_minor(I, base, n)
        q1 = principal_minor(I, shifted, n)
        features.append((q0 + q1) / 2)
    features.append(arb(1))
    if len(features) != len(coeffs):
        raise AssertionError("feature and dual dimensions differ")

    score = sum((coeffs[i] * features[i] for i in range(41)), arb(0))
    target = (
        [rational("-1/41") for _ in range(30)]
        + [rational("1/533") for _ in range(10)]
        + [arb(1)]
    )
    target_score = sum((coeffs[i] * target[i] for i in range(41)), arb(0))

    if not (score < rational("-1/4")):
        raise AssertionError(f"continuous physical escape not certified: {score}")
    if not (target_score < rational("-9/10")):
        raise AssertionError(f"target score not strictly negative: {target_score}")

    result = {
        "status": "certified_rationalized_dual_has_strictly_positive_period_two_escape",
        "precision_bits": ctx.prec,
        "dual_coefficients": data["dual_coefficients"],
        "escape_atom": atom,
        "all_cycle_couplings_strictly_positive": True,
        "target_score": str(target_score),
        "physical_escape_score": str(score),
        "quartic_witnesses": witnesses,
        "finite_pool_farkas_inequalities_certified": False,
        "global_separator": False,
        "scope": (
            "The exact rational functional has negative score on the balanced "
            "target and on this strictly-positive period-two physical atom. "
            "This refutes its use as a global separator. The finite 100000-column "
            "Farkas inequalities were not independently certified."
        ),
        "source": data["source"],
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "target_score": result["target_score"],
        "physical_escape_score": result["physical_escape_score"],
        "finite_pool_farkas_inequalities_certified": False,
        "global_separator": False,
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
