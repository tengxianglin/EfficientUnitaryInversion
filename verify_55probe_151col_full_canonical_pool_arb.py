"""128-bit Arb audit of every unused column in the frozen 1,641-column canonical pool.

If every unused column has a strictly negative certified pricing interval, the
151-column dual extends to the entire frozen canonical pool on the pinned
1,779-row feature set. This remains finite-pool evidence, not an all-Hamiltonian
or all-moment theorem.
"""
import hashlib
import json
from fractions import Fraction
from math import comb

import numpy as np
from flint import arb, arb_mat, ctx

from audit_complete_sixth_moments import canonical_ensemble, ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit
from joint_low_six_eighth_lp import EIGHTH_ROWS
from verify_ising_sixth_escape import rotation_entries_exact
from verify_ising_moment_pricing import ball

CERT_PATH = ROOT / "evidence/55probe_151col_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_151col_55probe_n21.json"
SCREEN_PATH = ROOT / "evidence/55probe_151col_dual_pricing_screen_n21.json"
SIXTH_SCREEN_PATH = ROOT / "evidence/sixth_moment_screen_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
OUTPUT_PATH = ROOT / "evidence/55probe_151col_full_canonical_pool_arb_n21.json"
PRECISION_BITS = 128


def orbit_average_minor(entries, indices):
    group = orbit(indices)
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


