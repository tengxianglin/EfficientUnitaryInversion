"""Convert the seven-row binary64 LP output into an exact rational candidate input."""
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "evidence/joint_low_six_eighth_lp_with_probe_n21.json"
OUTPUT = ROOT / "evidence/candidate_joint_input_7row_n21.json"


def main():
    raw = SOURCE.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    lp = json.loads(raw)
    if lp["columns"] != 83 or lp["rows"] != 1724:
        raise RuntimeError("unexpected LP dimensions")
    if lp["row_blocks"] != {"low": 1461, "sixth_screen": 256, "selected_eighth": 7}:
        raise RuntimeError("unexpected LP row blocks")
    if lp["selected_eighth_rows"][-1] != [0, 1, 3, 14, 19, 24, 29, 40]:
        raise RuntimeError("Arb-certified separator row is missing")
    if not lp["lp_max"] < 1 / 3:
        raise RuntimeError("finite LP objective is not below 1/3")

    raw_weights = [(int(column), Fraction.from_float(float(weight)))
                   for column, weight in lp["lp_positive_weights"]]
    if not raw_weights or any(weight <= 0 for _, weight in raw_weights):
        raise RuntimeError("LP support contains a nonpositive reported weight")
    if len({column for column, _ in raw_weights}) != len(raw_weights):
        raise RuntimeError("duplicate physical column in LP support")

    total = sum((weight for _, weight in raw_weights), Fraction(0))
    probabilities = [
        {"column": column, "probability": str(weight / total)}
        for column, weight in raw_weights
    ]
    exact_sum = sum((Fraction(item["probability"]) for item in probabilities), Fraction(0))
    if exact_sum != 1:
        raise RuntimeError("exact rationalized probabilities do not sum to one")

    candidate = {
        "base_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "source_file": "evidence/joint_low_six_eighth_lp_with_probe_n21.json",
        "source_sha256": source_sha,
        "candidate_input_sha256": hashlib.sha256(
            (ROOT / "evidence/candidate_joint_input_n21.json").read_bytes()
        ).hexdigest(),
        "precision_bits": 64,
        "strict_upper": "1/3",
        "columns": [column for column, _ in raw_weights],
        "exact_probabilities": probabilities,
        "exact_probability_sum": "1",
        "support_size": len(probabilities),
        "rationalization": "Each HiGHS binary64 weight is converted exactly with Fraction.from_float, then the positive weights are normalized exactly.",
        "finite_lp_objective": repr(lp["lp_max"]),
        "selected_eighth_rows": lp["selected_eighth_rows"],
        "scope": "Exact rational probability input for a 32-column physical candidate derived from a finite binary64 LP; no moment certificate is implied.",
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
