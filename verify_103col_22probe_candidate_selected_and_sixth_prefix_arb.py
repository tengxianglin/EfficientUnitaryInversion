"""Arb-check the 103-column / 22-probe candidate and its first 1,024 sixth orbits."""
import hashlib
import json
from fractions import Fraction
from itertools import islice
from math import comb
from pathlib import Path

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, orbit_keys, burnside, ROOT
from ising_fourth_moments import FourthMoments, representative
from screen_ising_sixth_moments import orbit, target
from verify_full_low_moment_certificate import all_features
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_103col_22probe_n21.json"
LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_103col_22probe_n21.json"
PARENT_LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_103col_21probe_n21.json"
PARENT_CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_103col_21probe_n21.json"
PARENT_PREFIX_IN = ROOT / "evidence/candidate_103col_21probe_selected_and_sixth_prefix_arb_n21.json"
SEED_POOL_IN = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT = ROOT / "evidence/candidate_103col_22probe_selected_and_sixth_prefix_arb_n21.json"
CAP = Fraction(1, 3)
PRECISION_BITS = 128
PREFIX_ORBITS = 1024
EXPECTED_SIXTH_ORBITS = 63133


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def key_hash(keys):
    payload = json.dumps([list(key) for key in keys], separators=(",", ":"))
    return sha256(payload.encode())


def principal_minor(entries, indices):
    return arb_mat([[entries[int(i)][int(j)] for j in indices] for i in indices]).det()


def orbit_moment(bank, indices):
    group = orbit(indices)
    moment = arb(0)
    for weight, entries in bank:
        subtotal = arb(0)
        for subset in group:
            subtotal += principal_minor(entries, subset)
        moment += weight * subtotal / len(group)
    return moment, group


def block_summary(records, label):
    cap = ball(CAP)
    failures = []
    worst = None
    worst_midpoint = -1.0
    for record in records:
        absolute = abs(record["error"])
        if not absolute.upper() < cap:
            lower = absolute.lower()
            failures.append({
                key: value for key, value in record.items()
                if key != "error"
            } | {
                "status": "strict_violation" if lower > cap else "interval_unresolved",
                "absolute_error_lower": str(lower),
                "absolute_error_upper": str(absolute.upper()),
            })
        midpoint = float(absolute)
        if midpoint > worst_midpoint:
            worst_midpoint = midpoint
            worst = {key: value for key, value in record.items() if key != "error"}
    return {
        "label": label,
        "rows": len(records),
        "strict_upper": str(CAP),
        "worst_midpoint": worst_midpoint,
        "worst_row": worst,
        "failures": failures,
        "passed": not failures,
    }


