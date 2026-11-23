"""Differentiable discovery search for a continuous escape from the 186-column dual.

This is a discovery-only optimizer over positive path magnitudes. Any candidate
is rounded to an exact decimal-rational input and must pass the independent
128-bit Arb verifier before it is called a continuous-family counterexample.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm, expm_frechet
from scipy.optimize import minimize

from audit_complete_sixth_moments import ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit

CERT_PATH = ROOT / "evidence/55probe_186col_third_continuous_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_186col_third_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
ESCAPE_PATH = ROOT / "evidence/185col_continuous_dual_escape_arb_n21.json"
SEED_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
SEED_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
PRECISION_DIGITS = 12
LOW_COUNT = 1461
SIXTH_SCALE = 5.0 / 19721.0
EIGHTH_SCALE = 1.0 / 19721.0


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def cofactor_matrix(matrix, determinant=None):
    determinant = float(np.linalg.det(matrix)) if determinant is None else determinant
    n = matrix.shape[0]
    try:
        inverse = np.linalg.inv(matrix)
        # Near-singular principal blocks occur close to signed-permutation
        # regimes.  det(M) M^{-T} is algebraically the cofactor matrix, but
        # forming it through an ill-conditioned inverse can lose digits.
        if np.linalg.norm(inverse, ord=np.inf) < 1e8:
            return determinant * inverse.T
    except np.linalg.LinAlgError:
        pass
    result = np.empty_like(matrix)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            result[i, j] = (-1.0 if (i + j) % 2 else 1.0) * np.linalg.det(minor)
    return result


def add_minor_group(rotation, gradient_matrix, subsets, coefficient):
    total = 0.0
    factor = coefficient / len(subsets)
    for subset in subsets:
        idx = np.asarray(subset, dtype=int)
        block = rotation[np.ix_(idx, idx)]
        determinant = float(np.linalg.det(block))
        total += determinant
        gradient_matrix[np.ix_(idx, idx)] += factor * cofactor_matrix(block, determinant)
    return total / len(subsets)


def complex_step_derivative(pricing, couplings, coordinate, step=1e-20):
    c = np.asarray(couplings, dtype=np.complex128).copy()
    c[coordinate] += 1j * step
    generator = np.zeros((42, 42), dtype=np.complex128)
    for j, value in enumerate(c):
        generator[j, j + 1] = 2.0 * value
        generator[j + 1, j] = -2.0 * value
    rotation = expm(generator)
    score = complex(pricing.lam)
    for row in pricing.active:
        if row < LOW_COUNT:
            subsets = pricing.second_groups[int(row)] if row < 21 else pricing.fourth_groups[int(row - 21)]
        elif row < 2106:
            subsets = pricing.sixth_groups[int(row)]
        else:
            subsets = pricing.eighth_groups[int(row)]
        total = 0.0j
        for subset in subsets:
            idx = np.asarray(subset, dtype=int)
            total += np.linalg.det(rotation[np.ix_(idx, idx)])
        score += pricing.coefficients[int(row)] * total / len(subsets)
    return float(score.imag / step)


class DualPricing:
    def __init__(self):
        cert_raw = CERT_PATH.read_bytes()
        lp_raw = LP_PATH.read_bytes()
        cut_raw = CUT_LP_PATH.read_bytes()
        self.cert = json.loads(cert_raw)
        self.lp = json.loads(lp_raw)
        self.cut = json.loads(cut_raw)
        self.cert_sha = sha(cert_raw)
        self.lp_sha = sha(lp_raw)
        self.cut_sha = sha(cut_raw)
        if self.cert.get("status") != "strict_186col_2113row_third_continuous_escape_minimax_obstruction" or not self.cert.get("complete"):
            raise RuntimeError("the 186-column parent dual is not strictly certified")
        if self.cert.get("lp_transcript_sha256") != self.lp_sha:
            raise RuntimeError("186-column certificate/LP hash mismatch")
        if self.lp.get("cut_lp_transcript_sha256") != self.cut_sha:
            raise RuntimeError("186-column LP does not pin the 2,113-row cut inventory")
        self.z = np.asarray([float(Fraction(x)) for x in self.cert["dual_vector_rational"]])
        if self.z.shape != (2113,):
            raise RuntimeError("unexpected dual vector dimension")
        self.lam = float(Fraction(self.cert["dual_lambda_exact"]) - Fraction(self.cert["dual_slack_delta"]))
        self.active = np.flatnonzero(self.z)
        if len(self.active) != 54:
            raise RuntimeError("unexpected 186-column active dual support")

        system = FourthMoments(21)
        system.exact_target_check()
        self.low_scales = np.asarray(
            [1.0 / 41.0] * 21
            + [float(Fraction(210) * Fraction(1, 111930))] * len(system.keys),
            dtype=float,
        )
        # The exact fourth-order scale is C(21,2)/C(42,4) = 210/111930.
        if len(self.low_scales) != LOW_COUNT:
            raise RuntimeError("unexpected complete low-row count")
        self.fourth_groups = {
            row - 21: [tuple(int(v) for v in subset) for subset in system.indices[system.ids == row - 21]]
            for row in self.active if 21 <= row < LOW_COUNT
        }
        self.second_groups = {
            row: [tuple(sorted((i, (i + row + 1) % 42))) for i in range(42)]
            for row in self.active if row < 21
        }
        self.sixth_rows = [tuple(int(v) for v in row) for row in self.cut["sixth_cut_rows"]]
        self.eighth_rows = [tuple(int(v) for v in row) for row in self.cut["selected_eighth_rows"]]
        if len(self.sixth_rows) != 645 or len(self.eighth_rows) != 7:
            raise RuntimeError("unexpected mixed-order row inventory")
        self.sixth_groups = {row: orbit(self.sixth_rows[row - LOW_COUNT], 42) for row in self.active if LOW_COUNT <= row < 2106}
        self.eighth_groups = {row: orbit(self.eighth_rows[row - 2106], 42) for row in self.active if row >= 2106}
        self.coefficients = {}
        for row in self.active:
            if row < LOW_COUNT:
                scale = self.low_scales[row]
            elif row < 2106:
                scale = SIXTH_SCALE
            else:
                scale = EIGHTH_SCALE
            self.coefficients[row] = self.z[row] / scale

    def value_gradient(self, couplings, need_gradient=True):
        c = np.asarray(couplings, dtype=float)
        if c.shape != (41,) or np.any(c <= 0) or not np.all(np.isfinite(c)):
            raise ValueError("expected 41 finite strictly-positive edge magnitudes")
        generator = np.zeros((42, 42), dtype=float)
        for j, value in enumerate(c):
            generator[j, j + 1] = 2.0 * value
            generator[j + 1, j] = -2.0 * value
        rotation = expm(generator)
        gradient_matrix = np.zeros_like(rotation)
        score = self.lam

        for row in self.active:
            coefficient = self.coefficients[int(row)]
            if row < LOW_COUNT:
                subsets = self.second_groups[int(row)] if row < 21 else self.fourth_groups[int(row - 21)]
            elif row < 2106:
                subsets = self.sixth_groups[int(row)]
            else:
                subsets = self.eighth_groups[int(row)]
            feature = add_minor_group(rotation, gradient_matrix, subsets, coefficient)
            score += coefficient * feature

        if not need_gradient:
            return float(score)
        adjoint = expm_frechet(generator.T, gradient_matrix, compute_expm=False)
        gradient = 2.0 * (adjoint[np.arange(41), np.arange(1, 42)] - adjoint[np.arange(1, 42), np.arange(41)])
        return float(score), gradient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--maxiter", type=int, default=100)
    args = parser.parse_args()

    pricing = DualPricing()
    escape = json.loads(ESCAPE_PATH.read_text())
    if escape.get("status") != "certified_continuous_path_dual_escape" or not escape.get("strictly_positive"):
        raise RuntimeError("the third exact continuous path seed is not Arb-certified")
    old = np.asarray([float(Fraction(x)) for x in escape["candidate_couplings_exact"][:-1]])
    if old.shape != (41,) or np.any(old <= 0):
        raise RuntimeError("invalid prior continuous path starting point")
    prior_score = pricing.value_gradient(old, False)
    prior_interval = next(item["interval"] for item in pricing.cert["column_dual_lhs_intervals"] if int(item["column"]) == 1643)
    prior_midpoint = float(prior_interval.split("[", 1)[1].split(" +/-", 1)[0])
    if abs(prior_score - prior_midpoint) > 1e-8:
        raise RuntimeError(
            f"pricing-value regression against Arb-certified third escape column 1643 failed: "
            f"computed={prior_score}, certified-midpoint={prior_midpoint}"
        )

    rng = np.random.default_rng(202611231511)
    starts = [old]
    for sigma in (0.08, 0.2, 0.45):
        starts.append(old * np.exp(rng.normal(0.0, sigma, size=41)))
    seed_raw = SEED_PATH.read_bytes()
    seed = np.load(SEED_PATH, allow_pickle=False)
    seed_sha = sha(np.asarray(seed, dtype="<f8").tobytes())
    if seed.shape != (1600, 42) or seed_sha != SEED_SHA256:
        raise RuntimeError("frozen seed pool hash/shape mismatch")
    for index in (159, 559, 959, 1359):
        starts.append(np.clip(np.abs(seed[index, :41]), 1e-4, 100.0))
    for _ in range(2):
        starts.append(np.exp(rng.uniform(np.log(1e-3), np.log(100.0), size=41)))

    # Validate the analytic Frechet/cofactor gradient at the first interior point.
    _, analytic = pricing.value_gradient(old)
    checks = []
    for j in (0, 20, 40):
        complex_step = complex_step_derivative(pricing, old, j)
        step = 1e-6 * max(1.0, old[j])
        plus, minus = old.copy(), old.copy()
        plus[j] += step
        minus[j] -= step
        central = (pricing.value_gradient(plus, False) - pricing.value_gradient(minus, False)) / (2.0 * step)
        absolute = abs(complex_step - analytic[j])
        relative = absolute / max(1.0, abs(complex_step), abs(analytic[j]))
        checks.append({"coordinate": j, "analytic": float(analytic[j]), "complex_step": float(complex_step),
                       "central_difference": float(central), "absolute_defect": float(absolute),
                       "relative_defect": float(relative)})
    gradient_defect = max(item["relative_defect"] for item in checks)
    if gradient_defect > 2e-6:
        raise RuntimeError(f"Frechet/cofactor complex-step gradient check failed: {checks}")

    lower, upper = np.log(1e-4), np.log(100.0)
    records = []
    best = None
    for start_index, start in enumerate(starts):
        x0 = np.log(np.clip(start, 1e-4, 100.0))

        def objective(log_c):
            value, grad_c = pricing.value_gradient(np.exp(log_c))
            return -value, -(grad_c * np.exp(log_c))

        initial_score = pricing.value_gradient(np.exp(x0), False)
        result = minimize(
            objective,
            x0,
            jac=True,
            method="L-BFGS-B",
            bounds=[(lower, upper)] * 41,
            options={"maxiter": args.maxiter, "ftol": 1e-13, "gtol": 1e-8, "maxls": 30},
        )
        optimized = np.exp(result.x)
        exact_strings = [format(float(value), f".{PRECISION_DIGITS}f") for value in optimized] + ["0"]
        rounded = np.asarray([float(x) for x in exact_strings[:-1]])
        rounded_score = pricing.value_gradient(rounded, False)
        record = {
            "start_index": start_index,
            "initial_score": float(initial_score),
            "optimized_score_binary64": float(-result.fun),
            "rounded_score_binary64": float(rounded_score),
            "iterations": int(result.nit),
            "success": bool(result.success),
            "message": str(result.message),
            "gradient_norm_log_coordinates": float(np.linalg.norm(result.jac, ord=np.inf)),
            "candidate_couplings_exact": exact_strings,
        }
        records.append(record)
        if best is None or record["rounded_score_binary64"] > best["rounded_score_binary64"]:
            best = record
        print(json.dumps({"start": start_index, "initial": initial_score, "rounded": rounded_score, "nit": result.nit}), flush=True)

    found = bool(best and best["rounded_score_binary64"] > 1e-8)
    result = {
        "status": "positive_continuous_escape_candidate_found" if found else "no_positive_candidate_in_local_search",
        "complete": True,
        "discovery_only": True,
        "dual_certificate_sha256": pricing.cert_sha,
        "lp_transcript_sha256": pricing.lp_sha,
        "cut_lp_transcript_sha256": pricing.cut_sha,
        "prior_escape_certificate_sha256": sha(ESCAPE_PATH.read_bytes()),
        "seed_pool_sha256_le_f64": seed_sha,
        "seed_pool_file_sha256": sha(seed_raw),
        "precision_digits_exact_decimal_input": PRECISION_DIGITS,
        "gradient_method": "cofactor determinant derivative plus adjoint Frechet derivative of exp",
        "gradient_check_coordinates": [0, 20, 40],
        "gradient_check_max_relative_defect": gradient_defect,
        "gradient_checks": checks,
        "search_domain": "1e-4 <= c_j <= 100 for all 41 open-path edge magnitudes; c_41=0",
        "starts": len(starts),
        "max_iterations_per_start": args.maxiter,
        "best_candidate_couplings_exact": best["candidate_couplings_exact"] if best else None,
        "best_candidate_score_binary64": best["rounded_score_binary64"] if best else None,
        "prior_third_escape_score_binary64": prior_score,
        "prior_third_escape_arb_interval": prior_interval,
        "candidate_found": found,
        "records": records,
        "scope": "A positive binary64 score is discovery only; a continuous-family escape is claimed only after the independent exact-rational 128-bit Arb verifier proves a strictly positive interval lower endpoint. Failure to find one is not a global separation proof.",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    result["output"] = str(output)
    print(json.dumps({k: result[k] for k in ("status", "best_candidate_score_binary64", "candidate_found", "gradient_check_max_relative_defect", "output")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
