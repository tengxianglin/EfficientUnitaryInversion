"""Freeze exact rational weights for the LP with five certified sixth-order probes."""
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "evidence/joint_low_six_eighth_lp_with_sixth_probes_n21.json"
OUTPUT = ROOT / "evidence/candidate_joint_input_with_sixth_probes_n21.json"
PARENT_CANDIDATE_SHA256 = "403614d80d8c5eeb15d56960fc7503103f8d376a7ab990fcb8988b1850d1a54d"
PREFIX_GIT_BLOB_SHA1 = "6604c6727b075b79ceca438b01faadbbb0ebbd19"


def main():
    raw = SOURCE.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    lp = json.loads(raw)
    expected_blocks = {
        "low": 1461,
        "sixth_screen": 256,
        "sixth_certified_probes": 5,
        "selected_eighth": 7,
    }
    if lp["columns"] != 83 or lp["rows"] != 1729 or lp["row_blocks"] != expected_blocks:
        raise RuntimeError("unexpected LP dimensions or row blocks")
    if lp["parent_candidate_input_sha256"] != PARENT_CANDIDATE_SHA256:
        raise RuntimeError("LP transcript refers to a different parent candidate")
    if lp["sixth_prefix_transcript_git_blob_sha1"] != PREFIX_GIT_BLOB_SHA1:
        raise RuntimeError("LP transcript does not pin the Arb sixth-order separators")
    if not lp["finite_candidate_below_cap"] or not lp["lp_max"] < 1 / 3:
        raise RuntimeError("finite LP objective is not strictly below 1/3")

    raw_weights = [
        (int(column), Fraction.from_float(float(weight)))
        for column, weight in lp["lp_positive_weights"]
    ]
    if not raw_weights or any(weight <= 0 for _, weight in raw_weights):
        raise RuntimeError("LP support contains a nonpositive reported weight")
    if len({column for column, _ in raw_weights}) != len(raw_weights):
        raise RuntimeError("duplicate physical column in LP support")
    total = sum((weight for _, weight in raw_weights), Fraction(0))
    probabilities = [
        {"column": column, "probability": str(weight / total)}
        for column, weight in raw_weights
    ]
    exact_sum = sum((Fraction(row["probability"]) for row in probabilities), Fraction(0))
    if exact_sum != 1:
        raise RuntimeError("exact rational probabilities do not sum to one")

    candidate = {
        "base_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "source_file": "evidence/joint_low_six_eighth_lp_with_sixth_probes_n21.json",
        "source_sha256": source_sha,
        "parent_candidate_input_sha256": PARENT_CANDIDATE_SHA256,
        "sixth_prefix_transcript_git_blob_sha1": PREFIX_GIT_BLOB_SHA1,
        "precision_bits": 64,
        "strict_upper": "1/3",
        "columns": [column for column, _ in raw_weights],
        "exact_probabilities": probabilities,
        "exact_probability_sum": "1",
        "support_size": len(probabilities),
        "rationalization": "Each HiGHS binary64 weight is converted exactly with Fraction.from_float, then the positive support is normalized exactly.",
        "finite_lp_objective": repr(lp["lp_max"]),
        "sixth_probe_rows": lp["sixth_probe_rows"],
        "sixth_probe_targets": lp["sixth_probe_targets"],
        "selected_eighth_rows": lp["selected_eighth_rows"],
        "scope": "Exact rational input for a finite physical candidate; moment claims require the separate Arb transcript.",
    }
    OUTPUT.write_text(json.dumps(candidate, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "source_sha256": source_sha,
        "support_size": len(probabilities),
        "exact_probability_sum": str(exact_sum),
        "finite_lp_objective": lp["lp_max"],
    }, indent=2))


if __name__ == "__main__":
    main()
