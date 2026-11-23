"""Discovery search for the 192-column dual on the exact uniform-path 21-torus.

The optimizer is discovery only. A positive candidate is promoted to a physical
uniform-ray escape only if the independent Arb verifier certifies its exact
decimal phase vector with a strictly positive interval.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

from audit_complete_sixth_moments import ROOT
from ising_fourth_moments import FourthMoments
from screen_ising_sixth_moments import orbit

CERT_PATH = ROOT / "evidence/55probe_192col_ninth_continuous_escape_dual_certificate_n21.json"
LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_192col_ninth_continuous_escape_n21.json"
CUT_LP_PATH = ROOT / "evidence/joint_low_six_eighth_lp_152col_full_sixth_cuts_n21.json"
SEED_POOL_PATH = ROOT / "evidence/seed_pool_n21_frozen.npy"
OUTPUT_DEFAULT = ROOT / "evidence/192col_uniform_torus_search_n21.json"
SEED_POOL_SHA256 = "93aa5acc6ac559b6b5f2dea3e780f86d47ddd2545e3972eead836d24b5054315"
PRECISION_DIGITS = 12
LOW_COUNT = 1461
SIXTH_END = 2106
SIXTH_SCALE = 5.0 / 19721.0
EIGHTH_SCALE = 1.0 / 19721.0
PI = np.pi


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
        seed_raw = SEED_POOL_PATH.read_bytes()
        self.cert = json.loads(cert_raw)
        self.lp = json.loads(lp_raw)
        self.cut = json.loads(cut_raw)
        self.cert_sha = sha(cert_raw)
        self.lp_sha = sha(lp_raw)
        self.cut_sha = sha(cut_raw)
        if self.cert.get("status") != "strict_192col_2113row_ninth_continuous_escape_minimax_obstruction" or not self.cert.get("complete"):
            raise RuntimeError("the 192-column dual is not strictly Arb-certified")
        if (self.cert.get("column_count"), self.cert.get("row_count")) != (192, 2113):
            raise RuntimeError("unexpected 192-column certificate dimensions")
        if self.cert.get("lp_transcript_sha256") != self.lp_sha:
            raise RuntimeError("192-column certificate/LP hash mismatch")
        if self.lp.get("status") != "192col_ninth_continuous_escape_lp_above_one_third":
            raise RuntimeError("192-column LP is not the expected above-cap discovery")
        if (self.lp.get("columns"), self.lp.get("rows")) != (192, 2113):
            raise RuntimeError("unexpected 192-column LP dimensions")
        if self.lp.get("cut_lp_transcript_sha256") != self.cut_sha or self.cert.get("cut_lp_transcript_sha256") != self.cut_sha:
            raise RuntimeError("192-column branch does not pin the exact 2,113-row cut design")
        seed = np.asarray(np.load(SEED_POOL_PATH, allow_pickle=False), dtype="<f8")
        seed_sha = sha(seed.tobytes())
        if seed.shape != (1600, 42) or seed_sha != SEED_POOL_SHA256:
            raise RuntimeError("frozen seed-pool hash/shape mismatch")
        if self.cert.get("seed_pool_sha256_le_f64") != seed_sha or self.lp.get("seed_pool_sha256_le_f64") != seed_sha:
            raise RuntimeError("192-column evidence does not pin the frozen seed pool")
        self.seed_file_sha = sha(seed_raw)
        self.seed_sha = seed_sha

        zq = [Fraction(value) for value in self.cert["dual_vector_rational"]]
        norm = sum((abs(value) for value in zq), Fraction(0))
        if len(zq) != 2113 or norm != Fraction(self.cert["dual_l1_norm_exact"]) or norm > 1:
            raise RuntimeError("exact 192-column dual dimension/L1 normalization mismatch")
        self.z = np.asarray([float(value) for value in zq], dtype=float)
        self.lam = float(Fraction(self.cert["dual_lambda_exact"]) - Fraction(self.cert["dual_slack_delta"]))
        self.active = np.flatnonzero(self.z)
        if len(self.active) != 61:
            raise RuntimeError("unexpected 192-column active dual support")

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
        canonical_defect = float(np.max(np.abs(self.qt @ generator @ self.q - canonical)))
        t = 0.731
        theta = t * self.frequencies
        torus_rotation = self.rotation(theta)
        direct_rotation = expm(t * generator)
        rotation_defect = float(np.max(np.abs(torus_rotation - direct_rotation)))
        pricing_defect = abs(float(np.real(self.value_only(theta))) - float(np.real(self.value_from_rotation(direct_rotation))))
        if max(q_defect, canonical_defect, rotation_defect, pricing_defect) > 2e-10:
            raise RuntimeError(
                "uniform-torus basis/pricing regression failed: "
                f"Q={q_defect}, canonical={canonical_defect}, R={rotation_defect}, pricing={pricing_defect}"
            )
        self.regression = {
            "orthogonality_max_abs": q_defect,
            "canonical_form_max_abs": canonical_defect,
            "uniform_ray_rotation_max_abs": rotation_defect,
            "uniform_ray_pricing_abs": pricing_defect,
            "test_time": t,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT_DEFAULT))
    parser.add_argument("--maxiter", type=int, default=120)
    parser.add_argument("--starts", type=int, default=12)
    args = parser.parse_args()

    pricing = DualPricing()
    index = np.arange(21, dtype=float)
    theta0 = 1.35 * np.sin(0.37 * index) + 0.82 * np.cos(0.23 * index)
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
            "absolute_defect": float(absolute),
            "relative_defect": float(relative),
            "central_absolute_defect": float(central_absolute),
            "central_relative_defect": float(central_relative),
        })
    gradient_defect = max(
        max(item["relative_defect"], item["central_relative_defect"]) for item in checks
    )
    if gradient_defect > 2e-5:
        raise RuntimeError(f"torus cofactor gradient failed generic-point complex-step/central regression: {checks}")

    rng = np.random.default_rng(2026112421)
    starts = [
        np.zeros(21),
        np.full(21, np.pi / 2.0),
        np.linspace(-np.pi, np.pi, 21, endpoint=False),
        np.linspace(np.pi, -np.pi, 21, endpoint=False),
    ]
    starts.extend(rng.uniform(-np.pi, np.pi, size=21) for _ in range(max(0, args.starts - len(starts))))
    records = []
    best = None
    bounds = [(-np.pi, np.pi)] * 21
    for index, start in enumerate(starts):
        initial = float(np.real(pricing.value_only(start)))

        def objective(phases):
            value, gradient = pricing.value_gradient(phases)
            return -value, -gradient

        result = minimize(
            objective,
            start,
            jac=True,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": args.maxiter, "ftol": 1e-13, "gtol": 1e-8, "maxls": 40},
        )
        optimized = np.asarray(result.x, dtype=float)
        exact_strings = [format(float(value), f".{PRECISION_DIGITS}f") for value in optimized]
        rounded = np.asarray([float(value) for value in exact_strings], dtype=float)
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
            "phases_exact_decimal": exact_strings,
        }
        records.append(record)
        if best is None or record["rounded_score_binary64"] > best["rounded_score_binary64"]:
            best = record
        print(json.dumps({
            "start": index,
            "initial": initial,
            "rounded": rounded_score,
            "iterations": int(result.nit),
            "success": bool(result.success),
        }), flush=True)

    candidate_found = bool(best and best["rounded_score_binary64"] > 1e-8)
    output = {
        "status": "positive_uniform_torus_candidate_found" if candidate_found else "no_positive_candidate_in_local_search",
        "complete": True,
        "discovery_only": True,
        "dual_certificate_sha256": pricing.cert_sha,
        "lp_transcript_sha256": pricing.lp_sha,
        "cut_lp_transcript_sha256": pricing.cut_sha,
        "seed_pool_sha256_le_f64": pricing.seed_sha,
        "seed_pool_file_sha256": pricing.seed_file_sha,
        "parameterization": "R(theta)=Q (direct_sum_k [[cos(theta_k),sin(theta_k)],[-sin(theta_k),cos(theta_k)]]) Q^T",
        "phase_dimension": 21,
        "phase_domain": "[-pi,pi]^21 with periodic identification",
        "gradient_method": "cofactor determinant derivative contracted with dR/dtheta_k",
        "gradient_check_coordinates": [0, 10, 20],
        "gradient_check_max_relative_defect": gradient_defect,
        "gradient_checks": checks,
        "regression_checks": pricing.regression,
        "starts": len(starts),
        "max_iterations_per_start": args.maxiter,
        "best_candidate_phases_exact_decimal": best["phases_exact_decimal"] if best else None,
        "best_candidate_score_binary64": best["rounded_score_binary64"] if best else None,
        "candidate_found": candidate_found,
        "records": records,
        "scope": (
            "A positive binary64 score is discovery only. A uniform-ray escape is claimed only after "
            "the independent exact-decimal 128-bit Arb verifier certifies a strictly positive torus "
            "pricing interval. Failure of this finite multi-start search is not a global separation proof."
        ),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "status": output["status"],
        "best_candidate_score_binary64": output["best_candidate_score_binary64"],
        "candidate_found": candidate_found,
        "gradient_check_max_relative_defect": gradient_defect,
        "output": str(output_path),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
