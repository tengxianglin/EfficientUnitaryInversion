#!/usr/bin/env python3
"""Independent exact one-query certificates in (i,b,a,o) order.

No r1 code is imported. Integer identities, not a solver status, certify PSD.
The separate proof supplies the promised-family amplitude/span reductions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np


ORDER = ("i", "b", "a", "o")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sparse(matrix: np.ndarray) -> dict:
    return {"shape": list(matrix.shape), "nonzero": [
        [int(r), int(c), int(matrix[r, c])]
        for r, c in zip(*np.nonzero(matrix))]}


def partial(matrix: np.ndarray, dims: tuple[int, ...], axis: int) -> np.ndarray:
    """Trace one *named position*, retaining the other positions' order."""
    kept = dims[:axis] + dims[axis + 1:]
    n = int(np.prod(kept))
    return np.trace(matrix.reshape(dims + dims), axis1=axis,
                    axis2=axis + len(dims)).reshape(n, n)


def expected_unit(d: int, a: int, b: int, target: str) -> np.ndarray:
    ans = np.zeros((d, d), dtype=np.int64)
    if target == "transpose":
        ans[b, a] = 1
    else:
        if a == b:
            ans += np.eye(d, dtype=np.int64)
        ans[a, b] -= 1
    return ans


def coefficients(d: int, target: str) -> np.ndarray:
    """Construct map column-by-column from E_ab, not an r1 delta formula."""
    out = np.zeros((d,) * 4, dtype=np.int64)
    for a in range(d):
        for b in range(d):
            image = expected_unit(d, a, b, target)
            for i in range(d):
                for o in range(d):
                    out[i, b, a, o] = image[o, i]
    return out


def unit_checks(t: np.ndarray, target: str) -> tuple[bool, list[dict]]:
    d = t.shape[0]
    records = []
    for a in range(d):
        for b in range(d):
            actual = t[:, b, a, :].T.copy()
            expected = expected_unit(d, a, b, target)
            records.append({"a": a, "b": b, "actual": actual.tolist(),
                            "expected": expected.tolist(),
                            "equal": bool(np.array_equal(actual, expected))})
    return all(x["equal"] for x in records), records


def scalar_partial(matrix: np.ndarray, dims: tuple[int, ...], axis: int) -> np.ndarray:
    """Independent scalar-index implementation; does not call np.trace."""
    kept = dims[:axis] + dims[axis+1:]
    size = int(np.prod(kept))
    out = np.zeros((size,size), dtype=np.int64)
    for left in np.ndindex(kept):
        for right in np.ndindex(kept):
            value = 0
            for traced in range(dims[axis]):
                r = left[:axis] + (traced,) + left[axis:]
                c = right[:axis] + (traced,) + right[axis:]
                value += int(matrix[np.ravel_multi_index(r,dims), np.ravel_multi_index(c,dims)])
            out[np.ravel_multi_index(left,kept),np.ravel_multi_index(right,kept)] = value
    return out


def teleportation_coefficient(d: int, target: str) -> np.ndarray:
    """Explicit prepare/Bell-postselect network, numerator of its t/d.

    Memory e=(r,s): preparation creates Bell pair b,r and stores input in s.
    Bell postselection joins query output a to s; r becomes output o.
    Each normalized network factor contributes 1/sqrt(d).
    """
    out = np.zeros((d,)*4,dtype=np.int64)
    J = np.array([[0,1],[-1,0]],dtype=np.int64) if target == "adjugate2" else None
    for i,b,a,o in np.ndindex(out.shape):
        value = 0
        for r,s in np.ndindex((d,d)):
            if J is None:
                prep = int(b == r and s == i)
                post = int(o == r and a == s)
            else:
                # Apply J before the transpose protocol and -J afterwards.
                prep = int(b == r) * int(J[s,i])
                post = -int(J[o,r]) * int(a == s)
            value += prep * post
        out[i,b,a,o] = value
    return out


