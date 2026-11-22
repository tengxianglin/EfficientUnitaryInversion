"""Complete 63,133-orbit sixth-order binary64 screen for the exact 152-column candidate.

This computes every sixth-order dihedral orbit (5,245,786 six-subsets total)
for the 51-support rational mixture. It is a complete floating-point screen,
not an interval certificate. Every violating orbit is persisted as an LP cut.
"""
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np

from audit_complete_sixth_moments import canonical_ensemble, orbit_keys, burnside, orbit_size_from_gaps, ROOT
from ising_fourth_moments import representative
from screen_ising_sixth_moments import orbit, target
from joint_low_six_eighth_lp import matrix

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
OUTPUT = ROOT / "evidence/candidate_152col_complete_sixth_binary64_n21.json"
N = 42
SCALE = 5 / 19721


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    candidate_raw = CANDIDATE_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    escape_raw = ESCAPE_CERT.read_bytes()
    candidate = json.loads(candidate_raw)
    lp = json.loads(lp_raw)
    escape = json.loads(escape_raw)
    candidate_sha, lp_sha, escape_sha = sha(candidate_raw), sha(lp_raw), sha(escape_raw)
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate input does not pin the 152-column LP")
    if candidate.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("candidate input does not pin the continuous escape certificate")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous escape lacks a strict Arb certificate")
    probabilities = {
        int(row["column"]): Fraction(row["probability"])
        for row in candidate["exact_probabilities"]
    }
    if sum(probabilities.values(), Fraction(0)) != 1:
        raise RuntimeError("exact probabilities do not sum to one")
    if len(probabilities) != candidate["support_size"] or 1641 not in probabilities:
        raise RuntimeError("unexpected candidate support")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != candidate["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical pool hash/count mismatch")
    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("escape couplings disagree with Arb certificate")

    support = sorted(probabilities.items())
    weights = np.asarray([float(p) for _, p in support], dtype=np.float64)
    weights /= weights.sum()
    matrices = []
    for column, _ in support:
        couplings = escape_couplings if column == 1641 else all_columns[column]
        matrices.append(matrix(couplings))
    matrices = np.asarray(matrices, dtype=np.float64)

    keys = orbit_keys(N)
    counts = burnside(N)
    if len(keys) != 63133 or len(keys) != counts["orbits"]:
        raise RuntimeError("sixth-order orbit count mismatch")
    reps = [representative(key) for key in keys]
    sizes = np.asarray([orbit_size_from_gaps(key, N) for key in keys], dtype=np.int64)
    if int(sizes.sum()) != comb(N, 6):
        raise RuntimeError("orbit sizes do not partition all six-subsets")
    targets = np.asarray([float(target(I)) for I in reps], dtype=np.float64)

    moments = np.zeros(len(keys), dtype=np.float64)
    total_sets = 0
    batch_size = 256
    for start in range(0, len(keys), batch_size):
        batch = keys[start:start + batch_size]
        groups = [orbit(representative(key), N) for key in batch]
        indices = np.asarray([subset for group in groups for subset in group], dtype=np.int64)
        ids = np.repeat(np.arange(len(batch)), [len(group) for group in groups])
        group_counts = np.bincount(ids, minlength=len(batch))
        total_sets += len(indices)
        for weight, rotation in zip(weights, matrices):
            values = np.linalg.det(rotation[indices[:, :, None], indices[:, None, :]])
            averaged = np.bincount(ids, weights=values, minlength=len(batch)) / group_counts
            moments[start:start + len(batch)] += weight * averaged
        if (start // batch_size) % 16 == 0:
            print(f"Audited sixth orbits {min(start + batch_size, len(keys))}/{len(keys)}; six-subsets {total_sets}", flush=True)

    if total_sets != comb(N, 6):
        raise RuntimeError("sixth-order orbit enumeration did not cover every six-subset")
    errors = np.abs(moments - targets) / SCALE
    worst = int(np.argmax(errors))
    top = np.argsort(errors)[::-1][:25]
    violating = np.flatnonzero(errors >= 1 / 3)
    parity = np.asarray([(-1) ** sum(i % 2 for i in I) for I in reps], dtype=np.int64)
    signed_minor_sum = float((sizes * parity) @ moments)
    expected_signed_sum = -comb(21, 3)
    if abs(signed_minor_sum - expected_signed_sum) > 1e-6:
        raise RuntimeError(f"sixth elementary-symmetric identity failed: {signed_minor_sum}")

    moment_sha = sha(moments.astype("<f8").tobytes())
    error_sha = sha(errors.astype("<f8").tobytes())
    result = {
        "status": "complete_sixth_binary64_screen_pass" if len(violating) == 0 else "complete_sixth_binary64_violations_found",
        "complete": True,
        "precision": "IEEE-754 binary64; not interval arithmetic",
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "candidate_support_size": len(support),
        "exact_probability_sum": "1",
        "escape_column_probability": str(probabilities[1641]),
        "sixth_orbits": len(keys),
        "six_subsets": total_sets,
        "burnside": counts,
        "normalized_error_scale": "5/19721",
        "maximum_normalized_error": float(errors[worst]),
        "maximum_orbit_index": worst,
        "maximum_indices": list(reps[worst]),
        "maximum_target": str(target(reps[worst])),
        "maximum_mixture_moment": float(moments[worst]),
        "violating_orbit_count_at_or_above_one_third": int(len(violating)),
        "violating_orbits": [
            {"orbit_index": int(j), "indices": list(reps[j]), "target": str(target(reps[j])),
             "mixture_moment": float(moments[j]), "normalized_error": float(errors[j])}
            for j in violating
        ],
        "top_25": [
            {"orbit_index": int(j), "indices": list(reps[j]), "target": str(target(reps[j])),
             "mixture_moment": float(moments[j]), "normalized_error": float(errors[j])}
            for j in top
        ],
        "moments_sha256_le_f64": moment_sha,
        "errors_sha256_le_f64": error_sha,
        "sixth_elementary_symmetric_signed_sum": signed_minor_sum,
        "expected_signed_sum": expected_signed_sum,
        "scope": (
            "Complete binary64 scan of all 63,133 sixth-order dihedral orbits / 5,245,786 six-subsets "
            "for the exact-rational 51-support candidate after converting its probabilities and "
            "rotation matrices to binary64. A passing screen is not a rigorous interval certificate; "
            "a failing screen gives explicit rows for LP repair."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_support_size": len(support),
        "sixth_orbits": len(keys),
        "six_subsets": total_sets,
        "maximum_normalized_error": float(errors[worst]),
        "maximum_indices": list(reps[worst]),
        "violating_orbit_count": int(len(violating)),
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
