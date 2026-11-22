"""128-bit Arb audit of every eighth-order orbit for the 29-column candidate.

The enumeration is exact and independent of floating-point moment values.
A full certificate is emitted only if all 1,408,185 orbits pass strict
interval comparisons and the orbit-size sum is C(42,8).
"""
import argparse
import hashlib
import json
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path

from eighth_orbit_enumeration import (
    enumeration_summary,
    orbit_size_from_gaps,
    representative_from_gaps,
    task_keys,
)

ROOT = Path(__file__).resolve().parent
N = 42
K = 8
PRECISION_BITS = 128
STRICT_UPPER = Fraction(1, 3)
EXPECTED_INPUT_SHA256 = "5ae3afde386225dc1a398643303684ac1589fc2abfcf3cf2ff177ace4b640059"

BANK = None
ARB = None
ARB_MAT = None
BALL = None
ORBIT = None
CAP = None


def initialize_worker(cfg, input_sha256, precision_bits):
    global BANK, ARB, ARB_MAT, BALL, ORBIT, CAP
    from flint import arb, arb_mat, ctx
    from audit_complete_sixth_moments import canonical_ensemble
    from screen_ising_sixth_moments import orbit
    from verify_ising_moment_pricing import ball
    from verify_ising_sixth_escape import rotation_entries_exact

    ctx.prec = precision_bits
    raw = (ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()
    actual_input_sha256 = hashlib.sha256(raw).hexdigest()
    if actual_input_sha256 != input_sha256 or input_sha256 != EXPECTED_INPUT_SHA256:
        raise RuntimeError("candidate input SHA256 mismatch")
    source = ROOT / "evidence/joint_low_six_eighth_lp_n21.json"
    if hashlib.sha256(source.read_bytes()).hexdigest() != cfg["source_sha256"]:
        raise RuntimeError("joint LP source SHA256 mismatch")
    if Fraction(cfg["exact_probability_sum"]) != 1:
        raise RuntimeError("candidate probabilities do not sum exactly to one")
    if cfg["support_size"] != 29 or len(cfg["exact_probabilities"]) != 29:
        raise RuntimeError("unexpected candidate support size")

    all_columns, _, _ = canonical_ensemble()
    BANK = []
    for item in cfg["exact_probabilities"]:
        column = int(item["column"])
        weight = Fraction(item["probability"])
        BANK.append((ball(weight), rotation_entries_exact(all_columns[column])))
    if len(BANK) != 29:
        raise RuntimeError("failed to reconstruct all 29 physical columns")

    ARB = arb
    ARB_MAT = arb_mat
    BALL = ball
    ORBIT = orbit
    CAP = ball(STRICT_UPPER)


def minor(E, indices):
    return ARB_MAT([[E[i][j] for j in indices] for i in indices]).det()


def target_eighth(indices):
    odd_count = sum(i % 2 for i in indices)
    return Fraction((-1) ** (odd_count + 4), 19721)


def audit_task(record):
    task_id = record["task_id"]
    spec = tuple(record["task"])
    keys = list(task_keys(N, K, spec))
    if len(keys) != record["orbits"]:
        raise RuntimeError("worker orbit count disagrees with parent enumeration")
    from eighth_orbit_enumeration import hash_keys
    if hash_keys(keys) != record["key_sha256"]:
        raise RuntimeError("worker key hash disagrees with parent enumeration")

    scanned_sets = 0
    worst_midpoint = -1.0
    worst_record = None
    for offset, key in enumerate(keys):
        indices = representative_from_gaps(key)
        group_orbit = ORBIT(indices, N)
        expected_size = orbit_size_from_gaps(key, N)
        if len(group_orbit) != expected_size:
            raise RuntimeError("explicit dihedral orbit size disagrees with gap stabilizer")

        moment = ARB(0)
        for weight, matrix in BANK:
            subtotal = ARB(0)
            for subset in group_orbit:
                subtotal += minor(matrix, subset)
            moment += weight * subtotal / len(group_orbit)

        target = target_eighth(indices)
        error = (moment - BALL(target)) / BALL(abs(target))
        absolute_error = abs(error)
        scanned_sets += len(group_orbit)

        if not (absolute_error < CAP):
            definite = absolute_error.lower() > CAP
            return {
                "task_id": task_id,
                "task": list(spec),
                "passed": False,
                "status": "definite_violation" if definite else "interval_unresolved",
                "orbits_expected": len(keys),
                "orbits_scanned": offset + 1,
                "eight_sets_scanned": scanned_sets,
                "failure_indices": list(indices),
                "failure_orbit_size": len(group_orbit),
                "relative_error_interval": str(error),
                "absolute_error_lower": str(absolute_error.lower()),
                "absolute_error_upper": str(absolute_error.upper()),
                "strict_upper": str(STRICT_UPPER),
                "key_sha256": record["key_sha256"],
            }

        midpoint = float(absolute_error)
        if midpoint > worst_midpoint:
            worst_midpoint = midpoint
            worst_record = {
                "indices": list(indices),
                "orbit_size": len(group_orbit),
                "relative_error_interval": str(error),
            }

    return {
        "task_id": task_id,
        "task": list(spec),
        "passed": True,
        "status": "all_task_orbits_certified",
        "orbits_expected": len(keys),
        "orbits_scanned": len(keys),
        "eight_sets_scanned": scanned_sets,
        "key_sha256": record["key_sha256"],
        "worst_midpoint_diagnostic": worst_record,
        "strict_upper": str(STRICT_UPPER),
    }


def run(workers=8, limit_tasks=None, precision_bits=PRECISION_BITS):
    summary, records = enumeration_summary(N, K)
    raw = (ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()
    cfg = json.loads(raw)
    input_sha256 = hashlib.sha256(raw).hexdigest()
    if input_sha256 != EXPECTED_INPUT_SHA256:
        raise RuntimeError("candidate input is not the pinned 29-column witness")
    selected = records if limit_tasks is None else records[:limit_tasks]

    results = []
    with ProcessPoolExecutor(
        max_workers=workers,
        mp_context=multiprocessing.get_context("spawn"),
        initializer=initialize_worker,
        initargs=(cfg, input_sha256, precision_bits),
    ) as pool:
        futures = [pool.submit(audit_task, record) for record in selected]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: item["task_id"])
    scanned_orbits = sum(item["orbits_scanned"] for item in results)
    scanned_sets = sum(item["eight_sets_scanned"] for item in results)
    determinant_evaluations = scanned_sets * 29
    all_passed = all(item["passed"] for item in results)
    all_tasks_returned = len(results) == len(selected)
    complete = (
        limit_tasks is None
        and all_tasks_returned
        and all_passed
        and len(results) == summary["task_count"]
        and scanned_orbits == summary["canonical_orbits"]
        and scanned_sets == summary["all_k_subsets"]
    )

    statuses = {item["status"] for item in results}
    if complete:
        status = "complete_interval_certificate"
    elif "definite_violation" in statuses:
        status = "definite_counterexample"
    elif "interval_unresolved" in statuses:
        status = "interval_unresolved"
    else:
        status = "partial_or_incomplete"

    return {
        "base_commit": "0f1a4f2c7a2828ff1d6ca06f69ee1542b1e14f34",
        "candidate_input_sha256": input_sha256,
        "canonical_key_sha256": summary["canonical_key_sha256"],
        "precision_bits": precision_bits,
        "strict_upper": str(STRICT_UPPER) if complete else None,
        "status": status,
        "complete": complete,
        "tasks_total": summary["task_count"],
        "tasks_run": len(results),
        "orbits_expected": summary["canonical_orbits"],
        "orbits_scanned": scanned_orbits,
        "eight_sets_expected": summary["all_k_subsets"],
        "eight_sets_scanned": scanned_sets,
        "determinant_evaluations": determinant_evaluations,
        "determinant_evaluations_if_complete": summary["all_k_subsets"] * 29,
        "burnside": summary["burnside"],
        "task_results": results,
        "scope": (
            "A complete result certifies only the eighth-order maximum for this "
            "fixed 29-column physical distribution. It does not establish orders "
            "10-20, exact all-moment uniformity, an operational inversion error, "
            "or optimality over all physical Hamiltonians."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit-tasks", type=int)
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--enumeration-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.enumeration_only:
        summary, _ = enumeration_summary(N, K)
        result = {
            "base_commit": "0f1a4f2c7a2828ff1d6ca06f69ee1542b1e14f34",
            "candidate_input_sha256": hashlib.sha256(
                (ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()
            ).hexdigest(),
            **summary,
            "moment_scan_complete": False,
            "scope": "Exact orbit enumeration only; no eighth-order determinants evaluated.",
        }
    else:
        result = run(args.workers, args.limit_tasks, args.precision_bits)

    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload)
    print(payload, end="")
