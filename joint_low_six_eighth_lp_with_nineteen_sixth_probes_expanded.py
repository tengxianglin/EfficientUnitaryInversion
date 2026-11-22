"""Reweight the expanded 93-column pool against nineteen Arb-certified sixth-order separators."""
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
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import EIGHTH_ROWS, matrix, orbit_minor, verify_counterexample_pin
from joint_low_six_eighth_lp_with_fourteen_sixth_probes import (
    verify_sixth_probe_pin,
    verify_second_prefix_pin,
    verify_third_prefix_pin,
)

FOURTH_PREFIX_PATH = ROOT / "evidence/candidate_sixth_prefix_14probe_n21.json"
FOURTH_PREFIX_GIT_BLOB_SHA1 = "8578b04b4af392e34b57673a24e83c0c710f8563"
FOURTH_PARENT_CANDIDATE_SHA256 = "ac789d6fa678a4759c13d3d5588253e57d63e5a448946bdd9bb915369d401d80"
EXPECTED_FOURTH_FAILURES = [
    ([0, 1, 2, 3, 19, 26], "5/19721"),
]


def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def verify_fourth_prefix_pin():
    raw = FOURTH_PREFIX_PATH.read_bytes()
    blob_sha = git_blob_sha1(raw)
    if blob_sha != FOURTH_PREFIX_GIT_BLOB_SHA1:
        raise RuntimeError(f"fourth sixth-prefix Git blob SHA mismatch: {blob_sha}")
    prefix = json.loads(raw)
    if prefix["candidate_input_sha256"] != FOURTH_PARENT_CANDIDATE_SHA256:
        raise RuntimeError("fourth prefix refers to a different 35-column parent")
    if prefix["precision_bits"] < 128 or prefix["support_size"] != 35:
        raise RuntimeError("fourth prefix lacks expected Arb precision/support")
    if prefix["status"] != "strict_violation" or prefix["complete"]:
        raise RuntimeError("expected a strict sixth-order violation in the fourth prefix")
    observed = [(row["indices"], row["target"]) for row in prefix["failures"]]
    if observed != EXPECTED_FOURTH_FAILURES:
        raise RuntimeError("the new sixth-order separator changed")
    row = prefix["failures"][0]
    if row["status"] != "strict_violation":
        raise RuntimeError("the fourth-prefix row is not a strict Arb violation")
    if Fraction(row["target"]) != Fraction(target(tuple(row["indices"]))):
        raise RuntimeError("the fourth-prefix target sign is inconsistent with parity")
    if row["absolute_error_lower"] == "":
        raise RuntimeError("the fourth-prefix certificate has no interval lower endpoint")
    return prefix, blob_sha


