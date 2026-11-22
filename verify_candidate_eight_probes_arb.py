"""128-bit Arb checks for the exact candidate with eight sixth-order separators."""
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

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_with_eight_sixth_probes_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_with_eight_sixth_probes_n21.json"
SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
PREFIXES = [
    (ROOT / "evidence/candidate_sixth_prefix_7row_n21.json", "6604c6727b075b79ceca438b01faadbbb0ebbd19"),
    (ROOT / "evidence/candidate_sixth_prefix_12row_n21.json", "4827a61b30abdfdab2675eac6df557e71081294e"),
]
OUTPUT_PATH = ROOT / "evidence/candidate_selected_moments_arb_with_eight_sixth_probes_n21.json"
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
    if candidate["source_sha256"] != lp_sha:
        raise RuntimeError("candidate input does not pin the current LP transcript")
    if Fraction(candidate["exact_probability_sum"]) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")
    if candidate["support_size"] != len(candidate["exact_probabilities"]):
        raise RuntimeError("candidate support metadata mismatch")

    prefix_blob_shas = []
    for path, expected_blob in PREFIXES:
        raw = path.read_bytes()
        actual_blob = git_blob_sha1(raw)
        if actual_blob != expected_blob:
            raise RuntimeError(f"sixth-prefix transcript changed: {path.name}")
        prefix_blob_shas.append(actual_blob)
    if candidate["sixth_prefix_transcript_git_blob_sha1s"] != prefix_blob_shas:
        raise RuntimeError("candidate does not pin both Arb sixth-prefix transcripts")

    all_columns, _, _ = canonical_ensemble()
    bank = []
    for record in candidate["exact_probabilities"]:
        column = int(record["column"])
        bank.append((ball(Fraction(record["probability"])),
                     rotation_entries_exact(all_columns[column])))
    if sum((Fraction(row["probability"]) for row in candidate["exact_probabilities"]), Fraction(0)) != 1:
        raise RuntimeError("exact candidate probabilities do not sum to one")

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
        "sixth_prefix_transcript_git_blob_sha1s": prefix_blob_shas,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": len(bank),
        "exact_probability_sum": "1",
        "certified_blocks": {
            "low_all_rows": low,
            "sixth_screen_and_eight_probes": sixth,
            "eighth_selected_only": eighth,
        },
        "scope": (
            "Arb certification of all 1461 low rows, 264 selected sixth rows "
            "(256 screen plus eight strict separators), and seven selected eighth "
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
