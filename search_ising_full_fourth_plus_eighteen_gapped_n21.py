"""Deterministic pricing search for the Arb-certified 6,141-column n=21 dual.

The search tests arbitrary nonnegative nearest-neighbour couplings on a 42-site
open path (the wrap coupling is fixed to zero), including connected and
multi-segment paths. It is finite multistart discovery, not a global
optimization certificate. Any proposed escape must be frozen as exact
rationals and independently re-evaluated with Arb before it is claimed.
"""
import hashlib
import json
import time
from pathlib import Path
from fractions import Fraction

import numpy as np
from scipy.optimize import minimize

from ising_fourth_moments import seed_pool
from ising_moment_pricing import MomentFunctional

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = ROOT / "evidence/ising_full_fourth_plus_eighteen_gapped_n21.json"
FINITE_CERT = ROOT / "evidence/ising_full_fourth_plus_eighteen_gapped_arb_n21.json"
OUTPUT = ROOT / "evidence/ising_full_fourth_plus_eighteen_gapped_search_n21.json"
N = 42
RANDOM_SEED = 20261129
POOL_SAMPLE_COUNT = 256
CONNECTED_RANDOM_COUNT = 256
MULTISEGMENT_RANDOM_COUNT = 256
OPTIMIZE_PER_CLASS = 12
MAX_ITER = 160
COUPLING_MAX = 500.0
ESCAPE_DISCOVERY_MARGIN = 1e-6


def load_functional():
    diagnostic_raw = DIAGNOSTIC.read_bytes()
    finite_raw = FINITE_CERT.read_bytes()
    diagnostic = json.loads(diagnostic_raw)
    finite = json.loads(finite_raw)

    diagnostic_sha = hashlib.sha256(diagnostic_raw).hexdigest()
    finite_sha = hashlib.sha256(finite_raw).hexdigest()

    if finite.get("status") != "arb_certified_finite_6141_column_full_fourth_plus_eighteen_gapped_separator":
        raise RuntimeError("the 6,141-column Arb certificate is not complete")
    if not finite.get("complete") or finite.get("candidate_count") != 6141:
        raise RuntimeError("the 6,141-column certificate has incorrect pool metadata")
    if finite.get("diagnostic_sha256") != diagnostic_sha:
        raise RuntimeError("the Arb certificate does not pin the current 6,141-column diagnostic")
    if finite.get("dual_scaled_l1_exact") != "1" or finite.get("dual_full_coordinate_l1_upper_bound") != 533:
        raise RuntimeError("the exact dual normalization/norm bound is missing")
    if Fraction(finite.get("dual_full_coordinate_l1_exact", "0")) > 533:
        raise RuntimeError("the exact full-coordinate dual norm exceeds 533")
    if (
        finite.get("base_atom_count") != 22
        or finite.get("fractional_grid_count") != 6101
        or finite.get("general_gapped_count") != 16
        or finite.get("dual_nonzero_coefficients") != 103
    ):
        raise RuntimeError("the 6,141-column certificate has unexpected pool/dual dimensions")

    metadata = {
        int(item["feature_index"]): item
        for item in diagnostic["dual"]["nonzero_coefficients"]
    }
    exact = {
        int(item["feature_index"]): item["coefficient"]
        for item in finite["dual_coefficients_exact_rational"]
    }
    if len(exact) != 103 or set(exact) != set(metadata):
        raise RuntimeError("the 103-term Arb dual does not match the discovery metadata")

    second = ["0"] * 21
    terms = []
    for index, coefficient in sorted(exact.items()):
        item = metadata[index]
        if index < 21:
            second[index] = coefficient
        else:
            if not item.get("representative"):
                raise RuntimeError(f"missing orbit representative for feature {index}")
            terms.append({
                "indices": item["representative"],
                "coefficient": coefficient,
            })
    functional = MomentFunctional({
        "n": 21,
        "second_coefficients": second,
        "terms": terms,
    })
    exact_target = functional.exact_target()
    target_mid = float(
        finite["target_score_interval"].split(" +/- ")[0].strip("[]")
    )
    if abs(float(exact_target) - target_mid) > 2e-14:
        raise RuntimeError("reconstructed exact target score disagrees with the Arb certificate")
    return functional, exact_target, {
        "diagnostic_sha256": diagnostic_sha,
        "finite_certificate_sha256": finite_sha,
        "target_score_exact": str(exact_target),
        "target_score_float": repr(float(exact_target)),
        "dual_nonzero_coefficients": len(exact),
        "finite_certificate_status": finite["status"],
    }

