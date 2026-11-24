"""Independent Arb check of general gapped-path pricing candidates.

The discovery optimizer is floating point.  This verifier reconstructs the
candidate couplings as exact decimal rationals, rebuilds the 42x42 physical
rotation, and evaluates the frozen 80-term separator with Arb.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from ising_fourth_moments import FourthMoments
from verify_ising_low_moment_design import build_rotation, rational
from verify_ising_full_fourth_fractional_grid_dual_arb import full_score

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_fractional_grid_n21.json"
FINITE_CERT = ROOT / "evidence/ising_full_fourth_fractional_grid_dual_arb_n21.json"
CONTINUOUS_CERT = ROOT / "evidence/ising_full_fourth_continuous_single_path_n21.json"
SEARCH = ROOT / "evidence/ising_full_fourth_general_gapped_search_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_general_gapped_escape_arb_n21.json"
PRECISION_BITS = 256


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    finite_raw = FINITE_CERT.read_bytes()
    continuous_raw = CONTINUOUS_CERT.read_bytes()
    search_raw = SEARCH.read_bytes()
    diagnostic = json.loads(diagnostic_raw)
    finite = json.loads(finite_raw)
    continuous = json.loads(continuous_raw)
    search = json.loads(search_raw)

    diagnostic_sha = hashlib.sha256(diagnostic_raw).hexdigest()
    finite_sha = hashlib.sha256(finite_raw).hexdigest()
    if finite.get("status") != "arb_certified_finite_6123_column_full_fourth_separator":
        raise RuntimeError("finite-grid separator certificate is not valid")
    if finite.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("finite certificate does not pin the current diagnostic")
    if continuous.get("status") != "arb_certified_continuous_single_open_path_separator":
        raise RuntimeError("continuous single-path certificate is not valid")
    if continuous.get("finite_grid_certificate_sha256") != finite_sha:
        raise RuntimeError("continuous certificate does not pin the current finite certificate")
    if search.get("pins", {}).get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("search result used a different diagnostic")
    if search.get("pins", {}).get("finite_certificate_sha256") != finite_sha:
        raise RuntimeError("search result used a different finite certificate")

    coefficient_by_feature = {
        int(item["feature_index"]): Fraction(item["coefficient"])
        for item in finite["dual_coefficients_exact_decimal_rationals"]
    }
    if len(coefficient_by_feature) != 80:
        raise RuntimeError("expected the frozen 80-term rational separator")
    system = FourthMoments(21)
    target_score = sum(
        (
            rational(coefficient_by_feature[index])
            * rational(system.rational_target[index])
            for index in coefficient_by_feature
        ),
        arb(0),
    )
    finite_target = arb(finite["target_score_interval"])
    if not (target_score - finite_target).contains(0):
        raise RuntimeError("exact target score does not match the pinned Arb interval")

    candidates = {}
    for kind in ("connected", "multisegment"):
        record = search.get(f"best_{kind}")
        if record is None:
            continue
        couplings = [Fraction(value) for value in record["couplings_exact_decimal"]]
        if len(couplings) != 42 or couplings[-1] != 0:
            raise RuntimeError(f"{kind} candidate does not have exactly one wrap cut")
        if any(value < 0 for value in couplings[:-1]):
            raise RuntimeError(f"{kind} candidate has a negative coupling after sign-gauge reduction")
        zero_edges = [j for j, value in enumerate(couplings[:-1]) if value == 0]
        if kind == "connected" and zero_edges:
            raise RuntimeError("connected candidate unexpectedly has an internal zero edge")
        if kind == "multisegment" and not zero_edges:
            raise RuntimeError("multi-segment candidate has no internal cut")

        atom = {
            "kind": "gapped",
            "couplings": [str(value) for value in couplings],
        }
        rotation = build_rotation(atom)
        orthogonality_checks = 0
        for row in range(42):
            for column in range(42):
                inner = sum(
                    (rotation[k, row] * rotation[k, column] for k in range(42)),
                    arb(0),
                )
                expected = arb(1) if row == column else arb(0)
                defect = inner - expected
                if not defect.contains(0):
                    raise RuntimeError(
                        f"{kind} candidate is not Arb-certified orthogonal at "
                        f"({row},{column}): {defect}"
                    )
                orthogonality_checks += 1
        determinant = rotation.det()
        if not determinant.contains(1):
            raise RuntimeError(
                f"{kind} candidate determinant is not certified to equal one: {determinant}"
            )
        score = full_score(rotation, system, coefficient_by_feature)
        gap = target_score - score
        discovery_score = float(record["score_float"])
        discrepancy = abs(float(score) - discovery_score)
        if discrepancy > 2e-7:
            raise RuntimeError(
                f"{kind} Arb score disagrees with floating discovery by {discrepancy}"
            )
        escaped = gap.upper() < 0
        separated = gap.lower() > 0
        candidates[kind] = {
            "label": record["label"],
            "optimized": record["optimized"],
            "couplings_exact_rational": [str(value) for value in couplings],
            "internal_zero_edges": zero_edges,
            "discovery_score_float": record["score_float"],
            "discovery_gap_float": record["target_minus_score_float"],
            "arb_score_interval": str(score),
            "arb_target_minus_score_interval": str(gap),
            "float_arb_midpoint_discrepancy": discrepancy,
            "orthogonality_matrix_entries_checked": orthogonality_checks,
            "orthogonality_all_interval_defects_contain_zero": True,
            "determinant_interval": str(determinant),
            "determinant_contains_one": True,
            "strict_separator_escape_certified": escaped,
            "strictly_below_target_certified": separated,
        }

    if not candidates:
        raise RuntimeError("search output contains no candidates")
    escape_kinds = [kind for kind, value in candidates.items()
                    if value["strict_separator_escape_certified"]]
    ambiguous_kinds = [kind for kind, value in candidates.items()
                       if not value["strict_separator_escape_certified"]
                       and not value["strictly_below_target_certified"]]
    if escape_kinds:
        status = "arb_certified_general_gapped_separator_escape"
    elif ambiguous_kinds:
        status = "arb_candidate_score_ambiguous"
    else:
        status = "no_escape_in_this_finite_multistart_search"

    result = {
        "status": status,
        "complete": True,
        "precision_bits": PRECISION_BITS,
        "interval_backend": "python-flint / Arb",
        "diagnostic_sha256": diagnostic_sha,
        "finite_certificate_sha256": finite_sha,
        "continuous_certificate_sha256": hashlib.sha256(continuous_raw).hexdigest(),
        "search_sha256": hashlib.sha256(search_raw).hexdigest(),
        "target_score_interval": str(target_score),
        "candidate_results": candidates,
        "escape_kinds": escape_kinds,
        "ambiguous_kinds": ambiguous_kinds,
        "proof_scope": (
            "If an escape is certified, it is one exact positive-coupling connected "
            "open path or a multi-segment open path with the wrap edge cut. This "
            "refutes extension of this particular frozen separator to the tested "
            "general gapped family. It does not establish a positive ensemble, a "
            "global no-go, or a channel diamond-distance bound. If no escape is "
            "certified, only the listed finite search candidates have been checked; "
            "there is no global separation conclusion."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": status,
        "precision_bits": PRECISION_BITS,
        "escape_kinds": escape_kinds,
        "candidates": {
            kind: {
                "score": value["arb_score_interval"],
                "gap": value["arb_target_minus_score_interval"],
                "zero_edges": value["internal_zero_edges"],
            }
            for kind, value in candidates.items()
        },
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
