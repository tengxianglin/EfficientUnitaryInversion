"""Independent interval probe for one eighth-order orbit of the pinned 29-column witness.

This uses mpmath.iv interval matrices as a discovery/independent cross-check.
For the repository's Arb-standard replay, run verify_candidate_eighth_probe_arb.py.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from audit_complete_sixth_moments import canonical_ensemble
from screen_ising_sixth_moments import orbit
from verify_candidate_eighth_bound import (
    EXPECTED_INPUT_SHA256,
    EXPECTED_KEY_SHA256,
    K,
    N,
    ROOT,
    target_eighth,
)

PROBE = (0, 1, 3, 14, 19, 24, 29, 40)


def iv_fraction(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def gaps_of(indices, n=N):
    return tuple(
        indices[(j + 1) % len(indices)] - indices[j]
        if j + 1 < len(indices)
        else n + indices[0] - indices[-1]
        for j in range(len(indices))
    )


def run(dps=22):
    mp.iv.dps = dps
    raw = (ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()
    input_sha = hashlib.sha256(raw).hexdigest()
    if input_sha != EXPECTED_INPUT_SHA256:
        raise RuntimeError("candidate input SHA256 mismatch")
    cfg = json.loads(raw)
    source = ROOT / "evidence/joint_low_six_eighth_lp_n21.json"
    source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    if source_sha != cfg["source_sha256"]:
        raise RuntimeError("joint LP source SHA256 mismatch")
    if cfg["support_size"] != 29 or len(cfg["exact_probabilities"]) != 29:
        raise RuntimeError("unexpected candidate support")
    if sum((Fraction(x["probability"]) for x in cfg["exact_probabilities"]), Fraction(0)) != 1:
        raise RuntimeError("candidate probabilities do not sum exactly to one")

    columns, _, _ = canonical_ensemble()
    group_orbit = orbit(PROBE, N)
    if len(group_orbit) != 42 or len(set(group_orbit)) != 42:
        raise RuntimeError("unexpected probe orbit")
    gaps = gaps_of(PROBE)
    if gaps != (1, 2, 11, 5, 5, 5, 11, 2):
        raise RuntimeError("probe gap fingerprint mismatch")

    moment = mp.iv.mpf(0)
    for ordinal, item in enumerate(cfg["exact_probabilities"], 1):
        column = int(item["column"])
        weight = Fraction(item["probability"])
        couplings = columns[column]
        A = mp.iv.matrix(N, N)
        for j, coupling in enumerate(couplings[:-1]):
            entry = 2 * iv_fraction(coupling)
            A[j, j + 1] = entry
            A[j + 1, j] = -entry
        R = mp.iv.expm(A)

        subtotal = mp.iv.mpf(0)
        for subset in group_orbit:
            minor = mp.iv.matrix([[R[i, j] for j in subset] for i in subset])
            subtotal += mp.iv.det(minor)
        moment += iv_fraction(weight) * subtotal / len(group_orbit)
        print(f"interval column {ordinal}/29 (source {column})", flush=True)

    target = target_eighth(PROBE)
    error = (moment - iv_fraction(target)) / iv_fraction(abs(target))
    absolute_error = abs(error)
    cap = mp.iv.mpf(1) / 3
    strict_violation = bool(absolute_error.a > cap.b)
    if not strict_violation:
        raise RuntimeError("interval did not strictly separate the probe from 1/3")

    return {
        "base_commit": "3518a8769bf6e9d325a1915c306af5a636a00ddf",
        "candidate_input_sha256": input_sha,
        "joint_lp_source_sha256": source_sha,
        "canonical_eighth_key_sha256": EXPECTED_KEY_SHA256,
        "support_size": len(cfg["exact_probabilities"]),
        "exact_probability_sum": "1",
        "indices": list(PROBE),
        "cyclic_gaps": list(gaps),
        "dihedral_orbit_size": len(group_orbit),
        "odd_index_count": sum(i % 2 for i in PROBE),
        "target": str(target),
        "interval_backend": "mpmath.iv",
        "mpmath_version": mp.__version__,
        "decimal_precision": dps,
        "principal_minor_determinant_evaluations": len(group_orbit) * len(cfg["exact_probabilities"]),
        "moment_interval": str(moment),
        "relative_error_interval": str(error),
        "absolute_error_interval": str(absolute_error),
        "strict_upper_test": "1/3",
        "absolute_error_lower_minus_cap_upper": str(absolute_error.a - cap.b),
        "strict_violation": strict_violation,
        "status": "definite_interval_counterexample_pending_Arb_replay",
        "scope": (
            "This disproves the proposed 1/3 eighth-order bound for this fixed "
            "29-column candidate. It is not the global G8 maximum and does not "
            "rule out other physical ensembles. The interval calculation uses "
            "mpmath.iv; an Arb-standard targeted replay is provided separately."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dps", type=int, default=22)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = run(args.dps)
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload)
    print(payload, end="")
