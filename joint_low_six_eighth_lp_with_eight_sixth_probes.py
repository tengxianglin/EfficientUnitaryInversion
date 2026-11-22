"""Reweight the frozen 83-column pool against eight Arb-certified sixth-order rows."""
import hashlib
import json
import os
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit, target
from joint_low_six_eighth_lp import EIGHTH_ROWS, matrix, orbit_minor, verify_counterexample_pin
from joint_low_six_eighth_lp_with_sixth_probes import verify_sixth_probe_pin

SECOND_PREFIX_PATH = ROOT / "evidence/candidate_sixth_prefix_12row_n21.json"
SECOND_PREFIX_GIT_BLOB_SHA1 = "4827a61b30abdfdab2675eac6df557e71081294e"
SECOND_PARENT_CANDIDATE_SHA256 = "00ba81adfcbebb02137e02b75a7f180d0bf528f71a4bdaa8afe9b9e2b19b7e99"
EXPECTED_SECOND_FAILURES = [
    ([0, 1, 2, 3, 19, 22], "5/19721"),
    ([0, 1, 2, 4, 7, 15], "5/19721"),
    ([0, 1, 2, 4, 22, 40], "5/19721"),
]


def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def verify_second_prefix_pin():
    raw = SECOND_PREFIX_PATH.read_bytes()
    blob_sha = git_blob_sha1(raw)
    if blob_sha != SECOND_PREFIX_GIT_BLOB_SHA1:
        raise RuntimeError(f"second sixth-prefix Git blob SHA mismatch: {blob_sha}")
    prefix = json.loads(raw)
    if prefix["candidate_input_sha256"] != SECOND_PARENT_CANDIDATE_SHA256:
        raise RuntimeError("second prefix refers to a different 34-column parent")
    if prefix["precision_bits"] < 128 or prefix["support_size"] != 34:
        raise RuntimeError("second prefix lacks expected Arb precision/support")
    if prefix["status"] != "strict_violation" or prefix["complete"]:
        raise RuntimeError("expected strict sixth-order violations in the second prefix")
    observed = [(row["indices"], row["target"]) for row in prefix["failures"]]
    if observed != EXPECTED_SECOND_FAILURES:
        raise RuntimeError("the three newly certified sixth-order separators changed")
    if any(row["status"] != "strict_violation" for row in prefix["failures"]):
        raise RuntimeError("a second-prefix row is not a strict Arb violation")
    return prefix, blob_sha