def run():
    first_prefix, first_blob_sha = verify_sixth_probe_pin()
    second_prefix, second_blob_sha = verify_second_prefix_pin()
    third_prefix, third_blob_sha = verify_third_prefix_pin()
    fourth_prefix, fourth_blob_sha = verify_fourth_prefix_pin()
    prefixes = (first_prefix, second_prefix, third_prefix, fourth_prefix)
    prefix_blob_shas = (first_blob_sha, second_blob_sha, third_blob_sha, fourth_blob_sha)

    extra_prefix_path = ROOT / "evidence/candidate_sixth_prefix_15probe_expanded_n21.json"
    extra_prefix_raw = extra_prefix_path.read_bytes()
    extra_prefix_blob_sha = git_blob_sha1(extra_prefix_raw)
    if extra_prefix_blob_sha != "520c98d1d6bfea8f3b5676cdece12de7ff0ec7c8":
        raise RuntimeError("the 15-probe expanded-candidate prefix transcript changed")
    extra_prefix = json.loads(extra_prefix_raw)
    if extra_prefix.get("candidate_input_sha256") != "0c7425d053162e48afd9c10e85b20ac39e54c8896ceb9bad03da3647abada4e6":
        raise RuntimeError("the extra prefix does not pin the frozen 42-column candidate")
    if extra_prefix.get("precision_bits", 0) < 128 or extra_prefix.get("status") != "strict_violation" or extra_prefix.get("complete"):
        raise RuntimeError("the extra prefix is not a 128-bit strict sixth-order rejection")
    expected_extra = [
        ([0, 1, 2, 3, 20, 21], "5/19721"),
        ([0, 1, 2, 4, 15, 40], "-5/19721"),
    ]
    observed_extra = [(row["indices"], row["target"]) for row in extra_prefix.get("failures", [])]
    if observed_extra != expected_extra or any(row.get("status") != "strict_violation" for row in extra_prefix["failures"]):
        raise RuntimeError("the two new Arb-certified sixth-order separators changed")
    for row in extra_prefix["failures"]:
        if Fraction(row["target"]) != Fraction(target(tuple(row["indices"]))):
            raise RuntimeError("an extra prefix target sign disagrees with the parity formula")
    prefixes = (*prefixes, extra_prefix)
    prefix_blob_shas = (*prefix_blob_shas, extra_prefix_blob_sha)

    latest_prefix_path = ROOT / "evidence/candidate_sixth_prefix_17probe_expanded_n21.json"
    latest_prefix_raw = latest_prefix_path.read_bytes()
    latest_prefix_blob_sha = git_blob_sha1(latest_prefix_raw)
    if latest_prefix_blob_sha != "4c4ba9931ecaf8c5b0878831d7e687ff7f5a7137":
        raise RuntimeError("the 17-probe expanded-candidate prefix transcript changed")
    latest_prefix = json.loads(latest_prefix_raw)
    if latest_prefix.get("candidate_input_sha256") != "028b3d27e291bb6963d247ee41ef8e7728c5a044b09c8c6fd02a12d2e349bfaa":
        raise RuntimeError("the latest prefix does not pin the frozen 39-column parent candidate")
    if latest_prefix.get("precision_bits", 0) < 128 or latest_prefix.get("status") != "strict_violation" or latest_prefix.get("complete"):
        raise RuntimeError("the 17-probe parent prefix is not a 128-bit strict sixth-order rejection")
    expected_latest = [
        ([0, 1, 2, 3, 21, 22], "5/19721"),
        ([0, 1, 2, 4, 11, 18], "-5/19721"),
    ]
    observed_latest = [(row["indices"], row["target"]) for row in latest_prefix.get("failures", [])]
    if observed_latest != expected_latest or any(row.get("status") != "strict_violation" for row in latest_prefix.get("failures", [])):
        raise RuntimeError("the two latest Arb-certified sixth-order separators changed")
    for row in latest_prefix["failures"]:
        if Fraction(row["target"]) != Fraction(target(tuple(row["indices"]))):
            raise RuntimeError("a latest-prefix target sign disagrees with the parity formula")
        if not row.get("absolute_error_lower"):
            raise RuntimeError("a latest-prefix strict separator has no interval lower endpoint")
    prefixes = (*prefixes, latest_prefix)
    prefix_blob_shas = (*prefix_blob_shas, latest_prefix_blob_sha)
    eighth_certificate_sha256 = verify_counterexample_pin()

    all_columns, _, probabilities = canonical_ensemble()
    base_columns = sorted(probabilities)
    all_column_array = np.asarray(all_columns, dtype="<f8")
    all_columns_sha = hashlib.sha256(all_column_array.tobytes()).hexdigest()

    base_lp_path = ROOT / "evidence/joint_low_six_eighth_lp_with_fifteen_sixth_probes_n21.json"
    base_lp_raw = base_lp_path.read_bytes()
    base_lp_sha = hashlib.sha256(base_lp_raw).hexdigest()
    cert_path = ROOT / "evidence/fifteen_probe_dual_certificate_n21.json"
    cert_raw = cert_path.read_bytes()
    cert_sha = hashlib.sha256(cert_raw).hexdigest()
    cert = json.loads(cert_raw)
    screen_path = ROOT / "evidence/fifteen_probe_dual_pricing_screen_n21.json"
    screen_raw = screen_path.read_bytes()
    screen_sha = hashlib.sha256(screen_raw).hexdigest()
    pricing_path = ROOT / "evidence/fifteen_probe_dual_pricing_arb_n21.json"
    pricing_raw = pricing_path.read_bytes()
    pricing_sha = hashlib.sha256(pricing_raw).hexdigest()
    pricing = json.loads(pricing_raw)

    if cert.get("lp_transcript_sha256") != base_lp_sha or pricing.get("lp_transcript_sha256") != base_lp_sha:
        raise RuntimeError("dual/pricing evidence does not pin the current 83-column LP transcript")
    if pricing.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("Arb pricing evidence does not pin the current dual certificate")
    if pricing.get("pricing_screen_sha256") != screen_sha:
        raise RuntimeError("Arb pricing evidence does not pin the current float screen")
    if pricing.get("canonical_all_columns_sha256_le_f64") != all_columns_sha:
        raise RuntimeError("Arb pricing evidence does not pin the current canonical column pool")
    if cert.get("status") != "strict_pool_separation" or cert.get("complete") is not True:
        raise RuntimeError("the 83-column dual certificate is not complete")
    index_hash = hashlib.sha256()
    for column in base_columns:
        index_hash.update(int(column).to_bytes(4, "little", signed=False))
    if cert.get("columns") != base_columns or cert.get("canonical_83_column_index_sha256") != index_hash.hexdigest():
        raise RuntimeError("the active 83-column index set differs from the certified dual pool")

    priced_rows = pricing.get("results", [])
    if pricing.get("status") != "arb_positive_columns_found" or pricing.get("precision_bits", 0) < 128:
        raise RuntimeError("top-column Arb pricing did not produce a 128-bit positive certificate")
    if len(priced_rows) != 10 or pricing.get("arb_certified_positive_count") != 10:
        raise RuntimeError("expected ten Arb-certified positive pricing candidates")
    new_columns = []
    for record in priced_rows:
        column = int(record["column"])
        if not record.get("strictly_positive") or column in base_columns or column < 0 or column >= len(all_columns):
            raise RuntimeError(f"invalid positive pricing candidate {column}")
        if [float(value) for value in all_columns[column]] != record["couplings"]:
            raise RuntimeError(f"priced candidate {column} does not match the canonical physical pool")
        new_columns.append(column)
    if len(set(new_columns)) != 10:
        raise RuntimeError("the ten Arb-priced columns are not distinct")
    columns = sorted(set(base_columns) | set(new_columns))
    if len(columns) != 93:
        raise RuntimeError(f"expected 93 columns after adding ten priced columns, got {len(columns)}")
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
        for prefix in prefixes
        for row in prefix["failures"]
    ]
    if len(probe_rows) != 19:
        raise RuntimeError(f"expected nineteen pinned Arb separators, got {len(probe_rows)}")
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
    if m != sum(row_blocks.values()) or n != 93:
        raise RuntimeError(f"unexpected expanded LP dimensions: {m} rows x {n} columns")
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
    inequality_marginals = np.asarray(result.ineqlin.marginals, dtype=np.float64)
    equality_marginal = float(result.eqlin.marginals[0])
    if inequality_marginals.shape != (2 * m,):
        raise RuntimeError("unexpected HiGHS inequality-dual dimension")
    dual_z = inequality_marginals[:m] - inequality_marginals[m:]
    dual_l1_norm = float(np.abs(dual_z).sum())
    dual_objective = equality_marginal + float(np.dot(dual_z, y))
    dual_max_column_lhs = float(np.max(A.T @ dual_z + equality_marginal))
    if abs(dual_objective - float(result.fun)) > 1e-7:
        raise RuntimeError("HiGHS primal/dual objectives do not agree")
    baseline = np.array([float(probabilities.get(index, Fraction(0))) for index in columns])
    baseline_residual = np.abs(A @ baseline - y)
    optimized_residual = np.abs(A @ weights - y)
    cuts = np.cumsum([0] + list(row_blocks.values()))

    transcript = {
        "base_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "parent_candidate_input_sha256": "028b3d27e291bb6963d247ee41ef8e7728c5a044b09c8c6fd02a12d2e349bfaa",
        "sixth_prefix_transcripts": [
            {
                "parent_candidate_input_sha256": prefix["candidate_input_sha256"],
                "git_blob_sha1": blob_sha,
                "failure_rows": [row["indices"] for row in prefix["failures"]],
            }
            for prefix, blob_sha in zip(prefixes, prefix_blob_shas)
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
        "base_pool_columns": base_columns,
        "added_priced_columns": sorted(new_columns),
        "pricing_arb_sha256": pricing_sha,
        "pricing_screen_sha256": screen_sha,
        "dual_certificate_sha256": cert_sha,
        "canonical_all_columns_sha256_le_f64": all_columns_sha,
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
        "dual_certificate_discovery": {
            "convention": "z = first m inequality marginals minus second m; lambda is the equality marginal for sum(weights)=1",
            "inequality_marginals": [float(value) for value in inequality_marginals],
            "equality_marginal": equality_marginal,
            "z_l1_norm": dual_l1_norm,
            "dual_objective": dual_objective,
            "max_column_lhs": dual_max_column_lhs,
            "primal_dual_objective_gap": abs(dual_objective - float(result.fun)),
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
            for prefix in prefixes
            for row in prefix["failures"]
        ],
        "selected_eighth_rows": EIGHTH_ROWS,
        "selected_eighth_targets": [
            str(Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8)))
            for row in EIGHTH_ROWS
        ],
        "scope": (
            "Finite binary64 minimax LP over the expanded 93-column physical pool (83 certified-pool columns plus ten 128-bit Arb-priced legal columns), "
            "all 1461 low rows, 256 screened sixth rows, nineteen Arb-certified sixth "
            "separators from six parent candidates, and seven selected eighth rows. "
            "The ten added columns violate the old 83-column dual inequalities; this LP is still finite binary64 discovery. No exact feasibility, complete sixth/eighth maximum, or physical global "
            "optimum is implied."
        ),
    }
    return transcript


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
