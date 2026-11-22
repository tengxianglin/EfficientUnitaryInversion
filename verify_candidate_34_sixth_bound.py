"""Complete Arb sixth-order audit for the exact 34-column reweighted candidate."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, orbit_keys, burnside, ROOT
from ising_fourth_moments import representative
from screen_ising_sixth_moments import orbit, target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_with_sixth_probes_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_with_sixth_probes_n21.json"
PREFIX_PATH = ROOT / "evidence/candidate_sixth_prefix_7row_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_META_PATH = ROOT / "evidence/seed_pool_n21_frozen.json"
DEFAULT_OUTPUT = ROOT / "evidence/candidate_complete_sixth_bound_12row_n21.json"

EXPECTED_CANDIDATE_SHA256 = "00ba81adfcbebb02137e02b75a7f180d0bf528f71a4bdaa8afe9b9e2b19b7e99"
EXPECTED_LP_SHA256 = "92e366abd639d80418b60a4831efd39c5c4ffeeb05a134fedc2ff1331f41963d"
EXPECTED_PARENT_CANDIDATE_SHA256 = "403614d80d8c5eeb15d56960fc7503103f8d376a7ab990fcb8988b1850d1a54d"
EXPECTED_PREFIX_GIT_BLOB_SHA1 = "6604c6727b075b79ceca438b01faadbbb0ebbd19"
EXPECTED_SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
EXPECTED_ORBITS = 63133
EXPECTED_SIX_SETS = comb(42, 6)
CAP = "1/3"

BANK = None
CANDIDATE_SHA = None
LP_SHA = None


def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def key_hash(keys):
    payload = json.dumps([list(key) for key in keys], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def load_exact_candidate():
    raw = CANDIDATE_PATH.read_bytes()
    candidate_sha = hashlib.sha256(raw).hexdigest()
    if candidate_sha != EXPECTED_CANDIDATE_SHA256:
        raise RuntimeError(f"candidate input SHA mismatch: expected {EXPECTED_CANDIDATE_SHA256}, got {candidate_sha}")

    lp_raw = LP_PATH.read_bytes()
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    if lp_sha != EXPECTED_LP_SHA256:
        raise RuntimeError(f"LP transcript SHA mismatch: expected {EXPECTED_LP_SHA256}, got {lp_sha}")

    candidate = json.loads(raw)
    lp = json.loads(lp_raw)
    if candidate["source_sha256"] != lp_sha:
        raise RuntimeError("candidate input does not pin the current LP transcript")
    if candidate["parent_candidate_input_sha256"] != EXPECTED_PARENT_CANDIDATE_SHA256:
        raise RuntimeError("candidate parent-input hash mismatch")
    if candidate["sixth_prefix_transcript_git_blob_sha1"] != EXPECTED_PREFIX_GIT_BLOB_SHA1:
        raise RuntimeError("candidate does not pin the certified sixth-order prefix")
    if git_blob_sha1(PREFIX_PATH.read_bytes()) != EXPECTED_PREFIX_GIT_BLOB_SHA1:
        raise RuntimeError("certified sixth-order prefix transcript changed")
    if candidate["support_size"] != 34 or len(candidate["exact_probabilities"]) != 34:
        raise RuntimeError("unexpected candidate support size")
    if candidate["columns"] != [int(row["column"]) for row in candidate["exact_probabilities"]]:
        raise RuntimeError("candidate column list and exact probabilities disagree")
    if sum((Fraction(row["probability"]) for row in candidate["exact_probabilities"]), Fraction(0)) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")
    if any(Fraction(row["probability"]) <= 0 for row in candidate["exact_probabilities"]):
        raise RuntimeError("candidate contains a nonpositive probability")
    if candidate["selected_eighth_rows"] != lp["selected_eighth_rows"]:
        raise RuntimeError("candidate and LP selected eighth rows disagree")
    if candidate["sixth_probe_rows"] != lp["sixth_probe_rows"]:
        raise RuntimeError("candidate and LP sixth probes disagree")

    seed_array = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = hashlib.sha256(seed_array.tobytes()).hexdigest()
    if seed_array.shape != (1600, 42) or seed_sha != EXPECTED_SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool content hash or shape mismatch")
    seed_meta = json.loads(SEED_META_PATH.read_text())
    if seed_meta["sha256_le_f64"] != EXPECTED_SEED_POOL_SHA256 or seed_meta["shape"] != [1600, 42]:
        raise RuntimeError("frozen seed-pool metadata mismatch")
    return candidate, candidate_sha, lp_sha


def initialize_worker(candidate, candidate_sha, lp_sha, precision_bits):
    global BANK, CANDIDATE_SHA, LP_SHA
    ctx.prec = precision_bits
    CANDIDATE_SHA = candidate_sha
    LP_SHA = lp_sha
    all_columns, _, _ = canonical_ensemble()
    bank = []
    for record in candidate["exact_probabilities"]:
        column = int(record["column"])
        couplings = all_columns[column]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"candidate column {column} is not a legal 42-site path column")
        bank.append((ball(Fraction(record["probability"])), rotation_entries_exact(couplings)))
    BANK = bank


def principal_minor(entries, indices):
    return arb_mat([[entries[i][j] for j in indices] for i in indices]).det()


def certify_shard(shard_id, start, keys):
    cap = ball(CAP)
    evaluated_sets = 0
    worst_midpoint = -1.0
    worst_record = None
    for offset, key in enumerate(keys):
        indices = representative(key)
        group = orbit(indices)
        moment = arb(0)
        for weight, entries in BANK:
            subtotal = arb(0)
            for subset in group:
                subtotal += principal_minor(entries, subset)
            moment += weight * subtotal / len(group)

        error = (moment - ball(target(indices))) / ball(abs(target(indices)))
        absolute_error = abs(error)
        evaluated_sets += len(group)
        if not absolute_error < cap:
            lower = absolute_error.lower()
            status = "strict_violation" if lower > cap else "interval_unresolved"
            return {
                "passed": False,
                "status": status,
                "shard": shard_id,
                "start": start,
                "failure_orbit_index": start + offset,
                "indices": list(indices),
                "cyclic_gap_key": list(key),
                "orbit_size": len(group),
                "target": str(target(indices)),
                "error_interval": str(error),
                "absolute_error_lower": str(lower),
                "absolute_error_upper": str(absolute_error.upper()),
                "evaluated_orbits": offset + 1,
                "evaluated_six_sets": evaluated_sets,
                "key_sha256_evaluated_prefix": key_hash(keys[:offset + 1]),
                "candidate_input_sha256": CANDIDATE_SHA,
            }

        midpoint = float(absolute_error)
        if midpoint > worst_midpoint:
            worst_midpoint = midpoint
            worst_record = {
                "indices": list(indices),
                "cyclic_gap_key": list(key),
                "orbit_size": len(group),
                "error_interval": str(error),
            }

    return {
        "passed": True,
        "shard": shard_id,
        "start": start,
        "stop": start + len(keys),
        "orbits": len(keys),
        "six_sets": evaluated_sets,
        "key_sha256": key_hash(keys),
        "candidate_input_sha256": CANDIDATE_SHA,
        "lp_transcript_sha256": LP_SHA,
        "worst_midpoint": worst_midpoint,
        "worst_row": worst_record,
        "strict_row_cap": CAP,
    }


def verify(workers=8, limit=None, precision_bits=128):
    if not 1 <= workers <= 8:
        raise ValueError("workers must be between 1 and 8")
    candidate, candidate_sha, lp_sha = load_exact_candidate()
    keys = orbit_keys(42)
    burnside_result = burnside(42)
    if len(keys) != burnside_result["orbits"] or len(keys) != EXPECTED_ORBITS:
        raise RuntimeError("sixth-order orbit enumeration disagrees with Burnside")
    full_orbit_hash = key_hash(keys)

    if limit is not None:
        if not 0 < limit <= len(keys):
            raise ValueError("limit must be between 1 and the full orbit count")
        keys = keys[:limit]

    boundaries = [len(keys) * i // workers for i in range(workers + 1)]
    tasks = []
    results = []
    with ProcessPoolExecutor(
        max_workers=workers,
        mp_context=multiprocessing.get_context("spawn"),
        initializer=initialize_worker,
        initargs=(candidate, candidate_sha, lp_sha, precision_bits),
    ) as pool:
        for shard_id, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
            if left < right:
                tasks.append(pool.submit(certify_shard, shard_id, left, keys[left:right]))
        for future in as_completed(tasks):
            results.append(future.result())

    results.sort(key=lambda row: row["start"])
    failures = [row for row in results if not row["passed"]]
    passed = not failures
    complete = passed and limit is None

    if passed:
        cursor = 0
        total_sets = 0
        for row in results:
            if row["start"] != cursor or row["candidate_input_sha256"] != candidate_sha:
                raise RuntimeError("shard coverage or candidate-input hash mismatch")
            expected_keys = keys[row["start"]:row["stop"]]
            if row["key_sha256"] != key_hash(expected_keys):
                raise RuntimeError("shard canonical-key hash mismatch")
            cursor = row["stop"]
            total_sets += row["six_sets"]
        if cursor != len(keys):
            raise RuntimeError("shard ranges do not cover the requested orbit prefix")
    else:
        total_sets = sum(row.get("evaluated_six_sets", row.get("six_sets", 0)) for row in results)

    if complete and total_sets != EXPECTED_SIX_SETS:
        raise RuntimeError("complete sixth-orbit scan does not cover all six-subsets")

    status = "complete_pass" if complete else ("prefix_pass" if passed else failures[0]["status"])
    return {
        "status": status,
        "passed": passed,
        "complete": complete,
        "base_commit": candidate["base_commit"],
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "parent_candidate_input_sha256": EXPECTED_PARENT_CANDIDATE_SHA256,
        "sixth_prefix_transcript_git_blob_sha1": EXPECTED_PREFIX_GIT_BLOB_SHA1,
        "seed_pool_sha256_le_f64": EXPECTED_SEED_POOL_SHA256,
        "precision_bits": precision_bits,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": candidate["support_size"],
        "strict_error_upper": CAP if complete else None,
        "requested_orbits": len(keys),
        "expected_sixth_orbits": EXPECTED_ORBITS,
        "evaluated_six_sets": total_sets,
        "expected_six_sets": EXPECTED_SIX_SETS,
        "principal_minor_determinant_evaluations": total_sets * candidate["support_size"],
        "canonical_key_sha256": full_orbit_hash if complete else key_hash(keys),
        "burnside": burnside_result,
        "shards": results,
        "failures": failures,
        "scope": (
            "A complete pass certifies the strict normalized sixth-order maximum below 1/3 "
            "for this exact 34-column physical distribution only. A prefix pass is not a "
            "complete certificate. A strict violation is candidate-specific, not a no-go "
            "theorem for other physical ensembles. No eighth-order maximum or operational "
            "inversion/channel-error bound follows."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, default=None,
                        help="development prefix only; cannot certify the complete sixth-order maximum")
    parser.add_argument("--precision-bits", type=int, default=128)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = verify(args.workers, args.limit, args.precision_bits)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "passed": result["passed"],
        "complete": result["complete"],
        "candidate_input_sha256": result["candidate_input_sha256"],
        "support_size": result["support_size"],
        "requested_orbits": result["requested_orbits"],
        "evaluated_six_sets": result["evaluated_six_sets"],
        "principal_minor_determinant_evaluations": result["principal_minor_determinant_evaluations"],
        "failures": result["failures"][:1],
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