def load_inputs():
    candidate_raw = CANDIDATE_IN.read_bytes()
    lp_raw = LP_IN.read_bytes()
    parent_lp_raw = PARENT_LP_IN.read_bytes()
    parent_candidate_raw = PARENT_CANDIDATE_IN.read_bytes()
    parent_prefix_raw = PARENT_PREFIX_IN.read_bytes()
    candidate = json.loads(candidate_raw)
    lp = json.loads(lp_raw)
    parent_lp = json.loads(parent_lp_raw)
    parent_candidate = json.loads(parent_candidate_raw)
    parent_prefix = json.loads(parent_prefix_raw)

    candidate_sha = sha256(candidate_raw)
    lp_sha = sha256(lp_raw)
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate does not pin the 103-column / 22-probe LP transcript")
    if candidate.get("parent_lp_sha256") != sha256(parent_lp_raw) or lp.get("parent_lp_sha256") != sha256(parent_lp_raw):
        raise RuntimeError("new LP/candidate does not pin the parent 103-column LP")
    if candidate.get("parent_candidate_input_sha256") != sha256(parent_candidate_raw) or lp.get("parent_candidate_input_sha256") != sha256(parent_candidate_raw):
        raise RuntimeError("new LP/candidate does not pin the parent exact candidate")
    if candidate.get("parent_prefix_audit_sha256") != sha256(parent_prefix_raw) or lp.get("parent_prefix_audit_sha256") != sha256(parent_prefix_raw):
        raise RuntimeError("new LP/candidate does not pin the Arb prefix separator")
    if parent_candidate.get("source_sha256") != sha256(parent_lp_raw):
        raise RuntimeError("parent candidate does not pin the parent LP")
    if parent_prefix.get("candidate_input_sha256") != sha256(parent_candidate_raw):
        raise RuntimeError("parent prefix audit does not pin the parent candidate")
    if lp.get("columns") != 103 or lp.get("rows") != 1746:
        raise RuntimeError("unexpected 103-column / 1,746-row LP dimensions")
    if candidate.get("support_size") != len(candidate.get("exact_probabilities", [])):
        raise RuntimeError("candidate support metadata mismatch")
    if candidate.get("columns") != [int(row["column"]) for row in candidate["exact_probabilities"]]:
        raise RuntimeError("candidate columns and rational weights disagree")
    probabilities = [Fraction(row["probability"]) for row in candidate["exact_probabilities"]]
    if any(value <= 0 for value in probabilities) or sum(probabilities, Fraction(0)) != 1:
        raise RuntimeError("candidate probabilities are not a positive exact simplex point")
    if candidate.get("exact_probability_sum") != "1":
        raise RuntimeError("candidate exact probability-sum metadata mismatch")
    if candidate.get("canonical_all_columns_sha256_le_f64") != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("candidate and LP canonical-column fingerprints disagree")
    if candidate.get("sixth_probe_rows") != lp.get("sixth_probe_rows"):
        raise RuntimeError("candidate and LP sixth-probe rows disagree")
    if candidate.get("sixth_probe_targets") != lp.get("sixth_probe_targets"):
        raise RuntimeError("candidate and LP sixth-probe targets disagree")
    if candidate.get("selected_eighth_rows") != lp.get("selected_eighth_rows"):
        raise RuntimeError("candidate and LP selected eighth rows disagree")
    if candidate.get("new_sixth_separator") != lp.get("new_sixth_separator"):
        raise RuntimeError("candidate and LP new separator metadata disagree")
    if len(candidate["sixth_probe_rows"]) != 22:
        raise RuntimeError("expected 22 Arb-certified sixth-order probes")

    all_columns, _, _ = canonical_ensemble()
    all_hash = sha256(np.asarray(all_columns, dtype="<f8").tobytes())
    if all_hash != candidate["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical 1,641-column physical pool hash mismatch")
    if len(all_columns) != 1641:
        raise RuntimeError("canonical physical pool size changed")
    seed = np.asarray(np.load(SEED_POOL_IN, allow_pickle=False), dtype="<f8")
    seed_hash = sha256(seed.tobytes())
    if seed.shape != (1600, 42) or seed_hash != "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315":
        raise RuntimeError("frozen seed-pool content hash or shape mismatch")

    bank = []
    for record in candidate["exact_probabilities"]:
        column = int(record["column"])
        couplings = all_columns[column]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"candidate column {column} is not a legal 42-site path generator")
        entries = rotation_entries_exact(couplings)
        bank.append((ball(Fraction(record["probability"])), entries))
    return candidate, lp, candidate_sha, lp_sha, bank


def verify_selected(candidate, lp, bank):
    ctx.prec = PRECISION_BITS
    system = FourthMoments(21)
    system.exact_target_check()
    if len(system.rational_target) != 1461:
        raise RuntimeError("unexpected complete low-moment row count")

    low_mixture = [arb(0) for _ in system.rational_target]
    for weight, entries in bank:
        features = all_features(system, entries)
        for index, value in enumerate(features):
            low_mixture[index] += weight * value
    low_records = []
    for index, (actual, expected) in enumerate(zip(low_mixture, system.rational_target)):
        error = (actual - ball(expected)) / ball(abs(expected))
        low_records.append({
            "row": index,
            "order": 2 if index < 21 else 4,
            "error": error,
            "error_interval": str(error),
        })
    low = block_summary(low_records, "all 1,461 second/fourth rows")

    screen_rows = json.loads((ROOT / "evidence/sixth_moment_screen_n21.json").read_text())["records"]
    sixth_rows = [tuple(row["indices"]) for row in screen_rows] + [tuple(row) for row in candidate["sixth_probe_rows"]]
    sixth_targets = [Fraction(row["target"]) for row in screen_rows] + [Fraction(x) for x in candidate["sixth_probe_targets"]]
    if len(sixth_rows) != 278:
        raise RuntimeError("expected 256 screened and 22 Arb-certified sixth rows")
    sixth_records = []
    for row_index, (indices, expected) in enumerate(zip(sixth_rows, sixth_targets)):
        moment, group = orbit_moment(bank, indices)
        error = (moment - ball(expected)) / ball(abs(expected))
        sixth_records.append({
            "row": row_index,
            "indices": list(indices),
            "target": str(expected),
            "orbit_size": len(group),
            "error": error,
            "error_interval": str(error),
        })
    sixth = block_summary(sixth_records, "278 selected sixth rows")

    eighth_rows = [tuple(row) for row in candidate["selected_eighth_rows"]]
    eighth_records = []
    for row_index, indices in enumerate(eighth_rows):
        expected = Fraction((-1) ** (sum(index % 2 for index in indices) + 4), 19721)
        moment, group = orbit_moment(bank, indices)
        error = (moment - ball(expected)) / ball(abs(expected))
        eighth_records.append({
            "row": row_index,
            "indices": list(indices),
            "target": str(expected),
            "orbit_size": len(group),
            "error": error,
            "error_interval": str(error),
        })
    eighth = block_summary(eighth_records, "seven selected eighth rows")
    return {"low": low, "sixth_selected": sixth, "eighth_selected": eighth}


