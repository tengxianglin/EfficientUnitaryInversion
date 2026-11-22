"""Finite numerical low/sixth/seven-eighth minimax LP on the frozen 83-column pool.

The newly added eighth row is Arb-certified to violate the 29-column witness.
This LP is still a binary64 design diagnostic: it does not certify all sixth
or eighth orbits, exact feasibility, or optimization over new physical columns.
"""
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit

EIGHTH_ROWS = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 5, 10, 15, 20, 25, 30, 35],
    [0, 1, 8, 9, 16, 17, 24, 25],
    [0, 4, 12, 16, 20, 28, 32, 36],
    [0, 2, 6, 14, 22, 30, 34, 40],
    [0, 3, 9, 14, 21, 27, 33, 39],
    [0, 1, 3, 14, 19, 24, 29, 40],
]

COUNTEREXAMPLE_SHA256 = "5ae3afde386225dc1a398643303684ac1589fc2abfcf3cf2ff177ace4b640059"


def verify_counterexample_pin():
    path = ROOT / "evidence/candidate_eighth_probe_arb_n21.json"
    raw = path.read_bytes()
    cert = json.loads(raw)
    assert hashlib.sha256((ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()).hexdigest() == COUNTEREXAMPLE_SHA256
    assert cert["candidate_input_sha256"] == COUNTEREXAMPLE_SHA256
    assert cert["strict_violation"] is True
    assert Fraction(cert["certified_error_lower_bound"]) == Fraction(1877, 2000)
    assert Fraction(cert["failed_cap"]) == Fraction(1, 3)
    assert cert["precision_bits"] >= 128
    assert tuple(cert["indices"]) == tuple(EIGHTH_ROWS[-1])
    return hashlib.sha256(raw).hexdigest()


def orbit_minor(R, indices):
    O = orbit(indices)
    return float(np.mean([np.linalg.det(R[np.ix_(J, J)]) for J in O]))


def matrix(c):
    A = np.zeros((42, 42))
    for i, value in enumerate(map(float, c[:-1])):
        A[i, i + 1] = 2 * value
        A[i + 1, i] = -2 * value
    return expm(A)


def run():
    arb_certificate_sha256 = verify_counterexample_pin()
    allc, _, prob = canonical_ensemble()
    keys = sorted(prob)
    cs = [allc[j] for j in keys]

    s = FourthMoments(21)
    low = np.array([s.features(np.array(list(map(float, c)))) for c in cs])
    low_target = s.target.copy()
    low_scale = np.r_[
        np.full(21, 1 / 41),
        np.full(len(s.keys), comb(21, 2) / comb(42, 4)),
    ]

    screen = json.loads((ROOT / "evidence/sixth_moment_screen_n21.json").read_text())["records"]
    sixth_rows = [r["indices"] for r in screen]
    six_target = np.array([float(Fraction(r["target"])) for r in screen])

    six = np.empty((len(cs), len(sixth_rows)))
    eighth = np.empty((len(cs), len(EIGHTH_ROWS)))
    for j, c in enumerate(cs):
        R = matrix(c)
        six[j] = [orbit_minor(R, I) for I in sixth_rows]
        eighth[j] = [orbit_minor(R, I) for I in EIGHTH_ROWS]

    eighth_target = np.array([
        float(Fraction((-1) ** (sum(i % 2 for i in I) + 4) * comb(21, 4), comb(42, 8)))
        for I in EIGHTH_ROWS
    ])
    eighth_scale = np.full(len(EIGHTH_ROWS), 1 / 19721)

    A = np.vstack([
        low.T / low_scale[:, None],
        six.T / (5 / 19721),
        eighth.T / eighth_scale[:, None],
    ])
    y = np.r_[
        low_target / low_scale,
        six_target / (5 / 19721),
        eighth_target / eighth_scale,
    ]

    m, n = A.shape
    aub = np.vstack([np.c_[A, -np.ones(m)], np.c_[-A, -np.ones(m)]])
    bub = np.r_[y, -y]
    result = linprog(
        np.r_[np.zeros(n), 1],
        A_ub=aub,
        b_ub=bub,
        A_eq=np.r_[np.ones(n), 0][None, :],
        b_eq=[1],
        bounds=[(0, None)] * n + [(0, None)],
        method="highs",
    )
    assert result.success

    weights = result.x[:-1]
    baseline = np.array([float(prob[j]) for j in keys])
    baseline_residual = np.abs(A @ baseline - y)
    optimized_residual = np.abs(A @ weights - y)
    split = [len(low_target), len(six_target), len(eighth_target)]
    cuts = np.cumsum([0] + split)

    return {
        "base_commit": "9f26680c96c269eb5ad0e84fd8ee5efacff132ee",
        "counterexample_arb_certificate_sha256": arb_certificate_sha256,
        "candidate_input_sha256": COUNTEREXAMPLE_SHA256,
        "input_sha256": hashlib.sha256((ROOT / "evidence/complete_sixth_certificate_input_n21.json").read_bytes()).hexdigest(),
        "sixth_screen_sha256": hashlib.sha256((ROOT / "evidence/sixth_moment_screen_n21.json").read_bytes()).hexdigest(),
        "columns": n,
        "rows": m,
        "row_blocks": {"low": split[0], "sixth_screen": split[1], "selected_eighth": split[2]},
        "solver": "scipy.optimize.linprog(method=highs), binary64 finite design only",
        "baseline_max": float(baseline_residual.max()),
        "lp_max": float(optimized_residual.max()),
        "baseline_low_max": float(baseline_residual[cuts[0]:cuts[1]].max()),
        "lp_low_max": float(optimized_residual[cuts[0]:cuts[1]].max()),
        "baseline_sixth_screen_max": float(baseline_residual[cuts[1]:cuts[2]].max()),
        "lp_sixth_screen_max": float(optimized_residual[cuts[1]:cuts[2]].max()),
        "baseline_selected_eighth_max": float(baseline_residual[cuts[2]:cuts[3]].max()),
        "lp_selected_eighth_max": float(optimized_residual[cuts[2]:cuts[3]].max()),
        "lp_objective": float(result.fun),
        "lp_positive_weights": [[int(j), float(x)] for j, x in zip(keys, weights) if x > 1e-8],
        "selected_eighth_rows": EIGHTH_ROWS,
        "selected_eighth_targets": [str(Fraction((-1) ** (sum(i % 2 for i in I) + 4) * comb(21, 4), comb(42, 8))) for I in EIGHTH_ROWS],
        "scope": "Finite LP over frozen 83-column pool, 1461 low rows, 256 screened sixth rows, and seven selected eighth rows; no complete sixth/eighth certification, exact feasibility, or physical global optimum.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
