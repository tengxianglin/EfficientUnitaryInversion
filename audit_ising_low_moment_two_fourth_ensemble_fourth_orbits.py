"""Floating full-fourth-orbit audit of the Arb-certified 41-atom ensemble.

This is a diagnostic over all 1,440 D_42 fourth-order orbits. The exact
positive-weight and two-probe claims remain in the independent Arb verifier.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from flint import ctx

from ising_fourth_moments import FourthMoments, orbit_key
from verify_ising_low_moment_design import build_rotation

ROOT = Path(__file__).resolve().parent
CERT = ROOT / "evidence/ising_low_moment_two_fourth_ensemble_n21.json"
OUTPUT = ROOT / "evidence/ising_low_moment_two_fourth_fourth_audit_n21.json"
N = 42


def interval_midpoint(text):
    return float(text.split(" +/- ")[0].strip("[]"))


def main():
    ctx.prec = 192
    raw = CERT.read_bytes()
    cert = json.loads(raw)
    if cert.get("status") != "arb_certified_positive_41_atom_two_fourth_probe_ensemble":
        raise RuntimeError("the exact 41-atom certificate is missing or has wrong status")
    atoms = cert["atoms"]
    weights = np.array([interval_midpoint(x) for x in cert["weights"]], dtype=float)
    if len(atoms) != 41 or len(weights) != 41 or not np.all(weights > 0):
        raise RuntimeError("the frozen exact certificate does not contain 41 positive weights")

    system = FourthMoments(21)
    if len(system.keys) != 1440 or len(system.indices) != 111930:
        raise RuntimeError("unexpected D_42 fourth-orbit enumeration")
    moment = np.zeros(len(system.keys), dtype=float)
    for atom, weight in zip(atoms, weights):
        Rarb = build_rotation(atom)
        R = np.array([[float(Rarb[i, j]) for j in range(N)] for i in range(N)])
        I = system.indices
        values = np.linalg.det(R[I[:, :, None], I[:, None, :]])
        moment += weight * (
            np.bincount(system.ids, weights=values, minlength=len(system.keys))
            / system.counts
        )

    target = np.array([float(x) for x in system.rational_target[21:]], dtype=float)
    residual = moment - target
    relative = np.abs(residual) / np.abs(target)
    order = np.argsort(np.abs(residual))[::-1]
    records = []
    for j in order[:20]:
        records.append({
            "representative": system.representatives[int(j)],
            "canonical_gap_key": list(system.keys[int(j)]),
            "orbit_size": int(system.counts[int(j)]),
            "moment_midpoint": float(moment[j]),
            "target": float(target[j]),
            "residual_midpoint": float(residual[j]),
            "relative_absolute_error": float(relative[j]),
        })

    local_key = orbit_key([0, 1, 2, 3], N)
    distant_key = orbit_key([0, 2, 21, 23], N)
    local_id = system.keys.index(local_key)
    distant_id = system.keys.index(distant_key)
    result = {
        "status": "floating_full_fourth_orbit_diagnostic_not_interval_proof",
        "complete": True,
        "precision_bits_for_rotation_reconstruction": ctx.prec,
        "interval_backend_for_rotation_reconstruction": "python-flint / Arb; midpoint conversion for orbit scan",
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "atom_count": len(atoms),
        "quartet_count": len(system.indices),
        "dihedral_orbit_count": len(system.keys),
        "orbit_size_sum": int(system.counts.sum()),
        "max_absolute_residual_midpoint": float(np.max(np.abs(residual))),
        "max_relative_absolute_error_midpoint": float(np.max(relative)),
        "orbits_with_relative_error_above_one_third": int(np.sum(relative > 1 / 3)),
        "orbits_with_absolute_residual_above_1e-8": int(np.sum(np.abs(residual) > 1e-8)),
        "consecutive_probe": {
            "representative": system.representatives[local_id],
            "residual_midpoint": float(residual[local_id]),
            "target": float(target[local_id]),
        },
        "distant_probe": {
            "representative": system.representatives[distant_id],
            "residual_midpoint": float(residual[distant_id]),
            "target": float(target[distant_id]),
        },
        "top_20_absolute_residuals": records,
        "scope": (
            "All 1,440 fourth-order dihedral orbits were screened using floating "
            "determinants of midpoint rotations and weights. This is a discovery "
            "diagnostic, not an interval certificate. The exact two-probe results "
            "and positivity are established separately by the 384-bit Arb certificate."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "atom_count", "quartet_count", "dihedral_orbit_count",
        "orbit_size_sum", "max_absolute_residual_midpoint",
        "max_relative_absolute_error_midpoint",
        "orbits_with_relative_error_above_one_third",
        "orbits_with_absolute_residual_above_1e-8",
        "consecutive_probe", "distant_probe", "top_20_absolute_residuals"
    )}, indent=2), flush=True)


if __name__ == "__main__":
    main()
