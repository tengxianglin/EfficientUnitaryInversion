"""128-bit Arb verification of an explicit finite uniform-path escape time for the 196-column dual."""
import hashlib
import json
from fractions import Fraction

from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import ROOT
from verify_184col_full_sixth_cut_dual_arb import (
    active_low_feature,
    load_exact_design,
    orbit_average_minor,
)
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_196col_uniform_ray_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_196col_uniform_ray_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
DISCOVERY_PATH = ROOT / "evidence/196col_uniform_ray_time_search_n21.json"
OUTPUT_PATH = ROOT / "evidence/196col_uniform_ray_time_arb_n21.json"
TORUS_CERT_PATH = ROOT / "evidence/196col_uniform_torus_arb_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_195col_uniform_ray_escape_n21.json"
PARENT_DUAL_PATH = ROOT / "evidence/55probe_195col_uniform_ray_escape_dual_certificate_n21.json"
PARENT_TIME_CERT_PATH = ROOT / "evidence/195col_uniform_ray_time_arb_n21.json"
ANCESTOR_TIME_CERT_PATH = ROOT / "evidence/194col_uniform_ray_time_arb_n21.json"

PRECISION_BITS = 128
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = Fraction(5, 19721)
EIGHTH_SCALE = Fraction(1, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def exact_uniform_ray_rotation(t_exact):
    t = Fraction(t_exact)
    if t <= 0:
        raise RuntimeError("uniform-ray time must be strictly positive")
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
    for k in range(1, 22):
        omega = 4 * (pi * ball(Fraction(k, 43))).cos()
        angle = ball(t) * omega
        cosine, sine = angle.cos(), angle.sin()
        index = k - 1
        block[2 * index, 2 * index] = cosine
        block[2 * index, 2 * index + 1] = sine
        block[2 * index + 1, 2 * index] = -sine
        block[2 * index + 1, 2 * index + 1] = cosine

    qt = arb_mat([[q[j, i] for j in range(42)] for i in range(42)])
    rotation = q * block * qt
    return [[rotation[i, j] for j in range(42)] for i in range(42)]


def main():
    ctx.prec = PRECISION_BITS
    cert_raw = CERT_PATH.read_bytes()
    lp_raw = LP_PATH.read_bytes()
    cut_raw = CUT_LP_PATH.read_bytes()
    discovery_raw = DISCOVERY_PATH.read_bytes()
    torus_raw = TORUS_CERT_PATH.read_bytes()
    parent_lp_raw = PARENT_LP_PATH.read_bytes()
    parent_dual_raw = PARENT_DUAL_PATH.read_bytes()
    parent_time_raw = PARENT_TIME_CERT_PATH.read_bytes()
    ancestor_time_raw = ANCESTOR_TIME_CERT_PATH.read_bytes()
    cert, lp, cut, discovery, torus, parent_lp, parent_dual, parent_time, ancestor_time = [
        json.loads(raw) for raw in (cert_raw, lp_raw, cut_raw, discovery_raw, torus_raw, parent_lp_raw, parent_dual_raw, parent_time_raw, ancestor_time_raw)
    ]
    cert_sha, lp_sha, cut_sha, discovery_sha, torus_sha, parent_lp_sha, parent_dual_sha, parent_time_sha, ancestor_time_sha = map(
        sha, (cert_raw, lp_raw, cut_raw, discovery_raw, torus_raw, parent_lp_raw, parent_dual_raw, parent_time_raw, ancestor_time_raw)
    )
    if cert.get("status") != "strict_196col_2113row_uniform_ray_escape_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("196-column dual is not strictly Arb-certified")
    if (cert.get("column_count"), cert.get("row_count")) != (196, 2113) or cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("196-column certificate dimensions/hash mismatch")
    if cert.get("parent_195col_lp_sha256") != parent_lp_sha or cert.get("parent_195col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("196-column certificate does not pin its 195-column parent")
    if cert.get("uniform_ray_time_arb_certificate_sha256") != parent_time_sha:
        raise RuntimeError("196-column certificate does not pin the previous 195-column finite-time path")
    if cert.get("parent_194col_uniform_ray_time_arb_certificate_sha256") != ancestor_time_sha:
        raise RuntimeError("196-column certificate does not pin the 194-column ancestor time")
    if parent_lp.get("status") != "195col_uniform_ray_escape_lp_above_one_third" or (parent_lp.get("columns"), parent_lp.get("rows")) != (195, 2113):
        raise RuntimeError("195-column parent LP is not the expected above-cap discovery")
    if parent_dual.get("status") != "strict_195col_2113row_uniform_ray_escape_minimax_obstruction" or not parent_dual.get("complete") or parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("195-column parent dual is not strictly certified against its LP")
    if parent_lp.get("uniform_ray_time_arb_certificate_sha256") != ancestor_time_sha or parent_dual.get("uniform_ray_time_arb_certificate_sha256") != ancestor_time_sha:
        raise RuntimeError("195-column parent LP/dual does not pin the 194-column time certificate")
    if ancestor_time.get("status") != "certified_finite_uniform_ray_escape" or not ancestor_time.get("finite_physical_escape_certified"):
        raise RuntimeError("194-column ancestor time is not Arb-certified")
    if ancestor_time.get("dual_certificate_sha256") != parent_lp.get("parent_194col_dual_certificate_sha256") or ancestor_time.get("lp_transcript_sha256") != parent_lp.get("parent_194col_lp_sha256"):
        raise RuntimeError("194-column ancestor time provenance mismatch")
    if parent_time.get("status") != "certified_finite_uniform_ray_escape" or not parent_time.get("finite_physical_escape_certified"):
        raise RuntimeError("195-column previous uniform path is not Arb-certified")
    if parent_time.get("dual_certificate_sha256") != parent_dual_sha or parent_time.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("195-column previous uniform path provenance mismatch")
    if Fraction(cert["uniform_ray_time_exact_rational"]) != Fraction(parent_time["t_exact_rational"]):
        raise RuntimeError("196-column dual has the wrong previous 195-column uniform time")
    if Fraction(cert["parent_194col_uniform_ray_time_exact_rational"]) != Fraction(ancestor_time["t_exact_rational"]):
        raise RuntimeError("196-column dual has the wrong 194-column ancestor uniform time")
    if lp.get("status") != "196col_uniform_ray_escape_lp_above_one_third" or (lp.get("columns"), lp.get("rows")) != (196, 2113):
        raise RuntimeError("196-column LP is not the expected above-cap discovery")
    if lp.get("parent_195col_lp_sha256") != parent_lp_sha or lp.get("parent_195col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("196-column LP does not pin its 195-column parent")
    if lp.get("uniform_ray_time_arb_certificate_sha256") != parent_time_sha or lp.get("parent_194col_uniform_ray_time_arb_certificate_sha256") != ancestor_time_sha:
        raise RuntimeError("196-column LP does not pin both previous uniform-ray certificates")
    if torus.get("status") != "certified_196col_uniform_torus_dual_escape" or not torus.get("complete") or not torus.get("strictly_positive"):
        raise RuntimeError("196-column torus point is not independently Arb-certified positive")
    if torus.get("dual_certificate_sha256") != cert_sha or torus.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("196-column torus certificate does not pin the current dual/LP")
    if discovery.get("dual_certificate_sha256") != cert_sha or discovery.get("lp_transcript_sha256") != lp_sha or discovery.get("cut_lp_transcript_sha256") != cut_sha:
        raise RuntimeError("196-column finite-time discovery does not pin the current dual/LP/cut")
    if discovery.get("torus_arb_certificate_sha256") != torus_sha or discovery.get("torus_phase_vector_sha256") != torus.get("phase_vector_sha256"):
        raise RuntimeError("196-column finite-time discovery does not pin the exact torus Arb certificate")
    if discovery.get("parent_195col_lp_sha256") != parent_lp_sha or discovery.get("parent_195col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("196-column finite-time discovery does not pin the 195-column parent")
    if discovery.get("parent_195col_uniform_ray_time_arb_certificate_sha256") != parent_time_sha or discovery.get("parent_194col_uniform_ray_time_arb_certificate_sha256") != ancestor_time_sha:
        raise RuntimeError("196-column finite-time discovery does not pin both previous uniform-ray certificates")
    if not discovery.get("candidate_found"):
        result = {
            "status": "no_positive_finite_uniform_ray_candidate_found",
            "complete": True,
            "strictly_positive": False,
            "precision_bits": ctx.prec,
            "dual_certificate_sha256": cert_sha,
            "lp_transcript_sha256": lp_sha,
            "parent_195col_lp_sha256": parent_lp_sha,
            "parent_195col_dual_certificate_sha256": parent_dual_sha,
            "parent_195col_uniform_ray_time_arb_certificate_sha256": parent_time_sha,
            "parent_194col_uniform_ray_time_arb_certificate_sha256": ancestor_time_sha,
            "torus_arb_certificate_sha256": torus_sha,
            "torus_phase_vector_sha256": torus.get("phase_vector_sha256"),
            "discovery_sha256": discovery_sha,
            "best_t_exact_decimal": discovery.get("best_t_exact_decimal"),
            "best_score_binary64": discovery.get("best_score_binary64"),
            "scope": (
                "The bounded one-dimensional search found no positive candidate. The previously "
                "proved dense-torus argument still establishes existence of some finite t>0, but "
                "this search did not locate an explicit decimal witness."
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
    if len(z) != 2113 or norm != Fraction(cert["dual_l1_norm_exact"]) or norm > 1:
        raise RuntimeError("exact 196-column dual dimension/L1 normalization mismatch")
    active = [index for index, value in enumerate(z) if value]
    active_low = [index for index in active if index < LOW_COUNT]
    active_sixth = [index for index in active if LOW_COUNT <= index < SIXTH_END]
    active_eighth = [index for index in active if index >= SIXTH_END]
    if (len(active), len(active_low), len(active_sixth), len(active_eighth)) != (63, 5, 57, 1):
        raise RuntimeError("unexpected 196-column active dual row blocks")

    system, low_scales, sixth_rows, eighth_rows, y, row_blocks = load_exact_design(cut)
    if row_blocks != cert.get("row_blocks"):
        raise RuntimeError("exact 2,113-row design block mismatch")
    entries = exact_uniform_ray_rotation(t)
    fourth_groups = {
        row - 21: system.indices[system.ids == row - 21]
        for row in active_low if row >= 21
    }
    lam = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
    score = ball(lam)
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
        "parent_195col_lp_sha256": parent_lp_sha,
        "parent_195col_dual_certificate_sha256": parent_dual_sha,
        "parent_195col_uniform_ray_time_arb_certificate_sha256": parent_time_sha,
        "parent_194col_uniform_ray_time_arb_certificate_sha256": ancestor_time_sha,
        "torus_arb_certificate_sha256": torus_sha,
        "torus_phase_vector_sha256": torus.get("phase_vector_sha256"),
        "cut_lp_transcript_sha256": cut_sha,
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
            "This is a directly Arb-certified finite positive uniform-coupling path escaping the "
            "particular 196-column dual. It does not invalidate the finite 196-column minimax theorem "
            "or prove a full continuous-family minimax result."
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
