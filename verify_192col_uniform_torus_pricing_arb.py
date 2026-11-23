"""Independent 128-bit Arb verification of a 192-column uniform-torus witness.

A positive interval at an exact rational phase vector, together with the
proved density of the uniform positive-coupling ray in the 21-torus, implies
that some finite uniform coupling t > 0 has positive 192-column dual pricing.
"""
import hashlib
import json
from fractions import Fraction

from flint import arb, arb_mat, ctx, fmpq

from audit_complete_sixth_moments import ROOT
from screen_ising_sixth_moments import orbit
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    orbit_average_minor,
)
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_192col_ninth_continuous_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DISCOVERY_PATH = ROOT / "evidence/192col_uniform_torus_search_n21.json"
OUTPUT_PATH = ROOT / "evidence/192col_uniform_torus_arb_n21.json"

PRECISION_BITS = 128
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def exact_torus_rotation(phase_strings):
    phases = [Fraction(value) for value in phase_strings]
    if len(phases) != 21:
        raise RuntimeError("expected 21 exact rational torus phases")
    if any(abs(float(value)) > 3.1415926536 for value in phases):
        raise RuntimeError("phase input lies outside the pinned [-pi,pi] search box")

    pi = arb.pi()
    scale = ball(Fraction(4, 43)).sqrt()
    q = arb_mat(42, 42)
    for j in range(42):
        residue = j % 4
        cos_sign = (1, 0, -1, 0)[residue]
        sin_sign = (0, 1, 0, -1)[residue]
        if cos_sign == 0 and sin_sign == 0:
            raise RuntimeError("impossible phase-sign table")
        for k in range(1, 22):
            sine = (pi * ball(Fraction((j + 1) * k, 43))).sin()
            if cos_sign:
                q[j, 2 * k - 2] = scale * sine * cos_sign
            if sin_sign:
                q[j, 2 * k - 1] = scale * sine * sin_sign

    block = arb_mat(42, 42)
    for k, phase in enumerate(phases):
        angle = ball(phase)
        cosine = angle.cos()
        sine = angle.sin()
        block[2 * k, 2 * k] = cosine
        block[2 * k, 2 * k + 1] = sine
        block[2 * k + 1, 2 * k] = -sine
        block[2 * k + 1, 2 * k + 1] = cosine

    qt = arb_mat([[q[j, i] for j in range(42)] for i in range(42)])
    rotation = q * block * qt
    return [[rotation[i, j] for j in range(42)] for i in range(42)]


def main():
    ctx.prec = PRECISION_BITS
    cert_raw = CERT_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    cut_raw = CUT_LP_PATH.read_bytes()
    discovery_raw = DISCOVERY_PATH.read_bytes()
    cert, lp, cut, discovery = [
        json.loads(raw) for raw in (cert_raw, lp_raw, cut_raw, discovery_raw)
    ]
    cert_sha, lp_sha, cut_sha, discovery_sha = map(
        sha, (cert_raw, lp_raw, cut_raw, discovery_raw)
    )

    if cert.get("status") != "strict_192col_2113row_ninth_continuous_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("192-column parent dual is not strictly Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (192, 2113):
        raise RuntimeError("unexpected 192-column parent dimensions")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("192-column certificate/LP hash mismatch")
    if lp.get("status") != "192col_ninth_continuous_escape_lp_above_one_third":
        raise RuntimeError("192-column LP is not the expected above-cap discovery")
    if (lp.get("columns"), lp.get("rows")) != (192, 2113):
        raise RuntimeError("unexpected 192-column LP dimensions")
    if lp.get("cut_lp_transcript_sha256") != cut_sha or cert.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("192-column branch does not pin the exact cut design")
    if discovery.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("discovery does not pin the exact 192-column dual")
    if discovery.get("lp_transcript_sha256") != lp_sha or discovery.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("discovery LP/cut provenance mismatch")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    norm = sum((abs(value) for value in z), Fraction(0))
    if len(z) != 2113 or norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("exact 192-column dual dimension/L1 normalization mismatch")
    active = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active if index < LOW_COUNT]
    active_sixth = [index for index in active if LOW_COUNT <= index < SIXTH_END]
    active_eighth = [index for index in active if index >= SIXTH_END]
    if (len(active), len(active_low), len(active_sixth), len(active_eighth)) != (61, 2, 56, 3):
        raise RuntimeError("unexpected 192-column active dual row blocks")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut)
    if row_blocks != cert.get("row_blocks") or len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("192-column exact row inventory mismatch")
    sixth_hash = sha(json.dumps([list(row) for row in sixth_rows], separators=(",", ":")).encode())
    eighth_hash = sha(json.dumps([list(row) for row in eighth_rows], separators=(",", ":")).encode())
    if sixth_hash != lp.get("sixth_rows_sha256") or eighth_hash != lp.get("eighth_rows_sha256"):
        raise RuntimeError("192-column LP row-inventory hash mismatch")

    if not discovery.get("candidate_found"):
        result = {
            "status": "no_positive_candidate_in_local_search",
            "complete": True,
            "strictly_positive": False,
            "precision_bits": ctx.prec,
            "interval_backend": "python-flint 0.8.0 / Arb",
            "dual_certificate_sha256": cert_sha,
            "lp_transcript_sha256": lp_sha,
            "discovery_sha256": discovery_sha,
            "best_candidate_score_binary64": discovery.get("best_candidate_score_binary64"),
            "records_checked": len(discovery.get("records", [])),
            "scope": (
                "No positive candidate was found in the finite deterministic torus local search. "
                "This is not a global upper bound on the torus and does not prove separation of the uniform ray."
            ),
        }
        OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        return

    phase_strings = discovery.get("best_candidate_phases_exact_decimal")
    if not isinstance(phase_strings, list) or len(phase_strings) != 21:
        raise RuntimeError("discovery candidate must contain 21 exact-decimal phases")
    phases = [Fraction(value) for value in phase_strings]
    if any(abs(float(value)) > 3.1415926536 for value in phases):
        raise RuntimeError("candidate phase lies outside the search box")

    entries = exact_torus_rotation(phase_strings)
    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
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
    phase_sha = sha(json.dumps(phase_strings, separators=(",", ":")).encode())
    result = {
        "status": "certified_uniform_torus_dual_escape" if strict_positive else "candidate_not_strictly_positive_by_arb",
        "complete": True,
        "candidate_found": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_sha,
        "discovery_sha256": discovery_sha,
        "phase_vector_sha256": phase_sha,
        "phase_vector_exact_decimal": phase_strings,
        "dual_l1_norm_exact": str(norm),
        "dual_lambda_minus_slack_exact": str(lam),
        "active_dual_rows": {"low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)},
        "pricing_score_interval": str(score),
        "pricing_score_lower_endpoint": str(lower),
        "pricing_score_upper_endpoint": str(upper),
        "strictly_positive": strict_positive,
        "uniform_ray_escape_exists_by_density": strict_positive,
        "row_contributions": contributions,
        "row_blocks": row_blocks,
        "scope": (
            "A strictly positive Arb interval at this exact torus point, combined with the proved "
            "Kronecker density of the uniform positive-coupling ray and continuity of the pricing "
            "functional, proves existence of a finite t > 0 with positive pricing on c=(t,...,t). "
            "It refutes global separation by this particular 192-column dual only; it is not a "
            "full-family minimax theorem."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "phase_vector_sha256": phase_sha,
        "pricing_score_interval": str(score),
        "strictly_positive": strict_positive,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