def score(functional, couplings):
    return functional.value_gradient(np.r_[np.asarray(couplings, dtype=float), 0.0], False)


def finite_difference_self_test(functional, rng):
    c = np.exp(rng.normal(-0.2, 0.35, size=41))
    value, gradient = functional.value_gradient(np.r_[c, 0.0], True)
    errors = []
    for index in (0, 20, 40):
        step = 2e-6
        plus = c.copy()
        minus = c.copy()
        plus[index] += step
        minus[index] -= step
        finite_difference = (
            score(functional, plus) - score(functional, minus)
        ) / (2 * step)
        errors.append(abs(finite_difference - gradient[index]))
    maximum = max(errors)
    if maximum > 2e-5:
        raise RuntimeError(f"Frechet-gradient self-test failed: {maximum}")
    return {
        "base_value": float(value),
        "tested_coordinates": [0, 20, 40],
        "absolute_errors": errors,
        "maximum_absolute_error": maximum,
    }


def random_connected(rng):
    scale = 10.0 ** rng.uniform(-0.8, 2.5)
    sigma = rng.uniform(0.2, 1.35)
    return np.clip(
        scale * np.exp(sigma * rng.normal(size=41)),
        1e-6,
        COUPLING_MAX,
    )


def random_fractional_perturbation(rng):
    length = int(rng.integers(2, 43))
    alpha = float(rng.uniform(0.05, 2.0))
    profile = np.zeros(41)
    j = np.arange(length - 1, dtype=float)
    profile[: length - 1] = (
        alpha * np.pi / 4 * np.sqrt((j + 1) * (length - 1 - j))
    )
    scale = max(float(np.max(profile)), 1.0)
    background = scale * 10.0 ** rng.uniform(-3.0, -0.7)
    profile += background * np.exp(0.5 * rng.normal(size=41))
    return np.clip(profile, 1e-6, COUPLING_MAX), {
        "length": length,
        "alpha": alpha,
    }


def random_multisegment(rng):
    segment_count = int(rng.integers(2, 6))
    cuts = sorted(
        int(x) for x in rng.choice(np.arange(1, 40), segment_count - 1, replace=False)
    )
    c = np.zeros(41)
    boundaries = [0, *cuts, 41]
    segment_scales = []
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        scale = 10.0 ** rng.uniform(-0.8, 2.5)
        sigma = rng.uniform(0.15, 1.0)
        c[left:right] = np.clip(
            scale * np.exp(sigma * rng.normal(size=right - left)),
            1e-6,
            COUPLING_MAX,
        )
        segment_scales.append(scale)
    c[cuts] = 0.0
    return c, {
        "segment_count": segment_count,
        "zero_edges": cuts,
        "segment_scales": segment_scales,
    }


def optimize_start(functional, start, fixed_zero_edges, connected):
    start = np.asarray(start, dtype=float).copy()
    fixed = set(int(x) for x in fixed_zero_edges)
    free = np.asarray([j for j in range(41) if j not in fixed], dtype=int)
    if not len(free):
        return start, score(functional, start), {
            "success": False,
            "message": "no free coupling coordinates",
            "iterations": 0,
        }
    lower = 1e-6 if connected else 1e-8
    bounds = [(lower, COUPLING_MAX)] * len(free)

    def objective(x):
        c = start.copy()
        c[free] = x
        value, gradient = functional.value_gradient(np.r_[c, 0.0], True)
        return -float(value), -np.asarray(gradient[free], dtype=float)

    result = minimize(
        objective,
        start[free],
        method="L-BFGS-B",
        jac=True,
        bounds=bounds,
        options={
            "maxiter": MAX_ITER,
            "ftol": 1e-12,
            "gtol": 1e-7,
            "maxls": 30,
        },
    )
    optimized = start.copy()
    optimized[free] = result.x
    for edge in fixed:
        optimized[edge] = 0.0
    return optimized, score(functional, optimized), {
        "success": bool(result.success),
        "message": str(result.message),
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
    }


