"""Independent 128-bit Arb pricing audit for a candidate escaping the 191-column dual.

The local optimizer is discovery only. This verifier consumes its exact-decimal
candidate, reconstructs the exact rational dual from the already-certified
191-column certificate, and recomputes the candidate's pricing score with Arb.
"""
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

CERT_PATH = ROOT / "evidence/55probe_191col_eighth_continuous_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_191col_eighth_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DISCOVERY_PATH = ROOT / "evidence/191col_continuous_dual_search_n21.json"
OUTPUT_PATH = ROOT / "evidence/191col_continuous_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
ESCAPE_PATHS = (
    ROOT / "evidence/continuous_path_dual_escape_arb_n21.json",
    ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/188col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/189col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/190col_continuous_dual_escape_arb_n21.json",
)
PRECISION_BITS = 128
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    cert_raw = CERT_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    cut_raw = CUT_LP_PATH.read_bytes()
    discovery_raw = DISCOVERY_PATH.read_bytes()
    seed_raw = SEED_POOL_PATH.read_bytes()
    escape_raw = [path.read_bytes() for path in ESCAPE_PATHS]
    cert, lp, cut, discovery = [
        json.loads(raw) for raw in (cert_raw, lp_raw, cut_raw, discovery_raw)
    ]
    escapes = [json.loads(raw) for raw in escape_raw]
    cert_sha, lp_sha, cut_sha, discovery_sha = map(
        sha, (cert_raw, lp_raw, cut_raw, discovery_raw)
    )
    escape_hashes = [sha(raw) for raw in escape_raw]

    if cert.get("status") != "strict_191col_2113row_eighth_continuous_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("191-column dual is not strictly Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (191, 2113):
        raise RuntimeError("unexpected 191-column certificate dimensions")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("191-column certificate/LP hash mismatch")
    if lp.get("status") != "191col_eighth_continuous_escape_lp_above_one_third":
        raise RuntimeError("191-column LP is not the expected above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (191, 2113):
        raise RuntimeError("unexpected 191-column LP dimensions")
    if lp.get("cut_lp_transcript_sha256") != cut_sha or cert.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("191-column branch does not pin the exact 2,113-row cut design")
    if lp.get("parent_190col_lp_sha256") != cert.get("parent_190col_lp_sha256"):
        raise RuntimeError("191-column LP/certificate parent-LP provenance mismatch")
    if lp.get("parent_190col_dual_certificate_sha256") != cert.get("parent_190col_dual_certificate_sha256"):
        raise RuntimeError("191-column LP/certificate parent-dual provenance mismatch")

    if len(escapes) != 8:
        raise RuntimeError("expected eight previously Arb-certified continuous escapes")
    prior_couplings = []
    for index, escape in enumerate(escapes, 1):
        if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
            raise RuntimeError(f"prior continuous escape {index} is not strictly Arb-certified")
        coupling = [Fraction(value) for value in escape["candidate_couplings_exact"]]
        if len(coupling) != 42 or coupling[-1] != 0 or any(value <= 0 for value in coupling[:-1]):
            raise RuntimeError(f"prior continuous escape {index} is not a legal positive 41-edge path")
        prior_couplings.append(tuple(coupling))
    if len(set(prior_couplings)) != 8:
        raise RuntimeError("the eight prior continuous escapes are not pairwise distinct")
    if discovery.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("discovery transcript does not pin the exact 191-column dual")
    if discovery.get("lp_transcript_sha256") != lp_sha or discovery.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("discovery transcript LP/cut provenance mismatch")
    if discovery.get("prior_escape_certificate_sha256") != escape_hashes[-1]:
        raise RuntimeError("discovery transcript does not pin the eighth prior escape")
    if discovery.get("seed_pool_sha256_le_f64") != SEED_POOL_SHA256:
        raise RuntimeError("discovery transcript has a different frozen seed pool")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if cert.get("seed_pool_sha256_le_f64") != seed_sha or lp.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("191-column evidence does not pin the frozen seed pool")

    canonical_columns, _, _ = canonical_ensemble()
    canonical_sha = sha(np.asarray(canonical_columns, dtype="<f8").tobytes())
    if len(canonical_columns) != 1641 or canonical_sha != cert.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("frozen canonical inventory count/hash mismatch")

    if not discovery.get("candidate_found"):
        result = {
            "status": "no_positive_candidate_in_local_search",
            "complete": True,
            "candidate_found": False,
            "strictly_positive": False,
            "precision_bits": ctx.prec,
            "interval_backend": "python-flint 0.8.0 / Arb",
            "dual_certificate_sha256": cert_sha,
            "lp_transcript_sha256": lp_sha,
            "discovery_sha256": discovery_sha,
            "records_checked": len(discovery.get("records", [])),
            "search_scope": discovery.get("search_domain"),
            "scope": (
                "No positive candidate was found in the finite deterministic local search. "
                "This is not a global separation proof for the positive 41-edge path family."
            ),
        }
        OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        return

    coupling_strings = discovery.get("best_candidate_couplings_exact")
    if not isinstance(coupling_strings, list) or len(coupling_strings) != 42:
        raise RuntimeError("discovery candidate must contain 42 exact-decimal coupling strings")
    couplings = [Fraction(value) for value in coupling_strings]
    if couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
        raise RuntimeError("candidate is not a strictly-positive 41-edge open path")
    if tuple(couplings) in set(prior_couplings):
        raise RuntimeError("candidate duplicates one of the eight prior continuous escapes")
    candidate_sha = sha(json.dumps(coupling_strings, separators=(",", ":")).encode())

    candidate_float = np.asarray([float(value) for value in couplings], dtype="<f8")
    if any(np.array_equal(candidate_float, np.asarray(column, dtype="<f8")) for column in canonical_columns):
        raise RuntimeError("candidate duplicates a frozen canonical generator")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    norm = sum((abs(value) for value in z), Fraction(0))
    if len(z) != 2113 or norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("exact 191-column dual dimension/L1 normalization mismatch")
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
    active = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active if index < LOW_COUNT]
    active_sixth = [index for index in active if LOW_COUNT <= index < SIXTH_END]
    active_eighth = [index for index in active if index >= SIXTH_END]
    if (len(active), len(active_low), len(active_sixth), len(active_eighth)) != (59, 2, 55, 2):
        raise RuntimeError("unexpected 191-column active dual row blocks")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut)
    if row_blocks != cert.get("row_blocks") or len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("191-column row inventory mismatch")
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
        feature = orbit_average_minor(entries, sixth_rows[row - LOW_COUNT])
        term = ball(z[row]) * feature / ball(SIXTH_SCALE)
        score += term
        contributions.append({"row": row, "block": "sixth", "contribution": str(term)})
    for row in active_eighth:
        feature = orbit_average_minor(entries, eighth_rows[row - SIXTH_END])
        term = ball(z[row]) * feature / ball(EIGHTH_SCALE)
        score += term
        contributions.append({"row": row, "block": "eighth", "contribution": str(term)})

    lower, upper = score.lower(), score.upper()
    strict_positive = bool(lower > 0)
    result = {
        "status": "certified_continuous_path_dual_escape" if strict_positive else "candidate_not_strictly_positive_by_arb",
        "complete": True,
        "candidate_found": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_sha,
        "discovery_sha256": discovery_sha,
        "prior_escape_certificate_sha256": escape_hashes[-1],
        "candidate_sha256": candidate_sha,
        "candidate_couplings_exact": coupling_strings,
        "all_41_edge_magnitudes_strictly_positive": True,
        "candidate_outside_frozen_canonical_pool": True,
        "candidate_differs_from_all_eight_prior_continuous_escapes": True,
        "dual_l1_norm_exact": str(norm),
        "dual_lambda_minus_slack_exact": str(lam),
        "active_dual_rows": {"low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)},
        "pricing_score_interval": str(score),
        "pricing_score_lower_endpoint": str(lower),
        "pricing_score_upper_endpoint": str(upper),
        "strictly_positive": strict_positive,
        "row_contributions": contributions,
        "row_blocks": row_blocks,
        "search_scope": discovery.get("search_domain"),
        "scope": (
            "A strictly positive Arb pricing interval refutes global separation by this particular "
            "191-column dual over the positive 41-edge path family. A failed local search is not "
            "a global separation proof."
        ),
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
