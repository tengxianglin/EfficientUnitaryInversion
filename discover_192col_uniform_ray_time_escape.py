"""Search for an explicit finite uniform coupling t>0 escaping the 192-column dual."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from audit_complete_sixth_moments import ROOT
from discover_192col_uniform_torus_pricing import DualPricing

OUTPUT_DEFAULT = ROOT / "evidence/192col_uniform_ray_time_search_n21.json"
RANGES = ((1e-3, 1e3), (1e3, 1e4), (1e4, 1e5))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT_DEFAULT))
    parser.add_argument("--maxiter", type=int, default=120)
    parser.add_argument("--popsize", type=int, default=20)
    args = parser.parse_args()

    pricing = DualPricing()
    omega = pricing.frequencies

    def score_at(t):
        return float(np.real(pricing.value_only(float(t) * omega)))

    records = []
    best = None
    for index, bounds in enumerate(RANGES):
        seed = 2026112424 + index
        result = differential_evolution(
            lambda x: -score_at(x[0]),
            [bounds],
            strategy="best1bin",
            maxiter=args.maxiter,
            popsize=args.popsize,
            tol=1e-9,
            atol=1e-10,
            mutation=(0.5, 1.0),
            recombination=0.7,
            seed=seed,
            polish=True,
            updating="immediate",
            workers=1,
        )
        t_decimal = format(float(result.x[0]), ".15f")
        t_rounded = float(t_decimal)
        rounded_score = score_at(t_rounded)
        record = {
            "range_index": index,
            "bounds": [float(bounds[0]), float(bounds[1])],
            "seed": seed,
            "iterations": int(result.nit),
            "function_evaluations": int(result.nfev),
            "optimizer_success": bool(result.success),
            "optimizer_message": str(result.message),
            "t_exact_decimal": t_decimal,
            "score_at_optimizer_t_binary64": float(-result.fun),
            "score_at_rounded_t_binary64": rounded_score,
        }
        records.append(record)
        if best is None or record["score_at_rounded_t_binary64"] > best["score_at_rounded_t_binary64"]:
            best = record
        print(json.dumps({
            "range": index,
            "t": t_decimal,
            "score": rounded_score,
            "nfev": int(result.nfev),
            "success": bool(result.success),
        }), flush=True)

    candidate_found = bool(best and best["t_exact_decimal"] and best["score_at_rounded_t_binary64"] > 1e-8)
    output = {
        "status": "positive_finite_uniform_ray_candidate_found" if candidate_found else "no_positive_finite_uniform_ray_candidate_found",
        "complete": True,
        "discovery_only": True,
        "dual_certificate_sha256": pricing.cert_sha,
        "lp_transcript_sha256": pricing.lp_sha,
        "cut_lp_transcript_sha256": pricing.cut_sha,
        "uniform_path": "c_j=t for all 41 edges, t>0",
        "frequency_formula": "omega_k=4*cos(k*pi/43), k=1,...,21",
        "search_ranges": [list(bounds) for bounds in RANGES],
        "max_iterations_per_range": args.maxiter,
        "population_size": args.popsize,
        "best_t_exact_decimal": best["t_exact_decimal"] if best else None,
        "best_score_binary64": best["score_at_rounded_t_binary64"] if best else None,
        "candidate_found": candidate_found,
        "records": records,
        "scope": (
            "A positive binary64 score is only a candidate. The explicit finite-time physical escape "
            "is established only if the independent Arb verifier certifies the exact decimal t>0. "
            "Failure of these bounded one-dimensional searches does not contradict the nonconstructive "
            "dense-torus existence theorem."
        ),
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "status": output["status"],
        "best_t_exact_decimal": output["best_t_exact_decimal"],
        "best_score_binary64": output["best_score_binary64"],
        "candidate_found": candidate_found,
        "output": str(path),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
