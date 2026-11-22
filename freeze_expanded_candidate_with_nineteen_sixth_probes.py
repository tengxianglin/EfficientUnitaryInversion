"""Freeze exact rational weights for the 93-column expanded LP with nineteen certified sixth-order probes."""
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "evidence/joint_low_six_eighth_lp_with_nineteen_sixth_probes_expanded_n21.json"
OUTPUT = ROOT / "evidence/candidate_joint_input_with_nineteen_sixth_probes_expanded_n21.json"
PARENT_CANDIDATE_SHA256 = "028b3d27e291bb6963d247ee41ef8e7728c5a044b09c8c6fd02a12d2e349bfaa"
PREFIX_BLOBS = [
    "6604c6727b075b79ceca438b01faadbbb0ebbd19",
    "4827a61b30abdfdab2675eac6df557e71081294e",
    "6b655f83d87b9ea24f9394355ef1aa8c4633136e",
    "8578b04b4af392e34b57673a24e83c0c710f8563",
    "520c98d1d6bfea8f3b5676cdece12de7ff0ec7c8",
    "4c4ba9931ecaf8c5b0878831d7e687ff7f5a7137",
]


def main():
    raw = SOURCE.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    lp = json.loads(raw)
    expected_blocks = {
        "low": 1461,
        "sixth_screen": 256,
        "sixth_certified_probes": 19,
        "selected_eighth": 7,
    }
    if lp["columns"] != 93 or lp["rows"] != 1743 or lp["row_blocks"] != expected_blocks:
        raise RuntimeError("unexpected LP dimensions or row blocks")
    if lp["parent_candidate_input_sha256"] != PARENT_CANDIDATE_SHA256:
        raise RuntimeError("LP transcript refers to a different parent candidate")
    if [row["git_blob_sha1"] for row in lp["sixth_prefix_transcripts"]] != PREFIX_BLOBS:
        raise RuntimeError("LP transcript does not pin all six Arb prefix certificates")
    if not lp["finite_candidate_below_cap"] or not lp["lp_max"] < 1 / 3:
        raise RuntimeError("finite LP objective is not strictly below 1/3")
    if len(lp["sixth_probe_rows"]) != 19 or len(lp["sixth_probe_targets"]) != 19:
        raise RuntimeError("LP transcript does not contain nineteen sixth-order probes")

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
        "source_file": "evidence/joint_low_six_eighth_lp_with_nineteen_sixth_probes_expanded_n21.json",
        "source_sha256": source_sha,
        "parent_candidate_input_sha256": PARENT_CANDIDATE_SHA256,
        "sixth_prefix_transcript_git_blob_sha1s": PREFIX_BLOBS,
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
        "expanded_pool_columns": lp["columns"],
        "priced_added_columns": lp["added_priced_columns"],
        "pricing_arb_sha256": lp["pricing_arb_sha256"],
        "pricing_screen_sha256": lp["pricing_screen_sha256"],
        "dual_certificate_sha256": lp["dual_certificate_sha256"],
        "canonical_all_columns_sha256_le_f64": lp["canonical_all_columns_sha256_le_f64"],
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
