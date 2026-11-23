"""Binary64-screen and 128-bit Arb-price all unused canonical paths against the 185-column dual."""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from joint_low_six_eighth_lp import matrix, orbit_minor
from screen_ising_sixth_moments import orbit
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_185col_mixed_order_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_lp_185col_mixed_order_n21.json"
PARENT_LP_PATH = ROOT / "evidence/joint_low_six_lp_182col_sixth_only_n21.json"
PARENT_DUAL_PATH = ROOT / "evidence/55probe_182col_sixth_only_dual_certificate_n21.json"
PARENT_SCREEN_PATH = ROOT / "evidence/55probe_182col_mixed_order_dual_pricing_screen_n21.json"
PARENT_PRICING_ARB_PATH = ROOT / "evidence/55probe_182col_mixed_order_dual_pricing_arb_n21.json"
PARENT_172_LP_PATH = ROOT / "evidence/joint_low_six_lp_172col_sixth_only_n21.json"
PARENT_172_DUAL_PATH = ROOT / "evidence/55probe_172col_sixth_only_dual_certificate_n21.json"
PARENT_162_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_162col_full_sixth_cuts_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
ESCAPE_CERT_PATH = ROOT / "evidence/continuous_path_dual_escape_arb_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
SCREEN_OUTPUT = ROOT / "evidence/55probe_185col_mixed_order_dual_pricing_screen_n21.json"
ARB_OUTPUT = ROOT / "evidence/55probe_185col_mixed_order_dual_pricing_arb_n21.json"
PRECISION_BITS = 128
MAX_CANDIDATES = 10
SIXTH_SCALE_FLOAT = 5 / 19721
SIXTH_SCALE_EXACT = Fraction(5, 19721)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def orbit_average_minor(entries, indices):
    group = orbit(indices, 42)
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[i][j] for j in subset] for i in subset]).det()
    return total / len(group)


def active_low_feature(system, entries, row, fourth_groups):
    if row < 21:
        d = row + 1
        total = arb(0)
        for i in range(42):
            j = (i + d) % 42
            total += entries[i][i] * entries[j][j] - entries[i][j] * entries[j][i]
        return total / 42
    group = fourth_groups[row - 21]
    total = arb(0)
    for subset in group:
        total += arb_mat([[entries[int(i)][int(j)] for j in subset] for i in subset]).det()
    return total / len(group)


