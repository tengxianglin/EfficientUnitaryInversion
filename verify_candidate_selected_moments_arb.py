"""128-bit Arb verification of all low rows and the finite 256+7 selected higher rows."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from screen_ising_sixth_moments import orbit
from verify_full_low_moment_certificate import FourthMoments, all_features, rotation_entries
from verify_ising_moment_pricing import ball

CANDIDATE_PATH = ROOT / "evidence/candidate_joint_input_7row_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_with_probe_n21.json"
SIXTH_SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
OUTPUT_PATH = ROOT / "evidence/candidate_selected_moments_arb_n21.json"
CAP = Fraction(1, 3)


def strict_block(records, label):
    worst_midpoint = -1.0
    worst = None
    for record in records:
        error = record["error"]
        absolute = abs(error)
        if not absolute.upper() < ball(CAP):
            raise RuntimeError(f"{label} row failed strict Arb upper bound: {record}")
        midpoint = float(absolute)
        if midpoint > worst_midpoint:
            worst_midpoint = midpoint
            worst = {key: value for key, value in record.items() if key != 'error'}
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
        raise RuntimeError("candidate exact probabilities do not sum to one")
    if candidate["support_size"] != 32 or len(candidate["exact_probabilities"]) != 32:
        raise RuntimeError("unexpected candidate support")
    if candidate["columns"] != [int(x["column"]) for x in candidate["exact_probabilities"]]:
        raise RuntimeError("candidate column list and exact weights disagree")

    lp = json.loads(lp_raw)
    eighth_rows = [tuple(I) for I in lp["selected_eighth_rows"]]
    if eighth_rows != [tuple(I) for I in candidate["selected_eighth_rows"]]:
        raise RuntimeError("candidate and LP selected eighth rows disagree")

    all_columns, _, _ = canonical_ensemble()
    bank = []
    for item in candidate["exact_probabilities"]:
        column = int(item["column"])
        weight = ball(Fraction(item["probability"]))
        bank.append((weight, rotation_entries(all_columns[column])))

    # Complete low block: all 21 second rows and all 1,440 fourth-order orbits.
    system = FourthMoments(21)
    system.exact_target_check()
    low_mixture = [arb(0) for _ in system.rational_target]
    for weight, entries in bank:
        features = all_features(system, entries)
        for i, value in enumerate(features):
            low_mixture[i] += weight * value

    low_records = []
    for i, (actual, target) in enumerate(zip(low_mixture, system.rational_target)):
        error = (actual - ball(target)) / ball(abs(target))
        low_records.append({
            "row": i,
            "order": 2 if i < 21 else 4,
            "error": error,
            "error_interval": str(error),
        })
    low = strict_block(low_records, "low")

    # Frozen 256-row sixth-order screen. This is not the complete 63,133-orbit audit.
    screen = json.loads(SIXTH_SCREEN_PATH.read_text())["records"]
    sixth_records = []
    for row_index, row in enumerate(screen):
        indices = tuple(row["indices"])
        group_orbit = orbit(indices)
        moment = arb(0)
        for weight, entries in bank:
            subtotal = arb(0)
            for subset in group_orbit:
                subtotal += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
            moment += weight * subtotal / len(group_orbit)
        target = Fraction(row["target"])
        error = (moment - ball(target)) / ball(abs(target))
        sixth_records.append({
            "row": row_index,
            "indices": list(indices),
            "target": str(target),
            "error": error,
            "error_interval": str(error),
            "orbit_size": len(group_orbit),
        })
    sixth = strict_block(sixth_records, "sixth-screen")

    # All seven selected eighth-order rows, including the new Arb separator.
    eighth_records = []
    for row_index, indices in enumerate(eighth_rows):
        group_orbit = orbit(indices)
        moment = arb(0)
        for weight, entries in bank:
            subtotal = arb(0)
            for subset in group_orbit:
                subtotal += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
            moment += weight * subtotal / len(group_orbit)
        target = Fraction((-1) ** (sum(i % 2 for i in indices) + 4), 19721)
        error = (moment - ball(target)) / ball(abs(target))
        eighth_records.append({
            "row": row_index,
            "indices": list(indices),
            "target": str(target),
            "error": error,
            "error_interval": str(error),
            "orbit_size": len(group_orbit),
        })
    eighth = strict_block(eighth_records, "eighth-selected")

    result = {
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "seed_pool_sha256_le_f64": "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315",
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "support_size": len(bank),
        "exact_probability_sum": "1",
        "certified_blocks": {
            "low_all_rows": low,
            "sixth_screen_only": sixth,
            "eighth_selected_only": eighth,
        },
        "scope": "Arb certification of all 1461 low rows, 256 frozen sixth-screen rows, and seven selected eighth rows for the exact rational 32-column candidate; not a complete sixth/eighth maximum or operational inversion bound.",
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "candidate_input_sha256": candidate_sha,
        "lp_transcript_sha256": lp_sha,
        "support_size": len(bank),
        "precision_bits": ctx.prec,
        "low_worst_midpoint": low["worst_midpoint"],
        "sixth_screen_worst_midpoint": sixth["worst_midpoint"],
        "selected_eighth_worst_midpoint": eighth["worst_midpoint"],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
