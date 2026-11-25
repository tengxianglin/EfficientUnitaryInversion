"""Deterministic one-dimensional search for an explicit time escaping the 201-column dual."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from discover_201col_uniform_torus_pricing import DualPricing

ROOT = Path(__file__).resolve().parent
TORUS_CERT_PATH = ROOT / "evidence/201col_uniform_torus_arb_n21.json"
OUTPUT_DEFAULT = ROOT / "evidence/201col_uniform_ray_time_search_n21.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT_DEFAULT))
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--maxiter", type=int, default=400)
    args = parser.parse_args()

    pricing = DualPricing()
    torus_raw = TORUS_CERT_PATH.read_bytes()
    torus = json.loads(torus_raw)
    torus_sha = sha(torus_raw)
    if torus.get("status") != "certified_positive_uniform_torus_escape" or not torus.get("complete") or not torus.get("strict_uniform_ray_escape_certified"):
        raise RuntimeError("201-column torus point is not independently Arb-certified")
    if torus.get("dual_certificate_sha256") != pricing.cert_sha or torus.get("lp_transcript_sha256") != pricing.lp_sha:
        raise RuntimeError("201-column torus certificate does not pin the current dual/LP")
    if torus.get("cut_lp_transcript_sha256") != pricing.cut_sha:
        raise RuntimeError("201-column torus certificate does not pin the exact cut design")

    omega = pricing.frequencies

    def score_gradient_at(t):
        phases = np.remainder(float(t) * omega + np.pi, 2.0 * np.pi) - np.pi
        value, gradient = pricing.value_gradient(phases)
        return value, float(np.dot(gradient, omega))

    rng = np.random.default_rng(202611251837)
    starts = rng.uniform(0.0, 1.0e8, size=args.starts)
    records = []
    best = None
    for index, start in enumerate(starts):
        initial_score, initial_derivative = score_gradient_at(start)
        result = minimize(
            lambda x: (
                -score_gradient_at(float(x[0]))[0],
                np.asarray([-score_gradient_at(float(x[0]))[1]], dtype=float),
            ),
            np.asarray([start], dtype=float),
            jac=True,
            method="L-BFGS-B",
            bounds=[(1e-9, 1e8)],
            options={"maxiter": args.maxiter, "ftol": 1e-14, "gtol": 1e-9, "maxls": 50},
        )
        t_string = format(float(result.x[0]), ".15f")
        t_rounded = float(t_string)
        rounded_score, derivative = score_gradient_at(t_rounded)
        record = {
            "start_index": index,
            "initial_t_binary64": float(start),
            "initial_score_binary64": float(initial_score),
            "initial_derivative_binary64": float(initial_derivative),
            "t_exact_decimal": t_string,
            "score_at_rounded_t_binary64": float(rounded_score),
            "derivative_at_rounded_t_binary64": float(derivative),
            "iterations": int(result.nit),
            "optimizer_success": bool(result.success),
            "optimizer_message": str(result.message),
        }
        records.append(record)
        if best is None or rounded_score > best["score_at_rounded_t_binary64"]:
            best = record
        print(json.dumps({
            "start": index,
            "t": t_string,
            "score": float(rounded_score),
            "iterations": int(result.nit),
            "success": bool(result.success),
        }), flush=True)

    candidate_found = bool(best and best["score_at_rounded_t_binary64"] > 1e-8)
    output = {
        "status": "positive_finite_uniform_ray_candidate_found" if candidate_found else "no_positive_finite_uniform_ray_candidate_found",
        "complete": True,
        "discovery_only": True,
        "dual_certificate_sha256": pricing.cert_sha,
        "lp_transcript_sha256": pricing.lp_sha,
        "cut_lp_transcript_sha256": pricing.cut_sha,
        "torus_arb_certificate_sha256": torus_sha,
        "torus_phase_vector_sha256": torus.get("phase_vector_sha256"),
        "torus_pricing_interval": torus.get("pricing_interval"),
        "uniform_path": "c_j=t for j=0,...,40, closing edge c_41=0, t>0",
        "frequency_formula": "omega_k=4*cos(k*pi/43), k=1,...,21",
        "search_domain": "[1e-9, 1e8]",
        "starts": args.starts,
        "max_iterations_per_start": args.maxiter,
        "seed": 202611251720,
        "best_t_exact_decimal": best["t_exact_decimal"] if best else None,
        "best_score_binary64": best["score_at_rounded_t_binary64"] if best else None,
        "candidate_found": candidate_found,
        "records": records,
        "scope": (
            "A positive binary64 score is discovery only. A finite physical escape is claimed only if "
            "the independent 128-bit Arb verifier certifies the exact decimal t>0 against the pinned "
            "201-column rational dual. Failure of this bounded one-dimensional search does not undo "
            "the independently certified positive torus point and dense-ray existence theorem."
        ),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "status": output["status"],
        "best_t_exact_decimal": output["best_t_exact_decimal"],
        "best_score_binary64": output["best_score_binary64"],
        "candidate_found": candidate_found,
        "output": str(output_path),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