def load_and_validate():
    paths = (
        CERT_PATH, LP_PATH, PARENT_LP_PATH, PARENT_DUAL_PATH,
        PARENT_SCREEN_PATH, PARENT_PRICING_ARB_PATH, PARENT_172_LP_PATH,
        PARENT_172_DUAL_PATH, PARENT_162_LP_PATH, CUT_LP_PATH,
        ESCAPE_CERT_PATH, SEED_POOL_PATH,
    )
    raw = [path.read_bytes() for path in paths]
    values = [
        json.loads(value) if path.suffix != ".npy" else value
        for path, value in zip(paths, raw)
    ]
    (
        cert, lp, parent_lp, parent_dual, parent_screen, parent_pricing,
        parent_172_lp, parent_172_dual, parent_162_lp, cut_lp, escape, seed_raw,
    ) = values
    hashes = dict(zip((p.name for p in paths), map(sha, raw)))

    cert_sha = hashes[CERT_PATH.name]
    lp_sha = hashes[LP_PATH.name]
    parent_lp_sha = hashes[PARENT_LP_PATH.name]
    parent_dual_sha = hashes[PARENT_DUAL_PATH.name]
    screen_sha = hashes[PARENT_SCREEN_PATH.name]
    pricing_sha = hashes[PARENT_PRICING_ARB_PATH.name]
    parent_172_lp_sha = hashes[PARENT_172_LP_PATH.name]
    parent_172_dual_sha = hashes[PARENT_172_DUAL_PATH.name]
    parent_162_lp_sha = hashes[PARENT_162_LP_PATH.name]
    cut_sha = hashes[CUT_LP_PATH.name]
    escape_sha = hashes[ESCAPE_CERT_PATH.name]

    if cert.get("status") != "strict_185col_2106row_mixed_order_minimax_obstruction" or not cert.get("complete"):
        raise RuntimeError("185-column Arb certificate is incomplete")
    if (cert.get("column_count"), cert.get("row_count")) != (185, 2106):
        raise RuntimeError("unexpected 185-column certificate dimensions")
    if cert.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("185-column certificate does not pin its LP")
    if lp.get("parent_182col_lp_sha256") != parent_lp_sha or cert.get("parent_182col_lp_sha256") != parent_lp_sha:
        raise RuntimeError("185-column LP/certificate does not pin the 182-column parent LP")
    if lp.get("parent_182col_dual_certificate_sha256") != parent_dual_sha or cert.get("parent_182col_dual_certificate_sha256") != parent_dual_sha:
        raise RuntimeError("185-column LP/certificate does not pin the 182-column parent dual")
    if cert.get("parent_172col_lp_sha256") != parent_172_lp_sha:
        raise RuntimeError("185-column certificate does not pin the 172-column ancestor LP")
    if cert.get("parent_172col_dual_certificate_sha256") != parent_172_dual_sha:
        raise RuntimeError("185-column certificate does not pin the 172-column ancestor dual")
    if parent_lp.get("parent_172col_lp_sha256") != parent_172_lp_sha or parent_dual.get("parent_172col_lp_sha256") != parent_172_lp_sha:
        raise RuntimeError("182-column parent chain disagrees on the 172-column LP")
    if parent_lp.get("parent_172col_dual_certificate_sha256") != parent_172_dual_sha or parent_dual.get("parent_172col_dual_certificate_sha256") != parent_172_dual_sha:
        raise RuntimeError("182-column parent chain disagrees on the 172-column dual")
    if cert.get("parent_162col_lp_sha256") != parent_162_lp_sha:
        raise RuntimeError("185-column certificate does not pin the 162-column ancestor")
    if cert.get("parent_sixth_row_inventory_sha256") != cut_sha:
        raise RuntimeError("185-column certificate does not pin the sixth-row inventory")
    if cert.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("185-column certificate does not pin the continuous-path certificate")
    if parent_lp.get("parent_162col_lp_sha256") != parent_162_lp_sha or parent_dual.get("parent_162col_lp_sha256") != parent_162_lp_sha:
        raise RuntimeError("182-column parent chain disagrees on the 162-column ancestor")
    if parent_lp.get("parent_sixth_row_inventory_sha256") != cut_sha or parent_dual.get("parent_sixth_row_inventory_sha256") != cut_sha:
        raise RuntimeError("182-column parent chain disagrees on the sixth-row inventory")
    if parent_lp.get("continuous_escape_arb_certificate_sha256") != escape_sha or parent_dual.get("continuous_escape_arb_certificate_sha256") != escape_sha:
        raise RuntimeError("182-column parent chain disagrees on the continuous-path certificate")

    if parent_lp.get("status") != "182col_sixth_only_lp_above_one_third" or (parent_lp.get("columns"), parent_lp.get("rows")) != (182, 2106):
        raise RuntimeError("182-column parent LP has unexpected status or dimensions")
    if parent_dual.get("status") != "strict_182col_2106row_mixed_order_minimax_obstruction" or not parent_dual.get("complete"):
        raise RuntimeError("182-column parent Arb certificate is incomplete")
    if parent_dual.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("182-column parent dual does not pin its LP")
    if parent_pricing.get("status") != "arb_positive_columns_found" or parent_pricing.get("candidates_checked") != 3 or parent_pricing.get("arb_certified_positive_count") != 3:
        raise RuntimeError("182-column parent pricing does not contain three strict Arb-positive escapes")
    if parent_pricing.get("dual_certificate_sha256") != parent_dual_sha or parent_pricing.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("182-column parent pricing hash mismatch")
    if parent_pricing.get("pricing_screen_sha256") != screen_sha:
        raise RuntimeError("182-column parent pricing does not pin its screen")
    if parent_screen.get("dual_certificate_sha256") != parent_dual_sha or parent_screen.get("lp_transcript_sha256") != parent_lp_sha:
        raise RuntimeError("182-column parent screen hash mismatch")
    if parent_screen.get("unused_column_count") != 1460 or parent_screen.get("canonical_column_count") != 1641:
        raise RuntimeError("unexpected 182-column parent pricing inventory")
    if parent_172_dual.get("status") != "strict_172col_2106row_sixth_only_minimax_obstruction" or not parent_172_dual.get("complete"):
        raise RuntimeError("172-column ancestor certificate is incomplete")
    if parent_172_dual.get("lp_transcript_sha256") != parent_172_lp_sha:
        raise RuntimeError("172-column ancestor certificate does not pin its LP")
    if parent_162_lp.get("columns") != 162 or parent_162_lp.get("rows") != 2113:
        raise RuntimeError("162-column ancestor inventory mismatch")
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("complete") or not escape.get("strictly_positive"):
        raise RuntimeError("continuous-path generator lacks its strict Arb certificate")

    seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    if seed.shape != (1600, 42) or sha(seed.tobytes()) != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")
    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = sha(all_array.tobytes())
    if len(all_columns) != 1641 or all_sha != cert.get("canonical_all_columns_sha256_le_f64"):
        raise RuntimeError("canonical pool hash/count mismatch")

    if cert.get("columns") != lp.get("column_order"):
        raise RuntimeError("185-column certificate and LP physical order mismatch")
    active_canonical = sorted(int(x) for x in cert["columns"] if int(x) != 1641)
    expected_active = sorted(
        set(int(x) for x in cert["base_columns"])
        | set(int(x) for x in cert["previous_added_canonical_columns"])
        | set(int(x) for x in cert["added_canonical_columns"])
    )
    if active_canonical != expected_active or len(active_canonical) != 184 or len(set(active_canonical)) != 184:
        raise RuntimeError("185-column canonical inventory mismatch")
    unused = [j for j in range(len(all_columns)) if j not in set(active_canonical)]
    if len(unused) != 1457:
        raise RuntimeError("expected 1,457 unused canonical columns")

    zq = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(zq) != 2106 or sum((abs(value) for value in zq), Fraction(0)) != 1:
        raise RuntimeError("185-column exact dual vector or L1 norm mismatch")
    active_rows = [i for i, value in enumerate(zq) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if i >= 1461]
    if active_low != cert.get("active_dual_low_row_indices") or active_sixth != cert.get("active_dual_sixth_row_indices"):
        raise RuntimeError("185-column dual support indices mismatch")
    if len(active_low) != 2 or len(active_sixth) != 54:
        raise RuntimeError("185-column dual support no longer matches its mixed-order theorem")

    sixth_rows = [tuple(int(x) for x in row) for row in cut_lp["sixth_cut_rows"]]
    sixth_hash = sha(json.dumps([list(x) for x in sixth_rows], separators=(",", ":")).encode())
    if len(sixth_rows) != 645 or sixth_hash != cert.get("sixth_rows_sha256"):
        raise RuntimeError("sixth-order row inventory hash/count mismatch")
    return cert, lp, all_columns, active_canonical, unused, zq, active_low, active_sixth, sixth_rows, {
        "certificate_sha256": cert_sha, "lp_sha256": lp_sha,
        "parent_182_lp_sha256": parent_lp_sha, "parent_182_dual_sha256": parent_dual_sha,
        "parent_182_screen_sha256": screen_sha, "parent_182_pricing_arb_sha256": pricing_sha,
        "parent_172_lp_sha256": parent_172_lp_sha, "parent_172_dual_sha256": parent_172_dual_sha,
        "parent_162_lp_sha256": parent_162_lp_sha, "sixth_rows_sha256": cut_sha,
        "continuous_escape_sha256": escape_sha, "canonical_pool_sha256": all_sha,
        "seed_pool_sha256": SEED_POOL_SHA256,
    }


