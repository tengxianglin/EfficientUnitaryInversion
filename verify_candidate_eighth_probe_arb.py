"""Arb-standard targeted replay of the eighth-order counterexample orbit."""
import argparse
import hashlib
import json
from pathlib import Path

from fractions import Fraction

import verify_candidate_eighth_bound as audit

PROBE = (0, 1, 3, 14, 19, 24, 29, 40)


def run(precision_bits=128):
    raw = (audit.ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()
    input_sha = hashlib.sha256(raw).hexdigest()
    cfg = json.loads(raw)
    audit.initialize_worker(cfg, input_sha, precision_bits)

    group_orbit = audit.ORBIT(PROBE, audit.N)
    if len(group_orbit) != 42:
        raise RuntimeError("unexpected probe orbit size")

    moment = audit.ARB(0)
    for weight, matrix in audit.BANK:
        subtotal = audit.ARB(0)
        for subset in group_orbit:
            subtotal += audit.minor(matrix, subset)
        moment += weight * subtotal / len(group_orbit)

    target = audit.target_eighth(PROBE)
    error = (moment - audit.BALL(target)) / audit.BALL(abs(target))
    absolute_error = abs(error)
    strict = absolute_error.lower() > audit.CAP
    if not strict:
        raise RuntimeError("Arb interval did not strictly certify error > 1/3")

    return {
        "base_commit": "3518a8769bf6e9d325a1915c306af5a636a00ddf",
        "candidate_input_sha256": input_sha,
        "canonical_eighth_key_sha256": audit.EXPECTED_KEY_SHA256,
        "precision_bits": precision_bits,
        "support_size": len(audit.BANK),
        "indices": list(PROBE),
        "cyclic_gaps": [1, 2, 11, 5, 5, 5, 11, 2],
        "dihedral_orbit_size": len(group_orbit),
        "target": str(target),
        "moment_interval": str(moment),
        "relative_error_interval": str(error),
        "absolute_error_lower": str(absolute_error.lower()),
        "strict_upper": "1/3",
        "strict_violation": True,
        "principal_minor_determinant_evaluations": len(group_orbit) * len(audit.BANK),
        "scope": (
            "Targeted Arb certificate for one violating eighth-order orbit of "
            "the fixed 29-column candidate; not a full G8 maximum or a no-go "
            "for other physical ensembles."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=128)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = run(args.precision_bits)
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload)
    print(payload, end="")