def record_candidate(couplings, value, target, label, optimized, optimizer=None):
    c = np.asarray(couplings, dtype=float)
    return {
        "label": label,
        "optimized": bool(optimized),
        "optimizer": optimizer,
        "score_float": format(float(value), ".17g"),
        "target_minus_score_float": format(float(target - value), ".17g"),
        "couplings_exact_decimal": [format(float(x), ".17g") for x in c] + ["0"],
        "internal_zero_edges": [int(j) for j in np.flatnonzero(c == 0.0)],
        "minimum_positive_coupling": (
            format(float(np.min(c[c > 0])), ".17g") if np.any(c > 0) else None
        ),
        "maximum_coupling": format(float(np.max(c)), ".17g"),
    }


def main():
    started = time.perf_counter()
    rng = np.random.default_rng(RANDOM_SEED)
    functional, exact_target, pins = load_functional()
    target = float(exact_target)
    gradient_check = finite_difference_self_test(functional, rng)

    pool = seed_pool()
    pool_hash = hashlib.sha256(pool.astype("<f8", copy=False).tobytes()).hexdigest()
    pool_indices = rng.choice(len(pool), size=min(POOL_SAMPLE_COUNT, len(pool)), replace=False)

    connected = []
    multisegment = []
    for index in pool_indices:
        c = np.asarray(pool[int(index), :41], dtype=float)
        connected.append((c, {"source": "frozen_seed_pool", "pool_index": int(index)}))
    for index in range(CONNECTED_RANDOM_COUNT):
        connected.append((random_connected(rng), {"source": "independent_lognormal", "index": index}))
    # Include every pinned gapped path as a reproducible local-search start.
    # These columns are in the finite pool and provide useful basins for pricing
    # the newly certified dual.
    for index in range(CONNECTED_RANDOM_COUNT // 2):
        c, meta = random_fractional_perturbation(rng)
        connected.append((c, {"source": "fractional_profile_plus_positive_background", "index": index, **meta}))
    diag = json.loads(DIAGNOSTIC.read_text())
    for column in diag["appended_gapped_columns"]:
        exact = [Fraction(value) for value in column["couplings_exact_rational"]]
        couplings = np.asarray([float(value) for value in exact[:41]], dtype=float)
        zero_edges = [int(j) for j, value in enumerate(exact[:41]) if value == 0]
        label = {
            "source": "certified_6141_finite_pool",
            "column_kind": column["kind"],
            "zero_edges": zero_edges,
            "segment_count": len(zero_edges) + 1,
        }
        if zero_edges:
            multisegment.append((couplings, label))
        else:
            connected.append((couplings, label))
    for index in range(MULTISEGMENT_RANDOM_COUNT):
        c, meta = random_multisegment(rng)
        multisegment.append((c, {"source": "piecewise_random_segments", "index": index, **meta}))

    evaluated = []
    for kind, collection in (("connected", connected), ("multisegment", multisegment)):
        for index, (c, label) in enumerate(collection):
            value = score(functional, c)
            evaluated.append({
                "kind": kind,
                "index": index,
                "score": float(value),
                "couplings": c,
                "label": label,
                "fixed_zero_edges": list(label.get("zero_edges", [])),
            })

    best_by_kind = {}
    optimization_records = []
    for kind, collection in (("connected", connected), ("multisegment", multisegment)):
        candidates = [item for item in evaluated if item["kind"] == kind]
        candidates.sort(key=lambda item: item["score"], reverse=True)
        best_value = candidates[0]["score"]
        best_c = candidates[0]["couplings"].copy()
        best_label = candidates[0]["label"]
        best_optimized = False
        best_optimizer = None

        for start_item in candidates[:OPTIMIZE_PER_CLASS]:
            fixed = start_item["fixed_zero_edges"]
            optimized, value, optimizer_info = optimize_start(
                functional,
                start_item["couplings"],
                fixed,
                connected=(kind == "connected"),
            )
            optimization_records.append({
                "kind": kind,
                "start_index": start_item["index"],
                "start_label": start_item["label"],
                "score_before": start_item["score"],
                "score_after": float(value),
                "optimizer": optimizer_info,
            })
            if value > best_value:
                best_value = float(value)
                best_c = optimized
                best_label = start_item["label"]
                best_optimized = True
                best_optimizer = optimizer_info

        best_by_kind[kind] = record_candidate(
            best_c,
            best_value,
            target,
            best_label,
            best_optimized,
            best_optimizer,
        )

    overall_kind = max(
        best_by_kind,
        key=lambda kind: float(best_by_kind[kind]["score_float"]),
    )
    overall = best_by_kind[overall_kind]
    overall_score = float(overall["score_float"])
    escape = overall_score > target + ESCAPE_DISCOVERY_MARGIN

    result = {
        "status": (
            "floating_general_gapped_separator_escape_candidate"
            if escape
            else "no_escape_found_in_deterministic_multistart_search"
        ),
        "complete": True,
        "n": 21,
        "coupling_convention": (
            "A[j,j+1]=2*c[j], A[j+1,j]=-2*c[j], j=0,...,40; c[41]=0. "
            "The wrap edge is exactly cut. Internal zero couplings split the open path."
        ),
        "sign_gauge_reduction": (
            "It is sufficient to search c[0:41]>=0: on an open path, a diagonal "
            "sign conjugation recursively removes every coupling sign; all principal "
            "minors and second-moment coordinates are invariant under that conjugation."
        ),
        "proof_scope": (
            "Deterministic finite multistart and local-optimization discovery only. "
            "A score above the target is an escape candidate from the newly "
            "Arb-certified 6,141-column separator and must be independently "
            "verified with Arb. Failure to find one is not a global upper bound."
        ),
        "pins": pins,
        "seed_pool_sha256_le_f64": pool_hash,
        "random_seed": RANDOM_SEED,
        "pool_sample_count": len(pool_indices),
        "connected_random_count": CONNECTED_RANDOM_COUNT,
        "fractional_perturbation_count": CONNECTED_RANDOM_COUNT // 2,
        "multisegment_random_count": len(multisegment),
        "initial_candidates_evaluated": len(evaluated),
        "optimization": {
            "method": "L-BFGS-B with analytic Frechet gradient",
            "starts_per_class": OPTIMIZE_PER_CLASS,
            "max_iterations_per_start": MAX_ITER,
            "coupling_bounds": [1e-6, COUPLING_MAX],
            "multisegment_zero_edges_fixed": True,
            "records": optimization_records,
        },
        "gradient_self_test": gradient_check,
        "target_score_exact": str(exact_target),
        "target_score_float": format(target, ".17g"),
        "best_connected": best_by_kind["connected"],
        "best_multisegment": best_by_kind["multisegment"],
        "best_overall_kind": overall_kind,
        "best_overall_score": format(overall_score, ".17g"),
        "best_overall_gap": format(target - overall_score, ".17g"),
        "escape_discovery_margin": ESCAPE_DISCOVERY_MARGIN,
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "initial_candidates_evaluated": result["initial_candidates_evaluated"],
        "best_connected_score": best_by_kind["connected"]["score_float"],
        "best_connected_gap": best_by_kind["connected"]["target_minus_score_float"],
        "best_multisegment_score": best_by_kind["multisegment"]["score_float"],
        "best_multisegment_gap": best_by_kind["multisegment"]["target_minus_score_float"],
        "best_overall_kind": overall_kind,
        "best_overall_gap": result["best_overall_gap"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
