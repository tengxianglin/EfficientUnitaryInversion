"""Independent 128-bit Arb pricing of the exact 201-column dual on the uniform-path torus.

A strictly positive interval at an exact rational phase vector, together with
THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md, proves that some finite positive
equal-coupling open-path time escapes this particular 201-column dual.
"""
import hashlib
import json
from fractions import Fraction

from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import ROOT
from screen_ising_sixth_moments import orbit
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    orbit_average_minor,
)
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_201col_uniform_ray_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_201col_uniform_ray_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DISCOVERY_PATH = ROOT / "evidence/201col_uniform_torus_search_n21.json"
TORUS_THEORY_PATH = ROOT / "THEORY_UNIFORM_42SITE_PATH_DENSE_TORUS.md"
OUTPUT_PATH = ROOT / "evidence/201col_uniform_torus_arb_n21.json"

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
    theory_raw = TORUS_THEORY_PATH.read_bytes()
    cert, lp, cut, discovery = (json.loads(raw) for raw in (cert_raw, lp_raw, cut_raw, discovery_raw))
    cert_sha, lp_sha, cut_sha, discovery_sha = map(sha, (cert_raw, lp_raw, cut_raw, discovery_raw))
    theory_sha = sha(theory_raw)

    if cert.get("status") != "strict_201col_2113row_uniform_ray_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("201-column dual is not independently Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (201, 2113):
        raise RuntimeError("unexpected 201-column certificate dimensions")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("201-column certificate/LP hash mismatch")
    if cert.get("cut_lp_transcript_sha256") != cut_sha or lp.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("201-column evidence does not pin the exact mixed-order row design")
    if lp.get("status") != "201col_uniform_ray_escape_lp_above_one_third" or (lp.get("columns"), lp.get("rows")) != (201, 2113):
        raise RuntimeError("201-column LP transcript is not the pinned above-cap discovery")
    if discovery.get("dual_certificate_sha256") != cert_sha or discovery.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("torus search does not pin the exact 201-column dual and LP")
    if discovery.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("torus search does not pin the exact cut design")
    if discovery.get("status") != "positive_uniform_torus_candidate_found" or not discovery.get("candidate_found"):
        result = {
            "status": "no_positive_candidate_in_local_search",
            "complete": True,
            "strict_uniform_ray_escape_certified": False,
            "discovery_sha256": discovery_sha,
            "dual_certificate_sha256": cert_sha,
            "lp_transcript_sha256": lp_sha,
            "scope": "The finite multi-start search found no positive candidate. This is not a global separation proof and does not certify the 201-column dual on the continuous uniform ray.",
        }
        OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        return

    phase_strings = discovery.get("best_candidate_phases_exact_decimal")
    if not isinstance(phase_strings, list) or len(phase_strings) != 21:
        raise RuntimeError("positive discovery lacks 21 exact-decimal phase strings")
    entries = exact_torus_rotation(phase_strings)
    system, low_scales, sixth_rows, eighth_rows, target, row_blocks = load_exact_design(cut)
    if row_blocks != cert.get("row_blocks") or row_blocks != lp.get("row_blocks"):
        raise RuntimeError("201-column exact row-block mismatch")
    if len(sixth_rows) != 645 or len(eighth_rows) != 7:
        raise RuntimeError("unexpected mixed-order row inventory")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    lam = Fraction(cert["dual_lambda_exact"])
    delta = Fraction(cert["dual_slack_delta"])
    norm = sum((abs(value) for value in z), Fraction(0))
    objective = lam + sum((value * target_value for value, target_value in zip(z, target)))
    if len(z) != 2113 or norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("exact 201-column dual vector/norm mismatch")
    if objective != Fraction(cert["dual_objective_exact"]):
        raise RuntimeError("exact 201-column dual objective mismatch")
    if objective - delta != Fraction(cert["certified_minimax_lower_bound"]):
        raise RuntimeError("exact 201-column minimax lower bound mismatch")
    if objective - delta <= Fraction(1, 3):
        raise RuntimeError("201-column certified lower bound is not above one third")

    active = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active if index < LOW_COUNT]
    active_sixth = [index for index in active if LOW_COUNT <= index < SIXTH_END]
    active_eighth = [index for index in active if index >= SIXTH_END]
    active_blocks = {
        "total": len(active),
        "low": len(active_low),
        "sixth": len(active_sixth),
        "eighth": len(active_eighth),
    }
    expected_blocks = {"total": 62, "low": 2, "sixth": 58, "eighth": 2}
    if active_blocks != cert.get("active_dual_rows") or active_blocks != expected_blocks:
        raise RuntimeError("201-column active dual row support mismatch")

    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }
    score = ball(lam - delta)
    for row in active_low:
        feature = active_low_feature(system, entries, row, fourth_groups)
        score += ball(z[row]) * feature / ball(low_scales[row])
    for row in active_sixth:
        feature = orbit_average_minor(entries, sixth_rows[row - LOW_COUNT])
        score += ball(z[row]) * feature / ball(SIXTH_SCALE)
    for row in active_eighth:
        feature = orbit_average_minor(entries, eighth_rows[row - SIXTH_END])
        score += ball(z[row]) * feature / ball(EIGHTH_SCALE)

    lower, upper = score.lower(), score.upper()
    strict_positive = bool(lower > 0)
    result = {
        "status": "certified_positive_uniform_torus_escape" if strict_positive else "candidate_not_strictly_certified",
        "complete": True,
        "strict_uniform_ray_escape_certified": strict_positive,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_sha,
        "discovery_sha256": discovery_sha,
        "parent_200col_torus_search_sha256": discovery.get("parent_200col_torus_search_sha256"),
        "dense_torus_theory_sha256": theory_sha,
        "phase_exact_decimal": phase_strings,
        "phase_vector_sha256": sha(json.dumps(phase_strings, separators=(",", ":")).encode()),
        "pricing_interval": str(score),
        "pricing_lower_endpoint": str(lower),
        "pricing_upper_endpoint": str(upper),
        "dual_objective_exact": str(objective),
        "dual_l1_norm_exact": str(norm),
        "dual_slack_delta": str(delta),
        "certified_minimax_lower_bound": str(objective - delta),
        "interpretation": (
            "A strictly positive Arb interval at this exact rational point of the uniform-path torus, "
            "combined with the pinned rational-independence/dense-ray theorem, proves existence of "
            "some finite t>0 on the equal-positive-coupling physical open path with positive 200-dual pricing."
            if strict_positive else
            "The binary64 candidate did not yield a strictly positive Arb interval; no uniform-ray escape is certified."
        ),
        "scope": (
            "This refutes global separation by the particular 201-column dual if and only if "
            "strict_uniform_ray_escape_certified is true. It does not invalidate the finite 201-column "
            "mixed-order theorem, prove full-family feasibility/infeasibility, complete sixth/eighth "
            "orbit control, or imply a Choi/diamond operational bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "pricing_interval": result["pricing_interval"],
        "strict_uniform_ray_escape_certified": strict_positive,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
