"""Discovery pricing of the exact 204-column dual on the uniform-path 21-torus.

A positive floating score is discovery only. The companion Arb verifier must
certify the exact decimal phase vector before any continuous-family escape is
claimed.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit

ROOT = Path(__file__).resolve().parent
CERT_PATH = ROOT / "evidence/55probe_204col_uniform_ray_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_204col_uniform_ray_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
PARENT_SEARCH_PATH = ROOT / "evidence/203col_uniform_torus_search_n21.json"
OUTPUT_DEFAULT = ROOT / "evidence/204col_uniform_torus_search_n21.json"

LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = 5.0 / 19721.0
EIGHTH_SCALE = 1.0 / 19721.0
SEARCH_SEED = 202611260040


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def cofactor_matrix(matrix, determinant=None):
    determinant = float(np.linalg.det(matrix)) if determinant is None else determinant
    try:
        inverse = np.linalg.inv(matrix)
        if np.linalg.norm(inverse, ord=np.inf) < 1e8:
            return determinant * inverse.T
    except np.linalg.LinAlgError:
        pass
    n = matrix.shape[0]
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


def uniform_path_basis():
    q = np.zeros((42, 42), dtype=float)
    frequencies = np.empty(21, dtype=float)
    for k in range(1, 22):
        frequencies[k - 1] = 4.0 * np.cos(k * np.pi / 43.0)
        for j in range(42):
            sine = np.sin((j + 1) * k * np.pi / 43.0)
            q[j, 2 * k - 2] = np.sqrt(4.0 / 43.0) * sine * np.cos(j * np.pi / 2.0)
            q[j, 2 * k - 1] = np.sqrt(4.0 / 43.0) * sine * np.sin(j * np.pi / 2.0)
    return q, frequencies


def block_rotation(theta):
    dtype = np.complex128 if np.iscomplexobj(theta) else np.float64
    block = np.zeros((42, 42), dtype=dtype)
    for k, angle in enumerate(theta):
        c, s = np.cos(angle), np.sin(angle)
        block[2 * k, 2 * k] = c
        block[2 * k, 2 * k + 1] = s
        block[2 * k + 1, 2 * k] = -s
        block[2 * k + 1, 2 * k + 1] = c
    return block


class DualPricing:
    def __init__(self):
        cert_raw = CERT_PATH.read_bytes()
        lp_raw = LP_PATH.read_bytes()
        cut_raw = CUT_LP_PATH.read_bytes()
        parent_raw = PARENT_SEARCH_PATH.read_bytes()
        self.cert = json.loads(cert_raw)
        self.lp = json.loads(lp_raw)
        self.cut = json.loads(cut_raw)
        self.parent_search = json.loads(parent_raw)
        self.cert_sha = sha(cert_raw)
        self.lp_sha = sha(lp_raw)
        self.cut_sha = sha(cut_raw)
        self.parent_search_sha = sha(parent_raw)

        if self.cert.get("status") != "strict_204col_2113row_uniform_ray_escape_minimax_obstruction" or not self.cert.get("complete"):
            raise RuntimeError("the exact 204-column dual is not Arb-certified")
        if (self.cert.get("column_count"), self.cert.get("row_count")) != (204, 2113):
            raise RuntimeError("unexpected 204-column certificate dimensions")
        if self.cert.get("lp_transcript_sha256") != self.lp_sha:
            raise RuntimeError("204-column certificate/LP hash mismatch")
        if self.cert.get("cut_lp_transcript_sha256") != self.cut_sha or self.lp.get("cut_lp_transcript_sha256") != self.cut_sha:
            raise RuntimeError("204-column evidence does not pin the exact cut design")
        if self.lp.get("status") != "204col_uniform_ray_escape_lp_above_one_third":
            raise RuntimeError("204-column LP is not the expected above-cap discovery")
        if (self.lp.get("columns"), self.lp.get("rows")) != (203, 2113):
            raise RuntimeError("unexpected 204-column LP dimensions")
        if self.parent_search.get("status") != "positive_uniform_torus_candidate_found" or not self.parent_search.get("candidate_found"):
            raise RuntimeError("204-column warm-start torus search is not positive")
        if self.parent_search.get("dual_certificate_sha256") != self.cert.get("parent_203col_dual_certificate_sha256"):
            raise RuntimeError("204-column warm start does not pin the parent dual")
        if self.parent_search.get("lp_transcript_sha256") != self.cert.get("parent_203col_lp_sha256"):
            raise RuntimeError("204-column warm start does not pin the parent LP")
        self.parent_phases = self.parent_search["best_candidate_phases_exact_decimal"]
        if len(self.parent_phases) != 21:
            raise RuntimeError("204-column warm start has the wrong phase dimension")

        zq = [Fraction(value) for value in self.cert["dual_vector_rational"]]
        norm = sum((abs(value) for value in zq), Fraction(0))
        if len(zq) != 2113 or norm != Fraction(self.cert["dual_l1_norm_exact"]) or norm > 1:
            raise RuntimeError("exact 204-column dual dimension/L1 normalization mismatch")
        self.z = np.asarray([float(value) for value in zq], dtype=float)
        self.lam = float(Fraction(self.cert["dual_lambda_exact"]) - Fraction(self.cert["dual_slack_delta"]))
        self.active = np.flatnonzero(self.z)
        active_blocks = (
            sum(row < LOW_COUNT for row in self.active),
            sum(LOW_COUNT <= row < SIXTH_END for row in self.active),
            sum(row >= SIXTH_END for row in self.active),
        )
        if len(self.active) != 71 or active_blocks != (4, 64, 3):
            raise RuntimeError(f"unexpected 204-column active dual support: {active_blocks}")
        if self.cert.get("active_dual_rows") != {"total": 71, "low": 4, "sixth": 64, "eighth": 3}:
            raise RuntimeError("204-column certificate active-row metadata mismatch")

        system = FourthMoments(21)
        system.exact_target_check()
        self.low_scales = np.asarray(
            [1.0 / 41.0] * 21
            + [float(Fraction(210, 111930))] * len(system.keys),
            dtype=float,
        )
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
        self.sixth_groups = {
            row: orbit(self.sixth_rows[row - LOW_COUNT], 42)
            for row in self.active if LOW_COUNT <= row < SIXTH_END
        }
        self.eighth_groups = {
            row: orbit(self.eighth_rows[row - SIXTH_END], 42)
            for row in self.active if row >= SIXTH_END
        }
        self.coefficients = {}
        for row in self.active:
            if row < LOW_COUNT:
                scale = self.low_scales[row]
            elif row < SIXTH_END:
                scale = SIXTH_SCALE
            else:
                scale = EIGHTH_SCALE
            self.coefficients[int(row)] = self.z[row] / scale
        self.q, self.frequencies = uniform_path_basis()
        self.qt = self.q.T
        self._regression_checks()

    def rotation(self, theta):
        return self.q @ block_rotation(theta) @ self.qt

    def feature_groups(self, row):
        if row < 21:
            return self.second_groups[int(row)]
        if row < LOW_COUNT:
            return self.fourth_groups[int(row - 21)]
        if row < SIXTH_END:
            return self.sixth_groups[int(row)]
        return self.eighth_groups[int(row)]

    def value_from_rotation(self, rotation):
        score = complex(self.lam) if np.iscomplexobj(rotation) else self.lam
        for row in self.active:
            subsets = self.feature_groups(int(row))
            total = 0.0j if np.iscomplexobj(rotation) else 0.0
            for subset in subsets:
                idx = np.asarray(subset, dtype=int)
                total += np.linalg.det(rotation[np.ix_(idx, idx)])
            score += self.coefficients[int(row)] * total / len(subsets)
        return score

    def value_only(self, theta):
        return self.value_from_rotation(self.rotation(theta))

    def value_gradient(self, theta):
        theta = np.asarray(theta, dtype=float)
        if theta.shape != (21,) or not np.all(np.isfinite(theta)):
            raise ValueError("expected 21 finite torus phases")
        rotation = self.rotation(theta)
        gradient_matrix = np.zeros((42, 42), dtype=float)
        score = self.lam
        for row in self.active:
            coefficient = self.coefficients[int(row)]
            feature = add_minor_group(rotation, gradient_matrix, self.feature_groups(int(row)), coefficient)
            score += coefficient * feature
        gradient = np.empty(21, dtype=float)
        for k, angle in enumerate(theta):
            c, s = np.cos(angle), np.sin(angle)
            derivative_block = np.zeros((42, 42), dtype=float)
            derivative_block[2 * k, 2 * k] = -s
            derivative_block[2 * k, 2 * k + 1] = c
            derivative_block[2 * k + 1, 2 * k] = -c
            derivative_block[2 * k + 1, 2 * k + 1] = -s
            derivative_rotation = self.q @ derivative_block @ self.qt
            gradient[k] = float(np.sum(gradient_matrix * derivative_rotation))
        return float(score), gradient

    def complex_step_derivative(self, theta, coordinate, step=1e-20):
        phases = np.asarray(theta, dtype=np.complex128).copy()
        phases[coordinate] += 1j * step
        return float(np.imag(self.value_only(phases)) / step)

    def _regression_checks(self):
        q_defect = float(np.max(np.abs(self.qt @ self.q - np.eye(42))))
        generator = np.zeros((42, 42), dtype=float)
        for j in range(41):
            generator[j, j + 1] = 2.0
            generator[j + 1, j] = -2.0
        canonical = np.zeros((42, 42), dtype=float)
        for k, omega in enumerate(self.frequencies):
            canonical[2 * k, 2 * k + 1] = omega
            canonical[2 * k + 1, 2 * k] = -omega
        t = 0.731
        theta = t * self.frequencies
        rotation_defect = float(np.max(np.abs(self.rotation(theta) - expm(t * generator))))
        if max(q_defect, float(np.max(np.abs(self.qt @ generator @ self.q - canonical))), rotation_defect) > 2e-10:
            raise RuntimeError("uniform-torus spectral basis regression failed")
        self.regression = {
            "orthogonality_max_abs": q_defect,
            "canonical_form_max_abs": float(np.max(np.abs(self.qt @ generator @ self.q - canonical))),
            "uniform_ray_rotation_max_abs": rotation_defect,
            "test_time": t,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT_DEFAULT))
    parser.add_argument("--maxiter", type=int, default=120)
    parser.add_argument("--starts", type=int, default=8)
    args = parser.parse_args()
    pricing = DualPricing()
    theta0 = 1.35 * np.sin(0.37 * np.arange(21)) + 0.82 * np.cos(0.23 * np.arange(21))
    _, analytic = pricing.value_gradient(theta0)
    checks = []
    for coordinate in (0, 10, 20):
        complex_step = pricing.complex_step_derivative(theta0, coordinate)
        step = 1e-6
        plus, minus = theta0.copy(), theta0.copy()
        plus[coordinate] += step
        minus[coordinate] -= step
        central = float(np.real((pricing.value_only(plus) - pricing.value_only(minus)) / (2.0 * step)))
        absolute = abs(complex_step - analytic[coordinate])
        relative = absolute / max(1.0, abs(complex_step), abs(analytic[coordinate]))
        central_absolute = abs(central - analytic[coordinate])
        central_relative = central_absolute / max(1.0, abs(central), abs(analytic[coordinate]))
        checks.append({
            "coordinate": coordinate,
            "analytic": float(analytic[coordinate]),
            "complex_step": float(complex_step),
            "central_difference": central,
            "relative_defect": float(relative),
            "central_relative_defect": float(central_relative),
        })
    gradient_defect = max(max(x["relative_defect"], x["central_relative_defect"]) for x in checks)
    if gradient_defect > 2e-5:
        raise RuntimeError(f"analytic torus pricing gradient failed: {checks}")

    rng = np.random.default_rng(SEARCH_SEED)
    starts = [
        np.zeros(21),
        np.full(21, np.pi / 2.0),
        np.asarray([float(value) for value in pricing.parent_phases], dtype=float),
    ]
    starts.extend(rng.uniform(-np.pi, np.pi, size=21) for _ in range(max(0, args.starts - len(starts))))
    records = []
    best = None
    for index, start in enumerate(starts):
        initial = float(np.real(pricing.value_only(start)))
        result = minimize(
            lambda phases: (-pricing.value_gradient(phases)[0], -pricing.value_gradient(phases)[1]),
            start,
            jac=True,
            method="L-BFGS-B",
            bounds=[(-np.pi, np.pi)] * 21,
            options={"maxiter": args.maxiter, "ftol": 1e-13, "gtol": 1e-8, "maxls": 40},
        )
        phases = [format(float(value), ".12f") for value in result.x]
        rounded = np.asarray([float(value) for value in phases], dtype=float)
        rounded_score = float(np.real(pricing.value_only(rounded)))
        record = {
            "start_index": index,
            "initial_score_binary64": initial,
            "optimized_score_binary64": float(-result.fun),
            "rounded_score_binary64": rounded_score,
            "iterations": int(result.nit),
            "success": bool(result.success),
            "message": str(result.message),
            "gradient_norm_inf": float(np.linalg.norm(result.jac, ord=np.inf)),
            "phases_exact_decimal": phases,
        }
        records.append(record)
        if best is None or rounded_score > best["rounded_score_binary64"]:
            best = record
        print(json.dumps({"start": index, "initial": initial, "rounded": rounded_score, "iterations": int(result.nit), "success": bool(result.success)}), flush=True)

    candidate_found = bool(best and best["rounded_score_binary64"] > 1e-8)
    output = {
        "status": "positive_uniform_torus_candidate_found" if candidate_found else "no_positive_candidate_in_local_search",
        "complete": True,
        "discovery_only": True,
        "dual_certificate_sha256": pricing.cert_sha,
        "lp_transcript_sha256": pricing.lp_sha,
        "cut_lp_transcript_sha256": pricing.cut_sha,
        "parent_203col_torus_search_sha256": pricing.parent_search_sha,
        "parameterization": "R(theta)=Q (direct_sum_k [[cos(theta_k),sin(theta_k)],[-sin(theta_k),cos(theta_k)]]) Q^T",
        "phase_dimension": 21,
        "phase_domain": "[-pi,pi]^21 with periodic identification",
        "gradient_method": "cofactor determinant derivative contracted with dR/dtheta_k",
        "gradient_checks": checks,
        "gradient_check_max_relative_defect": gradient_defect,
        "regression_checks": pricing.regression,
        "starts": len(starts),
        "starts_requested": args.starts,
        "random_seed": SEARCH_SEED,
        "numpy_version": np.__version__,
        "scipy_version": __import__("scipy").__version__,
        "optimizer": "L-BFGS-B",
        "phase_rounding_decimals": 12,
        "max_iterations_per_start": args.maxiter,
        "best_candidate_phases_exact_decimal": best["phases_exact_decimal"] if best else None,
        "best_candidate_score_binary64": best["rounded_score_binary64"] if best else None,
        "candidate_found": candidate_found,
        "records": records,
        "scope": (
            "A positive binary64 score is discovery only. A continuous uniform-ray escape is claimed "
            "only after the independent exact-decimal 128-bit Arb verifier certifies a strictly positive "
            "torus pricing interval. Failure of this finite multi-start search is not a global separation proof."
        ),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "best_candidate_score_binary64": output["best_candidate_score_binary64"], "candidate_found": candidate_found, "output": str(output_path)}, indent=2), flush=True)


if __name__ == "__main__":
    main()
