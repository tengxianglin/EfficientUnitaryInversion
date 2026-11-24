"""Independent 128-bit Arb verification of an explicit finite uniform-path escape for the 197-column dual."""
import hashlib
import json
from fractions import Fraction

from flint import ctx

from audit_complete_sixth_moments import ROOT
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    orbit_average_minor,
)
from verify_192col_uniform_ray_time_arb import exact_uniform_ray_rotation
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_197col_uniform_ray_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_197col_uniform_ray_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
TORUS_CERT_PATH = ROOT / "evidence/197col_uniform_torus_arb_n21.json"
DISCOVERY_PATH = ROOT / "evidence/197col_uniform_ray_time_search_n21.json"
OUTPUT_PATH = ROOT / "evidence/197col_uniform_ray_time_arb_n21.json"

PRECISION_BITS = 128
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ctx.prec = PRECISION_BITS
    raw = [path.read_bytes() for path in (
        CERT_PATH, LP_PATH, CUT_LP_PATH, TORUS_CERT_PATH, DISCOVERY_PATH
    )]
    cert, lp, cut, torus, discovery = [json.loads(value) for value in raw]
    cert_sha, lp_sha, cut_sha, torus_sha, discovery_sha = map(sha, raw)

    if cert.get("status") != "strict_197col_2113row_uniform_ray_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("197-column dual is not independently Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (197, 2113) or cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("197-column certificate dimensions/hash mismatch")
    if lp.get("status") != "197col_uniform_ray_escape_lp_above_one_third" or (lp.get("columns"), lp.get("rows")) != (197, 2113):
        raise RuntimeError("197-column LP is not the pinned above-cap discovery")
    if cert.get("cut_lp_transcript_sha256") != cut_sha or lp.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("197-column evidence does not pin the exact mixed-order row design")
    if torus.get("status") != "certified_positive_uniform_torus_escape" or not torus.get("complete") or not torus.get("strict_uniform_ray_escape_certified"):
        raise RuntimeError("197-column torus witness is not strictly Arb-certified")
    if torus.get("dual_certificate_sha256") != cert_sha or torus.get("lp_transcript_sha256") != lp_sha or torus.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("197-column torus certificate provenance mismatch")
    if discovery.get("dual_certificate_sha256") != cert_sha or discovery.get("lp_transcript_sha256") != lp_sha or discovery.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("finite-time search does not pin the exact 197-column dual/LP/cut design")
    if discovery.get("torus_arb_certificate_sha256") != torus_sha or discovery.get("torus_phase_vector_sha256") != torus.get("phase_vector_sha256"):
        raise RuntimeError("finite-time search does not pin the exact torus Arb certificate")

    if not discovery.get("candidate_found"):
        result = {
            "status": "no_positive_finite_uniform_ray_candidate_found",
            "complete": True,
            "strictly_positive": False,
            "finite_physical_escape_certified": False,
            "precision_bits": ctx.prec,
            "dual_certificate_sha256": cert_sha,
            "lp_transcript_sha256": lp_sha,
            "torus_arb_certificate_sha256": torus_sha,
            "discovery_sha256": discovery_sha,
            "best_t_exact_decimal": discovery.get("best_t_exact_decimal"),
            "best_score_binary64": discovery.get("best_score_binary64"),
            "scope": (
                "The bounded one-dimensional search did not locate an explicit decimal time. "
                "The independently certified positive torus point and dense-ray theorem still prove "
                "existence of some finite t>0, but this run has no explicit finite-time witness."
            ),
        }
        OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        return

    t_string = discovery.get("best_t_exact_decimal")
    if not isinstance(t_string, str):
        raise RuntimeError("finite-time candidate must be an exact decimal string")
    t = Fraction(t_string)
    if t <= 0:
        raise RuntimeError("finite-time candidate is not strictly positive")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    norm = sum((abs(value) for value in z), Fraction(0))
    lam = Fraction(cert["dual_lambda_exact"])
    delta = Fraction(cert["dual_slack_delta"])
    if len(z) != 2113 or norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("exact 197-column dual dimension/L1 normalization mismatch")

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
    if active_blocks != cert.get("active_dual_rows") or active_blocks != {"total": 63, "low": 2, "sixth": 59, "eighth": 2}:
        raise RuntimeError("197-column active dual row blocks mismatch")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut)
    if row_blocks != cert.get("row_blocks"):
        raise RuntimeError("exact 2,113-row design block mismatch")
    entries = exact_uniform_ray_rotation(t)
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
        "status": "certified_finite_uniform_ray_escape" if strict_positive else "finite_time_candidate_not_strictly_positive_by_arb",
        "complete": True,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "cut_lp_transcript_sha256": cut_sha,
        "torus_arb_certificate_sha256": torus_sha,
        "torus_phase_vector_sha256": torus.get("phase_vector_sha256"),
        "discovery_sha256": discovery_sha,
        "t_exact_decimal": t_string,
        "t_exact_rational": str(t),
        "uniform_couplings_exact_decimal": [t_string] * 41,
        "uniform_path": "c_j=t for j=0,...,40",
        "pricing_score_interval": str(score),
        "pricing_score_lower_endpoint": str(lower),
        "pricing_score_upper_endpoint": str(upper),
        "strictly_positive": strict_positive,
        "finite_physical_escape_certified": strict_positive,
        "dual_l1_norm_exact": str(norm),
        "active_dual_rows": {"low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)},
        "row_blocks": row_blocks,
        "scope": (
            "This is a directly Arb-certified finite positive equal-coupling physical path escaping "
            "the particular 197-column dual. It does not invalidate the finite 197-column mixed-order "
            "theorem, prove full continuous-family feasibility/infeasibility, complete sixth/eighth "
            "orbit control, or imply a Choi/diamond operational bound."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "t_exact_decimal": t_string,
        "pricing_score_interval": str(score),
        "strictly_positive": strict_positive,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