def main():
    ctx.prec = PRECISION_BITS
    cert_raw = CERT_PATH.read_bytes()
    cert_sha = hashlib.sha256(cert_raw).hexdigest()
    cert = json.loads(cert_raw)
    lp_raw = LP_PATH.read_bytes()
    lp_sha = hashlib.sha256(lp_raw).hexdigest()
    screen_raw = SCREEN_PATH.read_bytes()
    screen_sha = hashlib.sha256(screen_raw).hexdigest()
    lp = json.loads(lp_raw)
    screen = json.loads(screen_raw)

    if cert.get("status") != "strict_pool_separation" or not cert.get("complete"):
        raise RuntimeError("the 151-column Arb dual certificate is incomplete")
    if cert["lp_transcript_sha256"] != lp_sha:
        raise RuntimeError("certificate and LP transcript hashes disagree")
    if cert["column_count"] != 151 or cert["row_count"] != 1779:
        raise RuntimeError("unexpected 151-column certificate dimensions")
    if screen.get("dual_certificate_sha256") != cert_sha:
        raise RuntimeError("pricing screen does not pin the 151-column certificate")
    if screen.get("lp_transcript_sha256") != lp_sha:
        raise RuntimeError("pricing screen does not pin the LP transcript")
    if screen.get("canonical_all_columns_sha256_le_f64") != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("pricing screen and certificate use different canonical pools")
    if screen.get("unused_positive_pricing_count") != 0:
        raise RuntimeError("binary64 screen reports positive columns; use the candidate Arb verifier first")

    seed_array = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
    seed_sha = hashlib.sha256(seed_array.tobytes()).hexdigest()
    if seed_array.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
        raise RuntimeError("frozen seed-pool hash/shape mismatch")

    all_columns, _, _ = canonical_ensemble()
    all_array = np.asarray(all_columns, dtype="<f8")
    all_sha = hashlib.sha256(all_array.tobytes()).hexdigest()
    if len(all_columns) != 1641 or all_sha != cert["canonical_all_columns_sha256_le_f64"]:
        raise RuntimeError("canonical physical column pool hash/count mismatch")

    active_columns = sorted(int(value) for value in cert["columns"])
    active_set = set(active_columns)
    if len(active_columns) != 151 or len(active_set) != 151:
        raise RuntimeError("the certificate does not contain 151 distinct columns")
    active_hash = hashlib.sha256()
    for column in active_columns:
        active_hash.update(int(column).to_bytes(4, "little", signed=False))
    if active_hash.hexdigest() != cert["canonical_151_column_index_sha256"]:
        raise RuntimeError("151-column index hash mismatch")

    z = [Fraction(value) for value in cert["dual_vector_rational"]]
    if len(z) != 1779:
        raise RuntimeError("unexpected exact dual-vector dimension")
    if sum((abs(value) for value in z), Fraction(0)) != Fraction(cert["dual_l1_norm_exact"]):
        raise RuntimeError("exact dual L1 norm does not match the certificate")
    lam = Fraction(cert["dual_lambda_before_slack"]) - Fraction(cert["dual_slack_delta"])
    z_arb = [ball(value) for value in z]

    system = FourthMoments(21)
    system.exact_target_check()
    low_scales = (
        [Fraction(1, 41)] * 21
        + [Fraction(comb(21, 2), comb(42, 4))] * len(system.keys)
    )
    screen_rows = json.loads(SIXTH_SCREEN_PATH.read_text())["records"]
    if len(screen_rows) != 256:
        raise RuntimeError("the frozen sixth-order screen must contain 256 rows")
    sixth_rows = [tuple(row["indices"]) for row in screen_rows]
    sixth_rows += [tuple(row) for row in lp["sixth_probe_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_full_audit_separator_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_prefix_separator_rows"]]
    sixth_rows += [tuple(row) for row in lp["sixth_additional_full_audit_separator_rows"]]
    eighth_rows = [tuple(row) for row in lp["selected_eighth_rows"]]
    if len(sixth_rows) != 311 or eighth_rows != [tuple(row) for row in EIGHTH_ROWS]:
        raise RuntimeError("pinned 55-separator row inventory mismatch")
    if (len(z), len(low_scales) + len(sixth_rows) + len(eighth_rows)) != (1779, 1779):
        raise RuntimeError("feature/dual dimensions disagree")

    active_rows = [i for i, value in enumerate(z) if value]
    active_low = [i for i in active_rows if i < 1461]
    active_sixth = [i for i in active_rows if 1461 <= i < 1772]
    active_eighth = [i for i in active_rows if 1772 <= i < 1779]
    fourth_groups = {
        row - 21: system.indices[system.ids == (row - 21)]
        for row in active_low if row >= 21
    }

    unused = [column for column in range(len(all_columns)) if column not in active_set]
    if len(unused) != 1490:
        raise RuntimeError("expected exactly 1,490 unused canonical columns")

    results = []
    max_upper = None
    max_upper_column = None
    max_lower = None
    min_upper = None
    for position, column in enumerate(unused, start=1):
        couplings = all_columns[column]
        if len(couplings) != 42 or couplings[-1] != 0 or any(value == 0 for value in couplings[:-1]):
            raise RuntimeError(f"canonical column {column} is not a legal 42-site path generator")
        entries = rotation_entries_exact(couplings)
        score = ball(lam)
        for row in active_low:
            feature = active_low_feature(system, entries, row, fourth_groups)
            score += z_arb[row] * feature / ball(low_scales[row])
        for row in active_sixth:
            score += z_arb[row] * orbit_average_minor(entries, sixth_rows[row - 1461]) / ball(Fraction(5, 19721))
        for row in active_eighth:
            score += z_arb[row] * orbit_average_minor(entries, eighth_rows[row - 1772]) / ball(Fraction(1, 19721))

        lower, upper = score.lower(), score.upper()
        negative = upper < 0
        result = {
            "column": int(column),
            "arb_pricing_score_interval": str(score),
            "arb_lower_endpoint": str(lower),
            "arb_upper_endpoint": str(upper),
            "strictly_negative": bool(negative),
        }
        results.append(result)
        if max_upper is None or upper > max_upper:
            max_upper, max_upper_column = upper, int(column)
        if min_upper is None or upper < min_upper:
            min_upper = upper
        if position % 100 == 0:
            print(json.dumps({
                "progress": position,
                "total": len(unused),
                "last_column": int(column),
                "last_upper": str(upper),
                "current_max_upper": str(max_upper),
                "current_max_column": max_upper_column,
            }), flush=True)

    negative_count = sum(1 for row in results if row["strictly_negative"])
    status = "strict_full_canonical_pool_separation" if negative_count == len(unused) else "canonical_pool_escape_found"
    unused_hash = hashlib.sha256()
    for column in unused:
        unused_hash.update(int(column).to_bytes(4, "little", signed=False))
    result = {
        "status": status,
        "complete": True,
        "dual_certificate_sha256": cert_sha,
        "lp_transcript_sha256": lp_sha,
        "pricing_screen_sha256": screen_sha,
        "canonical_all_columns_sha256_le_f64": all_sha,
        "canonical_column_count": len(all_columns),
        "certified_active_column_count": len(active_columns),
        "arb_audited_unused_column_count": len(unused),
        "unused_column_index_sha256": unused_hash.hexdigest(),
        "row_count": 1779,
        "active_dual_row_count": len(active_rows),
        "active_row_blocks": {
            "low": len(active_low), "sixth": len(active_sixth), "eighth": len(active_eighth)
        },
        "precision_bits": ctx.prec,
        "interval_backend": "python-flint 0.8.0 / Arb",
        "strictly_negative_count": negative_count,
        "nonnegative_count": len(unused) - negative_count,
        "maximum_arb_upper_endpoint": str(max_upper),
        "maximum_upper_endpoint_column": max_upper_column,
        "minimum_arb_upper_endpoint": str(min_upper),
        "results": results,
        "scope": (
            "If status is strict_full_canonical_pool_separation, the pinned 151-column dual "
            "is Arb-certified against all 1,641 columns in the frozen canonical 42-site path "
            "pool, for the exact 1,779 low/sixth/selected-eighth rows. This remains a finite "
            "canonical-pool theorem; it is not a result for all legal physical Hamiltonians, "
            "all moment rows, or operational Choi/diamond distance."
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": status,
        "canonical_column_count": len(all_columns),
        "arb_audited_unused_column_count": len(unused),
        "strictly_negative_count": negative_count,
        "nonnegative_count": len(unused) - negative_count,
        "maximum_arb_upper_endpoint": str(max_upper),
        "maximum_upper_endpoint_column": max_upper_column,
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
    }, indent=2), flush=True)
    if status != "strict_full_canonical_pool_separation":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