def certify(d: int, target: str, source: dict) -> dict:
    t = coefficients(d, target)
    v = t.reshape(-1)
    T = np.outer(v, v)
    Q = partial(T, (d,) * 4, ORDER.index("o"))  # remaining i,b,a
    identity3 = np.eye(d ** 3, dtype=np.int64)
    M = d * identity3 - Q
    lift = np.kron(M, np.eye(d, dtype=np.int64))  # i,b,a then o
    D = d * T + lift  # Cdet = D/d^3, success = T/d^2
    units_ok, units = unit_checks(t, target)
    checks = {
        "all_matrix_units": units_ok,
        "Q_symmetric": bool(np.array_equal(Q, Q.T)),
        "Q_squared_equals_d_Q": bool(np.array_equal(Q @ Q, d * Q)),
        "M_symmetric": bool(np.array_equal(M, M.T)),
        "M_squared_equals_d_M": bool(np.array_equal(M @ M, d * M)),
        "Tr_a_Q_equals_I_ib": bool(np.array_equal(partial(Q, (d,) * 3, 2), np.eye(d * d, dtype=np.int64))),
        "Tr_o_D_equals_d_squared_I_iba": bool(np.array_equal(partial(D, (d,) * 4, 3), d * d * identity3)),
        "Tr_b_identity_ib_equals_d_identity_i": bool(np.array_equal(partial(np.eye(d * d, dtype=np.int64), (d, d), 1), d * np.eye(d, dtype=np.int64))),
        "completion_difference_equals_M_tensor_I_o": bool(np.array_equal(D - d * T, lift)),
        "t_norm_squared_equals_d_squared": int(v @ v) == d * d,
        "Tr_Q_squared_equals_d_cubed": int(np.trace(Q @ Q)) == d ** 3,
        "scalar_trace_o_matches_Q": bool(np.array_equal(scalar_partial(T, (d,)*4, 3), Q)),
        "scalar_trace_a_Q_equals_identity": bool(np.array_equal(scalar_partial(Q,(d,)*3,2), np.eye(d*d,dtype=np.int64))),
        "scalar_trace_o_completion": bool(np.array_equal(scalar_partial(D,(d,)*4,3),d*d*identity3)),
        "explicit_teleportation_network_t_over_d": bool(np.array_equal(teleportation_coefficient(d,target), t)),
    }

    # Compare only after constructing all independent matrices and identities.
    old_t = np.zeros(d ** 4, dtype=np.int64)
    for flat, value in source["t_nonzero"]:
        old_t[flat] = value
    old_tensor = old_t.reshape((d,) * 4)  # o,a,b,i
    converted = old_tensor.transpose(3, 2, 1, 0)  # i,b,a,o
    checks["r1_tensor_after_named_axis_conversion"] = bool(np.array_equal(t, converted))
    checks["r1_primal_probability"] = source["primal_p"] == f"1/{d*d}"
    checks["r1_dual_probability"] = source["dual_upper_p"] == f"1/{d*d}"

    # Deliberate oracle input/output swap: normalization alone cannot replace
    # the required matrix-unit check. First off-diagonal image must be wrong.
    wrong = t.swapaxes(1, 2)
    wrong_units_ok, wrong_units = unit_checks(wrong, target)
    wrong_Q = partial(np.outer(wrong.reshape(-1), wrong.reshape(-1)), (d,) * 4, 3)
    wrong_trace_ok = np.array_equal(partial(wrong_Q, (d,) * 3, 2), np.eye(d * d, dtype=np.int64))
    checks["wrong_order_rejected_by_matrix_units"] = not wrong_units_ok
    checks["wrong_order_rejected_by_dual_trace"] = not bool(wrong_trace_ok)

    adjugate = None
    if target == "adjugate2":
        # Store iY as a real integer matrix. Y X^T Y = -(iY) X^T (iY).
        iY = np.array([[0, 1], [-1, 0]], dtype=np.int64)
        adjugate = []
        for a in range(2):
            for b in range(2):
                E = np.zeros((2, 2), dtype=np.int64)
                E[a, b] = 1
                lhs = -iY @ E.T @ iY
                rhs = expected_unit(2, a, b, "adjugate2")
                adjugate.append({"a": a, "b": b, "Y_E_transpose_Y": lhs.tolist(),
                                  "trace_E_I_minus_E": rhs.tolist(),
                                  "equal": bool(np.array_equal(lhs, rhs))})
        checks["Y_X_transpose_Y_equals_adjugate_all_units"] = all(x["equal"] for x in adjugate)

    assert all(checks.values()), checks
    max_value = max(int(np.max(np.abs(x))) for x in (T, Q, M, D))
    return {"dimension": d, "target": target, "status": "exact-finite",
            "tensor_order": list(ORDER), "flattening": "C-order",
            "remaining_Q_order": ["i", "b", "a"],
            "primal_p": f"1/{d*d}", "dual_upper_p": f"1/{d*d}",
            "dual_scalar_numerator": {"Tr_C1": d, "Tr_Q_squared": d**3},
            "denominators": {"success_T": d*d, "Cdet_D": d**3, "C1_identity": d},
            "PSD_reason": "T outer product; real symmetric Q^2=dQ and M^2=dM imply eigenvalues 0,d; completion difference M tensor I_o is PSD",
            "int64_multiplication_safe_bound": d**4 * max_value**2,
            "checks": checks, "matrix_units": units, "adjugate_units": adjugate,
            "t_nonzero": [[int(k), int(v[k])] for k in np.flatnonzero(v)],
            "teleportation_numerator_nonzero": [[int(k),int(x)] for k,x in enumerate(teleportation_coefficient(d,target).reshape(-1)) if x],
            "Q": sparse(Q), "M": sparse(M), "D": sparse(D),
            "wrong_order_negative": {"error": "swap oracle b,a while retaining (i,b,a,o) interpretation",
                "matrix_units_wrong": sum(not x["equal"] for x in wrong_units),
                "first_mismatch": next(x for x in wrong_units if not x["equal"]),
                "Tr_a_Q_equals_identity": bool(wrong_trace_ok)}}