def run():
    first_prefix, first_blob_sha = verify_sixth_probe_pin()
    second_prefix, second_blob_sha = verify_second_prefix_pin()
    eighth_certificate_sha256 = verify_counterexample_pin()

    all_columns, _, probabilities = canonical_ensemble()
    columns = sorted(probabilities)
    physical_columns = [all_columns[index] for index in columns]

    system = FourthMoments(21)
    low = np.array([
        system.features(np.array(list(map(float, couplings))))
        for couplings in physical_columns
    ])
    low_target = system.target.copy()
    low_scale = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]

    screen = json.loads((ROOT / "evidence/sixth_moment_screen_n21.json").read_text())["records"]
    screen_rows = [tuple(row["indices"]) for row in screen]
    probe_rows = [
        tuple(row["indices"])
        for prefix in (first_prefix, second_prefix)
        for row in prefix["failures"]
    ]
    sixth_rows = screen_rows + probe_rows
    sixth_targets = np.array(
        [float(Fraction(row["target"])) for row in screen]
        + [float(target(row)) for row in probe_rows]
    )

    sixth = np.empty((len(columns), len(sixth_rows)))
    eighth = np.empty((len(columns), len(EIGHTH_ROWS)))
    for column_index, couplings in enumerate(physical_columns):
        rotation = matrix(couplings)
        sixth[column_index] = [orbit_minor(rotation, row) for row in sixth_rows]
        eighth[column_index] = [orbit_minor(rotation, row) for row in EIGHTH_ROWS]

    eighth_targets = np.array([
        float(Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8)))
        for row in EIGHTH_ROWS
    ])
    sixth_scale = np.full(len(sixth_rows), 5 / 19721)
    eighth_scale = np.full(len(EIGHTH_ROWS), 1 / 19721)

    A = np.vstack([
        low.T / low_scale[:, None],
        sixth.T / sixth_scale[:, None],
        eighth.T / eighth_scale[:, None],
    ])
    y = np.r_[
        low_target / low_scale,
        sixth_targets / sixth_scale,
        eighth_targets / eighth_scale,
    ]

    row_blocks = {
        "low": len(low_target),
        "sixth_screen": len(screen_rows),
        "sixth_certified_probes": len(probe_rows),
        "selected_eighth": len(EIGHTH_ROWS),
    }
    m, n = A.shape
    if m != sum(row_blocks.values()) or n != 83 or len(probe_rows) != 8:
        raise RuntimeError(f"unexpected LP dimensions: {m} rows x {n} columns")
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
    if not result.success:
        raise RuntimeError(f"HiGHS failed: {result.message}")

    weights = result.x[:-1]
    baseline = np.array([float(probabilities[index]) for index in columns])
    baseline_residual = np.abs(A @ baseline - y)
    optimized_residual = np.abs(A @ weights - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))

    transcript = {
        "base_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "parent_candidate_input_sha256": SECOND_PARENT_CANDIDATE_SHA256,
        "sixth_prefix_transcripts": [
            {
                "parent_candidate_input_sha256": first_prefix["candidate_input_sha256"],
                "git_blob_sha1": first_blob_sha,
                "failure_rows": [row["indices"] for row in first_prefix["failures"]],
            },
            {
                "parent_candidate_input_sha256": second_prefix["candidate_input_sha256"],
                "git_blob_sha1": second_blob_sha,
                "failure_rows": [row["indices"] for row in second_prefix["failures"]],
            },
        ],
        "eighth_counterexample_arb_certificate_sha256": eighth_certificate_sha256,
        "low_input_sha256": hashlib.sha256(
            (ROOT / "evidence/full_low_moment_certificate_input_n21.json").read_bytes()
        ).hexdigest(),
        "sixth_screen_sha256": hashlib.sha256(
            (ROOT / "evidence/sixth_moment_screen_n21.json").read_bytes()
        ).hexdigest(),
        "columns": n,
        "rows": m,
        "row_blocks": row_blocks,
        "solver": "scipy.optimize.linprog(method=highs), binary64 finite design only",
        "baseline_max": float(baseline_residual.max()),
        "lp_max": float(optimized_residual.max()),
        "lp_objective": float(result.fun),
        "strict_finite_cap": "1/3",
        "finite_candidate_below_cap": bool(result.fun < 1 / 3),
        "block_maxima": {
            name: float(optimized_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "baseline_block_maxima": {
            name: float(baseline_residual[cuts[i]:cuts[i + 1]].max())
            for i, name in enumerate(row_blocks)
        },
        "lp_positive_weights": [
            [int(column), float(weight)]
            for column, weight in zip(columns, weights)
            if weight > 1e-10
        ],
        "sixth_probe_rows": [list(row) for row in probe_rows],
        "sixth_probe_targets": [str(target(row)) for row in probe_rows],
        "sixth_probe_arb_intervals": [
            {
                "indices": row["indices"],
                "target": row["target"],
                "error_interval": row["error_interval"],
                "absolute_error_lower": row["absolute_error_lower"],
                "absolute_error_upper": row["absolute_error_upper"],
            }
            for prefix in (first_prefix, second_prefix)
            for row in prefix["failures"]
        ],
        "selected_eighth_rows": EIGHTH_ROWS,
        "selected_eighth_targets": [
            str(Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8)))
            for row in EIGHTH_ROWS
        ],
        "scope": (
            "Finite binary64 minimax LP over the frozen 83-column physical pool, "
            "all 1461 low rows, 256 screened sixth rows, eight Arb-certified sixth "
            "separators from two parent candidates, and seven selected eighth rows. "
            "No exact feasibility, complete sixth/eighth maximum, or physical global "
            "optimum is implied."
        ),
    }
    return transcript


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
