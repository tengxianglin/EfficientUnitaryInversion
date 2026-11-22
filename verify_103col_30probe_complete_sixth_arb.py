"""Complete 128-bit Arb audit of all sixth-order dihedral orbits for the 103-column / 30-probe candidate."""
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

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_103col_30probe_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_103col_30probe_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_103col_22probe_n21.json"
PARENT_CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_103col_22probe_n21.json"
PARENT_SIXTH_AUDIT_PATH = ROOT / "evidence/candidate_103col_22probe_complete_sixth_arb_n21.json"
CURRENT_PREFIX_PATH = ROOT / "evidence/candidate_103col_30probe_selected_and_sixth_prefix_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
DEFAULT_OUTPUT = ROOT / "evidence/candidate_103col_22probe_complete_sixth_arb_n21.json"

EXPECTED_ORBITS = 63133
EXPECTED_SIX_SETS = comb(42, 6)
EXPECTED_SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
CAP = Fraction(1, 3)

BANK = None
CANDIDATE_SHA = None
LP_SHA = None


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def key_hash(keys):
    payload = json.dumps([list(key) for key in keys], separators=(",", ":"))
    return sha256(payload.encode())


def load_exact_candidate():
    candidate_raw = CANDIDATE_PATH.read_bytes()
    candidate_sha = sha256(candidate_raw)
    candidate = json.loads(candidate_raw)
    lp_raw = LP_PATH.read_bytes()
    lp_sha = sha256(lp_raw)
    lp = json.loads(lp_raw)
    parent_lp_raw = PARENT_LP_PATH.read_bytes()
    parent_candidate_raw = PARENT_CANDIDATE_PATH.read_bytes()
    parent_audit_raw = PARENT_SIXTH_AUDIT_PATH.read_bytes()
    current_prefix_raw = CURRENT_PREFIX_PATH.read_bytes()
    parent_lp = json.loads(parent_lp_raw)
    parent_candidate = json.loads(parent_candidate_raw)
    parent_audit = json.loads(parent_audit_raw)
    current_prefix = json.loads(current_prefix_raw)

    parent_lp_sha = sha256(parent_lp_raw)
    parent_candidate_sha = sha256(parent_candidate_raw)
    parent_audit_sha = sha256(parent_audit_raw)
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate does not pin the 103-column / 30-probe LP transcript")
    if candidate.get("parent_lp_sha256") != parent_lp_sha or lp.get("parent_lp_sha256") != parent_lp_sha:
        raise RuntimeError("candidate/LP does not pin the parent 103-column / 22-probe LP")
    if candidate.get("parent_candidate_input_sha256") != parent_candidate_sha or lp.get("parent_candidate_input_sha256") != parent_candidate_sha:
        raise RuntimeError("candidate/LP does not pin the parent exact 44-support candidate")
    if candidate.get("parent_sixth_audit_sha256") != parent_audit_sha or lp.get("parent_sixth_audit_sha256") != parent_audit_sha:
        raise RuntimeError("candidate/LP does not pin the parent 128-bit sixth-order rejection")
    if parent_candidate.get("source_sha256") != parent_lp_sha:
        raise RuntimeError("parent candidate does not pin its LP")
    if parent_audit.get("status") != "strict_violation" or parent_audit.get("complete") is not False:
        raise RuntimeError("parent sixth audit is not a candidate-specific strict rejection")
    if parent_audit.get("candidate_input_sha256") != parent_candidate_sha or parent_audit.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("parent Arb rejection does not pin its exact candidate and LP")
    failures = parent_audit.get("failures", [])
    separators = candidate.get("new_sixth_separators", [])
    if len(failures) != 8 or len(separators) != 8 or separators != lp.get("new_sixth_separators"):
        raise RuntimeError("expected eight inherited strict Arb separators")
    for failure, separator in zip(failures, separators):
        if failure.get("status") != "strict_violation" or failure.get("candidate_input_sha256") != parent_candidate_sha:
            raise RuntimeError("parent audit has a non-strict or mismatched separator")
        if separator.get("indices") != failure.get("indices") or separator.get("target") != failure.get("target"):
            raise RuntimeError("inherited separator differs from the pinned parent Arb audit")
    if lp.get("columns") != 103 or lp.get("rows") != 1754:
        raise RuntimeError("unexpected 103-column / 1,754-row LP dimensions")
    if parent_lp.get("columns") != 103 or parent_lp.get("rows") != 1746:
        raise RuntimeError("unexpected parent 103-column / 1,746-row LP dimensions")
    if candidate.get("support_size") != len(candidate.get("exact_probabilities", [])):
        raise RuntimeError("candidate support metadata mismatch")
    if candidate.get("columns") != [int(row["column"]) for row in candidate["exact_probabilities"]]:
        raise RuntimeError("candidate column list and exact probabilities disagree")
    if sum((Fraction(row["probability"]) for row in candidate["exact_probabilities"]), Fraction(0)) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")
    if any(Fraction(row["probability"]) <= 0 for row in candidate["exact_probabilities"]):
        raise RuntimeError("candidate contains a nonpositive probability")
    if candidate.get("exact_probability_sum") != "1":
        raise RuntimeError("candidate exact probability-sum metadata mismatch")
    if len(candidate.get("sixth_probe_rows", [])) != 30:
        raise RuntimeError("candidate does not contain 30 sixth-order probes")
    expected_rows = [list(row) for row in parent_lp["sixth_probe_rows"]] + [failure["indices"] for failure in failures]
    expected_targets = list(parent_lp["sixth_probe_targets"]) + [failure["target"] for failure in failures]
    if candidate.get("sixth_probe_rows") != expected_rows or lp.get("sixth_probe_rows") != expected_rows:
        raise RuntimeError("30 sixth rows do not equal the parent 22 plus eight strict Arb separators")
    if candidate.get("sixth_probe_targets") != expected_targets or lp.get("sixth_probe_targets") != expected_targets:
        raise RuntimeError("30 sixth targets do not equal the parent and separator targets")
    if candidate.get("selected_eighth_rows") != lp.get("selected_eighth_rows"):
        raise RuntimeError("candidate and LP selected eighth rows disagree")
    if current_prefix.get("status") != "prefix_pass" or current_prefix.get("complete") is not False:
        raise RuntimeError("current 30-probe candidate has not passed its strict sixth-prefix audit")
    if current_prefix.get("candidate_input_sha256") != candidate_sha or current_prefix.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("current prefix audit does not pin the exact 30-probe candidate")
    if current_prefix.get("precision_bits", 0) < 128 or current_prefix.get("sixth_prefix", {}).get("evaluated_orbits") != 1024:
        raise RuntimeError("current prefix audit is not a complete 1,024-orbit 128-bit Arb prefix")
    selected = current_prefix.get("selected_blocks", {})
    if not all(selected.get(key, {}).get("passed") for key in ("low", "sixth_selected", "eighth_selected")):
        raise RuntimeError("current selected-row Arb certificate has a failure")
    if selected["low"].get("rows") != 1461 or selected["sixth_selected"].get("rows") != 286 or selected["eighth_selected"].get("rows") != 7:
        raise RuntimeError("current selected-row Arb block sizes changed")

    all_columns, _, _ = canonical_ensemble()
    all_hash = sha256(np.asarray(all_columns, dtype="<f8").tobytes())
    if all_hash != candidate.get("canonical_all_columns_sha256_le_f64") or all_hash != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical physical-column fingerprint mismatch")
    if len(all_columns) != 1641:
        raise RuntimeError("canonical physical pool size changed")
    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_hash = sha256(seed.tobytes())
    if seed.shape != (1600, 42) or seed_hash != EXPECTED_SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash or shape mismatch")
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
        "strict_row_cap": "1/3",
    }


def verify(workers=8, limit=None, precision_bits=128):
    if not 1 <= workers <= 8:
        raise ValueError("workers must be between 1 and 8")
    candidate, candidate_sha, lp_sha = load_exact_candidate()
    keys = orbit_keys(42)
    burnside_result = burnside(42)
    if len(keys) != EXPECTED_ORBITS or burnside_result["orbits"] != EXPECTED_ORBITS:
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
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "parent_candidate_input_sha256": sha256(PARENT_CANDIDATE_PATH.read_bytes()),
        "parent_sixth_audit_sha256": sha256(PARENT_SIXTH_AUDIT_PATH.read_bytes()),
        "current_prefix_audit_sha256": sha256(CURRENT_PREFIX_PATH.read_bytes()),
        "seed_pool_sha256_le_f64": EXPECTED_SEED_POOL_SHA256,
        "precision_bits": precision_bits,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": candidate["support_size"],
        "strict_error_upper": "1/3" if complete else None,
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
            "for this exact rational 41-support candidate only. A prefix pass is not a complete "
            "certificate. A strict violation is candidate-specific, not a no-go theorem for other "
            "physical ensembles. No complete eighth-order maximum or operational inversion/"
            "channel-error bound follows."
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
