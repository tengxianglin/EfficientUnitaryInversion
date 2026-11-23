"""Independent 128-bit Arb verification of a continuous-path escape from the 190-column dual."""
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

CERT_PATH = ROOT / "evidence/55probe_190col_seventh_continuous_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_190col_seventh_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
CUT_DUAL_PATH = ROOT / "evidence/55probe_152col_full_sixth_cut_dual_certificate_n21.json"
CANDIDATE_152_PATH = ROOT / "evidence/candidate_joint_input_152col_continuous_escape_n21.json"
DISCOVERY_PATH = ROOT / "evidence/190col_continuous_dual_search_n21.json"
OUTPUT_PATH = ROOT / "evidence/190col_continuous_dual_escape_arb_n21.json"
PARENT_189_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_189col_sixth_continuous_escape_n21.json"
PARENT_189_DUAL_PATH = ROOT / "evidence/55probe_189col_sixth_continuous_escape_dual_certificate_n21.json"
ESCAPE_PATHS = (
    ROOT / "evidence/continuous_path_dual_escape_arb_n21.json",
    ROOT / "evidence/184col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/186col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/187col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/188col_continuous_dual_escape_arb_n21.json",
    ROOT / "evidence/189col_continuous_dual_escape_arb_n21.json",
)
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
PRECISION_BITS = 128
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    paths = (
        CERT_PATH, LP_PATH, CUT_LP_PATH, CUT_DUAL_PATH, CANDIDATE_152_PATH,
        DISCOVERY_PATH, PARENT_189_LP_PATH, PARENT_189_DUAL_PATH,
        *ESCAPE_PATHS, SEED_POOL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    values = [
        value if path.suffix == ".npy" else json.loads(value)
        for path, value in zip(paths, raw)
    ]
    (
        cert, lp, cut_lp, cut_dual, candidate152, discovery,
        parent_189_lp, parent_189_dual, *tail,
    ) = values
    escapes = tail[:-1]
    seed_raw = tail[-1]
    (
        cert_sha, lp_sha, cut_lp_sha, cut_dual_sha, candidate152_sha,
        discovery_sha, parent_189_lp_sha, parent_189_dual_sha,
        *escape_hashes_and_seed,
    ) = map(sha, raw)
    escape_hashes = escape_hashes_and_seed[:-1]
    seed_file_sha = escape_hashes_and_seed[-1]

    if cert.get("status") != "strict_190col_2113row_seventh_continuous_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("190-column dual is not strictly Arb-certified")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("190-column dual/LP transcript hash mismatch")
    if (cert.get("column_count"), cert.get("row_count")) != (190, 2113):
        raise RuntimeError("unexpected 190-column dual dimensions")
    if lp.get("status") != "190col_seventh_continuous_escape_lp_above_one_third":
        raise RuntimeError("190-column LP is not the expected above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (190, 2113):
        raise RuntimeError("unexpected 190-column LP dimensions")
    if lp.get("parent_189col_lp_sha256") != parent_189_lp_sha:
        raise RuntimeError("190-column LP does not pin the 189-column parent LP")
    if lp.get("parent_189col_dual_certificate_sha256") != parent_189_dual_sha:
        raise RuntimeError("190-column LP does not pin the 189-column parent dual")
    if cert.get("parent_189col_lp_sha256") != parent_189_lp_sha or cert.get("parent_189col_dual_certificate_sha256") != parent_189_dual_sha:
        raise RuntimeError("190-column certificate does not pin the 189-column parent")
    if parent_189_lp.get("status") != "189col_sixth_continuous_escape_lp_above_one_third":
        raise RuntimeError("189-column parent LP has an unexpected status")
    if parent_189_dual.get("status") != "strict_189col_2113row_sixth_continuous_escape_minimax_obstruction" or not parent_189_dual.get("complete"):
        raise RuntimeError("189-column parent dual is not strictly Arb-certified")
    if parent_189_dual.get("lp_transcript_sha256") != parent_189_lp_sha:
        raise RuntimeError("189-column parent dual does not pin its LP")

    if lp.get("parent_152col_candidate_sha256") != candidate152_sha or cert.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("190-column branch does not pin the exact 152-column ancestor candidate")
    if lp.get("cut_lp_transcript_sha256") != cut_lp_sha or cert.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("190-column branch does not pin the 2,113-row cut design")
    if lp.get("cut_dual_certificate_sha256") != cut_dual_sha or cert.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("190-column branch does not pin the 152-column cut dual")
    if parent_189_lp.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("189-column parent does not pin the 152-column candidate")
    if parent_189_lp.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_189_lp.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("189-column parent does not pin the cut design and dual")
    if parent_189_dual.get("parent_152col_candidate_sha256") != candidate152_sha:
        raise RuntimeError("189-column parent dual does not pin the 152-column candidate")
    if parent_189_dual.get("cut_lp_transcript_sha256") != cut_lp_sha or parent_189_dual.get("cut_dual_certificate_sha256") != cut_dual_sha:
        raise RuntimeError("189-column parent dual does not pin the cut design and dual")
    if candidate152.get("continuous_escape_arb_certificate_sha256") != escape_hashes[0]:
        raise RuntimeError("152-column ancestor candidate does not pin the first escape")
    if cut_dual.get("status") != "strict_152col_2113row_minimax_obstruction" or not cut_dual.get("complete"):
        raise RuntimeError("152-column cut dual is not strictly Arb-certified")
    if cut_dual.get("lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("152-column cut dual does not pin its LP")

    escape_keys = (
        "first_continuous_escape_arb_certificate_sha256",
        "second_continuous_escape_arb_certificate_sha256",
        "third_continuous_escape_arb_certificate_sha256",
        "fourth_continuous_escape_arb_certificate_sha256",
        "fifth_continuous_escape_arb_certificate_sha256",
        "sixth_continuous_escape_arb_certificate_sha256",
        "seventh_continuous_escape_arb_certificate_sha256",
    )
    for index, (escape, digest, key) in enumerate(zip(escapes, escape_hashes, escape_keys), 1):
        if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
            raise RuntimeError(f"prior continuous escape {index} is not strictly Arb-certified")
        if lp.get(key) != digest or cert.get(key) != digest:
            raise RuntimeError(f"190-column branch does not pin prior escape {index}")
        if index <= 6 and (parent_189_lp.get(key) != digest or parent_189_dual.get(key) != digest):
            raise RuntimeError(f"189-column parent does not pin prior escape {index}")
    if escapes[6].get("dual_certificate_sha256") != parent_189_dual_sha or escapes[6].get("lp_transcript_sha256") != parent_189_lp_sha:
        raise RuntimeError("sixth escape does not pin the exact 189-column parent dual/LP")
    if escapes[6].get("candidate_outside_frozen_canonical_pool") is not True:
        raise RuntimeError("sixth escape is not certified outside the canonical inventory")

    if discovery.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("discovery transcript does not pin the exact 190-column dual")
    if discovery.get("lp_transcript_sha256") != lp_sha or discovery.get("cut_lp_transcript_sha256") != cut_lp_sha:
        raise RuntimeError("discovery transcript LP/cut provenance mismatch")
    if discovery.get("prior_escape_certificate_sha256") != escape_hashes[6]:
        raise RuntimeError("discovery transcript does not pin the sixth prior escape")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = sha(seed.tobytes())
    if seed_file_sha == "" or seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    if lp.get("seed_pool_sha256_le_f64") != seed_sha or cert.get("seed_pool_sha256_le_f64") != seed_sha:
        raise RuntimeError("190-column branch seed-pool provenance mismatch")

    canonical_columns, _, _ = canonical_ensemble()
    canonical_sha = sha(np.asarray(canonical_columns, dtype="<f8").tobytes())
    if len(canonical_columns) != 1641 or canonical_sha != lp.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical inventory count/hash mismatch")
    if cert.get("canonical_all_columns_sha256_le_f64") != canonical_sha:
        raise RuntimeError("190-column dual uses a different canonical inventory")

    base_columns = [int(value) for value in parent_189_lp["base_columns"]]
    added_columns = [int(value) for value in parent_189_lp["added_canonical_columns"]]
    parent_order = [int(value) for value in parent_189_lp["column_order"]]
    expected_parent_order = base_columns + [1641] + added_columns + [1642, 1643, 1644, 1645, 1646]
    column_order = [int(value) for value in lp["column_order"]]
    if len(base_columns) != 151 or len(added_columns) != 32 or parent_order != expected_parent_order:
        raise RuntimeError("189-column parent physical inventory/order mismatch")
    if column_order != parent_order + [1647] or len(column_order) != 190 or len(set(column_order)) != 190:
        raise RuntimeError("190-column physical inventory/order mismatch")
    if cert.get("columns") != column_order:
        raise RuntimeError("190-column certificate physical ordering differs from its LP")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut_lp)
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("190-column LP row-inventory hash mismatch")
    if row_blocks != lp.get("row_blocks") or row_blocks != cert.get("row_blocks"):
        raise RuntimeError("189-column row-block inventory mismatch")

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
        raise RuntimeError("discovery candidate must contain 42 exact coupling strings")
    couplings = [Fraction(value) for value in coupling_strings]
    if couplings[-1] != 0 or any(value <= 0 for value in couplings[:-1]):
        raise RuntimeError("candidate is not a strictly-positive 41-edge open path")
    candidate_sha = sha(json.dumps(coupling_strings, separators=(",", ":")).encode())

    candidate_float = np.asarray([float(value) for value in couplings], dtype="<f8")
    if any(np.array_equal(candidate_float, np.asarray(column, dtype="<f8")) for column in canonical_columns):
        raise RuntimeError("candidate duplicates a canonical generator")
    prior_paths = [
        [Fraction(value) for value in escape["candidate_couplings_exact"]]
        for escape in escapes
    ]
    if any(couplings == prior for prior in prior_paths):
        raise RuntimeError("candidate duplicates one of the six previously certified continuous paths")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    norm = sum((abs(value) for value in z), Fraction(0))
    if len(z) != 2113 or norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("exact 190-column dual dimension/L1 normalization mismatch")
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
    active = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active if index < 1461]
    active_sixth = [index for index in active if 1461 <= index < 2106]
    active_eighth = [index for index in active if index >= 2106]
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
        "status": "certified_continuous_path_dual_escape" if strict_positive else "candidate_not_strictly_positive_by_arb",
        "complete": True,
        "candidate_found": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_lp_sha,
        "discovery_sha256": discovery_sha,
        "prior_escape_certificate_sha256": escape_hashes[6],
        "candidate_sha256": candidate_sha,
        "candidate_couplings_exact": coupling_strings,
        "all_41_edge_magnitudes_strictly_positive": True,
        "candidate_outside_frozen_canonical_pool": True,
        "candidate_differs_from_all_seven_prior_continuous_escapes": True,
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
            "190-column dual over the positive 41-edge path family. A failed local search is not "
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