def verify_sixth_prefix(candidate, candidate_sha, lp_sha, bank):
    keys = orbit_keys(42)
    burnside_result = burnside(42)
    if len(keys) != EXPECTED_SIXTH_ORBITS or burnside_result["orbits"] != EXPECTED_SIXTH_ORBITS:
        raise RuntimeError("sixth-order orbit enumeration disagrees with Burnside")
    prefix = list(islice(keys, PREFIX_ORBITS))
    evaluated_sets = 0
    worst_midpoint = -1.0
    worst_row = None
    failure = None
    cap = ball(CAP)

    for offset, key in enumerate(prefix):
        indices = representative(key)
        moment, group = orbit_moment(bank, indices)
        expected = target(indices)
        error = (moment - ball(expected)) / ball(abs(expected))
        absolute = abs(error)
        evaluated_sets += len(group)
        if not absolute.upper() < cap:
            failure = {
                "status": "strict_violation" if absolute.lower() > cap else "interval_unresolved",
                "failure_orbit_index": offset,
                "indices": list(indices),
                "cyclic_gap_key": list(key),
                "orbit_size": len(group),
                "target": str(expected),
                "error_interval": str(error),
                "absolute_error_lower": str(absolute.lower()),
                "absolute_error_upper": str(absolute.upper()),
                "evaluated_orbits": offset + 1,
                "evaluated_six_sets": evaluated_sets,
            }
            break
        midpoint = float(absolute)
        if midpoint > worst_midpoint:
            worst_midpoint = midpoint
            worst_row = {
                "indices": list(indices),
                "cyclic_gap_key": list(key),
                "orbit_size": len(group),
                "error_interval": str(error),
            }

    return {
        "status": failure["status"] if failure else "prefix_pass",
        "complete": False,
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "precision_bits": PRECISION_BITS,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": candidate["support_size"],
        "requested_orbits": PREFIX_ORBITS,
        "expected_sixth_orbits": EXPECTED_SIXTH_ORBITS,
        "evaluated_orbits": failure["evaluated_orbits"] if failure else PREFIX_ORBITS,
        "evaluated_six_sets": evaluated_sets,
        "principal_minor_determinant_evaluations": evaluated_sets * candidate["support_size"],
        "canonical_key_sha256": key_hash(prefix),
        "full_canonical_key_sha256": key_hash(keys),
        "burnside": burnside_result,
        "worst_midpoint": worst_midpoint if failure is None else None,
        "worst_row": worst_row if failure is None else None,
        "failure": failure,
        "scope": (
            "128-bit Arb audit of the first 1,024 canonical dihedral sixth-order orbits for this "
            "exact rational candidate only. A prefix pass is not a complete sixth-order certificate; "
            "a strict violation rejects this candidate only. No full eighth-order maximum or "
            "operational inversion/channel-error bound follows."
        ),
    }


def main():
    ctx.prec = PRECISION_BITS
    candidate, lp, candidate_sha, lp_sha, bank = load_inputs()
    selected = verify_selected(candidate, lp, bank)
    selected_pass = all(selected[key]["passed"] for key in selected)
    prefix = verify_sixth_prefix(candidate, candidate_sha, lp_sha, bank) if selected_pass else None
    if not selected_pass:
        status = "selected_rows_violation"
    elif prefix["status"] == "strict_violation":
        status = "prefix_strict_violation"
    elif prefix["status"] == "interval_unresolved":
        status = "prefix_interval_unresolved"
    else:
        status = "prefix_pass"

    result = {
        "status": status,
        "complete": False,
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": candidate["support_size"],
        "exact_probability_sum": "1",
        "selected_blocks": selected,
        "sixth_prefix": prefix,
        "scope": (
            "Exact-rational 103-column / 22-probe LP candidate independently checked with 128-bit Arb "
            "on all 1,461 low rows, 278 selected sixth rows, and seven selected eighth rows. The first "
            "1,024 sixth-order orbits are additionally audited if selected rows pass. No complete "
            "sixth/eighth maximum, global physical optimum, or operational channel-error theorem."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": status,
        "candidate_input_sha256": candidate_sha,
        "support_size": candidate["support_size"],
        "selected_row_blocks": {
            key: {
                "rows": value["rows"],
                "passed": value["passed"],
                "worst_midpoint": value["worst_midpoint"],
                "failures": value["failures"][:3],
            }
            for key, value in selected.items()
        },
        "sixth_prefix": None if prefix is None else {
            key: prefix[key] for key in (
                "status", "evaluated_orbits", "evaluated_six_sets",
                "principal_minor_determinant_evaluations", "failure", "worst_midpoint", "worst_row"
            )
        },
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