def frequency_controls() -> list[dict]:
    spectra = ([1, -3], [9, -3, -15], [7, -5, -3, 1], [0], [-2, 2], [3, -1])
    records = []
    for values in spectra:
        S = set(values)
        gt = set.intersection(*({nu - lam for nu in S} for lam in S))
        gm = set.intersection(*({nu + lam for nu in S} for lam in S))
        brute_minus = [gamma for gamma in range(2*min(S)-1, 2*max(S)+2)
                       if {gamma-x for x in S} == S]
        assert gt == {0}
        assert sorted(gm) == brute_minus
        records.append({"distinct_spectrum": sorted(S), "Gamma_transpose": sorted(gt),
                        "Gamma_dagger_or_star": sorted(gm),
                        "reflection_enumeration": brute_minus,
                        "amplitude_form": "identically zero" if not gm else "c exp(-it gamma)",
                        "zero_at_origin_forces_zero_on_ray": True})
    assert records[0]["Gamma_dagger_or_star"] == [-2]
    assert records[1]["Gamma_dagger_or_star"] == [-6]
    assert records[2]["Gamma_dagger_or_star"] == []
    return records


def reorder_control() -> dict:
    # The target tensors happen to be invariant under reversing all four axes.
    # A dense asymmetric sentinel is needed to audit the conversion itself.
    old = np.empty((2,) * 4, dtype=np.int64)
    for o, a, b, i in np.ndindex(old.shape):
        old[o, a, b, i] = 1000*o + 100*a + 10*b + i
    new = old.transpose(3, 2, 1, 0)
    rows = []
    for i, b, a, o in np.ndindex(new.shape):
        expected = 1000*o + 100*a + 10*b + i
        assert new[i, b, a, o] == expected
        rows.append({"ibao": [i,b,a,o], "expected": expected,
                     "actual": int(new[i,b,a,o]), "incorrect_unconverted": int(old[i,b,a,o])})
    wrong_count = sum(x["expected"] != x["incorrect_unconverted"] for x in rows)
    assert wrong_count > 0
    return {"sentinel": rows, "incorrect_direct_reinterpretation_mismatches": wrong_count,
            "target_reversal_invariance_warning": "both targets are invariant under reversal; raw t comparison alone would miss this order bug"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dims", nargs="+", type=int, required=True)
    ap.add_argument("--targets", nargs="+", choices=("transpose", "adjugate2"), required=True)
    ap.add_argument("--certificates", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit("fresh output directory required")
    if set(args.dims) - {2,4}:
        raise SystemExit("bounded audit supports only d=2,4")
    started = time.process_time()
    source = json.loads(args.certificates.read_text())
    lookup = {(x["d"], x["target"]): x for x in source["cases"]}
    cases = [certify(d, target, lookup[d, target]) for d in args.dims
             for target in args.targets if target != "adjugate2" or d == 2]
    result = {"schema": "independent-comb-audit-v1", "status": "exact-finite",
              "cases": cases, "frequency_controls": frequency_controls(),
              "order_conversion_control": reorder_control(),
              "source_hashes": {"audit_comb_indices.py": digest(Path(__file__)),
                  "r1/results/comb_certificates.json": digest(args.certificates),
                  "r1/THEORY.md": digest(args.certificates.parent.parent / "THEORY.md"),
                  "proofs/one_query_audit.md": digest(Path(__file__).resolve().parents[1] / "proofs/one_query_audit.md"),
                  "run_bounded.py": digest(Path(__file__).with_name("run_bounded.py"))},
              "environment": {"python": platform.python_version(), "numpy": np.__version__,
                              "solver": "none", "GPU": 0, "seed": None},
              "cpu_seconds": time.process_time()-started,
              "limitations": ["All-parameter physical optimality also requires the separate analytic reduction.",
                  "Finite spectrum controls certify these sets only; the general amplitude lemma is analytic.",
                  "No auxiliary-qubit or known-gate minimum is established."]}
    args.output.mkdir(parents=True)
    with (args.output / "comb_index_audit.json").open("x") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps({"status": result["status"], "cases": len(cases),
                      "all_checks": all(all(x["checks"].values()) for x in cases),
                      "cpu_seconds": result["cpu_seconds"]}))


if __name__ == "__main__":
    main()
