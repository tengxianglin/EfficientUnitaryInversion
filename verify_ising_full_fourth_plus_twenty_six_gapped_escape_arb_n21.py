"""Independent 256-bit Arb verification of escapes from the 6,149-column dual.

The pricing search is floating-point discovery. This verifier reconstructs each
candidate coupling from its frozen decimal string as an exact rational,
rebuilds the 42x42 rotation with Arb, checks all orthogonality entries and
determinant, and evaluates the exact rational 106-term dual.

A certified escape refutes only extension of this particular finite-pool dual
to the full gapped family; it is not a global feasibility/no-go theorem.
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
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_twenty_six_gapped_n21.json"
FINITE_CERT = ROOT / "evidence/ising_full_fourth_plus_twenty_six_gapped_arb_n21.json"
SEARCH = ROOT / "evidence/ising_full_fourth_plus_twenty_six_gapped_search_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_plus_twenty_six_gapped_escape_arb_n21.json"
PRECISION_BITS = 256


def main():
    ctx.prec = PRECISION_BITS
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    finite_raw = FINITE_CERT.read_bytes()
    search_raw = SEARCH.read_bytes()
    diagnostic = json.loads(diagnostic_raw)
    finite = json.loads(finite_raw)
    search = json.loads(search_raw)

    diagnostic_sha = hashlib.sha256(diagnostic_raw).hexdigest()
    finite_sha = hashlib.sha256(finite_raw).hexdigest()
    search_sha = hashlib.sha256(search_raw).hexdigest()

    if finite.get("status") != "arb_certified_finite_6149_column_full_fourth_plus_twenty_six_gapped_separator":
        raise RuntimeError("the 6,149-column Arb certificate is invalid")
    if not finite.get("complete") or finite.get("candidate_count") != 6149:
        raise RuntimeError("the 6,149-column Arb certificate is incomplete")
    if finite.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("the finite certificate does not pin the current discovery diagnostic")
    if diagnostic.get("candidate_count") != 6149 or len(diagnostic.get("appended_gapped_columns", [])) != 26:
        raise RuntimeError("the discovery diagnostic does not contain the exact 6,149-column/twenty-six-gapped pool")
    if finite.get("general_gapped_count") != 26 or finite.get("full_feature_count") != 1461:
        raise RuntimeError("the finite certificate has unexpected gapped or full-feature dimensions")
    if finite.get("dual_scaled_l1_exact") != "1" or finite.get("dual_full_coordinate_l1_upper_bound") != 533:
        raise RuntimeError("the finite certificate lacks exact dual normalization/norm bound")
    if finite.get("dual_nonzero_coefficients") != 106:
        raise RuntimeError("the finite certificate does not contain the expected 106-term dual")
    if search.get("status") not in {
        "floating_general_gapped_separator_escape_candidate",
        "no_escape_found_in_deterministic_multistart_search",
    } or not search.get("complete"):
        raise RuntimeError("the 6,149-dual search did not report a completed deterministic search")
    pins = search.get("pins", {})
    if pins.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("search result is not pinned to the current 6,149-column diagnostic")
    if pins.get("finite_certificate_sha256") != finite_sha:
        raise RuntimeError("search result is not pinned to the current 6,149-column Arb certificate")

    coefficient_by_feature = {
        int(item["feature_index"]): Fraction(item["coefficient"])
        for item in finite["dual_coefficients_exact_rational"]
    }
    if len(coefficient_by_feature) != 106:
        raise RuntimeError("expected the exact rational 106-term dual")
    if finite.get("dual_scaled_l1_exact") != "1":
        raise RuntimeError("the exact dual scaled-l1 normalization is missing")

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
        raise RuntimeError("exact dual target score disagrees with the finite-pool Arb certificate")

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
        if kind == "connected" and any(value <= 0 for value in couplings[:-1]):
            raise RuntimeError("connected candidate is not strictly positive on all 41 interior edges")
        if kind == "multisegment" and not zero_edges:
            raise RuntimeError("multi-segment candidate has no internal cut")
        if kind == "multisegment" and zero_edges != record.get("internal_zero_edges", []):
            raise RuntimeError("multi-segment candidate zero-edge metadata is inconsistent")

        atom = {"kind": "gapped", "couplings": [str(value) for value in couplings]}
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
            "minimum_positive_coupling": str(min(value for value in couplings[:-1] if value > 0)),
            "maximum_coupling": str(max(couplings[:-1])),
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
    escape_kinds = [
        kind for kind, value in candidates.items()
        if value["strict_separator_escape_certified"]
    ]
    ambiguous_kinds = [
        kind for kind, value in candidates.items()
        if not value["strict_separator_escape_certified"]
        and not value["strictly_below_target_certified"]
    ]
    if escape_kinds:
        status = "arb_certified_6149_dual_general_gapped_escape"
    elif ambiguous_kinds:
        status = "arb_6149_dual_candidate_score_ambiguous"
    else:
        status = "no_escape_in_this_finite_multistart_search"

    result = {
        "status": status,
        "complete": True,
        "precision_bits": PRECISION_BITS,
        "interval_backend": "python-flint / Arb",
        "diagnostic_sha256": diagnostic_sha,
        "finite_certificate_sha256": finite_sha,
        "search_sha256": search_sha,
        "target_score_interval": str(target_score),
        "candidate_results": candidates,
        "escape_kinds": escape_kinds,
        "ambiguous_kinds": ambiguous_kinds,
        "proof_scope": (
            "A certified candidate with y^T(b-F(R(c)))<0 is an exact escape "
            "from this particular rational dual, which is rigorously positive "
            "on the 6,149-column finite pool. A connected escape has all 41 "
            "interior couplings strictly positive and the wrap edge zero. This "
            "refutes extending this dual unchanged to the full connected "
            "general-gapped family. It does not invalidate the finite-pool "
            "certificate, prove global feasibility/infeasibility, construct an "
            "all-even-minor ensemble, or imply a Choi/diamond-distance bound. "
            "A failure to find an escape would certify only the listed finite "
            "multistart candidates, not a continuum upper bound."
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
                "minimum_positive_coupling": value["minimum_positive_coupling"],
            }
            for kind, value in candidates.items()
        },
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