def main():
    cert, lp, all_columns, active_canonical, unused, zq, active_low, active_sixth, sixth_rows, hashes = load_and_validate()
    system = FourthMoments(21)
    system.exact_target_check()
    low_scales_float = np.r_[
        np.full(21, 1 / 41),
        np.full(len(system.keys), comb(21, 2) / comb(42, 4)),
    ]
    z = np.asarray([float(value) for value in zq], dtype=np.float64)
    lam_q = Fraction(cert["dual_lambda_exact"]) - Fraction(cert["dual_slack_delta"])
    lam = float(lam_q)
    active_low_np = np.asarray(active_low, dtype=int)

    scores = np.empty(len(all_columns), dtype=np.float64)
    for column, couplings in enumerate(all_columns):
        rotation = matrix(couplings)
        low_features = system.features(np.asarray(couplings, dtype=np.float64))
        score = lam
        if len(active_low_np):
            score += float(np.dot(z[active_low_np], low_features[active_low_np] / low_scales_float[active_low_np]))
        for row in active_sixth:
            score += z[row] * orbit_minor(rotation, sixth_rows[row - 1461]) / SIXTH_SCALE_FLOAT
        scores[column] = score
        if (column + 1) % 100 == 0:
            print(f"Priced canonical columns {column + 1}/{len(all_columns)}", flush=True)

    active_scores = [float(scores[column]) for column in active_canonical]
    ranked = sorted(((column, float(scores[column])) for column in unused), key=lambda item: item[1], reverse=True)
    positive = [(column, score) for column, score in ranked if score > 0]
    screen = {
        "status": "priced_unused_canonical_pool_against_185col_mixed_order_dual",
        **hashes,
        "canonical_column_count": len(all_columns),
        "active_column_count": len(cert["columns"]),
        "active_canonical_column_count": len(active_canonical),
        "active_canonical_columns": active_canonical,
        "unused_column_count": len(unused),
        "active_dual_row_count": len(active_low) + len(active_sixth),
        "active_low_dual_rows": active_low,
        "active_sixth_dual_rows": active_sixth,
        "active_pool_max_float_pricing_score": max(active_scores),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": ranked[0][1] if ranked else None,
        "top_unused_candidates": [
            {"column": int(column), "float_pricing_score": float(score),
             "couplings": [float(value) for value in all_columns[column]]}
            for column, score in ranked[:50]
        ],
        "top_positive_candidates": [
            {"column": int(column), "float_pricing_score": float(score),
             "couplings": [float(value) for value in all_columns[column]]}
            for column, score in positive[:50]
        ],
        "scope": (
            "Binary64 pricing of all 1,457 unused canonical paths against the exact rational 185-column "
            "mixed-order dual. Scores include its two active low-order and 54 active sixth-order rows. "
            "Positive scores are discovery candidates and require Arb checks; nonpositive binary64 scores "
            "are not strict exclusion certificates."
        ),
    }
    SCREEN_OUTPUT.write_text(json.dumps(screen, indent=2) + "\n")
    print(json.dumps({
        "status": screen["status"],
        "unused_column_count": len(unused),
        "unused_positive_pricing_count": len(positive),
        "max_unused_float_pricing_score": screen["max_unused_float_pricing_score"],
        "top_positive_candidates": screen["top_positive_candidates"][:10],
        "screen_output": str(SCREEN_OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)

    ctx.prec = PRECISION_BITS
    low_scales_exact = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }
    candidates = screen["top_positive_candidates"][:MAX_CANDIDATES]
    results = []
    for item in candidates:
        column = int(item["column"])
        couplings = all_columns[column]
        if [float(value) for value in couplings] != item["couplings"]:
            raise RuntimeError(f"candidate {column} differs from the frozen canonical pool")
        entries = rotation_entries_exact(couplings)
        score = ball(lam_q)
        for row in active_low:
            score += ball(zq[row]) * active_low_feature(system, entries, row, fourth_groups) / ball(low_scales_exact[row])
        for row in active_sixth:
            score += ball(zq[row]) * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(SIXTH_SCALE_EXACT)
        lower, upper = score.lower(), score.upper()
        results.append({
            "column": column,
            "float_pricing_score": item["float_pricing_score"],
            "arb_pricing_score_interval": str(score),
            "arb_lower_endpoint": str(lower),
            "arb_upper_endpoint": str(upper),
            "strictly_positive": lower > 0,
            "couplings": [float(value) for value in couplings],
        })
        print(f"Arb-priced canonical column {column}: {score}", flush=True)

    strict_positive = [item for item in results if item["strictly_positive"]]
    arb_result = {
        "status": "arb_positive_columns_found" if strict_positive else (
            "no_float_positive_candidates" if not candidates else "float_candidates_not_arb_certified"
        ),
        **hashes,
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "active_dual_rows": len(active_low) + len(active_sixth),
        "active_low_dual_rows": active_low,
        "active_sixth_dual_rows": active_sixth,
        "active_canonical_column_count": len(active_canonical),
        "unused_canonical_column_count": len(unused),
        "float_positive_candidate_count": len(positive),
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(strict_positive),
        "results": results,
        "scope": (
            "128-bit Arb checks of up to ten highest binary64-positive unused canonical columns against "
            "the exact 185-column mixed-order dual. A strictly positive lower endpoint proves that the "
            "185-column separator is escaped after adding that column; it does not prove a feasible mixture. "
            "If no checked candidate is positive, this does not certify all unused columns."
        ),
    }
    ARB_OUTPUT.write_text(json.dumps(arb_result, indent=2) + "\n")
    print(json.dumps({
        "status": arb_result["status"],
        "candidates_checked": len(results),
        "arb_certified_positive_count": len(strict_positive),
        "results": results,
        "arb_output": str(ARB_OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
