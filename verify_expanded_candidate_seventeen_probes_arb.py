"""128-bit Arb checks for the exact candidate with fifteen sixth-order separators."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from screen_ising_sixth_moments import orbit, target
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball
from verify_full_low_moment_certificate import FourthMoments, all_features

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_with_seventeen_sixth_probes_expanded_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_with_seventeen_sixth_probes_expanded_n21.json"
SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
PREFIXES = [
    (ROOT / "evidence/candidate_sixth_prefix_7row_n21.json", "6604c6727b075b79ceca438b01faadbbb0ebbd19"),
    (ROOT / "evidence/candidate_sixth_prefix_12row_n21.json", "4827a61b30abdfdab2675eac6df557e71081294e"),
    (ROOT / "evidence/candidate_sixth_prefix_8probe_n21.json", "6b655f83d87b9ea24f9394355ef1aa8c4633136e"),
    (ROOT / "evidence/candidate_sixth_prefix_14probe_n21.json", "8578b04b4af392e34b57673a24e83c0c710f8563"),
    (ROOT / "evidence/candidate_sixth_prefix_15probe_expanded_n21.json", "520c98d1d6bfea8f3b5676cdece12de7ff0ec7c8"),
]
PARENT_CANDIDATE_SHA256 = "ac789d6fa678a4759c13d3d5588253e57d63e5a448946bdd9bb915369d401d80"
OUTPUT_PATH = ROOT / "evidence/candidate_selected_moments_arb_with_seventeen_sixth_probes_expanded_n21.json"
CAP = Fraction(1, 3)


def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def strict_block(records, label):
    worst_midpoint = -1.0
    worst = None
    for record in records:
        absolute = abs(record["error"])
        if not absolute < ball(CAP):
            raise RuntimeError(f"{label} row failed strict Arb upper bound: {record}")
        midpoint = float(absolute)
        if midpoint > worst_midpoint:
            worst_midpoint = midpoint
            worst = {key: value for key, value in record.items() if key != "error"}
    return {
        "rows": len(records),
        "strict_upper": str(CAP),
        "worst_midpoint": worst_midpoint,
        "worst_row": worst,
    }


def main():
    ctx.prec = 128
    candidate_raw = CANDIDATE_PATH.read_bytes()
    candidate_sha = hashlib.sha256(candidate_raw).hexdigest()
    candidate = json.loads(candidate_raw)
    lp_raw = LP_PATH.read_bytes()
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    lp = json.loads(lp_raw)
    if lp.get("columns") != 93 or lp.get("rows") != 1739:
        raise RuntimeError("expanded LP transcript has unexpected dimensions")
    pricing_raw = (ROOT / "evidence/fifteen_probe_dual_pricing_arb_n21.json").read_bytes()
    pricing_sha = hashlib.sha256(pricing_raw).hexdigest()
    if candidate.get("pricing_arb_sha256") != pricing_sha:
        raise RuntimeError("candidate does not pin the Arb pricing certificate")
    if candidate.get("priced_added_columns") != lp.get("added_priced_columns"):
        raise RuntimeError("candidate and expanded LP priced-column lists disagree")
    if candidate["source_file"] != "evidence/joint_low_six_eighth_lp_with_seventeen_sixth_probes_expanded_n21.json":
        raise RuntimeError("candidate source-file path mismatch")
    if lp.get("columns") != 93 or lp.get("rows") != 1741:
        raise RuntimeError("seventeen-probe expanded LP has unexpected dimensions")
    if candidate["source_sha256"] != lp_sha:
        raise RuntimeError("candidate input does not pin the current LP transcript")
    if candidate["parent_candidate_input_sha256"] != PARENT_CANDIDATE_SHA256:
        raise RuntimeError("candidate parent-input hash mismatch")
    if candidate["support_size"] != len(candidate["exact_probabilities"]):
        raise RuntimeError("candidate support metadata mismatch")
    if len(candidate["sixth_probe_rows"]) != 17:
        raise RuntimeError("candidate does not contain seventeen sixth-order separators")
    if candidate["sixth_probe_rows"] != lp["sixth_probe_rows"]:
        raise RuntimeError("candidate and LP sixth-probe rows disagree")
    if candidate["sixth_probe_targets"] != lp["sixth_probe_targets"]:
        raise RuntimeError("candidate and LP sixth-probe targets disagree")
    if candidate["selected_eighth_rows"] != lp["selected_eighth_rows"]:
        raise RuntimeError("candidate and LP selected eighth rows disagree")
    if Fraction(candidate["exact_probability_sum"]) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")
    if candidate["columns"] != [int(row["column"]) for row in candidate["exact_probabilities"]]:
        raise RuntimeError("candidate column list and exact probabilities disagree")

    prefix_blob_shas = []
    for path, expected_blob in PREFIXES:
        actual_blob = git_blob_sha1(path.read_bytes())
        if actual_blob != expected_blob:
            raise RuntimeError(f"sixth-prefix transcript changed: {path.name}")
        prefix_blob_shas.append(actual_blob)
    if candidate["sixth_prefix_transcript_git_blob_sha1s"] != prefix_blob_shas:
        raise RuntimeError("candidate does not pin all four Arb sixth-prefix transcripts")

    all_columns, _, _ = canonical_ensemble()
    bank = []
    for record in candidate["exact_probabilities"]:
        column = int(record["column"])
        bank.append((ball(Fraction(record["probability"])),
                     rotation_entries_exact(all_columns[column])))
    if sum((Fraction(row["probability"]) for row in candidate["exact_probabilities"]), Fraction(0)) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")
    if any(Fraction(row["probability"]) <= 0 for row in candidate["exact_probabilities"]):
        raise RuntimeError("candidate contains a nonpositive probability")

    system = FourthMoments(21)
    system.exact_target_check()
    low_mixture = [arb(0) for _ in system.rational_target]
    for weight, entries in bank:
        features = all_features(system, entries)
        for index, value in enumerate(features):
            low_mixture[index] += weight * value
    low_records = []
    for index, (actual, target_value) in enumerate(zip(low_mixture, system.rational_target)):
        error = (actual - ball(target_value)) / ball(abs(target_value))
        low_records.append({
            "row": index,
            "order": 2 if index < 21 else 4,
            "error": error,
            "error_interval": str(error),
        })
    low = strict_block(low_records, "low")

    screen = json.loads(SCREEN_PATH.read_text())["records"]
    sixth_rows = [
        (tuple(row["indices"]), Fraction(row["target"]), "screen")
        for row in screen
    ]
    for indices, target_text in zip(candidate["sixth_probe_rows"], candidate["sixth_probe_targets"]):
        row = tuple(indices)
        exact_target = target(row)
        if exact_target != Fraction(target_text):
            raise RuntimeError(f"sixth-probe target sign mismatch for {row}")
        sixth_rows.append((row, exact_target, "arb_separator"))

    sixth_records = []
    for row_index, (indices, target_value, source) in enumerate(sixth_rows):
        group = orbit(indices)
        moment = arb(0)
        for weight, entries in bank:
            subtotal = arb(0)
            for subset in group:
                subtotal += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
            moment += weight * subtotal / len(group)
        error = (moment - ball(target_value)) / ball(abs(target_value))
        sixth_records.append({
            "row": row_index,
            "source": source,
            "indices": list(indices),
            "target": str(target_value),
            "error": error,
            "error_interval": str(error),
            "orbit_size": len(group),
        })
    sixth = strict_block(sixth_records, "sixth-selected")

    eighth_records = []
    for row_index, indices_list in enumerate(candidate["selected_eighth_rows"]):
        indices = tuple(indices_list)
        group = orbit(indices)
        moment = arb(0)
        for weight, entries in bank:
            subtotal = arb(0)
            for subset in group:
                subtotal += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
            moment += weight * subtotal / len(group)
        target_value = Fraction((-1) ** (sum(i % 2 for i in indices) + 4), 19721)
        error = (moment - ball(target_value)) / ball(abs(target_value))
        eighth_records.append({
            "row": row_index,
            "indices": list(indices),
            "target": str(target_value),
            "error": error,
            "error_interval": str(error),
            "orbit_size": len(group),
        })
    eighth = strict_block(eighth_records, "eighth-selected")

    result = {
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "parent_candidate_input_sha256": PARENT_CANDIDATE_SHA256,
        "sixth_prefix_transcript_git_blob_sha1s": prefix_blob_shas,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": len(bank),
        "exact_probability_sum": "1",
        "certified_blocks": {
            "low_all_rows": low,
            "sixth_screen_and_fifteen_probes": sixth,
            "eighth_selected_only": eighth,
        },
        "scope": (
            "Arb certification of all 1461 low rows, 271 selected sixth rows "
            "(256 screen plus fifteen strict separators), and seven selected eighth "
            "rows for this exact rational candidate. This is not a complete "
            "sixth/eighth maximum or an operational inversion bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "support_size": len(bank),
        "precision_bits": ctx.prec,
        "low_worst_midpoint": low["worst_midpoint"],
        "sixth_selected_worst_midpoint": sixth["worst_midpoint"],
        "selected_eighth_worst_midpoint": eighth["worst_midpoint"],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
