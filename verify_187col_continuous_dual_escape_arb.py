"""Independent 128-bit Arb verification of a continuous-path escape from the 187-column dual."""
import hashlib
import json
from fractions import Fraction

import numpy as np
from flint import ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    orbit_average_minor,
)
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_187col_fourth_continuous_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_187col_fourth_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DISCOVERY_PATH = ROOT / "evidence/187col_continuous_dual_search_n21.json"
OUTPUT_PATH = ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json"
FIRST_ESCAPE_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SECOND_ESCAPE_PATH = ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json"
THIRD_ESCAPE_PATH = ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json"
FOURTH_ESCAPE_PATH = ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json"
PARENT_186_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json"
PARENT_186_DUAL_PATH = ROOT / "evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json"
PRECISION_BITS = 128


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        CERT_PATH, LP_PATH, CUT_LP_PATH, DISCOVERY_PATH,
        FIRST_ESCAPE_PATH, SECOND_ESCAPE_PATH, THIRD_ESCAPE_PATH, FOURTH_ESCAPE_PATH,
        PARENT_186_LP_PATH, PARENT_186_DUAL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    (cert, lp, cut_lp, discovery, first_escape, second_escape, third_escape,
     fourth_escape, parent_186_lp, parent_186_dual) = [
        json.loads(value) for value in raw
    ]
    (cert_sha, lp_sha, cut_sha, discovery_sha, first_sha, second_sha,
     third_sha, fourth_sha, parent_186_lp_sha, parent_186_dual_sha) = map(sha, raw)

    base = {
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_sha,
        "discovery_sha256": discovery_sha,
        "first_escape_certificate_sha256": first_sha,
        "second_escape_certificate_sha256": second_sha,
        "third_escape_certificate_sha256": third_sha,
        "fourth_escape_certificate_sha256": fourth_sha,
        "parent_186col_lp_sha256": parent_186_lp_sha,
        "parent_186col_dual_certificate_sha256": parent_186_dual_sha,
        "search_scope": discovery.get("search_domain"),
        "scope": (
            "A strictly positive Arb pricing interval is a counterexample to extending this "
            "specific 187-column dual over the full positive-coupling path family. A failed "
            "local search is not a global separation proof."
        ),
    }

    if cert.get("status") != "strict_187col_2113row_fourth_continuous_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("187-column parent dual is not strictly Arb-certified")
    if cert.get("lp_transcript_sha256") != lp_sha or lp.get("columns") != 187 or lp.get("rows") != 2113:
        raise RuntimeError("187-column certificate/LP dimensions or hash mismatch")
    if lp.get("cut_lp_transcript_sha256") != cut_sha or cert.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("187-column LP/certificate does not pin the 2,113-row cut inventory")
    if discovery.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("discovery does not pin the exact 187-column dual")
    if discovery.get("lp_transcript_sha256") != lp_sha or discovery.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("discovery LP/cut-row provenance mismatch")
    if discovery.get("prior_escape_certificate_sha256") != fourth_sha:
        raise RuntimeError("discovery does not pin the fourth certified escape used as its search seed")

    if parent_186_dual.get("status") != "strict_186col_2113row_third_continuous_escape_minimax_obstruction" or not parent_186_dual.get("complete"):
        raise RuntimeError("186-column parent dual is not strictly certified")
    if parent_186_dual.get("lp_transcript_sha256") != parent_186_lp_sha:
        raise RuntimeError("186-column parent dual/LP hash mismatch")
    if cert.get("parent_186col_lp_sha256") != parent_186_lp_sha or cert.get("parent_186col_dual_certificate_sha256") != parent_186_dual_sha:
        raise RuntimeError("187-column certificate does not pin the exact 186-column parent")
    if fourth_escape.get("dual_certificate_sha256") != parent_186_dual_sha or fourth_escape.get("lp_transcript_sha256") != parent_186_lp_sha:
        raise RuntimeError("fourth escape does not pin the exact 186-column parent dual/LP")
    if third_escape.get("dual_certificate_sha256") != parent_186_dual.get("parent_185col_dual_certificate_sha256") or third_escape.get("lp_transcript_sha256") != parent_186_dual.get("parent_185col_lp_sha256"):
        raise RuntimeError("third escape does not pin the 185-column parent dual/LP")

    escapes = (first_escape, second_escape, third_escape, fourth_escape)
    escape_shas = (first_sha, second_sha, third_sha, fourth_sha)
    for index, escape in enumerate(escapes, 1):
        if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
            raise RuntimeError(f"continuous escape {index} is not strictly Arb-certified")
    expected_hashes = (
        cert.get("first_continuous_escape_arb_certificate_sha256"),
        cert.get("second_continuous_escape_arb_certificate_sha256"),
        cert.get("third_continuous_escape_arb_certificate_sha256"),
        cert.get("fourth_continuous_escape_arb_certificate_sha256"),
    )
    if tuple(expected_hashes) != escape_shas:
        raise RuntimeError("187-column certificate does not pin all four prior escape certificates")
    lp_hashes = tuple(lp.get(key) for key in (
        "first_continuous_escape_arb_certificate_sha256",
        "second_continuous_escape_arb_certificate_sha256",
        "third_continuous_escape_arb_certificate_sha256",
        "fourth_continuous_escape_arb_certificate_sha256",
    ))
    if lp_hashes != escape_shas:
        raise RuntimeError("187-column LP does not pin all four prior escape certificates")

    if not discovery.get("candidate_found"):
        result = {
            **base,
            "status": "no_positive_candidate_in_local_search",
            "complete": True,
            "candidate_found": False,
            "strictly_positive": False,
            "records_checked": len(discovery.get("records", [])),
        }
        OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        return

    coupling_strings = discovery.get("best_candidate_couplings_exact")
    if not isinstance(coupling_strings, list) or len(coupling_strings) != 42:
        raise RuntimeError("discovery candidate must contain 42 exact coupling strings")
    couplings = [Fraction(x) for x in coupling_strings]
    if couplings[-1] != 0 or any(x <= 0 for x in couplings[:-1]):
        raise RuntimeError("candidate is not a strictly-positive 41-edge open path")
    candidate_sha = sha(json.dumps(coupling_strings, separators=(",", ":")).encode())

    columns, _, _ = canonical_ensemble()
    candidate_float = np.asarray([float(x) for x in couplings], dtype="<f8")
    if any(np.array_equal(candidate_float, np.asarray(column, dtype="<f8")) for column in columns):
        raise RuntimeError("candidate duplicates a canonical generator")
    prior_paths = [
        [Fraction(x) for x in escape["candidate_couplings_exact"]]
        for escape in escapes
    ]
    if any(couplings == prior for prior in prior_paths):
        raise RuntimeError("candidate duplicates one of the four previously certified continuous paths")

    system, low_scales, sixth_rows, eighth_rows, y, blocks = load_exact_design(cut_lp)
    z = [Fraction(x) for x in cert["dual_vector_rational"]]
    if len(z) != 2113 or sum((abs(x) for x in z), Fraction(0)) > 1:
        raise RuntimeError("exact dual dimension or L1 normalization mismatch")
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
    active = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active if i < 1461]
    active_sixth = [i for i in active if 1461 <= i < 2106]
    active_eighth = [i for i in active if i >= 2106]
    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }

    entries = rotation_entries_exact(couplings)
    score = ball(lam)
    contributions = []
    for row in active_low:
        feature = active_low_feature(system, entries, row, fourth_groups)
        term = ball(z[row]) * feature / ball(low_scales[row])
        score += term
        contributions.append({"row": row, "block": "low", "contribution": str(term)})
    for row in active_sixth:
        feature = orbit_average_minor(entries, sixth_rows[row - 1461])
        term = ball(z[row]) * feature / ball(Fraction(5, 19721))
        score += term
        contributions.append({"row": row, "block": "sixth", "contribution": str(term)})
    for row in active_eighth:
        feature = orbit_average_minor(entries, eighth_rows[row - 2106])
        term = ball(z[row]) * feature / ball(Fraction(1, 19721))
        score += term
        contributions.append({"row": row, "block": "eighth", "contribution": str(term)})

    lower, upper = score.lower(), score.upper()
    strict_positive = bool(lower > 0)
    result = {
        **base,
        "status": "certified_continuous_path_dual_escape" if strict_positive else "candidate_not_strictly_positive_by_arb",
        "complete": True,
        "candidate_found": True,
        "candidate_sha256": candidate_sha,
        "candidate_couplings_exact": coupling_strings,
        "all_41_edge_magnitudes_strictly_positive": True,
        "candidate_outside_frozen_canonical_pool": True,
        "candidate_differs_from_all_four_prior_continuous_escapes": True,
        "dual_l1_norm_exact": str(sum((abs(x) for x in z), Fraction(0))),
        "dual_lambda_minus_slack_exact": str(lam),
        "active_dual_rows": {"low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)},
        "pricing_score_interval": str(score),
        "pricing_score_lower_endpoint": str(lower),
        "pricing_score_upper_endpoint": str(upper),
        "strictly_positive": strict_positive,
        "row_contributions": contributions,
        "row_blocks": blocks,
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_sha256": candidate_sha,
        "pricing_score_interval": str(score),
        "strictly_positive": strict_positive,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
