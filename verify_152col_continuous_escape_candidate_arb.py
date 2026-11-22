"""128-bit Arb audit of the exact rational 152-column selected-row candidate.

The audit covers every second-/fourth-order row and all 311 pinned sixth-order
plus seven selected eighth-order rows.  It does not claim a complete sixth- or
eighth-order orbit maximum.
"""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import target
from joint_low_six_eighth_lp import EIGHTH_ROWS
from verify_full_low_moment_certificate import all_features
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
from verify_55probe_151col_full_canonical_pool_arb import orbit_average_minor
from verify_continuous_path_dual_escape_arb import CANDIDATE_SHA256

PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_151col_55probe_n21.json"
DUAL_CERT = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_continuous_escape_n21.json"
CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
SIXTH_SCREEN = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT = ROOT / "evidence/candidate_152col_selected_rows_arb_n21.json"
PRECISION_BITS = 128
CAP = Fraction(1, 3)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    parent_raw = PARENT_LP.read_bytes()
    dual_raw = DUAL_CERT.read_bytes()
    escape_raw = ESCAPE_CERT.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    candidate_raw = CANDIDATE_PATH.read_bytes()
    parent = json.loads(parent_raw)
    dual = json.loads(dual_raw)
    escape = json.loads(escape_raw)
    lp = json.loads(lp_raw)
    candidate = json.loads(candidate_raw)

    parent_sha, dual_sha, escape_sha = sha(parent_raw), sha(dual_raw), sha(escape_raw)
    lp_sha, candidate_sha = sha(lp_raw), sha(candidate_raw)
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("candidate input does not pin the 152-column LP transcript")
    if candidate.get("parent_lp_sha256") != parent_sha or candidate.get("parent_dual_certificate_sha256") != dual_sha:
        raise RuntimeError("candidate input does not pin the 151-column parent evidence")
    if candidate.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("candidate input does not pin the Arb escape certificate")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("continuous escape has no strict Arb certificate")
    if candidate.get("candidate_sha256") != CANDIDATE_SHA256 or escape.get("candidate_sha256") != CANDIDATE_SHA256:
        raise RuntimeError("continuous escape input hash mismatch")
    if lp.get("candidate_sha256") != CANDIDATE_SHA256 or not lp.get("finite_candidate_below_one_third"):
        raise RuntimeError("152-column LP did not pin the sub-one-third discovery")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != candidate["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical pool hash/count mismatch")
    escape_couplings = [Fraction(x) for x in candidate["escape_couplings_exact"]]
    if [str(x) for x in escape_couplings] != escape["candidate_couplings_exact"]:
        raise RuntimeError("candidate and Arb escape couplings disagree")
    if len(escape_couplings) != 42 or escape_couplings[-1] != 0 or any(x <= 0 for x in escape_couplings[:-1]):
        raise RuntimeError("escape generator is not a legal strictly-positive open path")

    probabilities = {
        int(row["column"]): Fraction(row["probability"])
        for row in candidate["exact_probabilities"]
    }
    if len(probabilities) != len(candidate["exact_probabilities"]):
        raise RuntimeError("duplicate candidate support columns")
    if sum(probabilities.values(), Fraction(0)) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")
    if candidate.get("exact_probability_sum") != "1" or candidate.get("support_size") != len(probabilities):
        raise RuntimeError("candidate support metadata mismatch")
    if sorted(probabilities) != sorted(int(x) for x in candidate["columns"]):
        raise RuntimeError("candidate column list and exact probability support disagree")
    if 1641 not in probabilities:
        raise RuntimeError("the new continuous escape is absent from the candidate support")
    if any(index < 0 or index > 1641 for index in probabilities):
        raise RuntimeError("candidate support contains an unknown column index")

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    if len(system.rational_target) != 1461:
        raise RuntimeError("unexpected complete low-row count")

    screen_records = json.loads(SIXTH_SCREEN.read_text())["records"]
    sixth_rows = [tuple(row["indices"]) for row in screen_records]
    sixth_targets = [Fraction(row["target"]) for row in screen_records]
    sixth_rows += [tuple(row) for row in parent["sixth_probe_rows"]]
    sixth_targets += [Fraction(x) for x in parent["sixth_probe_targets"]]
    sixth_rows += [tuple(row) for row in parent["sixth_full_audit_separator_rows"]]
    sixth_targets += [Fraction(x) for x in parent["sixth_full_audit_separator_targets"]]
    sixth_rows += [tuple(row) for row in parent["sixth_prefix_separator_rows"]]
    sixth_targets += [Fraction(x) for x in parent["sixth_prefix_separator_targets"]]
    sixth_rows += [tuple(row) for row in parent["sixth_additional_full_audit_separator_rows"]]
    sixth_targets += [Fraction(x) for x in parent["sixth_additional_full_audit_separator_targets"]]
    if len(sixth_rows) != 311 or any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("pinned sixth-row inventory/target mismatch")

    eighth_rows = [tuple(row) for row in parent["selected_eighth_rows"]]
    if [list(row) for row in eighth_rows] != EIGHTH_ROWS:
        raise RuntimeError("selected eighth-row inventory mismatch")
    eighth_targets = [
        Fraction((-1) ** (sum(index % 2 for index in row) + 4) * comb(21, 4), comb(42, 8))
        for row in eighth_rows
    ]

    low_mix = [arb(0) for _ in range(1461)]
    sixth_mix = [arb(0) for _ in range(311)]
    eighth_mix = [arb(0) for _ in range(7)]
    column_summaries = []
    for step, (column, probability) in enumerate(sorted(probabilities.items()), 1):
        couplings = escape_couplings if column == 1641 else all_columns[column]
        entries = rotation_entries_exact(couplings)
        weight = ball(probability)
        features = all_features(system, entries)
        if len(features) != 1461:
            raise RuntimeError("complete low feature vector has wrong dimension")
        for row, value in enumerate(features):
            low_mix[row] += weight * value
        for row, indices in enumerate(sixth_rows):
            sixth_mix[row] += weight * orbit_average_minor(entries, indices)
        for row, indices in enumerate(eighth_rows):
            eighth_mix[row] += weight * orbit_average_minor(entries, indices)
        column_summaries.append({"column": column, "probability": str(probability)})
        print(f"Arb-certified feature contribution {step}/{len(probabilities)} (column {column})", flush=True)

    row_results = []
    max_upper = None
    max_row = None

    def record(block, index, actual, desired, scale):
        nonlocal max_upper, max_row
        residual = (actual - ball(desired)) / ball(scale)
        error = abs(residual)
        upper = error.upper()
        passed = bool(error < ball(CAP))
        row_results.append({
            "block": block,
            "row": index,
            "normalized_residual_interval": str(residual),
            "absolute_error_upper_endpoint": str(upper),
            "strictly_below_one_third": passed,
        })
        if max_upper is None or upper > max_upper:
            max_upper, max_row = upper, {"block": block, "row": index}
        return passed

    for row, (actual, desired, scale) in enumerate(zip(low_mix, system.rational_target, low_scales)):
        record("low", row, actual, desired, scale)
    for row, (actual, desired) in enumerate(zip(sixth_mix, sixth_targets)):
        record("sixth_selected", row, actual, desired, Fraction(5, 19721))
    for row, (actual, desired) in enumerate(zip(eighth_mix, eighth_targets)):
        record("eighth_selected", row, actual, desired, Fraction(1, 19721))

    passed = all(row["strictly_below_one_third"] for row in row_results)
    row_bytes = json.dumps(row_results, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "status": "strict_selected_row_candidate_certified" if passed else "selected_row_candidate_failed",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "parent_lp_sha256": parent_sha,
        "parent_dual_certificate_sha256": dual_sha,
        "continuous_escape_arb_certificate_sha256": escape_sha,
        "lp_transcript_sha256": lp_sha,
        "candidate_input_sha256": candidate_sha,
        "candidate_sha256": CANDIDATE_SHA256,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_pool_size": len(all_columns),
        "candidate_support_size": len(probabilities),
        "exact_probability_sum": "1",
        "exact_probabilities": column_summaries,
        "certified_row_counts": {"low_complete": 1461, "sixth_selected": 311, "eighth_selected": 7},
        "total_certified_rows": len(row_results),
        "strict_cap": "1/3",
        "all_rows_strictly_below_one_third": passed,
        "maximum_absolute_error_upper_endpoint": str(max_upper),
        "maximum_error_row": max_row,
        "margin_to_one_third": str(ball(CAP) - max_upper),
        "row_transcript_sha256": sha(row_bytes),
        "rows": row_results,
        "scope": (
            "Strict Arb certificate for the exact rational mixture on all 1,461 second/fourth rows "
            "and the 311 selected sixth plus seven selected eighth rows. The sixth/eighth subsets "
            "are not their complete orbit domains; this is not a complete all-moment, full-family "
            "optimality, or Choi/diamond-norm operational theorem."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "support_size": len(probabilities),
        "total_rows": len(row_results),
        "all_rows_strictly_below_one_third": passed,
        "maximum_absolute_error_upper_endpoint": str(max_upper),
        "maximum_error_row": max_row,
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)
    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
