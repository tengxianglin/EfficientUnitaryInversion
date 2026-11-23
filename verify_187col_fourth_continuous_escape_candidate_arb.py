"""128-bit Arb audit of an exact 187-column mixture on all 2,113 pinned rows.

This is a selected-design certificate only. A complete 63,133-orbit sixth-order
audit is a separate required step before any complete-sixth claim.
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
from verify_full_low_moment_certificate import all_features
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
from verify_55probe_151col_full_canonical_pool_arb import orbit_average_minor

LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_187col_fourth_continuous_escape_n21.json"
CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_187col_fourth_continuous_escape_n21.json"
PARENT_LP = ROOT / "evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json"
PARENT_DUAL = ROOT / "evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json"
CANDIDATE_152 = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
CUT_LP = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
OLD_ESCAPE_CERT = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SECOND_ESCAPE_CERT = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
THIRD_ESCAPE_CERT = ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json"
FOURTH_ESCAPE_CERT = ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json"
OUTPUT = ROOT / "evidence/candidate_187col_fourth_continuous_escape_arb_n21.json"
PRECISION_BITS = 128
CAP = Fraction(1, 3)
OLD_ESCAPE_COLUMN = 1641
NEW_ESCAPE_COLUMN = 1642
THIRD_ESCAPE_COLUMN = 1643
FOURTH_ESCAPE_COLUMN = 1644


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    paths = (LP_PATH, CANDIDATE_PATH, PARENT_LP, PARENT_DUAL, CANDIDATE_152,
             CUT_LP, OLD_ESCAPE_CERT, SECOND_ESCAPE_CERT, THIRD_ESCAPE_CERT, FOURTH_ESCAPE_CERT)
    raw = [path.read_bytes() for path in paths]
    (lp, candidate, parent_lp, parent_dual, candidate152, cut_lp,
     old_escape, second_escape, third_escape, fourth_escape) = [json.loads(value) for value in raw]
    (lp_sha, candidate_sha, parent_lp_sha, parent_dual_sha, candidate152_sha,
     cut_lp_sha, old_escape_sha, second_escape_sha, third_escape_sha, fourth_escape_sha) = map(sha, raw)

    if lp.get("status") != "187col_fourth_continuous_escape_lp_candidate_below_one_third" or not lp.get("finite_candidate_below_one_third"):
        raise RuntimeError("186-column LP did not produce a sub-one-third discovery")
    if candidate.get("source_sha256") != lp_sha:
        raise RuntimeError("exact candidate does not pin the 186-column LP transcript")
    if candidate.get("parent_186col_lp_sha256") != parent_lp_sha or candidate.get("parent_186col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("candidate does not pin the 184-column parent evidence")
    if candidate.get("first_continuous_escape_arb_certificate_sha256") != old_escape_sha:
        raise RuntimeError("candidate does not pin the first escape certificate")
    if candidate.get("second_continuous_escape_arb_certificate_sha256") != second_escape_sha or candidate.get("third_continuous_escape_arb_certificate_sha256") != third_escape_sha or candidate.get("fourth_continuous_escape_arb_certificate_sha256") != fourth_escape_sha:
        raise RuntimeError("candidate does not pin the second escape certificate")
    if candidate.get("canonical_all_columns_sha256_le_f64") != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("candidate and LP canonical-pool hashes disagree")
    if parent_dual.get("status") != "strict_186col_2113row_third_continuous_escape_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("186-column parent dual is not strictly Arb-certified")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("184-column parent dual/LP hash mismatch")
    if second_escape.get("status") != "certified_continuous_path_dual_escape" or not second_escape.get("strictly_positive") or third_escape.get("status") != "certified_continuous_path_dual_escape" or not third_escape.get("strictly_positive") or fourth_escape.get("status") != "certified_continuous_path_dual_escape" or not fourth_escape.get("strictly_positive"):
        raise RuntimeError("second continuous path is not Arb-certified")
    if third_escape.get("dual_certificate_sha256") != parent_lp.get("parent_185col_dual_certificate_sha256") or third_escape.get("lp_transcript_sha256") != parent_lp.get("parent_185col_lp_sha256"):
        raise RuntimeError("third escape does not pin the 185-column parent dual/LP")
    if fourth_escape.get("dual_certificate_sha256") != parent_dual_sha or fourth_escape.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("fourth escape does not pin the 186-column parent dual/LP")
    if old_escape.get("status") != "certified_continuous_path_dual_escape" or not old_escape.get("strictly_positive"):
        raise RuntimeError("first continuous path is not Arb-certified")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != old_escape_sha:
        raise RuntimeError("152-column ancestor does not pin the first escape")
    if candidate.get("source_file") != str(LP_PATH.relative_to(ROOT)):
        raise RuntimeError("candidate source-file metadata mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_sha = sha(np.asarray(all_columns, dtype="<f8").tobytes())
    if len(all_columns) != 1641 or all_sha != candidate["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical pool hash/count mismatch")

    old_couplings = [Fraction(x) for x in candidate["first_continuous_escape_couplings_exact"]]
    second_couplings = [Fraction(x) for x in candidate["second_continuous_escape_couplings_exact"]]
    third_couplings = [Fraction(x) for x in candidate["third_continuous_escape_couplings_exact"]]
    fourth_couplings = [Fraction(x) for x in candidate["fourth_continuous_escape_couplings_exact"]]
    if [str(x) for x in old_couplings] != old_escape["candidate_couplings_exact"]:
        raise RuntimeError("first escape input differs from its Arb certificate")
    if [str(x) for x in second_couplings] != second_escape["candidate_couplings_exact"]:
        raise RuntimeError("second escape input differs from its Arb certificate")
    if [str(x) for x in third_couplings] != third_escape["candidate_couplings_exact"]:
        raise RuntimeError("third escape input differs from its Arb certificate")
    if [str(x) for x in fourth_couplings] != fourth_escape["candidate_couplings_exact"]:
        raise RuntimeError("fourth escape input differs from its Arb certificate")
    for label, couplings in (("first", old_couplings), ("second", second_couplings), ("third", third_couplings), ("fourth", fourth_couplings)): 
        if len(couplings) != 42 or couplings[-1] != 0 or any(x <= 0 for x in couplings[:-1]):
            raise RuntimeError(f"{label} path is not a strictly-positive 41-edge open path")
    if len({tuple(old_couplings), tuple(second_couplings), tuple(third_couplings), tuple(fourth_couplings)}) != 4:
        raise RuntimeError("three continuous path generators are not pairwise distinct")

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
    if any(index < 0 or index > FOURTH_ESCAPE_COLUMN for index in probabilities):
        raise RuntimeError("candidate support contains an unknown physical column")
    if any(column not in candidate["column_order"] for column in (OLD_ESCAPE_COLUMN, NEW_ESCAPE_COLUMN, THIRD_ESCAPE_COLUMN, FOURTH_ESCAPE_COLUMN)): 
        raise RuntimeError("expanded physical inventory omits one continuous escape")

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    if len(system.rational_target) != 1461:
        raise RuntimeError("unexpected complete low-order row count")

    sixth_rows = [tuple(int(v) for v in row) for row in candidate["sixth_cut_rows"]]
    sixth_targets = [Fraction(v) for v in candidate["sixth_cut_targets"]]
    eighth_rows = [tuple(int(v) for v in row) for row in candidate["selected_eighth_rows"]]
    eighth_targets = [Fraction(v) for v in candidate["selected_eighth_targets"]]
    expected_sixth_rows = [tuple(int(v) for v in row) for row in cut_lp["sixth_cut_rows"]]
    expected_sixth_targets = [Fraction(v) for v in cut_lp["sixth_cut_targets"]]
    expected_eighth_rows = [tuple(int(v) for v in row) for row in cut_lp["selected_eighth_rows"]]
    expected_eighth_targets = [Fraction(v) for v in cut_lp["selected_eighth_targets"]]
    if sixth_rows != expected_sixth_rows or sixth_targets != expected_sixth_targets:
        raise RuntimeError("candidate sixth-row inventory differs from the pinned cut design")
    if eighth_rows != expected_eighth_rows or eighth_targets != expected_eighth_targets:
        raise RuntimeError("candidate eighth-row inventory differs from the pinned cut design")
    if len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected mixed-order row counts")
    if any(target(row) != value for row, value in zip(sixth_rows, sixth_targets)):
        raise RuntimeError("sixth target mismatch")

    low_mix = [arb(0) for _ in range(1461)]
    sixth_mix = [arb(0) for _ in range(len(sixth_rows))]
    eighth_mix = [arb(0) for _ in range(len(eighth_rows))]
    summaries = []
    for step, (column, probability) in enumerate(sorted(probabilities.items()), 1):
        if column == OLD_ESCAPE_COLUMN:
            couplings = old_couplings
        elif column == NEW_ESCAPE_COLUMN:
            couplings = second_couplings
        elif column == THIRD_ESCAPE_COLUMN:
            couplings = third_couplings
        elif column == FOURTH_ESCAPE_COLUMN:
            couplings = fourth_couplings
        else:
            couplings = all_columns[column]
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
        summaries.append({"column": column, "probability": str(probability)})
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
        record("sixth_selected_plus_cuts", row, actual, desired, Fraction(5, 19721))
    for row, (actual, desired) in enumerate(zip(eighth_mix, eighth_targets)):
        record("eighth_selected", row, actual, desired, Fraction(1, 19721))

    passed = all(row["strictly_below_one_third"] for row in row_results)
    row_bytes = json.dumps(row_results, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "status": "strict_187col_selected_row_candidate_certified" if passed else "187col_selected_row_candidate_failed",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "lp_transcript_sha256": lp_sha,
        "candidate_input_sha256": candidate_sha,
        "parent_186col_lp_sha256": parent_lp_sha,
        "parent_186col_dual_certificate_sha256": parent_dual_sha,
        "first_continuous_escape_arb_certificate_sha256": old_escape_sha,
        "second_continuous_escape_arb_certificate_sha256": second_escape_sha,
        "third_continuous_escape_arb_certificate_sha256": third_escape_sha,
        "fourth_continuous_escape_arb_certificate_sha256": fourth_escape_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_pool_size": len(all_columns),
        "candidate_support_size": len(probabilities),
        "exact_probability_sum": "1",
        "exact_probabilities": summaries,
        "certified_row_counts": {
            "low_complete": 1461,
            "sixth_selected_plus_cuts": len(sixth_rows),
            "eighth_selected": len(eighth_rows),
        },
        "total_certified_rows": len(row_results),
        "strict_cap": "1/3",
        "all_rows_strictly_below_one_third": passed,
        "maximum_absolute_error_upper_endpoint": str(max_upper),
        "maximum_error_row": max_row,
        "margin_to_one_third": str(ball(CAP) - max_upper),
        "row_transcript_sha256": sha(row_bytes),
        "rows": row_results,
        "scope": (
            "Strict Arb certificate for the exact rational mixture on all 1,461 second/fourth rows, "
            "645 pinned sixth rows, and seven selected eighth rows. This is not a complete 63,133-orbit "
            "sixth-order certificate, a complete eighth-order certificate, full-family optimality, "
            "or an operational Choi/diamond-norm theorem."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "support_size": len(probabilities),
        "total_certified_rows": len(row_results),
        "all_rows_strictly_below_one_third": passed,
        "maximum_absolute_error_upper_endpoint": str(max_upper),
        "maximum_error_row": max_row,
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)
    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
