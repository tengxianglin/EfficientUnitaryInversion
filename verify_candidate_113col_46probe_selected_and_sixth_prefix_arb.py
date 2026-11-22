"""Arb-check the 113-column cutting-plane candidate with 46 sixth separators and a 1,024-orbit prefix."""
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

CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_113col_46probe_n21.json"
LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_113col_46probe_n21.json"
OLD_CANDIDATE_IN = ROOT / "evidence/candidate_joint_input_113col_38probe_n21.json"
AUDIT_IN = ROOT / "evidence/candidate_113col_38probe_complete_sixth_arb_n21.json"
PARENT_LP_IN = ROOT / "evidence/joint_low_six_eighth_lp_103col_38probe_n21.json"
DUAL_IN = ROOT / "evidence/38probe_103col_dual_certificate_n21.json"
PRICING_SCREEN_IN = ROOT / "evidence/38probe_103col_dual_pricing_screen_n21.json"
PRICING_ARB_IN = ROOT / "evidence/38probe_103col_dual_pricing_arb_n21.json"
SEED_POOL_IN = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT = ROOT / "evidence/candidate_113col_46probe_selected_and_sixth_prefix_arb_n21.json"
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
    dual_raw = DUAL_IN.read_bytes()
    pricing_screen_raw = PRICING_SCREEN_IN.read_bytes()
    pricing_arb_raw = PRICING_ARB_IN.read_bytes()
    old_candidate_raw = OLD_CANDIDATE_IN.read_bytes()
    audit_raw = AUDIT_IN.read_bytes()
    candidate = json.loads(candidate_raw)
    lp = json.loads(lp_raw)
    parent_lp = json.loads(parent_lp_raw)
    dual = json.loads(dual_raw)
    pricing_screen = json.loads(pricing_screen_raw)
    pricing_arb = json.loads(pricing_arb_raw)
    old_candidate_sha = sha256(old_candidate_raw)
    audit_sha = sha256(audit_raw)
    audit = json.loads(audit_raw)

    candidate_sha = sha256(candidate_raw)
    lp_sha = sha256(lp_raw)
    parent_lp_sha = sha256(parent_lp_raw)
    dual_sha = sha256(dual_raw)
    pricing_screen_sha = sha256(pricing_screen_raw)
    pricing_arb_sha = sha256(pricing_arb_raw)

    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate does not pin the 113-column / 46-separator LP transcript")
    if audit.get("status") != "strict_violation" or audit.get("complete") is not False or audit.get("candidate_input_sha256") != old_candidate_sha:
        raise RuntimeError("parent full-domain Arb rejection does not pin the exact previous candidate")
    if candidate.get("parent_complete_sixth_audit_sha256") != audit_sha or lp.get("parent_complete_sixth_audit_sha256") != audit_sha:
        raise RuntimeError("new candidate/LP does not pin the parent full-domain Arb separator transcript")
    if lp.get("parent_lp_sha256") != parent_lp_sha or candidate.get("parent_lp_sha256") != parent_lp_sha:
        raise RuntimeError("expanded LP/candidate does not pin the 103-column parent LP")
    if dual.get("status") != "strict_pool_separation" or not dual.get("complete"):
        raise RuntimeError("parent 103-column Arb dual certificate is not complete")
    if dual.get("lp_transcript_sha256") != parent_lp_sha or dual.get("column_count") != 103 or dual.get("row_count") != 1762:
        raise RuntimeError("parent dual certificate does not pin the 103-column / 1,762-row LP")
    if lp.get("parent_dual_certificate_sha256") != dual_sha or candidate.get("parent_dual_certificate_sha256") != dual_sha:
        raise RuntimeError("expanded LP/candidate does not pin the parent dual certificate")
    if pricing_screen.get("dual_certificate_sha256") != dual_sha or pricing_screen.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("pricing screen does not pin the parent LP and dual certificate")
    if lp.get("parent_pricing_screen_sha256") != pricing_screen_sha or candidate.get("parent_pricing_screen_sha256") != pricing_screen_sha:
        raise RuntimeError("expanded LP/candidate does not pin the pricing screen")
    if pricing_arb.get("status") != "arb_positive_columns_found" or pricing_arb.get("precision_bits", 0) < 128:
        raise RuntimeError("the top-column pricing transcript is not a 128-bit Arb positive certificate")
    if pricing_arb.get("dual_certificate_sha256") != dual_sha or pricing_arb.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("Arb pricing does not pin the parent LP and dual certificate")
    if pricing_arb.get("pricing_screen_sha256") != pricing_screen_sha:
        raise RuntimeError("Arb pricing does not pin the pricing screen")
    if pricing_arb.get("arb_certified_positive_count") != 10 or len(pricing_arb.get("results", [])) != 10:
        raise RuntimeError("expected ten Arb-certified positive priced columns")
    if lp.get("parent_arb_pricing_sha256") != pricing_arb_sha or candidate.get("parent_arb_pricing_sha256") != pricing_arb_sha:
        raise RuntimeError("expanded LP/candidate does not pin the Arb pricing transcript")

    if parent_lp.get("columns") != 103 or parent_lp.get("rows") != 1762:
        raise RuntimeError("parent LP dimensions changed")
    if lp.get("columns") != 113 or lp.get("rows") != 1770:
        raise RuntimeError("expanded LP dimensions are not 113 columns x 1,770 rows")
    expected_blocks = dict(parent_lp.get("row_blocks", {}))
    expected_blocks["sixth_full_audit_separators"] = 8
    if lp.get("row_blocks") != expected_blocks:
        raise RuntimeError("expanded LP changed the pinned row inventory or omitted the eight full-domain separators")
    if lp.get("sixth_probe_rows") != parent_lp.get("sixth_probe_rows") or lp.get("sixth_probe_targets") != parent_lp.get("sixth_probe_targets"):
        raise RuntimeError("expanded LP changed the 38 Arb-certified sixth separators")
    if lp.get("selected_eighth_rows") != parent_lp.get("selected_eighth_rows"):
        raise RuntimeError("expanded LP changed the selected eighth-order rows")
    audit_rows = [row["indices"] for row in audit.get("failures", [])]
    audit_targets = [row["target"] for row in audit.get("failures", [])]
    if len(audit_rows) != 8 or sorted(int(row["shard"]) for row in audit["failures"]) != list(range(8)):
        raise RuntimeError("parent full-domain transcript does not contain eight shard separators")
    if lp.get("sixth_full_audit_separator_rows") != audit_rows or lp.get("sixth_full_audit_separator_targets") != audit_targets:
        raise RuntimeError("new LP separator rows differ from the Arb rejection transcript")

    base_columns = [int(x) for x in dual["columns"]]
    priced_columns = sorted(int(row["column"]) for row in pricing_arb["results"] if row.get("strictly_positive"))
    if len(base_columns) != 103 or base_columns != sorted(set(base_columns)):
        raise RuntimeError("parent dual column list is malformed")
    if lp.get("base_columns") != base_columns or lp.get("added_arb_positive_columns") != priced_columns:
        raise RuntimeError("expanded LP columns differ from the Arb-priced 103+10 pool")
    expanded_columns = sorted(set(base_columns) | set(priced_columns))
    if len(expanded_columns) != 113:
        raise RuntimeError("expected exactly 113 distinct expanded physical columns")

    if candidate.get("support_size") != len(candidate.get("exact_probabilities", [])):
        raise RuntimeError("candidate support metadata mismatch")
    if candidate.get("columns") != [int(row["column"]) for row in candidate["exact_probabilities"]]:
        raise RuntimeError("candidate columns and rational probabilities disagree")
    probabilities = [Fraction(row["probability"]) for row in candidate["exact_probabilities"]]
    if not probabilities or any(value <= 0 for value in probabilities) or sum(probabilities, Fraction(0)) != 1:
        raise RuntimeError("candidate probabilities are not a positive exact simplex point")
    if candidate.get("exact_probability_sum") != "1":
        raise RuntimeError("candidate exact probability-sum metadata mismatch")
    if any(int(row["column"]) not in expanded_columns for row in candidate["exact_probabilities"]):
        raise RuntimeError("candidate uses a column outside the pinned 113-column pool")
    if candidate.get("canonical_all_columns_sha256_le_f64") != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("candidate and LP canonical-column fingerprints disagree")

    expected_rows = parent_lp["sixth_probe_rows"]
    expected_targets = parent_lp["sixth_probe_targets"]
    if candidate.get("sixth_probe_rows") != expected_rows or candidate.get("sixth_probe_targets") != expected_targets:
        raise RuntimeError("candidate does not preserve the 38 parent sixth-order probes")
    if candidate.get("selected_eighth_rows") != lp.get("selected_eighth_rows"):
        raise RuntimeError("candidate and LP selected eighth rows disagree")
    if candidate.get("sixth_full_audit_separator_rows") != audit_rows or candidate.get("sixth_full_audit_separator_targets") != audit_targets:
        raise RuntimeError("candidate does not preserve the eight Arb-certified full-domain separators")
    if len(candidate["sixth_probe_rows"]) != 38:
        raise RuntimeError("expected exactly 38 parent certified sixth-order probes")

    all_columns, _, _ = canonical_ensemble()
    all_hash = sha256(np.asarray(all_columns, dtype="<f8").tobytes())
    if all_hash != candidate["canonical_all_columns_sha256_le_f64"] or all_hash != parent_lp["canonical_all_columns_sha256_le_f64"]:
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
    return candidate, lp, candidate_sha, lp_sha, audit_sha, bank

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
    sixth_rows = ([tuple(row["indices"]) for row in screen_rows]
                  + [tuple(row) for row in candidate["sixth_probe_rows"]]
                  + [tuple(row) for row in candidate["sixth_full_audit_separator_rows"]])
    sixth_targets = ([Fraction(row["target"]) for row in screen_rows]
                     + [Fraction(x) for x in candidate["sixth_probe_targets"]]
                     + [Fraction(x) for x in candidate["sixth_full_audit_separator_targets"]])
    if len(sixth_rows) != 302:
        raise RuntimeError("expected 256 screened, 38 parent certified, and eight new full-domain Arb sixth rows")
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
    sixth = block_summary(sixth_records, "302 selected sixth rows (256 screen + 38 parent probes + 8 full-domain separators)")

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
    candidate, lp, candidate_sha, lp_sha, audit_sha, bank = load_inputs()
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
        "parent_complete_sixth_audit_sha256": audit_sha,
        "scope": (
            "Exact-rational 113-column cutting-plane candidate independently checked with 128-bit Arb "
            "on all 1,461 low rows, 302 selected sixth rows (including eight strict separators from "
            "the previous full-domain rejection), and seven selected eighth rows. The first 1,024 "
            "sixth-order orbits are additionally audited if selected rows pass. No complete sixth/eighth "
            "maximum, global physical optimum, or operational channel-error theorem."
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
